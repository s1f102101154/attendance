from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('priv', views.private_page, name='priv'),
    path('pub', views.public_page, name='pub'),
    path('attendance/', views.home, name='attendance'),
    path('edit_attendance/<int:id>/', views.edit_attendance, name='edit_attendance'),
    path('delete_attendance/<int:id>/', views.delete_attendance, name='delete_attendance'),
]

