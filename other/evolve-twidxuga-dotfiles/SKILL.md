---
name: evolve
description: Self-improvement loop for opencode configuration. Analyzes session history, queues candidate learnings, lints them, promotes high-confidence rules, and tracks rule effectiveness via Reflexion-style feedback. Use when you want the agent setup to learn from accumulated experience.
---

# Evolve Skill v2 — Configuration Self-Improvement with Feedback Loop

You are running the **evolve loop**: a structured capture → queue → lint → promote → measure pipeline that improves the opencode agent configuration based on real session data.

This is v2. The big differences from v1:
1. Candidates go to a **queue** first; promotion is a separate, evidence-gated step
2. **Sensitivity classification** uses a maintained term list + regex pack (not hardcoded grep)
3. **Reflexion feedback loop**: every promoted rule gets a `rule_id` and we measure whether the symptom recurs
4. **Detection beyond keywords**: tool-failure mining, repeated-question detection, runtime-discovery extraction
5. **Better scoring**: includes reversibility, effort, and blast radius
6. **Dual logs**: generic to public, full to private

## CRITICAL: Public vs Private File Routing

`~/.config/opencode/` is published to a **public GitHub repository**. NEVER write content there that names the user's employer, internal hostnames, AWS profiles, internal repo paths, internal namespaces, or any other private detail.

**Private knowledge base lives at `~/Documents/QuickAccess/kb/ai-agents/`** (Dropbox-synced, never pushed).

### Sensitivity Classifier (apply to EVERY finding AND its evidence)

Run all THREE checks before deciding public vs private:

1. **Term match** — grep proposed content against `~/Documents/QuickAccess/kb/ai-agents/PRIVATE-TERMS.txt` (case-insensitive substring). Any hit → private.
2. **Regex match** — grep proposed content against `~/Documents/QuickAccess/kb/ai-agents/SENSITIVITY-REGEX.txt`. Any hit → private.
3. **Provenance check** — if the source session referenced any private file, or any session read pulled content from `~/Documents/QuickAccess/` or internal repo paths, the finding is sensitive **by association**, even if the proposed text looks generic.

**Default-private** when any uncertainty remains. Move to public only when all three checks pass AND the content describes generic tools/CLIs/Anthropic/Slack/MCP behaviour with no inferred internal context.

Both files are user-maintained and updated by `/evolve` when new sensitive terms are discovered.

## What You Are Improving

### Public files (in `~/.config/opencode/`, published)
| File | Purpose | When to update |
|------|---------|----------------|
| `AGENTS.md` | Global system prompt | Generic stack patterns, workflow preferences |
| `rules/global.md` | Always-active rules | Generic anti-patterns, generic CLI rules |
| `rules/terraform.md` | Terraform rules | Generic HCL patterns |
| `opencode.json` | Core config | Model, watcher, generic agents, permission policies |
| `oh-my-openagent.json` | Agent framework | Generic concurrency/timeout tuning |
| `commands/*.json` | Slash commands | Generic reusable workflows |
| `skills/*/SKILL.md` | Agent skills | Generic skill instructions |
| `agent/*.md` | Agent definitions | Generic specialist prompts |
| `EVOLUTION_LOG.md` | Public log | Generic entries only |

### Private files (in `~/Documents/QuickAccess/kb/ai-agents/`, off-repo)
| File | Purpose |
|------|---------|
| `AGENTS.md` | Company/infra root TOC |
| `aws.md`, `auth.md`, `dynamic-envs.md`, `observability.md`, `terraform-conventions.md` | Topic files (split from a monolithic AGENTS.md) |
| `rules-terraform.md` | Internal IRSA/SCP/namespace/bundling rules |
| `EVOLUTION_LOG.md` | Full evolve history with sensitive details |
| `QUICKACCESS-INDEX.md` | Recursive index of `~/Documents/QuickAccess/` |
| `QUEUE.jsonl` | Candidate learnings awaiting promotion (one event per line) |
| `RULES-INDEX.jsonl` | Per-rule telemetry: created/cited/recurred/validated/demoted |
| `PRIVATE-TERMS.txt` | Term list for sensitivity classifier |
| `SENSITIVITY-REGEX.txt` | Regex pack for sensitivity classifier |

---

## Phase 0 — Regression Check (run FIRST on every `/evolve`)

Before doing anything else, scan public files for any sensitive strings that may have leaked since last run:

```bash
# IMPORTANT: filter out comment lines and empty lines BEFORE passing to grep.
# Empty lines in the pattern file would cause grep to match every line.

# 0a. Scan public files against the private-terms list (case-insensitive substring)
TERMS=$(grep -vE '^\s*(#|$)' ~/Documents/QuickAccess/kb/ai-agents/PRIVATE-TERMS.txt)
echo "$TERMS" | grep -inFf /dev/stdin \
  ~/.config/opencode/AGENTS.md \
  ~/.config/opencode/EVOLUTION_LOG.md \
  ~/.config/opencode/rules/*.md \
  ~/.config/opencode/skills/evolve/SKILL.md \
  ~/.config/opencode/commands/*.json \
  ~/.config/opencode/command/*.md \
  ~/.config/opencode/agent/*.md \
  ~/.config/opencode/opencode.json \
  ~/.config/opencode/oh-my-openagent.json \
  2>/dev/null

# 0b. Scan against the regex pack
REGEXES=$(grep -vE '^\s*(#|$)' ~/Documents/QuickAccess/kb/ai-agents/SENSITIVITY-REGEX.txt)
echo "$REGEXES" | grep -nEf /dev/stdin \
  ~/.config/opencode/AGENTS.md \
  ~/.config/opencode/EVOLUTION_LOG.md \
  ~/.config/opencode/rules/*.md \
  ~/.config/opencode/skills/evolve/SKILL.md \
  ~/.config/opencode/commands/*.json \
  ~/.config/opencode/command/*.md \
  ~/.config/opencode/agent/*.md \
  2>/dev/null
```

If anything matches: **report to user and STOP**. Resolution choices:
- Move the line to private kb and replace with a pointer
- Accept and add the term to an allowlist (rare)
- Strip the line entirely

Never auto-fix regressions — user decides.

---

## Phase 1 — Session Analysis (parallel)

Run 1a-1d in PARALLEL; they're independent.

### 1a. Recent sessions
```
session_list(limit=20, from_date="<2 weeks ago>")
```
Read each session with >4 messages:
```
session_read(session_id="...", include_todos=true)
```

### 1b. Keyword pattern search
```
session_search(query="don't", limit=20)        # corrections
session_search(query="no, ", limit=20)         # corrections
session_search(query="wrong", limit=20)
session_search(query="instead", limit=20)
session_search(query="actually", limit=20)
session_search(query="never", limit=20)
session_search(query="always", limit=20)
session_search(query="remember", limit=20)
session_search(query="fail", limit=20)         # NEW v2: tool-failure mining
session_search(query="timeout", limit=20)      # NEW v2
session_search(query="error", limit=30)
```

### 1c. opencode-mem memories
```bash
for db in ~/.opencode-mem/data/projects/project_*_shard_0.db; do
  sqlite3 "$db" "SELECT content, created_at FROM memories ORDER BY created_at DESC LIMIT 30;"
done
```

### 1d. Beyond-keyword detection (NEW in v2)

Look for these patterns in the session transcripts you read in 1a:
- **Tool-failure clusters**: same tool failed 3+ times in one session → tool-usage rule gap or agent prompt issue
- **Repeated identical questions across sessions**: agent re-discovered the same thing → missing context in AGENTS.md
- **Runtime discoveries**: agent had to `grep` / `read` to find something basic (file path, config name) → candidate for AGENTS.md
- **Oracle misuse**: oracle was called for a trivial task, or NOT called for a hard one → oracle-invocation rule
- **Model-selection mistakes**: expensive model used for trivial work, or vice versa
- **Overfitting signals**: a rule from a previous evolve was cited but contradicted by the user → demote candidate

---

## Phase 2 — Pattern Classification

For each finding, decide:

### A. Category (extended in v2)

| Category | Signal |
|----------|--------|
| `correction` | User said no/don't/wrong/actually |
| `friction` | Same task done manually 3+ times |
| `missing-context` | Agent had to discover at runtime; same question across sessions |
| `config-bug` | Something broke due to config |
| `missing-agent` | Task needed specialist that doesn't exist |
| `outdated-rule` | Rule contradicts actual practice |
| `outdated-context` | Codebase moved on; rule references nonexistent files |
| `skill-gap` | Skill instructions wrong or incomplete |
| `pattern` | Recurring workflow → command candidate |
| `tool-failure-pattern` | Same tool fails repeatedly → tool-usage rule |
| `model-selection-mistake` | Wrong model tier picked |
| `oracle-mis-invocation` | Oracle over- or under-used |
| `overfitting` | Existing rule too narrow/specific |
| `privacy-leak` | Sensitive content found in public files |

### B. Sensitivity (run all 3 checks from the top of this skill)
`public` | `private` | `unknown` (default-private)

### C. Source provenance
Record source session IDs and a short evidence quote (≤200 chars).

---

## Phase 3 — Scoring v2

For each finding, score five dimensions (1-5):
- **Impact** — how much does this improve future sessions?
- **Confidence** — how certain is this the right change?
- **Reversibility** — how easy to undo if wrong? (5 = trivial, 1 = breaks many things)
- **Risk** — likelihood of breaking something else (5 = high, 1 = none)
- **Effort** — implementation cost (5 = many file changes, 1 = one-line)
- **BlastRadius** — how many things this affects (5 = global, 1 = isolated)

**Value = (Impact × Confidence × Reversibility) / (Risk × Effort × BlastRadius)**

Decision matrix:
| Value | Action |
|-------|--------|
| `> 4` | **Apply now** (auto-write to public/private file) |
| `> 1` | **Queue** in `QUEUE.jsonl` for next-run review |
| `<= 1` | Skip — log as "skipped" with reason |

Special cases:
- Any `privacy-leak` category → **apply now** regardless of score (privacy is urgent)
- Any `outdated-rule` or `outdated-context` → **queue**, never auto-delete
- Any `overfitting` → **queue** with proposed rewrite

---

## Phase 4 — Apply or Queue

### Auto-apply category (score > 4, low blast-radius)

| Change type | Auto-apply? |
|-------------|-------------|
| Additive rule (new bullet in existing section) | ✅ Yes |
| New log entry | ✅ Yes |
| `QUICKACCESS-INDEX.md` row addition | ✅ Yes |
| `watcher.ignore` addition | ✅ Yes |
| Append to private `aws.md`/`auth.md`/etc | ✅ Yes |
| New `PRIVATE-TERMS.txt` entry | ✅ Yes |
| `QUEUE.jsonl` append | ✅ Yes |

### Approval-required category (always queue with notification)

| Change type | Why approval |
|-------------|--------------|
| Delete or rewrite any existing rule | Reversibility risk |
| `opencode.json` structural change (plugin, mcp, provider) | Global blast radius |
| Model/provider switch | Cost implications |
| New slash command | New surface area |
| New skill or new agent file | New behaviour |
| Any change with sensitivity=unknown | Privacy risk |
| Any `overfitting` rewrite | Could break workflow that depends on current rule |

### Diff-before-write rule
Always print the diff (old vs new) before writing. For private kb files, the diff is shown in the run log.

### Writing a rule (with rule_id tracking)

When writing a new rule to `rules/*.md` or `kb/ai-agents/*.md`:
1. Generate `rule_id` = `r` + 6 random hex chars (e.g. `r3a7f1c`)
2. Add an HTML-comment with the rule_id at the end of the line: `<!-- rule:r3a7f1c -->`
   - Example: `- Never set temperature on extended-thinking agents <!-- rule:r3a7f1c -->`
3. Append a `created` event to `~/Documents/QuickAccess/kb/ai-agents/RULES-INDEX.jsonl`:
```json
{"ts":"2026-05-15T20:00:00Z","rule_id":"r3a7f1c","event":"created","source_session_id":"ses_xxx","file":"~/.config/opencode/rules/global.md","line":99,"evidence_quote":"...","category":"correction"}
```

### Queueing a candidate

Append one line to `~/Documents/QuickAccess/kb/ai-agents/QUEUE.jsonl`:
```json
{"id":"q3a7f1c","ts":"2026-05-15T20:00:00Z","source_session_ids":["ses_xxx"],"evidence_quote":"...","category":"correction","summary":"...","confidence":3,"recurrence_count":1,"sensitivity":"private","proposed_target_file":"~/Documents/QuickAccess/kb/ai-agents/aws.md","status":"pending","notes":"score 1.8 < apply threshold; recheck next run"}
```

---

## Phase 5 — Dual Log

Append TWO entries per run:

### Public log: `~/.config/opencode/EVOLUTION_LOG.md`
- Generic findings only
- No company/internal names
- No source session IDs that may correlate to private work
- Format: short markdown summary

### Private log: `~/Documents/QuickAccess/kb/ai-agents/EVOLUTION_LOG.md`
- Full version: all findings, sources, evidence, rule_ids, queue events
- Includes everything from public log + the sensitive details

Both logs use this top-level structure:

```markdown
## YYYY-MM-DD — Evolution Run [v2]

### Sessions Analysed
- N sessions; date range; brief patterns

### Applied (Public)
- `rules/global.md` rule:r3a7f1c → "<summary>" (Value=4.5)

### Applied (Private — kb/ai-agents/)  [omit from public log]
- `kb/ai-agents/auth.md` rule:r5b8d2e → "<summary>" (Value=6.0)

### Queued
- q3a7f1c "<summary>" Value=1.8 → recheck if recurrence ≥ 3

### Validated rules (recurrence dropped after promotion)
- r5b8d2e: 4 prior recurrences → 0 in last 2 weeks → marked validated

### Demoted rules (no impact / contradicted)
- r9f4a1c: rule cited 0 times, symptom still recurring → demoted to QUEUE

### Skipped (low value)
- "<finding>" Value=0.6 reason: blast-radius too high

### Privacy regressions (Phase 0)
- None [or: list with action taken]

### Next focus
- Watch for: ...
```

---

## Phase 6 — Index + Telemetry Maintenance

### 6a. RULES-INDEX feedback loop (Reflexion)

For every existing `rule_id` from previous runs:
1. Search session transcripts for the rule's symptom (evidence quote from the `created` event)
2. Count recurrences in sessions AFTER the `created` timestamp
3. Search session transcripts for the rule itself being cited (the agent quoting / following it)
4. Update events:
   - `validated` if symptom recurrence dropped to ≤1 in the last N sessions AND citations > 0
   - `cited` if rule was followed (with session ID)
   - `recurrence_detected` if symptom recurred despite rule existing
   - `stale` if symptom hasn't recurred in 6+ months AND rule never cited
   - `demoted` if recurred 3+ times despite rule (move back to QUEUE with notes)

### 6b. QUICKACCESS-INDEX.md (incremental)

Don't rebuild from scratch. Cache mtime+size per file in a sidecar `~/Documents/QuickAccess/kb/ai-agents/.qa-index-cache.json` keyed by absolute path with `{mtime, size, summary}` per entry.

For each file in `~/Documents/QuickAccess/`:
- If mtime+size unchanged → skip
- If new → read first 3 lines, generate one-line summary, add row, update cache
- If missing → mark as "removed (verify with user)" in index, do NOT delete entry

Cache example schema (one entry per file, keyed by path):
```
{"<file-path>": {"mtime": "...", "size": 12345, "summary": "..."}}
```

Full rebuild monthly (record date in `QUICKACCESS-INDEX.md`).

### 6c. PRIVATE-TERMS.txt maintenance

If Phase 0 caught a sensitive string that ISN'T in PRIVATE-TERMS.txt:

- **Normal mode**: auto-add if the string matches an existing regex in `SENSITIVITY-REGEX.txt` (clearly sensitive); otherwise propose to user and wait for confirmation.
- **`--dry-run` mode**: never write. Print the candidate term, the matching regex (if any), and the proposed action. Output goes to the dry-run summary at end of run, not silently dropped.

---

## Modes / Arguments

| `$ARGUMENTS` | Behaviour |
|--------------|-----------|
| (empty) | Full pipeline: Phase 0 → 6 |
| `--dry-run` | Run all phases; print diffs; write nothing |
| `--promote` | Skip Phase 1-3; review QUEUE; promote items with `recurrence_count ≥ 3` or `confidence ≥ 4` |
| `--reject <id>` | Mark queue entry `id` as `status:rejected` |
| `--focus=rules` | Only update rules files |
| `--focus=agents` | Only update AGENTS.md (public + private topic files) |
| `--focus=skills` | Only update skills |
| `--focus=commands` | Only update commands |
| `--focus=opencode` | Only analyse opencode.json |
| `--focus=index` | Only run Phase 6b (incremental index) |
| `--focus=privacy` | Only run Phase 0 |
| `--review-queue` | List queued items + their stats; no writes |
| `--validate-rules` | Only run Phase 6a (Reflexion loop); no new findings |
| `--rebuild-index` | Force full QUICKACCESS-INDEX rebuild |
| `--since=YYYY-MM-DD` | Limit Phase 1 to sessions after this date |
| `--session=<id>` | Only analyse one session |

These ARE valid stop points. Don't continue past them.

---

## Safety Constraints

- **Never commit** changes to git
- **Never delete** existing rules without explicit user approval (demote/queue instead)
- **Never delete or rename** files under `~/Documents/QuickAccess/`
- **Never modify** `opencode.json`, `opencode-mem.jsonc`, or `oh-my-openagent.json` without showing full diff
- **Never touch** `plugin` array or `mcp` block in `opencode.json` without explicit user approval
- **Never write company-identifying content into `~/.config/opencode/`** — always route private
- **Always** read the file before editing
- **Always** show the diff
- **Stop and ask** on contradictions between sessions

## Verbose vs structured output

End-of-run: produce BOTH
- Long markdown summary (for human) → appended to dual logs
- Compact JSON manifest (for diffing/automation) → `~/Documents/QuickAccess/kb/ai-agents/evolve-runs/<date>.json` with: `{run_id, ts, mode, findings, applied, queued, skipped, validated, demoted, sensitivity_counts}`
