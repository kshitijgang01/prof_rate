# Generated by Django 3.0.3 on 2020-03-26 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0009_messages_way_of_communication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='conversation',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='Messages',
        ),
    ]
