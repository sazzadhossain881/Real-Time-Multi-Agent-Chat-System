from user.models import User
from chat.models import ChatSession
from django.db.models import Count


from chat.models import ChatSession, User

def assign_agent(visitor):
    session = ChatSession.objects.filter(visitor=visitor, is_active=True).first()

    available_agent = User.objects.filter(role='agent', is_available=True).first()

    if session:
        if not session.agent or not session.agent.is_available:
            if available_agent:
                session.agent = available_agent
                session.save()

                available_agent.is_available = False
                available_agent.save()
        return session

    session = ChatSession.objects.create(visitor=visitor, agent=available_agent)
    
    if available_agent:
        available_agent.is_available = False
        available_agent.save()

    return session
