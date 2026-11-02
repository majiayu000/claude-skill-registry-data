---
name: alt-text
description: |-
  Use when the user shares an image, chart, diagram, screenshot, or figure and needs it described — for alt-text, accessibility, documentation, or to understand what it depicts.
---

# Alt-Text

## When to Use

- User attaches an image and asks for a description or alt-text
- User shares a chart, diagram, schematic, or screenshot and wants it explained
- User needs an accessible description for documentation or publishing

If the image is not attached, ask the user to attach it before proceeding.

## Invocation Notice

- Tell the user when this skill is running: `alt-text`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Instructions

Describe the figure so a reader who cannot see it understands both what it depicts and what it communicates.
The description should be detailed enough that someone could reproduce or redraw the figure from the text alone.

Cover, as applicable:

- Figure type and overall structure (e.g., bar chart, flowchart, photograph, schematic)
- Key elements: labels, axes, data values, components, or steps
- Relationships, trends, comparisons, sequences, or hierarchies shown
- Outcomes, conclusions, or emphasis the figure conveys

Write in plain declarative sentences, present tense.
End with a period.

Do not:

- Open with "image of," "picture of," "figure of," "graphic of," or similar
- Use phrases like "shown above," "as seen," or "depicted here"
- Describe visual styling (colors, fonts, layout) unless it carries meaning
- Guess at emotions, identities, or intent not clearly conveyed by the figure

## Output

Respond with the description only — no preamble, commentary, or metadata.
