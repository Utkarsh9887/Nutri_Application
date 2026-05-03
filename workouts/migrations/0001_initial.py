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
            name='Exercise',
            fields=[
                ('id',               models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',             models.CharField(max_length=100, unique=True)),
                ('muscle_group',     models.CharField(max_length=50)),
                ('equipment',        models.CharField(max_length=50)),
                ('experience_level', models.CharField(choices=[('Beginner','Beginner'),('Intermediate','Intermediate'),('Advanced','Advanced')], max_length=20)),
                ('instructions',     models.TextField()),
                ('recommended_sets', models.CharField(max_length=30)),
                ('tips',             models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutTemplate',
            fields=[
                ('id',        models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',      models.CharField(max_length=100, unique=True)),
                ('exercises', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutLog',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',       models.CharField(max_length=100)),
                ('sets',       models.IntegerField()),
                ('reps',       models.IntegerField()),
                ('weight',     models.FloatField(default=0)),
                ('difficulty', models.CharField(choices=[('Easy','Easy'),('Medium','Medium'),('Hard','Hard')], default='Medium', max_length=10)),
                ('date',       models.DateField()),
                ('logged_at',  models.DateTimeField(auto_now_add=True)),
                ('exercise',   models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='workouts.exercise')),
                ('user',       models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-logged_at']},
        ),
    ]