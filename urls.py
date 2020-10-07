from django.urls import path

from . import views

app_name = 'femacronyms'
urlpatterns = [
    path('fdsa/', views.index_view, name='all acronyms'),
    path('query/', views.query_view, name='search'),
    path('', views.index_view, name='acronyms home'),
    path('<str:pass_name>/', views.index_view, name='detail'),
]
