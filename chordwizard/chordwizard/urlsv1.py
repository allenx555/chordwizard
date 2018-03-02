from django.conf.urls import url, include
from rest_framework.authtoken import views
from users.views import Register
from users.views import Beta

urlpatterns = [
    url(r'^auth/$', views.obtain_auth_token),
    url(r'^activity/', include('activity.urlsv2')),
    url(r'^me/', include('user.urls')),
    url(r'^register/', Register.as_view()),
    url(r'^beta/', Beta.as_view()),
]
