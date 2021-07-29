# TrueHome Backend Challenge

https://github.com/vash512/truehome_challenge
https://vash-truehome-challenge.herokuapp.com
https://documenter.getpostman.com/view/4537189/TzscpmzF

# Business Requirements

Implement a CRUD with Django Rest Framework in which you can Add new activities, Reschedule, Cancel and List the activities.

**Requisitos**


- Add activities
    * Activities cannot be created if a Property is deactivated
    * Activities cannot be created on the same date and time (for the same property), taking into account that each activity must last a maximum of one hour.

- Reschedule activities
    * You can only modify the date on which the activity will take place
    * You cannot reschedule canceled activities.

- Cancel activities
    * You can only modify the status of the activity

- Activities list
    * The rule must be met: (current_date - 3 days) <= schedule <= (current_date + 2 weeks)
    * The response format must comply with the following
        - id
        - schedule
        - title
        - created_at
        - status
        - condition. The condition of the activity meets the following characteristics:
            * If the activity has an active status and the date on which the activity will be carried out is greater than or equal to the current date, then the condition is: Pending to be carried out
            * If the activity has an active status and the date on which it will take place is less than the current date, then the condition is: Overdue
            * If the activity has the status of done, the condition is: Finished
        - property
            - id
            - title
            - address
        - survey: As a link (URL) to the survey detail (it is not mandatory to program the survey detail)

    * Filters to consider (When filtering you should no longer follow the first rule)
        - Date range for schedule
        - Status

**Mandatory technical requirements**
- Versioning all changes to code with Git
- Use PostgreSQL as a database
- Use Django (version less than 2.x)

**Additional features**
- Create unit tests.
- Implement the API on a server (AWS, Heroku, DigitalOcean, etc)

---

# Main Solution

A project was created that satisfies the requested requirements through a REST API service, using a persistent database PostgreSQL, Bearer Authentication in the header, limiting the records and accesses only to the Authenticated users, implemented for testing in:

https://vash-truehome-challenge.herokuapp.com


# Implementation

Help guide for repository implementation.

Clone repository:

    git clone https://github.com/vash512/truehome_challenge

Requirements:

    python 3.x
    Django==1.11.29
    djangorestframework==3.11.2
    django-cors-headers==3.2.1
    gunicorn==20.1.0
    psycopg2==2.8.6

The github ignore already has the venv folder added, so it is recommended to create a virtual environment in the root of the repository, it requires python 3.x.

python3 as default:

    virtualenv venv

if you have multiple python:

    virtualenv venv -p = python3

turn on the virtual environment and requirements installation

    pip install -r requirements.txt


(Optional) Set the environment variables, the repository already has the default settings to be used with the SQLite database. But for greater compatibility it is necessary to use a PostgreSQL database configuration.

    SECRET_KEY
    DEBUG
    ALLOWED_MAIN_HOST
    POSGRESQL_DB: True to indicate that a postgres db will be occupied
    DB_NAME
    DB_USER
    DB_PASSWORD
    DB_HOST
    DB_PORT
    AUTH_PASSWORD_VALIDATORS: default False, if activated, password validators will be used
    STATIC_FILES_BY_DJANGO
    MEDIA_FILES_BY_DJANGO

Run migrations.

    python manage.py migrate

Default data can be loaded.

    python manage.py loaddata fixtures/auth.json
    python manage.py loaddata fixtures/property.json
    python manage.py loaddata fixtures/activity.json

(Optional) Create superuser.

    python manage.py createsuperuser

It is recommended to run the unit tests.

    python manage.py test

finally it can be run locally with.

    python manage.py runserver

For the implementation in heroku you can use the branch with the same name, which already has the appropriate settings..
    

# Urls available:

    /admin/
    /api/login/
    /api/property/
    /api/property/{{property_id}}/
    /api/activity/
    /api/activity/{{activity_id}}/

# /admin/

Classic Admin for data management by staff users.


# The endpoints are exemplified in the following link:

https://documenter.getpostman.com/view/4537189/TzscpmzF




# Tests

Object creation test and previously available services.

- [x] Unit Testing


        python manage.py test
