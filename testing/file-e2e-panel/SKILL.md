---
name: file-e2e-panel
description: Use when the lead wants a fresh batch of e2e panel runs filed — "file the e2e panel", "file the e2e runs", "I need more genealogist tasks", "who needs to run an e2e test", or a bare "/file-e2e-panel", any time, as often as wanted. Files one issue per panel fixture — four more on every run, unconditionally — each an unassigned half-day task a genealogist can take, so the e2e corpus gets runs from more than one operator. Also reports each fixture's last run and proposes closing panel issues nobody has taken in two weeks. Proposes first and applies only what the lead approves; never runs an e2e test itself, never writes the project board.
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# File a batch of e2e panel runs

The e2e tier is the only measurement of the whole research loop, and it had one
operator: runs per ISO week fell 43 → 37 → 12 → 4 → 4 → 1 → 1 over the seven weeks
to 2026-09-07, so every corpus report opens on a two-run window and nothing can be
compared month over month. Four issues per batch, filed separately, is how the work
reaches four people instead of one.

**Run this whenever more panel work is wanted — twice in a week, or not at all for
three.** Every run files four more. Nothing here is anchored to a calendar week, and
there is no cadence to keep to.

**You propose, then apply what is approved.** No branches, no PRs, no code edits,
and you never run an e2e test yourself — each issue is someone else's half-day.
You have no `Edit` or `Write` tool on purpose.

**Never write the project board.** `add-to-project.yml` cards each new issue into
Backlog on its own. A `gh` token without the `project` scope fails a board write
*while appearing to succeed*, so do not run `gh project` commands.

## 0. Pool facts

Repo `PioneerAIAcademy/cowork-genealogy`, project **1**. The panel is fixed:

| Fixture | Why it is on the panel |
|---|---|
| `eval/tests/e2e/spriggs-parents-1898/` | deepest run history |
| `eval/tests/e2e/hannah-earnest-children/` | deepest run history |
| `eval/tests/e2e/anders-monsen-ancestry/` | deep history, non-US locality |
| `eval/tests/e2e/cruz-corona-ancestry/` | deep history, Spanish-language records |

**Fixed on purpose.** Fixture difficulty varies enormously, so a month's aggregate
is comparable to the next month's only if the mix is constant. Do not swap a
fixture in because it looks more interesting today — that silently ends the
comparison the panel exists for. The panel is defined once, in `PANEL` in
`eval/harness/e2e/panel_report.py`, and `eval/harness/tests/unit/test_e2e_panel_report.py`
fails if this table and that constant disagree.

## 1. Check the label exists, before anything else

```sh
gh api repos/PioneerAIAcademy/cowork-genealogy/labels/e2e-panel
```

**Non-zero exit: stop and tell the lead.** Everything below depends on this label,
and its absence is invisible in the obvious places — `gh issue list --label
e2e-panel` on a missing label exits **0 with empty output**, which reads exactly
like a clean board, and `gh issue create --label e2e-panel` fails *without filing
the issue*. Skip this check and you report "nothing stale, four filed" on a run
where nothing happened. One-time fix:

```sh
gh label create e2e-panel --repo PioneerAIAcademy/cowork-genealogy \
  --description "One e2e panel run; filed by /file-e2e-panel" --color 1D76DB
```

## 2. Read where the panel stands

```sh
make e2e-panel
```

Per fixture: its last run and how many days ago, plus its run count over the last 28
days. `SINCE=all` for the whole history — the all-time counts are a different number
from the trailing-month ones, and it is the trailing month that says whether the
panel is working. A batch is one run per fixture, so filing about weekly reads as
roughly four per fixture in that window; that is the number a working panel shows.

**This gates nothing.** You file four either way. The number is what you report to
the lead, and the thing to say out loud when it stays at zero: issues are being filed
and not run, which is a staffing problem, not a filing problem.

## 3. File four issues

One per fixture, every run, unassigned. No conditions — not "the ones that have no
run yet", not "the ones whose last issue closed", and not "only if the last batch is
gone". Four more, every time.

```sh
gh issue create --repo PioneerAIAcademy/cowork-genealogy \
  --label genealogist --label e2e-panel \
  --title "e2e panel run <YYYY-MM-DD>: <slug>" \
  --body-file - <<'EOF'
...
EOF
```

The body goes in on stdin from a quoted heredoc, so the dollar amounts and
backticks in it arrive as written. Inside `--body "..."` bash would expand
`$2.50` to `.50` and run every backticked span.

The date is **today**, the same for all four in the batch, so batches are
distinguishable in a list and the label query stays exact. Two batches on one day is
fine — the issue numbers differ, and that is a deliberate ask for eight, not a
mistake to guard against.

Each body carries its own fixture's time and cost, measured when you file. Read them
from a checkout whose `main` is current. Do not `git pull` into a working branch, and
note that a plain `git pull` reads `origin`, which can be a fork. The command reads the
run logs in the checkout, so the body gives the checkout's short sha
(`git rev-parse --short HEAD`).

It runs in the harness venv. The fixture's real wall-clock cap comes from `load_fixture`
in `eval/harness/e2e/orchestrator.py`, the one place a fixture's `caps` override is
merged over the default. `result_jsons_for` in `eval/harness/e2e/runlog_selection.py`
already skips `.ann.json` and `.final-*` files:

```sh
cd eval/harness && uv run python - <slug> <<'PY'
import json, sys
from pathlib import Path
from e2e.orchestrator import load_fixture
from e2e.runlog_selection import result_jsons_for
slug = sys.argv[1]
cap = load_fixture(Path("../tests/e2e") / slug).caps.wall_clock_seconds
print(f"wall-clock cap: {cap / 60:.0f} min")
for p in result_jsons_for(slug)[-5:]:
    d = json.loads(p.read_text(encoding="utf-8"))
    u = d.get("usage") or {}
    secs, cost = u.get("wall_clock_seconds"), u.get("total_cost_usd")
    print(p.stem, "no time" if secs is None else f"{secs / 60:.0f} min",
          "no cost" if cost is None else f"${cost:.2f}", d.get("stop_reason"))
PY
```

Fill the template's placeholders from its output:

- `<per-run minutes>` is the five times, oldest first. `<time range>` is their lowest
  to highest, rounded outward to 5 min. If any of the five has a `stop_reason` other
  than `completed` or `natural_end`, add one sentence after the list saying which,
  and when.
- `<cap>` is the printed wall-clock cap.
- `<recorded costs>` are the costs that exist. `<k>` is how many of the five recorded
  none. A run that ends before the SDK's final message (a `timeout` or an `inactivity`
  stop) records no cost, so the figure is a floor. When `<k>` is 0, drop the sentence
  that carries it. `<budget>` is the highest recorded cost, rounded up to the next
  dollar.
- `<date>` is today. `<sha>` is the checkout's short HEAD.

Leave `<ts>`, `<run date>` and `#N` as written. The runner fills them in. The issue
number is not known until `gh issue create` has run, and a create-then-edit would be a
second write on every issue.

Body, short — the guide holds the detail:

```
**Touches:** eval/runlogs/e2e/<slug>/

Run the `<slug>` e2e fixture, grade it, and land the run log. Half a day, most of
it waiting. Assign yourself when you start.

The fixture is already authored, so this is the short route through
`docs/e2e-testing-guide.md`: steps **0, 5–9**. Skip 1a/1b/2/3 (authoring) and 4
(live debugging); a debug pass only delays the measurement. Run from a freshly
pulled `main` (step 0). The run log records its own `git_sha`.

    make e2e-preflight            # Windows: eval\CheckSetup.bat
    make e2e-login                # Windows: eval\Login.bat   (~24h token)
    make e2e-run TEST=<slug>      # Windows: eval\RunE2E.bat

**Expect <time range> minutes, and do not kill it.** The last five runs of this
fixture took <per-run minutes> min, oldest first. Measured <date> at <sha> from
`usage.wall_clock_seconds` in `eval/runlogs/e2e/<slug>/run-*.json`, read with
`result_jsons_for` (`eval/harness/e2e/runlog_selection.py`). The harness stops a
run at its wall-clock cap, <cap> min for this fixture (`caps` in its
`fixture.json`, default in `FixtureCaps`, `eval/harness/e2e/orchestrator.py`), and
can run a few minutes past it. It still writes the run log. Cost has no stop:
`max_cost_usd` only labels a finished run `cost_cap`, and runs have cost well past
it. A run you abort writes nothing.

Then, in Claude Code in this checkout, **grade first, then interpret** (guide
step 6). Skip both for a run that stopped on `host_slept` (the landing rule
below). The interpreter reports which expected findings were recovered, so
reading it first anchors your grade. CI checks only that the `.ann.json`
exists, not how it was made, so nothing will catch the wrong order.

    /grade-e2e-run                # FIRST, blind -> run-<ts>.ann.json
    /interpret-e2e-result         # only after the .ann.json is written

The labels in the `.ann.json` are your judgment as a genealogist. Do not let
Claude Code propose them or fill them in.

**Land the run at whatever verdict it earned: pass, partial, fail, or a cap or
timeout stop.** A failed panel run is the data point (guide, "The standing
panel"). This overrides guide step 8's "fix it in Step 4 and re-run" and step 9's
"commit a passing run", which are for authoring a fixture. Re-run only after an
environment failure: no `run-<ts>.json` written at all (`mcp_unavailable`, or an
abort before any file), or a run that stopped on `host_slept` because the
machine slept. Commit a slept run's three files without grading it, as the
harness prints, keep the machine awake for the re-run (`eval/README.md`, "Keep
the machine awake during a run"), and land both runs in one PR, titled for the
graded one, with a line in its body naming the run that slept. In this PR:
- No SKILL.md, agent, harness or fixture edits. `fixture.json` and
  `expected-findings.json` are inside the blind-grading bundle
  (`eval/harness/e2e/blind_bundle.py`, `bundle_paths`), so editing either one
  breaks the digest of every earlier `.ann.json` for this fixture.
- No `/mine-unit-test`. A new unit test makes that skill's run log inactive, and
  `check_runlogs.py` then blocks the PR until a paid `make eval-skill` run lands.
  If a failure looks worth mining, say so in a comment on this issue.

If it fails, read `narration[]` alongside `tool_calls[]` before blaming a skill
(guide step 8). Put what you find in the PR body.

Then open one PR carrying `run-<ts>.json`, `run-<ts>.ann.json` and both `.final-*`
siblings, titled "<slug>: e2e panel run <run date>, graded (#N)", with
`Closes #N` in its body, where N is this issue's number. If this issue is still
open after the PR merges, close it with a link to the PR. After you commit and
before you push, run the gate the way CI does. With no SHAs set it prints
`skipped`, which is not a pass. Run before the commit, it checks 0 run logs,
which is not a pass either. Expect `1 added-or-renamed run log(s) checked`
(2 with a slept run):

    BASE_SHA="$(git merge-base origin/main HEAD)" HEAD_SHA="$(git rev-parse HEAD)" \
      python3 eval/harness/scripts/check_e2e_fixtures.py

Run it in Git Bash or WSL on Windows. `origin/main` must be the `main` you
branched from: if `origin` is your fork, use `upstream/main`.

That gate blocks a run log shipped without its annotation, one made with the 1M
context window (`usage.betas` non-empty), one made with tool search off
(`usage.tool_search` or `usage.tool_search_offered` false), and one containing a
FamilySearch or OpenRouter credential.

**Cost:** budget about $<budget> of API spend: the highest cost recorded in this
fixture's last five runs, rounded up (<recorded costs>). <k> of the five recorded
no cost, so this is a floor. Measured <date> at <sha> from `usage.total_cost_usd`
in the same run logs; every new run moves these figures. After you have graded,
`make e2e-latency TEST=<slug>` shows the latest run, verdict included (Git Bash or
WSL on Windows; it prints `cost: $None` when none was recorded).
```

**Do not paste a run's expected findings into the body.** The grading pass in step
6 is blind by design, and a body that names the answer corrupts the calibration
number this whole tier rests on.

## 4. Sweep the panel issues nobody took

Unconditional filing accumulates: a batch nobody picks up is still there when the
next one lands, and a genealogist facing sixteen near-identical issues cannot tell
which is live.

```sh
gh issue list --repo PioneerAIAcademy/cowork-genealogy --state open --limit 300 \
  --label e2e-panel --json number,title,assignees,createdAt
```

**`--limit` defaults to 30 and truncates silently**, newest first — so the default
hides exactly the old issues this step exists to close, and the pool it hides can
then only grow. Confirm the returned count is below the limit you asked for before
trusting it.

Propose closing each one that is **older than 14 days**, **unassigned**, and has
**no linked PR**.

**Age, not "the previous batch."** Filing twice in one week is a supported thing to
do, and a sweep that closed whatever predates today's batch would delete the first
half of a deliberate double-fill. Fourteen days is the line: past it, nobody was
going to take it.

Check the no-PR half two ways and treat a hit from either as linked:

```sh
gh pr list --repo PioneerAIAcademy/cowork-genealogy --state open --search "<N> in:title,body"
gh issue view <N> --repo PioneerAIAcademy/cowork-genealogy --json closedByPullRequestsReferences
```

Neither alone is enough, and both failure modes propose closing work that is in
flight. `closedByPullRequestsReferences` sees only PRs carrying a **closing
keyword**. The template asks for one, but an operator can still leave it out. And
`in:body` alone misses this repo's own convention of naming the issue in the
**PR title** — measured:
PR #2151 is titled "person-evidence becomes a skill-agent pair (#1853)" and
`--search "1853 in:body"` returns nothing for it, while `in:title,body` finds it.

```sh
gh issue close <N> --repo PioneerAIAcademy/cowork-genealogy --reason "not planned" \
  --comment "Unclaimed for over two weeks; the <today> batch supersedes it."
```

**One at a time, and only what the lead approves.** Never batch this, and never
close an assigned issue — an assignee who has not finished is a conversation, not
a sweep.

## 5. Verify before you repeat anything

Every number you report comes from a command you ran this session — the coverage
from `make e2e-panel`, the open issues from `gh`, each fixture's time and cost from
its own run logs (§3). Do not carry a figure over from last week's report, and do
not quote a corpus-wide or per-run cost median: nothing in this repo computes one,
so a dollar figure in prose is a hand-maintained copy that rots. The exception is a
per-fixture range read from that fixture's own run logs when you file, with the date,
the checkout's sha and the command in the issue body.

## Output shape

1. **Filed** — the four issues, one line each: fixture, title, and the fact that
   motivates it ("no run since 2026-07-13, 56d").
2. **Where the panel stands** — the `make e2e-panel` table, and one sentence on the
   trend. Say it plainly when the answer is that nobody has run it.
3. **Sweep** — panel issues proposed for closing, one line of reasoning each; and
   separately, the ones you are leaving because they are assigned or have a PR.
4. **Panel health** — how many open panel issues there are now, and whether the same
   fixture keeps going unrun. A pile of open panel issues means the panel is being
   filed and not staffed, which is the lead's to act on, not a reason to file fewer.

Then stop and wait for approval. File and close only what he approves. Do not
begin any of the runs yourself.
