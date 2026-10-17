---
name: designpowers-agent-team
description: Control a team of 10 design agents that run an inclusive design process from discovery through handoff with accessibility woven into every step.
triggers:
  - "run designpowers"
  - "start the design team"
  - "design this with the agent team"
  - "review this design with designpowers"
  - "run a design critique"
  - "start design discovery"
  - "build this with the design agents"
  - "audit accessibility with designpowers"
---

# Designpowers Agent Team

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Designpowers is an agent design team you control: 10 specialist agents that run an inclusive design process while you direct. The system discovers, researches, strategises, designs, builds, reviews, and hands off — with accessibility (WCAG/COGA) woven into every step.

**Model-agnostic.** Designpowers is markdown files that work with any AI coding tool: Claude Code, Cursor, Windsurf, Copilot, Aider, Gemini CLI.

## Installation

### As a Claude Code Plugin

```bash
# Clone the repository
git clone https://github.com/Owl-Listener/designpowers.git
cd designpowers

# Link as a Claude Code plugin
claude plugin link .

# Or install directly
claude plugin install Owl-Listener/designpowers
```

### As a Gemini CLI Extension

```bash
# Clone and configure
git clone https://github.com/Owl-Listener/designpowers.git
cd designpowers

# Add to Gemini CLI extensions
gemini ext add ./designpowers
```

### For Other AI Coding Tools

```bash
# Clone into your project's context directory
git clone https://github.com/Owl-Listener/designpowers.git .designpowers

# Reference in your tool's context:
# - Cursor: Add .designpowers/ to .cursorrules
# - Windsurf: Include in .windsurfrules
# - Copilot: Reference in .github/copilot-instructions.md
```

## Architecture

### 10 Specialist Agents

| Agent | Role | Handoff Targets |
|-------|------|-----------------|
| `design-strategist` | Flows, IA, personas, principles, journey maps | → design-lead, motion-designer |
| `design-scout` | Competitive research, pattern evidence, benchmarking | → design-strategist |
| `inspiration-scout` | Aesthetic references, cross-domain inspiration | → design-lead |
| `design-lead` | Visual design — layout, colour, typography, components | → motion-designer, content-writer |
| `motion-designer` | Animation, transitions, micro-interactions, reduced motion | → content-writer, design-builder |
| `content-writer` | Interface copy, labels, errors, plain language (Grade 6) | → design-builder |
| `design-builder` | Builds specs into production code | → accessibility-reviewer |
| `accessibility-reviewer` | WCAG/COGA evaluation, audits output, loops back with fixes | → design-critic |
| `design-critic` | Reviews against brief, plan, principles | → design-builder (if gaps) |
| `heuristic-evaluator` | Nielsen's 10 heuristics, cognitive walkthroughs | → design-critic |

### 2 Lanes

**Build Lane** — Full design process from discovery to handoff:
```
Discover → Research → Strategy → Taste → Inspire → Plan → Design → Build → Review → Fix → Ship
```

**Review Lane** — Audit existing designs (screenshot, URL, or code):
```
Input → accessibility-reviewer + design-critic + heuristic-evaluator (parallel) → Report
```

### 2 Modes

**Direct Mode** (default) — You approve every handoff:
```
Agent completes work → Handoff message → Wait for your approval → Next agent
```

**Auto Mode** — Agents run the pipeline, you review at the end:
```
"go auto" → Full pipeline executes → Final output + all handoff logs
```

## Usage Patterns

### Starting a New Design

```bash
# Start the design process
"Design a habit tracker app"

# System responds with welcome + mode confirmation
# First handoff appears:
# design-strategist → design-scout: "Need competitive research on habit trackers..."

# Approve to continue
"ok"

# Or correct direction
"Focus on mindfulness apps, not productivity"

# Or switch to auto
"go auto"
```

### Reviewing Existing Work

```bash
# Review a screenshot
"Review this design for accessibility" [attach screenshot]

# Review a URL
"Audit https://example.com for WCAG compliance"

# Review code
"Review this component" [paste React component]

# System runs accessibility-reviewer, design-critic, heuristic-evaluator in parallel
# Returns consolidated report with findings categorized by severity
```

### Working with Design Taste

```bash
# Define aesthetic direction
"My taste: clean, high contrast, inspired by Linear and Stripe. I hate gradients and glassmorphism."

# Point to existing design system
"Use the design tokens from ./design-system/tokens.json"

# Reference a DESIGN.md
"Build from DESIGN.md in this project"

# Pull a known brand's style
"Start with GitHub's design language"

# Mid-build taste check
# System shows checkpoint: "Is this weight right, or bolder/lighter?"
"Bolder. And increase the letter spacing."
```

### Controlling Agent Flow

```bash
# Skip an agent
"Skip motion, go straight to builder"

# Redirect work
"Send this back to design-strategist"

# Talk to specific agent
"design-lead, why frosted glass?"

# Request debate
"Show me competing approaches for the navigation"

# Add requirement mid-flow
"Also handle dark mode"
```

### Working with DESIGN.md

```bash
# Read existing DESIGN.md
"Read DESIGN.md and build the login flow"

# Author new DESIGN.md
"Create a DESIGN.md for this project based on our decisions"

# Pull from library
"Use the Stripe DESIGN.md as a starting point"

# System extracts:
# - Color tokens
# - Typography scale
# - Spacing system
# - Component patterns
# - Brand voice
```

## Key Skills Reference

### Core Pipeline Skills

| Skill | Trigger Phrase | Output |
|-------|---------------|--------|
| `design-discovery` | "Start discovery" | Problem definition, users, constraints, brief |
| `design-strategy` | "Create design strategy" | Principles, positioning, journey map, metrics |
| `design-taste` | "Define taste direction" | Aesthetic references, emotional targets, quality bar |
| `writing-design-plans` | "Create design plan" | 2-5 min tasks with accessibility checks |
| `ui-composition` | "Design the UI" | Layout, colour, typography (WCAG-compliant) |
| `interaction-design` | "Design interactions" | States, transitions, feedback, errors |
| `accessible-content` | "Write interface copy" | Plain language, headings, alt text, labels |
| `motion-choreography` | "Design animations" | Duration, easing, stagger, reduced-motion |
| `designpowers-critique` | "Critique this design" | Review against plan, principles, personas |
| `design-handoff` | "Create handoff specs" | Specs, rationale, accessibility requirements |

### Alternative Entry Points

| Skill | Use When | Output |
|-------|----------|--------|
| `design-express` | First-time user, quick taster | 2-min critique or build without full pipeline |
| `design-review` | Audit existing work | Parallel review from all reviewers |
| `design-md` | Working with DESIGN.md | Read/author design system as DESIGN.md |
| `design-library` | Start with known brand | Pull and adapt brand DESIGN.md |

### Support Skills

| Skill | Purpose |
|-------|---------|
| `design-memory` | Observational record of how you design (never applied) |
| `design-debate` | Agents argue competing directions |
| `inspiration-scouting` | Cross-domain aesthetic references |
| `taste-feedback` | Mid-build checkpoints for aesthetic alignment |
| `design-debt-tracker` | Living register of deferred findings |
| `design-retrospective` | Post-ship reflection and learnings |
| `heuristic-evaluation` | Nielsen's 10 heuristics evaluation |
| `synthetic-user-testing` | Walk through as personas after fixes |

## Configuration

### Environment Variables

```bash
# Optional: Set preferred model for specific agents
export DESIGNPOWERS_STRATEGIST_MODEL="claude-3-5-sonnet-20241022"
export DESIGNPOWERS_BUILDER_MODEL="gpt-4"

# Optional: Set accessibility audit level
export DESIGNPOWERS_WCAG_LEVEL="AAA"  # Default: AA

# Optional: Enable verbose handoff logging
export DESIGNPOWERS_VERBOSE="true"
```

### Project Configuration

Create `.designpowers.yml` in your project root:

```yaml
# Mode preferences
default_mode: direct  # or 'auto'
show_guided_walkthrough: true  # First-time users

# Pipeline customization
skip_agents:
  - motion-designer  # Skip motion if not needed
  - inspiration-scout

# Accessibility defaults
accessibility:
  wcag_level: AA  # or AAA
  contrast_ratio_threshold: 4.5
  test_personas: true

# Taste preferences (optional)
taste:
  references:
    - "Linear app"
    - "Stripe dashboard"
  avoid:
    - "gradients"
    - "glassmorphism"

# Design system integration
design_system:
  path: "./design-system"
  tokens: "./design-system/tokens.json"
  components: "./design-system/components"

# DESIGN.md preferences
design_md:
  auto_generate: true
  path: "./DESIGN.md"
```

## Real-World Examples

### Example 1: Full Build Pipeline

```bash
# User starts
"Design a dashboard for tracking carbon footprint"

# design-strategist activates
# Output: Problem brief, user personas (ability spectrum), success metrics

# User approves
"ok"

# design-scout → design-strategist
# Output: Competitive analysis of Wren, Joro, Earth Hero

# User corrects
"Focus on enterprise users, not consumers"

# design-strategist updates strategy
# Handoff → inspiration-scout

# inspiration-scout → design-lead
# Output: References (Grafana for data viz, Notion for organization)

# User adds
"Also look at Bloomberg Terminal for density"

# design-lead → motion-designer
# Output: Layout with card-based metrics, green/amber/red colour system (WCAG AAA)
# Mid-build taste check: "Is this data density right?"

# User responds
"Increase density. Power users prefer more info."

# motion-designer → content-writer
# Output: Subtle progress animations, reduced-motion fallbacks

# content-writer → design-builder
# Output: Plain language labels, Grade 6 reading level, descriptive errors

# design-builder → accessibility-reviewer
# Output: React component with ARIA labels, keyboard navigation

# accessibility-reviewer → design-critic
# Output: 2 findings (focus indicators too subtle, one heading level skipped)

# design-critic → design-builder (loop back)
# Output: Fixes applied, re-review passes

# Final handoff
# Output: Production-ready code, accessibility documentation, design rationale
```

### Example 2: Review Existing Design

```bash
# User provides screenshot
"Review this login form" [attach screenshot]

# System activates Review lane
# Runs in parallel:
# - accessibility-reviewer: WCAG audit
# - design-critic: Heuristic evaluation
# - heuristic-evaluator: Nielsen's 10 principles

# Consolidated output:
# 
# CRITICAL (Accessibility)
# - Password field missing visible label (WCAG 3.3.2)
# - Error message colour-only (WCAG 1.4.1)
# - Focus indicator contrast 2.1:1 (need 3:1 minimum)
#
# MAJOR (Usability)
# - "Submit" button generic label (heuristic: match system & real world)
# - No feedback during loading state (heuristic: visibility of system status)
#
# MINOR (Design)
# - Inconsistent spacing between fields
# - Button size below 44×44 touch target

# User asks for fixes
"Fix the critical issues"

# design-builder generates corrected code
```

### Example 3: Working with DESIGN.md

```bash
# User references existing design system
"Build the onboarding flow using DESIGN.md"

# design-md skill reads ./DESIGN.md
# Extracts:
# - Color tokens: primary.500 = #3B82F6
# - Typography: heading.lg = 32px/1.2 'Inter'
# - Spacing: space.4 = 16px
# - Component: Button with 4 variants

# design-lead uses exact tokens
# Output: Onboarding with buttons using primary.500, heading.lg, space.4

# User exports updated design
"Update DESIGN.md with the new onboarding patterns"

# design-md authors updated file
# Adds:
# - components.onboarding-card
# - patterns.multi-step-flow
# - tokens.color.success (new)
```

### Example 4: Design Debate

```bash
# User requests alternatives
"Show me competing approaches for the mobile navigation"

# design-debate activates
# Agent A (Tab Bar): "Thumb-friendly, clear context, standard pattern"
# Agent B (Hamburger): "More screen space, scalable to many items"

# Cross-examination
# Agent A: "Hamburger hides navigation, increases cognitive load"
# Agent B: "Tab bar limited to 5 items, doesn't scale"

# Evidence from brief
# Agent A: "Personas include seniors with motor challenges — tap targets matter"
# Agent B: "We have 8 top-level sections, tab bar forces prioritization"

# User decides
"Use tab bar with 5 core items. Move other 3 to profile menu."

# design-lead proceeds with decision + rationale logged
```

### Example 5: Design Taste Workflow

```bash
# User defines taste at start
"My taste: brutalist, high contrast, inspired by Craigslist and Hacker News. No animations except loading states."

# System records taste signals:
# - aesthetic: brutalist
# - contrast: high
# - references: [Craigslist, Hacker News]
# - motion: minimal

# design-lead uses taste
# Output: Monospace typography, black/white palette, dense layout

# Mid-build taste check
"Here's the layout. Too austere or just right?"

# User responds
"Perfect. But make links underlined, not just blue."

# Taste signal recorded: links = underlined
# design-builder applies preference

# At retrospective
"What taste decisions landed?"
# System reports: "Brutalist aesthetic tested well with technical users. Underlined links reduced confusion."
```

## Common Patterns

### Pattern: Quick Iteration Loop

```bash
# For rapid prototyping
"go auto"  # Let pipeline run
# Review output
"The colours are too muted. Make them bolder."
# System re-runs design-lead → builder with correction
"Now add dark mode."
# Incremental addition without full restart
```

### Pattern: Accessibility-First Build

```bash
# Start with accessibility requirements
"Design a form with WCAG AAA compliance. Users include screen reader users and people with cognitive disabilities."

# System activates inclusive-personas
# Output: Permanent (blind), Temporary (concussion), Situational (distracted)

# Every agent considers all personas
# design-lead: Ensures 7:1 contrast
# content-writer: Grade 6 reading level, clear errors
# design-builder: Full keyboard navigation, ARIA live regions
```

### Pattern: Design System Alignment

```bash
# Ensure consistency with existing system
"Build this using our design system at ./src/design-system"

# design-system-alignment skill activates
# Reads tokens, components, naming conventions

# design-lead matches existing patterns
# Output: Uses system tokens, follows naming (btn-primary not button-main)

# design-debt-tracker notes deviations
# "New pattern: inline-edit. Should this become a system component?"
```

### Pattern: Mid-Flight Course Correction

```bash
# Pipeline running, user sees issue at handoff
# design-lead → motion-designer: "Card-based layout with slide transitions"

# User corrects
"Stop. The card layout won't work on mobile. Use a list instead."

# System pauses pipeline
# design-lead re-does layout
# New handoff: "List layout with expand/collapse"

# User approves
"ok"
# Pipeline resumes from motion-designer
```

## Troubleshooting

### Agent Not Activating

**Problem:** Designpowers doesn't respond to "design this"

**Solution:**
```bash
# Check if plugin/extension is loaded
claude plugin list  # or equivalent for your tool

# Verify skills are in context
ls .designpowers/skills/

# Try explicit skill trigger
"Run design-discovery for a mobile app"

# Check for conflicts
# Remove other design-related plugins that might intercept
```

### Handoff Loop Between Agents

**Problem:** accessibility-reviewer and design-builder stuck in loop

**Solution:**
```bash
# Intervene directly
"accessibility-reviewer, accept the current contrast ratio. We'll note it as design debt."

# Or skip problematic agent
"Skip accessibility-reviewer for now"

# Or provide explicit guidance
"design-builder, use #000000 on #FFFFFF. That's 21:1 contrast."
```

### Taste Signals Not Applied

**Problem:** Agents ignore stated aesthetic preferences

**Solution:**
```bash
# Re-state taste with examples
"design-lead, review my taste preferences. I said 'brutalist' — that means monospace type, no rounded corners, black and white. Reference Craigslist."

# Or provide visual reference
"Here's an example" [attach screenshot]

# Check design-taste skill ran
"Did design-taste run? Show me the taste record."
```

### DESIGN.md Not Found

**Problem:** "Build from DESIGN.md" fails

**Solution:**
```bash
# Check file exists
ls DESIGN.md

# Or specify path
"Read DESIGN.md from ./docs/DESIGN.md"

# Generate if missing
"Create a DESIGN.md from our design system at ./src/tokens"

# Verify format
# DESIGN.md must follow Google Labs Stitch format
```

### Review Lane Returns Generic Findings

**Problem:** Review of screenshot produces shallow critique

**Solution:**
```bash
# Provide more context
"Review this dashboard screenshot. It's for enterprise analytics users. Check WCAG AAA and cognitive load."

# Request specific review
"accessibility-reviewer, check colour contrast on all text"
"heuristic-evaluator, focus on error prevention and recovery"

# Provide code alongside screenshot
"Here's the React code for this component" [paste]
```

### Design Debt Not Tracking

**Problem:** Deferred issues not appearing in debt register

**Solution:**
```bash
# Explicitly log debt
"Add to design debt: Focus indicators need 3:1 contrast. Deferred due to time. Affects keyboard users."

# Review register
"Show design debt register"

# Check auto-escalation settings
# Edit .designpowers.yml:
# design_debt:
#   auto_escalate: true
#   escalate_after_days: 30
```

## Integration Examples

### With Cursor

```bash
# Add to .cursorrules
# Include Designpowers context
@designpowers Run design review on current file

# Or add to Rules for AI
Always consult .designpowers/skills/ for design decisions
Run accessibility-reviewer before marking design tasks complete
```

### With GitHub Actions

```yaml
# .github/workflows/design-review.yml
name: Design Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Designpowers Review
        run: |
          # Install Designpowers
          git clone https://github.com/Owl-Listener/designpowers .designpowers
          # Run review on changed components
          designpowers review --files=$(git diff --name-only HEAD~1)
```

### With Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Run accessibility check before commit

if git diff --cached --name-only | grep -E '\.(jsx|tsx|vue)$'; then
  echo "Running Designpowers accessibility review..."
  designpowers review --accessibility-only --staged
  if [ $? -ne 0 ]; then
    echo "Accessibility issues found. Fix or use --no-verify to skip."
    exit 1
  fi
fi
```

## Advanced Usage

### Custom Agent Chains

```bash
# Skip straight to visual design
"design-lead, design a settings page. Skip discovery and strategy."

# Run only reviewers
"accessibility-reviewer and design-critic, review this code"

# Custom handoff sequence
"design-strategist → inspiration-scout → design-builder. Skip design-lead."
```

### Taste Report Generation

```bash
# After several projects
"Generate a taste report"

# Output:
# YOUR DESIGN TASTE (observed across 7 projects)
# - Typography: Strong preference for sans-serif, typically Inter or Helvetica
# - Colour: High contrast, limited palettes (2-3 colours)
# - Layout: Dense, information-forward
# - Motion: Minimal, functional only
# - References: Consistently cite Linear, Stripe, GitHub

# This is descriptive, never prescriptive
# Each new project starts fresh
```

### Synthetic User Testing

```bash
# After build and fixes
"Run synthetic user testing"

# System walks through key tasks as each persona
# Output:
# Persona: Sarah (screen reader user)
# Task: Add new habit
# Step 1: Navigate to "Add" button — ✓ Found via landmark
# Step 2: Fill form — ✗ "Frequency" label not programmatically linked
# Step 3: Submit — ✓ Success message announced

# Generates actionable fixes
```

### Multi-Project Design Memory

```bash
# After retrospective
"Update design memory"

# System adds observations:
# - Project used brutalist aesthetic, tested well with technical users
# - High-density layouts preferred by power users
# - Underlined links reduced confusion vs colour-only

# Later, on new project
"How do I design?"
# System shows memory (read-only)
# New project direction comes from current brief, not memory
```

## Command Reference

```bash
# Core commands
designpowers build <description>          # Start build pipeline
designpowers review <file|url>            # Run review lane
designpowers express <description>        # Quick 2-min taster

# Mode control
designpowers mode direct                  # Approve every handoff
designpowers mode auto                    # Run full pipeline

# Taste management
designpowers taste define                 # Interactive taste definition
designpowers taste show                   # Display current taste record
designpowers taste report                 # Generate written taste report

# DESIGN.md operations
designpowers dm read <path>               # Read existing DESIGN.md
designpowers dm write <path>              # Author new DESIGN.md
designpowers dm library <brand>           # Pull brand DESIGN.md

# Debt tracking
designpowers debt show                    # Display debt register
designpowers debt escalate <id>           # Escalate specific debt item

# Agent control
designpowers agent <name> <instruction>   # Direct command to agent
designpowers skip <agent-name>            # Skip agent in pipeline
designpowers handoff                      # Show current handoff

# Memory and retrospective
designpowers memory show                  # Read design memory
designpowers retro                        # Run retrospective
```

## Best Practices

1. **Define taste early** — The more aesthetic direction you provide upfront, the better the output.

2. **Use Direct mode first** — Learn the agent handoffs before going Auto.

3. **Provide real constraints** — "Must work on IE11" or "Budget: 2 days" shapes better decisions.

4. **Correct at handoffs** — Cheapest time to change direction is when work hands off, not after full build.

5. **Review design debt regularly** — Don't let deferred issues accumulate untracked.

6. **Run retrospectives** — Post-ship reflection builds better design memory.

7. **Use DESIGN.md for consistency** — Especially multi-project or team contexts.

8. **Let agents debate** — When uncertain, request competing approaches before deciding.

9. **Taste checks matter** — Engage with mid-build checkpoints — they catch aesthetic drift early.

10. **You're the creative director** — Your word overrides everything. The agents work for you.
