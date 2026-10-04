---
name: mem0
preamble-tier: 3
version: 1.0.0
description: |
  Persistent cross-session memory for AI agents. Mem0 stores user preferences,
  past decisions, domain knowledge, and agent learnings across all sessions,
  all tools, and all users. Complements planning-with-files (task-level memory)
  with long-term agent intelligence (CRM + personal knowledge base layer).
  Use when asked to "remember this", "store preference", "mem0", "long-term memory",
  "user memory", "agent memory", or when building multi-session agents that need
  to recall past interactions.
benefits-from: [planning-with-files]
triggers:
  - mem0
  - long-term memory
  - user memory
  - agent memory
  - remember this
  - store preference
  - persistent memory
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - AskUserQuestion
---

# Mem0 — Persistent Agent Memory

## What Mem0 Does

Mem0 is your agent's **long-term memory layer**. Where `planning-with-files` remembers
what you're building *right now* (task plan, findings, progress), Mem0 remembers
*who you are* across all tasks — your preferences, past decisions, domain knowledge,
and what each user has told your agents.

| Dimension | planning-with-files | Mem0 |
|---|---|---|
| **Scope** | This task, this session, this repo | Across all sessions, all agents, all users |
| **Storage** | Markdown files on disk | Vector DB + Graph DB + Key-Value DB |
| **What it remembers** | Current build, sub-tasks, progress | User identity, preferences, past decisions, domain knowledge |
| **Readable by humans?** | Yes — plain markdown | No — embeddings and graph nodes |
| **Git-trackable?** | Yes | No (lives in DB infrastructure) |
| **Analogous to** | Your current task notepad | Your long-term CRM + personal knowledge base |
| **Lifespan** | Lives until project is closed | Persists indefinitely across all agents |

## Installation

### Option A — Hosted Platform (Recommended Starting Point)

No infrastructure. Mem0 manages all three storage layers in the cloud.

1. Go to [app.mem0.ai](https://app.mem0.ai), sign up, get your API key
2. Store the key in your environment: `MEM0_API_KEY=your-key`
3. In Python projects:

```python
from mem0 import MemoryClient
client = MemoryClient(api_key=os.environ["MEM0_API_KEY"])
```

**This is the right starting point for Elephant Gin / CarbonIQ projects.**

### Option B — Self-Hosted (For Full Data Control)

```bash
pip install mem0ai
```

Configure in `config.py`:

```python
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333}
    },
    "llm": {
        "provider": "anthropic",
        "config": {"model": "claude-sonnet-4-20250514", "api_key": "..."}
    }
}
```

Self-hosted means you run Qdrant locally (`docker run -p 6333:6333 qdrant/qdrant`)
and Mem0 routes memories into it. Adding Neo4j graph memory is optional for
relationship-heavy use cases.

## Core Operations

### Store a Memory

```python
# Store something the user said or a preference discovered
client.add(
    messages=[{"role": "user", "content": "I prefer OSINT outputs with commodity desk specificity and confidence ratings"}],
    user_id="koo",
    metadata={"project": "carboniq", "context": "research_preferences"}
)
```

### Retrieve Memories

```python
# Search for relevant memories before responding
memories = client.search(
    query="user preferences for research outputs",
    user_id="koo"
)
# Returns ranked, relevant past memories with timestamps
```

### Get All Memories for a User

```python
all_memories = client.get_all(user_id="koo")
```

### Delete a Memory

```python
client.delete(memory_id="specific-memory-id")
```

## Integration Patterns

### Pattern 1: Agent Session Warm-Up

At the start of every agent session, after loading `planning-with-files` context:

```python
# Pull user context from Mem0
user_context = client.search(
    query="current project preferences domain knowledge",
    user_id="koo",
    limit=5
)
# Inject into system prompt or agent context
```

### Pattern 2: Preference Learning Loop

When an agent discovers a user preference (tone, format, depth):

```python
client.add(
    messages=[{"role": "assistant", "content": "User prefers concise bullet points over paragraphs"}],
    user_id="koo",
    metadata={"type": "preference", "domain": "output_format"}
)
```

### Pattern 3: Cross-Session Project Memory

When working across multiple projects (CarbonIQ, LNG dashboard, client intelligence):

```python
# Store project-specific learnings
client.add(
    messages=[{"role": "user", "content": "Petronas contact prefers morning calls, cares about EU taxonomy alignment"}],
    user_id="koo",
    metadata={"project": "client_intelligence", "entity": "Petronas", "type": "contact_note"}
)
```

### Pattern 4: Multi-Agent Shared Memory

When multiple agents (Codex, Claude, Gemini, Kimi) work with the same user:

```python
# All agents read from the same user_id
# Memories stored by Claude are available to Gemini in the next session
client.search(query="what did we decide about", user_id="koo")
```

## Complementary Workflow: planning-with-files + Mem0

These two tools operate at **completely different layers** of the memory stack.
They do not conflict — they complement each other.

### Division of Labor

**planning-with-files handles the work session:**
- "Build the supply agent for the LNG dashboard" → writes `task_plan.md` with phases
- Writes `findings.md` with LNG market structure notes
- Tracks `progress.md` through the build
- If context clears mid-build, recovers automatically from `.planning/` folder
- Entirely local and project-specific

**Mem0 handles cross-session agent intelligence:**
- CarbonIQ agent talks to users → stores what each user told it (project types, jurisdictions, preferred methodologies)
- Client intelligence agent researches Petronas → stores that user prefers OSINT outputs with commodity desk specificity
- Next time any agent in any session works with user, pulls those preferences via `mem0.search()`

### Session Start Protocol (Both Skills)

At the start of EVERY session:

1. **Run planning-with-files protocol** (H.1 auto-fire):
   - Check for `task_plan.md` → read it, `findings.md`, `progress.md`
   - Create if missing for multi-step tasks

2. **Run Mem0 warm-up** (H.1 auto-fire):
   - Query Mem0 for user context: `client.search(query="current preferences and context", user_id="koo")`
   - Inject retrieved memories into agent context window
   - Signal: "Loaded N memories from Mem0 for user koo"

3. **Proceed with task** — agent now has both:
   - Task plan from files (what we're building now)
   - User context from Mem0 (who we're building for, what they prefer)

### Session End Protocol (Both Skills)

At the end of EVERY session:

1. **Update planning-with-files**:
   - Mark phases complete in `task_plan.md`
   - Log session in `progress.md`
   - Save findings to `findings.md`

2. **Store key learnings to Mem0**:
   - Any new user preferences discovered
   - Any decisions made that affect future work
   - Any domain knowledge worth remembering

3. **Signal completion**: "Session closed. Plans.md updated. Mem0 synced."

## Claude Code Plugin

Mem0 has both `.claude-plugin` and `.cursor-plugin` directories in its repo,
meaning it can be installed as a Claude Code plugin alongside `planning-with-files`.
They do not conflict.

**Plugin repo:** [github.com/mem0ai/mem0](https://github.com/mem0ai/mem0)

## Cost-Priority Note

Mem0 hosted platform has a generous free tier. For Elephant Gin / CarbonIQ
projects, start with the hosted platform (Option A). Only move to self-hosted
(Option B) if data control requirements demand it.

## Error Handling

- If `MEM0_API_KEY` is missing: surface clear error, prompt for key, do not silently fail
- If Mem0 API is unreachable: log error, continue with planning-with-files only

## Security Guardrails (MANDATORY)

**These rules are non-negotiable. Violating them is a CRITICAL security incident.**
Full protocol below. MASTER_RULES_v1.md H.8 points here.

### DENYLIST — NEVER Store These in Mem0

| Category | Examples | Reason |
|----------|---------|--------|
| API Keys | `MEM0_API_KEY`, `KIMI_API_KEY`, `GEMINI_API_KEY`, OpenAI/Anthropic keys | Full account compromise |
| Passwords & Credentials | Login passwords, DB passwords, token secrets | Irreversible account takeover |
| Government IDs | Passport numbers, NRIC, driver's license | Identity theft |
| Financial Instruments | Credit cards, bank accounts, crypto seeds | Financial fraud |
| Personal File Paths | Any path containing `C:\Users\` or `/home/` | Privacy & recon |
| Raw Conversation Logs | Unedited full agent transcripts | May contain pasted credentials |
| Commercially Sensitive Data | Unpublished financials, contracts, proprietary algorithms | Business confidentiality |

### Pre-Store Sanitization Checklist

Before EVERY `client.add()` call:

- [ ] Scan for API key patterns (`sk-`, `m0-`, `AIza`, `kimi-`, `-----BEGIN`)
- [ ] Scan for email addresses (user's personal email)
- [ ] Scan for file paths containing usernames
- [ ] Scan for numeric patterns matching passport/ID formats
- [ ] Replace matches with `[REDACTED]`
- [ ] Log: "Sanitization: N items redacted. Proceeding."

### Post-Store Audit

After any seeding session:

```python
all_memories = client.get_all(user_id="koo")
# Audit every memory for DENYLIST patterns
# Flag matches as CRITICAL — delete immediately via client.delete()
```

### Credential Rotation Protocol

If any credential is suspected of exposure in Mem0:
1. **IMMEDIATELY** rotate the credential at its source
2. Delete the offending memory: `client.delete(memory_id="...")`
3. Update `.env` with the new credential
4. Log incident in `~/master-rules/security-incidents.md`

### Warm-Up Security Pre-Check

At session start, when retrieving memories:
1. Verify `MEM0_API_KEY` is set and valid
2. Query: `client.search(query="current preferences and context", user_id="koo")`
3. Scan retrieved memories for DENYLIST patterns before injecting into context
4. Inject sanitized memories into agent context
5. Signal: `"Loaded N memories from Mem0 for user koo [security: CLEAN]"`
6. If DENYLIST pattern detected: flag as CRITICAL, do NOT inject, alert user
- If no memories found for user: proceed normally, store new ones as discovered
