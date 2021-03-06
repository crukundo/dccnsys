# Generated by Django 2.2.4 on 2019-08-29 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0010_proceedingvolume'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtifactDescriptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(choices=[('ANY', 'Any file'), ('PDF', 'PDF files only'), ('SCAN', 'Any PDF or image file'), ('ZIP', 'ZIP archive')], default='ANY', max_length=8, verbose_name='Type of files expected')),
                ('max_size_mb', models.IntegerField(default=10, verbose_name='Maximum size in MB')),
                ('name', models.CharField(max_length=256)),
                ('code', models.CharField(max_length=8)),
                ('description', models.TextField(verbose_name='Description of the artifact')),
                ('proc_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artifacts', to='conferences.ProceedingType')),
            ],
        ),
    ]
