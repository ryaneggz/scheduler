from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from src.entities import JobTrigger
from src.db import DATABASE_URL
from loguru import logger

# Scheduler setup
jobstores = {'default': SQLAlchemyJobStore(url=DATABASE_URL)}
scheduler = AsyncIOScheduler(jobstores=jobstores)

def create_trigger(trigger: JobTrigger):
    if trigger.type == "cron":
        return CronTrigger.from_crontab(trigger.expression)
    else:
        raise ValueError("Invalid trigger type")

def my_job():
    logger.info("Scheduled task executed.")
    
def my_job2():
    logger.info("Scheduled 2 task executed.")
    
def job_with_args(a, b):
    logger.info(f"Scheduled task with args {str(a)} and {str(b)} executed.")