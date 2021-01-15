from django.conf.urls import url
from .views import result_report, initialise_game, delete, ticket_list, calls_list, processClaim

urlpatterns = [
    url(r'^init/(?P<game_id>[0-9]+)$', initialise_game),
    url(r'^claim/(?P<game_id>[0-9]+)/(?P<ticket_state>[0-1]{27})/(?P<key>[A-Z]{13})$', processClaim),
    url(r'^result/(?P<game_id>[0-9]+)$', result_report),
    url(r'^ticket/(?P<game_id>[0-9]+)/(?P<key>[A-Z]{13})(/(?P<discord>[0-9]{18}))?$', ticket_list),
    url(r'^call/(?P<game_id>[0-9]+)(/(?P<num>[0-9]+))?$', calls_list),
    url(r'^del/(?P<game_id>[0-9]+)$', delete)
]
