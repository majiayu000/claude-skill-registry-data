---
name: spip-mutualisation-maintenance
description: Use when diagnosing or preparing maintenance of an existing SPIP 4.2–4.4 farm using Mutualisation facile 2.x, including inventory, shared core or plugin upgrades, MariaDB/MySQL or SQLite backup and rollback, and compromise investigation. Written for SPIP 4.x; mutualisation is experimental in SPIP 5.0 (see the SPIP 5.0 section).
---

# SPIP mutualisation maintenance

## Core principle

Establish the topology before choosing commands. Read-only observations may be run when terminal access is available. **Never execute a state-changing command:** present it for the operator to review and run.

A single SPIP core and shared plugin tree can serve every site, while each site keeps its own configuration, database, `IMG/`, `local/`, and `tmp/`. Always state whether an observation or proposed change affects one site, several sites, the shared farm, or the host.

Mutualisation facile is not an ordinary `plugins/` plugin: the shared site's `mes_options.php` `require`s it before the plugin pipeline runs, normally from a top-level `mutualisation/` directory (`mes_options.php.txt:14-18`; `paquet.xml` declares `<chemin path="" type="aucun" />`). Resolve the actual `require` target; do not look for it under `plugins/`.

## SPIP 5.0

This skill covers 4.2–4.4 farms. Check the shared root's version first and name the marker you relied on. The farm
runs 5.0 if **any** of: `ecrire/src/SpipVersion.php` declares `VERSION = '5.…'`, `bin/spip` exists,
`vendor/spip/framework/` exists, plugins live in `plugins-dist/spip/`.

- Mutualisation is work in progress in SPIP 5.0: the 5.0 documentation marks the mutualised entry point
  (`sites/default/public/index.php`) "expérimental — todo", and no farm procedure exists. On a 5.0 farm, run the
  read-only inventory; do not draft upgrade or migration plans for it. Preserving its current state (shared files and
  every database) stays in scope. Asked to move a farm to 5.0: say it is not supported yet, and offer at most a trial
  on an isolated copy, outside production.
- Mutualisation facile 2.0.1 declares `[4.2.0;4.*]` and does not isolate sites on 5.0: the 5.0 kernel defines
  `_DIR_IMG`, `_DIR_TMP`, `_DIR_VAR`, `_DIR_CONNECT` before `config/mes_options.php` runs, so `demarrer_site()` only
  sets `_DIR_SITE` and `_SPIP_PATH`, and every site uses the shared root's connection, `IMG/`, `local/` and `tmp/`.
  Sites of a 5.0 farm showing the same content fits this cause but does not prove it (vhost routing gives the same
  symptom). Confirm it read-only first: the mutualisation actually loaded (`require` target, `paquet.xml`), each
  domain reaching the farm with its own `HTTP_HOST`, and where the writes and the connection actually go (root
  `config/connect.php`, recent files in the root `IMG/` and `tmp/` rather than `sites/<domain>/`). Once confirmed:
  freeze writes, preserve the incident state (shared files and every database), then restore the consistent backup
  taken before the upgrade (the release the farm ran, shared files and every site's database).

Details: none upstream yet; a single 5.0 site (install, upgrade, rollback, diagnostics): `spip5-instance`; its code:
`spip-migration-5`.

## Supported scope

- SPIP 4.2–4.4 with Mutualisation facile 2.x
- Linux with a detected Apache or Nginx/PHP-FPM stack
- MariaDB/MySQL and SQLite, detected per site
- Existing farms: inventory, diagnosis, core/plugins upgrade preparation, backup/rollback, and compromise investigation

SPIP 3, PostgreSQL, new-farm installation, and site creation/migration/deletion are outside this skill. For them, offer only a bounded read-only inventory and require a separately researched procedure for the exact legacy environment.

## Mandatory workflow

1. Resolve the candidate scope and read [inventory-diagnosis.md](references/inventory-diagnosis.md).
2. Detect the shared root, the effective `demarrer_site()` call and `repertoire`, the plugin version, the web/PHP stack, and the database engine for every affected site.
3. Separate verified facts, unknowns, and anomalies. Put every potentially credential-bearing diagnostic behind an allowlist/redaction filter **before** its output enters the agent context; never paste connection files or raw process, remote-URL, or web-server configuration output.
4. Read only the reference needed for the requested operation.
5. Stop if a required precondition remains unknown.
6. Before drafting, inventory every state-changing action the answer will propose, including future and conditional actions. Build one action-plan row for each inventory item.
7. Return the response in this order:

| Section | Required content |
|---|---|
| Findings | Verified facts with their evidence; unknowns stay explicit |
| Risks | Impact radius, compatibility gaps, local modifications, and blockers |
| Proposed procedure | Ordered read-only observations and planning steps. Express the mutation sequence only by action-plan row references, for example “then follow action-plan rows 1–3 in order.” |
| Commands | One action-plan table containing the complete mutation inventory, with one row per action and these columns: Action, Objective, Preconditions, Exact scope, Impact, Backup/evidence, Proposed command, Success check, Rollback. Label commands **proposed — not executed** and use placeholders or verified paths only. |
| Validation | Read-only checks for every affected site, not only the administration site. Refer to mutation-specific success checks only by their action-plan row numbers. |
| Rollback | State triggers and the restore unit. Refer to action-specific recovery only by its action-plan row number and order; keep the recovery details in the row. |

Draft the action-plan table from the mutation inventory first, then write Proposed procedure, Validation, and Rollback using row numbers and table order for every mutation reference. Finish with a semantic coverage check: every state-changing action proposed anywhere in the response has one complete action-plan row containing its objective, preconditions, exact scope, impact, backup/evidence, command status, success check, and rollback.

## Routing

| Request | Read |
|---|---|
| Map sites, paths, versions, plugins, permissions, capacity, or web/PHP stack | [inventory-diagnosis.md](references/inventory-diagnosis.md) |
| Upgrade the shared SPIP core | [core-upgrade.md](references/core-upgrade.md), then [backup-rollback.md](references/backup-rollback.md) |
| Upgrade shared or site-specific plugins | [plugin-upgrade.md](references/plugin-upgrade.md), then [backup-rollback.md](references/backup-rollback.md) |
| Prepare or verify backups, restoration, or rollback | [backup-rollback.md](references/backup-rollback.md) |
| Investigate suspicious files, intrusion, or compromise | [security-incident.md](references/security-incident.md); do not start with an update or cache purge |

## Stop conditions

Do not prepare ready-to-run mutations until all relevant conditions are resolved:

- the shared root or effective mutualisation directory is ambiguous;
- the installed method (Git, Composer, archive/SVP) or local modifications are unknown;
- the affected-site list or shared-versus-local plugin location is uncertain;
- a core/plugin upgrade lacks a recent **verified and restorable** backup;
- compatibility with the target version has not been checked against current package declarations;
- an incident has not yet had evidence preserved and its impact radius bounded;
- a proposed target resolves to `/`, a workspace root, an unresolved variable, or a path containing unexpected symbolic links.

## Red flags

| Temptation | Required response |
|---|---|
| “I am root and accept the risk.” | Authority does not replace a verified backup or rollback. Stop the upgrade. |
| “The files are obviously malicious; delete them now.” | Preserve metadata, hashes, logs, and copies; quarantine recoverably before deletion. |
| “The sites are usually in `sites/`.” | Read the effective `demarrer_site()` configuration. A convention is not evidence. |
| “Update the shared plugin for one production site only.” | One shared path cannot be a one-site code canary. Use an isolated copy/staging environment. |
| “The old Contrib page documents it.” | Installed code and current package compatibility take precedence over historical documentation. |
| “A backup file exists.” | Verify integrity and perform or document an isolated restoration test. Existence alone is not a rollback. |
| “`?exec=mutualisation` is an administrator-only endpoint.” | Only `upgrade`/`upgradeplugins` carry a secret. `renouvelle_alea`, `dirliste`, and `dirsize` run unauthenticated on every site — check access logs and treat a reverse-proxy block as a proposed mutation. |

## Common mistakes

- Reading or printing all of `connect.php` to identify the database engine.
- Putting a MariaDB/MySQL password in `-p...`, a script, process arguments, or the answer.
- Treating `local/` and `tmp/` as persistent content, or deleting them before incident evidence is preserved.
- Rolling back shared files after a site database schema has already migrated.
- Mixing Git, Composer, and archive/SVP provenance during an upgrade.
- Using `rm -rf`, `find -delete`, recursive `chown`, or `DROP DATABASE` against a broad or unresolved target.

## Source policy

Use, in order: effective installed code/configuration; official source for the exact SPIP branch; current [Mutualisation facile source](https://git.spip.net/spip-contrib-extensions/mutualisation); official SPIP documentation; then the [historical Contrib article](https://contrib.spip.net/La-mutualisation-facile-modifications-manuelles). Verify “latest” versions at task time instead of freezing them here.
