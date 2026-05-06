from .. import celery


@celery.task
def send_email_task(email):
    print(f"sending mail to {email}")
