# Generated by Django 3.2.5 on 2021-08-20 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_project_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=200, verbose_name='title'), max_length=200, verbose_name='slug'),
        ),
    ]