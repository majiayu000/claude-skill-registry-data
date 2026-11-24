---
name: dry-run
description: 'Dry-run the Senzing Bootcamp plugin to find defects that reading it cannot: phase 1 verifies every MCP call against the live Senzing MCP server, phase 2 executes the hooks and bundled scripts against a realistic scratch project, phase 3 walks the conversational layer with the maintainer answering as the Bootcamper, or with a simulated Bootcamper answering from a separate process. Use when the maintainer wants to dry-run, smoke-test, or exercise the plugin, verify it actually works rather than reads correctly, or asks what a fresh audit should look at next. Maintainer tool — not part of the bootcamper experience.'
argument-hint: "[phases: 1, 2, 3 or all] [module phase 3's analysis starts at] [--simulated [persona]] [--draft <run-dir> | --file <run-dir>]"
---

# Dry Run

This is a **maintainer** tool for developing the Senzing Bootcamp Claude Plugin
(SBCP). It is never invoked during a bootcamp. It is a **test-gate action** before
publishing.

## Why this exists

Three full audits and 399 passing tests all read the plugin. Then one dry run found
that **Module 5's mapping workflow could not execute at all** — `mapping_workflow`
requires a `workspace_dir` parameter the plugin never passed, and five of its eight
documented action names were payload field names rather than actions. The
instructions were coherent, internally consistent, well cross-referenced, and wrong
about the tool they called.

That is the defect class this skill exists for, and it has a shape:

> Static analysis can only confirm the plugin agrees **with itself**. It cannot see
> where the plugin disagrees with the world — the MCP server's real schemas, the
> filesystem, a rendered artifact, or a human being answering questions.

Each phase points at one of those. Run them in order; each is independently useful
and each has found real defects.

| Phase | Checks the plugin against | Needs |
|---|---|---|
| 1 — [MCP call contracts](phase1-mcp-contracts.md) | the live Senzing MCP server's schemas | MCP access |
| 2 — [Hooks and scripts](phase2-hooks-and-scripts.md) | a real filesystem and real artifacts | `python3` |
| 3 — [Conversational layer](phase3-conversational.md) | a human answering questions | **the maintainer**, or a simulated Bootcamper (`--simulated`) |

Phase 1 is the highest yield per minute — it targets the plugin's hard dependency
and its entire factual foundation. Start there unless the maintainer says otherwise.

## Before you start

1. **Ask which phases to run** if the maintainer did not say, including when there is
   no argument. Present them as a numbered list (1, 2, 3, or all three); do not
   assume, and do not read "dry-run the plugin" as "all three". Phase 3 costs the
   maintainer's time in a way 1 and 2 do not, so it is never implied by "dry-run
   the plugin". (INV-333) **An argument naming phases is the answer to this question:** start
   at the lowest one.

   ⛔ **If phase 3 is among them, ask a second question before anything else runs:
   which module the analysis starts at.** A trailing module name in the argument answers
   it. Otherwise list the eleven modules in order, numbered,
   and mark which ones this environment can actually reach (step 3 below is that
   check). Everything before the chosen module is walked as a Bootcamper sees it with
   the analysis off; the analysis begins when that module does. This is not a
   refinement — a walk that analyzes from the top runs out of context around Module 1
   every time, which is why no phase-3 run has ever reached the later modules. Full
   rules, including what the fast-forward may and may not do, in
   [phase3-conversational.md](phase3-conversational.md).

   ⛔ **(INV-369, INV-333) Then a third: who answers as the Bootcamper.** The maintainer-answered walk
   is the default, so offer it first: (1) the maintainer, or (2) a simulated Bootcamper, with a
   persona. `--simulated [persona]` in the argument answers it, and a phase-3 argument without
   it answers it as the maintainer. With no argument every question is asked: whether to run
   phase 3, the start module, and who answers; nothing is assumed. The
   simulated walk spends tokens, and the human walk costs the maintainer's time, so neither is
   inferred from silence. The procedure is [phase3-conversational.md → "A simulated
   Bootcamper"](phase3-conversational.md#a-simulated-bootcamper---simulated-persona).
2. **Work outside the repo.** Phase 2 and 3 create a bootcamp project. Put it in
   `$HOME/senzing-bootcamp-dryrun` (or `-phase3`), never inside the repo and never
   under `/tmp` — a maintainer hook blocks system-temp writes, and the plugin's own
   file-placement rules assume a project directory. `scaffold_project.py` refuses both.
   Its `--run-root DIR` is for `/auto-test` alone, which passes the `mkdtemp` run root it
   created: a target inside that root is built, and any other `/tmp` target is still
   refused (#840).
3. **Note the environment's limits up front**, so the report can state them rather
   than imply coverage it did not have. Check and record: is the `senzing` Python
   package importable? is `libSz.so` present? is `fpdf2` installed? is `docker`
   available? is there a headless browser? Missing pieces are fine — silently
   skipping the paths that need them is not.
4. **Run the coverage reports to choose where to look.** Two blind spots have hidden
   real defects — an invariant no test cites, and a spec file a ledger entry never
   recorded changing. Both are reports rather than tests, because a hit in either is
   usually legitimate; they tell you where a conformance sweep is unguarded:

   ```bash
   python3 .claude/skills/dry-run/coverage_reports.py both
   ```

   `invariants` lists invariants no test mentions by ID — INV-060 and INV-097 both sat
   there while standing unimplemented for weeks. It splits its hits three ways so the
   actionable number is visible: **fully superseded** (filtered — a retired rule needs no
   test, and the list comes from the index's own "Fully superseded" entries, **not** a grep,
   because a *partly* superseded invariant such as INV-040 still binds), **bootcamp outcome
   invariants** (the first 50 ids — banners, questions, "the SDK is installed", which no
   offline suite can assert, so they are phase 3's business rather than test debt), and the
   **development rules** that remain. `shipped` is its mirror on the other side of
   the contract: invariants that **name a shipped artifact** (a path, module, step or bundled
   script) and that no file under `source/`, `hosts/` or `tools/bootcamp_build/` cites, so the rule binds a step the guide cannot
   look it up from (INV-183). It is the question `conformance.py rules` cannot ask — that scan
   is satisfied by *any* `INV-NNN` in a section, which is how it reported **0** on 2026-08-13
   while INV-212 was named nowhere near the step it was registered from. Development-environment
   rules are exempt via the `INVARIANTS.md` index group that declares itself the exemption, and
   invariants stating a general property with no artifact are not reported at all — both filters
   exist so the output stays short enough to read. `affected` lists ledgered specs whose
   `## Affected files` predicted a path the entry's `Files changed:` never recorded —
   which is how the graduation half of INV-097 went missing. Its rows are classified, most
   actionable first: **names a real current file**, then **path no longer exists**, **bare
   filename** (an artifact, not a repo path) and **glob**, the last three being predictions
   the scan structurally cannot match. Within the first class, **★ marks the rows whose spec's
   `## Acceptance criteria` name the file** — the discriminator INV-097's defect actually had,
   since an `## Affected files` entry alone is only a prediction. `negatives` lists every dated
   "this MCP tool does **not** contain X" claim, oldest server version first — that one is
   **phase 1's worklist**, not just a report, because a negative is the single claim shape
   the offline suite can never notice going stale. Read-only, stdlib-only, exit 0
   whatever it finds. The `auto-test` skill can call it the same way.

   `unmarked` is `negatives`' complement and the newer half of phase 1's worklist: dated
   tool-absence claims in **shipped prose (the plugin and `hosts/`) that carry no marker**, which `negatives` cannot
   see because it only lists what is already tagged. The **date** is the discriminator — undated
   prose explaining how a tool behaves is not a re-checkable claim and is not reported. A hit needs
   judgment (it may be prose *about* behavior), which is why this reports rather than gates, and
   the vocabulary is a phrase list, so a miss is weak evidence. ⛔ **Never mark one of these by
   stamping today's date on it** — re-ask the owning route first; if the server has moved, the fix
   is to correct the prose, not to certify it.

   `negatives` also reads **`specs/DECLINED.md`** — the only file under `specs/` it scans,
   added 2026-08-13. The rest of `specs/` is a frozen archive (INV-307): a spec body there is a
   record that is never re-verified, so its negatives are history, not claims. `DECLINED.md`
   stays live, and a negative in a `Revisit if:` clause is re-read as authority whenever the
   decline is revisited, with nothing else re-verifying it. Give those markers the same weight
   as a shipped claim: a wrong one sends the next revisit check to the wrong answer, which is
   exactly what a phase 1 sweep found there.
5. **Exclude the walk's own docs from any Markdown-lint hook you run**, if your
   `~/.claude/settings.json` has one. A `PostToolUse` hook matching `Write|Edit` that
   enforces CommonMark will reject the guide's writes to `docs/bootcamp_recap.md` at
   **every module close**, for MD022/MD032 — rules the bootcamp defers on purpose.
   `bootcamp-onboarding/ground-rules.md` tells the guide to write these files plain and
   leave prettification to graduation, which runs one normalization pass before the recap
   PDF renders.

   ⛔ **Neither side is wrong, and the plugin is not what needs changing.** It ships **no
   `PostToolUse` hook on Write or Edit** — its one `PostToolUse` hook, `failed-run-net.py`
   (#910), matches Bash only and never blocks — so this
   is host configuration, no Bootcamper can encounter it, and it is friction in *your*
   walk rather than a defect in the product. ⛔ **Do not "fix" it by relaxing the
   defer-to-graduation rule or by adding a hook to the plugin**: both push a maintainer's
   environment into behavior every Bootcamper carries, to solve a problem none of them has.

   **What to exclude: top-level `docs/*.md`.** ⚠️ Take that set from what
   `source/scripts/normalize_docs_markdown.py` globs rather than
   maintaining a file list — it globs `docs/*.md` **non-recursively**, so
   `docs/feedback/SENZING_BOOTCAMP_FEEDBACK.md` is out of scope structurally
   (INV-015) instead of by an exclusion someone has to remember, and
   `docs/REVISIT_BOOTCAMP.md` is **in** scope because it is a top-level `docs/*.md`.
   A hand-kept list drifts the moment the normalizer's scope changes; this one cannot.

   **The same goes for your `~/.claude/CLAUDE.md`.** A user-level instruction file is read
   by every `claude` process this machine starts, the bootcamp's included, so a rule such as
   "end every response with a 👉 **Suggested next step:** line" is obeyed by the guide
   and then scored against the plugin. One walk filed **13 BREAKING
   `INV-251-multi-question` findings** that way, every one of them the host's rule rather
   than the plugin's text, and whether a given run was contaminated was not visible in its
   report (#733).

   ⛔ **(INV-379, INV-417) A host response rule is never a plugin defect, and never a plugin change.** The
   shipped plugin contains "Suggested next step" nowhere; the rule is your configuration and
   no Bootcamper carries it, so writing the host's response style into the plugin would push
   one maintainer's environment into every bootcamp to solve a problem none of them has.
   Neither side is wrong here, any more than it is for the hook above. A **simulated** walk
   now keeps it out for you — `walk.py` runs both of its
   processes with `--setting-sources project,local`, and `autotest.py` names any host
   instruction file the run could still read as a `coverage_limits` line
   ([`auto-test` → the sandbox](../auto-test/SKILL.md#the-sandbox-and-why-each-layer-is-there)).
   A **maintainer-answered** phase 3 walk runs in your own session, where your `CLAUDE.md`
   still applies: read a two-👉 turn there as your own rule until you have ruled it out.

## Absolute rules

⛔ **Nothing leaves the machine except two outward acts, each under INV-314's gate: show
the maintainer the exact text and get a yes, given out of character, one record at a time. For
issues and comments it may instead be one yes for the whole list shown in one message (INV-314,
2026-10-13 note), under the conditions in
`.claude/skills/feedback-to-issues/drafts.py` → "The batch yes".**

1. **A GitHub issue, or a comment on an existing one, in this repository.**
2. **`submit_feedback`, only for a finding whose verdict is `mcp-server`**: certain that the
   defect is the server's and that nothing in the Senzing Bootcamp needs to change.
   *Certain* means re-verified live against the server, with any absence claim carrying
   `owner-checked:` naming the route that owns the fact (INV-194, INV-213). ⛔ A `both`
   finding does not qualify: it gets a GitHub issue with the drafted upstream message
   inside it, for the maintainer to send. The send follows `/feedback-to-issues` Step 8: a
   self-contained technical report, everything identifying stripped (INV-321),
   `category='bug'` or `'feature'`, and ⛔ never `category='license_request'`.

A yes given in character, while answering as the Bootcamper, never authorizes either act, and
neither does a yes from a simulated Bootcamper: the walk blocks both tools by flag
([`auto-test` → Guardrails](../auto-test/SKILL.md#guardrails)).
A dry run must not file junk upstream or transmit a name and email. Verifying a tool's
schema sends nothing; `download_resource` on anything large stays forbidden.

⛔ **(INV-369) Never answer as the Bootcamper in the session that runs or grades the bootcamp.**
That is self-play, and phase 3 cannot be self-played: the plugin forbids simulating the
Bootcamper's response (INV-007), and an assistant grading its own 👉 discipline proves
nothing. **A simulated walk (`--simulated`) is not self-play and not
fabrication:** a separate process that has never seen the plugin answers, the process
running the bootcamp is never told it is under test, and this session grades only the saved
transcript, afterwards. This session never writes, edits or adds an answer to that walk. If
the maintainer is unavailable and no simulated walk was chosen, say phase 3 is untested
rather than approximating it.

⛔ **Commit or copy aside before mutating the tree.** This one cost real work twice
in the session that produced this skill. `git restore` cannot tell your fix from a
defect you injected to test a guard — it reverts both. Either commit the fix first,
or back the file up with `cp` and restore with `mv`.

⛔ **Clear `__pycache__` after any same-size revert.** `"…"` and `"..."` are both
three bytes; a restored file with the same size and a same-second mtime lets Python
reuse bytecode compiled from the mutated source, so the suite keeps failing on
already-correct code. `find . -name __pycache__ -type d -exec rm -rf {} +`.

⛔ **A `pgrep -f` guard matches its own command line.**
`while pgrep -f "unittest discover -s tests"; do sleep 15; done` never exits: `-f`
matches the full command line, and the watcher's own `bash -c` argument contains the
pattern, so it finds itself. Bracket the first character — `"[u]nittest discover"` — or
match the process rather than the string (`pgrep -f "python3.*unittest"`). Four such
watchers spun for **27 hours** after a phase-2 run here, and they kept each other alive:
killing three would not have freed the fourth, because it still matched them.

⚠️ **The second half is why this is a rule and not a footnote.** Two later "is anything
still running?" sweeps reported *nothing* while all four were spinning — the sweeps
searched for `unittest|until grep` and these used `while`, so the cleanup check missed the
thing it was written to find. When verifying a scratch run left nothing behind, list the
session's own shells (`pgrep -a bash`) rather than grepping for the idiom you remember
using.

## What to do with a finding

A dry-run finding is only half done when the plugin is fixed. Follow this for each:

1. ⛔ **(INV-317) Draft each finding into the run's dated `specs/IMPLEMENTED.md` entry as you
   find it, marked not yet filed, before fixing anything** — never into a new file under `specs/`,
   which is a read-only archive (INV-307). A finding that exists only in the conversation is
   not recorded, it is *remembered*, and it dies at session end or the next compaction. This
   is not a filing preference; it is the difference between a durable improvement and a good
   afternoon. How the draft becomes a GitHub issue is [the finding
   lifecycle](#the-finding-lifecycle) below.

   - **Shape:** `../feedback-to-issues/issue-template.md` — the same body the issue will
     carry. Cite `file:line`, and date every MCP claim with the server version that
     produced it.
   - **When:** immediately for phase 3, because a walk stops on whatever turn the
     maintainer stops it; by the end of the phase at the latest for phases 1 and 2.
     Do **not** defer to the final report — the report is the last thing that happens
     and the first thing lost.
   - **Even when you fix it the same session.** The issue is what the `IMPLEMENTED.md`
     entry names, what makes the finding legible to whoever reads it next, and what
     survives if the fix has to be reverted; the fix can close it. Filing the issue is not
     made redundant by also fixing it.
   - **Grouping:** one issue per root cause. Several small prose corrections from one walk
     may share an issue when each is a few lines in the same file or two — give each its own
     acceptance criteria so they stay independently implementable — but two unrelated
     defects never share one.
   - **Where not to put it.** Not the session scratchpad: the maintainer's global
     `write-location-gate.py` blocks system-temp paths, so a `/tmp/...` note fails outright.
     Not repo `tmp/` either — it is not gitignored, so it becomes untracked clutter that
     "leave the repo with only intended changes" then tells you to delete.

   Phase 3's collapsed test-notes blocks are *working notes* — the running observation
   channel for a walk in progress. They are never the record.

2. **Fix the class, not the instance,** where the class is cheap to remove. The
   `_clip` ellipsis defect had three call sites; changing the suffix to ASCII inside
   `_clip` made the ordering hazard unreachable instead of fixing three callers.
3. **Write a test in the repo-level `tests/`** — stdlib only, no `source/` (INV-108).
   A dry run you cannot repeat cheaply is a one-off; a test is the durable half.
4. ⛔ **Negative-control the test.** Reintroduce the defect, confirm the test fails,
   revert. A guard whose docstring claims more than its assertion checks is worse
   than no guard, because it certifies what it never tested. This is not optional:
   in the originating session, one existing test had **pinned the wrong premise**,
   which is how the defect it covered survived three audits.
5. **Record the outcome** in the same `specs/IMPLEMENTED.md` entry step 1 drafted into,
   naming the issue each finding became, and either queue the invariant it establishes or
   state that it establishes none — `tests/test_spec_ledger_invariants.py` enforces this for
   entries dated on or after its cutoff.
   ⛔ **(INV-365) Route it through `/review-invariants`; never edit `specs/INVARIANTS.md` here:** write a
   `DEFERRED INVARIANT` block in the run's `specs/IMPLEMENTED.md` entry, as
   [`review-invariants` → "Writing one"](../review-invariants/SKILL.md#writing-one) shows
   (INV-300), then tell the maintainer to run `/review-invariants`. Two homes, two
   purposes: the **issue** is the finding as pending work, the **ledger** is what was done
   about it and where each finding went. A finding you did not fix has an open issue (or a
   draft marked not filed) and a ledger line saying it is open, which is exactly right — it
   stays visible as outstanding rather than looking handled.
6. **Propose a correction when the invariant itself is wrong.** INV-132
   asserted the MCP reference could not answer parameter shapes; the server answers
   them. The correction is a dated note explaining what was verified and when.
   ⛔ **(INV-365) Route it through `/review-invariants`; never edit `specs/INVARIANTS.md` here:** write a
   `PROPOSED AMENDMENT` block in the run's `specs/IMPLEMENTED.md` entry, as
   [`review-invariants` → "Writing one"](../review-invariants/SKILL.md#writing-one) shows
   (INV-300), then tell the maintainer to run `/review-invariants`. An invariant that
   encodes a false premise is worse than a missing one.

⛔ **Do not end a run with unwritten findings.** Before reporting, list what you found and
confirm each one is drafted in the run's ledger entry and has reached the end of the
lifecycle below. "I described it in the report" is not recorded — the report is a message,
and messages are not durable. This rule exists because a phase-3 walk reached eight turns
with four findings held only in conversation, and it took the maintainer asking *"are you
keeping notes that might lead to improvements / specs?"* to surface it.
Under `--draft`, a finding's `drafts.py` record counts as recorded, and the caller writes the
ledger (INV-317's 2026-10-13 note).

## The finding lifecycle

Where a drafted finding goes, from step 1's ledger draft to its GitHub issue:

⛔ **(INV-368) With `--draft <run-dir>`, this run files nothing, fixes nothing and sends nothing, and writes
nothing outside `<run-dir>`** but its scratch project. A simulated walk's is `autotest.py`'s
sandbox, and its reports go to `<run-dir>/walk/` ([phase 3](phase3-conversational.md), "A
simulated Bootcamper" step 3). Each finding and upstream message becomes a
[`drafts.py`](../feedback-to-issues/drafts.py) `add` record as it is found, in place of steps 1, 3
and 5 below; [What to do with a finding](#what-to-do-with-a-finding) steps 2–6 are not run, and the
run ends with `drafts.py list`. `--draft` is the release cycle's interface (#573), and the caller records
unresolved drafts (INV-317). **With `--file <run-dir>`**, file what `drafts.py file-plan` prints,
after a yes for each record or one yes for the whole list shown in one message (INV-314,
2026-10-13 note), under the conditions in `.claude/skills/feedback-to-issues/drafts.py` → "The batch yes",
then report; an upstream draft is never sent by `--file` and keeps its own yes. Both stages, the
manifest and its statuses are stated once in `drafts.py` (INV-300).

1. **Draft — on sight.** The run's dated entry is a `## dry-run-<YYYY-MM-DD>` heading in
   `specs/IMPLEMENTED.md`, marked **Not a spec** as the `production-readiness-audit-<date>`
   entries are, and opened at the first finding. The ledger is a live record (INV-182), so the
   draft is durable at once and the walk never stops for it. Write no new file under
   `specs/` (INV-307): it holds live records only, the table in `specs/README.md` is the list
   of the files that belong there, and the frozen archive of the spec files is in the
   repository `specs/README.md` names. The 2026-09-24 run that followed the pre-freeze
   instruction wrote four new files there and turned the suite red.
2. **Search open and closed issues before filing**, as `/feedback-to-issues` Step 4 does
   (`gh issue list --state all --search "<terms>"`). A finding already tracked points at that
   issue instead of opening a duplicate; a comment adding what the issue lacks goes under the
   same gate as an issue. A duplicate of a **closed** issue references it and says what is
   new, and re-filing it needs a reason that answers the earlier decision.
3. **File at the end of phase 1 or 2, and when a phase 3 walk pauses or ends** — never
   mid-walk: a filing question inside a bootcamp turn adds a second 👉 and changes what is
   being tested. Then, one issue at a time:

   ⛔ **(INV-314) Show the maintainer each title and body and get a yes, one issue at a
   time, or one yes for the whole list shown in one message (INV-314, 2026-10-13 note), under
   the conditions in `.claude/skills/feedback-to-issues/drafts.py` → "The batch yes".** Any
   other "yes to all" is not assent to each. Filing is outward-facing and immediate: the
   issue is visible the moment it exists and its notifications have gone out; it can be
   edited or closed but never un-filed.

   ```bash
   gh issue create --title "<the defect, not the symptom>" --body-file <file>
   ```

   ⛔ **(INV-319) Never pass `--repo`** — this repository only, as `/feedback-to-issues` Step 7 says.
   Then replace the draft's marker with the issue number.

   ⛔ **(INV-318) Never apply `unattended-ok` to an issue the run files.** Choosing what runs unattended
   is the maintainer's decision alone, and a run that labels its own findings lets
   `/unattended-issue-loop` *(user level)* execute work it generated with nobody in between.
4. **The two outcomes that file nothing.**
   - **No maintainer present: file nothing** (INV-314). The draft stays marked **not filed —
     needs the maintainer to file it**.
   - **Declined:** recorded as declined, with the maintainer's reason if one was given. A
     declined finding is a decision, not a gap.
5. **Upstream — only under the outbound rule in [Absolute rules](#absolute-rules).** Put each
   qualifying `mcp-server` message to the maintainer out of character, after the phase or the
   walk, on its own. ⛔ **(INV-314) A yes given in character never authorizes it** — graduation
   Step 0's upstream offer included (`phase3-conversational.md`). When the server is unreachable
   and certainty cannot be re-established, nothing is sent upstream: the finding is filed as a
   GitHub issue with the upstream draft inside it. Record the outcome on the finding's ledger
   line: sent (date and category), declined, or carried in an issue.

## Reporting

Report to the maintainer with the severity ordering the findings deserve, and:

- ⛔ **(INV-317) Name the issue each finding became, or its ledger draft and the lifecycle marker it
  carries**, and say plainly which findings are fixed and which are recorded-but-open. A
  report that lists findings without naming where they live reads as though the work is
  captured when it is only described.
- **Lead with anything that breaks a documented path**, not with the longest list.
- **If phase 3 ran, say which module the analysis started at**, and that everything
  before it was walked rather than tested.
- ⛔ **(INV-369) If phase 3 ran with a simulated Bootcamper, a clean run reads "no regression detected
  (simulated Bootcamper, persona `<p>`)"**, never "phase 3 passed" or "the bootcamp works",
  and the report lists phase 3 with the maintainer as not yet done. Findings count; a clean
  simulated run is weak evidence ([`auto-test` → "What it is for, and what it cannot
  do"](../auto-test/SKILL.md#what-it-is-for-and-what-it-cannot-do)). Say where the walk
  stopped and why, from its `walk_stop` event, and if it stopped before the start module,
  name the module it reached and leave the rest untested.
- **Say what you verified as correct**, briefly. "The routing table is right, the
  opaque-state contract is handled, no `add_data_source` confabulation" is
  information, and it stops the next audit re-checking the same ground.
- ⛔ **State the coverage limits explicitly.** "No `libSz.so`, so the live server and
  every SDK-dependent path went unexercised" is the difference between a report and
  a false clean bill of health.
- **Report your own mistakes.** If a probe was wrong, or a fix was under-specified,
  or a `git restore` ate work, say so — the methodology's value depends on the
  reader trusting the parts that did work.

## Cleaning up

Remove the scratch project when the run is done (`rm -rf $HOME/senzing-bootcamp-dryrun`)
and clear `__pycache__`. Leave the repo with only intended changes: `git status`
should show the fixes, the new tests, **and the run's `specs/IMPLEMENTED.md` entry** — no
new file under `specs/`, and nothing else.

⛔ **(INV-317) The scratch project is disposable; the issues and the ledger entry are the run's actual
output.** Deleting the project is cleanup. Deleting or never writing the ledger drafts loses
the run. If a run produced no issue and no ledger entry, it produced nothing durable, however
good the conversation was. Under `--draft`, a finding's `drafts.py` record counts as recorded,
and the caller writes the ledger (INV-317's 2026-10-13 note). `git status` then shows no entry.

## Scope note

`.claude/` is **not** propagated to the public repo (`python3 -m tools.bootcamp_build promote`
publishes the built packages, each assistant's catalog, `site/` and `public/` only), so this
skill and its `scaffold_project.py` helper never ship to bootcampers.
