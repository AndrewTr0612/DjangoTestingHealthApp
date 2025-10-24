from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User Profile
    path('profile/setup/', views.profile_setup_view, name='profile_setup'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Weight Management
    path('weight/add/', views.add_weight_view, name='add_weight'),
    path('goal/set/', views.set_goal_view, name='set_goal'),
    
    # Chatbot
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('api/chatbot/', views.chatbot_api_view, name='chatbot_api'),
]