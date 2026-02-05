---
name: Pattern Development
description: Guide through updating AI design patterns with comprehensive checklist completion, code examples, images, documentation, and interactive demos
---

# Pattern Development Skill

This skill helps you complete the 24 AI design patterns for the AIUX project. **15 patterns are fully updated**, and **9 patterns require comprehensive review and updates**. Each pattern must have all components completed before considering it done.

## Intent Detection - When Claude Should Suggest This Skill

Claude should **automatically proactively suggest using the pattern generator** when detecting these keywords:
- "work on [pattern name]" → Suggest: `npm run generate-pattern [slug]`
- "update pattern" or "update [pattern-name]" → Suggest generator or manual workflow
- "next pattern" or "which pattern should I work on?" → Run `npm run list-patterns` and recommend
- "finish remaining patterns" → Suggest `npm run generate-all-patterns`
- "pattern" + "incomplete" or "need work" → Check status and suggest generator
- When user reviews CLAUDE.md pattern checklist → Remind them to use the generator

## Auto-Suggestion Logic

**When user mentions pattern work, Claude should:**

1. **Check status**: `npm run list-patterns` (in background)
2. **Detect incomplete patterns**: Identify which of the 9 need work
3. **Suggest appropriate action**:
   - For NEW patterns: "Ready to generate? Run: `npm run generate-pattern [slug]`"
   - For IN-PROGRESS: "Continue with manual updates following the checklist"
   - For INCOMPLETE: "Let me generate this pattern for you"
4. **Explain the generator**: "This will create all necessary files and structure automatically"
5. **Coordinate next steps**: After generation, guide through validation and testing

## Available Patterns: Complete Status (24 Total)

### ✅ Fully Updated (15/24)
1. Contextual Assistance
2. Progressive Disclosure
3. Human-in-the-Loop
4. Explainable AI
5. Conversational UI
6. Adaptive Interfaces
7. Predictive Anticipation
8. Multimodal Interaction
9. Guided Learning
10. Augmented Creation
11. Responsible AI
12. Error Recovery
13. Collaborative AI
14. Confidence Visualization
15. Selective Memory

### 🔄 Need Updates (9/24)
1. **Ambient Intelligence** - Context-aware background processing
2. **Safe Exploration** - Risk-free experimentation environments
3. **Feedback Loops** - Continuous learning from user interactions
4. **Graceful Handoff** - Seamless transitions between AI and humans
5. **Context Switching** - Managing multiple conversation contexts
6. **Intelligent Caching** - Smart data persistence strategies
7. **Progressive Enhancement** - Layered feature availability
8. **Privacy-First Design** - Data minimization and user control
9. **Universal Access Patterns** - Inclusive design for all users

## Pattern Completion Checklist

Each pattern must have ALL of the following completed before marking as done:

- [ ] **Code Examples** - Working implementations with titles, descriptions, and code samples
- [ ] **Images & Visuals** - Optimized images, examples, diagrams with alt text
- [ ] **Text Content** - Description, use cases, key benefits clearly written
- [ ] **Guidelines** - Best practices and recommendations for using the pattern (minimum 1)
- [ ] **Considerations** - Important trade-offs and considerations (minimum 1)
- [ ] **Figma Prompts** - Design prompts for creating visual assets
- [ ] **Interactive Demo** - Working React component demonstration at `/patterns/[slug]`
- [ ] **Component Tests** - Comprehensive tests for the demo component
- [ ] **Validation Passed** - Run `npm run test:patterns` successfully
- [ ] **Browser Review** - Review pattern at http://localhost:3000 and verify all looks good

## Workflow

### Step 1: Select Your Pattern
Ask which pattern you want to work on, or I'll suggest the next priority pattern.

### Step 2: Review Current State
```bash
# Check existing pattern structure
npm run list-patterns
```
Examine what exists and what's missing from the checklist.

### Step 3: Work Through Checklist Items
For EACH checklist item, follow these steps:

#### Code Examples
- Review existing code at `src/data/patterns/patterns/[pattern-slug]/code-examples.ts`
- Add/update 2-3 working code examples
- Include practical use cases
- Ensure code is properly formatted and runnable

#### Images & Visuals
- Add 1-2 high-quality images to `public/images/patterns/[pattern-slug]/`
- Use WebP/AVIF formats (run `npm run optimize-images`)
- Include descriptive alt text
- Ensure images are 800-1200px width

#### Text Content
- Update `src/data/patterns/patterns/[pattern-slug]/index.ts`
- Write clear description (2-3 paragraphs)
- List 3-5 use cases
- Include key benefits and real-world applications

#### Guidelines
- Add to `guidelines.ts` in pattern directory
- Provide 3-5 actionable guidelines
- Each should be specific and implementable
- Include when to use and when NOT to use

#### Considerations
- Add to `considerations.ts` in pattern directory
- Document trade-offs and limitations
- Include accessibility considerations
- Note performance implications if any

#### Figma Prompts
- Create design prompts that help generate visuals
- Store in pattern's data file
- Should describe UI states and interactions

#### Interactive Demo Component
- Create React component at `src/components/examples/[PatternName]Example.tsx`
- Make it interactive and demonstrate the pattern in action
- Use existing component patterns and Tailwind styling
- Include explanatory text and controls

#### Component Tests
- Create test file at `src/components/examples/__tests__/[PatternName]Example.test.tsx`
- Test interactions, rendering, state changes
- Aim for 80%+ coverage of the component

#### Validation
```bash
npm run test:patterns
```
All pattern data must validate successfully against the Zod schema.

#### Browser Review
1. Start dev server: `npm run dev`
2. Navigate to the pattern: `http://localhost:3000/patterns/[pattern-slug]`
3. Review visuals, demo, and all content
4. Test interactive demo component
5. Check responsive design on mobile

### Step 4: Mark Complete
Only when ALL 10 checklist items are 100% complete, mark the pattern as done.

### Step 5: Move to Next Pattern
Select the next pattern from the list and repeat.

## Using the AI Pattern Generator

**The pattern generator automates most of the work!** Instead of manually creating all files:

```bash
# Generate one pattern (interactive)
npm run generate-pattern

# Or specify pattern slug directly
npm run generate-pattern --slug="ambient-intelligence"

# Generate ALL missing patterns at once
npm run generate-all-patterns
```

**What the generator does automatically:**
- ✅ Creates all required pattern files (index.ts, code-examples.ts, guidelines.ts, considerations.ts)
- ✅ Generates detailed code examples with explanations
- ✅ Creates realistic use case examples
- ✅ Writes comprehensive guidelines and considerations
- ✅ Creates interactive React demo component
- ✅ Validates everything against the schema

**After generation, you may need to:**
- Add/optimize images (run `npm run optimize-images`)
- Review and enhance the demo component
- Add tests for the demo component
- Browser review at http://localhost:3000

## Commands Reference

```bash
# List all patterns and their status (check which need work)
npm run list-patterns

# Generate one specific pattern
npm run generate-pattern [slug]

# Generate all 9 missing patterns
npm run generate-all-patterns

# Validate pattern data structure
npm run test:patterns

# Start development server for testing
npm run dev

# Run tests for specific pattern component
npm test -- --testPathPattern="pattern-slug"

# Optimize images after adding new ones
npm run optimize-images

# Check if there are untested components
npm run list-untested

# Generate tests for a component
npm run generate-test [component-path]
```

## Important Rules

⚠️ **Stay Focused**: Work on ONE pattern at a time. Do not jump to another pattern until the current one is 100% complete with all checklist items done.

✅ **Complete Everything**: Don't skip items. Every checklist item matters for consistency and user experience.

🎯 **Quality First**: Focus on making each pattern excellent rather than rushing through them.

📱 **Test Thoroughly**: Always review in browser and test on mobile before marking complete.

## Pattern Structure Reference

Each pattern at `src/data/patterns/patterns/[pattern-slug]/` should have:

```
[pattern-slug]/
├── index.ts                    # Main pattern data with metadata
├── code-examples.ts           # Working code examples
├── guidelines.ts              # Best practices and guidelines
└── considerations.ts          # Trade-offs and considerations
```

Plus:
- Demo component: `src/components/examples/[PatternName]Example.tsx`
- Demo test: `src/components/examples/__tests__/[PatternName]Example.test.tsx`
- Images: `public/images/patterns/[pattern-slug]/`

## Success Criteria

A pattern is complete when:

✅ All 10 checklist items are checked
✅ `npm run test:patterns` passes with no validation errors
✅ Pattern displays correctly at http://localhost:3000/patterns/[slug]
✅ Interactive demo works smoothly
✅ Mobile responsive design verified
✅ All code examples work as expected
✅ Images are optimized and load quickly

## Agent Coordination & Workflow Automation

This skill works with other AI agents in the project for coordinated development:

### Related Skills & Agents
- **guide-gen** (NEW) - Generates Designer Guides learning paths
- **test-gen** - Generates component tests automatically
- **demo-gen** - Scaffolds interactive demo components
- **design** - Analyzes and fixes design consistency

### Coordinated Workflow
When working on patterns, you can leverage multiple agents:

```bash
# Pattern workflow: Generate → Test → Validate
npm run generate-pattern [slug]      # Step 1: Pattern generator creates structure
npm run generate-test [component]    # Step 2: Test generator creates tests
npm run test:patterns                # Step 3: Validate everything
npm run dev                          # Step 4: Browser review
```

### Future Guide Integration
The new guide generator (`guide-gen`) is being built alongside pattern development. When both are ready:

```bash
# Complete AIUX workflow
npm run generate-pattern              # Generate pattern
npm run generate-guide                # Generate guide lesson about the pattern
npm run generate-test                 # Generate tests
npm run design-analyze                # Analyze design consistency
npm run progress-report               # Track overall progress
```

## Next Steps After Pattern Completion

1. Commit changes with pattern name in message
2. Check if corresponding guide lesson exists (future)
3. Move to next pattern from the list
4. Track progress in `npm run progress-report`
5. Repeat until 24/24 patterns complete

---

**Project Goal**: Complete all 24 AI design patterns with comprehensive implementations, interactive demos, and documentation. Currently: 15/24 complete, 9 need updates.

**Companion Project**: 6 Designer Guide learning paths (Claude Code ✅, Cursor ✅, and 4 tools in progress)
