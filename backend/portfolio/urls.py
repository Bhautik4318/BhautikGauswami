"""
URL configuration for the Portfolio app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'personal-info', views.PersonalInfoViewSet)
router.register(r'skill-categories', views.SkillCategoryViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'project-categories', views.ProjectCategoryViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'contact-messages', views.ContactMessageViewSet)
router.register(r'site-config', views.SiteConfigurationViewSet)

urlpatterns = [
    # API routes
    path('', include(router.urls)),
    
    # Custom endpoints
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('portfolio-data/', views.portfolio_data, name='portfolio-data'),
]
