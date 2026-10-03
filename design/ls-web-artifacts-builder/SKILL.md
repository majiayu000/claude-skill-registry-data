---
name: ls-web-artifacts-builder
description: Guide creation of rich HTML/React web artifacts. Use for self-contained
  interactive artifacts, prototypes, dashboards, and visual demos.
metadata:
  version: '1.0'
extensions:
  external_skill:
    source_kind: native-reference
    source_url: https://github.com/anthropics/skills
    source_path: skills/web-artifacts-builder/SKILL.md
    source_commit: 9d2f1ae187231d8199c64b5b762e1bdf2244733d
    source_ref: main
    source_sha256: 81c5002c6643b0de7b8710b00e7a9038daa6fb9b68d59870ee6adb12da8d10f8
    license: NO_REPO_LICENSE_FOUND
    import_date: '2026-07-03'
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Web Artifacts

Use this skill when working on web artifacts tasks.

## Workflow

- Choose the simplest artifact shape that satisfies the interaction: static HTML, vanilla JS, or React only when state complexity warrants it.
- Keep artifacts self-contained, accessible, responsive, and free of secrets or live credentials.
- Test rendered output in a browser or Playwright when layout, interaction, or canvas behavior matters.
- For design-heavy work, use image generation only as a concept aid: create candidate visuals, ask the user which direction to implement, then treat the accepted design as the implementation spec.
- Extract the accepted design into concrete system decisions: layout grid, hierarchy, typography, color roles, spacing, component states, imagery, and interaction details.
- Implement faithfully against those decisions, cross-routing to `ls-frontend-design` for visual direction and `ls-ui-browser-debugging` for screenshot evidence.
- Compare desktop and mobile browser screenshots against the accepted concept, then adjust layout, spacing, contrast, and responsive behavior before claiming visual parity.

## Boundaries

- Inspect the target repository before making changes.
- Prefer existing project patterns, declared package managers, and documented validation commands.
- Do not expose secrets, credentials, private user data, or production account identifiers in source, examples, or logs.
- When external APIs or current vendor behavior matter, verify against official docs before implementation.
- For OpenAI image generation workflows, verify current API behavior against:
  - https://developers.openai.com/api/docs/guides/image-generation
  - https://developers.openai.com/api/reference/resources/images


## License Boundary

The upstream repository snapshot did not expose a top-level license file during this run. This skill is LocalSetup-native guidance and does not copy upstream body text or bundled assets.

## Provenance

- Source: `https://github.com/anthropics/skills`
- Ref: `main` at `9d2f1ae187231d8199c64b5b762e1bdf2244733d`
- Source path: `skills/web-artifacts-builder/SKILL.md`
- License classification: `NO_REPO_LICENSE_FOUND`
- Source SHA-256: `81c5002c6643b0de7b8710b00e7a9038daa6fb9b68d59870ee6adb12da8d10f8`
