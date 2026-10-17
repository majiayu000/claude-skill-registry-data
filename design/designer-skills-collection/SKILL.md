---
name: designer-skills-collection
description: Install and use agentic design skills, commands, and plugins for Claude Code — covering research, systems, UI, interaction, and delivery.
triggers:
  - how do I install designer skills for Claude
  - use the designer skills collection
  - add design research plugins to my agent
  - install UX strategy skills in Claude Code
  - help me with design system commands
  - set up designer-skills plugins
  - use Owl-Listener design tools
  - add design ops skills to my workspace
---

# Designer Skills Collection

> Skill by [ara.so](https://ara.so) — Design Skills collection.

The **Designer Skills Collection** is a comprehensive library of 91 skills and 28 commands across 9 plugins for AI coding agents like Claude Code. It provides domain expertise in design research, design systems, UX strategy, UI design, interaction design, prototyping, design ops, and visual critique.

## What It Does

This collection teaches AI agents how to:
- Conduct user research (personas, journey maps, interviews, usability testing)
- Build and maintain design systems (tokens, components, accessibility)
- Define UX strategy (competitive analysis, IA, content strategy)
- Design polished UI (layout grids, color systems, typography)
- Create meaningful interactions (micro-animations, state machines, gestures)
- Validate designs (prototyping, testing, heuristic evaluation)
- Streamline design operations (handoff specs, sprint planning, workflows)
- Critique visual designs (hierarchy, brand consistency, composition)

## Installation

### Claude Code

**Step 1: Add the Marketplace**

```bash
/plugin marketplace add Owl-Listener/designer-skills
```

**Step 2: Install Plugins**

```bash
/plugin
```

Navigate to the **Discover** tab, then select and install the plugins you need from these 9 options:
- `design-research` (12 skills, 4 commands)
- `design-systems` (11 skills, 3 commands)
- `ux-strategy` (11 skills, 3 commands)
- `ui-design` (14 skills, 4 commands)
- `interaction-design` (15 skills, 3 commands)
- `prototyping-testing` (8 skills, 4 commands)
- `design-ops` (9 skills, 3 commands)
- `designer-toolkit` (7 skills, 3 commands)
- `visual-critique` (4 skills, 1 command)

### Gemini CLI

Install individual plugins as workspace-scoped extensions:

```bash
# Install one plugin
mkdir -p .gemini/extensions
cp -r path/to/designer-skills/.gemini/extensions/design-research .gemini/extensions/

# Or install all extensions at once
git clone https://github.com/Owl-Listener/designer-skills /tmp/designer-skills
cp -r /tmp/designer-skills/.gemini/extensions/. .gemini/extensions/
```

For user-global installation (available in all projects):

```bash
cp -r path/to/designer-skills/.gemini/extensions/design-research ~/.gemini/extensions/
```

Each extension directory contains:
- `gemini-extension.json` (manifest)
- `GEMINI.md` (context file with all skills)

## Key Commands

### Design Research

```bash
# Run a full user research discovery cycle
/design-research:discover

# Prepare and conduct a user interview
/design-research:interview

# Create a usability test plan
/design-research:test-plan

# Synthesize research data into insights
/design-research:synthesize
```

### Design Systems

```bash
# Audit a design system for consistency and accessibility
/design-systems:audit-system

# Scaffold a full component specification
/design-systems:create-component

# Extract and organize design tokens
/design-systems:tokenize
```

### UX Strategy

```bash
# Develop a complete UX strategy
/ux-strategy:strategize

# Run a competitive benchmarking analysis
/ux-strategy:benchmark

# Structure an ambiguous challenge into a clear problem
/ux-strategy:frame-problem
```

### UI Design

```bash
# Design a complete screen layout
/ui-design:design-screen

# Generate a full color palette with accessibility checks
/ui-design:color-palette

# Create a complete typography system
/ui-design:type-system

# Audit a design for responsive behavior
/ui-design:responsive-audit
```

### Interaction Design

```bash
# Design a complete interaction flow
/interaction-design:design-interaction

# Model states and transitions for a component
/interaction-design:map-states

# Design error handling for a feature
/interaction-design:error-flow
```

### Prototyping & Testing

```bash
# Create a prototyping and testing plan
/prototyping-testing:prototype-plan

# Run a heuristic evaluation
/prototyping-testing:evaluate

# Design a complete usability testing plan
/prototyping-testing:test-plan

# Design an A/B experiment
/prototyping-testing:experiment
```

### Design Ops

```bash
# Plan a design sprint
/design-ops:plan-sprint

# Generate a developer handoff package
/design-ops:handoff

# Set up a design team workflow
/design-ops:setup-workflow
```

### Designer Toolkit

```bash
# Write design rationale for decisions
/designer-toolkit:write-rationale

# Structure a design presentation
/designer-toolkit:build-presentation

# Create a portfolio case study
/designer-toolkit:write-case-study
```

### Visual Critique

```bash
# Run all four visual critiques on a screen and output a prioritised fix list
/visual-critique:critique-screen
```

## Usage Patterns

### Example: Create a Design System Component

```bash
# Install the design-systems plugin first
/plugin

# Then use the command
/design-systems:create-component
```

The agent will guide you through:
1. Component naming and purpose
2. Variant definitions
3. Accessibility requirements
4. Token usage
5. Documentation structure
6. Code examples

### Example: Run User Research Discovery

```bash
# Install the design-research plugin
/plugin

# Start the discovery cycle
/design-research:discover
```

The agent will help you:
1. Define research goals
2. Choose appropriate methods
3. Create screeners and scripts
4. Plan recruitment
5. Synthesize findings
6. Generate artifacts (personas, journey maps)

### Example: Audit Responsive Design

```bash
# Install the ui-design plugin
/plugin

# Run the audit
/ui-design:responsive-audit
```

The agent will check:
1. Breakpoint strategy
2. Layout flexibility
3. Touch target sizes
4. Content prioritization
5. Performance considerations

## Configuration

Each plugin is self-contained with no external configuration required. Skills and commands are immediately available after installation.

### Plugin Structure

```
designer-skills/
├── design-research/
│   ├── skills/
│   │   ├── user-personas.md
│   │   ├── journey-mapping.md
│   │   └── ...
│   └── commands/
│       ├── discover.md
│       └── ...
├── design-systems/
├── ux-strategy/
└── ...
```

### Gemini Extension Structure

```
.gemini/extensions/
└── design-research/
    ├── gemini-extension.json
    └── GEMINI.md
```

## Common Workflows

### Setting Up a New Design Project

```bash
# Install strategic and research plugins
/plugin

# Frame the problem
/ux-strategy:frame-problem

# Run discovery research
/design-research:discover

# Define UX strategy
/ux-strategy:strategize
```

### Building a Component Library

```bash
# Install design-systems plugin
/plugin

# Extract design tokens
/design-systems:tokenize

# Create component specs
/design-systems:create-component

# Audit for consistency
/design-systems:audit-system
```

### Preparing for Developer Handoff

```bash
# Install design-ops and designer-toolkit plugins
/plugin

# Write design rationale
/designer-toolkit:write-rationale

# Generate handoff package
/design-ops:handoff
```

## Troubleshooting

### Plugin Not Found

**Issue**: `/plugin` command doesn't show the marketplace or plugins.

**Solution**: Ensure you've added the marketplace first:

```bash
/plugin marketplace add Owl-Listener/designer-skills
```

### Commands Not Working

**Issue**: Commands like `/design-research:discover` return an error.

**Solution**: Verify the plugin is installed:

```bash
/plugin
```

Check the **Installed** tab. If missing, go to **Discover** and install the required plugin.

### Gemini Extensions Not Loading

**Issue**: Gemini CLI doesn't recognize the extensions.

**Solution**: Ensure the directory structure is correct:

```bash
ls -la .gemini/extensions/design-research/
# Should show: gemini-extension.json and GEMINI.md
```

Restart your Gemini session after copying extensions.

### Partial Installation

**Issue**: Only some plugins are available.

**Solution**: Install plugins individually as needed. You don't need all 9 plugins — install only what your project requires to keep the context manageable.

## Best Practices

1. **Install Incrementally**: Start with 2-3 plugins relevant to your current work, not all 9 at once.

2. **Use Commands as Workflows**: Commands chain multiple skills together — use them for complex tasks rather than invoking skills individually.

3. **Combine Plugins**: Many workflows benefit from multiple plugins (e.g., `ux-strategy` + `design-research` + `ui-design`).

4. **Reference Documentation**: Each skill includes detailed context. Ask the agent to explain a skill if you're unsure how to use it.

5. **Workspace vs Global**: For Gemini, use workspace-scoped extensions for project-specific design work, global extensions for personal design methodology.

## Repository Structure

The source repository contains:
- Plugin directories (each with skills and commands)
- `.gemini/extensions/` compiled for Gemini CLI
- `CONTRIBUTING.md` for adding new skills
- Individual `SKILL.md` and `COMMAND.md` files

## License

MIT License — free to use, modify, and distribute.
