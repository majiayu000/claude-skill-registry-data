---
name: ci-debug
description: >-
  Debug failing CI pipelines, pre-push gates, hosted GitHub Actions workflows, and
  reproduce test failures in safe isolation. Applies debug-mantra ground-truth discipline,
  recon seam/blast radius mapping, and foundationally sound (non-bandage) ponytail
  least-mechanism resolutions. Use when an operator says "fix failing CI", "debug this pipeline",
  "why is CI red", "gate failed", "pre-push gate red", "reconcile failed", "test contention",
  "container won't start", or "reproduce this CI bug".
---

# ci-debug — Governed CI/CD Diagnostic & Resolution Ladder

`ci-debug` is an end-to-end debugging and resolution ladder for failing CI/CD pipelines, local pre-push gates, and test suites. It coordinates three core disciplines:

1. **`/debug-mantra`**: Ground-truth extraction from raw CI artifacts, safe deterministic reproduction in a disposable full clone (GH-564), fail-path tracing, and disproof-first hypothesis falsification.
2. **`/recon`**: Seam, contract, and blast-radius mapping across callers, scripts, and harnesses before modifying code.
3. **`/ponytail` (Sound Root-Cause, Never a Bandage)**: The least-mechanism, foundationally sound long-term resolution (stdlib/native first, single authority/resolver, zero duplicate subsystems, deleting dead code). **Never** masks symptoms with `|| true`, loose regexes, silenced assertions, or unmeasured `sleep`s.

---

## The 4-Phase Resolution Ladder

```text
[1. Ground Truth & Repro (/debug-mantra)] ──► Raw logs/receipts, disposable clone (GH-564), isolate knobs, disproof-first
                 │
                 ▼
[2. Seam & Blast Radius Recon (/recon)]   ──► Identify failure archetype, map callers, contracts, build manifests
                 │
                 ▼
[3. Sound Minimal Resolution (/ponytail)] ──► Root-cause fix (least mechanism, zero bandages), leave 1 runnable check
                 │
                 ▼
[4. Governed Verification & Receipts]    ──► Preflight (validate.sh), qualifying gate (ci-local.sh), hosted CI watch
```

---

## Phase 1: Ground Truth & Isolation (`/debug-mantra`)

Establish primitive ground truth from raw artifacts before hypothesizing or modifying code.

### 1. Extract Raw Failure Evidence
Inspect the raw CI run or gate output directly. Never theorize from a summary:
```bash
# List recent hosted runs for the workflow or branch
gh run list --workflow ci.yml --limit 5

# Inspect exact failed step logs and error traces
gh run view <RUN_ID> --log-failed

# Or view local gate failure logs
cat .tick/gate-last.log 2>/dev/null || cat .git/pre-push.log 2>/dev/null
```

### 2. Provision Safe Full Clone Isolation (GH-564)
**Never run test reproductions or mutation suites in the primary checkout or a linked worktree.** Suites mutate `.git/config`, remotes, and ref locks:
```bash
# Provision a standalone disposable full clone outside the primary checkout
git clone . /tmp/XYZ-forge-ci-debug-$$-$(date +%s)
cd /tmp/XYZ-forge-ci-debug-$$-$(date +%s)
bash githooks/install.sh
```

### 3. Reproduce Deterministically
Reproduce the exact command executed by CI:
* **Local Gate Preflight:** `./validate.sh` (or targeted subsystem suite: `bash test/ci-route.sh --subsystem <name>`).
* **Hosted CI Command:** Check `.github/workflows/ci.yml` for exact step flags and environment variables.
* **Isolate Concurrency Knobs:** If parallel execution (`./validate.sh`, default cores/2) fails intermittently, run the failing suite in serial isolation (`bash test/<suite>.sh`). If it passes in serial, record the issue as **resource contention / timing race**, not a logic error.

### 4. Trace the Fail Path & Falsify Hypotheses
* Trace from the failing assertion back to the input state.
* Generate 2–3 ranked hypotheses. Identify the cleanest **disproof** for each.
* Run the disproof first: if a hypothesis fails to explain the failure path end-to-end, discard it immediately.
* Keep a running session breadcrumb ledger of ruled-out causes.

---

## Phase 2: Seam & Blast Radius Recon (`/recon`)

Map the system boundaries before drafting a fix to ensure no unread code enters the blast radius.

### 1. Classify the Failure Archetype

| Archetype | Common Signatures in XYZ Forge | Diagnostic Seam |
|---|---|---|
| **A. Static Guard & Lint** | `Frozen Bash twin guard (GH-308)` failed, `pipe-grep guard (GH-139)` failed, `mktemp trap guard (GH-177)` triggered, PDDA frontmatter missing `updated:` | `test/gh308-frozen-twin-guard.sh`, `security-scan.sh`, `utils/pdda/pdda.sh run` |
| **B. Concurrency & Contention** | SQLite `database is locked`, file lock timeout, generation trio mismatch (`gh32-releases-app` #558, `gh53` #541) | Lock paths in `utils/py/`, parallel worker count in `validate.sh` |
| **C. Platform & Runner Delta** | BSD vs GNU `sed`/`awk`/`stat`/`date` differences, macOS passing but `canary-ubuntu` failing on `ubuntu-latest` (#588/#590) | Missing flags, non-portable bash syntax, path casing |
| **D. Gate Provenance & Receipt Gap** | `wave-reconcile` exit 6, `--gate` missing `TESTS-RESULTS/` receipt (#546, #565, #592) | `check_provenance_receipts()`, `ci-local.sh` execution |
| **E. Reconciler / Ledger Drift** | Legacy issue drift (`GH-52` #584), missing DB table/column, roadmap sync error | `releases_app.py`, `wave_reconcile.py` |

### 2. Map Seams and Blast Radius
* Trace callers, consumer scripts, and exported environment variables touching the failing seam.
* Check whether the seam has a single authoritative implementation (e.g. Python in `utils/py/` vs legacy `.sh` twin).
* Document unknowns: anything unverified by a direct source read is an unknown, not an assumption.

---

## Phase 3: Sound Minimal Resolution (`/ponytail` — Structural Root-Cause)

Apply Ponytail to engineer the **least-mechanism, foundationally sound resolution**.

> [!IMPORTANT]
> **Ponytail is NOT a Bandage.**
> Ponytail minimizes the *mechanism* required to solve the true root cause. It is never permission to mask symptoms, silence guards, or introduce fragile workarounds.

### The Resolution Ladder:
1. **Does the failing code/machinery need to exist at all?** Delete dead code, retired views, or obsolete wrappers instead of patching them.
2. **Standard library / Native platform feature covers it?** Use built-in Python stdlib (`pathlib`, `sqlite3`, `subprocess`) or POSIX shell constructs over custom helper layers.
3. **Single Canonical Authority:** Centralize lock resolution, path lookup, or DB operations into one canonical utility rather than duplicating logic across scripts.
4. **Frozen Twin Rule (GH-308):** Behavior fixes belong in the authoritative Python twin under `utils/py/`, NOT the frozen `.sh` fallback. If an emergency edit to a `.sh` twin is truly warranted, add the mandatory commit trailer:
   `Frozen-twin-exception: <path> — <reason>`
5. **No Static Comment Traps (SOP §3b):** Static security guards read comments. Never write banned syntax (e.g. piped grep or credentials) inside explanatory comments.
6. **Leave One Runnable Red Control:** Every non-trivial fix must leave behind a runnable test/assertion that proves the defect is resolved and fails when mutated.

---

## Operational Containment Protocol (Secrets, Leakage & Incident Response)

If a defect, failed workflow, test artifact, or prompt transcript exposes API keys, service tokens, or private credentials:

1. **Priority 1 — Provider Revocation & Rotation First:**
   - Immediately revoke or rotate the compromised credential in the identity/cloud provider console or CLI before attempting git history manipulation.
2. **Priority 2 — Blast Radius Audit in Access Logs:**
   - Query provider audit and access logs for the compromised key's token ID during the exposure window to identify unauthorized accesses.
3. **Priority 3 — Preserve Sanitized Evidence:**
   - Never copy raw credentials, secret tokens, or decrypted payloads into issues, PR descriptions, or prompt logs. Replace all secret instances with deterministic redactions (`[REDACTED_API_KEY]`).
4. **Priority 4 — Explicitly Authorized History Scrubbing:**
   - History rewriting tools (`git-filter-repo` / BFG) require explicit operator confirmation.
   - Strictly comply with `WORKTREE-SAFETY.md`: verify that no linked worktrees depend on the rewritten refs, take a full backup of `.git` beforehand, and coordinate ref updates across active clones.

---

## Phase 4: Governed Verification & Receipts

1. **Preflight in Disposable Clone:**
   ```bash
   ./validate.sh
   ```
   Ensure 100% of test suites pass cleanly.
2. **Qualifying Gate Run (Receipt Generation):**
   ```bash
   bash ci-local.sh
   ```
   Verify that a valid, machine-readable JSONL receipt is written to `TESTS-RESULTS/`.
3. **Commit & Push Boundary:**
   Push the task branch to GitHub (`githooks/pre-push` executes automatically).
4. **Watch Hosted CI:**
   ```bash
   gh run watch $(gh run list --workflow ci.yml --limit 1 --json databaseId --jq '.[0].databaseId')
   ```
   Confirm both `smoke-gate-macos` and `canary-ubuntu` jobs turn green.

---

## Anti-Patterns: What NEVER to Do

* ❌ **Blind CI Reruns:** Running `gh run rerun` repeatedly hoping a flake disappears without a controlled baseline comparison.
* ❌ **Masking Failures:** Adding `|| true`, loose `grep -q`, or vacuous assertions that pass on empty strings (AGENTS.md §6).
* ❌ **Running Mutation Suites in Primary Tree / Worktrees:** Running `validate.sh` in the primary clone or linked worktrees corrupts `.git` shared state (GH-564).
* ❌ **Symptom Bandages via Ponytail:** Injecting arbitrary `sleep`s or skipping safety guards under the guise of "simplicity."
* ❌ **Gate Bypasses as Merge Readiness:** Using `git push --no-verify` or `XYZ_SKIP_PREPUSH=1` for anything other than operator-requested WIP drafts.
* ❌ **Editing Frozen Twins Silently:** Modifying frozen `.sh` files without updating the authoritative Python implementation and providing explicit trailers (GH-308/GH-321).
