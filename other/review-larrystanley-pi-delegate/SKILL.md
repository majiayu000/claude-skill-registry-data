---
description: Have pi review code as a second opinion, then adjudicate its findings
disable-model-invocation: true
---

The user wants pi to review: $ARGUMENTS

This is the one part of pi-delegate that is not delegation. Everywhere else pi writes
characters you would otherwise type. Here pi writes nothing — it reads, and gives an
opinion, and **your job is to judge that opinion, not to relay it**.

That distinction decides the whole shape of this skill. A reviewer whose findings get
pasted through unexamined is worse than no reviewer: it launders a guess into something
that looks adjudicated. What makes a second model worth running is that it notices
different things than you do — and that only pays off after you have checked which of
those things are real.

## 1. Work out the scope

With no `$ARGUMENTS`, review uncommitted work:

```bash
git diff HEAD --stat && git diff HEAD
```

If `$ARGUMENTS` names a ref, compare against it (`git diff <ref>...HEAD`). If it names
files or directories, restrict to those. If the diff comes back empty, say so and stop —
do not invent a scope.

Note the size. A diff over ~1500 lines is worth splitting into two reviews: pi's attention
degrades across a long diff the same way anyone's does, and two focused passes beat one
distracted one.

## 2. Write the task book

Put it in a temp file, and have pi write its findings to a **temp path too** — an absolute
one. pi resolves absolute paths straight through (`resolveToCwd` applies no sandbox), so
the findings land outside the repo and nothing needs gitignoring or cleaning up:

```bash
DIR=$(mktemp -d)
cat > "$DIR/TASK.md" <<EOF
Review the change below. You are a second reviewer: the author has already read it, so
say what they would not have noticed themselves.

Write your findings to $DIR/FINDINGS.md and nothing else. Do not modify any source file.

Use exactly this format, one block per finding, most serious first:

### <relative/path.ts>:<line>
主張: <one sentence — what is wrong>
理由: <why it breaks, concretely: what input, what happens>
信心: 高 / 中 / 低

Rules:
- A finding needs a concrete failure. "Could be clearer" is not a finding.
- 信心: 低 is fine and useful — say it rather than dropping the finding or overselling it.
- If you find nothing worth reporting, write "(no findings)" and stop. An empty review is
  a real result; padding it is not.

--- THE CHANGE ---
$(git diff HEAD)
EOF
echo "$DIR"
```

Then dispatch with `pi_dispatch`: `task_file="$DIR/TASK.md"`, `cwd` = the repo root (so pi
can read surrounding code the diff does not show), `tools="read,write"`, `mode="sync"`.

Leave `provider` / `model` unset — the user's own pi default is right here.

`tools="read,write"` and not `edit`: pi needs to create one file and read the tree. Nothing
in a review justifies changing a line of source, and not granting it is cheaper than
trusting it not to.

## 3. Adjudicate — this is the actual work

Read `$DIR/FINDINGS.md`. Then, for each finding, **check it against the real code** before
you believe it. Read the file. Trace the path it claims breaks.

Report to the user in three groups, most useful first:

- **確認** — you verified it. Say what you checked, in a clause. These are the only ones
  worth acting on.
- **誤判** — you checked and it is wrong. One line on why, so the user need not re-check
  your re-check.
- **待確認** — needs a decision or context you do not have (a product call, an unstated
  invariant). Name what would settle it.

Keep every group. A review that reports only the hits hides its own false-positive rate,
and the user needs that rate to know how much to trust the next one.

Do not fix anything. Reviewing and fixing in one motion is how a wrong finding becomes a
committed change. If the user wants the confirmed findings fixed, that is a dispatch —
`skills/delegating-to-pi` — and it starts from a task book naming them.

## 4. Say what it cost

Close with the dispatch's `duration_s` and token counts from the verdict, and the count of
findings raised vs confirmed. Over a few runs that ratio tells the user whether this review
is worth running at all — which is a thing they should be able to find out.

## When this is worth running

Best on: a diff you wrote and have stopped being able to see; unfamiliar code where you
want a second read before touching it; a change whose failure mode is subtle (concurrency,
error paths, resource lifetime).

Weakest on: anything requiring product or user context pi has never seen. It reviews the
code in front of it, not the decision behind it.
