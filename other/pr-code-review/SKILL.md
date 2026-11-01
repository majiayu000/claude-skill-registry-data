---
name: pr-code-review
version: "1.3.0"
user-invocable: true
description: "Dual-axis (Standards∥Spec) multi-perspective PR review with confidence ≥80 filtering, severity calibration, plan alignment, and optional GitHub/GitLab review comment. Best-of: Claude /code-review pipeline + mattpocock dual-axis + Superpowers plan/severity habits. Triggers — 「PR 代码审查」「审查这个 PR」「code-review」「/code-review」「审 PR」「pull request review」「双轴审查 PR」 / pr code review, review this PR. Do NOT use as a name alias for mattpocock code-review or Superpowers requesting-code-review."
---

# PR Code Review

> Portable PR review for open-skills. Combines Anthropic Claude Code **code-review** plugin flow (eligibility, multi-perspective, ≥80 confidence, permalink comments), mattpocock **Standards∥Spec** separation + fixed-point diff, and Superpowers **plan alignment / severity / strengths-first** habits. Platform-agnostic agent dispatch (no host model-tier hardcoding).
>
> Install: `npx skills add FuDesign2008/open-skills -g --skill pr-code-review --yes`

## When this applies

- User asks to review an open PR/MR, or `merge-discipline` Part R requires pre-merge review.
- **Skip** (state reason, do not comment): PR closed, draft, trivial/automated, or already reviewed by this skill this session/tip.

## Depth (`full` | `light`)

Callers (especially `merge-discipline` Part R) MAY pass `depth=full` or `depth=light`. **Default: `full`.**

| Depth | Behavior |
|-------|----------|
| **full** | Dual-axis Standards∥Spec; multi-perspective review preferred in parallel when the host supports it (current default process below) |
| **light** | Dual-axis Standards∥Spec on the pinned tip is still **mandatory**; parallel multi-perspective swarm is **not** required. Confidence ≥80 Critical/Important clearance and publish rules are unchanged |

Standalone user triggers without a depth parameter MUST use `full`.

## Process

1. **Eligibility** — Open, non-draft, needs review; not already reviewed this session on this tip. Else stop.
2. **Resolve depth** — `full` (default) or `light` from the caller.
3. **Pin fixed point** — PR/MR base ref, or user-supplied commit/branch, or `origin/<default-branch>` for merge candidates. Confirm ref resolves and three-dot diff vs tip is **non-empty**. Empty diff → abort (do not spawn perspectives).
4. **Resolve Spec source** (first hit wins): PR/issue body + linked tickets → user path → OpenSpec change delta / related `openspec/specs` → ask user → else Spec axis = **skipped (no spec available)**.
5. **Resolve Standards sources** — `AGENTS.md` / `CLAUDE.md` (root + dirs the PR touches), plus coding-standards docs if present. Optional smell baseline: [reference.md](reference.md) (repo docs **override**; smells are judgement calls, never sole hard violations).
6. **Summarize** — Short change summary (title, intent, diff shape).
7. **Dual-axis review** (**do not** merge-rank across axes):
   - **Standards axis** — Documented guidance breaches (cite file + rule); optional smell heuristics.
   - **Spec axis** — Missing/partial planned behavior; unjustified scope creep; wrong implementation of a stated requirement (quote spec/plan line). Skip entire axis if no Spec source.
   - **full only:** also prefer parallel perspectives (bugs-in-diff-only, blame/history, prior PR comments on same files, in-file comment guidance).
   - **light:** skip the mandatory parallel swarm; single-pass dual-axis is enough.
8. **Calibrate** — Each surviving candidate: severity **Critical / Important / Minor**, then confidence **0–100** (rubric below). **Drop scores below 80.** Map: Critical/Important usually land ≥75–100 if verified; Minor usually drops unless guidance-hard.
9. **Strengths** — If any, list briefly **before** issues (accurate praise builds trust in the rest).
10. **Re-check eligibility** — Still open / same tip before publish.
11. **Publish** — Comment via `gh` / `glab` (or report in-session if host forbids comment). Dual-axis sections in the comment; full-SHA permalinks. Templates: [reference.md](reference.md).

### Confidence rubric

| Score | Meaning |
|------|---------|
| 0 | False positive / pre-existing / fails scrutiny |
| 25 | Unverified / stylistic / not in guidance |
| 50 | Real but nit or rare |
| 75 | Likely real and important; or explicitly required by guidance/plan |
| 100 | Definitely real; evidence confirms |

### False positives to discard

Pre-existing; lookalike non-bugs; pedantic nits; linter/typechecker/compiler catchable; generic “more tests/docs/security” unless guidance/plan requires it; unchanged lines; intentional PR-scoped behavior.

## Host contract (`merge-discipline` Part R)

- Run against the **open PR/MR about to merge**, at the depth Part R selected (`full` or `light`).
- **Pass** → neither axis retains ≥80 **Critical** or **Important** issues (Minor-only or all scores below 80 = pass). Light depth MUST NOT weaken this gate.
- **Fail** → report fail to the caller. `merge-discipline` Part R owns fix → **re-review until clean** (or user **explicit** Part R skip / accept-residual 留痕) before Part D. Implementing findings alone is **not** a Part R pass.
- CI green / coverage skip is **not** a substitute.
- Do **not** require a full receiving-code-review loop to pass Part R.

## After feedback (optional pointer)

When acting on review comments (human or this skill): verify against the codebase before changing anything; no performative agreement; reasoned technical pushback when wrong; clarify unclear items before implementing. Full reception discipline is optional and **out of Part R**.

## Integration guide

- Strong-dep from `merge-discipline`; missing → abort with  
  `npx skills add FuDesign2008/open-skills -g --skill pr-code-review --yes`
- Do not rename to `code-review` (external name collision).
