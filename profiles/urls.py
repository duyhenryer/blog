from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^accounts/$', views.ShowProfile.as_view(), name='show_self'),
    url(r'^account/edit$', views.EditProfile.as_view(), name='edit_self'),
    url(r'^(?P<slug>[\w\-]+)$', views.ShowProfile.as_view(),
        name='show'),
]