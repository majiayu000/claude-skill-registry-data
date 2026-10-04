---
name: sam-tdd-pipeline
description: Autonomous TDD pipeline - transform PRD into working tested code using RED-GREEN-REFACTOR methodology
---

# SAM Autonomous TDD Pipeline

This skill orchestrates a complete TDD development workflow using specialized SAM agents.

## When to Use
Invoke this skill when you want to:
- Transform a PRD into working, tested code
- Follow strict TDD methodology (RED-GREEN-REFACTOR)
- Use autonomous AI agents for development

## The Pipeline

### Phase 1: Validate PRD
- sam-atlas reviews technical feasibility
- sam-iris validates UX requirements

### Phase 2: Generate Stories
- Break PRD into epics and user stories
- Create detailed acceptance criteria

### Phase 3: TDD Loop (for each story)
1. **RED**: sam-titan writes failing tests based on acceptance criteria
2. **GREEN**: sam-dyna writes minimal code to make tests pass
3. **REFACTOR**: sam-argus reviews and improves code quality
4. **UI**: sam-iris reviews layout and fixes alignment (web apps only)
5. **CSS**: sam-cosmo reviews styling consistency (web apps only)

### Phase 4: Complete
- sam-sage generates documentation
- Final review and handoff

## Usage
Provide a PRD or feature description to start the autonomous TDD pipeline.

## Available Agents
- /sam-orchestrator - Pipeline coordinator
- /sam-atlas - Architect (PRD validation, technical design)
- /sam-titan - Test Architect (RED phase)
- /sam-dyna - Developer (GREEN phase)
- /sam-argus - Code Reviewer (REFACTOR phase)
- /sam-cosmo - CSS Consistency Reviewer (web apps only)
- /sam-sage - Technical Writer (documentation)
- /sam-iris - UX Designer (UX validation)
