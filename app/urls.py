from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views
from app.views.main_view import *

urlpatterns = [
    path('', home, name='home'),
    path('teams/', team, name='team'),
    path('teams/<int:team_id>/addPlayer', add_player, name='player'),
    path('teams/<int:team_id>/', players, name='players'),
    path('teams/<int:team_id>/report/', report, name='send_report'),
    path('teams/<int:team_id>/player/<int:player_id>/', player, name='info_player'),
    path('teams/<int:team_id>/player/<int:player_id>/fine/', fine, name='fine_player')
]
