---
name: creo-design-review
description: >
  Comprehensive UI/UX design review with Playwright. Evaluates responsive design
  (375-1920px), WCAG AA accessibility, Nielsen's 10 heuristics, component consistency,
  and visual polish. Trigger keywords: design review, UI review, accessibility audit,
  responsive check, heuristic evaluation.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# Design Review

Conduct comprehensive UI/UX reviews of web applications using Playwright for automated interaction testing. Produces structured implementation roadmaps for the creo-design-implement skill.

## Commands

| Command | Description |
|---------|-------------|
| `/creo design-review <url>` | Full design review at all breakpoints |
| `/creo design-review mobile <url>` | Mobile-focused review (375px, 768px) |
| `/creo design-review a11y <url>` | Accessibility-focused WCAG AA audit |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Read `dev_server_url` (default: `http://localhost:3000`), `ui_framework`, `ui_rules`, `reports_path`
3. Load project extension if it exists at `.claude/skills/creo-design-review/creo-design-review-{project_id}.md`. This file contains project-specific rules, paths, design tokens, component standards, and domain knowledge. `{project_id}` comes from `project-config.md`. Always load it before doing work.
4. If no config exists, use defaults or ask user

### Phase 1: Environment Setup

- Expected URL: read from project config, default `http://localhost:3000`
- Do NOT start the server -- expect it to be already running
- If server is not available, stop work and inform user immediately
- If MCP connection fails, close browser and retry navigation

### Phase 2: Principle-Based Analysis

Evaluate the current implementation against design principles:

- Visual hierarchy and information architecture
- Component consistency and design system adherence
- Accessibility compliance (WCAG 2.1 AA)
- Responsive design and mobile optimization

### Phase 3: Comprehensive Assessment

Use Playwright MCP tools for automated testing:

- **Navigation**: browser navigate to target pages
- **Interactions**: click, type, select for functional testing
- **Screenshots**: capture visual evidence at each breakpoint
- **Viewport testing**: resize to 375px, 768px, 1440px, 1920px
- **DOM analysis**: snapshot for structural review
- **Console**: check for errors and warnings

### Phase 4: Implementation Roadmap

Create a prioritized task list:

- **Blockers**: Critical issues preventing functionality
- **High-Priority**: Significant UX/accessibility problems
- **Medium-Priority**: Visual consistency improvements
- **Enhancements**: Polish and optimization opportunities

### Report Structure

```markdown
# Design Review and Implementation Roadmap

## Executive Summary
[Current state assessment and principle compliance overview]

## Design Principles Analysis
### [Principle Name]
- Current State: [How well implemented]
- Gap Analysis: [What is missing or wrong]
- Impact: [User experience implications]

## Implementation Tasks

### Blockers (Critical)
- [ ] Task 1: [Specific action needed]

### High-Priority
- [ ] Task 1: [Specific action needed]

### Medium-Priority
- [ ] Task 1: [Specific action needed]

### Enhancements
- [ ] Task 1: [Specific action needed]

## Verification Screenshots
[Screenshots at different breakpoints]

## Next Steps
This report should be passed to creo-design-implement for systematic implementation.
```

### Report Output

Save the complete report to: `.claude/reports/design-review-[timestamp].md`

The review is NOT complete until the report file is created and saved.

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/design-principles.md` | Design principles checklist |
| `references/wcag-checklist.md` | WCAG 2.1 AA compliance items |

## Quality Gates

- Every review must produce a written report file
- All four breakpoints (375px, 768px, 1440px, 1920px) must be tested
- Screenshots must be captured as visual evidence
- Issues must be categorized by priority level
- Report must include actionable tasks with specific file/component references
- Maintain objectivity while being constructive
- Balance perfectionism with practical delivery timelines
