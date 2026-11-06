---
name: mock_websites
description: "How to set up and manipulate mock web application state via HTTP APIs for CUA-Gym tasks. For setup-gen and reward-gen agents."
user-invocable: false
---

# Mock Websites — Setup & State Injection Guide

This skill teaches **setup-gen** how to create initial web app state and golden patches for mock website tasks. Unlike file-based domains, mock website tasks involve **HTTP state injection** — there are no local files on the VM.

- Libraries: `requests`, `json`, `uuid`
- All 16 mocks are deployed at `https://cua-gym-<name>.xlang.ai`

---

## 0. Mock Website Registry

All mocks are publicly deployed. The URL pattern is `https://cua-gym-<name>.xlang.ai` where `<name>` is the directory name without `_mock`, with underscores replaced by hyphens.

| Mock | Public URL | SCHEMA.md |
|------|-----------|-----------|
| asana_mock | `https://cua-gym-asana.xlang.ai` | `openrlvr-mock/asana_mock/SCHEMA.md` |
| aws_console_mock | `https://cua-gym-aws-console.xlang.ai` | `openrlvr-mock/aws_console_mock/SCHEMA.md` |
| discord_mock | `https://cua-gym-discord.xlang.ai` | `openrlvr-mock/discord_mock/SCHEMA.md` |
| docusign_mock | `https://cua-gym-docusign.xlang.ai` | `openrlvr-mock/docusign_mock/SCHEMA.md` |
| github_mock | `https://cua-gym-github.xlang.ai` | `openrlvr-mock/github_mock/SCHEMA.md` |
| gitlab_mock | `https://cua-gym-gitlab.xlang.ai` | `openrlvr-mock/gitlab_mock/SCHEMA.md` |
| gmail_mock | `https://cua-gym-gmail.xlang.ai` | `openrlvr-mock/gmail_mock/SCHEMA.md` |
| jira_mock | `https://cua-gym-jira.xlang.ai` | `openrlvr-mock/jira_mock/SCHEMA.md` |
| linkedin_mock | `https://cua-gym-linkedin.xlang.ai` | `openrlvr-mock/linkedin_mock/SCHEMA.md` |
| notion_mock | `https://cua-gym-notion.xlang.ai` | `openrlvr-mock/notion_mock/SCHEMA.md` |
| reddit_mock | `https://cua-gym-reddit.xlang.ai` | `openrlvr-mock/reddit_mock/SCHEMA.md` |
| salesforce_mock | `https://cua-gym-salesforce.xlang.ai` | `openrlvr-mock/salesforce_mock/SCHEMA.md` |
| slack_mock | `https://cua-gym-slack.xlang.ai` | `openrlvr-mock/slack_mock/SCHEMA.md` |
| trello_mock | `https://cua-gym-trello.xlang.ai` | `openrlvr-mock/trello_mock/SCHEMA.md` |
| twitter_mock | `https://cua-gym-twitter.xlang.ai` | `openrlvr-mock/twitter_mock/SCHEMA.md` |
| youtube_mock | `https://cua-gym-youtube.xlang.ai` | `openrlvr-mock/youtube_mock/SCHEMA.md` |

---

## 1. State API

Every mock exposes identical HTTP endpoints:

### POST `/post?sid=<sid>` — State Injection

| Action | Body | Effect |
|--------|------|--------|
| `set` | `{"action":"set", "state":{...}}` | Writes current_state AND creates initial_state (if first write). Used by `initial_setup.py`. |
| `set_current` | `{"action":"set_current", "state":{...}}` | Writes ONLY current_state. Never touches initial_state. Used by `golden_patch.py`. |
| `reset` | `{"action":"reset"}` | Deletes both current and initial state files. |

All actions support `"merge": true` to deep-merge into existing state instead of replacing.

### GET `/go?sid=<sid>` — State Inspection

Returns:
```json
{
  "initial_state": { ... },
  "current_state": { ... },
  "state_diff": { ... }
}
```

- `initial_state` = snapshot from first `action:"set"` call
- `current_state` = latest state (updated by UI interactions or `set_current`)
- `state_diff` = keys that changed between initial and current

### GET `/state?sid=<sid>` — Raw State Read

Returns `{stored_state, has_custom_state, sid}`.

### POST `/upload?sid=<sid>` — File Upload

Upload files (attachments, images, documents) to the mock server. Files are stored per-session and served via `/files/`.

**Request**: `multipart/form-data` with one or more file fields.

**Response**:
```json
{
  "success": true,
  "files": [
    {
      "original_name": "report.pdf",
      "stored_name": "a1b2c3d4_report.pdf",
      "size": 12345,
      "content_type": "application/pdf",
      "url": "/files/<sid>/a1b2c3d4_report.pdf"
    }
  ]
}
```

**Usage in initial_setup.py** — upload a file and reference its URL in state:
```python
import requests

# Upload a file
with open('/path/to/attachment.pdf', 'rb') as f:
    resp = requests.post(
        f'{BASE_URL}/upload?sid={sid}',
        files={'file': ('attachment.pdf', f, 'application/pdf')},
        timeout=30
    )
uploaded = resp.json()['files'][0]
file_url = uploaded['url']  # e.g., /files/<sid>/a1b2c3d4_attachment.pdf

# Reference it in state injection
state['messages']['general'].append({
    'messageId': 'msg_1',
    'content': 'Here is the report',
    'attachments': [{'name': 'attachment.pdf', 'url': file_url, 'size': uploaded['size']}],
    # ... other fields
})
```

### GET `/files/<sid>/<filename>` — Serve Uploaded Files

Returns the uploaded file with appropriate Content-Type header. Files are served with `Content-Disposition: attachment`.

---

## 2. Session ID (sid) Pattern

The sid links `initial_setup.py`, `golden_patch.py`, and `reward.py` to the same state.

**Flow:**
1. `initial_setup.py` generates a UUID sid → writes to `/tmp/task_web_sid` on the VM
2. `initial_setup.py` POSTs `action:"set"` with the sid → creates both initial and current state
3. `golden_patch.py` reads sid from `/tmp/task_web_sid` → POSTs `action:"set_current"` → updates ONLY current state
4. `reward.py` reads sid from `/tmp/task_web_sid` → GETs `/go?sid=<sid>` → compares initial vs current

```python
# Generate and persist sid (initial_setup.py)
import uuid
sid = str(uuid.uuid4())
with open('/tmp/task_web_sid', 'w') as f:
    f.write(sid)

# Read sid (golden_patch.py and reward.py)
with open('/tmp/task_web_sid') as f:
    sid = f.read().strip()
```

---

## 3. State Schemas

Each mock has a schema file documenting the full state shape, default IDs, and observable state changes. Schemas are stored locally in this skill directory.

**MANDATORY: Always read the schema before writing state injection code.** The schema tells you:
- Required top-level keys (e.g., `currentUser`, `channels`, `messages` for slack)
- Object shapes for each entity type
- Default IDs for users, channels, projects, etc.
- Which state fields change when the user performs specific actions

**To load the schema for a mock** (do this in Step 0, immediately after reading this SKILL.md):
```
Read: .claude/skills/mock_websites/schemas/<mock_name>.md
```

Example — for a Slack task:
```
Read: .claude/skills/mock_websites/schemas/slack_mock.md
```

For multi-mock tasks, read ALL schemas for every mock listed in `task_config.json`'s `domains` array.

**Available schemas:** asana_mock, aws_console_mock, discord_mock, docusign_mock, github_mock, gitlab_mock, gmail_mock, jira_mock, linkedin_mock, notion_mock, reddit_mock, salesforce_mock, slack_mock, trello_mock, twitter_mock, youtube_mock.

If no schema file exists for a mock, inspect the mock's default state via `GET /go?sid=nonexistent` to discover the state shape (it returns default data when no custom state is set).

---

## 4. initial_setup.py Template

```python
"""
Initial Setup: <task_description>
Task ID: <task_id>
Domain: mock_websites
Mock: <mock_name>
"""
import json
import os
import shlex
import subprocess
import time
import uuid

import requests

# --- Config ---
BASE_URL = 'https://cua-gym-<name>.xlang.ai'  # e.g., cua-gym-slack.xlang.ai
sid = str(uuid.uuid4())

# Persist sid for golden_patch.py and reward.py
with open('/tmp/task_web_sid', 'w') as f:
    f.write(sid)

# --- Build initial state ---
# Consult SCHEMA.md for the full state shape.
# Include ALL required top-level keys. Missing keys → blank UI or crash.
state = {
    # ... full state matching SCHEMA.md ...
}

# --- Inject state ---
resp = requests.post(
    f'{BASE_URL}/post?sid={sid}',
    json={'action': 'set', 'state': state},
    timeout=30
)
assert resp.status_code == 200, f'State injection failed: {resp.text}'
print(f'State injected: sid={sid}')

# --- Verify ---
go = requests.get(f'{BASE_URL}/go?sid={sid}', timeout=10).json()
assert go['initial_state'] is not None, 'initial_state is None after injection'
print('Verified: initial_state and current_state are set')

# --- Launch browser ---
def launch_gui(command, delay_sec=1.0):
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)

launch_gui(f'google-chrome "{BASE_URL}/?sid={sid}"', delay_sec=2.0)
print(f'GUI_READY: launched browser at {BASE_URL}/?sid={sid}')
```

---

## 5. golden_patch.py Template

**CRITICAL: Always use `action:"set_current"`. NEVER use `action:"set"` in golden_patch.py.**

Using `action:"set"` would overwrite `initial_state`, making `state_diff` empty and breaking reward evaluation entirely.

```python
"""
Golden Patch: <task_description>
Task ID: <task_id>
Domain: mock_websites
Mock: <mock_name>
Changes: <brief list of what this patch does>
"""
import copy
import json

import requests

# --- Config ---
BASE_URL = 'https://cua-gym-<name>.xlang.ai'

# Read sid from initial_setup.py
with open('/tmp/task_web_sid') as f:
    sid = f.read().strip()

# --- Fetch current initial state ---
go = requests.get(f'{BASE_URL}/go?sid={sid}', timeout=10).json()
state = copy.deepcopy(go['initial_state'])

# --- Apply ONLY the minimal changes the task requires ---
# Example: send a message in #general
# state['messages']['general'].append({
#     'messageId': 'msg_new_1',
#     'senderId': 'user_1',
#     'content': 'Hello world!',
#     'timestamp': '2024-06-15T14:30:00Z',
#     'threadId': None,
#     'reactions': [],
#     'attachments': [],
#     'isEdited': False
# })

# --- Write ONLY current_state (preserve initial_state) ---
resp = requests.post(
    f'{BASE_URL}/post?sid={sid}',
    json={'action': 'set_current', 'state': state},
    timeout=30
)
assert resp.status_code == 200, f'set_current failed: {resp.text}'
print(f'Golden state applied via set_current: sid={sid}')

# --- Verify diff exists ---
go2 = requests.get(f'{BASE_URL}/go?sid={sid}', timeout=10).json()
assert go2['state_diff'], 'state_diff is empty — golden state matches initial (no changes applied)'
print(f'Verified: state_diff is non-empty')
```

---

## 6. Multi-Mock Tasks

When `task_config.json` contains a `domains` list with multiple mocks:

```json
{
  "domains": ["slack_mock", "notion_mock"],
  "task_instruction": "Copy the meeting notes from Slack #general to a new Notion page"
}
```

Use the **same sid** across all mocks:

```python
# initial_setup.py — inject into ALL listed mocks
sid = str(uuid.uuid4())
with open('/tmp/task_web_sid', 'w') as f:
    f.write(sid)

mocks = {
    'slack_mock': 'https://cua-gym-slack.xlang.ai',
    'notion_mock': 'https://cua-gym-notion.xlang.ai',
}

for name, url in mocks.items():
    state = build_state_for(name)  # mock-specific state
    resp = requests.post(f'{url}/post?sid={sid}', json={'action': 'set', 'state': state}, timeout=30)
    assert resp.status_code == 200

# Launch browser with primary mock
launch_gui(f'google-chrome "{mocks["slack_mock"]}/?sid={sid}"', delay_sec=2.0)
```

Golden patch similarly uses `set_current` on each mock that should change.

---

## 7. Sanity Check (for setup-gen Step 7)

Instead of `ls /home/user/`, use curl to verify state:

```bash
python3 scripts/env_cli.py -c "<workdir>/env_config_initial.json" execute \
  "sid=\$(cat /tmp/task_web_sid); curl -s 'https://cua-gym-slack.xlang.ai/go?sid='\$sid | python3 -m json.tool | head -60"
```

---

## 8. Bitter Lessons

1. **`action:"set"` in golden_patch.py is the #1 bug.** It overwrites initial_state, making state_diff empty. Reward scripts that compare initial vs current will always see 0 diff → reward = 0. ALWAYS use `action:"set_current"`.

2. **Missing state keys cause blank pages.** If you inject `{"channels": [...]}` without `currentUser`, `users`, `messages`, etc., the UI renders empty or crashes. Always provide ALL required top-level keys from SCHEMA.md.

3. **Array keys are replaced, not merged.** `deepMerge` treats arrays as atomic values. If you POST `{"messages": {"general": [msg1]}}` with `merge: true`, it replaces the entire `general` array. To add a message, fetch current state first, append, then write back.

4. **sid must be alphanumeric + hyphens + underscores.** The server sanitizes sid with `[^a-zA-Z0-9_-]`. UUIDs work perfectly. Do not use special characters.

5. **State is NOT persisted in the browser.** The browser fetches state from the server on page load via `?sid=xxx`. If you inject state after the browser loads, the user must refresh. Always inject state BEFORE launching the browser.

6. **`/go` without sid returns default state.** Always include `?sid=<sid>` in all API calls. Missing sid returns the app's built-in default data, not your injected state.

7. **Timestamps should be ISO 8601.** Most mocks expect `"2024-06-15T14:30:00Z"` format. Using Unix timestamps or other formats may cause rendering issues.

8. **IDs must be unique within their collection.** When adding new messages, channels, etc., generate unique IDs (e.g., `msg_new_1`, `ch_custom_1`). Duplicate IDs cause silent data corruption.

9. **golden_patch should copy initial_state and apply minimal changes.** Don't build golden state from scratch — start from `go['initial_state']`, deep-copy it, and modify only what the task requires. This ensures the state_diff accurately reflects task completion.

10. **HTTPS is required.** All mocks are served over HTTPS at `cua-gym-*.xlang.ai`. HTTP will not work.
