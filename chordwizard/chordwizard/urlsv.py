from django.conf.urls import url, include
from rest_framework.authtoken import views
from users.views import Register

urlpatterns = [
    url(r'^auth/$', views.obtain_auth_token),
    url(r'^me/', include('users.urls')),
    url(r'^register/', Register.as_view()),
]
