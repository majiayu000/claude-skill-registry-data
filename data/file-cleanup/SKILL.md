---
name: file-cleanup
description: Session-based file cleanup for privacy compliance. Use to delete temporary files, uploaded clinical notes, generated outputs, and expired logs to maintain HIPAA-friendly operations.
---

# File Cleanup Skill

## Overview

This skill handles deletion of temporary session files and expired logs to maintain privacy compliance and prevent disk space exhaustion. All PHI (Protected Health Information) is deleted immediately after processing.

## When to Use

Use this skill to:
- Delete uploaded clinical notes after processing
- Remove generated JSON outputs after serving to user
- Clear session directories when processing completes
- Delete expired log files (>30 days old)
- Maintain HIPAA-compliant data retention policies

## Installation

**IMPORTANT**: This skill has its own isolated virtual environment (`.venv`) managed by `uv`. Do NOT use system Python.

Initialize the skill's environment:
```bash
# From the skill directory
cd .agent/skills/file-cleanup
uv sync  # Creates .venv (no external dependencies, uses Python stdlib)
```

No external dependencies - uses Python standard library (`pathlib`, `os`).

## Usage

**CRITICAL**: Always use `uv run` to execute code with this skill's `.venv`, NOT system Python.

### Initialize Cleanup Manager

```python
# From .agent/skills/file-cleanup/ directory
# Run with: uv run python -c "..."
from file_cleanup import FileCleanup

# Initialize with defaults
cleanup = FileCleanup(
    data_dir=".data/sessions",  # Temporary session files
    log_dir="logs"               # Log files directory
)
```

### Session Cleanup (Most Common)

```python
# Delete all files for a specific session
session_id = "abc123-clinical-note"
deleted_count = cleanup.delete_session_files(session_id)
print(f"Deleted {deleted_count} files from session {session_id}")
```

### Delete Individual Files

```python
# Safely delete a specific file
file_path = ".data/sessions/abc123/uploaded_note.txt"
success = cleanup.delete_file(file_path)

if success:
    print(f"Deleted: {file_path}")
else:
    print(f"File not found or already deleted: {file_path}")
```

### Delete All Sessions

```python
# WARNING: Deletes ALL session data
total_deleted = cleanup.delete_session_files()  # No session_id = delete all
print(f"Deleted {total_deleted} files from all sessions")
```

### Create Session Directory

```python
import uuid

# Create unique session directory
session_id = str(uuid.uuid4())
session_dir = cleanup.create_session_dir(session_id)
print(f"Session directory created: {session_dir}")

# Now you can save files to this directory
note_path = session_dir / "uploaded_note.txt"
note_path.write_text(clinical_note_content)
```

### List Session Files

```python
# List all files in a session (for debugging)
files = cleanup.list_session_files(session_id)
for file_path in files:
    print(f"Session file: {file_path}")
```

### Delete Expired Logs

```python
# Delete logs older than 30 days (default retention)
deleted_logs = cleanup.delete_expired_logs(retention_days=30)
print(f"Deleted {deleted_logs} expired log files")
```

## Typical Session Lifecycle

```python
from pathlib import Path
import uuid

# 1. Start session - create directory
session_id = str(uuid.uuid4())
session_dir = cleanup.create_session_dir(session_id)

# 2. Save uploaded file
uploaded_file = session_dir / "note.txt"
uploaded_file.write_text(clinical_note_text)

# 3. Generate outputs
toc_path = session_dir / "toc.json"
summary_path = session_dir / "summary.json"
plan_path = session_dir / "plan.json"

# ... processing happens ...

# 4. Serve outputs to user (Flask response)
# ... send JSON files to user ...

# 5. Immediate cleanup (delete ALL session files)
cleanup.delete_session_files(session_id)
```

## Privacy Compliance

**HIPAA Best Practices**:
1. **Immediate Deletion**: Delete uploaded notes right after processing
2. **Output Cleanup**: Delete generated JSONs after serving to user
3. **Session Isolation**: Use unique session IDs to prevent cross-contamination
4. **Log Sanitization**: Never log actual PHI - use summaries only (handled by `structured-logging` skill)
5. **Retention Policy**: Auto-delete logs after 30 days

## Integration with Flask Web App

```python
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)
cleanup = FileCleanup()

@app.route('/upload', methods=['POST'])
def upload_note():
    session_id = str(uuid.uuid4())
    
    try:
        # Create session directory
        session_dir = cleanup.create_session_dir(session_id)
        
        # Save uploaded file
        file = request.files['clinical_note']
        note_path = session_dir / "note.txt"
        file.save(note_path)
        
        # Process note...
        result = process_clinical_note(note_path)
        
        # Generate outputs
        toc_path = session_dir / "toc.json"
        toc_path.write_text(result.toc_json)
        
        # Serve to user
        response = jsonify(result.to_dict())
        
        # Cleanup immediately (even before response sent)
        cleanup.delete_session_files(session_id)
        
        return response
        
    except Exception as e:
        # Cleanup on error too
        cleanup.delete_session_files(session_id)
        raise
```

## Cron Job for Log Cleanup

Add to crontab for automated log cleanup:

```bash
# Run daily at 2 AM to delete logs >30 days old
0 2 * * * cd /path/to/project && uv run python -c "from src.skills.file_cleanup.file_cleanup import FileCleanup; FileCleanup().delete_expired_logs()"
```

## Best Practices

1. **Always Cleanup**: Use try/finally or context managers to ensure cleanup happens
2. **Session Isolation**: Unique session IDs prevent file collisions
3. **Immediate Deletion**: Delete as soon as processing completes
4. **Error Handling**: Cleanup even when errors occur
5. **Audit Trail**: Log cleanup operations (without listing actual file contents)

## Error Handling

- Delete operations are safe - no error if file/directory doesn't exist
- Partial deletions succeed (e.g., if one file is locked, others still deleted)
- All errors are silently handled to prevent cleanup failures from blocking workflows

## Implementation

See `file_cleanup.py` for the full Python implementation.
