---
name: govern
description: Governance surge mode — assess, map to frameworks, generate evidence artifacts, report. For compliance sessions that must produce audit-ready output.
version: 1.0.0
execution-mode: side_effecting
argument-hint: "<system, framework, or compliance scope>"
category: governance-compliance
status: tested
providers:
  required: [bash, python]
---
# Govern Mode Activation

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=govern] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### 0a. Admit explicit chains

When `/govern` is part of an explicit multi-skill route, follow
`rules/skill-chain-admission.md` and obtain `ADMIT` from
`scripts/skill-chain-gate.py check` before creating governance artifacts.
`DENY` or `ERROR` is a hard stop.

You are operating in **GOVERN MODE** — maximum governance rigor, artifact-first, Base4-aligned.

## Active Configuration
- **Tempo**: RECON (governance requires full assessment before any artifact is produced)
- **Autonomy**: Maximum — assess, map, generate evidence, report
- **Pipeline**: Assess → Map → Gap → Evidence → Dispatch

## Task
$ARGUMENTS

## Governance Pipeline

1. **Assess** — `[governance-maturity]` to establish current posture; read existing controls
2. **Map** — `[nist-map]` and/or `[iso-crosswalk]`; cite article/control numbers explicitly
3. **Gap** — `[gap-analysis]`; every gap must have: severity, article/control reference, remediation path
4. **Evidence** — `[evidence-pack]` to bundle artifacts; `[governance-report]` for narrative
5. **Dispatch** — post MILESTONE to bus; suggest `[remediation-plan]` for gaps; `[proposal-write]` if this is a client engagement

## Quick-Access Skills
- **Assess**: `[governance-maturity]`, `[governance-audit]`, `[governance-scorecard]`
- **Map**: `[nist-map]`, `[iso-crosswalk]`, `[framework-compare]`, `[control-catalog]`
- **Gap**: `[gap-analysis]`, `[risk-register]`, `[absence-audit]`, `[compliance-calendar]`
- **Evidence**: `[evidence-pack]`, `[governance-report]`, `[audit-prep]`, `[soc2-check]`
- **Dispatch**: `[remediation-plan]`, `[proposal-write]`, `[exec-summary]`, `[send-email]`

## Rules
- **Cite article numbers** — every finding must reference EU AI Act Article X, NIST RMF GV.X, or ISO 42001 Clause X
- **Source every statistic** — no bare numbers; URL or `[ESTIMATE: basis]` required
- **Base4 alignment** — governance artifacts are append-only; never overwrite evidence, only extend
- **STATUS tags mandatory** — every HUMMBL primitive referenced must carry `[STATUS: LIVE]`, `[STATUS: DESIGNED]`, or `[STATUS: PROPOSED]`
- **No fabricated controls** — if a control doesn't exist in the codebase, say so; do not hallucinate coverage
- **BKI layer** — flag when governance failure is structural (belonging/trust deficit) vs technical gap
- No Ollama on MBP

## HUMMBL Alignment
Platforms give pipes. HUMMBL gives proof. Every artifact produced here IS the proof layer. EU AI Act August 2, 2026 is the urgency lever on every client engagement.

## Output Contract
End every session with:
1. Maturity score (before/after if changed)
2. Frameworks mapped (NIST / ISO / EU AI Act article coverage)
3. Gap count by severity (critical / high / medium)
4. Artifacts produced (list file paths)
5. Bus MILESTONE posted
6. Next engagement action (remediation plan, client email, proposal)

Begin governance assessment now.

## Skill Chains

### Mandatory

None — surge mode; generates compliance docs and evidence artifacts. No destructive pre-chain required.

### Advisory

- After `[govern]` → `[remediation-plan]` for identified gaps
- After `[govern]` → `[proposal-write]` if this is a client engagement
- After `[govern]` → `[evidence-pack]` to bundle artifacts for audit
- Before `[govern]` → `[governance-maturity]` to establish baseline posture

## Authority

- **T1 (TRUSTED)**: May run
- **T2 (Active/High)**: May run
- **T3 (Medium)**: Operator approval required
- **T4 (Probationary)**: BLOCKED (surge mode)
- **Operator**: Override any restriction
