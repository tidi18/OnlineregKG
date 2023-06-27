from django.urls import path
from . import views

urlpatterns = [
    path('', views.MemberViews.as_view(),  name='member'),

]