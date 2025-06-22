from celery import shared_task

@shared_task
def send_welcome_email(user_email):
    # Simulate sending an email
    print(f"Sending email to {user_email}")
    return "Email sent"