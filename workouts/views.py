from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Exercise, WorkoutTemplate, WorkoutLog
from .serializers import ExerciseSerializer, WorkoutTemplateSerializer, WorkoutLogSerializer


# ── EXERCISES ──────────────────────────────────────────────────────────────────
# GET /api/workouts/exercises/
# Returns the full exercise library. No auth required — it's static reference data.

@api_view(['GET'])
def get_exercises(request):
    exercises = Exercise.objects.all().order_by('muscle_group', 'name')
    return Response(ExerciseSerializer(exercises, many=True).data)


# ── TEMPLATES ──────────────────────────────────────────────────────────────────
# GET /api/workouts/templates/
# Returns pre-defined workout templates.

@api_view(['GET'])
def get_templates(request):
    templates = WorkoutTemplate.objects.all()
    return Response(WorkoutTemplateSerializer(templates, many=True).data)


# ── WORKOUT LOGS ───────────────────────────────────────────────────────────────
# GET  /api/workouts/logs/   — returns all logs for this user, newest first
# POST /api/workouts/logs/   — saves a new workout log entry

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def workout_logs(request):

    if request.method == 'GET':
        logs = WorkoutLog.objects.filter(user=request.user)
        return Response(WorkoutLogSerializer(logs, many=True).data)

    # POST — log a new workout
    data = request.data

    # Resolve exercise FK if exercise_id provided (optional — name is always stored too)
    exercise_id = data.get('exercise_id')
    exercise    = None
    if exercise_id:
        try:
            exercise = Exercise.objects.get(id=exercise_id)
        except Exercise.DoesNotExist:
            pass

    name       = data.get('name', exercise.name if exercise else '').strip()
    sets       = data.get('sets')
    reps       = data.get('reps')
    weight     = data.get('weight', 0)
    difficulty = data.get('difficulty', 'Medium')
    date       = data.get('date')

    # Basic validation
    if not name:
        return Response({'error': 'Exercise name is required.'}, status=400)
    try:
        sets = int(sets)
        reps = int(reps)
        assert sets > 0 and reps > 0
    except (TypeError, ValueError, AssertionError):
        return Response({'error': 'Sets and reps must be positive integers.'}, status=400)
    if not date:
        from django.utils.timezone import now
        date = now().date()

    log = WorkoutLog.objects.create(
        user       = request.user,
        exercise   = exercise,
        name       = name,
        sets       = sets,
        reps       = reps,
        weight     = float(weight),
        difficulty = difficulty,
        date       = date,
    )

    return Response(WorkoutLogSerializer(log).data, status=201)


# ── DELETE LOG ─────────────────────────────────────────────────────────────────
# DELETE /api/workouts/logs/<id>/

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_log(request, log_id):
    try:
        log = WorkoutLog.objects.get(id=log_id, user=request.user)
        log.delete()
        return Response({'success': True})
    except WorkoutLog.DoesNotExist:
        return Response({'error': 'Log not found.'}, status=404)