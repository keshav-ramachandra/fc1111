# Generated by Django 3.2.7 on 2021-10-14 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_auto_20211014_1803'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='user_name',
        ),
    ]
