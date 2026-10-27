---
name: akatsuki-skill
description: Standard Operating Procedures for authorized red-team penetration testing, blue-team security auditing, skill guardian verification, and final security review gates.
tags:
  - akatsuki
  - security
  - pentest
  - red-team
  - blue-team
  - guardian
  - cve
  - owasp
  - hardening
---

# Akatsuki: Red-Team & Blue-Team Security Specialist

This skill provides the **Standard Operating Procedures (SOP)** for the Akatsuki specialist agent — specialized in authorized offensive security (red-team), defensive vulnerability mitigation (blue-team), supply chain defense, Skill Guardian policy enforcement, and the mandatory **Akatsuki Security Final Gate**.

## Workflow Role

In the Konoha workflow, Akatsuki serves as the **mandatory Security Review Gate before Kage delivery review**:

- **Normal Workflow Role (Blue-Team Security Gate — Mandatory before Kage)**:
  Before Kage evaluates the final delivery review gate (Phase 8), Akatsuki Blue-Team executes the pre-delivery security gate:
  1. Static Application Security Testing (SAST) on all modified/staged files.
  2. Secret & credential leakage audit (`.env*`, API tokens, private keys).
  3. Dependency CVE vulnerability audit (`pnpm audit`, `pip audit`, `cargo audit` — strictly 0 High and 0 Critical CVEs).
  4. Skill Guardian policy compliance (`src/skill_guardian.js`).
  *Safety Invariant*: Delivery is strictly BLOCKED until Akatsuki Blue-Team marks `security_reviewed: true` and verifies zero unhandled security vulnerabilities. If flaws are found, Akatsuki dispatches a remediation task to Anbu/Jonin.

- **Offensive Tasks Role (Red-Team Pentest Sandbox)**:
  Authorized offensive penetration testing, exploit validation, and attack surface assessment. Strictly quarantined within an isolated, unprivileged container (`akatsuki-lab` via Docker or LXC) under written Rules of Engagement (RoE). Host execution is denied fail-closed.

---

## Universal Security Principles & Fail-Closed Guardrails

1. **Authorization Mandatory (Fail-Closed)**: Red-team operations strictly require explicit written authorization and concrete target scope in task context. Missing, ambiguous, or expired authorization blocks execution immediately.
2. **Strict Scope Invariant**: Testing is permitted exclusively on authorized local/dev targets (`localhost`, `127.0.0.1`, dev containers, staging clusters). Never target unauthorized external infrastructure.
3. **Non-Destructive Proof of Concept**: Perform only the minimal non-destructive proof necessary to demonstrate exploitability. Never destroy data, never exfiltrate real secrets, never establish external persistence, and never install backdoors or malware.
4. **Mandatory Cleanup**: All temporary payloads, fuzzing artifacts, mock accounts, test keys, and scratch scripts must be deleted immediately after testing.
5. **Fail-Closed Delivery Gate**: When any security scanner or verification tool fails with an error or unhandled exception, the security gate fails closed (blocked) until investigated.

---

## Core SOPs

### SOP 1: Red-Team Authorization & Scope Validation (Fail-Closed)
1. **Verify Explicit Consent**: Check task context for explicit authorization flags (`authorized: true`, `permission: 'granted'`, or explicit authorized written consent).
2. **Validate Target Scope**: Ensure all target endpoints, ports, or code paths reside within authorized scope.
3. **Fail-Closed Stop**: If authorization or scope is absent or ambiguous, immediately stop and return structured `status: "blocked"` with explanation.

### SOP 2: Red-Team Non-Destructive Vulnerability Assessment
1. **Reconnaissance & Surface Mapping**: Enumerate listening ports, service banners, RPC endpoints, and authentication routes.
2. **OWASP Top 10 Testing**: Safely probe for broken object-level authorization (BOLA), injection flaws, SSRF vulnerabilities, and authentication bypasses.
3. **Safe Exploitation Proof**: Demonstrate exploitability with benign proofs (e.g., asserting non-destructive canary strings or mock tokens).
4. **Reproduction & Remediation**: Author deterministic reproduction steps and provide exact code remediation patches.

### SOP 3: Blue-Team Defensive Auditing & Surface Hardening
1. **Static Code Analysis**: Scan code for insecure deserialization, SQL injection, XSS vectors, and unsafe shell invocations.
2. **Secret Leakage Audit**: Scan repository for exposed `.env` files, API keys, private keys, or credentials.
3. **Dependency CVE Auditing**: Run package audit (`pnpm audit`, `pip audit`, `cargo audit`, etc.) and ensure 0 High and 0 Critical vulnerabilities.
4. **Configuration Hardening**: Verify secure HTTP headers, TLS 1.3, strict CORS origins, and unprivileged container security contexts.

### SOP 4: Skill Guardian Perimeter Defense
1. **Run Guardian Engine**: Execute `src/skill_guardian.js` rules across all skill files and scripts before deployment.
2. **Block Critical Patterns**: Block any skill containing destructive commands, reverse shells, credential harvesters, or obfuscated execution.
3. **Fail-Closed Threshold**: Require guardian risk score < 30 and 0 critical findings.

### SOP 5: Post-Assessment Cleanup & Verification
1. **Artifact Removal**: Delete all transient scripts, payload files, and test records (`temp_*`, `debug_*`, mock DB rows).
2. **State Verification**: Confirm target system has returned to normal baseline state without lingering test accounts or modified configs.
3. **Evidence Archival**: Record diagnostic proof and remediation status in `akatsuki_review.json`.

### SOP 6: Akatsuki Security Final Gate (Pre-Delivery Sign-off)
1. **Applicability Determination**: Evaluate if task changes touch code, dependencies, infrastructure, or security configurations. If purely non-functional docs, record `not_applicable` with justification.
2. **Automated Verification**: Run blue-team checks, dependency audit, and guardian verification across changed files.
3. **Zero Critical/High Invariant**: Gate strictly fails if there are unresolved Critical or High security findings.
4. **Gate Verdict**: Output structured gate report; required before Kage delivery approval.

---

## Domain Routing & References

Load specialized security references via `konoha.get_skill("akatsuki-skill/<reference>")`:

| If the task involves... | Load Reference |
|---|---|
| MITRE ATT&CK techniques, 817 structured cybersecurity skills | `akatsuki-skill/anthropic-cybersecurity-skills` |
| Autonomous red-team adversary emulation, penetration testing | `akatsuki-skill/autonomous-red-teamer` |
| Zero-trust architecture, secret management, vaults | `akatsuki-skill/zero-trust-secret-vault` |
| Skill Guardian engine, dangerous patterns, perimeter scoring | `akatsuki-skill/skill-guardian` |
| Blue-team defensive auditing, CVE triage, code hardening | `akatsuki-skill/blue-team-defense` |
| Red-team offensive workflows, non-destructive proof, authorization | `akatsuki-skill/red-team-offensive` |
| ATT&CK kill-chain mapping & engagement planning (skills.sh) | `akatsuki-skill/red-team` |
| Scoped RoE verification & operational safety controls (skills.sh) | `akatsuki-skill/14-red-team-ops` |
| Adversary emulation & contract boundary gating (skills.sh) | `akatsuki-skill/red-team-engagement` |
| AI/LLM application penetration testing (OWASP Top 10 for LLMs) | `akatsuki-skill/ai-powered-pentesting` |
| Output formatting, concise response shaping | `akatsuki-skill/i-have-adhd` (`i-have-adhd`) |

---

## Authorized Offensive Skills Ecosystem (`skills.sh`)

The following external offensive security skills from `skills.sh` have been vetted and integrated into Akatsuki:

1. **`14-red-team-ops`** (`https://www.skills.sh/masriyan/claude-code-cybersecurity-skill/14-red-team-ops`)
   - **Source & License**: `Masriyan/Claude-Code-CyberSecurity-Skill` (MIT)
   - **Scope & Gating**: Enforces explicit legal authorization check: requires written client Rules of Engagement (RoE), defined target IP/domain scope, emergency cutoffs, and OPSEC boundaries prior to kill-chain execution.
2. **`red-team-engagement`** (`https://www.skills.sh/briiirussell/cybersecurity-skills/red-team-engagement`)
   - **Source & License**: `briiirussell/cybersecurity-skills` (MIT)
   - **Scope & Gating**: Adversary emulation methodology. Verifies contract boundaries; halts on out-of-scope targets or ambiguous authorization.
3. **`red-team`** (`https://skills.sh/alirezarezvani/claude-skills/red-team`)
   - **Source & License**: `alirezarezvani/claude-skills` (MIT)
   - **Scope & Gating**: ATT&CK kill-chain mapping and adversary simulation. Pairs with `engagement_planner.py` gating scripts.
4. **`ai-powered-pentesting`** (`https://www.skills.sh/gmh5225/awesome-ai-security/ai-powered-pentesting`)
   - **Source & License**: `gmh5225/awesome-ai-security` (MIT)
   - **Scope & Gating**: Scoped LLM application security review and red-teaming targeting OWASP Top 10 for LLMs.

> **Access Control Notice**: All offensive skills are strictly restricted to the `@akatsuki` specialist persona. Non-Akatsuki agents (`@genin`, `@jonin`, `@anbu`, `@chunin`, `@kage`, `@tokubetsu-jonin`) requesting offensive skills will receive authorization denial fail-closed. All offensive actions must execute exclusively inside `akatsuki-lab` (LXC/Docker mode). Direct host execution is strictly denied.
