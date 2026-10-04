---
name: weixin-article-to-obsidian
description: Use when saving a Weixin Official Account article from mp.weixin.qq.com into an Obsidian vault as Markdown with locally downloaded images and vault-style asset links.
---

# Weixin Article to Obsidian

## Overview

Capture a Weixin Official Account article into an Obsidian vault with local image assets. Prefer `opencli weixin download` for the initial article fetch, then verify and supplement the result by parsing the page source for picture-page images and article metadata.

## When to Use

Use this skill when the user:
- Provides an `mp.weixin.qq.com` article URL
- Wants the article body saved as a Markdown note in an Obsidian vault
- Wants article images downloaded locally instead of referenced from remote CDN URLs
- Wants Obsidian image links such as `![[assets/title/image.png]]`
- Wants a repeatable workflow for Weixin article clipping

## Do not use

Do not use this skill when:
- The URL is not a Weixin Official Account article
- The user only wants a visual theme extracted from the article
- The user wants to publish Markdown back to Weixin
- The target is not a local Markdown or Obsidian knowledge base

## Instructions

1. Read the target vault guidance first, especially directory rules, asset rules, and index maintenance rules.
2. Choose the semantic note directory from the article topic. Do not default to a generic clipping folder when the vault has a more specific category.
3. Run `opencli weixin download` if available:

```bash
opencli weixin download --url "https://mp.weixin.qq.com/s/example" --output /tmp/weixin-article --download-images true -f yaml
```

4. If `opencli` misses images, or if the article is a picture-page article, run the bundled script:

```bash
python3 scripts/download_weixin_article.py "https://mp.weixin.qq.com/s/example" \
  --vault-root /path/to/obsidian-vault \
  --target-dir "FrontEnd/security"
```

5. Review the generated Markdown and remove platform chrome, duplicated metadata, recommendation blocks, or reward prompts if any remain.
6. Verify every image reference is an Obsidian vault link pointing under `assets/<note-title>/`.
7. If the vault requires topical indexes, update the local index page with a wiki link to the new note.

## Script Behavior

`scripts/download_weixin_article.py`:
- Attempts `opencli weixin download` first and reuses its Markdown body when it is complete enough
- Fetches the article HTML directly as a fallback or supplement
- Extracts title, account name, publish time, description/body text, and picture-page image URLs
- Downloads images into `assets/<safe-title>/`
- Writes a Markdown note into the requested `--target-dir`
- Emits a JSON summary with the note path, asset directory, image count, and whether `opencli` ran

Important options:
- `--vault-root`: Obsidian vault root. Defaults to the current working directory.
- `--target-dir`: Relative note directory inside the vault. Defaults to the vault root.
- `--title`: Override the extracted title and asset folder name.
- `--locale`: Use `zh` or `en` metadata labels. Defaults to `zh`.
- `--overwrite`: Replace an existing Markdown note with the same title.

## Output Rules

- Save Markdown under the chosen content directory.
- Save images under `assets/<note-title>/`, relative to the vault root.
- Use Obsidian image syntax, not regular Markdown image syntax.
- Keep the source URL as a short metadata line unless the user asks to remove it.
- Do not add YAML frontmatter unless the vault already requires it.

## Validation Checklist

- The note exists in the selected directory.
- The asset folder exists and contains all expected article images.
- `rg "mmbiz|data:image|http" <note>` only shows the source URL, not remote image links.
- Image links render as `![[assets/...]]`.
- The topical index is updated when required by the vault.
