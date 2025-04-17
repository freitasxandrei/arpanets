from django.urls import path
from . import views

urlpatterns = [
    # Outras rotas para autenticação
    path('', views.home_redirect_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    # Rota para a API do SRQ-20
    path('api/srq20/', views.srq20_response_list, name='srq20_response_list'),
]
