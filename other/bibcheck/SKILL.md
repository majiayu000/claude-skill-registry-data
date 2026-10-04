---
name: bibcheck
description: Audit an existing .bib entry by entry against Crossref, OpenAlex, arXiv, and Zotero for wrong years, mis-cited authors, wrong venue or volume, dead DOIs, and hallucinated entries. TRIGGER on "/bibcheck", "audit my .bib", "verify my references", "check my bibliography", "are any of these citations fake", "did Claude hallucinate a citation", or a pre-submission bib audit.
allowed-tools: Read, Write, Glob, Grep, Bash, Agent, Monitor, WebFetch, mcp__zotero__zotero_search_items, mcp__zotero__zotero_get_item_metadata
---

# bibcheck

Given a `.bib`, spawn subagents over batches of 5 entries to verify each entry against canonical
metadata, then emit a PASS/WARN/FAIL report and a `corrected.bib` the user reviews and merges. The
source `.bib` is never modified.

One agent asked to audit 200 entries in a single pass drifts: early entries get careful treatment,
late entries get pattern-matched. Batches of 5 stay short enough that the cliff never arrives, and
the batch contract in phase 1 polices the same drift inside each batch.

Per-entry verification against canonical metadata is adapted from Scott Cunningham's
[MixtapeTools](https://github.com/scunning1975/MixtapeTools).

Hallucinated citations have a recognizable signature: plausible authors, plausible title, a DOI
that 404s, and no match in Crossref, OpenAlex, or arXiv. Surfacing that pattern is the point.

## Inputs and scoping

Take a `.bib` path as the argument. With no argument, Glob in this order and ask if ambiguous:

1. `references.bib`, `refs.bib`, `bibliography.bib`, then `*.bib` in the cwd.
2. `~/Library/CloudStorage/Dropbox*/Apps/Overleaf/*/*.bib` (this setup assumes Overleaf projects sync here via Dropbox; adjust to your machine).

With several `.bib` files in one project, grep the `.tex` for `\bibliography{}` / `\addbibresource{}`
to pick the one actually loaded. Skip anything under `_archive/` or `Old/` unless asked.

Scope before dispatching. Zotero-exported libraries carry far more entries than the manuscript
cites (one real project here: 345 entries, 170 cited), and auditing an uncited entry is wasted work.
Collect the cited keys and offer to restrict to them:

```bash
grep -ohE '\\[a-zA-Z]*[Cc]ite[a-zA-Z]*\*?(\[[^]]*\])*\{[^}]*\}' /abs/path/to/*.tex \
  | grep -oE '\{[^}]*\}$' | tr -d '{}' | tr ',' '\n' | tr -d ' ' | sort -u
```

Report both counts and let the user choose. Default to cited-only above 100 entries.

## Phase 0: parse

Read the `.bib` in full. Split on `^@\w+\{` boundaries and capture the entry type, citation key, and
every `field = {value}` pair (braced and quoted forms, escaped braces, multi-line values). Malformed
entries (unbalanced braces, missing key, duplicate key) go straight to FAIL with no subagent.

Triage by entry type, because the checks that apply differ:

- Indexed types (`@article`, `@inproceedings`, `@book`, `@incollection`, `@phdthesis`): full check set.
- Non-indexed types (`@misc`, `@online`, `@software`, `@dataset`, and `@unpublished` with no arXiv
  id): blog posts, docs pages, and repos legitimately have no DOI and appear in no index. Check the
  `url`/`howpublished` link resolves (`curl -sSI -o /dev/null -w '%{http_code}'`) and that `year`
  looks sane. Never assign the fabrication verdict to these.

Create `<bib_dir>/bibcheck_<YYYYMMDD_HHMM>/` containing `entries/` (one `.bib` fragment per entry,
subagent input) and `reports/` (one `.json` per entry, subagent output), plus `input.bib` as a
verbatim copy of the source for provenance.

## Phase 1: dispatch

Group the well-formed entries into batches of 5, preserving file order; the last batch holds the
remainder. Launch batch subagents with the `Agent` tool, keeping 8 in flight. They run in the
background: when a completion notice arrives, launch the next batch, and carry on with any
aggregation already possible in the meantime. Respect `--max-parallel N` if the user passes it;
drop to 2 when rate-limited.

Each subagent gets its batch's raw entry texts, the absolute `entries/` paths, one absolute output
path `reports/<citekey>.json` per entry, and the check list below. Subagent working directories
reset between Bash calls, so every path handed to a subagent must be absolute.

The batch contract: the subagent returns the full per-entry output schema for every entry in its
batch, each verified independently against the lookup tools, with no verdict inferred from a
batchmate.

Give each subagent a 60-second lookup budget per entry. On expiry it writes
`{"verdict": "WARN", "diagnostic": "lookup_timeout"}` for that entry and moves to its next one.
Raise the budget on a cold cache; `paper.py` disk-caches responses for 30 days, so reruns are fast.

## Phase 2: per-entry checks

### The two lookup tools

`paper.py` is the resolver from the `reading-papers` skill. Read
`~/.claude/skills/reading-papers/SKILL.md` if unfamiliar.

```bash
~/.claude/skills/reading-papers/scripts/paper.py resolve "<query>" --json
```

It returns a JSON array. Interpreting it is the whole game:

- One element with `title`, `authors`, `year`, `venue`, `is_oa` populated: a confident canonical
  match.
- One element with only `{"doi": ..., "title": null}`: the identifier exists as a string but no
  index recognizes it. Exit code is still 0, so test the payload, not `$?`.
- Several elements carrying only `{doi, title, venue}`: no confident match, just relevance-ranked
  candidates. Treat as "not found" unless one clears the 0.85 title threshold below.

It does not return volume, issue, or pages. Crossref does, and Crossref is free and unmetered.
Replace `you@example.edu` with your real address in both Crossref calls in this file: the
`mailto=` parameter joins Crossref's polite pool, and Crossref asks for a real contact.

```bash
curl -sS -w '\nHTTP:%{http_code}' "https://api.crossref.org/works/<doi>?mailto=you@example.edu" \
  | python3 -c 'import sys,json; b=sys.stdin.read(); code=b.rsplit("HTTP:",1)[1].strip()
if code!="200": print(json.dumps({"crossref_status":code})); raise SystemExit
m=json.loads(b.rsplit("\nHTTP:",1)[0])["message"]
print(json.dumps({k:m.get(k) for k in ("DOI","title","container-title","short-container-title","volume","issue","page","issued","type","author","ISSN")},ensure_ascii=False))'
```

A dead DOI returns HTTP 404 with the non-JSON body `Resource not found.`, so test the status code,
never `$?` alone (`--fail` exits 56 here, not the documented 22). Use `WebFetch` on the same URL only
if Bash is unavailable; it summarizes through a model and drops fields.

Cost discipline. OpenAlex is metered: an identifier lookup costs 1 credit, anything routed through
`search` (including title search) costs 10. Spend identifiers before strings. Order per entry:
Crossref by DOI (free) → `paper.py resolve` by DOI or arXiv id (1 credit) → Crossref
`query.bibliographic` (free) → `paper.py resolve` by title (up to 10 credits), reaching the last rung
only when the entry has no identifier at all.

### The checks, in order, stopping once the verdict is settled

1. DOI resolution. With a `doi` field, run the Crossref call above for volume, issue, pages, ISSN,
   and `issued`, then `paper.py resolve "<doi>" --json` for the authoritative author spellings and
   venue. Crossref 404 plus `"title": null` from `paper.py` is a dead DOI, so go to check 4.

2. arXiv resolution and preprint versus published. When the entry carries `eprint`,
   `archivePrefix = {arXiv}`, or `arXiv:` in `note`, run
   `paper.py resolve "<arxiv_id>" --json`. A hit returns `arxiv_id`, `title`, `authors`, `year`,
   `abstract`, and `doi` (null when arXiv-only). Confirm the title matches the entry. If the entry
   has no `doi`, resolve the exact title once to see whether a journal version now exists; a single
   full record with a non-arXiv `venue` means it does, and that is a WARN suggesting the published
   `@article` in place of the preprint `@misc`. Skip this probe for entries that already carry a
   published DOI, since it is the expensive rung.

3. Title match, last resort only. With no DOI and no arXiv id:

   ```bash
   curl -sS "https://api.crossref.org/works?query.bibliographic=<urlencoded+title>&rows=5&select=DOI,title,container-title,volume,issue,page,issued,author&mailto=you@example.edu"
   ```

   Crossref ranks by relevance, and the preprint often outranks the version of record (a real case:
   the SSRN copy of a Marketing Science paper comes back first). Pick by container: prefer a journal
   container over `SSRN Electronic Journal`, `arXiv`, `Research Square`, or `SocArXiv`. Confirm the
   winner with `paper.py resolve "<winning doi>" --json` at 1 credit. Only if Crossref returns
   nothing plausible, fall back to `paper.py resolve "<title>" --json`.

   Title match rule: lowercase, strip LaTeX braces and accents, strip punctuation, drop the
   stopwords {a, an, the, of, on, in, for, and, to}, tokenize on whitespace, and compute Jaccard
   overlap of the token sets. Accept at ≥ 0.85. Run the comparison in code, never by inspection:

   ```bash
   python3 -c 'import re,sys,unicodedata
   S={"a","an","the","of","on","in","for","and","to"}
   def t(s):
       s=unicodedata.normalize("NFKD",s); s="".join(c for c in s if not unicodedata.combining(c))
       return {w for w in re.sub(r"[^a-z0-9 ]"," ",s.lower().replace("{","").replace("}","")).split() if w not in S}
   a,b=t(sys.argv[1]),t(sys.argv[2]); print(round(len(a&b)/len(a|b),3))' "<entry title>" "<candidate title>"
   ```

   The same normalization (NFKD, combining marks stripped, lowercase, punctuation removed) is what
   check 5 means for surnames; reuse `t()` on the surname strings.

4. Fabrication test. FAIL with `fabricated? DOI does not resolve and no index recognizes the title`
   when all of these hold: the entry is an indexed type; a `doi` is present and both Crossref and
   `paper.py` reject it (or no `doi` is present at all); and the title clears 0.85 against nothing
   in Crossref, OpenAlex, or arXiv. All three conditions are required. A missing DOI alone is
   normal for older and non-English work.

5. Author normalization. Compare surname sequences after NFKD normalization, combining-mark removal,
   lowercasing, and punctuation stripping.
   - Clear surname mismatch, or a different number of named authors where the source lists fewer:
     FAIL.
   - Initials against full given names: no flag, that is a style choice.
   - Accent loss (`Pena` for `Peña`) or a dropped tussenvoegsel (`Van Den Bulte` for
     `van den Bulte`): WARN. Strip leading particles {van, van der, van den, de, de la, del, della,
     di, du, von, zu, ter, ten, la, le} before the surname comparison, then compare the particle on
     its own.
   - Author-list truncation (`and others`, missing trailing authors): WARN.
   - Judge accents against `paper.py`/OpenAlex, never against Crossref. Crossref frequently stores
     the stripped form (it returns `Yildirim` where OpenAlex returns `Yıldırım`), so a Crossref
     diff alone is not evidence of an error in the entry.

6. Year reconciliation against Crossref `issued.date-parts[0][0]`. With an arXiv id present and the
   entry year matching the arXiv submission year, WARN
   (`entry cites preprint year <y1>; published version is <y2>`), because citing the preprint year
   is a legitimate choice. Otherwise FAIL.

7. Journal canonicalization. Compare `journal` against Crossref `container-title`. WARN on
   abbreviation drift (`J. Mark. Res.` for `Journal of Marketing Research`, `Mark. Sci.` for
   `Marketing Science`, `Mgmt. Sci.` for `Management Science`, `Quant. Mark. Econ.` for
   `Quantitative Marketing and Economics`). FAIL on a different journal entirely, confirmed by a
   disjoint `ISSN` set. Apply the same logic to `booktitle` on `@inproceedings` (ICML, NeurIPS, KDD
   and their full names).

8. Volume, issue, and pages against Crossref `volume`, `issue`, `page`. Normalize page ranges before
   comparing: `831--847`, `831-847`, and `831–847` are the same range, and BibTeX's double hyphen is
   correct style. WARN on one field disagreeing. FAIL on two or more, which usually means a swapped
   entry, the title of paper A glued to the volume and pages of paper B.

9. Zotero cross-check, optional. For a Better BibTeX shaped key, call
   `mcp__zotero__zotero_search_items(query="<title>", qmode="titleCreatorYear", limit=3)` and pull
   `mcp__zotero__zotero_get_item_metadata` on a hit. A Zotero item with a different DOI than the
   entry is a WARN. Zotero reads work only while the desktop app is open, so any error means
   `checks_skipped: ["zotero"]`, never a WARN.

   When a Zotero call fails, tell the user directly, in the chat reply and not only in the report:
   Zotero looks closed, open the Zotero desktop app and this can be re-run to add the library
   cross-check. Say it once, up front, rather than burying it in per-entry output. A closed Zotero
   is the usual cause and it is a five-second fix, so it is worth interrupting for. Do not stop the
   audit over it; the other eight checks do not need Zotero.

### Subagent output

One file per entry at `reports/<citekey>.json`:

```json
{
  "citekey": "liu2022implications",
  "verdict": "PASS | WARN | FAIL",
  "diagnostic": "one line",
  "field_findings": [
    {"field": "year", "status": "FAIL", "entry_value": "2023",
     "canonical_value": "2022", "source": "crossref:10.1287/mksc.2022.1361"}
  ],
  "canonical_source": "crossref | openalex | arxiv | zotero | none",
  "checks_skipped": ["zotero"],
  "suggested_replacement": "<full corrected BibTeX entry, or null>"
}
```

## Phase 3: aggregate and report

First reconcile: every `entries/<key>.bib` must have a `reports/<key>.json`
(`comm -3 <(ls entries | sed 's/.bib$//' | sort) <(ls reports | sed 's/.json$//' | sort)`).
Re-dispatch the missing keys as one batch before aggregating, and state the reconciled count in
the report header.

Read every JSON in `reports/`. Bucket by FAIL, then WARN, then PASS; sort alphabetically by citekey
within each bucket so runs diff cleanly. Write
`<bib_dir>/bibcheck_<YYYYMMDD_HHMM>/bibcheck_report.md`:

```markdown
# Bibliography audit: <bib filename>

Date: YYYY-MM-DD HH:MM
Source: <absolute path>
Entries audited: N parsed, M malformed, K uncited and skipped

## Summary
| Verdict | Count |
|---|---|
| PASS | a |
| WARN | b |
| FAIL | c |
| Possibly fabricated | d (subset of FAIL) |

## FAIL (verify before submission)
| Citekey | Diagnostic | Source |
|---|---|---|

## WARN (preprint status, field drift, style)
| Citekey | Diagnostic |
|---|---|

## PASS
<one line each>

## Per-entry detail
<the JSON for every FAIL and WARN>

## Next steps
1. Review each FAIL row against corrected.bib.
2. `git diff --no-index <source>.bib corrected.bib`
3. Move corrected.bib into place yourself; this skill never overwrites the source.
```

Also write `corrected.bib`: the full source with FAIL and WARN entries replaced by their
`suggested_replacement`, PASS entries copied byte for byte, comments and entry order preserved. An
entry with no confident correction stays as-is under a leading
`% bibcheck:FAIL <diagnostic>` comment line.

## Verdict tolerances

PASS: a canonical source resolves and title, authors, year, venue, and volume/issue/pages all agree
within style tolerance. For a non-indexed `@misc`, PASS means the URL resolves.

WARN: at most one of accent or tussenvoegsel drift, journal abbreviation drift, preprint year
against published year, a single volume/issue/page disagreement, a preprint entry whose published
version now exists, a Zotero DOI mismatch, or `lookup_timeout`.

FAIL: a dead DOI, a wrong surname, a wrong year with no preprint explanation, a wrong journal
confirmed by ISSN, two or more volume/issue/page disagreements, a malformed or duplicate-key entry,
or the fabrication signature.

## Output layout

```
<bib_dir>/bibcheck_<YYYYMMDD_HHMM>/
  input.bib            verbatim copy of the source
  entries/<key>.bib    subagent inputs
  reports/<key>.json   subagent outputs
  bibcheck_report.md   consolidated report
  corrected.bib        candidate replacement for the user to diff and merge
```

## Failure modes

`.bib` not found: ask for the path, do not invent one.

Every entry returns `lookup_timeout`: a network or rate-limit problem. Retry once at
`--max-parallel 2`, then surface the error. Do not mark a whole bibliography FAIL on this.

A wave of year FAILs: usually preprint versus published. Widen the arXiv detection in check 2 and
leave the year tolerance alone.

Title match confidence below 0.7 across the board: the bibliography may be non-English or in a venue
neither Crossref nor OpenAlex indexes. Say so, ask for one entry known to be correct, and recalibrate
against it.

OpenAlex credits exhausted (1,000/day anonymous, 10,000 with the key in
`~/.claude/secrets/scholar.env`): fall back to Crossref-only checking, which still covers checks 1
and 6 through 8, and mark author-accent findings as skipped.

## Out of scope

Do not add entries. Hand a DOI to `mcp__zotero__zotero_add_by_doi`, or use the reading-papers
skill for anything else.

Do not overwrite the source `.bib` under any circumstances.

Do not claim a citation supports a textual claim. This skill verifies that an entry's metadata
matches a real paper and nothing more.

Do not bulk-reformat. A PASS entry is copied verbatim into `corrected.bib` even where its style
differs from the rest of the file.
