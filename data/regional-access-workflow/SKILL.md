---
name: regional-access-workflow
description: Use when a source must be reached through DergiPark, ULAKBIM TR Dizin, HEAL-Link, YOK Thesis Center, or an institutional library route, when off-campus access fails, or when a lawful retrieval plan is needed for Turkish, Greek, or European materials.
---

# Regional Access Workflow

## When to use

Use this skill when a researcher needs a lawful and reproducible route to regional academic sources, especially Turkish, Greek, European, university, thesis, or institutional materials. It picks up the search protocol from social-science-literature-triage and writes what it finds into source-passport-ledger entries. It is not for building a systematic PRISMA search log across multiple databases, that is prisma-scoping-review-pipeline.

## Inputs

- Source target or research topic.
- Country, language, or institution scope.
- Known databases.
- Access constraints.
- Whether the user has authorized institutional access.

## Workflow

1. Classify the source need as journal article, thesis, report, guideline, book, dataset, or policy document.
2. Route the search to regional sources such as DergiPark, ULAKBIM TR Dizin, YOK Thesis Center, HEAL-Link, university repositories, or library discovery systems.
3. Route international metadata to Crossref, PubMed, Scopus, Web of Science, Semantic Scholar, or OpenAlex when available.
4. Record access status, metadata status, DOI status, and full-text status separately.
5. Keep login, VPN, and institutional identity steps on the user's side.
6. Produce a source passport entry for each located item.
7. Flag unresolved access problems and lawful next steps.

## Output

Return:

- Access route map.
- Search locations.
- Metadata fields to capture.
- DOI and identifier status.
- Full-text access status.
- Source passport template.
- Manual user actions.
- Blockers and alternatives.
- What to record at session end: the databases searched, each source passport entry created, and any unresolved access blockers with the lawful next step noted.

## Verification

- The workflow never bypasses paywalls, licenses, or institutional access controls.
- DOI absence is not treated as evidence that a source is invalid.
- Regional databases are not replaced by global search alone.
- Full-text status is separated from metadata existence.
- User-side login actions are clearly marked.
- Before closing: all located source passport entries are ready to hand to source-passport-ledger, and any systematic search log is flagged for prisma-scoping-review-pipeline if the review protocol requires it.

## Safety

Do not request or store VPN credentials, library passwords, proxy URLs containing tokens, or institutional session cookies. Do not download full text through unauthorized routes.

## Example prompt

"Find a lawful access workflow for Turkish clinical psychology theses and DergiPark articles on digital addiction."

Expected smoke output:

- YOK Thesis Center, DergiPark, TR Dizin, Crossref, and library discovery lanes.
- A source passport template with access status and DOI status.
- Manual login steps left to the user.

## Türkçe kullanım notu

Bu beceri, bir kaynağa yasal ve tekrarlanabilir bir erişim yolu kurar. Bölgesel diziler, üniversite depoları ve kütüphane keşif sistemleri uluslararası kanallarla birlikte haritalanır, giriş ve VPN adımları her zaman sizde kalır. Açık erişim önce denenir, bulunan her kaynak için bir pasaport kaydı oluşturulur ve erişilemeyen kaynaklar için erişimin mümkün olmadığı açıkça belirtilir.
