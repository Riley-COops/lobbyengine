from rest_framework import generics
from .models import Messages
from .serializers import MessageSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer