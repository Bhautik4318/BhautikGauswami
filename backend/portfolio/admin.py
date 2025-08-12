"""
Django Admin configuration for the Portfolio application.
Enhanced admin interface with custom styling and functionality.
"""

from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import (
    PersonalInfo, SkillCategory, Skill, ProjectCategory, 
    Project, ContactMessage, SiteConfiguration, ProjectImage
)


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    """
    Admin interface for Personal Information.
    """
    # summernote_fields = ('bio',)  # Removed - using regular TextField
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'email', 'phone', 'profile_image')
        }),
        ('Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'postal_code'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'github_url', 'twitter_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Content', {
            'fields': ('bio', 'skills_summary', 'resume_file')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        """Prevent creating multiple instances (singleton)."""
        if PersonalInfo.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of personal info."""
        return False


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Skill Categories.
    """
    list_display = ('name', 'icon', 'skills_count', 'display_order', 'is_active', 'color_display')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')
    
    def skills_count(self, obj):
        """Display number of skills in this category."""
        return obj.skills.filter(is_active=True).count()
    skills_count.short_description = 'Active Skills'
    
    def color_display(self, obj):
        """Display color as a colored box."""
        return format_html(
            '<div style="width:20px;height:20px;background-color:{};border:1px solid #ccc;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Admin interface for Skills.
    """
    list_display = ('name', 'category', 'level', 'icon', 'years_of_experience', 'is_featured', 'display_order', 'is_active')
    list_editable = ('level', 'is_featured', 'display_order', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active', 'years_of_experience')
    search_fields = ('name', 'description')
    ordering = ('category__display_order', 'display_order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'icon', 'level')
        }),
        ('Details', {
            'fields': ('description', 'years_of_experience')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'display_order', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('category')


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Project Categories.
    """
    list_display = ('name', 'projects_count', 'display_order', 'is_active', 'color_display')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')
    
    def projects_count(self, obj):
        """Display number of projects in this category."""
        return obj.projects.filter(is_active=True).count()
    projects_count.short_description = 'Active Projects'
    
    def color_display(self, obj):
        """Display color as a colored box."""
        return format_html(
            '<div style="width:20px;height:20px;background-color:{};border:1px solid #ccc;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'


class ProjectImageInline(admin.TabularInline):
    """
    Inline admin for project images.
    """
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'display_order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin interface for Projects.
    """
    # summernote_fields = ('detailed_description',)  # Removed - using regular TextField
    inlines = [ProjectImageInline]
    
    list_display = ('title', 'category', 'is_featured', 'display_order', 'is_active', 'tech_count', 'image_preview', 'created_at')
    list_editable = ('is_featured', 'display_order', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active', 'technologies', 'created_at')
    search_fields = ('title', 'description', 'technologies__name')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('technologies',)
    date_hierarchy = 'created_at'
    ordering = ('-is_featured', 'display_order', '-created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'featured_image')
        }),
        ('Content', {
            'fields': ('description', 'detailed_description')
        }),
        ('Technologies & Links', {
            'fields': ('technologies', 'live_url', 'github_url', 'demo_url')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('is_featured', 'display_order', 'is_active')
        }),
    )
    
    def tech_count(self, obj):
        """Display number of technologies used."""
        return obj.technologies.count()
    tech_count.short_description = 'Tech Count'
    
    def image_preview(self, obj):
        """Display project image preview."""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:4px;" />',
                obj.featured_image.url
            )
        return "No Image"
    image_preview.short_description = 'Image'
    
    def get_queryset(self, request):
        """Optimize queryset with prefetch_related."""
        return super().get_queryset(request).select_related('category').prefetch_related('technologies')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for Contact Messages.
    """
    list_display = ('name', 'email', 'subject_display', 'is_read', 'created_at', 'replied_at')
    list_filter = ('is_read', 'replied_at', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('ip_address', 'user_agent', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Admin Actions', {
            'fields': ('is_read', 'admin_notes', 'replied_at')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subject_display(self, obj):
        """Display subject or truncated message."""
        if obj.subject:
            return obj.subject[:50]
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    subject_display.short_description = 'Subject/Message'
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        """Mark selected messages as read."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} messages marked as read.')
    mark_as_read.short_description = 'Mark selected messages as read'
    
    def mark_as_replied(self, request, queryset):
        """Mark selected messages as replied."""
        from django.utils import timezone
        updated = queryset.update(is_read=True, replied_at=timezone.now())
        self.message_user(request, f'{updated} messages marked as replied.')
    mark_as_replied.short_description = 'Mark selected messages as replied'
    
    def has_add_permission(self, request):
        """Prevent manual creation of contact messages."""
        return False


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """
    Admin interface for Site Configuration.
    """
    fieldsets = (
        ('Site Information', {
            'fields': ('site_title', 'site_description', 'site_keywords')
        }),
        ('Theme Colors', {
            'fields': ('primary_color', 'secondary_color', 'accent_color')
        }),
        ('Features', {
            'fields': ('show_social_links',)
        }),
        ('Analytics', {
            'fields': ('google_analytics_id',),
            'classes': ('collapse',)
        }),
        ('Maintenance', {
            'fields': ('maintenance_mode', 'maintenance_message'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent creating multiple instances (singleton)."""
        if SiteConfiguration.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of site configuration."""
        return False


# Custom admin site styling
admin.site.site_header = "Portfolio Admin Dashboard"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to your Portfolio Administration"
