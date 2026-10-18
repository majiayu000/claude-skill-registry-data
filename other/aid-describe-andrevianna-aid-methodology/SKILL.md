---
name: aid-describe
description: >
  Gather requirements through an adaptive interview and write them to REQUIREMENTS.md. Use
  this skill when you know roughly what you want built but the scope, the users, and the
  acceptance criteria are not yet pinned down. It asks one question at a time, each chosen
  by a seasoned-analyst elicitation engine that picks its next move from the gaps in what
  you have said so far. The first run builds the document incrementally; a later run resumes
  wherever it is still incomplete. It ends by presenting the finished requirements for your
  approval and handing off to `/aid-define`.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit
argument-hint: "[work-001] resume work  [--reset work-001] clear and restart"
---

# Conversational Requirements Gathering

State machine: FIRST-RUN -> Q-AND-A -> CONTINUE -> {greenfield: DESCRIBE-SEED ->} COMPLETION [PAUSE -> /aid-define].

## Agents Involved

aid-describe is **multi-agent** — different states use different agents.

| State | Phase | Agent | Why |
|-------|-------|-------|-----|
| 1–4 | Conversational interview | `aid-interviewer` | Empathetic dialogue, deterministic advancing |
| DESCRIBE-SEED | Greenfield KB seed authoring (aid-describe step per D3) | `aid-interviewer` + dispatches `aid-reviewer` for step 5 | Engine-driven 5-element seed elicitation + doc authoring + coherence check + greenfield-mode review gate |

The frontmatter default `agent: aid-interviewer` covers States 1–4. DESCRIBE-SEED also uses `aid-interviewer`, additionally dispatching `aid-reviewer` for its step 5 greenfield-mode review gate.

Gather requirements from a human stakeholder through the **seasoned-analyst elicitation
engine** (`references/elicitation-engine.md`): one fixed D1 opener followed by a
deterministic five-step next-move selector that adapts each question to the current gap,
calibration state, and move playbook (`references/move-playbook.md`,
`references/calibration.md`, `references/advisor-stance.md`). One question per turn.
Builds REQUIREMENTS.md incrementally -- each confirmed answer updates the document
immediately.

**Workspace structure:**
```
.aid/
  knowledge/           <- shared KB (populated by /aid-discover)
  work-001-name/       <- one work = one interview cycle
    STATE.md           <- process (§§ Interview State, Cross-phase Q&A, Features State...)
    REQUIREMENTS.md    <- product (clean document, only project information)
    features/          <- product (one folder per feature, created by /aid-define)
      feature-001-name/
                       #  § 11 feature sections gain their technical specification
                       #  when /aid-specify runs
```

**First run:** Conversational interview from scratch.
**Subsequent runs (before approval):** Resume interview for incomplete sections.
**After approval:** Approved REQUIREMENTS.md is ready — run `/aid-define {work}` to decompose into features.
**Loopback:** Process Q&A injected by downstream phases (e.g., `/aid-specify`).

**Not sure where to start?** If you don't know whether this is a full requirements
gathering effort or a small single-purpose change, run `/aid-triage` first — it
suggests the right entry (a specific shortcut, or this skill) from a one-line
description.

## ⚠️ Pre-flight Checks

### Check 1: Verify Workspace Exists

Check if `.aid/` directory exists. If it doesn't:
```
⚠️ AID workspace not found. Run /aid-config first to set up the project.
```
Exit. Do not proceed.

### Check 2: Verify Not in Plan Mode

- ✅ `Default` or `Auto-accept edits` → Proceed.
- ❌ `Plan mode` → **STOP.** Tell the user to switch out of Plan Mode.

## Arguments

| Argument | Effect |
|----------|--------|
| `work-NNN` | Work on the specified work item. |
| `--reset work-NNN` | Delete the work folder and restart from scratch. |
| *(no argument)* | Task routing (see below). |

### Direct `work-NNN` / `--reset work-NNN` argument -- locate + enter first

A direct `work-NNN` (or `--reset work-NNN`) argument **bypasses Task Routing and the Work
Initiation Gate entirely** -- there is no enumeration, no new-vs-continuation ASK. Because
this still resumes an existing work's isolated worktree, locate + enter it **before** State
Detection reads `.aid/works/{work}/STATE.md`:

1. **Normalize** to the bare `work-NNN` branch name:
   `[[ "$work" =~ ^(work-[0-9]+) ]] && work_id="${BASH_REMATCH[1]}"` (idempotent if already
   bare -- identical normalization to the gate's `§ 3b` step 1 / feature-003 § 3.3).
2. **Locate and enter:**
   `bash .aid/runtime/scripts/works/worktree-lifecycle.sh locate <work_id>` -- resolves via
   the 4-rung ladder and **exits 0 always**, printing `<abs_path>\t<status>` (split on the
   TAB); on an unrecoverable git state it degrades to a non-empty `<cwd-abs>\tcurrent` --
   it never fails the caller. Keep the **defensive** non-zero-exit/empty-path backstop guard
   (surface the error and STOP; this cannot fire against the real helper). Enter the
   resolved path unless `<status>` is `current` (host-native `EnterWorktree` where
   available, else treat the path as the working directory and surface it --
   `worktree-lifecycle.md § Step 2`).
3. **Only then** proceed to State Detection for `<work_id>`. This applies identically to
   `--reset work-NNN` -- the reset's delete-and-recreate (State Detection Step 1) runs
   after locate+enter has already placed the agent inside the work's own isolated worktree.

---

## Task Routing

When no work ID is provided, consult the shared **Work Initiation Gate**
(`.aid/runtime/templates/work-initiation-gate.md`) before doing anything else. Run its
enumeration helper (which scans `.aid/works/*` across the main tree **and every git
worktree**):

```bash
bash .aid/runtime/scripts/works/enumerate-works.sh
```

### No works exist (empty output) -> NEW, no prompt

1. Ask for a short name for this work:
   ```
   What's a short name for this work? (e.g., "user-auth", "reporting", "api-v2")
   ```
2. **Create and enter the worktree, before authoring anything** (gate `§ 3a` step 2):
   `bash .aid/runtime/scripts/works/worktree-lifecycle.sh create work-001 {name}` --
   idempotent; prints the worktree's absolute path on success/no-op; on a non-zero exit or
   an empty path, surface the error and **STOP** (do not create the work folder on the
   current, possibly `master`, tree); on success, enter the resolved path (host-native
   `EnterWorktree` where available, else cwd + surface -- `worktree-lifecycle.md § Step 2`).
3. **Only now**, inside the entered worktree, create `.aid/works/work-001-{name}/`.
4. Proceed to State Detection with this work.

### One or more works exist -> ASK (never auto-continue)

Present the gate's single new-vs-continuation question, showing the enumerated list
(group by `work_id`; annotate each with its `[phase · lifecycle]` and worktree/branch
label from the helper's record columns):

```
Works already exist. Is this a NEW work, or a CONTINUATION of an existing one?

Existing works:
  work-001-user-auth        [Describe · Running]                (main)
  work-002-reporting        [Plan · Running]                    (main)
  work-016-numberless-...   [Specify · Paused-Awaiting-Input]   (worktree: work-016)

[N] New work
[1] Continue work-001-user-auth
[2] Continue work-002-reporting
[3] Continue work-016-numberless-...
```

Wait for the response, then act per the gate:

- **New work:** ask for a name; **resolve `<work-id>`** as `work-{NNN+1}`, where `NNN` is
  the maximum `work-NNN` numeric prefix across every record the enumeration above already
  returned (cross-worktree by construction -- never re-scan a local `.aid/works/` glob;
  gate `§ 3a` step 1; `work-001` if the enumeration returned no records). **Create and
  enter the worktree, before authoring anything** (gate `§ 3a` step 2):
  `bash .aid/runtime/scripts/works/worktree-lifecycle.sh create <work-id> {name}` -- STOP
  on a non-zero exit or empty path (do not create the work folder on the current tree),
  else enter the resolved path. **Only then** create `.aid/works/<work-id>-{name}/` and
  proceed to State Detection.
- **Continuation:** route per the chosen work's `STATE.md` `phase`/`lifecycle` (gate
  Step 3b). When the gate resolves to **`/aid-describe <work>`** (the chosen work is a
  Describe-phase work), **first normalize** the chosen work's id to its bare `work-NNN`
  branch name (`[[ "$chosen_work" =~ ^(work-[0-9]+) ]] && work_id="${BASH_REMATCH[1]}"` --
  the enumeration supplies the full folder slug, but `locate` keys on the bare branch name;
  gate `§ 3b` step 1), then **locate and enter** that work's worktree per the gate's `§ 3b`
  steps 2-4 (`worktree-lifecycle.sh locate <work_id>` -- always exits 0, degrading to a
  non-empty `<cwd-abs>\tcurrent` on a git-broken state; keep the defensive non-zero-exit/
  empty-path backstop guard, which cannot fire against the real helper; enter unless
  `<status>` is `current`), and **only then** proceed straight to **State Detection** for
  that work in this same invocation -- that IS aid-describe resuming. When it resolves to a
  **different** door (a later-phase full-path work, or a halted shortcut work ->
  `/aid-execute`), print the resolved resume command and STOP; do not create or drive a
  work here (the locate+enter for that target happens inside the routed command's own run).

> There is **no** auto-continue shortcut: a lone unapproved work is never silently
> resumed. The gate always asks when any work exists (deliberate UX change; the previous
> "if only one work exists and it's not yet Approved, go directly to it" behavior is
> removed).

---

## State Detection

State detection reads the files on disk, every run. Nothing remembered from an
earlier run or from this conversation counts as state, because the files may
have changed since.

All paths below are relative to `.aid/works/{work}/`.

```plaintext
State 1:  No STATE.md (§ Interview State)                           -> FIRST-RUN
State 2:  STATE.md § Cross-phase Q&A has Pending entries            -> Q-AND-A
State 3:  Interview State: In Progress, incomplete                  -> CONTINUE
State GS: Interview State: In Progress, all done,
          greenfield (no brownfield KB on disk) + seed not complete -> DESCRIBE-SEED
State 4:  Interview State: In Progress, all done,
          not greenfield OR seed already complete                   -> COMPLETION
Approved: Interview State: Approved                                 -> hand-off to /aid-define
```

**Detection logic:**

1. If `--reset` → delete the work folder → recreate → proceed as State 1
2. Check for `STATE.md` in the work folder and look for the `## Interview State` section
3. If missing → **State 1: FIRST-RUN**
4. If exists:
   a. Check `## Cross-phase Q&A` section for entries with `**Status:** Pending`
   b. If Pending entries exist → **State 2: Q-AND-A**
   c. Read `**Interview State:**` field in `## Interview State`
      - If State is `In Progress`:
        - Read Section Status table under `## Interview State`
        - If any section is `Pending` or `Partial` → **State 3: CONTINUE**
        - If all sections are `Complete` or `N/A`:
          **Greenfield check:** read `.aid/knowledge/` -- if no `.md` files are present OR every
          `.md` file present carries `source: forward-authored` (authored by DESCRIBE-SEED in a
          prior session), the project is greenfield (no brownfield KB on disk). If any file
          carries `source: hand-authored` or `source: generated`, the project is brownfield.
          **Seed check:** read STATE.md `## Seed Authoring` `**Status:**`. If the section is
          absent or its value is not `Complete`, the seed is not yet done.
          - If greenfield AND seed not done → **State GS: DESCRIBE-SEED**
          - Otherwise → **State 4: COMPLETION**
      - If State is `Approved`:
        - Print: `[aid-describe] Requirements for {work} are approved. Run /aid-define {work} to decompose into features.`
        - HALT

Print the state-entry line and "you are here" map. Examples for each state:

**FIRST-RUN:**
```
[State: FIRST-RUN] — Start a new interview from scratch; create STATE.md and REQUIREMENTS.md scaffold.
aid-describe  ▸ you are here
  [● FIRST-RUN ] → [ Q-AND-A ] → [ CONTINUE ] → [ COMPLETION ] → [ /aid-define ]
```

**Q-AND-A:**
```
[State: Q-AND-A] — Resolve pending cross-phase questions before continuing.
aid-describe  ▸ you are here
  [✓ FIRST-RUN ] → [● Q-AND-A ] → [ CONTINUE ] → [ COMPLETION ] → [ /aid-define ]
```

**CONTINUE:**
```
[State: CONTINUE] — Resume the conversational interview for incomplete sections.
aid-describe  ▸ you are here
  [✓ FIRST-RUN ] → [✓ Q-AND-A ] → [● CONTINUE ] → [ COMPLETION ] → [ /aid-define ]
```

**COMPLETION:**
```
[State: COMPLETION] — All sections captured; run KB hydration and present requirements for approval.
aid-describe  ▸ you are here
  [✓ FIRST-RUN ] → [✓ Q-AND-A ] → [✓ CONTINUE ] → [● COMPLETION ] → [ /aid-define ]
```

**DESCRIBE-SEED (greenfield full path — between CONTINUE and COMPLETION):**
```
[State: DESCRIBE-SEED] — Authoring forward-authored KB seed from elicited intent (greenfield mode).
aid-describe  ▸ you are here
  [✓ FIRST-RUN ] → [✓ Q-AND-A ] → [✓ CONTINUE ] → [● DESCRIBE-SEED ] → [ COMPLETION ] → [ /aid-define ]
  (greenfield seed authoring: 5-element seed + coherence check + greenfield-mode review gate)
```

---

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| FIRST-RUN | `references/state-first-run.md` | `aid-interviewer` | → CONTINUE |
| Q-AND-A | `references/state-q-and-a.md` | `aid-interviewer` | → CONTINUE |
| CONTINUE | `references/state-continue.md` | `aid-interviewer` | → DESCRIBE-SEED (greenfield: no brownfield KB on disk and seed not yet complete) / → COMPLETION (brownfield or seed already complete) |
| DESCRIBE-SEED | `references/state-describe-seed.md` | `aid-interviewer` | → COMPLETION |
| COMPLETION | `references/state-completion.md` | `aid-interviewer` | PAUSE-FOR-USER-DECISION → Run /aid-define {work} |

On state entry, print `[State: NAME]` + the "you are here" map from State Detection above.
When a state completes, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** / **PAUSE-FOR-USER-DECISION** → print the pause reason + resume command and exit.
- **HALT** → print the closing summary and exit.

---

## Targeted Interview (Loopback Re-entry)

When a downstream phase (e.g., `/aid-specify`) needs clarification on requirements:

1. The calling phase writes Q&A entries directly to the work's STATE.md
   in the `## Cross-phase Q&A` section
2. Next `/aid-describe {work}` run detects Pending Q&A → enters State 2 (Q-AND-A)
3. Questions are presented to the user one at a time
4. Answers are recorded in STATE.md `## Cross-phase Q&A` and REQUIREMENTS.md
5. The affected `§ 11` feature section is updated if the answer bears on one feature

**Q&A entry format for downstream phases to write:**

```markdown
### Q{N}

- **Category:** {category, e.g., Architecture, Requirements, Security}
- **Impact:** {High|Medium|Low|Required}
- **Status:** Pending
- **Context:** {why this matters — what the downstream phase found; cite the calling phase, e.g., "Surfaced by /aid-specify work-001/feature-001"}
- **Suggested:** {answer if inferrable, or "—"}
```
