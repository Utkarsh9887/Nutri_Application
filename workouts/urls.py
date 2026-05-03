from django.urls import path
from .views import get_exercises, get_templates, workout_logs, delete_log

urlpatterns = [
    path('exercises/',       get_exercises,  name='exercises'),    # GET
    path('templates/',       get_templates,  name='templates'),    # GET
    path('logs/',            workout_logs,   name='workout-logs'), # GET + POST
    path('logs/<int:log_id>/', delete_log,   name='delete-log'),   # DELETE
]