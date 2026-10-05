---
name: creo-ux-internal
description: >
  Analyze your own application UX flows by combining screenshots, code reading,
  and live UI testing. Identifies pain points, evaluates Nielsen heuristics, maps
  user journeys, and proposes simplifications using JTBD framework. Trigger keywords:
  UX analysis, internal UX, flow analysis, pain points, user journey, heuristic evaluation.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# Internal UX Analysis

Analyze your own application by combining existing screenshots, code reading, and live UI testing. Documents findings using JTBD framework, Nielsen's heuristics, and journey maps, then proposes concrete simplifications.

## Commands

| Command | Description |
|---------|-------------|
| `/creo ux-internal <flow>` | Analyze a specific feature or flow |
| `/creo ux-internal full` | Full application UX analysis |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Read `dev_server_url` (default: `http://localhost:3000`), `screenshots_path`, `reports_path`
c3. Load project extension if it exists at `.claude/skills/creo-ux-internal/creo-ux-internal-{project_id}.md`. This file contains project-specific user flows, JTBD, domain terminology, and feature mapping. `{project_id}` comes from `project-config.md`. Always load it before doing work.
4. If no config exists, use defaults or ask user

### Phase 0: Screenshot Analysis (Do First)

Check for existing screenshots in `screenshots/` or `.claude/screenshots/`.

1. Read all screenshots using the Read tool (multimodal)
2. Create initial observations table: Screenshot, First Impression, Obvious Issues, Questions
3. Identify patterns across screens (consistency issues, repeated problems)
4. Note specific elements that need live testing verification
5. Document hypotheses to verify in Phase 2

What to look for in screenshots:
- Visual hierarchy: Is the most important info prominent?
- Information density: Too much or too little on screen?
- Button placement: Are CTAs obvious and accessible?
- Form design: Are fields grouped logically?
- Navigation clarity: Can user understand where they are?
- Error states, empty states, loading states
- Mobile readiness

### Phase 1: Code Analysis

Read project overview and architecture rules first. Then analyze:
- Data models and relationships
- State management patterns
- API endpoints and data flow
- Decision points and branches

### Phase 2: Live Testing

Read `dev_server_url` from config, default: `http://localhost:3000`.

If server not running: STOP and report to user.

Navigation process:
1. Navigate to feature entry point
2. Take full page screenshot at each step
3. Interact as a real user would
4. Note confusion points and friction

### Phase 3: Professional Analysis

#### JTBD Framework
> When [situation], I want to [motivation], so I can [expected outcome].

#### Nielsen's 10 Heuristics (Score 0-4)

| # | Heuristic | What to Check |
|---|-----------|---------------|
| 1 | Visibility of system status | Loading states, feedback |
| 2 | Match with real world | Language, familiar concepts |
| 3 | User control and freedom | Undo, cancel, back |
| 4 | Consistency | Same patterns everywhere |
| 5 | Error prevention | Validation, confirmations |
| 6 | Recognition vs recall | Visible options, suggestions |
| 7 | Flexibility | Shortcuts, bulk actions |
| 8 | Minimalist design | Only necessary elements |
| 9 | Error recovery | Clear error messages |
| 10 | Help and documentation | Tooltips, help text |

#### Severity Scale
- 4 = Catastrophe (blocks task)
- 3 = Major (significant struggle)
- 2 = Minor (noticeable friction)
- 1 = Cosmetic
- 0 = Not an issue

### Phase 4: Simplification Proposals

For each issue document:
- Heuristic reference and severity
- Location (file path and line)
- Current behavior with screenshot reference
- Proposed simplified version
- Implementation steps (specific file changes)
- Impact: steps reduced, effort level

Simplification patterns to consider:
1. **Progressive Disclosure** -- Hide advanced options
2. **Smart Defaults** -- Pre-fill common choices
3. **Flow Consolidation** -- Merge steps
4. **Inline Actions** -- Edit in place

### Report Output

Save to: `.claude/reports/internal-ux-[feature]-[YYYYMMDD].md`

Report must include:
- Executive Summary
- Screenshot initial observations
- Business logic from code
- JTBD analysis
- User journey map with emotion curve
- Nielsen heuristic scores (total out of 40)
- Complexity metrics (steps, decisions, fields, time)
- Simplification proposals by severity
- Implementation roadmap (quick wins, medium effort, larger changes)
- Success metrics

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/nielsen-heuristics.md` | Detailed heuristic evaluation guide |
| `references/jtbd-framework.md` | JTBD analysis templates |

## Quality Gates

- Screenshots must use full page capture
- Every heuristic must be scored with evidence
- Each simplification proposal must include specific file paths
- Proposals must include effort estimates
- Report must be saved as a file (review is not complete without it)
- Live testing must be performed unless explicitly skipped by user
