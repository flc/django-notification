from notification.backends.base import NotificationBackend


class WebBackend(NotificationBackend):
    slug = "web"
    display_name = "Web"
    formats = ["short.txt", "full.txt"]

    def send(
        self, sender, recipient, notice_type, context, on_site=False, *args, **kwargs
    ):
        """Always "sends" (i.e. stores to the database), setting on_site accordingly."""
        # TODO can't do this at the top or we get circular imports
        from notification.models import Notice

        if not self.should_send(sender, recipient, notice_type):
            on_site = False

        Notice.objects.create(
            recipient=recipient,
            message=self.format_message(notice_type.label, "notice.html", context),
            notice_type=notice_type,
            on_site=on_site,
            data=context,
            sender=sender,
            **kwargs
        )
        return True
