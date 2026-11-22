---
name: adversarial-review
description: Run an adversarial two-phase code review of a change with TWO independent reviewers — Claude and Codex — who review alone, then cross-examine each other's findings, then Claude synthesizes a single weighted verdict. Use when the user says "/adversarial-review", "adversarial review", "review this with Codex", "get Codex to review", "two-reviewer review", "cross-examine this PR", or wants a second independent model to grade a change before merge.
---

# adversarial-review

Two independent reviewers grade the same change against a shared set of anchor documents, then
cross-examine each other before anything is reported. Reviewer A is **Claude** (run as an isolated
subagent so its Phase-1 context can't see the peer). Reviewer B is **Codex** (the `codex` CLI, run via
`codex exec`). You — the Claude running this skill — are the **orchestrator**, not a reviewer: you set
up the run, enforce the barrier between phases, and synthesize the two Phase-2 reports into one verdict.

This catches what a single reviewer misses: each model has different blind spots, and the Phase-2
cross-examination forces every finding to survive an adversary who is rewarded for refuting it. It is
read-and-report only — no GitHub posting, no push, no file edits.

It is heavier than `/code-review` (two models, four invocations, real compiles). Reach for it on
high-stakes changes — security-surface PRs, frozen-contract work, anything you want a second model to
sign off before merge — not routine diffs.

## Bundled files (in this skill dir)

- `review-prompt.md` — the verbatim two-phase reviewer prompt with `{{TOKENS}}` placeholders. **Do not
  paraphrase it** — both reviewers must receive the identical body so "BLOCK" means the same thing.
- `run-codex-reviewer.sh` — renders the prompt and runs `codex exec` with the right sandbox/cwd/writable
  flags. Used for the Codex side of each phase. `--help` documents every flag.

## Usage

```
/adversarial-review <target>
```

`<target>` is one of:
- a **PR number** — `/adversarial-review 1220` (resolve head SHA + base via `gh`)
- a **commit range** — `/adversarial-review dev..HEAD` or `87b3795..53c94cf`
- **`working`** — review the uncommitted working tree (staged + unstaged + untracked)
- empty — default to `dev..HEAD`; if that's empty on branch `dev`, ask whether `origin/dev..HEAD` is meant

## Prerequisites (check once, up front)

- `codex` on PATH and authenticated — `codex login status` should say "Logged in". If not, tell the
  operator to run `codex login` themselves (interactive; can't be done for them) and stop.
- `gh` authenticated if `<target>` is a PR number.
- A configured build dir for the platform under review, if you want Codex's empiricism (compiles/tests)
  to succeed under the `workspace-write` sandbox — it can't run network-dependent `meson setup` from a
  cold tree. See "Sandbox levels" below.

---

## Step 0 — Resolve the run (orchestrator, inline)

1. **TARGET.** Turn `<target>` into the full descriptor the reviewers need: repo path, head SHA, and
   diff range. For a PR: `gh pr view <n> --json headRefOid,baseRefName,title` → head SHA; diff range is
   `<merge-base>..<head>`. Compose a one-line TARGET string, e.g.
   `PR #1220 "<title>", repo /Users/<user>/Yuzu, head 53c94cf, diff 87b3795..53c94cf`.
2. **ANCHORS.** The authoritative ground truth severity is graded against. Pick them from the changed
   files via the CLAUDE.md routing table — e.g. a Guardian change pulls in
   `docs/yuzu-guardian-design-v1.1.md §24` + any frozen contract; an auth change pulls in
   `docs/auth-architecture.md`; everything gets `CLAUDE.md` + `docs/agentic-first-principle.md` (A1–A4).
   **If the anchor set isn't obvious, ask the operator** — a wrong anchor list silently mis-grades every
   blocking call. Format as a markdown bullet list (passed verbatim to both reviewers).
3. **REVIEW_DIR.** A shared scratch dir both reviewers read+write, e.g.
   `/tmp/yuzu-advrev-<short-slug>` (slug from PR number or range). `mkdir -p` it. Keep it OUTSIDE the
   repo so the git tree stays clean — `run-codex-reviewer.sh` passes it to Codex via `--add-dir` so the
   `workspace-write` sandbox can still write there.
4. Write a one-paragraph **scope note** to `REVIEW_DIR/TARGET.md` (target + anchors + range) so both
   sides and any later reader share the framing.

State the resolved TARGET, ANCHORS, and REVIEW_DIR back to the operator before launching.

## Step 1 — Phase 1: independent review (parallel, then barrier)

Launch **both reviewers concurrently**, in a single message with two tool calls. The standard pair is
Claude + Codex; an orchestrating skill may substitute Kimi through the bundled adapter below as long
as both reviewers receive the same prompt body, anchors, target, and phase barrier:

- **Claude side** — `Agent` tool, `subagent_type: general-purpose` (it needs Bash/Read/Grep for
  empiricism). Prompt = `review-prompt.md` rendered with `SELF=claude`, `PEER=codex`, `PHASE=1`, and the
  TARGET / REPO / REVIEW_DIR / ANCHORS resolved in Step 0. The subagent's isolated context IS the
  guarantee it can't peek at Codex's review. Tell it to write `REVIEW_DIR/claude.phase1.md` and return
  a one-paragraph summary + VERDICT.
- **Codex side** — `Bash`, **`run_in_background: true`** (Codex compiles/tests; it can run for many
  minutes — don't block the turn):
  ```bash
  bash .claude/skills/adversarial-review/run-codex-reviewer.sh \
    --phase 1 --review-dir "$REVIEW_DIR" --repo "$REPO" \
    --target "$TARGET" --anchors "$ANCHORS_MARKDOWN"
  ```
  (Add `--model <name>` to pin a Codex model, or `--sandbox danger-full-access` if empiricism needs it.)

**BARRIER.** Do not start Phase 2 until **both** `REVIEW_DIR/claude.phase1.md` and
`REVIEW_DIR/codex.phase1.md` exist and are non-empty. Poll the background Codex task / re-check the
files. If Codex's phase file is missing after it exits, read `REVIEW_DIR/codex.phase1.summary.md` to see
what happened (auth failure, sandbox-denied build, etc.) and surface it rather than proceeding with a
one-sided review.

### Kimi adapter and static-first mode

`run-kimi-reviewer.sh` writes `kimi.phaseN.md` and `kimi.phaseN.summary.md` using the same prompt and
schema. Its default is static and denies filesystem/search/write tools plus Bash. Trusted dynamic
mode requires
`--dynamic --i-trust-this-input`;
`--sandboxed-dynamic` routes Bash through the no-network Docker boundary and fails closed to static
when that boundary is unavailable. When Kimi replaces Claude, use `kimi.phase1.md`/`kimi.phase2.md`
at the barriers and use a fresh Kimi invocation for each phase. Kimi 0.17 restricts writes to its
workspace, so restricted modes require an excluded review directory inside the detached worktree;
copy that evidence to external scratch before removing the worktree. Restricted Kimi receives a
bounded materialized bundle (diff, relevant source context, anchors, prior reviews, and orchestrator
evidence) in its prompt; all filesystem/search/write tools and direct Bash are denied. Sandboxed
dynamic mode exposes only one fixed Docker collector through a fail-closed hook and returns its output
in the denied tool result.

An orchestrator may deliberately make Phase 1 a static safety gate before executing PR-controlled
code. Pass Codex `--static-only --sandbox read-only`, leave Kimi static, record the static synthesis,
and begin empirical work only after the trust gate. This explicit mode overrides the normal Phase-1
empiricism requirement; Phase 2 must ingest the separately recorded dynamic evidence and disclose any
remaining gap.

## Step 2 — Phase 2: cross-examination (parallel, then barrier)

Re-invoke **both** reviewers — **fresh** each, because all cross-phase state is on disk in REVIEW_DIR.
Same two-tool-calls-in-one-message pattern:

- **Claude side** — a NEW `Agent` call (not a continuation), prompt rendered with `SELF=claude`,
  `PEER=codex`, `PHASE=2`. It reads `codex.phase1.md` + its own `claude.phase1.md`, cross-examines, and
  writes `claude.phase2.md`.
- **Codex side** — `run-codex-reviewer.sh ... --phase 2 ...` (again `run_in_background: true`).

**BARRIER.** Wait for both `*.phase2.md` files.

## Step 3 — Synthesis (orchestrator, inline — this is YOUR job, not the reviewers')

Read `claude.phase2.md` and `codex.phase2.md`. Neither reviewer wrote a merged verdict; you do. Apply
this weighting — higher signal first:

1. **Dedupe.** Collapse `agrees-with-mine` / `confirmed-independently` cross-links into single findings.
   A defect both reviewers reached independently is the strongest class — rank it top.
2. **Weight by provenance.** `compiled` / `test-run` evidence outranks `static-read`. A finding one
   reviewer reproduced empirically and the other only argued from reading is graded on the empirical leg.
3. **Weight by anchor.** `contract` (cites an ANCHOR section) outranks `judgment`. A judgment-only BLOCK
   is reported but flagged as taste, not contract.
4. **Adjudicate disagreements.** Where they split on severity (`disagrees`) or one called the other
   `false-positive/unfair`, go to the cited code/anchor **yourself** and rule — show the line that
   decides it. Don't average; decide.
5. **Surface coverage gaps.** Cross the two FILES/COVERAGE lists. Any axis or file neither reviewer went
   deep on is an explicit gap in the final report — don't let parallel breadth hide a shared blind spot.
6. **Flag unresolved.** Anything left `not-verified` by both, or where you genuinely can't adjudicate,
   is reported as an open question, not silently dropped.

Produce the final report (and write a copy to `REVIEW_DIR/SYNTHESIS.md`):

- **Verdict:** `BLOCK` (any surviving CRITICAL/HIGH) or `PASS`, one sentence.
- **Consolidated findings**, ranked, each with severity, the winning provenance, anchor-or-judgment, and
  the minimal fix. Note for each whether it was found by both / one / surfaced only in cross-exam.
- **Adjudicated disagreements** — what split, how you ruled, the deciding evidence.
- **Coverage gaps & open questions.**
- **What each reviewer ran** (compiles/tests/CI) so the empiricism is auditable.

## Guardrails

- **Read-and-report only.** Neither reviewer nor the orchestrator posts to GitHub, comments, pushes, or
  edits source. The prompt forbids it; don't add a "post the findings" step unless the operator asks
  *after* seeing the synthesis (then it's `/code-review --comment` territory, a separate action).
- **Identical prompt body.** The only per-reviewer differences are SELF/PEER/PHASE and the shared
  TARGET/ANCHORS/REVIEW_DIR. Never hand one reviewer a different question than the other.
- **Independence is load-bearing.** The Claude reviewer is always a subagent, never you-the-orchestrator
  — you've already seen both sides, so you can't produce an uncontaminated Phase-1.
- **Sandbox levels (Codex).** `workspace-write` (default) lets Codex compile/test in the repo and write
  to REVIEW_DIR, but denies network — fine when a build dir already exists. If empiricism needs network
  or system access (cold `meson setup`, package installs), pass `--sandbox danger-full-access`, and only
  on a host the operator trusts. State which level you used in the synthesis so static-vs-empirical
  weighting is honest.
- **One-sided is not a review.** If Codex can't run (auth, sandbox, crash) and only `claude.phase*.md`
  exists, say so plainly and offer a single-reviewer fallback — don't dress a solo Claude review up as
  adversarial.

## Codex side — what `run-codex-reviewer.sh` does

Renders `review-prompt.md` → runs `codex exec --cd <repo> --sandbox <level> --add-dir <review_dir>
--skip-git-repo-check --ephemeral -o <summary>` with the prompt on stdin. Ephemeral + on-disk state
means Phase 1 and Phase 2 are independent process invocations — no Codex session to resume, matching the
protocol's disk-barrier model. Codex writes its full review to `REVIEW_DIR/codex.phaseN.md` itself; the
`-o` summary file is a fallback for diagnosing a run that didn't produce the phase file.
