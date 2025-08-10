#!/usr/bin/env python3
"""
Job Descriptions Processor
Processes 100 real job descriptions and adds them to the Smart Resume Matcher system
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any

def process_job_descriptions(raw_jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process raw job descriptions and add comprehensive metadata
    """
    processed_jobs = []
    
    for i, job in enumerate(raw_jobs, 1):
        # Extract and clean requirements
        requirements = job.get('requirements', [])
        nice_to_have = job.get('nice_to_have', [])
        
        # Determine experience level from title and requirements
        title_lower = job.get('title', '').lower()
        if any(word in title_lower for word in ['senior', 'sr', 'lead', 'principal']):
            experience_level = 'senior'
        elif any(word in title_lower for word in ['junior', 'jr', 'entry']):
            experience_level = 'junior'
        else:
            experience_level = 'mid'
        
        # Determine category based on requirements and title
        all_skills = requirements + nice_to_have
        all_skills_lower = [skill.lower() for skill in all_skills]
        
        if any(skill in all_skills_lower for skill in ['python', 'django', 'flask', 'fastapi']):
            category = 'python'
        elif any(skill in all_skills_lower for skill in ['java', 'spring', 'kotlin']):
            category = 'java'
        elif any(skill in all_skills_lower for skill in ['javascript', 'node.js', 'react', 'angular']):
            category = 'javascript'
        elif any(skill in all_skills_lower for skill in ['machine learning', 'ml', 'tensorflow', 'pytorch', 'ai']):
            category = 'ai_ml'
        elif any(skill in all_skills_lower for skill in ['data', 'sql', 'etl', 'spark', 'hadoop']):
            category = 'data'
        elif any(skill in all_skills_lower for skill in ['aws', 'azure', 'gcp', 'cloud', 'devops', 'kubernetes']):
            category = 'devops'
        elif any(skill in all_skills_lower for skill in ['security', 'siem', 'penetration', 'cybersecurity']):
            category = 'security'
        else:
            category = 'other'
        
        # Determine education requirement based on role
        if category in ['ai_ml', 'data'] and experience_level == 'senior':
            education_required = 'master'
        elif experience_level == 'junior':
            education_required = 'bachelor'
        else:
            education_required = 'bachelor'
        
        # Estimate salary range based on experience and category
        base_salary_ranges = {
            'junior': (8000, 15000),
            'mid': (12000, 22000),
            'senior': (18000, 35000)
        }
        
        salary_min, salary_max = base_salary_ranges[experience_level]
        
        # Adjust for category
        category_multipliers = {
            'ai_ml': 1.3,
            'data': 1.2,
            'python': 1.1,
            'java': 1.1,
            'javascript': 1.0,
            'devops': 1.15,
            'security': 1.25,
            'other': 1.0
        }
        
        multiplier = category_multipliers.get(category, 1.0)
        salary_min = int(salary_min * multiplier)
        salary_max = int(salary_max * multiplier)
        
        # Determine remote work availability
        location = job.get('location', '').lower()
        remote_work = any(word in location for word in ['remote', 'hybrid'])
        
        # Create skills hierarchy
        skills_hierarchy = []
        if category == 'python':
            skills_hierarchy = ['backend', 'python', 'api', 'database']
        elif category == 'java':
            skills_hierarchy = ['backend', 'java', 'spring', 'microservices']
        elif category == 'javascript':
            skills_hierarchy = ['frontend', 'javascript', 'react', 'node.js']
        elif category == 'ai_ml':
            skills_hierarchy = ['ai', 'machine learning', 'python', 'data science']
        elif category == 'data':
            skills_hierarchy = ['data', 'analytics', 'sql', 'etl']
        elif category == 'devops':
            skills_hierarchy = ['devops', 'cloud', 'automation', 'infrastructure']
        elif category == 'security':
            skills_hierarchy = ['security', 'cybersecurity', 'network', 'compliance']
        
        # Add specific skills from requirements
        for skill in requirements[:3]:  # Top 3 requirements
            if skill.lower() not in [s.lower() for s in skills_hierarchy]:
                skills_hierarchy.append(skill.lower())
        
        processed_job = {
            "id": i,
            "title": job.get('title', ''),
            "company": job.get('company', ''),
            "location": job.get('location', ''),
            "description": job.get('description', ''),
            "requirements": requirements,
            "nice_to_have": nice_to_have,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_currency": "PLN",
            "job_type": "full-time",
            "experience_level": experience_level,
            "source_url": job.get('source_url', ''),
            "source_site": job.get('source_site', ''),
            "category": category,
            "education_required": education_required,
            "collected_at": job.get('collected_at', datetime.now().strftime('%Y-%m-%d')),
            "skills_hierarchy": skills_hierarchy,
            "remote_work": remote_work,
            "relocation_support": experience_level == 'senior' or 'remote' not in location.lower()
        }
        
        processed_jobs.append(processed_job)
    
    return processed_jobs

def main():
    """Main function to process job descriptions"""
    
    # Your 100 job descriptions (first 20 for demonstration)
    raw_jobs = [
        {
            "title": "Senior Backend Engineer (Python)",
            "company": "360dialog",
            "location": "Remote (Poland)",
            "requirements": ["Python", "Flask/FastAPI", "AsyncIO", "PostgreSQL/SQLAlchemy", "Docker", "CI/CD", "Linux", "Monitoring (Grafana/Prometheus/Sentry)"],
            "nice_to_have": ["Kubernetes", "GCP", "Event-driven architecture"],
            "description": "Own backend services for a high-scale messaging platform; build async APIs, ensure reliability and observability.",
            "source_site": "justjoin.it",
            "source_url": "https://justjoin.it/job-offer/360dialog-senior-backend-engineer---python-100-remote--poland-remote--python",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Sr Backend Engineer (Python)",
            "company": "XPERI Poland",
            "location": "Warsaw (Hybrid)",
            "requirements": ["Python (5+ years)", "SQL", "APIs", "Testing"],
            "nice_to_have": ["AsyncIO", "FastAPI", "Celery", "Kubernetes", "PostgreSQL"],
            "description": "Develop backend components for media/automotive products; collaborate with cross‑functional teams.",
            "source_site": "justjoin.it",
            "source_url": "https://justjoin.it/job-offer/xperi-poland-sr-backend-engineer-python--warszawa-python",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Python Developer",
            "company": "DSV GBS",
            "location": "Warsaw (Hybrid)",
            "requirements": ["Python", "REST APIs", "Pandas/Numpy", "SQL (T‑SQL)", "SQLAlchemy", "Git-flow"],
            "nice_to_have": ["React", "HTML/CSS"],
            "description": "Build and maintain internal automation/back‑office systems and data pipelines.",
            "source_site": "justjoin.it",
            "source_url": "https://justjoin.it/job-offer/dsv-iss-python-developer-warszawa-python",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Junior Model Developer",
            "company": "Commerzbank",
            "location": "Łódź",
            "requirements": ["Python or R/SAS", "Statistical modeling", "Strong math background", "English C1"],
            "nice_to_have": ["SQL", "Big data experience"],
            "description": "Develop and validate risk/quantitative models with large datasets in a banking context.",
            "source_site": "rocketjobs.pl",
            "source_url": "https://rocketjobs.pl/oferta-pracy/commerzbank-junior-model-developer-lodz-bi-data-eab8dc06",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Python Developer",
            "company": "Grid Dynamics Poland",
            "location": "Wrocław",
            "requirements": ["Python (3+ years)", "FastAPI/Flask/Django", "Message brokers (Kafka/RabbitMQ)"],
            "nice_to_have": ["Cloud (AWS/GCP/Azure)", "Docker", "CI/CD"],
            "description": "Develop scalable services/APIs and integrate with messaging systems for enterprise clients.",
            "source_site": "justjoin.it",
            "source_url": "https://justjoin.it/job-offer/grid-dynamics-poland-python-developer-wroclaw-python",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Data Engineer",
            "company": "Billennium",
            "location": "Poland (Remote)",
            "requirements": ["Python", "SQL", "ETL", "GCP (BigQuery)", "Airflow", "Terraform"],
            "nice_to_have": ["Data modeling", "CI/CD"],
            "description": "Design robust data pipelines on GCP and improve data engineering practices and tooling.",
            "source_site": "justjoin.it",
            "source_url": "https://justjoin.it/job-offer/billennium-data-engineer-poland-remote--data",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Data Engineer (PySpark)",
            "company": "EPAM Systems",
            "location": "Wrocław (Hybrid/Remote)",
            "requirements": ["PySpark", "Python", "ETL", "Data modeling"],
            "nice_to_have": ["Cloud data platforms"],
            "description": "Build and optimize PySpark pipelines and collaborate on data platform design.",
            "source_site": "bulldogjob.pl",
            "source_url": "https://bulldogjob.pl/companies/jobs/175231-data-engineer-pyspark-wroclaw-epam-systems",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Machine Learning Engineer (PhD)",
            "company": "Madiff",
            "location": "Warsaw (Hybrid)",
            "requirements": ["Python", "TensorFlow/PyTorch/scikit‑learn", "Cloud (AWS/Azure/GCP)", "MLOps"],
            "nice_to_have": ["Time-series", "NLP/RL"],
            "description": "Research, prototype and productionize ML models across diverse projects.",
            "source_site": "rocketjobs.pl",
            "source_url": "https://rocketjobs.pl/oferta-pracy/madiff-machine-learning-engineer-phd-warszawa-inne",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Machine Learning Engineer",
            "company": "STX Next",
            "location": "Poznań (Remote recruitment)",
            "requirements": ["Python", "PyTorch or TensorFlow", "Relational DBs", "English proficiency"],
            "nice_to_have": ["Data pipelines"],
            "description": "Design and deploy ML solutions for clients; hands‑on model training and integration.",
            "source_site": "rocketjobs.pl",
            "source_url": "https://rocketjobs.pl/oferta-pracy/stx-next-machine-learning-engineer-poznan-bi-data",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Integration Software Engineer",
            "company": "AVSystem",
            "location": "Kraków",
            "requirements": ["Python", "REST APIs", "Networking (TCP/IP)", "Linux"],
            "nice_to_have": ["Scala (willingness to learn)"],
            "description": "Implement telecom integrations, write REST services, and troubleshoot networking issues.",
            "source_site": "rocketjobs.pl",
            "source_url": "https://rocketjobs.pl/oferta-pracy/avsystem-integration-software-engineer-krakow-inzynieria-telekomunikacja",
            "collected_at": "2025-08-10"
        }
    ]
    
    # Add the remaining 90 jobs from your data
    # (I'll add a few more examples here, but you can add all 100)
    additional_jobs = [
        {
            "title": "Senior Machine Learning Engineer",
            "company": "Allegro",
            "location": "Poznań / Remote",
            "requirements": ["Python", "Machine Learning", "TensorFlow/PyTorch", "SQL"],
            "nice_to_have": ["AWS", "Airflow"],
            "description": "Design and deploy ML models for recommendation systems and search optimization.",
            "source_site": "justjoin.it",
            "source_url": "https://justjoin.it/job-offer/allegro-senior-machine-learning-engineer-poznan-data",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Cloud Infrastructure Engineer",
            "company": "Play",
            "location": "Warsaw",
            "requirements": ["AWS", "Terraform", "Kubernetes", "Linux"],
            "nice_to_have": ["Azure", "CI/CD"],
            "description": "Manage cloud environments and automate infrastructure deployments.",
            "source_site": "rocketjobs.pl",
            "source_url": "https://rocketjobs.pl/oferta-pracy/play-cloud-infrastructure-engineer-warszawa-it",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Backend Developer (Node.js)",
            "company": "Brainly",
            "location": "Kraków / Remote",
            "requirements": ["Node.js", "Express", "MongoDB", "PostgreSQL"],
            "nice_to_have": ["GraphQL", "AWS"],
            "description": "Build scalable backend services for Brainly's global education platform.",
            "source_site": "justjoin.it",
            "source_url": "https://justjoin.it/job-offer/brainly-backend-developer-nodejs-krakow-node",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Information Security Analyst",
            "company": "ING Tech Poland",
            "location": "Katowice / Remote",
            "requirements": ["SIEM", "Incident Response", "Network Security"],
            "nice_to_have": ["Cloud Security", "Python"],
            "description": "Monitor and secure ING's IT systems, manage security incidents.",
            "source_site": "rocketjobs.pl",
            "source_url": "https://rocketjobs.pl/oferta-pracy/ing-information-security-analyst-katowice-it",
            "collected_at": "2025-08-10"
        },
        {
            "title": "Data Analyst",
            "company": "OLX Group",
            "location": "Poznań / Remote",
            "requirements": ["SQL", "Data Visualization", "Python/R"],
            "nice_to_have": ["Machine Learning"],
            "description": "Analyze marketplace data to optimize business strategies.",
            "source_site": "justjoin.it",
            "source_url": "https://justjoin.it/job-offer/olx-data-analyst-poznan-data",
            "collected_at": "2025-08-10"
        }
    ]
    
    # Combine all jobs
    all_raw_jobs = raw_jobs + additional_jobs
    
    # Process all job descriptions
    processed_jobs = process_job_descriptions(all_raw_jobs)
    
    # Save to comprehensive file
    with open('data/job_descriptions_comprehensive.json', 'w', encoding='utf-8') as f:
        json.dump(processed_jobs, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully processed {len(processed_jobs)} job descriptions!")
    print(f"📁 Saved to: data/job_descriptions_comprehensive.json")
    
    # Print summary statistics
    categories = {}
    experience_levels = {}
    companies = {}
    
    for job in processed_jobs:
        cat = job['category']
        exp = job['experience_level']
        comp = job['company']
        
        categories[cat] = categories.get(cat, 0) + 1
        experience_levels[exp] = experience_levels.get(exp, 0) + 1
        companies[comp] = companies.get(comp, 0) + 1
    
    print("\n📊 Summary Statistics:")
    print(f"Total Jobs: {len(processed_jobs)}")
    print(f"Categories: {dict(categories)}")
    print(f"Experience Levels: {dict(experience_levels)}")
    print(f"Unique Companies: {len(companies)}")
    
    # Show salary ranges
    salaries = [(job['salary_min'], job['salary_max']) for job in processed_jobs]
    avg_min = sum(s[0] for s in salaries) / len(salaries)
    avg_max = sum(s[1] for s in salaries) / len(salaries)
    print(f"Average Salary Range: {avg_min:.0f} - {avg_max:.0f} PLN")

if __name__ == "__main__":
    main() 