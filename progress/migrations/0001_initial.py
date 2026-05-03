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
            name='WeightEntry',
            fields=[
                ('id',        models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight',    models.FloatField()),
                ('date',      models.DateField()),
                ('logged_at', models.DateTimeField(auto_now_add=True)),
                ('user',      models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weight_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['date']},
        ),
        migrations.AlterUniqueTogether(
            name='weightentry',
            unique_together={('user', 'date')},
        ),
    ]