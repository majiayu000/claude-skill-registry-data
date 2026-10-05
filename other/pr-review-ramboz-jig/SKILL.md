---
name: pr-review
description: >
  Team baseline for PR and code review — produces scope, blockers, nits,
  and strengths. Auto-triggers when you say review this PR, check this
  diff, review these changes, pre-review before I share, what do you
  think of this PR, or review the diff on this branch. Defers to any
  other installed skill whose description identifies it as handling PR
  review, code review, or diff review — if such a skill is present,
  prefer it over this one (jig's version is a slim baseline). Does not
  defer to the generic built-in `review` skill. Do not use for:
  spec-compliance review of a finished slice (use
  `/jig:independent-review` instead); standalone architecture-doc review
  (use `/jig:arch-review`, or a richer installed arch-review skill, instead); single-line typo fixes
  or trivial whitespace changes (just merge and move on).
user-invocable: true
---

> Spec 012 introduced this skill as jig's **team baseline** for PR and
> code review. It is the first non-stub active jig skill that ships
> without a `.py` helper — pr-review is fundamentally a judgment skill,
> and the determinism it needs (`git diff`, file-type detection) Claude
> can run inline. If any other skill is installed whose description
> identifies it as handling PR review, code review, or diff review, the
> Claude Code skill router prefers that one over jig's baseline — the
> deferral is category-based, not name-specific, so a richer user skill
> named anything (`pr-review`, `code-reviewer`, `team-pr`, etc.) wins.
> Jig's slim version remains the auto-trigger when no such skill is
> installed.

## What this skill does

Produces a four-section markdown review of a pull request, a diff, or a
branch's accumulated changes:

1. **Scope** — a one-paragraph summary of what the PR is (new feature, bug
   fix, refactor, dep bump, etc.) and what it touches.
2. **Blockers** — concrete must-fix items. Each blocker has a file path, a
   line number, and a one-sentence rationale.
3. **Nits** — nice-to-haves and small polish items. Same shape as blockers
   but lower urgency.
4. **Strengths** — what the change gets right. Keeps tone constructive and
   surfaces patterns worth repeating.

The review is **breadth over depth**: catch the obvious across any
language/stack, leave the deep language-specific antipatterns to a richer
user-installed PR/code-review skill (or to a code reviewer with full
domain context). If you want multi-persona security/SRE/architecture
lenses, jig doesn't ship those — install a heavier skill at the user
scope and the router will prefer it.

## When to use vs. when to defer

There are three things people often confuse with this skill. Pick the right
one:

- **Any other user-installed PR/code-review skill.** Common location:
  `~/.claude/skills/pr-review/` — but the deferral is **category-based,
  not name-based**, so a skill named anything (`pr-review`,
  `code-reviewer`, `team-pr`, etc.) whose description claims PR review,
  code review, or diff review will be preferred. If one is present,
  **defer to it.** The Claude Code skill router should route to the
  more specific skill automatically; if you want to be sure, explicitly
  invoke it. The one exception jig's description carves out is the
  bundled `review` skill — jig:pr-review does **not** defer to that one
  (it's the generic fallback below jig's baseline, not above it).
- **`/jig:independent-review`** — a sibling jig skill for **spec-compliance
  review** of a finished slice (does the implementation satisfy the
  acceptance criteria of `spec.md`?). That's a spec-shape review against a
  written spec. This skill is a **PR-shape review** against a diff. Reach
  for `/jig:independent-review` when a slice is in REVIEWED-or-similar
  state with a spec.md to evaluate against; reach for this skill when
  there's a PR/diff/branch but no spec to compare against.
- **`agents/reviewer.md` (the reviewer subagent)** — different invocation
  primitive (subagent spawned via Task, not a skill). The subagent runs
  read-only and produces a structured verdict against a spec. Conceptually
  in the same neighborhood as `/jig:independent-review` (which builds the
  prompt the subagent reads), but distinct from this skill's PR-shape
  review.

Rule of thumb: **spec exists → `/jig:independent-review` or the subagent.
Just a diff → this skill (or the richer user one).**

## Inputs

Three input modes, ordered by richness:

1. **Full repo context (preferred).** You're inside a Claude Code session
   with the repo open. Run `git diff main...HEAD` (or the appropriate base)
   to get the diff. You can cross-reference the rest of the repo to check
   for duplicated logic, follow renames, examine related files, and verify
   that new code follows existing patterns. Highest signal.

2. **`land.py prepare --mode pr` output** (the artifact slice 007-01
   ships). When `/jig:slice-land` has run in `pr` mode, you get a PR body
   file and the branch name on disk. Read the PR body for stated intent
   and the diff for the actual changes. Still has repo context because
   you're inside the same session.

3. **Pasted diff or uploaded files.** No repo context. You can review
   shape, but you cannot verify whether similar logic exists elsewhere in
   the repo or whether the new code follows local conventions. Call out
   the limitations in the review header.

**Not supported by this baseline**: GitHub-PR-URL-only input (no local
repo, no MCP integration). Out of scope per spec 012's "GitHub MCP
integration deferred" decision. If the user has only a URL, ask them to
either open the repo locally or paste the diff. A richer user-installed
`pr-review` skill may handle URL-only input — defer to it if so.

## Scope discipline

Before writing any finding, apply scope discipline. A finding must be actionable
inside the PR's stated scope. Out-of-scope concerns are noise.

- **Different repo / system required** (worker, client SDK, infra, upstream spec):
  drop entirely or mention once in Scope as an "adjacent concern noted" — do NOT
  promote to Blocker or Nit.
- **Amendment to a parent spec, ADR, or design doc**: the spec is a contract for
  this PR, not a checklist to expand. Not a finding here.
- **"The PR should also document / specify / add X"** where X is a separate
  concern: separate PR, not a finding here.

Prophylactic expansion — demanding the author address every adjacent concern a
thorough reviewer template admits — is the most common AI-slop failure mode for
baseline reviews. Resist it.

## Review structure

For each PR, emit a markdown report with exactly these four H2 sections:

```markdown
## Scope
<one paragraph: what the PR is, what it touches, what it does not touch>

## Blockers
- `path/to/file.py:42` — <one-sentence rationale>. Required because <why>.
- (or: "None.")

## Nits
- `path/to/file.py:7` — <one-sentence rationale>. Nice-to-have because <why>.
- (or: "None.")

## Strengths
- <pattern or choice that's well done>. Worth repeating because <why>.
```

If a section is empty, write "None." rather than omitting the heading —
consistency makes the output scan-friendly.

### Worked example

Suppose the diff is:

```diff
+ def calculate_total(items):
+     total = 0
+     for item in items:
+         total += item.price * item.quantity
+     return total
+
+ def apply_discount(total, code):
+     if code == "SAVE10":
+         return total * 0.9
+     return total
```

A baseline review would read:

```markdown
## Scope
Adds two helper functions to the cart module: `calculate_total` and
`apply_discount`. Pure compute, no I/O, no side effects. Touches one
file; no tests added in this diff.

## Blockers
- `cart.py:8` — `apply_discount` has no test coverage and the magic code
  `"SAVE10"` is hard-coded. Required because pricing logic is a common
  source of regressions, and a future code change here would silently
  break the discount.

## Nits
- `cart.py:1` — `calculate_total` does no validation on `item.price` or
  `item.quantity` (e.g., negative quantities). Nice-to-have because the
  caller may or may not guarantee non-negative inputs.

## Strengths
- The two functions are pure and tiny — easy to test, easy to reason
  about. Worth repeating because most cart bugs come from mixing pricing
  logic with persistence.
```

Notice: no language-specific deep dive (no "use `Decimal` instead of
`float` for currency", no "this should be a `@dataclass`"). That depth
belongs in a richer user-installed PR/code-review skill, not the
baseline.

## Gotchas

- **A configured `review.pr_review_skill` (scaffold.json) is honored only in
  the orchestrated craft pass, not here.** Spec 096-01 / ADR-0040 D1 lets a
  project name its richer PR-review skill in `scaffold.json`; that key is read
  by `review.py` when it builds the **craft pass** prompt for the spec-workflow
  reviewer subagent. It is **not** consulted on this router-only interactive
  invocation, nor in `bug-fix`'s craft pass. Config honoring on those
  orchestrator-invoked surfaces is a tracked follow-up (ADR-0040 OQ1).
- **The deferral hint is the routing mechanism, not a code path.** Jig's
  description tells the Claude Code router "prefer any other installed
  skill whose description identifies it as handling PR/code/diff
  review." There is no filesystem probe, no plugin-precedence lookup,
  no name-matching against `pr-review` specifically. The deferral is
  category-based: a user skill named anything that claims the PR/code
  review surface area will win. If the router consistently picks jig's
  baseline over such a skill, jig's description is too greedy — open an
  issue. **This router-based deferral applies to _interactive_ use only.**
  The spec-workflow **craft pass** spawns a read-only `reviewer` subagent
  with no `Skill` tool, so it cannot use the router at all — there
  `review.py` does explicit file-read dispatch (detects
  `~/.claude/skills/pr-review/` and points the reviewer at it). See
  [docs/workflow.md](../../docs/workflow.md) § Post-implementation review.
- **The bundled `review` skill is explicitly excluded from the deferral.**
  Jig's description says it does **not** defer to `review`. That's the
  one carve-out; everything else in the PR/code review category wins
  over jig.
- **Lightweight is a feature, not a limitation.** The baseline does not
  ship language-specific reference files (Node, Java, Python, etc.). It
  does not run multiple personas. It does not check for security issues
  beyond the obvious. If you find yourself wishing the baseline did
  more, you are in the target audience for installing a richer skill
  at the user scope (commonly `~/.claude/skills/pr-review/`).
- **This is a PR-shape review, not a spec-shape review.** If a slice has
  a spec.md to evaluate against, use `/jig:independent-review` (or spawn
  the `agents/reviewer.md` subagent). Mixing the two surfaces leads to
  reviews that complain about ACs the diff isn't claiming to satisfy.
- **Fallback mode** (if the routing-dogfood in spec 012-01's DoD ever
  fails): the SKILL.md frontmatter gets `disable-model-invocation: true`
  and this skill becomes explicit-invocation-only (`/jig:pr-review`).
  In that mode, no auto-trigger fires — the user has to type the slash
  command. If you see `disable-model-invocation: true` in this skill's
  frontmatter, that's why.

## Relationship to other skills

- **`/jig:slice-land`** — emits the PR-shaped artifact this skill reviews
  (when run in `--mode pr`). The two skills compose: slice-land prepares
  the PR, pr-review evaluates the diff.
- **`/jig:independent-review`** — sibling skill, different shape.
  spec-compliance review against `spec.md`, not diff review. See "When
  to use vs. when to defer" above.
- **`/jig:contracts`** — orthogonal. Deliberate stub today (ADR-0002);
  if and when it activates, it will surface module-boundary violations
  that pr-review could call out as blockers.
