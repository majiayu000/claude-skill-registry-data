---
name: daftai-gpt-image-2-5-prompt-optimizer
description: >
  Optimizes natural-language image requests and rough prompts into ready-to-use
  GPT Image 2.5 prompts using the official prompting guide as a live reference.
  Use when users ask to improve image prompts, 优化生图提示词, 把想法变成提示词,
  or write prompts for GPT Image 2.5 Flare or Sunburst. Produces prompt text,
  not images, unless the user explicitly asks to generate.
---

# GPT Image 2.5 Prompt Optimizer

Turn a rough idea or existing draft into a clear, ready-to-use image prompt. Support new scenes, reference-assisted creation, and editing instructions without promising an absolute “best” prompt.

## Scope

- This skill produces prompt text only. Do not invoke image generation merely because an image-generation tool is available.
- If the user asks only to optimize or write a prompt, return the prompt and stop. Do not routinely ask whether they want to generate an image.
- If the user explicitly asks both to optimize the prompt and generate the image, complete the prompt first, then allow the host agent to invoke its image-generation capability as a separate step. Do not ask for a second confirmation.
- Do not request API keys, install dependencies silently, or create image output files. A Git-ignored local official reference may be written under `references/gpt-image-2-5/`.
- Target GPT Image 2.5. Preserve an explicitly selected Flare or Sunburst variant; otherwise do not require variant selection or switch model families.
- Use the current request and conversation, not persistent preferences. No configuration file or mandatory first-run setup is needed. This version does not read or write persistent preferences.
- Write questions and final prompts in the user's language unless they request another language. English skill instructions do not imply English-only output.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`.
2. Detect Bun once per session with `command -v bun`; if missing, report the requirement instead of silently installing it.
3. Set working directory to `${SKILL_DIR}`.
4. Follow Workflow §1. Run `bun ${SKILL_DIR}/scripts/fetch-guide.ts` only when the published layout check fails, or when the user requested `--refresh`.
5. Replace every `${SKILL_DIR}` with the actual absolute path.

| Script | Purpose |
|---|---|
| `scripts/fetch-guide.ts` | Write the published layout when it is missing or invalid; download only if `source.md` is absent; `--refresh` updates the source |
| `scripts/split-guide.ts` | Deterministic verbatim section slicing and index generation; invoked by the fetcher, not an LLM |
| `scripts/split-guide.test.ts` | Lossless slicing and index tests; run `bun test ${SKILL_DIR}/scripts/split-guide.test.ts` |
| `scripts/fetch-guide.test.ts` | Offline extraction and local-reference tests; run `bun test ${SKILL_DIR}/scripts/fetch-guide.test.ts` |

## Workflow

### 1. Check the published local layout; fetch only if it fails

Do this before drafting or asking creative-brief questions. [references/official-guide.md](references/official-guide.md) is a retrieval protocol, not the official guide.

The local official reference is gitignored and always uses this layout:

`${SKILL_DIR}/references/gpt-image-2-5/`

| Path | Pass if |
|---|---|
| `source.md` | File exists |
| `INDEX.md` | File exists, contains `Layout: gpt-image-2-5/v1`, and links Overview and Prompting fundamentals |
| The "Read first" files named in `INDEX.md` | Those files exist beside `INDEX.md` |

Compare only against this layout. Do not treat a path receipt, `references/official-guide.md`, or any other folder under `references/` as a pass.

| Result | Action |
|---|---|
| All rows pass | Read `INDEX.md`, then Overview and Prompting fundamentals. Do not run `fetch-guide.ts`. Do not announce downloading, crawling, or preparing the official guide. |
| Any row fails | Run `bun ${SKILL_DIR}/scripts/fetch-guide.ts`. Only a missing `source.md` downloads. Re-check the same layout, then read `INDEX.md`. |
| User requested an update | Run the same command with `--refresh`. |

Do not read the complete source or every section by default. A path receipt is not the reference itself.

Follow [references/official-guide.md](references/official-guide.md) for source boundaries and failures. Never present an unverified general rewrite as an official-guide-based result.

### 2. Guide beginners only when needed

Use the request, not whether this is a first session, to decide how much help to provide:

| Input | Action |
|---|---|
| Skill invoked without an idea, or “How do I use this?” | Briefly explain that a rough description is enough and the result is a prompt, not an image. Ask what they want to show; offer use and visual style as optional details. |
| A rough but usable idea | Draft immediately. Leave optional details open rather than presenting a questionnaire. |
| User explicitly requests guided help | Ask only missing, useful questions together; accept “you decide” for creative choices. |
| Conflicting requirements or indispensable missing content | Ask a focused clarification before finalizing. Do not silently invent exact copy, resolve contradictions, or claim to inspect inaccessible images. |

A possible beginner invitation, adapted to the user's language:

“Describe the image you have in mind, even in one sentence. What should it show? If you know, add where you will use it and the look you prefer. ‘Not sure’ is fine.”

Optional example: “A sleepy fox on a library windowsill, for a book-club invitation, in colored pencil, with no text.” This is an illustration of input, not a mandatory template.

When more guidance is requested, choose from these questions rather than asking all of them every time:
- What should the image show, or what should change in an existing image?
- Where will it be used, and is a shape or aspect ratio required?
- What visual style is intended? Is there exact text or anything that must remain unchanged?

When clarification is needed, prefer the host's native question dialog or structured user-input tool if available and permitted in the current mode. Use plain text only when that capability is unavailable or disallowed. Do not assume a particular tool name.

Combine related questions into one dialog where supported. Offer concise, relevant choices for bounded decisions, but allow free-text answers or “you decide” for creative preferences when the tool supports them. Do not create a dialog when the request is already clear, and do not treat a preselected choice as a submitted answer.

Follow the tool's actual waiting behavior: synchronous tools may return answers directly; asynchronous tools may deliver them later. Wait for essential answers before finalizing, but do not block on optional preferences.

### 3. Resolve references and select an official example

Inspect accessible user reference images before making visual claims. Assign roles such as edit canvas, subject identity, composition, style, or palette; a single image may have multiple roles. Do not assume that every reference controls every property.

Resolve aspect ratio in this order:
1. Honor the user's explicit output ratio. If it conflicts with a requirement to preserve the entire layout, ask whether cropping, extending the canvas, or changing the ratio is acceptable.
2. For an edit canvas or a reference explicitly defining composition, preserve its ratio unless instructed otherwise. Use available image dimensions to determine the ratio; never invent exact dimensions from a visual guess.
3. A style, identity, or palette reference alone does not determine output ratio. Use an explicit destination requirement when supplied. Otherwise leave the ratio unspecified, or offer a clearly labeled suggestion if useful; do not force a ratio question for every request.
4. With multiple incompatible composition references and no designated base, ask which image defines the canvas. Do not arbitrarily inherit the first image's dimensions.

Before writing the prompt, select the closest example from the verified official 2.5 guide by task and constraints, not merely by a shared subject. Use the generated index to read its complete section file plus any listed parent context. Preserve explanations, prompt blocks, settings, and image links; these files are direct source slices, not summaries. Follow references to earlier examples or input images through the index when needed. Sequential refinement workflows remain intact so later steps retain prerequisites. Add a second example only when it addresses a distinct requirement, such as exact text within an editing task.

Use these section titles as navigation hints, verifying they exist in the actual reference rather than treating this table as a substitute for reading:

| User task | Candidate official section |
|---|---|
| A new photograph with specific visual treatment | Control style and lighting |
| A poster with verbatim wording | Render exact text |
| Reuse only the appearance of a reference | Transfer a visual style |
| Preserve a subject while changing its presentation | Preserve identity and change clothing |
| Give several input images distinct roles | Combine references |
| Replace image text without redesigning the layout | Translate while preserving layout |
| Make one local change and preserve the rest | Remove an object / Change one condition |
| Reinterpret a sketch without losing its structure | Turn a drawing into a realistic image |
| Isolate a referenced product with transparency | Create a transparent product cutout |

Extract the useful instruction pattern: what the example specifies, what it preserves, how references are assigned, and how constraints are expressed. Adapt that pattern to the user's request; do not import the example's subject, branding, dimensions, quality settings, or unrelated exclusions.

If no example fits, use the guide's prompting fundamentals and say so when identifying the source. If the reference is unavailable, follow its failure rules rather than inventing an example match.

### 4. Preserve intent and optimize

Identify generation versus editing and preserve explicit subject, count, purpose, copy, aspect ratio, style, and exclusions. Minor unspecified details may remain open. Briefly disclose assumptions that materially affect the creative direction; do not invent brands, identities, or advertising claims.

If an editing reference cannot be accessed, do not claim to have seen it. Ask for the image when visual judgment is essential; a description-only request such as “change only the background” can be drafted with an explicit uninspected-reference note.

Apply relevant methods from the verified guide using original wording:
- Make the subject, purpose, composition, and meaningful material, lighting, or style choices concrete.
- Preserve required image text verbatim and specify placement and frequency. Translating the surrounding prompt does not authorize translating the image copy.
- Separate edits from preservation constraints. Assign each reference image a numbered role.
- Keep simple prompts short; use sections only when complexity warrants them. Avoid filler quality claims and unrelated platform syntax.

API settings are not prompt syntax. Omit settings by default. If requested, or necessary for a delivery requirement such as transparency, read the indexed 2.5 Model parameters section and place a short settings note outside the prompt. Never imply that prose alone guarantees a technical output property.

### 5. Check and deliver

Compare the prompt with the original request: no missing requirements, altered copy, unresolved conflicts, or unauthorized creative changes. Confirm the chosen example contributes a relevant instruction pattern and that reference roles and ratio decisions are consistent. Assess the prompt only; do not claim to have tested a generated image.

Default output:
1. One code block containing only the copyable final prompt, in the user's requested language.
2. A short assumption or settings note only when needed.
3. One short source note outside the code block naming the selected official section(s) and linking the guide, for example: “Pattern: Transfer a visual style.” If no example matched, name “Prompting fundamentals” instead. Disclose an unverified fallback when applicable.

Do not add long explanations, scores, multiple variants, or bilingual duplicates unless requested. For “prompt only,” omit optional commentary but do not conceal failed source verification.

## Maintenance validation

Use [references/acceptance-cases.md](references/acceptance-cases.md) after changes. These are original behavioral checks, not copied official examples.
