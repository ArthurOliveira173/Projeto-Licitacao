# Generated by Django 4.2.9 on 2024-06-26 18:10

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textEditor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
