---
name: social-science-literature-triage
description: Use for the search-planning stage of a literature review, when database lanes and language layers must be chosen, when DOI coverage policy is unclear, or when inclusion and exclusion criteria need drafting before any source is read; not for running the screening and PRISMA pipeline of a formal review, which is prisma-scoping-review-pipeline.
---

# Social Science Literature Triage

## When to use

Use this skill before a literature review, scoping review, thesis chapter, grant background, or manuscript introduction when the user needs a search plan that can survive method review rather than an immediate prose draft. Its protocol feeds regional-access-workflow for retrieval and source-passport-ledger for tracking what the search returns. It is not for running a full PRISMA-compliant systematic review pipeline, that is prisma-scoping-review-pipeline.

## Inputs

- Research question or topic.
- Discipline and population.
- Time window.
- Required languages.
- Preferred databases or regional indexes.
- Inclusion and exclusion criteria, if already known.

## Workflow

1. Restate the research aim in one precise sentence.
2. Classify the evidence need as exploratory, scoping, systematic, narrative, theoretical, or policy-facing.
3. Choose database lanes, such as PubMed, PsycINFO, Scopus, Web of Science, Crossref, Semantic Scholar, DergiPark, ULAKBIM TR Dizin, YOK Thesis Center, HEAL-Link, or institutional library routes.
4. Define language layers, at minimum English, Turkish, and any regional language requested by the user.
5. Build keyword blocks with synonyms, controlled vocabulary where available, and exclusion terms.
6. Specify DOI expectations, including which source types can reasonably lack a DOI.
7. Produce inclusion and exclusion criteria.
8. Identify early bias risks, missing regional sources, database over-reliance, and likely grey literature needs.

## Output

Return a compact protocol with these headings:

- Review aim.
- Evidence type.
- Database lanes.
- Search strings.
- Language strategy.
- DOI and metadata policy.
- Inclusion criteria.
- Exclusion criteria.
- Risk notes.
- Next action.
- What to record at session end: the search protocol file, which database lanes were confirmed available, and a one-line note for the AI-use disclosure.

## Verification

- The protocol names at least two database lanes.
- Regional access is considered when the topic involves Türkiye, Greece, education, public health, clinical psychology, or local policy.
- DOI expectations distinguish journal articles from reports, books, theses, and official guidelines.
- Search strings are reproducible enough for another researcher to run.
- No fabricated source claims are introduced.
- Before closing: the protocol is saved where the next session can find it, and if the topic requires a full systematic review, prisma-scoping-review-pipeline has been flagged as the next step.

## Safety

Do not request passwords, private vault paths, university database credentials, VPN secrets, or raw clinical data. If full-text access requires a logged-in institution, stop at the lawful access workflow and ask the user to retrieve the file through their own authorized route.

## Example prompt

"Scope a Turkish and English literature review on AI-assisted clinical psychology supervision, 2020 to 2026, with DOI discipline and regional database coverage."

Expected smoke output:

- Evidence type, scoping review.
- Database lanes, PubMed, PsycINFO or Scopus, Crossref, DergiPark, TR Dizin, YOK Thesis Center.
- Language strategy, English plus Turkish.
- DOI policy, DOI required for journal articles when available, not required for laws, official guidance, theses, or books.

## Türkçe kullanım notu

Bu beceri, literatür taramasına başlamadan önce yöntem incelemesine dayanacak bir arama planı kurar. Veritabanı kanalları, dil katmanları, DOI beklentileri ve dahil etme ölçütleri tek protokolde toplanır, bölgesel kaynaklar gözden kaçırılmaz. Arama dizgileri başka bir araştırmacının aynı sonuçlara ulaşabileceği kadar açık yazılır, yanlılık riskleri daha ilk adımda not edilir. Plan hazır olduğunda erişim için regional-access-workflow, bulunanların izlenmesi için source-passport-ledger devreye girer. Tam sistematik derleme gerekiyorsa prisma-scoping-review-pipeline'a devredilir. Oturum sonunda arama protokolü ve yapay zekâ katkı notu kaydedilir. Paylaşılan kimlik bilgileri veya kurumsal politika dışı yollarla erişim bu becerinin kapsamı dışındadır — yasal erişim yolları için regional-access-workflow devreye girer.
