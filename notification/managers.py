import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType

from .settings import OBSOLETE_DAYS


class NoticeSettingManager(models.Manager):

    def get_or_create(self, user=None, notice_type=None, backend=None,
                      **kwargs):
        try:
            return self.get(user=user,
                            notice_type=notice_type,
                            backend=backend.path()), False
        except self.model.DoesNotExist:
            default = backend.sensitivity <= notice_type.default
            setting = self.create(user=user,
                                  notice_type=notice_type,
                                  backend=backend.path(),
                                  send=default)
            return setting, True


class NoticeManager(models.Manager):

    def notices_for(self, user, archived=False, unseen=None, on_site=None,
                    sent=False):
        """
        returns Notice objects for the given user.

        If archived=False, it only include notices not archived.
        If archived=True, it returns all notices for that user.

        If unseen=None, it includes all notices.
        If unseen=True, return only unseen notices.
        If unseen=False, return only seen notices.
        """
        if sent:
            lookup_kwargs = {"sender": user}
        else:
            lookup_kwargs = {"recipient": user}
        qs = self.filter(**lookup_kwargs)
        if not archived:
            qs = qs.filter(archived=archived)
        if unseen is not None:
            qs = qs.filter(unseen=unseen)
        if on_site is not None:
            qs = qs.filter(on_site=on_site)
        return qs.select_related('notice_type')

    def unseen_count_for(self, recipient, **kwargs):
        """
        returns the number of unseen notices for the given user but does not
        mark them seen
        """
        return self.notices_for(recipient, unseen=True, **kwargs).count()

    def received(self, recipient, **kwargs):
        """
        returns notices the given recipient has recieved.
        """
        kwargs["sent"] = False
        return self.notices_for(recipient, **kwargs)

    def sent(self, sender, **kwargs):
        """
        returns notices the given sender has sent
        """
        kwargs["sent"] = True
        return self.notices_for(sender, **kwargs)

    def get_obsolete_notices(self):
        d = datetime.datetime.now() - datetime.timedelta(days=OBSOLETE_DAYS)
        query = self.exclude(unseen=True).filter(added__lt=d)
        return query

    def delete_obsolete_notices(self):
        query = self.get_obsolete_notices()
        deleted = 0
        for p in query.iterator():
            p.delete()
            deleted += 1
        return deleted


class ObservedItemManager(models.Manager):

    def all_for(self, observed, signal):
        """
        Returns all ObservedItems for an observed object,
        to be sent when a signal is emited.
        """
        content_type = ContentType.objects.get_for_model(observed)
        observed_items = self.filter(content_type=content_type,
                object_id=observed.id, signal=signal)
        return observed_items

    def get_for(self, observed, observer, signal):
        content_type = ContentType.objects.get_for_model(observed)
        observed_item = self.get(content_type=content_type,
                object_id=observed.id, user=observer, signal=signal)
        return observed_item
