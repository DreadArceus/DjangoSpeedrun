from django.contrib import admin
from .models import GameTickets, GameCalls, GameSecrets, Result

admin.site.register(GameTickets)
admin.site.register(GameCalls)
admin.site.register(GameSecrets)
admin.site.register(Result)
