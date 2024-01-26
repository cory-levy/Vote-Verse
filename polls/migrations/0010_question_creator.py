# Generated by Django 4.2.5 on 2024-01-26 02:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_rename_sf_symbol_gender_emoji'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
