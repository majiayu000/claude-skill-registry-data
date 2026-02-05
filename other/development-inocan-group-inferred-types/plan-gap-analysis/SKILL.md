---
name: plan-gap-analysis
description: Analyze gaps between implementation plans and actual codebase implementation for the Rust self-learning memory project
---

# Plan Gap Analysis Skill

Systematically analyze the implementation status of the self-learning memory system by comparing the detailed plans in `plans/` against the actual codebase implementation.

## Purpose

This skill enables comprehensive gap analysis between:
- Documented plans (Phase 1-6 in plans/ folder)
- Actual implementation (Rust codebase)
- Missing features, tests, and documentation
- Unimplemented components from the roadmap

## Workflow

### Phase 1: Plan Inventory

1. **Read all plan files** in `plans/` directory:
   - `00-overview.md` - Project summary and metrics
   - `01-understand.md` - Requirements and components
   - `02-plan.md` - Architecture decisions and roadmap
   - `03-execute.md` - Implementation details
   - `04-review.md` - Quality requirements
   - `05-secure.md` - Security requirements
   - `06-feedback-loop.md` - Refinements and improvements

2. **Extract requirements** from each phase:
   - Functional requirements (FR1-FR7)
   - Non-functional requirements (NFR1-NFR6)
   - Data structures and types
   - Functions and APIs
   - Tests and benchmarks
   - Security measures

### Phase 2: Codebase Inventory

1. **Scan Rust crates** structure:
   ```bash
   # List all crates
   find . -name "Cargo.toml" -not -path "*/target/*"

   # List all Rust source files
   find . -name "*.rs" -not -path "*/target/*"
   ```

2. **Analyze each crate**:
   - `memory-core` - Core data structures and memory orchestration
   - `memory-storage-turso` - Turso/libSQL storage backend
   - `memory-storage-redb` - redb cache layer
   - `memory-mcp` - MCP server and sandbox
   - `test-utils` - Test utilities
   - `benches` - Performance benchmarks

3. **Check implementation status**:
   - Data structures (Episode, Pattern, Heuristic, etc.)
   - Core functions (start_episode, log_step, complete_episode, etc.)
   - Storage operations (CRUD, queries, sync)
   - Pattern extraction algorithms
   - MCP integration and sandboxing
   - Tests (unit, integration, benchmarks)

### Phase 3: Gap Identification

For each phase, identify:

#### Phase 1 (UNDERSTAND) Gaps
- [ ] Missing data structures from specification
- [ ] Incomplete type definitions
- [ ] Missing edge case handling

#### Phase 2 (PLAN) Gaps
- [ ] Architectural decisions not implemented
- [ ] Success metrics not tracked
- [ ] Feature flags not implemented
- [ ] Circuit breakers missing
- [ ] Telemetry not fully implemented

#### Phase 3 (EXECUTE) Gaps
- [ ] Storage agent deliverables incomplete
- [ ] Learning agent features missing
- [ ] MCP agent sandbox security incomplete
- [ ] Sync mechanism not fully implemented

#### Phase 4 (REVIEW) Gaps
- [ ] Compliance tests missing (FR1-FR7)
- [ ] Performance tests incomplete (NFR1-NFR6)
- [ ] Quality metrics not measured
- [ ] Code coverage below 90%
- [ ] Integration tests incomplete

#### Phase 5 (SECURE) Gaps
- [ ] Security attack surface analysis missing
- [ ] Sandbox escape prevention incomplete
- [ ] SQL injection prevention validation missing
- [ ] Resource limits not enforced
- [ ] Network security not validated
- [ ] Penetration tests not implemented

#### Phase 6 (FEEDBACK LOOP) Gaps
- [ ] Edge case refinements not implemented
- [ ] Performance optimizations pending
- [ ] Two-phase commit not implemented
- [ ] Pattern extraction queue missing
- [ ] Schema migration not implemented

### Phase 4: Prioritization

Categorize gaps by priority:

**Critical (Blocks production)**:
- Security vulnerabilities
- Data corruption risks
- Missing core functionality

**High (Affects quality)**:
- Performance targets not met
- Test coverage below target
- Missing error handling

**Medium (Technical debt)**:
- Code quality issues
- Documentation gaps
- Optimization opportunities

**Low (Nice to have)**:
- Future enhancements
- Optional features
- Cosmetic improvements

### Phase 5: TODO Generation

Generate structured TODO list:

```markdown
## Phase [N]: [PHASE_NAME]

### Critical Priority
- [ ] [Component] - [Missing item] (Week X deliverable)
  - **File**: path/to/file.rs
  - **Plan Reference**: plans/0X-phase.md:LineNumber
  - **Impact**: [Description of impact]
  - **Effort**: [Estimated effort]

### High Priority
- [ ] [Component] - [Missing item]
  ...

### Medium Priority
...

### Low Priority
...
```

## Analysis Process

```rust
// Pseudo-code for analysis flow
async fn analyze_plan_gaps() -> GapAnalysisReport {
    let plans = read_all_plan_files().await;
    let codebase = scan_rust_codebase().await;

    let mut gaps = Vec::new();

    for phase in &plans {
        let requirements = extract_requirements(phase);
        let implementation = find_implementation(&codebase, &requirements);

        for req in requirements {
            if !implementation.contains(&req) {
                gaps.push(Gap {
                    phase: phase.number,
                    requirement: req,
                    priority: calculate_priority(&req),
                    file_location: find_best_location(&codebase, &req),
                    plan_reference: format_reference(phase, &req),
                });
            }
        }
    }

    GapAnalysisReport {
        total_requirements: count_all_requirements(&plans),
        implemented: codebase.count_implementations(),
        gaps: gaps.sorted_by_priority(),
        completion_percentage: calculate_completion(&gaps),
    }
}
```

## Key Files to Analyze

### Plans Directory
- `plans/00-overview.md` - Success metrics and targets
- `plans/01-understand.md` - All 47 core data structures
- `plans/02-plan.md` - 12-week roadmap, success metrics
- `plans/03-execute.md` - Week 1-2, 3-4, 5-6, 7-8 deliverables
- `plans/04-review.md` - FR1-FR7, NFR1-NFR6 tests
- `plans/05-secure.md` - Security attack surfaces and mitigations
- `plans/06-feedback-loop.md` - Refinements and edge cases

### Codebase to Check

**Core Types** (`memory-core/src/`):
- `types.rs` - TaskContext, TaskType, ComplexityLevel, etc.
- `episode.rs` - Episode, ExecutionStep, ExecutionResult
- `pattern.rs` - Pattern enum variants, Heuristic
- `error.rs` - Error types and Result
- `memory.rs` - SelfLearningMemory main orchestrator
- `extraction.rs` - PatternExtractor trait and implementations
- `reward.rs` - RewardCalculator
- `reflection.rs` - ReflectionGenerator
- `sync.rs` - Storage synchronization

**Storage** (`memory-storage-*/src/`):
- Turso: schema.rs, storage.rs (CRUD, queries)
- redb: tables.rs, storage.rs (cache operations)

**MCP** (`memory-mcp/src/`):
- `server.rs` - MCP server implementation
- `sandbox.rs` - Code execution sandbox
- `types.rs` - Tool definitions

**Tests**:
- Unit tests in each module
- Integration tests in `tests/` directories
- Benchmarks in `benches/`

## Output Format

```markdown
# Plan Gap Analysis Report
**Generated**: [Date]
**Project**: rust-self-learning-memory
**Total Requirements**: X
**Implemented**: Y (Z%)
**Gaps Identified**: N

## Executive Summary
- Phase 1: X/Y complete
- Phase 2: X/Y complete
- Phase 3: X/Y complete
- Phase 4: X/Y complete
- Phase 5: X/Y complete
- Phase 6: X/Y complete

## Detailed Gap Analysis

### Phase 1: UNDERSTAND
**Completion**: X%

#### Critical Gaps
1. [Gap description]
   - **Plan**: plans/01-understand.md:123
   - **Missing in**: memory-core/src/types.rs
   - **Priority**: Critical
   - **Effort**: [hours/days]

...

### Phase 2: PLAN
...

## Recommended Action Plan

### Week 1-2 Focus
- [ ] Critical gap 1
- [ ] Critical gap 2

### Week 3-4 Focus
...

## Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Retrieval Latency (P95) | <100ms | TBD | 🔴 Not Tested |
| Pattern Accuracy | >70% | TBD | 🔴 Not Tested |
| Test Coverage | >90% | X% | 🟡 Below Target |
| Episode Capacity | 10,000+ | TBD | 🔴 Not Tested |
| Security Vulnerabilities | 0 critical | X | 🔴 Not Assessed |
```

## Best Practices

1. **Be Systematic**: Check every requirement in every plan
2. **Be Specific**: Reference exact file locations and line numbers
3. **Be Accurate**: Verify implementation, don't assume
4. **Be Prioritized**: Critical > High > Medium > Low
5. **Be Actionable**: Include file paths and effort estimates

## Example Usage

When invoked, this skill will:
1. Read all 8 plan markdown files
2. Scan all Rust source files
3. Cross-reference requirements vs implementation
4. Generate prioritized TODO list by phase
5. Output comprehensive gap analysis report
