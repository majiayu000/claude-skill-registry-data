---
name: human-review
description: Assemble .human-review/review.html — a tabbed reviewer's guide for a change set — from the review-points.md the coding agent committed with its fixes (what it fixed, declined and assumed), plus diagram deltas, a Code City shot, a feature video, the endpoint-complexity increment, the REST contract diff and deep-linked snippets. Explicit invocation only — user types /human-review.
disable-model-invocation: true
---

# /human-review — assemble a review.html for a human

**This skill does not review the code. It writes up a review that already happened.**

The review happened in the coding agent's own conversation, and it left a record:
`/record-review`, run in the conversation that implemented the change, reviews it
adversarially (`/code-review` in Claude Code, reviewer subagents elsewhere) and writes
**`review-points.md`** at the repository root — what it fixed because the review was right, what it read and **declined**, and what it **assumed** where the ticket was
ambiguous — committed with the fixes, so the record arrives in the pull request's own file
list. This skill reads that file. It does not run a review, and it does not write one.

That is the whole division. The judgement is produced once, by the agent that made the
decisions, while it still has them; the page is assembled by programs from the branch.
What is left for you is two model-written artifacts — the cheap model's check of the
sentence↔test pairing behind the Tests tab (`test-mapping.json`: every scripted link
confirmed or rejected, the rest paired), and **+1 LLM script**, the Demo film's — plus the page's layout and its ledes. Everything else on
these five steps is a script. Do **not** commit or push.

A branch with no `review-points.md` is not an error and not a gate: the page says so, in a
band, and the piles read *not recorded*. **Do not write the piles by hand to fill the
gap** — a pile you compose at the end of a review is exactly the artifact this flow
replaced, and it reads on the page identically to one the agent actually recorded.

Resolve the skill's own directory once — a plugin install, an env override, a project
symlink, a gitignored CI clone and a `~/.copilot/skills/` symlink (VS Code Copilot Chat)
are all real layouts:

```sh
for candidate in "${CLAUDE_PLUGIN_ROOT:-/nonexistent}/skills/human-review" \
    "${HUMAN_REVIEW_HOME:-/nonexistent}" \
    "$(readlink -f .claude/skills/human-review 2>/dev/null)" ".claude/skills/human-review" \
    "$(readlink -f ~/.copilot/skills/human-review 2>/dev/null)"; do
  [ -x "$candidate/scripts/run-steps.py" ] && { SKILL="$candidate"; break; }
done
[ -n "${SKILL:-}" ] || { echo "cannot locate the human-review skill"; exit 1; }
```

Run everything from the repository root. Project-specific commands live in
`human-review.json` there, not in this file — `human-review.example.json` is the template.

## Step 1 — What does the branch record about its own review?

```sh
${SKILL}/scripts/review-points.py --check
```

It prints what it understood: how many items in each pile, which reviewer raised each one,
and what each is anchored to. **Read that output — it is the review.** Nothing below this
line produces findings, and nothing below this line may add one.

Four answers, and none of them is a refusal:

- **0** — the record is there and parses. Step 3 turns it into
  `.human-review/review-points.json` and the page's three piles are filled from it.
- **3** — no `review-points.md` on this branch. Say so to the human in one line and carry
  on: the page renders a band reading *nothing records what was reviewed or declined*, the
  assumptions pile says the coder could not be asked, and that is the honest page for this
  branch. If they want the record, the thing to run is `/record-review`, in the
  conversation that wrote the code — not a review pass here, whose findings would be
  nobody's decisions.
- **4** — the file is there and will not parse. Print the problems; they name lines. This
  one *does* stop Step 3, loudly, because a pile the parser skipped reads on the page
  exactly like a pile nobody wrote.
- **5** — every item is unanchored. The file exists and says nothing checkable, which is
  not the same thing as a clean review.

⚠️ **Never run `/code-review` or `/simplify` from here.** Not to fill a gap, not to
corroborate the file, not to "check" it. A pass run now is a second opinion formed after
the fact by an agent that did not write the code, and its findings carry no accept/decline
decision at all — which is the one thing the Review tab exists to show. `review-passes.py`
still runs, and is still worth reading, as a **cost** source: it finds the passes that ran
in the *coding* session and prices them. It is not a gate any more.

## Step 2 — Resolve the change set, then gate and wipe

From `$ARGUMENTS`: **empty** → uncommitted work, `BASE=HEAD` — unless the working tree is
clean, which is the normal state right after `/record-review`: then the branch against
`origin/main`. **A ref / range / SHA** →
`BASE=<the older ref>`. **A PR** (`#123`, a github URL) → `gh pr checkout <n>`, and
`BASE=$(gh pr view <n> --json baseRefName -q .baseRefName)`. Default `origin/main`. Print a
one-line scope banner; an empty change set is "Nothing to review." and stop.

```sh
${SKILL}/scripts/preflight.py --base "$BASE"
```

It pushes, waits for CI **on the pushed commit**, and only then wipes `assets/` and earlier builds' `*.out` logs, clears the
model state that is not HEAD's (`.model-prev/` and `.model-runs.json`/`.film-runs.json` rows
from another branch or from before the fork — the last run's branch is kept in `.branch`),
resets the ledger and writes the run's start markers. Exit 1 means the branch is not proven and nothing
was destroyed — report which workflow failed and stop. Whatever it prints on its last line
about the gate goes in the guide verbatim; *"no build proved this"* must never read as a pass.
Only the **authoritative** workflows count — `"ci": {"workflows": ["ci.yml"]}` in
`human-review.json` or `--workflow ci.yml` (repeatable, all must be green); unset, the one
workflow named like ci/build, else every run on the SHA. A green Pages deploy never opens the
gate. Cancelled, never-picked-up (runner outage) and GitHub-unreachable are reported as such,
not as a red build; the verdict (workflow, run id, SHA) is in `.human-review/.gate.json`.

If `.human-review/review.html` already exists, ask what changed first — see *Iterating*.

## Step 3 — Produce the evidence

**First, the film's script — the one producer input that is yours.** If none of
`.human-review/feature-script.js`, `human-review-feature.js` at the repo root, or
`$HUMAN_REVIEW_FEATURE_SCRIPT` exists, write `.human-review/feature-script.js` now, before
the producers run, following `reference/feature-script.md`: derive the screens from the diff,
drive the app through every one the change touched, `say()` what is new on each. Fork it to a
`model: sonnet` subagent, like the matrix. Without it the video step exits 2, "no feature
script", and the Demo tab says *nothing was filmed* — the reference run had a film because a
model wrote this file; the Copilot run of 2 Oct had none because nothing asked it to. Outside a
session the same step is a program, `scripts/rerun-film.py` (`claude -p --model sonnet` over
`reference/film-prompt.md`), which is what the Demo tab's 🤖 runs.

```sh
${SKILL}/scripts/run-steps.py --base "$BASE"
```

**Never end your turn while it runs.** It takes 5–15 minutes. Background it if you like
and write `content.json` meanwhile, but then wait for it in the same turn — again and
again if a wait times out — until it exits, then build. Under `claude -p` / `copilot -p`
the session ends with your turn and takes every background child with it: eval run 16
ended on "you'll get the page once that step finishes", and the film died half-rendered.
Never start it a second time while one is running.

One command runs every deterministic producer — the branch's own review record, what
landed after it, diagram deltas, sequence diagrams, the container view projected from
them, Code City, the feature film, complexity, the REST contract and its two second
opinions, the logging scan, the design-system audit, code owners, the test manifest, the
Playwright recordings — each gated on its own prerequisite, each ledger-wrapped, none of
them able to skip its `end`. When `review-points.md` records an `audited-base` on this
branch past the fork point, every producer — and the page build after them — measures from
it rather than from `$BASE`'s merge-base: a page never mixes two bases.

The first two steps are the Review tab, and neither of them is yours to write:

- **`reviewpoints`** parses `review-points.md` into `.human-review/review-points.json` and
  resolves the two commits by trailer (`Review-Points:`, `Implements:`) into
  `.human-review/review-commits.json`. Skipped, with a reason, when the file is absent;
  **failed**, loudly, when it is there and will not parse. See Step 1.
- **`aftermath`** measures `<review commit>..HEAD` and splits it by
  `human-review.json`'s `"generated"` globs. Anything a human wrote after the agent
  stopped opens the Review tab as a red band, each commit with a `revert` button that
  stages an inverse and stops. This is the one fact on the page no diff can carry, and the
  one you must not narrate around: if the band is red, say in the guide what those commits
  were and why, because everything else on the page describes the branch as the agent left
  it.

Read the status table it prints. Three things in it are yours:

- **`skipped`** — a missing optional binary, an unconfigured step, or a stack that is not
  up (the design-system audit needs *both* builds served — it starts them itself from
  `steps.dsaudit.app`, and without that block it skips naming the URL that did not
  answer). Its tab is dropped and named under the strip.
  That is honest; do not work around it. **Unless another step feeds
  the same tab** — `tests`, `traces` and `testcov` all feed Tests — in which case the tab
  stays and only that step's part of it is missing: say *that*, not that the tab was
  dropped. Without `testcov` the Tests tab's right-hand column is the AI's pairing and
  says coverage was not measured; with it, the column lists the tests that *execute* the
  change, measured per test, and the pairing is a 🤖 chip on the rows AI named.
- **`failed`** — say so in the guide. A failed producer is a fact about the run.
- **`note`** — things only the run knows: an amber `PARTIAL LIST` seal that is *correct*,
  a suite that could not start, and above all **video exit 3 — filmed, and the feature did
  not hold.** Lead the whole review
  with that one. You no longer have to *notice* it to keep it: the step writes
  `assets/feature.run.log` every time and `assets/feature.verdict.json` on any non-zero
  exit, and the page draws that verdict as a red band over the player. Say it in the prose
  as well — the band is the floor, not the review.

  The film is recorded against the instance `steps.video.app` starts, not against whatever
  happens to answer on :4200. The design-system audit reads the same block (`steps.dsaudit.app`,
  usually `"video"` to borrow it) and starts **two**: this branch and the merge-base, which is
  the only way one step can compare two running builds. Until 19 Sep 2026 it named two fixed
  ports instead, nothing started them, and the UX tab had been empty on every review since. A project without that block gets the old behaviour plus one
  guard: the recorder asks the application which commit it is (`/actuator/info`, or
  `$HUMAN_REVIEW_APP_COMMIT_URL`) and refuses to film a different one. An application that
  cannot say only warns — but if you see that warning, check by hand which tree is up
  before you believe a frame of it.
- **`UNLISTED SCREEN`** (a `dsaudit` note) — the branch changed a routed component that no
  entry in `steps.dsaudit.screens` reaches, so the design-system audit never looked at
  the one screen the change was about. That is a hole in the evidence, not a finding to
  narrate around: add the screen to `human-review.json` (the list is the app's whole
  catalogue; only the screens whose DOM changed are drawn) and re-run `--only dsaudit`
  before writing the guide. The page prints the same warning in red at the top of UX.

## Step 4 — Write the layout, the ledes, and the matrix

This is the only step that is yours, and it is much smaller than it was. **The three piles
are not in it.** `content.json` names them and nothing more:

```json
"findings":    {"auto": "review-points"},
"autofixes":   {"auto": "review-points"},
"assumptions": {"auto": "review-points"}
```

and the build fills them from the branch's own record, with the same item shapes the
renderers already read. Do not type an item into any of the three. Do not "improve" one
the parser produced — the file is committed, and the page disagreeing with it is worse
than the page being terse.

```sh
${SKILL}/scripts/steps-ledger.py start guide --label "assemble content.json and build the page" \
  > .human-review/.step-guide
```

### The matrix, and the model that checks its pairings

The Tests tab's matrix is drawn by a script, `scripts/semcov.py`, every build: the ticket
(`gh issue view`, cached in `ticket-body.json`) rendered on the left and split into
sentences with stable ids — followed, when the branch implements an OpenSpec change
(`openspec/changes/<name>/`, matched by branch name or by the issue number its proposal
cites), by that change's requirements as a numbered list, paired like the issue's own
sentences; on the right the tests whose per-test coverage (`assets/test-coverage.json`,
from the `testcov` step) runs a line this PR changed, the ones about the change first, each
saying on hover which changed lines brought it there; and the colouring and hover/click
association between them. The script **proposes** links — shared words of the test's name
and assertions, a synonym table, literals, the changed lines its coverage ran — and every
scripted link carries its evidence. **A proposed link is a candidate, not proof**: run 5
painted "sortable by any column" green over a test that checks the page size.

So a model reads them. **Always run it, every review, after `run-steps.py` and before the
build** — from the repository root:

```sh
${SKILL}/scripts/rerun-model.py           # Sonnet by default, one call for the whole ticket
```

In one call it confirms or rejects every scripted link with a one-line reason, pairs the
sentences the script could not, and marks a sentence `narrowed` when a scope decision the
branch recorded (an assumption or a declined finding in `review-points.md`, a scope cut in
the OpenSpec proposal) delivers less than it says. Until it has run, no scripted link is
drawn as covering anything — the sentence reads *unconfirmed*. It writes
`.human-review/test-mapping.json` (schema: `reference/test-mapping.schema.json`; prompt:
`reference/matrix-prompt.md`), refuses an answer that fails the schema, names a sentence,
test or decision it was not given, or leaves a scripted link without a verdict; it asks
nothing only when no sentence makes a claim. Two passes then check the answer and can only
lower it, each recording what it took away in the sentence's `downgrades`: a free script rule
drops a link whose test shares nothing specific with its sentence — never an `asserted` link
whose quoted assertion `line` is in the body, and never the last links of a sentence (those
it lowers to `exercised`: a word filter alone does not turn a sentence red) — and a second cheap call
(`reference/matrix-check-prompt.md`) re-reads every kept link against the test body, must
copy the assertion line that proves the claim (looked up in the real body), and turns
`covered` into `partial`/`exercised`/`missing` where it cannot (`--no-check`, or
`"mappingCheck": false`, turns it off; it runs by default only on haiku, which it was built
for). The model is Sonnet unless `"mappingModel"` in `human-review.json` (or `--model`)
says otherwise — measured on eval run 8, one Sonnet call beat haiku plus its second read
on accuracy and time at about the same price; the press's cost — both calls — is one
row of `.model-runs.json` and shows on the cost tab. **Under GitHub Copilot**, pick the cheap
model (*Auto*, or `gpt-5-mini`) yourself: `rerun-model.py --prompt-only` prints the prompt
with its input, you answer it as JSON, and `rerun-model.py --answer reply.json` checks and
installs the answer; `--check-prompt` and `--check-answer check.json` do the same for the
second read. Never write the matrix HTML yourself — the build draws it. **A pairing older than
the coverage** (`test-mapping.json` older than `assets/test-coverage.json`, or a candidate
test it was never shown — `rerun-model.py` records what it showed in `offered`) makes the
build and `refresh-report.py` warn on stderr and the Tests tab say so over the ticket, with
the command. Nothing re-runs it for you: run `rerun-model.py` again.

### The prose that is left

Everything else in the content file is prose: `title`, `subtitle`, `pr`, `verdict`, an
optional `note`, and the Review tab's block titles and ledes. **No `summary`**: the
Review tab opens on the grade's computed reasons, and a `summary` is dropped there.
`verdict` is `{"score": n}` plus at most two `bullets` for what only you know — CI, the
open piles, a breaking API change, tabs without evidence and commits outside the review
are computed, and they cap your score.

**Every tab after Review is the scripts', not yours — write nothing on it.** Demo, API,
Data, Tests, Sequence, Structure, Code City, UX, Complexity, Logging and CODEOWNERS show
what a step produced. List them in `tabs` with the blocks in the reference strip
(`reference/content-schema.md`, *The tab strip*) and stop: no section of your own, no
`intro`, no snippet, no `html` block, no re-pointing of `swaggerdiff`, `video`,
`conceptual`, `requirements-map`, `ds-audit` or `complexity-delta` at another fragment.
The build owns those (`scripts/hrbuild/shared/layout.py`): it drops anything else on a
script-owned tab, rebuilds those sections from its own table, puts back a Demo tab declared
empty, and prints each drop on stderr. A run that wrote an API note, a Data section with
two hand-picked snippets and a `gate green` chip produced a different page from the
reference one — that is what this rule ends. **`scope` is computed chips only**
(`{"auto": "diffstat"}`, `{"auto": "tests"}`, `{"auto": "autofixed"}`): a chip you type
is dropped, and a `gate`/CI chip says nothing — a red gate means there is no page.

**The writing rule: show the code, do not narrate it.** A finding is not a story about a
defect, it is the defect, quoted. It still applies, to the tab ledes and the sections:

- **Two or three sentences of prose, hard ceiling.** Past that, the reviewer is reading
  your reasoning instead of their code.
- **Then the code, and most of it is code.** Prefer several short captioned snippets over
  one long one; a caption names the *one thing* in the lines (`"the null branch that never
  runs"`), not the block.
- **Never retype code** — `extract-snippet.py path:from-to` cuts it verbatim at build time.
- **Never type a number the page computes** (the diffstat, the cost tab and its label, the
  auto-fixed count, the test balance, tab costs, the pile counts). A hand-typed number goes
  stale with nothing noticing — `unit tests · 125 green (20 new)` was true until somebody
  wrote the next test, `lines +1198 / −863` sat on a page for six days matching no range in
  the repository at all, and *"10 buildings lit"* over the Code City shot was a count of a
  city nobody had recounted. That last one is gone for good: the `codecity` block takes no
  lede at all now, and the picture starts under the tab strip. `files` and `lines` come from
  `{"auto": "diffstat"}`, which measures the change set and leaves generated files out.
- **Never say a test's state yourself.** Name the test under the requirement it pins;
  `test-changes.py` reads the code for whether it is new, edited, deleted, commented out
  or sitting under an `@Disabled`. It is the one thing on the page you would have had to
  check by hand, and the one a reviewer is least able to check behind you.
- **Never name a specific artefact's absence.** *"`add-visit.genseq.puml` does not exist"*
  stopped being true while it was being written. Describe the **case**; let the renderer
  say which instances hit it.
- **Never write a paragraph the reader can see.** *"Twelve items came back. They are one
  list: the nine that need your judgement first, then the three I applied, greyed out and
  numbered straight on."* — every clause of that is on screen underneath it. The reader is
  an experienced developer who came for the finding, not for a description of the list the
  finding is in. Say only what looking cannot tell them, in a line, and let the page do the
  rest. Where the counts are the whole content, they are computed and you write nothing.
- **A tooltip is a few words.** It is read standing up, in one glance, with a hand on the
  mouse. Numbers the face could not fit, or where a click goes — then stop. Rationale is
  not tooltip material even when it is true: it goes in the code comment beside the thing,
  where whoever needs it is already reading.

Write `.human-review/content.json` against **`reference/content-schema.md`** — every shape,
every block type, the tab vocabulary, and everything the renderer already enforces so you do
not restate it.

**Change no code in this step.** Not a fix, not a comment, not a rename. The page used to
apply the non-disputable half of its own findings and leave them uncommitted for the human
to inspect; it no longer triages anything, because the triage happened in the coding
session and is recorded. An edit made here would land *after* the review commit, which is
precisely what the aftermath band exists to report — so it would show up on the page, in
red, attributed to a human.

## Step 5 — Close, check, refresh

```sh
${SKILL}/scripts/steps-ledger.py end "$(cat .human-review/.step-guide)"
${SKILL}/scripts/steps-ledger.py check          # exits non-zero on a renamed tab
${SKILL}/scripts/report-cost.py                 # outside Claude Code: --harness copilot-cli
URL=$(${SKILL}/scripts/refresh-report.py | tail -1)
```

`report-cost.py` is this run measuring itself — the `$` tab's fourth row, *this guide*: your
session's model work since `.started` (a Claude transcript, or the Copilot CLI / VS Code
session that ran `/human-review` here), the paid model steps you shelled out to, and how
long the run took and how much of it the model was working. It writes
`.human-review/report-cost.json` once per run; a refresh adds its own time there, never
money. The other three rows were measured by `/record-review` (`review-cost.json`).

`end` before `check`, so the guide record is closed when the check reads it. `check` before
the refresh, so a `DRIFT:` line is still actionable — once the page is written, a renamed tab
is a column of blanks nobody can tell from a step never instrumented.

`refresh-report.py` is the build and the server, in that order and for a reason: the build
writes `.human-review/.actions.json` beside the page, and that file is the only thing that
lets the served copy *run* the commands its buttons describe — the environment, the
drive-to-cue, the diagram rerun. A page read off disk, or out of the zip, has no manifest
next to it and copies them to the clipboard as it always did.

It is also the whole of the machine half of this skill, which is why it is one command and
not three to retype. It pins the build to the session that did the work, it builds
`--no-model` so a refresh cannot quietly buy a privacy verdict nobody asked for, and it
**refuses** to build in two cases. One is a missing model-written part — `content.json`,
the model's half of the test pairing (`test-mapping.json`) — which it cannot re-run. The other is a commit
carrying a `Review-Points:` trailer whose file is not on disk: the branch says it recorded
its own review and the record is gone, so the band reading *nothing records what was
reviewed* would be true of the disk and false about the run. Restore the file, or drop the
trailer if the claim was never true.

**The page opens itself.** The first time `refresh-report.py` starts the server it shows
the page — in the VS Code window's own browser, beside the code, when the run is in a VS
Code terminal and the Human Review VS Code extension (`vscode-extension/` in this repository,
`victorrentea.human-review`) is installed; in the default browser otherwise. Later rebuilds open nothing: the tab already
open reloads itself. Do not open it again by hand, and never `open review.html`.

**Print `$URL` as the last line of the run.** Then make sure the app runs from *this*
checkout, open the screen the change affects, and start `/relay` so they can dictate tweaks
— **only when a human is there**: never in a headless run (`claude -p`, `copilot -p`,
`$CLAUDE_CODE_ENTRYPOINT` = `sdk-cli`, CI). Headless, stop at the URL. An eval run that
started the relay sat 20 of its 40 minutes waiting for dictation nobody was going to give.

## Iterating on a review that already exists

Most invocations after the first are not reviews — the page is on disk and what is wanted is
a change to the *page*. **Has the code changed since the page was built?** New commits, a
force-push, a finding fixed → re-review, start at Step 1. You will usually not have to ask:
a commit that landed since the review commit is already on the page, in the aftermath band,
in red. Otherwise it is an iteration, and an iteration is one command:

```sh
${SKILL}/scripts/refresh-report.py                  # the page changed: rebuild, re-serve
${SKILL}/scripts/refresh-report.py --steps static   # …and the producers that need nothing up
${SKILL}/scripts/refresh-report.py --steps cheap    # the branch changed: re-derive the fast evidence too
${SKILL}/scripts/refresh-report.py --steps all      # …including the film, the city and the traced suites
${SKILL}/scripts/refresh-report.py --steps static --force   # …ignoring the cache: re-run every producer
${SKILL}/scripts/refresh-report.py --steps static --timing  # …and print what each one cost
```

**A refresh only re-runs the producers whose inputs moved.** Each step declares what it
reads — git pathspecs in the repository, the producer scripts themselves, and any artifact
an earlier step wrote (`STEP_INPUTS` in `run-steps.py`) — and a step whose fingerprint
matches the one beside its last successful run prints `unchanged, N s saved` and is skipped.
Edit one test body and the test manifest, the complexity bars, the logging scan and the
owners check re-run while the diagram deltas and the container view do not. Nothing has to
be remembered: the default is incremental, `--force` is how you ask for all of it, and the
cache is keyed on inputs and never on a timestamp, so a hit means *nothing this answer
depends on has moved* rather than *somebody said it was fine*.

On petclinic that is **1m32s → 5s** for a refresh that changes nothing, and about 6s for one
that changes a single test. Two thirds of the saving is not the producers at all: a step that
runs stamps `.steps.json`, which the build's cost ledger is cached on, so a single needless
step used to cost the *build* another forty-five seconds re-reading a conversation that had
not gained a turn. A refresh therefore no longer stamps the ledger — its step windows would
name a stretch of a later session in which none of the reviewed conversation happened. The
review's own run (Step 2) still does, which is what the cost attribution is built from.

**On the served page, the reader can do the middle one themselves.** The masthead carries a
**Rerun** beside the `served` badge — `refresh-report.py --steps static`, which is the
producers that need nothing up: the diagram deltas, the container view, the complexity
increment, the REST contract and its second opinions, the logging scan, code owners and the
test manifest. It rebuilds and the tab reloads itself on the same tab, keeping its place.
It is deliberately *not* `--steps cheap`: that one keeps `traces`, whose configured commands
are the project's own e2e suite. And it is deliberately not the film — the button says so on
its hover, because that is the one a reader is right to worry about.

Beside it, **Rerun + AI** is the same thing with *this skill's own model step* in front of
it. It is the button form of the matrix instruction above: `rerun-model.py` asks a cheap
model (Sonnet by default) to confirm or reject the script's pairings and pair the rest, rewrites
`test-mapping.json`, and then the static refresh runs with `--allow-model` and redraws the
matrix from it.

Spelt as a program rather than as a fork because a *reader* is the one pressing it: the page
is read outside any Claude session, and someone with the report open in front of them and a
branch that has moved cannot fork a subagent. From inside a run, Step 4 is still the way —
the fork has the conversation's context and this does not.

It costs cents, and its hover says what the last runs really cost; it asks in the page's
own confirmation panel before it spends anything, and the answer it replaces is copied to
`.human-review/.model-prev/` first: this replaces a judgement rather than refreshing one. `content.json` is not in it —
the layout and the ledes are yours, and no button regenerates them.

**The Demo tab has its own 🤖**, beside its ↺: the film-only equivalent. `rerun-film.py`
hands `reference/film-prompt.md` to `claude -p --model sonnet`, which rewrites
`.human-review/feature-script.js` (the old one goes to `.model-prev/` first, and a result that
is missing, empty, fails `node --check` or exports no function is refused), then
`refresh-report.py --steps video` films it again. Same confirmation, its price on the hover
out of its own ledger (`.human-review/.film-runs.json`), and the tab reloads when it is done.

Both buttons exist only where the page is served; read off disk or out of the zip there is
nothing behind them, so there is nothing there, and the paid one is also absent where
`rerun-model.py` is not beside the server. A rerun that fails puts the program's last lines
in a red band under the header rather than leaving the reader guessing, and only one runs at
a time **across both** — a second click joins the run in flight, and a click that asked for
the free half never starts the paid one.

**The free rerun is offered a second time, in the aftermath band.** A red band says a human
moved the code after the review was written, and there are two honest answers to that, as
two buttons: **Revert it** and **Regenerate the report**. The second is this same Rerun,
offered from the place the reader is actually looking at the problem — so when the commits
were legitimate (the infrastructure cherry-pick that had to land here), catching the page up
does not mean scrolling back to the header. Nothing for you to write: the band renders both.

That is the loop for "the branch moved, catch the page up", and it is the reason to prefer it
over a terminal: the three commands are one command here, and the one it runs is the one that
cannot cost anything.

**Never hand-run the build, the server or `run-steps.py` to satisfy a request.** Edit
`content.json` if the request is about its words, then run the program. That is the point of
it: the machine half of this skill is reproducible and free, the model half is neither, and
typing the commands by hand is how the two ended up being run together every time somebody
wanted a page refreshed. `--steps` exists so "refresh the page" never silently means
"record the feature film again".

### Every command the page offers, it offers the same way

Anywhere the page offers an action that is a shell command underneath, the offer wears a
**copy glyph** and — served — a **play glyph**. The command itself is *not printed on the
page*; it is in the copy glyph's hover. A click on the offer runs it where there is a server
and copies it where there is not, so a reader with a terminal open beside the page always
has the line and a reader with a server always has the button, and neither has to know which
copy of the report they are on.

This matters to you only as things not to do. Do not write "run this in a terminal" into a
lede. Do not retype a command into `content.json` — declare it (`runtime`, a diagram's
`rerun`) and let the renderer wear it. Do not describe what the glyphs do: the hovers say
it, and a sentence repeating them is the page reading itself out loud.

The refresh pins the build to the session that did the work (`.human-review/.session`),
because a build run in a later session cannot recompute what the first one spent and a page
that drops the number silently is a page claiming the review was free. If that id is gone,
publish no number rather than a measured-looking one: delete `.human-review/.steps.json`.
With no session to ask, the cost tab reports what it still can — what the conversation that
wrote the code spent — and says in words why the run's own half is missing. If neither half
is measurable the tab drops itself: a pill reading `$0` is a claim that this change was free,
which is not what an absence means.

**Do not re-run the coding session's review passes, do not `steps-ledger.py reset`, do not
rewrite `.started`, do not wipe `assets/`, and do not open ledger records for the
iteration's own edits.** They belong to the run they timed.

The server is sticky, so the URL does not change — and a tab already open on it reloads
itself once the build stops writing, so an iteration lands in front of the reader without
anybody pressing F5.

### What the model half is, so the program half can never be asked to fake it

Written by a model, once, when the human asks — and restored, never regenerated, if it goes
missing: `test-mapping.json` (the cheap model's verdict on the script's pairings, and its
pairing of the sentences the script could not decide) and `content.json`. `refresh-report.py` exits 3 rather than build a page
without them. The matrix itself is no longer on this list: `semcov.py` draws it on every
build from the ticket, the per-test coverage and that JSON. A model-written
`assets/requirements-map.html` from an older run stands in for the JSON (it is rendered as
it is, with a note on stderr) until `rerun-model.py` has run once.

**+1 LLM script:** `.human-review/feature-script.js`, the Demo film's script, is model-written
too and owned the same way — `refresh-report.py` never writes or regenerates it, and only a
model run (Step 3's fork, or `rerun-film.py` behind the Demo tab's 🤖) does. Its absence is
**not** a refusal: no script means no film, which the Demo tab already says.

`content.json` is on that list and no longer for the reason it used to be. It *was* the
judgement — which findings were raised, which were fixed, which were left, what the coder
assumed — written by a model at the end of a review and corroborated by nothing outside
itself. That record belongs to the branch now: the coding agent writes `review-points.md`,
commits it with the fixes, and the content file asks for the three piles with
`{"auto": "review-points"}`. What is left in it is the layout and the ledes. Still a
model's work, still not reproducible, still not something a program will invent for you; a
much smaller claim.

Everything else under `.human-review/` is the output of a program and may be re-run at any
time. The one model call that hides inside a *build* — the Logging tab's privacy verdicts —
is cached by a hash of what was sent, and a refresh runs `--no-model`: cached verdicts
render, uncached statements say *not evaluated*, and nothing is bought.

## Wrap-up

`.human-review/` is a throwaway artifact — remind the human to delete it rather than commit
it (`serve-review.py --stop` first). Print the path and the URL. **Do not list what you
fixed**, because you fixed nothing: what was fixed and what was declined is in
`review-points.md`, which is committed, and the page renders it. What is worth saying in the
last lines is what the *run* could not do — a step that skipped, a tab named under the
strip, a red aftermath band — and nothing else. Do not commit or push.
