# Generated by Django 4.1.3 on 2022-11-12 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
    ]