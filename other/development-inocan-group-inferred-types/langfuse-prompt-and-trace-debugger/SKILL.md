---
name: langfuse-prompt-and-trace-debugger
description: MANDATORY skill when KeyError or schema errors occur. Fetch actual prompt schemas instead of guessing. Use for debugging traces and understanding AI model behavior.
---

# Langfuse Prompt & Trace Debugger - MANDATORY FOR KEYERRORS

## 🔥 CRITICAL: Use This Skill Immediately When:

**MANDATORY triggers (you MUST use this skill):**
- ❗ Tests fail with `KeyError` (e.g., `KeyError: 'therapist_response'`)
- ❗ Schema validation errors
- ❗ Unexpected prompt response structure
- ❗ Need to understand what fields a prompt actually returns

**Common triggers:**
- User asks to view a specific prompt
- Code references a prompt but logic is unclear
- Investigating why AI behavior doesn't match expectations
- Debugging Langfuse traces
- Analyzing model output in production

**🚀 PROACTIVE TRIGGERS (non-obvious scenarios where you should automatically use this skill):**

1. **Production Debugging Queries:**
   - "Why didn't user X get a message?"
   - "Why did this intervention not fire?"
   - "What errors happened in production [timeframe]?"
   - "Debug this trace ID from Slack alert"
   - User reports: "AI didn't respond" or "got wrong response"
   - **→ Use `fetch_error_traces.py` to find error traces automatically**

2. **Performance & Cost Investigation:**
   - "Why are OpenAI costs high this week?"
   - "Which prompts are slowest?"
   - "Show me what happened during [time window]"
   - Job timeout errors in CloudWatch/logs
   - **→ Use `fetch_traces_by_time.py` to analyze patterns**

3. **Response Validation Issues:**
   - Logs show `_validation_error` metadata
   - "LLM returned unexpected structure"
   - Pydantic validation errors on AI responses
   - **→ Use `fetch_trace.py` with trace ID to see actual vs expected**

4. **Intervention Logic Questions:**
   - "How does X intervention condition work?"
   - "What fields does cronjobs_yaml expect?"
   - "Show me actual intervention logic from production"
   - **→ Use `refresh_prompt_cache.py` to fetch YAML configs as prompts**

5. **Error Pattern Analysis:**
   - "Are users hitting a specific error frequently?"
   - "Find all traces with 'timeout' errors"
   - "Search for traces containing [error message]"
   - **→ Use `search_trace_errors.py` to grep across traces**

**❌ ANTI-PATTERNS (violations of this skill):**
- Saying "I need to check production" without actually fetching traces
- Debugging "why didn't user get X" by reading code instead of checking actual traces
- Investigating costs/performance by guessing instead of analyzing real trace data
- Answering "how does X work?" about prompts without fetching the actual prompt

## 🚨 VIOLATION: Guessing at Schemas

**WRONG:** "The prompt probably returns {field_name}, let me add that to the code"
**RIGHT:** *Uses this skill to fetch actual prompt, reads actual schema*

**DO NOT:**
- ❌ Assume field names without checking
- ❌ Guess at optional vs required fields
- ❌ Try multiple field names hoping one works
- ❌ Look at old code and assume it's current

**DO THIS:**
1. ✅ cd to `.claude/skills/langfuse-prompt-and-trace-debugger`
2. ✅ Run `uv run python refresh_prompt_cache.py PROMPT_NAME`
3. ✅ Read `docs/cached_prompts/PROMPT_NAME_production.txt`
4. ✅ Read `docs/cached_prompts/PROMPT_NAME_production_config.json`
5. ✅ Use the ACTUAL schema you just read

## 🏢 Understanding Langfuse Servers vs Labels

**CRITICAL: We have TWO separate Langfuse servers:**

1. **Staging Langfuse Server** (`https://langfuse.staging.cncorp.io`)
   - Separate database/instance on staging ECS cluster
   - Used for development and testing
   - Has prompts tagged with "production" label - these are DEFAULT prompts for staging tests
   - ⚠️ "production" label here does NOT mean real user-facing prompts

2. **Production Langfuse Server** (`https://langfuse.prod.cncorp.io`)
   - Separate database/instance on production ECS cluster
   - Used for real user-facing application
   - Has prompts tagged with "production" label - these ARE the real prompts shown to users
   - ✅ "production" label here means actual live prompts

**Key Points:**
- The two servers are **completely independent** - no automatic sync between them
- Both servers use the same label system (`production`, `development`, `staging`, etc.)
- A prompt with "production" label on **staging server** ≠ prompt with "production" label on **prod server**
- Labels control which prompt version is served within each server
- Server selection is controlled by `LANGFUSE_HOST` environment variable

## Environment Setup

**Required environment variables:**
- `LANGFUSE_PUBLIC_KEY` - Langfuse API public key
- `LANGFUSE_SECRET_KEY` - Langfuse API secret key
- `LANGFUSE_HOST` - Langfuse server URL
  - Staging: `https://langfuse.staging.cncorp.io`
  - Production: `https://langfuse.prod.cncorp.io`

**Optional:**
- `ENVIRONMENT` - Label to fetch within the server (defaults to "production")
  - This is the LABEL/TAG within whichever server you're connected to
  - NOT the same as which Langfuse server you're querying

**Setup:**
```bash
# Add to arsenal/.env:
# For STAGING Langfuse server (default for development):
LANGFUSE_PUBLIC_KEY_STAGING=pk-lf-...  # pragma: allowlist-secret
LANGFUSE_SECRET_KEY_STAGING=sk-lf-...  # pragma: allowlist-secret
LANGFUSE_HOST_STAGING=https://langfuse.staging.cncorp.io

# For PRODUCTION Langfuse server (real user-facing prompts):
LANGFUSE_PUBLIC_KEY_PROD=pk-lf-...  # pragma: allowlist-secret
LANGFUSE_SECRET_KEY_PROD=sk-lf-...  # pragma: allowlist-secret
LANGFUSE_HOST_PROD=https://langfuse.prod.cncorp.io

# Select which server to use:
LANGFUSE_ENVIRONMENT=staging  # or 'production'
```

**No manual environment loading needed!** The scripts automatically find and load `arsenal/.env` from anywhere in the project.

## Available Scripts

### 1. refresh_prompt_cache.py - Download Prompts Locally

Downloads Langfuse prompts to `docs/cached_prompts/` for offline viewing.

**IMPORTANT: Can fetch from BOTH staging and production servers**

**Usage:**
```bash
# Navigate to the skill directory
cd .claude/skills/langfuse-prompt-and-trace-debugger

# Fetch from STAGING (default)
uv run python refresh_prompt_cache.py PROMPT_NAME

# Fetch from PRODUCTION (explicit flag)
uv run python refresh_prompt_cache.py PROMPT_NAME --production

# Fetch all prompts from staging
uv run python refresh_prompt_cache.py

# Fetch all prompts from production
uv run python refresh_prompt_cache.py --production

# Fetch multiple prompts from production
uv run python refresh_prompt_cache.py prompt1 prompt2 prompt3 --production
```

**Environment Selection:**
- **Default:** Fetches from STAGING server (safe)
- **With `--production` flag:** Fetches from PRODUCTION server
- Clearly indicates which server is being used in output

**Cached Location:**
- `docs/cached_prompts/{prompt_name}_production.txt` - Prompt content + version
- `docs/cached_prompts/{prompt_name}_production_config.json` - Configuration

### 2. check_prompts.py - List Available Prompts

Lists all prompts available in Langfuse and checks their availability in the current environment.

**Usage:**
```bash
# Navigate to the skill directory
cd .claude/skills/langfuse-prompt-and-trace-debugger

# Check all prompts
uv run python check_prompts.py
```

**Output:**
- Lists all prompt names in Langfuse
- Shows which prompts are available in the specified environment (from `ENVIRONMENT` variable)
- Color-coded indicators (✓ green for available, ✗ red for missing)
- Summary statistics

### 3. fetch_trace.py - View Langfuse Traces

Fetch and display Langfuse traces for debugging AI model behavior.

**Usage:**
```bash
# Navigate to the skill directory
cd .claude/skills/langfuse-prompt-and-trace-debugger

# Fetch specific trace by ID
uv run python fetch_trace.py db29520b-9acb-4af9-a7a0-1aa005eb7b24

# Fetch trace from Langfuse URL
uv run python fetch_trace.py "https://langfuse.example.com/project/.../traces?peek=db29520b..."

# List recent traces
uv run python fetch_trace.py --list --limit 5

# View help
uv run python fetch_trace.py --help
```

**What it shows:**
- Trace ID and metadata
- All observations (LLM calls, tool uses, etc.)
- Input/output for each step
- Timing information
- Hierarchical display of nested observations
- Useful for debugging AI workflows

### 4. fetch_error_traces.py - Find Traces with Errors

Fetch traces that contain ERROR-level observations from a specified time range. Useful for investigating production issues and error patterns.

**Usage:**
```bash
# Navigate to the skill directory
cd .claude/skills/langfuse-prompt-and-trace-debugger

# Fetch error traces from last 24 hours (default)
uv run python fetch_error_traces.py

# Fetch error traces from last 48 hours
uv run python fetch_error_traces.py --hours 48

# Fetch error traces from last 7 days
uv run python fetch_error_traces.py --days 7

# Limit results to 5 traces
uv run python fetch_error_traces.py --limit 5

# Query production server for errors
uv run python fetch_error_traces.py --env production

# View help
uv run python fetch_error_traces.py --help
```

**What it shows:**
- Traces that contain observations with ERROR level
- Trace metadata (ID, name, timestamp, user)
- Error messages from failed observations
- Direct links to view traces in Langfuse UI
- Time-filtered results (last N hours/days)

**Common use cases:**
- Monitor production errors from the last day
- Investigate error patterns across multiple traces
- Find traces related to specific failure modes
- Debug issues reported by users

### 5. reconstruct_compiled_prompt.py - Prompt Reconstruction

Reconstructs **full** prompts from database + Langfuse template. Uses the same compilation logic as the admin panel prompt playground.

**⚠️ Lives in CODEBASE at `api/src/cli/` - uses shared `compile_prompt()` service.**

**Requires:**
- `--message-id` or `-m`: Message ID from the database
- `--prompt-name` or `-p`: Langfuse prompt name (e.g., `daily_question_summary`)

```bash
# Basic usage (from project root) - defaults to production database
cd api && PYTHONPATH=src python src/cli/reconstruct_compiled_prompt.py -m 91245 -p daily_question_summary

# A/B test with specific prompt version
cd api && PYTHONPATH=src python src/cli/reconstruct_compiled_prompt.py -m 91245 -p daily_question_summary --version 5

# Save to file
cd api && PYTHONPATH=src python src/cli/reconstruct_compiled_prompt.py -m 91245 -p daily_question_summary -o docs/debug/full_prompt.md

# Output as JSON
cd api && PYTHONPATH=src python src/cli/reconstruct_compiled_prompt.py -m 91245 -p daily_question_summary --json

# Use local docker database (for development)
cd api && PYTHONPATH=src python src/cli/reconstruct_compiled_prompt.py --local -m 12345 -p group_msg_intervention_needed

# List available prompts in Langfuse
cd api && PYTHONPATH=src python src/cli/reconstruct_compiled_prompt.py --list-prompts
```

**When to use:**
| Use Case | Command |
|----------|---------|
| Prompt reconstruction from message | `reconstruct_compiled_prompt.py -m MESSAGE_ID -p PROMPT_NAME` |
| A/B testing prompt versions | `reconstruct_compiled_prompt.py -m MESSAGE_ID -p PROMPT_NAME --version N` |
| List available prompts | `reconstruct_compiled_prompt.py --list-prompts` |

## Understanding Prompt Configs

### Prompt Text File
- Instructions: What AI should do
- Output format: JSON schema, required fields
- Variables: `{{sender_name}}`, `{{current_message}}`, etc.
- Allowed values: Enumerated options for fields
- Version: Header shows version

### Config JSON File
```json
{
  "model_config": {
    "model": "gpt-4.1",
    "temperature": 0.7,
    "response_format": {
      "type": "json_schema",  // or "json_object"
      "json_schema": { ... }
    }
  }
}
```

**response_format types:**
- `json_object` - Unstructured (model decides fields)
- `json_schema` - Strict validation (fields enforced)

## Debugging Workflows

### KeyError in Tests
1. Fetch the prompt using `refresh_prompt_cache.py`
2. Check if field is optional/conditional in prompt text
3. Check config: `json_object` vs `json_schema`
4. Fix test to handle optional field OR update prompt

### Schema Validation Fails
1. Fetch the prompt using `refresh_prompt_cache.py`
2. Read config's `json_schema` section
3. Check `required` array
4. Verify code provides all required parameters

### Understanding AI Behavior
1. Get trace ID from logs or Langfuse UI
2. Use `fetch_trace.py` to view full trace
3. Examine inputs, outputs, and intermediate steps
4. Check for unexpected model responses

### Investigating Production Errors
1. Use `fetch_error_traces.py` to find recent error traces
2. Review error messages and trace metadata
3. Use `fetch_trace.py` with specific trace ID for detailed analysis
4. Identify patterns across multiple error traces
5. Check for common error causes (API failures, schema issues, etc.)

## Quick Reference

```bash
# Setup (one-time)
# Add LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST to arsenal/.env
# Make sure to add # pragma: allowlist-secret comments after secrets

# Navigate to skill directory
cd .claude/skills/langfuse-prompt-and-trace-debugger

# List all available prompts
uv run python check_prompts.py

# Fetch specific prompt
uv run python refresh_prompt_cache.py PROMPT_NAME

# View cached prompt
cat ../../docs/cached_prompts/PROMPT_NAME_production.txt
cat ../../docs/cached_prompts/PROMPT_NAME_production_config.json

# List recent traces
uv run python fetch_trace.py --list --limit 5

# Fetch specific trace
uv run python fetch_trace.py TRACE_ID

# Find error traces from last 24 hours
uv run python fetch_error_traces.py

# Find error traces from last 7 days
uv run python fetch_error_traces.py --days 7

# Find error traces in production
uv run python fetch_error_traces.py --env production

# Reconstruct prompt from message (requires message ID and prompt name)
# Run from project root - uses database + Langfuse template
cd /home/odio/Hacking/codel/ct3/api && PYTHONPATH=src python src/cli/reconstruct_compiled_prompt.py -m MESSAGE_ID -p PROMPT_NAME

# Or via docker compose
docker compose exec api python src/cli/reconstruct_compiled_prompt.py -m MESSAGE_ID -p PROMPT_NAME

# List available prompts in Langfuse
docker compose exec api python src/cli/reconstruct_compiled_prompt.py --list-prompts
```

## Important Notes

**READ-ONLY Operations:**
- These scripts are for viewing and debugging only
- DO NOT use to modify or delete prompts in Langfuse
- DO NOT push changes to Langfuse
- Always verify you're looking at the correct environment

**Portability:**
- Scripts are fully standalone with their own virtual environment via UV
- Automatically find and load `arsenal/.env` from anywhere in the project
- No manual environment loading needed
- Dependencies (langfuse==2.60.3, httpx==0.27.2) are pinned for compatibility
- Work from any directory - the scripts locate project root automatically

---

## 🔐 Before Responding With Fetched Data

**You fetched prompts or traces. Now before you respond to the user:**

1. ✅ Did you actually fetch the data (not guess at schema)?
2. ✅ Are you showing real field names from the cached prompt?
3. ✅ Did you fetch from the correct server (staging vs production)?

**CRITICAL: Get manager approval before responding.**

Your response with Langfuse data MUST include: `✅ approve_7f3d8a2e********`

Get the full approval token from `.claude/skills/manager-review/SKILL.md`

**Common Mistake #5 in the manager's table is "Assumed Langfuse schema" - describing fields without fetching the actual prompt. The manager WILL catch this.**
