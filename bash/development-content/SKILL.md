---
name: development-content
description: Content-editor-posture skill for ongoing work. Takes change_spec.md and change_design.md as primary inputs, with the product's CONTENT.md, the instance's writing bar and the product's existing strings as the standard, and writes change_text.md, the exact words this one change puts in front of a person, one string per state, each verbatim and checked against the product's banned words, so the Developer places them without choosing a word. Runs only when the design's Publishes text line reads yes. Never decides that verdict, never edits a standing rule, never names an identifier or file layout. Run when a change_design.md and tl_instruction.md are on the branch and the design says yes.
license: MIT
metadata:
  version: "1.0.2"
---

# Development Content

## Purpose

Write the words one change publishes. The change's spec says what it does and the design says where
the words live. This skill turns those into the labels, messages and prose a person reads, to the
product's standard, and hands them to the Developer in `change_text.md` in a form the Developer can
place as written. Nothing downstream re-judges the prose, so what this skill writes is what the
person reads (`<CORE>/roles/loaders/content_editor_global.md`, opening paragraphs).

**Produces:** `change_text.md` in the change folder, from `references/change_text_template.md`.

## When to Use

- The chain's `content` step launches it, between `plan` and `implementation`, for a change whose
  `change_design.md` carries `**Publishes text:** yes — <places>`. A hand-opened change reaches it the
  same way through `ad-hoc-plan`.
- **Content Editor role only.** Run outside a `content-editor` session or subagent, this skill halts
  `wrong-posture` (§ *Halts*) before it reads any input and writes no `change_text.md`.

**Do not use for:**
- A rule every future string is held to. That is the Content Manager's standing words (`CONTENT.md`,
  the writing bar), and a rule that this change's text needs and the standard lacks goes to
  `## Findings for the Content Manager`, never into the standard.
- Deciding whether the change publishes text. The architect decides it and writes the
  `Publishes text:` line; this skill reads it and never decides it
  (`content_editor_global.md`, § *Non-responsibilities*).

## Enter the worktree

The upstream stages ran inside an isolated worktree for this change, and `change_spec.md`,
`change_design.md` and `tl_instruction.md` are on its branch, not on `main`. Derive the worktree from
the **change key** before reading anything, and work inside it for the whole run.

The **change key** is `<YYYY-MM-DD>_<slug>`, the Tobiishi folder (`journey/tobiishi/<key>/`) and the
branch name. You know it from the invocation. If several worktrees exist under `<repo>/.worktrees/`
and the intended change is ambiguous, ask which one, once.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE="$REPO_ROOT/.worktrees/<key>"
test -d "$WORKTREE" || echo "No worktree for <key> — the upstream stages must run first."
```

If `$WORKTREE` does not exist, **STOP**: the upstream stages have not run for this change. Do not
create it here and do not fall back to `main`. Write the halt report where § *Halts* sends a halt
with no worktree.

**Write `$WORKTREE`'s value down, as the absolute path, before you `cd` anywhere.** A shell variable
does not survive from one command to the next, and for an external product the product worktree
carries a `.worktrees/<key>` of its own. Every `$WORKTREE` below means the instance path you wrote
down.

From here the worktree is the working root. Read every pipeline input from `$WORKTREE/`, write
`change_text.md` under `$WORKTREE/`, and commit with `git -C "$WORKTREE"`. The change arc stays on the
branch. The path comes from the key alone, by the same convention `development-design` and
`development-implementation` use, and nothing is handed between sessions.

**Locate the project.** The orchestrator passes the project name `<project>` with the key. The change
folder is `$WORKTREE/system/projects/<project>/journey/tobiishi/<key>/`.

**Resolve the product.** The step asks the path tool, every run, and never composes a product path by
hand:

```bash
python3 "<CORE>/tools/development_path.py" resolve --format json \
  --worktree "$WORKTREE" --project <project> --key <key>
```

A non-zero exit is a STOP, with the tool's `message` in the halt report. From the contract's
`product_path`, `product_repo` and `product_worktree`: `<sub>` is `product_path` when it is relative,
else `product_path` relative to `product_repo` (`.` when the same), and
`PROJECT_DOCS = <product_worktree>/<sub>/docs`, with `PROJECT_ROOT` its parent. For an in-repo
product `product_worktree` is `$WORKTREE`; for an external one it is the product worktree opened for
this change, never the product's primary checkout.

## Workflow

### Step 1 — Check the posture

Before reading any input, confirm this session is a `content-editor` session or subagent. If it is
not, halt `wrong-posture` (§ *Halts*), write no `change_text.md`, and say in one sentence what to
open: "development-content is content-editor work. Open a session or subagent as `content-editor`."

### Step 2 — Enter the worktree and resolve the product

Run § *Enter the worktree*. Record the absolute `$WORKTREE` and `PROJECT_DOCS`.

### Step 3 — Read the verdict

Read `$WORKTREE/system/projects/<project>/journey/tobiishi/<key>/change_design.md` and take the first
line that starts with `Publishes text:` once its markdown dressing is removed (the header form is
`**Publishes text:** yes — <places>`). The value's first word, with its dressing removed, is the
verdict, and it must be exactly `yes` or `no`.

| The line | This skill |
|---|---|
| `yes`, with or without places after it | Continue. The places after the word are the blocks of `## Text`. A bare `yes` names none, and Step 4 reads the design for where the words live. |
| `no` | Halt `no-text-to-write`. Write no `change_text.md`. |
| missing, `Yes`, `maybe`, empty, or no `change_design.md` | Halt `missing-text-verdict`. Write no `change_text.md`. |

**This skill never decides the verdict.** It does not read the spec to find out whether the change
"really" publishes text, and it does not turn a `no` into a `yes` or the other way
(`content_editor_global.md`, § *Non-responsibilities*: it does not decide whether the change needs a
message at all). The engine already gates on this line and launches the step only on `yes`, so a `no`
or a missing line here means the run was started by hand against a design the engine would not have
run, and the report says so.

### Step 4 — Read the inputs

Read, in this order, and nothing from `tl_instruction.md`:

1. `change_spec.md` — what the change does and for whom. Copy `Date`, `Category` and `Behaviour` from
   its header verbatim.
2. `change_design.md` — the places the words live, from the `Publishes text:` line and the design's
   own description of the states. It is the primary input
   (`content_editor_global.md`, § *Inputs you expect*).
3. `$PROJECT_DOCS/CONTENT.md` when it exists. A product with none yet is a normal case, and then the
   instance's writing bar governs alone.
4. The instance's writing bar, `system/doctrine/writing_bar.md`.
5. The product's existing strings under `$PROJECT_ROOT`: the labels, messages and prose a person
   already reads there. They show which terms the product uses and what the standard looks like
   applied. Read them as vocabulary, and read no code for how it is built.

**This skill reads no `tl_instruction.md`.** The instruction is the Developer's scaffold and carries
identifiers and a file layout. The Content Editor names no identifier and no file layout
(`content_editor_global.md`, § *Non-responsibilities*), and an input that holds them is an input that
tempts the text toward them.

### Step 5 — Write the text

Write one string per state, to the standard's voice, terminology and message patterns and to its
accessibility and localization rules, in the form `references/change_text_template.md` sets.

Before a string is settled, answer four questions: what does this person know at this moment, what
is actually true of the system here, what must they be able to do next, and what happens if they do
nothing (`content_editor_global.md`, opening). Then:

- **Ground every claim.** A string that names a cause the system did not establish, a state it did
  not reach or a guarantee it does not make is wrong. Where a claim cannot be grounded, write the
  smaller true thing.
- **Cover the states nobody wrote a message for**, and collapse two strings for one concept into one.
- **Write every string whole**, so it can be translated and read cold. A sentence a runtime would
  assemble from fragments is taken apart into whole strings, each with its variable part marked in
  braces and described.
- **Use the product's own terms**, one term per concept.
- **Leave a name out of the strings, and out of the file around them.** The text names no identifier,
  no file, no layout and no framework, and chooses nowhere a string lives. The places are named as the
  person knows them.
- **The text is in a form the Developer can place without choosing a word.** Each string is verbatim,
  exact in its characters, with the state it belongs to named beside it. A string whose placement
  would need a word the Developer must pick is not finished.

Log each improvement over the request's own phrasing in `## Wording decisions`, with its reason. A
silent divergence is the failure mode.

**Where the standard does not answer.** A string that needs a rule the standard does not state goes
in `## Findings for the Content Manager`: the string, the missing rule, and how the string was
written meanwhile, as plainly as the existing rules allow. Keep writing the strings the standard does
cover. The run never writes the rule itself, into `CONTENT.md` or the writing bar or anywhere else.

**Where the meaning would change.** A string that cannot be written without changing what the change
means, a calculation, approved legal language or the standard, is not written. Halt `meaning-change`
(§ *Halts*). The incoherence goes to the owner of the change's meaning as a question, never as a
rewrite.

### Step 6 — Check the text cold

Read `change_text.md` as the Developer will, in a fresh session with nothing but the file. For each
string ask whether it stands alone, whether it is the state it is filed under, whether it traces to a
place the design's line names, and whether it contains a word the Developer would have to choose or an
identifier. Check each place the design's line names has a block, and that no block exists for a place
it does not name. Fix what fails.

**Then check every string against the words the product does not use.** Read the banned lexicon in
`CONTENT.md` (its terminology section: the banned words and the rejected names, each with what to say
instead) and any word the writing bar bans, and search every string in `change_text.md` for each, in
every inflection. Where the product carries a check that enforces its vocabulary — a word-list lint,
an audit target, a test that reads its strings — run it over the strings too, and read its result
rather than assuming it. Each hit is rewritten with the replacement the standard gives and logged in
`## Wording decisions`. No banned word is committed: the Developer places the text verbatim, so a word
that a downstream check refuses cannot be fixed there, only deferred.

### Step 7 — Commit

Commit `change_text.md` on the change branch through the shared builder. Read
`<CORE>/doctrine/governance/commit_via_builder.md` and supply its variables: `<repo>` = `$WORKTREE`,
the file to stage = the change folder's `change_text.md`, plus subject / body,
**`--actor content-editor`** (the agent `launcher.md` launches this skill as, named and never derived),
**`--skill development-content`** (this skill's own name, so `Skill-Version:` records what ran), the
directional line, and `--reasoning-effort` when the launch resolved one. Never hand-write
`git commit` or a trailer.

**The same commit removes any earlier `halt_report.md` this skill left in the change folder.** An
earlier halt of this skill leaves a report in the folder, and a report left beside the text it
preceded reads as a halt that still holds. Pass it to `--rm`. A `halt_report.md` that another stage
wrote, or that begins with the engine's own marker line, is not this skill's and is left alone.

This skill does not advance any inbox. It produces `change_text.md` or a halt report and returns its
step-outcome message (`<CORE>/doctrine/flow/step_outcome_contract.md`), and the chain sequences the
next stage from the folder.

## Halts

**Halt, don't ask.** This is an automatic pipeline skill. When a halting condition is found, write
`halt_report.md` and stop. Do not ask the user for clarification.

| Reason | When | Report location | Committed |
|---|---|---|---|
| `wrong-posture` | the session is not a `content-editor` session or subagent | `$WORKTREE/system/projects/<project>/journey/tobiishi/<key>/` when `$WORKTREE` exists. When it does not, the main checkout's `system/projects/<project>/journey/tobiishi/<key>/`, never creating a directory to hold it | **No.** A run out of posture has no seat to commit as. |
| `no-text-to-write` | the design's `Publishes text:` line reads `no` | the change folder in the worktree | Yes, as `content-editor` |
| `missing-text-verdict` | the line is missing, or its first word is not exactly `yes` or `no`, or there is no `change_design.md` | the change folder in the worktree | Yes, as `content-editor` |
| `meaning-change` | a string cannot be written without changing what the change means | the change folder in the worktree | Yes, as `content-editor` |

The two places `wrong-posture` may land are both places the engine's `DiskReader.halt_report` reads,
so the walk stops on it. Where neither the worktree nor the main checkout's change folder exists, the
report goes in the deepest of the change-folder directories that does, and **no directory is created to
hold it**: a missing directory is the finding, and a run that creates one leaves a folder claiming a
change is open where none is.

A halt report names the reason on its own line first (`**Halt Reason:** <reason>`), then what the run
found, concretely and specifically, with the line quoted from `change_design.md` where the reason is
about it, then what would be needed to proceed:

- `wrong-posture` — re-run from a `content-editor` session.
- `no-text-to-write` — the design says the change publishes no text. If it does, the architect corrects
  the `Publishes text:` line in `change_design.md` and the walk starts again.
- `missing-text-verdict` — add `**Publishes text:** yes — <places>` or `no` to `change_design.md`,
  commit it, and start the walk again.
- `meaning-change` — name the string, the meaning it would move, and the question for the owner of that
  meaning.

A halt writes **no `change_text.md`**, and the commit of a halt report is made as `content-editor`
with `--skill development-content`, exactly as Step 7's commit is.

## Critical Rules

- **Content Editor posture only.** Outside it, halt `wrong-posture` before any input is read.
- **Never decide the verdict.** `Publishes text:` is the architect's line. `yes` runs this skill. Any
  other value halts it.
- **Exact output filenames.** On success `change_text.md`, on a halt `halt_report.md`, and no other.
- **No `tl_instruction.md`, no identifier, no file layout.** The text is words, not code.
- **A rule is the Content Manager's.** A missing rule is a finding, never a rule written here.
- **A change in meaning is a halt, never a rewrite.** Product meaning, calculations and approved legal
  language stay as they are.
- **Every string is verbatim and whole.** The Developer places it without choosing a word, and a string
  that cannot be placed as written is recorded by the Developer, never reworded, and revised in a later
  change.
- **Every improvement is logged** in `## Wording decisions`, with its reason.
- **No banned word is committed.** Every string is checked against `CONTENT.md`'s banned lexicon and
  the writing bar, and run through the product's own vocabulary check where it has one (Step 6).
- **The commit that lands the text removes this skill's earlier halt report.**
- **Worktree-first.** All writes and commits go through `$WORKTREE`, never `main`.
