from django.contrib import admin
from .models import Match,FootballTream
# Register your models here.


class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'name',  'opponent_id', 'outcome', 'ownScore','opponentScore', 'side', 'coach_id','home_name')
    list_display_links = ('match_id', 'opponent_id','coach_id', 'name','home_name')
    search_fields = ('match_id', 'opponent_id', 'coach_id', 'name')

admin.site.register(Match, MatchAdmin)

class TreamAdmin(admin.ModelAdmin):
    list_display = ('name','tream_emblem','area','home_hall','famous_person','main_honor','chairman','owner','founding_time')
    list_display_links = ('name','tream_emblem','area','home_hall','famous_person','main_honor','chairman','owner','founding_time')
    search_fields = ('name','area','home_hall','famous_person','main_honor','chairman','owner','founding_time')

admin.site.register(FootballTream,TreamAdmin)