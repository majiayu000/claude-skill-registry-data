---
name: feature
description: >
  Use this whenever the user asks to "implement", "add", "build", "create",
  or "modify" a feature, page, view, component, or module in this Vue
  project. Three phases: Phase 0 scope analysis (flows + edge cases + UI
  needs + plan validation, STOP for user), Phase 1 implementation (layered
  UI → Store → API, Vue 3 Composition + Vuetify 4, /ui design rules), Phase
  2 Definition-of-Done checklist + /verify + /pull-request. Auto-runs
  /create-module if the target module doesn't exist.
---

# Feature Skill

## Phase 0.0 — Issue Claim (if invoked with `#N`)

**When this section runs:** only if the invocation provides a GitHub issue number, e.g. `/feature #1153`. Skip entirely for `/feature <freeform-spec>` (no issue to claim — proceed directly to Phase 0).

### 1. Read the issue state

```bash
gh issue view <N> --json number,title,state,body,createdAt,assignees,comments
```

If the command fails (issue not found, network down, missing scope) → **STOP** and surface the error to the user before proceeding. Do not silently fall through to the claim step.

If `state` is `closed` → **STOP**, ask the user (working on a closed issue is almost always wrong).

### 2. Detect collision

Inspect `assignees[]` and the most recent comment whose body starts with `WIP —` (em dash U+2014, not a hyphen — only the canonical em-dash form is detected; hyphen variants `WIP -` are silently ignored):

| Situation | Action |
|-----------|--------|
| `assignees` contains `@me` (current GitHub user) | Continue silently — resuming own work |
| Most recent `WIP —` comment by `@me` (any age) | Continue silently — resuming own work |
| `assignees` empty AND no `WIP —` comment from anyone | Proceed to claim (step 3) |
| `assignees` contains user ≠ `@me` | **STOP** — surface "Issue #N already assigned to <user>. Take over? (y/N)". Wait for explicit user confirmation. |
| Most recent `WIP —` comment by user ≠ `@me` AND `<24h` old | **STOP** — surface "Issue #N has fresh WIP from <user> (started <ts>). Collision likely. Continue anyway? (y/N)". Wait. |
| Most recent `WIP —` comment by user ≠ `@me` AND `>24h` old | Stale claim — surface "Issue #N has stale WIP from <user> (started <ts>, >24h). Reclaim? (y/N)". Wait. |

"Current GitHub user" = `gh api user --jq .login`. Run inline each time `@me` is compared (the call is fast and read-only).

### 3. Claim

If detection passed (or user confirmed override), run **both** commands:

```bash
gh issue edit <N> --add-assignee @me

gh issue comment <N> --body "WIP — session $(date -u +%Y%m%dT%H%M%SZ)-$(uuidgen | head -c 8), branch <branch-name>, started $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

Where `<branch-name>` is the branch this `/feature` invocation will use (planned name, even if not yet created). If the branch isn't decided yet, use `branch TBD`. Posting a follow-up comment with the real branch name after `/pull-request` creates it is best-effort manual — the linked PR superseding the WIP comment is what matters in practice.

### 4. Aged-scope gate (re-validate before implementing)

The issue `body` is the **primary scope source** — read it, not just the title (issues are often filed well ahead of execution, and the intended scope lives in the description). Before coding:

- If the issue is **old** (`createdAt` older than ~7 days), or its body references files, symbols, or routes that no longer match the current codebase → **re-validate the scope**: check the referenced code, summarize the drift ("the issue says X, the code now does Y"), and present it to the user for confirmation before proceeding. A stale scope implemented as-written ships against a codebase that has moved.
- Fresh issue with matching references → continue silently.
- If the user aborts at this gate, roll back the FULL claim from step 3 — `gh issue edit <N> --remove-assignee @me` AND delete the `WIP —` comment just posted (`gh api -X DELETE repos/<owner>/<repo>/issues/comments/<comment-id>` — capture the id when posting, or take the last own `WIP —` comment). Leaving the comment behind would make step 2 treat the aborted claim as resumable on the next run.

### 4b. Non-interactive invocation (orchestrated runs)

When the invoker's brief declares a **non-interactive run** (an orchestrating
agent executes the issue headlessly — no human present to answer), every
STOP-and-ask in this skill becomes a structured final line instead of a
question:

| Interactive behavior | Non-interactive replacement |
|---|---|
| Collision prompt (any `y/N` row of the table above) | Emit `SKIP: collision — <detail>` and stop |
| `gh` command failure (step 1) or `state == closed` | Emit `STOP: claim — <error>` and stop |
| Aged-scope drift confirmation (step 4) | Emit `STOP: freshness — <drift summary>` and stop |
| Phase 0 "Present plan & wait for validation" | Satisfied by the issue body when the brief states the scope was validated upstream; insufficient scope → emit `STOP: scope — <gap>` and stop |

Never wait on a prompt in a non-interactive run. If the stop happens after
the claim (step 3) already landed, roll the claim back first (step 4's
rollback: `--remove-assignee` + delete the `WIP —` comment) so the aborted
attempt doesn't read as live work on the next run. Interactive sessions keep
the exact behavior above.

### 5. Proceed to Phase 0

Continue to scope analysis below.

---

## Phase 0 — Scope Analysis (interactive, before coding)

### 1. Identify target module

- Read `CLAUDE.md` for project conventions and stack patterns.
- Read `ERRORS.md` for known bugs and non-obvious pitfalls to avoid before coding.
- Which module? Default to **ONE** unless justified.
- **If the module doesn't exist** → run `/create-module` to scaffold it first, then continue.

### 2. Analyze flows & edge cases

For each user-facing flow this feature creates or modifies, identify:

- **Happy path** — standard success scenario
- **Error path** — what fails, what does the user see?
- **"Last one" edge** — last owner, last org, last member
- **Retry edge** — can the user retry after failure/rejection?
- **Multi-user impact** — who else is affected?

### 3. Check completeness

- Will every backend API endpoint have a corresponding UI?
- Every UI action has visible feedback (success + error)
- Feature works without mailer / without organizations enabled

### 3b. Minimal-code ladder (run before presenting)

Challenge every **mechanism** this change would introduce — a store field, a persisted flag, a composable, a wrapper component, a new field in the API contract. Stop at the first rung that holds:

0. **Does a product decision remove it?** — accept the cost, accept the failure, do nothing, or surface it to the user. This rung holds **only if the mechanism then disappears**; if the product still needs it (a message still has to be rendered, a state still has to be held), keep going down the ladder.
1. **Already in this codebase?** — reuse the composable, store or component.
2. **In the standard library?** — use it.
3. **A native platform feature?** (HTML input validation, CSS, a framework or design-system built-in) — use it.
4. **An already-installed dependency?** — use it.
5. **One line, a constant, or config?** — make it that.
6. Only then: build it, minimal.

**Persisted state is the expensive rung.** State that **outlives the session** — a persisted store slice, a `localStorage` key, an API field the backend retains and replays back — encoding a *policy* (a preference, a cap, a memo of a past failure) is not a code choice: code is deleted, persisted state has to be migrated or read forever. A transient request or response field is **not** this; only state that is retained or restored counts. Rung 0 is mandatory for it, and it needs an **explicit, blocking user confirmation in §4** before it is built — a yes on that specific state, never implied by the general plan validation.

**Never traded away** (lazy ≠ negligent): understanding the problem before picking a rung, validation at trust boundaries, error handling that prevents data loss, security, accessibility, and anything the user explicitly asked for.

### 4. Present plan & ask questions

**STOP and present to the user:**
- Flows identified (happy + error + edge cases)
- UI elements needed
- **Ladder outcome (§3b)** — the **selected rung** first (`<rung> — <what it resolves to>`, e.g. `1 reuse — existing composable`), then one line per rejected mechanism (`<mechanism> — simpler option <X> rejected because <reason>`). A change that adds a mechanism and rejects nothing means nobody looked.
- **Persisted state, if any** — name it and **wait for an explicit yes on it**; a general "plan validated" does not cover it, and it is not built without that yes.
- Open questions or scope decisions

**Wait for user validation before coding.** (Non-interactive runs: Phase 0.0
§4b — a validated issue body satisfies this step; never wait.)

## Phase 1 — Implementation

### 5. Module structure

Follow layered approach: **UI → Store → API**. Each layer references only the one below.

- Use Vue 3 Composition API + Vuetify 4
- Follow `/naming` conventions
- Follow existing module patterns
- When an edge case or bug affects more than one call site, fix the root cause once in the shared function (store action, helper, service) — not a guard repeated at each caller.

**Pass-through store actions:** a store action that only forwards an API call (one request, no branching, no derived computation, and **no state change after the `await`** — a reset or assignment after the call needs its error-path test, since coverage stays 100% while the failure case goes untested) needs no dedicated test beyond being exercised once in the module's store test — skip the separate happy/error-path block for it. Keep the store's own test file; only the per-action boilerplate goes. This is reachable under this repo's per-file coverage thresholds (`vitest.config.js`) without lowering or excluding anything, because a zero-logic action has no branches to miss; the coverage report (`/verify`) is the check. If an action can't clear the thresholds from a single exercising call, give it its own test instead of skipping coverage.

### 6. UI rules

**If the feature has visual components**, apply `/ui` skill guidelines (design-system, components, patterns references).

**Feedback:**
- No `console.log(err)` in catch blocks — the axios interceptor handles snackbar display
- Use `catch { /* interceptor handles */ }` or re-throw

**Destructive actions — confirmation proportional to impact:**
- Low impact (remove member): simple confirm dialog
- High impact (delete org/account): type-to-confirm with entity name

**Consistency** (see `/ui` patterns):
- Dialogs: `max-width="440"`
- Destructive buttons: `color="error"` + `variant="tonal"` (inline) or `variant="flat"` (in dialog)
- Primary buttons: `color="primary"` + `variant="flat"` + `class="text-none text-body-medium"`
- All buttons: `:class="config.vuetify.theme.rounded"`
- Role chips: `roleColor()` + `variant="tonal"` + `size="small"` + `class="text-capitalize"`

**Responsive:**
- Side-by-side layouts: `flex-column flex-sm-row`
- Data tables: hide non-essential columns on `smAndDown`
- Form buttons: `:block="$vuetify.display.xs"` or flex-wrap

**State & UX guards:**
- Forms with dirty flag → `beforeRouteLeave` guard
- Dismissible banners → persist in `sessionStorage`, not component data
- Active context → visually indicate (badge, border, chip)
- Generated links/tokens → copy button with clipboard API
- Dates: relative for recent ("2d ago"), absolute for historical ("DD/MM/YY")

## Phase 2 — Definition of Done

### 7. Self-review checklist

**Flow completeness:**
- [ ] Every API has a UI, every action shows feedback
- [ ] Destructive actions have appropriate confirmation
- [ ] Edge cases handled (last-one, retry, no mailer)

**Consistency:**
- [ ] Dialog widths, button styles, chips follow rules above
- [ ] Responsive layout verified at mobile breakpoint

**State:**
- [ ] Unsaved changes guarded
- [ ] Dismissible UI persisted correctly
- [ ] Active context visually marked

**Modularity:**
- [ ] Isolated in ONE module (or justified)
- [ ] No cross-module Store imports except `useAuthStore`/`useCoreStore`
- [ ] Tests added
- [ ] Tests: unit tests (`*.unit.tests.js`) for all changes, except a pass-through store action (see Phase 1 §5) which only needs to be exercised once in the module's store test. E2E (`*.e2e.tests.js`) only if the change affects a critical user flow (auth, org onboarding, invite/join).

**Error documentation:**
- [ ] If a non-obvious bug was fixed, document it in `ERRORS.md` (root of repo) with: symptom, root cause, fix

### 7b. Elegance check

For non-trivial changes: pause and ask yourself "is there a simpler or more elegant approach?" If the current implementation feels hacky, refactor before proceeding.

### 8. Run `/verify`

### 9. Run `/pull-request`
