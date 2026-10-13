---
name: python-dependency-vetting
description: >
  Use this when adding a new entry to pyproject.toml dependencies, bumping a major
  version of an existing dep, reviewing TPRD §10 dependency declarations, or
  rendering an sdk-dep-vet-devil-python verdict at H6. Covers the license
  allowlist, pip-audit + safety + osv-scanner vulnerability tiers, package size /
  last-release-age / transitive-count / PyPI-adoption / GitHub-maintenance
  buckets, Sigstore (PEP 740) attestation checks, typosquatting Levenshtein
  scan, native-code provenance for wheels, and ACCEPT / CONDITIONAL / REJECT /
  INCOMPLETE aggregate verdict logic.
  Triggers: pip-audit, safety, license, CVE, Trove classifier, pip install, PyPI, Sigstore, typosquat, py.typed, manylinux, abi3, dependencies.
cross_language_ok: true
---

# python-dependency-vetting (v1.1.0)

## Rationale

Every Python dependency added to an SDK is a transitive dependency for every consumer of the SDK. License incompatibility, CVEs in deep transitives, abandoned upstreams, typosquatting attacks — these failure modes scale: one bad dep affects every downstream user. The Python pack's vetting discipline forces a per-dep verdict (ACCEPT / CONDITIONAL / REJECT) at design time before the dep ships in `pyproject.toml`.

This skill is cited by `sdk-dep-vet-devil-python` (the agent that renders verdicts), `sdk-convention-devil-python` (C-15 dependency declaration discipline), `sdk-security-devil` (cross-checks), `sdk-packaging-devil-python` (P-7 dep placement), and `python-sdk-config-pattern` (when Config inherits from a vetted base like pydantic).

## Activation signals

- Adding a new entry to `pyproject.toml [project] dependencies`.
- Bumping a major version of an existing dep.
- TPRD §10 declares a dep that needs review.
- `sdk-dep-vet-devil-python` is gating H6.
- A consumer asks "why does the SDK pull library X?"
- Reviewing whether a "small enough" pure-Python implementation can replace a dep.

## License allowlist

Acceptable (ACCEPT, no review needed):
- `MIT`
- `Apache-2.0`
- `BSD-3-Clause` / `BSD-2-Clause`
- `ISC`
- `0BSD`
- `MPL-2.0`
- `Python-2.0` (Python Software Foundation License)
- `Unlicense`
- `CC0-1.0`

Conditional (requires user OK at H6 — document the obligation):
- `LGPL-2.1-or-later` / `LGPL-3.0-or-later` — pip is dynamic linking, but document the obligation per LGPL.
- `EUPL-1.2` — compatible with most permissive licenses but requires LICENSE distribution.
- Dual-licensed where one option is in the allowlist (declare which option you're consuming under).

Reject (REJECT — must drop or substitute):
- `GPL-2.0-or-later` / `GPL-3.0-or-later` — copyleft incompatible with permissive SDK posture.
- `AGPL-3.0-or-later` — network-AGPL kicks in for SDK servers; even more aggressive than GPL.
- `SSPL` — non-OSI; effectively proprietary.
- Proprietary / commercial / "all rights reserved".
- Missing license metadata (`UNKNOWN` in `pip show`).

## License resolution order

1. `pip show <pkg>` — reads METADATA `License` and `License-Expression` (PEP 639) fields.
2. PyPI JSON API: `GET https://pypi.org/pypi/<pkg>/json` → `info.license` and `info.classifiers` (search for `License :: OSI Approved :: ...`).
3. Source repository's `LICENSE` / `COPYING` / `LICENCE` / `LICENSE.txt` file (best-effort if METADATA empty).
4. PyPI `info.classifiers` Trove license classifier.

If sources DISAGREE (METADATA says MIT but classifier says Apache-2.0), CONDITIONAL with a note. The package author should harmonize; the SDK shouldn't accept ambiguous licensing.

## Vulnerability scanning

### Tier 1: pip-audit (preferred)

```bash
pip-audit --requirement <(echo "<pkg>==<ver>") --format=json --vulnerability-service=osv > audit.json
```

`pip-audit` queries the PyPI Advisory Database (and falls back to OSV). Severity mapping:

| pip-audit severity | Verdict |
|--------------------|---------|
| CRITICAL / HIGH | REJECT |
| MEDIUM | CONDITIONAL (may ACCEPT if patched version cannot be reached due to constraints; document) |
| LOW | ACCEPT (note in report) |

Always include `--vulnerability-service=osv` as a secondary cross-check; OSV's database is broader.

### Tier 2: safety

```bash
safety check --full-report --json --file=<(echo "<pkg>==<ver>") > safety.json
```

`safety` checks the `pyup.io` database. It overlaps with pip-audit but occasionally surfaces CVEs the PyUp team curates that haven't landed in OSV yet. Cross-check — any disclosure in safety NOT in pip-audit is at minimum CONDITIONAL.

### Tier 3 (optional): osv-scanner

```bash
osv-scanner --lockfile=poetry.lock          # OR uv.lock OR requirements.lock
```

`osv-scanner` traverses the lock file recursively, surfacing transitive vulnerabilities. Run on the lock file (not pyproject.toml) so transitives are included.

## Per-dep checks

For every dep proposed in `pyproject.toml`, run the full check set:

### V-1. License (allowlist above)

### V-2. Vulnerability scan (pip-audit + safety + optionally osv-scanner)

### V-3. Package size

```bash
pip download "<pkg>==<ver>" --no-deps --dest /tmp/vet/ --quiet
du -sk /tmp/vet/*.whl    # OR *.tar.gz if no wheel
```

Buckets:
- `<5 MB` — ACCEPT.
- `5–20 MB` — CONDITIONAL (justify; e.g., bundled native or large data files).
- `>20 MB` — REJECT unless TPRD §10 waives (example: PyTorch, CUDA toolkits — legitimate but rare).

If only sdist (no wheel): downgrade verdict by one tier — sdist requires the consumer to compile, increasing supply-chain attack surface.

### V-4. Last-release age

```bash
LATEST_UPLOAD=$(curl -s "https://pypi.org/pypi/<pkg>/json" \
                | jq -r '.releases | to_entries | sort_by(.value[0].upload_time) | last | .value[0].upload_time')
```

| Age | Verdict |
|-----|---------|
| `<6 months` | ACCEPT (active maintenance) |
| `6–18 months` | ACCEPT with note (fine for stable libs, suspicious for evolving libs) |
| `18–36 months` | CONDITIONAL — abandonware risk; check fork signals |
| `>36 months` | REJECT unless intentionally frozen (RFC implementations) — TPRD §10 must waive |

Cross-check `requires_python` from PyPI metadata — must include the SDK's Python floor (`>=3.12` for the Python pack default).

### V-5. Transitive dependency count

```bash
pip download "<pkg>==<ver>" --dest /tmp/vet-t/ --quiet
ls /tmp/vet-t/*.whl | wc -l    # excludes the dep itself
```

| Transitives | Verdict |
|-------------|---------|
| `<10` | ACCEPT |
| `10–30` | CONDITIONAL — document each first-level transitive |
| `>30` | REJECT unless TPRD waives (web frameworks like FastAPI legitimately pull 30+) |

The point is awareness — high transitive count IS the supply-chain attack surface. SDKs are sticky upstream of consumers; the consumer can't drop our transitive without dropping us.

### V-6. PyPI adoption

```bash
# Best-effort via pypistats.org JSON API
curl -s "https://pypistats.org/api/packages/<pkg>/recent?period=month" | jq .
```

| Downloads/month | Verdict |
|-----------------|---------|
| `>10 k` | healthy |
| `1 k – 10 k` | ACCEPT with note |
| `100 – 1 k` | CONDITIONAL `low-adoption` (SDK becomes the primary stress-tester) |
| `<100` | REJECT `negligible-adoption` unless TPRD waives |

### V-7. GitHub maintenance signals

Best-effort lookup via the source URL declared in PyPI metadata:

- Repository archived flag → REJECT.
- Last commit `>12 months` ago → CONDITIONAL.
- Open-issue / closed-issue ratio `>0.5` → CONDITIONAL.
- No source repo (PyPI-only, "anonymous" package) → CONDITIONAL `source-not-discoverable`.
- < 100 stars on a package handling crypto / auth / serialization → CONDITIONAL (security-critical code shouldn't have niche maintenance).

### V-8. Sigstore attestation (PEP 740)

PEP 740 attestations for PyPI uploads are increasingly common. Verify via:

```bash
python -m sigstore verify identity \
    --bundle <pkg>-<ver>.whl.sigstore \
    --cert-identity "<expected-identity>" \
    --cert-oidc-issuer "https://accounts.google.com" \
    <pkg>-<ver>.whl
```

Attestation present + verified → ACCEPT signal (not required for ACCEPT, but absence is a CONDITIONAL note for security-critical deps). Attestation present but verification fails → REJECT.

The Python ecosystem's Sigstore adoption is partial as of 2026; most popular packages (httpx, aiohttp, pydantic) have started shipping attestations.

### V-9. Typosquatting check

```bash
# Compare against the top-1000 PyPI list (refresh monthly)
LEVENSHTEIN_DIST=$(python -c "
import Levenshtein, sys, json
top = json.load(open('top-1000-pypi.json'))
target = sys.argv[1]
for popular in top:
    d = Levenshtein.distance(target, popular)
    if 0 < d <= 2:
        print(d, popular)
        sys.exit(0)
" "<pkg>")
```

If the dep's name is ≤ 2 Levenshtein distance from a popular package AND first release `<90 days` ago → REJECT typosquat. Common attacks: `requst` (vs `requests`), `urlllib3`, `numppy`, `python-dateuitl`.

### V-10. Native-code provenance

If the wheel contains `*.so` / `*.pyd` / `*.dylib`:

- Confirm wheels exist for the platforms the SDK supports (manylinux2014 / manylinux_2_28 + macOS arm64 + macOS x86_64 + Windows AMD64).
- Verify the build CI is the upstream's official one (cibuildwheel / GitHub Actions in the project's repo). Random PyPI-only binaries are CONDITIONAL.
- Pure-Python alternative existing? Note in report; CONDITIONAL recommends pure-Python where viable.

If only sdist ships and the package contains a C extension: REJECT unless build is reproducible from sdist on a clean Python 3.12 env without external system deps.

### V-11. Python version compatibility

- `requires-python` floor must be `<= 3.12` (the SDK's floor).
- If the dep declares an upper bound (`<3.13`), confirm the SDK's intended max Python is supported.
- ABI tags: pure-Python (`py3-none-any`) preferred; ABI3-stable (`cp312-abi3-...`) acceptable; per-minor wheels (`cp312-cp312-...`) acceptable but require a regenerate cadence.

### V-12. Library-API-shape verification (added v1.1.0)

**Added in v1.1.0** in response to the `motadata-nats-v1` run's B1-B4 root cause: `nats-py>=2.7.0,<3` was vetted clean on V-1..V-11 but the kwargs/API surface drifted between 2.7 (TPRD-cited floor) and 2.14 (env-installed actual). The SDK code targeted 2.7-style kwargs (`replicas`, `allow_rollup`, `compression=...`) which fail at runtime against 2.14 (`num_replicas`, `allow_rollup_hdrs`, no `compression` kwarg). License/CVE checks all PASS — but the API SHAPE is not part of those checks.

**The check**: for each runtime dep with a declared version range, materialize a venv pinning the **highest pinnable minor in the range** (i.e. the minor a fresh `pip install` would resolve to). For each class/function the SDK code references via the design's `api-stub`, verify via reflection that the kwargs the SDK passes are accepted by that class's `__init__` / function signature.

```bash
# Resolve the actual minor the dep range would install
HIGHEST=$(python -c "
import json, urllib.request, packaging.specifiers as ps, packaging.version as pv
url = 'https://pypi.org/pypi/<pkg>/json'
data = json.loads(urllib.request.urlopen(url).read())
spec = ps.SpecifierSet('<range-from-pyproject.toml>')
versions = sorted([pv.parse(v) for v in data['releases'] if spec.contains(v)], reverse=True)
print(versions[0])
")

# Materialize a scratch venv at that pin
python -m venv /tmp/dep-vet-shape && /tmp/dep-vet-shape/bin/pip install "<pkg>==$HIGHEST"

# For each cited class/function in design/api-stub, reflect:
/tmp/dep-vet-shape/bin/python -c "
import inspect
from <pkg>.<module> import <cited_class>
sig = inspect.signature(<cited_class>.__init__)
print(list(sig.parameters.keys()))
" > /tmp/dep-vet-shape/<cited_class>-sig.txt
```

Compare the reflected kwarg list against the SDK's call sites in design `api-stub.py` (or design's `algorithms.md` referenced kwargs). Any kwarg the SDK passes that does NOT appear in the resolved-minor's signature: surface as **CONDITIONAL — kwarg-rename-required** with a hint specifying the SDK location and the resolved-minor's actual kwarg name (look for the closest match in the resolved signature).

| Outcome | Verdict | Action |
|---|---|---|
| All SDK call-site kwargs match resolved-minor signature | ACCEPT | nothing further |
| 1+ kwarg missing in resolved-minor; close-match available | CONDITIONAL — kwarg-rename-required | suggest renames in dep-vet report; design lead must update api-stub OR pin TPRD range tighter |
| 1+ kwarg missing; no close-match (kwarg removed entirely) | CONDITIONAL — kwarg-removed-required | impl must drop the kwarg; field can stay on the SDK's own dataclass for forward-compat, just not threaded into the call |
| `pip install` cannot resolve the range | INCOMPLETE | network or yank issue; never auto-PROMOTE to ACCEPT |

**Integration into D-DEP wave**: this check is REQUIRED at H6 for any dep whose runtime API surface is referenced from `design/api-stub.py`. Skip ONLY for tooling-only deps (pytest, ruff, mypy, build) where the SDK's own code never imports the lib.

**Cost**: ~30 seconds per dep (venv create + pip install + 1-3 reflect calls). Catches an entire class of "library-evolved-since-TPRD-was-authored" bug at design-time, eliminating the impl→test→re-impl loop.

**Cross-reference**: paired with `python-mock-strategy` v1.1.0 strict-signature-mocking guidance — the dep-vet skill is the FIRST line of defense (catches at design); the mock-strategy skill is the SECOND line (catches at unit test if dep-vet was skipped).

## Aggregate verdict logic

| Per-dep verdicts | Aggregate |
|------------------|-----------|
| All ACCEPT | ACCEPT |
| Any CONDITIONAL, no REJECT | CONDITIONAL — H6 surfaces |
| Any REJECT | REJECT — design lead must drop or substitute |
| Any INCOMPLETE (network failure, tool unavailable) | INCOMPLETE — never auto-promote |

## Common alternatives — when REJECT, what to substitute

| Rejected | Alternative | Reason |
|----------|-------------|--------|
| `requests` (sync only) | `httpx` | async + sync, pure-Python, MIT, healthy maintenance |
| `urllib3<1.26` (CVE backlog) | `httpx` or `urllib3>=2.0` | newer API, fewer CVEs |
| `pyyaml` (CVE-2017-18342 unsafe load) | `ruamel.yaml` (safe by default) OR `pyyaml>=6.0` with `safe_load` only | YAML default constructor history of unsafe-load CVEs |
| `pickle` (RCE on untrusted input) | `json` / `msgpack` / `protobuf` | pickle deserializes arbitrary objects |
| `dateutil` (parser tz-handling bugs) | stdlib `datetime` with `zoneinfo` (3.9+) | stdlib is sufficient for most cases |
| `aiohttp` (heavyweight; many transitives) | `httpx` | smaller transitive footprint for HTTP client use |
| Anything copyleft | search for permissive alternative | license incompatibility |

Don't blindly substitute — confirm the alternative exists, fits the use case, AND passes its own vetting.

## TPRD §10 dependency declaration template

```md
## §10. Dependencies

| Dep | Version | Role | License | Justification |
|-----|---------|------|---------|---------------|
| httpx | >=0.27,<1.0 | runtime | BSD-3-Clause | Async HTTP client; replaces `requests` per §3 async requirement |
| pydantic | >=2.5 | runtime | MIT | Config validation; alternative `@dataclass + __post_init__` is in scope but pydantic shines for the JSON-config consumer flow |
| opentelemetry-api | >=1.20 | runtime | Apache-2.0 | OTel wiring; consumer of the API only — no SDK |
| pytest | >=8.0 | dev (test) | MIT | Test runner |
| ruff | >=0.5 | dev (lint) | MIT | Lint + format |
| mypy | >=1.10 | dev (vet) | MIT | Strict type-check |

### Vetting summary
- License: all permissive (MIT / Apache-2.0 / BSD-3-Clause).
- pip-audit + safety: clean (run 2026-04-28).
- Transitives: 27 total (httpx pulls anyio, sniffio, idna, certifi, h11, h2, hpack, hyperframe, ...).
- Adoption: all >1M downloads/month.
- Native code: none (pydantic 2.x has Rust core but ships pre-built wheels).
- Sigstore: pydantic, httpx, opentelemetry-api ship attestations; pytest does not yet.
```

## BAD anti-patterns

```toml
# 1. No bound declared
[project]
dependencies = ["httpx"]                       # picks up arbitrary future versions

# 2. Gratuitous upper bound
dependencies = ["httpx<1.0"]                   # blocks downstream when httpx 1.0 ships
                                                # add upper bound only when documented incompatibility

# 3. Pinned exactly in runtime
dependencies = ["httpx==0.27.2"]               # ZERO room for downstream resolution

# 4. Dev dep in runtime
dependencies = ["pytest>=8.0"]                 # forces every consumer to install pytest

# 5. Build dep in runtime
dependencies = ["hatchling>=1.27"]             # build backend; not needed at runtime

# 6. Copyleft dep
dependencies = ["gpl-licensed-pkg>=2.0"]       # blanket rejection

# 7. Unmaintained dep with CVEs
dependencies = ["py>=1.0"]                     # archived 2023; CVE-2022-42969

# 8. Typosquat
dependencies = ["requsts>=2.0"]                # 1-letter typo of `requests`

# 9. Missing optional groups
[project]
dependencies = ["httpx", "pytest"]             # pytest in runtime; should be optional dev

# 10. No lockfile committed
# (uv.lock / poetry.lock / requirements.lock not in repo)
# Reproducible builds require pinned transitives; lockfile is the contract.
```

## Cross-references

- `python-sdk-config-pattern` — when to add pydantic (a vetted dep) vs stick with `@dataclass`.
- `python-mypy-strict-typing` — type-stub deps (`types-<name>`) often need their own vetting.
- `python-asyncio-patterns` — choosing between aiohttp and httpx (both vetted; httpx wins on transitive count).
- `python-otel-instrumentation` — `opentelemetry-api` vs `opentelemetry-sdk` (library uses API only; SDK is the consumer's choice).
- `sdk-dep-vet-devil-python` — agent that renders verdicts using these checks.
- `sdk-convention-devil-python` C-15 — dependency LIST shape rules (lower bounds, optional-dependencies groups).
- `sdk-packaging-devil-python` P-7 — runtime vs dev dep placement.
