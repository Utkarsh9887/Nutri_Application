from django.db.models import Sum
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Meal, MacroTarget
from .serializers import MealSerializer, MacroTargetSerializer


# ── ADD MEAL ───────────────────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_meal(request):
    serializer = MealSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'success': True, 'data': serializer.data}, status=201)
    return Response({'success': False, 'errors': serializer.errors}, status=400)


# ── MEALS BY DATE ──────────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meals_by_date(request, date):
    try:
        meals = Meal.objects.filter(
            user=request.user,
            created_at__date=date
        ).order_by('created_at')
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


# ── DELETE MEAL ────────────────────────────────────────────────────────────────
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_meal(request, meal_id):
    try:
        meal = Meal.objects.get(id=meal_id, user=request.user)
        meal.delete()
        return Response({'success': True}, status=200)
    except Meal.DoesNotExist:
        return Response({'error': 'Meal not found.'}, status=404)


# ── DASHBOARD ──────────────────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    try:
        today = now().date()
        meals = Meal.objects.filter(user=request.user, created_at__date=today)
        totals = meals.aggregate(
            total_calories=Sum('calories'),
            total_protein=Sum('protein'),
            total_carbs=Sum('carbs'),
            total_fats=Sum('fats'),
        )
        return Response({
            'total_calories': round(totals['total_calories'] or 0, 1),
            'total_protein':  round(totals['total_protein']  or 0, 1),
            'total_carbs':    round(totals['total_carbs']    or 0, 1),
            'total_fats':     round(totals['total_fats']     or 0, 1),
            'meals':          MealSerializer(meals, many=True).data,
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)


# ── MACRO TARGETS ──────────────────────────────────────────────────────────────
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def macro_targets(request):
    target, _ = MacroTarget.objects.get_or_create(user=request.user)
    if request.method == 'GET':
        return Response(MacroTargetSerializer(target).data)
    serializer = MacroTargetSerializer(target, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data})
    return Response({'success': False, 'errors': serializer.errors}, status=400)


# ── AI MEAL ANALYSER ─────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyse_meal(request):
    description = request.data.get('description', '').strip()

    if not description:
        return Response({'error': 'Description is required.'}, status=400)
    if len(description) > 500:
        return Response({'error': 'Description too long (max 500 characters).'}, status=400)

    try:
        from .ai import analyse_meal as ai_analyse
        result = ai_analyse(description)
        return Response({'success': True, 'data': result})

    except ValueError as e:
        # AI returned unparseable response
        return Response({'error': f'Could not parse meal: {str(e)}'}, status=422)

    except EnvironmentError as e:
        # API key missing
        return Response({'error': str(e)}, status=503)

    except Exception as e:
        return Response({'error': f'AI service error: {str(e)}'}, status=503)