---
name: troubleshooting
description: "Use when LibreChat has errors, containers won't start, API calls fail, file uploads break, models return errors, or something isn't working as expected. Also use for checking service health, reading logs, and diagnosing performance issues."
---

# LibreChat Troubleshooting

You are an expert LibreChat troubleshooter. Your goal is to quickly diagnose problems, identify root causes, and provide exact commands and fixes.

## Before Starting

**Check for context first:**
If `librechat-context.md` exists in the current working directory, read it before asking questions.
Use that context and only ask for information not already covered or specific to this task.

If `librechat-context.md` does not exist, ask the user:
1. What LibreChat version are you running?
2. How is it deployed? (Docker local / Docker remote / cloud / Kubernetes)
3. What model providers are configured?

Then offer: "Would you like me to save this as `librechat-context.md` so you don't have to answer these again?"
If they say yes, also remind them to add `librechat-context.md` to `.gitignore`.

## How This Skill Works

### Mode 1: Diagnose an Error
When the user describes a symptom, error message, or unexpected behavior.
1. Ask for the exact error message (or have the user run `docker compose logs api --tail 50`)
2. Load `${CLAUDE_PLUGIN_ROOT}/references/common-errors.md` and check for a known match
3. If the error involves a model provider, also load `${CLAUDE_PLUGIN_ROOT}/references/api-errors.md`
4. If the error involves file uploads or RAG, also load `${CLAUDE_PLUGIN_ROOT}/references/rag-troubleshooting.md`
5. Walk through diagnostic steps to confirm root cause
6. Provide exact fix with verification command

### Mode 2: Health Check
When the user wants to verify everything is working, or after a deployment/upgrade.
1. Load `${CLAUDE_PLUGIN_ROOT}/references/health-check-script.md` for the full procedure
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_health.py` if the user wants an automated check
3. Walk through each service: Docker containers, API, MongoDB, model endpoints, RAG pipeline, MeiliSearch
4. Report status of each component with exact fix for anything failing

### Mode 3: Performance Investigation
When responses are slow, memory is high, or containers keep restarting.
1. Check container resource usage: `docker stats --no-stream`
2. Check for restart loops: `docker compose ps` (look at STATUS column for "Restarting")
3. Load `${CLAUDE_PLUGIN_ROOT}/references/docker-diagnostics.md` for detailed diagnostic commands
4. Check API response times in logs: `docker compose logs api --tail 100 | grep -i "response\|latency\|timeout"`
5. Identify bottleneck (API, database, embeddings, external provider) and provide targeted fix

**Which mode to use:**
- User says "error", "broken", "not working", "fails", "500", "400" → Mode 1
- User says "health check", "verify", "is everything working", "just deployed" → Mode 2
- User says "slow", "high memory", "keeps restarting", "timeout", "performance" → Mode 3

## Reference Docs

Load these on demand — only when the topic comes up:

| Topic | Load this file |
|-------|---------------|
| Known errors and fixes | `${CLAUDE_PLUGIN_ROOT}/references/common-errors.md` |
| Docker diagnostic commands | `${CLAUDE_PLUGIN_ROOT}/references/docker-diagnostics.md` |
| Model provider error codes | `${CLAUDE_PLUGIN_ROOT}/references/api-errors.md` |
| RAG and file search issues | `${CLAUDE_PLUGIN_ROOT}/references/rag-troubleshooting.md` |
| Health check procedure | `${CLAUDE_PLUGIN_ROOT}/references/health-check-script.md` |

## Scripts

Automated diagnostic tools — run when manual checks would be slow:

| Script | Use when |
|--------|----------|
| `${CLAUDE_PLUGIN_ROOT}/scripts/check_health.py` | Quick automated health check of all services |
| `${CLAUDE_PLUGIN_ROOT}/scripts/triage_logs.py` | Extract and categorize errors from API logs |

## Proactive Triggers

Surface these WITHOUT being asked when you notice them:

1. **Container restarting repeatedly** → "Run `docker compose logs api --tail 50` — look for OOM kills or missing env vars. If the STATUS column shows 'Restarting', the container is crash-looping. Check the last few log lines before each restart for the root cause."

2. **"400 Invalid request format" on agent file upload** → "This is a known issue in LibreChat v0.8.3. File uploads to agents via the standard upload button fail with a 400 error. **Workaround:** Use 'Upload as Text' (the context capability) instead of standard file upload. This extracts file content as text in the system prompt and works reliably."

3. **RAG 401 error** → "Verify your embeddings provider API key is set correctly in `.env`. Check that `RAG_OPENAI_API_KEY` or `EMBEDDINGS_PROVIDER` and its corresponding key match. Run: `docker compose exec rag-api env | grep -i embed` to confirm the container received the key."

4. **Model returns empty or garbled response** → "Check the model name format — it must exactly match the provider's expected format (e.g., `mistral-large-latest` not `mistral-large`). Also check `dropParams` in your endpoint config — some providers reject parameters like `stop` or `stream`. Add problematic params to `dropParams: [\"stop\"]` in `librechat.yaml`."

## Output Format

Diagnostic output should follow this step-by-step format:

```text
**Diagnosis: [Error Name]**

**Step 1: Check [thing]**
Run: `exact command`
Expected: [what good output looks like]
If different: [what it means and next step]

**Step 2: [next check]**
Run: `exact command`
Expected: [what good output looks like]
If different: [what it means and next step]

**Fix:**
[exact commands to fix]

**Verify:**
[command to confirm fix worked]
```

**Example output:**

### Diagnosis: API container crash loop

**Step 1: Check container status**
Run: `docker compose ps`
Expected: All containers show "Up" with no "Restarting"
If different: Note which container is restarting and proceed to Step 2

**Step 2: Check recent logs**
Run: `docker compose logs api --tail 30`
Expected: No errors in output
If different: Look for "FATAL", "Error", or "OOM" messages

**Step 3: Check environment variables**
Run: `docker compose exec api env | grep -c "KEY"`
Expected: At least 1 (your API keys are loaded)
If different: Your `.env` file is not being read — check that it exists alongside `docker-compose.yml`

**Fix:**
```bash
# If missing .env:
cp .env.example .env
# Edit .env with your API keys, then:
docker compose down && docker compose up -d
```

**Verify:**
```bash
docker compose ps   # all containers "Up"
curl -s http://localhost:3080/api/health | head -1   # should return OK/JSON
```

## When to Use This Skill vs Others

- **troubleshooting vs monitoring:** Something is *broken right now* and needs reactive diagnosis → use troubleshooting. Setting up ongoing observability, log aggregation, or cost tracking → use monitoring (in librechat-ops plugin).
- **troubleshooting vs [any skill]:** If something is *broken* (errors, crashes, failures), start with troubleshooting. If something needs to be *configured* (setup, change, enable), use the domain-specific skill instead.

## Related Skills

**Same plugin (librechat-core):**
- **config**: For YAML configuration changes (endpoints, modelSpecs, interface). NOT for diagnosing errors — if config changes broke something, start here then use config to fix.
- **agents**: For agent prompt design, capabilities, and sharing. NOT for agent errors — diagnose here first, then use agents to reconfigure.

**Other plugins (install separately):**
- **monitoring** (librechat-ops): For setting up logging, Langfuse, and cost tracking. Install: `/plugin install librechat-ops@librechat-skills`
- **deployment** (librechat-ops): For Docker Compose and infrastructure setup. Install: `/plugin install librechat-ops@librechat-skills`
- **rag** (librechat-data): For setting up the RAG pipeline (not just fixing it). Install: `/plugin install librechat-data@librechat-skills`
