# Generated by Django 4.0.3 on 2022-03-28 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techsupport', '0008_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='path',
            field=models.FileField(max_length=255, upload_to='files/', verbose_name='Path to the media'),
        ),
    ]
