<<<<<<< HEAD
# MyHuduma: Public Service Request System

A mini eCitizen-style web application where citizens report public service
problems (broken streetlights, water issues, garbage collection) and officers
review, track and resolve them.

## Features

**Citizens**
- Register, log in and log out
- Submit a request with category, location, description and an optional photo
- View their own requests with colour-coded status (Pending, In Progress, Resolved)
- Receive an email when the status of a request changes

**Officers (staff users)**
- Dashboard listing all requests, with search and filters (status, category)
- Update the status of any request
- Analytics: total, open, pending, in progress and resolved counts,
  resolution rate and a breakdown by category
- Pagination for large numbers of requests

## Tech stack

- Python 3, Django
- SQLite database
- Bootstrap 5 for the interface
- Pillow for image uploads

## Setup

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

`migrate` also creates the default categories (Streetlight, Water,
Garbage Collection, Roads, Drainage).

## Using the system

1. **Citizen:** click Register, create an account, then use "New request".
2. **Officer:** the superuser created above is a staff user and sees the
   Dashboard link. To make another user an officer, open `/admin/`,
   edit the user and tick "Staff status".
3. **Emails:** by default, emails are printed in the terminal running the
   server (Django's console email backend). To send real emails, change the
   `EMAIL_*` settings in `config/settings.py`.

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
  Status changes use POST requests with CSRF protection.
- **Performance:** `select_related` avoids repeated queries, and analytics
  use one aggregate query instead of looping in Python.
- **Separation of concerns:** analytics and notifications live in their own modules.

## Limitations and future improvements

- Uses SQLite and the development server; a production deployment would
  need PostgreSQL, a production server and `DEBUG = False`.
- Emails use the console backend in development.
- Possible additions: status history per request, officer comments,
  SMS notifications and a map for request locations.

## Author

Edgar Odhiambo
=======
# MyHuduma: Public Service Request System

A mini eCitizen-style web application where citizens report public service
problems (broken streetlights, water issues, garbage collection) and officers
review, track and resolve them.

## Features

**Citizens**
- Register, log in and log out
- Submit a request with category, location, description and an optional photo
- View their own requests with colour-coded status (Pending, In Progress, Resolved)
- Receive an email when the status of a request changes

**Officers (staff users)**
- Dashboard listing all requests, with search and filters (status, category)
- Update the status of any request
- Analytics: total, open, pending, in progress and resolved counts,
  resolution rate and a breakdown by category
- Pagination for large numbers of requests

## Tech stack

- Python 3, Django
- SQLite database
- Bootstrap 5 for the interface
- Pillow for image uploads

## Setup

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

`migrate` also creates the default categories (Streetlight, Water,
Garbage Collection, Roads, Drainage).

## Using the system

1. **Citizen:** click Register, create an account, then use "New request".
2. **Officer:** the superuser created above is a staff user and sees the
   Dashboard link. To make another user an officer, open `/admin/`,
   edit the user and tick "Staff status".
3. **Emails:** by default, emails are printed in the terminal running the
   server (Django's console email backend). To send real emails, change the
   `EMAIL_*` settings in `config/settings.py`.

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
  Status changes use POST requests with CSRF protection.
- **Performance:** `select_related` avoids repeated queries, and analytics
  use one aggregate query instead of looping in Python.
- **Separation of concerns:** analytics and notifications live in their own modules.

## Limitations and future improvements

- Uses SQLite and the development server; a production deployment would
  need PostgreSQL, a production server and `DEBUG = False`.
- Emails use the console backend in development.
- Possible additions: status history per request, officer comments,
  SMS notifications and a map for request locations.

## Live Demo ##
- https://public-service-request-system-baxag1ena-dev-e38e.vercel.app/  

## Author

Edgar Odhiambo
>>>>>>> 73774e76834b01f064813bf3fb319f9224a56802

