"""
Django models for the Portfolio application.
These models match the React frontend data structures.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class TimestampedModel(models.Model):
    """
    Abstract base class with created and updated timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class PersonalInfo(TimestampedModel):
    """
    Model for storing personal contact information.
    This is a singleton model (only one instance).
    """
    name = models.CharField(max_length=100, default="Bhautik Gauswami")
    title = models.CharField(max_length=200, default="Machine Learning Engineer")
    email = models.EmailField(default="bhautikgosai4318@gmail.com")
    phone = models.CharField(max_length=20, default="+91 8141415113")
    
    # Address fields
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, default="Surat")
    state = models.CharField(max_length=100, default="Gujarat")
    country = models.CharField(max_length=100, default="India")
    postal_code = models.CharField(max_length=20, default="395005")
    
    # Social media links
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    
    # Bio and profile
    bio = models.TextField(
        help_text="Biography content",
        default="I'm a passionate Machine Learning Engineer with expertise in building intelligent systems that solve real-world problems."
    )
    profile_image = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        help_text="Profile photo (recommended: 400x400px)"
    )
    
    # Skills summary for hero section
    skills_summary = models.TextField(
        default="💡 Data Science | 🧠 Deep Learning | 🤖 AI Enthusiast",
        help_text="Brief skills summary for homepage hero section"
    )
    
    # Resume file
    resume_file = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True,
        help_text="PDF resume file"
    )
    
    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"
    
    def __str__(self):
        return f"{self.name} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        if not self.pk and PersonalInfo.objects.exists():
            # Update existing instance instead of creating new one
            existing = PersonalInfo.objects.first()
            existing.name = self.name
            existing.title = self.title
            existing.email = self.email
            existing.phone = self.phone
            existing.bio = self.bio
            existing.save()
            return existing
        return super().save(*args, **kwargs)


class SkillCategory(TimestampedModel):
    """
    Categories for organizing skills (ML & AI, Frontend, Backend, Tools, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#00f6ff', help_text="Category color for UI (hex format)")
    icon = models.CharField(
        max_length=10,
        default='🔧',
        help_text="Emoji icon for the category"
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class Skill(TimestampedModel):
    """
    Skills model matching the React frontend Skill interface.
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    level = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Skill level percentage (0-100)"
    )
    icon = models.CharField(
        max_length=10,
        default='💻',
        help_text="Emoji icon for the skill"
    )
    description = models.TextField(
        blank=True,
        help_text="Brief description of your experience with this skill"
    )
    years_of_experience = models.PositiveIntegerField(
        default=0,
        help_text="Years of experience with this skill"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show in featured skills section"
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ['category', 'display_order', 'name']
        unique_together = ['name', 'category']
    
    def __str__(self):
        return f"{self.name} ({self.category.name}) - {self.level}%"


class ProjectCategory(TimestampedModel):
    """
    Categories for organizing projects.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#1effc6', help_text="Category color for UI (hex format)")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class Project(TimestampedModel):
    """
    Projects model matching the React frontend Project interface.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(help_text="Brief project description")
    detailed_description = models.TextField(
        blank=True,
        help_text="Detailed project description"
    )
    
    # Project links
    live_url = models.URLField(
        blank=True,
        null=True,
        help_text="Live project URL"
    )
    github_url = models.URLField(
        blank=True,
        null=True,
        help_text="GitHub repository URL"
    )
    demo_url = models.URLField(
        blank=True,
        null=True,
        help_text="Demo or documentation URL"
    )
    
    # Project media
    featured_image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        help_text="Main project image (recommended: 800x600px)"
    )
    
    # Project metadata
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    technologies = models.ManyToManyField(
        Skill,
        related_name='projects',
        help_text="Technologies/skills used in this project"
    )
    
    # Status and visibility
    is_featured = models.BooleanField(
        default=False,
        help_text="Show in featured projects section"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Display on website"
    )
    display_order = models.PositiveIntegerField(default=0)
    
    # Project timeline
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-is_featured', 'display_order', '-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def tech_list(self):
        """Return list of technology names for API serialization."""
        return [skill.name for skill in self.technologies.all()]


class ContactMessage(TimestampedModel):
    """
    Model for storing contact form submissions.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional subject line"
    )
    message = models.TextField()
    
    # Admin fields
    is_read = models.BooleanField(default=False)
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes (not visible to user)"
    )
    replied_at = models.DateTimeField(blank=True, null=True)
    
    # Spam protection
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.email}"
    
    def mark_as_read(self):
        """Mark message as read."""
        self.is_read = True
        self.save(update_fields=['is_read'])
    
    def mark_as_replied(self):
        """Mark message as replied."""
        self.replied_at = timezone.now()
        self.is_read = True
        self.save(update_fields=['replied_at', 'is_read'])


class SiteConfiguration(TimestampedModel):
    """
    Site-wide configuration settings.
    """
    site_title = models.CharField(
        max_length=200,
        default="Bhautik Gauswami - ML Portfolio"
    )
    site_description = models.TextField(
        default="Portfolio website of Bhautik Gauswami, Machine Learning Engineer"
    )
    site_keywords = models.TextField(
        default="machine learning, AI, portfolio, python, tensorflow, data science",
        help_text="SEO keywords (comma-separated)"
    )
    
    # Theme colors (matching React frontend)
    primary_color = models.CharField(max_length=7, default='#00f6ff', help_text="Primary cyan color (hex format)")
    secondary_color = models.CharField(max_length=7, default='#1effc6', help_text="Neural green color (hex format)")
    accent_color = models.CharField(max_length=7, default='#b97aff', help_text="Soft violet color (hex format)")
    
    # Social media
    show_social_links = models.BooleanField(default=True)
    
    # Analytics
    google_analytics_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Google Analytics measurement ID"
    )
    
    # Maintenance mode
    maintenance_mode = models.BooleanField(
        default=False,
        help_text="Enable maintenance mode"
    )
    maintenance_message = models.TextField(
        blank=True,
        help_text="Message to show during maintenance"
    )
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
    
    def __str__(self):
        return self.site_title
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        if not self.pk and SiteConfiguration.objects.exists():
            existing = SiteConfiguration.objects.first()
            self.pk = existing.pk
        return super().save(*args, **kwargs)


class ProjectImage(TimestampedModel):
    """
    Additional images for projects (gallery).
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.project.title} - Image {self.display_order}"
