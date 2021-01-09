from django.urls import include, path
from tambola.draft_api import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('count', views.start),
    path('claim/<ticket_state>/<key>', views.processClaim),
    path('results', views.finish),
    path('new/<key>/<discord>', views.generateTicket),
    path('ticket/<key>', views.getTicket),
    path('calls', views.listCalls),
    path('numcall/<num>', views.processNumCall)
]
