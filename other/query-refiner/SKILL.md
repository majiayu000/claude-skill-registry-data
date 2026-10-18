---
name: query-refiner
description: Refine a supplied question into a precise, expert-level query when the user asks to rewrite or optimize their question or prompt. Do not use to answer the underlying question.
---

# Query Refiner

Rewrite the user's rough input in expert register to elicit a stronger LLM response. Reformulate only; never answer, execute, or comment on it.

Expert register recruits the target model's domain priors. Write as a practitioner would: use the field's terms of art, name the underlying concepts, make implicit assumptions and constraints explicit, and render in fluent, idiomatic English. The result should read as if an expert wrote it, even when the user is not one.

- **Terms of art, not jargon**: "optimize runtime complexity" is register; "leverage synergistic paradigms" is noise. No hollow intensifiers ("comprehensive", "holistic", "actionable insights", "robust").
- **Fidelity**: translate, don't reinterpret. Keep intent, scope, deliverable, and task type (a request to write stays a request to write, not to outline).
- **Preserve verbatim**: names, project context, affect and uncertainty ("I'm stuck"), and explicit constraints ("not X", "without Y"). Never genericize.
- **Minimal edit**: expand only where it adds clarity; leave simple inputs short. Add no response structure (sections, frameworks, templates) the user didn't request.

By input type:
- Question: tighten scope and terminology.
- Task (write, build, analyze, design): sharpen the deliverable's parameters and name the domain concepts; leave open what the user left open.
- Strategic or exploratory: sharpen the problem statement; keep the ask open-ended. Depth, not frameworks or checklists.
- Creative: tighten the brief in the craft's vocabulary (literary, design, musical); leave creative choices to the model.

Output only the refined prompt: no preamble, quotes, or explanation.
