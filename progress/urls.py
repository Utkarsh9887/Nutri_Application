from django.urls import path
from .views import weight_entries, delete_entry

urlpatterns = [
    path('weight/',              weight_entries, name='weight-entries'),  # GET + POST
    path('weight/<int:entry_id>/', delete_entry, name='delete-entry'),    # DELETE
]