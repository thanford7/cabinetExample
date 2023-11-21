from celery import shared_task
from celery.utils.log import get_task_logger

from app.models import RxFill

logger = get_task_logger(__name__)


@shared_task
def update_rx_status(rx_status_data: dict):
    logger.info('Updating RX status')
    logger.info(rx_status_data)
    rx = RxFill.objects.get(id=rx_status_data['id'])
    rx.status = rx_status_data['status']
    rx.update_sent_dt = rx_status_data['update_sent_dt']
    rx.save()
    