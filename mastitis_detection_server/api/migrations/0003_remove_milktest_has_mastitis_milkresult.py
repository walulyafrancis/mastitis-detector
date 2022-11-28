# Generated by Django 4.0 on 2022-11-28 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_tempreturetest_has_mastitis_tempretureresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milktest',
            name='has_mastitis',
        ),
        migrations.CreateModel(
            name='MilkResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('results', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.milktest')),
            ],
        ),
    ]
