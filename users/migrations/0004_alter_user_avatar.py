# Generated by Django 4.2.15 on 2024-09-13 21:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_user_phone_alter_user_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to="users/avatars", verbose_name="Аватар"
            ),
        ),
    ]
