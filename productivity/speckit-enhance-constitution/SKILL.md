---
name: speckit-enhance-constitution
description: One-time command to enhance constitution with workflow quality gates
  using LLM intelligence
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: templates/commands/enhance-constitution.md
---

# Speckit Enhance-Constitution Skill

# Constitution Enhancement (One-Time Use)

You are enhancing the project's constitution file (`.specify/memory/constitution.md`) with workflow-specific quality gates.

## Your Task

1. **Read the current constitution**: `.specify/memory/constitution.md`
2. **Review the template below**: Contains workflow selection guidelines and quality gates
3. **Intelligently merge**: Use `/specify.constitution` to:
   - Preserve all existing constitution content
   - Add missing workflow selection guidance
   - Add missing quality gates for each workflow type
   - Match the existing writing style, tone, and section numbering
   - Avoid duplicating content that already exists
   - Ensure smooth integration without jarring transitions

4. **Self-destruct**: After updating the constitution, DELETE this command file and any duplicates
   - Delete this file: `.Codex/commands/speckit.enhance-constitution.md`
   - Also check and delete any other enhance-constitution files in other agent directories:
     * `.github/prompts/speckit.enhance-constitution.prompt.md` and `.github/agents/speckit.enhance-constitution.md`
     * `.Codex/commands/speckit.enhance-constitution.md`
     * `.cursor/commands/speckit.enhance-constitution.md`
     * `.windsurf/workflows/speckit.enhance-constitution.md`
     * `.opencode/prompts/speckit.enhance-constitution.md`
     * `.amazon-q/commands/speckit.enhance-constitution.md`
     * `.codex/commands/speckit.enhance-constitution.md`
     * Or any other agent command directories in your project
   - This prevents accidental re-use

## Template Content to Integrate

```markdown
## Development Workflow

### Core Workflow (Feature Development)
1. Feature request initiates with `/speckit.specify <description>`
2. Clarification via `/speckit.clarify` to resolve ambiguities
3. Technical planning with `/speckit.plan` to create implementation design
4. Task breakdown using `/speckit.tasks` for execution roadmap
5. Implementation via `/speckit.implement` following task order
### Extension Workflows
- **Baseline**: `/speckit.baseline` → baseline-spec.md + current-state.md establishing project context
- **Bugfix**: `/speckit.bugfix "<description>"` → bug-report.md + tasks.md with regression test requirement
- **Enhancement**: `/speckit.enhance "<description>"` → enhancement.md (condensed single-doc with spec + plan + tasks)
- **Modification**: `/speckit.modify <feature_num> "<description>"` → modification.md + impact analysis + tasks.md
- **Refactor**: `/speckit.refactor "<description>"` → refactor.md + baseline metrics + incremental tasks.md
- **Hotfix**: `/speckit.hotfix "<incident>"` → hotfix.md + expedited tasks.md + post-mortem.md (within 48 hours)
- **Deprecation**: `/speckit.deprecate <feature_num> "<reason>"` → deprecation.md + dependency scan + phased tasks.md
- **Review**: `/speckit.review <task_id>` → review implementation against spec + update tasks.md + generate report
- **Cleanup**: `/speckit.cleanup` → organize specs/ directory + archive old branches + update documentation


### Workflow Selection
Development activities SHALL use the appropriate workflow type based on the nature of the work. Each workflow enforces specific quality gates and documentation requirements tailored to its purpose:

- **Baseline** (`/speckit.baseline`): Project context establishment - requires comprehensive documentation of existing architecture and change tracking
- **Feature Development** (`/speckit.specify`): New functionality - requires full specification, planning, and TDD approach
- **Bug Fixes** (`/speckit.bugfix`): Defect remediation - requires regression test BEFORE applying fix
- **Enhancements** (`/speckit.enhance`): Minor improvements to existing features - streamlined single-document workflow with simple single-phase plan (max 7 tasks)
- **Modifications** (`/speckit.modify`): Changes to existing features - requires impact analysis and backward compatibility assessment
- **Refactoring** (`/speckit.refactor`): Code quality improvements - requires baseline metrics, behavior preservation guarantee, and incremental validation
- **Hotfixes** (`/speckit.hotfix`): Emergency production issues - expedited process with deferred testing and mandatory post-mortem
- **Deprecation** (`/speckit.deprecate`): Feature sunset - requires phased rollout (warnings → disabled → removed), migration guide, and stakeholder approvals

The wrong workflow SHALL NOT be used - features must not bypass specification, bugs must not skip regression tests, refactorings must not alter behavior, and enhancements requiring complex multi-phase plans must use full feature development workflow.

### Quality Gates by Workflow

**Baseline**:
- Comprehensive project analysis MUST be performed
- All major components MUST be documented in baseline-spec.md
- Current state MUST enumerate all changes by workflow type
- Architecture and technology stack MUST be accurately captured

**Feature Development**:
- Specification MUST be complete before planning
- Plan MUST pass constitution checks before task generation
- Tests MUST be written before implementation (TDD)
- Code review MUST verify constitution compliance

**Bugfix**:
- Bug reproduction MUST be documented with exact steps
- Regression test MUST be written before fix is applied
- Root cause MUST be identified and documented
- Prevention strategy MUST be defined

**Enhancement**:
- Enhancement MUST be scoped to a single-phase plan with no more than 7 tasks
- Changes MUST be clearly defined in the enhancement document
- Tests MUST be added for new behavior
- If complexity exceeds single-phase scope, full feature workflow MUST be used instead

**Modification**:
- Impact analysis MUST identify all affected files and contracts
- Original feature spec MUST be linked
- Backward compatibility MUST be assessed
- Migration path MUST be documented if breaking changes

**Refactor**:
- Baseline metrics MUST be captured before any changes unless explicitly exempted
- Tests MUST pass after EVERY incremental change
- Behavior preservation MUST be guaranteed (tests unchanged)
- Target metrics MUST show measurable improvement unless explicitly exempted

**Hotfix**:
- Severity MUST be assessed (P0/P1/P2)
- Rollback plan MUST be prepared before deployment
- Fix MUST be deployed and verified before writing tests (exception to TDD)
- Post-mortem MUST be completed within 48 hours of resolution

**Deprecation**:
- Dependency scan MUST be run to identify affected code
- Migration guide MUST be created before Phase 1
- All three phases MUST complete in sequence (no skipping)
- Stakeholder approvals MUST be obtained before starting
```

## Instructions

1. First, run `/specify.constitution` with instructions to merge the above template content intelligently
2. Review the updated constitution to ensure quality
3. Then delete ALL enhance-constitution files from all agent directories (see self-destruct instructions above)

## Important Notes

- **Preserve existing content**: Don't remove or significantly alter existing constitution sections
- **Match style**: Adapt template language to match existing constitution's tone
- **Section numbering**: Continue existing numbering scheme (Roman numerals, numeric, or none)
- **No duplication**: If workflow guidance already exists, enhance rather than duplicate
- **One-time only**: This command deletes itself after use to prevent confusion
- **Multi-agent setups**: If you have multiple agents configured, delete enhance-constitution files from all agent directories

---

**After completion**:
1. Verify that `.specify/memory/constitution.md` contains both the original content and the new workflow quality gates, properly integrated
2. Delete ALL enhance-constitution files from all agent/prompt directories
