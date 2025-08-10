"""
Configuration file for Smart Resume Matcher
Contains all project settings, API configurations, and database settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Main configuration class"""
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///resume_matcher.db')
    
    # Job Board APIs and URLs
    JUSTJOIN_API_URL = "https://justjoin.it/api/offers"
    ROCKETJOBS_API_URL = "https://rocketjobs.pl/api/jobs"
    
    # Web Scraping Configuration
    SCRAPING_DELAY = 2  # seconds between requests
    MAX_RETRIES = 3
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # AI Model Configuration
    SENTENCE_MODEL = "all-MiniLM-L6-v2"  # Lightweight but effective
    SPACY_MODEL = "en_core_web_sm"
    
    # Matching Algorithm Parameters
    SKILL_WEIGHT = 0.4
    EXPERIENCE_WEIGHT = 0.3
    EDUCATION_WEIGHT = 0.2
    LOCATION_WEIGHT = 0.1
    
    # Thresholds
    MIN_MATCH_SCORE = 0.3
    HIGH_MATCH_THRESHOLD = 0.8
    MEDIUM_MATCH_THRESHOLD = 0.6
    
    # File Upload Configuration
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'resume_matcher.log'
    
    # Cache Configuration
    CACHE_TIMEOUT = 3600  # 1 hour
    
    # API Rate Limiting
    RATE_LIMIT_PER_HOUR = 100
    
    # Supported Job Categories
    JOB_CATEGORIES = [
        'python', 'javascript', 'java', 'data-science', 'machine-learning',
        'frontend', 'backend', 'fullstack', 'devops', 'cybersecurity',
        'mobile', 'ui-ux', 'product-management', 'qa-testing'
    ]
    
    # Skills Dictionary for Enhanced Matching
    SKILLS_MAPPING = {
        'python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy'],
        'javascript': ['javascript', 'js', 'node.js', 'react', 'angular', 'vue'],
        'java': ['java', 'spring', 'hibernate', 'maven'],
        'sql': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis'],
        'aws': ['aws', 'amazon web services', 'ec2', 's3', 'lambda'],
        'docker': ['docker', 'kubernetes', 'containerization'],
        'git': ['git', 'github', 'gitlab', 'version control'],
        'machine_learning': ['ml', 'machine learning', 'tensorflow', 'pytorch', 'scikit-learn'],
        'data_science': ['data science', 'data analysis', 'statistics', 'r']
    }

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Testing environment configuration"""
    DATABASE_URL = 'sqlite:///test_resume_matcher.db'
    TESTING = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 