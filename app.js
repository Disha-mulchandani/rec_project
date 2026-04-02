const config = {
    skills: [
        { id: 's_critical', label: 'Critical Thinking' },
        { id: 's_math', label: 'Mathematics' },
        { id: 's_prog', label: 'Programming' },
        { id: 's_listen', label: 'Active Listening' },
        { id: 's_write', label: 'Writing' },
        { id: 's_science', label: 'Science' },
        { id: 's_read', label: 'Reading Comprehension' },
        { id: 's_speak', label: 'Speaking' }
    ],
    interests: [
        { id: 'i_real', label: 'Realistic (Doers)' },
        { id: 'i_invest', label: 'Investigative (Thinkers)' },
        { id: 'i_art', label: 'Artistic (Creators)' },
        { id: 'i_social', label: 'Social (Helpers)' },
        { id: 'i_enter', label: 'Enterprising (Persuaders)' },
        { id: 'i_conv', label: 'Conventional (Organizers)' }
    ],
    values: [
        { id: 'v_achieve', label: 'Achievement' },
        { id: 'v_indep', label: 'Independence' },
        { id: 'v_recog', label: 'Recognition' },
        { id: 'v_rel', label: 'Relationships' },
        { id: 'v_support', label: 'Support' },
        { id: 'v_cond', label: 'Working Conditions' }
    ]
};

// Mock Career Database for matching logic
const careersDB = [
    { title: "Software Engineer", desc: "Design, develop, and maintain software systems and applications.", scores: { s_prog: 7, s_math: 6, s_critical: 6, i_invest: 6, i_conv: 5, v_indep: 6, v_achieve: 6 } },
    { title: "Data Scientist", desc: "Extract insights from complex data using machine learning and statistics.", scores: { s_math: 7, s_prog: 6, s_science: 6, s_critical: 7, i_invest: 7, v_achieve: 6 } },
    { title: "Registered Nurse", desc: "Provide direct patient care and educate patients about health conditions.", scores: { s_listen: 7, s_science: 5, s_speak: 6, i_social: 7, v_support: 7, v_rel: 7 } },
    { title: "Financial Analyst", desc: "Guide businesses and individuals making investment decisions.", scores: { s_math: 6, s_read: 6, s_write: 5, i_conv: 7, i_enter: 6, v_achieve: 6, v_recog: 6 } },
    { title: "Marketing Manager", desc: "Plan marketing programs and direct ad campaigns to generate interest.", scores: { s_speak: 7, s_write: 6, s_critical: 5, i_enter: 7, i_art: 5, v_recog: 7, v_achieve: 6 } },
    { title: "Graphic Designer", desc: "Create visual concepts to communicate ideas that inspire and captivate consumers.", scores: { s_critical: 5, s_listen: 5, i_art: 7, i_real: 5, v_indep: 6, v_achieve: 5 } },
    { title: "Civil Engineer", desc: "Design and supervise large construction projects and systems.", scores: { s_math: 6, s_science: 6, s_critical: 6, i_real: 7, i_invest: 6, v_cond: 6, v_support: 5 } },
    { title: "High School Teacher", desc: "Instruct secondary school students in specific academic subjects.", scores: { s_speak: 7, s_read: 6, s_listen: 6, s_write: 6, i_social: 7, v_rel: 7, v_support: 6 } },
    { title: "Lawyer", desc: "Advise and represent individuals, businesses, and government agencies on legal issues.", scores: { s_read: 7, s_write: 7, s_speak: 7, s_critical: 7, i_enter: 6, i_invest: 6, v_recog: 7 } },
    { title: "Medical Doctor", desc: "Diagnose and treat injuries or illnesses.", scores: { s_science: 7, s_critical: 7, s_listen: 6, s_read: 7, i_invest: 7, i_social: 6, v_achieve: 7 } },
    { title: "Sales Representative", desc: "Sell goods and services for organizations to businesses or individuals.", scores: { s_speak: 7, s_listen: 6, s_critical: 5, i_enter: 7, i_social: 6, v_indep: 6, v_achieve: 7 } },
    { title: "Writer / Author", desc: "Originate and prepare written material, such as scripts, books, and articles.", scores: { s_write: 7, s_read: 7, s_critical: 6, i_art: 7, i_invest: 5, v_indep: 7, v_achieve: 6 } },
    { title: "Architect", desc: "Plan and design houses, office buildings, and other structures.", scores: { s_math: 5, s_science: 5, s_critical: 6, i_art: 6, i_real: 6, v_achieve: 6, v_indep: 5 } },
    { title: "Accountant", desc: "Prepare and examine financial records to ensure accuracy.", scores: { s_math: 6, s_read: 6, s_write: 5, i_conv: 7, i_invest: 5, v_cond: 7, v_indep: 5 } },
    { title: "Human Resources Manager", desc: "Plan and coordinate the administrative functions of an organization.", scores: { s_speak: 6, s_listen: 7, s_write: 6, i_social: 7, i_conv: 6, v_rel: 7, v_support: 6 } },
    { title: "Mechanic", desc: "Inspect, maintain, and repair vehicles or machinery.", scores: { s_critical: 6, s_scienc: 4, i_real: 7, i_invest: 5, v_indep: 5, v_cond: 5 } },
    { title: "Chef / Head Cook", desc: "Oversee food preparation and direct culinary personnel.", scores: { s_critical: 5, s_speak: 5, i_real: 6, i_art: 6, i_enter: 5, v_achieve: 6, v_cond: 4 } },
    { title: "Psychologist", desc: "Study cognitive, emotional, and social processes and behavior.", scores: { s_listen: 7, s_science: 6, s_critical: 6, s_speak: 6, i_invest: 7, i_social: 7, v_support: 7 } },
    { title: "Event Planner", desc: "Coordinate all aspects of professional meetings and events.", scores: { s_speak: 6, s_listen: 6, s_write: 5, i_enter: 6, i_conv: 6, i_social: 5, v_rel: 6, v_achieve: 5 } },
    { title: "Veterinarian", desc: "Care for the health of animals and work to protect public health.", scores: { s_science: 7, s_math: 5, s_critical: 6, i_invest: 6, i_real: 6, v_achieve: 6, v_support: 6 } }
];

// Combine all fields for easy reference
const allFields = [...config.skills, ...config.interests, ...config.values];

// Generate HTML for ratings
function generateRatingHTML(item) {
    let radios = '';
    for (let i = 1; i <= 7; i++) {
        radios += `
            <label class="rating-option">
                <input type="radio" name="${item.id}" value="${i}" required>
                <div class="rating-circle">${i}</div>
            </label>
        `;
    }
    return `
        <div class="question-item">
            <div class="question-label">${item.label}</div>
            <div class="rating-group">
                ${radios}
            </div>
        </div>
    `;
}

// Initialize Form
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('skills-container').innerHTML = config.skills.map(generateRatingHTML).join('');
    document.getElementById('interests-container').innerHTML = config.interests.map(generateRatingHTML).join('');
    document.getElementById('values-container').innerHTML = config.values.map(generateRatingHTML).join('');

    const form = document.getElementById('career-form');
    const startOverBtn = document.getElementById('start-over-btn');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Button loading state
        const submitBtn = document.getElementById('submit-btn');
        const origContent = submitBtn.innerHTML;
        submitBtn.classList.add('loading');
        submitBtn.innerHTML = '<div class="spinner"></div><span style="display:none">Loading...</span>';
        submitBtn.disabled = true;

        // Simulate short calculation delay for better UX
        setTimeout(() => {
            processRecommendations();
            
            // Reset button and switch views
            submitBtn.classList.remove('loading');
            submitBtn.innerHTML = origContent;
            submitBtn.disabled = false;
            
            toggleView('results-section');
        }, 800);
    });

    startOverBtn.addEventListener('click', () => {
        form.reset();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        toggleView('form-section');
    });
});

function toggleView(viewId) {
    document.querySelectorAll('.view-section').forEach(el => {
        el.classList.remove('active');
        setTimeout(() => el.style.display = 'none', 500); // Wait for transition
    });
    
    setTimeout(() => {
        const target = document.getElementById(viewId);
        target.style.display = 'block';
        // Trigger reflow
        void target.offsetWidth;
        target.classList.add('active');
    }, 500);
}

// Matching Logic Engine
function processRecommendations() {
    // 1. Gather all user ratings
    const userProfile = {};
    const formData = new FormData(document.getElementById('career-form'));
    
    for (let field of allFields) {
        userProfile[field.id] = parseInt(formData.get(field.id)) || 1;
    }
    
    const eduLevel = parseInt(formData.get('education')) || 1;

    // 2. Score each career
    const scoredCareers = careersDB.map(career => {
        let matchScore = calculateMatch(userProfile, career.scores);
        
        // Tweak match score slightly by education constraints (mock logic)
        // If they have high education, boost more complex jobs slightly, etc.
        const requiresHighEdu = career.title.includes("Scientist") || career.title.includes("Doctor") || career.title.includes("Lawyer");
        if (requiresHighEdu && eduLevel < 5) {
            matchScore *= 0.85; // Penalty for low education
        } else if (!requiresHighEdu && eduLevel >= 5) {
            // No strict penalty, but maybe slight normalization
        }

        return {
            ...career,
            matchPercentage: Math.min(Math.max(Math.round(matchScore), 15), 99) // Clamp between 15% and 99%
        };
    });

    // 3. Sort by match percentage
    scoredCareers.sort((a, b) => b.matchPercentage - a.matchPercentage);
    
    // 4. Take top 10 and render
    renderResults(scoredCareers.slice(0, 10));
}

// Calculates Euclidean-style distance converted to percentage
function calculateMatch(userProfile, idealScores) {
    let maxDiff = 0;
    let actualDiff = 0;
    let factorsCount = 0;

    // Weight missing ideal traits differently so that jobs don't all look 99%
    for (let key in userProfile) {
        // If career has an ideal score for this trait, evaluate it heavily
        if (idealScores[key]) {
            const diff = Math.abs(userProfile[key] - idealScores[key]);
            actualDiff += diff * 2; // Weight primary traits twice
            maxDiff += 6 * 2; // Max diff is 6 (7-1)
            factorsCount += 2;
        } else {
            // General background traits: if user has high score but job doesn't need it
            // Small penalty if it's vastly different, to diversify results.
            const genericIdeal = 4; // Assume jobs prefer average if unspecified
            const diff = Math.abs(userProfile[key] - genericIdeal);
            actualDiff += diff * 0.5;
            maxDiff += 6 * 0.5;
            factorsCount += 0.5;
        }
    }

    // Convert diff to similarity percentage
    const similarity = 1 - (actualDiff / maxDiff);
    
    // Base line scale from ~40% to 100% to look realistic
    return (similarity * 100 * 0.6) + 40;
}

function renderResults(topCareers) {
    const container = document.getElementById('results-container');
    container.innerHTML = '';
    
    topCareers.forEach((job, index) => {
        const rank = index + 1;
        
        // Staggered animation delay
        const animDelay = index * 0.1;
        let rankClass = rank <= 3 ? `rank-${rank}` : '';
        let badgeColor = rank === 1 ? 'var(--accent-primary)' : 'rgba(255,255,255,0.1)';
        
        const cardHTML = `
            <div class="result-card" style="animation-delay: ${animDelay}s">
                <div class="card-header">
                    <h3 class="job-title">${job.title}</h3>
                    <span class="rank-badge ${rankClass}">#${rank}</span>
                </div>
                
                <div class="match-container">
                    <div class="match-header">
                        <span>Match Score</span>
                        <span class="match-score">${job.matchPercentage}%</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" style="width: 0%;" data-target="${job.matchPercentage}%"></div>
                    </div>
                </div>
                
                <p class="job-desc">${job.desc}</p>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', cardHTML);
    });

    // Trigger progress bar animations after cards are rendered
    setTimeout(() => {
        document.querySelectorAll('.progress-bar-fill').forEach(bar => {
            bar.style.width = bar.getAttribute('data-target');
        });
    }, 600); // slightly after section transition
}
