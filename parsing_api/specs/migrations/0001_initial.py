# Generated by Django 4.2.5 on 2023-10-05 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpecTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_status', models.CharField(choices=[('WAITING_DATA_PROCESSING', 'waiting_data_processing'), ('DATA_PROCESSING', 'data_processing'), ('WAITING_PARSING', 'waiting_parsing'), ('PARSING', 'parsing'), ('OK', 'ok'), ('ERROR', 'error')], default='WAITING_DATA_PROCESSING', max_length=30)),
            ],
            options={
                'db_table': 'specs_spec_tasks',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SpecTaskRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict)),
                ('spec_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spec_task', to='specs.spectask')),
            ],
            options={
                'db_table': 'specs_spec_task_requests',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.BigIntegerField(null=True)),
                ('link', models.CharField(max_length=1000)),
                ('data', models.JSONField(default=dict)),
                ('spec_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spec_product', to='specs.spectask')),
            ],
            options={
                'db_table': 'specs_products',
                'ordering': ['id'],
            },
        ),
    ]
