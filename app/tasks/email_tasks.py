from app.celery_app import celery
import logging


@celery.task
def send_email_task(email):
    logging.info(f"Sending email to {email}")
    print(f"sending mail to {email}")