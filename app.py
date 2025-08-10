"""
Main Flask Application for Smart Resume Matcher
Integrates all services and provides web interface
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename

# Import our services
from services.job_scraper import JobScraper
from services.resume_parser import ResumeParser
from services.matching_algorithm import AdvancedMatchingAlgorithm
from database.models import create_database_engine, create_tables, get_session, JobPosting, Resume, JobMatch
from config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
engine = create_database_engine(Config.DATABASE_URL)
create_tables(engine)

# Initialize services
job_scraper = JobScraper()
resume_parser = ResumeParser()
matching_algorithm = AdvancedMatchingAlgorithm()

# Ensure upload directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    """Serve CSS file"""
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def script():
    """Serve JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/data/<path:filename>')
def data_files(filename):
    """Serve data files"""
    return send_from_directory('data', filename)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '2.0'
    })

@app.route('/api/jobs/scrape', methods=['POST'])
def scrape_jobs():
    """Scrape jobs from multiple sources"""
    try:
        data = request.get_json() or {}
        categories = data.get('categories', ['python', 'javascript', 'data-science'])
        limit_per_source = data.get('limit_per_source', 25)
        
        logger.info(f"Scraping jobs for categories: {categories}")
        
        # Scrape jobs from multiple sources
        jobs = job_scraper.scrape_multiple_sources(
            categories=categories,
            limit_per_source=limit_per_source
        )
        
        # Store jobs in database
        session = get_session(engine)
        stored_jobs = []
        
        for job_data in jobs:
            # Check if job already exists
            existing_job = session.query(JobPosting).filter_by(
                title=job_data['title'],
                company=job_data['company'],
                source_url=job_data['source_url']
            ).first()
            
            if not existing_job:
                job = JobPosting(**job_data)
                session.add(job)
                stored_jobs.append(job)
        
        session.commit()
        session.close()
        
        # Get statistics
        stats = job_scraper.get_job_statistics(jobs)
        
        return jsonify({
            'success': True,
            'jobs_scraped': len(jobs),
            'jobs_stored': len(stored_jobs),
            'statistics': stats,
            'message': f'Successfully scraped {len(jobs)} jobs from multiple sources'
        })
        
    except Exception as e:
        logger.error(f"Error scraping jobs: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get jobs from database"""
    try:
        session = get_session(engine)
        
        # Get query parameters
        category = request.args.get('category')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Build query
        query = session.query(JobPosting).filter_by(is_active=True)
        
        if category:
            query = query.filter(JobPosting.category.contains(category))
        
        # Get total count
        total_count = query.count()
        
        # Get paginated results
        jobs = query.offset(offset).limit(limit).all()
        
        # Convert to dictionaries
        jobs_data = [job.to_dict() for job in jobs]
        
        session.close()
        
        return jsonify({
            'success': True,
            'jobs': jobs_data,
            'total_count': total_count,
            'limit': limit,
            'offset': offset
        })
        
    except Exception as e:
        logger.error(f"Error getting jobs: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/resume/upload', methods=['POST'])
def upload_resume():
    """Upload and parse resume file"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed types: {", ".join(Config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
        file.save(file_path)
        
        # Parse resume
        parsed_data = resume_parser.parse_resume_file(file_path)
        
        # Store in database
        session = get_session(engine)
        resume = Resume(
            candidate_name=parsed_data.get('candidate_name'),
            candidate_email=parsed_data.get('candidate_email'),
            candidate_phone=parsed_data.get('candidate_phone'),
            file_path=file_path,
            file_type=parsed_data.get('file_type'),
            raw_text=parsed_data.get('raw_text'),
            summary=parsed_data.get('summary'),
            experience_years=parsed_data.get('experience_years'),
            education_level=parsed_data.get('education_level'),
            skills_extracted=parsed_data.get('skills_extracted'),
            experience_details=parsed_data.get('experience_details'),
            education_details=parsed_data.get('education_details'),
            location=parsed_data.get('location'),
            linkedin_url=parsed_data.get('linkedin_url'),
            github_url=parsed_data.get('github_url'),
            portfolio_url=parsed_data.get('portfolio_url')
        )
        
        session.add(resume)
        session.commit()
        resume_id = resume.id
        session.close()
        
        return jsonify({
            'success': True,
            'resume_id': resume_id,
            'parsed_data': parsed_data,
            'message': 'Resume uploaded and parsed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error uploading resume: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/resume/parse-text', methods=['POST'])
def parse_resume_text():
    """Parse resume from text input"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({
                'success': False,
                'error': 'Empty text provided'
            }), 400
        
        # Parse resume text
        parsed_data = resume_parser.parse_resume_text(text)
        
        # Store in database
        session = get_session(engine)
        resume = Resume(
            candidate_name=parsed_data.get('candidate_name'),
            candidate_email=parsed_data.get('candidate_email'),
            candidate_phone=parsed_data.get('candidate_phone'),
            raw_text=text,
            file_type='text',
            summary=parsed_data.get('summary'),
            experience_years=parsed_data.get('experience_years'),
            education_level=parsed_data.get('education_level'),
            skills_extracted=parsed_data.get('skills_extracted'),
            experience_details=parsed_data.get('experience_details'),
            education_details=parsed_data.get('education_details'),
            location=parsed_data.get('location'),
            linkedin_url=parsed_data.get('linkedin_url'),
            github_url=parsed_data.get('github_url'),
            portfolio_url=parsed_data.get('portfolio_url')
        )
        
        session.add(resume)
        session.commit()
        resume_id = resume.id
        session.close()
        
        return jsonify({
            'success': True,
            'resume_id': resume_id,
            'parsed_data': parsed_data,
            'message': 'Resume text parsed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error parsing resume text: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/match', methods=['POST'])
def match_resume():
    """Match resume against jobs"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        resume_id = data.get('resume_id')
        job_ids = data.get('job_ids', [])
        category = data.get('category')
        limit = data.get('limit', 50)
        
        # Get resume from database
        session = get_session(engine)
        resume = session.query(Resume).filter_by(id=resume_id).first()
        
        if not resume:
            session.close()
            return jsonify({
                'success': False,
                'error': 'Resume not found'
            }), 404
        
        # Get jobs from database
        query = session.query(JobPosting).filter_by(is_active=True)
        
        if job_ids:
            query = query.filter(JobPosting.id.in_(job_ids))
        elif category:
            query = query.filter(JobPosting.category.contains(category))
        
        jobs = query.limit(limit).all()
        jobs_data = [job.to_dict() for job in jobs]
        
        session.close()
        
        # Convert resume to dictionary format
        resume_data = {
            'candidate_name': resume.candidate_name,
            'skills_extracted': resume.skills_extracted or [],
            'experience_years': resume.experience_years or 0,
            'education_level': resume.education_level,
            'location': resume.location,
            'experience_details': resume.experience_details or [],
            'education_details': resume.education_details or []
        }
        
        # Perform matching
        logger.info(f"Matching resume {resume_id} against {len(jobs_data)} jobs")
        matches = matching_algorithm.match_resume_to_jobs(resume_data, jobs_data)
        
        # Store matches in database
        session = get_session(engine)
        stored_matches = []
        
        for match_data in matches:
            # Check if match already exists
            existing_match = session.query(JobMatch).filter_by(
                resume_id=resume_id,
                job_posting_id=match_data['job_id']
            ).first()
            
            if not existing_match:
                match = JobMatch(
                    resume_id=resume_id,
                    job_posting_id=match_data['job_id'],
                    overall_score=match_data['overall_score'],
                    skills_score=match_data['skills_score'],
                    experience_score=match_data['experience_score'],
                    education_score=match_data['education_score'],
                    location_score=match_data['location_score'],
                    matched_skills=match_data['matched_skills'],
                    missing_skills=match_data['missing_skills'],
                    skill_gaps=match_data['skill_gaps'],
                    experience_match=match_data['experience_match'],
                    education_match=match_data['education_match'],
                    recommendations=match_data['recommendations'],
                    confidence_score=match_data['confidence_score'],
                    algorithm_version=match_data['algorithm_version']
                )
                session.add(match)
                stored_matches.append(match)
        
        session.commit()
        session.close()
        
        return jsonify({
            'success': True,
            'resume_id': resume_id,
            'matches': matches,
            'matches_stored': len(stored_matches),
            'message': f'Successfully matched resume against {len(jobs_data)} jobs'
        })
        
    except Exception as e:
        logger.error(f"Error matching resume: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/matches/<int:resume_id>', methods=['GET'])
def get_matches(resume_id):
    """Get matches for a specific resume"""
    try:
        session = get_session(engine)
        
        # Get matches from database
        matches = session.query(JobMatch).filter_by(resume_id=resume_id).all()
        
        # Get job details for each match
        matches_data = []
        for match in matches:
            job = session.query(JobPosting).filter_by(id=match.job_posting_id).first()
            if job:
                match_data = match.to_dict()
                match_data['job_details'] = job.to_dict()
                matches_data.append(match_data)
        
        session.close()
        
        return jsonify({
            'success': True,
            'resume_id': resume_id,
            'matches': matches_data,
            'total_matches': len(matches_data)
        })
        
    except Exception as e:
        logger.error(f"Error getting matches: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    try:
        session = get_session(engine)
        
        # Count records
        total_jobs = session.query(JobPosting).filter_by(is_active=True).count()
        total_resumes = session.query(Resume).filter_by(is_active=True).count()
        total_matches = session.query(JobMatch).count()
        
        # Get recent activity
        recent_jobs = session.query(JobPosting).filter_by(is_active=True).order_by(
            JobPosting.created_at.desc()
        ).limit(5).all()
        
        recent_resumes = session.query(Resume).filter_by(is_active=True).order_by(
            Resume.created_at.desc()
        ).limit(5).all()
        
        session.close()
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_jobs': total_jobs,
                'total_resumes': total_resumes,
                'total_matches': total_matches,
                'recent_jobs': [job.to_dict() for job in recent_jobs],
                'recent_resumes': [resume.to_dict() for resume in recent_resumes]
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    logger.info("Starting Smart Resume Matcher application...")
    logger.info(f"Database URL: {Config.DATABASE_URL}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    ) 