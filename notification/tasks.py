from celery.decorators import task

from notification.engine import emit_batch
from notification.models import NoticeQueueBatch, Notice


@task(ignore_result=True)
def emit_notice_batch(notice_batch_id, **kwargs):
    try:
        batch = NoticeQueueBatch.objects.get(id=notice_batch_id)
    except NoticeQueueBatch.DoesNotExist, e:
        emit_notice_batch.retry(countdown=2, exc=e)
    else:
        emit_batch(batch)


@task(ignore_result=True)
def delete_obsolete_notices(**kwargs):
    return Notice.objects.delete_obsolete_notices()
