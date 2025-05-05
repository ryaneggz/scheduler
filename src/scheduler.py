from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from src.db import DATABASE_URL
from loguru import logger

# Scheduler setup
jobstores = {'default': SQLAlchemyJobStore(url=DATABASE_URL)}
scheduler = AsyncIOScheduler(jobstores=jobstores)

def my_job():
    logger.info("Scheduled task executed.")
    
def my_job2():
    logger.info("Scheduled 2 task executed.")
    
JOBS_LIST = [
	{
		"id": "my_job",
		"func": my_job,
		"trigger": IntervalTrigger(seconds=3),
		"replace_existing": True
	},
	{
		"id": "my_job2",
		"func": my_job2,
		"trigger": CronTrigger(minute='*'),
		"replace_existing": True
	},
]