---
name: agnos-meta-demo
description: "AGNOS maintainer skill. Builds, rebuilds and verifies agnos-lightweight-process.demo, the simulated two-month demonstration project that shows the AGNOS process applied by a team and serves as the reference to demonstrate and test AGNOS. USE FOR: refreshing the demo after AGNOS evolves, checking it against its requirements, extending its scenario."
argument-hint: "build [--verify] | verify"
---

<!-- RQ-DMO-020, RQ-DMO-021 / ADR-DMO-001 (DEC-DMO-006) -->
# AGNOS Demo

Canonical procedure, shared by GitHub Copilot (`.github/skills/agnos-meta-demo/`) and Claude Code
(`.claude/skills/agnos-meta-demo/`, which points here). It is a **maintainer tool**: the demo holds no AGNOS
file but the `CLAUDE.md` and `AGENTS.md` written by `agnos-init` <!-- RQ-MTA-005, RQ-INI-008 -->, and this repository's CLAUDE.md and AGENTS.md do not list it.

The demo repository is created next to this one as `agnos-lightweight-process.demo`. Its history is
simulated: four fictitious people of the company Acme (`linda-pm`, product manager; `john-ux`, UX designer;
`andy-tech` and `sachin-tech`, architecture, development and tests; e-mails `@acme.example`), each working mostly with
an agent <!-- RQ-DMO-011, RQ-DMO-023 / DEC-DMO-003, DEC-DMO-009 -->, five sessions on `feature/<TRI>` branches (BKG, NTF, CLI, then DSN, a design system made with
`agnos-design-system`, and WEB, the booking interface built on its tokens <!-- DEC-DMO-007 -->), 2026-08-24 to 2026-10-23,
working days and hours only.
<!-- Requirements: FTR-DMO-001 and FTR-DMO-002; decisions: ADR-DMO-001. -->

## Layout

| Path | Role |
|---|---|
| `scripts/replay.ps1` | The engine: replays a scenario into a new git repository |
| `scripts/build.ps1` | Runs the engine on this skill's scenario and content, records the build |
| `scripts/verify.ps1` | One PASS/FAIL line per requirement, including a run of the product as the README says <!-- RQ-DMO-001 to RQ-DMO-027 --> |
| `assets/scenario.json` | Cast (humans and agents), calendar, and the ordered commits (date, time, identity, co-author, files) |
| `assets/content/` | The demo's files: process documents, Python and TypeScript code, README, calendar, and `project/` for its git files, named so they do not apply here |
| `tests/test_meta_prefix.py` | The tests of the names and of the prefix as the only criterion <!-- RQ-MTA-001, RQ-MTA-002 --> |
| `tests/test_replay_agents.py` | The tests of the agent identities and co-authors of the engine <!-- RQ-DMO-023 to RQ-DMO-025 --> |
| `references/code-contract.md` | The contract given to the sub-agents that generate the code |

## Sub-commands

Run from the repository root with `session.platform = windows` (PowerShell 5.1; there is no bash version).

### `build [--verify]`

```
powershell -NoProfile -File .github/skills/agnos-meta-demo/scripts/build.ps1 [-Verify]
```

1. Creates the repository, which holds the project and the block of `agnos-init` <!-- RQ-MTA-005, RQ-INI-008 -->; a session in it needs the AGNOS plugin installed.
2. Replays `assets/scenario.json` with `assets/content/`, committing with the identity and dates of each
   step through environment variables only: no git configuration is changed, no remote is added, nothing
   is pushed. The index of each step comes from this working tree's `agnos-index`.
3. Rebuilds an existing demo only if the engine created it (marker `.git/agnos-demo-generated`); any other
   folder is refused.
4. With `-Verify`, runs `verify` and returns its exit code.

A build on an unchanged working tree always ends on the same HEAD commit ID.

### `verify`

```
powershell -NoProfile -File .github/skills/agnos-meta-demo/scripts/verify.ps1 [-BaseRef <ref>] [-SkipRebuild]
```

Checks the demo against its requirements and prints `PASS` or `FAIL` for each (exit 1 if any fails).
It runs this repository's `agnos-index` and `agnos-perf-center` against the demo, so it doubles as a regression
test of AGNOS. `-BaseRef` also checks that this repository changed only under `agnos-process/` and the skill
folders since that ref. A failure is fixed in the scenario or the content, then the demo is rebuilt; the
demo's history is never edited by hand.

## When AGNOS evolves

1. Make and commit the AGNOS change.
2. Run `build -Verify`. The scenario is replayed with this working tree's `agnos-index`, and `verify` runs its `agnos-perf-center` on the demo.
3. If a check fails because a rule changed (a new template field, a new commit format), update
   `assets/content/` or `assets/scenario.json`, rebuild and verify again.
4. To show a new capability, extend the scenario with new steps inside the two-month period and add the
   content they commit. Keep identities, working days, hours and the order definitions-before-citations.

## Extending the content

- Process documents are stored in their final form. A plan is committed with every task `Not Started`
  and the `closeTasks` of a step puts back that task's final status and Verification. Use a step's `edits`
  (find and replace, strict) to commit an earlier draft and a later change of the same text.
- Code is generated by sub-agents from `references/code-contract.md`, then reviewed: IDs cited exist,
  exact marked lines present, tests pass (`python -m unittest discover -s tests -t .` in `service/`,
  `node --test "tests/*.test.ts"` in `client/`).
- Verification outputs written in the plans are illustrative; the README says so.
- Agents <!-- RQ-DMO-023 to RQ-DMO-025 / DEC-DMO-008 -->: an identity of `"kind": "agent"` is named `<Harness>/<Model>`
  as `commit-task` names it, with its tool's e-mail. A step's `"with": "<agent>"` ends its message with that agent's
  `Co-Authored-By` trailer; a step `by` an agent is a commit by the agent alone. The engine refuses `with` on a merge,
  `with` naming a human, and an agent alone that merges, has a co-author, adds a file or runs `init`.
