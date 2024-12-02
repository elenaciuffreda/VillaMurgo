# Generated by Django 4.2.16 on 2024-12-02 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homepage', '0004_recensione'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='utente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prenotazioni', to=settings.AUTH_USER_MODEL),
        ),
    ]
