"""
Comprehensive Profile API view for the portfolio frontend.
This view combines all necessary data into a single endpoint.
"""

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from .models import PersonalInfo, Skill, Project, SkillCategory, ProjectCategory
from .serializers import (
    PersonalInfoSerializer, SkillSerializer, ProjectSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def profile_view(request):
    """
    Comprehensive profile endpoint that returns all necessary data
    for the portfolio frontend in a single request.
    """
    try:
        # Get personal information
        personal_info = PersonalInfo.objects.first()
        if not personal_info:
            # Create default personal info if none exists
            personal_info = PersonalInfo.objects.create()
        
        # Get skills grouped by category
        skills = Skill.objects.select_related('category').all()
        
        # Get projects (featured first)
        projects = Project.objects.all().order_by('-is_featured', '-created_at')
        
        # Prepare the response data
        profile_data = {
            # Basic personal information
            'name': personal_info.name,
            'headline': f"{personal_info.title}",
            'summary': personal_info.bio,
            
            # Profile images
            'profile_photo_url': request.build_absolute_uri('/static/profile.jpg') if personal_info else '',
            'about_photo_url': request.build_absolute_uri('/static/profile.jpg') if personal_info else '',
            
            # CV/Resume
            'cv_url': request.build_absolute_uri('/static/resume.txt'),
            
            # Statistics
            'experience_years': 5,  # You can make this dynamic based on your data
            'projects_completed': projects.count(),
            'technologies_mastered': skills.count(),
            
            # Contact information
            'email': personal_info.email,
            'phone': personal_info.phone,
            'location': f"{personal_info.city}, {personal_info.state}, {personal_info.country}",
            
            # Social links
            'social_links': {
                'linkedin': personal_info.linkedin_url,
                'github': personal_info.github_url,
                'twitter': personal_info.twitter_url,
                'instagram': personal_info.instagram_url,
            },
            
            # Education (you can expand this with a separate Education model)
            'education': [
                {
                    'id': 1,
                    'institution': 'University of Technology',
                    'degree': 'Master of Science',
                    'field_of_study': 'Computer Science',
                    'start_date': '2018-09-01',
                    'end_date': '2020-05-01',
                    'description': 'Specialized in Machine Learning and Artificial Intelligence',
                    'gpa': '3.8'
                },
                # Add more education records as needed
            ],
            
            # Skills with detailed information
            'skills': [],
            
            # Projects with full details
            'projects': [],
        }
        
        # Add skills data
        for skill in skills:
            skill_data = {
                'id': skill.id,
                'name': skill.name,
                'category': skill.category.name if skill.category else 'Uncategorized',
                'proficiency_level': skill.proficiency_level,
                'years_of_experience': skill.years_of_experience if hasattr(skill, 'years_of_experience') else None,
                'description': skill.description,
            }
            profile_data['skills'].append(skill_data)
        
        # Add projects data
        for project in projects:
            project_data = {
                'id': project.id,
                'title': project.name,
                'description': project.description,
                'technologies': project.technologies_used.split(',') if project.technologies_used else [],
                'github_url': project.github_url,
                'live_url': project.live_url,
                'image_url': request.build_absolute_uri(project.image.url) if project.image else '',
                'start_date': project.start_date.isoformat() if project.start_date else '',
                'end_date': project.end_date.isoformat() if project.end_date else '',
                'is_featured': project.is_featured,
            }
            profile_data['projects'].append(project_data)
        
        return Response(profile_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        # Return fallback data if there's an error
        fallback_data = {
            'name': 'Bhautik Gauswami',
            'headline': 'Machine Learning Engineer & Full-Stack Developer',
            'summary': 'I\'m a passionate Machine Learning Engineer with a deep love for creating intelligent solutions that make a real difference.',
            'profile_photo_url': request.build_absolute_uri('/static/profile.jpg'),
            'about_photo_url': request.build_absolute_uri('/static/profile.jpg'),
            'cv_url': request.build_absolute_uri('/static/resume.txt'),
            'experience_years': 5,
            'projects_completed': 10,
            'technologies_mastered': 20,
            'email': 'bhautikgosai4318@gmail.com',
            'phone': '+91 8141415113',
            'location': 'Surat, Gujarat, India',
            'social_links': {
                'linkedin': '',
                'github': '',
                'twitter': '',
                'instagram': '',
            },
            'education': [],
            'skills': [],
            'projects': [],
            'error': f'Using fallback data: {str(e)}'
        }
        
        return Response(fallback_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Simple health check endpoint.
    """
    return JsonResponse({
        'status': 'healthy',
        'message': 'Portfolio API is running',
        'timestamp': timezone.now().isoformat()
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def contact_submit(request):
    """
    Handle contact form submissions.
    """
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {'error': f'{field} is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create contact message (if you have a ContactMessage model)
        try:
            from .models import ContactMessage
            contact_message = ContactMessage.objects.create(
                name=data['name'],
                email=data['email'],
                subject=data['subject'],
                message=data['message']
            )
            
            return Response(
                {'success': True, 'message': 'Message sent successfully!'}, 
                status=status.HTTP_201_CREATED
            )
        except:
            # Even if we can't save to database, we can still log it
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Contact form submission: {data}")
            
            return Response(
                {'success': True, 'message': 'Message received!'}, 
                status=status.HTTP_200_OK
            )
            
    except Exception as e:
        return Response(
            {'success': False, 'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
