import re
from collections import Counter


def extract_skills(text):

    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    words = text.split()

    skill_keywords = {

        # Programming
        "python","java","c","c++","c#","go","golang","rust","scala","kotlin","swift","r",

        # Web Development
        "html","css","javascript","typescript","react","angular","vue","node","nodejs",
        "express","nextjs","bootstrap","tailwind","jquery",

        # Backend
        "django","flask","spring","springboot","fastapi","laravel","rails",

        # Databases
        "sql","mysql","postgresql","sqlite","oracle","mongodb","cassandra",
        "redis","dynamodb","neo4j",

        # Data Science
        "pandas","numpy","matplotlib","seaborn","scipy","statsmodels",

        # Machine Learning
        "machine","learning","scikit","scikit-learn","xgboost","lightgbm",

        # Deep Learning
        "tensorflow","pytorch","keras","cnn","rnn","lstm","gan",

        # AI Fields
        "nlp","computer","vision","transformers","bert","gpt",

        # Big Data
        "hadoop","spark","hive","pig","kafka","flink",

        # Cloud
        "aws","azure","gcp","lambda","ec2","s3","cloud",

        # DevOps
        "docker","kubernetes","jenkins","ansible","terraform","ci","cd",

        # Version Control
        "git","github","gitlab","bitbucket",

        # OS
        "linux","unix","shell","bash",

        # Analytics
        "excel","powerbi","tableau","analytics","data","analysis",

        # Cybersecurity
        "penetration","testing","cryptography","security","hacking",

        # Mobile
        "android","ios","flutter","reactnative",

        # Software Engineering
        "oop","microservices","rest","api","graphql",

        # Testing
        "selenium","pytest","junit","testng","cypress",

        # Tools
        "jira","postman","figma","dockerhub",

        # Math / Stats
        "statistics","probability","linear","algebra","calculus",

        # Data Engineering
        "etl","airflow","databricks","snowflake"
    }

    detected_skills = []

    for word in words:
        if word in skill_keywords:
            detected_skills.append(word)

    return Counter(detected_skills)


def compare_roles(role1_skills, role2_skills):

    set1 = set(role1_skills)
    set2 = set(role2_skills)

    common = list(set1.intersection(set2))
    unique_role1 = list(set1.difference(set2))
    unique_role2 = list(set2.difference(set1))

    return {
        "common_skills": common,
        "role1_unique": unique_role1,
        "role2_unique": unique_role2
    }

def calculate_skill_gap(user_skills, role_skills):

    user_set = set([skill.strip().lower() for skill in user_skills])
    role_set = set([skill.lower() for skill in role_skills])

    common = user_set.intersection(role_set)
    missing = role_set.difference(user_set)

    if len(role_set) == 0:
        score = 0
    else:
        score = int((len(common) / len(role_set)) * 100)

    return score, list(common), list(missing)

def generate_learning_roadmap(missing_skills):

    skill_guidance = {

        # Programming
        "python": "Practice Python with data analysis and automation projects",
        "java": "Build backend applications using Java and Spring Boot",
        "c": "Learn memory management and system programming",
        "c++": "Practice algorithms and object-oriented programming",

        # Data Science
        "pandas": "Learn data manipulation using Pandas with real datasets",
        "numpy": "Understand numerical computing and array operations",
        "matplotlib": "Practice data visualization using Matplotlib",
        "seaborn": "Create statistical plots using Seaborn",

        # Machine Learning
        "machine": "Study machine learning fundamentals and algorithms",
        "learning": "Practice supervised and unsupervised learning techniques",
        "scikit": "Use Scikit-learn to build ML models",

        # Deep Learning
        "tensorflow": "Build neural networks and deep learning models",
        "pytorch": "Learn PyTorch for deep learning research and projects",

        # AI Fields
        "nlp": "Learn Natural Language Processing using HuggingFace",
        "computer": "Study Computer Vision fundamentals",
        "vision": "Practice image classification and CNN models",

        # Web Development
        "html": "Learn webpage structure and semantic HTML",
        "css": "Practice responsive design and layout techniques",
        "javascript": "Build interactive web pages and browser apps",
        "react": "Build modern frontend apps using React",
        "node": "Develop backend APIs using NodeJS",

        # Backend
        "django": "Build full stack web apps using Django",
        "flask": "Create lightweight Python web APIs",

        # Databases
        "sql": "Practice complex queries, joins, and database design",
        "mongodb": "Learn NoSQL database operations",

        # Cloud
        "aws": "Learn cloud deployment and EC2/S3 services",
        "azure": "Practice deploying apps using Microsoft Azure",
        "gcp": "Understand Google Cloud AI services",

        # DevOps
        "docker": "Learn containerization and deployment",
        "kubernetes": "Study container orchestration systems",
        "jenkins": "Automate CI/CD pipelines using Jenkins",

        # Big Data
        "spark": "Learn distributed data processing using Apache Spark",
        "hadoop": "Understand HDFS and big data storage systems",

        # Analytics
        "excel": "Practice data analysis using Excel formulas and pivot tables",
        "tableau": "Create dashboards and business reports",
        "powerbi": "Build interactive BI dashboards",

        # Data Engineering
        "etl": "Learn ETL pipelines for data integration",
        "airflow": "Automate data workflows using Apache Airflow",

        # Software Engineering
        "oop": "Understand object oriented programming principles",
        "microservices": "Design scalable distributed systems",
        "api": "Learn REST API design and implementation",

        # Testing
        "selenium": "Automate browser testing using Selenium",
        "pytest": "Write Python unit tests using PyTest",

        # Tools
        "git": "Practice version control using Git and GitHub",
        "github": "Collaborate on projects using GitHub workflows",

        # Statistics
        "statistics": "Learn statistical analysis for data science",
        "probability": "Understand probability theory for ML"
    }



    roadmap = []

    for skill in missing_skills:

        if skill in skill_guidance:

            roadmap.append(
                f"Learn {skill} → {skill_guidance[skill]}"
            )

        else:

            roadmap.append(
                f"Learn {skill} through online courses and practical projects"
            )

    return roadmap

def generate_resume_suggestions(resume_skills, role_skills):

    resume_set = set([s.lower() for s in resume_skills])
    role_set = set([s.lower() for s in role_skills])

    missing = role_set - resume_set

    suggestions = []

    for skill in list(missing)[:10]:
        suggestions.append(f"Add projects or experience related to {skill}")

    general_tips = [
        "Use strong action verbs (developed, built, designed)",
        "Add measurable results (e.g., improved accuracy by 20%)",
        "Include real-world projects",
        "Keep resume concise (1 page)",
        "Highlight relevant technical skills clearly"
    ]

    return suggestions, general_tips