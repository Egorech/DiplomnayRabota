# Generated by Django 4.2.6 on 2023-10-10 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0002_spectask_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='link',
            new_name='domain',
        ),
        migrations.RemoveField(
            model_name='product',
            name='article',
        ),
    ]
