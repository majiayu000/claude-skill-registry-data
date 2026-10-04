---
name: frontline-billing
allowed-tools: Bash(frontline:*)
description: Query Frontline billing information using the Frontline CLI — Studio plan usage, credit consumption history, Max plan usage, and Max seat assignment. Use when the user asks about their billing, credits, plan, subscription, usage limits, or Max seats.
---

## Prerequisites

- The `frontline` CLI must be installed (`npm i -g @getfrontline/cli`).
- The user must be authenticated (`frontline auth login`).
- `usage` commands and all `seats` commands require a USER API key (account-level keys are rejected).
- `seats assign` / `seats unassign` additionally require the calling user to be an OWNER or ADMIN.

## Commands

### Get current billing plan (summary)

```bash
frontline billing get [--pretty] [--debug]
```

Output is **JSON by default** (`--json` is accepted as a no-op). Use `--pretty` (or `--table`, an alias) for key/value display.

| Flag               | Description                                      |
| ------------------ | ------------------------------------------------ |
| `--pretty`         | Human-readable key/value display instead of JSON |
| `--api-key <key>`  | Override the stored API key for this request     |
| `--profile <name>` | Use a specific CLI profile                       |
| `--debug`          | Show HTTP request/response diagnostics           |

### Studio usage (account-level product)

```bash
# Get billing info as JSON (default)
frontline billing get

# View current billing plan as key/value pairs
frontline billing get --pretty
```

Returns credits used vs limit, counts of agents, workflows, flows, users and knowledge bases against plan limits, current plan, subscription details, and any scheduled plan change (`next`).

### Credit consumption history

```bash
frontline billing studio credits [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD] [--table]
```

Returns `{ results: [...] }` with one entry per day per AI model: `date`, `model`, `modelName`, `totalCredits`, `messageCount`. Use `--table` for a readable breakdown.

### Max usage

```bash
frontline billing max usage
```

Returns the Max plan (`plan`), subscription status and renewal (`subscription`), seat totals (`seats`), feature limits (`limits`: knowledge sources, playbooks, custom labels, tasks, WhatsApp numbers), and any scheduled plan change (`next`). All fields are `null` on the free trial except `limits`.

### Max seats

```bash
frontline billing max seats list [--pretty]
frontline billing max seats assign <userId>
frontline billing max seats unassign <userId>
```

- `list` returns `totalSeats`, `assignedCount`, `available`, plus `assigned` (users holding a seat, with `assignedAt`) and `unassigned` (users without one).
- `assign` / `unassign` take a single numeric user ID — find IDs with `frontline users list`. The backend handles seat accounting; do not try to send arrays or full seat lists.
- `assign` fails with 400 if the user already has a seat or has no Max profile, and with 426 (upgrade required) when no seats are available.
- `unassign` fails with 400 if the user has no active seat.
- Both require the caller to be an OWNER or ADMIN; otherwise they return 404 (the API does not reveal account/user existence to non-admins).

**Examples:**

```bash
# How many credits have we burned this month, by model?
frontline billing studio credits --start-date 2026-06-01 --table

# Who has a Max seat?
frontline billing max seats list --pretty

# Give Jane (user 42) a Max seat
frontline billing max seats assign 42
```

## Troubleshooting

- **"No API key found"**: run `frontline auth login` to authenticate.
- **401 on `usage` / `seats`**: the configured key is an account-level key; these endpoints need a USER API key.
- **404 on seat assign/unassign**: the target user doesn't exist in your account, or the calling user is not an OWNER or ADMIN.
- Use `--debug` to see the full HTTP request URL, headers, and response status for diagnosing issues.
- Output is JSON by default (pipe to `jq` or other tools); use `--pretty` for human-readable output instead. `--json` is also accepted as a no-op.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
