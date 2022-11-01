from django.contrib import admin

from notification.models import NoticeType, NoticeSetting, Notice, ObservedItem, NoticeQueueBatch


class NoticeTypeAdmin(admin.ModelAdmin):
    list_display = ['label', 'display', 'description', 'default']
    search_fields = ['label']


class NoticeSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_id', 'notice_type', 'backend', 'backend', 'send')
    search_fields = ['=notice_type__label', '=user__username']
    list_filter = (
        'backend',
        'send',
    )


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['message', 'recipient', 'recipient_id', 'sender', 'notice_type', 'added', 'unseen', 'archived']
    search_fields = ['=notice_type__label', 'recipient__username']


admin.site.register(NoticeQueueBatch)
admin.site.register(NoticeType, NoticeTypeAdmin)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(ObservedItem)
