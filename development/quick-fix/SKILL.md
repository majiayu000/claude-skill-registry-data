---
name: quick-fix
description: Fast workflow for small changes, bug fixes, and UI tweaks that don't require full feature development. Uses sub-agent orchestration with model selection (Sonnet 4.5 orchestrator, Haiku 4.5 workers) for efficient context management. Handles styling adjustments, minor functionality fixes, and quick improvements while maintaining project quality standards.
---

# Quick Fix Skill

Execute small changes, bug fixes, and UI tweaks efficiently without the overhead of full feature development workflows.

## When to Use This Skill

This skill should be used when:
- Making styling adjustments (colors, fonts, spacing, hover effects)
- Fixing minor bugs (broken links, non-working buttons, missing images)
- Updating text/copy across components
- Adding small UI elements (menu items, buttons)
- Making typography or layout improvements
- Applying consistent site styles to elements
- Any change that is well-scoped and doesn't require architectural planning

**Do NOT use for:**
- New features requiring architectural decisions
- Changes touching 5+ files with complex dependencies
- Unclear requirements needing extensive discovery
- Major refactoring or system-wide changes

Use `/feature-dev` for those scenarios instead.

## Workflow Overview

### Phase 1: Clarify (Orchestrator - Sonnet 4.5)
Parse the user's request and clarify any ambiguities before proceeding.

**Actions:**
1. Understand what the user wants to change/fix
2. **If anything is unclear or ambiguous, ask 1-3 focused follow-up questions**:
   - What specific element/component?
   - What should the behavior/appearance be?
   - Any constraints or preferences?
3. Determine change type:
   - **Text-only**: Content/copy changes (minimal verification)
   - **Code/functional**: Styling, logic, components (full verification)
4. Decide verification rigor based on change type

**Critical**: Do NOT guess or make assumptions. If unclear, ask. Keep questions focused since this is a quick fix.

---

### Phase 2: Explore (1 Explorer Agent - Haiku 4.5)
Quickly locate relevant files and understand necessary context.

**Actions:**
1. Launch 1 explorer agent with focused scope:
   - Use Glob/Grep to find relevant files
   - Read 1-3 key files to understand current implementation
   - Identify any theme/config files needed
   - Check for multiple instances if consistency is required
2. Agent returns:
   - List of files to modify
   - Current implementation patterns
   - Any style/theme references
   - Potential gotchas or dependencies

**Agent Configuration:**
- Model: Haiku 4.5 (cost-efficient for simple exploration)
- Tools: Glob, Grep, Read
- Scope: Targeted search, not comprehensive analysis

---

### Phase 3: Plan (2 Solution Agents - Haiku 4.5, in parallel)
Generate two independent solution approaches and choose the best one.

**Actions:**
1. Launch 2 solution agents in parallel, each creating an independent plan
2. Each agent should:
   - Propose specific changes to specific files
   - List exact edits (file:line references)
   - Identify if tests are needed (per project testing standards)
   - Note if documentation updates are required
   - Flag any risks or edge cases
3. Orchestrator reviews both plans and **chooses the best** based on:
   - **Simplicity**: Fewer changes, minimal complexity
   - **MVP focus**: Fastest path to working solution
   - **Project principles**: Follows CLAUDE.md standards
   - **Risk**: Lower risk of breaking changes
4. Present chosen plan to user for approval

**Agent Configuration:**
- Model: Haiku 4.5 (efficient for planning small changes)
- Each agent works independently (no shared context)
- Orchestrator makes final selection

---

### Phase 4: Implement (1 Implementation Agent)
Execute the approved plan with appropriate quality measures.

**Actions:**
1. Wait for user approval of chosen plan
2. Launch 1 implementation agent to:
   - Make the approved changes
   - Write tests if warranted (follow project testing standards in `.claude/modules/testing-standards.md`)
   - Update documentation if needed (theme docs, style guides, etc.)
   - Follow all patterns from exploration phase
3. Agent returns summary of changes made

**Agent Configuration:**
- Model: **Haiku 4.5** for simple changes, **Sonnet 4.5** for complex logic
- Orchestrator decides which model based on change complexity
- Tools: Read, Edit, Write, Bash (for running tests)

**Quality Requirements:**
- Follow all coding standards in `CLAUDE.md`
- Use existing patterns discovered in exploration
- Write clean, readable code
- Add tests only if change warrants it per project principles

---

### Phase 5: Verify (Orchestrator - Sonnet 4.5)
Run appropriate verification checks and summarize results.

**Actions:**
1. Determine verification level based on change type:
   - **Text-only changes**: Skip build (just confirm edits)
   - **Code/functional changes**: Run full verification
2. For code/functional changes, run:
   - `npm run build` (must pass - TypeScript, Next.js checks)
   - `npm test` (must pass - all tests)
   - Check for Tailwind class validity
   - Verify no console errors
3. If verification fails:
   - Identify the issue
   - Either fix automatically or ask user for guidance
4. Summarize what was done:
   - Files changed
   - Tests added (if any)
   - Documentation updated (if any)
   - Verification results
   - Any follow-up suggestions

**Critical**: All code changes MUST pass build and tests per project standards.

---

## Agent Architecture

### Orchestrator (Main Skill - Sonnet 4.5)
- Coordinates all phases
- Makes decisions about verification rigor
- Chooses best plan from solution agents
- Runs final verification
- Maintains conversation with user

### Explorer Agent (Haiku 4.5)
- Quick targeted codebase search
- Lightweight file reading
- Pattern identification
- Returns focused findings

### Solution Agents x2 (Haiku 4.5)
- Work in parallel independently
- Each proposes complete solution approach
- Orchestrator selects best based on simplicity/MVP principles

### Implementation Agent (Haiku 4.5 or Sonnet 4.5)
- Executes approved plan
- Writes tests if needed
- Updates documentation if needed
- Model selection based on complexity

---

## Example Usage

### Example 1: Styling Adjustment
```
User: "Make the Save Recipe button match our site's primary button style"

Phase 1 (Clarify): Clear request, no questions needed
Phase 2 (Explore): Find SaveRecipe component, identify site button styles
Phase 3 (Plan): Two agents propose approaches, choose simpler one
Phase 4 (Implement): Apply site button classes, verify hover effects
Phase 5 (Verify): Run build, confirm styling correct
```

### Example 2: Bug Fix
```
User: "The Modify Recipe button isn't working when clicked"

Phase 1 (Clarify): Ask: "What should happen when clicked?"
User: "Should open a dialog to modify the recipe"
Phase 2 (Explore): Find ModifyRecipe button, trace click handler
Phase 3 (Plan): Two solutions (fix handler vs rewire event), choose best
Phase 4 (Implement): Fix the click handler, add test
Phase 5 (Verify): Run tests, verify button works
```

### Example 3: Typography Improvement
```
User: "Make the recipe description section more readable with better typography"

Phase 1 (Clarify): Ask: "Any specific font preferences or spacing guidelines?"
User: "Use our Playfair font for headings, increase line height"
Phase 2 (Explore): Find recipe description component, check theme
Phase 3 (Plan): Two approaches (inline styles vs utility classes), choose utility classes
Phase 4 (Implement): Apply typography classes, adjust spacing
Phase 5 (Verify): Build passes, visually inspect (suggest screenshot)
```

---

## Quality Standards

### Always Follow Project Standards
- Review `CLAUDE.md` and `.claude/modules/` for standards
- Follow Next.js patterns from `.claude/modules/nextjs-patterns.md`
- Respect TypeScript standards (no `any`, explicit types)
- Use proper Supabase client patterns
- Follow testing standards when writing tests

### Testing Decisions
Write tests when:
- Adding new functionality (even small)
- Fixing bugs (regression prevention)
- Changing component behavior

Skip tests for:
- Pure text/copy changes
- Simple styling adjustments
- One-off visual tweaks

Use project testing framework (Vitest) per `.claude/modules/testing-standards.md`.

### Documentation Updates
Update documentation when:
- Modifying theme/style system
- Adding new reusable patterns
- Changing shared configuration
- Making changes that affect other developers

---

## Success Criteria

✅ Change implemented as requested
✅ No TypeScript errors (build passes)
✅ All tests pass
✅ Tailwind classes valid
✅ Tests written if warranted
✅ Documentation updated if needed
✅ Follows all project standards
✅ User confirms it looks/works as expected

---

## Tips for Users

**Be specific when possible:**
- ❌ "Make it prettier"
- ✅ "Increase padding to 16px and round corners to 8px"

**Provide context for bugs:**
- ❌ "This button is broken"
- ✅ "When I click Save Recipe, nothing happens - it should save to my library"

**Reference existing patterns:**
- ✅ "Make this match the style of our primary CTA buttons"
- ✅ "Use the same hover effect as the recipe cards"

**Trust the orchestrator to ask questions:**
- If something is unclear, the orchestrator will ask
- Answer clarifying questions to get better results
