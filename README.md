# HES Clinic – Phòng Khám Tai Mũi Họng Hữu Đức
### Full-Stack Bilingual Django Website

---

## 📋 Project Overview

A professional, bilingual (English/Vietnamese) clinic website for an ENT (Ear, Nose & Throat) specialty clinic in Hà Nội, Vietnam. Built with Django + Django REST Framework on the backend and vanilla JavaScript + Bootstrap 5 on the frontend.

**Clinic:** HES Clinic / Phòng Khám Tai Mũi Họng Hữu Đức  
**Head Doctor:** Dr. Hong Son Bui (Bùi Hồng Sơn) – MS in ENT  
**Phone:** +84 915 572 887  
**Email:** huuducclinic@gmail.com  
**Address:** BT Nam Cường, M04 - Lô 22, Khu A, P. Dương Nội, Hà Nội

---

## 🗂️ Project Structure

```
hes_clinic/               ← Django project settings
clinic/                   ← Main Django app
│   ├── models.py         ← DB models (Service, Doctor, Article, Appointment, Contact)
│   ├── views.py          ← Page views
│   ├── forms.py          ← Django forms
│   ├── admin.py          ← Admin panel registrations
│   ├── urls.py           ← App URL routes
│   ├── api_views.py      ← DRF API views
│   ├── api_urls.py       ← API URL routes
│   └── serializers.py    ← DRF serializers
locale/
│   ├── en/LC_MESSAGES/   ← English .po/.mo files
│   └── vi/LC_MESSAGES/   ← Vietnamese .po/.mo files
static/
│   ├── css/main.css      ← Full design system stylesheet
│   ├── js/main.js        ← Interactivity & animations
│   └── images/           ← Static image assets
templates/
│   ├── base.html         ← Base layout (navbar, footer, lang toggle)
│   └── clinic/           ← Page templates
│       ├── home.html
│       ├── about.html
│       ├── services.html
│       ├── news.html
│       ├── article_detail.html
│       ├── appointment.html
│       ├── contact.html
│       └── location.html
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- pip
- GNU gettext tools (`sudo apt install gettext` on Ubuntu)

### 2. Install dependencies
```bash
pip install django djangorestframework pillow
```

### 3. Apply migrations
```bash
python manage.py migrate
```

### 4. Compile translations
```bash
python manage.py compilemessages
```

### 5. Load sample data (optional)
```bash
python manage.py loaddata clinic_sample_data  # if fixture exists
# OR run the setup script:
python setup_sample_data.py
```

### 6. Create admin superuser
```bash
python manage.py createsuperuser
# Default dev credentials (change in production!):
# Username: admin  |  Password: admin1234
```

### 7. Collect static files
```bash
python manage.py collectstatic
```

### 8. Run development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser.

---

## 📄 Pages

| URL | Description |
|-----|-------------|
| `/` | Home – hero, stats, services overview, doctor, news |
| `/about/` | Clinic history, mission, doctor profiles |
| `/services/` | ENT services grouped by Ear / Nose / Throat |
| `/news/` | Blog-style health articles |
| `/news/<slug>/` | Article detail page |
| `/appointment/` | Appointment booking form |
| `/contact/` | Contact form + clinic info |
| `/location/` | Embedded Google Maps + address |
| `/admin/` | Django admin panel |

---

## 🌐 REST API Endpoints

All endpoints are prefixed with `/api/`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/services/` | List all ENT services |
| GET | `/api/doctors/` | List all doctor profiles |
| GET | `/api/articles/` | List all articles |
| POST | `/api/appointments/` | Submit an appointment |
| POST | `/api/contact/` | Submit a contact message |

---

## 🌏 Bilingual (i18n) System

- Language toggle in the navbar: 🇬🇧 EN | 🇻🇳 VI
- Uses Django's built-in `LocaleMiddleware` + `set_language` view
- Session-based language persistence across pages
- Translation files: `locale/en/LC_MESSAGES/django.po` and `locale/vi/LC_MESSAGES/django.po`

### To add new translatable strings:
1. Add `{% trans "Your string" %}` in templates or `_("Your string")` in Python
2. Run `python manage.py makemessages -l en -l vi`
3. Fill in `msgstr` values in the `.po` files
4. Run `python manage.py compilemessages`

---

## 🗄️ Database Models

| Model | Key Fields |
|-------|-----------|
| `Service` | title_en/vi, description_en/vi, icon, category (EAR/NOSE/THROAT) |
| `Doctor` | name, specialty, bio_en/vi, photo |
| `Article` | title_en/vi, content_en/vi, thumbnail, published_date, slug |
| `Appointment` | full_name, phone, email, preferred_date, preferred_time, branch |
| `ContactMessage` | name, phone, email, message, sent_at |

---

## 🎨 Design System

- **Primary color:** Deep teal-blue (`#0a7ea4`)
- **Accent color:** Soft green (`#2db87c`)
- **Background:** Clean white + light blue-grey sections
- **Typography:** System UI / Segoe UI
- **Framework:** Bootstrap 5.3
- **Icons:** Bootstrap Icons 1.11

### UX Features
- ✅ Sticky navbar with hamburger on mobile
- ✅ Hero section with animated gradient background
- ✅ Service card hover effects
- ✅ Loading spinner on form submissions
- ✅ Floating "Call Now" button on mobile
- ✅ Scroll-reveal animations
- ✅ Counter animations on stats bar
- ✅ Auto-dismiss alert messages

---

## ⚙️ Production Checklist

Before going live, update these settings in `hes_clinic/settings.py`:

```python
DEBUG = False
SECRET_KEY = 'your-strong-random-secret-key-here'
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

Also:
- Set up a production database (PostgreSQL recommended)
- Configure a web server (Nginx + Gunicorn)
- Set up HTTPS/SSL certificate
- Configure email backend for notifications
- Change admin password from default

---

## 📦 Dependencies

```
django>=4.2
djangorestframework>=3.14
pillow>=10.0
```

Install: `pip install -r requirements.txt`
