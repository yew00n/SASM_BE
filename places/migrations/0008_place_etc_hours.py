# Generated by Django 4.0 on 2022-08-13 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0007_place_left_coordinate_place_right_coordinate'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='etc_hours',
            field=models.TextField(default=0, max_length=500),
            preserve_default=False,
        ),
    ]