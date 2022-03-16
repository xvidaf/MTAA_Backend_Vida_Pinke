# Generated by Django 3.2.12 on 2022-03-16 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('techsupport', '0005_alter_devices_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessages',
            name='message',
            field=models.CharField(default='Message', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='devices',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='techsupport.media'),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Image', to='techsupport.media'),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='solutionText',
            field=models.CharField(blank=True, max_length=10000, null=True, verbose_name='Text of the solution'),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='solutionVideo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solutionVideo', to='techsupport.media'),
        ),
    ]
