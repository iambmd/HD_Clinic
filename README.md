# HES Clinic – Phòng Khám Tai Mũi Họng Hữu Đức
### Full-Stack Bilingual Django Website

---

## Project Overview

A professional, bilingual (English/Vietnamese) clinic website for an ENT (Ear, Nose & Throat) specialty clinic in Hà Nội, Vietnam. Built with Django + Django REST Framework on the backend and vanilla JavaScript + Bootstrap 5 on the frontend.

**Clinic:** HES Clinic / Phòng Khám Tai Mũi Họng Hữu Đức
**Head Doctor:** Dr. Hong Son Bui (Bùi Hồng Sơn) – MS in ENT
**Phone:** +84 915 572 887
**Email:** huuducclinic@gmail.com
**Address:** BT Nam Cường, M04 - Lô 22, Khu A, P. Dương Nội, Hà Nội

---

## Project Structure

```
manage.py
requirements.txt
db.sqlite3                        SQLite database (dev)

hes_clinic/                       Django project package
├── settings.py                   Settings (env-driven secrets, i18n, DRF)
├── urls.py                       Root URL config
├── wsgi.py / asgi.py             Server entrypoints

clinic/                           Main Django app
├── models.py                     Service, Doctor, Article, Appointment, ContactMessage
├── views.py                      Page views
├── forms.py                      Appointment & contact forms
├── admin.py                      Admin panel registrations
├── urls.py                       Page URL routes
├── api_views.py                  DRF API views
├── api_urls.py                   API URL routes
├── serializers.py                DRF serializers
├── context_processors.py         Injects clinic contact info into templates
├── tests.py                      Page, form, API and i18n tests
├── migrations/
│   └── 0001_initial.py
└── management/commands/
    └── seed_data.py              Baseline services, doctors, articles

locale/
├── en/LC_MESSAGES/django.po      English catalogue (source language)
└── vi/LC_MESSAGES/django.po      Vietnamese catalogue (128 strings)

static/
├── css/main.css                  Full design system stylesheet
├── js/main.js                    Interactivity & animations
└── images/                       Static image assets

templates/
├── base.html                     Base layout (navbar, footer, lang toggle)
└── clinic/                       Page templates
    ├── home.html
    ├── about.html
    ├── services.html
    ├── news.html
    ├── article_detail.html
    ├── appointment.html
    ├── contact.html
    └── location.html

media/                            User-uploaded files (doctor photos, thumbnails)
```

---

## Quick Start

### 1. Prerequisites
- Python 3.10+
- GNU gettext tools (for translations)
  - Windows: [gettext-iconv binaries](https://mlocati.github.io/articles/gettext-iconv-windows.html)
  - Ubuntu: `sudo apt install gettext`

### 2. Create a virtual environment and install dependencies
```bash
python -m venv .venv
.venv\Scripts\activate         # Windows
source .venv/bin/activate      # macOS / Linux

pip install -r requirements.txt
```

### 3. Apply migrations
```bash
python manage.py migrate
```

### 4. Compile translations
```bash
python manage.py compilemessages
```

### 5. Load baseline data (optional)
```bash
python manage.py seed_data
```

Add `--admin-password <password>` to also create an `admin` superuser in the same step. Otherwise create one interactively:

```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000**.

---

## Pages

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

## REST API Endpoints

All endpoints are prefixed with `/api/`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/services/` | List all ENT services |
| GET | `/api/doctors/` | List all doctor profiles |
| GET | `/api/articles/` | List all articles |
| GET | `/api/articles/<slug>/` | Retrieve a single article |
| POST | `/api/appointments/` | Submit an appointment |
| POST | `/api/contact/` | Submit a contact message |

---

## Bilingual (i18n) System

- Language toggle in the navbar: **EN | VI**
- Uses Django's built-in `LocaleMiddleware` + `set_language` view
- Session-based language persistence across pages
- Translation files: `locale/en/LC_MESSAGES/django.po` and `locale/vi/LC_MESSAGES/django.po`

Interface strings come from the `.po` catalogues. Content strings (service names, articles, doctor bios) are stored bilingually in the database as `*_en` / `*_vi` column pairs, and resolved at render time by the `BilingualMixin` in `clinic/models.py`.

### To add new translatable strings
1. Add `{% trans "Your string" %}` in templates or `_("Your string")` in Python
2. Run `python manage.py makemessages -l en -l vi --ignore=.venv`
3. Fill in `msgstr` values in `locale/vi/LC_MESSAGES/django.po`
4. Run `python manage.py compilemessages`

Compiled `.mo` files are git-ignored — run `compilemessages` after every clone or pull.

---

## Database Models

| Model | Key Fields |
|-------|-----------|
| `Service` | title_en/vi, description_en/vi, icon, category (EAR/NOSE/THROAT) |
| `Doctor` | name, specialty, bio_en/vi, photo |
| `Article` | title_en/vi, content_en/vi, thumbnail, published_date, slug |
| `Appointment` | full_name, phone, email, preferred_date, preferred_time, branch, created_at |
| `ContactMessage` | name, phone, email, message, sent_at |

---

## Running Tests

```bash
python manage.py test
```

Covers page rendering, form submission and validation, the REST API, and the bilingual field resolution.

---

## Design System

- **Primary color:** Deep teal-blue (`#0a7ea4`)
- **Accent color:** Soft green (`#2db87c`)
- **Background:** Clean white + light blue-grey sections
- **Typography:** System UI / Segoe UI
- **Framework:** Bootstrap 5.3
- **Icons:** Bootstrap Icons 1.11

### UX Features
- Sticky navbar with hamburger on mobile
- Hero section with animated gradient background
- Service card hover effects
- Loading spinner on form submissions
- Floating "Call Now" button on mobile
- Scroll-reveal animations
- Counter animations on stats bar
- Auto-dismiss alert messages
- Honours `prefers-reduced-motion`

---

## Media Files

Doctor photos and article thumbnails upload to `media/doctors/` and `media/articles/`. The `media/` directory is git-ignored, so image files must be supplied per environment.

> **Note:** the seeded doctor record references `media/doctors/Bui_Hong_Son.jpg`, which is not in the repository. Drop the photo at that path, or clear the **photo** field in the admin, to avoid a broken image on the home and about pages.

---

## Production Checklist

Settings read from environment variables — set these rather than editing `settings.py`:

```bash
DJANGO_SECRET_KEY=<strong-random-value>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

Also:
- Set up a production database (PostgreSQL recommended)
- Run `python manage.py collectstatic`
- Configure a web server (Nginx + Gunicorn)
- Set up an HTTPS/SSL certificate
- Configure an email backend for appointment notifications
- Use a strong admin password

---

## Dependencies

```
django>=4.2,<5.0
djangorestframework>=3.14
pillow>=10.0
```

Install: `pip install -r requirements.txt`
