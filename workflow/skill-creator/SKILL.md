---
name: skill-creator
description: >
  Create new skills using the Skill Seekers CLI (github.com/yusufkaraaslan/
  Skill_Seekers), generating SKILL.md files from GitHub repos, documentation URLs,
  or a blank slate. Invoke with /skill-creator. When to trigger: when the user wants
  to create a new skill from scratch or from a GitHub repository; when a useful
  workflow should be captured as a reusable SKILL.md for future projects; when the
  user pastes a docs URL and asks to turn it into a skill; and when a one-off workflow
  has been run successfully and should be permanently codified. Key capabilities:
  five invocation modes (URL, scratch, enhance, preset, interactive), automatic
  dependency installation if Skill Seekers is missing, AI enhancement at levels 1-5
  (from light polish to expert-level depth), catalog registration with provenance
  tracking, and mandatory security quarantine for all AI-generated skill output.
  Presents an impact analysis before any pipeline step runs — user approval is the
  gate. Ideal for developers who want to capture institutional knowledge, automate
  recurring workflows, or build a personal skill library. Also useful for teams
  standardizing processes across projects and for onboarding new developers with
  context-rich, auto-documented skill commands.
---

# Skill Creator — Powered by Skill Seekers

Uses the [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) CLI to
generate, enhance, and install SKILL.md files. After initial analysis, an impact
report is presented for your approval before any pipeline steps run. Once
approved, execution continues automatically until the skill is fully installed
and registered.

---

## Skill Seekers CLI — Quick Reference

```bash
pip install skill-seekers        # one-time install

skill-seekers create [URL]      # create from GitHub repo or docs URL
skill-seekers package <dir> --target claude   # package for Claude
skill-seekers enhance <dir> --level [1-5]    # AI enhancement
skill-seekers install-agent ~/.claude/skills/[name]   # install to library
```

**Enhancement levels:** 1=light polish, 2=standard (default), 3=deep, 4=comprehensive, 5=expert
**Enhancement modes:** `--mode api` (Claude API) or `--mode local` (claude CLI, free)

---

## Step 0: Ensure Skill Seekers Is Installed

```bash
which skill-seekers || pip3 show skill-seekers
```

If not present, install it automatically:
```bash
pip3 install skill-seekers
```

---

## Step 1: Parse Intent and Detect Mode

| Signal | Mode |
|---|---|
| `/skill-creator [URL]` | **URL mode** — create from GitHub repo or docs page |
| `/skill-creator --name [name]` | **Scratch mode** — scaffold from spec |
| `/skill-creator enhance [skill]` | **Enhance mode** — upgrade an existing skill |
| `/skill-creator --preset [name]` | **Preset mode** — scaffold from framework preset |
| No flags given | **Interactive mode** — ask what to create |

**Flag: `--quality-gate off`** — bypasses the description quality gate (Step 6). Default: gate is on.
When `--quality-gate off` is passed, `quality_gate_passed: null` is recorded in the catalog and the quality report is skipped in the final output.

Ask clarifying questions only for genuinely ambiguous intent. Infer what you can.

---

## Step 2: Initial Analysis (No Execution Yet)

Before running anything, analyze the request and present:

```
## Initial Analysis

**Mode:** [URL / Scratch / Enhance / Preset / Interactive]
**Source:** [URL or "user specification"]
**Skill name:** [derived or specified]
**Target platform:** claude

**Skill Seekers will:**
1. Scrape/parse the source
2. Generate SKILL.md + references/ subdir
3. Package output for the Claude platform
4. Install to ~/.claude/skills/[name]/

**Parameters available:**
- Enhancement level: 1-5 (default: 2)
- Enhancement mode: api / local (default: api if ANTHROPIC_API_KEY set)
- Framework preset: [available presets]

Do you want to approve this, or adjust parameters first?
```

Wait for your approval or parameter modification before proceeding.

---

## Step 3: Impact Analysis (Approval Gate)

After your approval, present the full impact analysis:

```
## Impact Analysis

**Mode:** [URL / Scratch / Enhance / Preset]
**Source:** [URL or "user specification"]
**Skill name:** [name]
**Target platform:** claude
**Framework preset:** [name or "standard"]
**Enhancement level:** [1-5]
**Enhancement mode:** [api | local]

**What will happen:**
1. skill-seekers create → [source parsed]
2. SKILL.md output → ~/.claude/skills/[name]/SKILL.md
3. references/ subdir → ~/.claude/skills/[name]/references/
4. INDEX.catalog.json → entry added/updated (provenance: "skill-seekers", trust_level: "agent-authored")
5. _security/ → skill queued for trust review (agent-authored tier)
6. obsidian-vault → skill creation logged with metadata

**Existing skills affected:** [list only if enhance mode]
**Catalog entries added:** 1
**Files created:** [2-N depending on enhancement level]

Proceed? (yes / no / modify parameters)
```

**Continue until the pipeline is done after you approve.** Do not stop mid-pipeline.

---

## Step 4: Run Skill Seekers

### URL Mode
```bash
skill-seekers create "[URL]"
skill-seekers package output/$(basename "$(pwd)") --target claude
```

### Scratch Mode
```bash
skill-seekers create \
  --name "[name]" \
  --preset standard \
  --enhance-level [level]
```

### Enhance Mode
```bash
skill-seekers enhance ~/.claude/skills/[existing-skill] \
  --level [1-5] \
  --mode [api|local]
```

### Preset Mode
```bash
skill-seekers create \
  --name "[name]" \
  --preset "[preset-name].json"
```

Default enhancement level: 2. Default mode: api if `ANTHROPIC_API_KEY` is set, local otherwise.

---

## Step 5: Install to Skills Library

```bash
skill-seekers install-agent [output-dir]
```

Falls back if `install-agent` is unavailable:
```bash
mkdir -p ~/.claude/skills/[name]
cp -r [output-dir]/* ~/.claude/skills/[name]/
```

---

## Step 6: Quality Gate — Rate Description Quality

**Skip this step if `--quality-gate off` was passed in Step 1.**

Run `/skill-quality [name]`. This:
1. Spawns two independent critics (Capability + Likelihood to Pick Up, 0–100 each)
2. Applies the calibrated gate: avg ≥ 80 AND at least one ≥ 85 AND no score < 70
3. On FAIL: rewrites the description automatically, then re-rates once
4. Writes results to `skill-quality/results/[name]-quality-results.json`
5. Returns a summary table

Collect the quality gate result. It tells you:
- `registration_status`: `"registered"` (PASS) or `"flagged"` (failed after rewrite)

---

## Step 7: Register to INDEX.catalog.json

Run the catalog update script:
```bash
bun ~/.claude/skills/scripts/update-catalog-from-skillseekers.ts ~/.claude/skills/[name]
```

Manual fallback — append to `INDEX.catalog.json` skills array:
```json
{
  "name": "[name]",
  "path": "skills/[name]/SKILL.md",
  "scope": "global",
  "dept": ["all"],
  "team": "-",
  "priority": "implementation",
  "triggers": ["[name]"],
  "aliases": [],
  "description": "[from SKILL.md frontmatter]",
  "last_updated": "[YYYY-MM-DD]",
  "trust_level": "agent-authored",
  "author": "skill-seekers",
  "provenance": "skill-seekers",
  "quality_gate_passed": [true | false | null]
}
```

Note: `quality_gate_passed` is set to the result from Step 6 — `true` for PASS, `false` for flagged, `null` if `--quality-gate off` was used.

Also append a row to `INDEX.md` table.

---

## Step 8: Security Gate — Quarantine Notification

Skill Seekers output is AI-enhanced (`trust_level: agent-authored`). Report:

```
⚠️ Trust review required: [name] generated by Skill Seekers.
Placed in _security/quarantine/. Human review needed before live use.
Run /cso to initiate security review.
```

Do not mark the skill live until the `_security/` review completes.

---

## Step 9: Obsidian Vault Logging

After successful installation, log to obsidian-vault:

```
## Skill Created: [name]
- **Date:** [YYYY-MM-DD]
- **Tool:** Skill Seekers CLI
- **Enhancement level:** [1-5]
- **Target platform:** claude
- **Framework preset:** [preset or "default"]
- **Enhancement mode:** [api | local]
- **Provenance:** skill-seekers
- **Trust level:** agent-authored (pending review)
- **Quality gate:** [PASS (C=N L=N avg=N) | FAIL flagged (C=N L=N avg=N) | skipped]
```

---

## Step 10: Report to User

**If `--quality-gate off` was used**, report:
```
Skill creation complete. Quality gate bypassed (--quality-gate off).

~/.claude/skills/[name]/
  SKILL.md
  references/

INDEX.catalog.json — entry added (quality_gate_passed: null)
INDEX.md — row appended
_obsidian-vault/Skills/[name].md — logged
_quarantine/ — pending trust review

This skill is AI-enhanced. Human trust review required before live use.
Quality gate was skipped — use /skill-quality [name] to audit description quality.
```

**Otherwise**, include the quality gate result from Step 6:
```
Skill creation complete.

~/.claude/skills/[name]/
  SKILL.md
  references/

INDEX.catalog.json — entry added (quality_gate_passed: [true | false])
INDEX.md — row appended
_obsidian-vault/Skills/[name].md — logged
_quarantine/ — pending trust review
skill-quality/results/[name]-quality-results.json — written

## Quality Gate Summary
| Critic   | Capability | Likelihood | Average | Gate |
|----------|-----------|------------|---------|------|
| critic-a | [C]        | [L]        | [avg]   | [PASS/FAIL] |
| critic-b | [C]        | [L]        | [avg]   | [PASS/FAIL] |
| **Combined** | —    | —          | **[avg]** | **[✅ PASS / ❌ FAIL]** |

[If flagged:] ⚠️ Description was auto-rewritten. Run /skill-creator enhance [name] --level 4 for deeper improvement.
[If discrepancy:] ⚠️ Critics disagreed by >20 pts — see results JSON for details.
```

---

## Common Rationalizations (Anti-Rationalization Table)

Every SKILL.md template should include a "Common Rationalizations" section. This is a first-class part of the skill definition — not an afterthought. Include it between the process steps and the Red Flags section.

**Why it matters:** Agents (and humans) rationalize skipping skills under pressure. Naming the rationalizations explicitly prevents them from succeeding silently.

**Format:**

```markdown
## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This task is too small for this skill" | [counter-argument] |
| "I'll skip this step just this once" | [what that actually costs] |
| "We don't have time for this" | [what the time actually buys] |
| "[specific domain rationalization]" | [specific counter] |
```

**Rules for the table:**
- 4–8 rows (not fewer than 4; more than 8 dilutes signal)
- Every rationalization must be a phrase someone would actually say or think — not abstract
- Every reality must be concrete: name the cost, the failure mode, or the specific thing that goes wrong
- Include at least one domain-specific rationalization (not just generic ones)
- Write rationalizations as quotes — they sound like something a developer says

When creating or enhancing a skill, if the input skill lacks a Common Rationalizations section, add one as part of the AI enhancement pass (level 2+).

---

## Simplify-Ignore Pattern (Locked-Section Protection)

When a skill or document contains sections that must not be modified by agents or automated tools — architecture contracts, no-touch zones, signed-off decisions — use the simplify-ignore pattern to protect them.

The pattern: mark locked sections with a content-hash placeholder so automated tools skip them while humans can still read the original content.

**When to apply this pattern in skill context:**
- A SKILL.md contains an "Integration Contracts" or "No-Touch Zones" section that Coords must not modify
- A project memory file contains a decision that is "locked" per decisions.md
- A configuration section is under change control

**Implementation approach (instruction-level, no hook required):**
Add this to the "Key Rules" section of any skill whose output includes locked content:

```
**Locked-section rule:** If this skill's output includes sections marked `<!-- LOCKED: [reason] -->`,
treat those sections as read-only. Do not modify, reformat, or simplify content between
`<!-- LOCKED-START -->` and `<!-- LOCKED-END -->` markers. Surface locked section presence to the
user before making any edits that could affect surrounding content.
```

**Do NOT implement this as a hook.** Hook implementation requires infrastructure management. Use HTML comment markers + instruction-level guidance in the skill that produces the output.

---

## Skill Learnings Convention

Every new skill should support the **staging → distill → promote** feedback model:

1. **Stage**: After invocation, if the user gives explicit feedback (positive or negative), append a timestamped entry to `{skill}/learnings-raw.md`. This file is never loaded into context — it's the raw archive.
2. **Distill**: After 10+ raw entries accumulate, distill into `{skill}/learnings.md` (max 20 lines of principles). This replaces the previous digest. `learnings.md` IS loaded at invocation start if it exists.
3. **Promote**: If a principle is universally true and stable, bake it into SKILL.md directly and remove from `learnings.md`.

When generating a new skill, include in the SKILL.md:
- A step near the start: "If `learnings.md` exists in this skill's directory, read it before proceeding."
- A step at the end: "If the user provides feedback on this run, append a `- {YYYY-MM-DD}: {insight}` line to `learnings-raw.md`."

---

## Key Rules

- **Always present impact analysis before executing** — your approval is the gate
- **Continue until pipeline is done after approval** — no stopping mid-execution
- **Install skill-seekers if missing** — handle automatically, don't ask
- **Register to catalog** — never create a skill without updating INDEX.catalog.json
- **Log to obsidian-vault** — skill creations are long-term memory events
- **Trust level is agent-authored** — Skill Seekers output triggers quarantine
