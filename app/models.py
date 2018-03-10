from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=200)
    def __str__(self):
        return self.team_name

    class Meta:
        ordering = ['team_name']

class Player(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete = models.CASCADE
    )
    player_name = models.CharField(max_length=50)
    monthly_fine = models.IntegerField(default=0)
    total_fine = models.IntegerField(default=0)
    def __str__(self):
        return self.player_name
    
    class Meta:
        ordering = ['player_name']

class Fine(models.Model):
    fine_name = models.CharField(max_length=50)

    def __str__(self):
        return self.fine_name