---
name: mariadb-lord
always: true
description: Architect-level mastery for MariaDB — design, operations, Laravel/Filament/Nova integration, multi-tenancy, migration from MySQL, Galera Cluster, and performance.
triggers:
  - mariadb lord
  - mariadb

---
[SKILL] mariadb-lord
[OBJ] Design, tune, secure, integrate with Laravel, Filament, Nova, implement multi-tenancy, migrate to/from, and operate MariaDB via Context7.
[RULES]
1. [CMD] IDs: MariaDB docs `/websites/mariadb` source `/mariadb/server`; Docker image `/mariadb/mariadb-docker` source `/mariadb-corporation/mariadb-server-docker`; Node connector `/mariadb-corporation/mariadb-connector-nodejs`; Python client `/pymysql/pymysql`; Laravel `/laravel/docs`; Spatie multi-tenancy `/spatie/laravel-multitenancy`; Stancl tenancy `/archtechx/tenancy`; Filament `/filamentphp/filament`; Filament tenancy `/tomatophp/filament-tenancy`; Filament Shield `/bezhansalleh/filament-shield`; Laravel Nova `/websites/nova_laravel_v5`.
2. [REQ] Route every question through pillars: design, performance, optimization, operations, migration, laravel-integration, multi-tenancy, admin-panels.
3. [REQ] Query Context7 with user's full question + topic (design, performance, optimization, operations, migration, laravel, multi-tenancy, filament, nova).
4. [REQ] Distinguish MariaDB vs MySQL: pluggable storage engines, optimizer enhancements, GTID/wsrep, Galera, JSON, virtual columns, dynamic columns, DEFAULT expressions, temporal tables.
5. [REQ] Concrete engine terms: InnoDB, Aria, MyRocks, ColumnStore, Spider, Buffer Pool, redo/undo log, WAL, LSN, MVCC, wsrep, SST, IST, GTID, virtual column, persistent column, query cache, binlog, slow query log.
6. [REQ] Prefer `mariadb`/`mariadb-dump`/`mariadb-backup`/`mariadb-secure-installation` over legacy `mysql*` tools in MariaDB 10.5+.
7. [REQ] Security: `MARIADB_*` env vars on Docker, TLS for Galera/client, least-privilege users, avoid `SUPER` over `root` unless required.
8. [REQ] Migration from MySQL: validate feature gaps, compatibility mode, `mariadb-upgrade`, `SET sql_mode=ORACLE/POSTGRESQL` only when intended.
9. [REQ] Operations: Galera bootstrap order, `wsrep_cluster_address=gcomm://`, SST/IST methods, `mariadb-backup --prepare` before restore, monitor `wsrep_local_state_comment`.
10. [REQ] Laravel + MariaDB: use `DB_CONNECTION=mysql` driver, MariaDB 10.6/10.11/11.x, `utf8mb4_unicode_ci`, `PDO::MYSQL_ATTR_SSL_CA`, migrations with `php artisan migrate`, model `#[Connection('tenant')]`, test with `migrate:fresh --database=`.
11. [REQ] Multi-tenancy: choose database-per-tenant vs schema-per-tenant vs table-per-tenant; central `landlord` DB; tenant connection switching via resolver/middleware; package commands `tenants:migrate`/`tenants:seed`; connection pool sizing; per-tenant backup/restore; avoid cross-tenant queries.
12. [REQ] Filament + MariaDB + multi-tenancy: tenant model in panel config; `->tenant()`/ownership relationship; auto-scope resources; use `filament-shield` for RBAC with `--relationships` tenant flag; `filament-tenancy` or Stancl/Spatie for database-per-tenant; MariaDB `utf8mb4` for emojis; queue per tenant.
13. [REQ] Laravel Nova + MariaDB: Nova uses Eloquent, so `mysql` driver and MariaDB versions apply; define Nova resources and policies; separate Nova policies with `php artisan nova:policy`; use `whenServing` for admin vs app authorization; tenancy via global query scope or tenant-aware resource policies.
14. [REQ] For Laravel/Filament/Nova + MariaDB + multi-tenancy, query `mariadb-lord`, `backend-frameworks-lord`, and the chosen package Context7 ID, then explain the cross-stack rationale.
15. [REQ] Cross-engine answers also query `database-lord` (MySQL/PostgreSQL) and explain the MariaDB-specific rationale.
