---
name: github-tasks
layer: method
description: Track work as GitHub issues in this monorepo — create epics + child/sub-issues, label them consistently by package/app, and tie them into the commit workflow. Use when planning a feature, breaking work into tasks, or asked to "track this in GitHub", "make issues", "set up tracking".
allowed-tools: mcp__github__issue_write, mcp__github__sub_issue_write, mcp__github__issue_read, mcp__github__list_issues, mcp__github__search_issues, mcp__github__get_label, Bash, Read, Grep
---

# GitHub Task Tracking

The canonical task tracker for this repo is **GitHub Issues** (`FriendlyInternet/nuxt-crouton`). This skill defines how to create and label them consistently so every task maps to a real part of the monorepo.

## Write it as a hypothesis (assumption-first — the default for every epic & issue)

**Frame work as an assumption, not a task list.** A task says "do X". A hypothesis says "we think *if* we do X, *then* Y will happen — and Y is what we want", so later we can look back and honestly say whether we were right. It's more human, it forces the *why* and the *how-we'll-know* up front, and it's what the daily digest surfaces. Use it for **every epic and issue as much as possible**; only trivial chores (a typo, a dep bump) may fall back to a plain task description.

The hypothesis has **4 parts**:

1. **We think that** — *if* we [do/change X], *then* [outcome Y] will happen — and Y is what we want. *(the hypothesis)*
2. **We'll do that by** — [this, this, and that]. *(the work)*
3. **We'll be right if** — [these things turn out to be true]. *(success conditions)*
4. **We'll know by** — [measuring / checking these signals]. *(measurement)*

**It's a lens over the sections below, not a new competing heading.** Don't bolt a 5th section on — map the hypothesis onto what's already required:

| Hypothesis part | Lives in |
|----------|----------|
| 1–2 · the hypothesis + the work (plain) | the **👤 For humans** lead (open the body with "We think that…") |
| 2 · the work (precise) | the **🤖 For agents** block |
| 3–4 · we'll be right if / we'll know by | the **🧪 How to test** section (retitle it `## 🧪 We'll be right if / We'll know by` when it reads more naturally as the hypothesis's check) |

A good epic body therefore *opens* with a `## Hypothesis` block, then the 👤/🤖 sections expand it, then the check closes it. See epic #359 and #357 / issues #358, #360, #361 for worked examples.

## Writing for two audiences (REQUIRED — applies to issues, PRs, and commits)

Everything that lands in GitHub is written for **two readers**, in this order:

### 👤 For humans (first — and it must be genuinely easy to read)
Lead with this. Plain language a busy person skims in seconds: *what changed, why it matters, what to expect* — impact over mechanics. Short sentences, no unexplained jargon, no raw file paths unless they're the point. Use a **diagram only when it makes the change easier to understand** (a flow, a before/after, an architecture or state change). Mermaid renders in issue/PR bodies — use it there. **Never add a diagram for decoration**; if it doesn't earn its space, leave it out.

### 🤖 For agents
A precise, structured block an AI can act on without guessing: scope, exact files/paths and symbols, behaviour changes, acceptance criteria, follow-ups, links to issues/docs.

Use explicit headings (`## 👤 For humans` / `## 🤖 For agents`) so both are obvious. Scale to the change — a one-line human summary is fine for something small — but **always include both**.

## Record what you *didn't* do (Considered & rejected)

A **"why not" is as load-bearing as a "why"** — it's the evidence the chosen path beat *something*, with reasons that may later expire. Whenever a decision had genuine alternatives, **write them down**, so future-us (and agents doing archaeology) stop re-litigating settled questions and understand the *shape* of a decision, not just its outcome.

- Add a short **`Considered & rejected`** note — one line per option: `option → ❌ why not`. It lives in the **🤖 For agents** block by default (or its own small block, or a comment on the issue/epic).
- **Required only when alternatives were actually weighed** — trivial chores opt out (same as the hypothesis framing).
- The **epic** is the natural home for a cross-cutting "why not" — record it in the epic's **Decisions log** (below), *when the decision is made*, while the reasoning is fresh.

Worked example (from epic #392):
> **Considered & rejected — E2E perf**
> - Bump Playwright workers → ❌ the harness shares one dev server + SQLite *per job*; parallel workers race on mutated state → flaky.
> - Shared "build packages once" prebuild job → ❌ serialises a parallel matrix; saves CI *minutes*, not wall-clock.
> - Cache the built packages → ❌ a stale cache makes the regression smoke pass *falsely* — defeating its purpose.

## The epic's Decisions log (capture the call *when it's made*)

`Considered & rejected` catches the alternatives you weighed **when you write the issue**. But the decisions that leak worst are the ones made **halfway through the work** — "team-scope at the query layer", "layout composition is deterministic, not LLM", "fake the payment in the POC". At authoring time they don't exist yet, so no up-front section can catch them; by close they're lost to chat.

So every epic carries a running **`## 🧭 Decisions`** log — in the epic body, or a maintained pinned comment on the epic — that you **append to the moment a real design call is made**, mid-work, while the reasoning is fresh. It's the *same reflex* as updating a POC's `HANDOFF.md` / `spec.json` at a sign-off (the `spec` skill), pointed at the epic: one concept, two homes.

**The format** — newest at the bottom, one line per decision:

```
[YYYY-MM-DD] Decision → why → (Rejected: X — why not)
```

**Append-only — reversals are kept, never edited away.** This is the one deliberate difference from the POC `spec.json`, which *supersedes* (newest wins, prune the stale entry — "this is how it behaves *now*"). A decision log does the opposite: when a decision is later reversed, append a **new** line recording the reversal and the rule learned — don't touch the original. The reversal *is* the lesson, exactly as `AGENTS.md` demands ("negative results are first-class data — record the reversal and extract the rule, don't delete it"). A ledger that erases its own reversals is the re-litigation trap wearing a fresh coat.

**Keep it a habit, not a gate.** Like the hypothesis framing, this is a strongly-modeled convention with a worked example — *not* a required section and *not* hook-enforced. Decision capture dies the instant it's a box you tick to unblock a merge (you get "N/A" and "see chat"). Trivial epics opt out.

Worked example (a running log on an epic):
> ## 🧭 Decisions
> - [2026-06-14] Team-scope at the **query layer** (drizzle `where team_id`), not per-route middleware → one choke-point you can't forget to add on a new endpoint → (Rejected: per-route guard — trivially omitted on the next route added; Rejected: DB row-level security — D1/SQLite has none).
> - [2026-06-20] POC default layout is **deterministic** (`layout-compose.ts` rules), not LLM-generated → reproducible, reviewable, no token cost on every boot → (Rejected: LLM "place the blocks" — non-deterministic and slow, can't diff two runs).
> - [2026-06-28] **Reversed** the 06-14 call *for the reporting endpoints only*: they team-scope in **middleware** after all → their cross-collection joins made per-query scoping duplicative and error-prone → rule learned: query-layer scoping for single-collection reads, middleware for joins.

## How to test (REQUIRED on every closeable issue/PR — written for a human)

Every issue that changes observable behaviour, and every PR, MUST carry a **`## 🧪 How to test`** section written for someone who knows the *app concept* but not the code. It is not "run the unit tests" — it is *where a person clicks and what they should see*. Treat it as the acceptance check: if a non-developer can't follow it to confirm the change, it's not done.

Write it as:
- **What changed** — one or two plain sentences: what's different now vs. before.
- **Where you'll see it** — the concrete surface: the URL/page, the button, the screen. Name it the way a user would ("the top-right log-out button", "the access-code screen"), not by file or component.
- **Steps** — a short numbered walk-through, each step an action + the expected result. Include the **before/after contrast** where it matters ("previously the kassa still showed; now you land on the access-code screen").
- **Test data** — any PINs, logins, or seed URLs needed to reproduce (e.g. `/test1/nl/vlaamsekermis`, helper PIN `1234`).

Keep it tight and skimmable. A `mermaid` flow is welcome when the steps branch or the state change is the point — never for decoration.

### Epic acceptance rollup (the epic is the verification unit)

Sub-issues are the **work** unit; the **epic** is the **verification** unit. When all of an epic's sub-issues have merged (the feature has "landed in the app"), post a single **`## 🧪 Verify the whole thing`** comment on the epic *before closing it* — so the owner does **one** QA pass instead of hunting across sub-issues:

- **What landed** — one plain line per merged sub-issue/PR (what's now different).
- **Where to test** — the **one** link: the deployed preview or production URL, plus any test data (PINs/logins/seed URLs) needed.
- **Walkthrough** — the per-issue "How to test" steps **stitched into one ordered pass** a human runs end-to-end, with the before/after where it matters.

Close the epic **only after that pass passes** (or the owner confirms). This turns "a bunch of merged PRs" into a single "now go click these and confirm it all works" checklist for a non-technical owner. If a sub-issue couldn't be auto-verified (e.g. needs a device), say so explicitly in the rollup rather than implying it's confirmed.

### Human-action tasks: assign them, and close them when answered (REQUIRED)

**Not every task ends in a PR.** When something needs **the owner** to act — a visual sign-off, a decision, an approval, a manual run/deploy — capture it as a **discrete issue assigned to them**, *never* as a bare comment buried on another issue. The owner's **"assigned to me" filter is their entire to-do list**; an action that lives only in a comment is invisible to it. Trackers/epics stay **unassigned** — only actionable tasks carry an assignee, so "assigned" always means "you, now".

These tasks are resolved by a **comment/confirmation, not a merge**, so they need their own closing path — and it's the agent's job, not the owner's:

- **Close it the instant the action is confirmed done** — the owner says "looks good", the deploy goes green, the question is answered — in that *same turn*, and drop its `status:*` label. Then run the parent/epic walk-up below.
- An action **answered in a comment but left open is a tracking leak**: the assignee filter fills with done-but-open noise and stops being trustworthy. Closing travels *with* the answer, exactly as closing a leaf travels with its merge.

So an issue closes by **either** path — `Closes #NN` on a merged PR, **or** a confirmed human-action task the agent closes on the spot — and **both** then walk up the tree:

### Closing a child? Always check the parent (REQUIRED — do it the moment the PR merges *or the task is answered*)

A merged PR auto-closes the issues in its `Closes #NN` lines — but **a parent epic has no `Closes` line of its own, so it never auto-closes**, and a fully-delivered epic left open is the most common stale-tracking bug.

> **⚠️ An epic-integration PR uses `Refs #NN`, never `Closes #NN` (#1690).** That "an epic has
> no `Closes` line" is an *assumption this whole flow rests on*, not something GitHub enforces —
> and epic #1652 broke it: its integration PR wrote `Closes #1652`, so merging closed the epic
> instantly, skipping the `/close-epic` gate (step 4) and landing the postmortem *after* the
> close it was meant to precede. Write `Refs #NN` on the epic→`main` PR and close via
> `/close-epic`. **Sub-issue PRs keep `Closes #NN`** — the resume merge-on-approval step
> identifies the gate PR by exactly that string (#1663), so don't "fix" those too. CI warns on
> a closing keyword aimed at an `epic`-labelled issue (`warn-closes-blocked.yml`). So **the instant you close an issue — or a PR merges that auto-closes one — walk up the tree, unprompted.** Don't wait to be asked and don't defer it to a later task: closing the leaf is not "done" until you've checked the branch above it. Closing the epic travels *with* the merge that closes its last child — same logical step, not a follow-up someone has to remember.

1. Resolve the parent: `mcp__github__issue_read` (`method: get`) → `parent_issue_url`, or read the epic's `get_sub_issues`.
2. If the issue has a parent, check whether **all** of the parent's children are now `closed` (`get_sub_issues` → every child's `state`).
3. **If they are, the epic is ready to close — but the epic is the *verification* unit, so never silently close it.** Post the `## 🧪 Verify the whole thing` rollup (above) as a comment on the epic, then **explicitly ask the owner to close it** (e.g. "All N sub-issues are merged — close the epic?") and close it as `completed` **only on their confirmation** (or after the end-to-end pass passes). If a sub-issue couldn't be auto-verified (needs a device, a manual check), say so in the rollup rather than implying it's confirmed.
4. **Postmortem before closing (verify = *does it work?*; postmortem = *how did it go?*).** After the verify rollup and **before** the epic is closed, run the **`postmortem`** skill on the epic — it posts a retro (what went well / what was hard, evidence-backed / 1–3 improvement proposals) and offers to mint accepted, not-already-tracked proposals as `workflow` issues, and ends with a **`🔭 Next` handoff** — the next epic to start + a paste-ready next-session prompt — so closing one epic opens the next (#615). This is how the loop tightens over time (epic #403). Skip only for a trivial epic. Once the postmortem has run the epic carries `status:ready-to-close`, so the owner can close it in one gesture by commenting **`/close-epic`** on the epic (`close-epic-on-comment.yml`, gated on that label, #856) — the label is the precondition, so an epic whose postmortem hasn't run can't be closed this way.
5. Recurse: a parent can itself be a child of a grander epic — keep walking up until you hit one with open siblings or no parent.

Don't stop at the issue you were asked about; closing the leaf without checking the branch above it leaves the epic falsely "in progress".

**Recurring/standing chores are standalone, never epic sub-issues.** A ticket that's re-armed on a cadence and intentionally never permanently closed (e.g. the quarterly dependency sweep) must **not** be a sub-issue of a deliverable epic. A future-dated child that legitimately never closes silently defeats the "are all children closed?" check above, so a fully-delivered epic is pinned open forever and never reaches its verify + postmortem close-out — the most common stale-tracking bug, just slower to spot (the #233 → #244 case: the epic sat done-but-open for days behind the next quarterly sweep). File the recurring chore **standalone** (it may *link* the originating epic for context, not parent to it), and when it re-arms, open the next occurrence standalone too. (#422)

**Titles are human-first too.** Issue/PR titles read like plain English that anyone grasps at a glance ("Run the whole app on a Raspberry Pi and print directly"), not jargon ("node-server preset + in-process TCP drainer"). Keep the technical specifics in the 🤖 body, never the title.

## Core rules

1. **Every issue maps to a package or an app — never "root".** If it feels like root-level work (CI, deploy, ops), label it with the **app it serves** (e.g. CI that builds fanfare → `app:fanfare`). Harness / method work that serves the *whole* monorepo rather than one app — `.claude/**`, `AGENTS.md`, skill/agent/hook changes — maps to **`meta:agents`** (see rule 3). There is deliberately no `root` label.
2. **Exactly one `type:*` label** per issue — except an **epic**, which carries `epic` instead of a type.
3. **Component label = where the source actually changes** (mirrors the commit-scope convention):
   - `pkg:<name>` for package source (`packages/*`, e.g. `pkg:crouton-sales`)
   - `app:<name>` for app/deployment/ops work (`apps/*`, e.g. `app:fanfare`)
   - `worker:<name>` for `workers/*`
   - **`meta:agents`** for **harness / method** work with no single app or package owner — `.claude/**` (skills, agents, hooks), `AGENTS.md`, and cross-cutting method changes. This *is* the component for that work: it serves the whole monorepo, so it satisfies rule 1's "never root" rather than being an exception to it.
   - Package work that also lands a schema/config change in an app gets **both** (e.g. `pkg:crouton-sales` + `app:fanfare`).
4. Use meta labels where they apply: `epic`, `spike`, `needs-triage`.
5. **Link issues & PRs when talking to the user.** Any time you mention an issue/PR in a chat reply, render it as a clickable link to the full URL (`[#303](https://github.com/FriendlyInternet/nuxt-crouton/issues/303)`, `[#376](https://github.com/FriendlyInternet/nuxt-crouton/pull/376)`) so the owner can open it in one click. This is a **chat-reply** convention only — commit messages keep bare `(#NN)`, and PR bodies use `Closes #NN` (not a URL) so GitHub auto-closes the issue on merge.

## Structure

- **Epic** — one tracking issue per initiative. Body: goals, a checklist of workstreams, links to design docs. Labels: `epic` + the primary `pkg:`/`app:` it spans.
- **Child issues** — one per workstream, each linked as a **sub-issue** of the epic so GitHub shows a progress bar.
- Keep issue bodies tight: scope, acceptance criteria, links to `docs/`, and the required **`## 🧪 How to test`** section (above).

## How to create them (tools)

Issues, sub-issues, and labels are managed through the GitHub MCP tools:

- Create / update: `mcp__github__issue_write` (`method: create|update`, pass `labels: [...]`).
- Link a child under a parent: `mcp__github__sub_issue_write` (`method: add`, `issue_number` = parent, `sub_issue_id` = the child's **id** from its create response — not its number).
- Read / list: `mcp__github__issue_read`, `mcp__github__list_issues`, `mcp__github__search_issues`.

**Scan without overflowing the context.** A broad `list_issues` / `search_issues` (e.g. `labels: ["epic"]`, or a keyword search with no `in:title`) can return a 90k–140k-char blob that overflows the tool result and has to be sliced out-of-band — pure wasted turns. For any repo-wide scan (the dedup and epic walk-up steps are where this bites): pass **`minimal_output: true`**, keep **`perPage` small (5–10)**, and prefer **`in:title`** filters over broad body matches. Only widen when a narrow query genuinely misses.

**Labels must already exist** before you can apply them — applying an unknown label errors. New labels are added via labels-as-code (below), not by the API.

**Projects v2 boards can't be created or managed via these tools** (UI-only). Tell the user to create the board in the web/iOS app; if they enable the project's "Auto-add" workflow, issues you create land on the board automatically.

## Labels-as-code

The label taxonomy lives in **`.github/labels.yml`** and mirrors the workspace: `pkg:*` for every `packages/*`, `app:*` for every `apps/*`, `worker:*` for `workers/*`, plus `type:*` and meta labels. It's synced **non-destructively** by `.github/workflows/labels.yml` (`skip_delete`) on changes to `main` or via `workflow_dispatch`.

To add or change a label: edit `.github/labels.yml`, commit, and let the workflow sync it on merge to `main`. When a new package or app is added, add its `pkg:`/`app:` label here too.

## Fit into the task workflow

GitHub issues slot into the repo's task-execution flow (see `CLAUDE.md`):

1. **Check for existing work FIRST, then pick / open an issue** — the issue is the unit of work. Because sessions are ephemeral and a teammate (or a past you) may already have opened the epic/tasks, **always search before creating**. This is no longer a soft step: run the **`issue-dedup`** skill (it searches open **and** recently-closed work by `epic` label + keywords, surfaces matches, and forces a **reuse / replace / new** decision), and the **`require-issue-dedup` PreToolUse hook blocks any `issue_write` create whose body lacks a `Dedup-checked:` attestation line**. If a matching epic or task already exists, continue *that* one (assign yourself, set `status:in-progress`) instead of opening a duplicate. Only when nothing matches do you open a new epic + sub-issues for a multi-step initiative. (Then, when you *pick up* an issue, the sibling **`issue-sanity-check`** skill is your pessimistic go/no-go — see CLAUDE.md step 1.)
2. **Mark in progress — do this the moment you START, not after.** Apply the `status:in-progress` label (swap to `status:blocked` when waiting; remove the status label on close). **The label is the signal that moves the board:** `.github/workflows/project-status.yml` listens for the `status:in-progress`/`status:blocked` label and writes the Project's *Status field* (→ **In progress** / **Blocked**) via a PAT, since these MCP tools can't write Projects v2 fields directly (`list_issue_fields` is empty). PR opened → **In review** and merged/closed → **Done** are handled by the same workflow + the Project's built-in workflows. **Prerequisite:** the `PROJECTS_TOKEN` repo secret must be set — without it the workflow is a green no-op and nothing moves, so the label is the only signal and the board won't reflect it.
3. **Branch + do the work** — work on a feature branch; follow `CLAUDE.md` patterns; run `pnpm typecheck`.
4. **Commit** — use the `/commit` skill, referencing the issue in the body (e.g. `(#NN)`).
5. **Open a PR** — early is fine. Put `Closes #NN` in the body so the issue auto-closes on merge. Let CI run and fix failures (the PR can be watched/autofixed).
6. **Merge preserving commits** (merge/rebase — don't squash by default; squash only a noisy `wip`/`oops` history, per `AGENTS.md` § Commits → Merge policy) → the issue closes automatically and the branch is deleted. Don't push feature work straight to `main`.
7. **Walk up the epic tree (REQUIRED — part of the merge, not an afterthought).** The moment the merge auto-closes the leaf issue, run the parent check in *"Closing a child? Always check the parent"* above. If that merge closed the epic's **last** open child, post the `## 🧪 Verify the whole thing` rollup on the epic, run the **`postmortem`** skill (retro + improvement proposals — see step 4 there), and **ask the owner to close it** (close on confirmation). A merge is not "done" until the parent epic is either closed or explicitly handed off for the verify + postmortem pass. When watching/auto-merging a PR, do this walk-up as soon as the merge lands.

Work lands via **PRs**, not direct pushes to `main`. Issues are the source of truth for *what* to do; `docs/PROGRESS_TRACKER.md` (if used) becomes an optional phase-level rollup, not the per-task tracker.

## Quick reference

| Want | Label(s) |
|------|----------|
| New feature in a package | `type:feat` `pkg:<name>` |
| Feature touching a package + app schema/config | `type:feat` `pkg:<name>` `app:<name>` |
| App/deployment/ops/CI work | `type:chore`/`type:docs` `app:<name>` |
| Cross-cutting initiative | `epic` `pkg:<name>` (+ `app:<name>`) |
| Harness / skill / agent / method change (`.claude/**`, `AGENTS.md`) | `type:docs`/`type:chore` `meta:agents` (+ `epic` if an epic) |
| Time-boxed proof-of-concept | `spike` `type:feat` `<component>` |
