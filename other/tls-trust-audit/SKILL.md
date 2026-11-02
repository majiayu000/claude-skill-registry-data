---
name: tls-trust-audit
description: Use when a CA is compromised or TLS trust is in doubt.
version: 1.0.0
author: Vesper
license: MIT
tags: [security, tls, certificates, ca-compromise, trust-store]
---

# TLS Trust Store Audit

When a certificate authority is compromised, revoked, or suspected, the question
"am I affected?" **cannot be answered once per machine.** Every TLS client keeps
its own trust store, and the OS being patched does not patch them.

## When to Use

- a CA compromise or mass-revocation event is announced
- "do I trust this certificate / is this machine exposed?"
- a connection is failing with an unexpected certificate error and you need to
  know which store is doing the rejecting
- auditing a machine — ours, Tyler's, or someone else's — for public discussion

## The core rule

**Test each client separately, and prove the test is capable of succeeding.**

An OS-level patch tells you almost nothing. In practice a machine can pass a
browser check, pass `curl`, and still be fully exposed through Python or Node.

## Procedure

### 1. Get the authoritative test hosts

Public compromise trackers publish purpose-built hosts that serve the revoked
chain, plus a control expectation. For the eMudhra incident the tracker is
`https://emudhra.we-have-a-problem.com/` (browser check + `chains.zip` +
`impacted-intermediates.json`). Prefer the tracker run by the reporting
community over news coverage — it carries the actual fingerprints and the
per-distro patch versions.

### 2. Always run a control alongside

```bash
curl -sS -o /dev/null https://revoked-test-host/ ; echo "exit $?"
curl -sS -o /dev/null https://example.com/      ; echo "exit $?"
```

**Exit-code reading:**

| Code | Meaning |
|---|---|
| **0** | Connected — the client trusts it (**BAD**, if it's a revoked host) |
| **35** | SSL connect error — handshake rejected (**GOOD**) |
| **60** | Peer certificate cannot be authenticated — rejected (**GOOD**) |
| anything, with the control also failing | Network/DNS problem, not a TLS verdict — retest |

Without the control you cannot distinguish "rejected the cert" from "couldn't
reach the host."

### 2b. Map which root programs actually include the compromised root

Headlines describe the worst case for the whole internet; the tracker describes
your machine. Before testing anything, read the tracker's root metadata (e.g.
`roots.json`) — it reports each root's inclusion status per program
(Apple / Chrome / Microsoft / Mozilla).

**A compromised root absent from a program cannot be exploited against that
program's clients, even before revocation.** That is what separates *structural
safety* from *prompt patching*, and it sets the priority order:

- root in **no** browser program → those browsers were never exposed; their
  revocation was belt-and-braces, not the save
- root in **Microsoft's store only** → Windows was the actual exposure surface,
  and the OS trust-list update is the fix that mattered
- root **removed** from one program, still present in another → clients on the
  same network have genuinely different risk

State which clients were structurally safe versus which needed patching. It
stops a "billions of devices" framing from deciding where you spend the effort.

### 3. Walk every client, not every machine

| Client | Its own store? | How to test |
|---|---|---|
| OS / Schannel / browsers | OS store + fast revocation | browser check page |
| `curl` | system CA bundle (usually) | plain curl test |
| **Python `certifi`** | **yes — per venv** | `ssl.create_default_context(cafile=certifi.where())` |
| **Node.js** | **yes — compiled in** | `https.get(...)`; fix with `--use-openssl-ca` |
| **Git (Windows)** | **yes — its own `ca-bundle.crt`** | `curl --cacert <git bundle>` |
| Java / .NET / Go | own truststore or system | test via the runtime |
| Docker images | **yes — baked into the image** | test inside the container |

**Python, per venv:**

```python
import ssl, urllib.request, certifi
ctx = ssl.create_default_context(cafile=certifi.where())
try:
    urllib.request.urlopen("https://revoked-test-host/", timeout=15, context=ctx)
    print("CONNECTED — vulnerable")
except Exception as e:
    print("REJECTED", type(e).__name__)
```

**Node:**

```bash
node -e 'require("https").get({host:"revoked-test-host",path:"/"},
  r=>console.log("CONNECTED",r.statusCode))
  .on("error",e=>console.log("REJECTED",e.code))'
```

### 4. Test a specific bundle with `--cacert`

To know whether one particular trust file trusts a host — rather than whether the
system does — point curl at it directly:

```bash
curl --cacert /path/to/ca-bundle.crt -sS -o /dev/null https://revoked-test-host/
echo "exit $?"
```

This is the only honest way to audit a client that ships its own bundle (Git,
Node, a container). **Do not infer from grep.** A bundle containing the *root*
name does not prove the client accepts the *intermediate* — a grep hit is a lead,
not a verdict. Test the chain.

### 5. Apply fixes per layer

- **OS:** package update (`ca-certificates`, `libnss3` on Debian/Ubuntu).
- **Python:** `pip install -U 'certifi>=<patched>'`, or with uv:
  `uv pip install --python <venv>/bin/python 'certifi>=<patched>'`. **Per venv.**
- **Node:** `--use-openssl-ca` (defer to the OS store), or upgrade the runtime so
  the bundled store refreshes. Verify the OS store is patched first.
- **Git for Windows:** `winget upgrade --id Git.Git`, then `--cacert` test it.
- **Containers:** pull current tags and rebuild; a host update does nothing for
  an image's baked-in bundle.
- **Offline / auto-update-disabled hosts:** most trackers publish a local
  blocklist script that imports the revoked intermediates into the OS
  "Disallowed"/untrusted store. Never apply one to an org-managed device without
  checking with IT.

## Pitfalls

- **A browser passing proves nothing about the rest of the machine.** Browsers
  use fast revocation (CRLSets / OneCRL / CRLite) and often enforce Certificate
  Transparency, so they were never the exposed layer.
- **A grep hit in a CA bundle is not a finding.** Report only what a chain test
  takes; otherwise you will alarm someone about a harmless string match.
- **A package already at the fixed version looks unpatched if you expect a bump
  dated after the incident.** Compare against the tracker's published fixed
  versions, string for string — an "no update available" conclusion is usually a
  version string you did not recognise as the fix.
- **`pip` may not exist in the venv.** uv-managed environments reject
  `python -m pip`; use `uv pip install --python <interpreter>`.
- **`curl` in PowerShell resolves to an alias, not the binary.** Call `curl.exe`
  explicitly, and read `$LASTEXITCODE` — the exit code is the result, not stdout.
- **Don't report a vulnerability without the fix in the same message.** The
  useful output of an audit is a per-client table with before/after and a
  verified rejection, not a list of scary names.
- **Update the check itself after fixing.** Re-run the same test and show the
  flip (CONNECTED → REJECTED). An unverified fix is the same as no fix.
- **When a report about a compromise reaches you, verify its numbers against the
  primary source before passing it on.** A competent-looking incident report can
  carry several wrong details that survive because they sound plausible. Check
  each: the actual key sizes (a "1 byte" claim is usually a garbled secondary
  summary — read the original reporting), the patched-version strings (compare
  against the tracker's fixed-version list), whether the affected tool is really
  in scope (OpenSSL does *not* ship a root store — it reads the OS bundle, so
  "update OpenSSL" is usually a category error), and the root certificate names
  (read them from `roots.json`, never from memory). Produce a short addendum that
  keeps what was right and corrects what was wrong — an addendum is easier to
  hand to the author than a rewrite that says the whole thing was broken.

## Related

- `windows-maintenance` — running these checks on a remote Windows box over SSH
  (use `-EncodedCommand`, not nested `-Command` quoting).
- `hermes-ops` — the VM's own runtime stack (Node tarball location, Hermes venvs).

*-every store, tested, with the control alongside-*
