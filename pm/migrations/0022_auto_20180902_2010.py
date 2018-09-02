# Generated by Django 2.0.8 on 2018-09-02 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0021_auto_20180902_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bioinfo',
            name='error_rate',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='mapped_bases',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='mapped_reads',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='pass_bases',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='pass_dir',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='pass_reads_avg',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='pass_reads_avg_score',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='pass_reads_median',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='pass_reads_n50',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='pass_total_reads',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='raw_dir',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='total_bases',
        ),
        migrations.RemoveField(
            model_name='bioinfo',
            name='total_reads',
        ),
        migrations.AddField(
            model_name='sequence',
            name='library_kit',
            field=models.CharField(max_length=50, null=True, verbose_name='建库试剂盒'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='library_size',
            field=models.CharField(max_length=50, null=True, verbose_name='建库大小'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='mapped_bases',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='过滤数据量'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='mapped_reads',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='过滤reads数目'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='pass_bases',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='过滤数据量'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='pass_dir',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Pass data 路径'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='pass_reads_avg',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Reads平均长度'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='pass_reads_avg_score',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='平均质量值'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='pass_reads_median',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Reads中位数长度'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='pass_reads_n50',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Reads N50长度'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='pass_total_reads',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='过滤reads数目'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='raw_dir',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Raw data 路径'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='total_bases',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='原始数据量'),
        ),
        migrations.AddField(
            model_name='sequence',
            name='total_reads',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='原始reads数目'),
        ),
        migrations.AlterField(
            model_name='extraction',
            name='bct_id',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='采血管编号'),
        ),
        migrations.AlterField(
            model_name='extraction',
            name='sample',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='extraction', to='pm.Sample', verbose_name='样本编号'),
        ),
    ]