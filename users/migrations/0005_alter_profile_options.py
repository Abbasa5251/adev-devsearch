# Generated by Django 3.2.5 on 2021-08-20 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['created'], 'verbose_name': 'profile', 'verbose_name_plural': 'profiles'},
        ),
    ]