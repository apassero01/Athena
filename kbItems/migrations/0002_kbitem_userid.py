# Generated by Django 4.2.2 on 2023-07-11 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbItems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kbitem',
            name='userID',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
