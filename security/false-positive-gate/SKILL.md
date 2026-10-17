---
name: false-positive-gate
category: security
description: Use when you have a candidate security finding and before it goes in a comment - restate it as a crossed boundary, prove reachability, impact and a concrete exploit, apply triage dismissals, route out-of-repository facts to needs-validation, keep the effect no stronger than the trace, then the self-refute and verifier passes
tech_stack: Secure review method
source: informed by trailofbits/skills fp-check (CC BY-SA 4.0, ideas only, own wording); anthropics/claude-code-security-review (MIT) false-positive filtering, adapted; cloudflare/security-audit-skill (MIT) candidate gate, source-visibility rule and candidate-verifier checklist, adapted
---
# False-Positive Gate

## Overview

Reviewers — language models especially — are biased toward seeing vulnerabilities and toward rating them higher than they are. A pattern that looks dangerous ("string concatenated into a query", "path from a variable") is a candidate, not a finding. Every false block costs a developer round-trip and teaches the team to skim your comments; that is how the real one gets missed.

**Core principle:** try to kill each finding before you write it. What survives an honest attempt is worth blocking on.

## 1. Restate the Claim

Write it in one sentence, concretely: "An unauthenticated caller can send `name=../../etc/passwd` to `GET /export` and read any file the server can read." Many candidates collapse here — you cannot name who sends what to where, or the sentence is obviously not true once written down.

The sentence must name six things: the **lower-trust principal**, the **input or action** they control, the **control** that was supposed to stop it, the **boundary** it crosses, the **affected principal or resource**, and the **concrete result**. A missing best practice, a guessed deployment behaviour, a generic parser crash or an effect on the attacker alone fills none of the last three.

## 2. Five Conditions — All Must Hold

1. **Reachability.** The attacker controls the data at the source. Trace it: a value from config, an environment variable, a CLI flag, a constant, a server-generated id or an admin-only form is not attacker input for the user-facing threat model.
2. **Real impact.** Reaching the sink produces code execution, privilege escalation, data disclosure or integrity loss for someone other than the attacker. A crash, a 500 or an ugly log line is a bug, not a vulnerability.
3. **A concrete exploit.** You can write the request, the payload or a unit test that would demonstrate it. If you cannot, the confidence is below 0.8.
4. **The bounds hold.** Length limits, type coercion, an integer parse, an enum switch, a regex anchor, a UUID format check — read them; one of them often makes the payload impossible.
5. **No environment control fully blocks it.** A framework default (auto-escaping, parameter binding, CSRF middleware), a gateway rule visible in the repo, a network policy. Read it — "probably the WAF catches it" is not an argument either way.

## 3. Facts Outside the Repository

Proxy and ingress behaviour, CDN cache keys, IdP and broker policy, cloud IAM attachments, browser and OS settings are real controls. Read them when they are in the repository. When they are not and one of them decides the finding, neither dismiss it ("the gateway probably strips it") nor block on it ("nothing strips it"): if the rest of the trace is complete and the claim would be HIGH or CRITICAL, it becomes a non-blocking `Needs validation` note with the exact missing fact (source-visibility-needs-validation). Otherwise drop it.

## 4. Triage Dismissals

Drop the candidate when:

- **No threat model fits.** You cannot complete "an attacker with [capability] can [action] → [impact]".
- **Exploit from the heavens.** It needs a capability that already equals the impact: "an attacker who can edit the server's config file can make it run commands".
- **Not in actual usage.** The vulnerable function has no caller reachable from input (`grep_code` the symbol) — unless this diff adds one.
- **Documented, intended behaviour.** An admin tool that runs admin-supplied SQL; a CLI that reads the path its user gives it.
- **The cure is worse than the disease.** Hardening that would break the feature for a theoretical gain.
- **A CVE number alone.** An advisory against a library is evidence only when the vulnerable function or configuration is actually used here (supply-chain-and-dependency-review).
- **The requester's own authority.** A user, job or agent doing what the requesting user is allowed to do is not a boundary crossing because a model or a queue executes it. It becomes one when attacker-controlled content causes the action and the user did not ask for it (llm-and-agent-security §3).

## 5. Do Not Strengthen the Effect

Report the effect the trace reaches, not the one it would be exciting to reach:

- a crash or panic is not code execution; an out-of-bounds read is not a write;
- ordinary per-request work is not a shared outage, and a slow query is not a denial of service;
- a same-principal action is not privilege gain; reading your own data is not disclosure;
- a reachable sink with a framework default you did not read is not yet a reachable sink.

If the strongest honest sentence is weaker than the category name suggests, the severity follows the sentence.

## 6. Self-Refute Pass (before anything blocks)

Name the **attacker** (who, with what access) and the **victim** (whose data or privilege). Then refute the finding if any is true:

- **Pre-existing.** The vulnerable line has no `+` and the diff adds no new path into it. Off-diff findings must name the enabling `+` or `-` line, or they are not this review's.
- **Already guarded.** A sanitiser, authorization check, type or allowlist on the path stops it. Open it; don't assume it exists and don't assume it works.
- **Harmless sink.** The value lands in a place where its content cannot do damage (a typed integer column, a text node React escapes, an `exec` argv slot after `--`).
- **Attacker == victim.** Self-XSS, a user reading their own data, a developer running their own script on their own machine.

## 7. Worked Examples

**Collapses at the restatement.**

```python
# candidate: "SQL injection in report query"
query = f"SELECT * FROM {REPORT_TABLES[kind]} WHERE org_id = %s"
cur.execute(query, (org_id,))
```

Restated: "an attacker controls `kind` and injects SQL". But `REPORT_TABLES[kind]` raises `KeyError` for anything not in a fixed dict of table names; the user value never reaches the string. No finding.

**Refuted after reading the router.**

```python
# + lines in this diff
@app.get("/files/<name>")
def download(name):
    return send_file(os.path.join(UPLOAD_DIR, name))
```

Candidate: path traversal. But Werkzeug decodes the URL before routing and the default string converter matches no `/`, so neither `../../etc/passwd` nor `..%2F..%2Fetc%2Fpasswd` reaches the handler, and `name=".."` resolves to a directory, which `send_file` refuses. Refuted — you read the converter instead of asserting traversal.

**Survives.**

```python
# + lines in this diff
@app.get("/files/<path:name>")
def download(name):
    return send_file(os.path.join(UPLOAD_DIR, name))
```

Attacker: any visitor — the route has no auth decorator, unlike its siblings. Victim: the server's own files. The `path` converter accepts the decoded slashes of `/files/..%2F..%2Fapp%2Fconfig.py`, `os.path.join` keeps the `..` segments, and `send_file` serves the file. HIGH (CWE-22), confidence 0.9; fix: `send_from_directory(UPLOAD_DIR, name)`, which rejects paths that escape the directory.

## 8. Verifier Pass

Before the comment is written, read each surviving finding as if someone else had written it and you are trying to refute it:

1. Re-open every `file:line` the evidence cites. Does each line say what the finding claims? Is the first entry a real lower-trust entry point, and the last one the claimed sink or effect?
2. Rebuild the strongest control on the path — validation, identity, authorization, normalization, framework default, containment — from the code, not from memory.
3. Check that severity and confidence match only what the trace establishes, and that severity does not exceed the impact.
4. Check the fix: does it enforce the invariant at the last trusted decision point, or does it only move trust (a client-side check, one caller patched while its sibling stays open, an exploit string special-cased)?

A finding that fails any step is corrected or dropped — not softened with "possibly".

## 9. What the Survivor Carries

A finding that passed the gate goes into the comment with: the restated claim as the exploit sentence, the trace (`source file:line → sink file:line`), the confidence you can defend, and the fix. Keep the refuted ones out of the comment entirely — not even as "considered and dismissed".

## Common Mistakes

- Treating "I could not find a sanitiser" as proof there is none — look upstream at the router, the binder, the validator and the type.
- Calling a server-side config value "user input" because it reaches a dangerous function.
- Promoting a finding because the code is ugly or the pattern is famous.
- Blocking on a pre-existing issue the diff merely sits next to.
- Letting a scanner's severity label replace conditions 1–5.
- Dismissing a finding because an unseen gateway "must" block it, or blocking because an unseen gateway "might not".

## Red Flags

- The exploit sentence needs the words "if", "assuming" or "in some configurations" more than once.
- You cannot say what the attacker sends.
- The victim turns out to be the attacker.
- The finding's `file:line` points at a line the diff did not touch and you cannot name the line that did.
