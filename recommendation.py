"""
Career Path Recommender
========================
O*NET-based system using Cosine Similarity.

Features used:
  - Skills        (LV scale,  weight = 50%)
  - Interests     (OI scale,  weight = 25%)
  - Work Values   (EX scale,  weight = 15%)
  - Education     (numeric,   weight = 10%)

Requirements:
    pip install pandas scikit-learn openpyxl

Usage:
    python career_recommender.py
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# ── File paths ────────────────────────────────────────────────────────────────
# Update these to point to your O*NET Excel files
DATA_DIR = r"C:\Users\disha\OneDrive\Desktop\rec_project\dataset"   # <-- change this if needed

SKILLS_FILE    = os.path.join(DATA_DIR, "Skills.xlsx")
INTERESTS_FILE = os.path.join(DATA_DIR, "Interests.xlsx")
VALUES_FILE    = os.path.join(DATA_DIR, "Work Values.xlsx")
OCC_FILE       = os.path.join(DATA_DIR, "Occupation Data.xlsx")
EDU_FILE       = os.path.join(DATA_DIR, "Education, Training, and Experience.xlsx")

# ── Weights ───────────────────────────────────────────────────────────────────
W_SKILLS, W_INTERESTS, W_VALUES, W_EDU = 0.50, 0.25, 0.15, 0.10

# ── Education label → numeric level ──────────────────────────────────────────
EDU_MAP = {
    "Less than a High School Diploma"                                         : 1,
    "High School Diploma - or the equivalent (for example, GED)"             : 2,
    "Post-Secondary Certificate"                                              : 3,
    "Some College Courses"                                                    : 3,
    "Associate's Degree (or other 2-year degree)"                            : 4,
    "Bachelor's Degree"                                                       : 5,
    "Post-Baccalaureate Certificate"                                          : 6,
    "Master's Degree"                                                         : 7,
    "Post-Master's Certificate"                                               : 7,
    "First Professional Degree (for example, MD, DDS, LLB, JD)"             : 8,
    "Doctoral Degree"                                                         : 9,
    "Post-Doctoral Training"                                                  : 9,
}

EDU_LABEL_MAP = {
    1: "Less than High School",
    2: "High School / GED",
    3: "Some College / Post-Secondary Certificate",
    4: "Associate's Degree",
    5: "Bachelor's Degree",
    6: "Post-Baccalaureate Certificate",
    7: "Master's Degree",
    8: "Professional Degree (MD, JD, etc.)",
    9: "Doctoral / Post-Doctoral",
}


# ══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING & PREPROCESSING
# ══════════════════════════════════════════════════════════════════════════════

def load_data():
    """Load and return all raw O*NET DataFrames."""
    print("Loading O*NET data files...")
    skills      = pd.read_excel(SKILLS_FILE)
    interests   = pd.read_excel(INTERESTS_FILE)
    values      = pd.read_excel(VALUES_FILE)
    occupations = pd.read_excel(OCC_FILE)
    education   = pd.read_excel(EDU_FILE)
    print(f"  Skills:      {skills.shape[0]:,} rows")
    print(f"  Interests:   {interests.shape[0]:,} rows")
    print(f"  Work Values: {values.shape[0]:,} rows")
    print(f"  Occupations: {occupations.shape[0]:,} rows")
    print(f"  Education:   {education.shape[0]:,} rows")
    return skills, interests, values, occupations, education


def build_occupation_profiles(skills, interests, values, occupations, education):
    """
    Build the master occupation feature matrix.
    Returns:
        occ_profiles  - weighted, normalised DataFrame (occupations × features)
        occ_titles    - {code: title}
        occ_desc      - {code: description}
        col_info      - dict with column name lists per domain
    """
    scaler = MinMaxScaler()

    # ── Filter to correct scales ───────────────────────────────────────────────
    skills_lv    = skills[skills["Scale ID"] == "LV"].copy()
    interests_oi = interests[interests["Scale ID"] == "OI"].copy()
    values_ex    = values[values["Scale ID"] == "EX"].copy()

    # ── Pivot: occupations × feature ──────────────────────────────────────────
    def pivot(df):
        return (
            df.groupby(["O*NET-SOC Code", "Element Name"])["Data Value"]
            .mean()
            .unstack(fill_value=0)
        )

    skills_pivot    = pivot(skills_lv)
    interests_pivot = pivot(interests_oi)
    values_pivot    = pivot(values_ex)

    # ── Education numeric level ────────────────────────────────────────────────
    edu_level = education[education["Element Name"] == "Required Level of Education"].copy()
    edu_level["edu_score"] = edu_level["Category"].map(EDU_MAP)
    edu_pivot = (
        edu_level.groupby("O*NET-SOC Code")["edu_score"]
        .max()
        .rename("edu_level")
        .to_frame()
    )

    # ── Normalise ──────────────────────────────────────────────────────────────
    def norm(df):
        return pd.DataFrame(
            scaler.fit_transform(df),
            index=df.index, columns=df.columns
        )

    skills_norm    = norm(skills_pivot)
    interests_norm = norm(interests_pivot)
    values_norm    = norm(values_pivot)
    edu_norm       = pd.DataFrame(
        scaler.fit_transform(edu_pivot),
        index=edu_pivot.index, columns=edu_pivot.columns
    )

    # ── Align on common occupation index ──────────────────────────────────────
    common_idx = (
        skills_norm.index
        .intersection(interests_norm.index)
        .intersection(values_norm.index)
    )
    skills_norm    = skills_norm.loc[common_idx]
    interests_norm = interests_norm.loc[common_idx]
    values_norm    = values_norm.loc[common_idx]
    edu_norm       = edu_norm.reindex(common_idx).fillna(0)

    # ── Weighted concatenation ─────────────────────────────────────────────────
    occ_profiles = pd.concat([
        skills_norm    * W_SKILLS,
        interests_norm * W_INTERESTS,
        values_norm    * W_VALUES,
        edu_norm       * W_EDU,
    ], axis=1)

    print(f"\nOccupation profile matrix: {occ_profiles.shape[0]} occupations × {occ_profiles.shape[1]} features")

    occ_titles = occupations.set_index("O*NET-SOC Code")["Title"].to_dict()
    occ_desc   = (
        occupations.set_index("O*NET-SOC Code")["Description"].to_dict()
        if "Description" in occupations.columns else {}
    )

    col_info = {
        "skills"    : list(skills_norm.columns),
        "interests" : list(interests_norm.columns),
        "values"    : list(values_norm.columns),
    }

    return occ_profiles, occ_titles, occ_desc, col_info


# ══════════════════════════════════════════════════════════════════════════════
#  RECOMMENDATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def build_user_vector(user_skills, user_interests, user_values,
                      user_edu_level, occ_profiles, col_info):
    """
    Construct a normalised user feature vector aligned with occ_profiles columns.

    Parameters
    ----------
    user_skills     : {skill_name: level 0–7}
    user_interests  : {interest_name: score 0–7}
    user_values     : {value_name: score 0–7}
    user_edu_level  : int 1–9
    """
    sv = pd.Series(0.0, index=col_info["skills"])
    for k, v in user_skills.items():
        if k in sv.index:
            sv[k] = v / 7.0

    iv = pd.Series(0.0, index=col_info["interests"])
    for k, v in user_interests.items():
        if k in iv.index:
            iv[k] = v / 7.0

    vv = pd.Series(0.0, index=col_info["values"])
    for k, v in user_values.items():
        if k in vv.index:
            vv[k] = v / 7.0

    ev = pd.Series({"edu_level": (user_edu_level - 1) / 8.0})

    user_vec = pd.concat([
        sv * W_SKILLS,
        iv * W_INTERESTS,
        vv * W_VALUES,
        ev * W_EDU,
    ])
    user_vec = user_vec.reindex(occ_profiles.columns, fill_value=0)
    return user_vec.values.reshape(1, -1)


def recommend(user_skills, user_interests, user_values, user_edu_level,
              occ_profiles, occ_titles, occ_desc, col_info, top_n=10):
    """Return a DataFrame of the top-N recommended occupations."""
    user_vec = build_user_vector(
        user_skills, user_interests, user_values,
        user_edu_level, occ_profiles, col_info
    )
    sims     = cosine_similarity(user_vec, occ_profiles.values)[0]
    top_idx  = np.argsort(sims)[::-1][:top_n]
    top_codes = occ_profiles.index[top_idx]

    results = pd.DataFrame({
        "Rank"       : range(1, top_n + 1),
        "O*NET Code" : top_codes,
        "Title"      : [occ_titles.get(c, c) for c in top_codes],
        "Match %"    : (sims[top_idx] * 100).round(1),
        "Description": [occ_desc.get(c, "N/A") for c in top_codes],
    })
    return results.reset_index(drop=True)


# ══════════════════════════════════════════════════════════════════════════════
#  CLI INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

def get_int(prompt, lo, hi):
    """Prompt user for an integer in [lo, hi]."""
    while True:
        try:
            val = int(input(prompt).strip())
            if lo <= val <= hi:
                return val
            print(f"  Please enter a number between {lo} and {hi}.")
        except ValueError:
            print("  Invalid input — enter a whole number.")


def cli_input(col_info):
    """Interactive CLI to collect user profile."""
    print("\n" + "═" * 60)
    print("  CAREER PATH RECOMMENDER — Profile Input")
    print("═" * 60)
    print("Rate each item from 1 (low) to 7 (high).\n")

    # ── Skills ────────────────────────────────────────────────────────────────
    print("── SKILLS ──")
    skill_prompts = [
        "Critical Thinking",
        "Mathematics",
        "Programming",
        "Active Listening",
        "Writing",
        "Science",
        "Reading Comprehension",
        "Speaking",
    ]
    # Only prompt for skills that exist in the dataset
    valid_skills = [s for s in skill_prompts if s in col_info["skills"]]
    user_skills = {}
    for s in valid_skills:
        user_skills[s] = get_int(f"  {s} (1-7): ", 1, 7)

    # ── Interests (RIASEC) ────────────────────────────────────────────────────
    print("\n── INTERESTS (RIASEC) ──")
    riasec = ["Realistic", "Investigative", "Artistic", "Social", "Enterprising", "Conventional"]
    valid_interests = [r for r in riasec if r in col_info["interests"]]
    user_interests = {}
    for r in valid_interests:
        user_interests[r] = get_int(f"  {r} (1-7): ", 1, 7)

    # ── Work Values ───────────────────────────────────────────────────────────
    print("\n── WORK VALUES ──")
    value_prompts = ["Achievement", "Independence", "Recognition",
                     "Relationships", "Support", "Working Conditions"]
    valid_values = [v for v in value_prompts if v in col_info["values"]]
    user_values = {}
    for v in valid_values:
        user_values[v] = get_int(f"  {v} (1-7): ", 1, 7)

    # ── Education ─────────────────────────────────────────────────────────────
    print("\n── EDUCATION LEVEL ──")
    for k, label in EDU_LABEL_MAP.items():
        print(f"  {k}. {label}")
    user_edu = get_int("\n  Your education level (1-9): ", 1, 9)

    return user_skills, user_interests, user_values, user_edu


def print_results(results):
    """Pretty-print the recommendation table."""
    print("\n" + "═" * 60)
    print("  TOP CAREER MATCHES")
    print("═" * 60)
    for _, row in results.iterrows():
        print(f"\n  #{int(row['Rank'])}  {row['Title']}  [{row['Match %']}% match]")
        desc = str(row["Description"])
        if desc and desc != "N/A":
            # Wrap description at 55 chars
            words, line = desc.split(), ""
            for w in words:
                if len(line) + len(w) + 1 > 55:
                    print(f"       {line}")
                    line = w
                else:
                    line = f"{line} {w}".strip()
            if line:
                print(f"       {line}")
    print("\n" + "═" * 60)


# ══════════════════════════════════════════════════════════════════════════════
#  QUICK TEST (hardcoded analytical profile — mirrors the notebook)
# ══════════════════════════════════════════════════════════════════════════════

def run_test(occ_profiles, occ_titles, occ_desc, col_info):
    test_skills    = {"Critical Thinking": 7, "Mathematics": 6, "Programming": 5,
                      "Active Listening": 4, "Writing": 4}
    test_interests = {"Investigative": 7, "Conventional": 5, "Enterprising": 3}
    test_values    = {"Achievement": 7, "Independence": 6, "Working Conditions": 4}
    test_edu       = 5  # Bachelor's

    print("\n[TEST MODE] Running with hardcoded analytical profile...")
    results = recommend(test_skills, test_interests, test_values, test_edu,
                        occ_profiles, occ_titles, occ_desc, col_info, top_n=10)
    print_results(results)


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # Load & preprocess
    skills, interests, values, occupations, education = load_data()
    occ_profiles, occ_titles, occ_desc, col_info = build_occupation_profiles(
        skills, interests, values, occupations, education
    )

    print("\nOptions:")
    print("  1. Enter my own profile (interactive)")
    print("  2. Run test with sample analytical profile")
    choice = input("\nChoose (1 or 2): ").strip()

    if choice == "2":
        run_test(occ_profiles, occ_titles, occ_desc, col_info)
    else:
        user_skills, user_interests, user_values, user_edu = cli_input(col_info)
        results = recommend(
            user_skills, user_interests, user_values, user_edu,
            occ_profiles, occ_titles, occ_desc, col_info, top_n=10
        )
        print_results(results)

    # Optionally save to CSV
    save = input("\nSave results to career_results.csv? (y/n): ").strip().lower()
    if save == "y":
        results.to_csv("career_results.csv", index=False)
        print("  Saved → career_results.csv")


if __name__ == "__main__":
    main()