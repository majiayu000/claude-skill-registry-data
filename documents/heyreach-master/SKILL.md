---
name: heyreach-master
description: "Internal resource library for HeyReach integration. Contains shared API client, operation scripts, and reference documentation."
---

# HeyReach Master (Internal)

Internal resource library containing:
- API client (`heyreach_client.py`)
- Config checker (`check_heyreach_config.py`)
- All operation scripts
- Reference documentation

---

## Architecture: DRY Principle

**Problem solved:** HeyReach skills would have duplicated content (setup instructions, API docs, auth flow, error handling).

**Solution:** Extract shared content into `heyreach-master/references/` and `heyreach-master/scripts/`, then reference from each skill.

**Result:** Single source of truth, reduced context per skill.

---

## Shared Resources

All HeyReach skills reference these resources (progressive disclosure).

### references/

**[setup-guide.md](references/setup-guide.md)** - Complete setup wizard
- Getting API key from HeyReach
- Environment configuration
- Verifying connection

**[api-reference.md](references/api-reference.md)** - HeyReach API patterns
- Base URL and authentication
- All endpoints documented
- Request/response examples
- Pagination patterns

**[error-handling.md](references/error-handling.md)** - Troubleshooting
- Common errors and solutions
- HTTP error codes
- Rate limiting
- Debug tips

### scripts/

#### Authentication & Configuration

**[check_heyreach_config.py](scripts/check_heyreach_config.py)** - Pre-flight validation
```bash
python check_heyreach_config.py [--json]
```
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--json` | No | False | Output structured JSON for AI consumption |

Exit codes: 0=configured, 1=partial, 2=not configured

**When to Use:** Run this FIRST before any HeyReach operation. Use to validate API key is configured, diagnose authentication issues, or check if setup is needed.

---

**[heyreach_client.py](scripts/heyreach_client.py)** - Shared API client
```python
from heyreach_client import get_client, HeyReachError

client = get_client()
result = client.post("/v2/campaigns/All", {"offset": 0, "limit": 100})
```

Features:
- Automatic retry with exponential backoff
- Rate limit handling (300 req/min)
- Consistent error responses
- API key management from .env

---

## Intelligent Error Detection Flow

When a HeyReach skill fails due to missing configuration, the AI should:

### Step 1: Run Config Check with JSON Output

```bash
python 00-system/skills/heyreach/heyreach-master/scripts/check_heyreach_config.py --json
```

### Step 2: Parse the `ai_action` Field

| ai_action | What to Do |
|-----------|------------|
| `proceed_with_operation` | Config OK, continue with the original operation |
| `prompt_for_api_key` | Ask user: "I need your HeyReach API key from Settings → API" |
| `create_env_file` | Create `.env` file and ask user for credentials |
| `verify_api_key` | Key exists but connection failed - verify it's correct |
| `retry_later` | API timeout - try again |
| `check_network` | Connection error - verify network |

### Step 3: Help User Fix Issues

If `ai_action` is `prompt_for_api_key`:

1. Tell user: "HeyReach integration needs setup. I need your API key."
2. Show them: "Get it from HeyReach: Settings → API"
3. Ask: "Paste your HeyReach API key:"
4. Once they provide it, **write directly to `.env`**:
   ```
   HEYREACH_API_KEY=their-key-here
   ```
5. Re-run config check to verify

---

## Environment Variables

Required in `.env`:
```
HEYREACH_API_KEY=your-api-key-here
```

---

## API Base URL

All API requests go to: `https://api.heyreach.io/api/public`

Authentication header: `X-API-KEY: {api_key}`

Rate limit: 300 requests/minute

---

## Script Usage Patterns

### List Campaigns
```python
from heyreach_client import get_client

client = get_client()
result = client.post("/v2/campaigns/All", {"offset": 0, "limit": 100})
campaigns = result.get("items", [])
```

### Get Campaign Details
```python
result = client.get(f"/v2/campaigns/{campaign_id}")
```

### Add Leads
```python
leads = [
    {"linkedInUrl": "https://linkedin.com/in/user1"},
    {"linkedInUrl": "https://linkedin.com/in/user2"}
]
result = client.post(f"/v2/campaigns/{campaign_id}/leads", {"leads": leads})
```

### Error Handling
```python
from heyreach_client import get_client, HeyReachError

try:
    client = get_client()
    result = client.get("/v2/campaigns/123")
except HeyReachError as e:
    print(f"Error {e.status_code}: {e.message}")
except ValueError as e:
    print(f"Config error: {e}")
```

---

**Version**: 1.0
**Created**: 2025-12-19
**Status**: Production Ready
