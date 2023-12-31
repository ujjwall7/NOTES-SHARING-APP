# Generated by Django 4.2.2 on 2023-06-15 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='file',
            field=models.FileField(null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='note',
            name='note_type',
            field=models.CharField(choices=[('Text', 'Text'), ('Audio', 'Audio'), ('Video', 'Video')], max_length=10, null=True),
        ),
    ]
