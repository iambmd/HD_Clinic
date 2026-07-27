import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='full name')),
                ('phone', models.CharField(max_length=20, verbose_name='phone')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('preferred_date', models.DateField(verbose_name='preferred date')),
                ('preferred_time', models.TimeField(verbose_name='preferred time')),
                ('branch', models.CharField(choices=[('MAIN', 'Main Clinic – Dương Nội')], default='MAIN', max_length=50, verbose_name='branch')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'appointment',
                'verbose_name_plural': 'appointments',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=300, verbose_name='title (EN)')),
                ('title_vi', models.CharField(max_length=300, verbose_name='title (VI)')),
                ('content_en', models.TextField(verbose_name='content (EN)')),
                ('content_vi', models.TextField(verbose_name='content (VI)')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='articles/', verbose_name='thumbnail')),
                ('published_date', models.DateField(default=django.utils.timezone.localdate, verbose_name='published date')),
                ('slug', models.SlugField(max_length=350, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
                'ordering': ['-published_date', '-id'],
            },
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('phone', models.CharField(max_length=20, verbose_name='phone')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('message', models.TextField(verbose_name='message')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='sent at')),
            ],
            options={
                'verbose_name': 'contact message',
                'verbose_name_plural': 'contact messages',
                'ordering': ['-sent_at'],
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('specialty', models.CharField(max_length=200, verbose_name='specialty')),
                ('bio_en', models.TextField(verbose_name='biography (EN)')),
                ('bio_vi', models.TextField(verbose_name='biography (VI)')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='doctors/', verbose_name='photo')),
            ],
            options={
                'verbose_name': 'doctor',
                'verbose_name_plural': 'doctors',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(max_length=200, verbose_name='title (EN)')),
                ('title_vi', models.CharField(max_length=200, verbose_name='title (VI)')),
                ('description_en', models.TextField(verbose_name='description (EN)')),
                ('description_vi', models.TextField(verbose_name='description (VI)')),
                ('icon', models.CharField(help_text='Bootstrap Icons class name, e.g. bi-ear', max_length=100, verbose_name='icon')),
                ('category', models.CharField(choices=[('EAR', 'Ear'), ('NOSE', 'Nose'), ('THROAT', 'Throat')], max_length=10, verbose_name='category')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
                'ordering': ['category', 'title_en'],
            },
        ),
    ]
