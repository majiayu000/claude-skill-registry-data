---
description: The agent's own reading of a piece — a dictation, a draft, anything the operator wrote and wants answered rather than summarised — posted as a review on the PR that carries it, each block anchored to the lines it is about. Invoke as `/feedback <file> [<language>]`. Use when the operator asks what you think of something, says "а твой отклик?", "рефлексия", or asks for the agent's half of a two-voice piece.
---

End state of this skill: the PR carrying the piece has one review saying what
you would say if the operator asked what you thought — the whole-piece blocks in
the review body and the rest anchored to the passages they are about, and short
enough that every block in it earns its place. The file is untouched.

**Language is a parameter**, `/feedback <file> [<language>]`, defaulting to the
language the operator asked in: a review is a PR comment, which `CLAUDE.md` §
"Language" files under conversation. A bare `/feedback <file>` is a token and
has no language to read, and there the material's decides.

## What it is for

A reading goes where it can be answered. The operator replies to a block in the
thread it hangs off, their answer sits under the block rather than beside it,
and what the two of you settled is legible as an exchange because that is what
it is.

**This is not `/code-review`.** That one hunts defects in a diff; this one reads
a piece — what it argues under what it says, where the argument is missing a
step.

## The bar

What earns a block is open. What the piece argues under what it says, what it
takes for granted without saying, where the argument is missing a step, what is
said three times where once would carry it — those are the kind of thing,
offered to show the altitude rather than to be worked through as a list.

**This is the half that earns the review.** A summary of what was already read,
or a compliment, is the failure mode — agreeing is fine where something actually
lands, but a block that only agrees is praise wearing the shape of a response.

**What would be cut from a post is not what gets cut from the source.** A
digression carrying a third of a recording is still the recording. Say "in a
post I would cut this" and leave the text alone.

## Where each block goes

**A block goes inline only where it points at a passage.** Most of what a
reading has to say is about the piece whole — its shape, what it assumes, the
step it skips — and a whole-piece thought forced onto a line is a false anchor:
the operator clicks it and lands on a sentence that is not what the block is
about. Those go in the **review body**, which is also where the reading is read
first.

Two further reasons the body carries the weight:

- **Inline comments are read in the file's order, not yours.** GitHub sorts them
  by position. So anything whose sequence is doing work — an argument that
  builds, a ranking of what matters — belongs in the body, where your order
  survives.
- **An anchor needs a line in the diff.** A piece the branch adds is wholly in
  it, so anything in it can be anchored; a file the branch only partly changes
  can carry an anchor in the touched hunks alone, and a block about an untouched
  passage quotes it in the body instead.

## Posting it

One review, not a scatter of comments. A comment posted on its own notifies the
operator as it lands; a review notifies once, on submission, and the whole
reading arrives together. Three calls, in this order:

1. `mcp__github__pull_request_review_write` with `method: "create"` and **no**
   `event` — that opens a pending review rather than submitting an empty one.
2. `mcp__github__add_comment_to_pending_review` per anchored block —
   `subjectType: "LINE"`, `path`, `side: "RIGHT"`, `line`, and `startLine` for a
   range. (`subjectType: "FILE"` is the whole-file form, for a review spanning
   several files; with one piece under review the body is that home.)
3. `mcp__github__pull_request_review_write` with `method: "submit_pending"`,
   `event: "COMMENT"`, and the whole-piece reading as `body`.

`COMMENT`, always. A reading is not an approval and not a change request, and
the PR's approval state is not this skill's to move.

**The rest of the mechanics are `CLAUDE.md` § "GitHub comments"** — a body
posted as text and not as a path, and **never resolving a thread**, which is the
one an eight-block review puts most temptation in front of.

## The reading is posted, not pursued

Submitting the review ends this skill. The blocks belong to the operator from
that moment: they read them, answer what is worth answering, and resolve what
satisfies them. An answered block becomes work through
`@.claude/skills/handle/SKILL.md`, in a session they open for it.

`CLAUDE.md` § "GitHub comments" governs comments the operator **points you at**.
Your own blocks are not those, and acting on one because you wrote it makes one
session both reviewer and author — the pairing this skill exists to keep apart.

## It needs a PR

No PR on the branch, no review. Say so and run `@.claude/skills/pr/SKILL.md`
rather than putting the reading somewhere else — a reading with two possible
homes has a boundary running through it that nothing holds, and what leaks
across it is the exchange the reading came out of.

## Do NOT

- Write one for a file the operator did not ask about. An unrequested reading on
  their PR is the agent talking over their work.
- Edit the material to make a finding land. The finding is about the text as it
  stands.
