import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id',             models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name',   models.CharField(blank=True, max_length=80)),
                ('bio',            models.TextField(blank=True)),
                ('gender',         models.CharField(blank=True, choices=[('male','Male'),('female','Female'),('other','Other')], max_length=10)),
                ('date_of_birth',  models.DateField(blank=True, null=True)),
                ('height_cm',      models.FloatField(blank=True, null=True)),
                ('goal',           models.CharField(blank=True, choices=[('lose','Lose Weight'),('maintain','Maintain Weight'),('gain','Gain Muscle')], max_length=10)),
                ('activity_level', models.CharField(blank=True, choices=[('sedentary','Sedentary'),('lightly_active','Lightly Active'),('active','Active'),('very_active','Very Active')], max_length=20)),
                ('updated_at',     models.DateTimeField(auto_now=True)),
                ('user',           models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]