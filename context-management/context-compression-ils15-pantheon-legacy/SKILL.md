---
name: context-compression
description: "Level 2 — Pantheon-native context compression with priority scoring, semantic summarization, downstream-aware compression, budget allocation, and cross-references"
context: fork
globs: ["**/01-active-context.md", "**/02-progress-log.md"]
alwaysApply: false
---

# Context Compression — Level 2 (Intelligent Compression)

Level 2 replaces Level 1 with priority-aware compression: scoring, semantic summarization for critical/high entries, downstream-aware field masks, budget allocation, and automatic cross-references. Zeus triggers, Mnemosyne executes.

---

## 1. Overview

Level 2 adds four capabilities beyond Level 1:

1. **Priority Scoring Engine** — Deterministic keyword-driven scoring (no LLM) for each subtask_summary across 5 dimensions. Outputs CRITICAL/HIGH/MEDIUM/LOW.
2. **Semantic Summarization** — Template-generated contextual summaries for CRITICAL/HIGH entries, tailored to the downstream agent pair. MEDIUM/LOW get standard mechanical 1-line compression.
3. **Downstream-Aware Compression** — Field masks preserve the most relevant fields per (from_agent, to_agent) pair. Themis gets all fields; Mnemosyne gets minimal.
4. **Cross-Reference Mechanism** — Auto-generated `_xref/index.md` with entity references for endpoints, tables, migrations, components, and decisions, surviving sprint boundaries.

Budget allocation is priority-greedy. CRITICAL entries are always expanded. Overflow escalates to Zeus.

---

## 2. Compression Triggers

Same 7 triggers as Level 1, with Level 2 behavior:

| Trigger | Fires | Level 2 Behavior |
|---------|-------|------------------|
| **C1 Phase Gate** | Themis APPROVED | Priority-score subtask_summary → semantic summary (CRITICAL/HIGH) or 1-line (MEDIUM/LOW) → `01-active-context.md` |
| **C2 Phase Gate** | Themis APPROVED | IMPL artifact → scored, archived to `02-progress-log.md`; `.tmp/` deleted |
| **C3 Phase Gate** | Themis APPROVED | REVIEW summary line → `02-progress-log.md`; `.tmp/` deleted |
| **C4 Feature Complete** | Last phase APPROVED | PLAN reference → `01-active-context.md`; `.tmp/` deleted |
| **C5 Sprint Close** | `@mnemosyne Close sprint` | Bulk cleanup + cross-ref archive + flag unresolved |
| **C6 Explicit** | `/compress` | Per-type compression with priority scoring |
| **C7 Size-based** | `01-active-context.md` Completed Phases > 100 lines | Priority-greedy trim: oldest LOW entries first, preserving CRITICAL and HIGH |

### Inline Compression Triggers (C8-C11 — Active Session)

These triggers fire DURING an active agent session. They call the Pantheon-native inline compressor (`compress-inline.py` MCP, "L1"). Scrubbing is automatic in the MCP layer — agents must NOT scrub manually.

| Trigger | Fires | Layer | Action |
|---------|-------|-------|--------|
| **C8 CRITICAL/HIGH subtask_summary** | A returned `subtask_summary` contains CRITICAL/HIGH findings | L1 Inline | `execute_code_script("compress-inline.py", args=["compress", "--text", "<content>"])` before the next phase |
| **C9 Pre-Delegation** | About to delegate a large context block to another agent | L1 Inline | Compress the block first to cut tokens |
| **C10 Context Pressure** | Context near limit / platform compaction signal | — (cross-ref) | OpenCode native compaction already handles this. No separate Pantheon mechanism — see §12. |
| **C11 Phase Boundary / Handoff** | Phase boundary or session handoff reached | L1 Inline | Compress completed work before promotion |

---

## 3. Priority Scoring Engine

The algorithm is DETERMINISTIC (keyword-driven, no LLM needed). Zeus scores each subtask_summary before compression using 5 dimensions. Total score is weighted sum.

### Scoring Dimensions

| Dimension | Weight | Range | Description |
|-----------|--------|-------|-------------|
| Impact | 0.30 | 0.0–1.0 | How broadly the change affects the system |
| Risk | 0.25 | 0.0–1.0 | Likelihood of breakage or subtle bugs |
| Novelty | 0.20 | 0.0–1.0 | New pattern, architecture, or files |
| Blockers | 0.15 | 0.0–1.0 | Whether this unblocked others or was blocked |
| Downstream relevance | 0.10 | 0.0–1.0 | How relevant to the next agent (from agent-pair table) |

### Full Keyword Scoring Map

| Keyword / Pattern | Impact | Risk | Novelty | Category |
|-------------------|--------|------|---------|----------|
| `schema` | 1.0 | 1.0 | 0.6 | schema/migration |
| `migration` | 1.0 | 1.0 | 0.4 | schema/migration |
| `auth` | 1.0 | 1.0 | 0.5 | auth/security |
| `login` | 1.0 | 1.0 | 0.4 | auth/security |
| `permission` | 0.8 | 1.0 | 0.5 | auth/security |
| `role` | 0.8 | 0.8 | 0.4 | auth/security |
| `JWT` | 0.8 | 1.0 | 0.4 | auth/security |
| `OAuth` | 0.8 | 1.0 | 0.5 | auth/security |
| `password` | 0.7 | 1.0 | 0.3 | auth/security |
| `encrypt` | 0.7 | 1.0 | 0.5 | auth/security |
| `token` | 0.7 | 0.8 | 0.3 | auth/security |
| `security` | 0.8 | 1.0 | 0.4 | auth/security |
| `new table` | 1.0 | 0.8 | 0.9 | schema/migration |
| `new column` | 0.7 | 0.8 | 0.6 | schema/migration |
| `index` | 0.5 | 0.6 | 0.3 | database |
| `foreign key` | 0.8 | 0.9 | 0.5 | database |
| `constraint` | 0.6 | 0.7 | 0.3 | database |
| `endpoint` | 0.9 | 0.6 | 0.5 | api |
| `route` | 0.8 | 0.5 | 0.4 | api |
| `API` | 0.8 | 0.5 | 0.4 | api |
| `service` | 0.7 | 0.4 | 0.4 | architecture |
| `new file` | 0.6 | 0.3 | 0.8 | structure |
| `refactor` | 0.5 | 0.7 | 0.6 | code-quality |
| `rename` | 0.4 | 0.6 | 0.3 | code-quality |
| `delete` | 0.5 | 0.7 | 0.2 | code-quality |
| `deprecat` | 0.4 | 0.4 | 0.3 | code-quality |
| `config` | 0.5 | 0.6 | 0.3 | infrastructure |
| `Docker` | 0.7 | 0.6 | 0.3 | infrastructure |
| `deploy` | 0.8 | 0.8 | 0.2 | infrastructure |
| `CSS` | 0.2 | 0.1 | 0.2 | style |
| `style` | 0.2 | 0.1 | 0.2 | style |
| `typo` | 0.0 | 0.0 | 0.0 | trivial |
| `comment` | 0.1 | 0.0 | 0.0 | trivial |
| `README` | 0.2 | 0.0 | 0.1 | documentation |
| `docstring` | 0.2 | 0.0 | 0.1 | documentation |
| `5+ files` | — | — | 0.8 | novelty (file count) |
| `10+ files` | — | — | 1.0 | novelty (file count) |

**Scoring rules:**
- For each dimension, find the **maximum** matching keyword score among all keywords found in the summary.
- If multiple keywords match in the same category, take the max per dimension.
- Novelty bonus: `files_changed` overrides keyword score — if >5 files, set novelty to 0.8; if >10 files, set to 1.0.
- If no keywords match, default to 0.0 for that dimension.

### Downstream Relevance Table

The relevance score is computed from the agent-pair lookup:

| From ↓ → To → | Hermes | Aphrodite | Demeter | Themis | Mnemosyne | Hephaestus | Prometheus |
|---------------|--------|-----------|---------|-------|-----------|------------|------------|
| **Hermes** | 1.0 | 0.9 | 0.8 | 0.7 | 0.3 | 0.6 | 0.5 |
| **Aphrodite** | 0.9 | 1.0 | 0.3 | 0.7 | 0.3 | 0.5 | 0.3 |
| **Demeter** | 0.9 | 0.3 | 1.0 | 0.7 | 0.3 | 0.6 | 0.6 |
| **Themis** | 0.8 | 0.8 | 0.8 | 1.0 | 0.5 | 0.8 | 0.8 |
| **Hephaestus** | 0.6 | 0.5 | 0.6 | 0.7 | 0.3 | 1.0 | 0.4 |
| **Prometheus** | 0.6 | 0.4 | 0.6 | 0.7 | 0.3 | 0.4 | 1.0 |
| **Mnemosyne** | 0.3 | 0.3 | 0.3 | 0.5 | 1.0 | 0.3 | 0.3 |

**Rows = from agent, Columns = to agent.** Score = `table[from_agent][to_agent]` scaled to 0.0–1.0 (already in range).

When the next-phase agent is unknown, default downstream relevance to 0.5.

### Priority Bands

| Band | Score Range | Storage Mode |
|------|-------------|--------------|
| CRITICAL | ≥ 0.75 | Expanded (3 lines, semantic summary) |
| HIGH | 0.50 – 0.74 | Expanded (2 lines) or Standard (1 line) per budget |
| MEDIUM | 0.25 – 0.49 | Standard (1 line) |
| LOW | < 0.25 | Aggressive (0.5 lines, filename only) |

### Scoring Example

```
subtask_summary:
  summary: "Added JWT auth endpoint with refresh token rotation"
  files_changed: ["backend/routers/auth.py", "backend/services/auth_service.py"]
  status: complete

Keywords found: JWT (auth/security), endpoint (api), token (auth/security)
  → Impact = max(0.8, 0.9, 0.7) = 0.9
  → Risk = max(1.0, 0.6, 0.8) = 1.0
  → Novelty = max(0.4, 0.5, 0.3) = 0.5 | files=2, no bonus
  → Blockers = 0.0 (no blockers mentioned)
  → Downstream = 0.9 (Hermes→Aphrodite)

Score = 0.9×0.30 + 1.0×0.25 + 0.5×0.20 + 0.0×0.15 + 0.9×0.10
     = 0.27 + 0.25 + 0.10 + 0.00 + 0.09
     = 0.71 → HIGH
```

---

## 4. Semantic Summarization

Zeus generates contextual summaries for CRITICAL and HIGH entries using the semantic-summarize prompt template. 
Each summary costs ~50 input tokens per entry (uses the same model as Zeus). MEDIUM/LOW entries get mechanical 1-line compression without summarization.

### Template: CRITICAL (3 lines)

```
1 sentence: What changed (include API/contract details if relevant to next agent)
1 sentence: Why it matters to the NEXT agent (from downstream table)
1 sentence: Gotcha/decision/trade-off
```

### Template: HIGH (2 lines)

```
1 sentence: What changed (include API/contract details if relevant to next agent)
1 sentence: Why it matters to the NEXT agent (from downstream table)
```

### Template: MEDIUM (1 line)

```
[agent] — <summary first sentence, ≤80 chars> — <files>
```

### Template: LOW (filename only)

```
[agent] — <files>
```

### Variants Per Agent Pair

| Agent Pair | What to Include |
|------------|-----------------|
| Hermes → Aphrodite | Endpoint path, request/response shape, status codes |
| Hermes → Demeter | Model/table names, relationships, foreign keys |
| Demeter → Hermes | Table/column names, migration version, data types |
| Demeter → Aphrodite | New fields added, field types, defaults |
| Aphrodite → Hermes | Component name, data requirements, event handlers |
| Aphrodite → Demeter | UI state shape, fields displayed |
| Themis → * | Verdict, critical issues count, coverage delta |
| * → Themis | Preserve ALL fields (full context for review) |
| * → Mnemosyne | Summary, status only (archive: minimal) |
| Hephaestus → Hermes | Pipeline inputs/outputs, model endpoints |
| Prometheus → Hermes | Deploy target, env vars, config changes |

For MEDIUM and LOW entries, skip variant templates — use standard 1-line or aggressive compression.

---

## 5. Downstream-Aware Compression

Each entry type uses a field mask based on (from_agent, to_agent). The field mask determines which subtask_summary fields survive compression.

### Available Fields

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | YYYY-MM-DD |
| `agent` | string | Agent name |
| `files` | string | Comma-separated file paths |
| `summary` | string | Full summary text |
| `summary_semantic` | string | Generated semantic summary (CRITICAL/HIGH only) |
| `tests` | string | Test status + count |
| `status` | string | complete / partial / escalated |
| `coverage` | string | Coverage percentage |
| `verdict` | string | Themis verdict (APPROVED/NEEDS_REVISION/FAILED) |
| `critical_issues` | int | Count of critical issues found |
| `blockers` | string | Blocker description |

### Field Masks Per Agent Pair

| From → To | Fields Preserved | Notes |
|-----------|-----------------|-------|
| hermes → aphrodite | date, agent, files, summary_semantic, tests, status | Endpoint + schema only |
| hermes → demeter | date, agent, files, summary_semantic, tests, status | Models + relationships only |
| hermes → * (default) | date, agent, files, summary_semantic, tests, status | |
| demeter → hermes | date, agent, files, summary_semantic, tests, status | Tables + migrations only |
| demeter → aphrodite | date, agent, files, summary_semantic, tests, status | New fields only |
| demeter → * (default) | date, agent, files, summary_semantic, tests, status | |
| aphrodite → hermes | date, agent, files, summary_semantic, tests, status | Component + data needs |
| aphrodite → demeter | date, agent, files, summary_semantic, tests, status | UI state + fields |
| aphrodite → * (default) | date, agent, files, summary_semantic, tests, status | |
| themis → * | date, agent, verdict, critical_issues, coverage, files | Review context |
| * → themis | date, agent, files, summary (full), tests, status, coverage | Full context |
| * → mnemosyne | date, agent, summary (first 60 chars), status | Minimal |
| hephaestus → * | date, agent, files, summary_semantic, tests, status | Pipeline + model info |
| prometheus → * | date, agent, files, summary_semantic, tests, status | Deploy + config info |

### Implementation

Zeus applies the mask before generating the compressed entry:

```python
def apply_mask(entry: dict, from_agent: str, to_agent: str) -> dict:
    mask = FIELD_MASKS.get((from_agent, to_agent), FIELD_MASKS[("*", "*")])
    return {k: v for k, v in entry.items() if k in mask}
```

---

## 6. Budget Allocation Algorithm

Compressed entries live in the `## Completed Phases` section of `01-active-context.md`. The total budget is managed to prevent unbounded growth.

### Budget

```
TOTAL_BUDGET = 100 lines for ## Completed Phases section
PER_PHASE_BUDGET = TOTAL_BUDGET / estimated_phases (floor 5 lines)
```

Estimated_phases is the total number of phases planned for the current feature. If unknown, default to 8 phases → PER_PHASE_BUDGET = 12 lines.

### Line Cost Table

| Priority | Expanded | Standard | Aggressive |
|----------|----------|----------|------------|
| CRITICAL | 3 lines | N/A | N/A |
| HIGH | 2 lines | 1 line | N/A |
| MEDIUM | N/A | 1 line | N/A |
| LOW | N/A | N/A | 0.5 lines |

### Priority-Greedy Algorithm

1. Sort all entries by `priority_score` descending.
2. CRITICAL entries always get EXPANDED (3 lines each) — non-negotiable.
3. For remaining budget (TOTAL_BUDGET − sum(CRITICAL×3)):
   - HIGH entries: EXPANDED (2 lines) if budget allows, else STANDARD (1 line).
   - MEDIUM entries: STANDARD (1 line).
   - LOW entries: AGGRESSIVE (0.5 lines, filename only).
4. If at any point CRITICAL entries would exceed TOTAL_BUDGET → **escalate to Zeus** (see Budget Guardrails, §18).

### Example

```
Feature has 8 phases. TOTAL_BUDGET = 100, PER_PHASE_BUDGET = 12.

Phase 1 submits:
- Entry A: score 0.82 → CRITICAL (3 lines)
- Entry B: score 0.45 → MEDIUM (1 line)
Total: 4 lines (of 12 budget). 8 lines carried to next phase.

Phase 2 submits:
- Entry C: score 0.91 → CRITICAL (3 lines)
- Entry D: score 0.67 → HIGH — budget has 20 remaining lines, so EXPANDED (2 lines)
- Entry E: score 0.21 → LOW (0.5 lines)
Total: 5.5 lines. Cumulative 9.5 of 24 budget.
```

---

## 7. Cross-Reference Mechanism

Auto-generated `_xref/index.md` provides persistent entity references that survive sprint boundaries and feature completions.

### Cross-Reference File Location

`.pantheon/memory-bank/_xref/index.md` (created if absent; committed like `_notes/`)

### Reference ID Format

| Prefix | Type | Example | Generated When |
|--------|------|---------|----------------|
| `D{NNNN}` | Decision | D0001 | REVIEW with decision note |
| `E{NNNN}` | Endpoint | E0001 | CRITICAL entry mentions new endpoint |
| `M{NNNN}` | Migration | M0001 | CRITICAL entry mentions new table/column |
| `C{NNNN}` | Component | C0001 | CRITICAL entry mentions new component |

IDs are monotonic integers pulled from `_xref/_next_id.json` and incremented.

### Auto-Generation Rules

| Condition | Action |
|-----------|--------|
| CRITICAL entry mentions a new endpoint (keywords: `POST`, `GET`, `PUT`, `DELETE`, `/api/`, `/v1/`, `/v2/`, `endpoint`, `route`) | Add to **By Entity** table with agent, phase, file reference |
| CRITICAL entry mentions new table/column (keywords: `new table`, `new column`, `migration`, `ALTER TABLE`, `CREATE TABLE`) | Add to **By Entity** table with migration reference |
| Entry that was previously `blocked` now completes | Link from blocking entry → unblocking entry in cross-refs |
| REVIEW with decision note (`## Decision` or ADR reference) | Add to **Decision Links** table |

### Cross-Reference Index File Structure

```markdown
# Cross-Reference Index

## By Feature

| Feature | Phase(s) | Agent(s) | Priority | Summary |
|---------|----------|----------|----------|---------|
| auth-jwt | 1, 2 | Hermes, Aphrodite | HIGH | JWT login + refresh token UI |

## By Entity

| Entity ID | Type | Name | Location | Phase | Agent |
|-----------|------|------|----------|-------|-------|
| E0001 | endpoint | POST /auth/login | backend/routers/auth.py:42 | P1 | Hermes |
| M0001 | migration | add refresh_tokens table | backend/migrations/0012_... | P1 | Demeter |

## Decision Links

| Ref ID | Type | Summary | Links To | Phase |
|--------|------|---------|----------|-------|
| D0001 | ADR | Use refresh token rotation instead of opaque tokens | _notes/ADR-auth-strategy.md | P1 |
```

---

## 8. ZZ Artifact Format

A compressed context artifact `ZZ-phase{N}-context.md` is generated after each phase and injected into the next phase's agent prompt. It lives in `.pantheon/memory-bank/.tmp/`.

### Location

`.pantheon/memory-bank/.tmp/ZZ-phase{N}-context.md`

### Format

```markdown
# Phase N → Phase N+1 Context
**From:** @agent_A (Phase N)
**To:** @agent_B (Phase N+1)

## Budget
- Allocated: 12 lines
- Used: 4 lines
- Carried: 8 lines

## Priority Entries

### CRITICAL (expanded)

**Entry:** Auth JWT endpoint
**Agent:** Hermes | **Score:** 0.82
**What changed:** Added POST /auth/login and POST /auth/refresh endpoints with JWT rotation. Access token lives 15 min, refresh token 7 days.
**To next agent:** Aphrodite needs to implement login form and token storage (httpOnly cookies), auto-refresh on 401.
**Gotcha:** Refresh tokens are stored in DB as hashed — no raw token access after issue. Rotate on every use.

**Entry:** Refresh token table
**Agent:** Demeter | **Score:** 0.91
**What changed:** Created `refresh_tokens` table with FK to `users`, hashed token, expires_at, revoked_at.
**To next agent:** Hermes needs the TokenService to call `create_refresh_token()` + `rotate_refresh_token()`.
**Gotcha:** Migration includes a unique composite index on (user_id, token_hash). Two-phase rollout — read-old/write-new first.

### HIGH (2-line)

**Entry:** Login page component
**Agent:** Aphrodite | **Score:** 0.62
**What changed:** Login form with email + password, validation, error display. Hits POST /auth/login.
**To next agent:** Hermes can test the full flow once Aphrodite's form is wired.

### STANDARD (1-line)

| Date | Agent | Summary | Status |
|------|-------|---------|--------|
| 2026-06-20 | Prometheus | Dockerized auth service with nginx | complete |

## Cross-References

| ID | Type | Name | File |
|----|------|------|------|
| E0001 | endpoint | POST /auth/login | backend/routers/auth.py |
| M0001 | migration | refresh_tokens table | backend/migrations/0012_... |
```

---

## 9. Delegation Flow (Level 2)

```
Zeus receives Themis APPROVED for Phase N
    │
    ├─ [COGNITIVE] Score each subtask_summary (priority scoring engine, no LLM)
    │     5 dimensions: Impact, Risk, Novelty, Blockers, Downstream relevance
    │     → CRITICAL / HIGH / MEDIUM / LOW per entry
    │
    ├─ [COGNITIVE] Determine next phase agents + downstream relevance
    │     Look up (from_agent, to_agent) in agent-pair table
    │
    ├─ [COGNITIVE] Run budget allocation (priority-greedy)
    │     CRITICAL always expanded → HIGH → MEDIUM → LOW
    │     Check overflow: if CRITICAL > budget → escalate
    │
    ├─ [COGNITIVE] Generate semantic summaries (CRITICAL/HIGH only, ~50 tok each)
    │     Template variants per (from_agent, to_agent)
    │
    ├─ [COGNITIVE] Identify cross-references
    │     New endpoints → E{NNNN}, new tables → M{NNNN}, decisions → D{NNNN}
    │
    ├─ DELEGATE @mnemosyne Compress batch (enhanced):
    │     a) Write ZZ-phase{N}-context.md to .tmp/
    │     b) Write compressed entries to 01-active-context.md (priority-aware)
    │        - CRITICAL: expanded (3 lines, semantic summary)
    │        - HIGH: expanded (2 lines) or standard (1 line) per budget
    │        - MEDIUM: standard (1 line)
    │        - LOW: aggressive (0.5 lines)
    │     c) Archive IMPL/REVIEW to 02-progress-log.md
    │     d) Update _xref/index.md
    │        - CRITICAL mentions of endpoints → By Entity
    │        - CRITICAL mentions of tables → By Entity
    │        - Decision notes → Decision Links
    │        - Blocked→unblocked links
    │     e) Increment _xref/_next_id.json
    │
    └─ Zeus injects ZZ-phase{N}-context.md into Phase N+1 agent prompts
         Included in the prompt preamble: "Previous phase context: <ZZ content>"
```

### Standard Flow (C1 + C2 + C3 fire together)

```
Zeus receives Themis APPROVED for Phase N
    │
    ├─ [COGNITIVE] Score + summarize + budget + cross-refs (as above)
    │
    ├─ @mnemosyne Compress (enhanced):
    │     a) Write ZZ-phase{N}-context.md to .tmp/
    │     b) Priority-aware write to 01-active-context.md
    │     c) Archive IMPL/REVIEW to 02-progress-log.md
    │     d) Update _xref/index.md
    │     e) Increment _xref/_next_id.json
    │
    ├─ @mnemosyne Confirm: "Compression complete: N entries compressed (M CRITICAL, P HIGH), K cross-refs added"
    │
    ├─ [COGNITIVE] Zeus checks: are there pending learnings? (Wisdom Bridge)
    │     If yes → inject into next agent's prompt
    │
    └─ Zeus continues orchestration → dispatches next phase with ZZ artifact
```

### Safety Preflight

Before ANY compression, Zeus MUST run this check:

```python
def can_compress(artifact_type, status, verdict):
    if artifact_type == "subtask_summary":
        return status == "complete"  # NOT in_progress, escalated, blocked
    if artifact_type == "IMPL":
        return True  # Themis APPROVED already verified
    if artifact_type == "REVIEW":
        return verdict == "APPROVED"  # NOT NEEDS_REVISION, FAILED
    if artifact_type == "PLAN":
        return all_phases_complete
    if artifact_type == "DISC":
        return user_approved
    if artifact_type == "ADR":
        return False  # NEVER compress ADRs
    return False
```

---

## 10. Safety Rules — NEVER Compress

Same as Level 1. Never compress the following:

| Artifact / Condition | Action |
|----------------------|--------|
| subtask_summary with `in_progress` / `escalated` / `blocked` | Skip. Flag to Zeus. |
| REVIEW with `NEEDS_REVISION` / `FAILED` | Skip. Leave in `.tmp/`. |
| Current active PLAN | Skip. Archive only at feature completion. |
| ADR notes (`_notes/`) — permanent, immutable | **NEVER touch.** |
| Any artifact with active blockers | Skip. Flag to Zeus. |

### Partial Compress — Warnlist

| Artifact / Condition | Action |
|----------------------|--------|
| subtask_summary with status `partial` | Compress BUT mark status as ⚠️ and score as MEDIUM minimum |
| DISC with `REQUEST CHANGES` | Flag to user, do not archive |
| DISC with `DISCARD` | Delete artifact, do not archive |
| Unrecognized `.tmp/` artifact | Flag to user, leave in place |

---

## 11. Transactional Write Protocol (C1 mitigation)

Same as Level 1. Atomic write prevents corruption from crashes during compression:

1. Write to target file + `.tmp` suffix (same directory)
2. `fsync()` the file descriptor — ensures data flushed to disk
3. **Validate:** file > 0 bytes, has a heading (`#` or `##` line)
4. `os.rename(.tmp, target)` — POSIX atomic rename on same filesystem
5. If crash during write: stale `.tmp` cleaned on next startup (>5 min old)

```python
import os

def atomic_write(path: str, content: str):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    if os.path.getsize(tmp_path) == 0:
        raise RuntimeError(f"Write validation failed: {tmp_path} is empty")
    os.rename(tmp_path, path)
```

---

## 12. Inline Compression — Active Session Protocol

"Inline compression" (L1) is the Pantheon-native mechanism agents use DURING an active session to shrink working context. It is distinct from "L2" batch promotion — the file-based Memory Bank writes Mnemosyne performs at phase boundaries (see §9). These are NOT a mandatory 3-layer trigger model: agents invoke L1 only; L2 happens automatically at gates.

### L1 — Inline Compression (the only agent-triggered step)
Call the compressor via the MCP tool. Scrubbing is AUTOMATIC in the MCP layer — never scrub manually and never embed raw secrets beyond what the tool scrubs:

```
execute_code_script("compress-inline.py", args=["compress", "--text", "<content>"])
```

Modes: `score` (preview priority), `compress` (scrub + score + compress), `stats`, `batch` (multiple files).

### L2 — Batch Promotion (automatic, not an agent trigger)
At phase gates / handoffs, Mnemosyne promotes compressed entries into the file-based Memory Bank (`01-active-context.md`, etc.). Agents do NOT invoke L2 — it runs automatically. Inline compression (L1) and batch promotion (L2) are NOT a mandatory 3-layer trigger model.

### Triggers (full table in §2)

- **C8**: after a CRITICAL/HIGH `subtask_summary` → L1 compress before next phase.
- **C9**: before delegating a large context block → L1 compress to cut tokens.
- **C10**: context pressure → handled by OpenCode native compaction (cross-reference only; no Pantheon mechanism).
- **C11**: phase boundary / handoff → L1 compress completed work.

### Promotion Pipeline (context flow, not a trigger model)

The Flow below shows how compressed context PROMOTES from live session → inline → batch. Agents run L1 only; L2 is automatic at gates:

```
Agent produces context (subtask_summary, large block, phase work)
    │
    ├─ [L1 INLINE] execute_code_script("compress-inline.py", args=["compress", "--text", "..."])
    │     → scrubbed + scored + compressed output (MCP layer scrubs automatically)
    │
    └─ [L2 PROMOTE] At phase gate / handoff, Mnemosyne promotes compressed
          entries into the file-based Memory Bank (01-active-context.md, etc.)
          → batch promotion, NOT an agent trigger
```

### Safety Rules

| Rule | Description |
|------|-------------|
| Scrubbing is automatic in the MCP layer | Never run a manual scrub; never embed raw secrets beyond what the tool scrubs |
| `compress-inline.py` always scrubs before scoring | Built-in security — no agent action needed |
| Inline compression (L1) is non-destructive to source files | Output is returned; originals untouched |

### Agent Responsibilities

**Implementation agents (Hermes, Aphrodite, Demeter, Hephaestus, Prometheus):**
- After a CRITICAL/HIGH `subtask_summary` → trigger C8 (L1 compress)
- Before delegating a large context block → trigger C9 (L1 compress)
- At a phase boundary / handoff → trigger C11 (L1 compress)
- Do NOT implement a separate context-pressure mechanism (C10 is OpenCode-native)

---

## 13. Security Scrubbing (H1 mitigation)

Scrubbing is automatic — the `memory_store` MCP server applies Layer 2 regex scrub before persisting content. No manual steps required.

### Layer 1 — Structural (metadata only)

Only promote structured metadata. NEVER promote:

- Raw stdout or stderr output
- Test output or command results
- Stack traces or error details
- Environment variables or configuration values

Allowed fields: file paths, status, pass/fail verdicts, phase names, agent names, dates.

### Layer 2 — Regex pattern scrub (automatic via MCP layer)

**Source of truth:** `scripts/scrub-secrets.py` — the single canonical scrubber. Both `memory_mcp_server.py` and `compress-inline.py` load it via `importlib` (the filename has a hyphen and cannot be `import`ed normally). Do NOT maintain a separate inline pattern list.

**Real signature:**

```python
def scrub(content: str) -> tuple[str, list[dict]]:
    # returns (scrubbed_text, redactions)
    # each redaction dict: {"type": str, "position": (start, end), "replacement": str}
```

**Secret types covered** (see `scripts/scrub-secrets.py` for the actual patterns): SSH private key, private key, certificate, Bearer token, JWT, GitHub PAT (`ghp_`), OpenAI key (`sk-...`), generic `api_key`/`token`/`secret`/`password`, AWS access key (`AKIA`), Google API key (`AIza`), Slack token (`xox`), Heroku API key (UUID), PostgreSQL/MySQL/Redis connection strings, and `.env` export statements.

> Scrubbing is AUTOMATIC in the MCP layer — `memory_store` and compress-inline both call `scrub()` before persistence. Agents never scrub manually.

---

## 14. Concurrency (M1 mitigation)

Same as Level 1. Zeus batches parallel phase completions into a single compression call. Lockfile safety net.

**Batching rule:** When multiple parallel phases complete simultaneously, Zeus collects all subtask_summaries and dispatches a single compression request to Mnemosyne:

```
@mnemosyne Compress batch (enhanced): [
  { type: subtask, phase: "2a", agent: Hermes, from: Hermes, to: Aphrodite, ... },
  { type: subtask, phase: "2b", agent: Aphrodite, from: Aphrodite, to: Hermes, ... },
  ...
]
```

Each entry is independently scored and budget-allocated.

**Lockfile safety net:** A lockfile at `.pantheon/memory-bank/.tmp/compress.lock` with `flock` as a safety net for the rare case of overlapping manual `/compress` and automatic compression.

---

## 15. Wisdom Bridge

Same as Level 1. Extraction BEFORE compression, non-blocking failures.

```
Phase N Themis APPROVED
    │
    ├─ 1. Agent extracts learnings → .pantheon/learnings/<feature>/learnings.md
    ├─ 2. Compression fires (scored + archived)
    └─ 3. Next agent dispatched with ZZ artifact + learnings injected
```

**Extraction is advisory, compression is mandatory.** If the agent fails to extract learnings (timeout, error), compression proceeds anyway.

### Injection

Zeus reads `.pantheon/learnings/<feature>/learnings.md` and includes in the next agent's prompt:

```
## Previous Wave Learnings
<contents of learnings.md>

## Compressed Context (Phase N → Phase N+1)
<contents of ZZ-phase{N}-context.md>

Apply these learnings and context to your implementation.
```

### Cleanup

At feature merge or sprint close:
1. Promote surviving learnings (those not already in `/memories/repo/`) to atomic facts
2. Delete `.pantheon/learnings/<feature>/learnings.md`

---

## 16. Rollback (C2 — use git)

Same as Level 1.

```bash
# View history of compressed file
git log -p .pantheon/memory-bank/01-active-context.md | less

# Restore pre-compression state
git show HEAD~1:.pantheon/memory-bank/01-active-context.md > .pantheon/memory-bank/01-active-context.md

# Or revert specific commit
git revert <commit-sha>
```

Pre-compression content is always available in git history.

---

## 17. Idempotency

Updated for Level 2 with content hashing and cross-ref dedup.

| Target | Idempotency Key | Behavior |
|--------|----------------|----------|
| `01-active-context.md` table row | (date, phase, agent) + content hash of summary | Skip if exact match exists; overwrite if same key but different hash |
| `02-progress-log.md` section | `### YYYY-MM-DD — <phase>: <agent>` | Skip append if heading exists |
| `02-progress-log.md` REVIEW line | `**Review:**` in same section | Skip if line exists |
| `01-active-context.md` Plans row | (date, feature) | Skip if exists |
| `_xref/index.md` | `| E{NNNN}` reference ID | Skip if ID exists; error if ID already used for different entity |
| `_xref/_next_id.json` | File path | Overwrite with incremented value |
| `ZZ-phase{N}-context.md` | Phase number | Overwrite if same phase (last write wins) |
| `.tmp/` file deletion | File path | File not found → silent skip |

### Content Hash

```python
import hashlib

def entry_hash(entry: dict) -> str:
    canonical = f"{entry['date']}|{entry['phase']}|{entry['agent']}|{entry.get('summary', '')}"
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]
```

When checking for duplicates, both the idempotency key AND the content hash must match for a skip. Same key but different hash → overwrite (entry was updated).

---

## 18. Budget Guardrails

Prevent budget abuse and ensure CRITICAL entries are never lost.

### Rules

| Guardrail | Threshold | Action |
|-----------|-----------|--------|
| **CRITICAL floor** | CRITICAL entries always expanded | Non-negotiable. Never compress to standard or aggressive. |
| **Overflow** | >5 CRITICAL entries per phase | Flag Zeus: "Phase N has M > 5 CRITICAL entries. Budget risk." |
| **Exceed budget** | CRITICAL entries alone exceed TOTAL_BUDGET (100 lines) | Escalate to Zeus: "CRITICAL entries require N lines but budget is 100. Options: (1) increase budget, (2) increase TOTAL_BUDGET permanently, (3) split phase." |
| **Carryover** | Unused PER_PHASE_BUDGET | 20% of unused budget rolls to next phase (round down). Remaining 80% is released (does not carry forward). |
| **Ceiling** | `## Completed Phases` section | Hard cap at 100 lines. Overflows trigger C7 size-based trim on LOW entries first. |

### Carryover Formula

```
carryover = floor(remaining_budget * 0.20)
next_phase_budget = PER_PHASE_BUDGET + carryover
```

Example: Phase 1 had 12-line budget, used 4 lines. Remaining = 8 lines. Carryover = floor(8 × 0.20) = 1 line. Phase 2 starts with 12 + 1 = 13 lines.

### C7 Trim Priority (Size-Based Auto-Trim)

When `01-active-context.md` exceeds 100 lines:

1. Sort entries by priority_score ascending (lowest first).
2. Trim LOW entries first (remove entire 0.5-line rows).
3. If still over budget, trim MEDIUM entries to 0.5 lines each.
4. Never trim CRITICAL or HIGH.
5. Trimmed entries are archived to `_notes/archive/YYYY-MM-compressed-entries.md`.
6. Log: "C7 trim: removed N low-priority entries, archived to _notes/archive/..."

---

## Quick Reference

```
┌────────────────────────────────────────────────────────────────────┐
│              CONTEXT COMPRESSION — LEVEL 2                         │
│                                                                    │
│  Priority Scoring (deterministic, no LLM):                         │
│    Score = 0.30×Impact + 0.25×Risk + 0.20×Novelty + 0.15×Blockers │
│            + 0.10×Downstream_relevance                             │
│    CRITICAL ≥ 0.75 | HIGH ≥ 0.50 | MEDIUM ≥ 0.25 | LOW < 0.25    │
│                                                                    │
│  Semantic Summarization (CRITICAL/HIGH only):                      │
│    Template per agent pair, ~50 tok each                           │
│    CRITICAL: 3 lines (what + why + gotcha)                         │
│    HIGH: 2 lines (what + why)                                      │
│                                                                    │
│  Downstream-Aware Field Masks:                                     │
│    (from_agent, to_agent) → field set                              │
│    *→Themis: preserve ALL  |  *→Mnemosyne: preserve MINIMAL       │
│                                                                    │
│  Budget Allocation (priority-greedy):                              │
│    TOTAL = 100 lines | PER_PHASE = floor(100 / phases)             │
│    CRITICAL always expanded → HIGH → MEDIUM → LOW                  │
│    20% of unused budget carries to next phase                      │
│                                                                    │
│  Cross-References:                                                 │
│    E{NNNN} endpoints | M{NNNN} migrations | D{NNNN} decisions     │
│    C{NNNN} components | Auto-generated in _xref/index.md          │
│                                                                    │
│  ZZ Artifact:                                                      │
│    .pantheon/memory-bank/.tmp/ZZ-phase{N}-context.md                    │
│    Injected into next phase agent prompt                           │
│                                                                    │
│  Safety: NEVER compress in_progress/escalated/                     │
│    blocked/NEEDS_REVISION/FAILED/ADR                               │
│  Write safety: atomic .tmp + fsync + rename                        │
│  Security: Layer 1 (structural) + Layer 2 (regex)                  │
│  Concurrency: Zeus batches, lockfile as safety net                 │
│  Rollback: git log -p                                              │
│  Idempotent: keyed by (date, phase, agent) + content hash          │
│  Budget guardrails: CRITICAL floor, overflow flag, carryover       │
│  Inline Compression (C8-C11 - Active Session, L1 = Pantheon-native): │
│    C8: CRITICAL/HIGH subtask_summary → compress (L1)                │
│    C9: pre-delegation large block → compress (L1)                   │
│    C10: context pressure → OpenCode native compaction (x-ref only)   │
│    C11: phase boundary / handoff → compress (L1)                    │
│    L1 = compress-inline.py MCP | L2 = batch promotion (Mnemosyne)   │
│    Scrubbing automatic in MCP layer — never scrub manually           │
│                                                                    │
│  Zeus: cognitive scoring + summarization + budget + cross-refs     │
│  Mnemosyne: file I/O (write ZZ, active context, progress log,      │
│              xref index, next_id.json, delete .tmp)                │
└────────────────────────────────────────────────────────────────────┘
```

---

**References:**
- `skill: artifact-management` — artifact lifecycle
- `instructions/agent-return-format.instructions.md` — subtask_summary format
- `skill: memory-bank` — memory bank structure
- `skills/wisdom-accumulation/SKILL.md` — learning extraction
- `skills/memory-bank/SKILL.md` — memory bank maintenance
- `instructions/backend-standards.instructions.md` — zeus scoring reference
