---
name: gpt-image-2-prompt-crafter
description: Create, refine, or template high-quality GPT-image-2 / GPT Image image-generation prompts. Use whenever the user asks to write a prompt, 提示词, 文生图提示词, 图像编辑提示词, prompt template, product visual, portrait, poster, UI mockup, infographic, character sheet, storyboard, or wants to turn an image idea into a ready-to-paste image prompt, even if they do not explicitly mention GPT-image-2.
---

# GPT Image Prompt Crafter

Create ready-to-paste visual prompts, not generic prompt-writing advice. Follow the user's language by default; for Chinese users, write the prompt in Chinese unless they ask otherwise.

## Core Workflow

1. Identify the task mode: new image, image edit, reference-image adaptation, text-heavy design, multi-panel layout, or reusable template.
2. Infer reasonable defaults from the user's intent. Ask at most three clarifying questions only when missing information would materially change the result.
3. Read [references/prompt-patterns.md](references/prompt-patterns.md) before drafting category-specific prompts, optimizing an existing prompt, or building a reusable template.
4. Build the prompt from concrete visual blocks:
   - output format and medium
   - subject, action, expression, pose, or product role
   - for human subjects, face-first aesthetic anchors: apparent adult age, face shape, facial proportions, eyes, nose, lips, skin texture, hair, makeup, and expression
   - environment and spatial relationships
   - composition, camera angle, framing, and aspect ratio
   - lighting, color palette, materials, texture, and atmosphere
   - exact text, typography, labels, UI elements, or layout rules when needed
   - preservation rules for edits and reference images
   - quality and realism cues that match the medium
5. Remove weak filler. Replace vague terms like "beautiful", "high quality", or "cool" with visible evidence: lens, light direction, material, layout, color, print texture, or interaction.
6. Keep constraints explicit. Do not add silent fallbacks, hidden caps, fake success paths, or defensive clauses that hide failure.

## Creative Expansion Rules

When the user's request is short, generic, or mainly aesthetic, do not collapse it into one fixed scene. First infer the latent visual intent, then expand it into distinct image directions that differ in environment, mood, composition, wardrobe, and light.

- Treat "漂亮", "好身材", "高级感", "氛围感", and similar words as signals to invent visible specifics, not as final description.
- Build scenes from a combination of environment archetype, spatial anchor, surface material, weather or time, and lighting signature instead of reusing a fixed background.
- Avoid repeating the same default human-photo stack across prompts unless the user explicitly asks for it.
- If the request is broad enough to support multiple good answers, output 2-3 ready-to-paste prompt variants with clearly different visual directions.
- If the user asks for one prompt only, still think through multiple directions internally and choose the strongest one.

## Human Beauty Defaults

For human-subject prompts, treat the user's beauty preference as a primary visual requirement, not a vague mood word. If the user asks for "女生", "女孩", "女模特", "漂亮", "脸蛋好看", "清纯", or similar without a conflicting style, default to an adult Asian woman with a clean, pure, natural face aesthetic.

- Convert "清纯" into visible traits: soft oval or small heart-shaped face, balanced facial thirds, clear almond-shaped eyes, natural straight brows, delicate straight nose bridge, softly defined lips, translucent natural skin, light blush, minimal eyeliner, transparent lip tint, and soft black or dark-brown hair.
- Keep the face attractive through concrete anatomy, expression, and light. Use phrases such as "干净柔和的鹅蛋脸", "清澈杏眼", "自然卧蚕", "鼻梁细直", "唇形柔和", "皮肤有真实细腻纹理", and "微笑克制自然".
- Avoid drifting into a mature, cold, seductive, heavy-makeup, nightclub, or overtly sexual style unless the user requests it.
- When the user says "脸蛋漂亮" or comments that previous faces were not good enough, make the face description the first detailed paragraph after the opening sentence.
- When the user says "身材好", describe elegant adult proportions, posture, garment fit, and silhouette through fashion photography language. Do not make body parts the center of the prompt.

## Mode Selection

Use the user's subject to choose the prompt shape:

- Human subject, portrait, model, fashion, street photo, editorial photo, actor, influencer, or character photo: use the structured human-subject prompt pattern from `references/prompt-patterns.md`.
- Product, packaging, UI, infographic, poster, character sheet, multi-panel layout, or image edit: use the matching category pattern from `references/prompt-patterns.md`.
- Simple abstract or environment-only requests can stay compact when structure would add empty detail.

## Default Output

Use this structure unless the user asks for another format:

```markdown
最终提示词：
[ready-to-paste prompt]

可替换变量：
- `{变量名}`: [meaning]
```

Omit `可替换变量` for one-off prompts with no placeholders. Default answers must contain only the sections shown above. When the user asks for variety or gives an underspecified aesthetic request, it is valid to place multiple distinct prompt variants under `最终提示词` as separate ready-to-paste options. When the user asks to avoid artifacts, style drift, text, layout errors, or unrelated edits, express those constraints as positive, concrete visual instructions inside `最终提示词`.

## Composition Rules

- Put the main deliverable first: "生成一张...", "Create...", "Replace only...", or another direct command.
- Use paragraph or section structure for complex prompts. For human-subject photography, default to multiple short structured paragraphs inside `最终提示词`, even when the user gives only a short idea.
- For human-subject photography, internal paragraph labels such as "人物外貌细节：", "灯光效果说明：" and "构图风格要素：" are allowed inside `最终提示词`; do not add extra top-level answer sections outside the default output structure.
- For human-subject photography where face attractiveness matters, include a compact "脸部审美锚点：" paragraph before wardrobe and scene. It should specify face shape, eye shape, brows, nose, lips, skin, makeup, hair, and expression in concrete visible terms.
- For human-subject photography, vary the visual recipe across requests: change scene archetype, camera height, lighting signature, outfit family, and emotional tone instead of repeating the same elegant studio or city-glass aesthetic.
- For templates, use `{变量名}` for reusable slots and define every variable once.
- For exact visible text, put the text in quotes and specify placement, language, typography, and readability.
- For image edits, name each reference image by role, state what must be preserved, state what changes, and forbid unrelated changes.
- For consistency tasks, explicitly preserve face, body shape, pose, camera angle, lighting, and background where relevant.
- For multi-panel grids, define row/column layout, each panel's content, scale consistency, and whether the grid borders should be visible.

## Quality Bar

Before finalizing, check that the prompt answers:

- What is the viewer looking at?
- Where is each important element placed?
- What makes the image belong to the requested genre?
- If a human face matters, is the face aesthetic concrete enough to guide generation instead of relying on "漂亮"?
- If the user prefers "清纯", did the prompt avoid heavy makeup, cold glamour, and seductive styling?
- How should light, color, texture, and camera behave?
- Which text must be exact and readable?
- What must remain unchanged if reference images are involved?
- Does any instruction contradict another instruction?

If the user provided an existing prompt, preserve the intent while making structure, specificity, and constraints clearer. Do not rewrite it into a different concept unless asked.
