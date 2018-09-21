# Generated by Django 2.0.8 on 2018-09-18 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0026_auto_20180918_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_type',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='项目类型'),
        ),
        migrations.AddField(
            model_name='sample',
            name='bct_id',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='采血管编号'),
        ),
        migrations.AddField(
            model_name='sample',
            name='nation',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='民族'),
        ),
        migrations.AddField(
            model_name='sample',
            name='sample_use',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='样本用途'),
        ),
    ]
