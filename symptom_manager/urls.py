from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^api/v1/symptoms/filter_symptoms/(?P<userid>[0-9]+)/(?P<incidentid>[0-9]+)/$',
        views.get_symptoms_by_user_and_incident,
        name='get_symptoms_by_user_and_incident'
    ),
    url(
        r'^api/v1/symptoms/filter_symptoms/(?P<userid>[0-9]+)/$',
        views.get_symptoms_by_user,
        name='get_symptoms_by_user'
    ),
    url(
        r'^api/v1/symptoms/(?P<pk>[0-9]+)$',
        views.get_delete_update_symptom,
        name='get_delete_update_symptom'
    ),
    url(
        r'^api/v1/symptoms/$',
        views.get_post_symptoms,
        name='get_post_symptoms'
    )
]
