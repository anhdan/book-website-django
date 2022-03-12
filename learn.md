# Lesson 2: Models

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
