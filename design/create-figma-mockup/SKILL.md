---
name: create-figma-mockup
description: Turn a PRD or idea into a low-fidelity mockup (screen inventory, wireframe spec with states and interactions, and a single-file HTML wireframe you can import into Figma). Use to visualize a feature before design starts. It does not edit Figma files directly.
---

# Create Figma Mockup

Give the team something to point at: a low-fidelity mockup of the screens a feature needs, built from the requirements, with the states engineers and designers will ask about.

## Reasoning Framework

PMs need to show, not just tell, and they need to do it early. High-fidelity mocks invite pixel debates, so this skill stays at wireframe fidelity: structure, real content, flows, and states. The output is plain markdown and HTML, which is reviewable, versionable, and importable into Figma. A designer takes it from there.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| Mockup spec | Markdown: screen inventory, per-screen spec, flow diagram | Designer, engineers, stakeholders |
| Wireframe | Single HTML file built from `references/wireframe-kit.html` (grayscale, no external assets) | Browser, or Figma via an HTML import plugin |
| Concept image prompt (optional) | Ready-to-paste prompt for Gemini or Grok | User |

## When to Use

- A PRD exists and the team needs to see the screens
- Exploring layout options for a flow before a designer is involved
- Preparing a stakeholder review or usability test prototype

## When NOT to Use

- Polished visual design or brand work: that belongs to a designer
- System architecture pictures: use `create-architecture-diagram`
- Writing the requirements themselves: use `create-prd` first

## Inputs

1. **Source**: PRD path, brief, or a description of the feature.
2. **Platform**: web desktop, web mobile, iOS, or Android (one or more).
3. **Primary user and job**: who, and what they are trying to get done.
4. **Key flows**: 1–3 flows to cover.
5. **Design system** (optional): component names or a Figma library to reference.
6. **Constraints**: accessibility, localization, existing screens to match.

## Steps

1. **Extract from the source**: user, job, flows, and every requirement that changes the UI. List your assumptions separately.
2. **Screen inventory**: one table row per screen (ID, name, purpose, entry points, primary action). Include variants for empty, loading, error, and permission states where they differ.
3. **Spec each screen**:
   - **Layout**: regions (header, navigation, content, sidebar, footer) and what lives in each.
   - **Components**: design-system names when known (for example "Data table", "Primary button").
   - **Content**: realistic copy and data, never lorem ipsum. Include edge data such as long names, zero results, or 10,000 rows.
   - **States**: empty, loading, error, success, no permission, offline where relevant.
   - **Interactions**: what each action does and where it goes.
   - **Accessibility**: focus order, labels, touch targets of at least 44×44 pt (iOS) or 48×48 dp (Android), and don't rely on color alone.
4. **Flow**: a Mermaid `flowchart` of screen transitions (it renders in GitHub and Obsidian).
5. **Build the wireframe**: copy `references/wireframe-kit.html` to the output folder and add one `<section class="screen">` per screen (add `desktop` for wide frames). Use the kit's classes, pin numbered notes to anything non-obvious, and keep it grayscale with no external fonts, scripts, or images.
6. **Check it**: open the file. If a browser tool is available, screenshot it at mobile and desktop widths and fix overflow or overlap.
7. **Hand off to Figma**: tell the user how to bring it in. For example, an HTML-to-Figma import plugin such as html.to.design, or give the spec to a designer. If a Figma connector with write access is available in this session, you may use it. Otherwise never claim that anything was created in Figma.
8. **Optional concept image**: if the user wants a high-fidelity look, write a ready-to-paste prompt for Gemini or Grok (this repo routes image generation there).

## Spec Template

```markdown
# [Feature]: Mockup Spec
Source: [PRD] · Platforms: [..] · Assumptions: [..]

## Screens
| ID | Screen | Purpose | Entry points | Primary action |
|---|---|---|---|---|

## S1 · [Screen name]
**Layout:** .. **Components:** .. **Content:** .. **States:** .. **Interactions:** .. **Accessibility:** ..

## Flow
(Mermaid flowchart)

## Open questions for design
- ..
```

## Examples

- "Mock up the bulk export feature from docs/prd-export.md for web." Produce 4 screens (list, export dialog, progress, done/error) plus the HTML wireframe and flow.
- "Sketch the onboarding checklist for iOS and Android." Produce a shared spec with platform notes and two sets of frames in the HTML.

## Guardrails

- Wireframes, not visual design. No brand colors or imagery unless asked.
- Don't invent requirements. Anything not in the source is marked as an assumption.
- Always include empty and error states. They are where most design gaps hide.
- No real customer data in mockups.
- Don't claim a Figma file was created unless a tool actually created it.

## Related Skills

- `create-prd` / `create-prd-one-pager`: the requirements this visualizes
- `jobs-to-be-done`: when the user and job are unclear
- `validate-hypothesis`: test the mockup with users
- `library/lenny-podcast/lenny-writing-specs-designs/SKILL.md`: specs that designers love
