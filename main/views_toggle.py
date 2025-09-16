from django.shortcuts import render
from django.http import HttpResponse

def toggle_preview(request):
    return render(request, 'toggle_preview.html')