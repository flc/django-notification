from django.conf import settings


QUEUE_ALL = getattr(settings, "NOTIFICATION_QUEUE_ALL", False)
OBSOLETE_DAYS = getattr(settings, "NOTIFICATION_OBSOLETE_DAYS", 30)

