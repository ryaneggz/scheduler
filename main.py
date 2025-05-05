import importlib
from fastapi import FastAPI
from apscheduler.triggers.cron import CronTrigger

from src.models import ScheduledJob
from src.scheduler import scheduler
from src.routes import router as scheduler_router
from src.db import get_db
from src.utils.module import load_function
# FastAPI app
app = FastAPI(title="Scheduler API", description="API for scheduling jobs", docs_url="/")

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    jobs = db.query(ScheduledJob).all()
    for job_entry in jobs:
        trigger = CronTrigger.from_crontab(job_entry.trigger["expression"])
        
        func = load_function(job_entry.func)
        
        scheduler.add_job(
            id=job_entry.job_id,
            func=func,
            trigger=trigger,
            args=job_entry.args,
            kwargs=job_entry.kwargs,
            replace_existing=True
        )
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    print("Scheduler shut down.")

# Routes
app.include_router(scheduler_router)

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
