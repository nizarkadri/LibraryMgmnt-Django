# Generated by Django 3.0b1 on 2021-07-29 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20210603_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Student',
            field=models.ForeignKey(default='john', on_delete=django.db.models.deletion.CASCADE, to='myapp.Student'),
        ),
    ]