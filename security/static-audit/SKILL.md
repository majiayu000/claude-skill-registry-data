---
name: static-audit
description: "Only when a security or performance audit is asked for (ship-check asks by name, and a release proposes it without running it): a static audit of AI-built code against documented trust boundaries or for N+1 queries, request waterfalls, over-fetching, missing indexes and caching."
argument-hint: "security | performance | both, then <path or area> | <base>..<head> | changes; the scope defaults to the whole repository"
allowed-tools: Read, Grep, Glob, Task, Bash(git status:*), Write(reports/**)
---

# Static audit

**Open the audit's reference before reading any code: it holds the whole procedure.** For security, open `references/security.md`. For performance, open `references/performance.md`. Follow each selected reference as written; this file only chooses between them.

**Run only the audit or audits the request asks for.** Open both references when the user asks for both or the ship check calls for both. If the request gives no audit type, ask which to run.

**Propose static audits during a release and run them only on request.**

**Give the audit type before the optional scope when invoking by name.** Use `security`, `performance` or `both`. For example, `/ai-shipping:static-audit both changes` asks for both audits on the uncommitted working tree.

## How you can tell it worked

Each requested audit has its own report for the requested scope with cited findings and the verification record its procedure calls for.
