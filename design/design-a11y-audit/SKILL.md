---
name: design-a11y-audit
description: Audit a Figma component or frame for accessibility in one pass — design lint, contrast, color-blindness simulation, focus order — with fixes. Use when the user points at a Figma design and wants a quick accessibility check before it goes to development. Not for a full WCAG-EM audit of a built site or app, or mentoring feedback; see /accessibility-scope or /coaching-a11y.
metadata:
  figma-aware: true
---

# Accessibility Audit

Run a full WCAG accessibility audit on a Figma component or frame, covering design lint, contrast, color blindness, and focus order.

See also `/accessibility-scope` for the full audit path — target, WCAG level and test plan — rather than a one-pass Figma check.

## Prerequisites

**Figma.** Steps marked *Figma* use a Figma MCP server you connect to this agent yourself; this pack ships none and makes no network calls. Before you ask the user anything or run the first such step, list the tools available to you and bind each capability the step names to one tool, as `references/figma-capabilities.md`, bundled with this skill, describes: the official Figma server's tool named there, else any tool whose description plainly does the same thing. With a capability bound, take the file key and node id from a Figma link in the request or the conversation, else from the `file:` line of the `## Tools` section of the latest earlier artifact of this project that has one; when a bound capability needs one and there is none, ask for the link once, with any other question you ask. With nothing bound, never ask for a link. Record the result in a `## Tools` section after any `## Recalled` section: a `- file:` line (the Design file; a board or a deck goes on a `- board:` or `- deck:` line), one line per bound capability (`- read-tokens: get_variable_defs (figma)`), and a `- created:` line for node ids you created; or the single line `No Figma server: steps marked Figma ran without one.`; a skill with no artifact says the same in its summary. For an unbound capability do what the step's *Without Figma* line says, using first any values the user gave in the request or in files it names: never ask the user to connect a server, never invent values a tool would have returned, and never report a step as run when it was not.

## Process

1. **Identify the target.** A Figma link to the component or frame, or colours and structure the user pasted. With `read-node` bound and neither given, ask for the link once; with nothing bound and nothing pasted, say what you cannot check and stop.

2. **Read the target.** *Figma (read-node, read-tokens):* read the node's structure, text, sizes, layer names and applied colours. *Without Figma:* use the values the user pasted.

3. **Run the checks** described in `references/a11y-checks.md`: contrast (normal and large text) for every foreground/background pair, colour-vision simulation for the primary pairs (note any pair that loses sufficient contrast), focus order, target size and text size, alt text. Each line of the report ends with `computed`, `simulated` or `not checked`.

4. **Compile the audit report:**
   - Summary: total checks run, pass/fail counts
   - Lint issues (text too small, touch targets, missing alt text)
   - Contrast results (AA/AAA pass/fail per pair)
   - Color blindness results
   - Focus order analysis
   - Remediation recommendations

5. **Present the report** to the user, opening with the tool binding: one line per bound capability, or the no-server sentence.

## Output

A comprehensive accessibility audit report presented to the user, opening with the tool binding, with actionable remediation steps.
