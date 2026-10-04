---
name: agent-playbooks
description: Create, list, inspect, update, and delete agent playbooks from the CLI, and see which playbooks are assigned to an agent. Agent playbooks are reusable instruction sets (SOPs) that steer how a Frontline agent handles a task. Use when managing playbooks for customer-facing agents.
allowed-tools: Bash(frontline:*)
---

# Agent Playbooks

Agent playbooks are reusable instruction sets that guide how a **Frontline agent**
(a customer-facing agent) handles a specific task. A playbook bundles instructions plus
optional tools, record types, and custom tools. Playbooks are then assigned to an
agent so it can execute them at runtime.

> Not to be confused with **Max playbooks** (`max playbooks …`), which steer the user's
> own Max agent. These commands manage playbooks for your Frontline agents.

## List & inspect

```bash
frontline playbooks list --table
frontline playbooks list --filter-text "refund" --visibility ACCOUNT --is-active true
frontline playbooks describe 42
```

## Create

Three fields are required: `--name`, `--description` (when to use it, min 10 chars), and
`--instructions` (the actual SOP, min 10 chars).

```bash
frontline playbooks create \
  --name "Refund flow" \
  --description "How to process a customer refund request" \
  --instructions "1. Verify the order number. 2. Confirm the refund window. 3. ..."
```

Playbooks are active by default. Pass `--inactive` to create one disabled.

Optional advanced fields take JSON:

- `--tools '["tool_name"]'` — system tool names the playbook may use.
- `--selected-record-types '[ ... ]'` — record-type tool settings.
- `--selected-custom-tools '[ ... ]'` — custom-tool settings.
- `--connected-account-configs '[ ... ]'` — connected-account tool configs.
- `--visibility ACCOUNT|PRIVATE` — `ACCOUNT` shares it with the whole account; `PRIVATE` keeps it to you (default `ACCOUNT`).

## Update & delete

Only the **creator** (or an OWNER/ADMIN) can update; only the **creator** can delete.

```bash
frontline playbooks update 42 --instructions "Updated steps ..."
frontline playbooks update 42 --inactive       # disable
frontline playbooks update 42 --active          # re-enable
frontline playbooks delete 42
```

## Assigned playbooks

See which playbooks are assigned to a specific agent:

```bash
frontline playbooks assigned --agent-id <agentId> --table
```

To find agent IDs, use `frontline agents list`.

---

## See also

- Agents: the `frontline-agents` skill and `frontline agents …`.
- Full reference: <https://docs.getfrontline.ai/cli>. App walkthroughs: <https://help.getfrontline.ai>.
