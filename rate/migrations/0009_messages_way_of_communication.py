# Generated by Django 3.0.3 on 2020-03-26 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0008_conversation_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='way_of_communication',
            field=models.IntegerField(default=0),
        ),
    ]
