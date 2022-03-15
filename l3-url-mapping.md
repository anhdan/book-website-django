# Lesson 3: Full flow of displaying a webpage


![Django architecture](resource/basic-django.png)


<br>

## 3.1. Defining resource URL

- `resource_container_name/`: overview of and links to all available resources (data models) in the web app. E.g. `catalog/`
- `resource_container_name/a_resource_list/`: list all instances of a resource (a data model). E.g. `catalog/books`, `catalog/authors`, etc.
- `resource_container_name/a_resource_instance/<id>`: detail view of an instance (an object) of a resource (a data model). E.g. `catalog/book/1` show detail of the book record with id=1 in the books table database.
- `resource_container_name/a_resource_list/?page=x`: show page number `x`th of a resource list in case of pagination.

<br>

## 3.2. URL mapping

The URL mapper will extract the encoded information and pass it to the view, and the view will dynamically determine what information to get from the database.

<br>

### 3.2.1. Link to app urls.py from project urls.py

``` python
# in "project_folder/urls.py"
from django.urls import include
urlspatterns += [
  path( 'app_name/', include(app_name.urls)) # point to "app_name/urls.py" file
]
```

<br>

### 3.2.2. Connect a view function/class with resource URL in app_name/urls.py

``` python
from . import view #import views.py

### Connect function-based view to a url pattern
#
# func_showing_resource_list(): a function defined in app_name/views.py what will be called when a request url string match the pattern 'app_name/a_resource_list/'
urlpatterns += [
  path( 'a_resource/', views.func_showing_resource, name='a_resource')
]


### Connect class-based view to a url pattern
#
# ResourceListView: A user-defined class in app_name/views.py to provides the view to all instances of a resource in the database
# ResourceDetailView: A user-defined class in app_name/views.py to provides detail view to a specific instance of a resource in the DB, indentified by 'pk'
urlpatterns += [
  path( 'a_resource_list/', views.ResourceListView.as_view(), name='resources')
  path( 'a_resource/<int:pk>', views.ResourceDetailView.as_view(), name='resource-detail')
]
```

<br>

## 3.3. Define the View

- View could be a function (**function-based view**) or a class (**class-based view**)
- view functions/classes are defined in *'app_name/views.py'*

<br>

### 3.3.1. Function-based view

``` python
def func_showing_resource(request):
  
  #TODO: Query database via Models to create context data
  context_data_1 = ...
  context_data_2 = ...
  ...
  context_data_n = ...

  # Wrap context data in a dictionary to bypass to an HTML file, which is responsible for the layout of the page showing the above data.
  context = {
    'context_data_1' : context_data_1,
    'context_data_2' : context_data_2,
    ...
    'context_data_n' : context_data_n,
  }

  # Render the HTML template an_html_template.html with the data in the context variable
  return render(request, 'an_html_template.html', context=context)
```

<br>

### 3.3.2. Class-based view

**For viewing list of all instance of a rersource (a model)**

``` python
from django.views import generic
from .models import [list of model names]

class ResourceListView(generic.ListView):
  model = ResourceModel # ResourceModel is model class defined in 'app_name/models.py'
```

**For viewing details of a specific instance of a resource**

``` python
from django.views import generic
from .models import [list of model names]

class ResourceListView(generic.DetailView):
  model = ResourceModel # ResourceModel is model class defined in 'app_name/models.py'
```

<br>

## 3.4. Templating

A template is a text file that defines the structure or layout of a file (such as an HTML page), it uses placeholders to represent actual content.


<br>

### 3.4.1. Location of templates file
- app index page template is defined in *'app_name/templates'* folder
- app resource view pages templates are defined in *'app_name/templates/app_name/template_for_a_resource.html'*
- **base_generic.html**: a base template file  in *'app_name/templates/*' defining layout for common components shared among all web pages (e.g. header, sidebar, navigations)
- CSS styles are located in *'app_name/static/css/'* folder.
- template files location is customizable via specifying `DIRS` in the `TEMPLATE` variable in the file *'project_folder/setting.py'*

``` python 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

<br>

### 3.4.2. Template inheritance

**base template vs extended template**

- base template defines basic and reuseable components which are shared among multile web pages. e.g. navigation, header, footer, sidebar.
- extended template has part of it layout from a base template, then either 
  - appending its own layout to show extra info or,
  - override a block in base template to show its own content.

- extending syntax (in extended template):

``` html
<!-- Copy base template layout -->
{% extends "base_template.html" %}

<!-- Override a reuseable block -->
{% block block_name %}
  <!-- Overriding content -->
{% endblock %}

<!-- Appending with own layout -->
```

**block**

- define a reusable section in a base template to be shared among many webpage.  

``` html
{% block block_name %}
<!-- default block content (typically empty) -->
{% endblocl %}}
```

- overide a block in an extended template (an example)

``` html
{% block block_name %}
  <h1>Local Library Home</h1>
  <p>Welcome to LocalLibrary, a website developed by <em>Mozilla Developer Network</em>!</p>
{% endblock %}
```

### 3.4.3 Variable and control in template

**variable**

- syntax: `{{ variable_name}}`
- they are placeholders to dynamic data bypassed in from a view render function or class.
- the variable name is either
  - exactly the key of a key/value entry in the context variable defined in a view function. E.g. 

``` python
# in app_name/views.py
# view function func_showing_resource()
def func_showing_resource(request):
  ...
  context = {
    'context_data_1' : context_data_1
  }

  render( request, 'index.html', context=context)
```

``` html
<!-- In app_name/templates/index.html -->
<p>conext_data_1 value is: {{ context_data_1 }}<p>
```
  - a field name of the model in the view class

``` python
# in app_name/views.py
# view class BookListView
def BookListView(generic.ListView):
  model = Book
```

``` html
<!-- In app_name/templates/app_name/book_list.html -->
{% for book in book_list %}
  <li>
    <a href="{{ book.get_absolute_url }}">{{ book.title }}</a> ({{book.author}})
  </li>
{% endfor %}
```

*Note:*

- *General naming for listview placeholder variable is `model_name_list` (e.g. `book_list` since `Book` model name is `"book"`)*
- *General naming for an instance placeholder variable in list is `model_name` (e.g. `book`)*


**Control**

``` html
<!-- For loop-->
{% for <instance_var> in <list_var> %}
  <!-- do some thing with that instance -->
  <!-- generate html to display result -->
{% endfor %}
```

``` html
<!-- Conditional -->
{% if <condition_formular> %}
  <!-- code here to list the books -->
{% else %}
  <p>There are no books in the library.</p>
{% endif %}
```