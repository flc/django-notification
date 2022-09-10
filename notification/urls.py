from django.urls import path, re_path
from notification.views import notices, mark_all_seen, feed_for_user, single, notice_settings


urlpatterns = [
    re_path(r"^$", notices, name="notification_notices"),
    re_path(r"^settings/$", notice_settings, name="notification_notice_settings"),
    re_path(r"^(\d+)/$", single, name="notification_notice"),
    re_path(r"^feed/$", feed_for_user, name="notification_feed_for_user"),
    re_path(r"^mark_all_seen/$", mark_all_seen, name="notification_mark_all_seen"),
]
