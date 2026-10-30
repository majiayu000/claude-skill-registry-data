---
name: review
description: >-
  Review and judgement router: evidence-based local code review, self-reflection,
  idea critique (roast, challenge), human-perspective checks (human-review, think-like-human),
  learning from outcomes (self-learning), and verification passes (verify,
  diagnosing-bugs). Use when the task is to critically evaluate work — yours
  or the agent's — or to run a structured review pass. One contract; the parts
  under parts/ carry the methods — open the ones the task needs.
---

# review — judgement router

> Home branch in Memora: `root/skill/review`.
>
> Boundary: client patches are out of scope — a retired patch set is not startup
> work, and patch history is read-only diagnosis when the owner asks for it.
> This router evaluates artifacts and claims; it does not revive client patches.
>
> Removed 2026-09-19 by owner order: rejudge, rejudge-diff, cross-eval
> (external LLM validation APIs). Answer 593 (2026-10-18) closed the last
> exception: there is no "second opinion per run" any more — every review is
> verified locally.

## Choosing a part

| Situation | Part |
|---|---|
| Technical code review / bug findings | Local code-review method below; matching `security` parts for security depth |
| Where the canonical truth on a question lives | `parts/relevance-scan/` |
| Pressure-test a product/business idea ("roast it") | `parts/roast/`; simulated perspectives are not independent evidence |
| Challenge an assumption or plan adversarially | `parts/challenge/` |
| Check work from a human user's perspective | `parts/think-like-human/`; `parts/human-review/` for interactive preview |
| Reflect on what went wrong / right after a task | `parts/self-reflection/`, `parts/reflect/` |
| Extract lessons into memory after outcomes | `parts/self-learning/` |
| Verify claimed work and delivery hygiene | `parts/verify/` |
| Debug a reported bug systematically | `parts/diagnosing-bugs/` |

Seven parts, all kept; load only the ones the task needs.

## Rules

- **Output shape: a compact prioritized list.** Each material finding gets
  `file:line`, the triggering scenario, the observed or source-traced cause, the
  impact and the suggested repair. No scores, no invented issues, no
  guaranteed-count quotas.
- **Local evidence only.** Tests, typecheck, targeted probes, reading the
  callers. No external reviewer API or proxy, no "confirm with another model".
  A suspicion stays a hypothesis until supported; severity follows actual
  consequences.
- **Forks go to `ask_questions`**: a material architecture or product change,
  conflicting requirements, a check that cannot run. Ordinary verified defects
  in scope are fixed and re-tested without a per-finding ceremony.
- **Lessons land in Memora** under `root/skill/review` as a node with `outcome`
  and a link to the incident — not in a flat log file.
- Review-only means findings, not automatic implementation. A clean bounded
  review does not certify the whole system.
- Read the method and the referenced executable source before relying on its
  tools; historical host paths and slash commands are not proof of capability.

## Related

`dev` (`verification-before-completion`, `systematic-debugging`), `challenge`,
`security`, `task-cycle`.
