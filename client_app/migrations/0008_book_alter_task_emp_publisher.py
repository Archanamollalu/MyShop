# Generated by Django 5.2.2 on 2025-06-17 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0007_employee_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookname', models.CharField(max_length=30, null=True)),
                ('author', models.CharField(max_length=30, null=True)),
                ('price', models.IntegerField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='emp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task', to='client_app.employee'),
        ),
        migrations.CreateModel(
            name='publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to='client_app.book')),
            ],
        ),
    ]
