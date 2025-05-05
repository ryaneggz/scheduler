import importlib
from fastapi import FastAPI
from apscheduler.triggers.cron import CronTrigger

from src.models import ScheduledJob
from src.scheduler import scheduler
from src.routes import router
from src.db import get_db

# FastAPI app
app = FastAPI(title="Scheduler API", description="API for scheduling jobs")

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    jobs = db.query(ScheduledJob).all()
    for job_entry in jobs:
        trigger = CronTrigger.from_crontab(job_entry.trigger["expression"])
        
        # Get the function from the path
        func_path = job_entry.func
        module_path, func_name = func_path.rsplit('.', 1)
        
        # Import the module dynamically
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)
        
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

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
