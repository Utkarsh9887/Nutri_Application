import django.db.models.deletion
import photos.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgressPhoto',
            fields=[
                ('id',          models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image',       models.ImageField(upload_to=photos.models.photo_upload_path)),
                ('caption',     models.CharField(blank=True, max_length=200)),
                ('date',        models.DateField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user',        models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-date', '-uploaded_at']},
        ),
    ]