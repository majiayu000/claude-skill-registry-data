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
- activate_skill('sam-orchestrator') - Pipeline coordinator
- activate_skill('sam-atlas') - Architect (PRD validation, technical design)
- activate_skill('sam-titan') - Test Architect (RED phase)
- activate_skill('sam-dyna') - Developer (GREEN phase)
- activate_skill('sam-argus') - Code Reviewer (REFACTOR phase)
- activate_skill('sam-cosmo') - CSS Consistency Reviewer (web apps only)
- activate_skill('sam-sage') - Technical Writer (documentation)
- activate_skill('sam-iris') - UX Designer (UX validation)
