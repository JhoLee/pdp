from django.urls import path

from . import views

app_name = 'mask'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/', views.PostFormView.as_view(), name='post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='delete'),

]
