# Generated by Django 4.0.1 on 2022-04-01 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customsession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile-pic-3.png', upload_to='profile-images'),
        ),
    ]