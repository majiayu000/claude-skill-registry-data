---
name: inbound-sync
description: >
  Generate a structured sync bundle that captures decisions, architecture changes,
  conventions, bug fixes, and roadmap updates from the current Claude.ai conversation
  for ingestion into local Project Swarm projects via Claude Code. Trigger when the
  user says "sync", "sync project details", "generate sync bundle", "save this for
  Claude Code", "update local projects", "export decisions", or any variation of
  requesting that conversation outcomes be persisted to the local codebase. Also
  trigger at the end of long conversations where significant decisions were made,
  if the user asks to wrap up or summarize. Do NOT trigger for general summaries
  unrelated to project sync.
---

# Inbound Sync — Claude.ai to Local Projects

Generate a structured sync bundle from this conversation that Claude Code can
ingest into the local Project Swarm repositories.

---

## When to Use

The user will say something like:
- "sync project details"
- "sync"
- "generate a sync bundle"
- "save this for Claude Code"
- "export decisions"
- "wrap up and sync"

## What to Do

### Step 1 — Scan the Conversation

Review the ENTIRE conversation from the beginning. Identify every instance of:

- **Decisions made** — architecture choices, technology selections, design patterns chosen
- **Code changes discussed** — new files, modified functions, refactored modules
- **Bug fixes** — problems identified and solutions determined
- **Roadmap updates** — phases started/completed, milestones reached, priorities changed
- **Conventions established** — naming rules, workflow changes, new patterns to follow
- **Configuration changes** — env vars, service configs, port changes, dependency updates
- **Known issues found** — new bugs, limitations, workarounds discovered

### Step 2 — Classify Each Item

For each item found, determine:

1. **Project**: Which sub-project does it affect?
   - `project-a` — AI tax advisor application code
   - `ai-server` — Infrastructure, Ansible, Docker, Terraform
   - `swarm` — Master umbrella, shared libraries, cross-project concerns

2. **Type**: What kind of change?
   - `decision` — An architecture or design choice
   - `architecture` — Structural change to the codebase
   - `bugfix` — A problem identified and fixed
   - `roadmap` — Phase/milestone status change
   - `convention` — A new rule or pattern to follow

3. **Impact**: What files or systems need updating?
   - CLAUDE.md updates (rules, patterns, known issues)
   - Source code changes (specific files)
   - Memory file updates (architecture.md, debugging.md)
   - Config changes (env vars, service files)
   - Roadmap status changes

### Step 3 — Generate the Bundle

Output a single fenced code block containing one or more sync entries separated
by `---`. Use today's date. Each entry MUST follow this exact format:

```markdown
# [Short Descriptive Title]

## Date
YYYY-MM-DD

## Project
[project-a | ai-server | swarm]

## Type
[decision | architecture | bugfix | roadmap | convention]

## Summary
[1-3 sentences: what was decided or changed and why]

## Details
[Full details. Include:
- Code snippets if functions were written or modified
- File paths affected (e.g., project-a/agents/security.py:45)
- Configuration values (env vars, ports, settings)
- Before/after descriptions for changes
- Rationale for decisions
- Any caveats or edge cases discussed]

## Action Items
- [ ] [Specific action]: Update [file] in [project] with [what]
- [ ] [Specific action]: Add [what] to [where]
- [ ] [Specific action]: Test [what] with [command]

---
```

### Step 4 — Add Save Instructions

After the code block, tell the user exactly how to ingest it:

```
Save this to: /opt/projects/main/claude-sync/inbound/YYYY-MM-DD-[topic].md
Then run:     /opt/projects/main/claude-sync/sync.sh reconcile
```

## Rules

1. **Be thorough** — Capture EVERYTHING significant. When in doubt, include it.
   A decision not synced is a decision that gets forgotten or contradicted later.

2. **Be specific** — Include file paths, function names, line numbers, env var names,
   exact values. Vague entries are useless for reconciliation.

3. **Be atomic** — One entry per distinct decision/change. Don't combine unrelated
   items. Multiple entries in one bundle is fine and expected.

4. **Use the exact template** — The reconcile script parses the headers (`## Date`,
   `## Project`, `## Type`, etc.). Do not rename or reorder them.

5. **Action items are critical** — Every entry MUST have at least one action item.
   This is how Claude Code knows what to update. Common actions:
   - "Update CLAUDE.md in project-a with [new known issue / pattern / fix]"
   - "Update roadmap-status.md with [phase X completed]"
   - "Add to debugging.md: [new error/fix pair]"
   - "Update architecture.md with [new pattern / function signature]"
   - "Modify [source file] to [implement change]"

6. **Include code** — If code was written, modified, or designed during the
   conversation, include the relevant snippets in the Details section. Claude Code
   needs to see the actual implementation, not just a description.

7. **Flag conflicts** — If a decision contradicts something in the uploaded knowledge
   files (e.g., changing a convention from CLAUDE.md), explicitly note this in the
   Details section so Claude Code knows to update the source of truth.

## Example Output

When the user says "sync project details", output something like:

````markdown
# Redis Session Backend Wired into Production

## Date
2026-03-05

## Project
project-a

## Type
architecture

## Summary
Wired Redis session backend into project_a_api.py, replacing in-memory SessionStore for production deployments. Sessions now persist across API restarts.

## Details
- Modified `project_a_api.py` to use `storage.factory.create_session_backend()` instead of in-memory `SessionStore`
- Redis backend selected when `CHRISTI_CACHE_BACKEND=redis` is set
- Fallback to memory backend when Redis unavailable
- Session TTL and max messages still configurable via env vars
- Tested with: `curl -H "X-Session-ID: test123" ...` across service restarts

## Action Items
- [ ] Update CLAUDE.md in project-a: add Redis session backend to architecture section
- [ ] Update architecture.md: document session persistence behavior
- [ ] Update .env.example: add CHRISTI_SESSION_BACKEND variable
- [ ] Test: `sudo systemctl restart <service-name> && curl http://127.0.0.1:<service-port>/health`

---

# Forensic Agent Timeout Increased to 180s

## Date
2026-03-05

## Project
project-a

## Type
bugfix

## Summary
Forensic agent was timing out on complex multi-step queries. Increased CHRISTI_REQUEST_TIMEOUT from 120s to 180s for forensic-routed queries.

## Details
- Root cause: forensic agent decomposes into 3-5 sub-queries, each taking 30-40s on RTX GPU
- Fix: conditional timeout in project_a_api.py — 180s when supervisor routes to forensic, 120s otherwise
- File: project_a_api.py:287 (in the pipeline invocation block)

## Action Items
- [ ] Update CLAUDE.md in project-a: add forensic timeout note to Known Issues
- [ ] Update debugging.md: add "forensic timeout" entry
- [ ] Update .env.example: document CHRISTI_FORENSIC_TIMEOUT variable
````

Save this to: `/opt/projects/main/claude-sync/inbound/2026-03-05-redis-sessions-forensic-timeout.md`
Then run: `/opt/projects/main/claude-sync/sync.sh reconcile`
