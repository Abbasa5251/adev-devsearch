# Generated by Django 3.2.5 on 2022-08-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_remove_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='projects/default.jpg', null=True, upload_to='projects/'),
        ),
    ]
