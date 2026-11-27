---
name: kio-cognitive
description: "Analyze architectural trade-offs from first principles, explain runtime code flows (HOW), trace Git decision history (WHY), and extract post-mortem lessons (REFLECT). Use when evaluating system design or investigating unfamiliar code."
license: MIT
metadata:
  author: Kio System / Toan Pham
  version: 1.1.0
---

# 🧠 Kio Cognitive & Thinking Powerhouse (`kio-cognitive`)

The meta-cognitive reasoning, architectural explanation, and deep reflection system of Kio Agent. Unifies 4 core cognitive disciplines:

---

## 🧭 4 Cognitive Modes Matrix

| Mode | Trigger Phrases / Context | Core Objective | Methodology |
| :--- | :--- | :--- | :--- |
| **1. `HOW`** | *"How does X work?"*, *"Code walkthrough"*, *"Where should I put this module?"* | Clarify runtime flow, architectural layering, and component mental models prior to refactoring. | Multi-tier codebase investigation, precise `path:line` citations, and data flow ASCII/Mermaid diagrams. |
| **2. `WHY`** | *"Why was this written this way?"*, *"Why did we choose Y?"*, *"Bug postmortem"* | Uncover factual decision rationale from historical artifacts without speculative guesswork. | Git archaeology (`git log -S`, `git log -L`, PR reviews, commit rationale, ADRs). |
| **3. `REFLECT`** | *"Reflect"*, *"Extract learnings"*, *"Review session insights"*, *"Save permanent lessons"* | Mine conversation transcripts for repeated friction or user corrections, persisting permanent rules. | Transcript analysis, failure mode detection, and updating `~/.kio/memory/global_learnings.md`. |
| **4. `IN-YOUR-OWN-WORDS`** | *"Do you understand my requirement?"*, *"Summarize the task"*, *"In your own words"* | Restate core business intent using concise, high-signal, empathetic language. | Deep listening, eliminating speculative noise, verifying 100% mutual alignment before executing. |

---

## 🛠️ Operational Guide Per Mode

### 1. 🔍 Mode `HOW`: Architecture & Runtime Flow Walkthrough
When asked how a system operates or before embarking on a complex refactor:
1. **Targeted Codebase Discovery (Read-only)**:
   - Inspect architectural overviews (`ARCHITECTURE.md` or `docs/codemap.md`).
   - Trace end-to-end execution flow: Entry point ➔ Routes/Controllers ➔ Services/Logic ➔ Database/Store.
2. **Delivery Format for Senior Engineers**:
   - **Mental Model**: High-level system principle in 1–2 sentences.
   - **Runtime Flow**: Step-by-step sequence from request to response (with exact `path:line` references).
   - **Ownership & Layering**: Explicit responsibility boundaries (e.g. business logic belongs in Services, never in Controllers or UI components).
   - **Gotchas & Caveats**: Hidden race conditions, edge-case failure modes, or architectural hazards.

---

### 2. 📜 Mode `WHY`: Git Archaeology & Technical Rationale
When investigating regressions or evaluating architectural decisions:
1. **Evidence-Based Historical Retrieval**:
   - Run `git log -S"<symbol>"` or `git log -L <start>,<end>:<file>` to find the genesis commit.
   - Read commit messages, PR descriptions, and author reasoning.
   - Cross-reference specifications (`docs/specs/`, `.spec-kit/`, ADRs).
2. **Attribution Integrity**:
   - Quote historical records verbatim.
   - Clearly delineate inferences: `[Inferred from commit context]`.
   - Explicitly acknowledge missing historical context rather than inventing fictional justifications.

---

### 3. 🪞 Mode `REFLECT`: Self-Learning & Memory Persistence
When consolidating lessons at a milestone boundary:
1. **Analyze Session Transcripts**:
   - Identify: User corrections, commands that required multiple attempts, or missed test assertions.
2. **Permanence Criteria**:
   - Retain only insights that **remain relevant in 6 months** and **permanently prevent regressions**.
   - Ignore ephemeral data (temporary commit SHAs, volatile version strings).
3. **Storage Destinations**:
   - Project-specific: `.kio/memory/` or project constitution.
   - Cross-project engineering principles: `~/.kio/memory/global_learnings.md`.

---

### 4. 🗣️ Mode `IN-YOUR-OWN-WORDS`: Deep Listening & Intent Restatement
When validating alignment on ambiguous or high-stakes business logic:
1. **Isolate First Principles**:
   - What fundamental problem is the user attempting to solve?
   - What are the non-negotiable success criteria vs negotiable implementation details?
2. **Restatement Protocol**:
   - Avoid regurgitating verbatim prompt text.
   - Synthesize the operational reality in your own words, highlighting potential edge cases before coding starts.
