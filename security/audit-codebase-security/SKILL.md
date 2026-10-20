---
name: audit-codebase-security
description: >-
  Load this skill when a whole codebase, not one diff, needs a security audit: attack surface, entry
  points traced to sinks, each exploitable finding with severity and fix. Trigger on "security
  audit", "is this codebase secure". Not for pending changes (use the built-in /security-review).
argument-hint: "[path or service]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Needs git for the secrets search through history. The dependency check needs the ecosystem's
  audit tool (pip-audit, npm audit, bun audit) and network access. Without them the audit runs and
  lists those checks as not run.
license: Apache-2.0
---

# Audit Codebase Security

Audit everything already in the codebase for weaknesses an attacker can reach, and report each
one as the attack it enables. Claude Code's built-in `/security-review` checks pending changes
only, and most vulnerabilities are in code that was merged long ago. Done means every entry point
is traced, every category below is checked or listed as skipped with a reason, and the report is
saved.

## Procedure

1. **Map the attack surface before reading for bugs.** List the entry points (HTTP routes, CLI
   arguments, queue consumers, webhooks, file uploads and parsers, jobs that read external data),
   the trust boundaries where outside data enters, the assets (credentials, personal data, money,
   admin actions), and the attackers who can reach each entry point (anonymous, signed-in user,
   another tenant, an operator). Severity only means something against an asset and an attacker
   who can reach it.
2. **Trace each entry point to its sinks**: queries, shell commands, file paths, HTML and
   templates, outbound requests, deserializers, `eval`. Request every search and file read that does not depend on another's result in the same turn. Check each category, and name the ones that
   do not apply:

   | Category         | Look for                                                                                                            |
   | ---------------- | ------------------------------------------------------------------------------------------------------------------- |
   | Access control   | A route with no auth, an object fetched by id with no owner check, a role checked only in the UI, tenant from input |
   | Injection        | SQL or shell built from strings, a file path from input with no containment check, unescaped HTML                   |
   | Secrets          | Credentials in code, config, tests, or git history (`git log -p -S '<pattern>'`), tokens written to logs            |
   | Outbound         | A server-side fetch of a URL from input (SSRF), an open redirect                                                    |
   | Parsing          | Unsafe deserialization (`pickle`, `yaml.load`), XML external entities, archive path traversal, unbounded uploads    |
   | Crypto, sessions | Fast hashes for passwords, `random` for tokens, unverified JWTs, cookies without `HttpOnly`, `Secure`, `SameSite`   |
   | Configuration    | Debug on in production config, CORS `*` with credentials, stack traces in error responses, default credentials      |
   | Resource limits  | No rate limit on login or costly endpoints, a regex with catastrophic backtracking on input                         |
   | Dependencies     | A pinned version with a published advisory                                                                          |

3. **Check dependencies only with consent to the network.** The audit tools send the dependency
   list to an advisory database, which is sending content to an external service. Run them when
   the user asked for the dependency check or network use is already authorized. Otherwise put the
   exact command under Not checked.
4. **Fan out on a large surface.** With more than one service, or more than about fifty entry
   points, write the surface map to the report first, then dispatch background subagents in
   parallel, one per group of categories, each with the report path and its categories. Merge by
   `path:line`, and re-read every quoted line before it becomes a finding.
5. **Confirm each finding** by quoting both ends: where the attacker's input enters and the sink
   it reaches, with every step between that could stop it. Rate **severity** (critical, high,
   medium, low) from impact and reachability, and **confidence**: confirmed (traced end to end, or
   proven by a local test) or likely. A finding you cannot trace goes under Possible, not in the
   table.
6. **Fix only on request.** When asked, fix confirmed critical and high findings first. Each fix
   lands with a test that fails before it and passes after. Leave the rest reported.

## Rules

- **Never copy a secret's value** into the report, a test, or the reply. Cite `path:line` and the
  kind of secret. Removing a committed secret from the code does not remove it from history, so
  the fix is rotating it, which is the owner's call: report it, never rotate it.
- **Prove locally, never live.** No request, scan, or exploit against a deployed system or a host
  the user does not run locally. A test or a local dev server is the proof.
- **Severity follows reachability.** An injection in a public route outranks the same injection in
  a script only an operator runs, so name the attacker in every finding.
- Save the report under `.agents_workspace/`, never in a committed path: a committed audit of an
  unfixed hole publishes it.

## Output

Save to `.agents_workspace/security-audit/SECURITY_AUDIT-<YYYY-MM-DD>.md`, and reply with the
counts by severity and the critical and high rows.

```markdown
# Security audit: <repo> at <short commit>, <YYYY-MM-DD>

## Attack surface

Entry points, trust boundaries, assets, and attackers from step 1.

## Findings

| #   | Severity | Confidence | Category       | Attacker  | Location               | Attack                                    | Fix                                     |
| --- | -------- | ---------- | -------------- | --------- | ---------------------- | ----------------------------------------- | --------------------------------------- |
| 1   | high     | confirmed  | Access control | signed-in | `app/api/orders.py:52` | GET /orders/{id} returns any user's order | Filter by `owner_id == current_user.id` |

## Possible

Leads that could not be traced end to end, each with what would settle it.

## Not checked

Each category or check not run, with the reason and the command that would run it.
```
