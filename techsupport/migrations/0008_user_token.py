# Generated by Django 3.2.12 on 2022-03-24 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techsupport', '0007_alter_tickets_assignedto'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=100, null=True, verbose_name='Last valid token'),
        ),
    ]
