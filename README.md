# Bhautik Gauswami - Portfolio Website

A fully responsive, animated black-and-white personal portfolio website built with Django and TypeScript.

## Features

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Animated Background**: Black and white particle animation using particles.js
- **Modern Stack**: Django backend with TypeScript frontend
- **Contact Form**: Functional AJAX contact form with email integration
- **Resume Download**: Direct PDF download functionality
- **Project Showcase**: Display of AI/ML and web development projects
- **Smooth Animations**: Scroll-triggered animations and transitions
- **SEO Optimized**: Semantic HTML structure with proper meta tags

## Tech Stack

- **Backend**: Django 4.2.7 (Python)
- **Frontend**: HTML5, CSS3, TypeScript
- **Styling**: Custom CSS with black and white theme
- **Animations**: Particles.js for background effects
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Inter font family from Google Fonts

## Project Structure

```
portfolio/
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot configuration
├── .vscode/
│   └── tasks.json                 # VS Code tasks configuration
├── portfolio/                     # Django project settings
│   ├── settings.py               # Django configuration
│   ├── urls.py                   # Main URL routing
│   └── wsgi.py                   # WSGI configuration
├── main/                         # Main Django app
│   ├── views.py                  # View functions
│   ├── urls.py                   # App URL routing
│   └── models.py                 # Database models (if needed)
├── templates/
│   └── main/
│       └── index.html            # Main template file
├── static/
│   ├── css/
│   │   └── styles.css            # Main stylesheet
│   ├── js/
│   │   └── main.js               # Compiled TypeScript
│   └── img/                      # Images directory
├── media/                        # Media files (resume PDF)
├── src/
│   └── main.ts                   # TypeScript source file
├── requirements.txt              # Python dependencies
├── package.json                  # Node.js dependencies
├── tsconfig.json                 # TypeScript configuration
└── manage.py                     # Django management script
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Compile TypeScript:**
   ```bash
   npm run build
   ```

4. **Run Django migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser and visit:**
   ```
   http://127.0.0.1:8000/
   ```

## Configuration

### Adding Your Content

1. **Profile Image**: Replace the placeholder by adding your profile image as `static/img/profile.png`
2. **Resume**: Add your resume PDF as `media/resume.pdf`
3. **Contact Email**: Update the email address in `main/views.py` and `portfolio/settings.py`

### Email Configuration

For production, update the email settings in `portfolio/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Development

### TypeScript Development

To watch for TypeScript changes during development:
```bash
npm run dev
```

### Django Development

The Django development server automatically reloads when you make changes to Python files.

## Deployment

### Static Files

For production deployment, collect static files:
```bash
python manage.py collectstatic
```

### Environment Variables

Create a `.env` file for production settings:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
```

## Features Breakdown

### Sections

1. **Home**: Hero section with animated particles background
2. **About**: Personal summary and statistics
3. **Skills**: Technical skills organized by category
4. **Experience**: Professional experience timeline
5. **Projects**: Showcase of key projects with links
6. **Certificates**: Academic and professional certifications
7. **Contact**: Contact form and social links

### Interactive Elements

- Smooth scrolling navigation
- Mobile-responsive hamburger menu
- Animated particles background
- Scroll-triggered animations
- AJAX contact form
- Active navigation highlighting

### Accessibility

- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- High contrast black/white theme
- Responsive design for all devices

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🌐 Netlify Deployment

### Option 1: Drag & Drop Deployment

1. **Build the project**:
   ```bash
   npm run build
   ```

2. **Visit Netlify Deploy**: https://app.netlify.com/drop
3. **Drag and drop** the entire project folder to deploy instantly

### Option 2: Git Integration

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/Bhautik4318/BhautikGauswami.git
   git push -u origin main
   ```

2. **Connect to Netlify**:
   - Go to [Netlify](https://app.netlify.com/)
   - Click "New site from Git"
   - Choose your GitHub repository
   - Build settings are automatically configured via `netlify.toml`

### Option 3: Netlify CLI

1. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Login and Deploy**:
   ```bash
   netlify login
   npm run build
   netlify deploy --prod
   ```

### Static Version

The project includes a static `index.html` file that works without Django for easy Netlify deployment. The static version includes:
- All portfolio sections
- Particle animations
- Theme switching
- Responsive design
- Contact form (demo version)

## 📁 Deployment Files

- `index.html` - Static version for Netlify
- `netlify.toml` - Netlify configuration
- `package.json` - Build scripts
- `static/` - All CSS, JS, and images

## Contact

- **Email**: bhautikgosai4318@gmail.com
- **GitHub**: [Bhautikgauswami33](https://github.com/Bhautikgauswami33)
- **LinkedIn**: [Bhautik Gauswami](https://www.linkedin.com/in/bhautik-gauswami-921b54320/)

## License

This project is open source and available under the [MIT License](LICENSE).
