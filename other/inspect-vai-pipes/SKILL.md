---
name: inspect-vai-pipes
description: Use when debugging, inspecting, or analyzing Vertex AI Pipeline jobs - checking worker logs, diagnosing 429 errors, confirming parameters, analyzing scores, finding straggler tasks, or estimating completion time. Also use when pipeline runs fail, hang, or produce unexpected results.
---

# Inspect Vertex AI Pipelines

Debug and analyze Vertex AI Pipeline jobs using the SDK, Cloud Logging, and GCS artifacts.

## Required Inputs from User

- **Pipeline display name or run ID** (e.g., `my-pipeline-run-20260319-150709`)
- **GCP project ID** (e.g., `hybrid-vertex`)
- **Region** (e.g., `us-central1`)
- **GCS bucket** for pipeline artifacts (if checking evidence reports, logs, progress)

## Quick Reference

| Task             | Method                                                                   |
| ---------------- | ------------------------------------------------------------------------ |
| Find pipeline    | `aiplatform.PipelineJob.list()` + filter by display name                 |
| Get state        | `r.state` (see state codes below)                                        |
| Get parameters   | `r.gca_resource.runtime_config.parameter_values`                         |
| Get task details | `r.task_details` (list of tasks with state, name, execution metadata)    |
| Worker logs      | Cloud Logging: `resource.type="ml_job"`                                  |
| Pipeline events  | Cloud Logging: `resource.type="aiplatform.googleapis.com/PipelineJob"`   |
| GCS artifacts    | Check `evidence_reports/`, `progress.json`, log files in pipeline bucket |

## Pipeline State Codes

| Code | State      | Description            |
| ---- | ---------- | ---------------------- |
| 1    | QUEUED     | Waiting to start       |
| 2    | PENDING    | Being prepared         |
| 3    | RUNNING    | Actively executing     |
| 4    | SUCCEEDED  | Completed successfully |
| 5    | FAILED     | Terminated with error  |
| 6    | CANCELLING | Cancel in progress     |
| 7    | CANCELLED  | User cancelled         |
| 8    | PAUSED     | Paused                 |
| 9    | SKIPPED    | Skipped (caching)      |

## Task Execution State Codes

| Code | State            | Notes                                              |
| ---- | ---------------- | -------------------------------------------------- |
| 1    | PENDING          |                                                    |
| 2    | RUNNING_DRIVER   |                                                    |
| 3    | DRIVER_SUCCEEDED | Also seen for lightweight tasks that skip executor |
| 4    | RUNNING_EXECUTOR |                                                    |
| 5    | SUCCEEDED        |                                                    |
| 7    | CANCELLED        | Upstream dependency failed                         |
| 8    | CACHED/SKIPPED   | KFP caching hit — task reused previous output      |
| 9    | FAILED           |                                                    |

## Pipeline DAG Structure (3-Component)

The pipeline uses a `ParallelFor` over datasets with 3 chained components per table:

```
for each table in datasets:
    get-table-metadata(table)          # lightweight BQ metadata, always runs
        |
        v
    scan-table(table, modified_time)   # Dataplex DATA_DOCUMENTATION scan, KFP cached
        |
        v
    run-fan-out-wrapper(scan_results)  # main worker, caching disabled
```

When inspecting, look for this chain per worker. If `scan-table` fails, `run-fan-out-wrapper` shows state=9 (SKIPPED) since its upstream dependency failed.

## Step 1: Find and Inspect the Pipeline

```python
from google.cloud import aiplatform
aiplatform.init(project='PROJECT_ID', location='REGION')

# Find by display name substring
runs = aiplatform.PipelineJob.list()
r = [r for r in runs if 'SEARCH_TERM' in (r.display_name or '')][0]

print(f'Display Name: {r.display_name}')
print(f'Resource Name: {r.resource_name}')
print(f'State: {r.state}')  # See state codes above
print(f'Created: {r.create_time}')

# Parameters
params = r.gca_resource.runtime_config.parameter_values
for k, v in sorted(params.items()):
    print(f'  {k}: {v}')

# Task details — include error messages for quick triage
for t in r.task_details:
    err = ''
    if t.error and t.error.message:
        err = t.error.message[:150]
    print(f'{t.task_name}: state={t.state} err={err}')
```

**Common gotcha:** `PipelineJob` objects lack `start_time` and `end_time` attributes. Use `create_time` and check Cloud Logging for actual start/end timestamps.

**Display name vs resource name:** The `display_name` and `resource_name` often differ slightly (e.g., `my-pipeline-20260319-150709` vs `my-pipeline-run-20260319-150709`). Always search with a substring.

## Step 2: Query Worker Logs (Cloud Logging)

Worker container logs use `resource.type="ml_job"`. Pipeline orchestration events use `resource.type="aiplatform.googleapis.com/PipelineJob"`.

### Get pipeline task events (start/complete times)

```bash
gcloud logging read \
  'resource.type="aiplatform.googleapis.com/PipelineJob" AND "PIPELINE_RUN_ID"' \
  --project=PROJECT_ID --limit=50 --format=json --order=asc
```

Parse with: `e['jsonPayload']['payload']['taskName']`, `state`, `startTime`, `endTime`

### Get worker execution logs

```bash
# Key execution milestones (epochs, scores, errors, timeouts, completions)
gcloud logging read \
  'resource.type="ml_job" AND
   (jsonPayload.message=~"EPOCH|Critic Score|completed|evidence|Error|429|ReadError|TimeoutError|crashed" OR
    jsonPayload.levelname="ERROR") AND
   timestamp>="PIPELINE_START_TIME"' \
  --project=PROJECT_ID --limit=500 \
  --format="value(timestamp,resource.labels.job_id,jsonPayload.message)" --order=asc
```

**Always include `resource.labels.job_id`** in the format string. Each ParallelFor worker runs in a separate container with a unique `job_id`. You need this to map logs to specific containers/datasets and build per-container progress reports.

**Log structure:** Worker logs are in `jsonPayload.message` (not `textPayload`). The `levelname` field contains `INFO`, `ERROR`, `WARNING`.

**Important:** Lightweight component logs (e.g., `get-table-metadata`, `scan-table`) often have empty `jsonPayload.message`. Use `textPayload` or full JSON format instead:

```bash
# For lightweight components, get the job_id from the task error message, then:
gcloud logging read \
  'resource.type="ml_job" AND resource.labels.job_id="JOB_ID" AND resource.labels.task_name="workerpool0-0"' \
  --project=PROJECT_ID --limit=50 \
  --format="value(jsonPayload.message)" --order=asc

# If messages are empty, try JSON format to see all fields:
gcloud logging read \
  'resource.type="ml_job" AND resource.labels.job_id="JOB_ID"' \
  --project=PROJECT_ID --limit=10 --format=json --order=desc
```

### Filter for specific issues

```bash
# 429 rate limit errors (Gemini API + Memory Bank)
jsonPayload.message=~"429|RESOURCE_EXHAUSTED"

# Critic scores
jsonPayload.message=~"Critic Score"

# Epoch transitions
jsonPayload.message=~"EPOCH.*Concurrency"

# Worker task assignments
jsonPayload.message=~"\\[Worker \\d+\\] Executing"

# Memory Bank writes
jsonPayload.message=~"Memory Bank|memory bank"

# GCS uploads (evidence reports, progress)
jsonPayload.message=~"Uploaded.*evidence|Uploaded.*progress"

# Pipeline completion
jsonPayload.message=~"fan_out_insights completed"
```

## Step 3: Check GCS Artifacts

```python
from google.cloud import storage
client = storage.Client(project='PROJECT_ID')
bucket = client.bucket('BUCKET_NAME')

# Evidence reports (per-epoch summaries)
for b in client.list_blobs(bucket, prefix='pipeline_root/evidence_reports/'):
    print(f'{b.name} ({b.size} bytes, updated {b.updated})')

# Progress file (live status)
blob = bucket.blob('pipeline_root/evidence_reports/progress.json')
if blob.exists():
    import json
    print(json.loads(blob.download_as_text()))

# Main log file
blob = bucket.blob('pipeline_root/evidence_reports/react_loop_fanout_log.json')
if blob.exists():
    print(f'Log size: {blob.size} bytes')
```

**Artifact paths may vary.** Some pipelines write to `pipeline_root/evidence_reports/`, others to `self-evolve/pipeline_root/evidence_reports/`. Check both.

## Step 4: Analyze Scores

Extract and analyze critic scores from logs:

```python
import re
from collections import Counter

scores, novelty_scores = [], []
persisted, not_persisted = 0, 0

for line in log_lines:
    score_m = re.search(r'Critic Score:\s*([\d.]+)', line)
    novelty_m = re.search(r'Novelty:\s*([\d.]+)', line)
    persist_m = re.search(r'Persist:\s*(True|False)', line)
    if score_m:
        scores.append(float(score_m.group(1)))
        if novelty_m: novelty_scores.append(float(novelty_m.group(1)))
        if persist_m: (persisted if persist_m.group(1) == 'True' else not_persisted) + 1

print(f'Total: {len(scores)}, Persisted: {persisted}, Rate: {persisted/len(scores)*100:.1f}%')
print(f'Mean: {sum(scores)/len(scores):.3f}, Max: {max(scores):.3f}, Min: {min(scores):.3f}')
```

**Floor scores (0.10) are NOT always errors.** Before assuming floor scores are API failures, check for `"Critic scoring failed"` or `"Skipping critic"` in the logs. If those messages are absent, the critic agent legitimately scored the insight at 0.10 — this is a quality signal, not a rate-limiting problem. True API failures return `0.0` (not `0.10`) via the error handler. Only diagnose floor scores as a rate-limiting issue when accompanied by actual error log messages.

## Common Issues

### Massive 429 Errors

**Symptom:** Logs flooded with `HTTP/1.1 429 Too Many Requests` or `RESOURCE_EXHAUSTED`

**Root cause:** `concurrency` param too high. Effective parallelism = `concurrency × num_datasets`. At concurrency=100 with 5 datasets = 500 simultaneous API calls.

**Fix:** Reduce concurrency to 20-30 per dataset.

### Memory Bank RESOURCE_EXHAUSTED

**Symptom:** `Quota exceeded for quota metric 'Memory Bank write requests'`

**Root cause:** Memory Bank write quota is 100 writes/min/region. High concurrency overwhelms the rate limiter.

**Fix:** Lower concurrency, or increase semaphore delay in `react_loop_fanout.py`.

### Straggler Workers

**Symptom:** Pipeline running long after most workers complete. One or two tasks still in state 2/4.

**Diagnosis:** Check which `for-loop-1-worker-N` tasks are still running. Cross-reference with `dataset_item` in task execution metadata to identify the slow dataset.

**Common causes:** Large tables triggering slow Dataplex scans, workers stuck in retry loops from persistent 429s.

### Pipeline State SKIPPED (9)

**Cause:** Vertex AI pipeline caching. If inputs match a previous run, tasks may be skipped entirely.

**Fix:** Change a parameter value or disable caching in the pipeline definition.

### scan-table Component Failures

The `scan-table` component runs in a lightweight `python:3.11` container with only `google-cloud-dataplex` installed. Common failure modes:

**`AttributeError: DATA_DOCUMENTATION`**
- **Cause:** Pinned `google-cloud-dataplex` version too old. `DataScanType.DATA_DOCUMENTATION` was added in later versions (needs >=2.10.0).
- **Fix:** Update version pin in `deploy_vertex_pipeline.py` `scan_table` component's `packages_to_install`.

**`501 Received http2 header with status: 404` on `create_data_scan`**
- **Cause:** Regional Dataplex endpoint (`{location}-dataplex.googleapis.com:443`) does NOT support `DATA_DOCUMENTATION` scan type. Only the global endpoint (`dataplex.googleapis.com`) works.
- **Fix:** Use `DataScanServiceClient()` without `client_options` (defaults to global endpoint).
- **Note:** The existing `src/dataplex_client.py` also uses the regional endpoint — this works for `DATA_PROFILE` but not `DATA_DOCUMENTATION` in some SDK versions.

**Cascading failures pattern:** When `scan-table` fails, `run-fan-out-wrapper` shows state=9 (SKIPPED) and `for-loop-1-worker-N` shows state=7 (CANCELLED) with error "The DAG failed because some tasks failed: [scan-table]". This is expected — fix the `scan-table` error and the downstream tasks will run.

### KFP Component Version Mismatches

**Symptom:** Component works locally but fails in pipeline with import/attribute errors.

**Root cause:** KFP `@dsl.component` containers install packages at runtime via pip. The pinned versions may differ from your local environment. A `python:3.11` base image also has different system packages than your dev machine.

**Diagnosis:** Check the worker logs for pip install output and the actual traceback. The error usually shows the exact missing attribute or module.

**Fix:** Match the version pins in `packages_to_install` to your local working versions. Check with `importlib.metadata.version('package-name')`.

### Container Bootstrap Time Variance

**Symptom:** Some `ParallelFor` containers start 3-4 minutes after others even though all were submitted simultaneously.

**Cause:** Vertex AI schedules containers across available resources. Startup time includes image pull, pip install of `packages_to_install`, and driver initialization. This is normal behavior, not an error.

**Impact on analysis:** When calculating per-container durations, use each container's first log entry as its start time, not the pipeline's `create_time`. Otherwise you'll overestimate duration for late-starting containers.

### Per-Worker Timeout Patterns

**Symptom:** Workers killed by `asyncio.TimeoutError` before completing their LLM call.

**Key observations:**
- Timeout rates increase in later epochs (Epoch 2 > Epoch 1) because richer context from elite skills and crossover makes prompts larger and LLM responses slower
- Adaptive concurrency (auto-reducing concurrency when timeout rate exceeds a threshold) can mitigate this
- Tuning data points: 180s timeout → ~26% timeout rate; 240s timeout → ~10% timeout rate (with concurrency 30, 4-5 datasets)
- Timeouts are per-worker, not per-epoch — a single worker timing out doesn't affect others in the same epoch

**Diagnosis:** Search for `TimeoutError` in worker logs. Group by `resource.labels.job_id` to identify which containers are most affected. Late-starting containers or those processing larger tables tend to have higher timeout rates.

### Epoch Regression (Epoch 2 worse than Epoch 1)

**Symptom:** Mean scores decrease across epochs instead of improving.

**Common causes:** 429 errors during epoch 1 corrupted skill evolution feedback; floor scores (0.10) polluting aggregate metrics used for skill selection.

## Cross-Validating Source Code

When logs show unexpected behavior, check the source:

| Concern                        | File to Check                                                      |
| ------------------------------ | ------------------------------------------------------------------ |
| Pipeline parameters & defaults | `deploy_vertex_pipeline.py` (argparse block + `deploy_pipeline()`) |
| Pipeline DAG & components      | `deploy_vertex_pipeline.py` (`get_table_metadata`, `scan_table`, `run_fan_out_wrapper`, `my_pipeline`) |
| Component package versions     | `deploy_vertex_pipeline.py` (`packages_to_install` in each `@dsl.component`) |
| Precomputed scan passthrough   | `deploy_vertex_pipeline.py` (`scan_results` param) → `react_loop_fanout.py` (`PRECOMPUTED_SCAN_RESULTS` env var) |
| Worker execution logic         | `react_loop_fanout.py` (`fan_out_insights()`)                      |
| Concurrency / rate limiting    | `react_loop_fanout.py` (semaphore, delay constants)                |
| Critic scoring                 | `src/prompts/critic_scoring.md`                                    |
| Skill evolution                | `src/swarm_manager.py`                                             |
| API endpoint defaults          | `backend/main.py`                                                  |
| Dataplex data scans (fallback) | `src/dataplex_client.py`                                           |

## Per-Container Progress Reports

To build a per-container progress report, map `resource.labels.job_id` to datasets:

### Step 1: Get job_id → dataset mapping

```bash
# Get component metadata logs that show dataset_item assignments
gcloud logging read \
  'resource.type="aiplatform.googleapis.com/PipelineJob" AND "PIPELINE_RUN_ID" AND "dataset_item"' \
  --project=PROJECT_ID --limit=100 --format=json --order=asc
```

Alternatively, get task details from the SDK — each `for-loop-1-worker-N` task's execution metadata contains the `dataset_item` input value.

### Step 2: Query per-container metrics

```bash
# Get epoch transitions, scores, and errors per container
gcloud logging read \
  'resource.type="ml_job" AND resource.labels.job_id="JOB_ID" AND
   (jsonPayload.message=~"EPOCH|Critic Score|completed|TimeoutError|crashed")' \
  --project=PROJECT_ID --limit=200 \
  --format="value(timestamp,jsonPayload.message)" --order=asc
```

### Step 3: Aggregate per container

For each container, extract:
- **Epochs completed** (count `EPOCH` transition messages)
- **Insights generated** (count `Critic Score` lines)
- **Mean/max/min scores** (parse score values)
- **Timeout rate** (count `TimeoutError` / total workers per epoch)
- **Persist rate** (count `Persist: True` / total scored)
- **Wall-clock duration** (first log → last log timestamp)

## Estimating Completion Time

1. Check how many `for-loop-1-worker-N` tasks have completed vs still running
2. Note the wall-clock time of completed workers (from Cloud Logging task events)
3. Workers processing larger tables or hitting more 429s take proportionally longer
4. Account for container bootstrap stagger (3-4 min between first and last container start)
5. A 2-epoch run with concurrency 30 on 5 tables typically takes 1-2 hours
6. A 2-epoch run with concurrency 100 on 5 tables can take 2-3+ hours (due to 429 backoff)
7. Later epochs take longer due to richer context (larger prompts, more timeouts)

## Google Cloud Console

Pipeline runs can also be inspected in the console at:

```
https://console.cloud.google.com/vertex-ai/pipelines/locations/REGION/runs/PIPELINE_RUN_ID?project=PROJECT_ID
```

The console shows the DAG visualization, task states, logs, and parameter values.
