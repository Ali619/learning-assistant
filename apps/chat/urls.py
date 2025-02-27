from django.urls import path

from apps.chat.views.chat_view import ChatView

urlpatterns = [
    path("chat/", ChatView.as_view(), name='chat')
]
