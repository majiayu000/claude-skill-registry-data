---
name: linear-custom-view
description: Read Linear Custom Views through the direct Linear GraphQL API using a local LINEAR_API_KEY. Use when the user asks to inspect a Linear view URL, extract the live issue queue, preserve manual order, or use a Custom View as a source of task priority.
metadata:
  category: productivity
  capability_taxonomy_ids:
    - cap.productivity.issue_tracking
    - cap.tools.api_automation
  compatibility:
    runtimes:
      - codex
      - claude_code
      - cursor
      - antigravity
      - windsurf
  distribution_scope: public
  invocation_strategy: explicit
  version: v0.2
  source_of_truth: https://github.com/nicshik/linear-skills
---

# Linear Custom View

Use this skill when the user gives a Linear Custom View URL, slug, ID, or view name and wants the live ordered issue list.

This skill is useful when Linear MCP cannot read custom views or when the view's manual order is the source of implementation priority.

## Preconditions

- `LINEAR_API_KEY` is available in the shell, `LINEAR_ENV_FILE`, `--env-file`, or a local `.env.local`.
- The key belongs to a Linear user with access to the workspace and the Custom View.
- Network access to `https://api.linear.app/graphql` is allowed.

## Non-Negotiable Rules

- Use `scripts/custom_view.py`.
- Use the shared GraphQL client from this repository; it resolves `LINEAR_API_KEY`, uses `certifi` for TLS when available, and redacts the token from API errors.
- Preserve manual order with `sort: [{ manual: { order: Ascending } }]` unless the user asks otherwise.
- Never print the API key.
- Treat the Custom View filter as the source of truth. Do not add hidden filters unless the user asks.
- If a completed issue disappears from the view, explain that the view filter controls visibility.
- Use this skill only to read the ordered Custom View queue. Read full issue details, comments, and blocking links through the normal Linear connector or the caller's project workflow.
- When another agent will consume the result, prefer `--json --first` and read `first_issue` instead of reinterpreting issue order.
- When the user gives an expected workstream, use `--expect-label`, `--exclude-label`, `--expect-title-regex`, or `--skip-title-regex` so the output includes `first_matching_issue` and `skipped_issues`.

## Codex Permission Rule

When Codex sandboxing asks for approval because the script needs network access, request a persistent command prefix:

- `sandbox_permissions`: `require_escalated`
- `prefix_rule`: `["python3", "linear-custom-view/scripts/custom_view.py"]`

Tell the user to choose the option like "Yes, and don't ask again for commands that start with this prefix". After that, the same Custom View script can run without repeated prompts.

Keep the command prefix stable by running from the `linear-skills` repository root. Pass the API key only through the environment or `--env-file`; never pass the key as a command argument.

For full setup details and a ready-to-copy rules snippet, see `docs/codex-approvals.md` in the repository root.

## Default Flow

1. Pass the Linear view URL, slug, ID, or exact name to the script.
2. Use `--json` when the result will drive automation.
3. Use `--first` when the workflow needs the first actionable issue from the manual queue.
4. Use `--explain-filter` when reporting why completed or filtered issues are missing.
5. Use `--include-relations-summary` only for a light read-only overview; do not treat it as a replacement for full `linear:linear` issue reads.
6. If the queue is expected to contain a specific workstream, pass explicit selection filters and read `first_matching_issue`, not just `first_issue`.
7. Read the returned `filterData`, issue count, ordered issues, optional `first_issue`, and optional `skipped_issues`.
8. Use the returned order as the queue order.

## Recommended Commands

```bash
python3 scripts/custom_view.py "https://linear.app/example/view/team-queue-123abc" --env-file /path/to/.env.local
python3 scripts/custom_view.py 123abc --json
python3 scripts/custom_view.py 123abc --json --first --explain-filter
python3 scripts/custom_view.py 123abc --json --first --expect-label Platform --exclude-label Blocked --skip-title-regex '^\[Blocked\]'
python3 scripts/custom_view.py 123abc --json --include-relations-summary --limit 20
python3 scripts/custom_view.py "Team Queue" --limit 50
```

## Output Shape

- Text output: view name, slug, issue count, then one issue per line in manual order.
- `--json` output: `schema_version`, `fetched_at`, `queue_order`, view metadata, issue count, and ordered issue objects.
- `--first` output: `first_issue` with `row_index`, `identifier`, `status`, `status_type`, `manual_order`, `view_slug`, and the original issue row. Completed/canceled rows are skipped when looking for the first actionable issue.
- Selection filter output: when any of `--expect-label`, `--exclude-label`, `--expect-title-regex`, or `--skip-title-regex` is used, JSON includes `selection_filters`, `first_matching_issue`, and `skipped_issues`.
- `--explain-filter` output: `filter_explanation` with raw `filterData` and a note that visibility is controlled by the Custom View.
- `--include-relations-summary` output: labels plus light `relations_summary` and `comments_summary` counts from Linear connections.
- On ambiguity, the script lists matching views and exits without guessing.

## Project Workflow Boundary

For larger project workflows, this skill covers only the queue-read step:

1. Read the live manual queue from Linear Custom View.
2. Select the first actionable issue when requested.
3. Read full issue context through the normal Linear connector or project-specific workflow.
4. Change statuses outside this queue reader after the caller has completed its own readiness checks.
