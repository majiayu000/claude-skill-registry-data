---
name: googly-eyes
description: Reviews pull requests and local diffs against Google's eng-practices code review guide (design, complexity, tests, naming, comments, style, consistency, documentation, every-line, context) and emits a ranked, principle-tagged finding list with rich local diff rendering. Optional follow-up step posts selected findings as a GitHub PR review. Invoke when the user says "googly-eyes this PR", "review by the canon", "principled code review", "Google-style review", "review this CL", or pastes a PR URL and asks for a code review. 👀
license: MIT
compatibility: Requires git and gh; PR-mode requires authenticated GitHub access. Terminal rendering optimized for ANSI-capable TTYs.
---

# googly-eyes

👀 Holistic Google-shaped code review. Emits a ranked, principle-tagged finding list with rich local diff rendering. Optional `post` step files selected findings as a GitHub PR review.

## Install

```bash
npx skills add xornivore/skills@googly-eyes --agent claude-code -y
```

## When to invoke

Trigger phrases the user types or says:

- "googly-eyes this PR"
- "googly-eyes #123" or "googly-eyes <pr-url>"
- "review by the canon"
- "principled code review"
- "Google-style review"
- "review this CL"
- After pasting a PR URL: "code review please"

Do not invoke for:

- Bug-hunting with confidence scoring — that is the `code-review` skill's job.
- Observability gaps — that is `observablip`'s job.
- Drafting documentation — that is `doxcavate`'s job.

## Pipeline

The order is fixed. When invoked, walk these six steps in order:

1. **Detect target.** See [Target detection](#target-detection) below.
2. **Phase 1 — Triage.** Always runs. Load [triage-heuristics.md](./references/triage-heuristics.md) and emit a triage block per [assets/triage-report-template.md](./assets/triage-report-template.md).
3. **Phase 2 — Focused review.** Dispatch per triage verdict. Load [phase2-bundles.md](./references/phase2-bundles.md).
4. **Merge, dedupe, rank.** Load [output-format.md](./references/output-format.md).
5. **Render.** Load [rich-rendering.md](./references/rich-rendering.md).
6. **Posting (optional).** Only when the user explicitly invokes `googly-eyes post`. Load [posting-step.md](./references/posting-step.md).

## Target detection

Three cases, evaluated in order — first match wins:

1. **Explicit PR ref.** If the invocation includes `#N` or a `https://github.com/OWNER/REPO/pull/N` URL, fetch:

   ```bash
   gh pr diff N
   gh pr view N --json title,body,author,number,headRefOid,baseRefName,url
   ```

2. **Branch with open PR.** If `git branch --show-current` returns a branch and `gh pr view --json number 2>/dev/null` succeeds, treat as case 1 with that PR number.

3. **No PR.** Diff current branch against base (default `main`, override with `--base REF`):

   ```bash
   BASE=${BASE_OVERRIDE:-main}
   git diff "$BASE"...HEAD
   ```

   Replace PR-title and PR-body inputs with the branch's commit-message log:

   ```bash
   git log "$BASE"..HEAD --pretty=format:"%s%n%n%b%n---"
   ```

Hard rules:

- Never silently switch modes mid-run. If both an explicit PR ref and a local diff are detectable, the explicit ref wins.
- If `gh` is not authenticated and a PR target is required, exit with a clear error pointing at `gh auth login`. Never fall back to local diff in that case — the user asked for a PR review.

Correct example:

> User: "googly-eyes #42". Skill fetches PR #42, runs Phase 1 + Phase 2, renders output with `Target: PR #42`.

Wrong example:

> User: "googly-eyes #42". `gh` is not authenticated; skill falls back to local diff and renders output with `Target: local diff vs main`. Violates "never silently switch modes."

## Phase 1 — Triage

Run one pass producing the triage report. Load [triage-heuristics.md](./references/triage-heuristics.md) for the size, scope-mix, description-quality, and specialty checks. Emit:

- One filled triage block from [assets/triage-report-template.md](./assets/triage-report-template.md).
- Zero or more finding records (T-1, T-2, …) for non-green verdicts, per [assets/finding-record-template.md](./assets/finding-record-template.md).

Hand the filled triage block and its findings to Phase 2 as structured input.

## Phase 2 — Focused review

Decision rule on Phase-2 dispatch, read from the triage size verdict:

- `small` → single-pass review. Run all four bundles' prompt content in one model context.
- `medium` or `large` → dispatch four parallel sub-agents, one per bundle, using the prompt templates in [phase2-bundles.md](./references/phase2-bundles.md).

Each sub-agent (or the single-pass run) returns YAML finding records matching [assets/finding-record-template.md](./assets/finding-record-template.md).

## Merge, dedupe, rank

After Phase 2 returns:

1. Pool triage findings (T-…) and Phase-2 findings (F-…).
2. Dedupe per `(file, line ± 2, principle)`. Keep highest severity; concatenate non-redundant `why` clauses.
3. Rank per [output-format.md](./references/output-format.md).
4. Apply per-severity caps.
5. Render per [rich-rendering.md](./references/rich-rendering.md).

## Output

The rendered output has six blocks, in this order:

1. Header line: `👀 googly-eyes review — <target> @ <SHA>`
2. Triage block (from triage-report-template.md)
3. File map (per output-format.md)
4. `## Required (N)` followed by required finding records
5. `## Optional (M)`, `## Nit (K)`, `## FYI (J)`, `## Praise (P)` in that order
6. `## Next step` — one of: post selected findings, split CL, iterate locally

## Hard rules

### 1. Never post without explicit user confirmation

Render every comment exactly as it will appear on GitHub. Wait for explicit approval before any `gh` write. No batch auto-post.

Correct:

> "Here are the N comments I will post. Reply `confirm` to send."

Wrong:

> Posting immediately after composing the review body.

### 2. Never invent code locations

Every finding's `file:line` must reference a line present in the diff. Structural findings cite the function header line.

Correct: `pkg/auth/oauth.go:42-58` where the function spans those lines.

Wrong: `pkg/auth/oauth.go:200` when the diff only touches lines 42-58.

### 3. Never fabricate the `why`

Each finding must trace to one of the ten Google principles, or to `small-cl` / `description` / `specialty`. No principle, no finding.

Correct: `principle: design`, `why: "This function has three unrelated reasons to change..."`.

Wrong: `principle: design`, `why: "Feels off."` — no Google principle reasoning.

### 4. Never recommend "clean it up later"

Per Google `pushback.html`, refactors and follow-ups are filed as bugs, not promises. Emit `optional` findings for things the author can defer; never accept "I'll fix it in a follow-up" as a resolution path inside the review.

Correct: `severity: optional, suggestion: "Consider extracting the helper now; if deferred, file an issue."`

Wrong: `severity: required, suggestion: "OK to address in follow-up CL."`

### 5. Triage before review

Always run Phase 1 first. Phase 2 reads from triage, never re-derives size or scope-mix.

Correct: Phase 2 prompt receives `triage.size = "medium"` as an input.

Wrong: Phase 2 sub-agent re-counts files and recomputes size.

### 6. Idempotent posting

Before posting, check for the existing idempotency marker on the PR. If present, require `--force`.

Correct: bail out with "Existing googly-eyes review detected; re-run with --force to replace."

Wrong: posting a duplicate review without checking.

### 7. Read-only by default

The review pipeline (steps 1-5) makes zero writes — no files, no git, no GitHub. Only the explicit `post` subcommand writes.

Correct: terminal output, no `git` or `gh` mutations during review.

Wrong: any `git commit`, `gh pr edit`, or file write during a review run.

### 8. Auto-detect target deterministically

Per the rules in [Target detection](#target-detection) above.

## Branding

Every user-facing surface that names the skill starts with the 👀 (eyes) glyph: header line, posted summary body. The glyph is brand-only — never inside finding `why` or `suggestion` fields.

## Reference index

| Step | Reference |
| --- | --- |
| Target detection | inline, this file |
| Triage checks | [references/triage-heuristics.md](./references/triage-heuristics.md) |
| Triage emit format | [assets/triage-report-template.md](./assets/triage-report-template.md) |
| Phase 2 dispatch and bundles | [references/phase2-bundles.md](./references/phase2-bundles.md) |
| Per-finding record schema | [assets/finding-record-template.md](./assets/finding-record-template.md) |
| Severity vocabulary | [references/severity-labels.md](./references/severity-labels.md) |
| Google principle definitions | [references/google-principles.md](./references/google-principles.md) |
| Pragmatic citations | [references/pragmatic-citations.md](./references/pragmatic-citations.md) |
| Ranking, dedupe, caps, file map | [references/output-format.md](./references/output-format.md) |
| Terminal rendering | [references/rich-rendering.md](./references/rich-rendering.md) |
| Posting to GitHub | [references/posting-step.md](./references/posting-step.md) |
