---
name: amend-skill
description: >
  Inspects a skill's SKILL.md and its observations/runs.md log, identifies failure patterns,
  and proposes a targeted amendment to improve the skill. Trigger on: "improve this skill",
  "fix this skill", "update this skill", "why does X keep failing", "this skill is wrong",
  "add this to the skill", or automatically when observations/<skill-name>/runs.md contains
  3 or more failure entries. Outputs the amendment as a diff the user can review before
  applying. Records the amendment rationale in observations/<skill-name>/runs.md after
  user confirmation.
license: MIT
compatibility: Designed for Claude Code. No external tools required.
metadata:
  category: meta
  version: "0.1"
  source: original
  source_types: original
---

# Amend Skill

## Purpose

Skills degrade over time as targets change, new bypass techniques emerge, and failure patterns accumulate. This skill closes the feedback loop: it reads execution history, identifies what is systematically failing, and proposes a minimal surgical amendment to the skill.

## Trigger Conditions

Activate this skill when:

- User says "improve this skill", "fix this skill", "update this skill", "amend this skill"
- User says "why does X keep failing" where X is a skill name
- User says "add this to the skill" after describing a new technique that worked
- `observations/<skill-name>/runs.md` contains 3 or more entries with `outcome: fail`

## Methodology

1. **Identify the target skill** — confirm the skill name with the user if ambiguous.
2. **Read the skill** — load `skills/<bucket>/<category>/<skill-name>/SKILL.md` in full.
3. **Read the observations** — load `observations/<skill-name>/runs.md`.
4. **Analyze failure patterns**:
   - Which steps consistently fail?
   - Which payloads are blocked or produce wrong output?
   - Which trigger conditions are missing or too broad?
   - Are there new bypass techniques that worked but aren't documented?
   - Is the output format causing downstream confusion?
5. **Formulate a single targeted amendment** — one focused change rather than a full rewrite. The amendment should be one of:
   - **Tighten trigger**: remove or refine a trigger condition that causes false activation
   - **Add missing condition**: add a step, payload, or bypass that is now needed
   - **Reorder steps**: move a high-value step earlier to avoid wasted time
   - **Fix payload**: update an outdated payload that no longer works
   - **Change output format**: restructure how the skill presents findings
6. **Output the amendment as a unified diff** — show old text and proposed new text side by side.
7. **Ask for confirmation** — do not apply until the user approves.
8. **Apply and record** — edit the SKILL.md, then append to `observations/<skill-name>/runs.md`:

```
---
date: YYYY-MM-DD
skill: <skill-name>
task: Amendment applied via amend-skill
outcome: amendment
what_worked: |
  <describe what the amendment changes and why>
what_failed: |
  <describe the failure pattern that motivated the amendment>
errors: |
  N/A
notes: |
  Amendment type: <tighten-trigger | add-condition | reorder-steps | fix-payload | change-output>
  Rationale: <one-sentence reason>
---
```

## Example Interaction

User: "why does sql-injection keep failing on this target?"

Process:
1. Read `skills/owasp-wstg/injection/sql-injection/SKILL.md`
2. Read `observations/sql-injection/runs.md` — finds 3 fail entries, all noting WAF blocking `'` and `--`
3. Analysis: Bypass section exists but WAF-specific encoding variants not prominent enough in step 2
4. Amendment: Move WAF bypass step earlier in Methodology, add a WAF detection pre-step

Output:
```diff
-2. Submit `'`, `"`, `;`, `--`, `/* */` individually and observe response differences.
-3. Confirm with boolean pair: append `AND 1=1--` (true) vs `AND 1=2--` (false).
+2. Check for WAF: submit `'` and observe whether the response is a WAF block page (uniform
+   error regardless of input) vs. a database error (input-specific). If WAF present, use
+   encoding variants from the Bypass Techniques section before confirming injection.
+3. Submit `'`, `"`, `;`, `--`, `/* */` individually. If WAF present, substitute with
+   `%27`, `%2D%2D`, and comment fragmentation `UN/**/ION`.
+4. Confirm with boolean pair: `AND 1=1--` vs `AND 1=2--`.
```

## Fix Patterns

This is a meta-skill — it has no fix patterns of its own. Its output is an amendment to another skill's fix patterns.
