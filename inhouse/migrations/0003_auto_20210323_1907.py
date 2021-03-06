# Generated by Django 3.1.5 on 2021-03-23 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inhouse', '0002_auto_20210322_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='caseResponsible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsible', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cases',
            name='caseScannedDocs',
            field=models.FileField(upload_to='inhouse'),
        ),
        migrations.AlterField(
            model_name='person',
            name='nationaldExpiryDate',
            field=models.CharField(max_length=32),
        ),
    ]
