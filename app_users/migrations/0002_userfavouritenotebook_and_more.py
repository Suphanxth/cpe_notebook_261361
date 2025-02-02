# Generated by Django 5.0.1 on 2024-02-27 09:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_notebooks', '0004_notebook_image_relative_url'),
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavouriteNotebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.SmallIntegerField(choices=[(1, 'ต้องอ่านด่วนๆ'), (2, 'อ่านตอนว่าง'), (3, 'บันทึกไว้ก่อน')], default=3)),
                ('notebook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourited_user_pivot_set', to='app_notebooks.notebook')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_notebook_pivot_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='favourite_notebook_set',
            field=models.ManyToManyField(related_name='favourited_user_set', through='app_users.UserFavouriteNotebook', to='app_notebooks.notebook'),
        ),
    ]
