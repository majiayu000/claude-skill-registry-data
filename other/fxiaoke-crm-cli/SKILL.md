---
name: fxiaoke-crm-cli
description: Use for Fxiaoke or 纷享销客 CRM tasks, including records, customers, contacts, opportunities, contracts, deal cycles, conversion, sales orders, delivery, payments, receivables, follow-ups, statistics, and writes through the official sharecrm CLI.
metadata:
  requires:
    bins:
      - sharecrm
      - jq
---

# Fxiaoke CRM CLI

Treat Fxiaoke CRM as the fact source and use the official `sharecrm` CLI. Results are limited to the authenticated user's CRM permissions. Never ask for tokens, secrets, cookies, credentials, or manual token paste.

## Workflow

1. Check authentication:

```bash
sharecrm auth status
```

2. Verify the current remote command surface with `sharecrm --help` and the relevant subcommand `--help` before relying on syntax.
3. Inspect the live object schema before querying:

```bash
sharecrm data describe get -d '{"apiName":"ContractObj"}'
```

The following legacy form is incomplete and must not be run because it omits the required payload:

```text
sharecrm data describe get
```

4. Query records using the live object, field names, and options. Default to read-only work. Page with `LIMIT 50 OFFSET n` until `.queryMeta.returnedCount` and `.queryMeta.totalNumber` show the result set is complete.
5. Before any CRM create, update, delete, follow-up, or other write, show the exact intended change and obtain explicit confirmation immediately before executing it.

Tenant schemas and CLI commands can change. Never guess fields, option values, or write syntax. For every metric, disclose the date range and timezone, source object, date field, metric field, status field and filter, included records, formula, and numerator/denominator when applicable.

See [CLI reference](references/cli-reference.md) for commands, metric recipes, examples, and troubleshooting.
