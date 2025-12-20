from django.contrib import admin
from django.urls import path
from RAG.chat import chat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chat_view, name='chat'),
]