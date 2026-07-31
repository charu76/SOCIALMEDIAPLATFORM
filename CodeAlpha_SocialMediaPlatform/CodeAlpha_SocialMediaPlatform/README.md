# CodeAlpha_SocialMediaPlatform

Mini social media web app built with **Django** (backend) and **HTML/CSS** (frontend), fulfilling CodeAlpha Task 2.

## Features
- User registration & login (Django auth)
- User profiles with bio + avatar
- Create / view / delete posts (text + optional image)
- Comment on posts, delete your own comments
- Like / unlike posts
- Follow / unfollow other users
- Feed showing posts from people you follow
- Explore page to discover other users' posts
- Follower / following lists
- Django admin panel for managing all data

## Tech stack
- Python 3 + Django 6
- SQLite (default, zero-config database)
- Pillow (image uploads)
- Server-rendered HTML/CSS (no build step needed)

## Project structure
```
CodeAlpha_SocialMediaPlatform/
├── manage.py
├── requirements.txt
├── socialproj/        # project settings, root urls
└── core/               # the app: models, views, forms, templates, static
    ├── models.py        # Profile, Post, Comment, Like, Follow
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── signals.py       # auto-creates a Profile when a User is created
    ├── templates/core/
    ├── templates/registration/
    └── static/core/style.css
```

## Setup & run locally

```bash
# 1. Create & activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. (Optional) create an admin account
python manage.py createsuperuser

# 5. Run the dev server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** to sign up and start posting.
Visit **http://127.0.0.1:8000/admin/** to manage data as superuser.

## Database
Uses SQLite by default (`db.sqlite3`, created automatically on first `migrate`). Models:
- **Profile** – 1:1 with User (bio, avatar)
- **Post** – author, content, optional image
- **Comment** – post, author, content
- **Like** – unique per (post, user)
- **Follow** – unique per (follower, following)

## Notes
- This is a learning/demo project intended to satisfy the CodeAlpha Full Stack Development internship Task 2 (Social Media Platform) requirements: user profiles, posts & comments, like/follow system.
- For production use you'd want to set `DEBUG=False`, configure `ALLOWED_HOSTS`, use a production database (Postgres), serve static/media via a proper storage backend, and set a fresh `SECRET_KEY` via environment variable.
