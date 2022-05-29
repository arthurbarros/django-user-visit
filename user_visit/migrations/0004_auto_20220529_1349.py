# Generated by Django 3.1.7 on 2022-05-29 18:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_visit', '0003_uservisit_context'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uservisit',
            name='user',
        ),
        migrations.AddField(
            model_name='uservisit',
            name='user_cookie_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
