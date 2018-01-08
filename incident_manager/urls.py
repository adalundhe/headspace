from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^api/v1/incidents/filter_incidents/(?P<userid>[0-9]+)/$',
        views.get_incidents_by_user,
        name='get_incidents_by_user'
    ),
    url(
        r'^api/v1/incidents/(?P<pk>[0-9]+)$',
        views.get_delete_update_incident,
        name='get_delete_update_incident'
    ),
    url(
        r'^api/v1/incidents/$',
        views.get_post_incidents,
        name='get_post_incidents'
    )
]
