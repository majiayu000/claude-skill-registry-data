---
name: Database Upload
description: Upload estimation results to Supabase storage and register with Estimator API. Final phase of the estimation workflow.
---

# Database Upload

This skill uploads final estimation results to Supabase storage and registers them with the Backend Estimator API.

## When to Use This Skill

Use this skill when the user asks about:
- Uploading final estimation results to cloud storage
- Uploading comparative study results to cloud storage
- Registering estimation file metadata with the API
- Managing database upload for completed cost estimations or comparative studies

## Workflow Overview

This is the **final phase** in the estimation pipeline:

```
Ingestion → Context Extraction → Aggregation → Database Upload
```

**Purpose**: Take aggregation results and:
1. Upload JSON file to Supabase storage
2. Register file metadata with Estimator API
3. Update job status to COMPLETED
4. Return success/failure status

## CLI Usage

### Basic Upload

```bash
python upload_to_database.py \
  --file_to_upload temp_files/temp_project_123/aggregation_ui_xyz.json \
  --project_id project_123 \
  --job_id job_456
```

### Upload with Mode (Estimation)

```bash
python upload_to_database.py \
  --file_to_upload aggregation.json \
  --project_id project_123 \
  --job_id job_456 \
  --mode estimation
```

### Upload with Mode (Comparative Study)

```bash
python upload_to_database.py \
  --file_to_upload comparative_results.json \
  --project_id project_123 \
  --job_id job_456 \
  --mode comparative_study
```

### Command Options

```bash
usage: upload_to_database.py [-h] [--file_to_upload FILE] [--project_id ID] [--job_id ID] [--mode MODE]

options:
  -h, --help                Show help message
  --file_to_upload FILE     Path to aggregation JSON file
  --project_id ID          Project identifier
  --job_id ID              Job identifier for API registration
  --mode MODE              Upload mode: "estimation" or "comparative_study" (optional, defaults to estimation)
```

## Input Format

**Expected File:**
- Path: `temp_files/temp_project_{project_id}/aggregation_ui_uuid.json`
- Content: Final aggregation results from aggregation phase
- Format: JSON with projectId, projectName, and pricingLines array

**Example:**
```json
{
  "projectId": "project_123",
  "projectName": "Sample Project",
  "pricingLines": [
    {
      "id": "1",
      "type": "titre",
      "designation": "I - Site Preparation",
      "totalPrice": 50000.00,
      "indentLevel": 0
    }
  ]
}
```

## Output Format

**Storage Location:**
- Estimation mode: `estimator_files/receipt_drafts_ui/aggregation_ui_uuid.json`
- Comparative study mode: `estimator_files/comparative_files/results_files/aggregation_ui_uuid.json`
- Access: Public URL for API access

**API Registration:**
```json
{
  "status": "COMPLETED",
  "completed_at": "2025-11-05T14:15:00Z",
  "result_data": {
    "projectId": "project_123",
    "projectName": "Sample Project",
    "pricingLines": [...]
  }
}
```

## Processing Features

### 1. File Upload
- Uploads to mode-specific bucket:
  - **estimation**: `estimator_files/receipt_drafts_ui/`
  - **comparative_study**: `estimator_files/comparative_files/results_files/`
- Generates UUID-based filename
- Returns public URL for API access

### 2. API Registration
- Updates job status to COMPLETED
- Includes completion timestamp
- Stores full result data in job record

### 3. Error Handling
- Validates file exists before upload
- Verifies Supabase upload success
- Confirms API registration
- Logs all operations

## Configuration

### Environment Variables

Required in `.env` file:

```bash
# API Configuration
Backend_API_URL=
BACKEND_API_KEY=your_backend_api_key_here

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key_here
SUPABASE_BUCKET=estimo-archi-storage
```

### Storage Structure

```
estimo-archi-storage/
└── estimator_files/
    ├── receipt_drafts_ui/              # For estimation mode
    │   ├── aggregation_ui_xyz.json
    │   └── aggregation_ui_abc.json
    └── comparative_files/
        └── results_files/              # For comparative_study mode
            ├── aggregation_ui_def.json
            └── aggregation_ui_ghi.json
```

## Example Output

```bash
$ python upload_to_database.py --file_to_upload temp_files/temp_project_123/aggregation_ui_xyz.json --project_id project_123 --job_id job_456

2025-11-05 14:15:00 - INFO - Phase 5 - Database Upload: Processing file at temp_files/temp_project_123/aggregation_ui_xyz.json
2025-11-05 14:15:00 - INFO - Uploading aggregation results to Supabase: estimator_files/receipt_drafts_ui/aggregation_ui_xyz.json
2025-11-05 14:15:01 - INFO - Successfully uploaded to: https://storage.supabase.co/v1/object/public/bucket/estimator_files/receipt_drafts_ui/aggregation_ui_xyz.json
2025-11-05 14:15:01 - INFO - Phase 5 complete. Uploaded aggregation results for project 'project_123'
```

## Error Messages

### File Not Found
```
ERROR: The specified local file does not exist: temp_files/temp_project_123/missing.json
```

### Upload Failure
```
ERROR: Failed to upload the local file to Supabase
```

### API Registration Failure
```
ERROR: Failed to register the file_to jobs with the Backend API
```

## Dependencies

```python
# Core
import os
import logging
import mimetypes
import uuid
import json
from datetime import datetime, timezone
from pathlib import Path

# Local
from .api_utils.api_client import BackendClient
from .api_utils.supabase_client import SupabaseClient
```

## Validation

The skill validates:
- ✅ Input file exists and is readable
- ✅ Valid JSON format
- ✅ Supabase upload successful
- ✅ API registration successful

## Troubleshooting

**Environment variables not loaded:**
- Ensure `.env` file exists with required variables

**Supabase upload fails:**
- Check `SUPABASE_KEY` and bucket permissions
- Verify `SUPABASE_BUCKET` name is correct

**API registration fails:**
- Verify `BACKEND_API_KEY` is valid
- Check `Backend_API_URL` endpoint accessibility

**Invalid file path:**
- Use absolute paths or paths relative to script location
- Ensure file has `.json` extension

---

**Version:** 2.0 (Simplified)
**Last Updated:** November 2025