---
name: rseng-fact-checking
description: >-
  Covers verifying facts and sources at the content level: checking that a
  cited source actually contains and supports the claim it is cited for
  (claim-source alignment), assessing source trustworthiness (peer-review
  status, venue reputation, predatory-publishing signals, primary vs
  secondary), and flagging fabricated or misattributed support. Use
  PROACTIVELY whenever the agent itself asserts checkable facts or attaches
  sources to claims, and when the user asks to fact-check a document, verify
  that references support their claims, or assess whether a source is
  trustworthy. (rseng-citation-hygiene verifies references exist and are
  unretracted; rseng-research-integrity checks a document's own numbers.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Fact-checking and source verification

A reference can exist, resolve and be unretracted - and still not
say what it is cited for. That last mile is where fabrication
actually lives: real papers attached to claims they do not
support, secondary sources laundered as primary, numbers that
drifted in retelling. rseng-citation-hygiene verifies that
references EXIST and are current; this skill verifies that they
SUPPORT their claims and deserve trust. The duty is
self-referential and stated plainly: an agent that asserts a fact
or attaches a source must be prepared to show where in the source
the support lives - and must say "I could not verify this" when it
cannot. Confidence is not evidence.

## Claim-source alignment: the core check

For each claim-citation pair:

1. Extract what the claim actually asserts: the specific finding,
   number, method or position attributed to the source - not the
   general topic. Most misattribution hides in specificity ("X
   causes Y" cited to a paper showing correlation; "widely used"
   cited to a paper that merely mentions).
2. Open the source and FIND the support: the abstract often
   suffices for existence of a finding (OpenAlex serves
   abstracts); exact numbers, conditions and caveats need the
   relevant section. Record WHERE the support is (section, table)
   - unfindable support is the finding.
3. Grade the alignment honestly: supports as stated / supports
   with caveats the text drops / related but does not support /
   contradicts / cannot access to verify. The middle grades
   matter most - dropped caveats ("in mice", "n=12", "simulated
   data") are the commonest integrity leak
   (rseng-research-integrity's spirit applied to prose).
4. Check the chain: if the source itself cites something for the
   claim, it is a secondary source - prefer citing the primary
   after checking IT (citation chains degrade like photocopies;
   "as cited in" is honest when the primary is unreachable).

Batch mode for documents: extract all claim-citation pairs, run
the alignment check per pair, and report a table with grades and
locations - the content-level companion to rseng-citation-hygiene's
existence table, and a natural pre-submission step
(rseng-research-integrity's battery).

## Source trust assessment

Not all resolvable sources deserve citation:

- Status: peer-reviewed publication, preprint (legitimate but
  label it - rseng-open-science-practices), dataset, documentation,
  blog post? Cite the thing appropriate to the claim: software
  behavior -> the docs; a finding -> the paper; never a press
  release for a scientific result.
- Venue signals: is the journal in DOAJ (for open access
  venues), does the publisher follow recognizable review
  practice (Think-Check-Submit's checklist operationalizes
  this)? Predatory-venue signatures: guaranteed fast review,
  fake metrics, scope covering everything. A paper is not wrong
  for appearing in a weak venue - but weight it accordingly and
  prefer stronger support when available.
- Primary vs secondary: for facts, prefer the origin - the
  standard's text (as this pack's own skills link eur-lex and
  specifications), the tool's documentation, the original study.
  Reviews are excellent context and honest citations for
  consensus claims - "reviewed in [X]" - not for specific
  findings.
- Currency: is the source still the state of knowledge? A
  superseded version of a spec or a pre-replication-crisis
  finding may need updating, not just citing
  (rseng-citation-hygiene's preprint-to-published check is the
  mechanical half).

## Verifying facts the agent asserts

The proactive duty, in practice:

- Checkable claims in generated text (numbers, dates, "X supports
  Y", API behavior, legal obligations) get verified against an
  authoritative source before delivery, or labeled as unverified.
  For software claims, the executable check beats the document:
  run the command, read the actual API response
  (rseng-testing's instinct applied to prose).
- Distinguish knowledge from verification in the output when it
  matters: "per the docs at <link>" vs "from memory - verify
  before relying on this". Users calibrate on this honesty.
- When verification is impossible (paywall, offline, no
  authoritative source), say so and mark the claim - an honest
  gap outperforms confident invention every time.
- Everything this pack already mandates applies: verified links
  only (each skill's Learn-more discipline), retraction screening
  (rseng-citation-hygiene), and AI-contribution disclosure
  (rseng-ai-declaration) for documents the agent helped write.

## Working with this skill

This skill is source-independent: it encodes claim-source
verification practice, with the linked services as the checking
infrastructure. It completes the verification chain:
rseng-citation-hygiene (the reference is real) -> this skill (the
reference supports the claim, and deserves to) ->
rseng-research-integrity (the document's own numbers are
consistent).

Learn more (verified):
  - https://help.openalex.org - OpenAlex (metadata and abstracts
    for alignment checks)
  - https://api.crossref.org/swagger-ui/index.html - Crossref
    REST API
  - https://doaj.org - Directory of Open Access Journals
  - https://thinkchecksubmit.org - Think. Check. Submit. venue
    checklist
  - https://gitlab.com/crossref/retraction-watch-data -
    Retraction Watch database

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-citation-hygiene - existence check runs first
- rseng-documentation - README claims need the same bar
- rseng-honesty - when asked to fake support
- rseng-open-science-practices - preprint status labeling
- rseng-research-integrity - document-level pre-submission battery
- rseng-testing - executable checks beat document claims

<!-- related-skills:end -->
