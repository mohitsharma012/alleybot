# Generated by Django 5.0 on 2023-12-28 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='users_messages',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('message', models.TextField()),
                ('reply', models.TextField()),
            ],
        ),
    ]
