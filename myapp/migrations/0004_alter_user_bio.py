# Generated by Django 4.0.5 on 2022-06-28 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, default=None, max_length=200, null=True),
        ),
    ]