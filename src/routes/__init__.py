from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException

from src.db import get_db
from src.scheduler import create_trigger, scheduler
from src.utils.module import load_function
from src.entities import JobDeleted, JobList, JobUpdated, JobCreate
from src.repos.job import JobRepo

job_repo = JobRepo()
router = APIRouter(tags=["Job"])

### Create Job
@router.post(
    "/jobs", 
    status_code=201,
    responses={201: {"model": JobUpdated}}
)
async def create_job(job: JobCreate, db = Depends(get_db)):
    job_repo = JobRepo(db=db)
    job_entry = job_repo.create(job)
    trigger = create_trigger(job.trigger)
    func = load_function(job.func)
    scheduler.add_job(
        id=job_entry.job_id,
        func=func,
        trigger=trigger,
        args=job.args,
        kwargs=job.kwargs,
        replace_existing=True
    )
    return JSONResponse(
        status_code=201,
        content={"job": {"id": job_entry.job_id}}
    )

### List Jobs
@router.get("/jobs", responses={200: {"model": JobList}})
async def list_jobs(db = Depends(get_db)):
    job_repo = JobRepo(db=db)
    jobs = job_repo.list()
    return JSONResponse(
        status_code=200,
        content={
            "jobs": [
                {"id": j.job_id, "trigger": j.trigger, "next_run": j.next_run}
                for j in jobs
            ]
        }
    )

### Update Job
@router.patch("/jobs/{job_id}", responses={200: {"model": JobUpdated}})
async def update_job(job_id: str, job: JobCreate, db = Depends(get_db)):
    job_repo = JobRepo(db=db)
    try:
        trigger = create_trigger(job.trigger)
        scheduler.reschedule_job(job_id, trigger=trigger)
        job_repo.update(job_id, job)
        return JSONResponse(status_code=200, content={"job": {"id": job_id}})
    except Exception as e:
        raise HTTPException(400, "Failed to update job")

### Delete Job
@router.delete("/jobs/{job_id}", status_code=204, responses={204: {"model": None}})
async def delete_job(job_id: str, db = Depends(get_db)):
    job_repo = JobRepo(db=db)
    job_entry = job_repo.delete(job_id)
    if not job_entry:
        raise HTTPException(404, "Job not found")
    scheduler.remove_job(job_id)
    return JSONResponse(status_code=200, content=JobDeleted(message="Job deleted successfully"))