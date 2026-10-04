---
name: infra-security
description: Audit AICP's security posture across 4 layers — secrets management (.env, gitignored), backend guardrails (paths/response/mode enforcement in aicp/guardrails/), runtime exposure (LocalAI port 8090 + MCP server + cloud backend tokens), and supply chain (Python deps, model GGUF integrity). Loads when the operator says "security audit", "check secrets", "what's exposed", "harden AICP".
allowed-tools: Read, Bash, Glob, Grep
effort: high
---

# infra-security

Audits AICP's security posture across the 4 layers that actually matter for
a backend AI orchestration platform: **secrets** (env vars, tokens, API
keys), **guardrails** (the `aicp/guardrails/` enforcement that prevents
prompt-driven misuse), **exposure** (network ports + MCP server reach +
cloud-token blast radius), and **supply chain** (Python deps + GGUF model
integrity). Different from `quality-audit` (broad health) — this skill
focuses on adversarial properties.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "security audit", "check secrets", "what's exposed", "harden AICP", "is this safe to deploy", "secrets review", "supply chain check"
- **Pre-deployment gate**: before exposing AICP beyond localhost (e.g., before fleet integration extends to a remote node), audit ensures no secrets leak + no unintended exposure
- **Post-incident retrospective**: a security-relevant incident (leaked token, prompt injection, exposed backend) — audit traces the hole
- **Periodic cycle**: monthly security review (secrets rotate, deps drift, exposure surface changes silently)
- **New backend / MCP tool added**: any new entry point needs security review before it ships
- **Dependency update batch**: after `make` or `pip` updates, audit the new deps for known CVEs

Do NOT load when:

- The concern is correctness (load `feature-test` or `systematic-debugging`)
- The concern is performance (load `quality-performance`)
- The concern is a specific failing test (load `systematic-debugging`)
- A live incident is in progress (load `ops-incident` first; security audit afterward)
- You want to write the security policy (load `architecture-propose` for design-level work)

## Operations

This skill has 4 named operations. Execute in order. This is a READ-ONLY skill — it inventories findings; remediation is separate tasks.

### Operation 1: Secrets audit

**Trigger**: skill loaded; security audit requested.

**Process**:

1. Verify `.env` is gitignored:

   ```bash
   git check-ignore .env || echo "WARNING: .env not gitignored"
   git ls-files | grep -E '^\.env$|/\.env$' || echo "OK: no .env in tracked files"
   ```

2. Scan tracked code for hardcoded secrets (false positives expected — investigate each):

   ```bash
   grep -rEn 'api[_-]?key|token|password|secret|bearer' aicp/ tools/ tests/ \
     --include='*.py' --include='*.yaml' --include='*.json' \
     | grep -vE 'def |class |#|test_|argparse|description|description=|"description":' \
     | head -30
   ```

3. Scan committed history for accidental leaks (last 100 commits):

   ```bash
   git log --all --full-history --source -p --pickaxe-regex \
     -S '(api_key|API_KEY|secret|password|token).*=.*[a-zA-Z0-9]{16,}' \
     --since='6 months ago' \
     | grep -E 'commit |^\+.*=' | head -40
   ```

4. Check `.env.example` exists and contains ONLY placeholder values:

   ```bash
   ls .env.example 2>&1 && grep -E '=.+' .env.example | grep -vE '<.*>|REPLACE_ME|YOUR_|example|TODO'
   ```

5. Check `config/profiles/*.yaml` for embedded secrets (profiles should reference env vars, not contain values):

   ```bash
   grep -rn 'api_key:\|token:\|password:' config/profiles/ 2>/dev/null
   ```

6. Audit `.mcp.json` for committed secrets (MCP configs sometimes embed tokens):

   ```bash
   cat .mcp.json | python3 -m json.tool | grep -iE 'token|key|secret|auth'
   ```

7. Write findings to `wiki/decisions/00_inbox/security-audit-<date>.md` (type=reference). Per-source findings: tracked-files violations / history violations / config violations.

**Quality bar (Operation 1 done when)**:

- [ ] `.env` confirmed gitignored
- [ ] Code scan for hardcoded secrets ran; false positives reviewed
- [ ] Git history scan for last 6 months ran
- [ ] `.env.example` validated (placeholders only)
- [ ] Profiles + .mcp.json scanned for embedded secrets
- [ ] Findings recorded in audit page

### Operation 2: Guardrails + permission mode audit

**Trigger**: Operation 1 complete.

**Process**:

1. Read `aicp/guardrails/`. Capture the enforcement surface:
   - `aicp/guardrails/paths.py` — which paths are protected? Confirm `.env`, `.git/`, `~/.aicp/dlq/` (DLQ data), credentials directories are blocked
   - `aicp/guardrails/response.py` — what response patterns are filtered? Credential leaks, secret echoes, etc.
   - `aicp/guardrails/checks.py` — pre/post execution checks, what do they enforce?
2. Verify the THREE PERMISSION MODES from CLAUDE.md (Think / Edit / Act) are actually enforced:
   - **Think**: search for the code path that BLOCKS writes when mode=think. Trace from `aicp/core/modes.py` through enforcement.
   - **Edit**: confirm scope-limited paths actually deny out-of-scope writes
   - **Act**: confirm command allowlist exists and is enforced
3. Check `force_cloud_modes` in profiles. Each profile should explicitly state which modes route to cloud. Misconfiguration could route an Edit/Act request to a permissive backend that doesn't apply mode enforcement.
4. Confirm guardrails have TESTS (per [feature-implement Gotcha 1 — orphan code](../feature-implement/SKILL.md)). Without tests, guardrails can silently break:

   ```bash
   ls tests/test_guardrails*.py 2>&1 || ls tests/guardrails/ 2>&1
   pytest tests/test_guardrails*.py -v 2>&1 | tail -20
   ```

5. Identify guardrail BYPASS paths. Per Quality Standards: "instructions alone get ~25% compliance." If guardrails are only documented in CLAUDE.md but not enforced in code, they're not real. Find any rule that's documented-only.
6. Append findings to the audit page under `## Guardrails`.

**Quality bar (Operation 2 done when)**:

- [ ] Each guardrail file inspected; protected paths + filtered responses + enforcement checks enumerated
- [ ] Three permission modes traced through code (each blocks what it claims to block)
- [ ] Guardrails have passing tests (or absence flagged as a gap)
- [ ] Documented-only rules (no code enforcement) explicitly listed
- [ ] Findings recorded in audit page

### Operation 3: Exposure surface audit

**Trigger**: Operation 2 complete.

**Process**:

1. Network ports — what's listening?

   ```bash
   docker compose ps 2>&1 | head -20
   ss -tlnp 2>/dev/null | grep -E ':8090|:9090|:9101|:3000|:7771|:7772' || \
     netstat -tlnp 2>/dev/null | grep -E ':8090|:9090|:9101|:3000'
   ```

   Capture which ports bind to `0.0.0.0` (all interfaces, exposed externally) vs `127.0.0.1` (localhost only). `0.0.0.0` bindings expose to the network — flag if unintentional.

2. LocalAI exposure: `:8090` is the OpenAI-compatible API. If bound to `0.0.0.0`, anyone on the LAN can use the local models without auth. Per AICP architecture, LocalAI should be `127.0.0.1` only (or behind a firewall) unless explicitly exposed to the fleet.

3. MCP server exposure (`aicp/mcp/server.py`): trace which transport (stdio vs HTTP). HTTP transport on `0.0.0.0` exposes the 11 MCP tools — including `aicp_route` which can dispatch to backends. Confirm intended.

4. Cloud token blast radius:
   - Where is `ANTHROPIC_API_KEY` (or equivalent) read? `grep -rn 'ANTHROPIC_API_KEY\|OPENROUTER_API_KEY' aicp/ tools/ 2>/dev/null`
   - Is it logged? Check `aicp/core/observability.py` and structured log calls — tokens must NEVER appear in logs.
   - Is it exposed via MCP responses? `aicp_route` returns backend metadata — confirm token isn't in the response shape.

5. Outbound connections: which external services does AICP call?

   ```bash
   grep -rEn 'https?://[a-zA-Z0-9.-]+' aicp/ --include='*.py' \
     | grep -vE 'docstring|comment|#|test_' \
     | sort -u | head -20
   ```

   Capture the outbound surface (Claude API, OpenRouter, ntfy, etc.). Each is a tracking + leak vector.

6. Append findings to audit page under `## Exposure`.

**Quality bar (Operation 3 done when)**:

- [ ] All listening ports enumerated with bind interface
- [ ] LocalAI exposure intentionality confirmed
- [ ] MCP server transport + auth model documented
- [ ] Cloud token usage traced; logging + response leaks ruled out
- [ ] Outbound services enumerated
- [ ] Findings recorded in audit page

### Operation 4: Supply chain audit + close out

**Trigger**: Operation 3 complete.

**Process**:

1. Python dependencies — known vulnerabilities:

   ```bash
   pip install --quiet pip-audit 2>/dev/null
   pip-audit --desc 2>&1 | tail -40
   ```

   Capture: vulnerable packages, severity, available fix versions.

2. GGUF model integrity — AICP downloads models via `make model-*`. Each download should verify against an upstream checksum. Check `Makefile`:

   ```bash
   grep -E 'sha256|sha512|integrity|--checksum' Makefile 2>/dev/null
   ```

   If checksums are not verified, flag as a supply chain gap (an MITM attack on a model download could substitute a malicious GGUF).

3. Pinned vs unpinned deps — `requirements*.txt` and `pyproject.toml`:

   ```bash
   cat requirements*.txt pyproject.toml 2>/dev/null | grep -E '^[a-zA-Z]' | head -30
   ```

   Unpinned deps (no version specifier) silently update to potentially-vulnerable versions on next install. Pin all production deps.

4. Docker image versions — `docker-compose.yaml` references LocalAI v4.1.3 and other images. Pinned vs `latest`:

   ```bash
   grep -E 'image:.*' docker-compose.yaml
   ```

   `latest` tags allow silent updates with potentially-breaking or vulnerable changes. Pin all images.

5. Author the audit page summary:
   - Overall posture: GREEN (no critical findings) / YELLOW (some findings, none critical) / RED (critical finding — secret leak, exposed backend without auth, vulnerable dep with active exploit)
   - Per-layer summary (secrets / guardrails / exposure / supply chain)
   - Recommended remediation tasks (file as backlog tasks for any HIGH-severity finding)
6. If a CRITICAL finding (RED), STOP and report to operator immediately — don't bury in the audit page.
7. If a SYSTEMIC pattern (e.g., "every config file accepts secrets without env-var indirection"), contribute back as a lesson.
8. Run `tools/lint.py wiki/decisions/00_inbox/security-audit-<date>.md`.

**Quality bar (Operation 4 done when)**:

- [ ] `pip-audit` run; vulnerable deps captured
- [ ] GGUF integrity check status documented
- [ ] Dep pinning gaps flagged
- [ ] Docker image pinning verified
- [ ] Overall posture rating + per-layer summary in audit page
- [ ] CRITICAL findings escalated immediately (not buried)
- [ ] Remediation tasks filed for HIGH-severity items
- [ ] Audit page lint passes

## Gotchas (known failure modes — read before doing)

### Gotcha 1: False positives in secret scan (alert fatigue)

The temptation: secret scans return 50 matches. Tempting to skim and call it clean. NO — every match needs human review. False positives are common (variable names like `api_key_field`, test fixtures, docstrings) but real positives hide in the noise.

**Detection**: did you READ each match in context, or did you grep + count + report "looks fine"?

**The rule**: every match in Operation 1 step 2 gets human classification (real / false positive / needs investigation). False positives are documented in the audit page so the next audit can recognize them and skip.

### Gotcha 2: Trusting the .gitignore (without verifying history)

The temptation: `.env` is in `.gitignore`, so secrets are safe. NO — gitignore prevents FUTURE commits, not historical ones. If `.env` was committed once before being gitignored, the secret is in history. Operation 1 step 3 catches this.

**Detection**: did you actually run the history scan? Or did you accept "gitignore means safe"?

**The rule**: gitignore + history scan together. If history shows a leak, the secret must be ROTATED (the gitignore doesn't unleak the past).

### Gotcha 3: Auditing guardrails by reading the docs (not the code)

The temptation: CLAUDE.md says "Think mode → no writes allowed." Document the guardrail as enforced. NO — the documented rule is a CLAIM. Operation 2 step 2 traces the rule through CODE to verify it's actually enforced.

**Detection**: did you trace each permission-mode rule from CLAUDE.md through `aicp/core/modes.py` and confirm the enforcement code path exists + has tests?

**The rule**: per Quality Standards "instructions alone get ~25% compliance" — documented-only rules are NOT enforced. Audit the CODE.

### Gotcha 4: Reporting `0.0.0.0` bindings without context (false alarm OR missed alarm)

The temptation: any `0.0.0.0` binding gets flagged as exposure. Or: ignored because "it's behind WSL2's NAT anyway." Both are wrong. The right framing: WHO can reach this port, intentionally?

**Detection**: did Operation 3 confirm the INTENDED reach for each `0.0.0.0` binding? E.g., is LocalAI:8090 intended to be reachable from the LAN (fleet integration) or only from this host (solo dev)?

**The rule**: each binding has a documented intent. Document the intent in the audit page. Mismatches between intent and config are findings; aligned intents are not.

### Gotcha 5: Skipping supply chain because "deps are pinned" (incomplete audit)

The temptation: deps are pinned in `pyproject.toml`, so supply chain is fine. NO — pinning prevents silent UPDATES, but doesn't address: (a) the pinned version may have a CVE today, (b) Docker images may be unpinned even if Python deps are pinned, (c) GGUF model downloads may not verify integrity.

**Detection**: did Operation 4 cover all 4 sub-checks (pip-audit, GGUF integrity, dep pinning, Docker image pinning)?

**The rule**: supply chain is multi-layer. Pinning is one layer. Run pip-audit on every audit (CVEs are continuously published).

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact:

- **Security audit page**: same shape as sibling quality audits (coverage / lint / debt / performance) — reference page with per-layer findings + posture rating.
- **Real guardrails reference**: see `aicp/guardrails/` for what enforcement looks like (paths, response, checks) — your audit verifies these against documented intent.
- **Sibling skill** (`security-review` from the harness skill set): operates at PR-diff level, complementary to this skill's project-level audit.

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). AICP-specific concerns: LocalAI exposure on :8090, MCP server transport (stdio vs HTTP), cloud-backend tokens (Claude, OpenRouter, ntfy), GGUF model downloads, Docker compose stack.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| security-review | PR-diff level review | Tactical (per-PR); this skill is project-wide |
| quality-audit | umbrella quality (incl. lint, coverage) | Different axis (quality vs security) |
| ops-incident | live security incident response | Reactive; this skill is proactive |
| ops-deploy | deployment with pre-flight checks | Includes a basic security check; this skill is the deep audit |
| dependency-scanner | external dep vulnerability scanner | Sub-tool; this skill uses it (Operation 4) |
| config-secrets | secret rotation + management | Operational; this skill audits |
