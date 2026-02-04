---
name: adjust-behandeling-content
description: Adjust or rewrite behandeling (treatment) content pages for the Nuxt Content site. Use when a user provides new copy or asks to update `content/behandelingen/*.md`, including frontmatter, content blocks, or treatment descriptions. Focus on content edits; only touch routing/navigation or composables when a change clearly requires it.
---

# Adjust Behandeling Content

## Overview
Update treatment pages stored in `content/behandelingen/*.md`. Keep the frontmatter and content blocks valid for Nuxt Content and the existing page components, and preserve the database-linked `id` in the hero block unless the user provides a new one.

## Workflow
1. Identify the treatment slug/filename from the user's request. If missing, ask for it or infer from the treatment name and confirm.
2. Open the matching file under `content/behandelingen/` and keep the overall structure.
3. Update frontmatter (`title`, `description`) and the content blocks to match the provided copy.
4. Preserve or update `::behandeling-hero` fields:
   - Keep `id` unchanged unless the user supplies a new UUID.
   - Update `description` when the summary changes.
5. Validate block syntax:
   - Use kebab-case component names.
   - Use `:::` for nested blocks inside `::twee-kolommen`.
6. Check images:
   - Paths should be `/images/<file>.webp` and exist in `public/images/`.
   - If a new image is required but not provided, request it.
7. Only adjust routing/navigation/composables if the change explicitly needs it (for example, a slug rename). Otherwise keep edits limited to content.

## Example Prompts (Dutch)
- "Hier is nieuwe tekst voor behandeling Chakra Healing; pas de pagina aan en houd de structuur hetzelfde."
- "Update de voordelen en 'Voor Wie'-lijst voor ontspanningsmassage. Gebruik deze bullets: ..."
- "Vervang de intro en sectietekst van behandeling X; de titel en beschrijving moeten korter en duidelijker."

## References
- For content structure and components: see `references/content-structure.md`.
- For page wiring and data flow: see `references/page-wiring.md`.
- For the full admin/content guide: `docs/BEHANDELINGEN_BEHEREN.md`.
