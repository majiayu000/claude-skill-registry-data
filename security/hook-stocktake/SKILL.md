---
name: hook-stocktake
description: "Audit the harness hooks (hooks/*.sh, scripts/hooks/*) and their settings.json wiring, and give each a verdict (hook の棚卸し)."
origin: shimo4228
user-invocable: true
disable-model-invocation: true
---

# hook-stocktake — Hook Quality Audit

Evaluate every hook of the harness and assign each a verdict: `Keep / Improve / Update / Merge /
Dissolve / Retire`. A hook's cost is unlike a skill's or a rule's: it runs unattended on every
matching event, it can block, and it reads repo-controlled data (paths, commit metadata, tool
input). So the questions are wiring, evidence that it still earns its place, test coverage, and
its share of the harness threat surface (rule `security.md`).

**Roots.** `<harness>` below is the harness this audit covers: `~/.claude` by default, or a repository's `.claude/` when skill `harness-stocktake` runs in project mode (its Roots section maps the paths, names the evidence that is `n/a` there, and says which convention checks apply). The ledger `<ledger>` belongs to that harness: `${CLAUDE_SKILL_DIR}/results.json` when this skill's directory is inside `<harness>` (the harness carries its own copy of the skill), else `<harness>/stocktake/hook-stocktake.json` (an installed plugin, or project mode). Either way it is committed with the harness's other changes on the apply branch.

The paths and conventions below are the author's harness layout. In another
setup, map each target to where that setup keeps its hooks, and record a check whose input the
setup does not have (`harness_lint.py`, `hooks/README.md`, `tests/*.bats`, the usage-logging hooks,
rule `security.md`) as `—`, not as a No.

## Phase 1 — Inventory and wiring (deterministic)

Build the inventory with throwaway `python3` / `jq` over the files, and state the counts up front:

- **Targets**: `<harness>/hooks/*.sh` and `<harness>/scripts/hooks/*.py` (in a repository, every script the settings commands call). `hooks/_*-common.sh` are shared libraries:
  list which hooks source each one (`grep -l 'source.*_<name>' hooks/*.sh`)
- **Wiring**: from `<harness>/settings.json` `hooks`, one row per (event, matcher, command).
  Mark every target no command references (orphan) and every command that carries logic beyond
  invoking a script (CLAUDE.md: hook logic lives in scripts). Commands whose script is missing
  (dangling) come from the harness's lint script when it has one
  (`<harness>/scripts/hooks/harness_lint.py`); otherwise — and in project mode, or without Bash —
  check that each called script exists with Glob.
  `scripts/hooks/*.py` are called from hooks or from other scripts; resolve their callers with grep
- **Documentation**: `hooks/README.md` — the Active Hooks tables against the wiring rows, and its
  Shared list against `hooks/_*-common.sh` (missing and phantom rows)
- **Tests**: the `tests/*.bats` files that exercise each hook (`grep -l <script name> tests/*.bats`)
- **Fire evidence**: only the logging hooks leave a count — `log-skill-usage.sh` and
  `log-agent-usage.sh` append to `<harness>/metrics/skill-usage.jsonl` / `agent-usage.jsonl`, which
  count logged skill and agent events (`log-skill-usage.sh` is wired on two events), not every run
  of a hook. Every other hook gets `—`, which is not zero. A `metrics/*.jsonl` that no hook or script
  writes any more is an integrity finding

The wiring, dangling and README checks are integrity findings that feed Phase 2 as evidence.

## Phase 2 — Evaluation (inline, holistic)

Read every hook's header and body while seeing the whole set.

**Stage 1 — binary screen (every hook).** Answer Yes/No per hook; surface only the No answers:

- [ ] Wired, or sourced by a wired hook? (Phase 1)
- [ ] Logic lives in the script, not in `settings.json`? (Phase 1)
- [ ] A test exercises it? (blocking and advisory hooks both; a hook that blocks without a test is
  an Improve candidate)
- [ ] Its own retirement condition has not fired? Some headers and README rows state one (for
  example `bandit-precommit.sh` and `ruff-format-precommit.sh` retire once every Python repo has
  its own `.claude/verify.sh`). Check the condition against the current state, unconditionally
- [ ] Not absorbed by the substrate? Can Claude Code now do this natively (permission rules,
  sandbox, a built-in hook or check)? Verify against the current Claude Code docs (agent:
  `claude-code-guide`), not memory. A Yes that cannot name the native feature is not absorption
- [ ] Repo-controlled data reaches the shell safely? (paths, branch names and commit messages
  quoted, no `eval`, the shared extraction in `_git-target-common.sh` used where it applies —
  rule `security.md`)
- [ ] Its README row matches what it does?

**Stage 2 — pressure-test (non-Keep candidates only).** Generate 1–3 hook-specific yes/no
questions that try to refute the draft verdict, each answered with one line of evidence (a file
read, a test run, a docs check). For Dissolve, the mandatory question is "Can the absorbing native
feature be named and shown in the current docs — Yes/No". Fire counts are evidence, never a
verdict: a guard that never fires may be doing its job.

| Verdict | Meaning |
|---|---|
| Keep | Wired, tested, earns its run cost, safe |
| Improve | Keep, with a named fix (add a test, move logic out of `settings.json`, tighten quoting) |
| Update | A referenced tool, flag or path changed (verified) |
| Merge into [X] | Two hooks on the same event do overlapping work; name the survivor |
| Dissolve | Claude Code does it natively now; name the feature |
| Retire | Orphaned, its retirement condition fired, or broken beyond repair |

A security No is Improve or Update at least, and its application gets a security review of the
diff from a reviewer separate from the one who applied it (the author's harness runs agent
`security-reviewer`, per skill `implementation-chain`'s Security Review row).

## Phase 3 — Summary

Render a table: `Hook | Event | Tests | 90d | Verdict | Reason`. Close with one line: hooks found,
wired, orphaned, untested.

## Phase 4 — Report and apply

Turn every verdict into items (source `hooks`) of the report contract in skill:
`harness-stocktake` and hand them to it: one report, one approval from the author, application
on a task branch, a completion report, an ff-only merge. Called alone, this skill runs that
contract's Phases 2–5 with its own items.

- **Improve / Update / Merge**: `change` = the script diff and, when wiring changes, the
  `settings.json` edit. Script edits apply with their bats test in the same commit
- **Dissolve / Retire**: `change` = removal of the script and its tests, the README row, and the
  `settings.json` entry; `impact` = other hooks sourcing it, skills or rules naming it
- **Keep**: `reason` only

Every `reason` is self-contained and cites the No answers (question + one-line evidence), as in
skill-stocktake's Reason quality section.

**Ledger** `<ledger>`, updated on the apply branch in the same commit:

```json
{
  "evaluated_at": "2026-10-31T00:00:00Z",
  "hooks": {
    "hooks/validate-bash.sh": { "verdict": "Keep", "reason": "..." }
  }
}
```

Keys are paths from the `<harness>` root (`hooks/x.sh`, `scripts/hooks/x.py`), dotfiles and
`__pycache__` excluded — the set a ledger lint (harness_lint.py `lint_stocktake_ledgers`, where present) compares against disk;
`evaluated_at` is real UTC
from `date -u +%Y-%m-%dT%H:%M:%SZ`. An item the author skipped keeps its verdict with
`"skipped": true`.

## Related

- `harness-stocktake` — runs this audit with the other stocktakes into one report
- `skill-stocktake` / `rules-stocktake` / `agent-stocktake` — the sibling audits
- `security-reviewer` — reviews a hook diff that touches the threat surface
