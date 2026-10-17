---
name: chemistry-db-knowledgebase
description: "Chemistry and biochemistry database router: KEGG REST, PubChem, UniProt, NCBI E-utilities, KEGG C, K, R, EC and map IDs. Use to resolve a protein, metabolite or biochemical question, convert IDs across databases, or map metabolomics, spatial metabolomics or RNA-based metabolite predictions. For GATOM modules use gatom-metabolomic-predictions."
license: Apache-2.0
---

# Chemistry Database Knowledgebase

This skill routes a protein, metabolite or biochemical question to the one reference file that
holds the details, and pins the rules every route shares. Read the table, open one reference,
and stay out of the others until the question needs them.

## Prerequisites

1.  **Python 3** with the standard library only. `scripts/kegg_rest.py` has no dependencies.
2.  **User notification.** For each database the first time it is used in a workspace: if
    `.licenses/<database>_LICENSE.txt` does not exist in the workspace root, (1) tell the user to
    check the terms listed in [references/terms-and-limits.md](references/terms-and-limits.md),
    then (2) create the file recording the notification text and a timestamp. `<database>` is
    `kegg`, `pubchem`, `uniprot` or `ncbi`.
3.  **`NCBI_API_KEY`** (optional). It raises NCBI from 3 to 10 requests per second. Read it from
    the environment; never print it or write it into a file.

## Core Rules

-   **Rate limits are hard limits.** KEGG allows 3 calls per second and blocks the address that
    exceeds it. Send every KEGG call through `scripts/kegg_rest.py`, which holds 2.5 calls per
    second across all processes. Other limits are in the table under *Rate limits*.
-   **Answer from tool output.** Every identifier, formula, mass, pathway and annotation in a
    reply comes from an API response in this conversation. When a call returns nothing or an
    error, report that.
-   **Convert with the database that owns the target.** The route for each ID pair is in
    [references/id-conversion.md](references/id-conversion.md). A name or a mass is a query that
    returns candidates; an accession is an identity.
-   **Report ambiguity.** A conversion is one-to-one, one-to-many or empty. Keep every candidate
    and the count; picking the first row of a many-to-one is a claim that needs evidence.
-   **Mouse project defaults.** KEGG organism `mmu`, NCBI taxon `10090`. KEGG `mmu` gene IDs are
    NCBI Gene IDs, so `mmu:11651` is Gene ID 11651.
-   **Notification.** When this skill is used, say which databases answered.

## Routing

| The question | Open |
|---|---|
| Which pathway, reaction, enzyme, module or K number holds this gene or compound; KEGG syntax | [kegg-rest.md](references/kegg-rest.md) |
| What is this chemical: structure, formula, mass, synonyms, bioassays, similarity | [pubchem-pug.md](references/pubchem-pug.md) |
| What is this protein: function, sequence, reviewed entry, ortholog, ID mapping job | [uniprot.md](references/uniprot.md) |
| Gene records, RefSeq sequences, PubMed links, taxonomy | [ncbi-entrez.md](references/ncbi-entrez.md) |
| Convert one identifier type to another | [id-conversion.md](references/id-conversion.md) |
| Annotate metabolomics features or spatial metabolomics ion images with compounds | [metabolomics-mapping.md](references/metabolomics-mapping.md) |
| Read RNA-seq as metabolic reaction or metabolite predictions | [rna-metabolite-prediction.md](references/rna-metabolite-prediction.md) |
| Terms of use, citations, rate limits per service | [terms-and-limits.md](references/terms-and-limits.md) |

## Decision tree

```
What do you hold?
|
|- a gene symbol or Ensembl gene ID
|    |- want the protein ........ uniprot.md  (search gene_exact + organism_id)
|    |- want pathways or K ...... id-conversion.md: gene -> NCBI Gene ID -> kegg-rest.md link
|- a UniProt accession ............ id-conversion.md (KEGG conv uniprot, or UniProt map to KEGG)
|- a compound name ................ pubchem-pug.md resolve  (candidates) -> id-conversion.md
|- a KEGG C number ................ kegg-rest.md get  -> id-conversion.md for CID, ChEBI, InChIKey
|- a K number ..................... kegg-rest.md link ko -> genes, reactions, pathways
|- an m/z or an ion image ......... metabolomics-mapping.md
|- a DE table of enzyme genes ..... rna-metabolite-prediction.md
|- a sequence to fetch ............ ncbi-entrez.md (RefSeq) or uniprot.md (UniProtKB, UniParc)
|- sequence similarity or MSA ..... outside this skill; use a BLAST or alignment tool
```

## Identifier cheat sheet

| Pattern | Namespace | Home database |
|---|---|---|
| `C00031` | KEGG compound | KEGG |
| `D00009` | KEGG drug | KEGG |
| `G00001` | KEGG glycan | KEGG |
| `R00299` | KEGG reaction (`rn:`) | KEGG |
| `K00844` | KEGG Orthology (`ko:`) | KEGG |
| `1.1.1.1` | Enzyme Commission (`ec:`) | KEGG, UniProt |
| `map00010`, `mmu00010` | reference pathway, mouse pathway | KEGG |
| `M00001` | KEGG module | KEGG |
| `mmu:11651` | KEGG mouse gene = NCBI Gene ID | KEGG |
| `11651` | NCBI Gene ID | NCBI |
| `NM_`, `NP_`, `XP_` | RefSeq transcript, protein | NCBI |
| `P31750`, `Q8CF...` | UniProtKB accession | UniProt |
| `UPI...` | UniParc sequence | UniProt |
| `ENSMUSG`, `ENSMUST`, `ENSMUSP` | Ensembl gene, transcript, protein | Ensembl |
| `5793` | PubChem CID (compound) | PubChem |
| `3333` | PubChem SID (substance deposit) | PubChem |
| `WQZGKKKJIJFFOK-GASJEMHNSA-N` | InChIKey: 14-character connectivity block, stereo block, protonation flag | any |
| `CHEBI:17234` | ChEBI | EBI |
| `HMDB0000122` | HMDB | HMDB |

## Rate limits

| Service | Limit | Route |
|---|---|---|
| KEGG REST | 3 calls per second; 403 means blocked | `scripts/kegg_rest.py` |
| PubChem PUG | 5 requests per second, 400 per minute | one call per 0.25 s |
| NCBI E-utilities | 3 per second, 10 with `NCBI_API_KEY` | one call per 0.34 s |
| UniProt REST | no published ceiling; ID mapping runs as asynchronous jobs | poll every 2 s |

Sleep between calls in any loop that touches PubChem or NCBI, and batch inputs wherever the
service takes a list.

## Shared workflows

### Metabolite to everything

Copy this checklist and track progress:

-   [ ] Step 1: Resolve the name to candidates (`pubchem-pug.md`) or take the C number as given.
-   [ ] Step 2: Fetch the KEGG entry for formula, exact mass, reactions, pathways, `DBLINKS`.
-   [ ] Step 3: Convert C number to PubChem SID, then to CID, then to InChIKey (`id-conversion.md`).
-   [ ] Step 4: Convert to ChEBI with KEGG `conv chebi`; keep every ChEBI row.
-   [ ] Step 5: Record the count of candidates at each hop next to the final identifier.

### Gene to metabolic role

Copy this checklist and track progress:

-   [ ] Step 1: Strip the Ensembl version suffix and map to an NCBI Gene ID (`id-conversion.md`).
-   [ ] Step 2: `link ko mmu:<GeneID>` for K numbers; an empty answer means no KEGG orthology.
-   [ ] Step 3: `link reaction ko:<K>` and `link pathway mmu:<GeneID>`.
-   [ ] Step 4: `link compound rn:<R>` for substrates and products; mark currency metabolites.
-   [ ] Step 5: Pass the gene table to `rna-metabolite-prediction.md` for the interpretation limits.

## Common mistakes

-   **Treating `conv pubchem` output as CIDs.** KEGG returns PubChem SIDs. `C00031` gives
    `pubchem:3333`, and CID 5793 is one hop further through PUG `substance/sid/<SID>/cids`.
-   **Taking the first name hit.** PubChem and KEGG name searches return several candidates;
    stereoisomers and salts share names.
-   **Matching on mass alone.** `C00031` glucose, `C00095` fructose and `C00124` galactose share
    exact mass 180.063388. Mass defines a candidate set.
-   **Using a reference pathway for organism genes.** `map00010` lists no mouse genes; use
    `mmu00010`.
-   **Passing more than 10 entries in one KEGG `get`.** The wrapper batches; raw calls fail.
-   **Forgetting the Ensembl version suffix.** UniProt returns `ENSMUSG00000001729.12` in
    `failedIds`; `ENSMUSG00000001729` (Akt1) maps. Direct Ensembl to `GeneID` is an invalid pair.
-   **Reading KEGG compound entries as defined structures.** Some are generic (R groups,
    polymers); some drugs (`D`) duplicate a compound (`C`) under `Same as`.
-   **Using KEGG output beyond academic terms.** The REST API is licensed for academic use.

## Reference materials

-   [kegg-rest.md](references/kegg-rest.md), [pubchem-pug.md](references/pubchem-pug.md),
    [uniprot.md](references/uniprot.md), [ncbi-entrez.md](references/ncbi-entrez.md)
-   [id-conversion.md](references/id-conversion.md),
    [metabolomics-mapping.md](references/metabolomics-mapping.md),
    [rna-metabolite-prediction.md](references/rna-metabolite-prediction.md),
    [terms-and-limits.md](references/terms-and-limits.md)
-   `scripts/kegg_rest.py` — throttled KEGG client; run `python3 -I scripts/kegg_rest.py -h`
-   `NOTICE` and `LICENSE` — Apache-2.0 terms and the attribution for the derived material

## See also

-   `gatom-metabolomic-predictions` — Downstream consumer; solves the active metabolic module from the DE table and the KEGG-derived network
-   `bulkirna` — Prerequisite; produces the DE table whose gene IDs enter the gene route
-   `bulk-rnaseq-gsea` — Sibling; tests KEGG pathway sets by enrichment, where this skill resolves their members
-   `annotate-bulk-rnaseq-data` — Prerequisite; attaches the gene symbols and IDs this skill converts
