import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://admin:test1234@localhost:5432/apscheduler")

APP_DESCRIPTION = """
This API utilizes the APScheduler library to schedule jobs.

The following endpoints are available:

- `POST /jobs`: Create a new job
- `GET /jobs`: List all jobs
- `PATCH /jobs/{job_id}`: Update a job
- `DELETE /jobs/{job_id}`: Delete a job
"""