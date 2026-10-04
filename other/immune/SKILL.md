---
name: immune
version: "5.3.1"
description: "Hybrid adaptive system v5.3.0: Vector engine (local MiniLM by default, optional GPU daemon auto-detected on EMBED_PORT + cross-encoder re-ranking) + FTS4 via RRF. Cheatsheet (positive) + Immune (negative) + ContextMemory + Score + Flush. Standalone CLI, no external services or GPU required. Shared with Chimera."
---

# Immune System v4 — Hybrid Cheatsheet + Immune

You operate a hybrid adaptive system with two complementary memories:
- **Cheatsheet** (positive patterns): domain-specific strategies injected BEFORE generation to improve output quality
- **Immune** (negative patterns): antibodies that detect known errors and discover new threats AFTER generation

Both memories use Hot/Cold tiering to keep context lean.
All data access goes through the **adapter CLI** (`node ~/.claude/skills/immune/immune-adapter.js`).

## Input Parsing

The user invokes with content to scan. Parse these parameters:

- **input**: The text/code/content to scan (required — either inline or from context)
- **domain**: One of: domain, code, writing, research, strategy, webdesign, _global (default: auto-detect)
- **domains**: Array of domains (overrides single domain). Example: `domains=domain,code`
- **constraints**: Any specific requirements the output should satisfy (optional)
- **mode**: `full` (cheatsheet + scan, default) | `scan-only` (skip cheatsheet) | `cheatsheet-only` (return cheatsheet, no scan)

<examples>
<example>
/immune Check this function for common pitfalls
→ domains=["code"] (auto-detected), mode=full
</example>
<example>
/immune domain=domain Vérifie ce programme de musculation
→ domains=["domain"] (explicit)
</example>
<example>
/immune domains=domain,code Check this workout generator API
→ domains=["domain", "code"] (multi-domain)
</example>
<example>
/immune
→ scans the most recent output in the conversation
</example>
</examples>

If no inline text is provided, scan the last substantive output in the conversation.

**Shortcuts:**
- `/immune scan` → Full conversation scan in `mode=full`. Extracts BOTH new threats (antibodies) AND new good practices (strategies). Domains auto-detected. This is the standard "make this conversation teach the system" command.
- `/immune` (bare) → Same as `scan` if there is conversation context; otherwise scans the last output only.

Whenever the user invokes `/immune scan` or just says "scan la conversation" / "scan this conversation", default to extracting both threats AND strategies over the entire conversation history, in `mode=full`. Do not require the user to repeat "menaces + stratégies" — that is the default intent of `scan`.

**Domain auto-detection:** Read `~/.claude/skills/immune/config.yaml` and match content against `domain_keywords`. If no strong match, use `["_global"]`. If single `domain` string provided, wrap in array: `domains = [domain]`.

## Execution

### Step -1 — Context Search (past session awareness)

Search for relevant past sessions to inform the current scan:

```bash
node ~/.claude/skills/immune/immune-adapter.js get-context --query "{task keywords or domain}" --days 90 --limit 5
```

If results are found, note recurring patterns or past issues for the domain. This enriches the scan with historical awareness — the scanner will know if similar content was flagged before.

Log: `[IMMUNE] Context: {count} relevant past sessions found`

### Step 0 — Cheatsheet Injection (positive patterns)

Skip this step if `mode == "scan-only"`.

**0a. Load HOT strategies via adapter:**

Run:
```bash
node ~/.claude/skills/immune/immune-adapter.js get-strategies --domains '{domains_json}' --tier hot --limit 15
```
Parse the JSON output. The adapter returns strategies pre-filtered by domain, classified as HOT, sorted by effectiveness descending, and capped at 15.

**0b. Load COLD strategies summary:**

Run:
```bash
node ~/.claude/skills/immune/immune-adapter.js get-strategies --domains '{domains_json}' --tier cold
```
Extract a short keyword from each COLD strategy's `pattern` field. Join as comma-separated list.

**0c. Build cheatsheet block:**
Format HOT strategies as XML:
```xml
<cheatsheet domain="{domains}">
  <strategy id="{id}" effectiveness="{effectiveness}">
    {pattern}
    Example: {example}
  </strategy>
  ...
</cheatsheet>
```

If there are COLD strategies, add a one-liner:
```xml
<cheatsheet_cold>Also consider: {comma-separated COLD pattern keywords}</cheatsheet_cold>
```

If `mode == "cheatsheet-only"`, output the cheatsheet block and stop here.

Log:
```
[IMMUNE] Cheatsheet: {n_hot} HOT + {n_cold} COLD strategies (domains: {domains})
```

**0d. Present cheatsheet to user:**
If running standalone (`/immune`), show the cheatsheet as context the user should apply to their next generation. If called by Chimera, return the XML block for injection into PRISM prompts.

### Step 1 — Load & Classify Antibodies (Hot/Cold)

**1a. Load HOT antibodies via adapter:**

Run:
```bash
node ~/.claude/skills/immune/immune-adapter.js get-antibodies --domains '{domains_json}' --tier hot --limit 15
```
The adapter returns antibodies pre-filtered by domain, classified as HOT (severity=critical OR seen_count>=3 OR last_seen<30d), sorted by severity then seen_count, capped at 15.

**1b. Load COLD antibodies summary:**

Run:
```bash
node ~/.claude/skills/immune/immune-adapter.js get-antibodies --domains '{domains_json}' --tier cold
```
For each COLD antibody, extract a short keyword from its `pattern` field.
Join as comma-separated list.

Log:
```
[IMMUNE] Tier split: {n_hot} HOT + {n_cold} COLD / {n_hot + n_cold} total (domains: {domains})
```

### Step 2 — Scan

Spawn the `immune-scan` agent (Haiku) with the following XML-structured prompt:

```xml
<scan_request>
  <domains>{detected_domains as JSON array}</domains>
  <task>{task description or "Scan the following content for errors and threats"}</task>
  <constraints>{constraints or "none"}</constraints>

  <content>
{the input text/code/content to scan}
  </content>

  <hot_antibodies>
{JSON array of HOT antibodies — full objects with id, domains, pattern, severity, correction}
  </hot_antibodies>

  <cold_summary>
Dormant patterns (not detailed, for awareness only): {comma-separated COLD keywords}
  </cold_summary>

  <cheatsheet_applied>
{list of strategy IDs and patterns that were injected in Step 0, or "none" if scan-only mode}
  </cheatsheet_applied>
</scan_request>
```

Log: `[IMMUNE] Scanning... ({n_hot} active antibodies)`
Wait for result.

If corrections applied:
  Log: `[IMMUNE] Match {antibody_id}: {original} → {corrected}`
If new threats detected:
  Log: `[IMMUNE] New threat: {pattern}`
If new strategies detected:
  Log: `[IMMUNE] New strategy: {pattern}`

### Step 3 — Update Immune Memory (with COLD deduplication)

**3a. Matched HOT antibodies:**
For each antibody matched by the scanner, update via adapter:
```bash
node ~/.claude/skills/immune/immune-adapter.js update-antibody --id {antibody_id} --increment_seen true --last_seen {today}
```

**3b. New threats — deduplicate via similarity scoring:**
For each new threat in `new_threats_detected`:

1. Check for duplicate using multi-criteria similarity (Jaccard + substring + domain):
```bash
node ~/.claude/skills/immune/immune-adapter.js check-duplicate --pattern "{pattern}" --domains '{domains_json}' --type antibody
```
Returns `{ duplicate: true/false, best_match: { id, score, pattern }, threshold: 0.7 }`

2. **If duplicate is true** (score >= 0.7, same domain + similar pattern) → REACTIVATE:
   - Update the matched antibody: `update-antibody --id {matched_id} --increment_seen true --last_seen {today}`
   - Log: `[IMMUNE] Reactivated COLD antibody {id}: {pattern}`
   - Skip new antibody creation (deduplication preserves a single source of truth)
3. **If no match** AND `auto_add_threats` is true → CREATE new antibody:
```bash
node ~/.claude/skills/immune/immune-adapter.js add-antibody --json '{"id":"AB-{next_number}","domains":{domains},"pattern":"{pattern}","severity":"{severity}","correction":"{correction}","seen_count":1,"first_seen":"{today}","last_seen":"{today}"}'
```
   - Log: `[IMMUNE] + New antibody {id}: {pattern}`

**3c. Get updated stats:**
```bash
node ~/.claude/skills/immune/immune-adapter.js stats
```

Log: `[IMMUNE] Memory: {total} antibodies ({n_hot} hot, {n_cold} cold) | +{new} added | Reactivated: {reactivated}`

### Step 3b — Update Cheatsheet Memory (positive patterns)

Skip if `mode == "scan-only"` or no `new_strategies_detected` in scan result.

**3b-i. Deduplicate via similarity scoring:**
For each new strategy in `new_strategies_detected`:
1. Check for duplicate using multi-criteria similarity:
```bash
node ~/.claude/skills/immune/immune-adapter.js check-duplicate --pattern "{pattern}" --domains '{domains_json}' --type strategy
```
2. **If duplicate is true** (score >= 0.7, overlapping domains + similar pattern) → REINFORCE:
   - Calculate new effectiveness: `new_eff = old_eff * 0.8 + reported_eff * 0.2` (exponential moving average)
   - Update: `update-strategy --id {matched_id} --increment_seen true --last_seen {today} --effectiveness {new_eff}`
   - Log: `[IMMUNE] Reinforced strategy {id}: {pattern} (eff: {old}→{new})`
3. **If no match** AND `auto_add_strategies` is true → CREATE new strategy:
```bash
node ~/.claude/skills/immune/immune-adapter.js add-strategy --json '{"id":"{prefix}-{next_number}","domains":{domains},"pattern":"{pattern}","example":"{example}","effectiveness":{eff},"seen_count":1,"first_seen":"{today}","last_seen":"{today}"}'
```
   - Log: `[IMMUNE] + New strategy {id}: {pattern}`

**3b-ii. Prune low-effectiveness:**
If any strategy has `effectiveness < 0.2` AND `seen_count >= 5`, note it for manual review.

Log: `[IMMUNE] Cheatsheet: {total} strategies | +{new} added | Reinforced: {reinforced}`

### Step 4 — Score

Calculate the universal score via adapter:
```bash
node ~/.claude/skills/immune/immune-adapter.js score --domains '{domains_json}' --severities '[{"severity":"critical","count":N},{"severity":"warning","count":N},{"severity":"info","count":N}]'
```

The adapter returns: `score` (0-100), `pass` (boolean), `z` (z-score vs domain baseline), `baseline` (mean, std, threshold, n), `deductions`.

### Step 5 — Output

**If clean:**
```
───
IMMUNE v4 | domains={domains} | Score: {score}/100 ({PASS|FAIL}) | z={z}
   Baseline ({domain}): mean={mean} std={std} threshold={threshold}
   Cheatsheet: {n_strategies} strategies applied | Antibodies: {n_hot}/{max} HOT, {n_cold} COLD
   No issues detected
───
```

**If corrections or threats found:**
```
───
IMMUNE v4 | domains={domains} | Score: {score}/100 ({PASS|FAIL}) | z={z}
   Baseline ({domain}): mean={mean} std={std} threshold={threshold}

Corrections Applied:
  [AB-XXX] {pattern} → {correction}

New Threats Detected:
  [{severity}] {pattern} — {suggested_correction}

Reactivated:
  [AB-XXX] {pattern} (was COLD, now HOT)

New Strategies Learned:
  [CS-XXX] {pattern} (eff: {effectiveness})

───
Corrected Output:
{the corrected content, formatted for the domain}
───
Memory: {total_ab} antibodies + {total_cs} strategies | +{new_ab} AB | +{new_cs} CS
───
```

Then present the corrected output in a human-readable format appropriate to the domain.

### Step 6 — Session Log

Log the session result for future context:
```bash
node ~/.claude/skills/immune/immune-adapter.js log-session --date {today} --domains '{domains_json}' --result {clean|corrected|flagged} --summary "{brief summary of what was scanned and found}" --score {score}
```

This writes to `context/YYYY-MM-DD.md` + SQLite session_logs + FTS4 index for future `get-context` searches.

### Step 7 — Flush Pre-Compaction (optional)

If the conversation context is approaching compaction, save any pending antibodies/strategies that haven't been committed yet:
```bash
node ~/.claude/skills/immune/immune-adapter.js flush-pending --json '{"antibodies":[...],"strategies":[...]}'
```

Quality gate validation:
- Pattern must be >= 20 characters
- Antibodies require: id, pattern, severity, correction
- Strategies require: id, pattern
- FTS4 duplicate check prevents re-creating existing patterns
- Flushed records are flagged with `quality_gate=1`

Log: `[IMMUNE] Pre-compaction flush: +{n} antibodies, +{n} strategies (quality_gate=true)`

## Error Handling

- If adapter CLI fails: fall back to reading JSON files directly (`immune_memory.json`, `cheatsheet_memory.json`) — they are kept in sync via dual-write.
- If `immune_memory.json` does not exist: adapter auto-creates it with empty antibodies.
- If `cheatsheet_memory.json` does not exist: adapter auto-creates it with empty strategies.
- If `immune_memory.json` has `"version": 2`: adapter auto-migrates `"domain"` to `"domains": ["domain_value"]`.
- If the agent returns invalid JSON: retry once. If still invalid, report the raw output with a warning.
- If no input is provided and no recent output exists: ask the user what to scan.
- If all antibodies are COLD (none qualify as HOT): still send the scan with empty `hot_antibodies` array and full `cold_summary`. Haiku can still detect new threats via Phase 2.
