from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
import resend


class EmailBackend(BaseEmailBackend):

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        resend.api_key = settings.RESEND_API_KEY

    def send_messages(self, email_messages):

        if not email_messages:
            return 0

        sent = 0

        for message in email_messages:

            if not message.recipients():
                continue

            params = {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": message.to,
                "subject": message.subject,
                "html": message.body.replace("\n", "<br>"),
            }

            try:
                resend.Emails.send(params)
                sent += 1

            except Exception:

                if not self.fail_silently:
                    raise

        return sent