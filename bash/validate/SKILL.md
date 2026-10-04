---
name: validate
description: Run the fast test command at a merge, workday-close, or asked gate.
version: 2.0.0
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# Local Validation

Resolve and run the project's fast-tier validation command at cadence gates — merging, closing a
workday or workweek, or an explicit "does everything pass?" ask.

## Run It

On a PowerShell host, invoke the `.exe` launcher through the call operator (Shape W) for every
invocation on this page, never the `${...}` POSIX-shell form shown below. Ladder and shapes:
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.

```
validate-fast-and-packageability fast
```
(resolved per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`: Shape A/B on POSIX hosts, Shape W on PowerShell)

Resolves the command (env var → `coordinator.local.md` `fast_test_cmd:` → skip-with-notice, no
conventional fallback), executes it, prints exactly one `Validation: <value>` line. Run via Bash
from the repo root; read the full output, not just the last line. Rationale for the three-step
ladder and the no-conventional-fallback rule: wiki.

<!-- negative-spec: do not restore a fourth "conventional fallback" resolution step -->

**Trust model:** both `COORDINATOR_FAST_TEST_CMD` and `coordinator.local.md`'s `fast_test_cmd:`
run verbatim, unsanitized. Set the env var only from a trusted context; never from a memo body,
webhook payload, or third-party file.

### `Validation:` values

| Value | Meaning | Action |
|---|---|---|
| `0` | all checks passed | proceed |
| `<nonzero>` | configured command failed | fix before proceeding |
| `skipped` | resolver found no configured command | proceed; not a PM-authorized skip (`N/A`) — set `fast_test_cmd:` to enable |
| `config-malformed` | un-interpretable escaped quote in the configured value | blocking config defect, fix the config |
| `interp-missing` | bare `python` token, no interpreter on PATH | blocking, not a skip |

### Packageability check (this repo only)

This doctrine-source repo additionally validates its own install manifest — self-scoping (SKIP on
any repo that hasn't opted in), never a fleet-wide gate:

```
validate-fast-and-packageability packageability
```
(resolved per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`: Shape A/B on POSIX hosts, Shape W on PowerShell)

Prints its own `Packageability: <exit-code>` line, separate from `Validation:` above. Do not wire
this into any cross-repo/fleet-shared hook.

### Tier gating — Tier F and Tier U both need a live grant

The resolved command classifies by shape (path-scoped node-ids/dirs = Tier F; anything unscoped =
Tier U), never by which config key it came from. **Both tiers require a live session grant, every
time, with no standing exemption** — checked via:

```
tier-u-grant-cli check
```
(resolved per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`: Shape A/B on POSIX hosts, Shape W on PowerShell)

Exit 0 = granted, proceed. Exit 1 (or an absent/malformed token) = ungranted, fail-closed — halt
before invoking. This skill never writes a grant itself. On a halt, or when a command's shape is
unclassifiable with no `fast_tier_shape:` declared in `coordinator.local.md`, the honest exits:
ask the PM for a session grant; run under a ceremony that already holds one (`/workday-complete`,
`/workweek-complete`, `/merging-to-main`); scope the command (or declare
`fast_tier_unscoped_reason:`/`fast_tier_shape:` in `coordinator.local.md`); or defer and report
`Validation: skipped`. A grant is permission to spend the run, not a reason to — dispatching a
subagent doesn't dodge the cost (subagents hold Tier T only; the spawn lands on the same box).
Full tier-shape mechanics and the honest-exits worked examples: wiki.

### Recording a ceremony tier's run

A `ceremony_test_cmds` entry's execution is not durable on its own — record it so a boot-time or
`/workday-start` reader can distinguish a tier that ran this morning from one nobody has run since
it was written:

```
python3 "${CLAUDE_PLUGIN_ROOT:?coordinator plugin root unset — run this from a plugin command/skill, or substitute an absolute path}/bin/tier-last-run.py" record --entry <name> --cmd <the command run, verbatim> --exit <its exit code>
```

Run this immediately after invoking a ceremony tier by hand, not only from inside an automated
ceremony step — an unrecorded hand-run is an undocumented bypass, not a faster path.

## When to Use

Three cadence gates chain this skill: `/workday-complete`, `/workweek-complete`,
`/merging-to-main`. Every other invocation is the PM asking for it by name. Light closes
(`/quick-wrap`, `/workstream-complete`) close without tests. Mid-work iteration uses the targeted
subset covering the change's own surface (Tier T), not this skill.

## Integration

Complements `verification-before-completion` (that skill requires evidence; this skill produces
it). `/workday-complete` Step 1 and `/workweek-complete` Step 2 both delegate here as sole owner
of the resolution logic — `/workday-complete`'s delegation fires inside the engine and
is not yet grant-check-observable the way `/workweek-complete`'s Bash-level call is. Detail: wiki.

## Common Mistakes

Unstaged files not covered by validation; secrets/`.env` staged; malformed JSON/YAML frontmatter;
empty stub files in `docs/plans/`/`tasks/`; skimming past a FAIL line; treating `skipped` as
passing. Full list and worked examples: wiki.
