# Lesson 1: Working procedure

## 1. Initialize Django 1eb project and app

### 1.1 Start a new project

```
workon django_env_name
django-admin startproject project_name .
tree
python3 manage.py runserver
```

### 1.2. Create a new app

```
python3 manage.py startapp app_name
```
<br>

## 2. Activate the app for developement

### 2.1. Register the app to the project

  - Apps are registered by adding them to the **INSTALL_APPS** list in the project setting
  - The project setting resides in the path "project_name/setting.py"

``` python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # syntax for registering new app
    'app_name.apps.CatalogConfig' # class in app_name/apps.py
]
```

### 2.2. Hooking up the URL mapper

  - URL mappings are managed through `urlpatterns` variable, which is a Python list of `path()` functions.
  - Each `path()` either associates a URL pattern to a *specific view*, or with another list of URL pattern testing code.
  - Add app to */project_name/urls.py*:

``` python
from django.urls import include

urlpatterns += [
   path('app_name/', include('app_name.urls')), # app_name.urls is defined in app_name/urls.py
]
```

  - Redirect homepage to the app if need:

``` python
from django.views.generic improt RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='app_name/', permanent=True)),
]
```

  - Create file **urls.py** inside *app_name* folder to add further patterns for this app view.

``` python
from django.urls import path, include
from . import views

urlpatterns = [
]
```

### 2.3. Running database migration
  - Django uses an Object-Relational-Mapper (ORM) to map model definitions in the Django code to the data structures used by the underlying database.
  - Changing model definition triggers automatic migration of the underlying data structure in the database tp match the model. (via scripts in */app_name/migrations/*)
  - Run first migration to migrate admin models

``` sh
$ python3 manage.py makemigrations #creates but does not apply migration for all installed app in the project
$ python3 manage.py migrate #apply the migrations to the database.
```

  - *Node: Re-run migrations and re-test site whenerver making significant changes*


