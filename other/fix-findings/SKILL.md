---
name: fix-findings
description: "Invoked helper skill for fixing the /pre-merge findings a human has already chosen, with a fresh sub-agent writing each fix and a second fresh sub-agent trying to break it. User-invoked only — type /fix-findings <numbers> after picking findings from a review. Not for choosing which findings to act on, not for stamping review currency, and not for merging."
disable-model-invocation: true
sources:
  primary:
    - "Engineering a Safer World — Nancy Leveson"
  secondary:
    - "Best Kept Secrets of Peer Code Review — Jason Cohen"
    - "Introduction to Software Testing — Ammann & Offutt"
    - "Thinking in Systems — Donella Meadows"
    - "The Design of Everyday Things — Don Norman"
---

# Fix Findings

!`PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}" && mkdir -p "$PROJECT_DIR/.claude" && touch "$PROJECT_DIR/.claude/.fix-findings-active" && echo "fix-findings marker created at $PROJECT_DIR/.claude/.fix-findings-active — post-review edit lock open for this run"`

Take the review findings a human has already chosen, have a **fresh** sub-agent
write each fix, have a **second** fresh sub-agent try to break it, and report
both back. Hand off to a `/pre-merge` re-run, which is the only thing that
re-stamps.

## Why this skill exists

`/pre-merge` delegates the review to a sub-agent that did not write the code,
because the session that wrote it has already demonstrated it cannot see these
particular defects. Then the human picks findings, and the pipeline hands the
*fix* back to that same blind session. The responsive commit is the most
defect-dense code on the branch and the one commit with no independent reader.

Cohen's rule is that an author's job is to *annotate for* a reviewer, not to be
one. This skill applies it one link later: the fix's author must not be its only
reader. Leveson's is that a controller may not treat "sent" as "executed" without
feedback — a fixer's own green test run is exactly that unearned inference, which
is why a second agent attacks the fix rather than the fixer re-checking it.

## Invocation Position

**Invoked helper, and user-invoked only.** It fires when a human types
`/fix-findings <numbers>`; it never self-triggers. `disable-model-invocation:
true` is what enforces that, and it is the reason this skill costs nothing in a
downstream session's context window until it is actually wanted (`CLAUDE.md`
§ *Invocation mechanics*). If a future install strips that key the skill becomes
model-invocable — a context cost, not a correctness failure; nothing below
depends on the key being honored.

Enter it from `/pre-merge` Phase 4's next-step menu — the option **Fix a finding
on this branch first** — or by typing it directly after reading a review.

Do **not** enter it to decide what to fix, to review a diff (that is
`/pre-merge`), to merge (that is `/closeout`), or on an AFK run — there is no
human to dispose of findings, so there is no valid input.

## What this skill is NOT

- **It does not select findings.** The human's numbers are its only input. It
  never ranks, filters, batches, defers, or drops a finding, and it never adds
  one it noticed on the way. #190 draws that line deliberately: disposition is
  the human's. If a finding you were handed looks wrong, the fixer reports it
  **refuted** with evidence and stops — it does not decide the finding away.
- **It does not stamp.** `/pre-merge` is the only writer of the
  `<!-- reviewed-at: … -->` marker, and this skill's commits deliberately move
  the head *past* the stamp. That divergence is the mechanism working, and the
  handoff below is what closes it. `scripts/test-review-currency-marker.sh` pins
  the single-writer rule.
- **It does not merge**, open PRs, or edit PR bodies.
- **It does not re-fix.** One fixer pass and one breaker pass per finding, then
  stop. A surviving mutation is reported to the human, never fed back to the
  fixer. If the human wants another round they invoke `/fix-findings` again.
- **It does not review the branch.** It touches only what the chosen findings
  name. The `/pre-merge` re-run is the review.

## Inputs

- **The finding numbers**, as typed: `/fix-findings 1 3 4`.
- **The findings themselves.** In author-mode they are terminal output from the
  `/pre-merge` run still in this session. If that session is gone, read the
  `## Review Disposition Ledger` on the PR, which loop-mode wrote for exactly
  this case. If neither is available, stop and say so — do not reconstruct a
  finding from memory and fix your reconstruction.
- **A branch with a `/pre-merge` review behind it.** Working tree clean.

If a number the human gave does not correspond to a finding, say which numbers
exist and stop. Do not guess at intent, and do not silently fix the neighbors.

## Workflow

### Step 0. Preconditions

- [ ] `git status` is clean — uncommitted work would land inside a fix commit.
- [ ] The findings are in hand, by number, from one of the two sources above.
- [ ] `.claude/.fix-findings-active` exists (the harness line at the top of this
      file created it; see § *The two flags* for who reads it).
- [ ] The project's test command is known and currently green. If it is already
      red, say so and stop — a fixer cannot tell its own regression from the
      pre-existing failure, and a breaker cannot distinguish `killed` from
      "already broken."
- [ ] A run id is fixed for this invocation, once, before any fixer starts:
      `FIX_FINDINGS_RUN=$(date -u +%Y%m%dT%H%M%SZ)`. Every fixer commit in this
      run ends with the line `Fix-Findings-Run: $FIX_FINDINGS_RUN`. That line is
      how § Handoff counts the rounds already on the branch — from the tree,
      not from anyone's memory of how many times this skill has run.

### Step 1. Per finding, spawn a fresh fixer

**Spawn both sub-agents on the cheaper tier — `model: "sonnet"` on the `Agent` call.** What this skill buys is independence, not capability: the defect it exists to close is that the authoring session cannot see its own work, and a fresh Sonnet context removes that as completely as a fresh Opus one. Escalate to the session's own tier only on a signal — a fixer that returns `blocked`, or a finding that turns on a contract spanning several files. Per finding this skill spends two sub-agent runs, so the tier is where its cost actually lives. This is a default, not a rule anything enforces; issue #339 carries the hypothesis and the three signals that would refute it.

**One sub-agent per finding, never one for all of them.** A single fixer holding
every finding carries fix 1's reasoning into fix 2, which re-creates across
findings the correlated blindness this skill exists to remove. Per-finding
fixers are independent of each other as well as of the authoring session.

**What the fixer is handed, and what is withheld, is `/pre-merge` Phase 3's
contract, unchanged.** Read it there (`pre-merge/SKILL.md` § *The context
contract is about provenance, not permission*) rather than from a paraphrase
here; the same three parts apply:

- **Handed over** — the finding's text verbatim, the branch diff, this project's
  test command, and the PR body's `## Review Notes` block when one exists.
- **Reached for itself** — durable state, read at its source: the merged tree,
  `git log` and `git show`, the slice or PRD issue, `docs/solutions/`, the
  research artifact, installed types.
- **Withheld absolutely** — the authoring session's reasoning: why it wrote the
  code that way, what it considered and discarded, and any narration or summary
  of the finding standing in for the finding's own words.

The fixer's instructions, in order:

1. **Verify the finding against the tree first.** Reproduce the defect the
   finding describes — a failing case, a read of the code path, whatever the
   finding's own claim requires. If it cannot be reproduced, report
   **`refuted`** with the evidence and make **no commit**. A refuted finding is
   reported to the human, not argued into existence and not fixed anyway.
2. **Grep `docs/solutions/` for the class of thing you are about to write** — the same
   move `/execute` Step 1 makes before implementation — and read any entry that
   matches before touching the tree. The corpus is a list of shapes that have
   already failed here; on this skill's own PR, four fixers wrote grep-based
   assertions over prose eight days after an entry named that exact shape and
   said not to. A fixer that reads the entry first does not write the pin.
3. **Write the smallest fix that closes the finding**, following the project's
   conventions. Do not fix anything the finding does not name; scope creep in a
   post-review commit is invisible to the review that has already run. **When
   the finding is about what a sentence claims rather than what something
   does** — a claim in a prose contract, or any claim in a kind of text listed in [references/restated-claims.md](references/restated-claims.md) § *What is not a prose contract* — the fix is one of two
   actions: delete the sentence that carries the claim, or replace that
   sentence with a reference to the one place the claim is canonically stated.
   Rewording the claim is not a fix; a reworded sentence is new text no review
   has read. A finding that an instruction produces the wrong behavior is not
   this case.
4. **Run the project's test command** and report the exit status verbatim.
5. **Commit exactly one commit**, whose message says what the finding was and
   what the fix does, and whose last line is `Fix-Findings-Run: <run id>` — the
   id Step 0 fixed, passed in the brief verbatim. One commit per fix — a fix
   squashed together with another is a fix nobody can read separately.

The fixer reports back: `fixed` (with the commit SHA), or `refuted` (with
evidence), or `blocked` (with what it needed and did not have). Nothing else.
A `fixed` under item 3's prose-claim case also names the after-state of the
site the finding anchored on:

| After-state | Named by | What the anchored site holds at the fix commit |
|---|---|---|
| `deleted` | the fixer | nothing where the claim's sentence was |
| `pointer → <target>` | the fixer | a reference to the canonical statement at `<target>`, which exists |
| `rejected: reworded` | the controller | anything else |

**The controller reads the after-state off the fix, not off the report.** Before
spawning a breaker for a prose-claim finding, run `git show --word-diff
"$FIX_SHA" -- <path>` on the anchored file and look at the site: a deletion adds
no words there, and a pointer adds only the reference. If the site adds anything
else, the after-state is `rejected: reworded` whatever the fixer reported. Revert
the commit with `git revert --no-edit "$FIX_SHA"`, spawn no breaker, and leave
the finding for § Handoff's menu — a reworded sentence left on the branch would
be the next `/pre-merge` re-run's subject.

### Step 2. Spawn a fresh breaker against the fix

A second sub-agent, fresh, **read-only**, and working in a throwaway copy of the
tree. Spawn it on the same cheaper tier as the fixer, for the same reason and with the same escalation signal (Step 1). Its procedure is a checklist and its mutation is drawn from the corpus rather than composed, and the apparatus check gates the verdict — a breaker that cannot make its control go red reports `not-run` rather than false confidence. Neither sub-agent may drop below Sonnet: both read a real tree and run a real suite, and a breaker that misreports `killed` is worse than no breaker at all. It never edits the branch, never commits, never stamps, and never fixes
what it finds — #249 is the incident that rule comes from: a review sub-agent
mutated the tree it was reviewing. **And its subject has to be a fixed commit,
not whatever the branch holds when the breaker looks.** A round processes
findings one after another, and `HEAD` keeps moving as later findings' fixers
commit — by the time the round is reported, `HEAD` no longer names this fix.
A breaker's verdict has to be about the specific fix it was asked to check, not
a restatement of the fixer's own account of that fix (independence from the
fixer's account is the reason this sub-agent exists at all) and not whatever
the branch has accumulated by the time anyone reads the verdict back. So:
**it never reads the original working tree and never resolves a moving ref** —
not `git status`, not the working files, not `HEAD`. "Only for orientation" is
not an exception: orientation taken off `HEAD` names whichever commit is
current when it is taken, which is not this breaker's subject.

What it may read is what cannot move: the extracted copy, and the commit
`$FIX_SHA` names. A commit that already exists cannot be perturbed by anything
else running, so the `git archive "$FIX_SHA"` extraction below is not a
violation of this — and a breaker that needs to see what the fix changed runs
`git show "$FIX_SHA"` from the original repo, since the extracted copy has no
`.git`, rather than inferring the diff from the working files, which move.
Nor does it infer the diff from the fixer's report, on a different axis: that
report cannot move, but relying on it would make the breaker's verdict a
restatement of the fixer's own account of its fix rather than an independent
read of the fix, and independence is the reason this sub-agent exists at all.
Carrying dependencies into the copy is permitted on the same mutability axis:
a fixer repairing a review finding does not edit a dependency tree or
`.env.local` and its siblings, so symlinking the tree in and copying those
files brings over the test command's apparatus, not anything that moves.

PR and issue bodies are on the other side of that line. Nothing in a
`/fix-findings` run edits them — this skill opens no PRs and edits no bodies,
and fixers only commit — so they are durable state the breaker reads at its
source, on the same footing Step 1 gives the fixer for the slice or PRD issue.

**Where the copy lives: `git archive`, not a second worktree — and it archives
the fix, not `HEAD`.** `FIX_SHA` below is the commit the fixer reported in Step
1, handed to the breaker along with the finding. It is not `HEAD`, because a
round processes findings one after another and `HEAD` keeps moving as later
fixers commit — a verdict pinned to a moving ref stops naming this fix by the
time anyone reads it back, even though nothing else is touching the tree while
this particular breaker runs. `$FIX_SHA` names the exact commit the verdict is
about, permanently, regardless of when the round is read. The block does not
bind `FIX_SHA` itself — export it before running the block below: `export
FIX_SHA=<the SHA the fixer reported>`.

```bash
# pipefail is load-bearing: without it the pipeline reports tar's status, and a
# `git archive` that resolved nothing exits 0 having extracted an empty tree.
set -o pipefail
BREAKER_DIR="$(mktemp -d)"
if ! git archive "$FIX_SHA" | tar -x -C "$BREAKER_DIR"; then
  rm -rf "$BREAKER_DIR"
  echo "breaker aborted: could not extract $FIX_SHA into a throwaway copy" >&2
  exit 1
fi
echo "breaker copy: $BREAKER_DIR"
```

A `git worktree add` would register an entry in a git directory that other
sessions read and that survives a crashed breaker as a prunable stub — two
controllers over one stock, which is the coordination hazard Leveson names and
which is real here, because parallel-workspace hosts share one git directory
across sessions. `git archive` writes a plain directory with no `.git` inside it,
so the breaker has no branch to commit to — and **committing is the whole of what
the missing `.git` buys**. It does nothing about a write that lands in the
*original working tree* by another route: a bare relative path, a `sed` with the
wrong `-C`, a `$BREAKER_DIR` that was bound in the block's shell and had gone
empty by the shell that mutated. In the field a breaker reached the real repo
exactly that way and edited two rows of a file under review while a sibling agent
was reading it. The isolation is structural for commits and asserted for
everything else, and #344 is the run where the asserted half failed — so the two
halves are named separately here rather than under one word.

So the copy carries a mechanism for the second half rather than a promise. The
block prints the absolute path it created, and **every command the breaker runs
— the control, the mutation, and the check — runs with that path as its working
directory, `cd`'d there by the printed literal at the top of each shell.** Not by
re-reading `$BREAKER_DIR`, which lives only in the shell the block ran in: a
breaker that mutates from a later shell gets the empty string, and a relative
path then resolves against the repo under review. With the copy as cwd the
failure inverts into the safe direction — a bare relative path resolves *inside*
the copy, where it belonged, and a lost path makes the command fail rather than
land somewhere. `git show "$FIX_SHA"` run from the original repo stays permitted;
it is a read, and it is the one command in the breaker's repertoire that names
the original on purpose.

Clean up with `rm -rf <the printed path>` when the breaker reports — the literal,
for the same reason: `rm -rf "$BREAKER_DIR"` in a later shell expands to
`rm -rf ""`, which reports success and removes nothing.

**The extraction fails closed, and the guard is not decoration.** An unguarded
`git archive <bad-rev> | tar -x` prints its `fatal:` to stderr and exits **0**,
leaving an empty directory behind — so a breaker that trusted the exit status
would run its mutation against no tree at all and could still report a verdict.
That is the exact failure this skill is built to refuse: a green result that is
green for a reason nobody checked. If the block aborts, the breaker reports
**`not-run`** with the abort message and no verdict.

The same guard covers the new way to get this wrong: a controller that forgot to
hand the breaker a SHA. An unset `FIX_SHA` expands to the empty string, `git
archive ""` rejects it as `fatal: not a valid object name`, and under `pipefail`
the pipeline exits 128 — so the missing SHA aborts the extraction rather than
producing a verdict about nothing. No separate check is needed for it, and one
should not be added on the assumption that unset behaves differently from
unresolvable here; it does not.

The cost is that the copy has no git history and none of the repo's ignored
files. Bring over what the test command needs — symlink a read-only dependency
tree, copy `.env.local` and its siblings — or run the project's install command
inside the copy. If neither is affordable here, the breaker reports **`not-run`**
with the reason. It does not report `survived` on a mutation it could not run.

**What the breaker does**, once per finding and then stop:

1. **Validate its own apparatus before anything else** — apply a known-killable
   control and confirm the named check goes red on it.
2. **Apply one corpus-drawn mutation at the point of consumption** of the
   property the fix claims to hold.
3. **Report one of four verdicts** — `killed`, `survived`, `not-run`, or
   `not-applicable` — naming the check, the command, and its exit status.

All three steps, the four verdicts, what a known-killable control is for a shell
or prose change, and why a green result is not self-validating are stated once in
[references/mutation-at-consumption.md](references/mutation-at-consumption.md).
Read it there; it is not restated here.

**The verdict is advisory.** `survived` is reported to the human as a line item
and to the `/pre-merge` re-run as evidence. It is never auto-re-fixed (that is
the re-fix loop #253 recorded), and it never earns or withholds a stamp — a
`survived` verdict that nothing executed reads identically to one that did,
which is why the apparatus check gates the verdict and why the verdict gates
nothing.

### Step 3. Report, then release the lock

**First reconcile the original working tree — you do this, not the breaker.**
The breaker is read-only and works in an isolated copy (Step 2), which makes an
escape unlikely; it does not make it visible, and a breaker that escaped leaves
its mutation sitting in the repo under review. Run `git status --short` in the
original repo after each breaker reports. No fixer is ever editing while a
breaker runs — the two never overlap — so this is exact, not merely
file-granular: with no concurrent editor of any kind, any dirty path
`git status --short` reports is unexplained by construction, and unexplained
means an escaped breaker. Restore the path before the next fixer starts, report
that breaker's finding as **`not-run`** rather than passing its verdict
through, and say in the report that the reconciliation is why.

This sits with the controller rather than the breaker for the same reason
Step 2 gives: the breaker is forbidden to read the original working tree at
all, so handing it the reconciliation would contradict the restriction that
makes its read-only isolation mean anything.

Then print one block per finding — number, the fixer's verdict and commit SHA,
the after-state on a prose-claim finding, the breaker's verdict **and the SHA it
archived**, and the command behind each. No conclusions the human cannot re-run.

```
Finding 3 — fixed at a1b2c3d
  fixer:   `pnpm run test` → 0
  breaker: survived, against a1b2c3d — `pnpm run test -- guards.test.ts` → 0 with
           OVER_FETCH_MULTIPLIER left at 4 and the use site edited to `topK * 137`
           (control went red first: same file, deleted assertion → exit 1)

Finding 4 — fixed at d4e5f6a, deleted
  fixer:   `pnpm run test` → 0
  breaker: not-applicable, against d4e5f6a — no executable check reads the deleted sentence

Finding 5 — fixed at b7c8d9e, pointer → docs/architecture.md
  fixer:   `pnpm run test` → 0
  breaker: not-applicable, against b7c8d9e — no executable check reads the replaced sentence

Finding 6 — rejected: reworded at 9f8e7d6, reverted at 5c4b3a2
  controller: `git show --word-diff 9f8e7d6 -- src/retry.ts` → the site adds words that are not a reference
```

The archived SHA is on the breaker's line because it is the one thing that says
what the verdict is *about*. By the time the round's report prints, `HEAD` has
moved past this fix — later findings' fixers have committed on top of it — so a
report that names only the verdict leaves a `survived` attributable to whatever
the branch had accumulated by then, and a `survived` misattributed to the wrong
fix sends the human back to code that was never the subject. When the two SHAs
match, as they do above, the line is redundant and should still be printed: a
reader cannot tell a match from an omission.

Then remove `.claude/.fix-findings-active`, resolving it through the same
fallback the harness line above used, so the removal reaches the file that line
actually created:

```bash
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
if [ -e "$PROJECT_DIR/.claude/.fix-findings-active" ]; then
  rm "$PROJECT_DIR/.claude/.fix-findings-active"
  echo "fix-findings marker removed — post-review edit lock shut"
else
  echo "fix-findings marker NOT FOUND at $PROJECT_DIR/.claude/.fix-findings-active — the lock may still be standing open somewhere else; report this rather than assuming it is shut" >&2
fi
```

Remove it on every exit path, including an abort — a leaked flag leaves the
post-review edit lock silently open, which is the failure this whole mechanism
exists to close. **Report the not-found line if it prints.** `rm -f` would have
been shorter and would have reported success on a removal that removed nothing,
which is indistinguishable from the failure above; the branch is what makes a
miss sayable. All three sites — the harness line's `touch`, the hook's test, and
this `rm` — resolve `$CLAUDE_PROJECT_DIR` the same way for the same reason: a
flag written under `$PWD` in a subdirectory is a flag the hook never reads, so
the fixer would be refused by the lock written for it. Leave `.claude/.review-stamped` alone; `/closeout` removes it at
merge. The asymmetry is deliberate and is the fail-safe direction: a leaked
`.fix-findings-active` is an open lock nobody can see, while a leaked
`.review-stamped` is a closed lock that announces itself the moment someone tries
to edit.

## The two flags

Lock 1 is a writer, a refusing reader, and a lifecycle, on the same pattern as
`/tdd`'s `.claude/.tdd-active`. Both flags are transient by construction, which
is the condition under which this pack tolerates filesystem state at all. Every
row below names the step that reads the flag, because a flag no later step reads
is not load-bearing (#326).

| Flag | Written by | Read by | Removed by |
|---|---|---|---|
| `.claude/.review-stamped` | `/pre-merge` Phase 4, beside the review-currency stamp, under the same fallback | `.claude/hooks/enforce-classification.sh` — refuses Write/Edit on implementation files while it exists and `.fix-findings-active` does not | `/closeout` Step 3 at merge; `/execute` Step 0's fresh-slate checklist |
| `.claude/.fix-findings-active` | this skill, by the harness line at the top of this file, when it loads, under `${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}` | the same hook clause, at `$CLAUDE_PROJECT_DIR/.claude/.fix-findings-active` — its presence is what re-opens the lock | Step 3 above, on every exit path, resolving the same fallback and reporting a miss rather than swallowing one; `/execute` Step 0's fresh-slate checklist |

**`.review-stamped` also stands the classification clause down, which is what lets this skill's fixer write at all.** The same hook carries an earlier clause refusing implementation writes unless `.claude/.tdd-active`, `.claude/.tdd-skipped`, or `.claude/.lfg-active` exists — and `/execute` Step 6 removes every one of those *before* `/pre-merge` stamps, so no fixer ever arrives holding one. Were the two clauses genuinely independent in that order, the flag the harness line writes above would be read too late to matter: every fixer would be refused by the classification clause, under a message naming `/tdd`. So on a stamped branch the classification clause does not fire and this lock is the sole decider. Do not remove that coupling on the grounds that it looks like a leak between two unrelated gates — `scripts/test-post-review-edit-lock.sh` § 5 drives the real lifecycle, Step 6's removal included, and fails if it goes.

**Two routes the refusal names — which is not the same as two ways out.** The
refusal message names invoking this skill, and deleting `.claude/.review-stamped`
by hand. That second choice is made silently today, and the message is what makes
it visible (Norman — prospective memory fails silently, and "re-run the review
after fixing" is exactly the prospective act the field record shows being
skipped). Read that as a stop on the *default* post-review edit, not as an
enclosure: the hook is registered on `PreToolUse` `"matcher": "Write|Edit"` and
refuses only a path that matches `IMPL_PATTERNS` and survives the skip logic, so
several routes are already past it and leave no trace at all. Writing
`.claude/.fix-findings-active` opens the lock with no sub-agent behind it;
writing `.claude/hooks/enforce-classification.sh` rewrites the gate (`.sh` is not
an implementation pattern); writing `.claude/settings.json` deregisters it; and
no `Bash` write reaches this hook, `rm .claude/.review-stamped` included.
`scripts/test-post-review-edit-lock.sh` § 4 runs the three writes and records
their exit statuses, and reads the registration for the fourth, so the list is
measured rather than believed.

**What the lock does not cover, in the matcher's terms rather than a file's
role.** The hook reuses the classification gate's `IMPL_PATTERNS` list and its
`*test*` / `*spec*` / `*.d.ts` / `*.config.*` skip logic unchanged, and those
patterns match a *substring of the whole path*. Claude Code hands the hook an
absolute path, so the skips reach much further than "a test file, a type
declaration, a config file": `src/latest-news.ts` and `src/respectful.ts` are
skipped for containing `test` and `spec`, so is anything under a `testimonials/`
directory, so is `src/app.config.local.ts`, and so is every file in any repo
checked out beneath a path like `/Users/tester/`. Widening the patterns here
would make the two gates disagree about what "implementation file" means, so
they stay as they are and the consequence is stated: none of those edits is
refused after a review, and a `/pre-merge` re-run, not this hook, is what
covers them.

## Cap

**One fixer pass and one breaker pass per finding, then stop.** Stated here so it
is a property of the skill rather than a habit of the session. The fixer does not
respond to the breaker; the breaker does not re-run against a revised fix. If a
mutation survived and the human wants it addressed, that is a new invocation with
the human's decision behind it. Without the cap this is the fix-review-fix cycle
#253 recorded, with the loop half now also committing.

**Order and concurrency.** The cap says how many times each sub-agent runs; this
says in what order, because leaving that to the session is the same silence the
lock exists to close, one level down. Process the numbers in the order the human
typed them. **Fixers run one at a time, never in parallel** — each edits one
working tree and commits to one branch, so two at once is a race on both, and
"exactly one commit per fix" stops being something either can guarantee. Giving
each fixer its own worktree would trade that race for merge conflicts on exactly
the findings most likely to collide, since findings routinely land in one file
(three of five in one round of #338 landed in `/init-pipeline` § 2); at three to
eight findings that is not a trade worth making.

**A breaker runs only against a fix already committed, and nothing runs
concurrently with a fixer editing the working tree.** Per finding: spawn the
fixer and wait for its verdict; if `fixed`, spawn the breaker against
`$FIX_SHA` and wait for its verdict; only then start the next finding's fixer.
No two sub-agents are ever in flight together — not two fixers, not a fixer and
a breaker, not two breakers.

This section previously permitted a breaker to run concurrently with the next
fixer, and spent four corrective rounds (6cc84c0, 5272615, 04f9e35, 28aec29)
trying to keep that permission both safe and accurately described: a same-file
comparison before backgrounding a breaker, a cap bounding how long a
backgrounded breaker could stay in flight, and two further rounds correcting
false claims the cap's own text made about its consequences. The cap's own
derivation showed the overlap it was defending had already collapsed: the wait
gate it introduced made every breaker's report a precondition for the next
breaker's start, so no two breakers ever ran concurrently under it regardless
of what the section's lead sentence claimed. Four rounds could not make the
permission and its description agree at the same time. This round removes the
permission instead of patching its description again.

**Say the cost plainly: this is slower.** Wall clock is now fixer time plus
breaker time, summed per finding, with nothing hiding one behind the other. A
breaker's extraction, apparatus validation, mutation, and adversarial reasoning
against a fixer's single commit runs to completion before the next finding's
fixer starts, every time — and the cap's own derivation already showed that,
beyond the second finding, a breaker typically outlived the one fixer it was
allowed to overlap, so the concurrency being given up here was buying less than
it advertised. The trade is worth it regardless: the escape-detection ambiguity
the four prior rounds kept trying to bound — an escaped breaker mutation and a
concurrently-editing fixer's legitimate edit landing in the same file,
indistinguishable to `git status --short` — is not bounded by this change, it
is removed. With no concurrent editor of any kind, Step 3's reconciliation is
exact: any unexplained dirty path after a breaker reports is an escape, full
stop.

## Handoff

- **Expected input:** the finding numbers a human chose from a `/pre-merge`
  review, plus the findings themselves (terminal output or the PR's ledger), on a
  clean branch that has been reviewed.
- **Produces:** one commit per accepted finding, each authored by a context that
  did not write the code under repair; a per-finding breaker verdict, the SHA it
  archived, and the command behind it; `refuted` reports for findings the
  tree did not confirm; and a revert for any prose-claim fix Step 1 rejected. It produces no stamp, no PR edit, and no merge.
- **Comes next by default:** a re-run of `/pre-merge` in author-mode. It reads
  the stamp off the PR itself (`pre-merge/SKILL.md` Phase 1 step 4), takes the
  post-stamp delta — these fix commits — as its subject, runs the review
  dimensions on that delta with the tree readable around it, and replaces the
  existing stamp at the new head. Hand it the breaker verdicts as evidence and
  the finding numbers each commit closes. There is no range to hand it: it
  derives the range from the stamp, and falls back to the whole branch in the
  four states `pre-merge/SKILL.md` Phase 1 step 4 names. Then
  `/compound` if a lesson emerged — which commits onto the branch and hands
  back for a second re-run over that commit, on the same stamp mechanism — and
  then `/closeout`.

**Next-step menu.** This is a branch point, so offer it as a single
`AskUserQuestion` rather than leaving the user to retype a command (see
[references/next-step-menu.md](references/next-step-menu.md)). Which option leads
depends on how many rounds this branch has already had, and that number is read
from the tree — the `Fix-Findings-Run:` line Step 1 writes — never recalled:

```bash
# $BASE_REF: the base branch's ref, derived as /pre-merge Phase 1 step 3 derives it.
ROUNDS=$(git log --format=%B "$BASE_REF..HEAD" | sed -n 's/^Fix-Findings-Run: //p' | sort -u | wc -l | tr -d ' ')
```

**Below two rounds**, recommended option first: **→ Re-run `/pre-merge`
(recommended — review the fixes and re-stamp)**, **Fix another finding —
`/fix-findings <numbers>`**, **Stop here — leave the fixes unreviewed on the
branch**. **At two or more**, this branch has already been through a fix round
and a re-review, and across three repos the third round found a new
contradiction more often than it closed one (#347 — skills #345 counted its own
rounds to five before deleting the rule it was patching). Lead with **→ Hand
the remaining findings off as issues (recommended — `/qa` or
`/request-refactor-plan`), then re-run `/pre-merge` on what is here**, then
**Re-run `/pre-merge` — review the fixes and re-stamp**, then **Stop here**.
The count changes the order, not the set: nothing is taken off the menu, and
the human still chooses. Include a run-specific follow-up when the breaker
returned `survived` or `not-run`: **Show the surviving mutation for finding
N**. The platform's free-text "Other" option is the escape hatch — don't add
one.

Print the runtime handoff line either way:

```
**Next session:** /pre-merge
**Input:** branch <branch-name>, carrying the fix commits past the stamp — re-review and re-stamp
```
