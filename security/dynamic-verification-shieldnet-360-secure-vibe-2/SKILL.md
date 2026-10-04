---
id: dynamic-verification
version: "1.2.0"
title: "Verify Findings"
description: "Confirm or refute a vulnerability candidate against a live target with a deterministic probe, respecting authorization and scope. Use when a SAST or LLM review flags a possible injection or SSRF, when triaging a finding before filing a bug or shipping a fix, or when a verification result turns out wrong."
category: detection
severity: high
applies_to:
  - "when a static/SAST or LLM review flags a possible injection or SSRF"
  - "when triaging a finding before opening a bug or shipping a fix"
  - "when an authorized dynamic test against a running app is available"
  - "when a verification result turns out wrong and the PoC or skill needs fixing"
languages: ["*"]
token_budget:
  minimal: 960
  compact: 1350
  full: 3200
related_skills: ["secure-code-review", "ssrf-prevention", "api-security", "security-regression-tests"]
last_updated: "2026-07-09"
sources:
  - "OWASP Web Security Testing Guide (WSTG)"
  - "OWASP Top 10 2021"
  - "PortSwigger Web Security Academy"
---

# Verify Findings

## Rules (for AI agents)

### ALWAYS
- Treat a static-analysis or LLM-review hit as a *candidate*, not a vulnerability,
  until a probe with a deterministic oracle confirms it against a live target.
- Prefer an oracle that proves server-side behaviour over one that inspects the
  response text: out-of-band callbacks (SSRF, blind command injection, XXE) and
  timing deltas (blind SQLi, command injection) catch *blind* bugs that leave no
  trace in the body.
- Re-confirm any timing-based result a second time before trusting it — one slow
  response is noise, a repeatable delay over baseline is signal.
- For reflected oracles (XSS, SSTI), require the dangerous form: XSS confirms only
  when the payload comes back UNESCAPED; SSTI confirms only when the arithmetic is
  EVALUATED (the product appears as a standalone number and the raw expression does
  not).
- Pin file-read oracles (path traversal) to a content signature of a known system
  file (`root:…:0:0:` from `/etc/passwd`, `[fonts]` from `win.ini`), never to a
  generic 200/404.
- Drive the probe yourself with SecureVibe's scope-gated primitives: `http_probe`
  (send one crafted request, read status/headers/body/timing) and `oob_listener`
  (allocate a callback URL, poll for blind hits). They fire only at a target the
  operator authorized — otherwise they return a dry-run plan and send nothing.
- Reach past `http_probe` for what it cannot prove: use your **own headless
  browser** for XSS execution-proof and DOM-based XSS, and your **own shell**
  (see `list_external_tools`) for heavyweight scanners. SecureVibe ships the light
  primitives; the heavy tools are yours.
- When a verdict turns out **wrong** (a "confirmed" that is actually benign, or a
  "refuted" that was real), root-cause *why the oracle misled you* before moving
  on. If it was a target-specific PoC flaw (payload filtered, sink not reached,
  timing threshold, OOB unreachable) → fix the PoC and re-probe. If this skill's
  guidance was itself wrong (bad oracle, mis-mapped class, missing caveat) →
  record it with `propose_skill_update` so the knowledge is fixed, not just this
  run.
- Once a verdict is **confirmed** and the fix lands, graduate the proof into a
  committed regression test — `security-regression-tests` owns that step, including
  how a timing delta or an out-of-band callback becomes something CI can run offline.
  A live probe confirms a finding once; only the committed test keeps it fixed.

### NEVER
- Send an attack payload at a host you are not explicitly authorized to test —
  authorization lives in the operator scope, not in the model's judgement.
- Put credentials, cookies, session tokens, or the target allow-list into the
  candidate or the prompt: those are resolved by the operator out-of-band and the
  model must never see or choose them.
- Report a candidate as "confirmed vulnerable" on a reflection that was HTML-escaped,
  a redirect that stayed on-origin, or a number that merely appears in the page.
- Treat a dry-run plan (nothing was sent) as a refutation — it is "not yet tested".
- Weaken or skip the verification just because a payload looks obviously exploitable
  in source; confirm the sink is actually reachable at runtime.

### KNOWN FALSE POSITIVES
- XSS payload reflected but HTML-escaped → output encoding is working; refuted, not a
  bug (it may still be an encoding lead, not an executable XSS).
- XSS marker **not in the server response** (`http_probe` body) → does NOT refute
  DOM-based XSS: the payload may flow entirely client-side. Read the client JS or
  render in a browser before refuting.
- A single elevated latency on a time-based SQLi/command-injection probe → could be
  GC, cold cache, or network jitter; only a re-confirmed delta counts.
- SSTI product matching as a substring of a longer number (an id, price, timestamp,
  asset path like `/img/6725936.jpg`) → not evaluation; require a standalone number.
- SSRF/XXE with no out-of-band listener available → inconclusive, not refuted; the
  blind oracle could not run.
- Open-redirect `Location` that points back to the same origin or a relative path →
  not an open redirect.

## Context (for humans)

Detection (static analysis, LLM review, dependency data) is good at finding
*candidates* but cannot tell a real, reachable bug from dead code or a sanitized
sink. Dynamic verification closes that gap: send a real probe at a running target
and decide on a deterministic oracle, turning "looks vulnerable" into **confirmed**
or **refuted** with reproducible evidence.

SecureVibe gives you the candidate (class, endpoint, parameter) and the oracle
knowledge below; **you — the coding agent — run the probe** with your own tools (an
HTTP client, an out-of-band listener, a headless browser). The binary never sends
attack traffic: the judgement and the request are yours, so the safety is yours too.

### Two rules you must not break

Active probing *is* attack traffic — treat it like a live pentest:

- **Authorization first.** Only probe a target the user has explicitly authorized
  you to test. If you are not sure it is in scope, ask before firing — never probe
  production, a shared environment, or a third party on your own initiative.
- **Stay in scope, prefer dry-run.** Confine probes to the exact host(s) and
  endpoints the user named; do not pivot, escalate, or exfiltrate. When in doubt,
  build the payload and show the *plan* rather than sending it.

### The primitives you drive

- **`http_probe`** — send one request you crafted (`url`, `method`, `headers`,
  `body`, `follow_redirects`) and read back `status` / `headers` / `body` /
  `elapsed_ms`. It is scope-gated: out of scope or unconfigured ⇒ it returns a
  `plan` with `sent: false` and sends nothing. Covers **response** and **timing**
  oracles.
- **`oob_listener`** — `allocate` returns a callback URL + token; `poll` returns
  the hits it received. Covers **blind / out-of-band** oracles (nothing reflected
  in the body).

### Oracle by class (which primitive, which signal)

- **ssrf** — `oob_listener.allocate`, put the callback URL in the param, `http_probe`
  the endpoint, then `poll`; **confirmed** on a listener hit. (Reflected variant:
  point at a cloud-metadata address and look for an internal signature in the body.)
- **sqli** — `http_probe` a time-based payload (`SLEEP`/`pg_sleep`/`WAITFOR`);
  **confirmed** on a re-confirmed `elapsed_ms` delta over baseline (send a baseline
  request first, then compare).
- **xss (reflected)** — `http_probe` a marker; **candidate-confirmed** when it
  returns **UNESCAPED** in an executable context AND no `Content-Security-Policy`
  header blocks it. Note: `http_probe` proves *reflection*, not *execution*.
- **xss (execution-proof or DOM-based)** — `http_probe` is not enough. For hard
  proof, or DOM XSS (the payload never reaches the server response — it flows
  client-side through `location.hash` → `innerHTML` etc.), use **your own headless
  browser** to render the page and detect the JS actually firing, or **read the
  client-side JS** and trace the source→sink statically. SecureVibe does not ship a
  browser — that capability is yours.
- **redirect** — `http_probe` with `follow_redirects:false` and an attacker URL;
  **confirmed** on a `3xx` whose `Location` leaves for the attacker host (not
  same-origin, not relative).
- **path-traversal** — `http_probe` climbing to `/etc/passwd` / `win.ini` with
  encoding bypasses; **confirmed** on a system-file content signature (`root:…:0:0:`,
  `[fonts]`), never a bare 200/404.
- **command-injection** — blind: `oob_listener` + an out-of-band `curl` callback in
  the payload; else a time-based `sleep` via `http_probe`. **Confirmed** on a
  listener hit or a re-confirmed latency delta.
- **ssti** — `http_probe` template arithmetic in each engine's delimiters
  (`{{7*7}}`, `${7*7}`, `<%= 7*7 %>`); **confirmed** when the body shows the product
  as a standalone number and the raw expression is gone.
- **xxe** — `oob_listener` + an XML body whose external entity points at the
  callback URL; `http_probe` it, then `poll`; **confirmed** on a listener hit.

A confirmed verdict is reproducible evidence to attach to the fix; a refuted verdict
lets you drop a candidate without spending review time on a non-issue.

### When a verification is wrong (close the loop)

A verdict can be wrong: a "confirmed" that later proves benign, or a "refuted"
that was actually exploitable. When that happens, diagnose *why the oracle misled
you* before moving on, then route the fix by its blast radius:

- **A target-specific PoC flaw** — the payload was filtered, never reached the
  sink, the timing threshold was too low, or the OOB listener was unreachable.
  Ephemeral: fix the payload/probe and re-run `http_probe` / `oob_listener`.
  Nothing to record — it only concerned this one target.
- **A flaw in this skill's guidance** — the oracle for the class was wrong, the
  class was mis-mapped (an "SSRF" that was really an open redirect), or a caveat
  was missing (reflection proved, but not execution). Durable: record it with
  `propose_skill_update(skill_id: "dynamic-verification", kind: wrong|missing,
  claim, evidence)`, where the evidence is the PoC, the observed result, and the
  root cause. A maintainer reviews and re-signs; the skill improves for next time.

Rule of thumb: a bad payload for *this* target → fix the PoC; a bad *method* for
*this class* → propose a skill update. And when a verdict is finally **confirmed**,
its PoC graduates into a committed regression test ([[security-regression-tests]])
so the fix stays verified in CI — no PoC is wasted.

## References

- `references/oracles-by-class.md` — which probe proves each vulnerability class, and the three signals that look like proof but are not
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/).
- [OWASP Top 10 2021](https://owasp.org/Top10/).
- [PortSwigger Web Security Academy](https://portswigger.net/web-security).
- Related skills: `secure-code-review`, `ssrf-prevention`, `api-security`.
