#!/usr/bin/env python3
"""
Setup script for Smart Resume Matcher
Handles installation and initial setup
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def install_spacy_model():
    """Install spaCy model"""
    print("🧠 Installing spaCy model...")
    return run_command("python -m spacy download en_core_web_sm", "Installing spaCy model")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        'uploads',
        'logs',
        'database',
        'services'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def create_env_file():
    """Create .env file with default configuration"""
    print("⚙️ Creating environment configuration...")
    
    env_content = """# Smart Resume Matcher Environment Configuration

# Database Configuration
DATABASE_URL=sqlite:///resume_matcher.db

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True

# Logging Configuration
LOG_LEVEL=INFO

# API Configuration
RATE_LIMIT_PER_HOUR=100
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with default configuration")
    return True

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import flask
        import sqlalchemy
        import spacy
        import sentence_transformers
        import sklearn
        import pandas
        import numpy
        
        print("✅ All required packages imported successfully")
        
        # Test spaCy model
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("This is a test sentence.")
        print("✅ spaCy model loaded successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    print("📊 Creating sample data...")
    
    # Create sample resume
    sample_resume = """John Doe
Software Engineer
john.doe@email.com
+1-555-123-4567
New York, NY

SUMMARY:
Experienced software engineer with 5+ years in full-stack development, specializing in Python, JavaScript, and cloud technologies.

EXPERIENCE:
Senior Software Engineer - TechCorp (2020-2023)
- Developed REST APIs using Python FastAPI and Node.js
- Implemented microservices architecture with Docker and Kubernetes
- Led a team of 4 developers in agile environment

Software Developer - StartupXYZ (2018-2020)
- Built React frontend applications with TypeScript
- Worked with AWS services (EC2, S3, Lambda)
- Implemented CI/CD pipelines with GitHub Actions

EDUCATION:
Bachelor of Science in Computer Science - University of Technology (2018)

SKILLS:
Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes, SQL, MongoDB, Git, Agile, Scrum
"""
    
    with open('sample_resume.txt', 'w') as f:
        f.write(sample_resume)
    
    print("✅ Created sample resume file: sample_resume.txt")
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Start the application:")
    print("   python app.py")
    print("\n2. Open your browser and go to:")
    print("   http://localhost:5000")
    print("\n3. Test the application:")
    print("   - Upload the sample resume (sample_resume.txt)")
    print("   - Try the job matching functionality")
    print("\n4. For development:")
    print("   - Edit .env file to customize configuration")
    print("   - Check logs/resume_matcher.log for debugging")
    print("\n📚 Documentation:")
    print("   - Read PROJECT_DOCUMENTATION.md for detailed information")
    print("   - Check README.md for usage instructions")
    print("\n🔧 API Endpoints:")
    print("   - Health check: http://localhost:5000/api/health")
    print("   - Scrape jobs: POST http://localhost:5000/api/jobs/scrape")
    print("   - Upload resume: POST http://localhost:5000/api/resume/upload")
    print("   - Match resume: POST http://localhost:5000/api/match")
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🚀 Smart Resume Matcher - Setup Script")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check the error messages above.")
        sys.exit(1)
    
    # Install spaCy model
    if not install_spacy_model():
        print("❌ Failed to install spaCy model. Please check the error messages above.")
        sys.exit(1)
    
    # Create environment file
    if not create_env_file():
        sys.exit(1)
    
    # Create sample data
    if not create_sample_data():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed. Please check the error messages above.")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 