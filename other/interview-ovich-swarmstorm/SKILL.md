---
name: interview
description: Use when a person says "interview me" or asks to be interviewed about an idea or an existing design document (a board, a plan, a change) until it is understood the same way by them and the agent, or when another skill needs open decisions resolved one by one. Runs in chat and leaves the resolved decisions there, for the caller to write where they belong. Keeping the discussion as a document is brainstorm's, turning it into a plan is write-plan's.
---

# Interview

**The interview ends at shared understanding**: the person and the agent would describe
the object the same way, and every decision is agreed or deferred. Until then, keep going.

The object is a tree of decisions. Each is answered by what can be read or by the person.

**Throw ideas in as you go.** An option the person did not list, a consequence they did not
name, a neighbouring decision the conversation points at: one line, marked as yours, beside
the question it belongs to. The interview draws the person out; it also gives them something
to push against.

**Research every decision that rests on a claim about the world**: a tool exists, it works
with our versions, the industry does it this way. Read the official source, the
specification, the package as published, its types and its changelog, and how reputable
projects solve the same problem, from their sources. State the version read and the date.
A search result or a blog is where reading starts, never where it stops.

**One option, `experiments: yes | no`.** Ask it first, with your recommendation, when the
subject makes it plausible, and later the moment reading cannot settle a claim or the
person doubts a tool. On a yes, read `references/experiments.md`. The caller stores the
answer with its decisions.

**Before each question, read**: the code, the history, the existing documents. A question about a screen goes through the `point-at` skill first.

**One decision per message, in tree order**, a branch once its parent is agreed. What
reading settles is stated with its source, and the person confirms. Where a document says
one thing and the code another, the person chooses which holds. What reading leaves open
is asked: the decision with what it depends on, the question in one sentence, the
recommended option first and marked, each option with the trade-off that decides it, and
a closing line that takes a number or a rejection of the frame. A decision left unasked
is one the implementation makes silently.

**The short mode**, offered whenever the full interview would be skipped: three questions
at most, on the decisions that change an output (kind `contract`) only, each with the
recommendation first. Every decision it leaves unasked is closed as the agent's default,
and named so.

**Close in chat**, once understanding is shared: every decision with its status and source. The caller decides where
that goes. **The caller writes decisions as rows**: read `references/decisions.md`.
