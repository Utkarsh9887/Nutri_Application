from django.db import models
from django.contrib.auth.models import User


class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch',     'Lunch'),
        ('dinner',    'Dinner'),
        ('snack',     'Snack'),
    ]

    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name  = models.CharField(max_length=100)
    calories   = models.IntegerField()
    protein    = models.FloatField(default=0)
    carbs      = models.FloatField(default=0)
    fats       = models.FloatField(default=0)
    meal_type  = models.CharField(max_length=20, choices=MEAL_TYPES, default='snack')
    quantity   = models.FloatField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} ({self.user.username})"


class MacroTarget(models.Model):
    """
    Stores one row per user — their personal daily macro & calorie goals.
    Created automatically with sensible defaults the first time a user
    calls GET /api/nutrition/macro/.
    """
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='macro_target')
    calorie_goal = models.IntegerField(default=2000)
    protein      = models.IntegerField(default=150)   # grams
    carbs        = models.IntegerField(default=200)   # grams
    fats         = models.IntegerField(default=65)    # grams

    def __str__(self):
        return f"Macros for {self.user.username}"