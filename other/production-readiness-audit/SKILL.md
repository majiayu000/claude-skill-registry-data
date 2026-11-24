---
name: production-readiness-audit
description: 'Audit the whole Senzing Bootcamp plugin for production readiness — the last static gate before dry-run. Verifies the plugin is consistent, coherent, complete and concise, and checks INVARIANTS.md against the plugin in BOTH directions: every invariant is honored, and every durable rule the plugin states is registered as an invariant. Use when the maintainer asks for a deep dive, a conformance or coherence audit, whether the plugin conforms to every invariant, whether it is consistent/coherent/complete, or whether it is ready to ship. Maintainer tool — never invoked during a bootcamp.'
argument-hint: "[area to scope the invariant sweep to] (omit to let the lead generators choose) [--draft <run-dir> | --file <run-dir>]"
---

# Production-readiness audit

This is a **maintainer** tool for developing the Senzing Bootcamp Claude Plugin
(SBCP). It is never invoked during a bootcamp.

It is the **final static gate before `dry-run`**. When it passes, the SBCP should be
consistent, coherent, complete and concise enough that a Bootcamper's experience is
excellent — and whatever is left wrong is something only running the thing can find.

This skill continues the `deep-dive-audit-*` series in `specs/IMPLEMENTED.md`, which is
where the Step 7 defect classes come from. Those entries are the **origin** of the method;
the `production-readiness-audit-*` entries that follow them are the current record. **Reading
the most recent of them is required before a run** — see Step 1. Re-deriving a finding that is
already recorded is the most common way to waste a run.

⛔ **Do not enumerate those entries here, and do not state how many there are.** An earlier
version of this paragraph named six by date and called them "the only record"; by 2026-08-21
there were **thirty-two** entries across the two series, the newest of which carried the
guardrail a run following an unattended session most needs — and the list still pointed at the
six oldest. It was also wrong when written: the `deep-dive-audit-*` series has **seven**
entries, and `deep-dive-audit-2026-07-29-minor-fixes` was never in the list. A fixed set in
prose goes stale silently, because it keeps reading authoritative.

## Why this exists

`specs/INVARIANTS.md` opens with four foundational constraints. Two of them are this
skill's entire remit:

- **INV-003** — The SBCP MUST be consistent, coherent, and complete.
- **INV-004** — The SBCP MUST be production-ready.

Every other invariant constrains a file, a script, a step or a string, so a test can
hold it. These two are properties **of the whole**, which no test can hold — a suite
asserts N things about N places and cannot notice that place N+1 disagrees with them.
So INV-003 and INV-004 are enforced by a person doing this, or not at all.

Every prior audit in the two series ran against a **fully green suite** and found real
defects anyway. Their own summaries say it plainly: *"none of the findings was
mechanically enforced"*, and — quoting the run of the day — *"none of which any of the
1059 existing tests could see."*

⛔ **Read the count and the suite size off the ledger, never from here.** This paragraph
said *"The six prior audits"* and topped out at 1059 tests until 2026-09-02, by which point
the two series held **fifty-five** entries and the suite had passed **3,900** — the same
staleness the ⛔ two paragraphs above forbids, in the section arguing the method works. The
quoted figure above is left as a **quotation**, dated to the run that wrote it; it is not a
claim about today. A sample of what a green suite shipped:

- **Every screenshot was being lost from every Bootcamper's recap PDF.** INV-161 made
  image paths document-relative; `graduation/SKILL.md` said so correctly, and the three
  other files that *produce* the path still wrote the old form. One rule, four sites,
  fixed in one.
- **A Bootcamper named 李明 got `?? (Li Ming)` at 34 pt on their certificate**, exit 0,
  no warning — the page they frame.
- **The shipped six-tab visualization app was non-conformant with a still-standing
  invariant** whose text enumerated two tabs that had been removed, because the specs
  that removed them registered no invariant.

## What this skill is not

Five neighbors overlap. Keeping them distinct keeps all five useful.

| Skill | Asks |
|---|---|
| `dry-run` | Does the plugin work when **executed** — against the live server, a real filesystem, a human? |
| `auto-test` | Has the **server** drifted under the calls the plugin already makes? |
| `delegate-to-mcp-server` | What does the plugin still **own** that the server now owns? |
| `compact-dev-environment` | What can the **development environment** stop carrying? |
| **this skill** | Does the plugin agree **with itself and with its own ruleset**, in both directions? |

`dry-run`'s own framing draws the line exactly:

> Static analysis can only confirm the plugin agrees **with itself**. It cannot see
> where the plugin disagrees with the world.

This skill is the maximal version of the first half. It is the *last* static pass, so
being thorough here is what makes `dry-run`'s time worth spending on the things only
execution can reach.

⛔ **The conversational invariants are out of scope and MUST be reported as such.**
INV-251 (one 👉 question per turn), INV-006 (asked once), INV-014 (no unrequested skips), INV-005/INV-008/INV-009 (the 👉 marker, and each question's clarity) and every gate
ordering rule govern what the model *does in a live turn*. Reading cannot establish
them, and an assistant grading its own 👉 discipline proves nothing. Say they are
untested and route them to `dry-run` phase 3. A report that lets them pass silently is
a false clean bill of health.

## The four properties

The maintainer's standing prompt asks for three; the fourth was added because a plugin
can satisfy all three and still be unusable through sheer bulk.

| Property | Holds when | A violation looks like |
|---|---|---|
| **Consistent** | no two places disagree | `module-07/SKILL.md` described the retired A/B/C track model while its own `phase1` file described the current one |
| **Coherent** | the parts compose into one thing that makes sense in order | a cross-reference citing INV-077 where INV-129 governs; a rule described in vocabulary retired two invariants ago |
| **Complete** | everything promised exists, and every surface is reachable | two of three shipped slash commands documented nowhere; install docs covering macOS and Linux while INV-001 requires Windows |
| **Concise** | not too much definition, not too little — *just right* | one rule restated in four files; a skill file so long the governing sentence sits below the fold |

**On concision — the Goldilocks Principle.** Under-definition and over-definition fail
the same way: the model does the wrong thing. Too little and it improvises; too much
and the governing sentence is buried on screen three, which is functionally the same as
absent. So the target is not "shorter" — it is **findable at the moment of use**.

⛔ **Never cut rationale to make something shorter.** Every "observed:" clause in
`INVARIANTS.md` and every "the reason is" in a skill file names a real defect, and that
narrative is what stops the rule being re-argued or re-broken. `deep-dive-audit-2026-07-28b`
records the cost of removing it: a corrected example with the reason stripped got
"helpfully" corrected *back* to the broken form. The concision win is **merging
duplicated statements and moving a rule to where it is used** — never deleting why.

⚠️ **Concision is not currently an invariant.** INV-003 says "consistent, coherent, and
complete" and `INVARIANTS.md` rule 2 forbids changing an invariant's meaning in place.
So this property is audited because the maintainer asked for it, not because a rule
binds it. If a run finds concision defects worth binding, **ask** whether to register a
new invariant — do not read one into INV-003.

## The bidirectional invariant contract

This is the part no other skill does, and the direction that has repeatedly cost weeks.

**Forward — does the plugin honor `INVARIANTS.md`?** For each invariant, find every
site it binds and check them *all*. The dominant failure is not a rule ignored; it is a
rule **applied incompletely**. INV-142 said "a bundled generator" and was implemented in
one of two. INV-146's superseded "2-3 screenshots" survived in three places. INV-153 was
implemented for match keys only. When you find one site wrong, **the finding is the
class** — sweep for the rest before reporting.

**Reverse — does `INVARIANTS.md` capture what the plugin actually guarantees?** When a
change ships a durable rule and registers no invariant, the guarantee exists in the
product and nowhere in the ruleset. Nothing binds future work to it, and nothing
notices when a later change contradicts it. Both of these are real:

- **INV-134** — "the Bootcamper's name is detected silently, never asked" shipped and
  was ledgered with no invariant. Two files then cited **INV-076** as its authority — an
  invariant about the Core-vs-Customized path choice, which says nothing about names.
- **INV-155** — two specs removed visualization tabs and registered no invariant, so the
  shipped app contradicted INV-104's still-standing enumeration.

Run the mechanical half — **every view below** — then read every hit:

```bash
python3 .claude/skills/production-readiness-audit/conformance.py rules      # section-scoped
python3 .claude/skills/production-readiness-audit/conformance.py per-rule --uncited
python3 .claude/skills/production-readiness-audit/conformance.py since --since-last-audit
python3 .claude/skills/production-readiness-audit/conformance.py reverse-check --since-last-audit
```

The first three list hard rules — the repo's own `⛔` / bolded MUST/NEVER convention — and
differ in the **unit**, which is the whole story. The fourth does not list rules; it *decides*
about the ones `since` reports. Each prints its own current counts; read them off
the run rather than from a figure written here, which is how the previous baseline went stale.

- **`rules`** asks whether the *enclosing section* cites any invariant. It prints two
  populations: **line-anchored** hits, which is what every figure in a ledger entry before
  2026-08-21 counted, and **mid-line** hits — a stop sign that is not first on its line, which
  the pattern missed entirely until then. ⛔ **Compare a past figure against the line-anchored
  number, not the total**, or a fixed detector reads as a regression.
- **`per-rule`** asks whether a reader **at that line** can name the governing rule — the
  invariants cited in the rule itself or the sentence beside it. This is what INV-183 requires,
  and it is a much larger number than `rules` reports.
- **`since --since-last-audit`** lists the hard rules added since a start resolved from the
  ledger rather than guessed: the newest audit entry whose `Commit:` names a commit in this
  repository, or, when no entry yields one, the commit on the `Fallback commit` line of
  `specs/IMPLEMENTED.md`, with a `FALLBACK` line printed (INV-432). For a run following an
  unattended implement session, this is the set that session is answerable for.
- **`reverse-check --since-last-audit`** takes that set and asks, of each line, whether an
  invariant is cited **at it** — then prints a `VERDICT`. ⛔ **(INV-308) It says `clean` only when every
  added line was both tested and cited.** Lines it cannot test are counted and named as
  `UNTESTED`, because `per-rule` reads the plugin and the Markdown under `hosts/` while `since` also reaches the
  maintainer surface: the procedure this replaced compared those two spans silently and reported
  clean over 93 lines citing nothing (#80). ⚠️ A line it reports is a candidate — the other
  legitimate state is a `DEFERRED INVARIANT` block naming the rule, which lives in the ledger
  and is not read here.

⛔ **Commit an audit record on its own, BEFORE the implementations that answer it.** The
`--since-last-audit` resolver takes the newest audit entry whose `Commit:` field names a
commit in this repository as its range start (and, only when no entry yields one, the commit
on the `Fallback commit` line of `specs/IMPLEMENTED.md`, printing a `FALLBACK` line), so a
record committed *with* the work makes the range start at the work and report
`0 hard-rule lines added` — which reads exactly like a run that added none, and is enough to
let a hard rule ship with no invariant and no deferral. Measured 2026-09-03: `ffa6a2f` carried
a record plus its two implementations, `since --since-last-audit` reported 0, and
`since --ref e5fee7c` reported 6. The resolver now detects such a ref (`⛔ SUSPECT-REF`) and
widens to its parent, so the range is recoverable — but the ordering is what makes it right in
the first place. (Source: `since-last-audit-reports-zero-when-the-audit-record-shares-the-work-commit`.)

Each hit is *either* an unregistered rule (propose an invariant) *or* a missing citation to one
that exists (fix the citation). Both are findings, they need different fixes, and deciding which
requires reading the rule and searching `INVARIANTS.md` for its subject, which no regex can do.

⛔ **`rules` is section-scoped, so its count is NOT a count of unregistered rules and MUST NOT be
reported as one.** A new rule is invisible to it whenever it lands anywhere near an unrelated
`INV-nnn` — and it gets harder to see as citations grow denser. On 2026-08-21 a run added 26
hard-rule lines (net +25) and this count did not move at all, while three of those rules were on
subjects `INVARIANTS.md` covers nowhere. Both prior findings of this class
(`seven-hard-rules-shipped-in-one-run-with-no-invariant`, 2026-08-17, and
`the-2026-08-21-run-shipped-three-unregistered-guarantees`) were found by reading, not by the
count moving — and in the first case nothing establishes that the seven found were the whole set.

⛔ **Never propose deleting or renumbering an invariant.** `INVARIANTS.md` is
append-only; a superseded invariant is *marked* superseded, and a wrong one gets a dated
correction note. An invariant encoding a false premise is worse than a missing one — but
removing it silently breaks every citation that resolved to it.

## Step 1: Establish the baseline before looking at anything

1. **Confirm the suite is green first.** `python3 -m pytest tests/ -q`. Every prior
   audit began green; a red suite means you are debugging, not auditing, and findings
   will be attributed to the wrong cause.
2. **Read the most recent audit entries in `specs/IMPLEMENTED.md`** — the newest five or so
   `## production-readiness-audit-*` / `## deep-dive-audit-*` headings, whichever they are on
   the day you run, **plus any entry the generators in step 3 point at**. Get the list from the
   file, not from here:

   ```bash
   grep -n '^## \(production-readiness-audit\|deep-dive-audit\)' specs/IMPLEMENTED.md | head -8
   ```

   ⛔ **`head`, not `tail` — `IMPLEMENTED.md` is newest-first**, as its own header says. This
   line read `tail -8` until 2026-09-02, so it returned the OLDEST eight: a run that day was
   handed `2026-08-11` plus seven July `deep-dive-audit-*` entries, and the five entries from
   the previous day never appeared. That is the failure the ⚠️ two paragraphs below describes,
   produced by the command rather than by a hardcoded list — and it is silent, because a
   plausible list of real audit entries comes back either way.

   They name what was already found, which invariants each established, and — most useful — the
   *classes* that recur. Re-finding a fixed defect wastes the run; missing that a class recurs
   wastes more.

   ⚠️ **The newest entry matters most after an unattended run**, which is the case this
   instruction exists for. On 2026-08-17 the newest entry recorded a reverse-contract defect
   produced *specifically* by an unattended implement run and added a guardrail, then in the
   since-retired `implement-spec`, that a later run is supposed to follow. A reading list fixed
   at the oldest six routed around exactly that.

   The `deep-dive-audit-*` entries stay worth reading as the **origin** of the Step 7 classes.
   Their value is historical: they describe a much smaller ruleset and no
   `production-readiness-audit-*` history. Read them for the classes, not for the state.

3. **Run every lead generator**, then read the hits. `all` runs every view that needs no
   argument — including `per-rule`; `since` needs a range and is a separate call:

   ```bash
   python3 .claude/skills/production-readiness-audit/conformance.py all
   python3 .claude/skills/production-readiness-audit/conformance.py since --since-last-audit
   python3 .claude/skills/dry-run/coverage_reports.py both          # unguarded surface
   python3 .claude/skills/compact-dev-environment/citations.py verify   # referential integrity
   ```

   `both` includes **`shipped`** — invariants that name a shipped artifact and that no file
   under `source/`, `hosts/` or `tools/bootcamp_build/` cites. Read it alongside `conformance.py rules` in Step 3: the two are the
   same contract from opposite ends, and `rules` alone cannot see a rule that is registered,
   guarded by a test, and named at no step (the INV-212 case).

   ⛔ **These are lead generators, not verdicts.** A regex cannot tell a deliberately
   restated rule from one that drifted, nor a worked illustration from a cached
   authority. A run that reports these counts as findings has run a grep, not an audit.

4. **Record what this environment cannot reach**, so the report discloses rather than
   implies: is `fpdf2` installed? `pdftoppm` (poppler)? a headless browser? `docker`?
   `libSz.so`? Missing pieces are fine; silently skipping the paths that need them is
   not (INV-111/INV-163).

## Step 2: Sweep the invariants, forward

Read `specs/INVARIANTS.md`. The per-module outcome blocks (INV-028–INV-049) are the ones most
likely to have quietly stopped being true.

⛔ **A full forward sweep of every invariant is no longer feasible in one run, and a run that
implies it did one is reporting something it did not do.** The ruleset has grown past the point
where reading each rule and checking every site it binds fits in a session — the 2026-08-17 run
recorded plainly that it *"did not sweep the invariants one by one"*, which is an honest
disclosure, not a shortfall. So **scope the sweep deliberately and say what you scoped it to**:

- the invariants the step-3 generators put hits against;
- the enumerating subset below, which rots fastest;
- everything an invariant binds that the diff since the last audit entry touched;
- the per-module outcome blocks, on a rotation, so no block goes unread for long.

With no argument, those four are the scope the run chooses. **With an argument naming an
area, sweep that first, and still run every lead generator** (Step 1, step 3): a scoped run
that skips them cannot see what it chose not to look at.

For each invariant in scope, ask two questions and prefer the second:

1. Is it honored **where I first look**?
2. **What is the full set of sites it binds, and is it honored in all of them?**

Use the enumeration scan to prioritize, because enumerations rot fastest:

```bash
python3 .claude/skills/production-readiness-audit/conformance.py enumerations
```

It reports how many invariants enumerate something — an exact count, a closed list, or a
series of three or more literals. **Read the number off the run**; it grows with the ruleset,
and the proportion has been rising. An invariant stating a *property* survives change; one
*listing members* breaks the moment a member moves, and it breaks silently because the list
still reads authoritative. Check every enumeration against what the plugin ships **today**.

## Step 3: Sweep the invariants, reverse

Work the output of all three views (`rules` and `per-rule` come from `all`; `since
--since-last-audit` is its own call). For each
hit, decide between:

- **Unregistered rule** → the plugin guarantees something the ruleset does not record.
  Draft the invariant: its wording, its enforcer and every site it ships at. The
  maintainer's sign-off on the wording and the id come later, through `/review-invariants`.
  ⛔ **(INV-365) Route it through `/review-invariants`; never edit `specs/INVARIANTS.md` here:** write a
  `DEFERRED INVARIANT` block in the run's `specs/IMPLEMENTED.md` entry, as
  [`review-invariants` → "Writing one"](../review-invariants/SKILL.md#writing-one) shows
  (INV-300), then tell the maintainer to run `/review-invariants`.
- **Missing citation** → the rule *is* registered; the text just does not say which
  invariant governs. Add the citation. This is not cosmetic: INV-183 requires a step
  that generates an artifact to name its governing rules **at that step**, and a rule
  with no ID is one a later editor cannot look up.
- **Not a durable rule** → local instruction, one-off phrasing, or pedagogy. Out of
  scope. Say so and move on.

Also sweep the other way for **wrong** citations: an `INV-NNN` in shipped text whose
subject does not match the claim it is attached to. Two are on record (INV-077 cited
where INV-129 governs; INV-076 cited for the name rule). `citations.py verify` proves
the ID *exists*; only reading proves it is the *right* one.

## Step 4: Consistency and coherence

- **Every cross-reference resolves and points at the right thing** — file paths,
  step numbers ("pre-check 1a"), sibling phase files, invariant IDs.
- **No file contradicts a sibling in the same skill.** The module-07 track-model defect
  was a `SKILL.md` disagreeing with its own `phase1` file.
- **Vocabulary is canonical.** Module names in full and exact (INV-079); no
  abbreviations; no terminology retired by a later invariant.
- **Rules described in current vocabulary.** A parenthetical explaining a rule in terms
  of an invariant that has since been clarified is a coherence defect even when nothing
  it says is false.
- **Order makes sense.** A gate cannot depend on something a later step produces.

## Step 5: Completeness

- **Every enumerated thing exists** — files in the INV-050 layout tree, deliverables a
  module promises, tabs the app claims, commands a doc lists.
- **Every shipped surface is documented.** Slash commands, hooks, scripts, generated
  artifacts. Two of three commands were once documented nowhere.
- **Every platform is covered.** INV-001 makes Linux, macOS and Windows supported;
  guidance covering two of three is a defect even when the third is untestable here —
  disclose the untested half rather than omitting it.
- **Every language is served.** INV-002 makes the SBCP language-agnostic; a rule stated
  only for the reference implementation is incomplete.
- **Every always-produced deliverable has a producing step and a verification step**
  (INV-129 — verify the artifact, not the exit code).

## Step 6: Concision

```bash
python3 .claude/skills/production-readiness-audit/conformance.py size
python3 .claude/skills/production-readiness-audit/conformance.py duplication
```

Both scans print their own current totals — the shipped file and word counts, the heaviest
files, and the repeated passages with their file pairs. **Read them off the run.** A figure
copied into this file becomes a baseline nobody re-measures: the previous one sat here for
three weeks while every number in it moved, and the sentences around it went on reasoning from
the stale proportions.

Neither number is a target. Use them to find:

- **Repetition that has drifted.** Repetition *required* at a step is INV-183, not
  redundancy — but where the same rule appears in several files, read them side by side
  and check they still say the same thing. This is the same evidence trail as the
  forward sweep's incomplete-application class, approached from the other end.
- **A governing rule buried below the fold** of a long file, where the model reaches the
  action before the constraint. Moving it up is a concision fix that removes nothing.
- **Definition too thin** — a step that assumes a judgment the guidance never states.
  Goldilocks cuts both ways, and this half is easy to forget because nothing looks wrong.

## Step 7: The defect classes worth hunting, in value order

Drawn from the audits recorded in `IMPLEMENTED.md`. The first three produced the
highest-severity findings. (⚠️ This said *"the six prior audits"* until 2026-09-02, when
there were fifty-five — the classes below are what survived, and the number was never
what made them worth hunting.)

1. **A rule applied to some of the sites it binds.** Every time. When you fix one site,
   grep for the pattern and fix the class.
2. **A string that is wrong only relative to a working directory or a runtime.** A bare
   `scripts/…` path that works in the repo and fails in the Bootcamper's project; an
   f-string interpolated at runtime so the `⛔ RESERVED` framing above the dict never
   traveled with the value. Tests that model neither cannot see these.
3. **A guard narrower than the invariant it claims to enforce.** The INV-146 guard's
   regex required "most"|"best" after "2-3" and scanned two of three call sites, so it
   passed while three violations shipped. Read what a guard *asserts*, not its name.
4. **A stale enumeration inside an invariant** (Step 2).
5. **A cross-reference to the wrong invariant** (Step 3).
6. **A comment or docstring claiming a test exists that does not.** One generator's
   comment claimed `test_brand_sync.py` asserted its palette; it did not.
7. **An inlined constant diverging from its source of truth** — a fallback palette, a
   duplicated table, a figure hardcoded where the guidance says to look it up.
8. **A claim about behavior that the code stopped doing** — "silently skips" where the
   script now names each drop on stderr.

## Step 8: What to do with a finding

Follow `dry-run`'s discipline, which exists because findings held in conversation die at
session end:

1. ⛔ **(INV-317) Record it as you find it, before fixing anything** — one record per root cause,
   using `../feedback-to-issues/issue-template.md`. Cite `file:line`.

   ⛔ **Never write a new file under `specs/`.** It holds live records only (INV-307), and the
   table in `specs/README.md` is the list of the files that belong there. The frozen archive
   of the spec files is in the repository `specs/README.md` names. Read both freely — a
   spec often records why the plugin reads as it does — but nothing new lands under
   `specs/`.

   ⚠️ **Where the record goes depends on whether anyone is watching, and the two paths are
   NOT the same.** This asymmetry is deliberate and must not be "simplified" into one branch:

   - **Attended** → file a GitHub issue in this repository:
     ```bash
     gh issue create --title "<the defect, not the symptom>" --body-file <file>
     ```
     ⛔ **(INV-314) Show the maintainer the title and body and get a yes first, or
     one yes for the whole list shown in one message (INV-314, 2026-10-13 note), under the
     conditions in `.claude/skills/feedback-to-issues/drafts.py` → "The batch yes".** Filing is
     outward-facing and immediate: the issue is visible to anyone watching the repository the
     moment it exists, and its notifications have already gone out. An issue can be edited or
     closed afterwards but never un-filed — the same gate, for the same reason,
     `/feedback-to-issues` applies.

   - **Unattended** (running under `/unattended-issue-loop` *(user level)*) → ⛔ **(INV-314) file nothing.** Write the
     finding into the dated ledger entry from step 5 and list it in the handoff marked **not
     filed — needs the maintainer to file it**. ⚠️ **`gh issue create` leaves the machine**,
     and an unattended run creates only the records listed for the issue it is working
     (`.claude/skill-overlays/unattended-issue-loop.md`); a new issue is not one of them. A
     finding recorded in the ledger is durable and costs the maintainer one read; an issue
     filed by a run nobody watched cannot be un-filed.

   ⛔ **(INV-368) With `--draft <run-dir>`, this run files nothing, fixes nothing and sends nothing, and writes
   nothing outside `<run-dir>`.** In place of both paths, each finding becomes a
   [`drafts.py`](../feedback-to-issues/drafts.py) `add` record, steps 2–6 are not run, and the run
   ends with `drafts.py list`. `--draft` is the release cycle's interface (#573), and the caller records
   unresolved drafts (INV-317). **With `--file <run-dir>`**, file what `drafts.py file-plan`
   prints, after a yes for each record or one yes for the whole list shown in one message
   (INV-314, 2026-10-13 note), under the conditions in
   `.claude/skills/feedback-to-issues/drafts.py` → "The batch yes", then report (Step 9). Both
   stages, the manifest and its statuses are stated once in `drafts.py` (INV-300).

   ⛔ **(INV-318) Never apply the `unattended-ok` label to an issue you file.** An audit that labels its
   own findings lets `/unattended-issue-loop` *(user level)* work issues **it generated itself**, with no
   maintainer between generation and execution. Selecting what runs unattended is the
   maintainer's decision alone.

   ⛔ **Carry the `owner-checked:` clause on any absence claim** (INV-213): where a finding
   rests on the MCP server *lacking* something, name the route that would carry the fact and
   what it returned. The tools you asked and found empty are evidence about those tools.
2. **Fix the class, not the instance,** where the class is cheap to remove.
3. **Write a repo-level test** (`tests/`, stdlib only, no `source/` import — INV-108).
4. ⛔ **Negative-control it.** Reintroduce the defect, confirm the test fails, revert. A
   guard whose docstring claims more than its assertion checks certifies what it never
   tested. Verify the mutation actually landed — a "target missing" line and an escaped
   mutation look identical in a loop's output.
5. **Record the outcome in `specs/IMPLEMENTED.md`** — ⚠️ still live and exempt from the
   freeze, and the audit's own record that it **ran** and what it concluded, including
   "found nothing", which is a result. Reference each filed finding by issue number; an
   unattended run writes the findings themselves here. Then either queue the invariant it
   establishes or state that it establishes none (`tests/test_spec_ledger_invariants.py`
   enforces this).
   ⛔ **(INV-365) Route it through `/review-invariants`; never edit `specs/INVARIANTS.md` here:** write a
   `DEFERRED INVARIANT` block in the run's `specs/IMPLEMENTED.md` entry, as
   [`review-invariants` → "Writing one"](../review-invariants/SKILL.md#writing-one) shows
   (INV-300), then tell the maintainer to run `/review-invariants`. An audit that changes
   shipped code and leaves no ledger entry is the failure adjacent to the one INV-182
   prevents — follow the `deep-dive-audit-*` precedent and record it as a dated
   `## production-readiness-audit-<date>` entry marked **Not a spec**.
6. **Propose a correction when the invariant is what is wrong** — a dated note saying what
   was verified and when. Never delete or renumber it.
   ⛔ **(INV-365) Route it through `/review-invariants`; never edit `specs/INVARIANTS.md` here:** write a
   `PROPOSED AMENDMENT` block in the run's `specs/IMPLEMENTED.md` entry, as
   [`review-invariants` → "Writing one"](../review-invariants/SKILL.md#writing-one) shows
   (INV-300), then tell the maintainer to run `/review-invariants`.

⛔ **Do not end a run with unrecorded findings.** Before reporting, list what you found
and confirm each is **either a filed issue or a line in the dated ledger entry**. "I
described it in the report" is not recorded; a report is a message, and messages are not
durable. Under `--draft`, a finding's `drafts.py` record counts as recorded, and the caller
writes the ledger (INV-317's 2026-10-13 note).

## Step 9: Report

- **Lead with anything that breaks a documented path**, not the longest list. Severity
  ordering, not discovery order.
- ⛔ **(INV-317) Record every finding before fixing anything, as a filed issue or in the run's
  dated `specs/IMPLEMENTED.md` entry marked not filed — never a new file under `specs/`, which
  is a read-only archive (INV-307)**, as Step 8 says, so every finding the report names is
  already written down. Under `--draft`, a finding's `drafts.py` record counts as recorded,
  and the caller writes the ledger (INV-317's 2026-10-13 note).
- **Name the issue number or ledger entry each finding was recorded in**, and say which are
  fixed and which are recorded-but-open.
- **State the verdict on each of the four properties separately.** "Consistent and
  complete; two coherence defects; concision unchanged" is information. A single
  pass/fail is not.
- **Say what you verified as correct**, briefly — it stops the next audit re-checking it.
- ⛔ **State the coverage limits explicitly**, including that the conversational
  invariants were not tested and need `dry-run` phase 3, and any path this environment
  could not exercise.
- **Report your own mistakes.** A wrong probe or an over-claimed fix, said plainly. The
  methodology's value depends on the reader trusting the parts that did work.
- **Offer `dry-run` as the next step.** This skill is the gate before it, not a
  substitute for it.

## Guardrails

- **Report before changing.** Present findings and let the maintainer choose what to fix;
  fix in place only when asked. Every prior audit worked this way.
- **Never mark a property satisfied that you did not check.** An unexamined area is a
  disclosed gap, not a pass.
- **The MCP server outranks the plugin on every Senzing fact**, and a fact is re-asked
  this session or not asserted (INV-080). Do not launder a Senzing claim out of a spec,
  the ledger, or this file. Most audit findings are internal consistency and touch no
  Senzing fact — say so explicitly rather than implying a re-check happened.
- **`INVARIANTS.md` is append-only, and only `/review-invariants` writes to it.** A new
  invariant needs the maintainer's sign-off on the wording, and so does a correction.
  ⛔ **(INV-365) Route it through `/review-invariants`; never edit `specs/INVARIANTS.md` here:** write a
  `DEFERRED INVARIANT` block for a new rule, or a `PROPOSED AMENDMENT` block for a correction,
  in the run's ledger entry, as
  [`review-invariants` → "Writing one"](../review-invariants/SKILL.md#writing-one) shows
  (INV-300), then tell the maintainer to run `/review-invariants`. An unattended run, which
  cannot get a sign-off, takes the same route.
- **`.claude/` never ships.** `python3 -m tools.bootcamp_build promote` publishes the built
  packages, each assistant's catalog, `site/` and `public/` only, so this skill and its helper
  stay maintainer-side.
- **Apply the Goldilocks Principle to this file too.** If a future run finds this skill
  has grown a section nobody reads, cutting it is in scope — provided the reason it was
  written survives somewhere.
