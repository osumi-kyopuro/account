# Generated by Django 2.2.1 on 2020-11-24 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='authority',
            field=models.CharField(blank=True, choices=[('管理者', '管理者'), ('一般人', '一般人')], default='一般人', max_length=100, null=True, verbose_name='カラム名'),
        ),
    ]