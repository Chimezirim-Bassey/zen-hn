from logging import getLogger

from celery import shared_task
from django.core.mail import send_mail, get_connection

logger = getLogger(__name__)


@shared_task
def send_email_task(messages):
    """
    A Celery task to send an email.
    """
    try:
        conn = get_connection(backend="django.core.mail.backends.smtp.EmailBackend")
        res = conn.send_messages(messages)
        if not res:
            logger.error("No email messages were sent.")
    except Exception as err:
        logger.error("Error sending email: %s", err)


# celery -A proj worker -l INFO
