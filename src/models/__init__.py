from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from uuid import uuid4
from src.db import Base

class ScheduledJob(Base):
    __tablename__ = "scheduled_jobs"

    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(String, unique=True, default=lambda: str(uuid4()))
    trigger = Column(JSON, nullable=False)   # e.g. {"type":"cron","hour":"*/1"}
    func = Column(String, nullable=False)      # e.g. "app.tasks.my_task"
    args = Column(JSON, default=[])
    kwargs = Column(JSON, default={})
    next_run = Column(DateTime, nullable=True)
