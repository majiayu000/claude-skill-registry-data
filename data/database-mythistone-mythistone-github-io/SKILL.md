---
name: database
description: "MythiStone MySQL layer: schema in backend_scripts/database.sql, every query in databaseConnector.py, aggregation stored procs, the localDev seeder table registry. Use when adding or changing a table, query, proc or aggregate."
---

# Database domain

## Gotchas

Before changing a file listed below, read its gotcha: `ref/<id>.md` in this skill (or `kb_gotcha <id>`).

| id | rule | files |
|---|---|---|
| `add-database-table` | What else changes when backend_scripts/database.sql grows a base table (the seeder registry, seed rows, the production server), and what the table name decides | `backend_scripts/database.sql`, `backend_scripts/localDev/table_registry.py`, `backend_scripts/localDev/seed_test_db.py` |
| `aggregation-pipeline` | How to add or change a nightly aggregate without wedging the server, and what every reader of the aggregate tables owes the pipeline | `backend_scripts/database.sql`, `backend_scripts/aggPipelineHealth.py` |
| `dedup-dictionary-hash-contract` | The talent and bonus-id dictionaries (talent_sets / bonus_sets) tie the Python collector, any SQL that writes them and every talent aggregate together through one content hash and one join rule | `backend_scripts/commonUtils.py`, `backend_scripts/collectLeaderboardData.py`, `backend_scripts/database.sql`, `backend_scripts/databaseConnector.py` |
| `gear-and-talent-data-retention` | Equipped-gear rows and talent information are purged after about 2 weeks, so every aggregate over them is a full rebuild, never watermark-incremental, and test data must be recent | `backend_scripts/database.sql`, `backend_scripts/localDev/seeders.py` |
| `keystone-guru-mapping-data` | route_data.mapping_version is the keystone.guru per-dungeon mapping version, not its global mapping_version_id | `backend_scripts/collectLeaderboardData.py`, `backend_scripts/database.sql` |
| `lust-pull-signature` | The "Most Lusted Pulls" pull signature (npc_id:count tokens) is one string expression repeated in three SQL constants and parsed by the dungeon generator, the dungeon template and the bot | `backend_scripts/databaseConnector.py`, `backend_scripts/generateDungeonPages.py`, `templates/dungeon_page.html`, `discord_bot/cogs/dungeon.py` |
| `pooled-connection-gotchas` | Two rules every user of the mysql.connector pool follows, a write commits only on a configured session or with an explicit commit, and no pooled connection is held across a slow step | `backend_scripts/databaseConnector.py`, `backend_scripts/collectLeaderboardData.py`, `backend_scripts/simcBis.py`, `discord_bot/db.py` |
| `runs-per-dungeon-rollup` | The production DB runs at full load and cannot be scaled, so season-wide run counts are read from nightly rollups and a build never repeats or parallelizes a heavy query | `backend_scripts/databaseConnector.py`, `backend_scripts/database.sql`, `backend_scripts/image_generation/*`, `backend_scripts/generateDashboardPage.py` |
| `table-storage-placement` | Where the large MySQL tables physically live (general tablespaces vs. per-table DATA DIRECTORY on specific host drives) and the only working way to move a table to another drive | `backend_scripts/database.sql` |
| `verify-database-sql` | How to syntax and runtime verify backend_scripts/database.sql stored procedures against an ephemeral MySQL 8 Docker container | `backend_scripts/database.sql` |
