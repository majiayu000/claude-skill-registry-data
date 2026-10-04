---
name: review-plan
description: Fact-check an implementation plan against the real codebase and first-party documentation, flagging inaccuracies with what / why / evidence and a severity tier. Use when the user wants a plan reviewed or validated for accuracy, runs /review-plan, or wants a plan checked against real code before implementing. Accepts a Beads issue, a filesystem path, or a plan pasted into chat.
---

# review-plan

Review a **plan** (not code) for **inaccuracies**, grounding every finding in the **real code** and
**first-party documentation**. The output is a write-up where each issue states *what* is wrong,
*why* it's a problem, and the *evidence* that proves it.

This is distinct from [[review]] (which reviews a code diff) and [[domain-model]] (which stress-tests
plan language against DDD/decisions). This skill answers one question: **does what the plan claims
about the system actually hold up against ground truth?**

## When to Use

- The user runs `/review-plan <bead | path | (pasted plan)>` or asks to validate a plan's accuracy.
- Before implementing a plan (e.g. a `forge-plan` / `plans/drafts/*.md` output), to catch false
  premises early.

## Step 1 — Resolve the input → the plan text

First match wins:

1. **Filesystem path** that exists (`plans/drafts/<slug>.md`, `plans/committed/…`, any file) → read it.
2. **Beads id** — `bd show <arg>` succeeds → review its description / design / notes / AC; if it
   references a plan doc (e.g. `plans/drafts/<id>.md`), read that too.
3. **Pasted / attached in chat** → use the plan content from the conversation.
4. **Nothing resolvable** → ask the user for a path, bead id, or to paste the plan. Do not invent one.

State which plan you're reviewing (source + one-line summary) before starting.

## Step 2 — Build the claim inventory

Extract every **checkable assertion** the plan makes about the system — these are what you verify:

- File paths, modules, functions, types, and their **signatures**.
- Claims about **current behavior** ("X already does Y", "Z returns …").
- **Data shapes / schemas**, config keys, env vars, CLI flags, commands, test names.
- **Dependencies / integration points** ("A calls B", "this hooks into C").
- **Library / external API behavior** the plan relies on.
- **Assumptions** stated or implied as fact.

Prioritize **load-bearing** claims — the ones the plan's approach depends on. You can't verify
everything; spend effort where being wrong would break the plan.

## Step 3 — Verify each claim against ground truth

For each claim, find evidence — prefer primary sources, in this order:

1. **Real code** — Glob/Grep/Read the referenced files/symbols. Does the file/function/type exist?
   Does the signature match? Does it actually behave as claimed? (Read the implementation, don't guess.)
2. **First-party docs** — `knowledge/` YAML, `README` / `AGENTS.md` / `CONTRIBUTING`, `package.json`,
   and the library's **official** docs (WebFetch official sources only — not blogs/SO).
3. **Git history** when a claim is about recent/historical behavior.

Rules:
- **Only flag an issue when you have evidence.** Cite it (`path:line`, a doc quote, command output).
- Separate **Confirmed** (proven wrong) from **Needs confirmation** (couldn't verify; suspect).
- Never assert the plan is wrong from memory — verify, or mark it unverified.
- Note claims you checked that are **correct** too (brief), so the review shows coverage, not just gripes.

## Step 4 — Classify & write findings

Severity (plan-accuracy adaptation of the harness tiers):

| Tier | Meaning for a plan |
|------|--------------------|
| **Blocker** | A false premise the approach rests on — if followed, the plan cannot work (symbol/file doesn't exist; API behaves oppositely; wrong data model invalidating the design). |
| **High** | A significant inaccuracy that causes a wrong implementation or major rework in a key step (wrong signature, missing dependency, misidentified integration point, step conflicts with real behavior). |
| **Medium** | An unverified assumption presented as fact, an outdated reference, or an underspecified area likely to be wrong. |
| **Low** | Minor/cosmetic: stale-but-harmless path, naming nit, doc typo that won't change the build. |

Each finding uses this shape:

```md
### [SEVERITY] <short title>  — <plan location, e.g. "Step 3" / heading>
**What:** <the specific claim in the plan that is inaccurate>
**Why it's an issue:** <consequence if implemented as written>
**Evidence:** <path:line / doc quote / command output proving it> — Confidence: Confirmed | Needs confirmation
**Suggested correction:** <the accurate statement, if known>
```

## Step 5 — Verdict & output

Print the full write-up to chat **and** save it to `reports/<slug>-plan-review.md` (derive `<slug>`
from the plan/bead; create `reports/` if needed). Skip the file with `--no-file` if the user prefers
chat-only.

Open with a summary line and counts, then the findings (Blocker → Low), then a coverage note:

```md
# Plan Review: <slug> — <plan title>
Source: <path | bead id | chat> · Reviewed: <date>

## Verdict: <SOUND | NEEDS REVISION | UNSOUND> — <#B>/<#H>/<#M>/<#L>
<1–2 sentences: the headline accuracy problem, or "claims check out">

## Findings
<the [SEVERITY] blocks, highest first>

## Verified as accurate (spot-checks)
- <claim> — `path:line` ✓

## Not verified
- <claim the codebase/docs couldn't settle, and why>
```

Verdict guide: **UNSOUND** if any Blocker; **NEEDS REVISION** if any High; else **SOUND** (Medium/Low only).

If the plan came from a Beads issue, log it: `bd comments add <id> "review: plan <verdict> — <#B>/<#H>/<#M>/<#L>"`.

## Exit Criteria

- [ ] Every load-bearing claim was verified against real code or first-party docs (or explicitly listed as not-verified).
- [ ] Each finding has what / why / evidence (cited) and a severity + confidence.
- [ ] A verdict with counts is given; write-up printed (and saved unless `--no-file`).
- [ ] No issue is asserted without evidence.
