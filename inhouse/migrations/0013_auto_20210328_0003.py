# Generated by Django 3.1.5 on 2021-03-28 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inhouse', '0012_auto_20210327_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcomments',
            name='CommentCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobUpdates', to='inhouse.jobs'),
        ),
    ]