---
name: factory-log
description: Keep a ticket's working state in one Linear working doc attached to the issue, without burying the operator in text. A short "Now" block at the top of the doc, rewritten in place, says where things stand and what the operator owes; below it sit the plan, state model, decisions, findings and learn rep. The issue description stays the operator's. The agent never starts comment threads.
argument-hint: "<now|plan|state|finding|decision|resolve|learn> [issue-id] (issue auto-detected from branch)"
---

# Factory log

Linear is the ticket's working surface, but moving agent prose from the terminal into Linear only relocates the overload. The operator should be able to glance at the issue and know two things: **where it stands** and **what they owe**. Everything else is available one click away and never in the read path.

All the action lives in one place, the **working doc**: a Linear document attached to the issue, so it shows on the issue without adding text to it.

| Part | Job | Who writes |
|---|---|---|
| **Now block**, the top of the working doc | Status, what the operator owes, what's blocked | Agent; rewritten in place, never appended |
| **Sections** below it | Prep, codebase, plan, state model, decisions, findings, learn rep | Agent; each section edited in place |
| **Comments**, on the doc (preferred) or the issue | The operator's answers, pushback, and learn-rep code | Operator. The agent only *replies* to a comment the operator started. |
| **Issue description** | The ticket itself: problem, scope, decisions the operator records | Operator. The agent doesn't write here. |

**Invocation input:** a kind, optionally followed by an issue identifier. If the identifier is omitted, auto-detect it from the branch (as `factory-submit.md` does). If none can be derived, ask.

## Configuration

`.factory-kit/linear.json` (legacy `.claude/linear.json` as fallback):

```json
{
  "agentLabels": { "group": "Agent", "working": "Working", "needsDecision": "Needs decision", "blocked": "Blocked" },
  "learnSurface": "local"
}
```

- `agentLabels` names a Linear **label group**, so the issue carries exactly one agent state. If the group is missing, say so once and point to `factory-setup-linear.md`.
- `learnSurface: "linear"` lets learn reps run on the issue. A client's workspace is client-facing, so the default is `"local"`.

## The Now block

The first thing in the working doc, separated from the sections by a rule. **At most 8 lines.**

```md
**Now:** <what is happening, one line>
**Needs you** (comment on this doc):
1. <question>? Reply `1 <a>` or `1 <b>`
2. <ask>: reply `2 go`

**Blocked:** <one line, or "nothing">

---
```

- **Rewrite it whole on every change.** Re-read the doc immediately before writing. Linear normalises markdown (`_x_` becomes `*x*`, collapsibles are stored as `>>>`), so match against the stored form, never against what you sent.
- Each item under **Needs you** is one line with a reply code. The operator answers with a comment like `1 neutral`, on the doc or the issue; read both. More than four items means you're asking too much: decide the implementation-level ones yourself (`factory-voice.md` § When to ask vs when to decide).
- Leave out sections that would be empty. With nothing owed and nothing blocked, the block is one line.
## The working doc

One Linear document attached to the issue, titled `<KEY-N> · Working doc`. Create it on the first write of any kind and reuse it from then on. Below the Now block, sections come in this order, each replaced in place:

- `## Prep` and `## Codebase`: written by `factory-prep.md` when the ticket enters Todo or In Progress: the verdict, the assumption check, and a code map pinned to the commit it read.
- `## Plan`: a short step walkthrough. Mark done steps `✓`. Then **Verify:** and **Not doing:**.
- `## State model`: `ts` code blocks for the props type and the state union, plus a state → screen table (the recipe in `factory-state-modeling.md`).
- `## Decisions`: one line each, `- <date> · <question> → <answer>. <why>`, newest first.
- `## Findings`: one line each, `- <date> · <file:line> <what> → <what it changes>`. Only findings that change the plan. Progress belongs in commits.
- `## Learn rep`: only when `learnSurface` is `"linear"`.

## Kinds

- **`now`**: rewrite the Now block.
- **`plan`** / **`state`**: replace the doc section, then rewrite the Now block if the status changed.
- **`finding`**: add one line to `## Findings`. If it changes what the operator owes, update the Now block too. Never post it as a comment.
- **`decision`**: add a numbered line to **Needs you**. Set the label to `Needs decision`, then keep working on what the decision doesn't block. Ask in the terminal instead only when the operator is in the session right now and the answer blocks everything.
- **`resolve`**: when a reply answers an item, remove it from the Now block, add a line to `## Decisions`, and set the label back to `Working` once nothing is owed. If the answer is ambiguous, reply under it with one question, the only time the agent comments.
- **`learn`**: put the rep in `## Learn rep`: rung, `file · function`, the operator's job, done-when, and the skeleton with blanks. Add `Learn: <one line>, reply with a comment` to **Needs you**. When the operator comments with their code, coach in replies under *their* comment: one guiding question, then one hint, then a parallel case, per `factory-learn.md`. Copy their final code into the repo verbatim, without "fixing" it on the way in; a correction goes back as a hint. Record the review verdict in the doc section, and the rep in `~/.factory/learner/` with the comment link.

## Agent state

Set one label from the group: `Working` while work is underway, `Needs decision` while **Needs you** is non-empty, and `Blocked` when a failure needs the operator (credentials, a broken environment, a gate the agent may not cross). Remove the label on close. A saved Linear view filtered on `Needs decision` is the operator's queue across tickets.

## Terminal output

One line per write, nothing more:

```
KAI-329 · needs you: 2 items → <issue link>
```

## Rules

- **Budget:** the Now block is at most 8 lines, every doc line in Decisions and Findings is one line, and the agent starts no comment threads. If you're about to break the budget, cut it down.
- **No sensitive data.** Cite file paths, test names and synthetic fixtures only. Linear is an external service.
- **Concurrent sessions.** Another agent may be editing the same doc. Re-read right before every write, patch the smallest range you can, and never rewrite text you didn't write.

## Related

- `factory-voice.md`: register and when to ask versus decide.
- `factory-entry.md`: reads the Now block, the doc and new replies at session start, and runs `resolve`.
- `factory-prep.md`: writes `## Prep`, `## Codebase` and the first `## State model`.
- `factory-state-modeling.md`: what goes in `## State model`.
- `factory-learn.md` and `factory-mentor.md`: learn-rep rules.
- `factory-close.md`: builds the closing comment from `## Decisions` and clears the Now block and the label.
