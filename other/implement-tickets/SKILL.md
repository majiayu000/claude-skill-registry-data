---
name: implement-tickets
description: Orchestrate implementation of local tickets in .work/tickets — load each initiative's reviewed research, design, and plan; work the dependency frontier; delegate and commit each aligned ticket; then review the whole run against the source documents.
disable-model-invocation: true
---

# Implement Tickets

You are the **orchestrator**. You do not ask the user questions and you do not stop halfway. You drive every actionable ticket in `.work/tickets/` to `done`, committing on the current branch as you go.

Optional argument: one or more ticket ids (`/implement-tickets 03 04`) restricts the run to those tickets and their unfinished blockers. With no argument, run every ticket that isn't `done`.

## Autonomy rules

<autonomy>

- **Never ask the user a question.** When an implementation detail is ambiguous but the source documents are consistent, pick the option most consistent with those documents and the existing codebase, proceed, and record the choice under `## Notes`. Never guess through a document conflict.
- Only stop early if the repo is not a git repo, `.work/tickets/` is missing or empty, or every remaining ticket is `blocked`.
- If a ticket genuinely cannot be completed (missing credentials, an external dependency that does not exist, a contradiction with the code that no reasonable assumption resolves), set its `status: blocked`, append the reason under `## Notes`, commit that status change, and move on to the next ticket. Never leave a ticket `in-progress`.
- Work through to the end of the frontier, then run the single final thermo-review, then report. The user reads the summary once, at the end.
- **Never implement from a ticket alone.** Its `context` documents are required input. Read them in order and treat a conflict or missing document as a blocker, not permission to guess.

</autonomy>

## 0. Preflight

1. Confirm you are in a git repo and note the **current branch** and the **base sha** (`git rev-parse HEAD`) — all work commits on that branch, and the base sha is what the final review diffs against. Never create branches, never push, never open a PR.
2. Run `git status --porcelain` and record any **pre-existing** modified files. They are not yours: never stage them, and exclude them from every commit you make.
3. Learn this project's commit conventions: read the project `CLAUDE.md` (and `~/.claude/CLAUDE.md`) and skim `git log --oneline -20` for the message style actually in use.
4. Identify the project's verification commands (test / typecheck / lint / build) from `package.json`, `Makefile`, `CLAUDE.md`, or CI config. You will run them after every ticket.

## 1. Load source documents and build the graph

Read every ticket file at the root of `.work/tickets/` and parse its frontmatter (`id`, `title`, `status`, `blocked_by`, `context`). The initiative documents live below that root and are not tickets.

For every unfinished ticket in this run:

1. Require `context` to name a repository-relative directory containing `research.md`, `design.md`, and `plan.md`. A missing field or document blocks the affected ticket.
2. Read those documents in order: research, design, then plan. Do this before claiming or delegating the ticket.
3. Check the ticket against all three documents. Its outcome must implement a plan stage, its acceptance criteria must preserve the researched constraints and design decisions, and its `blocked_by` edges must enforce the plan's prerequisite gates.
4. Reconcile a clear ticket-decomposition mismatch to the documents before implementation. If reconciliation requires a new product or design decision, set the ticket to `blocked` and record the exact conflict under `## Notes`.

The **frontier** is every ticket with `status: todo` (or `in-progress` left over from an interrupted run) whose `blocked_by` ids are all `done`. Work the frontier one ticket at a time, lowest id first — sequential, not parallel, so each ticket's commit lands on a clean base.

After each ticket completes, recompute the frontier. Stop when it is empty.

## 2. Per ticket

<ticket-loop>

**a. Claim it.** Set `status: in-progress` in the ticket's frontmatter.

**b. Implement it in a fresh agent.** Delegate to a subagent (`general-purpose`) with a self-contained prompt containing the full ticket body, the exact `context` path, the project conventions learned in preflight, and these instructions: first read `research.md`, `design.md`, and `plan.md` in that order; then implement the whole ticket including tests without violating their evidence, decisions, constraints, or execution order; do not commit; do not touch files unrelated to this ticket; report the files changed, how each acceptance criterion is met, and any document conflict. A fresh context per ticket is the point; do not implement it inline yourself.

**c. Verify.** Check the implementation against the ticket and all three source documents, then run the project's test / typecheck / lint commands yourself. If behaviour has drifted from the documented design or anything fails, fix it (directly, or via another subagent) until the implementation is aligned and the checks pass. Never mark a ticket done on a red build or an unresolved document conflict.

**d. Close it.** Set `status: done` and append a short `## Result` section to the ticket file: what was built and any assumptions taken.

**e. Commit.** Stage only the files this ticket touched plus its ticket file (`git add <paths>` — never `git add -A`, which would sweep in the pre-existing changes from preflight). Commit on the current branch.

No review here — the frontier runs straight through. Review happens once, in step 3.

</ticket-loop>

## Commit rules

- Follow the project's own conventions first — the style in `git log`, and anything `CLAUDE.md` mandates. Conventional-commit prefixes (`feat:`, `fix:`, `docs:`, `chore:`) unless the repo clearly does otherwise.
- **Small and focused.** One commit per ticket is the default; split into a few focused commits when the ticket contains genuinely separable steps (e.g. prefactor, then feature). A ticket never spans more than one branch and never leaves uncommitted work behind. The review fixes from step 3 land as their own final commit on top.
- Add a `Ticket: <NN>-<slug>` trailer so each commit traces back to its ticket.
- Include whatever trailers the harness or project requires (e.g. the `Co-Authored-By` line Claude Code appends).
- Commit only. No `git push`, no PR, no branch creation, no rebasing or amending of commits you did not make in this run.

## 3. Final thermo-review

Once the frontier is empty, review the **whole run at once** — one review, not one per ticket.

1. Compute the run's diff: `git diff <base-sha>..HEAD` using the base sha from preflight, excluding the pre-existing modified files you recorded there. If the diff is very large, split it by area (not by ticket) across a few reviewer subagents running in parallel.
2. Read `~/.claude/skills/thermo-review/SKILL.md`. Give each reviewer its source document set — research, design, and plan — plus the relevant diff and the review skill. Ask for document-conformance findings as well as concrete code findings, most severe first, each anchored to `file:line`.
3. Verify plan coverage across the complete diff: every planned outcome exists, prerequisite boundaries hold, researched constraints are preserved, and the implemented architecture, failure behaviour, load handling, performance characteristics, monitoring, and extension seams match the design.
4. **Fix everything** in scope of the tickets just implemented — including ambitious structural findings. A finding that spans several tickets is still in scope: it is the run's diff and documented initiative being reviewed, not one ticket in isolation.
5. A finding that is real but genuinely outside the run's documented scope does not get smuggled in: write it as a **new ticket file** in `.work/tickets/` (next free id, `status: todo`, with the same `context`) and note it in the summary. Do not implement it in this run.
6. Re-run the project's verification commands. Never finish on a red build.
7. Commit the fixes as a **single final commit** on the current branch (split only if the fixes are genuinely separable). Stage only the files you touched. Use a `Ticket: review` trailer instead of a ticket id, and list the tickets the fixes cover in the body.

## 4. Report

When the final review commit has landed, print a compact summary — nothing else needed:

- One line per ticket: id, title, final status, commit sha.
- Any tickets left `blocked`, with the reason.
- The final thermo-review: number of findings, what was fixed, its commit sha.
- Any follow-up tickets spun out of thermo-review.
- The verification commands you ran and their final result.
</content>
</invoke>
