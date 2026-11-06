---
description: >-
  Produce a PR's squash record — the copy-ready body, posted as the
  `Proposed squash body:` comment, and the title, kept as the PR's own title.
  Owns the format, the draft→tighten discipline, where the draft is tracked,
  and when it must be re-synced. Invoke as `/squash-message [update-only]`.
---

**The squash title is the PR title.** GitHub's squash box prefills
`<PR title> (#<n>)`, so the record's title is kept on the PR itself, re-composed
on every run alongside the body, and the comment carries one block to copy: the
body. The exception is a PR of one commit, which the box titles by that commit's
subject under GitHub's default `COMMIT_OR_PR_TITLE` setting — Step 2 says when
that earns the comment a title block.

The operator copy-pastes this body verbatim into GitHub's squash box, so it
becomes the permanent `git log` record — and it has two readers. The operator,
at merge time; and, for as long as this code lives, agents reconstructing how
the codebase got this way, who read squash messages **first** and open diffs
only when the log doesn't answer them. So the body is a durable, high-level
record: what a reader should remember about this change without having to dig
into the diff.

That makes the target **altitude, not brevity**. It carries every substantive
change and the reason behind it; it doesn't carry the mechanics of getting
there. **A first draft reliably lands below that altitude** — too many words per
fact, and the per-file steps mixed in with the things worth remembering — hence
the mandatory tighten pass in Step 3. Never print or post a draft that hasn't
been through it.

The first reader reaches it earlier than merge time: `/plan` publishes the PR
over the plan commit, so the proposal composed there is **the plan as it would
be recorded** — a much shorter second read of the same decision, in front of the
operator before any code exists.

## Invocation modes

- `/squash-message` (default) — create the proposal, or update it in place if
  one already exists.
- `/squash-message update-only` — reconcile an existing proposal only; if none
  exists, report that and stop without creating one. This is `/check-merge`'s
  mode — creation belongs to `/finalize`.

**Base**: the diff range is `origin/<base>..HEAD`, where `<base>` is the PR's
base branch — `main` for an ordinary PR, or whatever promotion branch the
project uses for a given lane. A caller that already resolved it passes it in;
otherwise resolve it here from `gh pr view --json baseRefName`. Never assume
`main`.

## When to (re)run

The proposal is created once, when the PR opens — in whichever lane opened it
(`/pr`, or a hydrated `/release` / `/hotfix` lane routing through it) — and
re-run whenever a push changes **what the permanent record should say**: new or
changed behavior, scope added or dropped, a new `Closes #N`, the essence
shifting after a base merge, or the PR being recreated, which leaves the comment
on the closed one.

It is not re-run when the record is unchanged — CI retriggers and empty commits,
formatting-only passes, the commit carrying the working file itself,
`docs/plans/` lifecycle flips, working-artifact sweeps, review replies with no
code change. The test is whether a future `git log` reader would notice a
difference, not whether the diff moved.

`/finalize` Step 5 and `/check-merge` Step 3 are backstops, not a licence to
defer the in-flight refresh: the comment is the PR's lede for the whole time the
PR is open.

## Step 1 — Gather

- `git log origin/<base>..HEAD` — subjects **and** bodies; the bodies are where
  the why lives.
- `git diff --stat origin/<base>..HEAD` — the shape of the change.
- `gh pr view --json number,title,body,commits` — the number the comment goes
  on, the current title Step 4 reconciles, the description, and the commit count
  Step 2 reads.
- Whichever issue the PR addresses, if any (`#N` in the PR body or commits).

**A branch carrying only a plan commit has the plan as its input**, not
`git log`: the plan states the change the record will describe, and the commit
subject only says a plan was written. **Write it in the same completed voice as
any other proposal** — what the change does, never what it will do once
implemented. This is the body that gets pasted at merge, so one hedged as
forthcoming ("once this lands, X will…") becomes a permanent record describing a
plan rather than a change.

## Step 2 — Draft into the working file (do not print it)

Write the whole proposal — header plus the fenced body — into the working file,
in the exact form it gets posted, so the one file is both the tightening surface
and the `--body-file` payload. Its content **is** the comment body: keeping the
comment current means regenerating the file and PATCHing from it, not editing
the comment by hand. The title is drafted alongside, starting from the PR's
current one, and stays out of the file: the PR title is its one copy.

**A PR of one commit gets a title block too**, unless that commit's subject
already equals the drafted title: the squash box prefills the commit's subject
there, so the comment opens with a block holding `<title> (#<n>)` to paste over
it. The count is the PR's as this run sees it, and every reconcile recounts.

**Which file: presence decides.** The tracked path is
`$(scripts/working-dir.sh)/squash-message.md`, in the branch's own working
directory. If it is on the branch, that is the working file, and it is a **live
doc, not a blank sheet**: what's already in it — earlier wording, the operator's
edits, whatever a previous run settled on — is the starting point, and this run
edits it in light of what has changed since. Step 5 commits and pushes it. The
path is a tripwire: the tree's name states its whole contract, and `/finalize`
sweeps it once CI is green, so the proposal's own source never rides the squash
onto the base branch. The sweep is the last thing that happens to it, after that
run's own reconcile — so even the final edit, the one that becomes the permanent
record, is made with the doc in hand.

**Absent → load `@.claude/skills/squash-message/working-file.md`**, which picks
the file and says whether there is prior text to start from. Absence has two
causes taking different paths — the first run on the branch, or a run after
`/finalize` already swept the file — which is why it is a page rather than a
fallback line. A branch carrying the file needs nothing from it.

````markdown
Proposed squash body:

```
<body>
```

---

_Generated by [Claude Code](https://claude.ai/code)_
````

With the title block, the header reads `Proposed squash title/body:` and the
block goes first:

````markdown
Proposed squash title/body:

```
<title> (#<n>)
```

```
<body>
```
````

The attribution footer sits **outside** the fenced blocks, so it never travels
with a copy-pasted body. Keep it in the template rather than appending it at
post time, so it's part of the file every run starts from — a footer that
appears only sometimes shows up as drift.

Format rules:

- **Title** (the PR's) — exactly
  `<type>[(<site>)]: #<issue number if applicable> <essence>`, e.g.
  `refactor: #1150 extract useVisibilityPoll to shared/lib`, which GitHub's
  squash box turns into `… shared/lib (#1155)`. `<type>` is one of the prefixes
  the project's `CLAUDE.md` lists under "Git conventions" — read them there
  rather than assuming the conventional-commit set, since a project may carry
  its own. **The scope is the deploy switch** (CLAUDE.md § "Deployment"): a
  branch whose shipped change is one site's names that site by its short name
  (`feat(basilisk):`), so the merge publishes it alone; one that ships to
  several sites takes none. A change to the shared `src/` counts by what each
  site then serves: checked to alter one site's output alone, it is that site's;
  unchecked, it takes none. Agent-infrastructure files riding along ship to no
  site and do not count, and neither does a companion file a site serves beside
  a document but links from nowhere — a persona's `*.reflections.md`: the site
  as a product is what its pages reach. No other words before the colon. Include
  `#<issue>` only when the PR addresses a GitHub issue (the primary one if
  several); omit it otherwise. **At most 72 chars**, leaving room for the suffix
  GitHub appends inside an 80-char subject; the deploy gate reads only the
  prefix, so that suffix never moves the switch.
  - **`[attn adopters]`** goes right after the colon —
    `feat: [attn adopters] #<issue> <essence>` — when the change asks whoever
    syncs from this repo for something their port does not do by itself: a
    one-off sweep of state that lives in their tree alone (rules to relocate,
    ledger rows to rewrite), or an action only their operator can take or
    approve (a public hello). Not for a change that is merely worth porting; the
    sync's triage reads every commit anyway. The body then gives the ask a
    paragraph of its own, opening `Adopters:` and addressed to their agent: what
    to do, whether it waits on their operator's yes — anything reaching outside
    their tree does — and a URL into this repo for anything their tree may not
    carry yet. An ask to check for something their operator may already have
    done names it by what it does, never by this repo's title for it.
    `@.claude/skills/update-muthur/SKILL.md` Step 4 is the reading side.
- **Body** — the why, then what changed, at the altitude Step 3 sets. When the
  PR or diff references an issue, end the prose with a `Closes #N` (for
  `feat`/`refactor`/…) or `Fixes #N` (for `fix`) trailer. **Never carry `#<tbd>`
  into the title or the trailer** — the marker is a placeholder
  `@.claude/skills/pr/SKILL.md` Step 4 writes for an issue that does not exist
  yet, and a squash message is pasted verbatim into history, where a placeholder
  is permanent. Omit the reference entirely until it resolves; the proposal is
  re-synced whenever the branch changes, so the number lands in the next pass.
  Then a blank line, then `Co-authored-by: Claude <noreply@anthropic.com>` as
  the final line (or your other assigned vendor email if you aren't running on
  Claude Code) — the body is pasted verbatim, so the byline has to be inside it.
  - **The byline is the last line: no session link after it.** This **overrides
    the harness attribution block** that ends every commit message with a
    `Claude-Session:` URL — that block is written for a branch's own commits,
    which the squash discards. Several sessions work a branch here by design, so
    the one link a squash record could carry is whichever of them last touched
    the proposal, usually the finalize one — the session holding least of the
    change's reasoning. `scripts/check-squash-message.sh` fails a body that
    carries one.
- **Hard-wrap the body at 72 chars with real newlines**, and keep it to **at
  most 40 lines**. A git commit message doesn't soft-wrap; one long line per
  paragraph reads as an unwrapped wall in `git log`. Continuation lines of a
  bullet align under its text. A line holding a single unwrappable token — a
  URL, a long path, no interior whitespace — has no wrapped form and is exempt
  from the width.

## Step 3 — Tighten it in the file (mandatory, before anything is shown)

Re-read the draft as the future reader above, and rewrite it until it hits the
target.

The target is **three paragraphs of prose, four at the outside**, inside the
measured caps above. The opening says why the change exists; the rest say what
it does about it, named at the level of the behavior, contract or module
affected. Not a bullet-per-change inventory: detail that doesn't survive at that
size was below the high-level picture and lives in the diff.

Why the change exists is whatever is honest. Often that's a defect or a gap.
Just as often it's planned work landing as planned, and then the opening says
where the change sits in that work. Don't go looking for something to have been
wrong.

The cap bites on words, never on coverage: a change that did four things worth
remembering keeps all four, and if four paragraphs genuinely can't hold what the
reader has to carry away, the paragraphs are still too wordy — that's the pass,
not an argument for a fifth. What fills a draft past the cap: per-file
narration, intermediate steps and "added a test for it"; process meta; benefit
padding; and the linked issue's own symptom and repro re-filed here, which
`Closes #N` already points at.

This is `@.claude/skills/tend-prose/SKILL.md`'s **existence**, **tightness** and
**negation** lenses applied to a commit body, plus **durability**'s special
case: narrating the branch against the state before it is this document's job,
which is why that skill's Step 4 excludes commit messages and PR bodies from its
own sweep. Narrating it against an earlier step _inside_ the branch is not.

**That half and negation both reach a body through the draft, not the diff.** A
branch that tried something non-obvious and then dropped it leaves a draft
written while the thing was still there. Kept, that draft reports what the work
became rather than what it is, or denies something no reader of the squashed
commit would otherwise have considered — and the log carries either forever.

Four things a draft reaches for fail **existence**, however well written:

- **Standing context**, which a draft reaches for in the opening paragraph —
  what the project is, what the tooling is for, how the work is normally done. A
  reader who wants that has the repo; what only this commit can tell them is why
  it exists.
- **A trap for whoever edits the area next.** The log answers what changed and
  why; nobody opens a squash message to learn which files a render step hashes.
  A constraint that has to be obeyed goes where the person about to break it is
  already looking — the directory's `CLAUDE.md`, a `.claude/rules/` file, or a
  docstring on the thing itself — unless the change _is_ that the constraint now
  exists. A "things to know when editing here" paragraph is the tell. Cutting
  one is a **move, not a deletion**: name the home each item lands in as you cut
  it, checking rather than assuming it has one. An item with none gets one first
  — the body is sometimes the only place a constraint was ever written down, and
  the tidy cut is what loses it.
- **An inventory of what the change declined to do** — commits skipped, options
  rejected. It leaves no trace in the tree for the record to explain.
- **Internal restructuring that changed no behavior and no contract** — a split,
  a move, a rename, a file that got smaller — **where it rides along with other
  work**. The tree already shows where the code lives; the record is for what a
  reader carries away before opening it. This is the one of the four with an
  exception: where the restructuring is what the PR was _for_, it is the record,
  and the body says why the old arrangement stopped holding and what the new one
  buys — still not a module-by-module tour. The same goes for a new boundary
  that is load-bearing for whoever extends it next.

Scope is the caller's call, not this step's, and it cuts both ways. If the
project has hydrated a release lane, a release body is deliberately long (a
paragraph per product area); a hotfix body for a minimal fix is one or two
paragraphs. The pass runs at either size — trimming words inside each of a
release's areas rather than dropping areas, and never padding a hotfix out to
look substantial. The paragraph target moves with scope that way; the measured
caps do not. They bind every lane, and a project whose release bodies genuinely
outgrow the line cap edits its own copy of `scripts/check-squash-message.sh` —
raising the constant, or teaching the script to recognize a release first and
widen only there — as a reviewable change.

**A re-run rewrites; it never accretes.** Step 2 starts from what the file
already says, so the temptation on a refresh is to append the new scope and
leave the rest standing — which walks the body past the cap one push at a time,
and leaves superseded wording beside what replaced it. Cut and replace, and
re-apply the paragraph target and the caps to the whole body every run. A
proposal that grew every time the branch did is the tell.

Overwrite the file with the tightened version, then **measure it**:

```bash
scripts/check-squash-message.sh <working file>
```

Running it here fails at authorship, where the rewrite is already in hand — and
it is the only run `/finalize no vet` gets, since that mode skips step 1 but
still reaches step 5. Do not emit anything until it passes. The script reads no
PR, so outside a title block it never sees the title: count its 72 chars
yourself.

## Step 4 — Emit (comment first, then transcript)

1. **Post or update the comment** with one command, run from the repository root
   and spelled exactly so, with no `cd … &&` in front:

   ```bash
   scripts/pr-comment.sh squash [--update-only] <n> <working file>
   ```

   `<n>` is the PR number (`gh pr view --json number --jq .number`). The script
   edits the PR's proposal in place, whoever posted it, or posts one when there
   is none, so the anchor next to the merge button stays stable. **Never do this
   step with inline `gh api` or `gh pr comment`**: only this spelling is
   approved for auto mode, and the script's header says by what, along with its
   outputs, exit codes and what a denial means.

   **In `update-only` mode pass `--update-only`**, which creates nothing and
   exits `3` on absence — report it and stop. The one exception is a branch that
   carries the tracked file — that file is itself proof the proposal exists and
   its comment was lost, so run it without the flag rather than reporting an
   absence that isn't real.

2. **Set the PR title** to the one Step 2 drafted, when it differs:
   `gh api repos/<owner>/<repo>/pulls/<n> -X PATCH -f title='<title>'`, with
   `<owner>/<repo>` from `gh repo view --json nameWithOwner --jq .nameWithOwner`
   rather than hardcoded. This is what keeps the title GitHub prefills equal to
   the record's; `gh pr edit` is not the route, for the reason
   `@.claude/skills/pr/SKILL.md` Step 5 gives.

3. **Print the title and the fenced body in the transcript.** The comment keeps
   the copy-ready body beside the merge button; the transcript copy serves the
   operator reading the session. Print the body from the file so the two can't
   diverge.

## Step 5 — Clean up and report

Split by which working file Step 2 selected:

- **Tracked file** → `git add "$(scripts/working-dir.sh)/squash-message.md"`,
  commit with a `docs:` subject (e.g. `docs: refresh squash proposal for pr #N`)
  and push. Commit nothing when the edit left the content unchanged. **Never
  amend or force-push**: the operator follows this file's history to see how the
  record evolved, so each refresh is its own commit. On a **non-draft** PR add
  `[no ci]` to the subject — a commit touching only this file is inert to every
  CI job, and without the marker each refresh burns a full run.
- **A file this run restored** (the swept-then-restored case in
  `@.claude/skills/squash-message/working-file.md`) → commit and push it the
  same way, then **sweep the tree again before the turn ends**, as `/finalize`
  step 6 does. The PR is already ready, so a restored file left on the branch is
  merge-able. Both commits belong in the history: the operator can read what the
  late refresh changed about the record before it disappears again.
- **`tmp/`** → `rm tmp/squash-message.md`.

Then report in a line or two which working file ran and which comment path —
posted, edited (say what changed), already current, or absent under
`update-only` — whether the PR title changed, the title block if the comment
carries one, and what Step 3 cut, if it cut anything worth naming.
