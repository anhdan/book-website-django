# Generated by Django 3.2.12 on 2022-03-16 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_book_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('can_manage_author', 'Create, Update and Delete Author'),)},
        ),
    ]
