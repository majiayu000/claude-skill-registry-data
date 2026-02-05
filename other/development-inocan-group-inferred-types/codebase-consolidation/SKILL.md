---
name: codebase-consolidation
description: Analyze, consolidate, and document codebases through multi-perspective analysis. Identifies duplicate code, refactoring opportunities, architectural patterns, and generates comprehensive reports. Use when reviewing project structure, planning refactoring, creating documentation, or assessing technical debt.
---

# Codebase Consolidation & Analysis Skill

Systematically analyze codebases to identify consolidation opportunities, document architecture, assess code quality, and generate actionable insights for improvement.

## Purpose

Provide comprehensive codebase analysis including:
- **Code Duplication Detection** - Find duplicate/similar code blocks for consolidation
- **Architectural Analysis** - Document system structure, patterns, and design decisions
- **Refactoring Opportunities** - Identify areas for improvement and modernization
- **Technical Debt Assessment** - Quantify and prioritize technical debt
- **Documentation Generation** - Create architecture diagrams, API docs, and summaries
- **Multi-Perspective Analysis** - Review from architect, developer, and product perspectives
- **Quality Metrics** - Measure code complexity, test coverage, and maintainability

## When to Use

Use this skill when:

- **Starting on a new codebase** - Understand structure and patterns quickly
- **Planning refactoring** - Identify consolidation opportunities and priorities
- **Code review preparation** - Get comprehensive analysis before major changes
- **Documentation needs** - Generate architecture docs and technical summaries
- **Technical debt assessment** - Quantify and prioritize improvement areas
- **Onboarding new developers** - Create comprehensive codebase overview
- **Pre-release audits** - Comprehensive quality and security review
- **Legacy code modernization** - Identify outdated patterns and improvement paths

**Don't use** for:
- Single file analysis (use Read tool directly)
- Quick bug fixes with known location
- Simple feature additions following established patterns
- Real-time coding assistance

## Quick Reference

- **[Analysis Dimensions](analysis-dimensions.md)** - Detailed criteria for 8 analysis dimensions
- **[Consolidation Patterns](consolidation-patterns.md)** - Common refactoring patterns and examples
- **[Report Templates](report-templates.md)** - Output format examples and templates

## Analysis Dimensions

### 1. Code Duplication Analysis
Identify duplicate or similar code blocks for consolidation.

### 2. Architectural Structure
Document high-level system architecture and component relationships.

### 3. Code Organization & Modularity
Assess module structure and separation of concerns.

### 4. Refactoring Opportunities
Identify areas for improvement (large files, complex functions, etc.).

### 5. Technical Debt
Quantify and categorize technical debt (TODOs, missing tests, outdated deps).

### 6. Quality Metrics
Measure code quality indicators (LOC, complexity, coverage).

### 7. Design Patterns & Idioms
Identify patterns and anti-patterns in use.

### 8. Cross-Cutting Concerns
Analyze error handling, logging, security, performance.

See **[analysis-dimensions.md](analysis-dimensions.md)** for detailed criteria and checks.

## Analysis Workflow

### Phase 1: Codebase Discovery
```bash
# Project structure
tree -L 3 -I 'target|node_modules|.git'

# File counts
find . -type f -name "*.rs" | wc -l

# Configuration
cat Cargo.toml package.json 2>/dev/null
```

### Phase 2: Dependency Analysis
```bash
# Dependency tree
cargo tree --depth 2

# Outdated dependencies
cargo outdated

# Security audit
cargo audit
```

### Phase 3: Code Duplication Detection
```bash
# Find large files (potential duplication)
find . -name "*.rs" -not -path "*/target/*" -exec wc -l {} + | sort -rn | head -20

# Find tech debt markers
rg "TODO|FIXME|HACK|XXX" --count-matches
```

### Phase 4: Complexity Analysis
```bash
# LOC statistics
tokei

# Find long functions
rg "fn\s+\w+\s*\(" --count-matches
```

### Phase 5: Architecture Mapping
1. Identify major components/modules
2. Document component responsibilities
3. Map dependencies between components
4. Identify integration points
5. Document data flow
6. Note design patterns in use

### Phase 6: Quality Assessment
```bash
# Test coverage
cargo tarpaulin --out Html

# Linting
cargo clippy --all-targets -- -D warnings

# Formatting
cargo fmt -- --check
```

### Phase 7: Documentation Review
```bash
# Generate docs
cargo doc --no-deps

# Count public APIs vs. doc comments
rg "pub\s+(async\s+)?fn\s+\w+" | wc -l
rg "///|//!" | wc -l
```

### Phase 8: Synthesis & Report Generation
Combine findings into comprehensive report with:
- Executive summary
- Key metrics and statistics
- Prioritized recommendations
- Detailed findings by dimension
- Action items with effort estimates

See **[report-templates.md](report-templates.md)** for complete report formats.

## Output Formats

### Executive Summary Report
High-level overview with health score, key metrics, and prioritized recommendations.

### Architecture Documentation
System architecture, component diagram, design patterns, and data flows.

### Refactoring Roadmap
Phased plan with tasks, priorities, effort estimates, and success criteria.

### Consolidation Opportunities Report
Detailed analysis of duplicate code with refactoring recommendations.

### Technical Debt Report
Quantified debt by category with payoff strategy and reduction plan.

### Onboarding Document
Developer-friendly guide to codebase structure, setup, and common tasks.

See **[report-templates.md](report-templates.md)** for complete templates.

## Common Consolidation Patterns

See **[consolidation-patterns.md](consolidation-patterns.md)** for detailed examples of:

1. **Extract Function** - Consolidate duplicate code blocks
2. **Extract Module** - Group related functions
3. **Strategy Pattern** - Replace if/else chains with polymorphism
4. **Builder Pattern** - Simplify complex object construction
5. **Repository Pattern** - Eliminate CRUD duplication
6. **Facade Pattern** - Simplify complex subsystem interactions
7. **Template Method** - Common algorithm structure with varying steps
8. **Type State Pattern** - Enforce state transitions at compile time
9. **Newtype Pattern** - Prevent type confusion
10. **Parallel Refactoring** - Safe migration to new APIs

## Best Practices

### DO:

✓ **Start with high-level structure** before diving into details
✓ **Use automated tools** for metrics (tokei, cargo-tarpaulin, etc.)
✓ **Prioritize findings** by impact and effort
✓ **Provide concrete examples** from the actual codebase
✓ **Include file paths and line numbers** for all findings
✓ **Estimate effort** for each recommendation (S/M/L or days)
✓ **Consider multiple perspectives** (architect, developer, product)
✓ **Generate actionable items** not just observations
✓ **Use progressive disclosure** - summary first, details on demand
✓ **Create visual diagrams** for architecture when helpful

### DON'T:

✗ **Don't analyze without clear goals** - understand what user needs first
✗ **Don't only report problems** - highlight strengths too
✗ **Don't provide generic advice** - be specific to this codebase
✗ **Don't ignore context** - consider team size, timeline, priorities
✗ **Don't recommend big rewrites** - prefer incremental improvements
✗ **Don't forget the user** - connect technical findings to business impact
✗ **Don't just list issues** - provide roadmap and priorities
✗ **Don't overwhelm with detail** - use progressive disclosure pattern

## Integration with Other Skills

### Complements:
- **rust-code-quality**: Run after consolidation for detailed quality review
- **architecture-validation**: Verify architectural compliance after refactoring
- **plan-gap-analysis**: Compare implementation against planned architecture
- **test-runner**: Validate refactoring didn't break tests
- **analysis-swarm**: Get multi-perspective analysis on major refactoring decisions

### Invokes:
- **episode-start**: Track consolidation analysis as learning episode
- **episode-log-steps**: Record each analysis phase
- **episode-complete**: Score effectiveness of analysis

### Follows:
- **feature-implement**: Run consolidation analysis before implementing large features
- **debug-troubleshoot**: Use analysis to identify root causes

## Command Reference

### Rust Projects
```bash
# Code statistics
tokei

# Dependency analysis
cargo tree --depth 2
cargo outdated
cargo audit

# Quality checks
cargo fmt -- --check
cargo clippy --all-targets -- -D warnings
cargo test --all

# Coverage
cargo tarpaulin --out Html --output-dir coverage

# Documentation
cargo doc --no-deps --open
```

### Multi-Language Projects
```bash
# Code statistics
cloc . --exclude-dir=target,node_modules,.git

# Find large files
find . -name "*.rs" -o -name "*.ts" -o -name "*.py" \
  | xargs wc -l | sort -rn | head -20

# Find tech debt markers
rg "TODO|FIXME|HACK|XXX" --count-matches
```

## Quick Start Examples

### Example 1: New Developer Onboarding
**Goal**: Create comprehensive codebase overview for new team member.

**Focus**: High-level architecture, key components, development workflow, common patterns.

**Output**: Onboarding document with system diagram, component overview, setup guide, and first contribution ideas.

### Example 2: Technical Debt Assessment
**Goal**: Quantify tech debt for quarterly planning.

**Focus**: Code duplication, test coverage gaps, outdated dependencies, TODOs/FIXMEs.

**Output**: Technical debt report with quantified debt in developer-days, prioritized backlog, and ROI estimates.

### Example 3: Pre-Refactoring Analysis
**Goal**: Plan authentication system refactoring.

**Focus**: Current auth implementation, duplication, integration points, test coverage, migration risks.

**Output**: Refactoring plan with current state analysis, proposed architecture, migration strategy, and validation criteria.

## Validation Criteria

After consolidation, verify:

- [ ] No duplicate code blocks (exact or near-duplicates)
- [ ] Files under size limits (<500 LOC)
- [ ] Functions under complexity limits (<50 LOC)
- [ ] Test coverage maintained or improved
- [ ] All tests passing
- [ ] No new linter warnings
- [ ] Documentation updated
- [ ] Performance not degraded

## Meta-Learning

Track consolidation effectiveness:

### Metrics to Monitor
- LOC reduction from consolidation
- Time to implement new features (should decrease)
- Bug rate (should decrease)
- Test coverage (should increase)
- Onboarding time for new developers (should decrease)

### Improvement Patterns
- Which types of duplication are most common
- Which refactoring patterns provide most value
- Optimal timing for consolidation (before vs. during feature work)
- Balance between consolidation and feature delivery

## Summary

The Codebase Consolidation skill provides:

1. **Comprehensive Analysis**: 8 dimensions covering all aspects of code quality
2. **Actionable Insights**: Prioritized recommendations with effort estimates
3. **Multiple Perspectives**: Architect, developer, and product views
4. **Progressive Disclosure**: Summary reports with detailed references
5. **Integration**: Works with other skills for complete workflow
6. **Best Practices**: Based on 2025 industry standards and latest research

Use when you need deep understanding of codebase structure, want to identify improvement opportunities, or need to create comprehensive documentation for team alignment.
