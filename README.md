# book-website-django

## Working procedure

### 1. Initialize Django prject

** Start a new project **

```
workon django_env_name
django-admin startproject project_name .
tree
python3 manage.py runserver
```

** Create a new app **

```
python3 manage.py startapp app_name
```

** Register the app to the project **

  - Apps are registered by adding them to the **INSTALL_APPS** list in the project setting
  - The project setting resides in the path "project_name/setting.py"

**Hooking up the URL mapper**

  - URL mappings are managed through `urlpatterns` variable, which is a Python list of `path()` functions.
  - Each `path()` either associates a URL pattern to a *specific view*, or with another list of URL pattern testing code.
  - Add app to */project_name/urls.py*:

``` python
from django.urls import include

urlpatterns += [
   path('app_name/', include('app_name.urls')),
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

**Running database migration **
  - Django uses an Object-Relational-Mapper (ORM) to map model definitions in the Django code to the data structures used by the underlying database.
  - Changing model definition triggers automatic migration of the underlying data structure in the database tp match the model. (via scripts in */app_name/migrations/*)
  - Run first migration to migrate admin models

```
python3 manage.py makemigrations #creates but does not apply migration for all installed app in the project
python3 manage.py migrate #apply the migrations to the database.
```

  - *Node: Re-run migrations and re-test site whenerver making significant changes*


