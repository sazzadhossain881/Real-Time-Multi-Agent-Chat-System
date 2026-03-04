from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from chat.models import Message
from collections import defaultdict
from django.db.models import Q


# Create your views here.
class MessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        messages = Message.objects.filter(
            Q(session__visitor=user) | Q(session__agent=user)
        ).order_by("session__id", "timestamp")

        grouped_data = defaultdict(list)

        for m in messages:
            grouped_data[str(m.session.id)].append({
                "sender": m.sender.username,
                "content": m.content,
                "created_at": m.timestamp,
            })

        response_data = [
            {
                "session_id": session_id,
                "messages": msgs
            }
            for session_id, msgs in grouped_data.items()
        ]

        return Response(response_data)


class MessageRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        user = request.user

        messages = Message.objects.filter(
            Q(session__visitor=user) | Q(session__agent=user),
            session__id=session_id
        ).order_by("timestamp")

        grouped_data = defaultdict(list)

        for m in messages:
            grouped_data[str(m.session.id)].append({
                "sender": m.sender.username,
                "content": m.content,
                "created_at": m.timestamp,
            })

        response_data = [
            {
                "session_id": session_id,
                "messages": msgs
            }
            for session_id, msgs in grouped_data.items()
        ]

        return Response(response_data)


