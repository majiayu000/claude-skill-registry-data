---
name: document-authoring
description: Use to create or update document artifacts such as READMEs, developer guides, Markdown, agent Instructions and Skills, specifications, features, ADRs, OpenAPI, and JSON Schema. Covers reader needs, content planning, drafting, editing, examples, maintenance, formats, sources, and Markdown quality. Do not use solely to discover acceptance conditions without producing documents, summarize existing documents, or explain concepts.
---

# Author useful documents with OKF

Create documents within the requested purpose and publication scope. `docs/` below refers to the working repository; `references/` refers to this skill's bundled resources.

## Application and reference material

- Follow the target repository's language conventions when writing documentation, including Markdown and feature documents.
- Author ordinary Markdown and feature documents in OKF v0.2. Preserve specific formats for GitHub Issue and PR bodies and comments, agent instruction files, Agent Skills `SKILL.md`, and contract documents such as OpenAPI and JSON Schema; do not add OKF frontmatter where the target format does not call for it.
- When creating or updating Instructions, Skills, or their task references, read [Separate execution guidance from maintainer notes](references/agent-documents.md). Keep execution rules at their entry points, load operational detail only when needed, and put provenance and maintenance-only supplements in human-facing `docs/` material.
- For reader-facing technical prose, including READMEs, guides, reference explanations, and contributor instructions, read [Developer documentation practices](references/technical-writing.md). Apply its reader, content-type, drafting, and editing guidance to the changed scope; spelling or metadata corrections do not require a new documentation plan or walkthrough.
- When creating or updating requirements, external contracts, acceptance conditions, design decisions, Engineering Policies, or ADRs, read [Clarifying specifications with existing documents](references/specification.md), first checking authoritative existing features, ADRs, and API specifications.
- When choosing where to record design information, write effective guidance in documents, historical judgments in self-contained PRs/commits, and Why-not constraints beside code. Code expresses behavior and tests express contracts. For current policy prose, read [Current policy authoring](references/engineering-policies.md) and respect existing document placement.
- When creating or updating OKF documents, read [Basic format and references](references/basic-format.md). Check exceptions for indexes/history and ordinary concepts, Bundle boundaries, and link resolution.
- For documents relying on external material, updates to sourced documents, or judgments about trust, freshness, or status, read [Provenance, trust, and lifecycle](references/provenance.md). Preserve existing sources, unknown metadata, and checking history even for minor corrections; when separating agent guidance, preserve its provenance in the maintainer note.
- When handling computation definitions or checking methods, read [Attested Computation](references/computation.md). Do not introduce computation contracts merely because a document contains numbers.

## Scope and completion

Before repository document changes, reuse a saved and verified Issue plan or record the purpose, scope, success conditions, and validation. Retrieve the saved body, check agreement and display, and present its URL. Distinguish plan saving from execution approval; a clear change request supplies approval for its scope without requiring repeated confirmation.

For unpublished information, confirm permission for only necessary parts and the posting destination and draft. Do not request the same publication permission again for published facts or saved and verified plans.

- For Issue planning alone, stop after saving, retrieving, checking, and presenting the plan. Issue-body, comment-only, and PR-body-only updates do not authorize repository edits or merging. Preserve existing content and verify each saved update against its formatted body.
- For approved repository documents, check repository instructions, diffs/worktrees, and required main checks; protect other sessions' work and prepare a task branch before editing. Continue through commits, push, a draft PR, required CI, conflict resolution, ordinary latest-HEAD review, and the permitted squash or merge-commit method. Preserve required approvals and the final PR title/body verbatim; do not bypass protections or use rebase merging. Confirm actual-main checks, synchronize, and clean up the task branch. Honor explicit stopping points.
- Use English [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) titles for Issues and PRs; follow repository language and templates for bodies. Keep decisions understandable without following links, include actual validation status, and remove HTML comments from published descriptions. Applying this commit convention to Issue/PR titles is a local writing policy.
- Continue changes to steps or files within the approved purpose and success conditions. Confirm changed purpose, outcomes, acceptance conditions, external impact, or authority before dependent work. Do not require code TDD for documents alone.

If required access or tooling is unavailable, retain the approved scope and saved plan, present drafts and unverified work, and report what is needed to resume. Failed or unobtainable checks are not success; prioritize recovery of failing main before ordinary subsequent changes.

## Creation and update process

1. Check readers, their existing knowledge, the task or decision the document supports, and observable success conditions. Use available evidence rather than inventing user research. Check authoritative sources, model boundaries, and existing terminology. Use `docs/` as the default Knowledge Bundle, and explicitly state the root when handling another distribution unit.
2. Determine whether the target is an ordinary concept, reserved file, or specific format. Read existing content and frontmatter before making diffs; do not drop unknown keys or sources through regeneration.
3. Use one concept per file for ordinary concepts, and include `type`. Also include the recommended `title` and `description` for concepts authored in this environment. Do not call this extra condition a mandatory OKF conformance requirement.
4. Choose the content type and outline around the reader's task, then draft and edit using [Developer documentation practices](references/technical-writing.md). Apply only relevant techniques to specialized formats and preserve their contracts. Reuse the existing plan and document structure where they fit.
5. Record `sources` and stable-ID claim footnotes in externally grounded human-facing documents. For agent execution guidance, preserve that mapping in maintainer notes under [Agent-document separation](references/agent-documents.md). Keep operational lookup links and required attribution where needed. Do not substitute navigation links for evidence or remove citations required in the resulting user artifact.
6. Determine whether changes are meaningful or only spelling/formatting, and update only actual confirmed generation/checking facts. Do not invent dates, human checks, or expiration dates, or claim old checks verify updated content.
7. Perform [Document quality checks](references/validation.md), separately reporting Markdown results, content checking, warnings for unverified or expired items, and checks that cannot run.

## Placement and content

- Add documents to existing categories appropriate to their purpose. Current policy has no prescribed directory or document name; use discoverable topical documents. Behavior documents use `docs/behavior/`; other guidance follows existing repository conventions.
- Create new categories only when existing ones do not fit. Do not uniformly add indexes or history files to every directory.
- Write `*.feature.md` with OKF frontmatter and Markdown with Gherkin under [Feature documents](references/specification.md#feature-documents).
- Link bundled material through file-relative links for viewing on GitHub and through APM. Record external sources as complete URLs, without assuming the original repository exists at the installation destination.
- Do not use external assets such as images that cannot be included in Markdown. This is this environment's authoring policy, not an OKF conformance condition.
- Use headings, lists, tables, and code blocks to show structure needed for decisions. Do not create empty sections or decorative tables.

## Document quality checks

Before publication, read [Markdown and content checks](references/validation.md), and format/check with rumdl. Validate specific formats such as OpenAPI and JSON Schema according to each format.

Do not turn successful format checks into evidence of source truth, human content review, or executed computations. Also compare categories, terminology, links, commands, final diffs, and content, and distinguish unverified, expired, and unexecutable items.
