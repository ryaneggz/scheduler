from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

# Database setup
DATABASE_URL = "postgresql+psycopg2://admin:test1234@localhost:5432/apscheduler"
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Scheduler setup
jobstores = {'default': SQLAlchemyJobStore(url=DATABASE_URL)}
scheduler = AsyncIOScheduler(jobstores=jobstores)

# Job definition
def my_job():
    logger.info("Scheduled task executed.")
    
def my_job2():
    logger.info("Scheduled 2 task executed.")

# Add job (every 3 seconds)
scheduler.add_job(
    my_job,
    IntervalTrigger(seconds=3),
    id="my_job_id",
    replace_existing=True
)

scheduler.add_job(
    my_job2,
    IntervalTrigger(seconds=5),
    id="my_job2_id",
    replace_existing=True
)
# FastAPI app
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started.")
    
    # This ensures the application keeps running until shutdown
    # The scheduler will continue to run in the background
    # and execute jobs according to their schedule

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
