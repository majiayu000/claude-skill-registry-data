---
name: clickup-task
description: Create a ClickUp task in the Product Backlog and add it to the current sprint, with Rob's standard custom fields pre-filled.
user-invocable: true
allowed-tools: Bash
---

Create a ClickUp task in the Product Backlog, assign it to Rob, add it to the current sprint, and set the standard custom fields.

## Context

- **Rob's member ID**: `106018222`
- **Product Backlog lists** (pick the right one based on task type):
  | List | ID |
  |---|---|
  | Features | `901325511834` |
  | Bugs | `901325511839` |
  | Chores | `901326499064` |
  | Tech Debt | `901325511845` |
  | Requests | `901325511852` |

- **Current sprint**: Check the "FF Sprint Cycles 2025-2026" folder for the active sprint (the one whose date range includes today). As of late June 2026, Sprint #11 (6/8–7/1) is `901327441754` and Sprint #12 (7/1–7/27) is `901327580501`.

## Custom field defaults (Rob's standard)

These are the defaults to use unless the user says otherwise. All IDs and option UUIDs are stable.

| Field | Field ID | Default | Option UUID |
|---|---|---|---|
| Product Work Type | `84c55574-1161-45e1-adae-0a859f50f792` | Infrastructure & Maintenance | `beb29869-8349-4c7c-925b-9a3759f4f27c` |
| Capacity Type | `64ef3769-f7bd-4eb8-a535-8a280c52228d` | Rogue Time | `94fb9005-4caa-42d6-bef2-d9c4e7c405e2` |
| Task Purpose | `8bc56219-8b5a-4b41-8d3a-7d878aed9617` | Tech Debt | `d5af7f82-4762-4060-945a-a5c8c90a7468` |
| Rogue Time | `ee70f68e-da4f-43e1-a014-7d4e5124bd6c` | checked | `true` |

Other common Product Work Type options:
- Customer Growth & Retention: `62ac2807-199f-45db-af6b-fee110cfcffd`
- Paid Services & Modules: `70a97b90-154c-4a61-9b5b-1add65b8d75b`

Other common Task Purpose options:
- Feature Delivery: `dabf86ed-89e1-44f0-ad14-a97b37858aa4`
- Bug Fix: `4ee72bdf-bc3a-4734-be3e-9952219c37f4`
- Chores/Maintenance: `4d0f433a-400b-4b05-b3b8-bf125a0063bd`

## Steps

1. **Determine the task name** — use the description from the current jj commit if not provided by the user:
   ```bash
   jj log -r @ --no-graph -T 'description'
   ```

2. **Determine the target list** — ask the user if not obvious. Default to Tech Debt (`901325511845`) for infrastructure/devops work.

3. **Create the task** via `clickup_create_task`:
   - `list_id`: chosen above
   - `assignees`: `["106018222"]`
   - `custom_fields`: all four defaults above (override if user specified different values)

4. **Add to current sprint** via `clickup_add_task_to_list` with the active sprint list ID.

5. **Report** — output the task URL and ID (format: `CU-<id>`) for use in PRs.
