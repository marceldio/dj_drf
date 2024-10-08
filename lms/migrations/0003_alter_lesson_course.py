# Generated by Django 4.2.15 on 2024-09-16 18:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lms", "0002_alter_lesson_video"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lessons",
                to="lms.course",
                verbose_name="Курс",
            ),
        ),
    ]
