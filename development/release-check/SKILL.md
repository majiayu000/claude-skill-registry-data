---
name: release-check
description: Use for final verification before commit, merge, PR review, or release readiness checks, especially after content, workflow, nav, layout, or JavaScript changes.
---

# Release Check

## Article Release Gate

When an article is part of the change, this is a release audit of the complete article package, not just a command checklist and not just the latest diff hunk.

Reconstruct the intended release from the owner request, the final Japanese source, and the relevant ADR. Then read the applicable article skills again and verify the whole result:

- Content: read the final Japanese article end to end; check its structure, claims, links, media, and instructions. Fact-check claims that depend on models, nodes, or upstream behavior.
- Workflows: verify every documented workflow exists, is valid, remains reproducible, and matches the article, screenshots, models, and measured data.
- Localization: when EN/ZH are in scope, compare each complete page with the Japanese source. Preserve all sections, media, links, code, workflow shortcodes, options, and measurements. Inspect the rendered pages for locale-correct layout and component strings, including visible labels, tooltips, popups, status text, and accessible names. Matching source counts alone are not evidence of parity.
- Publication surface: for a new localized article, verify the matching nav entries, ADR scope, and one news row for every language whose page exists.

Do not declare the article ready or publish it while any applicable part of this package is unchecked. Report what was checked and anything intentionally left out.

## Baseline

Always start with:

```bash
git status --short --branch
git diff --check
```

## Standard Checks

- Content/nav/workflow changes: `npm run check`
- Site generation: `npm run build`
- UI, search, notes, nav, form, client JS, or layout changes: `npm run test:playwright`

## Notes

- `npm run build` failing on media that is not in `src/_data/media.json` is expected **only before the commit** — the pre-commit `media:sync` registers it. Once committed, the build has to pass; a still-failing build is a real failure, not the draft state. Never hand-edit `media.json`. See [preview-site](../preview-site/SKILL.md).
- Nav, slug or `ops/ia.md` changes need the dev server restarted before they show up.
- In this environment, Playwright may need approval because Eleventy dev server binds `0.0.0.0`.
- Report checks that were not run and why.
- Do not push or open/update PRs unless the owner explicitly says to do so.

## Pipeline

The last check before publishing in the article pipeline ([article-authoring](../article-authoring/SKILL.md)). Passing these checks is not permission to commit, push, or open a PR.

Next, only on an explicit request: [publish-pr](../publish-pr/SKILL.md).
