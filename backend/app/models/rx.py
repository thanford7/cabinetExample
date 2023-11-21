__all__ = ('RxFill',)

from enum import Enum

from django.db import models

from app.models.abstract import AuditFields


class RxFill(AuditFields):
    class FillStatus(Enum):
        SENT = 'SENT'
        RECEIVED = 'RECEIVED'
        PROCESSING = 'PROCESSING'
        FILLED = 'FILLED'
        PICKED_UP = 'PICKED UP'
    
    status = models.CharField(choices=[(fs.value, fs.value) for fs in FillStatus], default=FillStatus.SENT.value)
    update_sent_dt = models.DateTimeField()  # Used for optimistic locking
