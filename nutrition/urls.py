from django.urls import path
from .views import add_meal, meals_by_date, delete_meal, dashboard, macro_targets, analyse_meal

urlpatterns = [
    # existing
    path('log-food/',              add_meal,      name='log-food'),       # POST

    # new
    path('meals/<str:date>/',meals_by_date, name='meals-by-date'),  # GET  /meals/2026-05-02/
    path('meals/<int:meal_id>/',delete_meal,   name='delete-meal'),    # DELETE /meals/42/
    path('dashboard/',dashboard,     name='dashboard'),      # GET
    path('macro/',macro_targets, name='macro-targets'),  # GET + PUT
    path('analyse/',analyse_meal,  name='analyse-meal'),
]