---
name: gpt-image2-prompt-director
description: |
  Turn a weak idea into a high-impact GPT image2 (gpt-image-2) generation brief: prompt director workflows, idea generation, visual prompt frameworks, artifact specs for avatars, sticker/emoji packs, infographics, platform covers, posters and product shots, plus benchmark evaluation against an expert prompt set. Use when the user wants to create, improve, repair or systematically evaluate image generation prompts, or says $gpt-image2-prompt-director, 生图提示词, 图片提示词优化, 头像提示词, 表情包, 信息图提示词, 海报提示词, 修一下这个 prompt.

---

# GPT Image2 Prompt Director

Create high-quality GPT image2 prompts from weak ideas, or evaluate generated prompts against the archived Xiaoxiaodong expert prompt benchmark.

## Default Workflow

1. Identify the input mode:
   - **Weak idea**: one theme, title, object, phrase, image concept, or product.
   - **No idea**: user only gives identity, platform, or goal; first generate candidate ideas.
   - **Prompt repair**: user provides an existing prompt; evaluate and revise it.
   - **Evaluation**: user asks to run or inspect the benchmark.
2. Load [references/prompt-framework.md](references/prompt-framework.md) when generating or repairing prompts.
3. If the idea feels ordinary, avatar/IP-like, UI-like, or product-like, also load [references/artifact-spec-framework.md](references/artifact-spec-framework.md). First choose the artifact container before writing the prompt.
4. For avatar, profile-picture, sticker, emoji, meme, or expression-pack tasks, also load [references/avatar-expression-framework.md](references/avatar-expression-framework.md). Treat the output as a reusable identity asset or expression system, not as a generic portrait.
5. Generate one complete final prompt, plus 2-3 optional creative directions when useful.
6. Before finalizing, check the prompt has:
   - role positioning
   - anti-definition
   - input contract
   - internal planning
   - content planning
   - visual system
   - anti-failure constraints
   - output spec
   - self-check
7. If the user asks for validation, run the bundled evaluator.

## No-Idea Mode

When the user has no idea:

1. Ask for no clarification unless the goal is truly ambiguous.
2. Infer a likely publishing context from the user request.
3. Generate 10-20 candidate image plays.
4. Score each by:
   - surprise
   - GPT image2 fit
   - visual clarity
   - shareability
   - ease of execution
5. Pick the strongest direction and expand it into a complete prompt.

## Wow Mode

When the first output feels generic or the user asks for something less ordinary:

1. Stop optimizing adjectives.
2. Pick a stronger artifact container.
3. Decide whether a multi-cell grid/contact sheet would improve the result.
4. Create 3-5 high-concept collisions.
5. Prefer structured spec output for UI, social, avatar identity, poster systems, and product mockups.
6. Add a concrete Definition of Done.

For avatar and personal-brand work, prefer an `avatar identity system` over a standalone portrait unless the user explicitly asks for a single image only.

Use `n x n` grid decomposition when variety is part of the value: avatars, stickers, meme packs, character variants, icon systems, material/style tests, storyboards, or repeated information cards. Prefer `3 x 3` for avatar exploration and `4 x 4` for sticker/expression packs. Avoid grids for cinematic posters, hero key visuals, luxury product shots, or any image that needs one dominant focal point.

## Avatar / Sticker Rules

For avatar prompts:

- Do not default to a cinematic portrait, fashion editorial, or realistic headshot.
- If there is no reference image, prefer a `3 x 3 avatar exploration sheet` first.
- If the user needs one final avatar, make it a platform avatar asset: large head silhouette, simple background, one memorable symbol, one accent color, circular-crop safe, readable at `80px`.
- Keep the symbol secondary to the face. Do not cover most of the face with paper, crystals, UI, geometry, or decorative objects.
- Prefer semi-realistic / semi-graphic / illustrated / badge-like treatments over photographic realism unless the user explicitly asks for a photo.
- If a personal-brand avatar looks like a poster portrait, compare against [examples/personal-brand-avatar-repair.md](examples/personal-brand-avatar-repair.md) and repair toward avatar-asset mechanics.

For sticker and expression prompts:

- Default to a `4 x 4` expression pack.
- Use "consistent imperfection": the same character can be wrong, but must be wrong in the same way.
- Text, when present, should feel hand-drawn with the image, not typeset afterward.
- Each cell must be independently usable and emotionally clear.

## Evaluation Commands

Create a runnable eval pack:

```bash
cd gpt-image2-prompt-director
node scripts/eval_prompt_director.mjs --init-run /tmp/gpt-image2-prompt-director-eval
```

Evaluate the archived expert prompts as a sanity baseline:

```bash
cd gpt-image2-prompt-director
node scripts/eval_prompt_director.mjs --gold --report /tmp/gpt-image2-prompt-director-gold-report.md
```

Evaluate generated prompts saved as `outputs/<case-id>.md`:

```bash
cd gpt-image2-prompt-director
node scripts/eval_prompt_director.mjs \
  --outputs /tmp/gpt-image2-prompt-director-eval/outputs \
  --report /tmp/gpt-image2-prompt-director-eval/report.md \
  --fail-under 80 \
  --strict
```

Evaluate one prompt:

```bash
cd gpt-image2-prompt-director
node scripts/eval_prompt_director.mjs \
  --case-id 09 \
  --prompt-file /absolute/path/to/prompt.md
```

For scoring details, read [references/rubric.md](references/rubric.md).

## Benchmark Data

The benchmark is in [evals/benchmark-cases.json](evals/benchmark-cases.json). It contains 40 cases derived from an archived prompt corpus and regression tests. Each case includes:

- weak input
- source title
- category
- expected capabilities

Use it to test whether a generated prompt reconstructs expert-level capability from weak input. Do not treat it as a memorization target.
