---
name: doc-maintainer
description: Maintains high-quality, concise, project-aligned documentation. Creates, updates, and validates README.md, CLAUDE.md, code comments, and other documentation. Activates after implementing features, when documentation is outdated, or when explicitly requested.
allowed-tools: [Read, Write, Edit, Glob, Grep, mcp__ide__getDiagnostics, AskUserQuestion]
---

# Doc Maintainer Skill

## Purpose

Maintain documentation that is concise, accurate, scannable, and perfectly aligned with project standards.

## Activation Triggers

### Proactive Activation

- New features, packages, or significant code changes without documentation updates
- Documentation files appear outdated or inconsistent with current code
- Documentation exceeds recommended length limits (README.md > 150 lines)
- Public functions/types lack required doc comments (Go projects)
- Documentation quality issues detected during code review

### Manual Activation

- User requests documentation creation/update
- User asks to verify documentation completeness
- Before committing documentation changes

## Core Documentation Domains

1. **Project Documentation** (README.md, CLAUDE.md, SETUP.md)
2. **Code Documentation** (inline comments, doc comments)
3. **Documentation Quality Assurance** (consistency, accuracy, conciseness)

## Fundamental Principles (from ~/.claude/CLAUDE.md)

### README.md Standards

- **Conciseness**: Target 150 lines maximum
- **Scannable structure**: Clear sections with meaningful headings
- **No temporal information**: Describe current state only, not history
- **No manual metrics**: Use CI badges instead of hardcoded numbers
- **Avoid redundancy**: Don't duplicate information available in code/CI

**Essential Sections**:
- Project overview
- Technology stack (concise)
- Development environment setup
- Project structure
- Key features (current state only)
- Development commands
- License information
- Reference links

**Prohibited Content**:
- Detailed technology stack explanations
- Excessive project structure diagrams
- Information about unused platforms
- Change history (use Git instead)
- Verbose explanations of self-evident information

### CLAUDE.md Standards

- **Prescriptive tone**: Use "should" not "has been done"
- **Generality**: Describe ideal state, not current project-specific status
- **Separation of concerns**: Development guidelines in CLAUDE.md, usage in README.md
- **Normative descriptions**: Focus on what should be, not what is

### Code Documentation Standards

#### For Go Projects

- **Public functions/types**: MUST have doc comments starting with function/type name
- **Comment style**: Clear, concise, describing what and why (not how)
- **Error messages**: Lowercase start, no punctuation
- **Current state**: Describe present behavior, not past changes

#### For TypeScript/React Projects

- **JSDoc for public APIs**: Especially for library-like modules
- **Complex logic**: Explain non-obvious patterns
- **Type annotations**: Let TypeScript types self-document when possible
- **Avoid obvious comments**: Don't explain what code clearly shows

## Documentation Workflow

### Phase 1: Analyze Context

1. **Review existing patterns**
   - Check project-specific CLAUDE.md
   - Identify target audience
   - Understand documentation conventions

2. **Assess current state**
   - Read existing documentation
   - Identify gaps or inconsistencies
   - Check for outdated information

### Phase 2: Verify Compliance

1. **Length limits**
   - README.md: ≤ 150 lines
   - CLAUDE.md: Focus on principles, not exhaustive details

2. **Content quality**
   - Remove temporal/historical information
   - Replace hardcoded metrics with CI badges
   - Eliminate redundant information

3. **Markdown quality**
   - Run `mcp__ide__getDiagnostics` to check errors
   - Follow markdownlint rules (`~/.markdownlint.jsonc`)

### Phase 3: Structure Optimization

1. **Organize logically**
   - Most important information first
   - Clear, scannable headings
   - Appropriate formatting (code blocks, lists, emphasis)

2. **Internal consistency**
   - Validate internal links
   - Ensure consistent terminology
   - Maintain uniform style

### Phase 4: Quality Assurance

1. **Accuracy verification**
   - Ensure documentation matches current codebase
   - Test code examples
   - Validate all references

2. **Consistency check**
   - Compare with project conventions
   - Verify alignment with CLAUDE.md standards
   - Check language consistency

## Code Documentation Validation

### Coverage Check

- **Go**: Verify all exported functions/types have doc comments
- **TypeScript**: Check public API documentation completeness
- **Identify missing documentation** for complex logic

### Quality Assessment

- Comments explain "why" not "what" (code shows what)
- Descriptions are clear and concise
- Technical terms used accurately
- Examples provided where helpful

### Maintenance Flags

- Identify outdated comments that don't match current code
- Flag TODO/FIXME comments that should be addressed
- Detect redundant comments that add no value

## Output Format

When providing recommendations:

1. **Specific issues**: List exact problems with file/line references
2. **Suggested improvements**: Provide concrete, actionable changes
3. **Rationale**: Explain why changes align with project standards
4. **Priority**: Indicate severity (critical, important, nice-to-have)
5. **Examples**: Show before/after where helpful

## Integration with Other Skills

- **code-reviewer**: Flag documentation issues during code review
- **git-commit-assistant**: Ensure documentation is updated before commit
- **knowledge-manager**: Record documentation patterns and best practices

## Maintenance

Update this Skill when:

- Documentation standards evolve
- New documentation types are introduced
- Team feedback suggests improvements
- New projects require different conventions
