---
name: design
description: "Plan the implementation of multi-file changes, architecture decisions, or ambiguously scoped work before code is written; the plan node of the pm loop. Skip single-file fixes, renames, and small refactors with clear scope."
argument-hint: "[task description | handoff | continue]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
effort: max
disable-model-invocation: false
---

Design and plan implementation for the given task.

Task: $ARGUMENTS (if empty, ask the user)

## Modes

`$ARGUMENTS` selects the mode. When the **sole** argument is exactly one of these reserved tokens, run that mode instead of the normal plan flow:

- **`handoff`** → package the in-flight plan's mid-execution state into a paste-ready kickoff prompt for a fresh session/agent, then copy it to the clipboard. Read-only — writes nothing. See **Handoff mode** below.
- **`continue`** → resume the plan bound to THIS session, find the first unchecked step, and pick up implementation from there. See **Continue mode** below.
- **anything else (or empty)** → a task description; run the normal plan flow (Steps 1-7). A task whose description merely *contains* `handoff`/`continue` among other words is NOT a mode — only the bare single token dispatches.

## System — role in the pm-* loop

`design` is a **general-purpose** planning skill (any multi-file change). It is also the **plan** node of the project-management loop:

```
(pm-context · context | retro · memory | pm-roadmap · backlog)  ──▶  design · plan
```
When invoked on a `pm-roadmap` item, read its context/memory, reserve and enter its
dedicated worktree, stage the approved plan under that reservation, then call
`pm-roadmap.ts persist`. Persist journal-creates the canonical plan and backlog linkage,
seeds the worktree execution pointer, and selects or safely parks it in main. Standalone
plans use the same worktree and plan transaction without a backlog item.

## Product-Surface Gate Integration

When a request also matches `product-craft`, close the smallest applicable product-surface
gates before drafting the technical implementation plan:

1. PR/diff/review feedback remains owned by `code-review`; completed-feature confirmation
   remains owned by `verify`. Neither enters this planning path through product-craft.
2. New or materially changed client surfaces start with `product-craft`, which selects
   Seed, Focused Delta, or Full and obtains the required Experience and Interface gates.
3. After `READY FOR BUILD`, this skill owns technical planning whenever its independent
   trigger applies at any depth — including every expected three-or-more-file change.
4. Durable UI writes require both the applicable product-craft authorization and this
   skill's persisted active plan. A routine no-contract change still uses this skill when
   the normal design trigger applies.
5. Contract gaps return to `experience-design` or `interface-design` through
   `product-craft`; technical planning must not invent the missing design decision.

`design-contract.md` remains the product-surface authority. This plan records how the
approved contract will be implemented and verified; it does not replace or silently
amend the contract.

### Durable Product Proof Handoff

When product-craft supplies approved surface records:

1. Require its repo-relative Durable contract path, the approved `Surface Obligations` rows,
   the `## Artifact Ledger` entry for any selected artifact, and the approval tokens
   (`experience_approved`, `direction_selected`, `build_authorized` as applicable). Resolve
   the path inside the execution root and verify the same records are persisted under that
   contract's `## Decision Log & Open Questions`.
2. Reject a missing/escaping path, absent durable packet, duplicate/unknown/unmapped row,
   GAP, or incomplete required approval. A generic criterion such as “mobile tests pass”
   cannot replace a material row or its specimen evidence.
3. In the technical plan, create this exact section and copy the approved rows and packet
   verbatim:

   ```markdown
   ## Product Surface Proof Obligations

   Durable contract: <repo-relative design-contract.md path>

   <exact Surface Obligations rows>

   <exact Artifact Ledger rows, when an artifact was selected>

   <approval tokens with the user evidence recorded for each>
   ```

4. Copy the approval tokens and their user evidence verbatim. Technical planning cannot
   infer, add, or remove a token — least of all `direction_selected`, which only the user
   can produce.
5. Turn every applicable experience and interface obligation into a goal-level Verifiable
   Success Criterion with a concrete code, assertion, or inspected-render observable.
   Preserve `OBL-NNN` ids and their `Derives from` links so `verify` can walk the chain
   later.

`design` never writes implementation evidence or the Implementation Bridge section. If a required active
plan has a missing Durable contract path or cannot preserve the rows exactly, the product
surface portion of planning is `BLOCKED`.

## Execution Bootstrap (before Context Discovery)

Determine a stable kebab-case id and base ref before reading project code. A backlog item
already supplies its id. For an ad-hoc design, reserve a collision-free id. Explicit base
intent is authoritative; otherwise use the current branch only when unambiguous.

```bash
repo_root="$(git rev-parse --show-toplevel)" || exit 1
engine="$HOME/.config/ai/lib/worktree.mjs"
node "$engine" ensure --root "$repo_root" --id <id> --base <base-ref>
```

Announce the returned base ref/OID, branch, and execution root. Then enumerate and read
the target root's tool-native project instruction chain. All discovery, Git, file, build,
and test operations after this point are rooted at `execution_root`. If the engine
returns `migration_required`, run/review PM migration first. Ambiguous base intent,
non-empty store conflicts, dirty main legacy adoption, or an occupied branch/path stop
the flow; never guess or fall back to main execution.

## Context Discovery (inside the execution root)

Before starting, search for existing plan artifacts that may be relevant:

```bash
ls {{PLAN_DIR}}/ 2>/dev/null && grep -l "<relevant keywords>" {{PLAN_DIR}}/*.md 2>/dev/null
```

Match against the `description:` frontmatter field for highest signal-to-noise. Read related plans for context (prior decisions, lessons learned).

**Also consult the backlog** via the CLI — `pm-roadmap.ts list` (eligible items) or `pm-roadmap.ts get <id>` — to see whether this work is already a backlog item (pull its Priority/Note/owning task and any sibling decisions). If so, this design links back to that item at persist time. (CLI setup in Step 5; on a legacy repo the read prints a migrate hint instead.)

## Steps

### 1. Decompose

If 2+ independent subsystems exist, list them and ask which to start with.

Size the work before proposing anything, and say the number out loud: how many files change, and is the change mechanical (rename, signature update) or judgment-heavy (new abstraction, contract change)? Sweep for every existing occurrence of the pattern being changed — a fix applied to one call site while legacy ones survive elsewhere is not done, and finding those later reopens a closed plan.

For large, irreversible, or under-specified work, mention `/grill` before proposing approaches when intent alignment is the main risk; invoke it only if the user explicitly asks.

### 2. Propose approaches

Propose 2-3 approaches with:

- **How**: concrete implementation description
- **Trade-off**: pros and cons

Mark one as recommended.

### 3. Present incrementally

Present design section by section with confirmation. Do NOT dump all sections at once. Wait for approval before moving to the next section.

### 4. Implementation plan (presentation only — no execution yet)

After design approval, present the implementation plan as response text. **Do NOT begin executing edits in this step.**

Order the plan by revisability: lead with what 대협 is most likely to overturn — data model, type interfaces, anything user-facing — and put mechanical refactoring last. Reading top-down should hit the riskiest decision first, not the safest.

When a decision is visual or structural enough that prose under-specifies it — a layout, a state machine, a data shape with many relations — attach one self-contained HTML artifact beside the plan and link it from the row it belongs to. A mockup gets reacted to faster and more precisely than a paragraph describing the same thing. The plan artifact itself stays markdown; the pm loop parses it.

1. **File Structure**: Map Create/Modify/Test files with responsibilities. For each non-trivial modification, show a before/after sketch of the shape that changes — the current code and what it becomes. Prose describing an edit is not reviewable; the sketch is what the user approves, and it lands in the plan artifact so the reviewer sees the same thing at approval time
2. **Verifiable Success Criteria**: List the goal-level conditions that must hold for the work to count as done. Use a checkable table with these fields:

   | Condition | Proof command or observable | PASS condition |
   | --- | --- | --- |

   Each row must be specific enough for `/verify` to run or observe directly; generic prose or a command that can pass before the implementation exists is not sufficient. These seed `/verify`'s truth conditions — without them verify must re-derive the goal from scratch.
3. **Risks**: List what could break, what contract might be misread, and how each risk is bounded or mitigated.
4. **Tasks**: Use `- [ ]` checkboxes. Each step includes expected output (PASS/FAIL). During implementation, flip `- [ ]` → `- [x]` in the plan artifact the moment each step meets its PASS output — unconditionally, one step at a time.
5. If planned output differs from actual during implementation, investigate

### 5. Persist plan artifact (BEFORE implementation)

After the user approves the design (Step 3 approval = signal to persist) and **before any file writes that implement the plan**:

1. **Reuse the bootstrap id and mapping.** Do not generate a second id after discovery.
   Re-run read-only validation if the reservation or target instructions changed.

2. **Resolve the existing current automatically.** A draft/active current stays active in
   its own worktree and becomes parked when the new plan is selected; do not close it or
   ask merely because another design starts. A terminal current is stale and is eligible
   for exact cleanup. A different live plan already occupying the new target worktree is
   a hard conflict. `current.txt` is a selector, not a status field.

3. **Render and stage; do not write the canonical plan directly.** The canonical path is
   `{{PLAN_DIR}}/YYYY-MM-DD-<id>.md`, but the approved bytes first enter the
   reservation-bound stage through the engine. Include this English frontmatter:

```yaml
---
id: <english-kebab-slug>
title: <English title, ~80 chars>
description: <English 1-2 sentence summary, ~150 chars — used for grep/search>
date: YYYY-MM-DD
status: draft
pm_loop: true
base_branch: <resolved human-readable base ref>
base_commit: <resolved 40-character OID>
branch: <dedicated branch from ensure>
worktree: <repo-relative dedicated worktree path>
files_affected:
  - <file paths from implementation plan>
---
```

`pm_loop: true` tracks a backlog item. `pm_loop: false` is standalone; both still require
the execution mapping and dedicated worktree.

Follow with Goal, Approach, Decisions, Verifiable Success Criteria, Risks, Implementation
Steps, and the empty Post-Implementation Notes section. For product-surface work, insert
`## Product Surface Proof Obligations` before Verifiable Success Criteria and retain its
exact rows/path/packet. Pipe the complete bytes to the stage without a second persistent
input file:

```bash
node "$engine" stage-plan --root "$repo_root" --id <id> --input /dev/stdin <<'PLAN'
<complete rendered plan>
PLAN
```

5. **Persist through the CLI.** The id doubles as the backlog item id. Setup:

   ```bash
   repo_root="$(git rev-parse --show-toplevel)" || { echo "not in a git repo"; exit 1; }
   (cd ~/.config/ai/skills/pm-roadmap && [[ -d node_modules ]] || npm install)
   pm() { PM_ROOT="$repo_root" ~/.config/ai/skills/pm-roadmap/node_modules/.bin/tsx ~/.config/ai/skills/pm-roadmap/pm-roadmap.ts "$@"; }
   ```

   A real task key is required for `pm_loop:true`; create/triage it first when needed.

   ```bash
   pm task create <KEY> --title "<task title>"   # only when the task does not exist
   PM_SESSION_TOOL="<injected session tool>" PM_SESSION_ID="<exact injected session id>" pm persist <KEY> <id> "<plan-repo-rel-path>" --title "<plan title>"
   ```

   Copy the tool and exact, unsanitized session id from the current prompt's session-routing
   block. Never substitute a default, PPID, normalized id, or main `current.txt`. The CLI
   commits the persist transaction first and then binds that exact session to the persisted
   plan. Its final output line is `session_binding: bound` on success. If it reports
   `session_binding: unbound (<typed reason>); do not retry persist`, the persist already
   committed: report the explicit unbound recovery and stop without replaying the command.

   Persist acquires reservation lock then task-store lock, journal-creates the canonical
   plan from the staged bytes, creates/links the draft item, seeds the target execution
   pointer, and attempts the main launcher CAS. Report its exact outcome:

   - `persisted_selected`: main and target point to the new plan.
   - `persisted_parked`: a newer main selection survived; the target still owns the plan.

   Never retry a parked result by adopting a fresh main expectation. A later explicit
   `pm select --plan <path>` selects it. Never hand-edit tasks, canonical plan content,
   reservations, or current pointers.

   Standalone persistence uses `pm persist --standalone --id <id> --plan <path>` and creates no
   backlog/closed/deferred item; it still consumes the reservation and seeds the mapped
   target.

6. **The staged content already includes the empty Post-Implementation section:**

```markdown
## Post-Implementation Notes

<!-- Filled by /retro if run after implementation -->
```

7. **Confirm to the user:** "saved as `<path>` — review and reply with **승인** (active 전환), **취소** (dropped), or further edits. Run `/retro` after implementation to mark the plan `done`." For high-risk, multi-file, architecture, irreversible, or unclear-scope plans, recommend `/plan-review` before `승인`; if review is intentionally skipped for cost, latency, auth, or low-risk reasons, record an explicit `SKIP` in the plan review loop instead of treating the skip as approval.

**Status values & lifecycle**: `draft` (just saved) → `active` (in progress) → `done` | `dropped` (terminal).

### 6. Backlog linkage invariants

Step 5.5 already wrote the linkage; these are the rules it satisfies — all enforced by ops (a violation throws, it is never silently written):

- **id == plan slug**, and **one item per plan path** (`Plan:` 1:1 across every task's backlog + closed). `persist`/`plan` reject a duplicate plan link or a reused id.
- The backlog item **Status mirrors the plan** (`draft` at persist; `active` after `승인`).
- A **real task `<KEY>` is required** — an inbox item is untriaged and cannot carry a plan or be made in-flight. Triage it first (`pm triage <id> <KEY>`); `persist`/`plan`/`focus` reject inbox items.

Skip for a standalone (`pm_loop: false`) plan — it has no backlog item.

### 7. Archive aged plans

**After** linkage (the new plan is current + linked and won't be touched), run the deterministic archiver to keep `{{PLAN_DIR}}/` small. It moves **terminal** (`done`/`dropped`) plans **≥ 30 days old** that are **unreferenced** (not named by `current.txt`, not any backlog item's `Plan:`) into `{{PLAN_DIR}}/archive/`, and rewrites each task's `closed.md` `Plan:` pointer so closed-join / GUI still resolve. Reference-protected and idempotent (safe to re-run; recovers a crash between move and pointer rewrite). The just-saved `draft` plan is never archived (it is current + non-terminal). No-ops on a repo with no task store.

```bash
repo_root="$(git rev-parse --show-toplevel)" || { echo "not in a git repo"; exit 1; }
(cd ~/.config/ai/skills/pm-roadmap && [[ -d node_modules ]] || npm install)
~/.config/ai/skills/pm-roadmap/node_modules/.bin/tsx ~/.config/ai/skills/pm-roadmap/archive.ts "$repo_root"
```

Report the archiver's output (moved / skipped). Add `--dry-run` to preview without moving, or `--today=YYYY-MM-DD` to pin the age cutoff.

## Rules

- Do NOT implement until user approves the design
- **Implement only against an `active` plan.** An explicit build instruction (`승인`/"구현해"/"최대한 작업해"/"ㄱㄱ") IS the `승인` trigger: promote `status: draft → active` (+ `pm approve <KEY> <id>`) first, then implement. A terse go-ahead is no excuse to skip section-by-section approval or a warranted `/grill`.
- Plan artifact is saved ONLY after explicit design approval (Step 3)
- **Plan artifact MUST be persisted (Step 5) BEFORE any implementation begins.** Saving the plan after implementation breaks the verify/retro contract (they read the session-bound in-flight plan; the plan id is used for backlog linkage) and loses the pre-drift intent snapshot
- **ALWAYS check off implementation steps as you go.** The instant a step meets its
  PASS output, call `pm plan-step check <plan> <number>`; never batch at the end and never
  hand-edit checkbox lines.
- The plan MUST carry a `## Verifiable Success Criteria` section (goal-level PASS/FAIL conditions). It is the seed `/verify` checks against — a plan whose goal isn't expressed as checkable conditions weakens the design→verify contract.
- The plan MUST carry a `## Risks` section before `## Implementation Steps`, so known breakage modes and mitigations are visible before implementation starts.
- No file writes during design exploration (Steps 1-3)
- If the user declines to save, skip Step 5 — the plan remains conversation-only
- Frontmatter MUST be English. Body content can be Korean.
- `base_branch`, `base_commit`, `branch`, and `worktree` are required execution fields
  on every new draft/active plan. Surgical lifecycle updates must preserve them.
- Inline `#` comments in frontmatter are NOT used (natural-language triggers replace them).

## Handoff mode (`/design handoff`)

Package the current session-bound plan so a fresh session or another agent can resume it with full context. **Writes nothing** — the canonical plan and its execution mapping remain the durable source of truth; the ephemeral binding is intentionally recreated by explicit select in the receiving session. This is the mid-execution counterpart to `pm next` (which kicks off a *backlog item* before implementation); handoff kicks off an *in-flight plan* mid-implementation, and Continue mode is its consumer.

1. Run read-only `resolve-session` with the exact injected tool/id. Unbound,
   missing, or terminal → report no in-flight plan and stop. A routing error is reported
   verbatim. Use the returned `execution_root` for all subsequent reads.
2. Branch on the plan's frontmatter `status`:
   - **`done` / `dropped`** (stale pointer) → report "not an in-flight plan (already terminal)" and stop; do not hand off.
   - **`draft`** (unapproved) → hand off, but put "⚠ this plan is still `draft` (unapproved) — reply `승인` in the fresh session before implementing" at the top of the prompt.
   - **`active`** → normal handoff.
   - **any other / unknown status** → report "invalid plan status" and stop (the lifecycle only creates draft/active/done/dropped; this is a guard).
3. Extract from the plan: `id` / `title` / `status`, Goal, Verifiable Success Criteria, Risks, and the `## Implementation Steps` split into **done (`- [x]`)** and **remaining (`- [ ]`)**. If zero steps remain, put "all steps complete — run `/verify` then `/retro` in the fresh session" in the prompt instead of a resume pointer.
4. For a pm-loop plan (`pm_loop: true`), pull the owning task's links + memory via `pm get <id>` (id == plan slug). **On `pm get` failure / item-not-found (linkage drift)** → note that fact and continue with a plan-only handoff (do not stop). Skip this step for a standalone (`pm_loop: false`) plan.
5. Emit a paste-ready kickoff prompt containing the mapping and rooted resume commands:
   `codex -C <execution_root>` and `cd <execution_root> && claude`, plus `/design continue`.
6. Copy the prompt to the clipboard (`pbcopy`; `wl-copy`/`xclip` on Linux), then tell the user to paste it into the fresh session and stop. **If clipboard access fails, do NOT claim it was copied** — print the prompt inline (fenced) and tell the user to copy it manually.

## Continue mode (`/design continue`)

Resume the in-flight plan in THIS session.

1. Run `resolve-session` with the exact injected tool/id; re-anchor the session to its
   `execution_root`. Unbound/missing or a routing error stops with the exact remediation.
   Never consult main launcher state or continue from main.
2. Branch on frontmatter `status`: `draft` → unapproved, so request `승인` (a draft plan is not implementable per the Rules) and stop / `done` · `dropped` (stale pointer) → report and stop / any other · unknown → report "invalid plan status" and stop.
3. `active`:
   - **Unchecked `- [ ]` steps remain** → summarize the done steps, locate the first unchecked step, and resume implementation from there (honor the existing Rules: flip `- [ ]` → `- [x]` as each lands; implement only against the active plan).
   - **No unchecked steps remain** (all `- [x]`) → implementation is complete. Do NOT create new work or re-run steps. Route the user to `/verify` then `/retro` to close it, and stop (the `done` transition is /retro-exclusive per the Rules).

## Status Update Triggers (post-creation)

After this session is bound to a `draft` plan, watch for explicit user replies that promote or conclude it:

| User trigger       | Action                                         |
| ------------------ | ---------------------------------------------- |
| `승인` / `approve` | Assert the mapped execution root, then `pm approve <KEY> <id>`; the journal changes plan + item together. |
| `취소` / `cancel`  | `pm complete <KEY> <id> --plan <path> --status dropped --reason "<why>"`; the journal terminals plan + item before exact pointer cleanup. |

**Atomic mirror:** never edit plan status directly. PM-loop plans use the commands above.
Standalone plans use `pm approve --standalone --plan <path>` and
`pm complete --standalone --plan <path> --status dropped`. Both use the shared journal.

> The `done` transition is **delegated to `/retro`**. `/retro` Phase 5 closes the plan + item via the `complete` transaction together with `## Post-Implementation Notes`. Do NOT add a `완료` / `done` natural-language trigger here.

> A parked plan becomes eligible through explicit `pm select --plan <path>` after its
> mapped target current is validated. Never hand-edit the launcher pointer.

**Hard rules:**

- Trigger fires ONLY when `resolve-session` returns this session's validated plan with status `draft` or `active`. If the session is unbound, treat the reply as normal conversation unless the user supplies an explicit plan — do NOT consume main launcher state.
- NEVER infer status changes from context (e.g., "looks done", "I think we finished"). Status changes ONLY on the explicit trigger words above (or `/retro` for the `done` path).
- NEVER change status silently. Always confirm in the response: "✅ status: draft → active".
- Terminal commands clear only pointers whose exact content equals the terminal plan;
  unrelated main/worktree selections survive.
- During implementation, update checkboxes only with
  `pm plan-step check|uncheck <plan> <number>`; never edit checkbox lines directly.
