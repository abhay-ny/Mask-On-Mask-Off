# Generated by Django 3.0 on 2024-04-10 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20240410_0715'),
    ]

    operations = [
        migrations.CreateModel(
            name='Decryption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Decrypted_Image', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Encryption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Encrypted_Image', models.TextField()),
            ],
        ),
    ]
