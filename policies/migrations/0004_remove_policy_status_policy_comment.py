# Generated by Django 4.1 on 2023-08-05 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policies', '0003_alter_policy_disease_types_alter_policy_file_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='status',
        ),
        migrations.AddField(
            model_name='policy',
            name='comment',
            field=models.CharField(blank=True, max_length=2048, null=True, verbose_name='备注'),
        ),
    ]