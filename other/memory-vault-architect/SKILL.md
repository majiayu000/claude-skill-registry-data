---
name: memory-vault-architect
description: Use when a research note system needs architecture, when MOCs, frontmatter standards, and retrieval patterns must be designed for years of work, or when an existing vault has outgrown its structure and must migrate without breaking years of links.
---

# Memory Vault Architect

## When to use

Use this skill when the user needs an academic memory system that can survive multiple projects, long time horizons, bilingual notes, and repeated AI-assisted work. The source records it designs are maintained day to day through source-passport-ledger, and research-ritual-hooks automates the rituals that keep the vault alive. It is not for auditing whether sensitive participant data has been adequately anonymized before entering the vault, that is sensitive-data-anonymization-gate.

## Inputs

- Research domains.
- Active projects.
- Source types.
- Preferred note tool, if any.
- Required languages.
- Collaboration and privacy constraints.
- Retrieval goals.

## Workflow

1. Identify the vault's purpose, such as literature review, manuscript pipeline, clinical training, teaching, or grant work.
2. Separate durable knowledge, active projects, source records, daily work, and archived material.
3. Design MOCs for domains, projects, methods, people, institutions, and outputs.
4. Define frontmatter fields for source passports, project notes, meeting notes, and synthesis notes.
5. Specify retrieval patterns, including tags, aliases, backlinks, saved searches, and index notes.
6. Define rules for AI-generated notes, human-reviewed notes, and uncertain claims.
7. Provide a migration plan that avoids reorganizing everything at once.

## Output

Return:

- Vault objective.
- Folder architecture.
- MOC map.
- Frontmatter schemas.
- Source passport template.
- Retrieval pattern.
- Migration steps.
- Maintenance ritual.
- What to record at session end: the folder map decided, any MOC or frontmatter schemas created, and a handoff note naming the sensitive data lanes that need sensitive-data-anonymization-gate before population.

## Verification

- The architecture separates sources from interpretations.
- The system works without relying on a single proprietary tool.
- AI-generated content is visibly marked until reviewed.
- Sensitive clinical or participant material has a protected lane.
- The migration plan is small enough to execute.
- Before closing: the source passport template is ready to hand to source-passport-ledger for day-to-day record keeping, and any protected lane is documented so sensitive material cannot be accidentally placed in an open folder.

## Safety

Do not ask for private vault paths, credentials, raw clinical data, or participant identifiers. Use placeholder paths and anonymized examples unless the user explicitly provides safe local paths.

## Example prompt

"Design a bilingual research vault for AI and mental health papers, manuscript drafts, Zotero notes, and reviewer response materials."

Expected smoke output:

- Folder map.
- MOC list.
- Source passport frontmatter.
- Retrieval rules for sources, claims, and manuscript outputs.

## Türkçe kullanım notu

Bu beceri, yıllarca yaşayacak bir araştırma arşivinin mimarisini kurar. Kalıcı bilgi, aktif projeler, kaynak kayıtları ve günlük çalışma birbirinden ayrılır, MOC haritaları ve frontmatter şemaları geri çağırmayı tek aramaya indirir. Günlük işleyiş source-passport-ledger ve research-ritual-hooks becerileriyle yürür. Taşınma planı küçük adımlarla ilerler, her şeyi bir günde yeniden düzenlemeyi girişimde bulunulmaz. Hassas katmanlar arşive girmeden önce sensitive-data-anonymization-gate üzerinden geçirilir. Yapay zekâ tarafından üretilen notlar, insan incelemesinden geçene dek kasıtlı biçimde işaretlenir — arşiv içinde yapay zekâ katkısının görünür kalması bu etiketlemeye dayanır.
