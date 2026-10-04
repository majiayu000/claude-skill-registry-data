---
name: ryan-visual-asset-workflow
description: Use when a project or deliverable needs a generated image asset and the user explicitly allows using the signed-in ChatGPT web experience through ego browser. Keep prompts minimal, bounded, reviewable, and separate image generation from code or publishing.
---

# Ryan Visual Asset Workflow

Use this optional skill when a task genuinely needs a bitmap or other visual asset. Do not trigger it for ordinary process explanations: use Mermaid first for flow, state, sequence, and system relationships.

## Preconditions

- Confirm the asset is needed and define its role, dimensions, format, visual constraints, and acceptance criteria.
- Check whether the brief contains private documents, customer data, internal screenshots, credentials, or unreleased product details.
- If the prompt would disclose sensitive material, stop and ask Ryan to approve the exact disclosure scope or provide a sanitized brief.
- Use one isolated ego-browser task space for the generation goal. Do not use the user's ordinary browser tab.

## Generation Routine

1. Create or claim a task card when the asset is part of cross-session, product, or release work.
2. Prepare a short sanitized prompt. Keep the project name, private URLs, source code, customer data, and internal screenshots out unless explicitly approved.
3. Open a new conversation in the signed-in ChatGPT web page through ego browser.
4. Submit the prompt once. The default budget is one generation request and one bounded refinement; stop after two attempts unless Ryan explicitly changes the budget.
5. Wait for the page result and verify that the generated image is actually available before reporting success.
6. Save or retrieve only the selected asset. Record source, prompt version, dimensions, format, and review status in the local task evidence, not the login state or full browser transcript.
7. Render the asset in the target project and check crop, readability, dimensions, file size, transparency, and obvious privacy or brand risks.
8. Put the task in review. Publishing, sending, uploading to a public service, paid generation, or irreversible replacement requires a HOTS confirmation.

## Failure And Handoff

- Login, MFA, CAPTCHA, blocked download, permission prompt, payment, or public publishing: hand control to Ryan and wait.
- If the same browser operation fails twice, inspect the actual page state and change the hypothesis; do not repeat blindly.
- If the result is visually wrong, make one precise refinement or return to a local placeholder. Do not start an unbounded generation loop.
- If ego browser is unavailable, continue with a placeholder or another explicitly approved provider. The workflow must not depend on ChatGPT web availability.

## Output Contract

Report:

- asset path or explicit reason no asset was saved;
- prompt intent, not private page contents;
- generation attempts and whether the budget was exhausted;
- local render/validation evidence;
- rights, privacy, and brand risks still requiring review;
- whether the asset is ready for acceptance or needs Ryan's decision.

Never record cookies, login state, private page contents, full prompts containing sensitive data, or browser transcripts in Taskboard, Obsidian, MemOS, or a public repository.
