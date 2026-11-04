---
name: info
description: "Show Forge project state and harness metrics. Triggers: \"forge info\", \"where are we?\", \"show progress\", \"forge metrics\", \"measure Forge\"."
---

<Purpose>
One-glance view of the project plus harness effectiveness.
Answers: where are we, what's blocking, what's next, how much did Forge intervene.
Prioritizes actionable information over completeness.
</Purpose>

<Use_When>
- User asks "forge info", "where are we?", "show progress"
- KO: "진행 상황", "어디까지 했어"  JA: "進捗", "どこまで進んだ"  ZH: "进度", "到哪了"
- User asks for Forge metrics or harness overhead
- Between phases to check overall state
- When returning to a session
</Use_When>

<Steps>

## 1. Read state

Load `.forge/state.json`. If missing → "No active Forge project. Use `forge` to start one."

Also load if they exist:
- `.forge/runtime.json` — lanes, blockers, ownership, harness stats
- `.forge/holes/` — issue counts by severity
- Latest git tag matching `forge/*`

## 2. Calculate progress

Build mode (N/8):

| Phase | Range  |
|-------|--------|
| 0–1   | 0–25%  |
| 2     | 25–40% |
| 3     | 40–70% |
| 4–5   | 70–85% |
| 6     | 85–95% |
| 7     | 95–100%|

Repair mode (N/7):

| Phase | Range  |
|-------|--------|
| 0–1   | 0–25%  |
| 2     | 25–50% |
| 3     | 50–70% |
| 4–5   | 70–90% |
| 6     | 90–100%|

Within Phase 3, refine by lane completion ratio (done lanes / total lanes).

## 3. Display dashboard

### Default (compact) view

```
Forge: {{project_name}} ({{build|repair}})
Phase {{N}}/{{max}} — {{phase_name}}
{{progress_bar}} {{X}}%

Next action: {{next_action_summary}}
{{actionable_summary}}

Lanes: {{done}}/{{total}} done{{if blocked}}, {{blocked}} blocked{{/if}}
Issues: {{blocker}} blocker, {{major}} major, {{minor}} minor
Tag: {{latest_tag}}

Harness: tier={{tier}} sessions={{N}} agents={{N}} failures={{N}} stops={{N}}
```

### Actionable summary rules

Use `runtime.next_action.summary` when present. That is the canonical next-step line.

Then derive the supporting summary below. Pick the FIRST that applies:

| Priority | Condition                  | Output format                                        |
|----------|----------------------------|------------------------------------------------------|
| 1        | Customer blocker exists     | "Waiting on you: {{what's needed}}"                  |
| 2        | Internal blocker exists     | "Blocked: {{description}} (owner: {{role}})"         |
| 3        | Delivery ready for review   | "Ready for review — run `forge deliver` to finalize" |
| 4        | Lanes in progress           | "Active: {{lane names}}. Next: {{recommended action}}" |
| 5        | Default                     | "Phase {{name}} in progress"                         |

### Ownership hint

When lanes exist, append ownership context after the lane count:

```
Lanes: 2/5 done, 1 blocked
  auth-api (developer, in_progress) — last: "API routes done, testing auth middleware"
  db-schema (cto, blocked) — waiting on contract review
```

Only show lane detail for non-done lanes. Keep it to one line per lane.

### Verbose view

When the user asks "forge info --verbose", "detail", or "detailed":

- Full lane list with status, owner, and worktree path per lane
- All hole summaries with severity and attempt count
- Handoff notes from runtime (latest per lane)
- Active worktree paths
- Phase gate status (what's satisfied, what's pending)
- Full harness metrics: test runs, test failures, rollback count
- If baseline data exists, show with/without harness comparison

Default is always the compact view.

</Steps>

<Progressive_Disclosure>
- Load `skills/ignite/references/harness-ab-eval.md` when a structured with/without comparison is needed.
</Progressive_Disclosure>

<Tool_Usage>
- Read: .forge/state.json, .forge/runtime.json, .forge/holes/*.md
- Bash: git tag -l "forge/*" --sort=-version:refname | head -1
- Preferred implementation surface: `node scripts/forge-status.mjs` (`--json` or `--verbose` as needed)
</Tool_Usage>
