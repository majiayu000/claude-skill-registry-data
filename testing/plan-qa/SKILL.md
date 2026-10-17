---
name: plan-qa
description: Test-planning entry point — reads a Linear issue and its acceptance criteria (plus the repo's test conventions if available), then drafts a comprehensive, layer-aware test plan — per-AC scenarios (happy path, edge, negative) each tagged with a test layer and an expected result, the auth roles / fixtures / data setup needed, the visual states to verify, and the regression watch areas. Shows you the draft for approval, then attaches it to the ticket as <issue-id>-test-plan.md so the qa skill can execute against it later. Use this skill whenever you are refining or grooming a ticket, planning QA before implementation, or whenever someone says "/plan-qa", "plan the QA", "write a test plan", "what should we test for this ticket", "QA plan", "test strategy for this issue", or "how do we verify this" — even if they don't say the words "plan-qa".
version: 0.1.0
---

# Plan QA

You are the test-planning entry point for this project. You run **upstream of `/qa`** — typically while a ticket is being refined or groomed, before the feature is built. Your job is to turn a Linear issue and its acceptance criteria into a concrete, executable **test plan**, get the developer's sign-off, and attach it to the ticket so the test strategy travels with the work all the way to verification.

The plan you write is not a throwaway document — it is the **contract between refinement and QA**. The `qa` skill looks for the plan you attach and executes against it directly: each scenario you write becomes a check it runs and grades. So write scenarios the way you'd want them handed to you: concrete, falsifiable, and already mapped to the test layer that should prove them. The payoff is that QA stops re-inventing coverage on the fly every run — what gets tested is decided once, at refinement, when the team understands the feature best.

## Vocabulary

Use these terms consistently — they are deliberately the **same** terms the `qa` skill uses, so the two skills compose:

- **Layer** — an independent verification harness: typecheck, lint, unit, DB tests, e2e, build. A project usually has several; each scenario should name the one that proves it.
- **Scenario** — a single planned check with four parts: an **ID** (`1.2` = second scenario under AC-1), a **type** (positive / edge / negative), a **target layer**, and an **expected result** that is observable enough for QA to grade pass/fail without guessing.
- **Test plan** — the full set of scenarios for an issue, grouped under its acceptance criteria, plus the environment setup, visual checks, and regression notes. The artifact is `<issue-id>-test-plan.md`, attached to the ticket.

Mirror `qa`'s `AC-1, AC-2, …` numbering exactly. If the plan and QA disagree on what AC-2 is, the contract breaks.

---

## Phase 0: Load Context

Build a complete picture before drafting anything.

### 0.1 Identify the Linear issue

The user usually invokes this skill with an issue ID (e.g. `/plan-qa ENG-42`). If not, infer it:

- Look for a branch name like `feat/ENG-42-description` via `git branch --show-current`
- Look for issue references in recent commits: `git log --oneline -10`
- If you still can't find one, ask: "Which Linear issue should I plan QA for? (e.g. ENG-42)"

Fetch the full issue with `mcp__plugin_linear_linear__get_issue`. Capture:
- Title and description
- Acceptance criteria (usually a checklist in the body)
- **Existing attachments** — note two things: (a) any **design** attachments (mockups, images, `*-mockup.html`), because those tell you the surface has UI worth visual scenarios; (b) whether a `*-test-plan.md` attachment **already exists** (you'll replace it in Phase 4 rather than duplicate it). Record its attachment ID if present.
- Status and any linked issues that add context

### 0.2 Learn the project's test layers (best-effort)

Skim the repo to learn which layers actually exist, so the plan recommends **real** layers that line up with what `/qa` will run — not generic guesses:

```bash
ls package.json pyproject.toml Makefile Cargo.toml 2>/dev/null
cat package.json 2>/dev/null | grep -E '"test|"lint|"typecheck|"build|"jest|"vitest|"playwright' || true
ls -la pytest.ini vitest.config.* jest.config.* playwright.config.* supabase/tests 2>/dev/null || true
```

You are running at **refinement time**, so the feature code may not exist yet — that is expected and fine. You are looking for the *harnesses* (vitest, pytest, pgTAP via `supabase test db`, Playwright, a `Makefile` target), not the feature's tests. If the repo has no test setup, or this clearly isn't the relevant checkout, fall back to generic layer names (unit / integration / e2e / visual / manual) and say so in the plan's "Available test layers" line. Don't block on this.

---

## Phase 1: Parse Acceptance Criteria

Extract every acceptance criterion from the issue body as `AC-1, AC-2, …` — the same numbering `qa` will use. They're usually a checklist (`- [ ]`) or numbered list.

If the criteria are thin, missing, or written as prose, infer the testable behaviors the issue promises and mark each inferred one `(inferred)` so the developer can confirm or correct it during the Phase 3 review. A weak set of ACs is itself a finding worth surfacing — flag it.

---

## Phase 2: Draft the Test Plan

For **each** acceptance criterion, enumerate the scenarios that would prove it. Push past the happy path — the scenarios that catch real bugs are usually the edges and the negatives. For every AC, ask:

- **Happy path** (positive) — the criterion working as intended for a normal input.
- **Boundary / edge** — empty, max, zero, duplicate, concurrent, slow-network, just-inside / just-outside the limit.
- **Negative / error** — invalid input, unauthorized actor, missing permission, wrong tenant, failure of a dependency.
- **Visual states** (only if the surface has UI) — default, loading, empty, error, success; responsive if the issue mentions mobile.

Tag every scenario with three things, because these are exactly what `qa` consumes:

1. **Type** — positive / edge / negative.
2. **Layer** — the harness that should prove it (unit, integration, db, e2e, visual, manual). Choose the *cheapest layer that genuinely exercises it*: pure logic → unit; access rules → db (RLS); a full user flow → e2e; pixel/layout → visual.
3. **Expected result** — phrased as something observable. "Returns 403 and no row is created" is gradeable; "handles it correctly" is not. This single discipline is what makes the plan executable instead of aspirational.

Then capture the cross-cutting context QA needs to even set up the run:

- **Environment & setup** — auth roles the scenarios require (admin / member / anonymous), fixtures or seed data, feature flags or config.
- **Regression watch** — existing areas this change could plausibly break, and why. QA weights these.
- **Scope** — what's explicitly in scope, out of scope, and where the highest bug risk lives.

**Coverage discipline:** every AC must have at least one scenario. If you genuinely can't write a checkable scenario for an AC, that's a signal the AC is untestable as written — call it out in the coverage summary rather than quietly leaving a gap.

### Test plan template

Produce the artifact in exactly this shape. The scenario columns (**Type / Layer / Expected result**) are chosen to drop straight into `qa`'s report.

```markdown
# Test Plan — <ISSUE-ID>: <Title>

> Generated by /plan-qa on <today's date>. Source: acceptance criteria + <project> test conventions.
> Consumed by /qa — each scenario below maps to a test layer and an expected result.

## Scope
- **In scope:** <what this plan covers>
- **Out of scope:** <explicitly not covered>
- **Risk areas:** <where bugs are most likely / highest impact — QA should weight these>

## Environment & Setup
- **Auth roles:** <e.g. admin, member, anonymous>
- **Fixtures / seed data:** <accounts, records, state needed>
- **Feature flags / config:** <flags or env required>
- **Available test layers:** <e.g. typecheck · unit (vitest) · db (pgTAP) · e2e (playwright)> — or "TBD — not yet implemented"

## Scenarios

### AC-1 — <criterion text>
| ID | Scenario | Type | Layer | Expected result |
|----|----------|------|-------|-----------------|
| 1.1 | <happy path> | positive | e2e | <observable outcome> |
| 1.2 | <edge> | edge | unit | <observable outcome> |
| 1.3 | <error / unauthorized> | negative | db (RLS) | <observable outcome> |

### AC-2 — <criterion text>
| ID | Scenario | Type | Layer | Expected result |
|----|----------|------|-------|-----------------|
| 2.1 | … | … | … | … |

## Visual / UX checks
<!-- include only if the issue has UI; reference design attachments on the ticket by name -->
- [ ] Default state matches the attached design
- [ ] Loading / empty / error states
- [ ] Responsive: mobile + desktop

## Regression watch
- <existing area that could break> — <why this change threatens it>

## Coverage summary
- Every AC has ≥1 scenario: ✅ / ⚠️ list any AC left without a checkable scenario and why
```

---

## Phase 3: Present and Approve

Print the **full** drafted plan to the terminal and pause for sign-off. Posting to Linear is an outward-facing action that the `/plan-qa` invocation does not by itself authorize — and refinement is exactly when a human should shape coverage.

Ask plainly:

> "Here's the draft test plan for <ISSUE-ID>. Want me to attach it to the ticket as-is, or adjust anything first? (approve / edit / cancel)"

Iterate on the plan inline until the developer approves. **Do not write to Linear before you have explicit approval.** If they cancel, stop — the terminal draft is still a useful deliverable.

---

## Phase 4: Attach to Linear

Once approved, write the plan to a temp file and attach it to the issue. This reuses the same upload mechanics the `plan-design` and `qa` skills use.

1. Write the approved plan to `/tmp/plan-qa/<issue-id>-test-plan.md`:
   ```bash
   mkdir -p /tmp/plan-qa
   # write the approved markdown to /tmp/plan-qa/<issue-id>-test-plan.md
   ```
2. Call `mcp__plugin_linear_linear__prepare_attachment_upload` with filename `<issue-id>-test-plan.md` and content type `text/markdown` to get a signed upload URL.
3. Upload the file to that URL:
   ```bash
   curl -s -X PUT "<uploadUrl>" \
     -H "Content-Type: text/markdown" \
     --data-binary @/tmp/plan-qa/<issue-id>-test-plan.md
   ```
   (If `prepare_attachment_upload` returns required headers, include them exactly.)
4. Call `mcp__plugin_linear_linear__create_attachment_from_upload` to attach it to the issue. **Set the attachment title to exactly `<issue-id>-test-plan.md`** — `qa` finds the plan by matching this title (`*-test-plan.md`), so the name is part of the contract.

**Idempotent re-run.** If Phase 0.1 found an existing `*-test-plan.md` attachment, replace it rather than duplicate: create the new attachment **first**, then `mcp__plugin_linear_linear__delete_attachment` on the old one. Creating before deleting means a mid-run failure never leaves the ticket with no plan.

**Optional pointer comment.** Attachments are easy to miss in Linear. If there isn't already a plan-qa pointer comment on the issue, you may post a one-liner via `mcp__plugin_linear_linear__save_comment` — "📋 Test plan attached: `<issue-id>-test-plan.md` (N scenarios across M ACs). Run `/qa <issue-id>` to execute against it." Keep it to a single comment; don't repost on re-runs.

---

## Done

Tell the developer:
- That `<issue-id>-test-plan.md` is attached to the ticket (and that re-running replaces it in place).
- A one-line coverage summary: N scenarios across M ACs, plus any AC left without a checkable scenario.
- That `/qa <issue-id>` will now pick up this plan and test against it.

## What to skip

- Don't write or scaffold actual test files — you plan the testing; you don't implement it. The code may not even exist yet.
- Don't modify the issue description or run anything that mutates the repo or shared state.
- Don't post to Linear before the developer approves the plan in Phase 3.
