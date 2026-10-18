---
name: Diagnose
description: When something feels off, type /diagnose and describe the symptom. The skill walks the seven-layer stack (kernel, skills, hooks, daemons, vault, doctrine, principal config) and reports which layer is most likely responsible. Caddy pattern applied to debugging.
---

# Diagnose

Most failures in an aigent-OS install aren't bugs in any single component — they're integration failures across layers. `/diagnose` walks the stack with you so you don't have to.

## When to use

- "It used to work, now it doesn't"
- Caddy isn't surfacing a skill you expect
- `/open` produces incomplete context
- Hooks not firing
- Wikilinks not resolving
- AI behavior changed unexpectedly after an update
- Anything you can't immediately attribute to a single component

## How to execute

### Step 1 — Capture the symptom

Ask the user (or read from their prompt):
- **What were you trying to do?**
- **What happened instead?**
- **What did you expect?**
- **What changed recently?** (git pull, new skill installed, hook edit, kernel update)

Frame the symptom in one sentence. Example: *"Caddy used to surface /channel-audit when I asked about YouTube performance, now it doesn't."*

### Step 2 — Walk the seven-layer stack

For each layer, ask: could this layer be responsible for the symptom? If yes, run the specific check. If no, move on.

```
LAYER 7 — Principal Configuration
   - system/00_identity.md customized?
   - system/14_decision_framework.md reflects current priorities?
   - vault/projects/ and vault/people/ populated?
   Check first if symptom involves AI giving wrong context or missing your situation.

LAYER 6 — Doctrine (vault/concepts/)
   - Has a relevant doctrine note been edited recently?
   - Are there standing rules that should be firing but aren't?
   Check if symptom is about AI behavior changing without you having edited the kernel.

LAYER 5 — Vault Content
   - Wikilinks resolve? (run /system-check Tier 4)
   - Heat index up to date?
   - Memory layer current?
   Check if symptom is "AI doesn't know about X" or "/open missed Y."

LAYER 4 — Daemons
   - Heat compute daemon ran recently?
   - Semantic search index fresh?
   - Caddy reindex daemon firing?
   Check if symptom is "skills not surfacing" or "search results stale."

LAYER 3 — Hooks
   - Settings.json wired?
   - Hook scripts executable?
   - Hook output going where you expect?
   Check if symptom is "automated behavior stopped."

LAYER 2 — Skills
   - skill-index.json valid?
   - Trigger keywords match the user's actual phrasing? (run /skill-audit Section 3)
   - Skill descriptions match what the skill does?
   - Caddy fired correctly? Run /caddy-explain on the recent prompt to see the deterministic scoring.
   - Caddy index drift? Run /caddy-audit to see if any indexed skills are missing from disk or vice versa.
   Check if symptom is "wrong skill firing" or "no skill firing."

LAYER 1 — Kernel
   - All 15 system docs present and unmodified?
   - CLAUDE.md loaded?
   - Authority matrix consistent with what you've authorized?
   Check last — kernel issues are rare but high-blast-radius.
```

### Step 3 — Form a hypothesis

State the most likely layer + the specific issue. Example:
*"Hypothesis: Layer 2 (Skills) — the trigger keywords for /channel-audit don't match the phrasing you've started using. /skill-audit Section 3 will confirm."*

### Step 4 — Verify with one targeted check

Run the specific check that confirms or refutes. Don't fix yet — verify the diagnosis first.

### Step 5 — Recommend a fix

Concrete steps. Not advice ("you should…") — commands ("run /skill-audit then add 'performance check' to .claude/skill-index.json line 47").

## Output format

```
🩺 aigent-OS Diagnose

SYMPTOM
   {one-sentence framing}

WHAT CHANGED RECENTLY
   {if known}

LAYER WALK
   ✅ L7 Principal Config — OK
   ✅ L6 Doctrine — OK
   ✅ L5 Vault — OK
   ✅ L4 Daemons — OK
   ✅ L3 Hooks — OK
   ⚠️ L2 Skills — POSSIBLE CAUSE
   ✅ L1 Kernel — OK

HYPOTHESIS
   Layer 2 (Skills): trigger keywords for /channel-audit drift from current
   phrasing. Confirmed by /skill-audit Section 3.

FIX
   1. Add "performance check" and "review channels" to /channel-audit triggers
      in .claude/skill-index.json
   2. Save and re-test the failing prompt
   3. If still broken, escalate to L3 (Hooks) — Caddy hook may not be firing
```

## Step 6 — Write the outcome to the failure modes corpus (v0.2.2+)

When the diagnosis is verified (the layer + symptom matched the actual cause and the fix worked), append to `vault/memory/FAILURE_MODES.md`:

```markdown
## YYYY-MM-DD — {short symptom name}

**Symptom (verbatim from principal):** "{their own words}"
**Layer responsible:** L{N} ({layer name})
**Specific cause:** {file/line/config that was the actual issue}
**Fix applied:** {what the principal or agent did}
**Time to diagnose:** {minutes from /diagnose start to verified cause}
**Pattern (one line):** {what category of failure this was}
```

Why: a single failure is data; recurring failures are doctrine. The corpus enables Phase 2 promotion of patterns that occur 3+ times to [[Common Failure Modes]] permanent doctrine. Without the corpus, the framework can't harden against the failures it's actually had.

Skip this step if the diagnosis didn't verify — only confirmed causes get written. Hypotheses that didn't pan out aren't useful corpus data.

## Why this skill exists

Without `/diagnose`, a user with a broken install has to either dive into the source or give up. The seven-layer model gives them a structured path through the stack — even if they don't fix it themselves, they end up with a precise enough diagnosis to file a useful issue or ask a useful question.

Over time, the corpus this skill builds turns one-off diagnostics into framework hardening — the failure modes the framework has actually hit become the failure modes future principals can recognize in 30 seconds instead of 30 minutes.

## Anti-patterns this prevents

- "Something's broken" → maintainer asks 5 follow-up questions to figure out what
- User fixes the wrong layer (e.g., editing the kernel when the skill was the issue)
- Frustration from intermittent failures with no obvious cause
- Issues filed without enough information to action

## Connects to

- [`/system-check`](../system-check/SKILL.md) — verifies install integrity
- [`/skill-audit`](../skill-audit/SKILL.md) — checks skill catalog hygiene (Layer 2 deep-dive)
