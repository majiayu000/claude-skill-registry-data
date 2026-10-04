---
name: dotnet-techne-qa-pipeline
description: "Use when the user asks to verify a story or ticket implementation against its spec - per-AC verdicts, code reuse and design conformance, dead code, then adversarial maintainer verification. Requires the qa/review agent roles registered by scripts/install-codex.sh. Keywords: story QA, acceptance criteria, spec conformance, AC coverage, QA this branch, verify story."
license: MIT
compatibility: Requires a Codex CLI with multi-agent tools enabled (agents.enabled, default true) and the qa-* and review-maintainer roles registered in config.toml. Without the roles, fall back to the single-context dotnet-techne-story-qa skill.
---

# Story QA pipeline (multi-agent)

You are the orchestrator. Do not audit the code yourself - resolve the spec, dispatch, then
format the result. Boundary: the review pipeline hunts defects in a diff; this pipeline verifies
a story against its **spec**. Same branch, different question.

Paths below are relative to this skill's base directory. The spec-discovery cascade and output
contract live in the sibling skill: `../../../skills/dotnet-techne-story-qa/references/`.

## Step 0 - Check the budget, then the roles

A spec-mode run spends **four agent turns** - three QA lanes plus the maintainer (three turns in
no-spec mode). Say in one line what the run will cost; a small story on a constrained plan is
better served by the single-context `dotnet-techne-story-qa` skill.

List your available agent roles. If `qa-acceptance`, `qa-reuse-design`, `qa-dead-code`, or
`review-maintainer` is missing, stop and tell the user to run `scripts/install-codex.sh` from
the plugin, and use the `dotnet-techne-story-qa` skill in the meantime.

## Step 1 - Resolve target

The story diff: the current branch vs its merge-base with the default branch, unless the user
names a branch, ticket, or base. Slug the story (ticket key if known, else branch name).
Nothing to diff - halt and say so.

## Step 2 - Resolve the spec (cascade)

Follow `../../../skills/dotnet-techne-story-qa/references/spec-discovery.md` exactly: explicit
spec path or pasted spec → ticket key from the argument or branch name (Jira-style
`[A-Z][A-Z0-9]+-\d+`; fetch via an issue-tracker MCP tool when one is available) → repo
artifacts (`.episteme/DESIGN-*.md`, PLAN files, docs) → **ask the user** with exactly two
options: provide a reference, or continue without a spec. Never infer no-spec mode from a
missing path.

Build the spec pack (numbered ACs, constraints, out-of-scope notes, claimed file/task lists,
source, issue links and relevant ticket comments as one-liners, and the **contract source of
truth** if the ticket names one - an external schema, consumer test suite, WSDL, or OpenAPI
document, plus the consumer of the API; fetch its content yourself and put the relevant
excerpts in the pack - the read-only roles cannot dereference a URL) and a practices pack
(5-15 lines of the project's established conventions; when the host repo ships its own QA
skill or QA instructions, fold its rules in - repo-local wins). Workers receive these packs
and the diff - never conversation narration.

## Step 3 - Fan out

Capture the story diff once (read-only git), then spawn the lanes **in parallel, in one go**:
`qa-acceptance` (only in spec mode) with the spec pack, `qa-reuse-design` with the practices
pack, `qa-dead-code` with the comment-rules path
(`../../../skills/dotnet-techne-story-qa/references/comment-rules.md`; host-repo conventions
override it). Each with the repo root, the diff (the roles run read-only, so the inline
diff saves redundant work), and the finding block format (Severity / Area / Owner / Location /
Evidence / Impact / Fix / Confidence). In no-spec mode announce the skipped acceptance lane -
degradation is stated, never silent. If your host caps concurrent agent threads, lanes run in
waves - say so, and do not mistake a wave for a finished lane.

## Step 4 - Merge, then let the maintainer attack

Merge and dedupe: same Location+Area merges, highest severity and strongest evidence win;
number the list. Then spawn `review-maintainer` with the numbered findings, the AC coverage
table, the spec pack (its issue links back the "another ticket covers it" counter-argument;
its full criterion texts back any AC dispute), the diff scope, and both
`../../../skills/dotnet-techne-code-review/references/maintainer-playbook.md` and
`../../../skills/dotnet-techne-story-qa/references/falsification.md`. Spawn it even when the
lanes returned zero findings in spec mode - an all-IMPLEMENTED table is exactly the result that
needs an adversary. Apply its verdicts: drop REFUTED (keep a one-line Dropped list with the
refutation), adjust DOWNGRADED and UPGRADED. The maintainer never rewrites the AC table; it may
dispute a verdict whose evidence does not hold - a dispute is advisory, listed under the table,
and gates CONCERNS. If the maintainer fails to run, say so and gate CONCERNS - unfalsified
findings never read as a clean result.

## Step 4b - Run the suite (the roles cannot)

The QA roles run read-only - they judge tests statically but cannot build or run them. You can.
Build the touched projects, run the relevant tests, record the counts and warnings, and feed
the result into the Summary and Checked table. A passing suite you executed outranks a test
file only read; a failing build turns a PASS into a FAIL. Skip only when there is no runnable
project or the user says so.

## Step 5 - Gate, report, persist

Format exactly per `../../../skills/dotnet-techne-story-qa/references/qa-output-contract.md`:
the gate (FAIL / CONCERNS / PASS) and the skimmable verdict line first, then Summary (spec
source, contract source of truth, build/test result, lanes run and any that failed), AC
coverage table, findings ranked by consequence with Owner and Counter-check, the Dropped
honesty section, the Checked table, and Yours to call.

Persist the verdict to `.episteme/QA-<slug>.md` (create `.episteme/` if missing) with
frontmatter `target`, `spec_source`, `gate`, `date` - skip only if the user asked for
report-only. The QA changes no code: apply fixes only if the user asks afterwards (offering to
is fine). One narrow exception - comment findings (area: comments): offer to apply the
comment-line fixes (each finding carries the exact replacement line or "delete"), and apply
them yourself ONLY after the user explicitly confirms. The workers never edit.
