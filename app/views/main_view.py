from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import *
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from app.models import Team, Player


@login_required
def home(request):
    """
    """
    list_team = Team.objects.all()
    context = { 'list_team' : list_team }
    return render(request, 'app/home.html', context)

@login_required
def players(
    request,
    team_id,
):
    """
    """
    team_instance = Team.objects.get(id=team_id)
    if request.method == 'POST':
        player_name = request.POST.get('playername', False)
        if player_name:
            player = Player()
            player.team = team_instance
            player.player_name = player_name
            player.save()
            return HttpResponseRedirect(reverse('player', args=(team_id,)))
        else:
            return render(request, 'app/add_player.html', {'team_id':team_id})
    else:
        list_players = Player.objects.all().filter(team=team_instance)
        context = {
            'list_players' : list_players,
            'team_id': team_id
        }
    return render(request, 'app/list_players.html', context)

@login_required
def add_player(
    request,
    team_id,
):
    """
    """
    return render(request, 'app/add_player.html', {'team_id':team_id})

@login_required
def player(
    request,
    team_id,
    player_id,
):
    """
    """
    info_player = get_object_or_404(Player, id=player_id)
    context = {
        'info_player' : info_player,
        'team_id': team_id
    }
    return render(request, 'app/info_player.html', context)

@login_required
def fine(
    request,
    team_id,
    player_id,
):
    """
    """
    info_player = get_object_or_404(Player, id=player_id)
    info_player.monthly_fine += int(request.POST['fine'])
    info_player.save()
    return HttpResponseRedirect(reverse('info_player', args=(team_id, player_id)))

@login_required
def report(
    request,
    team_id,
):
    """
    """
    list_players = get_list_or_404(Player, team=team_id)
    for player in list_players:
        player.total_fine += player.monthly_fine
        player.monthly_fine = 0
        player.save()
    send_mail(
        'Subject here',
        'Here is the message.',
        'black_box@gmail.com',
        ['joris.laruelle83@gmail.com'],
        fail_silently=False,
    )
    return HttpResponseRedirect(reverse('players', args=(team_id,)))

@login_required
def team(request):
    """
    """
    if request.method == 'POST':
        team_name = request.POST.get('teamname', False)
        if team_name:
            new_team = Team()
            new_team.team_name = team_name
            new_team.save()
            return HttpResponseRedirect(reverse('players', args=(new_team.id,)))
        else:
            return render(request, 'app/add_team.html')
    else:
        return render(request, 'app/add_team.html')
   
