---
name: output-presentation
description: Apply a Kami-inspired editorial visual system to self-contained HTML after the secretary selects that output route.
license: MIT
compatibility: opencode
---

# Output Presentation

Apply this skill only after the secretary has selected HTML, or when the user explicitly requests Kami or editorial formatting. Do not use it for short Markdown or chat-only responses.

This skill defines presentation only. It does not decide whether HTML should be used, write or save files, open a browser, or return delivery status. Those actions belong to the secretary agent's core workflow. Language rewriting is outside this skill's scope.

## Design direction

Create a Kami-inspired, content-first paper document rather than a dashboard or marketing page. The result must be self-contained and require no network access or external resources.

- Use warm parchment `#f5f4ed` for the canvas.
- Use ivory `#faf9f5` or `#fffdf6` for the paper surface.
- Use ink blue `#1B365D` as the only strong emphasis color. Keep all other colors warm, quiet, and subordinate.
- Use serif-first fallback font stacks that work without downloaded fonts. Provide practical system fallbacks for Chinese and Latin text.
- Use moderate spacing, comfortable line height, readable measure, and clear hierarchy. Avoid both cramped density and theatrical whitespace.
- Use restrained borders plus ring or whisper shadows. Avoid heavy shadows, glassmorphism, flashy gradients, decorative animation, and effects that compete with content.

## Layout and components

- Center the paper in a responsive container with a sensible max-width, fluid side padding, and mobile-safe spacing.
- Use a quiet section rule to separate major parts without turning every section into a panel.
- Use cards only for meaningful summaries, steps, risks, or grouped facts. Keep their surfaces close to ivory and their borders subtle.
- Style quotes with restrained indentation or a thin ink-blue rule; do not make them oversized decorative blocks.
- Make code blocks readable, horizontally scrollable when needed, and visually integrated with the paper palette.
- Make tables responsive, with clear headers, light row rules, aligned values, and horizontal scrolling on narrow screens.
- Present metrics with strong typographic hierarchy rather than dashboard chrome.
- Use compact tags sparingly for real categories or states, not as decoration.
- Add a table of contents, comparison layout, or collapsible details only when document length and structure justify it.

## Self-contained constraints

Keep CSS and any essential presentation behavior inline in the document. Do not use CDNs, remote fonts, remote images, network requests, analytics, cookies, storage, redirects, or automatic downloads.

## Reference

The visual direction is inspired by Kami: https://github.com/tw93/Kami. This skill is a compact, self-contained adaptation, not a copy of the upstream project.
