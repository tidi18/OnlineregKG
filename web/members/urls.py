from django.urls import path
from . import views

urlpatterns = [
    path('', views.MemberViews.as_view(),  name='member'),
    path('successful/registration/', views.member_success, name='member_success')

]