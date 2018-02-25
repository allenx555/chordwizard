from django.conf.urls import url
from . import views
from .views import UserShow, ChangePassword

app_name = 'users'
urlpatterns = [
    url(r'^register/', views.registerview, name='registerview'),
    url(r'^$', UserShow.as_view()),
    url(r'^password/', ChangePassword.as_view())
]
