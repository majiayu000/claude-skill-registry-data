---
name: safety-scan
description: "Active security enforcement — scan for vulnerabilities (SAST), secrets (Gitleaks), insecure deps (SCA) before commit/deploy. Use when: scan security, check vulnerabilities, audit code, gitleaks, semgrep, finding secrets."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/security/safety-scan.skill.md"
  tags: "security"
  core: "true"
  context_cost: "medium"
---
# Safety Scan Skill

## Goal
Prevent "Insecure Code" from entering the codebase by strictly enforcing security checks.

## Flow

### Steps
## 1. Credentials Check (Gitleaks)
**Command**: `gitleaks detect --source . -v` (or regex fallback)
**Check**: Are there API Keys, Tokens, or Passwords in the diff?
*   *If Found*: **BLOCK COMMIT**. Auto-delete or `.gitignore` the secret. Alert Human.

### 2. Static Analysis (SAST)
**Command**: `semgrep scan --config=p/security-audit` (if installed) OR `npm audit` / `pip-audit`.
**Check**: High-Severity vulnerabilities (RCE, SQLi, XSS).
*   *If Found*: **BLOCK COMMIT**. Invoke `ci-autofix` to patch.

### 3. Logic & PII Check
**Action**: LLM Review of the diff.
*   "Does this code log User PII?"
*   "Does this code execute arbitrary system commands (`exec`, `eval`)?"
*   *If Risky*: Add `# TODO: SECURITY REVIEW` comment and flag in `project/TASKS.md`.

## Output
*   **PASS**: "No critical issues found."
*   **FAIL**: "Blocking Commit. Found [N] Issues."

## Security & Guardrails

### 1. Skill Security (Safety Scan)
- **Scan Configuration Tampering**: The agent must verify the integrity of the scanning configuration files (e.g., `p/security-audit.yml` or `.gitleaks.toml`) before execution. If the agent detects unauthorized modifications designed to weaken the scan (e.g., whitelisting the entire `src/` directory), it must abort the scan and raise a critical alert.
- **Autofix Exploitation**: When invoking `ci-autofix` to patch SAST vulnerabilities, the agent must ensure the suggested patch does not introduce a secondary, harder-to-detect vulnerability (like mitigating XSS but introducing a DOM clobbering bug). All automated security patches must require secondary human code review.

### 2. System Integration Security
- **Pipeline Bypass Prevention**: The agent must mandate that the `Safety Scan` is a required, non-bypassable status check in the Version Control System (VCS) for all branches merging into `main` or `production`. It must flag any repository configuration that allows an administrator to "force merge" past a failed security scan.
- **Fail-Closed Scanning**: If the SAST tool (`semgrep`) or Secret Scanner (`gitleaks`) fails to execute due to a licensing issue, network timeout, or misconfiguration, the CI pipeline MUST fail-closed. The agent must enforce that a lack of scan results is treated as a failed scan, never a pass.

### 3. LLM & Agent Guardrails
- **Logic Review Hallucination**: During the "Logic & PII Check" (Step 3), the LLM might hallucinate a vulnerability where none exists (False Positive) or miss a subtle logic flaw (False Negative). The agent must qualify its logic review findings with confidence scores and explicitly state that LLM review does not replace deterministic SAST/DAST scanning.
- **Adversarial Diff Manipulation**: An attacker might submit a Pull Request that intentionally includes highly complex, obfuscated code or a massive diff designed to exhaust the LLM's context window, causing it to truncate the review and miss a hidden backdoor. The agent must enforce strict chunking or reject diffs exceeding maximum token limits for security review.
