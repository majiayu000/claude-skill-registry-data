---
name: external-blog-repost-publisher
description: >-
  Repost external blog articles into StaticFlow with style-aware translation,
  adaptive source normalization, image ingestion, and verified publish updates.
---

# External Blog Repost Publisher

Ingest or update external articles in StaticFlow with source-grounded full-text fidelity,
professional translation, and reproducible publish/verification workflow.

## Companion Skills
- Required: `../staticflow-cli-publisher/SKILL.md`
- Required for translation + summary: `../article-bilingual-translation-publisher/SKILL.md`
- CLI failure recovery: `references/sf-cli-troubleshooting.md`

## Flow Routing

| Task | Flow | File |
|---|---|---|
| Scope and write-back boundaries | A | [flows/scope.md](flows/scope.md) |
| Source normalization (Markdown/HTML/mixed) | B | [flows/source-normalization.md](flows/source-normalization.md) |
| Translation + style adaptation | C | [flows/translation.md](flows/translation.md) |
| Publish + verification | D | [flows/publish-verify.md](flows/publish-verify.md) |

## Non-Negotiable Rules

### Rule 1: Scope lock
Confirm target fields and preservation policy (Flow A) before any write.
Update only in-scope fields; preserve everything else.

### Rule 2: Web-tool-first extraction + best-effort retry
- Use `web.search_query` + `web.open`/`web.click`/`web.find` first; no `curl`/`wget` as primary path.
- When the original page is blocked, incomplete, or renders only a shell, try a Jina Reader mirror form such as `https://r.jina.ai/http://<url>` or `https://r.jina.ai/https://<url>` before refusing.
- Follow Flow B retry and downgrade protocol; single timeout is never enough to refuse.

### Rule 3: Full-text fidelity + source grounding
- `content`/`content_en` must be source article translation/adaptation, not recap/review/commentary.
- `source_canonical_<lang>.md` must come from extracted source evidence, not model memory.
- Do not publish partial/summarized body when full-source extraction is unverified.

### Rule 4: Translation quality
- Preserve facts, examples, caveats, and argument flow.
- Keep target-language output professional and readable.
- See Flow C for detailed translation steps.

### Rule 5: Language policy
- English source → preserve/write `content_en`.
- Chinese import of English source → write both `content` and `content_en`.

### Rule 6: Attribution + date policy
- Reprint notice required with clickable source URL (`[url](url)`).
- Source publication date stays in notice/body text, not as DB `date`.
- Default `articles.date` to local import/publish date; preserve existing on update unless user requests change.

### Rule 7: Taxonomy + summary policy
- Source tags/categories are reference-only; derive from article semantics + local conventions.
- For updates, keep existing taxonomy unless user explicitly puts it in scope.
- Update `detailed_summary.zh/en` by default; skip only when user explicitly asks.

### Rule 8: Link/image normalization + verification
- Rewrite local relative links to valid targets.
- Import images → `images/<id>` unless user allows remote links.
- Always run Flow D checks after write.
- If blocked, provide causal chain + dominant cause label with evidence.
- For `sf-cli` failures, use `references/sf-cli-troubleshooting.md`.

## Workflow

1. Flow A → lock scope (`id`, language fields, overwrite policy).
2. Flow B → produce canonical Markdown from source (best-effort protocol before refusal).
3. Flow C → style-aware translation (when needed).
4. Flow D → publish and verify.
5. Report: changed/preserved fields, fidelity checks, verification result.

## Inputs

Required (at least one): external URL, local Markdown, or local HTML.

Optional: target `article_id`, db path, target language(s), field scope, metadata override.

## Workspace
`/tmp/external_repost/<article_id>/`
