# Generated by Django 4.0.4 on 2022-05-31 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0002_alter_favorites_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorites',
            old_name='book',
            new_name='books',
        ),
    ]
