---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-dream-weaving
description: Develop vague feelings, memories, fragmentary imagery, or an unsatisfying concept into a drawable visual scene through collaborative conversation. Preserve the initial feeling and user choices; hand clear briefs directly to the existing production capability.
triggers:
  - oneirloom-dream-weaving
  - oneirloom
  - dream
  - weaving

---

# Dream weaving

Use this entry when the user brings an emotional seed, memory, scattered imagery, or a concept that still has no satisfying drawable scene and wants to think it through together. Keep the original feeling visible as the scene takes shape. Do not infer autobiographical facts or prescribe a surreal, dreamy, or other particular style.

Before the first substantive response, read the [shared interaction contract](../oneirloom/references/interaction-contract.md), unless its unchanged content is already available. Read the [Oneirloom coordinator](../oneirloom/SKILL.md) when the user is ready to choose an existing visual, medium, or production capability.

## Route by what is still unclear

- Use this entry for unformed emotional or memory-based ideas, disconnected imagery, and creative directions the user finds unsatisfying.
- Keep reference reconstruction, a formed scene with unclear visible relations, and a request to translate one abstract aesthetic effect into concrete image relations with [visual analysis](../oneirloom-visual-analysis/SKILL.md).
- When the scene is clear or the user asks to proceed, hand it directly to the relevant existing capability. Exploration is not a required number of turns, and the user does not need to approve a concept as a separate gate.
- If the formed scene still has an open visual direction across media, the [visual-family index](../oneirloom/references/visual-families/index.md) is an optional way to compare relevant mechanisms. A settled style goes directly to its owner.
- For a real product, read [product art direction](../oneirloom-product-art-direction/SKILL.md) before proposing a creative transformation. Preserve the source and user-stated facts with their provenance; a fictional scene cannot establish ingredients, quantity, specifications, or claims.

## Develop the scene collaboratively

Keep compact conversation notes that distinguish the user's original wording, tentative proposals, accepted choices, rejected directions, and open questions. The user's feedback is authoritative. Treat your proposals as tentative until accepted, while allowing ordinary artistic elaboration without asking permission for every detail.

Adapt the conversation to the user's response rather than following fixed stages or rounds:

- Find the expressive core in what the user actually said, without turning it into a psychological or autobiographical explanation.
- Offer a short, imaginable scene or a meaningful relationship that the user can react to. One seed is usually enough; offer multiple distinct directions only when that helps with this request. There is no fixed option count.
- Ask only a question whose answer would change the scene's direction. Give the user something concrete to respond to instead of repeating mood words or presenting a survey.
- Update what is accepted, rejected, or still uncertain after each reply. If the user rejects a direction, change the underlying relation, scale, viewpoint, or action rather than decorating the rejected concept.
- Let the user deliberate or retain ambiguity when that is meaningful to them. Do not force convergence.

Progress means clarifying a defining relation, resolving an uncertainty that changes direction, or learning what must be preserved or replaced. Keep internal working notes out of the answer unless requested.

Keep exploration replies concise and in the user's language. Do not turn an exploratory exchange into a finished bilingual prompt unless asked. When a prompt or asset is requested, follow the shared contract and the selected capability's delivery rules.

Converge and hand off when a coherent drawable scene carries the original feeling through its visible relations, or when the user asks to proceed. Read a selected medium or production skill only when needed. Read visual analysis only when visual relations remain unclear; it is not a mandatory next step. For person prompts, read [person defaults and proportions](../oneirloom/references/person-prompts.md) only when prompt production for a person is requested.

## Finish the requested deliverable

Resolve the requested output from the conversation before handoff. In prompt-development collaboration, assent such as "可以，试试看" continues drafting or revising the prompt. It does not change the deliverable to image generation. Generate an image only when image generation is itself requested. If the output remains unclear, continue useful text work or ask only when the answer is needed to decide an external action. A clear scene goes straight to production without another ideation round.

Carry the accepted feeling and choices for the subject, body region, wardrobe, pose, framing, and space into the full visual specification. When the scene calls for them, explicitly read the selected medium's method, its matching template, and other relevant methods; reuse unchanged instructions already read. Put their applicable geometry, support and contact, view-dependent garment connections, framing, light, and material relations into the final prompt instead of relying on a style or pose label.

When the user wants the environment to lead, establish the whole-frame layout and subject scale before elaborating the person. Preserve that hierarchy through handoff, and simplify conflicting or unnecessary pose and viewpoint constraints while retaining the accepted action.

For prompt-only work, follow the shared interaction contract. Include every decisive accepted relation in each required language version, and keep controls and commentary outside prompt blocks. Do not require a heading scheme, an internal checklist in prompt prose, or a minimum length. Before returning, check the complete prompt against the accepted choices and active method and template. Reading the sources or matching a few keywords does not establish that their relations survived.

Do not start research, image generation, or other external work automatically. For conversational patterns that remain unclear, consult the optional [dialogue examples](references/dialogue-examples.md); their settings and props are not defaults for new requests.
