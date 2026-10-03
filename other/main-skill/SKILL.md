---
name: main
description: The entire workflow structure to follow during development.
license: MIT
metadata:
  author: AC Framework
  version: "1.0"
---

**Fundamental Principle**: *"Quality over speed. Documentation before code. Planning before execution."*

--- ⚠️ **CRITICAL: ZERO SKIP POLICY** ⚠️ ---

**YOU CANNOT SKIP ANY STEP. YOU CANNOT SKIP ANY SKILL. YOU CANNOT SKIP ANY PHASE.**

If you attempt to proceed without completing a required step, you MUST STOP and complete it first.

---

## 🛠️ Available Skills

### Quality and Security Skills

| Skill | Description | Primary Use | Required Before |
|-------|-------------|-------------|-----------------|
| `secure-coding-cybersecurity` | Detects and prevents security vulnerabilities (SQLi, XSS, command injection, hardcoded secrets). Follows OWASP Top 10 standards. | Secure code validation | `code-maintainability` |
| `code-maintainability` | Analyzes code maintainability: duplication, documentation, error handling, naming conventions, SOLID architecture, performance. | Refactoring and standards | `project-constitution` |
| `error-handling-patterns` | Error handling patterns in multiple languages: exceptions, Result types, retry, circuit breaker, graceful degradation. | Application resilience | `secure-coding-cybersecurity` |
| `performance-optimizer` | Methodologies for measuring, profiling, and optimizing code (caching, algorithm complexity, resource usage). | Performance Engineering | After Implementation |
| `test-generator` | Generate comprehensive test suites (Unit, Integration, E2E) ensuring requirements are met. | Test Driven Development | `openspec-continue-change` |

### SpecKit Consistency & Quality Skills

| Skill | Description | Primary Use | Required Before |
|-------|-------------|-------------|-----------------|
| `project-constitution` | Manage the project's core principles and ensuring alignment. | Project Governance | **PHASE 1 START** |
| `requirement-checklist` | Generate quality control checklists for requirements (unit tests for specs). | Requirements Quality | `spec-clarification` |
| `spec-analysis` | Analyze consistency across Spec, Plan, and Tasks. | Consistency Check | `openspec-continue-change` |
| `spec-clarification` | Interactively clarify specific sections of the spec. | Ambiguity Resolution | `openspec-new-change` |

### Planning and Design Skills

| Skill | Description | Primary Use | Required Before |
|-------|-------------|-------------|-----------------|
| `brainstorming` | Generates ALL questions at once about decisions before implementing. Explores requirements, constraints, and success criteria in a SINGLE comprehensive prompt. | Design and architecture | `openspec-explore` |
| `api-design-principles` | REST and GraphQL design principles: resources, endpoints, pagination, versioning, HATEOAS. | API design | `spec-clarification` [IF APIs] |
| `interface-design` | Interface design (dashboards, admin panels, apps). NOT for landing pages/marketing. | UI design | `spec-clarification` [IF UI] |

### AC Framework Core Skills

| Skill | Description | Primary Use | Required Before |
|-------|-------------|-------------|-----------------|
| `acfm-spec-workflow` | **START HERE - MANDATORY** - Understand the spec-driven workflow, directory structure (.acfm/ vs openspec/), and CLI commands. Essential before using any OpenSpec skills. | Foundation | **ANYTHING ELSE** |

### OpenSpec Skills (The heart of the framework)

| Skill | Description | Primary Use | Required Before |
|-------|-------------|-------------|-----------------|
| `openspec-explore` | Exploration mode to investigate problems, map architecture, find integration points before implementing. | Pre-analysis | `acfm-spec-workflow` |
| `openspec-new-change` | Creates a new change with step-by-step workflow (proposal → specs → design → tasks). | Structured start | `brainstorming` |
| `openspec-ff-change` | Fast-forward: creates all artifacts at once to start implementation quickly. | Quick start | `brainstorming` |
| `openspec-continue-change` | Continues an existing change by creating the next artifact in the sequence. | Continue workflow | `openspec-new-change` OR `microtask-decomposition` |
| `openspec-apply-change` | Implements tasks from a change (applies code according to specs and tasks). | Change execution | `test-generator` |
| `openspec-verify-change` | Verifies that implementation matches artifacts (specs, tasks, design). | Validation | `openspec-apply-change` |
| `openspec-archive-change` | Archives a completed change by moving it to `{specDir}/changes/archive/`. | Change closure | `openspec-verify-change` |
| `openspec-onboard` | Guided tutorial to learn OpenSpec with a complete example workflow. | Learning | `acfm-spec-workflow` |
| `openspec-sync-specs` | Synchronizes delta specs to main specs (intelligent merge). | Update specs | `openspec-verify-change` |
| `openspec-bulk-archive-change` | Archives multiple completed changes at once. | Bulk cleanup | `openspec-verify-change` |

### Documentation and Debugging Skills

| Skill | Description | Primary Use | Required Before |
|-------|-------------|-------------|-----------------|
| `project-index` | Generates structured project documentation: structure analysis, domains, agent guides. | Indexing and context | `project-constitution` |
| `sync-index` | Keep project documentation (`project-index` and sub-skills) in sync with codebase changes. | Documentation Sync | `openspec-apply-change` |
| `systematic-debugging` | Structured debugging in 4 phases: root cause investigation, pattern analysis, hypothesis, implementation. | Problem resolution | When bugs found |
| `changelog-generator` | Creates automated changelogs from git commits, translating technical to user language. | Version history | `openspec-archive-change` |
| `skill-writer` | Guide to create new skills for Claude Code with correct structure and frontmatter. | Create new skills | Anytime |
| `vercel-react-best-practices` | React and Next.js performance optimization guidelines from Vercel Engineering. | React/Next.js optimization | [IF REACT] |

### AC Framework Enhancement Skills

| Skill | Description | Primary Use | Required Before |
|-------|-------------|-------------|-----------------|
| `microtask-decomposition` | **LEVEL 2+ DECOMPOSITION** - Use when a single task from tasks.md is still too complex (affects 3+ files or requires multiple logic blocks). Breaks tasks into MICROTASKS (1 file/function each) for granular implementation. NOT for initial task breakdown. | Microtask planning & delegation | `openspec-continue-change` |
| `testing-qa` | Automate generation and maintenance of unit, integration, and E2E tests; generate test data and debugging. | Quality assurance | `openspec-apply-change` |
| `code-review` | Review generated code for style, security, and architecture issues; suggest refactorings and performance improvements. | Code quality & security | `openspec-apply-change` |
| `documentation` | Generate clear documentation for each task: technical descriptions, architecture diagrams, usage guides. | Documentation & communication | `openspec-verify-change` |
| `research-retrieval` | Search external documentation (web pages, API docs, papers) and generate useful summaries for development. | Research & context gathering | `openspec-explore` |
| `context-synthesizer` | Manage memory in long projects and summarize current state to prevent agent context loss. | Memory & context management | `project-constitution` |
| `ci-deploy` | Automate continuous integration, deployment, and post-deployment verification of developed solutions. | CI/CD automation | `openspec-verify-change` |

---

## 📍 CRITICAL: How to Use Skills - ZERO SKIP POLICY

### ⛔ BLOCKING RULES - YOU CANNOT PROCEED WITHOUT THESE:

**Rule 1: Phase Completion Checkpoint**
After EACH phase, you MUST confirm completion:
```
╔══════════════════════════════════════════════════════════╗
║  ⚠️  PHASE [X] COMPLETION CHECKPOINT                      ║
╠══════════════════════════════════════════════════════════╣
║  Have you COMPLETED ALL skills in Phase [X]?              ║
║  [ ] Yes - I have read and executed every skill           ║
║  [ ] No - I need to go back                               ║
╚══════════════════════════════════════════════════════════╝
```
**IF NO: STOP. Go back and complete missing skills.**

**Rule 2: Skill Dependency Chain**
Each skill table above shows "Required Before". You CANNOT use a skill until its dependency is satisfied.

**Rule 3: Output Verification**
Before proceeding to next phase, verify you have these outputs:

| Phase | Required Outputs | Check |
|-------|-----------------|-------|
| Phase 0 | `acfm spec status` shows initialized | [ ] |
| Phase 1 | project-constitution.md defined | [ ] |
| Phase 2 | project-index.md exists, exploration notes | [ ] |
| Phase 3 | proposal.md, specs/, design.md, tasks.md | [ ] |
| Phase 4 | Tests written, code implemented, tasks marked complete | [ ] |
| Phase 5 | Verification passed, docs updated, change archived | [ ] |

**Rule 4: Pre-Implementation Safety Check**
Before `openspec-apply-change`, ALL must be TRUE:
- [ ] tasks.md exists and has checkboxes
- [ ] All tests from `test-generator` are written
- [ ] design.md has been reviewed
- [ ] spec-analysis shows consistency

**IF ANY IS FALSE: STOP. Complete missing items.**

---

## 🚀 Workflow: New Project

When starting a project **from scratch**, follow this **MANDATORY** workflow:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    ⚠️  WORKFLOW: NEW PROJECT - ZERO SKIP  ⚠️                    │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │     START       │
    └────────┬────────┘
             │
             ▼
    ╔══════════════════════════════════════════════╗
    ║  ☠️  PHASE 0: AC FRAMEWORK SETUP (REQUIRED)   ║
    ║  BLOCKING: Cannot proceed without this       ║
    ╠══════════════════════════════════════════════╣
    ║  1. acfm-spec-workflow                       ║
    ║     └─ **ALWAYS START HERE**                 ║
    ║     └─ Understand .acfm/ vs openspec/        ║
    ║     └─ Learn CLI commands and workflow       ║
    ║     └─ Check project initialization status   ║
    ║     └─ RUN: acfm spec init (if needed)       ║
    ╚════════════════════╬═════════════════════════╝
                         ║
                         ║ ⛔ CHECKPOINT: Phase 0 Complete?
                         ║    [ ] acfm spec status shows "initialized": true
                         ║
                         ║ YES ▼
                         ▼
    ╔══════════════════════════════════════════════╗
    ║  PHASE 1: FOUNDATIONS & GOVERNANCE           ║
    ╠══════════════════════════════════════════════╣
    ║  1. project-constitution                     ║
    ║     └─ Define core principles                ║
    ║  2. secure-coding-cybersecurity              ║
    ║     └─ Establish security guidelines         ║
    ║  3. code-maintainability                     ║
    ║     └─ Define quality standards              ║
    ║  4. vercel-react-best-practices [IF REACT]   ║
    ║     └─ Apply React/Next.js best practices    ║
    ╚════════════════════╬═════════════════════════╝
                         ║
                         ║ ⛔ CHECKPOINT: Phase 1 Complete?
                         ║    [ ] project-constitution defined
                         ║    [ ] Security guidelines established
                         ║    [ ] Quality standards set
                         ║
                         ║ YES ▼
                         ▼
    ╔══════════════════════════════════════════════╗
    ║  PHASE 2: CONTEXT & DISCOVERY                ║
    ╠══════════════════════════════════════════════╣
    ║  5. context-synthesizer                      ║
    ║     └─ Initialize memory and context state   ║
    ║  6. project-index                            ║
    ║     └─ Document initial structure            ║
    ║  7. research-retrieval                       ║
    ║     └─ Gather external documentation         ║
    ║  8. openspec-explore                         ║
    ║     └─ Explore target architecture           ║
    ║  9. brainstorming                            ║
    ║     └─ Generate ALL questions in ONE prompt  ║
    ║     └─ Surface hidden assumptions            ║
    ║     └─ Challenge constraints                 ║
    ╚════════════════════╬═════════════════════════╝
                         ║
                         ║ ⛔ CHECKPOINT: Phase 2 Complete?
                         ║    [ ] project-index.md exists
                         ║    [ ] Exploration notes documented
                         ║    [ ] Brainstorming questions answered
                         ║
                         ║ YES ▼
                         ▼
    ╔══════════════════════════════════════════════╗
    ║  PHASE 3: REQUIREMENTS & DESIGN              ║
    ╠══════════════════════════════════════════════╣
    ║  10. spec-clarification (CRITICAL)           ║
    ║      └─ CLARIFY requirements first           ║
    ║  11. openspec-new-change                     ║
    ║      └─ Create proposal                      ║
    ║  12. microtask-decomposition                 ║
    ║      └─ ONLY if task is still too complex    ║
    ║      └─ Break into MICROTASKS (1 file each)  ║
    ║  13. openspec-continue-change                ║
    ║      └─ Draft Specs, Design, Tasks           ║
    ║  14. spec-analysis                           ║
    ║      └─ Verify consistency                   ║
    ║  15. requirement-checklist                   ║
    ║      └─ "Unit test" the specs                ║
    ║  16. api-design-principles [IF APIs]         ║
    ║      └─ Design REST/GraphQL APIs             ║
    ║  17. interface-design [IF UI]                ║
    ║      └─ Design dashboards/apps interface     ║
    ╚════════════════════╬═════════════════════════╝
                         ║
                         ║ ⛔ CHECKPOINT: Phase 3 Complete?
                         ║    [ ] proposal.md created
                         ║    [ ] specs/ directory with specs
                         ║    [ ] design.md written
                         ║    [ ] tasks.md with checkboxes
                         ║    [ ] spec-analysis passed
                         ║
                         ║ YES ▼
                         ▼
    ╔══════════════════════════════════════════════╗
    ║  PHASE 4: IMPLEMENTATION                     ║
    ╠══════════════════════════════════════════════╣
    ║  ☠️  SAFETY CHECK - ALL MUST BE TRUE:        ║
    ║  [ ] tasks.md exists                         ║
    ║  [ ] Tests from test-generator written       ║
    ║  [ ] design.md reviewed                      ║
    ║  [ ] spec-analysis shows consistency         ║
    ╠══════════════════════════════════════════════╣
    ║  18. test-generator                          ║
    ║      └─ TDD: Write tests first               ║
    ║  19. openspec-apply-change                   ║
    ║      └─ Implement code to pass tests         ║
    ║  20. testing-qa                              ║
    ║      └─ Automate test maintenance            ║
    ║  21. code-review                             ║
    ║      └─ Review for style/security/arch       ║
    ║  22. secure-coding-cybersecurity             ║
    ║      └─ Audit code for security              ║
    ║  23. error-handling-patterns                 ║
    ║      └─ Verify robust error handling         ║
    ║  24. performance-optimizer                   ║
    ║      └─ Optimize critical paths              ║
    ╚════════════════════╬═════════════════════════╝
                         ║
                         ║ ⛔ CHECKPOINT: Phase 4 Complete?
                         ║    [ ] All tasks in tasks.md marked [x]
                         ║    [ ] Tests passing
                         ║    [ ] Code reviewed
                         ║    [ ] Security audited
                         ║
                         ║ YES ▼
                         ▼
    ╔══════════════════════════════════════════════╗
    ║  PHASE 5: VALIDATION & CLOSURE               ║
    ╠══════════════════════════════════════════════╣
    ║  25. systematic-debugging                    ║
    ║      └─ Resolve any issues                   ║
    ║  26. openspec-verify-change                  ║
    ║      └─ Validate against specs               ║
    ║  27. documentation                           ║
    ║      └─ Generate technical docs & diagrams   ║
    ║  28. sync-index                              ║
    ║      └─ Update project documentation         ║
    ║  29. changelog-generator                     ║
    ║      └─ Generate release notes               ║
    ║  30. ci-deploy                               ║
    ║      └─ Deploy and verify solution           ║
    ║  31. openspec-archive-change                 ║
    ║      └─ Archive the change                   ║
    ╚══════════════════════════════════════════════╝
```

**Conditional Skills Notes:**
- `[IF REACT]`: Use vercel-react-best-practices only if the project uses React or Next.js
- `[IF APIs]`: Use api-design-principles only if the project involves REST/GraphQL APIs
- `[IF UI]`: Use interface-design only if the project has dashboards, admin panels, or apps
- `microtask-decomposition`: Use ONLY when a single task from tasks.md is still too complex (3+ files). NOT for initial breakdown.

---

## 🔄 Workflow: Existing Project

When working on an **existing codebase** (adding features, fixing bugs, refactoring):

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                  ⚠️  WORKFLOW: EXISTING PROJECT - ZERO SKIP  ⚠️                  │
└─────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │  START CHANGE   │
    └────────┬────────┘
             │
             ▼
    ╔══════════════════════════════════════════════╗
    ║  ☠️  PHASE 0: AC FRAMEWORK SETUP (REQUIRED)   ║
    ║  BLOCKING: Cannot proceed without this       ║
    ╠══════════════════════════════════════════════╣
    ║  1. acfm-spec-workflow                       ║
    ║     └─ **ALWAYS START HERE**                 ║
    ║     └─ Verify project initialization         ║
    ║     └─ Check existing changes                ║
    ╚════════════════════╬═════════════════════════╝
                         ║
                         ║ ⛔ CHECKPOINT: Phase 0 Complete?
                         ║
                         ║ YES ▼
                         ▼
    ╔══════════════════════════════════════════════╗
    ║  PHASE 1: CONTEXT & ANALYSIS                 ║
    ╠══════════════════════════════════════════════╣
    ║  2. context-synthesizer                      ║
    ║     └─ Load memory and context state         ║
    ║  3. project-index (if needed)                ║
    ║     └─ Map current system                    ║
    ║  4. research-retrieval                       ║
    ║     └─ Gather external documentation         ║
    ║  5. openspec-explore                         ║
    ║     └─ Deep dive into relevant modules       ║
    ║  6. brainstorming                            ║
    ║     └─ ALL questions in ONE prompt           ║
    ║     └─ Ideate on feature/fix                 ║
    ╚════════════════════╬═════════════════════════╝
                         ║ ⛔ CHECKPOINT
                         ▼
    ╔══════════════════════════════════════════════╗
    ║  PHASE 2: DISCOVERY & CLARIFICATION          ║
    ╠══════════════════════════════════════════════╣
    ║  7. spec-clarification (CRITICAL)            ║
    ║     └─ CLARIFY requirements first            ║
    ║  8. openspec-new-change                      ║
    ║     └─ Initialize change artifact            ║
    ║  9. microtask-decomposition                  ║
    ║     └─ If task too complex                   ║
    ╚════════════════════╬═════════════════════════╝
                         ║ ⛔ CHECKPOINT
                         ▼
    ╔══════════════════════════════════════════════╗
    ║  PHASE 3: DESIGN & PLANNING                  ║
    ╠══════════════════════════════════════════════╣
    ║  10. openspec-continue-change                ║
    ║      └─ Draft Specs, Design, Tasks           ║
    ║  11. spec-analysis                           ║
    ║      └─ Check consistency with existing      ║
    ║  12. requirement-checklist                   ║
    ║      └─ Validate requirements                ║
    ║  13. api-design-principles [IF APIs]         ║
    ║      └─ Design API changes                   ║
    ║  14. interface-design [IF UI]                ║
    ║      └─ Design interface changes             ║
    ╚════════════════════╬═════════════════════════╝
                         ║ ⛔ CHECKPOINT
                         ▼
    ╔══════════════════════════════════════════════╗
    ║  PHASE 4: IMPLEMENTATION                     ║
    ╠══════════════════════════════════════════════╣
    ║  ☠️  SAFETY CHECK REQUIRED                   ║
    ╠══════════════════════════════════════════════╣
    ║  15. test-generator                          ║
    ║      └─ Generate tests for new feature       ║
    ║  16. openspec-apply-change                   ║
    ║      └─ Implement code                       ║
    ║  17. testing-qa                              ║
    ║      └─ Automate test maintenance            ║
    ║  18. code-review                             ║
    ║      └─ Review for style/security/arch       ║
    ║  19. secure-coding-cybersecurity             ║
    ║      └─ Audit new code                       ║
    ║  20. error-handling-patterns                 ║
    ║      └─ Verify error handling                ║
    ║  21. performance-optimizer                   ║
    ║      └─ Ensure no perf degradation           ║
    ╚════════════════════╬═════════════════════════╝
                         ║ ⛔ CHECKPOINT
                         ▼
    ╔══════════════════════════════════════════════╗
    ║  PHASE 5: OPTIMIZATION & VERIFICATION        ║
    ╠══════════════════════════════════════════════╣
    ║  22. systematic-debugging                    ║
    ║      └─ Fix regressions                      ║
    ║  23. openspec-verify-change                  ║
    ║      └─ Final verification                   ║
    ║  24. documentation                           ║
    ║      └─ Generate technical docs & diagrams   ║
    ║  25. sync-index (IMPORTANT)                  ║
    ║      └─ Update docs with new changes         ║
    ║  26. changelog-generator                     ║
    ║      └─ Generate release notes               ║
    ║  27. ci-deploy                               ║
    ║      └─ Deploy and verify solution           ║
    ║  28. openspec-archive-change                 ║
    ║      └─ Archive change                       ║
    ╚══════════════════════════════════════════════╝
```

**Conditional Skills Notes:**
- `[IF APIs]`: Use api-design-principles only if modifying/creating REST/GraphQL APIs
- `[IF UI]`: Use interface-design only if modifying dashboards, admin panels, or apps
- `project-index`: Run only if you haven't indexed the project yet or need to refresh context

---

## 📝 Skill Loading Reference

All skills are located in: `skills/`

To load a skill, read its SKILL.md file:
- Example: Read `skills/spec-clarification/SKILL.md` to use the clarification workflow
- Example: Read `skills/interface-design/SKILL.md` to use interface design principles

### ⛔ MANDATORY SKILL EXECUTION CHECKLIST

Before claiming a skill is "done", verify:
- [ ] I have read the entire SKILL.md file
- [ ] I have executed ALL steps in the skill
- [ ] I have the required output artifacts
- [ ] I can answer: "What did this skill produce?"

**Remember**: Skills are documentation-based workflows with ZERO SKIP policy. Load them by reading the SKILL.md files, execute CLI commands when instructed, and NEVER proceed without completing all steps.

---

## ⚠️ VIOLATION CONSEQUENCES

If you SKIP a skill or phase:
1. The framework integrity is compromised
2. Quality cannot be guaranteed
3. You MUST go back and complete what was skipped
4. No exceptions. No shortcuts. Follow the workflow.

**Quality over speed. Documentation before code. Planning before execution.**
