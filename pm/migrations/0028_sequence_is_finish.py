# Generated by Django 2.0.8 on 2018-09-20 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0027_auto_20180918_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequence',
            name='is_finish',
            field=models.BooleanField(default=False, verbose_name='是否完成'),
        ),
    ]
