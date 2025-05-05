import importlib
from uuid import uuid4
from pydantic import BaseModel
from fastapi import Depends, APIRouter, HTTPException
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from src.scheduler import scheduler
from src.models import ScheduledJob
from src.db import get_db

USER_ONE_ID = str(uuid4())
USER_TWO_ID = str(uuid4())

class User(BaseModel):
    id: str
    username: str
    password: str
    
    
user_one = User(id=USER_ONE_ID, username="admin", password="admin")
user_two = User(id=USER_TWO_ID, username="user", password="user")

STATIC_USERS = [user_one, user_two]


def get_current_user():
    return STATIC_USERS[0]

router = APIRouter(tags=["jobs"])

class JobCreate(BaseModel):
    trigger: dict
    func: str
    args: list = []
    kwargs: dict = {}

@router.post("/jobs/")
async def create_job(job: JobCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    job_entry = ScheduledJob(**job.dict())
    db.add(job_entry)
    db.commit()
    db.refresh(job_entry)

    trigger = CronTrigger.from_crontab(job.trigger["expression"])
 
    # Get the function from the path
    func_path = job.func
    module_path, func_name = func_path.rsplit('.', 1)
    
    # Import the module dynamically
    module = importlib.import_module(module_path)
    func = getattr(module, func_name)
    
    scheduler.add_job(
        id=job_entry.job_id,
        func=func,
        trigger=trigger,
        args=job.args,
        kwargs=job.kwargs,
        replace_existing=True
    )
    return {"job_id": job_entry.job_id}

@router.get("/jobs/")
async def list_jobs(db: Session = Depends(get_db), user=Depends(get_current_user)):
    jobs = db.query(ScheduledJob).all()
    return [{"job_id": j.job_id, "trigger": j.trigger, "next_run": j.next_run} for j in jobs]

@router.patch("/jobs/{job_id}")
async def update_job(job_id: str, trigger: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    job_entry = db.query(ScheduledJob).filter_by(job_id=job_id).first()
    if not job_entry:
        raise HTTPException(404, "Job not found")

    scheduler.reschedule_job(job_id, trigger=CronTrigger(**trigger))
    job_entry.trigger = trigger
    db.commit()
    return {"status": "rescheduled"}

@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    job_entry = db.query(ScheduledJob).filter_by(job_id=job_id).first()
    if not job_entry:
        raise HTTPException(404, "Job not found")
    scheduler.remove_job(job_id)
    db.delete(job_entry)
    db.commit()
    return {"status": "deleted"}