---
name: law-mvt-research
description: >
  Searches for Memorie van Toelichting (explanatory memoranda) for a Dutch law
  and generates Gherkin test scenarios from legislature-intended examples.
  Use this skill proactively when: user wants MvT-derived BDD scenarios,
  mentions "memorie van toelichting", "MvT", "parlementaire stukken",
  "rekenvoorbeelden", or "kamerstukken" in the context of Dutch law.
  Activate automatically when a new law YAML file is created and the user
  discusses testing or validation.
allowed-tools: Read, Write, Bash, WebSearch, WebFetch, Grep, Glob
user-invocable: true
---

# Law MvT Research — Find Parliamentary Examples and Generate Gherkin Scenarios

Searches for Memorie van Toelichting documents and converts legislature-intended
examples into Gherkin acceptance tests.

## Setup

1. Read the target law YAML file to extract `bwb_id`, title, and `valid_from`.
   Note its directory: scenarios live beside the law, and you will write there.
2. Read an existing feature file as Gherkin style reference:
   `corpus/regulation/nl/wet/participatiewet/scenarios/bijstand.feature`

## Step 1: Find MvT Documents

Extract the `bwb_id` (e.g., `BWBR0018451`) from the law YAML's `bwb_id` field.

Search for related parliamentary documents using the overheid.nl SRU API at
`repository.overheid.nl`. **URL-encode the whole query string** before use.

The most productive search is by **dossiernummer**, which returns the complete
legislative file in one call (bill, MvT, every nota van wijziging, the Eerste
Kamer stukken). Find the dossier number from the title search below, or from the
citation `Kamerstukken II ..., 29 762, nr. 3` if you already have one:

```
https://repository.overheid.nl/sru?operation=searchRetrieve&version=2.0
  &query=(c.product-area==officielepublicaties) and (w.dossiernummer==29762)
  &maximumRecords=100
```

When you do not know the dossier, search by title (`dt.title` is the working
index; `dcterms.title` is not):

```
https://repository.overheid.nl/sru?operation=searchRetrieve&version=2.0
  &query=(c.product-area==officielepublicaties) and (dt.title any "{KEYWORD}")
  &maximumRecords=100
```

Filter the results **by reading `<dcterms:title>`**, not by a type index: the
document kind is written into the title after a semicolon ("…; Memorie van
toelichting", "…; Nota van wijziging"). Filtering on `dt.type` returns zero
records even when matching documents exist, so it silently hides everything.
The fields that carry the useful metadata are `<dcterms:title>`,
`<dcterms:identifier>`, `<dcterms:date>` and `<overheidwetgeving:dossiernummer>`.

Collect all of these, since each may explain a different part of the law:
- **Memorie van toelichting** (explanatory memorandum)
- **Nota naar aanleiding van het verslag** (response to parliamentary report)
- **Nota van wijziging** (amendment note)
- **Brief van de minister** (ministerial letter with examples)

There may be **multiple MvT documents** (original + amendments). Collect all of them.

**Do not use `zoekservice.overheid.nl/sru/Search`.** That host now rejects every
`x-connection` value except `cvdr` and `bwb`, answering anything else with SRU
diagnostic `info:srw/diagnostic/1/6` ("Unsupported parameter value"). It also has
no `dcterms.references` index, so a BWB-id search cannot be made to work there.

**Error handling:** If a search returns no results:
1. Try the alternate query (dossier number vs title, or vice versa)
2. Try broadening the title query (use fewer keywords)
3. Try WebSearch as a fallback (e.g., search for `site:zoek.officielebekendmakingen.nl memorie van toelichting {law_title}`)
4. If all searches fail, report "No MvT documents found" and proceed — this is not an error

## Step 2: Download and Read MvT Content

For each found document, extract the document identifier from the search results.
The `<dcterms:identifier>` field contains the document identifier, but its format
varies. It may be:
- A full URI: `https://identifier.overheid.nl/BWBR/sgd/kst-36450-3`
- A prefixed path: `/sgd/kst-36450-3`
- A bare ID: `kst-36450-3`

To extract the document ID: take the **last path segment** (split on `/`, take the
last non-empty part). For example, `kst-36450-3` from any of the above formats.
Then use it to download the HTML version:

```
https://zoek.officielebekendmakingen.nl/{DOCUMENT_ID}.html
```

**Do not use WebFetch for the document body.** WebFetch returns a model's
summary of the page, and a summary cannot be quoted: a paraphrase attributed to
a real parliamentary document is a fabricated citation, and this corpus is
published. Download the raw HTML instead and strip the tags yourself:

```bash
curl -s "https://zoek.officielebekendmakingen.nl/{DOCUMENT_ID}.html" -o {DOCUMENT_ID}.html
```

Then extract text locally (tags stripped, entities unescaped, whitespace
collapsed, nothing else). Every sentence you later quote must survive that path
literally. When a passage carries a **table** of worked examples, re-extract the
`<table>` markup cell by cell and reconcile it against the flattened text before
trusting any number: flattening a table can silently misalign rows against
values.

Note the source documents use guillemets («») and non-breaking spaces in
amounts; keep them as they are rather than normalizing them away.

If HTML is too large, focus on sections that contain:
- "voorbeeld" (example)
- "rekenvoorbeeld" (calculation example)
- "casus" (case)
- "scenario"
- "tabel" (table — often contains example calculations)
- "berekening" (calculation)
- "stel dat" (suppose that)
- "in het geval" (in the case of)

## Step 3: Extract Test-Relevant Information

### First: an MvT explains a bill, not necessarily the law

A memorie van toelichting describes the text **as introduced**. Parliament then
amends it. Where a nota van wijziging changed a provision, the original MvT
explains a rule that never entered into force, and mining it for scenarios
imports the opposite of legislative intent.

This is not a rare edge case. In the Wet op de zorgtoeslag the original MvT
(`kst-29762-3`) works out an example giving a verzekerde with a non-insured
partner a zorgtoeslag of **zero**. The nota van wijziging (`kst-29762-18`) calls
exactly that outcome "niet evenwichtig" and replaces it with the fifty-percent
rule that is in the law today. An agent reading only the MvT would encode the
abandoned design as the legislature's intention.

So, before using any passage:

1. Read **every** nota van wijziging in the dossier, not just the MvT.
2. Compare the article text the MvT explains with the article text in the corpus
   YAML. Where the wording differs, the MvT is describing something else.
3. Where the two conflict, the later document wins, and say so explicitly in the
   output rather than silently preferring one.
4. Percentages, amounts and thresholds in an old MvT are almost always stale.
   Use them to check the **shape** of a calculation, never as expected values.

A later amending MvT (a subsequent bill touching the same law) often restates
the enacted rule more cleanly than the original, and postdates the amendments.
Prefer it for a plain statement of how the article works.

### Then, from the MvT content, extract:

1. **Rekenvoorbeelden** (calculation examples):
   - Input values used by the legislature
   - Expected output values
   - Step-by-step calculations shown

2. **Concrete scenario's** (concrete scenarios):
   - Described situations with specific parameters
   - Expected outcomes stated by the legislature

3. **Randgevallen** (edge cases):
   - Boundary conditions explicitly discussed
   - Special cases the legislature considered

4. **Bedoelde uitkomsten** (intended outcomes):
   - "De bedoeling is dat..." (the intention is that...)
   - "Dit betekent dat een persoon die..." (this means that a person who...)

For each extracted example, note:
- Which article(s) it relates to
- The input parameters and their values
- The expected output/result
- The source document and page/section reference

## Step 4: Generate Gherkin Feature File

Write the `.feature` file **beside the law it tests**, in a `scenarios/`
directory next to the law YAML:

```
corpus/regulation/nl/wet/participatiewet/2025-01-01.yaml
corpus/regulation/nl/wet/participatiewet/scenarios/bijstand.feature
```

So the path is `{directory of the law YAML}/scenarios/{topic}.feature`. Create
the `scenarios/` directory if it does not exist yet.

`{topic}` names the subject the scenarios cover, not the law — the law is
already the directory. `bijstand.feature` under `participatiewet/`,
`eligibility.feature` under `wet_op_de_zorgtoeslag/`, `bezwaartermijn.feature`
under `vreemdelingenwet_2000/`. Do NOT use the full `$id` or the BWB ID as the
filename.

There is no top-level `features/` directory, and writing to one would silently
do nothing: the BDD runner
(`packages/engine/tests/bdd/main.rs`) collects `*.feature` from exactly two
places — any `scenarios/` directory under `corpus/regulation/` (bucket A, law
validation) and `bdd/conformance/` (bucket B, engine conformance). A file
anywhere else is never executed, while `just bdd` still reports green.

Follow the existing project conventions; the five feature files under
`corpus/regulation/**/scenarios/` are the style reference. The Gherkin
vocabulary itself is fixed by `bdd/grammar.yaml` — use steps that exist there.

**Structure:**
```gherkin
Feature: {Law title} — scenarios uit Memorie van Toelichting
  Testscenario's afgeleid uit de Memorie van Toelichting en parlementaire
  stukken bij {law_title}.

  # Bron: {MvT document identifier(s)}
  # URL: {MvT document URL(s)}

  Background:
    Given the calculation date is "{valid_from}"

  # === Rekenvoorbeelden uit MvT ===

  Scenario: {Description from MvT}
    # Bron: {document_id}, {section/page reference}
    Given a citizen with the following data:
      | parameter_1 | value_1 |
      | parameter_2 | value_2 |
    When the {law_execution} is executed for {law_id} article {N}
    Then the {output_name} is "{expected_value}" eurocent

  # === Randgevallen ===

  Scenario: {Edge case from MvT}
    # Bron: {document_id}, {section/page reference}
    ...
```

**Guidelines:**
- Each scenario MUST trace back to a specific MvT passage (add `# Bron:` comments)
- Convert monetary amounts in MvT to eurocent
- Use the same Given/When/Then step patterns as existing feature files
- If MvT examples reference external data sources (RVIG, Belastingdienst, etc.),
  use the appropriate Given steps for those sources
- If the MvT doesn't provide enough examples for a specific article, note this in
  a comment but do NOT invent scenarios — only use what the legislature provided
- Group scenarios by: rekenvoorbeelden, randgevallen, afwijzingsscenario's

## Step 5: Report MvT Findings

Report to the user before proceeding:

```
MvT Research for {LAW_NAME}

  Documents found: {COUNT}
  - {doc_id_1}: {title} ({date})
  - {doc_id_2}: {title} ({date})

  Extracted scenarios: {SCENARIO_COUNT}
  - Rekenvoorbeelden: {N}
  - Randgevallen: {N}
  - Afwijzingsscenario's: {N}

  Feature file: {law directory}/scenarios/{topic}.feature

  Articles without MvT examples: {list}
  Note: No synthetic scenarios were added for these articles.
```

If NO MvT documents are found, report this clearly. The generation phase will
fall back to the JSON-based test approach.
