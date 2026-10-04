---
name: dl-status
description: Etat temps reel du datalake (git, API, jobs, worker) via preprocessing shell
disable-model-invocation: true
---

# Etat actuel du datalake

## Git
!`git -C /home/TheWatcher01/projects/datalake-souverain status --short 2>/dev/null | head -20`

## API
!`curl -sf http://localhost:3001/api/stats 2>/dev/null | head -5 || echo "API offline"`

## Worker
!`curl -sf http://localhost:3001/api/worker/stats 2>/dev/null | head -10 || echo "Worker stats unavailable"`

## Pending jobs
!`PGPASSWORD="${DATALAKE_DB_PASSWORD:-datalake_dev}" psql -h localhost -p 5434 -U datalake -d datalake -tAc "SELECT coalesce(string_agg(jobType || '=' || cnt, ', '), 'aucun') FROM (SELECT \"jobType\", count(*) as cnt FROM dl_job_queue WHERE status='pending' GROUP BY \"jobType\") t;" 2>/dev/null || echo "DB unavailable"`
