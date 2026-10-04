---
name: review
description: Deep code review driven by a short interview. Read-only reader agents analyze the chosen scope per angle, the lead verifies every finding, and each point is routed to the skill that fixes it. Never edits the code.
argument-hint: "[scope or report path] [--deep]"
---

# Review

Analyze code in depth, say what is wrong or illogical, and route each point
to the skill that fixes it. The review never changes project code.

With a `docs/review/*/report.md` path, skip to step 5 on that report.

## 1. Interview

One question per message, in plain text and the conversation language. Wait
for each answer. Skip a question the request already answers. Offer your
suggestion each time.

1. What to analyze: the whole project, a folder, a feature, the current
   branch against its base, or a pull request.
2. What to look for: bugs, security, needless complexity, performance,
   consistency with what was planned (briefs, proposals, issues), another
   domain the user names, or all of them.
3. What worries the user in particular, or nothing.
4. Which model and thinking level for the readers. Default: the session's.
   Offer only what the harness allows (references/harness.md).
5. Consent: « Je lance N relecteurs en lecture seule sur <scope> : on y
   va ? ». N is one per chosen angle. This answer is the delegation consent;
   without it, review solo.

## 2. Readers

Launch one reader per angle, in parallel, read-only, through the harness
adapter in references/harness.md. Each receives: the scope (paths or diff
command), the angle's brief from references/angles.md, the user's worry,
and the planned work when the angle is consistency. Each returns only a JSON
array of `{severity, file, line, issue, evidence, fix_skill}`, where
`severity` is `critical`, `major` or `minor` and `fix_skill` is `ship`,
`issue`, `brief` or `propose`.

No reader available, refused consent, or a failed launch: review each angle
yourself, one after the other, and say so in one line.

## 3. Verify

The lead checks every finding before the report:

- open the cited file at the line and confirm the problem is real;
- read what calls that code: with GitNexus, when its index answers, use
  `context` and `impact`; otherwise a plain text search. GitNexus missing:
  recommend it once in one line, never require it. GitNexus failing: fall
  back to search without retrying it;
- reproduce with an existing command or a disposable check when cheap.

Mark each finding `confirmed` or `probable` with its proof, or drop it.
Count the dropped ones. With `--deep` and the user's consent, a second
reader may try to refute each finding before the lead decides.

## 4. Report

Write `docs/review/<YYYY-MM-DD>-<slug>/report.md` from
references/report-template.md, in the conversation language: findings from
most to least severe, a section for what is not logical, and for each point
the skill that fixes it. One checkbox per point so `next` sees what is left.
Render it with `scripts/render.py <report>` and give the path.

## 5. Next step

End with « On traite lesquels ? » in the conversation language. Offer, when
useful, to rerun one angle deeper or with another model. When the user picks
points, tick nothing yet: hand each picked point with its proof to Arsenal,
which runs the named skill with its own approval gates:

| Finding | Skill |
|---|---|
| a simple, local bug | ship |
| a problem to follow over time | issue |
| a missing feature | brief |
| a technical choice to settle | propose |

A point is ticked in the report once the skill that took it has delivered.

## Verify external facts

Before stating an external fact (a version, an API, a CVE, the behaviour of
a library), search first when the runtime offers web search: read the
`websearch` skill and run one quick search, then cite the source. Without
web search, mark the claim unverified.

## Execution policy

Readers only after the consent of step 1.5. No nested delegation, no hidden
advisor, no edits outside `docs/review/`. Never commit. Stop when the report
is delivered and the user has answered, or when the user stops.
