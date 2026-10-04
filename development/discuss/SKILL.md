---
description: Think a problem through with pi as a second opinion, over as many turns as it takes
disable-model-invocation: true
---

The user wants to talk through: $ARGUMENTS

Not a delegation and not a review — a conversation. pi writes nothing at all here; the
output is what it thinks, and the reason to want that is simply that it is a different
model and will not have made the same assumption you did.

Which means the one way to waste this: asking a question you already know the answer to and
reporting agreement. Use it where you are genuinely unsure, or where you want your own
reasoning attacked.

## The first turn

Write a task book to a temp file. Put the real question in it, along with the paths of any
files that matter — pi can read them, and a question about code it cannot see gets you an
answer about code in general:

```bash
DIR=$(mktemp -d)
cat > "$DIR/TASK.md" <<'EOF'
<the question, in full, with the constraints that actually bind>

Relevant files: <paths, or "none">

Answer in under 800 characters. Do not write or modify any file. If you disagree with a
premise in the question, say that first — it is more useful than answering the question as
asked.
EOF
echo "$DIR"
```

Dispatch with `pi_dispatch`: `task_file="$DIR/TASK.md"`, `cwd` = the repo root,
`tools="read"`, `mode="sync"`.

`tools="read"` with no write and no edit — there is nothing to write, and a discussion that
quietly edits a file is not a discussion.

The 800-character limit is not only context economy. A model given room to monologue will
fill it, and length reads as confidence whether or not any is warranted. A short answer is
easier to disagree with, which is the point.

pi's reply comes back as the verdict's `last_message`. If it says it was truncated, get the
rest with `pi_transcript session_id=<id> filter=text` — that reply is budgeted too.

## Following up

Keep the `session_id`. To continue, dispatch again with **`resume_session_id` set to it** —
pi keeps the previous turns, so the new task book carries only the new message, not a
re-statement of everything so far:

```
pi_dispatch(task_file=<new temp TASK.md>, cwd=<repo root>, tools="read",
            mode="sync", resume_session_id="<the id>")
```

Resuming is refused while a dispatch is still running, and refused for an id that was never
dispatched — in both cases loudly, with the valid ids listed. A silent fresh session would
mean a perfectly fluent answer from something that had forgotten the conversation.

Between turns, put the disagreement to it rather than the next question. "You assumed X;
here is why X does not hold" gets further in one turn than three rounds of clarification.

## Reporting back

Give the user pi's actual position, not a summary that sands off the disagreement. If pi
contradicts you, say so plainly and say which of you you think is right and why — that
judgment is the thing you are for, and hiding a disagreement behind "pi suggests
considering..." wastes the whole exchange.

If pi is simply wrong, say that too. A second opinion is worth having partly because it can
be checked, and a check you never report is a check you did not do.

## What this is not

It does not carry over into a dispatch. If the conversation lands on a plan, that plan
becomes a task book, written deliberately — pi's discussion session is not an instruction
to itself, and treating a conversation as an implicit contract is how a dispatch ends up
building something nobody agreed to.
