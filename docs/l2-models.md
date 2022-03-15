# Lesson 2: Models

## 2.1. Model definition

- **Step 1**: Figure out what types of object is need to store information creating by the app.
- **Step 2**: Draw the UML class diagram to show classes properties and relationship among them. Some common relationships:
    - OneToOneField
    - ForeignKey
    - OneToManyField
    - ManyToManyField
- **Step 2**: Implement models using Python class in the file *app_name/models.py*
  - All models must inherit `django.db.models.Model` and can include 3 fields:
    - **field**: data field/model class attributes. Types of fields:      
    - **methods**: model functions to be called for data manipulation.
    - **meta data**:  give some useful information on how data records are organized, controled access, abstracted. Commonly:

``` python
class Meta:
    ordering = ['field_name_1', '-field_name_2', ...]
    verbose_name = "Human readable model name"
```

<br>

### Common Types of Field

- `models.CharField`: short-to-mid size text.
- `models.TextField`: long text.
- `models.IntegerField`: integer.
- `models.DateField/DateTimeField`: Date/DateTime
- `models.EmailField`: email field (both storing and validating)
- `models.FileField` & `models.ImageField`: file/image (there is validation with image)
- `models.AutoField`: automatically increased integer.
- `models.ForeignKey`: specify on-to-many relationship. The 'one' class is define as ForeignKey field in the 'many' class.
- `model.ManyToManyField`: specify many-to-many relationship.

<br>

### Common Argument of Field

- `help_text`: text description for HTML forms.
- `verbose_name`: field labels for HTML forms. If not specified, deduced from field name.
- `default`: field default value.
- `null`: accept `NULL` value if `True`. Default `False`.
- `blank`: accept blank field if `True`. Default `False`.
- `choices`: a group of choices define in a tuple.
- `primary_key`: set to be model primary key if `True`.

<br>

### Common Types of Method

- Minimally, every model should define `__str__()` method to return human-readable string for each object.

``` python
def __str__(self):
    return self.field_name
```

- Method that returns a URL for displaying an individual model record on the website. If defined, Django automatically add button **"View on Site"** to the model's record editing screens in the Admin site.

``` python
def get_absolute_url(self):
    return reverse('model-detail-view`, arfs=[str(self.id)])
    # model-detail-view is a Python class that will do the work required to display the records with id=self.id
    # reverse() functions create the detail view page URL corresponding to the specific record to be displayed.
```

<br>

### Model Management

- **Creating and modifying records**: Create a new record with model constructor and save it which `.save()` method.

``` python
record = ModelName(field_name_1=value_1, field_name_2=value_2, ...)
record.field_name = value
print( record.field_name )
record.save()
```

- **Search for records**: 
  - Get all records: `all_records = ModelName.objects.all()`
  - Search for group of records: `filtered_records = ModelName.objects.filter(field_name__match_type='search_keyword')`.
  - `__match_type` includes:
    - `contains`: value of `field_name` contains case-sensitive `'search_keyword'`.
    - `icontains`: similar to to `contains`, except being case-insensitive.
    - `exact` & `iexact`: value of `field_name` case-sensitive and case-insensitive matches exactly `'search_keyword'`, respectively.
    - etc.



<br>

## 2.2. Registering models

- Register models of an app in file */app_name/admin.py* by calling function `admin.site.register()`

``` python
from .model import ModelName1, ModelName2, ..., ModelNameN

admin.site.register(ModelName1)
admin.site.register(ModelName2)
...
admin.site.register(ModelNameN)
```
<br>

## 2.3. Create superuser for site administration

```
python3 manage.py createsuperuser
```

- Use this superuser to login to admin site, so as to manage site's data.

<br>
 