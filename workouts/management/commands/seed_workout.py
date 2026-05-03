"""
Django management command to seed the Exercise and WorkoutTemplate tables.

Usage (from Nutri_app/):
    python manage.py seed_workouts

Safe to run multiple times — uses get_or_create so it won't duplicate rows.
"""

from django.core.management.base import BaseCommand
from workouts.models import Exercise, WorkoutTemplate


EXERCISES = [
    dict(id=1,  name="Barbell Bench Press",    muscle_group="Chest",      equipment="Barbell",    experience_level="Intermediate", instructions="Lie on bench, lower bar to mid-chest, press up.",       recommended_sets="3x8-12",    tips="Keep shoulders tucked."),
    dict(id=2,  name="Push-Up",                muscle_group="Chest",      equipment="Bodyweight", experience_level="Beginner",     instructions="Plank position, lower chest to floor, push up.",        recommended_sets="3x max",    tips="Core tight."),
    dict(id=3,  name="Pull-Up",                muscle_group="Back",       equipment="Bodyweight", experience_level="Advanced",     instructions="Hang, pull chin above bar.",                             recommended_sets="3x6-10",    tips="Avoid swinging."),
    dict(id=4,  name="Bent Over Row",          muscle_group="Back",       equipment="Barbell",    experience_level="Intermediate", instructions="Hinge at hips, row bar to belly.",                       recommended_sets="3x8",       tips="Flat back."),
    dict(id=5,  name="Seated Dumbbell Press",  muscle_group="Shoulders",  equipment="Dumbbells",  experience_level="Intermediate", instructions="Press overhead, slight arch.",                           recommended_sets="3x10",      tips="Don't lock elbows."),
    dict(id=6,  name="Lateral Raise",          muscle_group="Shoulders",  equipment="Dumbbells",  experience_level="Beginner",     instructions="Raise arms to side to shoulder height.",                 recommended_sets="3x12",      tips="Light weight, controlled."),
    dict(id=7,  name="Barbell Curl",           muscle_group="Biceps",     equipment="Barbell",    experience_level="Beginner",     instructions="Curl barbell, squeeze biceps.",                          recommended_sets="3x10",      tips="Elbows stationary."),
    dict(id=8,  name="Tricep Pushdown",        muscle_group="Triceps",    equipment="Cable",      experience_level="Beginner",     instructions="Push bar down, extend arms.",                            recommended_sets="3x12",      tips="Upper arms fixed."),
    dict(id=9,  name="Goblet Squat",           muscle_group="Quads",      equipment="Dumbbell",   experience_level="Beginner",     instructions="Hold dumbbell, squat deep.",                             recommended_sets="3x10",      tips="Chest up."),
    dict(id=10, name="Deadlift",               muscle_group="Hamstrings", equipment="Barbell",    experience_level="Advanced",     instructions="Hinge, lift bar, keep spine neutral.",                   recommended_sets="3x5",       tips="Engage lats."),
    dict(id=11, name="Leg Press",              muscle_group="Quads",      equipment="Machine",    experience_level="Beginner",     instructions="Push platform, full ROM.",                               recommended_sets="3x12",      tips="Don't lock knees."),
    dict(id=12, name="Walking Lunge",          muscle_group="Glutes",     equipment="Bodyweight", experience_level="Intermediate", instructions="Step forward, lower knee.",                              recommended_sets="3x10 each", tips="Keep torso upright."),
    dict(id=13, name="Plank",                  muscle_group="Abs",        equipment="Bodyweight", experience_level="Beginner",     instructions="Forearms, hold straight line.",                          recommended_sets="3x45s",     tips="Brace core."),
    dict(id=14, name="Hanging Knee Raise",     muscle_group="Abs",        equipment="Bodyweight", experience_level="Intermediate", instructions="Hang, raise knees to chest.",                            recommended_sets="3x12",      tips="No swing."),
    dict(id=15, name="Calf Raise",             muscle_group="Calves",     equipment="Machine",    experience_level="Beginner",     instructions="Push through balls of feet.",                            recommended_sets="3x15",      tips="Full range."),
]

TEMPLATES = [
    dict(name="Full Body Strength", exercises=[1, 2, 5, 9, 13]),
    dict(name="Push Day",           exercises=[1, 2, 5, 6]),
    dict(name="Pull Day",           exercises=[3, 4, 7]),
    dict(name="Leg Day",            exercises=[9, 10, 11, 12]),
]


class Command(BaseCommand):
    help = 'Seeds the Exercise and WorkoutTemplate tables with default data.'

    def handle(self, *args, **kwargs):
        # ── Exercises ──────────────────────────────────────────────────────────
        created_ex = 0
        for ex in EXERCISES:
            ex_id = ex.pop('id')   # don't pass id to get_or_create — let DB assign
            obj, created = Exercise.objects.get_or_create(name=ex['name'], defaults=ex)
            if created:
                created_ex += 1
            ex['id'] = ex_id       # restore for template lookup below

        self.stdout.write(f'  Exercises: {created_ex} created, {len(EXERCISES) - created_ex} already existed.')

        # Build a name→DB id map for template seeding
        ex_name_map = {ex['name']: Exercise.objects.get(name=ex['name']).id for ex in EXERCISES}
        # Remap static integer IDs to real DB IDs using the name map
        static_id_map = {ex['id']: ex_name_map[ex['name']] for ex in EXERCISES}

        # ── Templates ──────────────────────────────────────────────────────────
        created_tp = 0
        for tp in TEMPLATES:
            real_exercise_ids = [static_id_map[i] for i in tp['exercises']]
            obj, created = WorkoutTemplate.objects.get_or_create(
                name=tp['name'],
                defaults={'exercises': real_exercise_ids}
            )
            if created:
                created_tp += 1

        self.stdout.write(f'  Templates: {created_tp} created, {len(TEMPLATES) - created_tp} already existed.')
        self.stdout.write(self.style.SUCCESS('✅ Workout seed complete.'))