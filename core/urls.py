from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect_view, name='home'),  
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('questionnaire_result/<int:pk>/', views.questionnaire_result, name='questionnaire_result'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
