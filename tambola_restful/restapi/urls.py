from django.conf.urls import url
from .views import ticket_list, calls_list, result_report, initialise_game, processClaim, deleteAll

urlpatterns = [
    url(r'^init$', initialise_game),
    url(r'^claim/(?P<ticket_state>[0-1]{27})/(?P<key>[A-Z]{13})$', processClaim),
    url(r'^result$', result_report),
    url(r'^ticket/(?P<key>[A-Z]{13})(/(?P<discord>[0-9]{18}))?$', ticket_list),
    url(r'^call(/(?P<num>[0-9]+))?$', calls_list),
    url(r'^del', deleteAll)
]
