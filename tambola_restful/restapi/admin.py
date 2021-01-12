from django.contrib import admin
from .models import Ticket, Call, Secret, Result

admin.site.register(Ticket)
admin.site.register(Call)
admin.site.register(Secret)
admin.site.register(Result)
