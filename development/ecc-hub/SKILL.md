---
name: ecc-hub
description: On-demand bridge and catalog
---
# ECC Hub: Specialized Skills & Agent Catalog (`ecc-hub`)

The **ECC Hub** integrates the complete Everything Coding Companion (ECC) repository into Antigravity, providing access to **285+ production-grade engineering skills** and **120 specialized agent personas** stored locally at `C:\Users\goldl\.gemini\ecc\`.

---

## 1. How to Discover and Use ECC Skills

All ECC skills are stored at:
`C:\Users\goldl\.gemini\ecc\skills\<skill-name>\SKILL.md`

### 1. Dynamic Discovery via CLI:
```powershell
python "C:\Users\goldl\.gemini\config\skills\ecc-hub\scripts\ecc_hub.py" search "<technology-or-topic>"
```
Examples:
- `search "react"` -> returns `react-patterns`, `react-performance`, `react-testing`, `react-reviewer`
- `search "flutter"` -> returns `dart-flutter-patterns`, `flutter-dart-code-review`, `flutter-reviewer`
- `search "rust"` -> returns `rust-patterns`, `rust-testing`, `rust-reviewer`
- `search "kubernetes"` -> returns `kubernetes-patterns`, `docker-patterns`
- `search "security"` -> returns `security-review`, `security-scan`, `security-reviewer`

### 2. Activating an ECC Skill:
When working on a specific framework, simply view its skill instructions using `view_file`:
- Path: `C:\Users\goldl\.gemini\ecc\skills\<skill-name>\SKILL.md`

---

## 2. How to Launch ECC Specialized Sub-Agents

All 120 specialized agent personas are stored at:
`C:\Users\goldl\.gemini\ecc\agents\<agent-name>.md`

### 1. Inspecting an Agent:
```powershell
python "C:\Users\goldl\.gemini\config\skills\ecc-hub\scripts\ecc_hub.py" agent "<agent-name>"
```

### 2. Spawning via `invoke_subagent`:
When a task calls for specialized expertise (e.g. `security-reviewer`, `code-reviewer`, `architect`, `build-error-resolver`, `database-reviewer`):
1. Read the agent's prompt from `C:\Users\goldl\.gemini\ecc\agents\<agent-name>.md`.
2. Launch a sub-agent with `invoke_subagent` using the prompt.
3. The sub-agent delivers its deep technical report back to the parent agent.

---

## 3. Deactivated & Neutralized Conflicting Skills

To guarantee 100% stability, zero token bloat, and total harmony with our global rules, the following 8 ECC skills are **deactivated and superseded** by our native core protocols:

| Deactivated ECC Skill | Native Core Protocol in Charge | Reason for Superseding |
| :--- | :--- | :--- |
| `context-budget` | `Sub-Agent Anti-Hallucination Protocol` | ECC's skill forces skipping file reads, which causes sub-agent mistakes. |
| `verification-loop` | `loop-debug` | Native `loop-debug` handles Test-Diagnose-Fix-Retest + explicit `Debug` confirmation. |
| `autonomous-loops` | `loop-debug` + `end-to-end-executor` | Native protocols execute commands directly without multi-turn CLI stops. |
| `continuous-learning` / `v2` | `experience-learner` | Native `experience-learner` uses persistent global store `troubleshooting_history.md`. |
| `delivery-gate` | `request-completeness-sentinel` + `code-completeness-debugger` | Complete symbol, function, and requirement checklist enforcement. |
| `operator-approval-loop` | `end-to-end-executor` | Banned: stops to ask user permission; native protocol executes 100% autonomously. |
| `safety-guard` | Universal Mandate 1 (Zero Refusal) | Banned: triggers trivial refusals and overly aggressive directory fencing. |
