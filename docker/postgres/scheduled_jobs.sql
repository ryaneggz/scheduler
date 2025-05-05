CREATE TABLE scheduled_jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(36) NOT NULL UNIQUE,
    trigger JSONB NOT NULL,
    func VARCHAR(255) NOT NULL,
    args JSONB NOT NULL DEFAULT '[]'::JSONB,
    kwargs JSONB NOT NULL DEFAULT '{}'::JSONB,
    next_run TIMESTAMPTZ NULL
); 