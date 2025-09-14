#!/usr/bin/env python
import os
import subprocess
import shutil
from django.core.management import execute_from_command_line
from django.conf import settings

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

# Create build directory
build_dir = 'build'
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
os.makedirs(build_dir)

# Copy static files
shutil.copytree('static', os.path.join(build_dir, 'static'))

print("Static site build completed!")
