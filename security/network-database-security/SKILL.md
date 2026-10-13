---
name: network-database-security
description: >
  Assess reachable database services — PostgreSQL/MySQL/MSSQL/MongoDB/Redis — for unauthenticated
  access, weak/default accounts, over-broad grants, and dangerous features (xp_cmdshell,
  COPY FROM PROGRAM, UDF, Redis file write) that turn a DB login into OS code execution. Load when
  recon shows 3306/5432/1433/6379/27017, leaked app config yields DB creds, or a database review is
  in scope. Signals: 0.0.0.0 bind, unauth Redis PONG, mysql.user host '%', FILE priv,
  secure_file_priv empty, xp_cmdshell.
domain: network
type: methodology
stability: learning
modes: [pentest]
severity: high
mitre: [T1190, T1078]
cwe: [CWE-306, CWE-284]
tools: [nmap, psql, mysql, sqlcmd, redis-cli, mongosh, sqlmap, nuclei]
schema_version: 1
---

# Database security assessment

## When it applies
An authorized engagement has a reachable database instance — surfaced by `network-service-attacks`,
handed over as a review target, or via app credentials recovered from a config dump. Covers
PostgreSQL, MySQL/MariaDB, MSSQL, MongoDB, and Redis. Before touching anything, confirm in
`scope.txt` (see `tradecraft-scope-roe`): which instances, which accounts, and **whether
write/delete/exec is permitted**. On production systems, default to read-only proofs — no
destructive statements unless explicitly allowed.

## Why it works
Databases concentrate the crown jewels yet are routinely deployed as "internal-only": bound to
`0.0.0.0`, default or weak accounts, grants far wider than the app needs, and dangerous features
left enabled. Features like `xp_cmdshell`, `COPY ... FROM PROGRAM`, UDFs, and Redis's writable
config turn a mere database login into OS command execution — so an over-privileged *app* account
is often a quiet path to DBA and then to the host.

## Method
1. **Exposure & transport** — `nmap -sV -p 3306,5432,1433,6379,27017 <range>`; check bind address,
   security groups / firewall rules, and whether TLS is required or enforced. Probe unauthenticated
   access: `redis-cli -h <ip> ping` (`PONG` = unauth — a finding by itself),
   `mongosh --host <ip> --eval 'db.runCommand({listDatabases:1})'`, `mysql -h <ip> -u root`,
   `psql -h <ip> -U postgres`. `nuclei` has templates for known exposures.
2. **Authentication** — default/test accounts and weak passwords; for broad guessing use
   `network-password-spraying` discipline (lockouts apply to MSSQL/MySQL too). Record *from which
   hosts* each credential works — host-restricted grants matter for pivoting.
3. **Authorization & roles** — enumerate who can do what:
   - MySQL: `SELECT user,host FROM mysql.user;` `SHOW GRANTS;` — flag host `'%'`, `FILE`, `SUPER`,
     `GRANT OPTION`.
   - Postgres: `\du`, `SELECT * FROM pg_roles;` — flag superuser, `pg_read/write_server_files`,
     `pg_execute_server_program`.
   - MSSQL: `SELECT * FROM sys.server_principals;` — flag sysadmin membership for app logins.
   Check access control on the sensitive tables, not just server-level roles.
4. **Dangerous configuration** — the login→OS-command bridges:
   - MSSQL: `EXEC sp_configure 'xp_cmdshell';` (also Ole Automation / `sp_OACreate`, CLR).
   - MySQL: `secure_file_priv` empty, `FILE` priv, `SELECT * FROM mysql.func;` for existing UDFs.
   - Postgres: `COPY ... FROM PROGRAM`, `LOAD`, untrusted PL languages.
   - Redis: `CONFIG GET dir` / `CONFIG GET dbfilename` — writable dir enables the classic
     webshell / SSH-key write.
5. **Audit & resilience** — is logging on (MySQL `general_log`, `pgaudit`, SQL Server Audit, MongoDB
   `--auditDestination`)? Who can read backups and snapshots?
6. **Verify exploit chains safely** — where scope allows writes/exec, prove command execution with
   a benign command (`id`, `whoami`) and stop. Where it doesn't, report the chain as a configuration
   risk with the exact grant/feature that enables it. Use `sqlmap` only against an in-scope
   injection point (→ `web-sqli`) — never against the DB blindly.

## Gotchas
- Distinguish **misconfiguration** from **proven exploitable chain** — report both, but only claim
  what you demonstrated.
- Redis reachable only through a web SSRF is a different path — use `web-ssrf-gopher-redis-rce`.
- Cloud-managed RDS/Azure SQL/Cloud SQL: most issues live in the *control plane* (public
  accessibility, security groups, snapshot sharing, IAM) — review via the provider console and the
  `cloud-*` skills instead of hammering the endpoint.
- MSSQL `xp_cmdshell` "disabled" is not safe if the login is sysadmin — enabling it is one command
  (and is logged; note the noise in ROE).
- Hashes pulled from `mysql.user` or captured in transit feed `network-credential-cracking`;
  app-account → DBA privilege growth often comes from reused passwords, not missing patches.
- Dumping customer data to "prove impact" is over-collection — a version string or one
  non-sensitive row proves access.

## Verify success
The report states, per instance: network exposure, which credentials work and at what privilege
level, which dangerous features are reachable from the *app* account, and for every claimed chain a
benign proof (version string, `whoami` output). Every write/exec step maps to something `scope.txt`
allowed, and each recommended fix cites the exact grant or setting to change.

## References
PayloadsAllTheThings (PostgreSQL/MySQL/MSSQL injection & RCE sections); Redis unauthorized-access
write-ups; vendor hardening guides (CIS benchmarks).

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
