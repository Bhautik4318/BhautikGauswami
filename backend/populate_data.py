import os
import django
from datetime import date

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
django.setup()

from portfolio.models import Project, Skill, PersonalInfo, SkillCategory, ProjectCategory
from django.contrib.auth.models import User

def populate_data():
    print("Starting data population with Bhautik's information...")
    
    # Create PersonalInfo entry with Bhautik's details
    personal_info, created = PersonalInfo.objects.get_or_create(
        id=1,
        defaults={
            'name': 'Bhautik Gauswami',
            'title': 'Machine Learning Engineer & AI Architect',
            'bio': '''I'm a passionate Machine Learning Engineer and AI Architect with expertise in building intelligent systems that solve real-world problems. Currently pursuing B.Tech in Information Technology at Sarvajanik College of Engineering & Technology, Surat. I specialize in Python, Machine Learning, Artificial Intelligence, and Data Analytics, with extensive experience working with AI Agents like ChatGPT, Copilot, Gemini, and Deepseek. My focus is on creating innovative solutions that bridge the gap between cutting-edge AI technology and practical applications.''',
            'email': 'Bhautikgosai4318@gmail.com',
            'phone': '8141415113',
            'city': 'Surat',
            'state': 'Gujarat',
            'country': 'India',
            'postal_code': '395005',
            'linkedin_url': 'https://linkedin.com/in/bhautik-gauswami',
            'github_url': 'https://github.com/Bhautikgauswami33',
            'skills_summary': '🧠 Machine Learning | � AI Architect | � Data Analytics | 🐍 Python Expert'
        }
    )
    print(f"Personal info {'created' if created else 'updated'}")
    
    # Create Skill Categories
    skill_categories_data = [
        {'name': 'Machine Learning & AI', 'slug': 'ml-ai', 'color': '#00f6ff', 'icon': '🧠', 'display_order': 1},
        {'name': 'Programming Languages', 'slug': 'programming', 'color': '#1effc6', 'icon': '💻', 'display_order': 2},
        {'name': 'Web Development', 'slug': 'web-dev', 'color': '#b97aff', 'icon': '🌐', 'display_order': 3},
        {'name': 'Data & Analytics', 'slug': 'data-analytics', 'color': '#ff6b6b', 'icon': '📊', 'display_order': 4},
        {'name': 'AI Agents & Tools', 'slug': 'ai-tools', 'color': '#4ecdc4', 'icon': '🤖', 'display_order': 5},
        {'name': 'Leadership & Soft Skills', 'slug': 'soft-skills', 'color': '#ffe66d', 'icon': '👥', 'display_order': 6},
    ]
    
    for category_data in skill_categories_data:
        category, created = SkillCategory.objects.get_or_create(
            slug=category_data['slug'],
            defaults=category_data
        )
        if created:
            print(f"Created skill category: {category.name}")
    
    # Get categories for skill creation
    ml_ai_cat = SkillCategory.objects.get(slug='ml-ai')
    programming_cat = SkillCategory.objects.get(slug='programming')
    web_dev_cat = SkillCategory.objects.get(slug='web-dev')
    data_cat = SkillCategory.objects.get(slug='data-analytics')
    ai_tools_cat = SkillCategory.objects.get(slug='ai-tools')
    soft_skills_cat = SkillCategory.objects.get(slug='soft-skills')
    
    # Create Skills based on Bhautik's profile
    skills_data = [
        # Machine Learning & AI
        {'name': 'Python', 'level': 95, 'category': programming_cat, 'icon': '🐍', 'years_of_experience': 4, 'is_featured': True},
        {'name': 'Machine Learning', 'level': 90, 'category': ml_ai_cat, 'icon': '🧠', 'years_of_experience': 3, 'is_featured': True},
        {'name': 'Artificial Intelligence', 'level': 88, 'category': ml_ai_cat, 'icon': '🤖', 'years_of_experience': 3, 'is_featured': True},
        {'name': 'Data Analytics', 'level': 92, 'category': data_cat, 'icon': '📊', 'years_of_experience': 3, 'is_featured': True},
        {'name': 'Data Visualization', 'level': 85, 'category': data_cat, 'icon': '📈', 'years_of_experience': 2, 'is_featured': True},
        
        # AI Agents & Tools
        {'name': 'ChatGPT', 'level': 95, 'category': ai_tools_cat, 'icon': '💬', 'years_of_experience': 2, 'is_featured': True},
        {'name': 'GitHub Copilot', 'level': 90, 'category': ai_tools_cat, 'icon': '�', 'years_of_experience': 2, 'is_featured': True},
        {'name': 'Google Gemini', 'level': 85, 'category': ai_tools_cat, 'icon': '💎', 'years_of_experience': 1},
        {'name': 'Deepseek', 'level': 80, 'category': ai_tools_cat, 'icon': '�', 'years_of_experience': 1},
        {'name': 'Cursor AI', 'level': 88, 'category': ai_tools_cat, 'icon': '⚡', 'years_of_experience': 1},
        
        # Web Development (from courses)
        {'name': 'JavaScript', 'level': 85, 'category': programming_cat, 'icon': '�', 'years_of_experience': 2},
        {'name': 'React', 'level': 80, 'category': web_dev_cat, 'icon': '⚛️', 'years_of_experience': 2},
        {'name': 'Node.js', 'level': 75, 'category': web_dev_cat, 'icon': '�', 'years_of_experience': 2},
        {'name': 'Express.js', 'level': 70, 'category': web_dev_cat, 'icon': '🚄', 'years_of_experience': 2},
        {'name': 'MongoDB', 'level': 75, 'category': data_cat, 'icon': '🍃', 'years_of_experience': 2},
        
        # Data Science Tools
        {'name': 'Pandas', 'level': 85, 'category': data_cat, 'icon': '🐼', 'years_of_experience': 2},
        {'name': 'Scikit-learn', 'level': 80, 'category': ml_ai_cat, 'icon': '�', 'years_of_experience': 2},
        
        # Leadership & Soft Skills
        {'name': 'Leadership', 'level': 90, 'category': soft_skills_cat, 'icon': '�', 'years_of_experience': 3, 'is_featured': True},
        {'name': 'Project Management', 'level': 85, 'category': soft_skills_cat, 'icon': '�', 'years_of_experience': 2},
        {'name': 'Team Collaboration', 'level': 88, 'category': soft_skills_cat, 'icon': '🤝', 'years_of_experience': 3},
        
        # Additional Programming
        {'name': 'Django', 'level': 75, 'category': web_dev_cat, 'icon': '🎯', 'years_of_experience': 1},
        {'name': 'HTML/CSS', 'level': 80, 'category': web_dev_cat, 'icon': '🎨', 'years_of_experience': 2},
        {'name': 'Git', 'level': 85, 'category': programming_cat, 'icon': '📚', 'years_of_experience': 3},
    ]
    
    for skill_data in skills_data:
        skill, created = Skill.objects.get_or_create(
            name=skill_data['name'],
            category=skill_data['category'],
            defaults=skill_data
        )
        if created:
            print(f"Created skill: {skill.name}")
    
    # Create Project Categories
    project_categories_data = [
        {'name': 'AI & Machine Learning', 'slug': 'ai-ml', 'color': '#00f6ff'},
        {'name': 'Web Development', 'slug': 'web-development', 'color': '#1effc6'},
        {'name': 'Full-Stack Applications', 'slug': 'full-stack', 'color': '#b97aff'},
        {'name': 'Data Science', 'slug': 'data-science', 'color': '#ff6b6b'},
    ]
    
    for category_data in project_categories_data:
        category, created = ProjectCategory.objects.get_or_create(
            slug=category_data['slug'],
            defaults=category_data
        )
        if created:
            print(f"Created project category: {category.name}")
    
    # Get project categories
    ai_cat = ProjectCategory.objects.get(slug='ai-ml')
    web_cat = ProjectCategory.objects.get(slug='web-development')
    fullstack_cat = ProjectCategory.objects.get(slug='full-stack')
    data_cat = ProjectCategory.objects.get(slug='data-science')
    
    # Create Bhautik's Projects
    projects_data = [
        {
            'title': 'CodeDocGen – Automated Code Documentation Tool',
            'slug': 'codedocgen-automated-documentation',
            'description': 'Django + React application that automatically generates structured Markdown/HTML documentation from code files. Features multi-file upload, syntax highlighting, user authentication, and customizable output formats.',
            'detailed_description': '''CodeDocGen is a comprehensive automated documentation tool that I developed during my internship at Elite Technocrats. This full-stack application streamlines the documentation process for developers by automatically analyzing code files and generating professional documentation.

Key Features:
• Multi-file upload support for various programming languages
• Advanced syntax highlighting for better code readability  
• User authentication system for secure access
• Customizable documentation formats (Markdown/HTML)
• Real-time preview of generated documentation
• Support for project-level documentation organization
• Export capabilities for different output formats

Technical Implementation:
• Backend: Django with Django REST Framework
• Frontend: React with modern JavaScript
• Database: PostgreSQL for user and project data
• File Processing: Custom parsers for different programming languages
• Authentication: JWT-based authentication system
• Deployment: Docker containerization for easy deployment

This project showcases my ability to build complete full-stack applications with complex file processing capabilities and demonstrates my understanding of software architecture and user experience design.''',
            'github_url': 'https://github.com/Bhautikgauswami33/CodeDocGen',
            'live_url': 'https://codedocgen.herokuapp.com',
            'featured_image': 'projects/codedocgen.jpg',
            'is_featured': True,
            'category': fullstack_cat,
            'display_order': 1,
            'start_date': date(2025, 6, 1),
            'end_date': date(2025, 6, 30)
        },
        {
            'title': 'Dream11 Team Predictor',
            'slug': 'dream11-team-predictor',
            'description': 'Machine Learning-based cricket team predictor that analyzes player performance data from ESPNcricinfo to suggest optimal Dream11 teams. Uses Pandas, Scikit-learn, and features a CLI interface with customizable prediction parameters.',
            'detailed_description': '''Dream11 Team Predictor is an intelligent cricket team selection tool that leverages machine learning algorithms to analyze player performance and suggest optimal team combinations for fantasy cricket.

Key Features:
• Data scraping from ESPNcricinfo for real-time player statistics
• Advanced machine learning models for performance prediction
• Interactive command-line interface for easy usage
• Customizable input parameters (budget, team composition, match conditions)
• Historical performance analysis and trend identification
• Player form analysis and injury status consideration
• Head-to-head record analysis between teams

Technical Implementation:
• Data Collection: Web scraping using Beautiful Soup and Requests
• Data Processing: Pandas for data manipulation and analysis
• Machine Learning: Scikit-learn for predictive modeling
• Algorithms: Random Forest, Gradient Boosting for player performance prediction
• Data Storage: SQLite for local data caching
• CLI Interface: Custom command-line interface with argument parsing
• Performance Metrics: Accuracy tracking and model evaluation

Machine Learning Approach:
• Feature Engineering: Player stats, recent form, venue performance
• Model Training: Historical match data and player performance
• Prediction: Team composition optimization based on budget constraints
• Validation: Backtesting with historical Dream11 results

This project demonstrates my expertise in data science, machine learning, and sports analytics, combining my passion for cricket with technical skills.''',
            'github_url': 'https://github.com/Bhautikgauswami33/Dream11-Team-Predictor',
            'live_url': '',
            'featured_image': 'projects/dream11-predictor.jpg',
            'is_featured': True,
            'category': ai_cat,
            'display_order': 2,
            'start_date': date(2024, 8, 1),
            'end_date': date(2024, 10, 15)
        }
    ]
    
    for project_data in projects_data:
        # Define technologies for each project
        if 'CodeDocGen' in project_data['title']:
            tech_names = ['Python', 'Django', 'React', 'JavaScript', 'HTML/CSS', 'Git']
        elif 'Dream11' in project_data['title']:
            tech_names = ['Python', 'Machine Learning', 'Pandas', 'Scikit-learn', 'Data Analytics']
        else:
            tech_names = ['Python']
        
        project, created = Project.objects.get_or_create(
            title=project_data['title'],
            defaults=project_data
        )
        
        if created:
            # Add technologies after project creation
            for tech_name in tech_names:
                try:
                    skill = Skill.objects.filter(name__icontains=tech_name).first()
                    if skill:
                        project.technologies.add(skill)
                    else:
                        print(f"Warning: Skill containing '{tech_name}' not found for project '{project.title}'")
                except Exception as e:
                    print(f"Error adding skill '{tech_name}' to project '{project.title}': {e}")
            print(f"Created project: {project.title}")
        else:
            print(f"Project already exists: {project.title}")
    
    print("Data population completed with Bhautik's information!")
    print(f"Total Skills: {Skill.objects.count()}")
    print(f"Total Projects: {Project.objects.count()}")
    print(f"Personal info entries: {PersonalInfo.objects.count()}")
    print(f"Skill categories: {SkillCategory.objects.count()}")
    print(f"Project categories: {ProjectCategory.objects.count()}")

if __name__ == '__main__':
    populate_data()
