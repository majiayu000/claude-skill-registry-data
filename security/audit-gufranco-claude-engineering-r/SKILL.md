---
name: audit
description: Security audit across dependencies, secrets, Docker, code patterns, images, STRIDE, and OWASP. Covers dependency vulnerability scanning and threat modeling. Use when user says "security audit", "scan for vulnerabilities", "check dependencies", "find secrets", "audit Docker", "CVE scan", "cso", "threat model", "owasp audit", "deep security scan", or wants to find security issues across the full project. For code review, use /review; for architecture completeness, use /assessment; for running tests, use /test.
argument-hint: "/audit [deps [outdated|update <pkg>]|secrets|docker|code|scan|image <name>|threat [component]|daily|comprehensive|trust [path]]"
allowed-tools: "Read, Grep, Glob, Bash, WebFetch, AskUserQuestion"
sensitive: true
---

## Overview

Multi-layer security audit, dependency management, and threat modeling.

## When to Use

Run `trust` on any freshly received project before the first install or build command, `daily` before merging a significant PR, and `comprehensive` before a major release. The bare `/audit` covers dependencies, secrets, Docker, and code patterns in one pass.

### Subcommand Routing

| Invocation | Action |
|-----------|--------|
| `/audit` | Run all audit layers (deps, secrets, docker, code) |
| `/audit deps` | Dependency vulnerability scan |
| `/audit deps outdated` | List packages with newer versions |
| `/audit deps update [pkg]` | Update packages with approval |
| `/audit secrets` | Secret scanning across the full repo: Full Audit step 3 with the Extended Secret Detection Patterns under `deps` |
| `/audit docker` | Dockerfile security checks |
| `/audit code` | Code pattern analysis for injection, XSS, and the rest of Full Audit step 5, run alone |
| `/audit scan` | Deep scan with trivy, snyk, and gitleaks, per `scan (deep)` under `deps` |
| `/audit image <name>` | Docker image vulnerability and layer analysis, per `image <name>` under `deps` |
| `/audit threat` | STRIDE threat modeling for the project or a specific component |
| `/audit daily` | High-confidence security gate: secrets archaeology, supply chain, CI/CD pipeline review |
| `/audit comprehensive` | Deep scan: daily checks plus OWASP Top 10, STRIDE per component, LLM/AI review |
| `/audit trust` | Untrusted-project safety scan. Run before `pnpm install`, `uv sync`, or any build command on a freshly received project |

If no subcommand is given, run all layers except threat modeling, daily, and comprehensive, which require focused analysis.

## Process

1. Route the invocation per Subcommand Routing; with no subcommand, run Full Audit.
2. Check which scanners are on `PATH` and report the missing ones before scanning.
3. Run the Steps of the selected section in order.
4. Report findings in that section's output format, with severity buckets or 1-10 scores, and masked secret matches.
5. For `threat`, `daily`, and `comprehensive`, state every finding rated 8/10 or higher as blocking.

---

## Full Audit (default)

### Steps

1. **Detect project and tools**, parallel: identify languages from manifests, check for Dockerfiles, check available tools, `pnpm`, `pip-audit`, `cargo-audit`, `trivy`, `grype`, `semgrep`, `bandit`, read `.env.example`.
2. **Dependency scan**: per-language audit (see deps section).
3. **Secret scanning**: scan all tracked files, `git ls-files` using patterns from `~/.claude/hooks/secret-scanner.py`. Skip binaries, lockfiles, vendored code. Check [`.gitignore`](../../.gitignore) covers `.env`, `*.pem`, `*.key`. Apply the extended provider-specific patterns below (see secrets section) for Stripe, Twilio, GCP, Azure, Slack, Shopify, and other services not covered by the hook's generic patterns.
4. **Dockerfile and Compose checks**: see the `docker` subcommand section below. Run the full Dockerfile checklist and, when `compose*.yml` or `docker-compose*.yml` is present, the full Compose checklist. If `hadolint` is on `PATH`, run `hadolint Dockerfile`. If `docker scout` is available, run `docker scout quickview` and `docker scout cves`. If `trivy` is available, scan built images.
5. **Code patterns**: SQL injection, string concatenation in queries, command injection via `exec`, `spawn`, or `eval` with dynamic input, XSS through `dangerouslySetInnerHTML` or `innerHTML`, path traversal, hardcoded secrets, insecure randomness using `Math.random()` for security, empty catch blocks. Run `semgrep --config auto` if available. Also check supply chain risks: review `postinstall` scripts in dependencies via `cat node_modules/<pkg>/package.json | jq .scripts.postinstall`, verify scoped packages resolve to the private registry, `pnpm install --lockfile-only --ignore-scripts`, verify Docker secrets use `--mount=type=secret` not `ENV` or `ARG`, and confirm lockfile integrity hashes are present.
6. **Compile report** by severity:

```
## Security Audit Report

**Project:** <name>
**Date:** <date>
**Layers scanned:** dependencies, secrets, docker, code

### Critical (fix immediately)
### High (fix before next release)
### Medium (schedule fix)
### Low (backlog)

### Summary
| Layer | Critical | High | Medium | Low |
|-------|----------|------|--------|-----|

### Missing safeguards
- [ ] .gitignore covers .env and credential files
- [ ] .env.example documents all required env vars
- [ ] Dockerfiles use non-root user
- [ ] Dependencies have no critical vulnerabilities
```

1. **Suggest next steps** per finding severity.

---

## deps

Audit dependencies for known vulnerabilities. Detect package manager from lockfile.

### Package Manager Detection

`bun.lock`/`bun.lockb` = bun, `pnpm-lock.yaml` = pnpm, `yarn.lock` = yarn, `package-lock.json` = npm, which is converted to pnpm with `pnpm import`, `Cargo.toml` = cargo, `go.mod` = go, `pyproject.toml` with `uv.lock` = uv, `pyproject.toml` with `[tool.poetry]` = poetry, `pyproject.toml`/`requirements.txt` = pip. Also check for `Makefile`/`Justfile` targets.

### Audit (default)

Run language-specific audit: `pnpm audit`, `pip-audit`, `cargo audit`, `govulncheck ./...`. Parse and present by severity.

### outdated

Run `pnpm outdated`, `cargo outdated`, `go list -m -u all`, etc. Show current, wanted, and latest versions.

### update [package]

Show what would change, ask for approval, run update, re-audit to verify no new vulnerabilities.

### scan (deep)

Check available tools, parallel: `trivy`, `snyk`, `gitleaks`. Run all available:
- `trivy fs .` for dependency + config + secret scanning.
- `snyk test` + `snyk code test` for dependency + static analysis.
- `gitleaks detect --source .` for hardcoded secrets.

### Extended Secret Detection Patterns

Apply these provider-specific patterns during `secrets` and `scan` runs. These extend the generic patterns in `secret-scanner.py` with service-specific formats.

| Provider | Pattern | Severity |
|----------|---------|----------|
| AWS access key | `AKIA[0-9A-Z]{16}` | CRITICAL |
| Stripe | `sk_live_[a-zA-Z0-9]{24,}` or `pk_live_[a-zA-Z0-9]{24,}` | CRITICAL |
| Twilio | `AC[a-f0-9]{32}` or `SK[a-f0-9]{32}` | CRITICAL |
| GCP service account | `"type":\s*"service_account"` with `private_key_id` | CRITICAL |
| Azure storage | `AccountKey=[a-zA-Z0-9+/=]{88,}` | CRITICAL |
| Slack | `xoxb-[a-zA-Z0-9-]{50,}` or `hooks\.slack\.com/services/` | CRITICAL |
| GitHub PAT | `ghp_[a-zA-Z0-9]{36}` | CRITICAL |
| GitLab PAT | `glpat-[a-zA-Z0-9-]{20}` | CRITICAL |
| Shopify | `shppa_[a-z0-9]{32}` or `shpat_[a-z0-9]{32}` | CRITICAL |
| MongoDB Atlas | `mongodb\+srv://[^:]+:[^@]+@` | CRITICAL |
| Vault token | `s\.[a-zA-Z0-9]{24}` | CRITICAL |
| SendGrid | `SG\.[a-zA-Z0-9_-]{22,}` | CRITICAL |
| Firebase | `firebase-adminsdk` or `serviceAccount.json` | CRITICAL |
| npm registry | `//registry.npmjs.org/:_authToken` | CRITICAL |
| OpenAI | `sk-[a-zA-Z0-9]{48,}` | HIGH |
| Anthropic | `sk-ant-[a-zA-Z0-9_-]{48,}` | HIGH |
| Google Maps | `AIzaSy[a-zA-Z0-9_-]{33}` | HIGH |
| Datadog | `DD_API_KEY=[a-f0-9]{32}` | HIGH |
| Cloudflare | `CF_API_TOKEN=` or `X-Auth-Key:` | HIGH |
| Okta | `SSWS [a-zA-Z0-9_-]{40,}` | CRITICAL |

Also check high-risk contexts: test fixtures with real credentials, database seed files with production data, `.tfstate` files, Docker `ENV`/`ARG` with secrets, and `*.js.map` source maps containing decompiled secrets.

### image <name>

- `trivy image <name>` for OS and library vulnerabilities.
- `dive <name>` for layer analysis and wasted space.

---

## docker

Dockerfile, Compose, BuildKit, and image authoring audit. Authority for every rule below is [`standards/container-security.md`](../../standards/container-security.md).

### Dockerfile checklist

For each Dockerfile in the repo, verify:

- Base image pinned by digest, `FROM image:tag@sha256:...`, not floating tag such as `latest`, `lts`, or no tag
- `# syntax=docker/dockerfile:1` declared at the top to enable modern BuildKit frontend
- Multi-stage build; runtime stage does not include compilers, source, or dev dependencies
- `WORKDIR` absolute path
- `USER` directive in final stage sets a non-root UID. Numeric preferred for Kubernetes compatibility
- No `COPY .env*`, `COPY *.pem`, `COPY *.key`, `COPY *.crt`, `COPY id_rsa*`
- No `ENV` or `ARG` containing literal secret values such as `PASSWORD=`, `TOKEN=`, `API_KEY=`, or `PRIVATE_KEY=`
- Build-time secrets use `RUN --mount=type=secret,id=<name>`, never `ENV` or `ARG`
- Package installs use `--no-install-recommends`, apt, `--no-cache`, apk, or equivalent
- Package manager caches purged in the same layer: `rm -rf /var/lib/apt/lists/*`, `pip cache purge`, etc.
- BuildKit cache mounts used for package managers when build time matters: `--mount=type=cache,target=<path>`
- `COPY --link` used to maximize layer cache hits
- `HEALTHCHECK` declared with `--interval`, `--timeout`, `--start-period`, `--retries`
- PID 1 covered by `tini`, `dumb-init`, `docker run --init`, or Compose `init: true`
- `.dockerignore` exists and excludes `.env*`, `*.pem`, `*.key`, `.git/`, `node_modules/`, `.terraform/`
- Hadolint clean on the file when `hadolint` is on `PATH`. Run `hadolint Dockerfile`

### Compose checklist

For each `compose.yml`, `compose.*.yml`, `docker-compose.yml`, `docker-compose.*.yml`:

- No top-level `version:` key. Deprecated under Compose v2
- Every service has `read_only: true` unless the workload legitimately writes to its root
- Every service has `cap_drop: ["ALL"]` followed by minimal `cap_add:` entries
- Every service has `security_opt: ["no-new-privileges:true"]`
- No service has `privileged: true`
- No service has `pid: host`, `ipc: host`, `network_mode: host`, or `userns_mode: host`
- Every service either inherits a non-root `USER` from the Dockerfile or sets `user: "<uid>:<gid>"`
- Secrets defined via top-level `secrets:` with `file:`, `environment:`, or `external: true` source; never via plain `environment:`
- Apps consume secrets via the `*_FILE` convention (`DB_PASSWORD_FILE=/run/secrets/db_password`)
- Dev port bindings use `127.0.0.1:` prefix; internal services use `expose:`, not `ports:`
- Networks are explicit per tier; backend networks marked `internal: true`
- `depends_on:` uses `condition: service_healthy` form for ordering, paired with `healthcheck:`
- Every service sets `init: true` or has `tini`/`dumb-init` as PID 1 in its Dockerfile
- Resource limits set such as `deploy.resources.limits.memory`, `cpus`, plus `pids_limit`, or `ulimits.nofile`
- `restart:` uses `on-failure:<n>` or `unless-stopped`, not unbounded `always`
- Only namespaced `sysctls:`. No raw `net.core.*`
- Dev-only services gated behind `profiles: ["dev"]`
- Production deployment does not invoke `docker compose watch` or the `develop:` block

### Tools to invoke when present

| Tool | Command |
|------|---------|
| Hadolint | `hadolint Dockerfile` per Dockerfile; fail on any rule in the never-ignore list (DL3000, DL3007, DL3008, DL3018, DL3025, DL3027, DL3059, DL4006) |
| Docker Scout | `docker scout quickview <image>`; then `docker scout cves <image> --only-severity critical,high --exit-code`; then `docker scout policy evaluate <image>` for attestation coverage |
| Trivy | `trivy config .` for Dockerfile + Compose misconfigurations; `trivy image <name>` for OS+library CVEs |
| Grype | `grype <image>` cross-check with Trivy when the registry is sensitive |
| Dive | `dive <image>` for layer waste and base-image bloat |
| BuildKit attestation check | `docker buildx imagetools inspect <image> --format '{{ json .SBOM }}'` and `--format '{{ json .Provenance }}'` to confirm SBOM + provenance attached |

### Reporting

Report findings in the standard severity buckets: Critical, High, Medium, or Low. Critical: secrets in layers, `privileged: true`, host namespaces, `COPY .env`. High: missing `USER` non-root, floating tags, missing `cap_drop`, missing `no-new-privileges`, dev ports bound to `0.0.0.0`. Medium: missing `HEALTHCHECK`, missing `init: true`, missing `.dockerignore`, missing BuildKit cache mounts. Low: missing attestations, missing Hadolint config, image bloat.

---

## threat

STRIDE threat modeling for the full project or a specific component. Systematic analysis of security threats across six categories.

### When to use

- Before deploying a new service or API to production.
- When adding authentication, authorization, or data handling features.
- During security review of an existing system.
- When compliance or regulatory requirements demand threat analysis.

### Arguments

- No arguments: analyze the full project.
- `<component>`: focus on a specific module, service, or feature (e.g., `/audit threat auth`, `/audit threat payments`).

### Steps

1. **Map the attack surface.** Read the project structure and identify:
   - Entry points: API routes, webhooks, message consumers, CLI commands.
   - Data stores: databases, caches, file storage, session stores.
   - External integrations: third-party APIs, OAuth providers, payment processors.
   - Trust boundaries: where authenticated meets unauthenticated, where internal meets external.

2. **Analyze each STRIDE category.** For every entry point and data flow:

   | Category | Question | What to look for |
   |----------|----------|-----------------|
   | **S**poofing | Can an attacker impersonate a user or service? | Missing auth on endpoints, weak token validation, no mutual TLS between services |
   | **T**ampering | Can data be modified in transit or at rest? | Missing input validation, unsigned payloads, no integrity checks on stored data |
   | **R**epudiation | Can a user deny performing an action? | Missing audit logging, no transaction records, unsigned operations |
   | **I**nformation Disclosure | Can sensitive data leak? | Verbose error messages, exposed stack traces, missing field-level authorization |
   | **D**enial of Service | Can the system be overwhelmed? | Missing rate limits, unbounded queries, no payload size limits, resource-intensive operations without throttling |
   | **E**levation of Privilege | Can a user gain unauthorized access? | Missing authorization checks, IDOR vulnerabilities, role bypass, privilege escalation through API chaining |

3. **Score each finding.**

   | Severity | Criteria |
   |----------|---------|
   | Critical (9-10) | Exploitable without authentication, data breach risk |
   | High (7-8) | Exploitable with low-privilege access, significant impact |
   | Medium (4-6) | Requires specific conditions, moderate impact |
   | Low (1-3) | Theoretical risk, minimal impact |

4. **Generate the threat model report:**

   ```markdown
   ## STRIDE Threat Model

   **Scope:** <full project or component name>
   **Date:** <date GMT>
   **Entry points analyzed:** <count>

   ### Attack Surface Map
   <list of entry points, data stores, trust boundaries>

   ### Findings by Category

   #### Spoofing
   | # | Threat | Severity | Affected Component | Mitigation |
   |---|--------|----------|-------------------|------------|

   #### Tampering
   ...

   #### Repudiation
   ...

   #### Information Disclosure
   ...

   #### Denial of Service
   ...

   #### Elevation of Privilege
   ...

   ### Summary
   | Category | Critical | High | Medium | Low |
   |----------|----------|------|--------|-----|

   ### Priority Actions
   <findings rated 8+ must be resolved before shipping>
   ```

5. **Gate check.** Findings rated 8/10 or higher are blocking. State them explicitly and recommend resolution before deployment.

---

## daily

Fast security gate for routine use. Three focused checks that catch the highest-impact issues with minimal time investment.

### When to use

- Before merging a significant PR.
- As a periodic health check during active development.
- After onboarding a new dependency or changing CI configuration.

### Steps

1. **Secrets archaeology.** Search git history for leaked credentials:
   - Run `git log --all --diff-filter=A --name-only` to find added files.
   - Search for patterns: API keys, tokens, passwords, private keys, connection strings.
   - Check `.env` files that were committed and later removed but remain in history.
   - Check for high-entropy strings in configuration files.
   - Report each finding with the commit hash, file path, and pattern matched.

2. **Dependency supply chain check.** Audit the dependency tree:
   - Run the project's audit command: `pnpm audit`, `uv run pip-audit`, `cargo audit`, or equivalent.
   - Check for known CVEs with severity >= HIGH.
   - Flag packages with fewer than 100 weekly downloads or a single maintainer.
   - Flag packages added in the last 30 days that have no prior release history.
   - Cross-reference lockfile integrity: verify the lockfile is committed and matches the manifest.

3. **CI/CD pipeline security review.** Audit workflow files:
   - Check for `pull_request_target` triggers with checkout of PR code, which enables code injection.
   - Check for secrets passed to steps that run user-controlled code.
   - Check for `actions/checkout` without pinned SHA versions.
   - Check for overly permissive `permissions` blocks.
   - Check for self-hosted runners on public repos.
   - Verify OIDC is used for cloud provider authentication where possible.

### Output

```
## Security Daily Report

**Date:** <timestamp GMT>
**Mode:** daily
**Duration:** <seconds>

### Secrets Archaeology
| Commit | File | Pattern | Severity |
|--------|------|---------|----------|
| <hash> | <path> | <type> | <1-10> |

### Supply Chain
| Package | Issue | CVE | Severity |
|---------|-------|-----|----------|
| <name> | <description> | <id or N/A> | <1-10> |

### CI/CD Pipeline
| File | Line | Issue | Severity |
|------|------|-------|----------|
| <path> | <line> | <description> | <1-10> |

### Verdict
<PASS: no blocking findings / BLOCK: N findings rated 8/10+>
```

---

## comprehensive

Deep scan that includes everything from daily mode plus OWASP Top 10, STRIDE threat modeling per component, and LLM/AI security review.

### When to use

- Monthly security review cadence.
- Before a major release or launch.
- After significant architecture changes.
- When onboarding a new team member who needs a security overview.

### Steps

1. **Run all daily checks.** Execute steps 1-3 from the daily mode.

2. **OWASP Top 10 audit.** Read `~/.claude/skills/security-patterns.md` as a vulnerability pattern catalog. Map each pattern to its OWASP category when checking the codebase:

   | Category | What to check |
   |----------|--------------|
   | A01: Broken Access Control | Authorization checks on every endpoint, IDOR prevention, CORS configuration |
   | A02: Cryptographic Failures | TLS usage, password hashing algorithms, sensitive data exposure in logs |
   | A03: Injection | SQL injection, XSS, command injection, LDAP injection, template injection |
   | A04: Insecure Design | Business logic flaws, missing rate limiting, missing abuse prevention |
   | A05: Security Misconfiguration | Default credentials, unnecessary features enabled, error messages leaking internals |
   | A06: Vulnerable Components | Outdated frameworks, known vulnerable versions, unmaintained dependencies |
   | A07: Authentication Failures | Weak password policies, missing MFA, session fixation, credential stuffing prevention |
   | A08: Data Integrity Failures | CI/CD pipeline integrity, unsigned updates, deserialization vulnerabilities |
   | A09: Logging Failures | Missing audit logs, sensitive data in logs, no alerting on security events |
   | A10: SSRF | Server-side request forgery via user-controlled URLs, DNS rebinding |

3. **STRIDE threat modeling.** For each major component identified in the codebase:

   | Threat | Question | What to check |
   |--------|----------|--------------|
   | Spoofing | Can an attacker pretend to be someone else? | Authentication mechanisms, token validation, certificate pinning |
   | Tampering | Can an attacker modify data in transit or at rest? | Input validation, integrity checks, signed payloads |
   | Repudiation | Can an attacker deny performing an action? | Audit logging, non-repudiation controls, tamper-evident logs |
   | Information Disclosure | Can an attacker access data they should not see? | Authorization boundaries, error messages, debug endpoints, log contents |
   | Denial of Service | Can an attacker make the system unavailable? | Rate limiting, resource quotas, payload size limits, algorithmic complexity |
   | Elevation of Privilege | Can an attacker gain higher access than intended? | Role checks, privilege escalation paths, default permissions |

   Produce a threat matrix entry for each component-threat combination that has a non-trivial risk.

4. **LLM/AI security review.** If the project uses LLMs or AI models:
   - Check for prompt injection vulnerabilities in user-facing inputs.
   - Check for sensitive data leakage through model context or logs.
   - Check for missing output sanitization on model responses.
   - Check for excessive permissions granted to AI agents or tools.
   - Check for missing rate limiting on model API calls.
   - Skip this section entirely if the project does not use LLM or AI features.

### Output

```
## Security Comprehensive Report

**Date:** <timestamp GMT>
**Mode:** comprehensive
**Duration:** <minutes>

### Daily Checks
<Include full daily report sections>

### OWASP Top 10 Audit
| Category | Status | Findings | Severity |
|----------|--------|----------|----------|
| A01: Broken Access Control | PASS/FAIL | <description> | <1-10> |
| A02: Cryptographic Failures | PASS/FAIL | <description> | <1-10> |
| ... | ... | ... | ... |

### STRIDE Threat Matrix
| Component | Threat | Likelihood | Severity | Mitigation |
|-----------|--------|-----------|----------|------------|
| <name> | <S/T/R/I/D/E> | <low/medium/high> | <1-10> | <action> |

### LLM/AI Security
| Finding | Severity | Mitigation |
|---------|----------|------------|
| <description> | <1-10> | <action> |
(or "Not applicable: no LLM/AI features detected.")

### Summary
**Total findings:** <count>
**Blocking (8/10+):** <count>
**Action items:** <numbered list>

### Verdict
<PASS: no blocking findings / BLOCK: N findings rated 8/10+ require remediation>
```

---

## trust

Read-only safety scan for untrusted projects. Detects install-time hooks, credential-theft patterns, exfiltration endpoints, CI/CD attack patterns, editor auto-run, dependency red flags, and binary anomalies. Produces a verdict: SAFE / SUSPICIOUS / HIGH-RISK / MALICIOUS.

### When to use

- First contact with a project from any external source: take-home, contractor delivery, open-source repo from an unknown maintainer, a dependency you are considering adding.
- Automatically invoked by `/onboard` Phase 0 before any architecture exploration begins.
- Before running `pnpm install`, `uv sync`, `cargo build`, or any build/setup command on a fresh clone.

### When NOT to use

- Projects you wrote yourself.
- Projects from a trusted internal source where the provenance chain is known.
- After installation has already happened. The scan is preventive; once installation runs, lifecycle scripts have already executed.

### Arguments

- No arguments: scan the current directory.
- `<path>`: scan the given directory.
- `--no-semgrep`, `--no-trivy`, `--no-gitleaks`: opt out of specific external tools even if installed.
- `--strict`: upgrade MEDIUM findings to HIGH. Useful when the project is highly untrusted.
- `--json`: emit machine-readable findings instead of the narrative report. Used by `/onboard` Phase 0.
- `--no-signatures`: skip `pnpm audit signatures` in step 12.

### Steps

1. **Detect ecosystem.** In parallel, check for `package.json`, `pyproject.toml`/`requirements.txt`/`setup.py`, `Cargo.toml`, `go.mod`, `Gemfile`, `composer.json`. Record the ecosystem set.

2. **Read manifest and lockfile.** For each detected ecosystem, read the manifest. Extract scripts/lifecycle hooks, dependency list with versions, declared maintainer. Read the lockfile if present.

3. **Scan install hooks.** Apply Section A patterns from [`trust-patterns.md`](trust-patterns.md) to the manifest scripts, at the severity each row assigns. A lifecycle value that pipes to `bash` or `sh`, or decodes with `base64 -d` or `xxd -r`, is CRITICAL; one that calls `curl`, `wget`, `node -e`, or `python -c` without a pipe to a shell is HIGH.

4. **Scan auxiliary install configs.** Read `.npmrc`, `.yarnrc`, `.yarnrc.yml`, `.pip.conf`, `setup.cfg` `[install]` section. Apply Section A patterns. Unusual registry is HIGH.

5. **Scan source files for code patterns.** Walk source directories. Skip `node_modules`, `.git`, `dist`, `build`, `vendor`, `target`, `out`. For each text file under 1MB, apply Section B patterns. Cluster matches per the verdict logic in [`trust-patterns.md`](trust-patterns.md).

6. **Scan for sensitive path references.** Grep all source files for the Section C strings. Any match in a non-test file is at least HIGH. Cluster with Section D matches in the same file escalates to CRITICAL.

7. **Scan for exfiltration endpoints.** Grep for Section D patterns. Discord/Telegram webhook URLs are CRITICAL on sight. Pastebin URLs are HIGH. Direct public IP addresses in production code are HIGH. URL shorteners are HIGH.

8. **Scan CI/CD files.** Walk [`.github/workflows/`](../../.github/workflows), `.gitlab-ci.yml`, `.circleci/`, `Jenkinsfile`. Apply Section E patterns. `pull_request_target` with PR-ref checkout is CRITICAL. Unpinned actions in sensitive workflows are MEDIUM. Secrets piped to network calls is CRITICAL.

9. **Scan editor configs.** Read `.vscode/settings.json`, `.vscode/tasks.json`, `.idea/workspace.xml`, `.envrc`, `.devcontainer/devcontainer.json`. Apply Section F patterns. Auto-run on folder open is HIGH. `eval` in `.envrc` is CRITICAL.

10. **Scan dependencies.** For each direct dependency in the manifest:
    - Query offline metadata first, lockfile, package cache.
    - If `pnpm` is available and the user has internet, run `pnpm view <name> time` to get age. Skip if offline.
    - Compare names against the typosquat list and known-malicious package list in [`trust-patterns.md`](trust-patterns.md).
    - Apply Section G patterns. Known-malicious match is CRITICAL. Age under 7 days is HIGH. Lockfile resolving to non-default registry is CRITICAL.

11. **Scan binaries.** Walk the tree for files with executable bits, non-text content, in non-build directories. Apply Section H patterns. Pre-compiled binaries in source-only directories are HIGH.

12. **Integrate external tools, auto-detect, parallel.**
    - `gitleaks` if installed: run `gitleaks detect --no-git --redact --report-path /tmp/gitleaks-trust.json`. Parse findings.
    - `semgrep` if installed and the `apiiro/malicious-code-ruleset` is reachable: run with that ruleset. Parse findings.
    - `trivy` if installed: run `trivy fs --scanners misconfig,secret,vuln .`. Parse findings.
    - `pnpm audit signatures` if `package.json` and `pnpm-lock.yaml` are present, network is available, and `--no-signatures` was not passed. Verifies Sigstore provenance.
    - Each tool's findings merge into the master findings list with mapped severity. Tools are opt-out via `--no-<tool>` if the user wants speed.

13. **Compute verdict.** Per the rules in [`trust-patterns.md`](trust-patterns.md) Verdict Logic section. Per-file aggregate first, then project aggregate.

14. **Render the report.** Markdown output. Header with verdict, scan duration, timestamp, ecosystem(s) detected, external tools used. Findings grouped by section. Each finding includes severity, file:line, pattern matched, rationale, recommendation. Closing summary with next-step recommendations: do not install, do not run, sandbox in Docker, abandon the project.

### Output format

```
## Trust Scan Report

**Verdict:** SAFE / SUSPICIOUS / HIGH-RISK / MALICIOUS
**Project:** <path>
**Duration:** <seconds>
**Timestamp:** <YYYY-MM-DD HH:MM GMT>
**Ecosystems:** <list>
**External tools used:** <gitleaks, semgrep, trivy, none>

### Worst findings

1. [CRITICAL] <one-line summary> at <file:line>
2. [HIGH] <one-line summary> at <file:line>
3. [HIGH] <one-line summary> at <file:line>

### Findings by section

#### Section A. Install-time hooks
| Severity | File:Line | Pattern | Rationale |
|----------|-----------|---------|-----------|

[Repeat for sections B through H]

### Verdict explanation
<One paragraph stating why the verdict landed where it did>

### Recommendations
<Numbered next steps. Vary by verdict:
- SAFE: proceed with onboarding.
- SUSPICIOUS: review findings before installing.
- HIGH-RISK: do not run any setup command. Inspect the flagged files manually.
- MALICIOUS: do not install, do not run, do not open in your IDE. Move to a Docker sandbox or delete the directory.>
```

### Rules

- Read-only. Never install dependencies, never run lifecycle scripts, never execute any script from the project.
- Never read `.env` or `*.local.env` files. Only `.env.example`.
- Never reveal actual secret values. Show file, line, pattern name. Mask the match.
- Never call paid external APIs without explicit user opt-in.
- Pattern list in [`trust-patterns.md`](trust-patterns.md) is the single source of truth. Updates land there.
- Verdict MALICIOUS has no override, because it comes only from a definitive IOC: a row rated CRITICAL or a Section C read paired with a Section D endpoint, never from clustering alone. Verdict HIGH-RISK, including a HIGH cluster, requires the user to type a confirmation phrase. SUSPICIOUS asks once and defaults to no.
- Skip scan directories: `node_modules`, `.git`, `dist`, `build`, `vendor`, `target`, `out`, `coverage`. Their contents are not analyzed.

---

## Rules

- Never install scanning tools without asking. Report availability.
- Never modify code or fix vulnerabilities automatically. Report and let user decide.
- Never expose actual secret values. Show file, line number, pattern name only.
- Always scan `.env.example`, never `.env` directly.
- Always detect package manager from lockfile.
- Never update packages without showing changes and getting approval.
- Never apply `pnpm audit --fix` overrides that cross a major version without explicit approval.
- If no vulnerabilities found, say so clearly.
- Classify by actual severity, not quantity.

## Common Rationalizations

- "`trivy` is missing, so install it and continue": installing a scanner needs the user's approval. Report what is available and ask.
- "`pnpm audit --fix` clears the report fastest": it can jump major versions and break the build. Show the changes and get explicit approval.
- "Showing the leaked key makes the finding concrete": the report carries file, line, and pattern name, with the match masked.
- "Run `pnpm install` first so the dependency scan sees `node_modules`": on an untrusted project, install runs lifecycle scripts. Run `trust` first, from manifests and lockfiles only.
- "Twelve LOW findings outweigh one HIGH": classify by actual severity, never by count.

## Red Flags

- Stop and recommend no install, no run, and a Docker sandbox when `trust` reaches a MALICIOUS verdict.
- Stop and require the confirmation phrase when `trust` reaches HIGH-RISK.
- Stop and redact when a draft finding contains a live secret value instead of a masked match.
- Stop and read `.env.example` when a step points at `.env` or `*.local.env`.
- Stop and ask for approval when a step would modify code, a lockfile, or an installed package.

## Verification

- The report names every layer or section scanned, the scanners used, and a GMT date.
- Each finding carries a severity, a `file:line` or commit hash, and the matched pattern name.
- `git status` shows no change made by the run, except packages the user approved under `deps update`.
- After `deps update`, a re-audit ran and reports no new vulnerabilities.
- `daily`, `comprehensive`, and `trust` end with an explicit verdict line.

## Related skills

- `/review` -- Security-aware code review of specific changes.
- `/test` -- Run tests to verify security fixes.
- `/infra docker` -- Docker container management.
