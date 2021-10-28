# Generated by Django 3.2.7 on 2021-10-15 01:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodType',
            fields=[
                ('food_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('food_type', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('restaurant_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('website', models.URLField(blank=True, max_length=500)),
                ('contact', models.PositiveBigIntegerField(default=0)),
                ('address', models.TextField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('food_image_url', models.URLField(blank=True)),
                ('approve_status', models.BooleanField(default=False)),
                ('food_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.foodtype')),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.restaurant')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_id', 'post_id')},
            },
        ),
    ]
