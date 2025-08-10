// Global variables
let jobData = [];
let resumeData = [];
let currentFilter = 'all';

// DOM elements
const uploadOptions = document.querySelectorAll('.upload-option');
const pasteContent = document.getElementById('paste-content');
const uploadContent = document.getElementById('upload-content');
const resumeText = document.getElementById('resume-text');
const fileInput = document.getElementById('file-input');
const browseBtn = document.querySelector('.browse-btn');
const matchBtn = document.getElementById('match-btn');
const resultsSection = document.getElementById('results-section');
const resultsGrid = document.getElementById('results-grid');
const loadingModal = document.getElementById('loading-modal');
const filterBtns = document.querySelectorAll('.filter-btn');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    setupEventListeners();
    setupSmoothScrolling();
});

// Load job and resume data
async function loadData() {
    try {
        const [jobsResponse, resumesResponse] = await Promise.all([
            fetch('data/job_descriptions.json'),
            fetch('data/resumes_clean.json')
        ]);
        
        jobData = await jobsResponse.json();
        resumeData = await resumesResponse.json();
        
        console.log('Data loaded successfully:', {
            jobs: jobData.length,
            resumes: resumeData.length
        });
    } catch (error) {
        console.error('Error loading data:', error);
        showNotification('Error loading data. Please refresh the page.', 'error');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Upload option switching
    uploadOptions.forEach(option => {
        option.addEventListener('click', () => {
            const optionType = option.dataset.option;
            switchUploadOption(optionType);
        });
    });

    // File upload handling
    browseBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileUpload);

    // Match button
    matchBtn.addEventListener('click', handleMatchRequest);

    // Filter buttons
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.dataset.filter;
            applyFilter(filter);
        });
    });

    // Drag and drop for file upload
    const fileUploadArea = document.querySelector('.file-upload-area');
    if (fileUploadArea) {
        fileUploadArea.addEventListener('dragover', handleDragOver);
        fileUploadArea.addEventListener('drop', handleDrop);
    }
}

// Switch between upload options
function switchUploadOption(optionType) {
    uploadOptions.forEach(option => {
        option.classList.remove('active');
        if (option.dataset.option === optionType) {
            option.classList.add('active');
        }
    });

    if (optionType === 'paste') {
        pasteContent.classList.remove('hidden');
        uploadContent.classList.add('hidden');
    } else {
        pasteContent.classList.add('hidden');
        uploadContent.classList.remove('hidden');
    }
}

// Handle file upload
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            resumeText.value = e.target.result;
            showNotification('File uploaded successfully!', 'success');
        };
        reader.readAsText(file);
    }
}

// Handle drag and drop
function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.style.borderColor = '#667eea';
}

function handleDrop(e) {
    e.preventDefault();
    e.currentTarget.style.borderColor = '#e1e5e9';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                resumeText.value = e.target.result;
                showNotification('File uploaded successfully!', 'success');
            };
            reader.readAsText(file);
        } else {
            showNotification('Please upload a text file (.txt)', 'error');
        }
    }
}

// Handle match request
async function handleMatchRequest() {
    const resumeContent = resumeText.value.trim();
    
    if (!resumeContent) {
        showNotification('Please enter your resume content first.', 'error');
        return;
    }

    if (jobData.length === 0) {
        showNotification('Job data not loaded. Please refresh the page.', 'error');
        return;
    }

    showLoadingModal();
    
    try {
        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const matches = analyzeResume(resumeContent);
        displayResults(matches);
        
        hideLoadingModal();
        showNotification('Analysis complete! Check your matches below.', 'success');
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        hideLoadingModal();
        showNotification('Error analyzing resume. Please try again.', 'error');
        console.error('Error:', error);
    }
}

// Analyze resume against job data
function analyzeResume(resumeContent) {
    const resumeSkills = extractSkills(resumeContent);
    const matches = [];

    jobData.forEach(job => {
        const matchScore = calculateMatchScore(resumeSkills, job);
        const matchedSkills = getMatchedSkills(resumeSkills, job.requirements);
        const missingSkills = getMissingSkills(resumeSkills, job.requirements);
        
        matches.push({
            ...job,
            matchScore,
            matchedSkills,
            missingSkills
        });
    });

    // Sort by match score (highest first)
    return matches.sort((a, b) => b.matchScore - a.matchScore);
}

// Extract skills from resume content
function extractSkills(resumeContent) {
    const commonSkills = [
        'Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust',
        'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'FastAPI',
        'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes',
        'AWS', 'Azure', 'GCP', 'Git', 'GitHub', 'CI/CD', 'Jenkins', 'Travis',
        'Machine Learning', 'AI', 'TensorFlow', 'PyTorch', 'Scikit-learn',
        'Data Science', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn',
        'HTML', 'CSS', 'SASS', 'Bootstrap', 'Tailwind', 'TypeScript',
        'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum'
    ];

    const resumeLower = resumeContent.toLowerCase();
    const foundSkills = [];

    commonSkills.forEach(skill => {
        if (resumeLower.includes(skill.toLowerCase())) {
            foundSkills.push(skill);
        }
    });

    return foundSkills;
}

// Calculate match score between resume and job
function calculateMatchScore(resumeSkills, job) {
    const requiredSkills = job.requirements || [];
    const niceToHaveSkills = job.nice_to_have || [];
    
    if (requiredSkills.length === 0) return 0;

    const requiredMatches = requiredSkills.filter(skill => 
        resumeSkills.some(resumeSkill => 
            resumeSkill.toLowerCase().includes(skill.toLowerCase()) ||
            skill.toLowerCase().includes(resumeSkill.toLowerCase())
        )
    ).length;

    const niceToHaveMatches = niceToHaveSkills.filter(skill => 
        resumeSkills.some(resumeSkill => 
            resumeSkill.toLowerCase().includes(skill.toLowerCase()) ||
            skill.toLowerCase().includes(resumeSkill.toLowerCase())
        )
    ).length;

    const requiredScore = (requiredMatches / requiredSkills.length) * 80;
    const niceToHaveScore = (niceToHaveMatches / Math.max(niceToHaveSkills.length, 1)) * 20;
    
    return Math.round(requiredScore + niceToHaveScore);
}

// Get matched skills
function getMatchedSkills(resumeSkills, jobRequirements) {
    return jobRequirements.filter(skill => 
        resumeSkills.some(resumeSkill => 
            resumeSkill.toLowerCase().includes(skill.toLowerCase()) ||
            skill.toLowerCase().includes(resumeSkill.toLowerCase())
        )
    );
}

// Get missing skills
function getMissingSkills(resumeSkills, jobRequirements) {
    return jobRequirements.filter(skill => 
        !resumeSkills.some(resumeSkill => 
            resumeSkill.toLowerCase().includes(skill.toLowerCase()) ||
            skill.toLowerCase().includes(resumeSkill.toLowerCase())
        )
    );
}

// Display results
function displayResults(matches) {
    resultsSection.classList.remove('hidden');
    resultsGrid.innerHTML = '';

    matches.forEach(match => {
        const jobCard = createJobCard(match);
        resultsGrid.appendChild(jobCard);
    });

    // Update filter buttons
    updateFilterCounts(matches);
}

// Create job card element
function createJobCard(match) {
    const card = document.createElement('div');
    card.className = 'job-card';
    card.dataset.matchScore = match.matchScore;

    const matchLevel = getMatchLevel(match.matchScore);
    
    card.innerHTML = `
        <div class="job-header">
            <div>
                <div class="job-title">${match.title}</div>
                <div class="job-company">${match.company}</div>
            </div>
            <div class="match-score ${matchLevel}">${match.matchScore}%</div>
        </div>
        <div class="job-location">
            <i class="fas fa-map-marker-alt"></i> ${match.location}
        </div>
        <div class="job-description">${match.description}</div>
        
        <div class="skills-section">
            <h4>Required Skills</h4>
            <div class="skills-list">
                ${match.requirements.map(skill => 
                    `<span class="skill-tag ${match.matchedSkills.includes(skill) ? 'matched' : 'missing'}">${skill}</span>`
                ).join('')}
            </div>
        </div>
        
        ${match.nice_to_have && match.nice_to_have.length > 0 ? `
            <div class="skills-section">
                <h4>Nice to Have</h4>
                <div class="skills-list">
                    ${match.nice_to_have.map(skill => 
                        `<span class="skill-tag ${match.matchedSkills.includes(skill) ? 'matched' : 'missing'}">${skill}</span>`
                    ).join('')}
                </div>
            </div>
        ` : ''}
        
        <button class="apply-btn" onclick="applyToJob('${match.title}', '${match.company}', '${match.source_url || ''}')">
            <i class="fas fa-external-link-alt"></i> Apply Now
        </button>
    `;

    return card;
}

// Get match level for styling
function getMatchLevel(score) {
    if (score >= 80) return 'high';
    if (score >= 60) return 'medium';
    return 'low';
}

// Apply filter
function applyFilter(filter) {
    currentFilter = filter;
    
    // Update active filter button
    filterBtns.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.filter === filter) {
            btn.classList.add('active');
        }
    });

    // Filter job cards
    const jobCards = document.querySelectorAll('.job-card');
    jobCards.forEach(card => {
        const score = parseInt(card.dataset.matchScore);
        let show = false;

        switch (filter) {
            case 'high':
                show = score >= 80;
                break;
            case 'medium':
                show = score >= 60 && score < 80;
                break;
            case 'low':
                show = score < 60;
                break;
            default:
                show = true;
        }

        card.style.display = show ? 'block' : 'none';
    });
}

// Update filter counts
function updateFilterCounts(matches) {
    const counts = {
        high: matches.filter(m => m.matchScore >= 80).length,
        medium: matches.filter(m => m.matchScore >= 60 && m.matchScore < 80).length,
        low: matches.filter(m => m.matchScore < 60).length
    };

    filterBtns.forEach(btn => {
        const filter = btn.dataset.filter;
        if (filter !== 'all') {
            const count = counts[filter];
            btn.textContent = `${btn.textContent.split('(')[0]} (${count})`;
        }
    });
}

// Apply to job function
function applyToJob(title, company, jobUrl) {
    showNotification(`Redirecting to apply for ${title} at ${company}...`, 'info');
    
    // Use the actual job URL if available, otherwise fallback to job board
    const targetUrl = jobUrl && jobUrl.trim() !== '' ? jobUrl : 'https://justjoin.it';
    
    setTimeout(() => {
        window.open(targetUrl, '_blank');
    }, 1000);
}

// Show loading modal
function showLoadingModal() {
    loadingModal.classList.remove('hidden');
}

// Hide loading modal
function hideLoadingModal() {
    loadingModal.classList.add('hidden');
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 3000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;

    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    // Remove after 4 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 4000);
}

// Get notification icon
function getNotificationIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-circle';
        case 'warning': return 'exclamation-triangle';
        default: return 'info-circle';
    }
}

// Get notification color
function getNotificationColor(type) {
    switch (type) {
        case 'success': return '#28a745';
        case 'error': return '#dc3545';
        case 'warning': return '#ffc107';
        default: return '#667eea';
    }
}

// Setup smooth scrolling for navigation links
function setupSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Add some sample resume content for demonstration
function addSampleResume() {
    const sampleResume = `John Doe
Software Engineer
john.doe@email.com

SUMMARY:
Experienced software engineer with 5+ years in full-stack development, specializing in Python, JavaScript, and cloud technologies. Passionate about building scalable applications and leading development teams.

EXPERIENCE:
Senior Software Engineer - TechCorp (2020-2023)
- Developed REST APIs using Python FastAPI and Node.js
- Implemented microservices architecture with Docker and Kubernetes
- Led a team of 4 developers in agile environment
- Used PostgreSQL, Redis, and MongoDB for data management

Software Developer - StartupXYZ (2018-2020)
- Built React frontend applications with TypeScript
- Worked with AWS services (EC2, S3, Lambda)
- Implemented CI/CD pipelines with GitHub Actions
- Collaborated with data science team on ML projects

SKILLS:
Programming: Python, JavaScript, TypeScript, Java, SQL
Frameworks: FastAPI, React, Node.js, Django, Flask
Databases: PostgreSQL, MongoDB, Redis, MySQL
Cloud: AWS, Docker, Kubernetes, CI/CD
Tools: Git, GitHub, Jenkins, Jira, Agile/Scrum

EDUCATION:
Bachelor of Science in Computer Science
University of Technology, 2018`;

    resumeText.value = sampleResume;
}

// Add a button to load sample resume (for demonstration)
document.addEventListener('DOMContentLoaded', function() {
    const sampleBtn = document.createElement('button');
    sampleBtn.textContent = 'Load Sample Resume';
    sampleBtn.className = 'sample-btn';
    sampleBtn.style.cssText = `
        background: #28a745;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 1rem;
        font-size: 0.9rem;
    `;
    sampleBtn.addEventListener('click', addSampleResume);
    
    const uploadCard = document.querySelector('.upload-card');
    uploadCard.appendChild(sampleBtn);
});

// Add CSS for match score levels
const style = document.createElement('style');
style.textContent = `
    .match-score.high {
        background: linear-gradient(45deg, #28a745, #20c997);
    }
    .match-score.medium {
        background: linear-gradient(45deg, #ffc107, #fd7e14);
    }
    .match-score.low {
        background: linear-gradient(45deg, #dc3545, #e83e8c);
    }
`;
document.head.appendChild(style); 