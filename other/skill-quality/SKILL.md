---
name: skill-quality
description: >
  Automatically rate any skill's description quality and rewrite it if needed — the quality gate
  for the skill creation pipeline. Invoked by /skill-creator after skill installation, or
  directly with /skill-quality [skill-name]. When to trigger: automatically after every new
  skill is installed via /skill-creator; when manually auditing a skill's description
  quality; when a skill's description fails to attract correct usage; or when enhancing an
  existing skill and wanting to verify the description is strong. Key capabilities: two
  independent critics (Capability + Likelihood to Pick Up, 0–100 each); calibrated gate
  (avg≥80 AND one≥85 AND none<70); one automatic rewrite cycle on failure; results written
  to JSON immediately (survives session compaction); and discrepancy detection (flags when
  critics disagree by >20 points). Also handles: --quality-gate off bypass flag, self-referential
  check (skill-quality skips its own catalog registration), and idempotent re-rating of
  already-rated skills. Compare with skill-import (one-off conflict detection) and skill-creator
  (full creation pipeline that calls this skill automatically).
---

# Skill Quality — Description Critic Gate

Spawns two independent critics to rate a skill's description, applies the calibrated gate,
and rewrites automatically if it fails. Called by `/skill-creator` as a post-install step,
or run directly.

---

## Step 0: Parse Arguments

Accept `--skill [name]` or a bare skill name. No flags = error.

Detect `--quality-gate off` bypass: if present, skip all critics, write `quality_gate_passed: null`,
return immediately without catalog registration.

**Self-referential guard:** If the target is `skill-quality` itself, run the critic check normally
but mark `registration_status: "skipped"` in the output — skill-quality never registers itself to
the catalog.

---

## Step 1: Validate Target Exists

```python
import yaml
from pathlib import Path

skill = "[name]"
path = Path(f"~/.claude/skills/{skill}/SKILL.md").expanduser()

if not path.exists():
    raise ValueError(f"Skill not found: {skill}")

content = path.read_text()
fm = yaml.safe_load('---\n' + content.split('---', 2)[1])
desc = fm.get('description', '')
if not desc:
    raise ValueError(f"No description field in {skill}/SKILL.md")
```

Always use `yaml.safe_load('---\n' + content.split('---', 2)[1])` — not regex — to handle
folded scalar blocks with `:` characters correctly.

---

## Step 2: Spawn Critics in Parallel

Spawn two independent depth-1 subagents in parallel. Both read `memory/agents/critic/agent-card.md`
for the scoring rubric.

### critic-a
- Spawn: `Agent(tool=Agent, run_in_background=true)` — fires and waits for SendMessage callback
- Prompt: see agent-card.md

```
Rate ONE skill — [skill] — using its current description.

Extract description with:
```python
import yaml
from pathlib import Path
content = Path('~/.claude/skills/[skill]/SKILL.md').expanduser().read_text()
fm = yaml.safe_load('---\n' + content.split('---', 2)[1])
desc = fm['description']
```

**Dimension 1 — Capability (C):** How well does the description convey purpose, triggers, capabilities?
100 = instantly actionable to any agent.

**Dimension 2 — Likelihood to Pick Up (L):** How likely to invoke this skill based on
description alone? 100 = irresistible and obvious.

**Gate:** avg ≥ 80 AND at least one score ≥ 85 AND no score < 70.

Write result to /tmp/[skill]-critic-a.json:
```json
{"skill":"[skill]","critic":"critic-a","capability":N,"likelihood":N,"avg":N,"gate":"PASS|FAIL","notes":"...","timestamp":"[ISO8601]"}
```

Read memory/agents/critic/agent-card.md for full rubric before rating.
```

### critic-b
- Same as critic-a but write to `/tmp/[skill]-critic-b.json`, `critic: "critic-b"`

**Both critics fire simultaneously.** Wait for both SendMessage callbacks before proceeding to Step 3.
If a critic fails to respond within 5 minutes, retry it once. If it still fails, proceed with
`capability: null, likelihood: null, avg: null, gate: "ERROR"` — don't block the pipeline.

---

## Step 3: Collect and Combine Results

Read both JSON files:
```python
import json
critic_a = json.loads(Path("/tmp/[skill]-critic-a.json").read_text())
critic_b = json.loads(Path("/tmp/[skill]-critic-b.json").read_text())
```

### Compute gate conditions

```python
all_scores = [
    critic_a["capability"], critic_a["likelihood"],
    critic_b["capability"], critic_b["likelihood"]
]

avg_ge_80  = (critic_a["avg"] + critic_b["avg"]) / 2 >= 80
one_ge_85  = any(s >= 85 for s in all_scores if s is not None)
none_lt_70 = all(s >= 70 for s in all_scores if s is not None)
gate_met   = avg_ge_80 and one_ge_85 and none_lt_70

# Discrepancy: critics disagree by >20 points on average
critic_avg_gap = abs(critic_a["avg"] - critic_b["avg"])
discrepancy_flag = critic_avg_gap > 20
```

### Write immediate JSON
Write to `results/[skill]-critic-a.json` and `results/[skill]-critic-b.json`
(absolute paths from current dir). Write BEFORE applying gate — survives compaction.

---

## Step 4: Apply Gate — Pass Path

If `gate_met == true`:
1. Write `results/[skill]-quality-results.json` with gate_met=true, round=1, rewrite_performed=false, registration_status="registered"
2. Return the summary table (Step 6)

---

## Step 5: Apply Gate — Fail Path (One Rewrite Cycle)

If `gate_met == false`, rewrite the description automatically:

### 5a. Rewrite the Description

Write a new description that:
1. **Opens with user value** — what does the user gain? Not the mechanism.
2. **Lists 5–7 concrete trigger scenarios** — phrases a user would actually say
3. **Names key capabilities** — specific workflows, commands, platforms, frameworks
4. **Includes "Also for..."** coverage — adjacent use cases
5. **Differentiates from adjacent skills** — add "Compare with [skill-x]" if relevant
6. **Length: 600–1,000 chars** (hard cap: 1,536; minimum: 300)

### 5b. Write the Rewritten SKILL.md

```python
import yaml, json
from pathlib import Path

skill_path = Path(f"~/.claude/skills/[skill]/SKILL.md").expanduser()
content = skill_path.read_text()
fm = yaml.safe_load('---\n' + content.split('---', 2)[1])
fm['description'] = rewritten_description

# Re-serialize to YAML preserving the ---
out_lines = ["---"]
out_lines.append(yaml.safe_dump(fm, default_flow_style=False, sort_keys=False).rstrip())
out_lines.append("---")
skill_path.write_text('\n'.join(out_lines) + '\n')
```

Use `json.dumps(desc)` to safely write descriptions containing `:` — avoids folded-block colon parse errors.
Use `yaml.safe_load('---\n' + content.split('---', 2)[1])` for extraction.

### 5c. Re-rate (One More Round)

Spawn critic-a and critic-b again on the rewritten description — same prompt as Step 2,
but the description now comes from the just-rewritten SKILL.md.

Apply gate again. If still FAIL after rewrite, `registration_status = "flagged"`.

**One rewrite cycle only.** Do not loop. If it fails after rewrite, flag it and proceed.

### 5d. Write Final Quality Gate JSON

Write `results/[skill]-quality-results.json`:
```json
{
  "skill": "[skill]",
  "round": 2,
  "critic_a": {"capability": N, "likelihood": N, "avg": N},
  "critic_b": {"capability": N, "likelihood": N, "avg": N},
  "combined_avg": N,
  "gate_met": true|false,
  "gate_conditions": {
    "avg_ge_80": bool,
    "one_ge_85": bool,
    "none_lt_70": bool
  },
  "rewrite_performed": true,
  "discrepancy_flag": bool,
  "registration_status": "registered|flagged",
  "timestamp": "[ISO8601]"
}
```

---

## Step 6: Output Summary Table

```
## Quality Gate Results — [skill]

| Critic   | Capability | Likelihood | Average | Gate |
|----------|-----------|------------|---------|------|
| critic-a | [C]        | [L]        | [avg]   | [PASS/FAIL] |
| critic-b | [C]        | [L]        | [avg]   | [PASS/FAIL] |
| **Combined** | —    | —          | **[avg]** | **[✅ PASS / ❌ FAIL]** |

Gate conditions: avg≥80 [✅/❌]  one≥85 [✅/❌]  none<70 [✅/❌]
[+ "⚠️ Discrepancy detected (critics differed by [N] pts)" if discrepancy_flag]

Registration: [registered / flagged / skipped]
Rewritten: [yes / no]

Results written to:
  results/[skill]-critic-a.json
  results/[skill]-critic-b.json
  results/[skill]-quality-results.json
```

---

## Key Rules

- **Always use yaml.safe_load extraction** — never regex, to handle folded blocks with `:`
- **Write results JSON BEFORE applying gate** — survives session compaction
- **One rewrite cycle max** — do not loop after failure
- **Self-referential: skill-quality evaluates itself** but never registers itself to catalog
- **Error-tolerant critics** — if a critic errors, proceed with null scores and flag for review
- **depth-1 spawns only** — critics are spawned directly from the calling session, not from subagents
