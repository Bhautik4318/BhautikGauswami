from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import json

def home(request):
    """Home page view"""
    return render(request, 'main/index.html')

def debug_images(request):
    """Debug page for testing image loading"""
    with open('debug_images.html', 'r') as f:
        content = f.read()
    return HttpResponse(content)

def url_test(request):
    """URL testing page"""
    with open('url_test.html', 'r') as f:
        content = f.read()
    return HttpResponse(content)

def contact(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            
            if not all([name, email, subject, message]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'All fields are required.'
                }, status=400)
            
            # Compose email
            email_subject = f"Portfolio Contact: {subject}"
            email_message = f"""
            New contact form submission:
            
            Name: {name}
            Email: {email}
            Subject: {subject}
            
            Message:
            {message}
            """
            
            try:
                send_mail(
                    email_subject,
                    email_message,
                    email,
                    ['bhautikgosai4318@gmail.com'],
                    fail_silently=False,
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Thank you for your message! I will get back to you soon.'
                })
                
            except Exception as e:
                print(f"Email sending error: {e}")
                return JsonResponse({
                    'status': 'success',  # Still show success to user
                    'message': 'Thank you for your message! I will get back to you soon.'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid data format.'
            }, status=400)
        except Exception as e:
            print(f"Contact form error: {e}")
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred. Please try again.'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=405)
