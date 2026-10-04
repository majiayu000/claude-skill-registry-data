---
name: write-document
description: "Settles what a standalone document should be before it is written: whether a file is the right output at all, who consumes it (an agent, a third party, or the user), and which shape that consumer needs. Defers section order and house format to a more specific document skill whenever the session has one for that artifact. Invoked explicitly as `/write-document`, and applies on its own whenever a standalone document, plan, spec, handoff, analysis, report, runbook, or writeup is the deliverable. Not for chat replies, commit messages, PR bodies, or code comments, which the project's instruction files already govern."
user-invocable: true
---

# write-document

**Settle the consumer and the shape before the first line, then write to that consumer. Where the session has a skill for this specific artifact, that skill owns its format.**

A document fails in one of two ways, both decided before any writing starts: it is written for the wrong reader, or it should not have been a document. The steps below run in order and each one is cheap.

## When to Use

The deliverable is a standalone document: a plan, a spec, a design note, an analysis, an investigation writeup, a handoff, a runbook, a report.

It does not reach a chat reply, a commit message, a PR body, or a code comment. Those are prose the project's instruction files already govern, and routing them through here adds a step without changing the output.

## Inherited rules

The project's `AGENTS.md`, or the `CLAUDE.md` symlinked to it, governs every word this skill produces. This skill settles who a document is for and what shape that implies; it does not restate, relax, or replace the prose rules already in force. Where a shape rule here and a prose rule there both apply, both apply.

## Step 1: Confirm a document is the output

Explicit invocation settles this. The user asked for a document, so the step is a formality and the work moves on.

Reached on its own, the check is one question: does this need to outlive the conversation, or travel to someone who is not in it? A yes means a file. A no means the answer goes in the reply, because a document written to answer a question costs the reader a retrieval to reach a paragraph they could have read directly.

The call is not worth litigating. A wrong turn toward the reply is cheap to correct, and hesitating here costs more than an occasional short file does.

## Step 2: Name the consumer

The consumer is stated in one line before writing, because every decision after this one reads off it. A document with no named consumer defaults to a mixture of all three and serves none of them.

**An agent** reads a plan, a spec, an instruction file, or a sub-agent brief, and has to act on it without asking. It gets criteria and facts. Paths, commands, identifiers, and versions appear verbatim, because a paraphrased command fails in a way that is slow to diagnose. Motivation, narrative, and alternatives that were dropped change nothing about execution and come out.

**A third party** reads a deliverable or a handoff and cannot ask a follow-up before acting on it. They hold the high-level context of the work and not the specifics of the thing being documented, so orientation is a line or two and the specifics are the body. The document is complete on its own: nothing in it requires opening another file to follow, and related material is named in a closing references section rather than as a jump mid-sentence.

**The user** reads a plan they asked for, an explanation, or the result of an investigation, and needs the reasoning and the current state. It gets the logic, the working state, and what was decided along with what the decision rests on. This is the one consumer for whom the path to the answer is part of the answer.

Self-containment is not completeness. A third-party document holding every available fact is longer rather than more useful, and a reader who needs one more detail can ask for it. What survives is what the reader acts on, readable without leaving the page.

## Step 3: Check for a skill that owns this artifact

Before writing, look across the skills available in this session for one that covers this specific artifact: a report skill, a README skill, a spec or deliverable skill belonging to this repository. Where one exists it is read in full, and it owns the shape.

The split is fixed, so two skills never argue over the same file:

| Decision | Owner |
|---|---|
| Whether to write it, who consumes it, where it goes | this skill |
| Sections, their order, length, required fields, house format | the artifact's own skill |
| Wording, brevity, punctuation, formatting | the project's instruction files |

On a direct conflict about shape the artifact's skill wins, because it is the narrower domain and was written for that document. Neither skill restates the other's rules, since a copy drifts the moment one of them is edited and the stale copy is the one nobody notices.

With no such skill in the session, the consumer shape from Step 2 is the whole answer.

## Step 4: Write it

The answer comes first, then the support, then the detail, each part skippable. Depth is the reader's choice rather than a fixed ceiling, because a long document with a clear read path costs less to read than a short one that buried its conclusion.

Where more than one party appears, the acting party is named in every sentence about an action. An unbound "we", "you", or "they" makes the reader guess who does the work, and the guess is wrong often enough to matter.

Every claim is grounded in something on disk or in this session, and a figure appears only where the figure is the finding.

## Step 5: Check the finished file

- The named consumer could act on it without asking a question the document could have answered.
- Nothing in it records how it was produced: no session history, no plan or scratch paths, no tool or agent names, no note of which part came from where. The reader is receiving a result rather than a production log.
- Every identifier, path, and command is verbatim.
- Cutting one more sentence would lose something the reader acts on.

## Worked example

A writeup of a new authentication flow, for the team that will integrate against it.

Consumer: a third party. They know the product and the service; they do not know this flow.

```markdown
# Session authentication

Access tokens live 3 hours and refresh silently. A client holds one refresh token
per device and never sees the signing key.

## What a client does

1. `POST /login` with username and password, which returns both tokens.
2. Send the access token as `Authorization: Bearer <token>` on every request.
3. On a 401, `POST /refresh` with the refresh token, then retry once.

## What the server enforces

The server cuts a connection whose access token has expired, on its own timer.
Client-side refresh is convenience: removing it changes when a client notices,
never who can reach what.

## References

- Token envelope format: `internal/auth/token.go`
```

Two lines of orientation, the specifics as the body, and the pointer at the end rather than in the middle of the flow.
