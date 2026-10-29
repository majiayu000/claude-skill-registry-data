---
name: amazon-orders
description: Archive Amazon orders locally with amz, search purchases offline, and assess import coverage.
---

# Amazon orders

Use [jgalea/amz](https://github.com/jgalea/amz) through `bash scripts/amz`.
The launcher requests `latest` for Go and amz through mise without editing
project or global tool configuration. Downloads persist. Resolve this skill's
directory first; helper paths below are relative to it.

## Choose the operation

1. Select the account, storefront, and date range from the request or existing
   configuration (`bash scripts/amz accounts`). Use the same explicit `--account`
   and `--market` throughout: sync otherwise defaults to the home storefront,
   while offline queries may combine stored storefronts. Use `all` only for an
   intentional combined query.
2. For a purchase search or analysis of stored orders, continue below. Finish
   when the selected query succeeds and the result or absence of data is reported.
3. Before sync, login, or any browser-launching operation (including `--live`),
   read [sync.md](references/sync.md). Finish an import when sync exits successfully
   and the coverage check below is reported; otherwise report the unfinished stage.

The state directory is `AMZ_CONFIG_DIR`, defaulting to `~/.amz`. Retain its
`amz.db` and account profiles for the archive. Keep personal exports outside
public repositories and artifacts, in a private destination chosen by the user.

## Query stored orders

Ordinary `orders` reads SQLite; `--live` launches a browser and fetches the site.
Substitute the selected account, storefront, and real ISO dates in these examples:

```sh
bash scripts/amz orders --account personal --market com --since YYYY-MM-DD --until YYYY-MM-DD --grep cable
```

For coverage, feed all stored orders for that account/storefront to the helper,
then apply the date bounds there so it can report undated rows separately:

```sh
set -o pipefail
bash scripts/amz orders --account personal --market com --json | python3 scripts/order-coverage.py --since YYYY-MM-DD --until YYYY-MM-DD
```

The helper reports counts and date bounds without titles, order IDs, or amounts.
Its `stored_*` fields describe the input selection, not necessarily the entire
SQLite database. Missing fields require checking against the source before
calling them parser errors. An empty result establishes only that the local
store has no matching rows; offer a scoped sync if current site data is needed.

For an offline check after tool installation, set
`AMZ_CHROME=/nonexistent/amz-offline-check` on the launcher for one query.
A successful query with that setting establishes that Chrome was not required;
it does not block mise downloads or prove the absence of all network activity.

Report the selected account/storefront, requested and stored date ranges,
order/item counts, missing fields, and observed offline behavior. Reconcile with
source counts when available. Successful scraping alone cannot prove complete
history; upstream excludes archived orders. Reading and local archiving are the
scope here; account transactions, return submission, and external publication
require their own user instructions.
