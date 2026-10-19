# MyHuduma: Public Service Request System

A mini eCitizen-style web application where citizens report public service
problems (broken streetlights, water issues, garbage collection) and officers
review, track and resolve them.

**Live demo:** https://public-service-request-system-mu.vercel.app/

## Table of contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Try the live demo](#try-the-live-demo)
- [Run it locally](#run-it-locally)
- [Deploy to Vercel](#deploy-to-vercel)
- [How the system works](#how-the-system-works)
- [Project structure](#project-structure)
- [Design decisions](#design-decisions)
- [Limitations](#limitations)
- [Future improvements](#future-improvements)

## Features

**Citizens**
- Register, log in and log out
- Submit a request with category, location, description and an optional photo
- View their own requests with a colour-coded status:
  Pending (yellow), In Progress (blue), Resolved (green)
- Email notification when the status of a request changes

**Officers (staff users)**
- Dashboard listing all requests from all citizens
- Search by location, description or citizen username
- Filter by status and category
- Update the status of any request (Pending, In Progress, Resolved)
- Analytics: total, open, pending, in progress and resolved counts,
  resolution rate, and a breakdown of requests by category
- Pagination (10 requests per page)

**General**
- Responsive Bootstrap 5 interface with a collapsing mobile menu
- Default categories created automatically (Streetlight, Water,
  Garbage Collection, Roads, Drainage)
- Friendly 403 page for users without permission

## Tech stack

| Part | Technology |
|---|---|
| Language and framework | Python 3.12+ (developed on 3.14), Django 6.1 |
| Database | SQLite locally, PostgreSQL (Neon) in production |
| Front end | Django templates, Bootstrap 5 |
| Image uploads | Pillow |
| Hosting | Vercel |

## Try the live demo

1. Open https://public-service-request-system-mu.vercel.app/
2. **As a citizen:** click Register, create an account, then use
   "New request" to submit a report and "My requests" to track it.
3. **As an officer:** log in with the officer account provided with the
   submission, then open **Dashboard** in the navigation bar. Citizens who
   open `/dashboard/` see a 403 page.

## Run it locally

Requirements: Python 3.12 or newer and Git.

```bash
git clone https://github.com/ouko-o/Public-Service-Request-System.git
cd Public-Service-Request-System

python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/

- `migrate` creates the database tables and the default categories.
- The superuser you create is a staff user, so it can open the Dashboard
  and `/admin/`.
- To make another user an officer, open `/admin/`, edit the user and tick
  **Staff status**.
- Without a `DATABASE_URL` setting the app uses a local SQLite file
  (`db.sqlite3`).
- **Emails:** by default they are printed in the terminal running the server
  (Django's console mailer). To send real emails, change the `MAILERS`
  setting in `config/settings.py`.

## Deploy to Vercel

Vercel detects Django automatically. It has no permanent disk, so the app
uses a hosted PostgreSQL database.

1. Push the project to GitHub and import the repository in Vercel.
2. Add these environment variables:

   | Variable | Value |
   |---|---|
   | `SECRET_KEY` | a long random string (never reuse the development key) |
   | `DEBUG` | `False` |
   | `DATABASE_URL` | added automatically when a Neon Postgres database is connected in Vercel's Storage tab |

3. Connect a Neon Postgres database to the project and redeploy.
4. Create the tables on the live database from your own computer, using the
   unpooled connection URL:

```bash
   set "DATABASE_URL=<your unpooled database url>"       # Mac/Linux: export DATABASE_URL="..."
   python manage.py migrate
   python manage.py createsuperuser
```

Every later push to the `main` branch redeploys the site automatically.

## How the system works

**Request lifecycle:** a citizen submits a request, which starts as
**Pending**. An officer reviews it on the dashboard and moves it to
**In Progress**, then **Resolved**. The citizen sees the new status on
**My requests** and an email notification is generated on each change.

**Pages**

| Address | Who can open it | Purpose |
|---|---|---|
| `/` | Everyone | Home page |
| `/register/` | Visitors | Create a citizen account |
| `/login/`, `/logout/` | Everyone | Sign in and out |
| `/requests/new/` | Logged-in users | Submit a service request |
| `/requests/` | Logged-in users | The user's own requests and their status |
| `/dashboard/` | Staff only | All requests, search, filters, analytics |
| `/dashboard/requests/<id>/status/` | Staff only (POST) | Update a request's status |
| `/admin/` | Staff only | Django admin site |

**Data model**

- `Category`: name of a type of problem (Streetlight, Water, ...)
- `ServiceRequest`: citizen (user), category, location, description,
  optional image, status (Pending / In Progress / Resolved),
  created and updated timestamps

## Project structure

```
config/                  Project settings and main URL routes
requests_app/
  models.py              Category and ServiceRequest models
  forms.py               Registration, login, request and status forms
  views.py               Page logic for citizens and officers
  decorators.py          staff_required access control
  analytics.py           Status counts and category breakdown queries
  notifications.py       Status-change email
  templates/             Base layout and all pages
  migrations/            Database tables and default categories
```

## Design decisions

- **Access control:** `@login_required` protects citizen pages, and a custom
  `@staff_required` decorator protects the dashboard (non-staff get a 403 page).
- **Data privacy:** citizens only ever query their own requests.
- **Safe input:** forms validate every field, including the status value.
  State-changing actions use POST requests with CSRF protection, and the
  post-update redirect only accepts addresses on the same site.
- **Performance:** `select_related` avoids repeated queries, and analytics
  use aggregate queries instead of looping in Python.
- **Separation of concerns:** analytics and notifications live in their own
  modules, and form styling is shared through one mixin.
- **Configuration through environment variables:** secret key, debug mode
  and database are read from the environment, so the same code runs locally
  and in production.

## Limitations

- **Photo uploads:** images are saved on the local disk, so they work when
  running locally but are not persisted on the Vercel demo, which has no
  permanent file storage. Requests without a photo work everywhere.
- **Emails:** the default mailer prints messages to the server log instead
  of delivering them. Real delivery needs a mail provider configured in
  `MAILERS`.
- There are no automated tests yet.

## Future improvements

- Cloud storage for photo uploads (for example an S3-compatible service)
- Real email delivery through an SMTP or API provider
- Status history for each request and officer comments
- SMS notifications and a map for request locations
- Automated tests for the main user flows

## Author

Edgar Odhiambo
