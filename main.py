import os
from loguru import logger
from dotenv import load_dotenv
from fastapi import FastAPI
from src.scheduler import create_trigger, scheduler
from src.routes import router as scheduler_router
from src.db import get_db
from src.repos.job import JobRepo
from src.utils.module import load_function
from src.config import APP_DESCRIPTION
from src.entities import JobTrigger

load_dotenv()

# FastAPI app
app = FastAPI(
    title="Scheduler API", 
    description=APP_DESCRIPTION, 
    docs_url="/"
)

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    job_repo = JobRepo(db=db)
    jobs = job_repo.list()
    for job_entry in jobs:
        # Convert the trigger to a JobTrigger object
        trigger = create_trigger(JobTrigger(**job_entry.trigger))
        # Load the function
        func = load_function(job_entry.func)
        # Add the job to the scheduler
        scheduler.add_job(
            id=job_entry.job_id,
            func=func,
            trigger=trigger,
            args=job_entry.args,
            kwargs=job_entry.kwargs,
            replace_existing=True
        )
    # Start the scheduler
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    # Shutdown the scheduler
    scheduler.shutdown()
    logger.info("Scheduler shut down.")

# Routes
app.include_router(scheduler_router)

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=os.getenv("HOST", "0.0.0.0"), 
        port=os.getenv("PORT", 8050), 
        log_level=os.getenv("LOG_LEVEL", "info"), 
        reload=os.getenv("RELOAD", False)
    )
