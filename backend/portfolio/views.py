"""
Django REST Framework views for the Portfolio API.
These views provide endpoints for the React frontend to consume.
"""

from django.db.models import Count
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    PersonalInfo, SkillCategory, Skill, ProjectCategory, 
    Project, ContactMessage, SiteConfiguration
)
from .serializers import (
    PersonalInfoSerializer, SkillCategorySerializer, SkillSerializer,
    ProjectCategorySerializer, ProjectSerializer, ProjectDetailSerializer,
    ContactMessageCreateSerializer, ContactMessageSerializer,
    SiteConfigurationSerializer, DashboardStatsSerializer,
    SkillsByCategorySerializer, FeaturedContentSerializer
)


class PersonalInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for personal information (read-only for public).
    """
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current personal information."""
        try:
            personal_info = PersonalInfo.objects.first()
            if personal_info:
                serializer = self.get_serializer(personal_info)
                return Response(serializer.data)
            return Response({'detail': 'Personal information not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SkillCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for skill categories.
    """
    queryset = SkillCategory.objects.filter(is_active=True)
    serializer_class = SkillCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering = ['display_order', 'name']


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for skills.
    """
    queryset = Skill.objects.filter(is_active=True)
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description']
    ordering = ['category__display_order', 'display_order', 'name']
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get skills grouped by category."""
        categories = SkillCategory.objects.filter(
            is_active=True,
            skills__is_active=True
        ).distinct().prefetch_related('skills')
        
        data = []
        for category in categories:
            skills = category.skills.filter(is_active=True)
            data.append({
                'category': SkillCategorySerializer(category).data,
                'skills': SkillSerializer(skills, many=True).data
            })
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured skills."""
        featured_skills = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_skills, many=True)
        return Response(serializer.data)


class ProjectCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for project categories.
    """
    queryset = ProjectCategory.objects.filter(is_active=True)
    serializer_class = ProjectCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering = ['display_order', 'name']


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for projects.
    """
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'technologies']
    search_fields = ['title', 'description', 'technologies__name']
    ordering = ['-is_featured', 'display_order', '-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        """Use detailed serializer for single project views."""
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured projects."""
        featured_projects = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get projects grouped by category."""
        category_slug = request.query_params.get('category')
        if category_slug:
            projects = self.queryset.filter(category__slug=category_slug)
        else:
            projects = self.queryset.all()
        
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for contact messages.
    """
    queryset = ContactMessage.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_read']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializer for create vs read operations."""
        if self.action == 'create':
            return ContactMessageCreateSerializer
        return ContactMessageSerializer
    
    def get_permissions(self):
        """Allow anyone to create messages, but only authenticated users to read."""
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Create a new contact message with additional metadata."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Add IP address and user agent for spam protection
        contact_message = serializer.save(
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response(
            {'message': 'Thank you for your message! I will get back to you soon.'},
            status=status.HTTP_201_CREATED
        )
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a message as read."""
        message = self.get_object()
        message.mark_as_read()
        return Response({'status': 'Message marked as read'})
    
    @action(detail=True, methods=['post'])
    def mark_replied(self, request, pk=None):
        """Mark a message as replied."""
        message = self.get_object()
        message.mark_as_replied()
        return Response({'status': 'Message marked as replied'})


class SiteConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for site configuration.
    """
    queryset = SiteConfiguration.objects.all()
    serializer_class = SiteConfigurationSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current site configuration."""
        try:
            config = SiteConfiguration.objects.first()
            if config:
                serializer = self.get_serializer(config)
                return Response(serializer.data)
            return Response({'detail': 'Site configuration not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API endpoints for dashboard and statistics
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for admin.
    """
    stats = {
        'total_projects': Project.objects.filter(is_active=True).count(),
        'featured_projects': Project.objects.filter(is_active=True, is_featured=True).count(),
        'total_skills': Skill.objects.filter(is_active=True).count(),
        'skill_categories': SkillCategory.objects.filter(is_active=True).count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'total_messages': ContactMessage.objects.count(),
    }
    
    serializer = DashboardStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def portfolio_data(request):
    """
    Get all portfolio data in a single request.
    This endpoint matches your React frontend data structure exactly.
    """
    try:
        # Get personal info
        personal_info = PersonalInfo.objects.first()
        
        # Get all active projects
        projects = Project.objects.filter(is_active=True)
        
        # Get all active skills
        skills = Skill.objects.filter(is_active=True)
        
        # Transform data to match React interface
        projects_data = []
        for project in projects:
            projects_data.append({
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'tech': [skill.name for skill in project.technologies.filter(is_active=True)],
                'link': project.live_url or project.github_url or project.demo_url or "#",
                'image': request.build_absolute_uri(project.featured_image.url) if project.featured_image else None,
            })
        
        skills_data = []
        for skill in skills:
            skills_data.append({
                'name': skill.name,
                'level': skill.level,
                'icon': skill.icon,
            })
        
        data = {
            'projects': projects_data,
            'skills': skills_data,
            'personal_info': {
                'name': personal_info.name if personal_info else 'Bhautik Gauswami',
                'title': personal_info.title if personal_info else 'Machine Learning Engineer',
                'email': personal_info.email if personal_info else 'bhautikgosai4318@gmail.com',
                'phone': personal_info.phone if personal_info else '+91 8141415113',
                'bio': personal_info.bio if personal_info else '',
                'address': {
                    'city': personal_info.city if personal_info else 'Surat',
                    'state': personal_info.state if personal_info else 'Gujarat',
                    'country': personal_info.country if personal_info else 'India',
                    'postal_code': personal_info.postal_code if personal_info else '395005',
                } if personal_info else {},
                'social_links': {
                    'linkedin': personal_info.linkedin_url if personal_info else '',
                    'github': personal_info.github_url if personal_info else '',
                    'twitter': personal_info.twitter_url if personal_info else '',
                } if personal_info else {},
            }
        }
        
        return Response(data)
        
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch portfolio data', 'detail': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
