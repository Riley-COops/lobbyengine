from django.urls import path
# from .views import MessageListCreateView
from . import views

urlpatterns = [
    # path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('chat-history/<int:user_id>/', views.chat_history, name='chat_history'),
]