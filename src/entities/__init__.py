from pydantic import BaseModel, Field

class JobTrigger(BaseModel):
    type: str = Field(..., example="cron")
    expression: str = Field(..., example="0 0 * * *")
    
class JobId(BaseModel):
    id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    
class Job(JobId):
    trigger: JobTrigger
    func: str = Field(..., example="src.jobs.my_job")
    args: list = Field(default_factory=list)
    kwargs: dict = Field(default_factory=dict)

class JobCreate(BaseModel):
    trigger: JobTrigger
    func: str = Field(..., example="src.jobs.my_job")
    args: list = Field(default_factory=list)
    kwargs: dict = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True
        example = {
            "trigger": {
                "type": "cron",
                "expression": "0 0 * * *"
            },
            "func": "src.jobs.my_job",
            "args": [],
            "kwargs": {}
        }
        
class JobUpdated(BaseModel):
    job: Job = Field(..., example={'id': '123e4567-e89b-12d3-a456-426614174000'})
    
    class Config:
        example = {
            "job": {
                "id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
        
class JobList(BaseModel):
    jobs: list[Job] = Field(...)
    
    class Config:
        example = {
            "jobs": [
                {
                    "job_id": "123e4567-e89b-12d3-a456-426614174000",
                    "trigger": {
                        "type": "cron",
                        "expression": "0 0 * * *"
                    },
                    "func": "src.jobs.my_job",
                    "args": [],
                    "kwargs": {}
                }
            ]
        }
        
class JobDeleted(BaseModel):
    message: str = Field(..., example="Job deleted successfully")
    
    class Config:
        example = {
            "message": "Job deleted successfully"
        }