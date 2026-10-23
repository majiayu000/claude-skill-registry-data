---
name: security-hardening
description: Use when writing code that crosses a trust boundary (user input reaching a query or a template, a file upload, a new endpoint, an outbound call with a user-supplied target), a response header, a third-party resource, a production setting, or a browser or mobile client. The writing counterpart to the seraph agent.
---

# security-hardening

Step 6 of the pipeline (`WORKFLOW.md`). The distinction that keeps this block from duplicating
others: `seraph` **audits** a repo after the fact, `auth-session-conventions` owns **auth**, and this
block is what you apply **while writing** the code, on every other trust boundary. Every rule below
holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A).

A trust boundary is any point where data you don't control meets something that acts on it: a query,
a template, a filesystem path, a shell command, an HTTP call, a deserialiser.

**An applied override is recorded, not hidden.** Where an org catalogue or a platform policy governs a rule
here, write what it requires, and leave one short neutral trace addressed to whoever can decide (a line in the
PR description, the task summary or an ADR): which rule was overridden, by what, and that it is a resolved
case. Never phrase it as "a conflict between mentis and the house rules" to a non-technical stakeholder — that
framing reads as broken even when the case is a normal, resolved one, and has already caused a real project to
get abandoned and restarted over nothing. Raise one specific, named question to the decider only when no rule
anywhere actually resolves the case.

## When
As soon as a diff has user-controlled data reaching one of those, adds a file upload, adds an
endpoint, sets a response header or a cookie, embeds a third-party resource, changes production
configuration, or brings in a new dependency. Not as a generic pass over untouched code: that's `seraph`'s
job, on demand.

## Steps

**Read only the sections the boundary actually is.** The rules live one file per section under
`references/`; §1 and §2 are the two halves of a data path, §3 is any new entry point, §4 is uploads,
secrets and dependencies, §5 is what you owe before calling it done, and §6 to §8 are what the browser,
the production environment and the client enforce or expose, §9 is cryptography, §10 the level a review is held to, §11 services exposed beyond their host, §12 the audit of an AI-generated app.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Input: validate at the edge, on a whitelist | data you don't control enters | [`01-input.md`](./references/01-input.md) |
| 2 | Output: escaping depends on the destination | a value reaches a query, template, shell, path or outbound call | [`02-output.md`](./references/02-output.md) |
| 3 | Access control on every new route | an endpoint, consumer, job or webhook is added or changed | [`03-access-control.md`](./references/03-access-control.md) |
| 4 | Files, secrets and dependencies | an upload, a secret, or a new dependency | [`04-files-secrets-deps.md`](./references/04-files-secrets-deps.md) |
| 5 | Verification | before claiming the boundary is done | [`05-verification.md`](./references/05-verification.md) |
| 6 | Browser and transport: policy headers, framing, referrer, integrity, opener, mixed content, cookies, CORS | a page, a header, a cookie, a third-party resource or a cross-window message | [`06-browser-and-transport.md`](./references/06-browser-and-transport.md) |
| 7 | Production configuration and abuse: debug, startup validation, rate limits, error detail, audit | environment config, a public or authentication endpoint, a dependency gate | [`07-production-and-abuse.md`](./references/07-production-and-abuse.md) |
| 8 | Client templates and mobile: URL, component, style and event vectors; web views, deep links, binaries | data bound into a front-end template, a client bundle, a mobile app | [`08-client-and-mobile.md`](./references/08-client-and-mobile.md) |
| 9 | Applied cryptography: no home-made primitives, randomness, constant-time compare, nonces, password hashing, keys | code encrypts, signs, hashes a secret, generates a token or a key | [`09-cryptography.md`](./references/09-cryptography.md) |
| 10 | Assurance level: declared once, reviewed against | a spec or a security review of an application is written | [`10-assurance-levels.md`](./references/10-assurance-levels.md) |
| 11 | Exposed services: probing the right route, placeholder credentials, bind address, a control's real reach | a gateway, proxy or tool server is exposed, or someone asks whether a service is protected | [`11-exposed-services.md`](./references/11-exposed-services.md) |
| 12 | AI-generated or scaffolded apps: secrets reachable by the client, access rules that only look on, client-editable authorisation, model calls rated by position, honest rescan | the audit target was built mostly by an assistant or a scaffold | [`12-ai-generated-app-audit.md`](./references/12-ai-generated-app-audit.md) |

## Output / checkpoint
For each boundary the diff introduces: where validation happens, what the whitelist is, how output is
escaped, and the authorisation applied. The hostile-value and wrong-user replays observed, with
evidence, not reasoned about (§5.3).

## Guardrails
- **Never weaken a check to make something work** (§1.5). If a guard blocks a legitimate case, the
  whitelist is wrong: widen it deliberately, don't remove it.
- **Never disable escaping to fix a display bug** (§2.12). Fix the data or sanitise it.
- **Never build a query, a command or a path by concatenation** (§2.1, §2.3, §2.7).
- **Never ship an entry point with no authorisation declaration**, and never rely on the habit rather
  than a default-deny (§3.1, §3.5).
- Never test an injection against a shared or production environment: hostile-value replays belong in
  local or preview environments (§5.8 — that boundary is `seraph`'s rule too, and it applies to writing
  code just as much as to auditing it).
- Never loosen a protection of §6 to make a third-party widget load: allow that one origin, narrowly,
  and record why.
- Scope: this block covers what the application code and its configuration ask of the browser, the
  transport and the client (§6 to §8). Operating the platform (certificate lifecycle and the
  strict-transport rollout in `devops-conventions` §5, WAF, network policy, IdP configuration) is infra
  reality and stays outside this repo.

## Origin
A rewrite of a market generalist catalogue's `security-and-hardening` idea, against OWASP (Top 10,
ASVS) and OWASP's escaping cheat sheets; §6 to §8 added 2026-10-02 from the primary web, mobile and
OWASP specifications. The full provenance, the split with `seraph` and
`auth-session-conventions`, the 2026-08-10 OWASP coverage check and the refresh log are in
[`references/origin.md`](./references/origin.md).
