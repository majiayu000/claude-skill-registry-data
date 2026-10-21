---
name: github-repo-launch-polish
description: Turn a code repository into a discoverable, star-ready open-source project. Use when a repo has a bare README, no license, no screenshots, or no topics — or when an existing README is already well-written and only needs exposure elements (badges, license, English section, star CTA) added without rewriting the author's voice. Not for code changes, feature work, or a full rewrite the author did not ask for.
version: 1.0.1
---

# GitHub Repo Launch Polish

A repo with good code and a bare README gets no stars. Exposure on GitHub comes from search metadata (description, topics, English keywords) and from a README that proves the project works in five seconds.

## Two Modes — Pick First

**Mode A: bare or weak README.** Rebuild using the README Anatomy below.

**Mode B: README already well-written** (author's voice, honest metrics, real detail). Do NOT rewrite it — rewriting erases the voice that makes it credible. Only add exposure elements, surgically:

1. Badge block right after the H1 (live demo, license, one fact badge like "14/14 tests passing").
2. An `## English` summary section before the license/closing section.
3. A one-line star CTA in a centered div at the very bottom.
4. `LICENSE` file if missing.
5. If the README lacks an online demo link but Pages is enabled, check the root tree for `index.html` and add the Pages URL.

Everything else stays byte-identical. The diff should read as "additions only".

## README Anatomy (in order, for Mode A)

1. **Centered hero**: name, one-line slogan, what it is in one sentence, badges (live demo, license, stack, PRs welcome via shields.io `for-the-badge` style), quick nav links.
2. **Live demo link** in the hero and again in quick start. A clickable product beats any description.
3. **Screenshot table**: desktop and mobile side by side, real captures of the product's best screen and its differentiating feature. Use the `headless-webapp-screenshots` skill to produce them.
4. **What/why**: the pain point in two sentences, then the one thing this project does differently.
5. **The differentiator with a diagram**: an ASCII flow of the core mechanism (pipeline, state machine, data flow). This is what gets quoted.
6. **Features, quick start, tech stack, project structure, roadmap, contributing.**
7. **English summary section**: one paragraph + demo link. GitHub search and most readers index on English; a Chinese-only README is invisible internationally.
8. **Star call-to-action** at the bottom, one line, centered.

## Batch Polishing Several Repos

When polishing an owner's whole account:

1. List all repos first (`search_repositories user:<name>`, non-minimal output) and record for each: has license, has topics, has homepage, star count, Pages enabled. Skip nothing silently.
2. Do not forget the **profile README repo** (`<user>/<user>`) — it is the highest-traffic page on the account. Add new projects to its list and keep counts (number of skills, number of repos) in sync with reality.
3. One commit per repo (README + LICENSE together), then hand the owner a single consolidated list of manual About/description/topics/website edits — connector tools cannot set them.
4. When a description or README states a count ("4 skills", "five repos"), flag every place that count appears; adding a project invalidates all of them at once.

## Repository Metadata (manual, 2 minutes)

MCP/GitHub connectors used for file pushes cannot set these; do them in the web UI and never skip them:

- **About description**: one sentence, front-load English keywords (`AI daily planner with LLM output evaluation`), then Chinese.
- **Website**: tick "Use your GitHub Pages website" when Pages is enabled.
- **Topics**: 8-10 tags mixing domain and stack, e.g. `ai-agent` `llm` `evaluation` `productivity` `vanilla-javascript` `pwa`. Topics are how GitHub search surfaces small repos.

## License

Add a `LICENSE` file (MIT for personal portfolio projects, copyright line = GitHub username + year). No license means "all rights reserved" — many people will not star or fork.

## Publishing Files — Known Limitation

Text files push fine through connector/Contents-API style tools. **Binary files (PNG, GIF, fonts) do not**: the content string is stored as-is, so base64 text lands in the repo as literal text and the image is broken. Verified behavior — do not retry it.

- Push binaries via real Git transport, or drag the folder into the repo's web upload UI (`/upload/main`).
- If a probe was used to test behavior, delete probe files afterwards (`docs/.probe.txt`, `docs/_probe.png` style leftovers make a repo look sloppy).
- After pushing README references to images, open the repo page and confirm every image renders.

## Final Checklist

- [ ] README renders with zero broken images or badge links
- [ ] LICENSE present and linked from README
- [ ] About description + website + topics set
- [ ] Live demo link works from a logged-out / incognito browser
- [ ] Profile README repo updated (new projects listed, counts in sync)
- [ ] No secrets, personal data, employer names, or internal URLs anywhere in the tree (grep for them)

## Example

A repo whose README already reads well. Mode B, five surgical additions:

1. Add four badges under the title (skills count, license, runtime dependency, privacy).
2. Add a one-line value proposition in bold, before the existing prose.
3. Add a scenario index, ten lines of "I want X -> use Y".
4. Fill About: one sentence of description plus topics.
5. Append a star and issue call to action.

Nothing in the author's own wording is rewritten.
