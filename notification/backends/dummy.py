from notification.backends.base import NotificationBackend

class NotificationBackend:
    def send(self, notice, messages, context, *args, **kwargs):
        return False
