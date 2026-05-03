from django.db import models
from django.contrib.auth.models import User


class Exercise(models.Model):
    """
    Static exercise library — seeded once via the management command
    or Django admin. Not user-specific.
    """
    LEVEL_CHOICES = [
        ('Beginner',     'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced',     'Advanced'),
    ]

    name              = models.CharField(max_length=100, unique=True)
    muscle_group      = models.CharField(max_length=50)
    equipment         = models.CharField(max_length=50)
    experience_level  = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    instructions      = models.TextField()
    recommended_sets  = models.CharField(max_length=30)
    tips              = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class WorkoutTemplate(models.Model):
    """
    Pre-defined workout template (e.g. 'Push Day').
    exercises is a JSON list of Exercise IDs.
    """
    name      = models.CharField(max_length=100, unique=True)
    exercises = models.JSONField(default=list)   # e.g. [1, 2, 5, 6]

    def __str__(self):
        return self.name


class WorkoutLog(models.Model):
    """
    One row per exercise logged by a user in a single session.
    """
    DIFFICULTY_CHOICES = [
        ('Easy',   'Easy'),
        ('Medium', 'Medium'),
        ('Hard',   'Hard'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_logs')
    exercise    = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True, blank=True)
    name        = models.CharField(max_length=100)   # denormalised — kept even if exercise deleted
    sets        = models.IntegerField()
    reps        = models.IntegerField()
    weight      = models.FloatField(default=0)       # kg
    difficulty  = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')
    date        = models.DateField()
    logged_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return f"{self.user.username} — {self.name} ({self.date})"