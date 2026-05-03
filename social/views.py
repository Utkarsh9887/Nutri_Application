from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.utils.timezone import now
from datetime import timedelta

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Friendship
from nutrition.models import Meal
from workouts.models import WorkoutLog


# ── FRIENDS LIST ───────────────────────────────────────────────────────────────
# GET /api/social/friends/
# Returns users the current user is following.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friends(request):
    following = Friendship.objects.filter(from_user=request.user).select_related('to_user')
    data = []
    for f in following:
        u = f.to_user
        # Check if they follow back (mutual)
        is_mutual = Friendship.objects.filter(from_user=u, to_user=request.user).exists()
        data.append({
            'id':         u.id,
            'username':   u.username,
            'is_mutual':  is_mutual,
            'since':      f.created_at.date().isoformat(),
        })
    return Response(data)


# ── ADD FRIEND ─────────────────────────────────────────────────────────────────
# POST /api/social/friends/
# Body: { "user_id": 5 }

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_friend(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'user_id is required.'}, status=400)
    if int(user_id) == request.user.id:
        return Response({'error': "You can't follow yourself."}, status=400)
    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

    _, created = Friendship.objects.get_or_create(from_user=request.user, to_user=target)
    if not created:
        return Response({'error': f'Already following {target.username}.'}, status=400)

    return Response({'success': True, 'message': f'Now following {target.username}.'})


# ── REMOVE FRIEND ──────────────────────────────────────────────────────────────
# DELETE /api/social/friends/<user_id>/

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_friend(request, user_id):
    deleted, _ = Friendship.objects.filter(
        from_user=request.user,
        to_user_id=user_id
    ).delete()
    if deleted:
        return Response({'success': True})
    return Response({'error': 'Not following this user.'}, status=404)


# ── SEARCH USERS ───────────────────────────────────────────────────────────────
# GET /api/social/search/?q=john
# Returns up to 10 users matching the query (excluding self).

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    q = request.query_params.get('q', '').strip()
    if len(q) < 2:
        return Response({'error': 'Query must be at least 2 characters.'}, status=400)

    users = User.objects.filter(
        username__icontains=q
    ).exclude(id=request.user.id)[:10]

    # Which of these is the current user already following?
    already_following = set(
        Friendship.objects.filter(
            from_user=request.user,
            to_user__in=users
        ).values_list('to_user_id', flat=True)
    )

    data = [{
        'id':               u.id,
        'username':         u.username,
        'already_following': u.id in already_following,
    } for u in users]

    return Response(data)


# ── LEADERBOARD ────────────────────────────────────────────────────────────────
# GET /api/social/leaderboard/?period=week
# period: week (default) | month | all
# Returns top 20 users ranked by calories logged, with workout count.
# Only includes the current user + users they follow.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    period = request.query_params.get('period', 'week')

    # Date filter
    today = now().date()
    if period == 'week':
        since = today - timedelta(days=7)
    elif period == 'month':
        since = today - timedelta(days=30)
    else:
        since = None  # all time

    # Pool = current user + everyone they follow
    following_ids = list(
        Friendship.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)
    )
    pool_ids = following_ids + [request.user.id]

    # Calorie totals
    meal_qs = Meal.objects.filter(user_id__in=pool_ids)
    if since:
        meal_qs = meal_qs.filter(created_at__date__gte=since)
    calorie_totals = {
        row['user_id']: row['total']
        for row in meal_qs.values('user_id').annotate(total=Sum('calories'))
    }

    # Workout counts
    workout_qs = WorkoutLog.objects.filter(user_id__in=pool_ids)
    if since:
        workout_qs = workout_qs.filter(date__gte=since)
    workout_counts = {
        row['user_id']: row['count']
        for row in workout_qs.values('user_id').annotate(count=Count('id'))
    }

    # Build ranked list
    users = User.objects.filter(id__in=pool_ids)
    board = []
    for u in users:
        board.append({
            'user_id':       u.id,
            'username':      u.username,
            'is_you':        u.id == request.user.id,
            'calories':      calorie_totals.get(u.id, 0),
            'workouts':      workout_counts.get(u.id, 0),
        })

    # Sort by calories desc, then workouts desc
    board.sort(key=lambda x: (-x['calories'], -x['workouts']))

    # Add rank
    for i, row in enumerate(board):
        row['rank'] = i + 1

    return Response(board[:20])