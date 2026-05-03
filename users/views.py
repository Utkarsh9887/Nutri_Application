from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import UserProfile
from .serializers import ProfileSerializer, UserSerializer


# ── LOGIN ──────────────────────────────────────────────────────────────────────
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')
    if not username or not password:
        return Response({'success': False, 'message': 'Username and password are required.'}, status=400)
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'success': True, 'token': token.key, 'user': {'id': user.id, 'username': user.username}})
    return Response({'success': False, 'message': 'Invalid credentials.'}, status=401)


# ── REGISTER ───────────────────────────────────────────────────────────────────
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')
    if not username or not password:
        return Response({'success': False, 'message': 'Username and password are required.'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'success': False, 'message': 'Username already taken.'}, status=400)
    if len(password) < 6:
        return Response({'success': False, 'message': 'Password must be at least 6 characters.'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'success': True, 'token': token.key, 'user': {'id': user.id, 'username': user.username}}, status=201)


# ── PROFILE — GET & PUT ────────────────────────────────────────────────────────
# GET  /api/auth/profile/   → returns full user + profile info
# PUT  /api/auth/profile/   → updates profile fields + optional email

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user

    # Ensure profile row exists (for users created before the signal was added)
    prof, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'GET':
        return Response(UserSerializer(user).data)

    # PUT — update allowed fields
    data = request.data

    # Update email on the User model if provided
    if 'email' in data:
        user.email = data['email']
        user.save(update_fields=['email'])

    # Update profile fields
    prof_serializer = ProfileSerializer(prof, data=data, partial=True)
    if prof_serializer.is_valid():
        prof_serializer.save()
        return Response({'success': True, 'data': UserSerializer(user).data})

    return Response({'success': False, 'errors': prof_serializer.errors}, status=400)


# ── CHANGE PASSWORD ────────────────────────────────────────────────────────────
# POST /api/auth/change-password/
# Body: { "current_password": "...", "new_password": "..." }

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user             = request.user
    current_password = request.data.get('current_password', '')
    new_password     = request.data.get('new_password', '')

    if not current_password or not new_password:
        return Response({'success': False, 'message': 'Both fields are required.'}, status=400)

    if not user.check_password(current_password):
        return Response({'success': False, 'message': 'Current password is incorrect.'}, status=400)

    if len(new_password) < 6:
        return Response({'success': False, 'message': 'New password must be at least 6 characters.'}, status=400)

    user.set_password(new_password)
    user.save()

    # Re-issue a fresh token so the user stays logged in after password change
    Token.objects.filter(user=user).delete()
    new_token = Token.objects.create(user=user)

    return Response({'success': True, 'token': new_token.key, 'message': 'Password updated.'})


# ── DELETE ACCOUNT ─────────────────────────────────────────────────────────────
# DELETE /api/auth/profile/
# Permanently deletes the user and all their data (cascade).

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    password = request.data.get('password', '')
    if not request.user.check_password(password):
        return Response({'success': False, 'message': 'Incorrect password.'}, status=400)
    request.user.delete()
    return Response({'success': True, 'message': 'Account deleted.'})