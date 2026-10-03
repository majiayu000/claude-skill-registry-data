---
name: write-readme-header
description: Create or revise README opening headers with a centered HTML block containing a project icon, H1 title, bold one-line tagline, and language navigation, including a complete Simplified Chinese counterpart when README.md exists but README.zh_CN.md is missing. Use when Codex needs to polish a README introduction, reproduce a GugleFS-style centered masthead, standardize bilingual README files, add README branding, or complete a missing Simplified Chinese README translation.
---

# Write README Header

Create a compact, repository-native README masthead while preserving the existing document body.

## Workflow

1. Inspect every existing README variant and relevant project metadata.
2. Identify the canonical project name, a concise one-line value proposition, an existing repository icon, and the English/Simplified Chinese language pair.
3. If `README.md` exists but `README.zh_CN.md` is missing, create the Chinese file as a complete translation. Preserve commands, code, URLs, identifiers, filenames, configuration keys, and technical meaning.
4. Replace or insert the opening masthead in both files. Preserve existing body content except for the translation needed to create a missing counterpart or broader copy changes requested by the user.
5. Verify that local image and language links resolve, both HTML blocks close, section coverage remains aligned, and the raw Markdown remains readable.

## Header Format

Use this structure:

```html
<div align="center">

<img src="path/to/icon.png" width="256" height="256" alt="Project icon">

# Project Name

**A concise project value proposition.**

English | [简体中文](README.zh_CN.md)

</div>
```

Keep one blank line between each element. Use repository-relative paths with `/` separators. Prefer an existing tracked square icon; do not invent a broken path or add a remote image without approval. Omit the image row when no suitable asset exists and image creation is outside the request.

## Language Navigation

Maintain a complete Simplified Chinese counterpart for `README.md` by default. When the English file exists but the Chinese file is missing, translate the full document before adding navigation. Do not create a header-only translation stub. Render the current language as plain text and the other language as a link:

```markdown
English | [简体中文](README.zh_CN.md)
[English](README.md) | 简体中文
```

Use `README.md` for English and `README.zh_CN.md` for Simplified Chinese unless the repository already establishes another naming convention. Localize headings, prose, tagline, image alt text, captions, and explanatory comments while preserving executable and machine-readable content.

## Content Rules

- Use the repository's canonical capitalization for the H1.
- Write a concrete tagline that states what the project does; keep it to one sentence and avoid unsupported slogans.
- Do not add badges, installation commands, feature lists, or marketing copy inside the centered block unless requested.
- Replace an existing opening masthead as a unit instead of nesting another `<div>` around it.
- Keep translated section order and coverage aligned with the source README so neither language silently loses operational details.
- Check `git diff` after editing so changes below the opening section are intentional.
