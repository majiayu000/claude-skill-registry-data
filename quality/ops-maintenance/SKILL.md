---
name: ops-maintenance
description: Routine non-incident upkeep — security audit Python deps (`pip-audit`), refresh model GGUF inventory, prune Docker dangling images + volumes, rotate logs (`~/.aicp/dlq/<old-date>`, `~/.aicp/history/`), trim WSL VDisk, check `.env` token expiry / rotation cadence, refresh KB Collections, run `make profile-validate`. Distinct from `ops-incident` (reactive — something is broken) and `ops-deploy` (forward action — shipping change). Loads when the operator says "maintenance window", "weekly upkeep", "clean up", "rotate logs", "patch deps", "do the housekeeping".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# ops-maintenance

The preserve-not-change skill. Runs the periodic upkeep that keeps AICP from accumulating cruft — dependency security patches, log rotation, disk reclamation (especially the WSL VDisk that doesn't shrink on its own), token rotation cadence checks, KB Collections refresh. Distinct from the reactive (`ops-incident`) and forward (`ops-deploy`) skills — this skill is the one that runs on a calendar, not in response to a signal.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "maintenance", "weekly upkeep", "do the housekeeping", "rotate logs", "clean up", "patch deps", "is anything overdue".
- **Calendar trigger**: weekly / monthly cadence the operator runs ("first-of-month maintenance", "Friday cleanup").
- **Disk/resource pressure signal**: `df` reports low free space, WSL VDisk grew, `~/.aicp/dlq/` has accumulated weeks of files, Docker `system df` shows reclaimable space.
- **Security context**: a CVE landed in a watched package; `pip-audit` is overdue; secrets rotation cadence due.

Do NOT load when:

- Something is actively broken — load `ops-incident`.
- A specific dependency upgrade is the request — load `refactor-dependencies` (the surgical version) or `evolve-migrate` (cross-version replacement).
- A specific secret rotation is the request — load `config-secrets`.
- A backup is overdue — load `ops-backup`.
- A model needs install/swap — load `aicp-model-mgmt`.

## Operations

This skill has 4 named operations. They are independent — operator may run all or pick subset.

### Operation 1: Dependency security + freshness

**Trigger**: skill loaded; operator wants the dep audit (or full maintenance).

**Process**:

1. Run security audit:
   ```bash
   .venv/bin/pip-audit --desc 2>&1 | tail -50
   # if not installed: .venv/bin/pip install pip-audit
   ```
   Capture: list of vulnerable packages with CVE IDs.
2. Cross-reference with `pyproject.toml` / `requirements.txt`:
   - Direct dep with CVE → upgrade now.
   - Transitive dep with CVE → check if a direct dep upgrade pulls a fix; otherwise pin transitively.
3. Check freshness without forcing churn:
   ```bash
   .venv/bin/pip list --outdated --format=json | python3 -c "import sys,json; [print(p['name'], p['version'], '→', p['latest_version']) for p in json.load(sys.stdin)]"
   ```
   Triage: security/bugfix patches (apply), minor updates (apply if no breaking changelog notes), major updates (defer to `evolve-migrate` task).
4. Apply fixes:
   ```bash
   .venv/bin/pip install --upgrade <pkg>==<version>
   .venv/bin/pip freeze > requirements.lock.txt   # or pyproject regen
   make test 2>&1 | tail -10   # gate the upgrade
   ```
5. Commit upgrades as a SEPARATE commit from any code change in this maintenance window — keeps blame clean.

**Quality bar (Operation 1 done when)**:

- [ ] `pip-audit` output captured, every CVE either fixed or explicitly tracked as accepted-risk.
- [ ] Outdated list reviewed; security/bugfix patches applied.
- [ ] Test suite passes after upgrades (no regression).
- [ ] Lock file regenerated and committed.
- [ ] Commit isolated (`fix(deps): security upgrades for X, Y, Z` — no other changes).

### Operation 2: Disk + log housekeeping

**Trigger**: Operation 1 done OR operator wants disk cleanup specifically.

**Process**:

1. Inventory disk usage:
   ```bash
   du -sh ~/.aicp/dlq/ ~/.aicp/history/ /var/log/openclaw/ logs/ 2>/dev/null
   docker system df
   df -h /
   ```
2. Rotate AICP runtime state — keep last 30 days, archive or delete older:
   ```bash
   find ~/.aicp/dlq/ -name "*.jsonl" -mtime +30 -print   # review BEFORE delete
   # delete only after review:
   find ~/.aicp/dlq/ -name "*.jsonl" -mtime +30 -delete
   find ~/.aicp/history/ -mtime +60 -delete
   ```
3. Docker reclamation — prune dangling layers + unused volumes (NEVER `prune -a` blindly):
   ```bash
   docker image prune -f                # remove dangling
   docker volume ls -qf dangling=true   # review
   docker volume prune -f               # only after review of names above
   docker builder prune -f --keep-storage 5GB
   ```
4. WSL VDisk shrink (per the operator's environment — VDisk doesn't shrink on its own and `fstrim.timer` may be ConditionVirtualization-blocked):
   ```bash
   sudo fstrim -av 2>&1 | tail -5
   # if fstrim.timer is conditionally disabled, this is the manual run.
   # The Vdisk shrink itself is Windows-side: wsl --shutdown then `Optimize-VHD`.
   ```
5. Application logs — rotate / truncate any project log file >50 MB:
   ```bash
   find . -name "*.log" -size +50M -ls
   ```

**Quality bar (Operation 2 done when)**:

- [ ] Reclaimable disk reported BEFORE and AFTER (concrete numbers, not "freed up some space").
- [ ] DLQ + history retention applied per the 30/60-day windows.
- [ ] Docker `system df` shows reduced reclaimable.
- [ ] `fstrim` ran successfully (or noted as out-of-scope due to mount type).
- [ ] No log file in the working tree exceeds 50 MB.

### Operation 3: Secrets + certificate cadence

**Trigger**: Operation 2 done OR operator wants secrets-only check.

**Process**:

1. Inventory tokens in `.env` against the rotation policy:
   ```bash
   grep -E "^(ANTHROPIC|OPENROUTER|OLLAMA|HF|NTFY)_(API_KEY|TOKEN)" .env | cut -d= -f1
   ```
   For each, check operator's recorded "last rotated" date (typically tracked in `docs/SECRETS-ROTATION.md` or operator-internal notes).
2. Apply policy: a token older than 90 days is due. Surface those — don't auto-rotate without operator action (rotation is a multi-step process: provider portal → new token → update `.env` → restart).
3. Certificate check — AICP itself doesn't terminate TLS, but sister projects and any reverse proxy might:
   ```bash
   # if any HTTPS endpoint on the host:
   for url in <list-of-https-endpoints>; do
     echo | openssl s_client -servername "$url" -connect "$url:443" 2>/dev/null \
       | openssl x509 -noout -enddate
   done
   ```
   Flag any cert expiring in <30 days.
4. Verify `.env.example` matches `.env` keys (no secret keys missing from the example placeholder file):
   ```bash
   diff <(grep -oE "^[A-Z_]+=" .env | sort) <(grep -oE "^[A-Z_]+=" .env.example | sort)
   ```

**Quality bar (Operation 3 done when)**:

- [ ] Token inventory checked against 90-day rotation policy.
- [ ] Tokens overdue surfaced to operator with concrete provider portal link (or "no rotations due").
- [ ] Cert expiry checked (or "no TLS-terminating endpoints — N/A").
- [ ] `.env` ↔ `.env.example` parity verified.

### Operation 4: KB + profile + system smoke

**Trigger**: Operations 1-3 done; finalize maintenance with a full sanity check.

**Process**:

1. KB Collections refresh — drift check between source content and indexed Collections:
   ```bash
   make kb-status 2>/dev/null | tail -10
   make kb-sync 2>&1 | tail -10   # only if kb-status reports drift
   ```
2. Profile validation — every profile YAML still parses + tier_map covers all bands:
   ```bash
   make profile-validate 2>&1 | tail -10
   for p in config/profiles/*.yaml; do
     python3 -c "import yaml; yaml.safe_load(open('$p'))" || echo "INVALID: $p"
   done
   ```
3. Full system smoke:
   ```bash
   .venv/bin/aicp --check 2>&1 | tail -15
   .venv/bin/aicp --self-test 2>&1 | tail -10
   ```
4. Update `docs/MAINTENANCE-LOG.md` (or operator's chosen log location):
   ```markdown
   ## YYYY-MM-DD
   - Deps: <N> security upgrades; <N> bugfix patches; <list>
   - Disk: reclaimed <N> GB (DLQ <N>, Docker <N>, WSL VDisk <N>)
   - Secrets: <N> rotations due → operator action
   - KB: <synced | clean>
   - Smoke: <pass | issues: ...>
   ```

**Quality bar (Operation 4 done when)**:

- [ ] KB drift checked; synced if drift detected.
- [ ] Every profile YAML validates.
- [ ] `aicp --check` and `aicp --self-test` both pass.
- [ ] Maintenance log entry written with concrete numbers, not "did some cleanup".

## Gotchas (known failure modes — read before doing)

### Gotcha 1: `docker system prune -a` deletes work-in-progress images

Operator says "free up disk". Skill runs `docker system prune -a -f --volumes`. The `-a` flag deletes ALL images not currently used by a running container — including images for services that are intentionally stopped, builder caches the operator was iterating on, and the model-test images that take 20 minutes to rebuild.

**The rule**: never use `prune -a` in maintenance. Use `image prune -f` (dangling only), `volume prune -f` after listing volumes, and `builder prune -f --keep-storage 5GB` (keeps recent caches). Anything beyond is operator-explicit, not maintenance-automatic.

### Gotcha 2: Deleting DLQ files that haven't been processed

`find ~/.aicp/dlq/ -name "*.jsonl" -mtime +30 -delete` runs unconditionally. But a 31-day-old DLQ file might contain failures that NEVER got retried — the rotation policy assumes "after 30 days, the failure is irrelevant", which isn't always true. Operator's research-mode flow may have left useful failure context in those files.

**The rule**: Operation 2 step 2 lists files BEFORE deleting (`-print`). For research-class projects, default retention should be 90 days, not 30. The skill's default is 30 because most operators want it; for AICP specifically, verify operator's preferred window before applying.

### Gotcha 3: Auto-upgrading minor deps that have breaking changes

`pip-audit` flags package X. Skill runs `pip install --upgrade X`. The upgrade jumps a minor version (1.4.x → 1.5.x); changelog has a breaking API change. Tests still pass because no test covers the affected codepath; runtime hits the bug a week later.

**The rule**: Operation 1 step 2 reads the package's changelog/release notes between current and target version BEFORE upgrading. For "minor" upgrades (semver 1.4 → 1.5), look for "Breaking" / "Removed" / "Deprecated" sections. If found, treat as major-version semantics — defer to `evolve-migrate` rather than auto-applying.

### Gotcha 4: WSL VDisk doesn't actually shrink from inside WSL

Skill runs `fstrim -av`, reports "freed N GB". But the WSL VDisk file (`ext4.vhdx` on the Windows host) is unchanged — `fstrim` releases blocks INSIDE the filesystem; the VHDX wrapper doesn't auto-shrink. Operator looks at Windows disk and sees no change.

**The rule**: state explicitly that `fstrim` is the WSL-side preparation; the actual VHDX shrink is a Windows-side action (`wsl --shutdown` then `Optimize-VHD -Path <path> -Mode Full` in PowerShell as admin). For maintenance, do the WSL-side step and TELL the operator the Windows-side step is required to reclaim host disk. Don't claim space-recovery the operator can't actually see.

### Gotcha 5: Maintenance log says "did everything" without numbers

Maintenance log entry: "Cleaned up disk, updated deps, rotated logs, all good." Two months later, operator wonders if last maintenance actually helped. The log has no numbers to tell whether anything changed.

**The rule**: Operation 4 step 4 — the log entry MUST have numbers. "Reclaimed 8.3 GB" is a record. "Cleaned up disk" is a vibe. If a step found nothing to do, the log says "no rotations due", "no CVEs", "no drift" — not silence.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP's maintenance surface is shaped by its specifics: model GGUFs are large (1.7 GB to 60+ GB) and the WSL VDisk doesn't shrink on its own (per `feedback_storage_tiers_and_wsl_vdisk_rule` operator memory — model weights NEVER live on WSL VDisk; check mount point before any download). DLQ retention is per-day JSONL files in `~/.aicp/dlq/`. KB Collections live in LocalAI and need `make kb-sync` if source markdown drifted. The 11 profile YAMLs need YAML validation in the validate step. There is no traditional cert-renewal path because AICP itself doesn't terminate TLS — that lives in fronting reverse proxies if any.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| ops-incident | Active failure response | Reactive; this skill is preventive |
| ops-deploy | Forward action shipping change | Forward; this skill preserves status quo |
| ops-backup | Snapshot state for restore | One-shot capture; this skill is recurring upkeep |
| refactor-dependencies | Surgical dep audit + restructure | Deeper pkg-graph hygiene; this skill is patch + cadence |
| config-secrets | Add/rotate a specific secret | Surgical secret op; this skill checks cadence across all |
| evolve-migrate | Cross-version foundation swap | Major version jump; this skill is patch + minor |
| aicp-model-mgmt | Install/unload/swap models | Model lifecycle; this skill checks model inventory only |
