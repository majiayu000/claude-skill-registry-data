---
name: ref-verify
description: "Prevents citation hallucination in academic writing. Invoke when: finding papers to support a specific claim; verifying/checking/auditing existing citations or DOIs; confirming whether a paper actually says what the user claims it says ('is that what the paper says?', 'did they actually show X?'); adding a citation by describing a paper ('add a citation for the paper where X'); running a pre-submission reference sweep. Do NOT invoke for: formatting references in APA/IEEE style, general topic explanations, citation style questions, or prose editing. Selects Quick Screen (seconds per paper) or Full Audit (source-depth claim check) automatically."
---

# ref-verify — Reference Hallucination Guard

The specific failure this skill prevents: LLMs describe paper content from recalled training data rather than from what the abstract actually says. A paper gets attributed findings it doesn't contain, or cited for claims that appear nowhere in the text. The fix is one rule applied consistently:

**Every content statement about a paper must come from a live-fetched source — abstract for topline/headline claims, full text for mechanism/implementation/procedural claims — quoted or paraphrased verbatim. If you cannot fetch the required source, say so explicitly — never fill the gap with recalled description, and never let a topical abstract match stand in for a mechanism-level claim.**

---

## Mode Decision

Pick the mode before doing any work. The choice controls cost and depth.

```
User provides DOI(s) for sanity check?
  └─ ≤10 refs → Quick Screen all
  └─ >10 refs → Quick Screen all; Full Audit only MISMATCH/DEAD results

User says "find papers on X" or "cite papers supporting claim Y"?
  └─ Full Audit (searching from scratch requires content verification)

User says "verify/check my reference list" or pre-submission audit?
  └─ CLI available → Pre-submission sweep (below) first: check-bib, then check-file
  └─ ≤5 refs  → Full Audit all
  └─ >5 refs  → Quick Screen all first; Full Audit MISMATCH/DEAD + any ref
                 cited for a specific factual claim

User is writing inline and adds a single citation from memory?
  └─ Quick Screen minimum; Full Audit if citing for a specific claim
```

The expensive part is Full Audit (5-layer, source-depth evidence fetch). Quick Screen costs ~5s per paper. Only escalate to Full Audit when the task genuinely requires content verification.

---

## Executable Engine

Use this as a skill-level workflow. Do not build or require MCP for this path.
The CLI is an execution engine the skill can call from the terminal; the manual
protocol remains the fallback and the source of truth for layers the CLI does
not yet cover.

### CLI Availability Check

The skill ships its own engine: `npx skills add` copies the `src/` folder next
to this SKILL.md. Before a DOI-backed check, resolve the engine once, in this
order, and keep the first command that prints help:

1. **Bundled with this skill** (same version as this SKILL.md; no install, no
   network for setup):

   ```bash
   PYTHONPATH="$SKILL_DIR/src" python3 -m ref_verify.cli --help
   ```

   `$SKILL_DIR` is the absolute path of the folder that contains this SKILL.md
   (Claude Code shows it as the skill's base directory; `npx skills add -g`
   installs it under `~/.agents/skills/ref-verify`). Never use a relative
   `src` path: the working directory is the user's project, not the skill
   folder. Requires Python 3.10 or newer.

2. **Installed console script** (`pip install ref-verify` or `pipx install ref-verify`):

   ```bash
   ref-verify --help
   ```

   npx skills add does not pip-install the Python CLI, so this is often absent.

3. **From PyPI through uv**:

   ```bash
   uvx --from 'ref-verify>=1.3.2' ref-verify --help
   ```

The commands below use the bundled form; with engine 2 or 3, replace
`PYTHONPATH="$SKILL_DIR/src" python3 -m ref_verify.cli` with `ref-verify` (or
the `uvx` form). An unavailable engine is not a verification result. If all
three fail, follow the manual fallback protocol below. Do not pretend the CLI
ran, and do not invent a result from memory.

### CLI-first workflow

Use the CLI first when the user provides a DOI or asks whether a DOI-backed
abstract supports a specific factual claim. Current CLI scope is CrossRef
metadata verification plus DOI-bound abstract claim checks. Claim checks use
CrossRef first, then DOI-bound OpenAlex, Semantic Scholar, and PubMed fallback when
CrossRef has no abstract.

CrossRef metadata screen:

```bash
PYTHONPATH="$SKILL_DIR/src" python3 -m ref_verify.cli verify-doi <doi> \
  --title "<provided title>" \
  --first-author <provided-first-author-last-name> \
  --year <provided-year> \
  --json
```

`verify-doi` exits `0` only for `PASS`; `WARN` and `REJECT` return non-zero.
Supplying only a DOI checks that CrossRef resolves but is not enough to pass
metadata verification.

Route the result:

- `PASS`: report the metadata match, then continue Layer 4 DOI landing-page
  resolution and Layer 5 retraction checks when the selected mode requires them.
- `WARN`: report the missing or weak metadata, then continue manual fallback for
  the missing layers instead of silently accepting the reference. With
  `DOI_NOT_IN_CROSSREF` the DOI is registered outside CrossRef (arXiv, Zenodo,
  KISTI); verify title and authors at doi.org and never call the DOI dead.
- `REJECT`: stop using that citation as verified; report the mismatch and ask
  for a corrected DOI or citation unless the user explicitly wants alternatives.

Reference list check (BibTeX, RIS, or a plain-text/Markdown bibliography). Run
this first when the user hands over a reference list, then check claims:

```bash
PYTHONPATH="$SKILL_DIR/src" python3 -m ref_verify.cli check-bib <references.bib|.ris|.txt|.md>
```

When the user wants something to read or share (an advisor, co-authors), add
`--report <name>.html` (or `.md`): the HTML lists the items
that need a look first and explains each verdict in plain words. Give the user
the report path.

Route each result:

- `PASS`: the reference matches a CrossRef record (by its DOI, or found by
  search with `REFERENCE_RESOLVED` and a `resolved_doi`).
- `WARN` with `REFERENCE_UNMATCHED` (`status: UNVERIFIED`): CrossRef search
  found no matching record. Report it as unverified and run the manual Quick
  Screen on it; do not call it fabricated from this result alone.
- `WARN` with `DOI_NOT_IN_CROSSREF` (`status: UNVERIFIED`): the DOI is
  registered with another agency (arXiv/Zenodo via DataCite, KISTI, JaLC), so
  its metadata was not compared; confirm it at doi.org, never call it dead.
- Other `WARN`: metadata partly differs, the reference text was too thin to
  confirm, or (`status: MISMATCH`) a plain-text reference's DOI belongs to the
  paper named in `reason`; report the `reason` and check manually.
- `REJECT`: dead DOI (`DOI_NOT_FOUND`), retraction (`PAPER_RETRACTED`), or a
  DOI that points to a different paper. Stop using it as verified.

Single claim check against a DOI abstract:

```bash
PYTHONPATH="$SKILL_DIR/src" python3 -m ref_verify.cli check-claim <doi> --claim "<specific factual claim>" --json
```

`--source crossref|openalex|semantic-scholar|pubmed` forces one source (it
bypasses CrossRef), for debugging a single source's failure.

Route the result:

- `ACCEPT`: quote the CLI evidence and continue any required manual DOI
  resolution, second-source existence, and retraction layers.
- `WARN` or `PARTIAL`: report what the selected abstract source did and did not
  support, then continue manual fallback when more layers are required.
- `UNVERIFIABLE`: no trusted DOI-bound abstract evidence was available from the
  attempted CLI sources. Continue the manual fallback chain below instead of
  treating the claim as rejected or supported.

CLI `ACCEPT` is abstract-level evidence only. It means every number in the
claim, with its unit, sign, and direction, is supported by the same abstract
sentence; one number the sentence does not support blocks `ACCEPT` even when
another number matches. If the claim describes a mechanism, implementation,
or procedure, do not promote that result to the Full Audit verdict; classify
the claim in Layer 3 and obtain the required full-text evidence first.

For JSON output, use `abstract_source`, `source_attempts`, and `error_code` to
decide the next step:

- `CLAIM_SUPPORTED`: explicit abstract support found.
- `CLAIM_NOT_EXPLICIT`: an abstract was available, but the claim was not
  explicitly supported.
- `CLAIM_AMBIGUOUS`: numeric evidence or context exists, but binding is
  ambiguous.
- `NO_ABSTRACT`: attempted DOI-bound sources did not provide abstract text.
- `DOI_NOT_FOUND`: neither CrossRef nor doi.org knows the DOI, or the selected source did not find a DOI-bound record.
- `PAPER_RETRACTED`: CrossRef lists a retraction notice for the DOI; the claim is rejected before any abstract is read.
- `DOI_MISMATCH`: the primary or explicitly selected DOI-bound record did not
  match the requested DOI.
- `SOURCE_API_ERROR`, `SOURCE_TIMEOUT`, `SOURCE_RATE_LIMITED`, `SOURCE_UNSUPPORTED`: source lookup
  failed, timed out, was rate-limited, or could not be used.
- `REFERENCE_RESOLVED`, `REFERENCE_UNMATCHED` (`check-bib` only): a reference
  without a DOI did or did not match a CrossRef record.
- `DOI_NOT_IN_CROSSREF` (`verify-doi`, `check-claim`, `check-file`, `check-bib`): the
  DOI exists at another registration agency (DataCite, KISTI, JaLC), so it is
  unverified rather than dead. `check-claim` still judges the claim when OpenAlex
  or Semantic Scholar has the abstract; otherwise confirm the work at doi.org.

The CLI does not replace Layer 4 DOI landing-page resolution or two-source
existence checks, and it only catches retractions that CrossRef records as a
retraction notice. Continue the manual protocol for those layers when the
selected mode requires them.

### Pre-submission sweep

Use the engine for both jobs. It queries CrossRef and doi.org for references and
CrossRef, then OpenAlex, Semantic Scholar, and PubMed for abstracts, with a cache;
do not hand-write `curl` calls for these.

1. **References → `check-bib`.** Save only the reference list (the References
   section, or the `.bib`); body paragraphs become spurious UNVERIFIED rows. The
   text output gives one verdict and reason per reference. `--json` is too large
   for one tool result: write it to a file (`--json > refs-check.json`) and read
   it in parts.
2. **Numeric claims → `check-file`.** Write `claims.jsonl`, one
   `{"id", "doi", "claim"}` per cited sentence with a number (DOI from the
   reference or check-bib's resolved DOI). Copy numbers, units, and direction
   words exactly as the manuscript has them (`\SI{172.3}{\joule\per\mole}` is
   172.3 J/mol); never correct a claim while copying it. Run
   `PYTHONPATH="$SKILL_DIR/src" python3 -m ref_verify.cli check-file claims.jsonl`.
   The text output gives each claim's verdict and the abstract sentence it
   matched (`Evidence`).
3. **Judge each claim from that sentence, never from memory or the label alone.**
   - Different value, unit, or direction → the manuscript misstates the paper,
     even under `ACCEPT`; quote the sentence and give the correct value.
   - Same value, unit, and direction → quoted abstract support, not a problem
     (the label stays `WARN` in any verdict table).
   - Sentence about something else, or about only part of the claim → read the
     whole abstract (`check-claim` prints it under `paper`) before writing that
     the abstract does not state it.
4. **Look up by hand only what the engine left undecided** (`REFERENCE_UNMATCHED`,
   `DOI_NOT_IN_CROSSREF`, `UNVERIFIABLE`): Layer 1 sources and doi.org. For a
   citation without a title, search the author and journal plus the topic words of
   the sentence citing it; a record that fits but has another volume or page means
   the citation's volume or page is wrong. Mechanism claims still need Layer 3b,
   and Layers 4–5 still apply where the mode requires.

---

### Quick Screen — metadata + DOI sanity check

Use when the user provides a DOI or full citation and wants a sanity check.

1. Hit CrossRef: `https://api.crossref.org/works/{DOI}`
2. Compare returned title + first-author last name against what user provided
3. Fetch `https://doi.org/{DOI}` — confirm it resolves and lands on the right paper
4. Report one line per reference:

```
Smith et al. (2021) 10.1234/example — PASS (title/author match, DOI resolves)
Jones (2019) 10.5678/other — MISMATCH (CrossRef: Jones & Lee 2019, not Jones alone)
Kim (2023) 10.9999/fake — DEAD DOI
```

Escalate to Full Audit if: DOI resolves to a different paper, any field mismatches, or user is citing for a specific factual claim.

---

### Full Audit — for literature search or pre-submission check

Use when: searching for papers to support a claim, or doing a final citation sweep.

Run all five layers per paper. The layers are ordered by what they catch — don't skip forward.

**Layer 1 — Existence**

Search two sources independently:
- CrossRef: `https://api.crossref.org/works?query.bibliographic={title+author}&rows=5`
- OpenAlex: `https://api.openalex.org/works?search={title+author}&per-page=5`
- arXiv for preprints: `https://export.arxiv.org/api/query?search_query=ti:{title}&max_results=3`
- Semantic Scholar, only when these cannot settle the item (it rate-limits shared clients): `https://api.semanticscholar.org/graph/v1/paper/search?query={title+author}&fields=title,authors,year,externalIds,abstract&limit=5`

A paper is confirmed only if titles essentially match and first-author last name agrees across two sources.

- Two-source hit → `CONFIRMED`
- One-source → `SINGLE-SOURCE ⚠` — proceed with caution, note in output
- Zero → `NOT FOUND ✗` — stop; report clearly; do not invent a substitute

**Layer 2 — Metadata**

Extract from confirmed sources and compare: title, all authors (last names), year, journal full name, DOI, volume/pages (mark `[NOT IN SOURCE]` if absent). If any field differs between sources, show both — do not silently pick one.

**Layer 3 — Content Traceability** ← most important layer

This is where the skill's core value lies. The goal is not just "does this paper exist" but "does this paper actually contain the claim being attributed to it."

**Step 0 — Classify the claim.**

Before fetching anything, classify what kind of claim is being verified:

- **Topline/headline claim** — a finding of the kind abstracts conventionally state (overall result, top-line number, general conclusion). Abstract-only evidence is a legitimate source of truth for this class.
- **Mechanism/implementation/procedural claim** — describes *how* something works or was done: a specific mechanism, algorithm, architecture, parameter, experimental step, control condition, or a numeric value tied to a table/figure/method section rather than the summary result. Abstracts routinely omit this content even when the paper supports it. Signal words: "mechanism," "how," "architecture," "algorithm," "implementation," "procedure," "protocol," "parameter," "control group," "ablation," "table," "figure," or any claim more specific than what a one-paragraph summary would state.

If the claim is mechanism/implementation-class, an abstract-only check is not sufficient even when the abstract is topically on point. Fetch the abstract as evidence of existence/topic match, but do not resolve the verdict from the abstract alone — continue to Layer 3b below.

Fetch the abstract with the engine (`check-claim`/`check-file` try sources 1–3 and
PubMed). By hand, when the engine is unavailable or found no abstract, use this
priority order:
1. CrossRef raw JSON: `https://api.crossref.org/works/{DOI}` — check the `abstract` field
2. OpenAlex: `https://api.openalex.org/works/doi:{DOI}?mailto={contact_email}` — reconstruct `abstract_inverted_index`
3. Semantic Scholar: `https://api.semanticscholar.org/graph/v1/paper/DOI:{DOI}?fields=abstract`
4. Open-access fallback: `https://api.unpaywall.org/v2/{DOI}?email={contact_email}` — check `is_oa` and `oa_locations`
5. arXiv fallback for preprints: `https://export.arxiv.org/api/query?id_list={arxiv_id}`
6. PubMed Central for life/bio papers: `https://www.ncbi.nlm.nih.gov/pmc/articles/{PMCID}/`

For APIs that require a contact email, replace `{contact_email}` with a real,
user-authorized address from configuration. Do not send a placeholder address.

After fetching, check: does the abstract contain the specific claim being cited?

- Abstract explicitly contains the claim (quote it verbatim) → `CONTENT: SUPPORTED`
- Abstract is about the topic but doesn't make the specific claim → `CONTENT: PARTIAL — quote what it actually says`
- Abstract contradicts the claim → `CONTENT: CONTRADICTED — do not use this citation`
- Abstract not accessible after trying all sources → `CONTENT: UNVERIFIABLE — user must check full text`
- Claim is mechanism/implementation-class and full text could not be obtained after trying all Layer 3b sources → `CONTENT: ABSTRACT-ONLY — full text unavailable, verification insufficient`. This label must never be upgraded to SUPPORTED/ACCEPT.

**The rule that cannot be relaxed**: if you describe what a paper "shows" or
"demonstrates" or "reports," you must quote or directly paraphrase fetched
source text at the required depth. Summarizing from memory is not permitted
even if you feel confident.

**Layer 3b — Full-Text Confirmation (mechanism/implementation-class claims only)**

Required whenever Step 0 classified the claim as mechanism/implementation-class,
or whenever the abstract verdict is `PARTIAL` for a claim more specific than the
abstract's summary level. Skip only for topline claims that received
`CONTENT: SUPPORTED` directly from the abstract.

Fetch the paper body in this priority order, stopping at the first success:

1. **Local Zotero PDF** — if a Zotero library is configured, query its database
   for this DOI, resolve the attachment key, and read the linked PDF. A common
   default is `~/Zotero/zotero.sqlite` with attachments under
   `~/Zotero/storage/{key}/`; discover the actual path instead of assuming it.
2. **research-wiki vault** — when the `research-wiki` skill is available,
   search its configured vault for an already-ingested full-text copy. Do not
   assume a machine-specific vault path.
3. **Open-access link** — resolve and fetch the actual full text (not just an
   availability flag):
   - Unpaywall: `https://api.unpaywall.org/v2/{DOI}?email={contact_email}`
     → fetch `best_oa_location.url_for_pdf` (or any `oa_locations[].url_for_pdf`).
   - arXiv: `https://export.arxiv.org/api/query?id_list={arxiv_id}` → fetch the
     full paper, not only the `<summary>` field.
4. **Failure** — if none of the above yields a readable full text, do not treat
   the abstract as sufficient. Apply the `CONTENT: ABSTRACT-ONLY` label defined
   above.

When full text is obtained, quote the passage that supports, partially supports,
or contradicts the claim. For a mechanism/implementation claim, `CONTENT:
SUPPORTED` requires a full-text quote — an abstract-level topic match cannot
satisfy it.

**Layer 4 — DOI Resolution**

Fetch `https://doi.org/{DOI}`. Confirm the landing page matches the expected paper. A 403 (bot-blocked) from a URL slug containing the title and volume is not a dead link — note it as paywalled. A redirect to an unrelated page is a critical failure.

**Layer 5 — Retraction**

Search `"{first author last name}" "{journal name}" retraction` and check the DOI landing page for retraction banners. A retracted paper must not be used as a primary source.

---

## Output Format

**Quick Screen**: one line per reference (see above).

**Pre-submission sweep**: lead with decisions. For each problem: the reference
as cited, what is wrong, the evidence (engine reason, CrossRef record, or quoted
abstract sentence), and the fix. Then a short separate list, "Could not be
confirmed automatically — look these up yourself", for items still unverified
(theses, unindexed preprints). No commentary on tools, retries, or rate limits.

**Full Audit**: one card per paper, then a summary table.

```
REFERENCE AUDIT
────────────────────────────────────────────────
Paper:   [Title from live source — not from memory]
DOI:     [DOI] — [✓ Resolves | ✗ Dead | ✗ Wrong paper | ⚠ Paywalled-403]
Authors: [Full list from CrossRef/OpenAlex/S2]
Year:    [Year] — Source: CrossRef | S2 | arXiv
Journal: [Full name]

EXISTENCE:  ✓ Confirmed (sources) | ⚠ Single-source | ✗ Not found
METADATA:   ✓ Consistent | ⚠ Discrepancy: [field: value-A vs value-B]
CONTENT:    ✓ Supported — "[verbatim excerpt — abstract for topline, full text for mechanism claims]"
            ⚠ Partial — source says: "[what it actually says]"
            ⚠ Abstract-only — mechanism/implementation claim, full text unavailable after Zotero/research-wiki/OA attempts
            ✗ Contradicted | — Unverifiable (tried CrossRef/OpenAlex/S2/Unpaywall/arXiv/PubMed)
RETRACTION: ✓ None found | ✗ Retracted

VERDICT: ACCEPT | WARN | REJECT
Reason: [one sentence — what's missing or wrong]
────────────────────────────────────────────────
```

CONTENT field must show either a verbatim excerpt or an explicit non-support
state such as `ABSTRACT-ONLY` or `UNVERIFIABLE` — never a summary written from
memory.

**ACCEPT**: two-source confirmed, DOI resolves to the right paper, content supported at the required source depth (abstract for topline claims; full text for mechanism/implementation/procedural claims), and no retraction.
**WARN**: solvable issue — single source, partial content match, abstract inaccessible after trying all fallbacks, or (mechanism/implementation claim) full text inaccessible after trying Zotero/research-wiki/OA fallbacks. The full-text-inaccessible case must carry the ABSTRACT-ONLY label in the summary table (e.g. `WARN (ABSTRACT-ONLY: mechanism claim, PDF unreachable)`) and can never be reported as ACCEPT. Safe to use if user verifies the flagged item.
**REJECT**: DOI dead or resolves to wrong paper, paper not found anywhere, content contradicted, or retraction confirmed.

Summary table after all cards:

```
SUMMARY
────────────────────────────────────────────────
1. Smith et al. (2021)  — ACCEPT
2. Kim & Park (2019)    — WARN (abstract unverifiable; try PMC or institutional access)
3. Zhang (2023)         — REJECT (DOI resolves to different paper)
────────────────────────────────────────────────
X / Y verified.  Z need attention.
```

---

## Anti-Hallucination Rules

- Never recall a DOI from memory — fetch from CrossRef or OpenAlex.
- Never describe paper content without fetched source text at the required depth to quote from.
- Never fill in missing metadata by guessing or pattern-matching.
- If two sources disagree, show both — do not choose silently.
- If the source required for the claim depth is inaccessible after all fallbacks, mark UNVERIFIABLE or ABSTRACT-ONLY as defined above — do not substitute a description from memory.
- Never resolve a mechanism/implementation-class claim from an abstract topic match alone — fetch full text via Layer 3b, or mark ABSTRACT-ONLY and stop.

---

## Edge Cases

**Preprint vs. published**: record both DOIs; prefer published for citation; note if title changed between versions.

**Author name variants**: "J. Smith" vs "John Smith" — flag but do not merge; let user confirm.

**Conference proceedings**: volume/pages often absent from CrossRef; mark `[NOT IN SOURCE]`, not guessed.

**Rate limits (HTTP 429, e.g. Semantic Scholar)**: a 429 is no evidence either way. Decide from the other sources; mention it only if it leaves an item undecided, and never soften a verdict because of it.
