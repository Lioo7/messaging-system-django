from .models import Messaging


# Fetches a message from the database based on the provided ID and user
# Returns the message object if found, or None if the message does not exist
def get_message(message_id, user):
    try:
        return Messaging.objects.get(id=message_id, receiver=user)
    except Messaging.DoesNotExist:
        return None
