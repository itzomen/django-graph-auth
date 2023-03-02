"""
Sample tasks:

from celery import shared_task


@shared_task(bind=True, max_retries=3, on_failure=_email_send_failure)
def async_email_send(
    self,
    subject,
    from_email,
    message,
    html_message,
    recipient_list,
    fail_silently=False,
):
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=fail_silently,
            html_message=html_message,
        )
    except Exception as exc:
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
        logger.warning(f"Exception occurred while sending email: {exc}")
        self.retry(exc=exc, countdown=5)
"""
