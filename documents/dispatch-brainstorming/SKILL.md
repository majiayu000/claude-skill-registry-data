---
name: dispatch-brainstorming
description: "Use in a session with Dispatch tools whenever a design conversation with a person starts: brainstorming or /brainstorming, \"let's design\", writing or changing a spec, writing an implementation plan, or a feature request or change that needs a person's choices. In a session with Dispatch it replaces superpowers' brainstorming and writing-plans; a Legion architect's own spec follows skill://legion-architect instead."
---

# Brainstorming in Dispatch

This skill governs a design conversation with a person, never a Legion architect's own issue
spec: an architect follows `skill://legion-architect` for that, even for a child issue.

In a session with Dispatch, such a conversation happens in its issue's spec, and the plan that
follows is a document on the same issue. This skill replaces superpowers' `brainstorming` and
`writing-plans` there, even when the user invokes one of them by name:

- No design question goes to chat. Every question is a decision block in the spec, and your reply
  in chat links the issue and asks nothing.
- There is no limit of one question per message. Every question that is ready goes out at once.
- There is no approval after each section, only the one at the end.
- A small change gets a short spec, never a design in chat: its size shortens the spec and changes
  nothing about where the conversation happens.
- No spec or plan file goes in the repository (`docs/superpowers/specs/`,
  `docs/superpowers/plans/`, `docs/plans/`): the spec is the issue's primary document and the plan
  is its `plan.md` document.

The brainstorming stages still shape what you ask: clarifying questions, then two or three
approaches with a recommendation, then the design section by section. A question that depends on
no open answer goes out at once, whatever its stage.

Read `skill://dispatch` before the first version: its "Writing a spec", "Decision blocks",
"Writing for the human" and "Approval of a spec" sections define the spec's shape, each block's
shape, and when approval is requested. A Legion phase worker never writes the spec; it sends a
decision to its architect (`skill://legion-worker`).

## Where the spec lives

Search Dispatch first, as `skill://dispatch-first` says. When an issue already tracks the work, its
primary document is the spec: extend it in place with `dispatch_doc_edit`, keeping the human's own
text. Otherwise create the issue with its first version as `spec`, in the project a search hit
already named or, when none does, the project the human names:

```ts
dispatch_issue({ project, title, spec })
```

No tool lists every project, so when nothing you found names one, ask the human in chat which
project the issue belongs in before you create it — a filing question with nowhere else to land
yet, not a design question, so it does not change "your reply in chat links the issue and asks
nothing" for the design itself. Never read the project from the environment, a configuration file,
or the Dispatch HTTP API: every read and write goes through a `dispatch_*` tool.

Before the first version, read the code and documents the design touches, so the facts you write
are ones you checked.

## Each turn

1. **Start with what is established.** The first version holds only what the conversation has
   established: the problem and its evidence, what the human has said in their own words, the
   facts the next questions need, and each question that is ready, as a decision block at the end
   of the section that sets it up. Write nothing past those questions: no design, no defaults you
   chose, no "what we will build", and no recommendation outside a decision block's own text. A
   point the human has not stated, however obvious it seems (what a word in the request means, how
   an edge case behaves, what a change does to an existing command), goes inside a decision block
   or stays out. This is stricter than `skill://dispatch`'s general rule for an inferred point
   elsewhere in a spec ("a point you inferred says so, with the reasoning"): in a live conversation
   nothing is settled until the human has seen it, so even a flagged inference waits for its own
   decision block.
2. **The human answers or comments.** Reply to each human comment in its thread
   (`dispatch_comment` with `reply_to`), then rewrite the passage the answer or the comment changes.
   Under an open ask whose next move is yours, such as the approval request you must revise or
   hand back, reply with `reply_to_ask` and `turn: "agent"` instead: a `reply_to` reply takes the
   default turn, which hands the request back to the human unchanged, and a call with a corrected
   `summary` is refused while it waits on them.
3. **Each next version folds the answers in and adds what they open.** Keep each answered
   decision block where it is, fold its answer into the surrounding text in the human's words with
   the date, recording the person as `skill://dispatch`'s "Writing a spec" says for a settled
   point. Then add the next sections, each with its question. Every question that is ready goes out
   at once, each as a decision block at the end of the section that sets it up; a question waits
   only when it depends on an answer still open.
4. **A comment that answers a question settles it** as surely as the block does. Fold it into the
   text at once, and close the block with `dispatch_resolve_ask` if the human has not.
5. **Request approval at the end, not after each section.** Once nothing in the spec is new to the
   human, request it exactly when "Approval of a spec" in `skill://dispatch` says: every decision
   block settled and folded in, the human has agreed to every point in the spec, and the current
   version is not yet approved (or waived, as that section's next paragraph covers). The request
   carries nothing new, as that section also says.

## Coming to terms

The conversation comes to terms in both directions. Explain what the code does today, plainly
enough for the human to react to and with each tool, event and route it uses named exactly (as
"Writing for the human" in `skill://dispatch` says), and ask; the human's model comes out of those
reactions, and so do corrections to it. Neither your model nor theirs is the starting truth.

## The plan

Once the spec is approved — or, when the issue needed no spec at all (a bug fix with no design
decision), once you have enough to plan from — the implementation plan is the issue's `plan.md`
document, never its spec and never a repository file:

```ts
dispatch_artifact({ issue, name: "plan.md", content })
```

Uploading `plan.md` again writes its next version. `writing-plans`'s content rules still apply in
full — file structure, task right-sizing, bite-sized steps, no placeholders, the header, and its
self-review — only where the plan lives changes: the issue's `plan.md`, never a repository file.
Technical choices inside the approved design are made in the plan and need no question. A plan
never changes a decision the human made in the spec: a change to one goes back to the spec as a
decision block, with the evidence for it.

Execution reads the plan the same way: `dispatch_doc_read({ issue, artifact: "plan.md" })` in place
of opening a plan file, then follows `executing-plans` or `subagent-driven-development` as it would
for a file on disk.
