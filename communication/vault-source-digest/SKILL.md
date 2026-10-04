---
name: vault-source-digest
description: Digest a reference PDF (engineering standard, textbook, or paper) into the EmptyOS KB. Extracts the full verbatim page-marked text as a citation source artifact, then creates a `reference` landing note plus `clause`/`case` notes covering the document's real table-of-contents structure. Use when the user hands over a PDF (or several) and asks to "digest", "log", "file", "add to KB", or "reference in KB" a standard / source document. NOT for a pasted chat transcript (use eos-ai-conversation-ingest) and NOT for atomizing a standard already held in the KB (use eos-kb-atomize).
---

# Source Digest — PDF → KB (full-text + clauses)

File a reference PDF into the EmptyOS KB in two layers:

1. **Full verbatim text** — page-marked, watermark/PII-scrubbed, under
   `{vault}/30_Resources/EmptyOS/kb/sources/_fulltext/<SLUG>.md`. This is the
   citation anchor every clause note points at via `source_file:`.
2. **Distilled notes** — a `reference` landing note + `clause` notes covering the
   document's **real table of contents**, + `case` notes for worked examples.

The deterministic, error-prone half (extract, strip, page-mark, TOC → coverage ledger,
PII gate) is done by the bundled **`digest_pdf.py`**. This skill is the judgment half:
deciding which clauses earn a note, writing the paraphrase, and cross-linking.

The coverage ledger is **durable, not scratch** — it's written into the vault next to
the full text and doubles as resumable "what's left" state (see "Resuming a partial
digest" below). Row status updates are made with the bundled **`kb_coverage_status.py`**.

> **The full text is ALWAYS complete — every page, every section, verbatim. Nothing
> is ever omitted from it.** The "keep / fold / skip" decisions in Step 3 are *only*
> about which sections earn a distilled **clause note** — they never trim the full-text
> artifact. If a user says "don't skip anything / we need the full text," they're
> almost always reacting to the *coverage* language: reassure them the verbatim text is
> 100 % intact (verify per Step 7), and if they want it, give every TOC section a note
> too (Step 3 default already leans that way).

## Prerequisites (read first)

- **Required** — `python` + `pypdf` (text extraction fallback) and the bundled scripts in
  this skill folder (`digest_pdf.py`, `kb_coverage_status.py`). Both are pure file I/O — no
  kernel boot, safe to run while the daemons are up.
- **Optional** — `pdftoppm` (or the Read-as-image path) for scanned/image-only PDFs.
- **The daemon is NOT required.** Notes are written as direct file writes and picked up by
  VaultIndex on `vault:changed` — no restart. The only daemon call is the Step-7 citation
  check (`POST /kb/api/resolve-reference`); skip it and note so in the report if the daemon
  is down. Use `127.0.0.1:9000`, never `localhost` (IPv4-only bind); private mode needs
  `Authorization: Bearer <token>` from `emptyos.toml [network] auth_token`, and non-ASCII
  bodies go via Python `urllib`, never `curl -d`.

## Why this skill exists (two failure modes it prevents)

- **Under-coverage** — writing notes for the sections you happened to read instead of
  the document's actual structure. The coverage ledger makes the full clause inventory
  explicit so every section gets a keep/fold/skip decision — and, being durable, makes
  "did I actually finish this document" a fact you can check later instead of remember.
- **PII / watermark leak** — publisher stamps (IEEE Xplore download lines, ENA
  per-delivery watermarks carrying a third party's name+email) ending up in the vault.
  `digest_pdf.py` strips known stamps and **hard-fails (exit 3) if any residue
  survives** — nothing is written until extraction is clean.

## KB layout (current — do NOT use the stale `30_Resources/KB/...` paths)

| Layer | Path | kind |
|---|---|---|
| Full text | `{vault}/30_Resources/EmptyOS/kb/sources/_fulltext/<SLUG>.md` | — (verbatim source) |
| Coverage ledger (durable, resumable) | `{vault}/30_Resources/EmptyOS/kb/sources/_fulltext/<SLUG>.coverage.md` | — (todo/status table, not indexed) |
| Reference landing | `{vault}/30_Resources/EmptyOS/kb/notes/<slug>.md` | `reference` |
| Clause / worked example | `{vault}/30_Resources/EmptyOS/kb/sources/<slug>.md` | `clause` / `case` |

The kb app indexes these via VaultIndex on `vault:changed` — **no daemon restart needed**.

## Workflow

### Step 1 — Identify + run the extractor

Read the PDF's first 1–2 pages to get the **standard id**, **full title**, **edition/year**,
and **copyright holder**. Pick a `<SLUG>` (e.g. `IEEE_1547_2018`, `ENA_EREC_C55_2014`); the
note `<slug>` is the same lowercased with `_`→`-` (e.g. `ieee-1547-2018`). Then:

(If you can't render the PDF — e.g. `pdftoppm`/Read-as-image is unavailable — extract the
first pages' **text** instead: `python -c "import pypdf; r=pypdf.PdfReader(r'<pdf>'); print(r.pages[0].extract_text())"`.)

```bash
python skills/vault-source-digest/digest_pdf.py "<pdf>" \
  --slug IEEE_1547_2018 \
  --title "IEEE Std 1547-2018 — Interconnection and Interoperability of DER ..." \
  --copyright "(c) 2018 IEEE. All rights reserved." \
  --standard "IEEE Std 1547-2018"
```

- **Exit 3 = PII residue. STOP.** Read the offending lines it prints, add a
  `--strip-extra "<regex>"` for the publisher's stamp, and re-run. The full text only
  lands on a clean pass. (IEEE Xplore + ENA delivery watermarks are already built in.)
- **Exit 4 = a full text for this standard already exists.** The script searches BOTH
  the canonical `_fulltext/<SLUG>.md` layout AND the legacy per-standard subdir
  (`<slug>/<slug>-fulltext.md`, cited via `local_text:`) and refuses to write a duplicate.
  It prints the existing path(s). **Reuse that path** as the `source_file:` for your new
  clause notes — do NOT re-extract. Re-run with `--force` only to deliberately replace/
  migrate (then delete the old copy and repoint notes). This is the duplicate-fulltext
  trap; honour it.
- On success it writes the full text and the **coverage ledger** — saved into the vault at
  `_fulltext/<SLUG>.coverage.md` (sibling of the full text, `--coverage-out` overrides), an
  ID-keyed table with a `Status` column, all rows starting `pending`. Step 3 works through it.
- **The ledger is written ONCE.** Re-running the extractor on a slug that already has a
  ledger does NOT overwrite it (it may carry in-progress `Status` from a partial digest) —
  you'll see a "LEDGER ALREADY EXISTS" notice and nothing changes. Pass `--regen-coverage`
  only when you intentionally want to reset every row back to `pending` (this destroys any
  recorded progress — never pass it mid-digest).
- Use forward slashes in paths (Windows). Non-ASCII in `--title`/`--copyright` is fine.

### Step 2 — Reconcile against existing KB (time-dimension rule)

**First, check for an existing coverage ledger** at
`{vault}/30_Resources/EmptyOS/kb/sources/_fulltext/<SLUG>.coverage.md`. If it exists,
read it and filter for `Status: pending` rows — this **replaces** the manual ls-and-diff
below for any standard that was digested with a ledger. Jump straight to Step 3 with the
pending rows. See "Resuming a partial digest" below for the full same-session vs.
fresh-future-session shape.

For standards digested **before** the ledger existed (no `.coverage.md` on disk) or where
the TOC couldn't be auto-parsed at all, fall back to manual reconciliation. Before writing
anything:

```bash
ls "{vault}/30_Resources/EmptyOS/kb/sources/" | grep -i <standard-stem>
ls "{vault}/30_Resources/EmptyOS/kb/notes/"   | grep -i <standard-stem>
```

**Reconcile the full-text artifact first.** A prior digest may have filed the full text
under the legacy `<slug>/<slug>-fulltext.md` subdir (with a `local_text:` field) rather
than canonical `_fulltext/<SLUG>.md`. The extractor's exit-4 guard catches this, but if
you find a complete, PII-clean copy under *either* layout:

- **Reuse it.** Point new clause notes' `source_file:` (or `local_text:`) at the existing
  path. Do NOT create a second copy — two full-texts for one standard is the trap this
  guard exists to prevent. If you accidentally extracted a duplicate, delete *your* new
  copy and keep the established one (its `[[wikilinks]]` are already wired).
- **Match the existing convention.** If the prior digest used `standard: "IEEE Std 738"` +
  `edition: "2023"` (year split out) and slug pattern `ieee-738-2023-N`, follow it so
  nothing forks — even if it differs from the templates below. Consistency with the
  filed corpus beats the canonical default.

Then the clause/note layer:

- If clauses already exist → **don't duplicate**; add only what's missing.
- If metadata conflicts with the PDF (real example: TB 963 notes said *2024 / WG B1.72*
  but the actual brochure is *2025 / WG B1.87*) → **correct the existing notes in place**
  (keep filenames so `[[wikilinks]]` don't break) and say so in your report. Don't fork.

### Step 3 — Drive coverage from the ledger (not from what's easy)

Open `<SLUG>.coverage.md`. For **every `pending` row**, decide **keep-as-clause /
fold-into-another / skip**, and **log skips with a one-line reason**. Default policy —
**lean toward complete coverage**:

- **Keep** a clause note for every section that carries content — numbers, rules, methods,
  tables, limits. **Including definitions and informative annexes**: these routinely hold
  real substance (a radial-gradient method, a thermal-time-constant derivation, a
  covered-conductor extension, a worked example) and should get their own note, not be
  waved off as "annex boilerplate."
- **Expand** to a sub-clause when it carries distinct rules worth its own note (e.g. a
  formula-heavy `§4.4` splitting into convection / radiation+solar / resistance notes).
- **Worked examples → `kind: case`**; a **bibliography → a short provenance note** listing
  which sources back which clauses (it's useful, not noise).
- **Skip** only pure legal/navigation front-matter: cover, title page, participants,
  contents, foreword, legal disclaimers. **Fold** only genuine duplicates (e.g. an
  informative annex that merely restates a normative clause). Everything else gets a note.

The ledger's `skip?` hints flag boilerplate *candidates* — they are NOT a licence
to skip. Coverage should be **proportional to the document** (the suggested band is a floor,
not a ceiling). When the user says "don't skip" / "full coverage", give **every** TOC row a
note (front-matter excepted) and say so in the report.

**Ledger ownership — who writes Status, and when.** Only the **orchestrating session**
edits the ledger's `Status` column, via `kb_coverage_status.py`:

```bash
python skills/vault-source-digest/kb_coverage_status.py "<ledger-path>" \
  --set 5 written:cigre-tb-669-2016-3-1-1 \
  --set 6 skipped:pure-navigation-front-matter
```

If you fan work out to parallel sub-agents (large document, many clauses — see the TB 669
precedent), each sub-agent writes its own batch of clause notes and reports back which
`(ID, slug)` pairs it finished in its final message. **Sub-agents never touch the ledger
file directly.** The orchestrator applies each report's updates sequentially as
notifications arrive — this is what keeps a parallel fan-out race-free without any file
locking: there is exactly one writer, ever.

### Step 4 — Create the reference landing note

`{vault}/30_Resources/EmptyOS/kb/notes/<slug>.md`:

```yaml
---
tags:
  - kb
kind: reference
domain: <e.g. grid-connection | cable-thermal>
topic: <e.g. der-interconnection>
standard_id: "IEEE Std 1547-2018"   # aggregator key — KB pulls every clause whose `standard:` matches
title: IEEE Std 1547-2018 — <short title>
year: 2018
working_group: <if applicable>
related: [<clause-slugs>, <sibling-refs>]
created: <today>
updated: <today>
---
```

Body: what it is / what it provides / when to use / when not / companion standards /
**Source artifacts** (link the `_fulltext/<SLUG>.md` + list clause digests) / **Copyright**
(state it's a paraphrased personal study aid, not a reproduction).

### Step 5 — Create clause / case notes

Each in `{vault}/30_Resources/EmptyOS/kb/sources/<slug>.md`. **Frontmatter contract**
(verified against `apps/public/standard/kb/shared.py` + `indexes.py` — the citation parser matches on
`standard`/`edition`/`clause`, NOT on the slug):

```yaml
---
tags:
  - kb
kind: clause            # or: case (worked example)
domain: <same as reference>
standard: "IEEE Std 1547-2018"   # MUST share the reference's standard_id family
edition: "2018"                   # year string; omit for edition-independent matching
clause: "6.4"                     # the parser strips §, lowercases, collapses whitespace
clause_title: "<section name>"
source_file: "30_Resources/EmptyOS/kb/sources/_fulltext/<SLUG>.md"
title: "<Std> §<clause> — <topic>"
related: [<slugs>]            # PRIMARY cross-link — always resolves via the graph
references: ["<Other Std>:<ed> §<clause> (<desc>)"]   # bonus: auto-resolves IF the publisher is in the grammar
created: <today>
updated: <today>
---
```

**Cross-linking — two channels, different reliability:**
- `related: [<slug>]` (or `[[slug]]`) — the **always-reliable** link; resolves on the slug
  directly. Use it for every cross-link you want.
- `references: ["<Std>:<ed> §<clause>"]` — free-text, auto-resolved by the kb app's citation
  parser **only for publishers in its grammar**: IEC, CIGRE TB, AS/NZS, IEEE (incl. `IEEE Std
  1547-2018`), and ENA EREC. For any **other** publisher the string is inert until you add an
  alternative to `_CITATION_RE` in `apps/public/standard/kb/shared.py` (one line; then restart the daemon).
  Don't rely on `references:` alone for cross-app links — pair it with `related:`.

Body shape (match the existing corpus, e.g. `cigre-tb-880-2022-4-3-2.md`): a **Substance**
section (paraphrased — real numbers/tables, NOT verbatim copyright text), a **Why it matters**,
a **Source** line (standard + clause), and **Citing notes** (`[[wikilinks]]`).

Write notes by **direct file write** (these are the vault file tools / `vault_create_note`) —
the kb app's `create_note()` API does not bulk-create clauses; direct write is the path that
indexes correctly. No `author:` field (matches the existing KB corpus; the full-text header
already carries provenance).

### Step 6 — Cross-link both directions

Add the new clause slugs to the reference's `related:`, and add `references:` strings between
clauses that cite each other. Apply any Step-2 metadata corrections now.

## Resuming a partial digest

A large document doesn't need to finish in one sitting or one fan-out. The coverage ledger
IS the resumable state — there is no separate progress file to maintain.

**Same-session continuation** (you paused, or a batch of sub-agents just reported back):
the ledger is already current — re-open it, filter for `pending`, and keep going from
Step 3. Nothing else to reconstruct.

**Fresh future session** ("continue digesting <standard>", days or weeks later):

1. Locate the ledger: `{vault}/30_Resources/EmptyOS/kb/sources/_fulltext/<SLUG>.coverage.md`.
   If it doesn't exist, this standard predates the ledger mechanism or its TOC couldn't be
   auto-parsed — fall back to Step 2's manual ls-and-diff reconciliation instead.
2. Filter for `Status: pending` rows. Step 1 (extraction) is already done — skip straight to
   Step 3 for the pending rows only.
3. **Spot-check a couple of `written:<slug>` rows** actually resolve to real files on disk
   before trusting the ledger wholesale (`ls {vault}/30_Resources/EmptyOS/kb/sources/<slug>.md`)
   — cheap insurance against a ledger edit that didn't land for some reason.
4. Do **not** pass `--regen-coverage` to `digest_pdf.py` for an in-progress standard — that
   resets every row (including `written:`/`skipped:` ones) back to `pending` and discards
   the very state you're trying to resume from.

### Step 7 — Verify + report

- **Full text is complete** (the artifact the user cares about most): confirm the page-marker
  count equals the PDF page count and the last marker is `Page N of N` —
  `grep -c "<!-- Page" <fulltext>` (or `grep -c "PDF page"` for the legacy layout). Then
  spot-check that the "skipped-as-notes" sections are still *present in the text*: grep the
  full text for each annex / definitions heading. The verbatim text must contain **every**
  section even when those sections didn't earn a clause note.
- **PII = 0**: `grep -c "@" <fulltext>` should be 0 (or only legitimate in-standard emails —
  eyeball them).
- **Ledger fully resolved**: no `Status: pending` rows remain — every row reads
  `written:<slug>` / `skipped:<reason>` / `folded-into:<slug>`. (If some are deliberately
  left `pending` because the digest is being paused mid-document, say so explicitly in the
  report instead of silently under-reporting — see "Resuming a partial digest.")
- **KB indexed it** (no restart): if the daemon is up, spot-check a citation resolves.
  `POST /kb/api/resolve-reference` body `{"reference": "<string>"}` → `{slug, matched, …}`.
  Two gotchas that made first attempts fail this session:
  - **Use `127.0.0.1`, not `localhost`** (urllib resolves `localhost`→IPv6 `::1`; the daemon
    binds IPv4). `network.mode = private` → add `Authorization: Bearer <token>`
    (token at `emptyos.toml [network] auth_token`). POST non-ASCII (`§`) bodies via Python
    `urllib`, not `curl -d` (Windows mangles UTF-8 → cp1252).
  - **Citation string format:** the parser only matches `kind: clause` notes (not `case` /
    `reference`), and the **year must be colon/space-separated, not hyphenated**:
    `IEEE Std 738:2023 §4.4.3` ✅ resolves; `IEEE Std 738-2023 §4.4.3` ❌ (the `-2023` is
    absorbed into the standard token). So a whole-standard or case-note citation legitimately
    returns `matched: false` — verify against a real **clause** note.
- **Report**: counts (reference + N clauses + M cases), confirmation the full text is complete
  (page count), which TOC rows were skipped/folded and why, and any metadata you corrected.

## Multiple PDFs

Loop Steps 1–7 per PDF. Report which were net-new vs already-covered, and flag any whose
existing KB metadata you corrected.

**Folder convention (reconcile before batch-digesting):** a source drop may use a sibling
`logged in vault/` subfolder to mark **already-digested** sources — files in the top-level
folder are the to-do pile; ones moved into `logged in vault/` are done. Before digesting a
batch, list both and cross-check against the KB (`ls .../kb/sources | grep -i <stem>`) so you
don't re-digest. Subfolders of *software/tool manuals* (e.g. CDEGS/SES product guides) are
usually **not** standards and not KB-clause material — confirm scope before processing them.
When a "continue" spans many heterogeneous documents (standards vs papers vs manuals), it's
worth one scope check rather than digesting the wrong dozens.

## When NOT to use this skill

- Pasted **chat transcripts** → that's `eos-ai-conversation-ingest`, not this.
- **Scanned/image PDFs** (no text layer) → `digest_pdf.py` exits with "no extractable text";
  OCR is out of scope.
- A quick one-off lookup where no durable KB note is wanted → just read the PDF.

## Files

- `digest_pdf.py` (bundled) — extractor + watermark/PII hard-gate + TOC coverage ledger.
- `kb_coverage_status.py` (bundled) — mechanical, ID-addressed `Status`-cell updater for
  the coverage ledger. Only the orchestrating session runs this (see Step 3).
- Reuses the repo's `.eos-personal` (best-effort) as an extra PII detector on top of the
  built-in email/watermark scan.
