from fastapi import FastAPI
from loguru import logger
from src.scheduler import scheduler, JOBS_LIST

for job in JOBS_LIST:
    scheduler.add_job(
        job["func"],
        job["trigger"],
        id=job["id"],
        replace_existing=job["replace_existing"]
    )

# FastAPI app
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started.")

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
