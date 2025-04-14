from logging import getLogger

from django.core.mail.backends.base import BaseEmailBackend

from .tasks import send_email_task

logger = getLogger(__name__)


class CeleryEmailBackend(BaseEmailBackend):
    """
    Custom email backend that uses Celery to send emails asynchronously.
    """
    def send_messages(self, email_messages):
        """
        Send the given email messages.
        """
        try:
            send_email_task.delay(email_messages)
        except Exception as e:
            logger.critical("Error sending email: %s", e)
