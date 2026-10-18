---
name: aid-define
description: >
  Decompose approved requirements into discrete features, each recorded as a
  `### Feature NNN` section of REQUIREMENTS.md § 11 that cites the `AC-N` criteria it
  claims. Use this skill once `/aid-describe` has produced an approved REQUIREMENTS.md
  and the work needs splitting into features before any one of them is specified. It
  turns each functional requirement into a feature, then validates the requirements and
  the feature boundaries against the Knowledge Base and the codebase, and halts ready
  for `/aid-specify`.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit
argument-hint: "[work-001] decompose approved requirements  [--features work-001] re-run feature decomposition"
---

# Feature Definition from Approved Requirements

## Agents Involved

aid-define is **multi-agent** — different states use different agents.

| State | Phase | Agent | Why |
|-------|-------|-------|-----|
| 5 FEATURE-DECOMPOSITION | Feature Decomposition | `aid-architect` | Design work — breaking requirements into structured features |
| 6 CROSS-REFERENCE | Cross-Reference & Refine | `aid-reviewer` | Adversarial validation against KB and codebase |
| 7 DONE | DONE | (no dispatch) | Terminal state, user choice prompt |

Decompose approved `REQUIREMENTS.md` into `### Feature NNN` sections under § 11, then
cross-reference the
result against the Knowledge Base and codebase. Produces `REQUIREMENTS.md §11` feature sections
ready for `/aid-specify`.

**Precondition:** `## Interview State: Approved` must be present in `.aid/works/{work}/STATE.md`.
If requirements are not yet approved, run `/aid-describe {work}` first to gather and
approve requirements.

**Workspace structure:**
```
.aid/
  knowledge/           <- shared KB (populated by /aid-discover)
  work-001-name/
    STATE.md           <- process (Interview State: Approved, Cross-Reference, Features State)
    REQUIREMENTS.md    <- approved requirements (/aid-describe) + §11 Features
                          (this skill) + each feature's Technical Specification
                          (/aid-specify). Features are sections; they have no
                          folders and no files of their own.
```

> **State keys.** `interview.state`/`interview.grade`/`interview.sections[]` and
> **`features[]`** are real keys in `work-state-template.yml` -- this skill creates one
> `features[]` entry per `### Feature NNN` section it appends to `REQUIREMENTS.md § 11`,
> and `/aid-specify` updates it as each feature advances. A per-feature "Cross-Reference" status and a
> Q&A-adjacent "Review History" list, as used below, do still carry no dedicated key -- they
> describe this skill's aspirational tracking design rather than a writable structure, and
> that remains an open schema gap. The **Review History** list now has a real target of its own,
> the `review_history` sequence, and Cross-phase Q&A entries have the `qa` sequence.

**First run (after approval):** Decompose functional requirements into `REQUIREMENTS.md`
§11 feature sections.
**After cross-reference:** DONE — ready for `/aid-specify`.
**Re-run decomposition:** pass `--features {work}` to re-run even if features exist.

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
| `--features work-NNN` | Re-run feature decomposition for this work even if features exist. |
| *(no argument)* | Select from existing approved works (see Task Routing). |

---

## Task Routing

When no work ID is provided, resolve the `Approved` candidate set in two layers — a
cross-worktree candidate set (the same source the other downstream skills use), refined
by an `interview.state: Approved` sub-filter this skill alone needs, because the
enumerate record carries no Interview-State field.

### Layer 1 — cross-worktree candidate set

Enumerate works **cross-worktree**: run
`bash .aid/runtime/scripts/works/enumerate-works.sh` (main tree + every git worktree;
never the local `.aid/works/` glob, which is empty on `master`), taking each record's
field-1 `work_id` and field-4 `branch_label`.

**Zero records on any worktree** → **STOP.**
```
No approved works found. Run /aid-describe first to gather and approve requirements.
```
Exit.

### Layer 2 — per-candidate `Approved` sub-filter (read-only `git show`)

For each `(work_id, branch_label)` candidate from Layer 1, determine `Approved` without
entering any worktree:

- **`branch_label` is the literal `(detached)`** (a detached-HEAD worktree — not a
  resolvable git ref): **skip** the `git show` check for this candidate and **retain**
  it in the menu rather than drop it. Its `Approved` status is deferred to the
  authoritative post-enter `## State Detection` step 2 below, which HALTs if the
  entered work turns out not to be `Approved`. Never pass a `(detached)` label to
  `git show`.
- **Otherwise**, run a read-only `git show "<branch_label>:.aid/works/<work_id>/STATE.md"`
  and check whether its `## Interview State` section shows `Approved`:
  - **Shows `Approved`** → retain the candidate.
  - **Does not show `Approved`** (including "file not found at that ref") → drop the
    candidate from the menu.
- **De-duplicate** by `work_id` when the same work appears on more than one
  `branch_label`.

This `git show` reads the **committed** view only — best-effort, and it can skew in
either direction against a live worktree's uncommitted `STATE.md`:
- **False positive** (committed shows `Approved`, a live worktree has since regressed
  it): the candidate is retained here; `## State Detection` step 2 (post-enter, over the
  live file) HALTs on the non-`Approved` value — fail-closed, this can never route into
  a non-Approved work.
- **False negative** (a live worktree holds `Approved` **uncommitted**, the committed
  tip still shows pre-`Approved`): this pre-filter cannot see it, so the work is
  silently absent from the auto-generated menu below — a menu-completeness gap, not a
  correctness defect. **Documented fallback:** invoke `/aid-define work-NNN` directly.
  The argument path bypasses Task Routing (and this filter) entirely — see "Locate +
  Enter the Work's Worktree" below — so `## State Detection` step 2 confirms `Approved`
  from the live, entered `STATE.md`.

### No candidates survive Layer 2

```
No approved works found. Run /aid-describe first to gather and approve requirements.
```

Exit.

### One or more candidates survive Layer 2

```
Approved works ready for feature definition:
  work-001-user-auth   [3 features, cross-reference pending]
  work-002-reporting   [no features yet]

[1] Continue work-001-user-auth
[2] Continue work-002-reporting
```

Wait for response and proceed to State Detection for that work.

**Shortcut:** If only one candidate survives Layer 2, go directly to it without asking.

---

## Locate + Enter the Work's Worktree

**As soon as `<work-id>` is known** — from the `work-NNN` argument, or from Task Routing above —
and **before** State Detection reads `.aid/works/{work}/STATE.md`, follow
`.aid/runtime/templates/downstream-worktree-entry.md` to normalize `<work-id>` to its bare
`work-NNN` branch name, `locate` the worktree (which **always exits 0** and returns
`<path>\t<status>`), and enter the returned path. Keep the defensive empty-path/non-zero backstop
that stops rather than operate blindly — it should not fire against the real helper. Never create
a new worktree — creation belongs to the work-starting skills only.

---

## State Detection

State detection reads the files on disk, every run. Nothing remembered from an
earlier run or from this conversation counts as state, because the files may
have changed since.

All paths below are relative to `.aid/works/{work}/`.

```plaintext
Precondition: Interview State: Approved in STATE.md -- HALT if not met (see below)
State 5:  **Path:** full, Interview State: Approved,
          no § 11 feature sections                                 -> FEATURE-DECOMPOSITION
State 6:  **Path:** full, Interview State: Approved, features exist,
          cross-reference not yet done                             -> CROSS-REFERENCE
State 7:  **Path:** full, Interview State: Approved, features +
          cross-ref already complete                               -> DONE
```

**Detection logic:**

1. Read `STATE.md` `## Interview State` `**Interview State:**` field.
2. If field is absent or value is NOT `Approved`:
   - Print: `[aid-define] Requirements for {work} are not yet approved. Run /aid-describe {work} first to gather and approve requirements.`
   - HALT
3. If State is `Approved`:
   - If `--features` flag provided → **State 5: FEATURE-DECOMPOSITION**
   - Check if `REQUIREMENTS.md § 11 Features` exists and contains `### Feature NNN` subsections
   - If no feature sections → **State 5: FEATURE-DECOMPOSITION**
   - If feature sections exist:
     - Check STATE.md `## Interview State` `## Cross-Reference` sub-section for `**State:** Complete`
       (or check if cross-reference entries exist from a prior run)
     - If cross-reference not yet done → **State 6: CROSS-REFERENCE**
     - If cross-reference already complete → **State 7: DONE**

Print the state-entry line and "you are here" map. Examples for each state:

**FEATURE-DECOMPOSITION:**
```
[State: FEATURE-DECOMPOSITION] — Decompose approved requirements into § 11 feature sections.
aid-define  ▸ you are here
  (from /aid-describe: COMPLETION -> approved REQUIREMENTS)
  [● FEATURE-DECOMPOSITION ] → [ CROSS-REFERENCE ] → [ DONE ] → [ /aid-specify ]
```

**CROSS-REFERENCE:**
```
[State: CROSS-REFERENCE] — Validate REQUIREMENTS.md against KB and codebase; create Q&A for gaps.
aid-define  ▸ you are here
  [✓ FEATURE-DECOMPOSITION ] → [● CROSS-REFERENCE ] → [ DONE ] → [ /aid-specify ]
```

**DONE:**
```
[State: DONE] — Interview complete, approved, decomposed, and cross-referenced.
aid-define  ▸ you are here
  [✓ FEATURE-DECOMPOSITION ] → [✓ CROSS-REFERENCE ] → [● DONE ] → [ /aid-specify ]
```

---

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| FEATURE-DECOMPOSITION | `references/state-feature-decomposition.md` | `aid-architect` | → CROSS-REFERENCE |
| CROSS-REFERENCE | `references/state-cross-reference.md` | `aid-reviewer` | → DONE |
| DONE | `references/state-done.md` | `inline` | → halt |

On state entry, print `[State: NAME]` + the "you are here" map from State Detection above.
When a state completes, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **HALT** → print the closing summary and exit.
