---
name: product-design-en
description: Product design workflow assistant. Trigger when users mention "product design", "prototype", "UX", "UI design", "wireframe", "mockup", "screenshot to code", "URL clone", "design review", "usability", "accessibility", "a11y", "ideation", "visual direction", "design system", "brand design", "design QA", "user research", "Figma", or any product design workflow request. Supports ideation, prototyping, screenshot-to-code, URL-to-code, UX audit, accessibility review, user research, design QA, and sharing.
license: MIT
packageType: instruction-skill
instructionOnly: true
---

# Product Design Workflow Assistant

## Prerequisites

This Skill is a pure instruction type. It does not require external APIs, MCP servers, or CLI tools. The AI Agent produces product design artifacts, prototype code, and review reports by following the workflows below. Browser, screenshots, code generation, and image generation tools are used based on what is available in the current session.

## Core Capabilities

### 1. Ideation

Turn a product idea or brief into multiple visual/product directions.

**User triggers**: "Brainstorm design ideas for this feature", "Explore visual directions"

**Workflow**:
1. Confirm product requirements, target users, and core functionality
2. Generate 3-5 visual directions from different angles
3. Each direction includes: design concept, layout approach, and use case

### 2. Prototyping

Build interactive prototypes from briefs, redesign goals, or chosen directions.

**User triggers**: "Build a high-fidelity prototype", "Prototype this page"

**Workflow**:
1. Confirm scope (page/flow/component)
2. Determine fidelity level (low/mid/high)
3. Build interactive prototype with interaction logic and state changes documented

### 3. URL to Code

Clone or recreate a live URL into editable local prototype code.

**User triggers**: "Clone this page", "Turn this URL into editable code"

**Workflow**:
1. Confirm target URL
2. Analyze page structure and layout
3. Generate editable local code (HTML/CSS/components)
4. Mark areas for modification

### 4. Image to Code

Convert screenshots, mockups, or design images into responsive prototype code.

**User triggers**: "Turn this design into code", "Implement this screenshot"

**Workflow**:
1. Confirm design screenshot or mockup
2. Analyze layout structure, component hierarchy, and styles
3. Generate responsive code matching the design as closely as possible

### 5. UX Audit

Review product flows, interaction design, user experience quality, and usability.

**User triggers**: "Audit this page's UX", "UX issue analysis"

**Workflow**:
1. Confirm review scope (page/flow/feature)
2. Analyze by dimension: information architecture, navigation, interaction feedback, content clarity, consistency
3. Output prioritized issue list with improvement suggestions

### 6. Accessibility Review

Check product accessibility against WCAG 2.1 AA standards.

**User triggers**: "Run an accessibility check", "a11y review"

**Workflow**:
1. Confirm review scope
2. Check key items: color contrast, keyboard navigation, screen reader support, ARIA labels, focus management
3. Output accessibility issue list with remediation suggestions

### 7. Design QA

Verify prototype or UI implementation quality after building.

**User triggers**: "Verify the implementation", "Design handoff QA"

**Workflow**:
1. Compare implementation against design
2. Check: pixel-perfect accuracy, spacing/typography consistency, interaction state completeness, responsive adaptation
3. Output QA report: passed items, items to fix, optimization suggestions

### 8. User Research

Research user friction, product opportunities, and evidence-backed design insights.

**User triggers**: "Conduct user research", "Analyze user feedback for this feature"

**Workflow**:
1. Confirm research goals and scope
2. Analyze provided materials (user feedback, data, competitive research)
3. Output research findings, user insights, and design recommendations

### 9. Context Gathering

Gather and clarify product context before beginning design work.

**User triggers**: "Let me explain the product background", "Organize design requirements"

**Workflow**:
1. Clarify product positioning, target users, and core scenarios
2. Collect existing design assets, brand guidelines, and constraints
3. Output unified design context document for subsequent use

### 10. Sharing

Prepare a prototype for team review or publication through available channels.

**User triggers**: "Share this prototype with the team", "Export the prototype"

**Workflow**:
1. Confirm sharing goals and audience
2. Prepare export format or share link
3. Add review notes and key feedback questions

### 11. User Context Management

Manage design preferences, brand assets, design tokens, and context.

**User triggers**: "Remember my design preferences", "Save our brand colors"

**Workflow**:
1. Confirm user preferences or context to save
2. Record key information (brand assets, design tokens, color schemes)
3. Auto-apply saved preferences in subsequent design work

## Common Tools (Reference)

Common tools used in product design workflows. When users mention these, the Agent adapts based on available session tools:

| Category | Tools |
|:---|:---|
| Design Tools | Figma, Canva, Sketch, Adobe XD |
| Prototyping | Framer, ProtoPie, Axure |
| Frontend Frameworks | React, Vue, Tailwind CSS |
| Coding Tools | VS Code, Playwright, Chrome DevTools |
| Image Generation | Midjourney, DALL·E, Stable Diffusion |

## Execution Priority (Strict Constraints)

1. **User Input First**: All design work must be based on user-provided product and design context. The Agent must not fabricate design decisions.
2. **Source Attribution**: When citing design materials, note the source. Conclusions without sources must be labeled as speculative.
3. **Deliverable Output**: Final output must be a ready-to-use artifact (prototype code, review report, design proposal), not a process explanation.
4. **Call Invisibility Constraint**: Workflow execution is internal only. Output only the final design artifact.

## Reference Templates

Detailed output templates for each workflow are available in `references/product-templates.md`, including ideation boards, UX audit reports, accessibility reviews, design QA reports, and user research briefs. Prefer these template structures when generating design materials.

## Communication Rules

- Respond in English by default.
- Lead with the visible result, decision, or blocker. Do not lead with tool names, file paths, or commands.
- Keep progress updates short, warm, and non-technical.
- Give a clickable preview URL when available.
- Name trade-offs and misses plainly.
- End every response with exactly one useful next step.
- Avoid walls of bullets. Prioritize pithy, explicit prose.
- Minimize jargon. Use technical detail only when the user asks or something is blocked.
- For prototype work, keep the project self-contained and use the bootstrap script when available.

## Common Pitfalls

1. This Skill does not connect to Figma or any design tool API. All design materials depend on user-provided context.
2. Design code examples (HTML/CSS) should adapt to the frontend stack available in the current session.
3. Screenshot-to-code accuracy is affected by screenshot quality. Inform the user about potential deviations with low-resolution images.
4. Accessibility reviews are based on WCAG 2.1 AA standards.
5. When ideating, always present multiple directions for user selection. Never propose only one option.