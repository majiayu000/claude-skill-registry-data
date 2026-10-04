---
name: evo-flink-session-job
description: Implement Flink jobs for Google Cluster Data analysis, specifically session-based analysis of task events. Handles parsing Google Cluster Data v2 CSV formats, session window computation on task SUBMIT events, and job completion filtering. Use for any task involving Flink + Google cluster trace data processing.
---

# Flink Session Job for Google Cluster Data

## Overview

This skill implements a Flink job that processes Google Cluster Data v2 traces to find the longest stage (session of SUBMIT events) per finished job.

## Key Concepts

### Google Cluster Data v2 Schema

**Task Events CSV** (13 columns):
timestamp, missing_info, job_id, task_index, machine_id, event_type, user, scheduling_class, priority, cpu_request, memory_request, disk_request, different_machines_constraint

**Job Events CSV** (8 columns):
timestamp, missing_info, job_id, event_type, user, scheduling_class, job_name, logical_job_name

**Event Types:**
- 0 = SUBMIT
- 1 = SCHEDULE
- 2 = EVICT
- 3 = FAIL
- 4 = FINISH
- 5 = KILL
- 6 = LOST
- 7 = UPDATE_PENDING
- 8 = UPDATE_RUNNING

**Timestamps** are in microseconds.

### Session/Stage Logic

- A "stage" is a burst of task SUBMIT events (event_type=0) for a given job
- A stage ends when there is an inactivity gap >= sesssize seconds (default 600s = 10 min)
- Gap in microseconds = sesssize * 1,000,000
- For each finished job (job event_type=4), find the stage with the most SUBMIT events
- If a task is submitted, fails/evicted, and resubmitted, each SUBMIT counts separately
- Output format: `(jobId,maxTaskCount)` one per line

## Files

### templates/
- `TaskEvent.java` - Parses task event CSV lines
- `JobEvent.java` - Parses job event CSV lines  
- `LongestSessionPerJob.java` - Main Flink job implementation

### scripts/
- `generate_java.py` - Copies template Java files to workspace

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-flink-session-job/scripts')
from generate_java import generate_all
generate_all('/app/workspace')
```

## Build & Run

```bash
# Build
cd /app/workspace && mvn clean package -q

# Start Flink cluster
/opt/flink/bin/start-cluster.sh

# Run job
/opt/flink/bin/flink run /app/workspace/target/LongestSessionPerJob-jar-with-dependencies.jar \
  --task_input /app/workspace/data/task_events/part-00001-of-00500.csv.gz \
  --job_input /app/workspace/data/job_events/part-00001-of-00500.csv.gz \
  --output /app/workspace/output.txt
```

## Implementation Notes

1. The job reads gzipped CSV files directly using Java's GZIPInputStream
2. Job events are read first to identify finished jobs (event_type=4)
3. Task events are then filtered for SUBMIT events of finished jobs only
4. Timestamps are sorted per job, and sessions are identified by gaps >= threshold
5. The session gap comparison uses strict less-than (`<`) for same-session membership,
   matching Flink's session window semantics
6. Output is written directly to a file using PrintWriter
7. The skeleton's env.execute() is not called since processing is done in main()

## Troubleshooting

- If Flink cluster is not running, start with `/opt/flink/bin/start-cluster.sh`
- Data files are gzipped CSV - ensure GZIPInputStream is used
- Timestamps are microseconds, not milliseconds or seconds
- The `sesssize` parameter is in seconds, multiply by 1,000,000 for microseconds
