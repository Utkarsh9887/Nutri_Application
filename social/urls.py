from django.urls import path
from .views import friends, add_friend, remove_friend, search_users, leaderboard

urlpatterns = [
    path('friends/',              friends,       name='friends'),        # GET
    path('friends/add/',          add_friend,    name='add-friend'),     # POST
    path('friends/<int:user_id>/', remove_friend, name='remove-friend'), # DELETE
    path('search/',               search_users,  name='search-users'),   # GET ?q=
    path('leaderboard/',          leaderboard,   name='leaderboard'),    # GET ?period=week|month|all
]