---
name: live-source-prover
description: Before citing ANY number/status/metric, re-derives it at the live source and labels it "live @ HH:MM + source" — never repeats stale data
---

> **Auto-Trigger:** Before asserting any count, metric, health, deploy/route status, or completeness
> **Keywords:** "how many", "count", "status", "health", "metric", "number", "is it live", "stale", "where are we", "% complete"
> **Priority:** HIGH
> **Tools:** Bash, Read, Grep
> **Related doctrine:** `rules/learned-corrections.md` (LC-1, mechanized as a skill), `rules/epistemic-standards.md` (separating fact from recommendation).

# live-source-prover — verify LIVE before citing (LC-1)

Deal #1: **treat every datum inherited from a session/doc/snapshot/other agent as SUSPECT until confirmed at the live source.** Materializes LC-1 as a portable skill.

## Contract

**INPUT:** the statement to cite (number/status/metric) + its domain (count/operational/health/deploy/plan) + the project's `sources.yaml`.

**OUTPUT:** the re-derived value + the label `live @ HH:MM · source: <command/endpoint>` attached to the statement.

**EXIT CODES** (the domain's re-derivation command, whether `curl`/`urllib`/`git log`/`find`):

| Exit | Meaning |
|---|---|
| 0 | source answered — value confirmed, may be cited with the label |
| ≠0 | source did not answer/unavailable — do NOT cite the old number; declare "not verified" |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `sources.yaml` (next to this skill) | Reads | re-derivation command per domain |
| endpoint/disk/git of the live source | Reads (read-only) | the real value |

## Process
1. **Before citing** a number/status, identify the domain (file count, operational, service health, deploy/route, plan completeness).
2. **Re-derive LIVE** by running the command from the project's `sources.yaml` (see `sources.example.yaml` next to it):
   - count → `find/grep/ls`; service → `curl`/`urllib` on an endpoint; deploy → curl on a **route EXCLUSIVE to the new build** + build marker (not just the auth gate); plan → `git log --grep` + disk (see `audit_plan.py`).
3. **Paste the output** and **label** the value: `live @ HH:MM · source: <command/endpoint>`.
4. **Freshness TTL:** data older than `verification.stale_source_ttl_days` (default 7) = re-verify, do not repeat.
5. **No `sources.yaml`** defined for that domain → **WARN** ("not verified"); never invent the command or the number.

> Deploy/routing case: confirm that the **backend** switched (route/content exclusive to the new build), not just the process status or the auth gate. Proxy/tunnel chain: confirm EACH hop.

## When NOT to Activate
- When the number was already verified live **in this same reply**.
- Purely illustrative/hypothetical values explicitly marked as such.
- The question is specifically about plan vs reality (checkboxes/deliverables) → use `doc-consolidator-dedup`'s extractor (`audit_plan.py`), which is this same principle applied to plans.

## Executed examples

```console
$ git log --oneline -1
1e96ad3 docs: bring every page in line with the code
```
<!-- executed: 2026-09-24 · exit=0 -->
(domain "plan completeness" — the real commit, not what the previous session said.)

```console
$ python -c "
import urllib.request
with urllib.request.urlopen('http://127.0.0.1:8099/health', timeout=3) as r:
    print(r.status, r.read()[:80])
"
200 b'{"status": "ok", "service": "example-api"}'
```
<!-- executed: 2026-10-30 · exit=0 -->
(domain "service health" — example local server on port 8099; label it:
`live @ 15:03 · source: python -c urllib 127.0.0.1:8099/health`. Replace the port with the
real endpoint from your `sources.yaml`.)

```console
$ python -c "
import urllib.request
try:
    urllib.request.urlopen('http://127.0.0.1:1/health', timeout=2)
except Exception as e:
    print('ERRO:', type(e).__name__)
    raise SystemExit(1)
"
ERRO: URLError
```
<!-- executed: 2026-10-30 · exit=1 -->
(source unavailable — step 5 says declare "not verified", NEVER repeat an old value because the source went down.)

## Proof

```bash
python -c "import subprocess,sys; sys.exit(subprocess.run(['git','log','--oneline','-1'], capture_output=True).returncode)"
```
