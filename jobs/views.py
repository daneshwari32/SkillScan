from django.shortcuts import render
import re
import PyPDF2
import docx

# Skill List - 50+ skills
SKILL_DB = [
    'python', 'java', 'javascript', 'react', 'angular', 'vue',
    'django', 'flask', 'node js', 'express',
    'html', 'css', 'bootstrap', 'tailwind',
    'sql', 'mysql', 'postgresql', 'mongodb',
    'machine learning', 'deep learning', 'data science', 'ai',
    'pandas', 'numpy', 'tensorflow', 'pytorch',
    'aws', 'docker', 'kubernetes', 'git', 'github',
    'c++', 'c#', 'php', 'laravel', 'spring boot',
    'rest api', 'graphql', 'linux', 'excel', 'power bi'
]

# Sample Jobs
JOBS = [
    {"title": "Python Developer", "company": "Infosys", "skills": ["python", "django", "sql", "git"], "location": "Bangalore"},
    {"title": "Frontend Developer", "company": "Wipro", "skills": ["javascript", "react", "html", "css"], "location": "Bangalore"},
    {"title": "Data Scientist", "company": "TCS", "skills": ["python", "machine learning", "pandas", "sql"], "location": "Hyderabad"},
    {"title": "Full Stack Developer", "company": "Accenture", "skills": ["python", "react", "node js", "mongodb"], "location": "Pune"},
    {"title": "Java Developer", "company": "Capgemini", "skills": ["java", "spring boot", "sql", "aws"], "location": "Chennai"},
]

def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return " ".join([p.text for p in doc.paragraphs]).lower()

def extract_skills(text):
    found = []
    for skill in SKILL_DB:
        if skill in text:
            found.append(skill)
    return list(set(found))

def home(request):
    return render(request, 'home.html')

def analyze_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        file = request.FILES['resume']
        text = ""
        if file.name.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif file.name.endswith('.docx'):
            text = extract_text_from_docx(file)
        else:
            text = file.read().decode('utf-8', errors='ignore').lower()
        
        user_skills = extract_skills(text)
        
        # Match jobs
        matched_jobs = []
        for job in JOBS:
            match_count = len(set(user_skills) & set(job['skills']))
            if match_count > 0:
                score = int((match_count / len(job['skills'])) * 100)
                matched_jobs.append({**job, "match": score, "matched_skills": list(set(user_skills) & set(job['skills']))})
        
        matched_jobs = sorted(matched_jobs, key=lambda x: x['match'], reverse=True)
        
        return render(request, 'result.html', {
            'skills': user_skills,
            'jobs': matched_jobs,
            'text': text[:500]
        })
    return render(request, 'home.html')