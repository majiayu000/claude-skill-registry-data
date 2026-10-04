---
name: beads-priority-assignment
description: Choose Beads issue priority (P0–P4, numeric, or named) from urgency, impact, and risk when creating or triaging work.
---

# beads-priority-assignment

Use this skill whenever you **`bd create`** a issue or **re-triage** priority (`bd update`) so the queue reflects real severity. Follow `bd doctor` / your Beads version for the exact `--priority` values your CLI accepts (integers `0`–`4`, labels like `P0`–`P4`, and/or names like `critical` / `high` / `medium` / `low`).

## Harness mapping (dashboard + `types/beads.ts`)

Exports and the dashboard normalize numeric priority roughly as:

| Tier | Typical `bd` inputs | Meaning in this harness |
|------|---------------------|-------------------------|
| **Critical** | `0`, `P0`, `critical` | Drop other work: production down, active exploit, data loss, irreversible customer harm |
| **High** | `1`, `P1`, `high` | Urgent: broken main path, release blocker, failing CI on default branch, severe bug with weak workaround |
| **Medium** | `2`, `P2`, `medium` | Default scheduled work: most features, typical bugs, refactors with agreed dates |
| **Low** | `3`–`4`, `P3`–`P4`, `low` | Backlog: polish, nice-to-have, cleanup, research spikes with no near deadline |

Values `3` and above both map to **low** in the static dashboard export — use them to order work inside the backlog if your `bd` install preserves numeric order.

## Rubric (three axes)

Score mentally; **the highest axis that applies** usually wins (then downgrade one step if mitigations exist).

1. **Urgency** — Must this start today / this week / this sprint / later?
2. **Impact** — How many users or systems are affected, and how badly?
3. **Risk if deferred** — Does waiting increase security exposure, compliance exposure, cost, or cascade blockers?

**Escalate** one level if the issue **blocks** other ready work or sits on a **critical path** to a dated epic.

**De-escalate** one level if there is a **documented workaround**, the area is **feature-flagged off**, or the report is **duplicate / unclear** until clarified.

## Defaults

- If the user states “P0” / “urgent” / “critical”, map to that tier — do not normalize down.
- If you have **no** signal after the rubric, use **`P2` / `2` / `medium`** (harness default), not empty priority.
- **Never** inflate priority to look important; **never** leave priority unset on purpose when the CLI supports it.

## Examples

| Situation | Suggested priority |
|-----------|-------------------|
| Auth service returning 500 for all logins | `0` / `P0` / `critical` |
| CI red on `master`, no merge until fixed | `1` / `P1` / `high` |
| New feature from roadmap, normal sprint | `2` / `P2` / `medium` |
| Typo in internal-only docs | `3` or `4` / `low` |
| `/triage` auto-filed “CI failing on PR #n” (matches existing harness command) | `1` / `P1` / `high` |

## Commands (non-interactive)

```bash
bd create --type task --title "..." --repo <repo> --priority <value>
bd update <id> --priority <value>
```

After changing priority on an existing issue, add a short Beads comment: `worklog: priority set to <value> because <one line>.`
