from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('locarise_drf_oauth2_support.oauth2_client.urls')),  # noqa
    url(r'^', include('locarise_drf_oauth2_support.users.urls')),  # noqa
]
