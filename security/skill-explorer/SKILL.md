---
name: skill-explorer
description: Discover, security-vet, and install GitHub Copilot skills and extensions from public repositories with explicit provenance, integrity, and risk controls. Use when the user asks to find, compare, inspect, vet, or install a skill or extension.
license: MIT
---

# Skill Explorer

`skill-explorer` is a global skill for finding, security-vetting, and safely installing Copilot skills and extensions from trusted organizations and community repositories.

## Canonical Source

Search the following source first and rank matching entries above other results:

- Catalog: `https://awesome-copilot.github.com/skills/`
- Repository: `https://github.com/github/awesome-copilot/tree/main/skills`

Treat `github/awesome-copilot/skills` as Priority 0. Source priority affects discovery ranking and provenance only; it never bypasses security vetting. Scan every file in the exact selected skill folder before installation and block installation when the risk threshold is met.

## Secondary Source

Always search AI Hero's skills immediately after the canonical source and before all other sources:

- Catalog: `https://www.aihero.dev/skills`
- Repository: `https://github.com/mattpocock/skills`

Treat `mattpocock/skills` as Priority 1. Vet the exact selected skill folder before installation; source priority never bypasses or discounts security findings.

## Open Agent Skills Discovery

Use the open agent skills ecosystem as the first broad discovery source after the canonical and AI Hero catalogs:

- Check the [skills.sh leaderboard](https://skills.sh/) for popular matching skills.
- If the CLI is available, search with `npx skills find [query]` or `npx skills find [query] --owner <owner>`.
- Use the result's source, skill name, install count, repository stars, and skills.sh URL as discovery metadata.
- Deduplicate entries already discovered from Priority 0 or Priority 1.
- Leaderboard position, install count, audit badge, and search ranking are discovery metadata, not security approval.
- Resolve and vet the exact upstream skill folder before installation.
- Do not request or store registry or Vercel OIDC credentials.
- Never use `npx skills add` as the installation step. It bypasses this skill's revision, digest, risk-threshold, and confirmation controls.

## Capability Overview

This skill leverages the `skill-explorer` extension tools:

These tools are provided by the companion `skill-explorer` extension. If the extension is not installed or a tool is unavailable, explain the limitation and do not pretend that a search, vet, or installation operation completed.

1. **Search**: `skill_explorer_search`
   - Search `github/awesome-copilot/skills` first, `mattpocock/skills` second, then the open agent skills ecosystem (`skills.sh` and `npx skills find`), followed by official (`github`, `copilot-extensions`, `microsoft`), configured trusted, and community repos.
2. **Vet**: `skill_explorer_vet`
   - Run static analysis and produce a structured review covering purpose, benefits, trust-requiring capabilities, suspicious indicators, limitations, verdict, ratings, `sourceRevision` (40-char SHA), and `contentDigest` (`sha256`).
3. **Install**: `skill_explorer_install`
   - Vet and atomically install skills into global (`user`) scope (`~/.copilot/extensions/` or `~/.agents/skills/`) or `project` scope (`.github/extensions/` or `.github/skills/`).
   - Requires `expectedRevision` (40-char SHA) and `expectedDigest` (`sha256`) matching the vetting result. Re-resolves content at revision, checks byte equality, and automatically blocks installation if the risk score exceeds threshold (default: 50/100).
4. **Sync**: `skill_explorer_sync`
   - Re-vet and synchronize explicitly selected tracked installations. Requires explicit approval and replaces different local content only when `replaceExisting` is true.
5. **Configure**: `skill_explorer_configure`
   - View and update trusted organizations, whitelist repos, and risk threshold settings (`~/.copilot/skill-explorer-config.json`).
6. **Trending**: `skill_explorer_trending`
   - List skills ranked by `skills.sh` for `Trending (24h)`, `Hot`, or `All-time installs`.
   - Keep trend rank separate from source priority and security status.

## Chat UX

Use native interactive cards and questions:

- After a search, render the returned `chatUx.items` with the `inbox` widget. Cards must show skill name, description, source link, trust tier, and `Not vetted` status.
- Present cards before asking what to do next. Never dump raw search JSON when cards can be rendered.
- Cards are for browsing and opening source links. Use `ask_user` for actions because the native inbox widget does not expose custom Vet/Install buttons.
- Never label an action only `Open source`; this can be confused with open-source licensing. Use `View source code on GitHub (no install)` and explain that it opens the repository for manual inspection without downloading, installing, or executing the skill.
- Every decision requiring user acceptance must use `ask_user`; never ask for acceptance in plain chat text.
- Ask one question at a time. Prefer choices, with the recommended safe action first.
- Do not infer approval from a prior request, URL, card click, or conversational wording.

## Workflow Steps

### Searching for Skills
When requested to find skills for a domain or tool (e.g. Jira, Docker, Postgres):
- Call `discover_widgets` if the `inbox` schema has not been loaded in the current session.
- Render an `inbox` loading state before searching.
- Call `skill_explorer_search(query="...", source="all")`.
- When the user is looking for an existing capability, also use the open agent skills workflow: inspect `https://skills.sh/`, then run `npx skills find [query]` when available.
- Present install counts, source repository, repository stars, and the skills.sh link as discovery metadata only.
- Render the returned `chatUx.items` as interactive `inbox` cards.
- Open the `skill-shortlist` canvas with `chatUx.shortlistCanvas.input` to show each candidate's `View source`, `Request details`, `Request vetting`, and `Request install` controls.
- When `Fetch more skills` is used, retain the existing shortlist and append only new candidates to that same canvas; do not replace it or open a second shortlist.
- Treat `Request install` as an installation request only: vet the exact source, present revision/digest/risk details, and collect explicit confirmation before installation.
- Prefer Priority 0 canonical matches over all other sources.
- Prefer Priority 1 AI Hero matches over every source except Priority 0 canonical matches.
- Prefer Priority 2 Agent Skills Directory matches over all remaining sources, but never treat directory presence as trust or vetting.
- Omit previously installed skills when their recorded source revision and content digest still match upstream; retain changed skills with an update status. Treat installs without Skill Explorer metadata as unknown rather than synchronized.
- Ask: `Which skill should I vet?` with visible result names as choices. Include `Cancel` when appropriate.
- Resolve the selected result to its exact repository and skill directory before vetting; do not install directly from a registry result.

### Listing Trending Skills
When asked for trending, popular, hot, or widely installed skills:
- Render an `inbox` loading state.
- Call `skill_explorer_trending(period="trending24h")`; use `hot` or `alltime` only when requested.
- Render the returned `chatUx.items` as interactive cards.
- Show both the registry trend rank and source-priority badge. Do not reorder the registry trend list by source priority.
- State that trending reflects registry activity/popularity, not security approval or endorsement.
- Ask `Which trending skill should I vet?` with visible result names as choices.
- Resolve and vet the exact skill folder before offering installation. Trending status never bypasses vetting.

### Vetting Skills Before Installation
Before installing any remote skill:
- Call `skill_explorer_vet(repoOrUrl="owner/repo")`, a nested shorthand path such as `mattpocock/skills/skills/engineering/code-review`, or a full GitHub tree URL; pass the exact skill folder rather than the repository root.
- Review findings summary, risk score, `sourceRevision`, and `contentDigest`.
- For canonical skills, vet only the exact `skills/<name>/` folder rather than the entire `awesome-copilot` repository.
- Canonical provenance must not suppress findings, reduce the score, or bypass a block.
- Present a concise review before asking what to do next. The review must include:
  - **What it does**: plain-language purpose and intended workflow.
  - **Why it may help**: concrete benefits and suitable use cases.
  - **Revision & Digest**: exact 40-char SHA (`sourceRevision`) and sha256 (`contentDigest`).
  - **Capabilities requiring trust**: shell, network, credential, filesystem, or repository access.
  - **Suspicious or malicious indicators**: exact evidence, file/line, severity, and whether it appears executable, contextual, or defensive.
  - **Ratings**: overall, utility, clarity, safety, and provenance, each out of 10.
  - **Verdict** and static-review limitations.
- Keep the security risk score (`0–100`, higher is riskier) separate from the review rating (`0–10`, higher is better).
- Explain the rating methodology: utility 30%, clarity 25%, safety 35%, provenance 10%; popularity must not improve the rating.
- Never describe a skill as proven safe. Use `no suspicious indicators detected` and disclose static-analysis limitations.
- Update the selected card's status to `Vetted: Safe`, `Vetted: Review`, or `Blocked`, with the corresponding semantic status variant.
- If safe, ask what to do next with choices: `Install globally (Recommended)`, `Install in current project`, `View source code on GitHub (no install)`, `Cancel`.
- If blocked, ask what to do next with safe choices only: `View security findings (Recommended)`, `View source code on GitHub (no install)`, `Search again`, `Cancel`.
- When the source-view choice is selected, navigate to or provide the exact source URL and state: `This only opens the source for manual inspection; it does not download, install, or execute anything.`

### Installing Skills
- Ask a final confirmation question containing the exact skill name, source, chosen scope, expectedRevision (40-char SHA), expectedDigest (sha256), and vetting result.
- Only after explicit approval, call `skill_explorer_install` with:
  - `userConfirmed`: `true`
  - `confirmationSummary`: exact summary text
  - `expectedRevision`: 40-character commit SHA from vetting
  - `expectedDigest`: `sha256:...` digest string from vetting
  - `repoOrUrl` & `scope`
- If blocked by risk threshold or digest mismatch, do not install. Report the error.
- Run `extensions_reload()` to activate newly installed extensions/skills.
- Update the card to `Installed` after successful installation.
