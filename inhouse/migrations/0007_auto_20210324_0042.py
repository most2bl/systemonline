# Generated by Django 3.1.5 on 2021-03-24 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inhouse', '0006_auto_20210323_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='caseScannedDocs',
            field=models.FileField(upload_to='case/'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobCV',
            field=models.FileField(upload_to='cv/'),
        ),
    ]