# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from .models import Messages

# from django.contrib.auth import get_user_model

# User = get_user_model()




# @login_required
# def chat_history(request, user_id):
#     other_user =User.objects.get(id=user_id)
#     messages = Message.objects.filter(
#         (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
#         (models.Q(sender=other_user) & models.Q(receiver = request.user))
#     ).order_by('timestamp')

#     return JsonResponse({
#         'message': [
#             {"sender": msg.sender.username, 'content':msg.content, 'timestamp':msg.timestamp}
#             for msg in messages
#         ]
#     })