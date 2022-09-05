from celery import shared_task

from notification.engine import emit_batch
from notification.models import NoticeQueueBatch, Notice


@shared_task(ignore_result=True)
def emit_notice_batch(notice_batch_id, **kwargs):
    try:
        batch = NoticeQueueBatch.objects.get(id=notice_batch_id)
    except NoticeQueueBatch.DoesNotExist as e:
        emit_notice_batch.retry(countdown=2, exc=e)
    else:
        emit_batch(batch)


@shared_task(ignore_result=True)
def delete_obsolete_notices(**kwargs):
    return Notice.objects.delete_obsolete_notices()
