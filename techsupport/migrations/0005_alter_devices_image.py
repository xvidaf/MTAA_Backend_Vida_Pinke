# Generated by Django 3.2.12 on 2022-03-16 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('techsupport', '0004_auto_20220316_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='techsupport.media'),
        ),
    ]
