from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,  name='index'),
    path('profile/', views.profile, name='profile'),
    path('blocked/', views.blocked_view, name='blocked'),
    path('main/<slug:slug>/', views.CompetitionDetailView.as_view(), name='competition_detail'),
    path('editor/', views.editors_page, name='editor'),
    path('editor/update/competitions/<slug:slug>/', views.editor_update_competitions, name='editor_update_competitions'),
    path('editor/delete/competitions/<int:pk>/', views.editor_delete_competitions, name='editor_delete_competitions'),
    path('editor/update/news/<slug:slug>/', views.editor_update_news, name='editor_update_news'),
    path('editor/delete/news/<int:pk>/', views.editor_delete_news, name='editor_delete_news'),
    path('about', views.about, name='about'),

]