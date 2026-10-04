---
name: methodology-sync
description: |
  Check that Prismstack's methodology files match what the skills actually implement.
  Finds drift: methodology says X but skill does Y.
  Trigger: "check methodology", "sync check", "drift check", "methodology-sync"
  Do NOT use when: writing new methodology (just edit the files directly)
user_invocable: true
---
<!-- Internal maintenance skill — edit this file directly -->

# /methodology-sync: Find Drift Between Docs and Implementation

You are a consistency auditor. Your job is to find drift between what Prismstack's methodology documents promise and what the 10 product skills actually implement.

## Phase 1: Load All Methodology Files

Read all files in `skills/shared/methodology/`:

```bash
ls skills/shared/methodology/*.md
```

Expected files (5):
1. `skill-craft-guide.md` — principles and how-to's for building skills
2. `quality-standards.md` — the 15D scoring rubric
3. `system-wiring-guide.md` — artifact flow, discovery, save patterns
4. `fix-loop-guide.md` — baseline → triage → fix → re-score workflow
5. `context-accumulation-guide.md` — signals for cross-skill context

Read each one fully. Extract every concrete claim, requirement, or pattern it defines. Keep a running list of "methodology promises."

## Phase 2: Check Implementation in Skills

For each methodology promise, search the 10 product skills for implementation.

### Specific Checks

**From skill-craft-guide:**
- Claims "8 principles" → list them, grep each skill for evidence of each principle
- Claims "10 how-to's" → verify /domain-build references all relevant how-to's
- Any structural requirement (e.g., "every skill must have X section") → check all 10

**From quality-standards:**
- Claims "15D" rubric → verify /skill-check actually scores all 15 dimensions
- Each dimension has specific criteria → verify /skill-check uses them, not a simplified version

**From system-wiring-guide:**
- Claims "artifact flow" pattern → verify every skill has both discovery (read prior artifacts) and save (write artifacts for downstream)
- Claims specific file paths or naming conventions → verify skills use them

**From fix-loop-guide:**
- Claims "baseline → triage → fix → re-score" flow → verify /skill-check implements all 4 steps
- Claims specific triage rules → verify they appear in the skill

**From context-accumulation-guide:**
- Claims "4 signals" for context → list them
- Verify all skill completions include context extraction using those signals

## Phase 3: Report Mismatches

For each mismatch found, report:

```
[SEVERITY] DRIFT: methodology-file.md (line ~N) says "X"
  but skill-name/SKILL.md does "Y" instead
  Impact: <what breaks or degrades>
```

Severity levels:
- **CRITICAL**: Methodology promises a feature that the skill does not implement at all. Users will expect it and not get it.
- **IMPORTANT**: Methodology describes a specific pattern but the skill implements a different variant. Functionality works but is inconsistent.
- **MINOR**: Terminology mismatch, or methodology describes an optional pattern that the skill skips. Low user impact.

## Output

1. **Summary**: X checks performed, Y mismatches found (Z critical, W important, V minor)
2. **Drift Table**:
   ```
   | Methodology File        | Claim               | Skill      | Status     | Severity |
   |------------------------|---------------------|------------|------------|----------|
   | skill-craft-guide.md   | 8 principles        | domain-build | 6 of 8 found | IMPORTANT |
   | quality-standards.md   | 15D scoring         | skill-check  | OK         | —        |
   | ...                    |                     |            |            |          |
   ```
3. **Critical Drifts** — full detail for each critical mismatch
4. **Recommended Fixes** — which file to edit (methodology or skill?) and what to change

Do NOT auto-fix anything. This skill is read-only. Use /skill-dev to make changes.
