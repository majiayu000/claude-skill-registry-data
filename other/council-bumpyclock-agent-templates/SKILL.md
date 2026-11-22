---
name: council
description: Get review or feedback from three models at different providers. Use only when the user says 'council'.
---

# Council

Bring in three delegates for the user's request, usually review or feedback. Triage their findings. When this session owns the implementation, fix the valid findings and repeat until a round produces no finding you accept.

## Members

Use one strong model from each of three different providers, at high reasoning effort. If the user names members, use those. Otherwise pick the latest flagship model from any three providers or model families. Examples, not a fixed roster: fable (claude), 6.2-astra (codex), muse-wonder-full-1.0 (muse), Gemini Pro (antigravity) all at high reasoning.

In T3 Code, resolve the models with `orchestrator_capabilities`, then start one delegate per model with `delegate_task`. Elsewhere, use the harness's subagent tools or the providers' CLIs.

If a member or provider is unreachable, run the council with the members you reached. Name the missing member in the results. Do not fill the seat with a second model from a provider already on the council. If fewer than two providers are reachable, stop and report. One provider is not a council.

## Before a code review

When this session owns the implementation, first address outstanding PR comments, fix known issues, and run relevant checks. Delegates then review the updated implementation. Skip fixes to code the user plans to discard.

## Rounds

A round is one full review pass by every delegate, run in parallel.

Give every delegate the same brief:

- The request, the review target (diff, branch, files, or plan), and the intended scope.
- Read-only work for review or feedback.
- For a code review, a rubric and a score out of 10 against it. A 10 means ready to merge within the intended scope. Write the rubric before round 1 and reuse it unchanged in every round.
- For a UX review, the critique guidance. Invoke the `ux-designer` skill, read its critique guidance, and pass that guidance to the delegates.
- Findings ordered by severity, each with evidence. For code, the evidence is a file and line.

In round 1, leave out your own assessment and other delegates' findings, so the three reviews stay independent. From round 2, add what changed and the findings you rejected, with reasons.

When every delegate has returned:

1. Check each finding against the code. Accept it, or reject it as incorrect, out of scope, or a nitpick. Repeated rounds invite scope creep, and keeping scope limited is your job.
  1.1. For bugs, evaluate if it's an edge case and unlikely to occur or a valid finding that we should address. If it's an edge case or something extremely unlikely that can not happen then reject it.  Do not design for rare or future cases nobody asked about.
2. Report the round: each score, the accepted findings, the rejected findings with reasons, and disagreements between delegates. If a delegate gives no score, write `no score`. Do not invent one.
3. If this session owns the implementation, fix the accepted findings and start a new round. Do not edit files while a delegate is still reviewing the same checkout.

Run the rounds without waiting for user approval between them. Stop when a round produces no finding you accept, or after 5 rounds. If the request is feedback only, or this session does not own the code, run one round, report, and do not edit.

List out-of-scope findings that matter in the results. Do not fix them.

## Results

In the final reply, show the scores for every round, the fixes made, the rejected findings with reasons, and any missing member. Also list accepted findings that remain unfixed, with recommended next steps. These include every accepted finding of a feedback-only council, and findings accepted in round 5.

If this session's work has an open PR, also put the results in the PR description. Do not post a comment. Replace an existing council block. Put the block above any attribution line at the end of the description.

Format example. Copy the structure, not the names or scores. Keep the blank lines. Without them, GitHub shows the table as raw text.

```markdown
<details>
<summary>Council review</summary>

Rounds: 2

| Delegate | Round 1 | Round 2 |
| --- | --- | --- |
| Claude Opus | 7/10 | 9/10 |
| GPT Sol | 8/10 | 10/10 |
| Gemini Pro | 7/10 | 9/10 |

Fixed: one line per accepted finding.
Rejected: one line per rejected finding, with the reason.

</details>
```
