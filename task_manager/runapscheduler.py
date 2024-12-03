# import logging
# from datetime import timedelta
# from django.utils.timezone import now
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.interval import IntervalTrigger
# from django_apscheduler.jobstores import DjangoJobStore, register_events
# from django.core.mail import send_mail
# from .models import Task

# # Set up logging
# logger = logging.getLogger(__name__)

# def notify_upcoming_tasks():
#     # Check for tasks due in the next 24 hours and send email notifications.
#     upcoming_time = now() + timedelta(hours=24)  # Calculate time 24 hours from now
#     tasks = Task.objects.filter(due_date__lte=upcoming_time, due_date__gt=now(), task_status=Task.Status.IN_PROGRESS)

#     for task in tasks:
#         try:
#             send_mail(
#                 subject=f"Reminder: Task '{task.task_name}' is due soon",
#                 message=f"Hello {task.user.username},\n\nYour task '{task.task_name}' is due on {task.due_date}. Please complete it on time!",
#                 from_email="kotolada1@gmail.com",  # Replace with your email
#                 recipient_list=[task.user.email],
#                 fail_silently=False,
#             )
#             logger.info(f"Reminder email sent for task '{task.task_name}' to {task.user.email}.")
#         except Exception as e:
#             logger.error(f"Error sending email for task '{task.task_name}': {e}")

# def start_scheduler():
#     # Set up the scheduler to run periodically.
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")

#     # Add the job to check tasks every hour
#     scheduler.add_job(
#         notify_upcoming_tasks,
#         trigger=IntervalTrigger(hours=1),  # Adjust interval as needed
#         id="notify_upcoming_tasks",  # Unique job ID
#         replace_existing=True,
#     )

#     # Register events and start the scheduler
#     register_events(scheduler)
#     scheduler.start()
#     logger.info("APScheduler has been started.")

