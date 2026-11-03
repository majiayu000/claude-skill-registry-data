---
name: write-readme
description: Use when creating, improving, translating, restructuring, or reviewing repository README files. Trigger for full README drafts, GitHub homepage polish, bilingual README work, screenshots/previews, install or usage sections, release/download links, contribution/license sections, and small README.md diff edits such as project names, release URLs, installer filenames, badges, or command updates.
---

# Write Readme

## Purpose

Create README files that read like mature GitHub project home pages: clear title, short value proposition, fast path to usage, scannable highlights, accurate install commands, and a predictable lower section for release, contribution, license, and contact details.

## Trigger Discipline

Use this skill even when the README change looks incidental. A README title rename, product-name sync, installer filename update, release URL change, install command update, or `README.md` entry in a staged/unstaged diff is enough to trigger a README quality pass.

Do not treat README edits as mere release plumbing. If the README is touched, check whether the surrounding structure still reads well on GitHub.

## Workflow

1. Read the existing README, package metadata, docs, release notes, screenshots, and obvious entry files before rewriting.
2. Identify the repo's audience, project type, platform, install path, primary workflow, and whether the README should be bilingual.
3. Choose a structure that matches the project:
   - Library/framework: summary, install, quick example, documentation, examples, contributing, license.
   - App/tool: summary, preview, features, install/download, usage, FAQ, development, license.
   - Skill/plugin: purpose, trigger examples, workflow, bundled resources, installation, validation, contact.
4. Start with a clear title and one-line summary, add a compact badge row near the top, then give a short feature or highlight list.
5. Add a quick-start or usage path early enough that a reader can try the project without hunting.
6. Show a preview or screenshot early when visual assets exist.
7. Put release, download, or installer links in a dedicated section near the end unless the user explicitly wants them upfront.
8. Finish with FAQ, development, contribution, acknowledgements, license, and contact only when they add value or the repo already has those commitments.
9. If a centered brand header is appropriate but no real logo asset exists, tell the user the README needs a logo and ask for one before inventing or generating a placeholder.
10. If the user wants GitHub statistic badges, resolve `OWNER/REPO` from `git remote -v`, package metadata, homepage links, or existing README links before writing badges. If it cannot be resolved, remind the user to provide the GitHub repository path.
11. If the user wants tech stack badges, infer the stack from real project files such as `package.json`, `pnpm-lock.yaml`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, `*.csproj`, `Dockerfile`, CI files, or existing docs. If the stack cannot be confirmed, ask for it.

## High-Star README Patterns

Use `references/readme-blueprint.md` when drafting or restructuring a full README. It summarizes patterns from high-star repositories such as React, Next.js, Vite, and shadcn/ui:

- State what the project is in the first screen.
- Include a compact badge row in every README by default. At minimum, use a verified Markdown format badge; add project-specific badges only when their facts and destinations are confirmed.
- For branded projects, consider a centered hero header: logo, project name, one-line summary, and a compact badge/action row before the first section.
- For GitHub stats, use dynamic shields.io badges for stars, forks, issues, pull requests, release/version, license, downloads, or supported platforms when the repo slug is known.
- For technology stacks, add a compact badge strip for confirmed languages, frameworks, runtimes, package managers, databases, cloud services, or platforms.
- Prefer a small set of strong highlights over a long feature dump.
- Put installation and first-use commands in copy-ready code blocks.
- Link to docs, examples, community, contribution, security, and license sections where relevant.
- Keep maintenance and governance information near the bottom.

## Style Rules

- Mirror the feel of `Clash Verge`-style READMEs: language switcher first, preview early, release info later, and a clean section hierarchy.
- Use plain Markdown links for navigation and downloads. Include badges by default unless the user explicitly requests a badge-free README.
- Start the badge row with a factual Markdown format badge, for example: `![Markdown](https://img.shields.io/badge/format-Markdown-000000?logo=markdown&logoColor=white)`. When verified, add dynamic repository statistics, license, release, platform, or technology badges that link to the relevant page.
- Keep download links near the bottom when the user prefers that layout.
- If the project is bilingual, either split the README into parallel Chinese/English sections or provide separate `README_zh.md` and `README_en.md` files with a small top switcher.
- Keep the prose concise, concrete, and copy-ready. Do not over-explain.
- Avoid promotional clutter unless the user explicitly asks for it.
- Do not invent package names, install commands, license names, download URLs, metrics, or screenshots. Use repo evidence, ask briefly, or leave a clear placeholder.
- Preserve user-provided wording, contact details, and asset placement exactly when they specify them.
- Use HTML only for Markdown features GitHub supports well, such as centered images or fixed-width previews.
- Use a Next.js-style centered header when the user asks for that look: `<p align="center">` logo, `<h1 align="center">`, summary paragraph, then a centered badge row.
- Do not create a Next.js-style logo area with a fake, generic, or temporary logo. If no logo is present, remind the user to provide one.
- Do not hard-code fake GitHub counts. Use dynamic shields.io endpoints such as `/github/stars/OWNER/REPO`, `/github/forks/OWNER/REPO`, `/github/issues/OWNER/REPO`, and `/github/issues-pr/OWNER/REPO`.
- Prefer a compact centered badge strip for the "BongoCat style" the user likes; text links alone are not enough when they ask for synced stars or repository stats.
- Do not invent technology stack badges. Use badges only for technologies confirmed by repo files, docs, or explicit user input.

## Structure Template

Use this order when the user wants a full README draft:

```markdown
# Title
Language links
Short summary
Preview
Features
Installation / Usage
Download / Release
FAQ
Development
Contribution
Acknowledgements
License
```

## Output Expectations

- Return a complete README draft in Markdown.
- Rewrite existing README text instead of only commenting on it.
- Keep the final result ready to paste into GitHub with minimal cleanup.
- If important details are missing, make the smallest sensible assumption and list those assumptions separately.
- For repo edits, update the actual README file and any referenced local assets together.
