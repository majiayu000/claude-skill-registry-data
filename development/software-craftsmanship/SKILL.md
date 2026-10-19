---
name: software-craftsmanship
description: Clean code, robust architecture, no test slop. Foundational skill for high-quality software engineering, code structure, and reviews.
tier: core
version: 0.1.0
kind: reference
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Software Craftsmanship Skill 🛠️✨

> **Clean Code. Robust Architecture. No Test Slop.**
>
> A foundational skill for high-quality software engineering. Use this skill when writing code, structuring projects, or conducting code reviews.

## Usage

```bash
# Read the core principles
read skills/software-craftsmanship/SKILL.md
```

## Rules of Engagement 🛡️

### 1. NO_TEST_SLOP 🚫🧪
- **Definition:** Tests that verify only UI structure (snapshots), boilerplate, or mocked behavior without testing business logic.
- **Rule:** Only write tests for **Core Logic** (State Management, Data Transformation, Protocols).
- **Why:** Avoid bloated codebases, fragile tests, and maintenance nightmares.
- **Action:** If you see a test that doesn't verify a critical path -> Delete/Refactor it.

### 2. FORWARD_MOMENTUM 🚀
- **Definition:** Every interaction must yield a tangible artifact or decision.
- **Rule:** Do not loop in discussion. Create a file, run a command, or make a decision.
- **Why:** Action > Analysis Paralysis.
- **Action:** If stuck -> Execute `forward-momentum` skill logic.

### 3. OWN_YOUR_TOOLS 🔧
- **Definition:** Relying on magic or external services for critical build steps.
- **Rule:** Write your own scripts (e.g., `generate_proto.sh`) for reproducibility.
- **Why:** Robustness, independence, and clarity.
- **Action:** If a task is complex -> Script it.

### 4. GIT_ETIQUETTE 🔀🐙
- **Definition:** Professional collaboration via Git and GitHub.
- **Rule 1 (Branches):** Never push directly to `main`. Use `feat/<name>` or `fix/<name>`.
- **Rule 2 (PR Structure):** **Explain the Why, What, and Outcome.**
    - **Context:** Why is this necessary?
    - **Changes:** What implementation details matter?
    - **Impact:** What is the result?
    - *A PR without this context is unacceptable.*
- **Rule 3 (Review):** Self-review your diff before requesting review. Don't waste the reviewer's time with typos or debug logs.
- **Rule 4 (PR Metadata):** **Always fill PR metadata fields where applicable.**
    - `--reviewer`: Assign the responsible reviewer (default: `lx-0` for Yesterday repos).
    - `--assignee`: Assign the author (`@me`) so ownership is clear.
    - `--label`: Tag with e.g. `enhancement`, `bug`, `documentation`, `skill` -- helps triage.
    - `--milestone`: Attach to a milestone if one exists for the target release/sprint.
    - `--project`: Link to the relevant GitHub Project board if configured.
    - *A PR without reviewer assignment is invisible. Don't let work rot in the queue.*
- **Why:** Context > Code. A diff shows *what* changed; the PR description explains *why*. Metadata ensures the right people are notified and the work is properly tracked.
- **Action:** `git checkout -b feat/<name>` → commit → `gh pr create --body "..." --reviewer lx-0 --assignee @me --label enhancement`.

### 5. CLEAN_CODE 🧹 -- CCD Wertesystem

Das **Clean Code Developer (CCD)** Wertesystem strukturiert Qualitätsprinzipien in 5 aufeinander aufbauende Grade (Rot → Orange → Gelb → Grün → Blau). Jeder Grad vertieft Prinzipien und Praktiken:

- 🔴 **Rot:** DRY, KISS, IOSP, VCS, täglich reflektieren
- 🟠 **Orange:** SRP, SoC, SLA, Integrationstests, Reviews
- 🟡 **Gelb:** SOLID (ISP, DIP, LSP, OCP), Unit Tests, Mocks
- 🟢 **Grün:** CI, Statische Analyse, IoC Container
- 🔵 **Blau:** CD, TDD, iterative Entwicklung, Architektur

Vollständige Übersicht: [`references/ccd-principles.md`](references/ccd-principles.md)
- **Definition:** Code is for humans to read, machines to execute.
- **Rule:** Use meaningful names, short functions, and clear separation of concerns.
- **Why:** Maintainability.
- **Action:** Refactor ruthlessly.

## Instructions 📝

1. **When starting a new feature:** Read these rules first.
2. **During implementation:** Check your work against these principles.
3. **During review:** Flag violations explicitly (e.g., "Violation: NO_TEST_SLOP detected in `test/widget_test.dart`").

---

*Authored by ManniTheRaccoon.* 🦝
