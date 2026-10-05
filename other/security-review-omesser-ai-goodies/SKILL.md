---
name: security-review
description: Run a live security and compliance scan on the current repo — Python, Terraform, Kubernetes, JavaScript, Go, Rust, Shell, Helm, and secrets — applying the Company SDLC, Change Management, and Generative AI Use and Oversight compliance framework, and write a structured report.
disable-model-invocation: true
allowed-tools: Bash(*), Write(*)
---

You are performing a live security and compliance scan grounded in company's Secure SDLC Policy, Change Management Policy, and Generative AI Use and Oversight Policy for Engineering. Run the scans below, interpret the results, apply the compliance framework, and write a full Markdown report to a local file.

---

## Phase 0 — Determine scan scope

Run the following to understand git context:

```bash
git rev-parse --abbrev-ref HEAD
git status --short
git log --merges -1 --format="%H %s" 2>/dev/null || echo "(no merges)"
gh pr view --json number,title,baseRefName,headRefName 2>/dev/null || echo "(not a PR)"
```

**Decision rules — apply the first that matches:**

1. **PR branch** (`gh pr view` returned data): scope to PR diff. Use `--changed-only`; base is the PR's base branch.

2. **Feature branch** (branch name is not main/master/trunk, and commits exist ahead of main): scope to diff vs main. Use `--changed-only`.

3. **Main/master with uncommitted changes** (`git status --short` is non-empty):
   Compute `SCOPE_FILES`:
   ```bash
   git diff HEAD --name-only
   git diff --cached --name-only
   ```
   Do **not** use `--changed-only` — on main it scopes to committed changes vs main, which is empty and misses uncommitted work. Run a full scan in Phase 2; filter Phase 3 interpretation to `SCOPE_FILES` only.

4. **Main/master, clean working tree**: stop and ask the user before running — present these options:

   a. **Recent commits** *(recommended)* — scope to what actually changed recently. Compute:
      ```bash
      git log --merges -1 --format="%H"
      # If a merge SHA is found, files from that merge:
      git diff <sha>^1 <sha> --name-only
      # No merge found — fall back to last 5 commits:
      git diff HEAD~5..HEAD --name-only
      ```
      Store as `SCOPE_FILES`. Run a full scan; filter Phase 3 to `SCOPE_FILES`. Avoids surfacing pre-existing issues from earlier work.

   b. **Full repo** — scan everything. Expect findings unrelated to recent changes. Use for a deliberate comprehensive audit.

   c. **Specific path** — ask the user to specify a directory or file list.

   Wait for the answer before proceeding.

Record the scope mode and `SCOPE_FILES` (where applicable) — they govern Phase 2 flags and Phase 3 filtering.

---

## Phase 1 — Show change scope

Show the files in scope before scanning starts. Pick the right diff for the scope determined in Phase 0:

- **PR or feature branch**: `git diff --stat main...HEAD`
- **Main + uncommitted changes**: `git diff HEAD --stat; git diff --cached --stat`
- **Main + recent commits**: `git diff <sha>^1 <sha> --stat` (merge SHA from Phase 0), or `git diff HEAD~5..HEAD --stat` if no merge
- **Main + full repo**: skip — no pre-scope diff applies
- **Main + specific path**: display the path the user specified

---

## Phase 2 — Run security scans

Run the scan scripts directly from the skill directory using `${CLAUDE_SKILL_DIR}`:

```bash
# PR or feature branch — use changed-only scoping
bash ${CLAUDE_SKILL_DIR}/scripts/scan.sh --changed-only --save-reports

# Main branch (all cases) — --changed-only is empty on main (HEAD == main); always omit it
bash ${CLAUDE_SKILL_DIR}/scripts/scan.sh --save-reports
```

**Available flags:**
- `--changed-only` — scope to files changed vs main
- `--only secrets,python,rust` — run only named scanners
- `--skip trivy,ml` — skip named scanners
- `--save-reports` — write each scanner's raw output to `./.security_scan/.reports/<name>.txt`
- `--fail-on-findings` — exit 1 if any HIGH/CRITICAL finding is recorded
- `--timeout N` — per-tool timeout in seconds (default 120)

`scan.sh` auto-detects project types, runs all applicable tools in parallel, and prints a summary of skipped tools. Interpret its output section by section in Phase 3.

---

## Phase 3 — Interpret scan results

**Rust lane (when `Cargo.toml` detected):** treat `cargo audit` / RustSec IDs as first-class SCA (peer of pip-audit / govulncheck). Prefer those over duplicate Trivy Cargo.lock hits for the same advisory. `cargo deny` full check runs when `deny.toml` exists; otherwise advisories-only. `cargo geiger` and security-oriented `clippy` are **informational** — summarize unsafe hotspots and real clippy hits; do not auto-block solely on geiger counts.


**Scope filter**: if `SCOPE_FILES` was set in Phase 0 (main + uncommitted changes, or main + recent commits), report only findings in those files. Findings in files outside `SCOPE_FILES` are pre-existing issues outside the scope of this review — note their count in a single line ("N pre-existing findings in out-of-scope files — not reported") and do not list them.

For each scan that ran, produce a summary section:

**Per-scan summary format:**
- Tool name + what was scanned
- Finding counts by severity: Critical / High / Medium / Low
- **Noteworthy findings** (Critical and High only, or anything that looks real):
  - Rule ID and short description
  - File:line
  - Plain-language explanation of the risk
  - Assessment: genuine issue, needs context, or likely false positive — and why
- **Patterns**: repeated rule types suggest a systemic issue; call it out as a class rather than listing every instance
- **Verified secrets** from TruffleHog are always blocking regardless of other findings

Apply company's patch SLAs when flagging unresolved findings:
| Severity | Must fix within |
|---|---|
| Critical | 1 week |
| High | 1 month |

---

## Phase 3.5 — AI / GenAI compliance (GenAI Use Policy)

Skip this phase if the scan output shows "No AI/agentic artifacts detected."

Otherwise, the repo contains AI tooling (skills, MCP servers, agent config, or AI SDK usage) and must meet company's Generative AI Use and Oversight Policy. Work through the scan output section by section.

### Artifacts inventory

List every AI artifact found: CLAUDE.md, AGENTS.md, .mcp.json, .claude/settings*.json, skill files, files using AI SDKs. This is the surface area being evaluated.

### Tool approval
- [ ] Every AI service in use is company-sanctioned and accessed under a corporate account (not personal accounts)
- [ ] Any LLM provider confirmed to not train on user/prompt data (enterprise tier or documented DPA)
- [ ] No unapproved third-party AI services introduced by this change

Flag: any new SDK dependency or API endpoint pointing to an AI service not previously in use — it needs approval before merge.

### Secrets and sensitive data in AI context
From the scan's "Secrets check" and "Sensitive data in prompt context" outputs:
- [ ] No credentials, API keys, or tokens embedded in skill files, AGENTS.md, CLAUDE.md, or MCP configs
- [ ] No customer data, personal data, or proprietary configs passed into AI prompts without explicit authorization
- [ ] Privacy by design: prompts use anonymized or synthetic data where possible, not real customer records

Any hit from the secrets grep in AI config files is **blocking** — same as a secret in source code.

### MCP server scope
From the scan's "MCP server configurations" output:
- [ ] Each MCP server exposes only the minimum tools necessary (principle of least privilege)
- [ ] Shell execution tools (bash, run_command) have explicit scope documented — not granted by default
- [ ] Filesystem access restricted to specific paths, not root (`/`) or home (`~`)
- [ ] No MCP server connects to external services without documented business justification and approval

Any broad shell or root filesystem grant flagged by the scan is a **High** finding requiring documented justification.

### Agent permissions
From the scan's ".claude/settings*.json" output:
- [ ] `allowedTools` is scoped to what the agent actually needs — not a blanket allow-all
- [ ] Hooks (PreToolUse, PostToolUse, etc.) do not execute arbitrary external scripts or exfiltrate data
- [ ] No `dangerouslyAllowAll` or equivalent permission bypass

### Skills and prompt hygiene
From the scan's "Skill files: prompt injection patterns" output:
- [ ] No instruction-override patterns in skill prompts (no "ignore previous instructions", "act as if", "bypass")
- [ ] Skills that accept user input sanitize it before interpolating into prompts
- [ ] Skills with Bash/shell access document why that access is required

### Human oversight and documentation (policy requirement — manual check)
The policy requires that **all AI-generated code undergoes thorough human review** before use:
- [ ] PR description or commit messages document that AI-assisted code was reviewed for correctness, security flaws, and license issues
- [ ] AI-generated code is covered by the SAST/SCA scans run in Phase 2 (not exempt)
- [ ] No AI-generated code in core security functions or critical system code without explicit Security Engineering sign-off

### Prohibited uses (manual check)
- [ ] AI is not being used to process personal data, customer secrets, or proprietary configs without explicit authorization
- [ ] AI is not solely responsible for core security logic (auth, encryption, access control) — human-written and reviewed

### Logging
- [ ] AI interactions are logged (SOC 2 requirement) — confirm the AI tool used has audit logging enabled under the corporate account

---

## Phase 4 — Classify the change

Apply exactly one category from company's Change Management Policy:

| Category | Criteria |
|---|---|
| **Low-Risk / Standard** | Predefined, repeatable, reversible, no material security/data/architecture/availability risk. Pre-approval via CI/repo rules sufficient. |
| **Normal / Material** | Production or production-impacting; not emergency and not low-risk. Requires EM or PO approval before implementation. |
| **Emergency** | Urgent: restoring service, remediating active security risk, fixing severe defect. Can proceed before full approval with EM authorization; must be documented ≤ 5 business days post-implementation. |

---

## Phase 5 — Check security triggers

**Threat modeling required** (SDLC §3.2) — check all that apply:
- [ ] New cloud/edge infrastructure or major architectural change
- [ ] New externally facing cloud service
- [ ] New data pipeline touching customer data
- [ ] Change affecting authentication, secrets, or network boundaries

If any triggered: STRIDE/attack-tree threat model required. Deliverable: approved threat model + documented controls in design spec.

**Security Engineering review required** (Change Management §6.3) — check all that apply:
- [ ] Authentication or authorization
- [ ] Secrets or encryption
- [ ] Network boundaries
- [ ] Logging or monitoring
- [ ] Vulnerability remediation or incident response tooling
- [ ] New or modified AI/agentic tooling (MCP servers, skills, agent permissions, AI SDK integrations)

---

## Phase 6 — Compliance gates

### Code review
- [ ] Peer review completed
- [ ] Security checklist applied during review
- [ ] High-risk areas received dedicated security-focused review

### Scan coverage (tie back to Phase 2 results)
- [ ] SAST ran and passed (or findings triaged)
- [ ] SCA / dependency scan ran (Dependabot, npm audit, govulncheck, or Trivy)
- [ ] Secrets scan ran — no verified secrets
- [ ] IaC scan ran (if Terraform/K8s present)
- [ ] Container scan: ECR built-in scanning (if containers involved)

### Secrets and credentials
- [ ] No secrets in code, config repos, or CI logs
- [ ] Secrets managed via cloud key vault, secret manager, or environment-restricted injectors
- [ ] At rest: AES-256; in transit: TLS 1.2+ minimum; keys in managed KMS

### Deployment
- [ ] Artifacts signed (Docker images, Python packages, ML models, firmware)
- [ ] All Critical/High findings resolved or explicitly risk-accepted with documented justification

### Normal/Material changes — additionally
- [ ] Change record with: description, business reason, risk/impact assessment, test evidence, approval, implementation plan, rollback plan, links to PR/ticket/CI artifacts
- [ ] Approver ≠ implementer (or documented compensating control)
- [ ] Temporary elevated access is time-bound

### Emergency changes — additionally
- [ ] EM or above authorization on record
- [ ] Change scoped to minimum necessary
- [ ] Post-implementation review scheduled

### Compliance audit trail
Confirm artifacts are stored and auditable for ISO 27001/27034, SOC 2 Type II, NIST SP 800-53:
- [ ] Design docs, threat models, test results, approvals all linked from the change record

---

## Phase 7 — Write report and clean up

### Write the report

Determine the report filename using a full timestamp so reruns don't overwrite each other (ask the shell: `date +%Y-%m-%dT%H-%M-%S`). Format: `security-review-YYYY-MM-DDTHH-MM-SS.md`.

Write the full report to that file in the current working directory (the repo root directory). The report must include every section below — do not omit sections, do not truncate findings.

```markdown
# Security & Compliance Review — [repo name] [branch/PR] [YYYY-MM-DDTHH:MM:SS]

## Scan scope
[Branch or PR reviewed, whether --changed-only was used, files in scope]

## Change summary
[One paragraph: what changed and why it matters from a security perspective]

## Scan results

### [Tool name]
- **Scanned:** [what]
- **Findings:** Critical: N | High: N | Medium: N | Low: N
- **Noteworthy findings:**
  - `[RULE-ID]` — [description] (`file:line`)
    - Risk: [plain-language explanation]
    - Assessment: [genuine / needs context / likely FP] — [why]
- **Patterns:** [any systemic issues, or "None"]

[Repeat for each tool that ran]

### Skipped scanners
[List tools that were not installed, with install hints]

## AI / GenAI compliance
[N/A — no AI artifacts | or: full checklist results from Phase 3.5]

## Change classification
**[Low-Risk / Normal/Material / Emergency]** — [one-sentence rationale]

## Security triggers

### Threat modeling
**[Required / Not required]** — [reason]
[If required: what STRIDE/attack-tree work is needed]

### Security Engineering review
**[Required / Not required]** — [reason]
[If required: which triggers fired]

## Compliance gate results
| Gate | Status | Notes |
|---|---|---|
| Peer review | ✅ / ❌ / ⚠️ | |
| SAST | ✅ / ❌ / ⚠️ | |
| SCA / dependency scan | ✅ / ❌ / ⚠️ | |
| Secrets scan | ✅ / ❌ / ⚠️ | |
| IaC scan | ✅ / ❌ / N/A | |
| Container scan | ✅ / ❌ / N/A | |
| No secrets in code | ✅ / ❌ | |
| Artifacts signed | ✅ / ❌ / N/A | |
| Critical/High resolved | ✅ / ❌ / ⚠️ | |
| Change record complete | ✅ / ❌ / N/A | |
| Audit trail | ✅ / ❌ / ⚠️ | |

## Findings requiring action

| # | Severity | Description | File:line | Required action | SLA |
|---|---|---|---|---|---|
| 1 | CRITICAL | ... | ... | ... | 1 week |
| 2 | HIGH | ... | ... | ... | 1 month |

[If no findings: "No Critical or High findings requiring action."]

## Verdict

**[✅ Approved | ❌ Blocked | ⚠️ Conditional]**

[One paragraph: overall assessment. If Blocked: N findings listed above must be resolved. If Conditional: list what must happen before merge/deploy. If Approved: brief summary of clean areas.]

---
*Generated by /security-review — Company Secure SDLC*
```

### Clean up

After the report file has been written and confirmed, remove the scan reports directory:

```bash
rm -rf ./.security_scan
```

This removes the `.reports/` output written by `--save-reports`. The only artifact that remains is `security-review-YYYY-MM-DDTHH-MM-SS.md` in the repo root.

Tell the user: "Report written to `security-review-YYYY-MM-DDTHH-MM-SS.md`."

Do not approve if any verified secret was found, or if any Critical/High finding is unresolved without a documented risk-acceptance.
