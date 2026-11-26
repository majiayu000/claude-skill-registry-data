---
name: auto-evolver
description: Use when evolving the skill library from repeated usage patterns — mining successful fixes, recurring failures, and refactor patterns from agent sessions, then promoting them into new or upgraded skills so the library becomes more efficient the more it is used.
domain: core
subdomain: meta-skills
category: core
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- auto-evolve
- continuous-learning
- skill-evolution
- pattern-extraction
- self-improvement
triggers:
- auto evolve
- evolve skills
- learn from usage
- promote pattern
- skill evolution
- mine patterns
argument-hint: "[session-log | skill-name]"
---

# Auto-Evolver

## Overview

Auto-Evolver turns usage into capability. It mines agent session history, failure receipts, and repeated fix patterns, then promotes them into new skills or upgrades existing ones. The loop:

1. **Observe**: Track which skills are invoked, which queries miss, which fixes repeat across sessions.
2. **Extract**: Identify recurring patterns (the same bash recovery sequence, the same refactor applied 3+ times, the same diagnostic flow).
3. **Promote**: Draft a new SKILL.md (or extend an existing one) with the extracted pattern, triggers, and verification gates.
4. **Verify**: Run the full validation ladder before registering.

Paired with `auto-consolidator`: evolution adds skills, consolidation keeps the registry dense. Evolution without consolidation causes bloat; consolidation without evolution causes stagnation.

## When to Use

**Trigger phrases:**
- "auto evolve", "evolve skills", "learn from usage"
- "promote pattern", "skill evolution", "mine patterns"

Use directly when:
- The same manual fix/recovery sequence appears in 3+ sessions.
- A query repeatedly scores < 30 in skill-router and no import exists (gap signal).
- A skill's verification section accumulates recurring new failure modes (extend its Anti-Rationalization Table).
- User explicitly asks to capture a lesson as a reusable skill.

## When NOT to Use

- One-off failures with no recurrence evidence — log via `learn`, not a new skill.
- Patterns better served as a managed-skill update (small procedural tweak) than a full catalog skill.
- Speculative features with zero usage evidence (violates YAGNI).

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "This fix was quick, no need to capture it." | The third time you do it manually, it costs more than the 10 minutes to write the skill. |
| "I remember the pattern, that's enough." | Agent context does not survive compaction. Only skills and memory files persist. |
| "More skills means a stronger library." | Unverified, un-routed skills add noise. Evolution requires validation ladder + trigger registration or the new skill is invisible. |
| "Evolution can run fully automatic." | Skill promotion is a write to shared infrastructure. Require diff review before registering. |

## Workflow

### 1. Signal Sources (ranked by evidence strength)

| Signal | Source | Strength |
|---|---|---|
| Repeated fix in ≥3 sessions | `history://` transcripts, agent receipts | Strong — promote now |
| Query misses (score < 30) recurring | `skill_router.py` logs | Strong — gap exists, find or create |
| New failure mode on existing skill | Skill verification failures, user reports | Medium — extend skill |
| Single user "remember this" request | `learn` tool capture | Medium — managed skill first |
| Theoretical improvement | Brainstorm | Weak — backlog, do not implement |

### 2. Pattern Extraction

For each candidate pattern, capture:
- **Trigger**: what the user actually typed/said (verbatim phrases → `triggers:` frontmatter).
- **Sequence**: exact tool calls that resolved it (the workflow body).
- **Guardrails**: what failed when done wrong (→ Anti-Rationalization rows).
- **Proof**: the receipt that shows it worked (→ Verification checklist).

### 3. Promote

```bash
# create skill skeleton in the correct category
mkdir -p <category>/<new-skill>
# write SKILL.md with required sections:
# frontmatter (name, description "Use when...", domain, tags, triggers, version)
# ## When to Use, ## When NOT to Use, ## Anti-Rationalization Table,
# ## Workflow/Process, ## Verification
```

### 4. Validate & Register

```bash
python3 scripts/lint-skills.py --write   # indexes into SKILLS.json
python3 scripts/sync-counts.py
python3 scripts/check-broken-links.py
python3 scripts/validate-skills.py
python3 scripts/test-skills.py --quick
bash scripts/sync-skills.sh              # runtime mirror
```

### 5. Measure Evolution Impact

Track per skill: invocation count, success rate, post-promotion query score. Skills scoring consistently < 10 after 30 days are candidates for `auto-consolidator` demotion.

## Loop

```text
sessions → signals → extract → promote → validate → register
    ↑                                                    |
    └──────── auto-consolidator prunes bloat ←──────────┘
```

## Verification

- [ ] Pattern has recurrence evidence (≥3 sessions or explicit user request)
- [ ] Triggers copied from verbatim user phrases, not invented
- [ ] New skill passes full validation ladder before registration
- [ ] Existing skill extensions add to Anti-Rationalization Table + Verification, never rewrite wholesale
- [ ] No promotion from single-session evidence
- [ ] Post-registration router test: query scores ≥ 30 for the new skill