# Generated by Django 2.2.4 on 2019-10-08 00:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0015_artifactdescriptor_editable'),
        ('review', '0013_reviewdecisiontype_conference'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reviewdecisiontype',
            unique_together={('conference', 'decision', 'description')},
        ),
    ]