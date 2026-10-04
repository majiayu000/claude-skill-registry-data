---
name: vibe-fix-bug
description: >
  Full spec-driven workflow for diagnosing and fixing a bug with an AI coding agent.
  Triggers on "bug:" prefix, "I have a bug", "something is broken", "this is not working",
  "fix this issue", "there is a bug in", "debug this", "broken", "issue".
  Always use when the user reports unexpected behaviour — even without the exact prefix.
  Three-way severity triage: trivial bugs (3 tasks, no folder), environment bugs
  (runs vibe-doctor first, no BUG_SPEC), significant bugs (full workflow).
  Environment bugs — HMR loops, missing deps, config mismatches, build tool failures —
  are detected at triage and routed to vibe-doctor rather than full bug workflow.
  Diagnosis always before the fix. Regression test always before fix code.
  BUG_SPEC.md, BUG_PLAN.md, BUG_TASKS.md created for significant bugs only.
---

# Vibe Fix Bug Skill

Spec-driven bug diagnosis and surgical fixing.
Diagnosis before fix. Regression test before fix code. Smallest possible change.

**Use Plan Mode (Shift+Tab) for Steps 1–5. Exit before Step 6.**

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

---

## The O'Reilly principles this enforces

**Spec before code** — root cause confirmed and fix plan approved before any code changes.
**Context preservation** — CODEBASE.md read first, ARCHITECTURE.md patterns followed.
**Incremental verifiable progress** — regression test first, fix second, verify third.
**Drift prevention** — DECISIONS.md updated, ARCHITECTURE.md updated if fix reveals new pattern.

---

## Two audiences. Two file types.

**Human-facing:**
- `vibe/TASKS.md` — plain English, updated after every task

**Agent-facing (human never opens these):**
- `vibe/bugs/[date-slug]/BUG_SPEC.md` · `BUG_PLAN.md` · `BUG_TASKS.md`
- `vibe/CODEBASE.md` · `vibe/ARCHITECTURE.md` · `vibe/DECISIONS.md`

---

## Step 1 — Gather the bug report and triage severity

Extract or ask for:
- **What's happening** — the symptom
- **What should happen** — expected behaviour
- **Steps to reproduce** — how to trigger it
- **Frequency** — always / sometimes / only under X
- **Errors or logs** — any messages or stack traces

**Triage — three paths:**

**Environment bug** — route to vibe-doctor, NOT the bug workflow:

Check for these signals first:
- App won't start / server fails to launch
- WebSocket/HMR connection errors
- `Cannot find module`, `MODULE_NOT_FOUND`
- Tailwind classes not applying / CSS not loading
- `husky: command not found` or git hook failures
- Environment variable `undefined` at startup
- `.git` operation failures or submodule errors
- Build tool errors (Vite, Webpack, tsc) that aren't TypeScript type errors

Weigh the evidence — some single signals are conclusive on their own ("app
won't start" with a config/build error), while several weak signals may still be
a code bug. If the evidence points to the environment rather than application
code, treat it as an environment bug (state your confidence briefly):
> "This looks like an environment issue, not a code bug. Running doctor: to diagnose..."

Invoke `vibe-doctor`. After doctor: completes:
- If doctor fixed it and app starts → close, no bug folder created
- If doctor fixed env but code bug remains → continue to Trivial or Significant path
- If doctor can't fix → surface doctor's "NEEDS ATTENTION" items to user

**Trivial bug** — you're confident it's genuinely small. The signals below all
point that way; treat them as a confidence judgment, not a rigid all-must-be-true
gate (a clearly 1-line fix with mild uncertainty is still trivial):
- Root cause obvious from description (typo, missing CSS class, obvious off-by-one)
- Fix touches 1-2 lines in 1 file
- No regression risk in other features
- No architectural implication
- NOT an environment issue (handled above)

State your read briefly ("confident this is a 1-line trivial fix") and, if the
confidence is genuinely borderline, treat it as Significant instead.

→ "This is a quick fix. Regression test, fix, verify — 3 tasks, no spec folder needed."
→ Jump to **Trivial path** below.

**Significant bug** — root cause unclear, multiple files, regression risk, or architectural implication.
→ "This needs full diagnosis. Let me read the codebase."
→ Continue to Step 2.

---

## Trivial path

Insert into TASKS.md directly — no bug folder created:

```
🐛 [Bug summary — plain English] (0/3)
   [ ] BUG-001 · Regression test — write test that fails on current code
   [ ] BUG-002 · Apply fix — [one line: exactly what changes]
   [ ] BUG-003 · Verify — regression test passes, full suite green, linter clean
   → Trivial fix — no spec folder
```

Update "What just happened" and "What's next":
```
## What just happened
🐛 Bug found: [plain English description]
Quick fix path — regression test first.

## What's next
⬜ BUG-001 · Write a test that reproduces the bug
Say "next" to begin.
```

In autonomous mode (`vibe_state.py mode`), don't wait for "next": run the three BUG
tasks through vibe-mode's `references/AUTONOMOUS_EXECUTION_BLOCK.md` (regression test
first), then announce the fix complete.

After BUG-003, collapse to: `✅ [Bug summary] — fixed [date] (3/3 ✅)`

**CLAUDE.md:** No active bug section needed for trivial fixes — complexity doesn't warrant it.

**DECISIONS.md:** Append a brief entry:
```
---
### D-[ID] — Trivial fix: [bug summary]
- **Date**: [date] · **Type**: drift (trivial bug)
- **Root cause**: [one sentence]
- **Fix**: [one sentence — what changed and in which file]
- **Regression test**: [test name]
- **Approved by**: human
---
```

---

## Step 2 — Read vibe/CODEBASE.md (significant bugs only)

If vibe/CODEBASE.md exists:
Read fully. Use section 9 (key file paths) and section 5 (API routes) to pinpoint where to look.
If significantly out of date, note this to the user.

If vibe/CODEBASE.md does not exist:
Read `references/CODEBASE_MD.md` for the generation template.
Explore codebase focused on the bug area first — don't let CODEBASE.md generation delay diagnosis.
Generate after the bug is understood.

Also read vibe/ARCHITECTURE.md — the fix must follow existing patterns.
Also read vibe/DESIGN_SYSTEM.md if the bug is in a styled component.

---

## Step 3 — Explore and diagnose (time-boxed)

> 🧠 **Effort:** root-cause diagnosis is where extended thinking pays off most —
> run this at high/xhigh effort with adaptive thinking. Prefer thinking harder
> over reading more files: the time-box below is a floor for *giving up on a
> hypothesis*, not a substitute for reasoning. Form and test hypotheses explicitly.

**Check for dependency graph first:**
```bash
ls vibe/graph/DEPENDENCY_GRAPH.json 2>/dev/null && echo "GRAPH EXISTS" || echo "NO GRAPH"
```

**If graph exists — query it for the suspected file:**
```
vibe-graph: query [suspected file from Step 2]
```

The graph returns the blast radius immediately — imports, imported_by,
test file, verifier, API routes, concept. Load only those files.
Do NOT load the full CODEBASE.md — the graph replaces that read.

Also query the concept:
```
vibe-graph: query [concept name from graph result]
```
This shows upstream/downstream concepts where the bug may originate or propagate.

**If no graph exists — fall back to CODEBASE.md:**
Using CODEBASE.md section 9 as your map, read relevant files.

**In both cases:**
- Read the blast radius files fully — do not skim
- Trace execution path from entry to failure
- Check recent git changes: `git log --oneline -20 -- <file>`
- Read relevant test files to understand expected behaviour

**Time-box:** If after reading 5 files the root cause is still unclear, stop.
Present findings and top 2 hypotheses to the user. Ask for additional context.
Don't explore indefinitely — surface uncertainty early.

**Don't let the first plausible cause win.** The first explanation that fits is
often not the real one, and committing to it early is how debugging sessions burn
an hour fixing a symptom. Before you settle:

1. **Enumerate 2–3 competing hypotheses**, not one. Write them down. ("A: the guard
   runs before state loads. B: the id is stale from cache. C: the API returns 200
   with an empty body.")
2. **For each, name the evidence that would confirm it AND the evidence that would
   kill it.** A hypothesis you cannot imagine disproving is a belief, not a diagnosis.
3. **Gather that evidence** — a log line, a value at a breakpoint, a failing
   assertion, a git blame — and **reject** hypotheses it rules out. Prefer the
   cheapest disproving test first.
4. Only when one hypothesis survives and the others are actively ruled out do you
   commit to the fix. If two survive, you don't understand it yet — get more evidence.

Reproduce the failure *before* the fix and confirm the fix *removes* that exact
reproduction — a bug you cannot reproduce is a bug you cannot prove you fixed.

Land on the surviving hypothesis. Point to the exact file, function, and line, and
state the one piece of evidence that confirmed it over the alternatives.

---

## Step 4 — Generate BUG_SPEC.md

Draft BUG_SPEC.md:
1. **Bug summary** — one sentence
2. **Files involved** — exact paths from CODEBASE.md section 9
3. **Root cause hypothesis** — specific theory with line-level detail
4. **Confidence level** — how confident? what would change your mind?
5. **Blast radius** — what else could be affected by this bug or the fix?
6. **Fix approach** — what should change and why
7. **What NOT to change** — leave alone to avoid regressions
8. **Verification plan** — exact steps to confirm fix worked
9. **Regression test** — what test would catch this if it reappeared

Present. Ask: "Does this diagnosis look right?"
Wait for confirmation. Save as `vibe/bugs/[date-slug]/BUG_SPEC.md`.

---

## Step 5 — Generate BUG_PLAN.md

Read BUG_SPEC.md, files involved, existing tests. Check ARCHITECTURE.md — fix must follow patterns.

Draft BUG_PLAN.md:
1. **Exact files to modify** — nothing outside this list
2. **Exact files NOT to touch** — explicit list
3. **Change description** — for each file: what changes, which line, why
4. **Conventions to follow** — from CODEBASE.md section 6 and ARCHITECTURE.md
5. **Side effects check** — what could break?
6. **Test plan** — regression test spec + existing tests that must still pass
7. **Rollback plan** — how to revert
8. **CODEBASE.md update needed?** — Yes (which sections) or No (state explicitly)
9. **ARCHITECTURE.md update needed?** — Yes if fix reveals a pattern to document / No

**Principle:** Smallest possible change. Never fix other bugs noticed — log them separately.

Present. Ask: "Does this fix plan look right?"
Wait for approval. Save as `vibe/bugs/[date-slug]/BUG_PLAN.md`.

---

## Step 6 — Update CLAUDE.md (project root)

Append bug fix section — do NOT overwrite:

```
---
### Active Bug Fix: [Bug summary]
> Folder: vibe/bugs/[date-slug]/ | Added: [date]

**Files in scope**: [only files from BUG_PLAN.md]
**Files out of scope**: [everything else]
**Design system**: [check vibe/DESIGN_SYSTEM.md if bug is in styled component]
**Scope changes**: If user says "change:" — stop and run vibe-change-spec.

**Boundaries:**
Always: write regression test BEFORE fix · run full suite after fix ·
        smallest change only · follow ARCHITECTURE.md patterns ·
        update CODEBASE.md if fix changes routes/schema/files/patterns ·
        update TASKS.md after every task in plain English
Ask first: touching any file not in BUG_PLAN.md · refactoring beyond minimal fix
Never: fix other bugs noticed · modify existing passing tests ·
       introduce new patterns · change unrelated code "while here"

**Done condition:**
- [ ] Regression test written and passing
- [ ] Full test suite green · Linter clean
- [ ] No files outside BUG_PLAN.md scope modified
- [ ] CODEBASE.md updated if fix changed structure
- [ ] ARCHITECTURE.md updated if fix revealed a pattern

**Session startup:** Read CLAUDE.md · CODEBASE.md · ARCHITECTURE.md · TASKS.md · BUG_SPEC.md · BUG_TASKS.md
**Between tasks:** "next" → re-read TASKS.md silently → state next task in plain English → confirm.
---
```

Save updated `CLAUDE.md`.

---

## Step 7 — Generate BUG_TASKS.md

Read BUG_SPEC.md, BUG_PLAN.md, CODEBASE.md.

```
---
### BUG-001 · Write the regression test
- **Status**: `[ ]` | **Depends on**: None | **Touches**: [test file path]

**What to do**: Write a test that reproduces the bug exactly.
Must FAIL on current code before the fix. Name it clearly.

**Acceptance criteria**:
- [ ] Test exists and clearly named
- [ ] Test FAILS on current unfixed code — verified
- [ ] Test isolates the exact failing behaviour

**⚠️ Boundaries**: Do not touch any non-test files in this task.
**Decisions**: > Filled in by agent. None yet.
---

### BUG-002 · Implement the fix
- **Status**: `[ ]` | **Depends on**: BUG-001 | **Touches**: [exact paths from BUG_PLAN.md]
- **CODEBASE.md update**: [Yes — which sections / No — logic only]

**What to do**: [Fix from BUG_PLAN.md — specific and precise]
Modify only files in BUG_PLAN.md. Follow ARCHITECTURE.md patterns.
If CODEBASE.md update required, do it before marking done.

**Acceptance criteria**:
- [ ] Only BUG_PLAN.md files modified
- [ ] Matches BUG_PLAN.md approach
- [ ] Follows existing patterns — no new patterns introduced without ARCHITECTURE.md update
- [ ] No other behaviour changed
- [ ] CODEBASE.md updated if structural change

**⚠️ Boundaries**: Ask first before files not in BUG_PLAN.md · never refactor unrelated code
**Decisions**: > Filled in by agent. None yet.
---

### BUG-003 · Verify fix and run full suite
- **Status**: `[ ]` | **Depends on**: BUG-002 | **Touches**: none

**What to do**:
1. Run regression test from BUG-001 — must now pass
2. Run full test suite — all pre-existing tests must still pass
3. Run linter — no new errors

**Acceptance criteria**:
- [ ] Regression test passes
- [ ] All pre-existing tests pass — no regressions
- [ ] Linter clean

**Decisions**: > Filled in by agent. None yet.
---

### BUG-004 · Update docs
- **Status**: `[ ]` | **Depends on**: BUG-003
- **Touches**: [files with comments about buggy behaviour, if any]

**What to do**:
1. Update inline comments or JSDoc describing now-fixed behaviour
2. If BUG_PLAN.md section 8 says CODEBASE.md needs updating: update and add changelog line
3. If BUG_PLAN.md section 9 says ARCHITECTURE.md needs updating: add the pattern now
4. If the fix made a MEANINGFUL implementation decision (changed an approach, swapped a
   library, reshaped data, or established a pattern worth remembering), append an entry to
   vibe/IMPLEMENTATION_LOG.md per that file's header schema (`Touches:` = files/functions
   changed). A one-line "changed X to Y because Z" bug fix rarely qualifies — don't force it.

**Acceptance criteria**:
- [ ] Comments reflect corrected behaviour
- [ ] CODEBASE.md updated if fix changed structure
- [ ] ARCHITECTURE.md updated if fix revealed a pattern to document
- [ ] IMPLEMENTATION_LOG.md appended if the fix involved a meaningful implementation decision

**Decisions**: > Filled in by agent. None yet.
---
```

End with sign-off checklist:

```
---
#### Bug Fix Sign-off: [Bug summary]
- [ ] Regression test written, named clearly, passes after fix
- [ ] Full test suite green — no regressions
- [ ] Linter clean
- [ ] No files outside BUG_PLAN.md scope modified
- [ ] CODEBASE.md updated if fix changed structure
- [ ] ARCHITECTURE.md updated if fix revealed a pattern to document
- [ ] DECISIONS.md updated if any deviation from BUG_PLAN.md
- [ ] Doc commits separate from code commits
---
```

Save as `vibe/bugs/[date-slug]/BUG_TASKS.md`.

---

## Step 8 — Update vibe/TASKS.md

**1.** Note previously active feature or "none".

**2.** Insert inline bug block above active feature:
```
🐛 [Bug summary in plain English] (0/4)
   [ ] BUG-001 · Regression test — reproduce the bug in a test
   [ ] BUG-002 · Implement fix — smallest change that resolves root cause
   [ ] BUG-003 · Verify and run full suite — regression passes, nothing else broke
   [ ] BUG-004 · Update docs
   → Full specs: vibe/bugs/[date-slug]/BUG_TASKS.md (agent use)
```

**3.** Update "What just happened" and "What's next":
```
## What just happened
🐛 Bug found: [plain English description of what was broken]
Starting fix — regression test first, then fix.

## What's next
⬜ BUG-001 · Write a test that reproduces the bug
   Must fail before fix and pass after — proves the fix works.
Say "next" to begin.
```

After each task: mark [x], update count, update What just happened + What's next in plain English.

When fix completes: collapse to single line, restore interrupted feature:
```
✅ [Bug summary] — fixed [date] (4/4 ✅)
```

---

## Step 9 — Update vibe/DECISIONS.md

```
---
### D-[ID] — Bug fix: [Bug summary]
- **Date**: [date] · **Type**: drift
- **Folder**: vibe/bugs/[date-slug]/
- **Root cause**: [one line from BUG_SPEC.md]
- **Files in scope**: [from BUG_PLAN.md]
- **Fix approach**: [one line]
- **CODEBASE.md update**: [Yes — what / No]
- **ARCHITECTURE.md update**: [Yes — what pattern documented / No]
- **Deviations from BUG_PLAN.md**: [logged below / none]
---
```

Tell the user:

---
> ✅ **Bug fix kit ready.**
>
> **Created:** vibe/bugs/[date-slug]/
>   BUG_SPEC.md · BUG_PLAN.md · BUG_TASKS.md
> **Updated:** vibe/TASKS.md · CLAUDE.md · vibe/DECISIONS.md

**Read execution mode:**
```bash
grep "VIBE_MODE" CLAUDE.md 2>/dev/null | cut -d= -f2 | tr -d ' '
```

If `autonomous` → read the vibe-mode skill's `references/AUTONOMOUS_EXECUTION_BLOCK.md`
(resolve the vibe-mode install dir — commonly `~/.claude/skills/vibe-mode/`, or
`~/.claude/plugins/marketplaces/*/skills/vibe-mode/` under a plugin install)
and follow the autonomous execution protocol. Begin immediately.
Note: regression test task always runs first — it has no dependencies.

If `manual` or not set → tell the user:
> Tell your coding agent:
> ```
> Read CLAUDE.md, vibe/CODEBASE.md, vibe/ARCHITECTURE.md,
> vibe/TASKS.md. Confirm first task before writing any code.
> ```
> Regression test first. Always. Fix second.
> Say **"next"** after each task.
---

## Step 10 — Update dependency graph

After the fix is complete and verified, invoke `vibe-graph: update`.

The graph reads `git diff --name-only HEAD` to detect exactly which files
the fix touched. Only those nodes are re-indexed. Any new files created
during the fix get added as new nodes. Edges are updated to reflect
any import changes made during the fix.

This step runs automatically — no user input needed.
Keeps blast radius data accurate for the next bug that touches these files.

---

## Step 11 — Blast-radius test coverage

A regression test for the specific bug was written before the fix (diagnosis
discipline). This step invokes `vibe-test` (the `test:` skill) to extend
coverage across the fix's **blast radius** — the changed files plus their
dependents — catching regressions the single reproduction test wouldn't. This is
the auto-handoff vibe-test advertises from vibe-fix-bug.

- Trivial-bug path (no BUG folder): skip — the inline regression test is enough.
- Significant bugs, `VIBE_MODE=autonomous`: run automatically after the graph update.
- Significant bugs, `VIBE_MODE=manual`: offer it —
  > "Fix verified. Extend blast-radius tests for the [N] files it touched? (y/n)"

vibe-test scopes coverage from the `Touches` sections of `BUG_TASKS.md` (and the
graph, if present).
