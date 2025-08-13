import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
django.setup()

from portfolio.models import Project, Skill, PersonalInfo, SkillCategory, ProjectCategory
from django.contrib.auth.models import User

def populate_data():
    print("Starting data population...")
    
    # Create PersonalInfo entry
    personal_info, created = PersonalInfo.objects.get_or_create(
        id=1,
        defaults={
            'name': 'Bhautik Gauswami',
            'title': 'Full-Stack Developer & AI Enthusiast',
            'bio': '''I'm a passionate full-stack developer with expertise in modern web technologies. I specialize in React, TypeScript, Python, and AI/ML technologies. With a keen eye for design and a love for clean, efficient code, I create digital experiences that are both beautiful and functional.''',
            'email': 'bhautikgosai4318@gmail.com',
            'phone': '+91 8141415113',
            'city': 'Surat',
            'state': 'Gujarat',
            'country': 'India',
            'linkedin_url': 'https://linkedin.com/in/bhautik-gauswami',
            'github_url': 'https://github.com/bhautikgauswami',
            'skills_summary': '💡 Full-Stack Development | 🧠 AI/ML | 🚀 React & TypeScript'
        }
    )
    print(f"Personal info {'created' if created else 'updated'}")
    
    # Create Skill Categories
    skill_categories_data = [
        {'name': 'Frontend', 'slug': 'frontend', 'color': '#61DAFB', 'icon': '🎨', 'display_order': 1},
        {'name': 'Backend', 'slug': 'backend', 'color': '#68D391', 'icon': '⚙️', 'display_order': 2},
        {'name': 'Database', 'slug': 'database', 'color': '#F687B3', 'icon': '🗄️', 'display_order': 3},
        {'name': 'AI/ML', 'slug': 'ai-ml', 'color': '#FBD38D', 'icon': '🤖', 'display_order': 4},
        {'name': 'Tools', 'slug': 'tools', 'color': '#A78BFA', 'icon': '🔧', 'display_order': 5},
        {'name': 'Cloud', 'slug': 'cloud', 'color': '#FEB2B2', 'icon': '☁️', 'display_order': 6},
    ]
    
    for category_data in skill_categories_data:
        category, created = SkillCategory.objects.get_or_create(
            slug=category_data['slug'],
            defaults=category_data
        )
        if created:
            print(f"Created skill category: {category.name}")
    
    # Get categories for skill creation
    frontend_cat = SkillCategory.objects.get(slug='frontend')
    backend_cat = SkillCategory.objects.get(slug='backend')
    database_cat = SkillCategory.objects.get(slug='database')
    ai_ml_cat = SkillCategory.objects.get(slug='ai-ml')
    tools_cat = SkillCategory.objects.get(slug='tools')
    cloud_cat = SkillCategory.objects.get(slug='cloud')
    
    # Create Skills
    skills_data = [
        # Frontend Skills
        {'name': 'React', 'level': 95, 'category': frontend_cat, 'icon': '⚛️', 'years_of_experience': 4, 'is_featured': True},
        {'name': 'TypeScript', 'level': 90, 'category': frontend_cat, 'icon': '🔷', 'years_of_experience': 3, 'is_featured': True},
        {'name': 'JavaScript', 'level': 95, 'category': frontend_cat, 'icon': '🟨', 'years_of_experience': 5, 'is_featured': True},
        {'name': 'Next.js', 'level': 85, 'category': frontend_cat, 'icon': '⚡', 'years_of_experience': 2, 'is_featured': True},
        {'name': 'Tailwind CSS', 'level': 90, 'category': frontend_cat, 'icon': '🎨', 'years_of_experience': 3},
        {'name': 'Framer Motion', 'level': 80, 'category': frontend_cat, 'icon': '🎭', 'years_of_experience': 2},
        
        # Backend Skills
        {'name': 'Python', 'level': 90, 'category': backend_cat, 'icon': '🐍', 'years_of_experience': 4, 'is_featured': True},
        {'name': 'Django', 'level': 85, 'category': backend_cat, 'icon': '🎯', 'years_of_experience': 3, 'is_featured': True},
        {'name': 'Node.js', 'level': 80, 'category': backend_cat, 'icon': '🟢', 'years_of_experience': 3},
        {'name': 'Express.js', 'level': 75, 'category': backend_cat, 'icon': '🚄', 'years_of_experience': 2},
        
        # Database Skills
        {'name': 'PostgreSQL', 'level': 75, 'category': database_cat, 'icon': '🐘', 'years_of_experience': 3},
        {'name': 'MongoDB', 'level': 70, 'category': database_cat, 'icon': '🍃', 'years_of_experience': 2},
        {'name': 'SQLite', 'level': 80, 'category': database_cat, 'icon': '💽', 'years_of_experience': 4},
        
        # AI/ML Skills
        {'name': 'Machine Learning', 'level': 80, 'category': ai_ml_cat, 'icon': '🧠', 'years_of_experience': 2, 'is_featured': True},
        {'name': 'TensorFlow', 'level': 75, 'category': ai_ml_cat, 'icon': '🔥', 'years_of_experience': 2},
        {'name': 'OpenAI APIs', 'level': 85, 'category': ai_ml_cat, 'icon': '🤖', 'years_of_experience': 1, 'is_featured': True},
        {'name': 'scikit-learn', 'level': 70, 'category': ai_ml_cat, 'icon': '📊', 'years_of_experience': 2},
        
        # Tools
        {'name': 'Git', 'level': 90, 'category': tools_cat, 'icon': '📚', 'years_of_experience': 5, 'is_featured': True},
        {'name': 'Docker', 'level': 70, 'category': tools_cat, 'icon': '🐳', 'years_of_experience': 2},
        {'name': 'VS Code', 'level': 95, 'category': tools_cat, 'icon': '💻', 'years_of_experience': 5},
        
        # Cloud
        {'name': 'AWS', 'level': 65, 'category': cloud_cat, 'icon': '☁️', 'years_of_experience': 1},
        {'name': 'Vercel', 'level': 80, 'category': cloud_cat, 'icon': '▲', 'years_of_experience': 2},
    ]
    
    for skill_data in skills_data:
        skill, created = Skill.objects.get_or_create(
            name=skill_data['name'],
            defaults=skill_data
        )
        if created:
            print(f"Created skill: {skill.name}")
    
    # Create Project Categories
    project_categories_data = [
        {'name': 'Web Development', 'slug': 'web-development', 'color': '#3B82F6'},
        {'name': 'AI/ML Projects', 'slug': 'ai-ml', 'color': '#10B981'},
        {'name': 'Full-Stack Apps', 'slug': 'full-stack', 'color': '#8B5CF6'},
        {'name': 'Mobile Apps', 'slug': 'mobile', 'color': '#F59E0B'},
    ]
    
    for category_data in project_categories_data:
        category, created = ProjectCategory.objects.get_or_create(
            slug=category_data['slug'],
            defaults=category_data
        )
        if created:
            print(f"Created project category: {category.name}")
    
    # Get project categories
    web_cat = ProjectCategory.objects.get(slug='web-development')
    ai_cat = ProjectCategory.objects.get(slug='ai-ml')
    fullstack_cat = ProjectCategory.objects.get(slug='full-stack')
    
    # Create Projects
    projects_data = [
        {
            'title': 'Neural Portfolio Website',
            'slug': 'neural-portfolio-website',
            'description': 'A cutting-edge portfolio website built with React 19, TypeScript, and advanced animations. Features include neural network particle backgrounds, 3D animations, and responsive design with Framer Motion.',
            'github_url': 'https://github.com/bhautikgauswami/neural-portfolio',
            'live_url': 'https://bhautikgauswami.dev',
            'featured_image': 'projects/neural-portfolio.jpg',
            'is_featured': True,
            'category': web_cat,
            'display_order': 1
        },
        {
            'title': 'AI-Powered Chat Application',
            'slug': 'ai-powered-chat-application',
            'description': 'Real-time chat application with AI-powered responses using OpenAI API. Built with React frontend and Django backend with WebSocket support for instant messaging.',
            'github_url': 'https://github.com/bhautikgauswami/ai-chat-app',
            'live_url': 'https://ai-chat.bhautikgauswami.dev',
            'featured_image': 'projects/ai-chat.jpg',
            'is_featured': True,
            'category': ai_cat,
            'display_order': 2
        },
        {
            'title': 'E-Commerce Platform',
            'slug': 'e-commerce-platform',
            'description': 'Full-stack e-commerce platform with payment integration, inventory management, and admin dashboard. Built with Next.js and Django REST Framework for optimal performance.',
            'github_url': 'https://github.com/bhautikgauswami/ecommerce-platform',
            'live_url': 'https://shop.bhautikgauswami.dev',
            'featured_image': 'projects/ecommerce.jpg',
            'is_featured': True,
            'category': fullstack_cat,
            'display_order': 3
        },
        {
            'title': 'ML Model Deployment Platform',
            'slug': 'ml-model-deployment-platform',
            'description': 'Platform for deploying and managing machine learning models with REST APIs, monitoring, and scaling capabilities. Containerized with Docker and deployed on Kubernetes.',
            'github_url': 'https://github.com/bhautikgauswami/ml-platform',
            'live_url': '',
            'featured_image': 'projects/ml-platform.jpg',
            'is_featured': False,
            'category': ai_cat,
            'display_order': 4
        },
        {
            'title': 'Task Management App',
            'slug': 'task-management-app',
            'description': 'Collaborative task management application with real-time updates, team collaboration features, and project tracking. Features drag-and-drop interface and time tracking.',
            'github_url': 'https://github.com/bhautikgauswami/task-manager',
            'live_url': 'https://tasks.bhautikgauswami.dev',
            'featured_image': 'projects/task-manager.jpg',
            'is_featured': False,
            'category': fullstack_cat,
            'display_order': 5
        }
    ]
    
    for project_data in projects_data:
        # Remove technologies from initial creation since it's a ManyToMany field
        tech_names = ['React', 'TypeScript', 'Framer Motion', 'Three.js', 'Tailwind CSS', 'Particles.js'] if 'Neural Portfolio' in project_data['title'] else \
                    ['React', 'Django', 'OpenAI API', 'WebSockets', 'PostgreSQL', 'Redis'] if 'AI-Powered Chat' in project_data['title'] else \
                    ['Next.js', 'Django REST', 'Stripe', 'PostgreSQL', 'Redis', 'Tailwind CSS'] if 'E-Commerce' in project_data['title'] else \
                    ['Python', 'FastAPI', 'TensorFlow', 'Docker', 'Kubernetes', 'MLflow'] if 'ML Model' in project_data['title'] else \
                    ['React', 'Node.js', 'Socket.io', 'MongoDB', 'Express', 'JWT']
        
        project, created = Project.objects.get_or_create(
            title=project_data['title'],
            defaults=project_data
        )
        
        if created:
            # Add technologies after project creation
            for tech_name in tech_names:
                try:
                    skill = Skill.objects.get(name=tech_name)
                    project.technologies.add(skill)
                except Skill.DoesNotExist:
                    print(f"Warning: Skill '{tech_name}' not found for project '{project.title}'")
            print(f"Created project: {project.title}")
        else:
            print(f"Project already exists: {project.title}")
    
    print("Data population completed!")
    print(f"Total Skills: {Skill.objects.count()}")
    print(f"Total Projects: {Project.objects.count()}")
    print(f"Personal info entries: {PersonalInfo.objects.count()}")
    print(f"Skill categories: {SkillCategory.objects.count()}")
    print(f"Project categories: {ProjectCategory.objects.count()}")

if __name__ == '__main__':
    populate_data()
