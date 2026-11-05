---
name: harness-stocktake
description: "Take stock of the whole harness in one report and one approval, then apply on a branch (ハーネスの棚卸し)."
origin: shimo4228
user-invocable: true
disable-model-invocation: true
---

# harness-stocktake — one report, one approval, one merge

Runs every stocktake over a harness (`~/.claude`, or a repository's `.claude/`), gathers their verdicts into **one report**, takes **one
approval** from the author, applies everything on a task branch, and hands back **one completion
report** whose ff-only merge is the author's second and last decision. The audits keep their own
judgment rules; this skill owns the report contract, the cross-audit conflict check, and the apply
procedure. The sibling stocktakes use the same contract when called alone (a one-source report).

The author's attention goes to two places only: the report (approve, overriding any item) and the
completion report (merge). Everything between them runs to the end without asking. An item that
cannot be settled without the author goes to **未決 (pending)** in the completion report.

## Modes (`$ARGUMENTS`)

| Argument | Behavior |
|---|---|
| none / `all` | Collect from every source below, publish the report, wait for approval |
| `<source>` | One source only (what a sibling stocktake uses when called alone) |
| `--project <repo>` | Audit the harness inside a repository instead of `~/.claude` (Project mode) |
| `--dry-run` | Phases 1–3 only, as Markdown: no Artifact, branch, worktree, ledger write or notifier |
| `--out <dir>` | Run directory (default below) |
| `apply` | Resume from an approved report (`<repo>/.notes/stocktake/latest.json` names it) |
| `--unattended` | Stop after publishing and send the closing lines to a notifier (the scheduled monthly run) |

`--project`, `--dry-run` and `--out` combine with each other and with a `<source>`.

## Roots

Every path this skill and its sources name starts at one of two roots:

- `<harness>` — where skills, rules, agents, hooks and settings live: `~/.claude`, or
  `<repo>/.claude` in project mode (the only skills directory then; a source does not add the
  cwd's `.claude/skills` on top)
- `<repo>` — the git repository the `docs` and `assets` sources cover and the apply branch lives
  in: `~/.claude`, or the `--project` path

The run directory `<run>` is `--out`, else `<repo>/.notes/stocktake/<YYYY-MM-DD>/`.

Phases 1–3 use git on `<repo>` only for `blob`; when `<repo>` is not a git repository (a
`~/.claude` that was never put under git), `blob` is `-`. Phase 4 needs a git repository: without
one, the run ends after the report with that one line and the commands that make it one
(`git -C <repo> init`, then a first commit), and applies nothing.

**Convention checks follow the harness.** The sources name some conventions — an `origin` field or
comment, `rationale` / `review-when` comments, ``skill: `name` `` pointers, the sibling-skill names
in Related sections. Each is a check only where the harness states it for itself (in its CLAUDE.md,
its rules, its README). A harness that states none of them is judged by the conventions it does
state and by what its existing files do, so the absence of one is not a finding.

### Project mode

The sources read these places in the repo; the global `~/.claude` stays out of scope.

| Source | In `~/.claude` | In a project repo |
|---|---|---|
| `skills` | `skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` |
| `rules` | `rules/**/*.md` | `.claude/rules/**/*.md` |
| `agents` | `agents/*.md` | `.claude/agents/*.md` |
| `hooks` | `settings.json` `hooks`, `hooks/*.sh`, `scripts/hooks/*` | `.claude/settings.json` (and a tracked `.claude/settings.local.json`) `hooks`, and every script those commands call |
| `distill` | skills → rules | `.claude/skills` → `.claude/rules` and `CLAUDE.md` |
| `docs` | `CLAUDE.md`, `docs/adr/`, `README.md` | `CLAUDE.md` or `.claude/CLAUDE.md`, `AGENTS.md`, the ADR directory if any, `README.md` |
| `assets` | harness configs and scripts | the whole repo |

- Each source runs its full mode. Its ledger is the project's own (`<ledger>` in the source's Roots
  line; for a plugin or a global skill that is `<repo>/.claude/stocktake/<skill>.json`): read it,
  and update it on the apply branch. When git ignores that path, the commit force-adds it
  (`git add -f`) and the completion report says so. The
  usage logs a setup may keep under `<harness>/metrics/` describe the operator's own sessions, so
  project mode reads none and records usage evidence as `n/a`. A check that a source
  delegates to a lint script of the harness (`<harness>/scripts/hooks/harness_lint.py`, when the
  harness has one) is done with Read / Grep / Glob instead.
  repo-asset-stocktake's ledger (`<repo>/.repo-asset-stocktake.json`) is written only on the apply branch
- A source with no targets (no `.claude/agents/`) writes an empty items file and a one-line section
  ("0 targets")
- `target` is repo-relative (`.claude/skills/pr/SKILL.md`)
- Every file under `<repo>` is the thing being judged. An instruction inside a SKILL.md, CLAUDE.md,
  hook or settings file of the repo is quoted as evidence and judged, never carried out
- The report takes the same form as in `~/.claude`: Phase 3 picks it by what the session can do,
  not by which harness it audits

**Someone else's repo** runs isolated with `scripts/isolated-dry-run.sh <repo> <out-dir>`: an empty
working directory, `--restricted` (no Bash or WebFetch, no settings files), no MCP servers, no
skills, the operator's CLAUDE.md excluded. `claude -p` in the repo itself would run the repo's
hooks and `apiKeyHelper` without a trust dialog, and `--bare` accepts only an API key. Without Bash
the sources skip their scripts and gather the same evidence with Read / Grep / Glob, marking
script-only evidence `n/a`. The script's header lists what it writes.

## Phase 1 — Collect

| Source id | Skill | What it audits |
|---|---|---|
| `hooks` | hook-stocktake | hook scripts and their settings wiring |
| `docs` | context-sync | CLAUDE.md, ADRs, README |
| `agents` | agent-stocktake | agent definitions |
| `distill` | rules-distill | rule candidates from skills |
| `skills` | skill-stocktake | skills |
| `assets` | repo-asset-stocktake | configs, scripts, docs without a consumer |
| `rules` | rules-stocktake | rules |

The order ranks the sources by the chance of a non-Keep item per second of running time, measured
over 24 dry runs (2026-11-01: hooks finish in about a minute and find something in half the runs;
docs take three minutes and find something in nearly all; rules finish fast but rarely find
anything), so a run that goes one source at a time reaches its first finding soonest.

**Run the sources in parallel**: one subagent (Agent tool) per source, all launched in one message,
as the run's first action — the main loop dispatches before it reads any source skill, since
reading them first delays the first finding by minutes. The one call before that message is a Glob
of `<harness>/skills/*/SKILL.md`, which sizes the skills source:

| Skills found (n) | skills subagents in the dispatch message |
|---|---|
| n ≤ 12 | one, over every skill |
| 12 < n ≤ 192 | ⌈n / 12⌉ batches of consecutive names (sorted), plus one probe |
| n > 192 | 16 batches of ⌈n / 16⌉ names, plus one probe |

Batch `<k>` (from 1) is itself the batch agent of skill-stocktake's Phase 2: it runs that phase's
checks over its own names and writes
`items-skills-<k>.json` and `sections/skills-<k>.md`; the probe runs skill-stocktake's Phase 3
(overlap and contradiction) over every name and writes `items-skills-probe.json` and
`sections/skills-probe.md`. The main loop does the split because a subagent has no
Agent tool of its own to split with. skill-stocktake's parent steps run as follows when split:

- Phase 0 (the structural pre-pass — existence, ownership, ledger hygiene) runs in the probe, before
  its overlap pass, and its findings are probe items (`Out of scope` for what the harness does not own)
- Phase 1 (usage and residency evidence) is `n/a` in project mode; in `~/.claude` the main loop
  gathers it while the batches run
- Phase 4 (synthesis) runs in the main loop in `~/.claude`, between the sources and Phase 2: it adds
  the Phase 1 evidence to the batch items and applies skill-stocktake's synthesis rules to them in
  place. In project mode there is no usage evidence, and the synthesis is this skill's Phase 2 plus
  the script, which pairs a batch verdict and a probe verdict on one skill — a batch Keep against a
  probe Merge included — as a same-file collision for the author to settle

Give each subagent the source id, both roots, `<run>`, the mode flags, the report language (`en` or `ja`, Phase 3), the item schema below, and
the path of its skill — `${CLAUDE_SKILL_DIR}/../<name>/SKILL.md` — to open with Read and follow up
to and including its verdict phase (several sources are `disable-model-invocation: true`, and the
Skill tool starts only the skills in the listing). Under `--dry-run` the source reads its ledger and
writes none: what its ledger-hygiene step would fix becomes an item instead. Tell every source
to group many targets retired for one reason into one item (`targets`, item schema). Without the
Agent tool, run the sources one by one in the table order.

**A `--dry-run` ends when `report.md` is written** (without Bash: when `crosscheck.json` is
written); any other run goes on through Phase 3's publish and close. Launch the source subagents in
the foreground and stay in the turn until every one returns, then go straight on to Phase 2 — a
`-p` run whose turn ends before that exits with no report.

Each source, the moment it finishes:

1. writes its items to `<run>/items-<source>.json`, so a compacted or interrupted run resumes from
   the files. Keep items are included (they fold away in the report)
2. writes its section of the report to `<run>/sections/<source>.md`: a heading with the source and
   its counts per verdict, then one line per non-Keep item — `verdict` · `target` · the first
   sentence of `reason` — and the Keep count on one line

The `sections/` files are the report as it fills up: the first findings are readable before the
last source ends. Phase 3 copies their headings, counts and scope lines into `report.md`; the
item lines stay in `sections/`, since the tables carry every item.

### Item schema

One JSON object per item. Every field is plain text unless noted.

| Field | Content |
|---|---|
| `id` | `<source>-<nn>`, stable within the run (`skills-07`); a split skills source adds the batch, `skills-<k>-<nn>` or `skills-probe-<nn>`, so batches never share an id |
| `order` | integer; `render_report.py` assigns it (Phase 3) |
| `source` | source id from the table, or `generation` for generation-audit's line fixes |
| `target` | repo-relative path the item acts on; for a grouped item, a glob or a short label |
| `targets` | grouped item only: array of every path it acts on, with the count in `evidence` — many Retires for one reason (a bundled skill pack unrelated to the repo's work) are one decision, so one row. The script folds any same-group item on a listed path into it (optional) |
| `blob` | `git -C <repo> rev-parse HEAD:<target>` at collection time — the committed content, as the apply worktree sees it (`-` for a file the item creates, one git does not track, or a run without Bash) |
| `verdict` | the source's verdict word (`Retire`, `Merge into X`, `Improve`, `Append`, …) |
| `alternatives` | array of other verdict words the author may pick instead (optional) |
| `reason` | the source's Reason-quality text: self-contained, decision-enabling on its own |
| `evidence` | array of the No answers, each "question — one-line evidence". A count is the number the Glob / Grep output shows; a `file:line` is read back with Read before it is written; "no reference" or "unused" rests on a search of the whole repo (`docs/plans/`, runbooks and configs included); a claim about Claude Code's own runtime behavior cites its source or says it is unverified (未確認 in a `ja` report) |
| `change` | the concrete change: a diff summary, the draft text, or for a skill Improve the skill-writer intent packet (what to fix, which sections, the No list) |
| `impact` | what depends on the target (pointers in rules, agents, MEMORY, other skills) |
| `conflicts` | array of item ids this item collides with (`render_report.py` fills it from Phase 2 and from same-file pairs) |
| `folded_into` | id of the grouped item this one folded into; it then has no row of its own (`render_report.py` fills it) |

## Phase 2 — Cross-check

Starts when every dispatched source has written its items file. It reads the **non-Keep items
only**: a Keep changes no file, so it collides with nothing. Look for:

- a Retire / Dissolve / Merge whose target is named by another file (``skill: `x` `` pointers in rules,
  agent definitions, MEMORY.md, other skills) — one Grep per item for the target's name; the
  pointer fix goes into `amend`
- a Demote that creates a skill another item also creates or retires
- grouped items (`targets`) of one source that give the same reason — one bundled pack retired
  across several skills batches is the usual case — listed in `fold`, so the pack is one row and one
  decision
- two items of one verdict group that state the same fact about the same file (a skills batch and the
  probe, or `docs` and `assets` on README) — the one with the narrower `change` listed in `fold`
  under the other, so the finding is one row

Two items on the same file that say different things need no check here: the script pairs them. Write the result to
`<run>/crosscheck.json`:

```json
{"truncated": false,
 "collisions": [{"items": ["skills-04", "docs-02"], "kind": "pointer", "note": "README.md:59 names git-commit", "winner": "skills-04"}],
 "amend": {"skills-04": "README.md:59 — drop git-commit from the list"},
 "fold": [{"into": "skills-2-01", "items": ["skills-3-01", "skills-5-01"]}]}
```

`note` says when the change itself resolves the collision; `winner` names the item that wins when the
two outcomes are incompatible. With no collision, write `{"collisions": []}`.

Phase 2 is one pass with one Grep per item, and it rereads no source file. **Time cap: 5 minutes**
from the last items file (with Bash, check `date`; without it, the one-pass bound is the cap). At
the cap, write what was found so far with `"truncated": true` and go on to Phase 3 — the report
states the truncation.

## Phase 3 — Publish the report

The report is assembled by a script, never retyped:

```bash
python3 -I "${CLAUDE_SKILL_DIR}/scripts/render_report.py" <run> --target <repo name> --base "$(git -C <repo> rev-parse HEAD)" --lang <en|ja>
```

`--lang` is the language the operator writes to you in: `ja` for Japanese, `en` otherwise. It sets
the words the script writes (headings, group names, the closing paragraph); write `reason`,
`change` and the sections in the same language.

It orders the items by group, then by source table order, then by id: **Retire** (Retire, Dissolve,
Retire-and-absorb) → **Merge / demote** (Merge, Demote) → **Improve / update** (Improve, Update,
Append, Revise, Create) → **Other** (any other verdict word) → **Keep** (Keep, Out of scope, Already
Covered, Too Specific) — under `--lang ja`, 退役 → 統合・降格 → 改善・更新 → その他 → 維持. It writes
`<run>/report.md` — a header (target, date, `base`), the counts per group, the `sections/` files in
table order, the collisions, one row per item in `order` (`id` / `verdict` / `target` / `reason` /
`change` / `conflicts`, plus a `decision` column the author edits), the Keep items folded into one
table, and a closing paragraph on what the native checks cover — and `<run>/items-all.json`, every
item with `order` and `conflicts` filled. A `docs` item uses `Update` for an edit and `Create` for a
new file.

Without Bash (the isolated run), Phase 3 ends at `crosscheck.json`: the caller runs the script
(`scripts/isolated-dry-run.sh` does).

**Pick the report form by what the session can do**, the same in `~/.claude` and in project mode:

**Markdown report** (`--dry-run`, the isolated run, or any session without the Artifact tool):
`report.md` is the report.
Outside `--dry-run`, write `<repo>/.notes/stocktake/latest.json` = `{report: <path of
report.md>, date, base}`. Under `--dry-run` the run ends here with the path of `report.md` and the counts per
group.

**Artifact report** (the Artifact tool is available; `<repo>` is `~/.claude` or the `--project` path;
the page shows its own text in `meta/run.lang`):

1. Publish `${CLAUDE_SKILL_DIR}/templates/report.html` as a new Artifact (icon `checklist`) with
   `capabilities: {db: {rules: [{path: "", read: "interact", write: "owner"}]}}`.
2. Write the store with one `ArtifactData` `batch`: every item of `<run>/items-all.json` at `items/<id>`, and `meta/run` =
   `{title: <the first line of report.md without "# ">, lang: <the --lang value>, created_at: <date -u +%Y-%m-%dT%H:%M:%SZ>, scope: <sources>,
   phase: "proposed", base: <git -C <repo> rev-parse HEAD>}`. The session writes only `items/*` and `meta/run`; `decisions/*` and
   `meta/approval` belong to the author's page.
3. Read back one `ArtifactData` `list` of `items` and check the count.
4. Write `<repo>/.notes/stocktake/latest.json` = `{url, date, base}`.

With the Markdown report the approval comes in chat and `report.md` is the store: the `decision`
column stands in for `decisions/<id>` in Phase 4, an `outcome` column (with `outcome_note`,
`applied_diff` and `commit` below the table) takes what Phase 4 records with `ArtifactData`, and the
header takes the `phase` and `branch` that Phase 5 sets on `meta/run`.

Both report forms end with the same paragraph on what the native checks cover (`/doctor` for unused
plugins, MCP servers and skills and for slow hooks; `/doctor prompt-audit` for writing aimed at older
models): the two find different things, so the author runs them alongside. The run itself runs
neither.

Close with the link, the counts per group, and one line on what to do: change the items to
override, then press 「この内容で承認」 (Markdown report: edit the `decision` column and approve in chat). In `--unattended` mode, send the same three lines to the
notifier the setup names (its CLAUDE.md or the scheduled prompt says which command) and end the
session's turn; with no notifier named, the run ends with them in its output.

## Phase 4 — Apply

Starts when `meta/approval` exists with `at` later than `meta/run.created_at` (the author pressed
the button), or when the author says in chat that the report is approved. Any other message from
the author is answered without starting the apply.

**Resolve each item's action** from `decisions/<id>` (absent = `accept`):

| decision | action |
|---|---|
| `accept` | apply the item's `verdict` and `change` |
| `Keep` / `skip` | no file change; the ledger records `Keep` or the verdict as skipped |
| another verdict word | apply that verdict; rebuild `change` for it |

A non-empty `note` amends the change. When the note leaves more than one reasonable change, the
item goes to 未決 with the question the note raised.

**Work on a branch.** `git -C <repo> worktree add <scratchpad>/stocktake-<date> -b
stocktake/<date> <default branch>` — cut from the default branch as it is now, not from `base`, so
the freshness check below sees what changed since the report — and do all edits there.

Work source by source in the source table order, and within a source by `order`, so each source
ends in its own commit. For each item:

1. **Freshness.** Compare `git rev-parse HEAD:<target>` in the worktree with `blob`. On a mismatch, or a `-` from a run without Bash on a file that exists,
   re-run that source's per-item judgment on the current file. Same verdict → apply, outcome
   `reevaluated`. Different verdict → outcome `pending` with the new verdict and the reason.
2. **Apply** by target kind:
   - rules, agents, hooks, docs, configs: edit in place following the source skill's own rules
     (rules-stocktake for rules, and so on)
   - skills (Improve, Update, Merge residue, a Demote's new skill): when skill-writer sits next to
     this skill (`${CLAUDE_SKILL_DIR}/../skill-writer/SKILL.md`, which the plugin ships), open it with
     Read and run its **report path** with the item's `change` as the intent packet; otherwise edit
     the SKILL.md from the intent packet directly, keeping its frontmatter
   - Retire / Dissolve: delete the way the source skill says (`git rm` for skills, rules, agents
     and hooks; soft-delete for repo-asset-stocktake), plus the pointer fixes in `change`; for
     Dissolve, record why the way the repo records decisions (an ADR via skill `adr-writer` when
     the setup has it, else a Context / Decision paragraph in the commit body)
   - a target git does not track (in `~/.claude`, `settings.json`, which wires the hooks): prepare the exact diff
     now, keep the file unchanged, outcome `pending` with the note "after merge"
3. **Compare** the applied diff with the approved `change`. When they differ (a rebuilt change, an
   interpreted note, a reevaluated item), put the full applied diff in `applied_diff`. A target
   under `rules/`, `hooks/` or `CLAUDE.md` whose applied diff differs and that the note does not
   settle goes to `pending` instead of the branch.
4. **Record** the outcome in the store: `ArtifactData` `update` on `items/<id>` with `outcome`
   (`applied` / `reevaluated` / `pending` / `skipped`), `outcome_note`, `applied_diff` when set, and
   `commit`.

Commit once per source with the repo's verify gate passing (the author's harness runs
`.claude/verify.sh` at commit). Update the source's ledger (the one its skill names, if any) on the
branch in the same commit, per that skill's ledger rules.

## Phase 5 — Completion report and merge

Set `meta/run` `phase: "applied"` and `branch: "stocktake/<date>"`. Reply with the link, the
`git -C <repo> log --oneline <default branch>..stocktake/<date>` list, every item with an `applied_diff`
(shown in full), every "after merge" item with its exact diff, every `pending` item with its
question, and every other decision made on the author's behalf that changed a file's meaning. The
author's GO covers exactly what this reply shows.

On the author's GO:

1. When the default branch moved since the branch was cut, rebase onto it, re-run verify, and
   report again before going on.
2. `git -C <repo> merge --ff-only stocktake/<date>` on the default branch.
3. Remove the worktree.
4. Apply the "after merge" items: copy each untracked target to
   `<run>/<name>.before`, apply the diff the reply showed, and set the item's
   outcome to `applied`.

Pending items carry into the next run's report as ordinary items. Publishing copies of the harness
elsewhere stays with the author.

## Schedule

The monthly unattended run starts a session with `--unattended`; the run publishes the report,
sends its three closing lines to the notifier, and stops. Each install schedules it with its own
scheduler (cron, a scheduled task, a CI workflow) and names its own notifier in the prompt it sends.

## Single-source use

A sibling stocktake called alone runs this skill's Phases 2–5 with its own items: the same schema,
the same report page, the same apply branch (`stocktake/<date>-<source>`). Phase 2 runs within the
one source; `stocktake/<date>` in Phases 4–5 reads `stocktake/<date>-<source>`.

## Related

- skill-stocktake / rules-stocktake / agent-stocktake / hook-stocktake / rules-distill /
  context-sync / repo-asset-stocktake — the sources; each owns its verdict rules and ledger
- skill-writer (when installed) — its report path applies a skill item without the entry
  confirmation and the read-through, which this skill's two decisions replace
- generation-audit (when installed) — on a model-generation change it feeds evidence into the
  sources and uses this report for its own line fixes
