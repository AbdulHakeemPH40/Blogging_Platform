# Generated by Django 5.0.6 on 2024-08-15 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpanel', '0002_user_table_blocked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_table',
            old_name='blocked',
            new_name='is_blocked',
        ),
    ]
