---
name: comprehensive-context-handover
description: Forensic, high-fidelity context handover for seamless continuation in a new chat. Produces a single Markdown transfer artifact plus reusable templates, preserving decisions, requirements, non-negotiables, and open loops without truncation by judgment. Not for code continuation unless explicitly stated.
allowed-tools: "Read, Write"
metadata:
  model: opus
  color: slate
  version: "2.1"
---

# Comprehensive Context Handover Protocol (CCHP) v2.1

## Part 1: Operational Logic

Name: comprehensive-context-handover  
Profile: Forensic Context Specialist  
Objective: Synthesize non-coding sessions into high-fidelity artifacts for near-perfect session resumption.

### Core Directives

1. Forensic Specificity
   - Preserve exact wording for load-bearing constraints (“must”, “never”, “only”).
   - Do not truncate by judgment.

2. Epistemological Tracking
   - Use [G/C/P/K] tags to label maturity of key insights:
     - [G] Genesis (novel discovery)
     - [C] Custom (emerging pattern)
     - [P] Product (proven approach)
     - [K] Commodity (standard knowledge)

3. Ledger Rigor
   - Maintain:
     - Decision Log (the why)
     - Requirements Ledger (the what)

4. Antifragile Ordering
   - Structure by priority so critical data survives truncation:
     - Orientation → Non-Negotiables → Decisions → Requirements → Open Loops → Context

### Trigger Instructions

When invoked via “handover”, “checkpoint”, or “save context”:

- Scan the full conversation for unique terminology (e.g., Syriac, Latin, Intel codes).
- Identify 3–10 “Stop Re-Asking” points.
- Generate the artifact using the structured templates in Parts 2 and 3.

### Deliverables

- **Deliverable Format (Mandatory)**:
  - All outputs produced by this skill MUST be delivered as a downloadable Markdown (.md) file.
  - Inline summaries or partial outputs are not acceptable substitutes.

---

## Part 2: Reusable Artifact Template

```text
═══════════════════════════════════════════════════════════════════
CONTEXT TRANSFER ARTIFACT v2.1
═══════════════════════════════════════════════════════════════════
Generated: [ISO timestamp]
Session ID: [if available]
Transfer Type: [○ continuation | ◐ pivot | ● fresh start]
Domain: [context]
Code Continuation Required: [yes/no — default no unless explicit]

───────────────────────────────────────────────────────────────────
§ 1. IMMEDIATE ORIENTATION [SCAN FIRST]
───────────────────────────────────────────────────────────────────

MISSION
[One sentence: what is being done and why it matters]

STATUS
State: [✓ resolved | ⧗ in-progress | ⚠ blocked | ↻ iterating]
Progress: [where things stand]
Momentum: [↑ accelerating | → steady | ↓ stalled]

NEXT ACTION
[Exact next step when conversation resumes]

STOP RE-ASKING
- [Questions the receiver must NOT re-ask]

───────────────────────────────────────────────────────────────────
§ 2. USER NON-NEGOTIABLES [LOAD-BEARING]
───────────────────────────────────────────────────────────────────

- Format constraints:
- Scope constraints:
- Behavior/tone constraints:
- Explicit “must / never” rules:

───────────────────────────────────────────────────────────────────
§ 3. DECISION LOG [ANTI-REHASH]
───────────────────────────────────────────────────────────────────

| Decision | Rationale | Alternatives Rejected | Tradeoff Accepted | Type | Status |
|----------|-----------|-----------------------|------------------|------|--------|

Type: explicit | implicit | emergent
Status: final | tentative | pending

───────────────────────────────────────────────────────────────────
§ 4. REQUIREMENTS LEDGER [VERIFIABLE]
───────────────────────────────────────────────────────────────────

| Requirement | Scope | Priority | Acceptance Criteria | Status |
|-------------|-------|----------|---------------------|--------|

───────────────────────────────────────────────────────────────────
§ 5. ARTIFACTS & OUTPUTS [WHAT EXISTS]
───────────────────────────────────────────────────────────────────

Created:
- [Artifact]: [what it is + why it matters]

Referenced:
- [Resource]: [why it matters]

Tools Used:
- [Tool]: [how used + outcome]

───────────────────────────────────────────────────────────────────
§ 6. CRITICAL CONTEXT [INTERPRETIVE LAYER]
───────────────────────────────────────────────────────────────────

Key Insights [G/C/P/K]:
- [G] Genesis insight
- [C] Emerging pattern
- [P] Proven approach
- [K] Commodity knowledge

Constraints (Technical/Resource/Organizational/Ethical):
- Technical:
- Resource:
- Organizational:
- Ethical:

Uncertainty Map (Known unknowns/Fragile assumptions/Risks):
- Known unknowns:
- Fragile assumptions:
- Risks:

Values at Stake:
- [What matters beyond completion]

───────────────────────────────────────────────────────────────────
§ 7. OPEN LOOPS [FORWARD MOMENTUM]
───────────────────────────────────────────────────────────────────

Unresolved Questions:
- [ ]

Blockers:
- [ ]

Pending Inputs:
- [ ]

Hypotheses to Test:
- [ ]

───────────────────────────────────────────────────────────────────
§ 8. CONVERSATION HISTORY [OPTIONAL DEPTH]
───────────────────────────────────────────────────────────────────

<details>
<summary>Chronological narrative</summary>

Act I: Problem Formation
Act II: Exploration & Development
Act III: Current State

Notable Quotes:
- “…”

</details>

───────────────────────────────────────────────────────────────────
§ 9. TRANSFER METADATA [SYSTEM LEVEL]
───────────────────────────────────────────────────────────────────

Provenance:
Context Window Pressure: [○ | ◐ | ●]
Completeness: [% + what’s missing]
Verification: [✓ reviewed | ⚠ unverified | ⧗ partial]

Omissions (if any):
- [What was omitted and why]

───────────────────────────────────────────────────────────────────
§ 10. RECEIVER START PROMPT
───────────────────────────────────────────────────────────────────

Read this artifact fully.
Respond with:
1) Mission (in your words)
2) Current status
3) Immediate next action

Do not rehash decisions already logged.

═══════════════════════════════════════════════════════════════════
§ TRANSFER READY—Review for accuracy before sharing.
═══════════════════════════════════════════════════════════════════

---

## Part 3: Generator Prompt

Generate a CONTEXT TRANSFER ARTIFACT using the Comprehensive Context Handover Protocol (CCHP) v2.1.

Hard rules:
- Forensic detail. Do not omit “minor” constraints.
- No truncation by judgment. Only deduplicate exact repeats.
- Preserve exact wording when load-bearing.
- If anything is omitted, list it explicitly in an Omissions section.
- This is NOT for code continuation unless explicitly stated.

Use the Context Transfer Artifact v2.1 template exactly.
Fill every section. If something does not apply, write “N/A”.

Priority order if truncation occurs:
1) Immediate Orientation
2) User Non-Negotiables
3) Decision Log
4) Requirements Ledger
5) Open Loops
6) Critical Context
7) Artifacts & Outputs
8) Conversation History
9) Transfer Metadata

After generating, append:
“§ TRANSFER READY—Review for accuracy before sharing.”