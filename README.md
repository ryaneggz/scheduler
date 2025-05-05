# Advanced Python Scheduler Demo

### Development

```bash
## Virtual Env
uv venv

## ACtivate
source .venv/bin/activate

## Install
uv pip install -r requirements.txt

## Run
python main.py
```

### Run this in the `apscheduler` database

```sql
CREATE TABLE scheduled_jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(36) NOT NULL UNIQUE,
    trigger JSONB NOT NULL,
    func VARCHAR(255) NOT NULL,
    args JSONB NOT NULL DEFAULT '[]'::JSONB,
    kwargs JSONB NOT NULL DEFAULT '{}'::JSONB,
    next_run TIMESTAMPTZ NULL
);
```

### Example Queries


```bash
### Get Jobs
curl =X GET http://localhost:8000/jobs

### Without Args
curl -X POST http://localhost:8000/jobs/ \
  -H "Content-Type: application/json" \
  -d '{
    "trigger": {
      "type": "cron",
      "expression": "* * * * *"
    },
    "func": "src.scheduler.my_job",
    "args": [],
    "kwargs": {}
  }'


### With Args
curl -X POST http://localhost:8000/jobs/ \
  -H "Content-Type: application/json" \
  -d '{
    "trigger": {
      "type": "cron",
      "expression": "* * * * *"
    },
    "func": "src.scheduler.job_with_args",
    "args": [1, 3],
    "kwargs": {}
  }'
```