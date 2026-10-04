---
name: max-playbooks
description: Create, list, inspect, update, delete, and assign your own Max playbooks from the `max` CLI. Max playbooks are reusable instruction sets that steer the user's personal Max agent — Chat playbooks (workflows/SOPs) and Auto-Drafting playbooks (email tone/templates). Use when managing how Max itself behaves, not customer-facing agents.
allowed-tools: Bash(max:*)
---

# Max Playbooks

Max playbooks are reusable instruction sets for **your own Max agent**. Two types:

- `CHAT` — workflows, procedures, and SOPs for chat-based interactions (desktop app, WhatsApp, Slack).
- `AUTO_DRAFTING` — email-specific playbooks for tone guides, templates, and drafting instructions.

> These steer **Max itself**. To manage playbooks for customer-facing Frontline agents,
> use `frontline playbooks …` (the `agent-playbooks` skill) instead.

Auth is the same per-user API key the `frontline` CLI uses (`max auth login <key>`).

## List & inspect

```bash
max playbooks list --type CHAT --pretty
max playbooks list --filter-text "follow up" --is-active true
max playbooks get 42
```

## Create

`--name`, `--type` (`CHAT` or `AUTO_DRAFTING`), and `--instructions` (min 10 chars) are required.
A new playbook is active and auto-assigned to your Max agent by default.

```bash
max playbooks create \
  --type CHAT \
  --name "Weekly status update" \
  --instructions "When asked for a status update, pull open deals and summarize by stage."
```

Useful flags:

- `--description "<when to use it>"`
- `--visibility ACCOUNT|PRIVATE` (default `PRIVATE`)
- `--no-assign` — create without assigning to your Max agent.
- `--inactive` — create disabled.
- `--tools '["tool_name"]'`, `--integrations '["gmail"]'`, `--selected-record-types '[…]'`, `--selected-custom-tools '[…]'` (JSON). **Note:** These tool and resource scoping flags are only applicable to `AUTO_DRAFTING` playbooks; they are ignored for `CHAT` playbooks, which run in a sandbox with complete access.

### Email scoping (AUTO_DRAFTING only)

By default a playbook applies to **all** of your connected email accounts. To scope an
`AUTO_DRAFTING` playbook to specific Gmail/Outlook accounts, pass their connected-account IDs:

```bash
max playbooks create \
  --type AUTO_DRAFTING \
  --name "Sales tone" \
  --instructions "Reply warmly, sign off with my name, keep it under 5 sentences." \
  --connected-account-ids '[12, 19]'
```

- `--connected-account-ids '[…]'` automatically sets `--applies-to-all-accounts false`.
- Only **email** accounts (Gmail/Outlook) that belong to you can be scoped; non-email or
  non-AUTO_DRAFTING playbooks are rejected.
- On update, pass `--applies-to-all-accounts true` to clear scoping and apply to all accounts.

> File attachments (for `AUTO_DRAFTING`) are not yet available via the CLI.

## Update & delete

Only the creator can update or delete a playbook.

```bash
max playbooks update 42 --instructions "Updated steps ..."
max playbooks update 42 --active        # enable
max playbooks update 42 --inactive      # disable
max playbooks delete 42
```

## Assign / unassign to your Max agent

Assigning makes the playbook available to your Max agent at runtime (subject to your plan's
assignment quota).

```bash
max playbooks assign 42
max playbooks unassign 42
```

---

## See also

- Chatting with Max: the `max-chat` skill. Auth: the `max-auth` skill.
- Full reference: <https://docs.getfrontline.ai/cli>. App walkthroughs: <https://help.getfrontline.ai>.
