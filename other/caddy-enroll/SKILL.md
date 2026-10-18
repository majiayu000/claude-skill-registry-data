---
name: caddy-enroll
description: Enroll a skill into Caddy's index so it can be surfaced when the right prompt arrives. Use when a new skill is created, copied in, or when a skill needs updated triggers. Usage — "/caddy-enroll <path to SKILL.md>".
user-invocable: true
---

# /caddy-enroll

Enroll a skill into Caddy's `skill-index.json` so prompts matching the skill's triggers surface it as a hint.

## When to Use

- A new skill was created (often by `/skills-builder`) and needs to join the index
- A skill was copied in from outside (cloned plugin, downloaded skill)
- An existing skill's triggers need refreshing after its SKILL.md changed
- User says "enroll this skill" / "add this to Caddy" / "update Caddy for /X"

## When NOT to Use

- The skill is already indexed with correct triggers (check `.claude/skill-index.json` first)
- The skill has no SKILL.md / no description / no clear use case (fix the skill first, enroll after)

## Arguments

`$1` = path to the skill's SKILL.md or .md file. If omitted, ask which skill.

## Protocol

### Step 1: Read the target skill

Read the full SKILL.md at the given path. Parse:
- **name** — from the `name:` frontmatter field, or the filename stem
- **description** — from the `description:` frontmatter field, or first heading/line

### Step 2: Extract structured metadata

Produce this five-field structure:

```
- what: <one-line what it does>
- triggers: <comma-separated keywords/intents a prompt matcher could catch — 6-12 items, mix multi-word phrases and single keywords>
- use_cases: <3-5 concrete "when user says X, use this">
- anti_cases: <1-3 "do NOT use when...">
- related: <comma-separated related skills from the existing index>
```

**Trigger quality rules:**
- Multi-word phrases score 3x — prefer them for specific intents
- Single words only for unambiguous terms
- Avoid stopwords and generic terms ("help", "check", "run", "fix" alone)
- Aim for prompts a user would actually type — not jargon from the skill's own docs

**Anti-case quality:**
- Name the sibling skill that SHOULD be used instead
- Name any confidentiality or scope boundaries

### Step 3: Append to skill-index.json

Read `.claude/skill-index.json` (relative to AIGENT_ROOT).

If a skill with this `name` already exists: update its `triggers` and `why` — don't clobber triggers the user added manually.

If it's new: append a new entry with `{name, triggers, why}`.

Validate the file is still valid JSON before writing.

### Step 4: Test the enrollment

Run:
```bash
echo '{"prompt":"<test prompt that should trigger this skill>"}' | bash $AIGENT_ROOT/daemons/caddy.sh
```

Confirm the `[CADDY] /<name> - <why>` hint surfaces. If not, tune the triggers and retry.

### Step 5: Confirm

Report:
- Skill name and path
- Trigger count + short list
- Test prompt used + whether it surfaced

## Output Format

```
Enrolled: /<skill-name>
Triggers: <count> (<short list>)
Test: "<prompt>" → [CADDY] /<name> ✓
```

If the test failed or triggers need work:
```
Enrolled with warning: triggers need tuning
Test: "<prompt>" → no match
Suggested fix: add trigger "<candidate>"
```

## Why This Exists

Every skill the framework can execute must be enrolled here. Skipping enrollment = skill sits in the golf bag unlabeled. Caddy can't hand it to the AIgent if it's not indexed.
