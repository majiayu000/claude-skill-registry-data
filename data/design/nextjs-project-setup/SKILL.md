---
name: nextjs-project-setup
description: Comprehensive Next.js project setup from scratch following industry best practices. Use when creating new Next.js projects, requiring template selection, design system ideation, specifications, wireframes, implementation with TDD, QA validation, and complete documentation. Handles both simple quick-start and complex multi-phase projects with sub-agent orchestration.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__vercel__*, mcp__shadcn__*, mcp__supabase__*, mcp__21st_dev__*, mcp__firecrawl__*
---

# Next.js Project Setup Skill

## Overview

This skill orchestrates complete Next.js project setup from scratch, adapting to project complexity. It handles template selection, specifications, design systems, wireframes, implementation, testing, and documentation following Claude Code best practices with optimal token efficiency through progressive disclosure and sub-agent orchestration.

**Outcomes**:
- Production-ready Next.js project
- Complete design system
- Comprehensive documentation
- Passing tests with TDD approach
- Clean, audited repository

---

## Prerequisites

<prerequisites>

This skill leverages three global skills containing 3,316 lines of curated knowledge. Reference these skills BEFORE researching:

**Global Skills Available**:
1. **shadcn-ui** (1,053 lines) - Component library, dark mode, forms, theming
   - Installation & setup
   - Component categories (forms, layouts, overlays, display)
   - Dark mode implementation
   - Customization patterns
   - Framework integration

2. **nextjs** (1,129 lines) - Next.js 15+ framework knowledge
   - App Router architecture
   - Server vs Client Components
   - Routing (static, dynamic, parallel, intercepting)
   - Data fetching patterns
   - Metadata & SEO
   - Image/Font optimization
   - Deployment patterns

3. **tailwindcss** (1,134 lines) - Design system foundation
   - Utility-first approach
   - Design tokens (colors, spacing, typography)
   - Responsive design patterns
   - Dark mode setup
   - Component examples
   - Framework integration

**Usage Pattern**:
```
Research_Flow :=
  Query global skills (300-500 tokens)
    ∘ Query MCP tools (200-400 tokens)
    ∘ Targeted reads (500-1000 tokens)
  vs Spawn research agents (8,000 tokens)

Token_Savings := 6,500+ tokens (81% reduction in research phase)
```

**When to Reference**:
- Before Phase 1 research (review what's known)
- During design system planning (shadcn + tailwind patterns)
- When selecting components (shadcn workflows)
- For Next.js best practices (nextjs patterns)
- For responsive design (tailwind breakpoints)

</prerequisites>

---

## Decision Framework

<complexity_assessment>

**Simple Project Indicators** (choose simple path if ≤1 is true):
- Standard website/blog
- No database required
- No custom authentication
- Single tenant
- Simple design requirements

**Complex Project Indicators** (choose complex path if ≥2 are true):
- Database required (Supabase)
- Custom authentication patterns
- Multi-tenant architecture
- E-commerce features
- Complex/custom design system
- Multiple integrations

**User Override**: Always ask user to confirm complexity assessment.

</complexity_assessment>

---

## Simple Path Workflow

<simple_setup>

**Use when**: Quick setup, standard requirements, minimal customization
**Duration**: 15-30 minutes
**Load**: @docs/simple-setup.md

### Quick Steps (CoD^Σ)

```
Template ← Vercel_MCP(search + select)
  ↓
Setup ← {env_vars, config, structure}
  ↓
Components ← Shadcn_MCP(core_components)
  ↓
Design ← {tailwind_config, basic_theme}
  ↓
Docs ← {README, CLAUDE.md}
```

### Execution

1. **Assess & Confirm**
   - Confirm simple path appropriate
   - Gather basic requirements

2. **Load Instructions**
   - Follow @docs/simple-setup.md completely
   - Document provides step-by-step guidance

3. **Deliverables**
   - Installed template
   - Core components configured
   - Basic design system
   - Minimal documentation
   - Ready for development

</simple_setup>

---

## Complex Path Orchestration

<complex_setup>

**Use when**: Database, auth, complex design, multi-tenant, or multiple complex features
**Duration**: 2-4 hours (with user feedback iterations)
**Pattern**: Research ∥ → Template → Spec → Design → Wireframes → Implement ∥ → QA ∥ → Docs

### Phase 1: Foundation Research

**Progress**: [█░░░░░░░] 12.5% (1/8 phases)

```
<research_phase>

**Purpose**: Gather foundational knowledge using global skills + MCP queries

**Workflow** (CoD^Σ):
```
Foundation_Knowledge :=
  Review_Global_Skills ∘ Query_MCPs ∘ Synthesize_Context

Global_Skills_Review (300-500 tokens):
  1. Reference nextjs global skill → App Router patterns, data fetching, routing
  2. Reference shadcn-ui global skill → Component workflows, dark mode, forms
  3. Reference tailwindcss global skill → Design tokens, responsive patterns

MCP_Queries (200-400 tokens):
  1. Vercel MCP → Available templates (filter by DB/auth requirements)
  2. Shadcn MCP → Component registry overview (@ui, @magicui catalogs)
  3. Supabase MCP (if DB required) → Project setup patterns
  4. 21st Dev MCP → Design inspiration (optional)

Synthesis (500-1000 tokens):
  1. Document template options → /reports/foundation-research.md
  2. Note component patterns → reference global skills
  3. Identify setup requirements → specific to project
  4. List design considerations → leverage global knowledge
```

**Token Comparison**:
- OLD: 4 agents × 2000 tokens each = 8,000 tokens
- NEW: Global skills (500t) + MCP queries (300t) + synthesis (700t) = 1,500 tokens
- **SAVINGS**: 6,500 tokens (81% reduction)

**Output**:
- /reports/foundation-research.md (concise, 700-1000 tokens)
  - Available templates summary
  - Component strategy (reference global skills)
  - Database setup approach (if applicable)
  - Design system starting point

**Key Principle**:
Don't duplicate what's in global skills - REFERENCE them. Main agent can load specific sections when needed.

**Rollback Procedure**:
```bash
# If Phase 1 fails or needs to be restarted:
rm -f reports/foundation-research.md
# Phase 1 can now be re-executed cleanly
```

**When to Rollback**:
- MCP queries fail repeatedly
- Global skills not loading properly
- Research synthesis incomplete or incorrect
- User requests different project approach

</research_phase>
```

### Phase 2: Template Selection

**Progress**: [██░░░░░░] 25.0% (2/8 phases)

```
<template_selection>

**Prerequisites**: @reports/foundation-research.md
**Load**: @docs/complex/phase-2-template.md

**Workflow**:
1. Analyze user requirements against template features
2. Use Vercel MCP to filter templates
3. Present top 3 options with rationale
4. User selects template
5. Install: `npx create-next-app --example <template>`
6. Verify installation and structure

**Outputs**:
- Installed template
- /docs/template-selection.md (rationale, features, setup notes)

**Rollback Procedure**:
```bash
# If Phase 2 fails or wrong template selected:
rm -rf * .[^.]* ..?*  # Remove all files (BE CAREFUL - only in project dir)
rm -f docs/template-selection.md
# OR: cd .. && rm -rf project-name && mkdir project-name && cd project-name
# Return to Phase 1 or retry Phase 2 with different template
```

**When to Rollback**:
- Template installation fails
- Wrong template selected
- Template doesn't match requirements
- Need to start fresh with different approach

</template_selection>
```

### Phase 3: Specification

**Progress**: [███░░░░░] 37.5% (3/8 phases)

```
<specification_phase>

**Prerequisites**: Template installed
**Load**: @docs/complex/phase-3-spec.md

**Workflow** (CoD^Σ):
```
Product_Spec := use(product-skill) → /docs/product-spec.md
Constitution := use(constitution-skill) → /docs/constitution.md
Features := {
  âˆ€feature ∈ requirements:
    feature → {description, acceptance_criteria, dependencies}
}
Audit := review ∧ clarify → user_feedback
```

**Required Skills**:
- REQUIRED SUB-SKILL: product-skill
- REQUIRED SUB-SKILL: constitution-skill

**Outputs**:
- /docs/product-spec.md
- /docs/constitution.md
- /docs/features.md
- /docs/architecture.md

**Rollback Procedure**:
```bash
# If Phase 3 fails or specifications need major revision:
rm -f docs/product-spec.md
rm -f docs/constitution.md
rm -f docs/features.md
rm -f docs/architecture.md
# Keep template and template-selection.md
# Return to Phase 3 start or Phase 2 if template needs change
```

**When to Rollback**:
- Specifications fundamentally flawed
- Major scope change required
- User rejects specification direction
- Need to restart specification from scratch

</specification_phase>
```

### Phase 4: Design System Ideation

**Progress**: [████░░░░] 50.0% (4/8 phases)

```
<design_system_phase>

**Prerequisites**: Specifications, shadcn-ui global skill, tailwindcss global skill
**Load**: @docs/complex/phase-4-design.md

**Tools**: Shadcn MCP, 21st Dev MCP
**Pattern**: Brainstorm → Showcase → Iterate → Finalize

**Workflow**:
1. **Brainstorm** (reference global skills + dispatch @.claude/agents/nextjs-design-ideator.md):
   - Review tailwindcss global skill → color systems, design tokens, responsive patterns
   - Review shadcn-ui global skill → component theming, dark mode, customization
   - Create design options:
     - Color palettes (3-4 options based on tailwind patterns)
     - Typography systems (2-3 options using tailwind scales)
     - Component styles (2-3 directions leveraging shadcn customization)
     - Layout patterns (referencing tailwind grid/flex utilities)

2. **Showcase**:
   - Create design-showcase page
   - Display all variations visually
   - Use @templates/design-showcase.md

3. **User Feedback Loop** (max 3 iterations):
   - Present showcase to user
   - Gather specific feedback
   - Refine based on feedback
   - **Iteration Limit**: Maximum 3 iterations
   - **If iteration 3 reached AND not approved**:
     - Proceed with best available option from iterations
     - Document user concerns in /docs/design-system.md
     - Mark concerns for future improvement
     - DO NOT continue iterating indefinitely

4. **Finalize**:
   - Document chosen system in /docs/design-system.md
   - Configure Tailwind (CSS variables only)
   - Set up Shadcn component structure
   - Import base components via Shadcn MCP

**Critical Rules**:
- Use global Tailwind CSS variables ONLY
- No inline custom styles
- Follow Shadcn workflow: Search → View → Example → Install
- Prioritize @ui registry for core components
- Use @magicui sparingly (subtle animations ≤300ms)

**Outputs**:
- /docs/design-system.md
- tailwind.config.ts with CSS variables
- components.json configured
- Base components installed

**Rollback Procedure**:
```bash
# If Phase 4 fails or design direction needs complete change:
rm -f docs/design-system.md
git checkout tailwind.config.ts  # Restore to template default
git checkout components.json     # Restore to template default
rm -rf components/ui/*           # Remove installed Shadcn components
# OR: git reset --hard HEAD      # If all design work needs rollback
# Return to Phase 4 start with fresh design direction
```

**When to Rollback**:
- Design direction rejected by user
- Shadcn components incompatible
- Need to restart with different design system
- Tailwind configuration conflicts

</design_system_phase>
```

### Phase 5: Wireframes & Asset Management

**Progress**: [█████░░░] 62.5% (5/8 phases)

```
<wireframes_phase>

**Prerequisites**: Design system, specifications
**Load**: @docs/complex/phase-5-wireframes.md

**Pattern**: Assets → Wireframes → Iterate

**5.1 Image Asset Management**:
```
IF user_provides_images THEN:
  1. Inventory ← list(all_images)
  2. ∀image:
     - Describe(image)
     - Rename(descriptive_name)
     - Categorize(purpose)
  3. Document → /assets/inventory.md
  4. Reference in wireframes
ELSE:
  Note missing assets in wireframes
```

**5.2 Wireframe Generation**:
1. **Brainstorm Options**:
   - Create 2-3 layout variations per major page
   - Use text-based wireframes (detailed)
   - Reference design system components
   - Include image placeholders with @asset references

2. **Template**: Use @templates/wireframe-template.md

3. **User Feedback Loop** (max 3 iterations):
   - Present wireframe options to user
   - Discuss pros/cons of each approach
   - Refine based on UX/conversion/accessibility feedback
   - **Iteration Limit**: Maximum 3 iterations
   - **If iteration 3 reached AND not approved**:
     - Proceed with best available option from iterations
     - Document user concerns in /docs/wireframes/concerns.md
     - Mark layout decisions as "provisional, pending future refinement"
     - DO NOT continue iterating indefinitely

4. **Expert Evaluation** (for each option):
   - UX best practices
   - Conversion optimization
   - Accessibility (WCAG 2.1 AA)
   - Mobile-first approach
   - SEO considerations

**Outputs**:
- /docs/wireframes/*.md (one file per page/section)
- /assets/inventory.md (if images provided)
- Finalized layouts approved by user

**Rollback Procedure**:
```bash
# If Phase 5 fails or wireframes need major revision:
rm -rf docs/wireframes/
rm -f assets/inventory.md
# Keep design system from Phase 4
# Return to Phase 5 start or Phase 4 if design system also needs revision
```

**When to Rollback**:
- Wireframe layouts rejected
- Asset management issues
- Need to restart with different layout approach
- Major UX/accessibility concerns discovered

</wireframes_phase>
```

### Phase 6: Implementation

**Progress**: [██████░░] 75.0% (6/8 phases)

```
<implementation_phase parallel="true">

**Prerequisites**: Wireframes, design system, template
**Load**: @docs/complex/phase-6-implement.md

**Pattern**: TDD + Parallel + Visual Validation

**Core Principles**:
1. **TDD Mandatory**: Tests before implementation, no exceptions
2. **Visual Validation**: Every page reviewed before marking complete
3. **Interaction Testing**: All links, buttons, animations validated
4. **Parallel Execution**: Independent features via sub-agents

**Workflow** (CoD^Σ):
```
∀feature ∈ features:
  Tests ← define(acceptance_criteria) FIRST
  Implementation ← code(feature) | tests_pass
  Components ← Shadcn_MCP(Search → View → Example → Install)
  Visual_Review ← validate(render ∧ interactions ∧ responsiveness)
  âœ" ⇔ (tests_pass ∧ visual_validated ∧ interactions_work)

Parallel := {
  features[independent] ∥ via sub-agents,
  qa_agent ∥ validation
}

Database (if applicable):
  Supabase_MCP ONLY (never CLI)
  Schema → RLS → Edge_Functions
  Server_Actions for mutations
```

**Component Management**:
- Use Shadcn MCP for all components
- Prefer Magic UI registry for enhanced components
- Follow: Search → View → Example → Install (never skip Example)
- Global Tailwind CSS variables (no hardcoded colors)

**Database Setup** (if applicable):
- Use Supabase MCP tools ONLY
- Start with staging environment
- Define schema requirements strictly
- Implement RLS policies
- Follow template auth patterns
- Multi-tenant: additional patterns per template

**Testing Setup**:
- Linting configuration
- GitHub workflows / CI/CD
- Test framework setup
- Visual regression testing

**Outputs**:
- Complete codebase
- Passing test suite
- Visually validated pages
- Database schema (if applicable)
- CI/CD configured

**Rollback Procedure**:
```bash
# If Phase 6 fails or implementation needs restart:
# Option 1: Soft rollback (keep some work)
git status                          # Review changes
git stash                           # Stash current work
git reset --hard HEAD~N             # Reset N commits back
git stash pop                       # Optionally restore parts

# Option 2: Hard rollback (nuclear option)
git reset --hard <commit-before-phase-6>  # Reset to before Phase 6
git clean -fd                             # Remove untracked files

# Option 3: Selective rollback
git revert <commit-hash>            # Revert specific commits

# After rollback:
npm install                         # Restore dependencies if needed
# Return to Phase 6 start with clean state
```

**When to Rollback**:
- Tests failing consistently
- Implementation approach fundamentally flawed
- Database schema needs complete redesign
- Need to restart with different architecture

</implementation_phase>
```

### Phase 7: Quality Assurance (Parallel)

**Progress**: [███████░] 87.5% (7/8 phases)

```
<qa_phase parallel="true">

**Prerequisites**: Implementation in progress
**Load**: @docs/complex/phase-7-qa.md
**Agent**: @.claude/agents/nextjs-qa-validator.md (runs continuously)

**Validation Checklist**:

**Critical (Must Fix)**:
- [ ] All tests passing
- [ ] Visual validation complete
- [ ] All links functional
- [ ] All buttons working
- [ ] All forms submitting
- [ ] All animations smooth (≤300ms)
- [ ] Mobile responsive
- [ ] Accessibility compliant (WCAG 2.1 AA)

**Important (Should Fix)**:
- [ ] Performance optimized
- [ ] SEO meta tags
- [ ] Error handling
- [ ] Loading states
- [ ] Empty states

**Process**:
1. QA agent validates continuously
2. Reports issues immediately
3. Implementation agents fix
4. Re-validate
5. No task marked complete until QA ✓

**Outputs**:
- QA report
- Issue tracking
- Resolution verification

**Rollback Procedure**:
```bash
# If Phase 7 identifies critical issues requiring major rework:
# Option 1: Fix issues incrementally (preferred)
git commit -am "WIP: Before QA fixes"  # Save current state
# Fix issues one by one
# Re-run QA validation after each fix

# Option 2: Rollback to last stable state
git log --oneline                   # Find last stable commit
git reset --hard <last-stable-commit>

# Option 3: Return to Phase 6
# Use Phase 6 rollback procedures
# Re-implement with QA feedback in mind

# After rollback:
# Address root causes identified by QA
# Return to implementation with fixes
```

**When to Rollback**:
- Too many critical QA failures
- Implementation needs fundamental architectural change
- Accessibility issues require major refactor
- Performance issues require complete redesign

</qa_phase>
```

### Phase 8: Documentation & Audit

**Progress**: [████████] 100% (8/8 phases)

```
<documentation_phase>

**Prerequisites**: Implementation complete, QA passing
**Load**: @docs/complex/phase-8-docs.md
**Agent**: @.claude/agents/nextjs-doc-auditor.md

**Documentation Structure**:
```
project-root/
├── CLAUDE.md                    # Main context (comprehensive)
│   ├── Overview (2-3 sentences)
│   ├── Tree structure
│   ├── Tech stack
│   ├── Development workflow
│   ├── Skills/commands to use
│   ├── MCP tool usage
│   ├── Conventions
│   └── Anti-patterns
├── /docs/
│   ├── architecture.md          # System architecture
│   ├── design-system.md         # Design tokens
│   ├── database-schema.md       # DB structure
│   ├── product-spec.md          # Product requirements
│   ├── constitution.md          # Project principles
│   └── features.md              # Feature specifications
├── /components/CLAUDE.md        # Component conventions
├── /app/CLAUDE.md               # Routing conventions
└── /lib/CLAUDE.md               # Utility conventions
```

**CLAUDE.md Template**: Use @templates/claude-md-template.md

**Audit Process**:
1. Doc auditor agent reviews all documentation
2. Checks completeness, accuracy, consistency
3. Verifies file structure compliance
4. Identifies missing docs
5. Cleans up messy files
6. Validates all references work
7. Ensures CoD^Σ used appropriately

**Outputs**:
- Complete documentation hierarchy
- Clean, organized repository
- Audit report
- All references functional

**Rollback Procedure**:
```bash
# If Phase 8 documentation needs complete overhaul:
# Option 1: Restore from backup (if created before Phase 8)
cp -r ../project-backup/* .         # Restore entire project
# OR: git worktree for backup
# git worktree add ../backup <commit-before-phase-8>

# Option 2: Selective documentation rollback
rm -f CLAUDE.md
rm -rf docs/
git checkout HEAD~N -- CLAUDE.md docs/  # Restore N commits ago
# OR: Use git reflog to find exact state

# Option 3: Keep code, regenerate docs
# Keep all implementation and QA work
# Delete only documentation files
rm -f CLAUDE.md
rm -rf docs/*.md
# Return to Phase 8 start with fresh documentation

# Create backup before Phase 8 (prevention):
git tag phase-8-start
git archive --format=tar.gz -o ../project-phase-7-complete.tar.gz HEAD
```

**When to Rollback**:
- Documentation structure fundamentally wrong
- Audit reveals major inconsistencies
- Need to restart documentation from scratch
- References broken beyond repair

**Prevention (Recommended)**:
- Create git tag before Phase 8: `git tag phase-8-start`
- Create backup: `tar -czf ../backup-$(date +%Y%m%d).tar.gz .`
- Enables safe documentation experimentation

</documentation_phase>
```

</complex_setup>

---

## MCP Tool Usage Guidelines

<mcp_tools>

### Vercel MCP

**Purpose**: Template discovery, deployment

**Workflow**:
```
Search(category, features) → Filter → Compare → Select → Install
```

**Commands**:
- List templates: Filter by DB, auth, use case
- Get info: Detailed template features
- Install: `npx create-next-app --example <template>`

### Shadcn MCP

**Purpose**: Component discovery and installation

**Critical Workflow** (NEVER skip steps):
```
Search → View → Example → Install
```

**Registries**:
- `@ui`: Core components (check first always)
- `@magicui`: Animated components (use sparingly, ≤300ms)
- `@elevenlabs`: Audio/voice components (if applicable)

**Rules**:
1. ALWAYS follow Search → View → Example → Install
2. NEVER skip Example step
3. Prioritize @ui for foundation
4. Use @magicui animations sparingly
5. Install one component at a time
6. Verify integration after each install

**Example**:
```bash
# Search
mcp__shadcn__search_items_in_registries([@ui, @magicui], "button")

# View details
mcp__shadcn__view_items_in_registries(["@ui/button"])

# Get example
mcp__shadcn__get_item_examples_from_registries([@ui], "button-demo")

# Install
mcp__shadcn__get_add_command_for_items(["@ui/button"])
# Execute: npx shadcn@latest add button
```

### Supabase MCP

**Purpose**: Database and auth setup

**Critical Rule**: NEVER use Supabase CLI, ALWAYS use MCP tools

**Workflow**:
```
Schema_Design → Create_Tables → RLS_Policies → Auth_Setup → Edge_Functions
```

**Best Practices**:
- Start with staging environment
- Define schema requirements strictly before creating
- Implement RLS policies immediately
- Use server actions for mutations
- Edge functions for API routes
- Follow template auth patterns
- Multi-tenant: additional RLS patterns

### 21st Dev MCP

**Purpose**: Component inspiration and discovery

**Usage**:
- Search for UI inspiration
- Find pre-built components
- Copy-paste-adapt workflow
- Not for installation (manual integration)

</mcp_tools>

---

## Quality Standards & Requirements

<quality_standards>

### Token Efficiency
- Simple path: ≤2000 tokens total
- Complex orchestrator: ≤2500 tokens main context
- Sub-agent reports: ≤2500 tokens each
- Micro-docs: 500-1000 tokens each
- Use CoD^Σ notation where appropriate

### TDD Approach
- **Iron Law**: No code without tests first
- **Process**: RED (test fails) → GREEN (minimal code) → REFACTOR (improve)
- **No Exceptions**: "Just this once" is never acceptable
- **Validation**: All tests must pass before marking complete

### Visual Validation
- **Required**: Every page/component must be visually reviewed
- **Check**: Render, layout, responsiveness, interactions
- **Test**: Links, buttons, forms, animations, loading states
- **Criteria**: Mobile-first, accessible, performant

### Documentation
- **Comprehensive**: CLAUDE.md + folder docs + /docs/*
- **Current**: Updated continuously throughout project
- **Structured**: Domain-separated, focused docs
- **Referenced**: Use @references for cross-linking
- **Compressed**: Use CoD^Σ where beneficial

### Clean Repository
- **Organized**: Clear folder structure
- **Documented**: Every folder has purpose
- **Audited**: Regular cleanup and review
- **Tracked**: State documented and current

### Accessibility
- **Standard**: WCAG 2.1 AA minimum
- **Testing**: Use accessibility tools
- **Keyboard**: Full keyboard navigation
- **Screen readers**: Proper ARIA labels
- **Contrast**: Sufficient color contrast

</quality_standards>

---

## Anti-Patterns (Do NOT Do)

<anti_patterns>

### MCP Tools
❌ Using Supabase CLI instead of MCP
   **Why**: MCP provides better error messages, type safety, and integrates with Claude Code workflows; CLI bypasses these safeguards and causes integration issues.

❌ Skipping Shadcn Example step
   **Why**: Examples reveal real-world usage patterns, edge cases, and integration requirements that prevent bugs discovered only after installation.

❌ Not following Search→View→Example→Install workflow
   **Why**: Each step provides critical context (search: availability, view: API, example: usage patterns, install: dependencies); skipping steps causes mismatched expectations and integration failures.

❌ Installing multiple Shadcn components without testing each
   **Why**: Components have complex dependencies and theming interactions; testing each individually isolates issues, while bulk installation creates debugging nightmares.

### Code Quality
❌ Writing code before writing tests
   **Why**: Tests written after code merely confirm existing behavior (not requirements); tests-first ensures implementation meets actual acceptance criteria and catches logic errors early.

❌ Skipping visual validation
   **Why**: Automated tests miss layout breaks, responsive issues, animation glitches, and accessibility problems that only appear when humans interact with rendered UI.

❌ Marking tasks complete without verification
   **Why**: "Done" without verification creates technical debt and false progress; only passing tests and working demos prove completion.

❌ Using inline custom Tailwind styles
   **Why**: Inline styles bypass the design system, create inconsistency, break dark mode, and make theme changes require hunting through every component instead of updating CSS variables.

❌ Hardcoding colors instead of CSS variables
   **Why**: Hardcoded colors break theme switching, prevent design system updates, violate accessibility requirements (can't adjust contrast), and create unmaintainable color sprawl.

### Documentation
❌ Missing CLAUDE.md files
   **Why**: AI agents and developers need project context (conventions, commands, architecture) to work effectively; missing CLAUDE.md causes repeated questions and inconsistent code.

❌ Outdated documentation
   **Why**: Stale docs are worse than no docs—they mislead developers into wrong approaches, waste time debugging non-issues, and erode trust in all documentation.

❌ Putting reusable patterns in CLAUDE.md (use skills)
   **Why**: CLAUDE.md is project-specific context; reusable patterns belong in skills for discoverability, maintenance, and cross-project sharing. Duplication across projects causes drift.

❌ Force-loading with @path (use skill name references)
   **Why**: Direct path references break when files move and bypass progressive disclosure; skill name references enable metadata-first loading and graceful updates.

### Project Structure
❌ Monolithic, unorganized code
   **Why**: Monoliths slow development (hard to find code), increase bugs (unclear boundaries), prevent parallel work (merge conflicts), and make testing difficult (tangled dependencies).

❌ No clear folder conventions
   **Why**: Inconsistent organization wastes time searching for files, creates duplicate implementations (can't find existing code), and makes onboarding painful.

❌ Missing folder-level documentation
   **Why**: Folders represent architectural boundaries; undocumented boundaries cause developers to put files in wrong places, violate separation of concerns, and create spaghetti imports.

❌ Bloated, messy repository
   **Why**: Repository clutter (unused files, commented code, temp files) obscures actual codebase, slows searches, confuses intent, and signals low quality standards.

### Workflow
❌ Sequential execution when parallel is possible
   **Why**: Sequential work wastes time (wait for task A to finish B) when tasks are independent; parallel execution uses resources efficiently and delivers faster.

❌ Duplicate research across agents
   **Why**: Multiple agents researching same topic wastes tokens, creates inconsistent findings (each agent sees different sources), and delays results unnecessarily.

❌ Bloating main context with research details
   **Why**: Main context is finite and expensive; research details (150k token logs, full API docs) crowd out reasoning space. Use subagents for heavy analysis, return summaries only.

❌ Not using sub-agents for isolated tasks
   **Why**: Complex tasks in main context pollute with noise (debug logs, search results, intermediate states); subagents isolate noise, return clean summaries, and keep main context focused on high-level coordination.

</anti_patterns>

---

## Sub-Agent Coordination

<sub_agent_orchestration>

### When to Use Sub-Agents

**Use for**:
- Parallel research (multiple topics simultaneously)
- Isolated task execution (fresh context)
- Independent feature implementation
- QA validation (continuous monitoring)
- Documentation audit (independent review)

**Don't use for**:
- Simple linear tasks
- Tasks requiring main conversation context
- Quick one-off operations

### Handover Protocol

**Pattern**:
```
Main Agent:
  1. Define task clearly
  2. Specify output format and location
  3. List required tools
  4. Set token budget
  5. Dispatch sub-agent
  
Sub-Agent:
  1. Execute task in isolated context
  2. Write concise report
  3. Save to specified location
  4. Signal completion
  
Main Agent:
  1. Read report (not full process)
  2. Continue workflow
```

### Report Template

All sub-agents use this structure:

```markdown
# [Task Name] Report

## Summary (1-2 sentences)
[Key finding or recommendation]

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Recommendations
[Specific, actionable recommendations]

## Details
[Supporting information, kept concise]

## References
[Sources, if applicable]
```

**Target**: 1500-2500 tokens per report

### Agent Token Truncation Protocol

**Purpose**: Enforce token limits on agent reports to prevent context pollution while preserving critical information

**Hard Limit**: 2500 tokens per agent report (ENFORCED)

**Automatic Truncation Behavior**:

When an agent report approaches 2500 tokens:

1. **Keep** (Priority Order):
   - Executive summary (1-2 sentences)
   - Key findings (bullet points, max 5)
   - Actionable recommendations (specific, concise)
   - Critical errors or blockers
   - File:line references for evidence

2. **Truncate** (Deprioritize):
   - Detailed examples (keep brief versions only)
   - Verbose explanations (compress to essentials)
   - Redundant context (already in main conversation)
   - Step-by-step process details (unless critical)
   - Extensive code snippets (keep signatures/interfaces only)

3. **Truncation Marker**:
   ```markdown
   [TRUNCATED at 2500 tokens - Request [CONTINUE: section-name] for more details]

   Available sections for continuation:
   - detailed-examples: Full code examples with explanations
   - process-steps: Step-by-step implementation details
   - alternative-approaches: Other solutions considered
   - edge-cases: Additional scenarios and handling
   ```

**Continuation Mechanism**:

Main agent can request additional details:

```markdown
[CONTINUE: detailed-examples]

Reason: Need to understand implementation approach
Focus: Color palette generation algorithm
```

Agent responds with focused continuation (≤1500 tokens):

```markdown
# Continuation: Detailed Examples

[Focused content for requested section only]

[END CONTINUATION - Request [CONTINUE: section-name] for other sections]
```

**Token Budget Breakdown** (for 2500 token reports):
- Executive summary: 100-150 tokens
- Key findings: 300-400 tokens (5 bullets × 60-80 tokens each)
- Recommendations: 200-300 tokens
- Details: 1500-1700 tokens (truncated if needed)
- References: 200-300 tokens

**Enforcement Rules**:
- Agents MUST check token count before returning report
- IF report > 2500 tokens → automatic truncation with marker
- Main agent CAN request continuation (unlimited follow-ups)
- Each continuation ≤1500 tokens (focused on specific section)
- NO agent report may exceed 2500 tokens in initial response

**Example Truncated Report**:

```markdown
# Design System Analysis Report

## Summary
Analyzed 15 design system options. Recommend Option 3 (Tailwind + Shadcn) for token efficiency and flexibility.

## Key Findings
- Option 1 (Material UI): Heavy bundle (250KB), limited customization
- Option 2 (Chakra UI): Good DX, moderate bundle (180KB), theme API verbose
- Option 3 (Tailwind + Shadcn): Minimal bundle (40KB with tree-shaking), full control, CSS variables
- Option 4 (Ant Design): Enterprise features, heavy (300KB), opinionated
- Option 5 (Custom): Maximum flexibility, high maintenance, design debt risk

## Recommendations
1. Use Tailwind CSS + Shadcn UI (Option 3)
   - Rationale: Smallest bundle, full customization, active ecosystem, CSS variables
   - Trade-off: Manual composition vs. pre-built components
2. Initialize with `npx shadcn@latest init` (New York style, CSS variables)
3. Start with 8 core components: button, card, input, label, form, toast, alert, dialog

## Implementation Details

### Color System
CSS variables approach enables theme switching:
```css
:root {
  --primary: 222.2 47.4% 11.2%;
  --secondary: 210 40% 96.1%;
  ...
}
```

[TRUNCATED at 2500 tokens - Request [CONTINUE: section-name] for more details]

Available sections for continuation:
- component-examples: Full Shadcn component integration examples
- theme-configuration: Complete tailwind.config.ts setup
- dark-mode-implementation: Dark mode strategy with next-themes
- accessibility-patterns: WCAG 2.1 AA compliance approach

## References
- Tailwind CSS docs: @global-skills/tailwindcss
- Shadcn UI catalog: @MCP/shadcn
- Analysis file: /tmp/design-system-analysis.json
```

**Benefits**:
- **Context Efficiency**: Main conversation stays focused (≤2500t per report)
- **Information Preservation**: Full details available on-demand via continuation
- **Clear Signals**: Truncation markers show what's available
- **Flexible Depth**: Main agent controls detail level (request more when needed)

### Agent Clarification Protocol

**Purpose**: Enable agents to request additional information when reports are insufficient

**When Agents Need Clarification**:
- Report lacks critical details for next phase
- Requirements ambiguous or conflicting
- User intent unclear from available context
- Technical approach needs validation
- Edge cases or constraints not specified

**Protocol Markers**:

**1. Request Clarification** (from Agent to Main):
```markdown
[CLARIFY: Specific question here?]

Context: [Brief context why clarification needed]
Options: [If applicable, suggest 2-3 options]
Impact: [What decision this affects]
```

**2. Provide Answer** (from Main to Agent):
```markdown
[ANSWER: Clear, focused response]

Rationale: [Why this decision]
Constraints: [Any limitations or considerations]
```

**3. Request Continuation** (for truncated reports):
```markdown
[CONTINUE: section-name]

Reason: [Why more detail needed]
Focus: [Specific aspect to expand]
```

**Example Exchange**:
```markdown
# Design Agent Report (Phase 4)

## Color Palette Options
... [content truncated at 2500 tokens]

[CLARIFY: Should we prioritize accessibility (WCAG AAA) or brand alignment?]

Context: Brand colors may not meet AAA contrast ratios
Options:
  1. Adjust brand colors slightly for AAA compliance
  2. Use brand colors, meet AA only (still compliant)
  3. Create accessibility-first palette, suggest brand update
Impact: Affects all component theming and documentation
```

**Main Agent Response**:
```markdown
[ANSWER: Prioritize accessibility with Option 1]

Rationale: Accessibility is constitutional requirement (WCAG 2.1 AA minimum)
Constraints: Keep brand colors within 10% adjustment if possible
Next: Proceed with accessibility-first palette, document brand color deltas
```

**Token Limits**:
- Clarification request: ≤200 tokens
- Answer: ≤1000 tokens (focused, specific)
- Continuation request: ≤100 tokens
- Continuation response: ≤1500 tokens (additional details)

**Rules**:
1. One clarification per report maximum (prevents back-and-forth loops)
2. Questions must be specific and actionable
3. Provide 2-3 options when possible (not open-ended)
4. Main agent must answer before agent continues
5. If answer requires user input, main agent queries user first

**Handling Edge Cases**:
```
IF agent_needs_clarification AND no_response:
  agent_proceeds_with_best_assumption
  documents_assumption_clearly
  marks_decision_as [ASSUMPTION: rationale]
  enables_easy_rollback

IF multiple_clarifications_needed:
  prioritize_blocking_decisions
  defer_nice-to-have_clarifications
  proceed_with_partial_information
```

**Benefits**:
- Prevents agents getting stuck
- Enables informed decision-making
- Documents decision points
- Maintains workflow momentum
- Clear audit trail

</sub_agent_orchestration>

---

## Progressive Disclosure Pattern

<progressive_disclosure>

**Principle**: Load only what's needed, when needed

**Levels**:
1. **Metadata** (always loaded): Skill name/description, available commands
2. **Core Instructions** (loaded on trigger): This SKILL.md file
3. **Phase Docs** (loaded on reference): @docs/complex/phase-*.md
4. **Templates** (loaded as needed): @templates/*.md
5. **Sub-agents** (dispatched when needed): @agents/*.md

**Usage**:
```
# ✓ Correct - reference by name
Use @docs/complex/phase-4-design.md for design system workflow

# ✗ Wrong - don't force-load full paths
Read @~/.claude/skills/nextjs-project-setup/docs/complex/phase-4-design.md
```

**Benefits**:
- Minimal token usage
- Focused context
- Faster processing
- Better maintainability

**Progressive Loading Budget** (Token Allocation):

**Total Maximum**: ~16,500 tokens (complex path, all levels loaded)

**Breakdown by Level**:
- **Level 1 (Metadata)**: 30-50 tokens
  - YAML frontmatter (name, description, allowed-tools)
  - Always loaded at session start
  - Cost: Persistent throughout session

- **Level 2 (Core Instructions)**: 2,000-2,500 tokens
  - SKILL.md main body
  - Loaded when skill triggered by description match
  - Cost: One-time per skill invocation

- **Level 3 (Phase Docs)**: 500-1,000 tokens × 4 files = 2,000-4,000 tokens
  - @docs/simple-setup.md (550 lines ~2,500t)
  - @docs/complex/*.md (4 consolidated files, ~1,000t each)
  - Loaded on-demand via @ reference
  - Cost: Only when phase explicitly referenced

- **Level 4 (Templates)**: 200-500 tokens × 5 templates = 1,000-2,500 tokens
  - design-showcase.md, wireframe-template.md, report-template.md, etc.
  - Loaded on-demand when template needed
  - Cost: Only when output format required

- **Level 5 (Sub-agents)**: 2,500 tokens × 3 agents = 7,500 tokens
  - Agent reports (truncated at 2,500t each)
  - Isolated context (100k per agent, returns summary only)
  - Cost: Per agent invocation, main thread receives summary only

**Budget Management**:
```
Minimal Path (Simple setup):
  L1 (50t) + L2 (2,500t) + L3 simple-setup (2,500t) = ~5,000t

Typical Path (Complex, 2 phases + 1 agent):
  L1 (50t) + L2 (2,500t) + L3 (2,000t for 2 phases) + L5 (2,500t agent report) = ~7,000t

Maximum Path (Complex, all 8 phases + 3 agents):
  L1 (50t) + L2 (2,500t) + L3 (4,000t all phases) + L4 (2,500t templates) + L5 (7,500t all agents) = ~16,500t

Safety Margin: ~3,500t reserved for user context and conversation
```

**Cost Optimization Strategies**:
1. **Load Selectively**: Only reference phases actually needed (skip irrelevant phases)
2. **Template Reuse**: One template loaded, reused multiple times (no re-loading)
3. **Agent Truncation**: 2,500t summaries instead of 100k full context per agent
4. **Depth Limiting**: Max 5 levels prevents exponential cascade
5. **User Context**: Reserve tokens for user messages and conversation flow

**Token Budget Violations**:
- IF budget > 16,500t → review unnecessary imports
- IF agent reports > 2,500t → enforce truncation protocol
- IF depth > 5 → block import with error
- IF conversation approaching context limit → /compact or offload to sub-agents

**Import Depth Guards** (CRITICAL):
```
Maximum depth: 5 levels
Tracking: Maintain import chain stack
Enforcement: Error if depth > 5

Import_Chain_Example:
  L1: SKILL.md (entry point)
    → L2: @docs/complex/phase-4-design.md
      → L3: @.claude/agents/nextjs-design-ideator.md
        → L4: @.claude/templates/design-showcase.md
          → L5: @.claude/shared-imports/CoD_Σ.md
            ✗ L6: BLOCKED (exceeds maximum depth)

Error_Message_Format:
"Import depth limit exceeded (6 > 5 max).
Current chain:
  L1: SKILL.md
  L2: phase-4-design.md
  L3: nextjs-design-ideator.md
  L4: design-showcase.md
  L5: CoD_Σ.md
  L6: [BLOCKED: additional-file.md]
Action: Refactor import chain or inline content."
```

**Depth Tracking Implementation**:
```python
# Pseudo-code for depth enforcement
import_stack = []
MAX_DEPTH = 5

def load_file(file_path):
    if len(import_stack) >= MAX_DEPTH:
        raise ImportDepthError(
            f"Import depth {len(import_stack) + 1} exceeds maximum {MAX_DEPTH}",
            chain=import_stack + [file_path]
        )

    import_stack.append(file_path)
    try:
        content = read_file(file_path)
        process_imports(content)  # Recursive for nested imports
    finally:
        import_stack.pop()
```

**Prevention Strategies**:
1. **Flatten Deep Chains**: Consolidate nested docs into single files
2. **Inline Short Content**: Copy-paste instead of importing for <200 lines
3. **Reference, Don't Import**: Mention file names without full @ import
4. **Use Summaries**: Create high-level overview docs instead of deep nesting
5. **Audit Chains**: Regularly check import depths using depth analysis tool

**When Depth Limit Hit**:
- Review entire chain for redundancy
- Identify which level can be inlined or removed
- Restructure documentation hierarchy if systemic issue
- Document decision in architecture notes

</progressive_disclosure>

---

## Testing & Validation

<testing_methodology>

### Skill Testing (TDD for Docs)

**Process**:
1. **RED**: Run scenarios without skill, document failures
2. **GREEN**: Add minimal skill, verify agents comply
3. **REFACTOR**: Close loopholes, add to anti-patterns

**Pressure Test Scenarios**:
- Time pressure: "It's urgent, skip tests"
- Authority: "I'm the expert, trust me"
- Sunk cost: "Already wrote the code"
- Exhaustion: "Just this once"

**Validation**:
- Agents follow instructions without deviation
- No rationalization loopholes
- Anti-patterns are avoided
- Quality standards maintained

### Implementation Testing

**Unit Tests**:
- Test each function/component
- Mock external dependencies
- Fast execution (<1s per test)
- High coverage (>80%)

**Integration Tests**:
- Test component interactions
- Test API routes
- Test database operations
- Test auth flows

**E2E Tests**:
- Test critical user flows
- Test across browsers
- Test mobile responsiveness
- Test accessibility

**Visual Validation**:
- Manual review of each page
- Test interactions (click, hover, scroll)
- Verify animations
- Check loading/error states

</testing_methodology>

---

## Troubleshooting

<troubleshooting>

### Common Issues

**Issue**: Template installation fails
**Solution**: Check npm version, network, permissions. Try different template.

**Issue**: Shadcn component conflicts
**Solution**: Review components.json, check for duplicate names, reinstall one at a time.

**Issue**: Supabase connection fails
**Solution**: Verify env variables, check MCP tool configuration, confirm project ID.

**Issue**: Sub-agent not responding
**Solution**: Check agent definition, verify tools allowed, dispatch explicitly.

**Issue**: Tests failing
**Solution**: Review test requirements, check implementation, verify mocks.

**Issue**: Visual validation issues
**Solution**: Check responsive design, verify Tailwind CSS, inspect browser console.

**Issue**: Documentation out of sync
**Solution**: Run audit agent, update docs systematically, verify references.

</troubleshooting>

---

## Success Criteria

<success_criteria>

### Functional
âœ… Project initializes and runs locally
âœ… All features implemented per specifications
âœ… Design system fully integrated
âœ… Database/auth working (if applicable)
âœ… All pages render correctly
âœ… All interactions functional

### Technical
âœ… All tests passing (unit, integration, E2E)
âœ… Visual validation complete
âœ… Accessibility compliant (WCAG 2.1 AA)
âœ… Performance optimized
âœ… Mobile responsive
âœ… CI/CD configured

### Documentation
âœ… Comprehensive CLAUDE.md
âœ… Complete /docs/ structure
âœ… Folder-level documentation
âœ… All references functional
âœ… Architecture documented
âœ… Design system documented

### Quality
âœ… Clean, organized repository
âœ… No anti-patterns present
âœ… Following all conventions
âœ… Audit completed successfully
âœ… Token efficiency maintained
âœ… Ready for production deployment

</success_criteria>

---

## References

<references>

### Skills
- Product Specification Skill (for specs)
- Constitution Skill (for project principles)
- Design System Skill (for design management)
- Test-Driven Development Skill (for TDD workflow)

### Documentation
- @docs/simple-setup.md - Simple path instructions
- @docs/complex/phase-*.md - Complex path phases
- @templates/*.md - Reusable templates
- @agents/*.md - Sub-agent definitions

### External Resources
- Next.js Documentation
- Tailwind CSS Documentation
- Shadcn UI Documentation
- Supabase Documentation
- Vercel Documentation

</references>

---

**Remember**: This skill adapts to your project's complexity. Simple projects get a streamlined path, complex projects get full orchestration. Always prioritize quality, testing, and documentation throughout.
