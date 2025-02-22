from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.notifications import check_application_deadlines

def init_scheduler():
    scheduler = BackgroundScheduler()
    # Check deadlines every day at midnight
    scheduler.add_job(check_application_deadlines, 'cron', hour=0)
    scheduler.start()
