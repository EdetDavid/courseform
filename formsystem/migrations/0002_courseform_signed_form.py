# Generated by Django 5.0.8 on 2024-08-09 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formsystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseform',
            name='signed_form',
            field=models.FileField(blank=True, null=True, upload_to='signed_course_forms/'),
        ),
    ]
