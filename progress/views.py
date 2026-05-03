from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import WeightEntry
from .serializers import WeightEntrySerializer


# ── WEIGHT ENTRIES ─────────────────────────────────────────────────────────────
# GET  /api/progress/weight/   — all entries for this user, oldest first (for charting)
# POST /api/progress/weight/   — log a new weight entry

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def weight_entries(request):

    if request.method == 'GET':
        entries = WeightEntry.objects.filter(user=request.user)
        return Response(WeightEntrySerializer(entries, many=True).data)

    # POST
    weight = request.data.get('weight')
    date   = request.data.get('date', str(now().date()))

    try:
        weight = float(weight)
        assert weight > 0
    except (TypeError, ValueError, AssertionError):
        return Response({'error': 'Weight must be a positive number.'}, status=400)

    # update_or_create — if user already logged today, just update the value
    entry, created = WeightEntry.objects.update_or_create(
        user=request.user,
        date=date,
        defaults={'weight': weight}
    )

    return Response(WeightEntrySerializer(entry).data, status=201 if created else 200)


# ── DELETE ENTRY ───────────────────────────────────────────────────────────────
# DELETE /api/progress/weight/<id>/

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_entry(request, entry_id):
    try:
        entry = WeightEntry.objects.get(id=entry_id, user=request.user)
        entry.delete()
        return Response({'success': True})
    except WeightEntry.DoesNotExist:
        return Response({'error': 'Entry not found.'}, status=404)