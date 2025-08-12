"""
Django REST Framework serializers for the Portfolio API.
These serializers convert Django models to JSON format for the React frontend.
"""

from rest_framework import serializers
from .models import (
    PersonalInfo, SkillCategory, Skill, ProjectCategory, 
    Project, ContactMessage, SiteConfiguration, ProjectImage
)


class PersonalInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for personal information.
    """
    profile_image_url = serializers.SerializerMethodField()
    resume_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PersonalInfo
        fields = [
            'id', 'name', 'title', 'email', 'phone', 
            'address_line_1', 'address_line_2', 'city', 'state', 
            'country', 'postal_code', 'linkedin_url', 'github_url', 
            'twitter_url', 'instagram_url', 'bio', 'profile_image_url',
            'skills_summary', 'resume_file_url', 'updated_at'
        ]
    
    def get_profile_image_url(self, obj):
        """Return full URL for profile image."""
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
        return None
    
    def get_resume_file_url(self, obj):
        """Return full URL for resume file."""
        if obj.resume_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resume_file.url)
        return None


class SkillCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for skill categories.
    """
    skills_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SkillCategory
        fields = [
            'id', 'name', 'slug', 'description', 'color', 
            'icon', 'display_order', 'skills_count'
        ]
    
    def get_skills_count(self, obj):
        """Return count of active skills in this category."""
        return obj.skills.filter(is_active=True).count()


class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer for skills matching React frontend Skill interface.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'level', 'icon', 'description', 
            'years_of_experience', 'is_featured', 'display_order',
            'category_name', 'category_slug', 'category_color'
        ]


class ProjectCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for project categories.
    """
    projects_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectCategory
        fields = [
            'id', 'name', 'slug', 'description', 'color', 
            'display_order', 'projects_count'
        ]
    
    def get_projects_count(self, obj):
        """Return count of active projects in this category."""
        return obj.projects.filter(is_active=True).count()


class ProjectImageSerializer(serializers.ModelSerializer):
    """
    Serializer for project images.
    """
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectImage
        fields = ['id', 'image_url', 'caption', 'display_order']
    
    def get_image_url(self, obj):
        """Return full URL for project image."""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for projects matching React frontend Project interface.
    """
    tech = serializers.SerializerMethodField()  # Match React interface field name
    link = serializers.SerializerMethodField()  # Match React interface field name
    image = serializers.SerializerMethodField()  # Match React interface field name
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'detailed_description',
            'tech', 'link', 'image', 'live_url', 'github_url', 'demo_url',
            'category_name', 'category_slug', 'category_color', 'images',
            'is_featured', 'display_order', 'start_date', 'end_date',
            'created_at', 'updated_at'
        ]
    
    def get_tech(self, obj):
        """Return list of technology names (matches React interface)."""
        return [skill.name for skill in obj.technologies.filter(is_active=True)]
    
    def get_link(self, obj):
        """Return primary link (matches React interface)."""
        return obj.live_url or obj.github_url or obj.demo_url or "#"
    
    def get_image(self, obj):
        """Return full URL for featured image (matches React interface)."""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
        return None


class ProjectDetailSerializer(ProjectSerializer):
    """
    Detailed serializer for individual project views.
    """
    technologies = SkillSerializer(many=True, read_only=True)
    
    class Meta(ProjectSerializer.Meta):
        # Include all fields from ProjectSerializer plus technologies
        fields = ProjectSerializer.Meta.fields + ['technologies']


class ContactMessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating contact messages.
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
    
    def validate_email(self, value):
        """Validate email format."""
        return value.lower().strip()
    
    def validate_name(self, value):
        """Validate and clean name."""
        return value.strip()
    
    def validate_message(self, value):
        """Validate message length."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters long."
            )
        return value.strip()


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for contact messages (admin view).
    """
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'subject', 'message', 
            'is_read', 'admin_notes', 'replied_at', 
            'ip_address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['ip_address', 'created_at', 'updated_at']


class SiteConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer for site configuration.
    """
    class Meta:
        model = SiteConfiguration
        fields = [
            'id', 'site_title', 'site_description', 'site_keywords',
            'primary_color', 'secondary_color', 'accent_color',
            'show_social_links', 'maintenance_mode', 'maintenance_message'
        ]


# Summary serializers for dashboard/stats
class DashboardStatsSerializer(serializers.Serializer):
    """
    Serializer for dashboard statistics.
    """
    total_projects = serializers.IntegerField()
    featured_projects = serializers.IntegerField()
    total_skills = serializers.IntegerField()
    skill_categories = serializers.IntegerField()
    unread_messages = serializers.IntegerField()
    total_messages = serializers.IntegerField()


class SkillsByCategorySerializer(serializers.Serializer):
    """
    Serializer for skills grouped by category.
    """
    category = SkillCategorySerializer()
    skills = SkillSerializer(many=True)


class FeaturedContentSerializer(serializers.Serializer):
    """
    Serializer for homepage featured content.
    """
    personal_info = PersonalInfoSerializer()
    featured_projects = ProjectSerializer(many=True)
    featured_skills = SkillSerializer(many=True)
    site_config = SiteConfigurationSerializer()
