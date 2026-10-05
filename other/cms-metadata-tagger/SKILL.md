---
name: cms-metadata-tagger
description: "Takes a finished piece of content and produces a complete, archive-ready metadata record — including descriptive tags, subject classifications, rights notes, and an archival summary — for entry into a content management or digital archive system."
status: stable
category: archive-legal
subcategory: publishing
version: 1.0
eval_score: 4.2
tags: [cms, metadata, archive, tagging, content management, finished piece, publishing]
---
# CMS Metadata Tagger

## What This Skill Does
Takes a finished piece of content and produces a complete, archive-ready metadata record — including descriptive tags, subject classifications, rights notes, and an archival summary — for entry into a content management or digital archive system.

## When To Use This Skill
- A piece has been published and needs to be formally archived with consistent metadata for long-term retrieval
- Your archive team is cataloguing a backlog of published content and needs metadata generated at volume
- You are migrating content between systems and need a metadata record that works for the destination archive structure
- A piece contains legally sensitive elements (third-party images, named individuals, licensed data) and needs rights and restrictions noted in the archive record before the file is stored

## What You Need To Provide
**Required:**
- The full text or a detailed summary of the finished piece
- Content type (news article, feature, opinion column, video script, audio transcript, photo essay, social post series)
- Publication date

**Optional:**
- Named individuals, organisations, or locations that must appear in the record
- Rights or licensing information (image credits, wire service content, licensed data sources)
- Any restrictions on reuse (e.g. "not for republication", "interview subject requested anonymity in byline", "embargoed material — cleared for archive only")
- Your archive's controlled vocabulary or subject taxonomy — paste it so the assistant uses your terms rather than its own
- Internal reference number or file ID if you want it included in the record

## How the Assistant Approaches This
1. Reads the content and extracts the primary subject, secondary subjects, named entities (people, places, organisations, events), and content format. Notes any elements with potential rights or legal implications mentioned in what you provide.
2. Drafts a short archival summary (distinct from a publish-facing standfirst) written for internal retrieval — factual, dateline-style, without promotional language.
3. Assembles the full metadata record in a field-by-field format. If a controlled vocabulary was provided, all subject tags are drawn from it. Rights and restriction fields are populated with whatever you have supplied; if none was supplied, the field is flagged as requiring manual entry rather than left blank silently.

## Output Format
A structured metadata record with one clearly labelled field per line. Fields are:

```
Content type: ...
Publication date: ...
Archival summary: ... (2–3 sentences, factual, past tense)
Primary subject: ...
Secondary subjects: ..., ..., ...
Named people: ..., ...
Named organisations: ..., ...
Named locations: ..., ...
Tags: ..., ..., ..., ...
Rights: ...
Restrictions: ...
Internal reference: ... (if provided)
```

Fields with no available information are marked `[REQUIRES MANUAL ENTRY]` rather than left blank. No markdown formatting inside field values. Output is ready to paste directly into an archive system's form fields.

## Quality Criteria
- [ ] Archival summary is factual and dateline-accurate — no editorialising, no superlatives
- [ ] Named entities (people, organisations, locations) are complete and correctly separated into their respective fields
- [ ] Rights field is populated with what was provided, or clearly flagged for manual follow-up
- [ ] Restrictions field is populated if any reuse limitation was mentioned, or clearly flagged
- [ ] Tags are specific enough to distinguish this piece from other pieces on the same general topic
- [ ] If a controlled vocabulary was provided, all subject terms appear verbatim in that vocabulary
- [ ] No field is silently blank — every field has a value or an explicit flag

## Example

### Input
Content type: Feature article
Publication date: 14 February 2025
Text summary: A long-form investigation into the use of facial recognition technology by private landlords in residential buildings across three major cities. The piece profiles three tenants who discovered cameras in building lobbies linked to commercial facial recognition databases, and interviews a privacy lawyer, a property management consultant, and a civil liberties researcher. Quotes from named individuals throughout. Primary photography by the publication's staff photographer — all rights held. Statistics sourced from a government housing agency's annual report (public domain). No embargo; published in full.
Internal reference: FEA-2025-0214-007

### Output
Content type: Feature article
Publication date: 14 February 2025
Archival summary: An investigative feature examining the deployment of facial recognition technology by private landlords in residential buildings across three unnamed cities. Three tenants describe discovering cameras linked to commercial identification databases in their building lobbies. The piece includes interviews with a privacy lawyer, a property management consultant, and a civil liberties researcher.
Primary subject: Facial recognition technology
Secondary subjects: Tenant rights, Housing, Privacy law, Surveillance, Property management
Named people: [REQUIRES MANUAL ENTRY — named individuals present in text; verify byline and anonymisation preferences before finalising]
Named organisations: [REQUIRES MANUAL ENTRY — property management companies named in text; confirm publication policy on naming]
Named locations: [REQUIRES MANUAL ENTRY — cities described as unnamed in source material; log internal identifiers if held]
Tags: facial recognition, landlords, residential buildings, tenant surveillance, privacy, civil liberties, housing law, investigation
Rights: Photography — all rights held by publication. Statistical data — government housing agency annual report (public domain). Text — all rights held by publication.
Restrictions: None. Published in full with no embargo. No anonymisation of journalists. Verify anonymisation status of tenant sources before any republication.
Internal reference: FEA-2025-0214-007

## Known Limitations
- The assistant works only from the information you provide. If rights or restrictions are not mentioned in your input, the skill will flag those fields for manual entry — it will not invent or assume rights status. Always verify rights information before the archive record is finalised.
- Named individuals require careful handling. If any source was granted anonymity, this skill will flag the people field for manual review rather than auto-populate it, to avoid inadvertently creating a discoverable record linking a real person to a sensitive piece.
- Subject tagging without a provided controlled vocabulary produces useful but non-standardised terms. For archives requiring strict taxonomy compliance, always supply your controlled vocabulary list.
- This skill produces a metadata record, not a legal clearance. It is not a substitute for your organisation's rights or legal review process.

## Related Skills
- [cms-fields-writer](../cms-fields-writer/SKILL.md)
- [asset-description-writer](../../production-support/formatting/asset-description-writer/SKILL.md)
