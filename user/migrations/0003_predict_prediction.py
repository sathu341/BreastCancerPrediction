# Generated by Django 3.2 on 2022-01-29 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_predict'),
    ]

    operations = [
        migrations.AddField(
            model_name='predict',
            name='prediction',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
