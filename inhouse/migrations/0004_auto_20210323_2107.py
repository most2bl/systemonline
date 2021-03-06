# Generated by Django 3.1.5 on 2021-03-23 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inhouse', '0003_auto_20210323_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobs',
            old_name='jobEduLevel',
            new_name='jobUniversity',
        ),
        migrations.RemoveField(
            model_name='jobs',
            name='jobScannedDocs',
        ),
        migrations.AlterField(
            model_name='casecomments',
            name='caseCommentWriter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caseCommentOwner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jobcomments',
            name='JobCommentWriter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobCommentOwner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='JobResponsible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hr', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobCV',
            field=models.FileField(upload_to='inhouse'),
        ),
        migrations.DeleteModel(
            name='Experience',
        ),
    ]
