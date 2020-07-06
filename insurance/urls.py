from django.urls import path, include
from insurance import views

urlpatterns = [
    path('test/', views.test_view),
]