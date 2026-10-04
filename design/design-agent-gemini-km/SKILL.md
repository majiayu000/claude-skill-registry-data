---
name: "Design Agent Gemini"
description: "Run a focused UI polish or mockup-to-implementation pass through Gemini CLI using the custom subagent `design-agent-gemini`."
alwaysAllow: ["Bash"]
---

# Design Agent Gemini

Use this when you want Gemini CLI to handle a visual-first UI pass.

## Preferred agent
On Gemini CLI, prefer the custom subagent:

- `design-agent-gemini`

## Model guidance
- The bundled subagent is set to `gemini-3.1-pro-preview` on this machine because it is available and strong for design review.
- Inspect screenshots or real UI before making design claims.

## Recommended prompt shape
"Use design-agent-gemini for a UI polish pass on <surface>. Inspect the current UI or screenshots first, state the design intent, make the smallest high-leverage improvements, then report visual QA findings, interaction QA findings, and remaining weaknesses."

## Output checklist
- Design intent summary
- Top UI/UX issues found
- Concrete changes recommended or applied
- Breakpoint and interaction QA notes
- Remaining risks / next pass
