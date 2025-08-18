# Ivy Verse — Modern Blogging Platform (Django)

A Django 5.2 project that delivers a clean, JWT‑secured blogging experience with rich‑text editing, media hosting via Cloudinary, and a custom user model using email‑based authentication.

## Tech Stack
- **Backend**: Django, Django REST Framework, SimpleJWT
- **Auth**: JWT (HttpOnly cookies), Custom User (email as username)
- **Editor**: CKEditor (rich text)
- **Storage**: Cloudinary (images/files)
- **DB**: PostgreSQL
- **Other**: CORS Headers, python‑decouple

## Features
- **Email-based authentication** with JWT stored in HttpOnly cookies
- **Custom User** with profile image, bio, and soft‑delete
- **Blog posts** with CKEditor content, featured image, and file attachments
- **Engagement**: likes, dislikes, read count tracking
- **Comments** with admin approval workflow
- **Admin Dashboard** for posts, comments, and users (custom views + Django Admin)
- **JWT middleware**: reads tokens from cookies and sets `request.user`

## Project Structure
```
ivy_verse/
├─ adminapp/           # Admin-facing HTML views for content/user moderation
├─ authentication/     # Signup/login/logout, forms, custom user model, JWT cookie utils
├─ blogs/              # Post listing/detail, comments, like/unlike, read logs
├─ core/               # JWT cookie auth middleware, auth decorators
├─ ivy_verse/          # Project settings, URLs, WSGI/ASGI
└─ manage.py
```

## Getting Started

### 1) Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Cloudinary account (for media)

### 2) Clone and setup
```bash
# clone your repository
git clone <your-repo-url>
cd ivy_verse

# create and activate virtual environment
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

# install dependencies
pip install -r requirements.txt
```

### 3) Environment variables
Create a `.env` file inside `ivy_verse/ivy_verse/` with:
```env
# Core
SECRET_KEY=your-django-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_NAME=ivy_verse_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432

# Cloudinary
CLOUD_NAME=your_cloud_name
API_KEY=your_cloudinary_key
API_SECRET=your_cloudinary_secret
```

### 4) Database and run
```bash
python manage.py migrate
python manage.py createsuperuser  # optional but recommended
python manage.py runserver
```

- App home (redirects to login): `/`
- Django Admin: `/admin/`

## Key URLs

### Authentication
- `POST /api/auth/signup/` — register user
- `POST /api/auth/login/` — login; sets `access_token` and `refresh_token` cookies
- `GET  /api/auth/user_logout` — logout; clears cookies

Notes:
- Access token lifetime: 60 minutes
- Refresh token lifetime: 7 days (rotation + blacklist enabled)
- Tokens stored in HttpOnly cookies; middleware reads `access_token` and sets `request.user`

### Blogs
- `GET  /api/blogs/user_home/` — user feed (published posts)
- `GET  /api/blogs/post_detail/<id>/` — post detail + tracks reads
- `POST /api/blogs/comment-create/<id>/` — create comment
- `POST /api/blogs/like/<id>/` — like
- `POST /api/blogs/unlike/<id>/` — unlike

### Admin (custom dashboard)
- `GET  /api/admin/admin_posts/` — list/manage posts
- `GET|POST /api/admin/admin_create_post/` — create post (CKEditor)
- `GET|POST /api/admin/admin_edit_post/<id>/` — edit post
- `POST /api/admin/admin_delete_post/<id>/` — soft delete
- `GET  /api/admin/admin_comments/` — pending/approved comments
- `POST /api/admin/admin_approve_comment/<id>/` — approve comment
- `GET  /api/admin/admin_users/` — list users
- `POST /api/admin/admin_edit_user/<id>/` — edit user
- `POST /api/admin/admin_delete_user/<id>/` — soft delete

All admin endpoints require a superuser (checked via decorators and middleware).

## Security Considerations
- **JWT in HttpOnly cookies**: mitigates XSS token theft; in production set cookie `Secure`/`SameSite`/domain
- Configure **CORS** and **CSRF** for your deployment
- Refresh tokens rotate and are blacklisted after rotation (enabled)

## Media and Rich Text
- **CKEditor** provides rich text editing for posts (uploads to `uploads/`)
- **Cloudinary** stores images/files via `cloudinary_storage`

## Configuration Highlights
- **AUTH_USER_MODEL**: `authentication.CustomUser` (email as `USERNAME_FIELD`)
- **Middleware**: `core.middleware.JWTAuthMiddleware` sets `request.user` from cookie JWT
- **Decorators**: `jwt_required`, `superuser_required` to protect views
- **Static/Media**: `MEDIA_URL` at `/media/`, Cloudinary as default file storage

## Deployment Notes
1. Set `DEBUG=False` and configure `ALLOWED_HOSTS`
2. Add `STATIC_ROOT` (e.g., `BASE_DIR / "staticfiles"`) and run `python manage.py collectstatic`
3. Serve via a production WSGI server (e.g., gunicorn/uvicorn + nginx)
4. Use HTTPS so cookies can be marked `Secure`
5. Ensure PostgreSQL and Cloudinary credentials are production‑ready

## Useful Commands
- Install deps: `pip install -r requirements.txt`
- Migrations: `python manage.py makemigrations && python manage.py migrate`
- Superuser: `python manage.py createsuperuser`
- Run dev server: `python manage.py runserver`

## License
Add your preferred license (e.g., MIT).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.