---
name: aid-specify
description: >
  Turn one feature into a technical specification, collaboratively. Use this skill when a
  feature has been defined and how it will actually be built needs settling before any task
  is planned. The agent works as a tech lead: it reads the Knowledge Base, the requirements,
  and the codebase, proposes a technical approach, and refines it with you, writing the
  result into that feature's `#### Technical Specification` subsection in REQUIREMENTS.md
  § 11. One feature at a time.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit
argument-hint: "work-001/feature-001 (required)  [--reset] clear technical spec for this feature"
---

# Technical Specification — Conversational Refinement

Specify the technical implementation of a single feature through conversational refinement
with the user.

**The agent is a tech lead, not an interviewer.** It proposes concrete solutions grounded
in the existing architecture. The user validates, redirects, or deepens the discussion.

**One feature at a time.** The feature path is a required argument.

**The Loop:**

Every section follows the same cycle:

```
1. PROPOSE  → agent proposes (grounded in KB, codebase, SPEC)
2. DISCUSS  → user and agent refine together
3. WRITE    → save what was agreed into REQUIREMENTS.md §11 / Feature NNN
4. REVIEW   → grade what was written against KB/codebase reality
             → pass? next section. fail? back to 1.
```

**Re-run = enter at step 4 with existing content.**

**Workspace:**
```
.aid/
  knowledge/               ← shared KB
  work-NNN-{name}/
    STATE.yml              ← process (features sequence, qa sequence)
    REQUIREMENTS.md        ← product: §11 Features holds one section per
                              feature (decomposition from /aid-define +
                              Technical Specification from here). Features have
                              no folders and no files of their own.
```

> **Accuracy note.** Features State is **AUTHORED**, and it now has a real
> target: the `features:` sequence in `work-state-template.yml`, one entry per
> feature, created by `/aid-define` at decomposition and updated here as each
> feature advances. It carried no key and was documented as a read-only DERIVED
> view for as long as this note said so, which was wrong twice over -- nothing
> derives it, and the mislabel made the `STATE.md` -> `STATE.yml` converter treat
> a real row as proof that a work predated the per-unit hierarchy, so it refused
> every work that had been through `/aid-define`. Cross-phase Q&A's `qa` key is
> AUTHORED only at the delivery level (`delivery-state-template.yml`) or, on the
> flattened Lite path, at the work level (`work-state-template.yml`) -- a
> full-path work has no `qa` key at the work level at all (full-layout omission
> rule), and `/aid-specify` runs before any delivery exists (Specify precedes
> Plan), so a full-path work has no delivery yet to hold one either -- that half
> of the gap is unchanged and is still a candidate follow-up. The Features State
> half is closed: write `features[]` entries for real.

---

## ⚠️ Pre-flight Checks

### Check 1: Feature Path Required

If no feature path was provided, resolve **work-first**: features live inside each
work's own worktree, so they cannot be listed from the main checkout until one is
entered — the feature glob below runs only after that.

1. Enumerate works **cross-worktree**: run
   `bash .aid/runtime/scripts/works/enumerate-works.sh` (main tree + every git
   worktree; never the local `.aid/works/` glob, which is empty on `master`), taking
   each record's field-1 `work_id`.
2. **Zero works** → **STOP.**
   ```
   No works found. Run /aid-describe first.
   ```
   Exit.
3. **Single work** → normalize its `work_id` to the bare `work-NNN` branch name and
   `locate`+enter it (`.aid/runtime/templates/downstream-worktree-entry.md` — the
   same mechanics as "Locate + Enter the Work's Worktree" below), then list *that*
   work's features locally, now visible inside the entered tree:
   ```
   Usage: /aid-specify feature-001

   Available features in work-001-user-auth:
     feature-001-login        [No STATE — not started]
     feature-002-password      [In Discussion — 2/5 sections]
   ```
   Read `REQUIREMENTS.md § 11 Features` inside the entered worktree. For each `###`
   feature subsection, check the work STATE.yml's `features:` entry (the one whose id is that
   feature) and show status.
   Exit.
4. **Multiple works** → present the work list:
   ```
   Usage: /aid-specify work-001/feature-001

   Available works:
     work-001-user-auth
     work-002-reporting

   [1] work-001-user-auth
   [2] work-002-reporting
   ```
   Ask which work. Once chosen, normalize + `locate`+enter it exactly as step 3, then
   list its features the same way. Exit.

**Shortcut:** If only one work exists, accept bare `feature-001` and resolve
automatically — this is step 3 above; the single-work case already enters the work
before the feature glob runs.

### Locate + Enter the Work's Worktree

**As soon as the `work-NNN` prefix is parsed / auto-selected** (right after Check 1) and
**before** Check 2 resolves the feature in `REQUIREMENTS.md §11`, follow
`.aid/runtime/templates/downstream-worktree-entry.md` to normalize `<work-id>` to its bare
`work-NNN` branch name, `locate` the worktree (which **always exits 0** and returns
`<path>\t<status>`), and enter the returned path. Keep the defensive empty-path/non-zero backstop
that stops rather than operate blindly — it should not fire against the real helper. Never create
a new worktree — creation belongs to the work-starting skills only.

### Check 2: Feature Exists

Resolve the feature to a `###` subsection of `REQUIREMENTS.md § 11 Features` by its
three-digit number:
- `feature-001` → the `### Feature 001 — …` subsection of `.aid/works/{work}/REQUIREMENTS.md`
- `work-001/feature-002` → the `### Feature 002 — …` subsection of `.aid/works/work-001-*/REQUIREMENTS.md`

**If §11 is absent or has no such subsection:** Exit with instruction to run
`/aid-define` first (or `/aid-describe`, if REQUIREMENTS.md itself is missing).
**If found:** Print: `[Resolved: REQUIREMENTS.md §11 / Feature 001 — {Title}]`

The number is exact, not a prefix match: sections are numbered, so there is nothing
to disambiguate and no glob to widen.

### Check 3: Plan Mode

- ✅ `Default` or `Auto-accept edits` → Proceed.
- ❌ `Plan mode` → **STOP.** Tell the user to switch out of Plan Mode.

---

## Arguments

| Argument | Effect |
|----------|--------|
| `work-NNN/feature-NNN` | **Required.** Path to the feature to specify. |
| `feature-NNN` | Shortcut when only one work exists. |
| `--reset` | Clear the feature section's `#### Technical Specification` back to its placeholder and delete STATE.yml. |

---

## State Detection

The feature is a section of `.aid/works/{work}/REQUIREMENTS.md § 11`; its per-feature process state is its entry in the work `STATE.yml`'s `features:` sequence.

```
State 1: No features[] entry, or state Pending, in work STATE.yml -> INITIALIZE
State 2: Feature State: In Discussion                         → CONTINUE
State 3: Feature State: Spike Needed                          → SPIKE
State 4: Feature State: Blocked (loopback pending)            → BLOCKED
State 5: Feature State: Ready                                 → REVIEW (enter loop at step 4)
```

Print the state-entry line and "you are here" map. Examples for INITIALIZE:

```
[State: INITIALIZE] — First run for this feature; load context, determine sections, begin The Loop.
aid-specify ({feature})  ▸ you are here
  [● INITIALIZE ] → [ CONTINUE ] → [ REVIEW ] → [ DONE ]
```

For CONTINUE:
```
[State: CONTINUE] — Resume The Loop (Propose → Discuss → Write → Review) for the next pending section.
aid-specify ({feature})  ▸ you are here
  [✓ INITIALIZE ] → [● CONTINUE ] → [ REVIEW ] → [ DONE ]
```

For REVIEW:
```
[State: REVIEW] — All sections complete; re-review entire spec against current KB and codebase.
aid-specify ({feature})  ▸ you are here
  [✓ INITIALIZE ] → [✓ CONTINUE ] → [● REVIEW ] → [ DONE ]
```

For DONE (Ready):
```
[State: DONE] — Spec is Ready and has met the minimum grade.
aid-specify ({feature})  ▸ you are here
  [✓ INITIALIZE ] → [✓ CONTINUE ] → [✓ REVIEW ] → [● DONE ]
```

**SPIKE:**
```
[State: SPIKE] — Feature has unknowns requiring investigation; spike work needed.
aid-specify ({feature})  ▸ you are here
  [✓ INITIALIZE ] → [ CONTINUE ] → [● SPIKE ] → [ REVIEW ] → [ DONE ]
```

**BLOCKED:**
```
[State: BLOCKED] — Feature has a pending loopback that must be resolved before continuing.
aid-specify ({feature})  ▸ you are here
  [✓ INITIALIZE ] → [ CONTINUE ] → [● BLOCKED ] → [ REVIEW ] → [ DONE ]
```

---

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| INITIALIZE | `references/state-initialize.md` | `aid-architect` | → CONTINUE |
| CONTINUE | `references/state-continue.md` | `aid-architect` | → REVIEW |
| SPIKE | `references/state-spike.md` | `inline` | → CONTINUE |
| BLOCKED | `references/state-blocked.md` | `inline` | → CONTINUE |
| REVIEW | `references/state-review.md` | `aid-reviewer` | → DONE |
| DONE | `references/state-done.md` | `inline` | → halt |

On state entry, print `[State: NAME]` + the "you are here" map from State Detection above.
When a state completes, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** / **PAUSE-FOR-USER-DECISION** → print the pause reason + resume command and exit.
- **HALT** → print the closing summary and exit.

---

## Handling Outcomes During Discussion

Read `references/handling-outcomes.md` for how to handle KB issues, requirement gaps,
spikes, blocks, feature splits, and feature merges during discussion.

---

## Known Issues & Quality Gates

Read `references/known-issues-scope.md` for the known-issues filter (what to register
vs skip) and feature-specific quality gates (test/lint requirements beyond baseline).

---

## Conversation Style

**Do:**
- Propose concrete solutions based on what exists
- Reference specific files, classes, patterns
- Explain trade-offs when multiple approaches exist
- Push back if the user contradicts KB patterns
- Admit when you don't know something

**Don't:**
- Ask generic questions — propose based on KB
- Generate walls of spec without discussion
- Move to next section without clear agreement
- Be a yes-machine — if you see a problem, say so

**The rhythm:**
```
Agent: "Based on {KB}, I propose {concrete approach}."
Dev:   "Actually, we should do X because Y."
Agent: "Good point. That means we also need Z. Updated approach..."
Dev:   "Yeah, works."
Agent: [writes] [reviews: ✅ consistent] [next section]
```
