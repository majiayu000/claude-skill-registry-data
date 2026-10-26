---
name: ui-design-prompt
description: Generate a polished UI design image-generation prompt from the current product discussion, a specification issue, or a plan, including the requested aspect ratio.
---

# UI Design Prompt

Turn the available product decisions into a single, ready-to-paste prompt for an AI image
generator. This skill creates a visual design brief; it does not implement the
UI, generate an image, or create project files.

## Input

1. Use the source named by the user: the current conversation, a specification
   issue, or a plan file. If none is named, use the current conversation.
2. Read the requested aspect ratio from the invocation. Accept common ratios
   such as `16:9`, `9:16`, `4:3`, `3:4`, and `1:1`.
3. If a named source cannot be found, ask the user for it. If the aspect
   ratio is missing and cannot be reasonably inferred from the primary device
   or screen, ask for it before generating the prompt.

## Process

Extract only design-relevant information from the source:

- Product purpose and target users
- Primary user journey and the most important screen
- Required screens, content, actions, and states
- Platform, device, and responsive requirements
- Brand, tone, accessibility, and technical constraints

Make sensible visual decisions where the plan is silent. Label no assumptions
in the final prompt; instead, choose a coherent direction that supports the
product and its users. Do not invent features, data, or workflows that are not
needed to show the planned experience.

## Output

Return exactly these sections:

### Design Direction

One short paragraph describing the visual concept and why it fits the product.

### Image Prompt

One complete prompt in a fenced `text` code block. The prompt must:

- State the product, audience, and primary screen or flow
- Describe the layout, hierarchy, navigation, controls, content, and states
- Specify the visual language: composition, typography, color, surfaces,
  spacing, iconography, imagery, and depth
- Describe realistic, legible interface content without relying on tiny text
- Include the platform/device context and responsive intent when relevant
- Explicitly include `aspect ratio: <ratio>`
- Ask for a high-fidelity UI/UX design presentation, not a generic poster,
  marketing illustration, wireframe, or code screenshot
- End with a concise negative prompt covering clutter, unrelated screens,
  unreadable text, distorted controls, inconsistent spacing, excessive effects,
  watermarks, and device mockups unless the plan specifically calls for them

Do not return multiple alternative prompts unless the user asks for options.
Keep the final prompt detailed enough to guide image generation but concise
enough to paste into a model directly. Preserve important product terminology
from the plan.

## Example invocation

```text
/ui-design-prompt --aspect-ratio 16:9
```
