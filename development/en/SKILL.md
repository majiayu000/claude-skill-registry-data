---
name: bugsweep
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-06-13
description: Systematic bug sweep with a codebase-scaled target value, doubling escalation, area tracking, and final verification. Use on /bugsweep or whenever the user requests a systematic bug pass.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="bugsweep banner">

> **English** — Official English version of `bugsweep`.


# /bugsweep — Systematic Bug-Sweep Workflow (English)

Iterative bug hunting with a converging stop criterion. Scales with the codebase, escalates when the search looks superficial, and prevents repetition through area tracking.

## 1. Compute the base rate

```
LOC = productive source lines (src/, lib/ — excluding tests, configs, docs, generated)
x = max(1, ceil(LOC / 1500))
base_rate = x * 3
```

| LOC | x | Base rate |
|-----|---|-----------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

Report to the user: "Codebase: {LOC} LOC → base rate = {base_rate} clean search passes."

## 2. Search loop

```
counter = 0
target = base_rate
any_bug_found = False
checked = []  # (area_name, type: code|task)

LOOP:
  area = pick_new_area()  # see area rules
  checked.append(area)

  Perform a thorough bug search

  IF bug found:
    any_bug_found = True
    Fix following bugfix-protocol (phases 4+5)
    Review: see model rule (newer model classes: no external review needed)
    Commit + push
    counter = 0  # RESET
  ELSE:
    counter += 1
    Report: "✓ Clean: {area} — {counter}/{target}"

  IF counter >= target:
    IF NOT any_bug_found:
      # Doubling escalation: not a single bug → search too shallow?
      target = base_rate * 2
      any_bug_found = True  # escalate only ONCE
      Report: "⚠ No bug in {base_rate} passes → target doubled to {target}."
      CONTINUE LOOP
    ELSE:
      GOTO final verification
```

### Practical notes on the search loop (learned from real sweeps)

- **Non-git repos:** Where there is no `git` (e.g. cloud-synced project folders), a **versioned backup** replaces "commit + push": create `file_<ts>.bak` before the first fix. **Caution — the pre-fix backup is NOT a backup of your work:** after the last fix, take a fresh `_FINAL_` backup, otherwise a sync hiccup can wipe the entire fix session.
- **Many bugs known up front:** If N bugs are already known at the start (e.g. from a previous run), "per bug: fix → review → commit → reset" is impractical. Process the known bugs as ONE fix block (joint review at the end) and start counting the base rate / search loop from the first NEWLY found bug. The reset logic still applies to bugs newly found during the sweep.
- **Same bug in multiple places:** A found defect (e.g. a wrong regex, a broken format assumption) is often copied elsewhere. After each fix, search for the same pattern in other locations — that is a worthwhile dedicated "area".

## 3. Area rules (anti-gaming)

An "area" is either a **code focus** or a **task** (purpose of the code).

### Code focus
- May be **extended** (more files) or **shifted** (different part) between passes
- Must NOT be exactly the same selection as in an earlier pass
- OK: pass 1 = `maintenance.py`, pass 5 = `maintenance.py + orchestrator.py` (extended)
- NOT OK: pass 1 = `maintenance.py`, pass 5 = `maintenance.py` (identical)

### Task (purpose)
- May be made **more granular** (check a subfunction) or **broader** (related functions together)
- Must NOT be exactly the same task
- OK: pass 1 = "thread safety in the watchdog", pass 5 = "thread safety across the whole tray" (broader)
- OK: pass 1 = "process detection", pass 5 = "store-marker matching inside process detection" (more granular)
- NOT OK: pass 1 = "thread safety in the watchdog", pass 5 = "thread safety in the watchdog" (identical)

### Naming
- The area MUST be named BEFORE the search (no retroactive assignment)
- Format: `"{name}" ({type}: code|task)`

## 4. Final verification

Once counter >= target AND any_bug_found:

**Step A — bugfix-protocol phase 5:**
- [ ] Full test suite green (`pytest`)
- [ ] **Actually execute the changed execution path at least once** — not just tests. Green unit tests on code that never calls the changed location are false safety. Run the actually changed path (dry run, smoke run, CLI invocation) and check for tracebacks / signature / naming errors. `py_compile` or a plain import only checks syntax — not whether the path runs.
- [ ] **Every fix has at least one test that touches it** — a fix without a test that actually triggers the changed branch counts as unverified (for orchestration/network paths, combine mock + dry run if needed).
- [ ] Type check (if configured)
- [ ] Lint (if configured)
- [ ] Edge cases of the session's fixes checked

**Step B — review (model rule):**
- **Newer model classes (e.g. Claude 5 / Fable class):** NO external advisor/second-model review required. Step A (tests + a real smoke run) is the verification. Optionally, on genuine uncertainty: a fresh review subagent — but verify its findings empirically (test against the unchanged code) before counting them as bugs. Background (sweep experience 2026-06-11): the second reviewer was unavailable, the substitute subagent delivered 1 finding (confidence 85) that a test proved to be a non-bug — an external review did not change the outcome.
- **Older models:** closing discussion with the advisor (fallback: a second model as reviewer); the advisor confirms or names gaps.

**If a bug is found during verification:**
→ Fix + test + commit
→ RESET: counter = 0, target = base_rate (fresh, NO doubling)
→ Back to the search loop (checked list persists, any_bug_found = True)

**If verification is clean:**
→ DONE. Commit + push. Print the protocol.

## 5. Protocol (at the end)

```markdown
## Bug Sweep Result

- **Codebase:** {LOC} LOC
- **Base rate:** {base_rate} (escalated: {target})
- **Areas checked:** {len(checked)}
- **Bugs found:** {count}
- **Resets:** {reset_count}
- **Doubling triggered:** yes/no
- **Fixes:**
  - {title} — {commit_hash}
  - ...
- **Final test suite:** {passed}/{total} green
- **Review verdict:** self-verification (newer model class) / advisor confirmed / gaps named
```

## When to use this workflow

- After feature development (quality assurance)
- Before a release (acceptance sweep)
- Periodically as a hygiene check
- When the user types `/bugsweep`

## Interaction with other skills

- **bugfix-protocol:** fix procedure (phases 4+5) for every found bug
- **systematic-debugging:** for hard-to-reproduce bugs within the sweep
- **code-review:** can be used as a task area

---

## Changelog

### 1.1.0 (2026-06-13)
- Backported the model rule for step B (from the local skill installation, state 2026-06-11): newer model classes self-verify via tests + a real smoke run, no external review needed; protocol field "Review verdict" extended accordingly

### 1.0.0 (2026-06-13)
- First publication in the skill library (adopted from local skill installation, state 2026-06-01)
