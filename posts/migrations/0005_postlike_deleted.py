# Generated by Django 5.2.1 on 2025-06-10 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_postlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlike',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
