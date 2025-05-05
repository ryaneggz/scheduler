from fastapi import Depends
from src.models import ScheduledJob
from src.db import get_db
from sqlalchemy.orm import Session

from src.entities import JobCreate
from src.exceptions import InternalServerErrorException, NotFoundException

class JobRepo:
    _instance = None
    
    def __new__(cls, db: Session = Depends(get_db)):
        if cls._instance is None:
            cls._instance = super(JobRepo, cls).__new__(cls)
            cls._instance.db = db
        return cls._instance
    
    def __init__(self, db: Session = Depends(get_db)):
        # The actual initialization happens in __new__
        # This ensures db can be updated if a new instance is requested with a different db
        self.db = db

    def list(self):
        return self.db.query(ScheduledJob).all()
    
    def create(self, job: JobCreate):
        job_entry = ScheduledJob(**job.dict())
        self.db.add(job_entry)
        self.db.commit()
        self.db.refresh(job_entry)
        return job_entry
    
    def update(self, job_id: str, job: JobCreate):
        job_entry = self.db.query(ScheduledJob).filter(ScheduledJob.id == job_id).first()
        if not job_entry:
            raise NotFoundException("Job not found")
        self.db.query(ScheduledJob).filter(ScheduledJob.id == job_id).update(job.dict())
        self.db.commit()
        self.db.refresh(job_entry)
        return job_entry
    
    def delete(self, job_id: str):
        try:
            self.db.query(ScheduledJob).filter(ScheduledJob.id == job_id).delete()
            self.db.commit()
        except Exception as e:
            raise InternalServerErrorException(e)
