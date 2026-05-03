import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0002_remove_meal_date_meal_created_at_meal_meal_type_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MacroTarget',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calorie_goal', models.IntegerField(default=2000)),
                ('protein',      models.IntegerField(default=150)),
                ('carbs',        models.IntegerField(default=200)),
                ('fats',         models.IntegerField(default=65)),
                ('user',         models.OneToOneField(
                                    on_delete=django.db.models.deletion.CASCADE,
                                    related_name='macro_target',
                                    to=settings.AUTH_USER_MODEL,
                                )),
            ],
        ),
    ]