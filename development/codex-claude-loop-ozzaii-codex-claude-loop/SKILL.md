---
name: codex-claude-loop
description: Use when driving a gated build loop where Claude orchestrates and Codex CLI implements — Claude plans and judges, Codex plans/implements from a persistent thread, with approve-the-plan and review-the-diff gates that refuse to be skipped. For delegating serious multi-file work to Codex instead of one-shot prompts.
---

# codex-claude-loop — the gated Claude × Codex build loop

Claude is the principal orchestrator; it rarely types product code. Codex CLI does the
hands-on implementation from **persistent threads**. The whole thing is bash around
`codex exec` — no framework, no MCP, no daemon.

## The cycle (one brief)

```
Claude writes a brief  →  Codex authors a plan (persistent thread)  →  back to Claude
   →  Claude APPROVES the plan (loop until tight)  →  Codex implements (same thread)
   →  Claude REVIEWS the diff against the plan (loop until clean)  →  cl_release
```

**The persistent thread is the trick:** the plan Codex authored carries into
implementation, so it implements *its own approved plan* with full context. The approved
plan text is also sent with the implementation instruction, so if a human edited and
re-approved the plan file, the file wins over what the thread drafted.

## How to run it

`source ${CLAUDE_PLUGIN_ROOT}/skills/codex-claude-loop/lib/codex-claude-loop.sh` then use
the phase functions, or call `bash lib/codex-claude-loop.sh <phase> …` directly. Config
via env (`CL_REPO`, `CL_IMPL_MODEL`, `CL_PLAN_MODEL`, `CL_REVIEW_MODEL`, `CL_SANDBOX`,
`CL_LOCK_TIMEOUT`).

0. **First run:** `cl_doctor` (codex/jq/git/sha256 present, the four codex capabilities
   the loop needs, repo + schema resolve).
1. **Codex plans:** `cl_plan <slug> <brief.md>` → writes `<slug>.plan.md`, opens a
   persistent thread, stores its id.
2. **Claude approves the plan** (judgment — YOU read it): read `<slug>.plan.md`. If tight,
   `cl_record_verdict <slug> plan approve "why"`. If not, re-brief and re-plan. Loop until
   the plan holds. Prompt yourself to *refute* it, not rubber-stamp it.
3. **Codex implements:** `cl_impl <slug>` → resumes the thread, writes code, runs tests,
   holds the writer lock, and records a success marker only if codex exited clean.
4. **Optional same-session follow-up:** `cl_prompt <slug> "<additional request>"` queues
   behind the lane's writer lock, resumes the exact stored thread, and prints Codex's
   response. It requires a successful implementation and makes re-review mandatory.
5. **Claude reviews the diff:** `cl_review_human <slug>` (rich review you read) — or
   inspect `git diff <base>` yourself. Judge it *against the plan*. Approve
   (`cl_record_verdict <slug> review approve "why"`) or send the blocking items back into
   the same thread with `cl_revise <slug> "…"` and re-review. Loop until clean.
6. **Release:** `cl_release <slug>` confirms both gates still hold for the tree as it is
   right now, and refuses otherwise. Then changelog, tag, merge, deploy (honor the
   project's own deploy gate).

`cl_status` shows where every slug stands. `cl_wave <slug> <brief.md>` advances one step
per call and returns **3** when it is your turn, **0** when both gates hold — re-run it
after each judgment rather than expecting it to block.

## Autonomous fallback (no orchestrator to gate)

When there is no Claude brain available to judge (e.g. usage cap spent), `cl_codex_gate
<slug>` stands in a **Codex adversarial reviewer** that emits a parseable verdict
(`schemas/verdict.schema.json`, defaults to `revise` unless confident). Use it to keep the
loop moving unattended — but a real orchestrator review is the standard.

## Rails (load-bearing)

- **One writer.** `cl_impl`, `cl_revise`, and `cl_prompt` share one lock; don't bypass it.
  Two Codex processes writing the same tree = corruption.
- **Never review a tree that is being written.** Both review paths refuse while the lock
  is held. To genuinely overlap review and implementation, give each lane its own
  worktree and its own `CL_REPO`.
- **Gates must refute, not rubber-stamp.** A gate that always approves is worse than no
  gate. Blocking items need concrete fixes, and `approve` with a non-empty blocking list
  is downgraded on disk.
- **A revise round is not closed by a matching sentence.** Every item you send back with
  `cl_revise` is kept and handed to the next review, which is told to judge it on intent.
  When you review, do the same: ask what the item was trying to prevent, then check the
  code prevents it. A change that satisfies the wording and misses the point stays blocking.
- **Approvals are bound to what they judged.** Editing the plan voids its approval;
  changing the tree voids the review approval. If a re-approval is refused, read the
  reason rather than deleting state to make it pass.
- **The plugin guards git publication.** Normal Claude Code Bash calls for `git commit`,
  `push`, `merge`, and `tag` are refused while a successful implementation is not covered
  by both current approvals. The standalone skill install has no hook; neither path binds
  a human terminal or deliberately wrapped git commands.
- **Verify model variants before architecting on them.** Set `CL_IMPL_MODEL` /
  `CL_REVIEW_MODEL` only to models you have actually confirmed behave as you assume.
- **Tail the log within a minute of launching any lane.** A bad flag makes `codex exec`
  die into its jsonl while you believe a lane is running.
- **First run = `cl_selfreview`:** have Codex adversarially tear apart THIS harness before
  you trust it.
- Honor the repo's own rules (branch protection, deploy gates, secrets never printed).

## State

`~/.codex-claude-loop/<repo>-<hash of its path>/` — plans, verdicts, thread ids, base
SHAs, JSONL logs. Outside the repo so it never pollutes a tree Codex is writing, and keyed
by path so two repos with the same basename never share approvals. Override with
`CL_STATE`.
