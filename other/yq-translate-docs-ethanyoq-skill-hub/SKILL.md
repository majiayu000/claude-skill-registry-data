---
name: yq-translate-docs
description: 维护中英双语文档的语义一致、结构对应和自然表达。
---

# Translate Bilingual Docs

Keep an English and Chinese document pair equivalent without forcing either language into the other's sentence structure. Use the repository's own localization contract; do not import another project's filenames, sidecars, manifests, or validation rules.

This skill is explicit-only. Use it when the user invokes `$yq-translate-docs` to translate, synchronize, reconcile, rename, or audit bilingual documentation. It covers maintained documentation such as READMEs, guides, release notes, and website pages. Source-code locale dictionaries follow the project's application-i18n workflow unless the user includes them.

While this explicitly invoked workflow is active, apply [`$yq-technical-writing`](../yq-technical-writing/SKILL.md) to both languages so every source proposition survives in natural prose. Before a user-authorized push or readiness claim, invoke `$yq-pre-push-checks` once for the outgoing change set; do not run it per document or infer permission to commit or push.

## Discover the pair contract

Before editing, read the applicable repository instructions and determine:

- the default document, its counterpart, and any legacy alias or redirect;
- whether either side is generated, frozen, or owned by another source;
- the glossary, terminology table, style sample, link policy, and locale-specific assets already used by the project;
- existing localization, link, rendering, or documentation checks.

Either language may be the authored side for a change. Product facts come from current code, configuration, release evidence, or another declared owner; neither language automatically overrides those sources.

## Classify the change

- **Update:** one side changed. Translate only the changed semantic units and preserve reviewed wording outside that diff.
- **New pair:** no counterpart exists. Translate the whole document in sections, keeping the source structure visible as work progresses.
- **Both sides changed:** compare both sides with their common base and reconcile each changed unit. Preserve independent valid updates instead of choosing one language for the whole file.
- **Rename or delete:** move or remove the counterpart and repair navigation, language switches, and inbound links according to repository policy.
- **Alias or redirect:** preserve its routing role. Do not expand a deliberate compatibility stub into a second maintained translation.

## Update an existing pair

Use the current diff, merge base, or repository pairing record to identify what changed. Translate the smallest complete semantic unit that carries the change: a paragraph, list item, table row, heading section, or whole document only when smaller alignment is unsafe.

Preserve meaning clause by clause:

- keep obligations, exceptions, limitations, numbers, platform support, release names, and failure behavior equivalent;
- follow the project's established terminology and introduce an unresolved term explicitly rather than inventing a silent translation;
- keep commands, code spans, identifiers, URLs, and file names exact unless the repository deliberately localizes them;
- keep headings, lists, tables, code blocks, and link targets structurally corresponding, but do not require physical line-count equality;
- allow language-specific screenshots, alt text, examples, and search wording when they serve the same documented fact and audience.

Write natural target-language prose first, then compare it with the source clause by clause. Literal sentence transposition is not fidelity when it produces awkward or misleading text.

## Create or reconcile a complete pair

For a new counterpart, translate section by section and read the completed target alone before the final source comparison. For divergent existing files, establish the owner of each changed claim, merge compatible additions, and report unresolved factual conflicts rather than translating one conflict into the other language.

Do not copy stale facts merely to make both sides match. Repair the owning fact first when authorized; otherwise mark the discrepancy and the evidence needed to resolve it.

## Validate without adding process

Run only the repository's existing relevant checks, such as localized README tests, link checks, documentation rendering, or an established pairing verifier. If no such check exists, compare headings, code blocks, commands, links, assets, version claims, limitations, and language switches manually.

Do not create a sidecar, hash record, translation manifest, line-count rule, test, script, or CI gate merely because the project has a bilingual pair. Add process only when the user separately requests it or the repository already requires it.

Report the pair and authored side, units translated or reconciled, terminology decisions, deliberate locale-specific differences, unresolved conflicts, and checks actually run.
