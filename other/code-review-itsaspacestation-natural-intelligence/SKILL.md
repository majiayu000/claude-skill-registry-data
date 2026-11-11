---
name: code-review
description: "Use when the user asks for a full review of a change, pull request, or merge request against the personal checklist, covering design, tests, performance, security, and correctness — including local changes before pushing or opening an MR/PR. Also use when the user asks to read, address, answer, or reply to reviewer comments or threads, to post findings as applicable suggestions on GitLab or GitHub, or to prepare a plan from reviewer feedback, on any forge, including GitLab merge requests through glab (MR discussions, unresolved threads, suggestion blocks, glab auth) and GitHub pull requests through gh (PR discussions, review threads, suggestion blocks, gh auth)."
---
# Code Review

> Based on "What to look for in a code review" by Trisha Gee (Java Champion, JetBrains) and [personal notes](https://cboudereau.github.io/bookworm/2023-01-23_Code_Review/)

## When to use

- User asks to review code, local changes before pushing, a pull request, or a merge request
- User asks for the review checklist
- User wants to assess the quality of a change
- User mentions design, readability, test coverage, security, or correctness concerns
- User asks what reviewers said, or to address, answer, or reply to review feedback
- User asks for a plan built from review comments

## Overview

Two sides of a review, both language- and forge-agnostic:

1. **Giving a review** — the built-in review, then the checklist below run by two
   subagents. Reviews reduce cognitive load, catch correctness issues, and share
   knowledge — not just find bugs.
2. **Answering a review** — the flow in "Answering review feedback". Read, preview,
   get approval, then write. Never write first.

Forge commands (reading threads, posting, resolving) live in [gitlab.md](gitlab.md) or
[github.md](github.md) per the [forge routing rule](../git-conventions/SKILL.md#forge-routing);
git rules in the [`git-conventions`](../git-conventions/SKILL.md) skill.

## Giving a review

Four steps, in this order. Do not start the checklist before step 1 has returned.
When the diff is under 50 changed lines, run step 2 inline instead of with subagents.

**Local target** (working tree, staged, or an unpushed branch — the common pre-push
review): diff via local git against the merge-base of the target branch, no forge
routing. Steps 1–3 unchanged; step 4 does not apply — the findings report is the
deliverable; fixes go straight to the working tree on request, no suggestion fences.

1. **Built-in review first.** Run Claude Code's built-in `code-review` skill (the diff
   reviewer for correctness bugs and simplification) on the same target, at the effort
   level the user gave, or medium when none was given. Keep its findings.
2. **Checklist with two subagents in parallel.** Dispatch two subagents in the same
   message, each with the diff target and its half of the checklist below:
   - Subagent 1: Design, Readability & Maintainability, Tests (items 1-16)
   - Subagent 2: Performance, Data Structures, Security, Correctness, Cross-cutting, Intent (items 17-40)

   Each subagent reads the actual code around every finding and returns one line per
   finding in the format below, prefixed with the item number; none without a `file:line`.
3. **Merge and report once.** Drop checklist findings the built-in review already
   reported, dedupe across the two subagents, rank by severity, and report in one
   message. Say which step each finding came from.
4. **Post after approval.** Once the user approves the findings report, post each finding
   as its own diff-anchored discussion: suggestion per the ladder below, prose fallback,
   assembled per the read-first rule; forge commands in the reference files, routed as above.

Quick bug pass without the checklist: spawn `ni:reviewer` — same one-line format, nothing else.

## Classification ladder

A finding posts as an applicable suggestion only when ALL hold: (a) the fix is
mechanical — final code for one contiguous span, no judgement left to the
reviewee; (b) the span anchors on kept or added lines inside the current diff —
deleted-line targets never carry a fence; (c) the note anchors **in the file the fix
changes** — a fence never rides a note anchored in another file; (d) it fits one hunk
and the forge's range cap. An **insertion** (new code, such as a missing test) is
still mechanical: anchor on a kept or added line of the target file adjacent to the
insertion point and include that line verbatim in the block — mechanics in the forge
reference file. Paste-ready code in a plain code fence is a failed suggestion, not
prose: when the body carries final code and the target file has a kept or added line
in the diff, post it as a suggestion there. Prose fallback is for genuine judgement
calls, or a target file with no kept or added line in the diff — and it still states
the concrete fix. Severity is orthogonal: a mechanical `bug` fix still gets a
suggestion. Anchoring errors: refetch refs once, retry once, then prose. One concern
per thread; a suggestion is a posting mechanism, never a licence for bigger rewrites.
When the defect shows in one file but the fix lands in another, the suggestion goes
on the fix's file; a one-line pointer on the defect's line may reference it.

**Read first, both directions.** No suggestion without the real file open.
Replacement lines are edited copies of the actual lines, exact indentation kept,
never regenerated from memory or from comment text alone. The posting step above
and the answering flow below both follow this rule.

**Own-thread resolution.** On re-review of a change with new commits, check each
thread you yourself opened: re-read the anchored span at the new head and the diff
since the finding was posted. When the posted fix, or an equivalent that removes the
defect, is present, reply with one line naming the fixing commit, then resolve the
thread. Own threads only — never resolve another reviewer's thread. Ambiguous: leave
open, no nag replies. An applied suggestion resolves the thread natively on GitLab;
this rule covers the manual-fix path and GitHub.

## Finding format

One line per finding. Location, problem, fix. No throat-clearing.

Format: `file:L42: <severity>: <problem>. <fix>.` Multi-file diffs always carry the file.

| Severity | Use for |
|---|---|
| `bug` | Wrong output, crash, security hole, data loss |
| `risk` | Works but fragile: race, leak, missing guard, perf cliff |
| `nit` | Style, naming, micro-optimisation. The author can ignore it |
| `q` | Genuine question. Use it instead of hedging |

Drop: "I noticed that", "it seems like", "you might want to consider", "this is just a
suggestion" (use `nit`), praise per comment (say it once at the top), restating what the
line does, hedging ("perhaps", "maybe", "I think": use `q`).

Keep: exact line numbers, exact symbol names in backticks, a concrete fix rather than
"consider refactoring", and the why when the fix is not obvious from the problem.

Examples:

- Not: "I noticed that on line 42 you're not checking if the user object is null before
  accessing the email property. This could cause a crash. You might want to add a null check."
- Yes: `src/user.ts:L42: bug: user can be null after .find(). Add guard before .email.`
- Yes: `src/order.ts:L88-140: nit: 50-line function does 4 things. Extract validate, normalise, persist.`
- Yes: `src/client.ts:L23: risk: no retry on 429. Wrap in withBackoff(3).`

Full prose instead of one line for: security findings (state the risk and a reference),
architectural disagreements (rationale needed), and an author new to the codebase who
needs the why. Write the paragraph, then resume the one-line format.

## Checklist

### Design

1. **Architecture fit** — Does the change align with the overall architecture and existing conventions?
2. **SOLID** — Are Single Responsibility, Open/Closed, Liskov, Interface Segregation, and Dependency Inversion respected?
3. **DDD** — Are domain concepts clearly named and properly modelled?
4. **YAGNI / KISS** — No speculative generality; prefer the simplest solution that works
5. **Code reuse** — Is there a refactoring or extraction opportunity to avoid duplication?

### Readability & Maintainability

6. **Understandability** — Can a new reader understand the intent without context?
7. **Naming** — Are names precise, consistent, and self-documenting?
8. **Happy path vs exceptional cases** — Are both paths handled explicitly and clearly?
9. **Configuration vs hard-coded values** — No magic constants; prefer named config

### Tests

10. **Coverage of new code** — Are all new branches and edge cases covered?
11. **Test intent** — Does each test name and assertion communicate *why*, not just *what*?
12. **Tests are code** — Apply the same quality rules (naming, readability, no duplication)
13. **Granularity** — Right level: unit > integration > end-to-end; avoid testing implementation details
14. **Edge cases** — Cardinality (empty, single, many), nullability, boundary values, error paths
15. **Limitations** — Are test limitations intentional and documented, or accidental gaps?
16. **Performance & security tests** — Are they needed? Are they present?

### Performance

17. **Requirements** — Does the implementation meet the stated performance requirements?
18. **Readability vs performance trade-off** — Only optimise when measurements justify it
19. **Network cost** — Are batching and call counts considered?
20. **Resource management** — Are connections, streams, and handles properly closed?
21. **Memory leaks** — Are data lifecycle and collection bounds controlled?
22. **Locks & race conditions** — Are shared resources properly protected?
23. **Concurrency vs parallelism** — Is the right model applied?
24. **Pool configuration** — Use safe defaults; only tune with evidence

### Data Structures

25. **Right choice** — Is the data structure appropriate for the access pattern and complexity (Big-O)?
26. **Pitfalls** — Watch for lazy evaluation traps, infinite streams, or iterator invalidation
27. **Optionality** — Is absence of a value modelled explicitly (Option/Maybe/Optional) rather than null?

### Security

28. **Automated checks** — Are dependency scanners (e.g. Dependabot) and SAST tools in CI?
29. **Dependency surface** — Are new dependencies justified and minimal?
30. **Regulatory requirements** — Does the change touch data subject to compliance rules (GDPR, PCI, …)?

### Correctness

31. **Wrong data structure** — Could the structure cause subtle bugs (e.g. set vs list, map ordering)?
32. **Race conditions** — Is concurrent access safe?
33. **Caching** — Are cache invalidation and staleness handled correctly?

### Cross-cutting Concerns

34. **Documentation impact** — Does the change require updating docs, ADRs, or READMEs?
35. **UI / error messages** — Are user-visible messages clear, actionable, and tested?
36. **Automated vs human review split** — Delegate formatting/style to linters; focus human review on design and logic

### Intent

Needs the originating request, ticket, or plan. When none is available, skip this category and say so in the report.

37. **Request coverage** — Does every requirement of the originating request, ticket, or plan have a change in the diff?
38. **Scope** — Does anything in the diff go beyond that request (scope creep, drive-by refactors, unrequested features)?
39. **Preserved behaviours** — Is every behaviour the request says to preserve still exercised by a test?
40. **Slice** — Does each commit land one behaviour end to end ([`plan`](../plan/SKILL.md#rules-for-both-routes)), tested through the public surface ([`tdd`](../tdd/SKILL.md))? Skip when the review target has no commits.

## Culture

- Share tooling: IDE configs, linter rules, and CI checks should be committed and consistent
- Reviewers should ask "Have you thought about…?" for security, edge cases, and docs — not just critique
- Prefer collaborative tone; a review is a knowledge-sharing session, not an audit
- Pair review option: a reviewer can write the missing tests as part of the review, as a follow-up to the findings

## Answering review feedback

Turn reviewer threads into a table preview of replies and code suggestions; write to
the forge only after the user approves the preview. The flow is always:
**read -> preview -> approve -> post + resolve**. Never write first. One approval
covers the whole write: the preview states, per thread, the reply and whether it
resolves; posting does both in one pass — never come back to ask about resolving.
First review with no reviewer threads yet: use the checklist above.

### Rules

1. Always preview and wait for explicit approval before any write to the forge.
2. Resolve every approved thread whose preview **Disposition** said `reply + resolve`.
   This is required, not optional, and happens in the same pass as the reply.
   Never unresolve, approve, merge, close, or delete anything: those stay the user's calls.
3. Follow the git rules in [`git-conventions`](../git-conventions/SKILL.md).
4. Quote the reviewer's comment verbatim in the preview. Do not paraphrase feedback.
5. Follow the read-first rule in the classification ladder before proposing any suggestion.
6. If a comment is unclear or technically questionable, say so in the preview instead of complying.
7. Write the preview to the session scratchpad by default. Write it into the repository only when the user asks.
8. One suggestion per discussion thread. Do not bundle unrelated changes into one note.
9. Comments may live on an **earlier** MR/PR while the fix lives in a follow-up.
   Reply and resolve on the one that carries the thread, not the one that carries the code.

### Preview format and after approval

Formats and the post-approval report: [answering.md](answering.md). Read it before
writing the preview.

### Red flags - the write is not finished

- Replies posted, resolve left for the user
- "Resolving is the user's call" — it was, at preview time, and they answered
- A second question about resolving after the replies are already up
- Every thread previewed as `reply only` with no outstanding item named
- Reporting note ids without saying which threads are resolved

**All of these mean: go back and resolve the approved threads now.**
