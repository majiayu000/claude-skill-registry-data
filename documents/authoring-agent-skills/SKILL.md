---
name: authoring-agent-skills
description: Use when creating, adding, or maintaining a skill in this agent-skills repo — especially a "working-with-X" skill that wraps external/official docs by fetching them (llms.txt, sitemap, or a curated URL list), storing them in references/, and keeping them current with an auto-update script plus freshness metadata. Covers the naming taxonomy (working-with-X / developing-X / topic skills), SKILL.md frontmatter, the doc-fetching cookbook, the doc-frontmatter.cjs freshness helpers, the Makefile/CI auto-discovery, and the registration checklist. Invoke on "create a skill", "add a working-with-X skill", "wrap these docs in a skill", "write an auto-update script", "add freshness metadata", or "add a skill to this repo".
metadata:
  last_updated: "2026-08-12"
---

# Authoring Agent Skills

## Overview

This skill encodes **this repo's** conventions for building skills — the patterns that have worked well across ~20 existing skills. It is the playbook for adding a new skill that an agent can follow end-to-end without reverse-engineering the existing ones.

It is **repo-specific** and complements the generic skill tooling rather than replacing it:

- Use `skill-creator` (or `superpowers:writing-skills`) for **generic** skill quality — description wording, triggering accuracy, progressive disclosure, evals.
- Use **this** skill for the **agent-skills conventions** — naming taxonomy, the doc-fetching + freshness pipeline, the shared `doc-frontmatter.cjs` helper, Makefile/CI auto-discovery, and what to update when registering a new skill.

The biggest, most distinctive convention here is the **doc-wrapping `working-with-X` skill**: fetch a tool's official docs into `references/`, stamp each file with `source`/`fetched_at`/`sha256`, and let a weekly GitHub Action keep them current. If that's what you're building, the [doc-fetching cookbook](references/doc-fetching-cookbook.md) and [freshness metadata](references/freshness-metadata.md) references are the heart of the job.

## When to use

- Creating any new skill in `skills/` in this repo.
- Specifically wrapping an external tool/library's docs into a `working-with-X` skill with an auto-update script.
- Adding or fixing freshness metadata (`source`/`fetched_at`/`sha256`, `metadata.last_updated`).
- Registering a skill (AGENTS.md table, README, Makefile target, version bump).
- Deciding which archetype a new skill should be and how to name it.

## Quick reference

| Need to… | Read this |
| --- | --- |
| Pick an archetype, name the skill, lay out the directory, write SKILL.md frontmatter | [`references/naming-and-structure.md`](references/naming-and-structure.md) |
| Write the auto-update fetch script (llms.txt / sitemap / curated-list patterns) | [`references/doc-fetching-cookbook.md`](references/doc-fetching-cookbook.md) |
| Wrap a **locally-installed** tool (not just a hosted API/library) — live inspection, event schemas, retention limits | [`references/local-tool-inspection.md`](references/local-tool-inspection.md) |
| Wire freshness signals (`doc-frontmatter.cjs` API, change-detection, backfill) | [`references/freshness-metadata.md`](references/freshness-metadata.md) |
| Register the skill so it's discoverable and shippable | [`references/registration-checklist.md`](references/registration-checklist.md) |

## Naming taxonomy (the short version)

Three archetypes — pick the one that matches the skill's job. Full detail, directory layouts, and frontmatter spec are in [`references/naming-and-structure.md`](references/naming-and-structure.md).

- **`working-with-X`** — wraps the **external/official docs** for a tool or library X (Claude Code, Codex, the Vercel AI SDK, GitHub Actions). `references/` is **auto-fetched** by a script in `scripts/` and carries per-doc freshness frontmatter. This is the archetype the fetch/freshness pipeline is built for.
- **`developing-X`** — the **workflow/lifecycle** for *building plugins or extensions for* platform X (developing Claude Code / Codex / Cursor / Gemini plugins). `references/` is **hand-written** (patterns, structure, troubleshooting), no fetch script. Cross-references the matching `working-with-X` for official docs.
- **Topic / capability skills** — a domain or capability, not a single tool: `agent-instructions`, `domain-driven-design`, `web-research`, `git-github-workflows`. Hand-written `references/`, no fetch script.

> This skill itself is a topic skill — it wraps no external docs and ships **no** fetch script.

## Authoring workflow

Track these with TodoWrite when building a real skill.

1. **Decide archetype & name.** Match one of the three archetypes above. Name = kebab-case, directory name == `name:` in frontmatter. See [naming-and-structure](references/naming-and-structure.md).
2. **Scaffold `SKILL.md`.** Frontmatter (`name`, trigger-rich `description`, `metadata.last_updated`) + body (overview, when-to-use, quick-reference table pointing at `references/`, behavioral guidance). Mirror the shape of [`skills/developing-claude-code-plugins/SKILL.md`](../developing-claude-code-plugins/SKILL.md) (workflow-style) or [`skills/working-with-vercel-ai-sdk/SKILL.md`](../working-with-vercel-ai-sdk/SKILL.md) (doc-wrapper style).
3. **(Doc-wrappers only) Write the fetch script.** `skills/<name>/scripts/update_docs.js` (or `update.js`/`update.sh`). Choose a discovery pattern — llms.txt, sitemap, or curated list — from the [cookbook](references/doc-fetching-cookbook.md). Output to `skills/<name>/references/`.
4. **(Doc-wrappers only) Wire freshness.** Import `withFrontmatter` + `setSkillLastUpdated` from `scripts/lib/doc-frontmatter.cjs`, wrap each written doc, track `wrapped.changed`, restamp `SKILL.md` only when something changed. See [freshness-metadata](references/freshness-metadata.md).
5. **Register the skill.** Update `AGENTS.md` (Available Skills table + Common Workflows), `README.md`, add a named `update-<name>` Makefile target (doc-wrappers only), and bump the plugin version. Full list in [registration-checklist](references/registration-checklist.md).
6. **Verify.** `make list-update-scripts` (confirm discovery), `make update-<name>` (doc-wrappers — confirm it fetches and stamps), and check that every `references/*.md` path the SKILL.md links to actually exists.

## Canonical examples (real paths to copy from)

- **Sitemap fetch + slug-collision handling** — [`skills/working-with-vercel-ai-sdk/`](../working-with-vercel-ai-sdk/) ([`scripts/update_docs.js`](../working-with-vercel-ai-sdk/scripts/update_docs.js))
- **llms.txt fetch** — [`skills/working-with-claude-code/`](../working-with-claude-code/) ([`scripts/update_docs.js`](../working-with-claude-code/scripts/update_docs.js))
- **Curated list + HTML→Markdown + manifest (ESM)** — [`skills/devcontainers/`](../devcontainers/) ([`scripts/update.js`](../devcontainers/scripts/update.js))
- **`developing-X` shape (workflow skill)** — [`skills/developing-claude-code-plugins/`](../developing-claude-code-plugins/)
- **Freshness exception (merged upstreams, hand-curated)** — [`skills/working-with-pieces/`](../working-with-pieces/)
- **Shared freshness helper** — [`scripts/lib/doc-frontmatter.cjs`](../../scripts/lib/doc-frontmatter.cjs)

## Cross-references

- `skill-creator` / `superpowers:writing-skills` — generic skill description quality, triggering, and progressive disclosure.
- `agent-skills:agent-instructions` (`references/editing-discipline.md`) — RED-GREEN discipline for *editing* an existing `SKILL.md` or runbook, as opposed to authoring a new one.
- `marketplace-publishing` — version bump rules and official-marketplace submission once the skill is registered.
- Repo conventions also summarized in [`AGENTS.md`](../../AGENTS.md) ("Auto-generated docs convention" and "Freshness metadata convention").
