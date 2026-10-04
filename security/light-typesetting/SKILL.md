---
name: light-typesetting
description: Build and preflight submission-ready LaTeX/PDF artifacts for Light stage 11. Use when receiving a paper-writing manuscript, figure delivery, citation delivery.json/references.bib/citekey-audit.json, or a venue/template profile; when selecting pdfLaTeX/XeLaTeX/LuaLaTeX and BibTeX/Biber; when diagnosing LaTeX errors or unresolved references; when checking page limits, double-blind identity, PDF metadata, template, page box, embedded fonts, TODOs, figures, tables, labels and citations; or when producing a reproducible compile manifest, PDF, compliance report, failure bundle and venue-matching handoff. Distinguishes PASS, manuscript ERROR, toolchain UNAVAILABLE and convergence UNRESOLVED without redoing citation authenticity or figure scientific QA.
---

# Typesetting · stage 11

Turn approved author artifacts into a reproducible PDF submission bundle. The
job is not merely to make LaTeX compile: preserve provenance, select a coherent
engine/backend, preflight dependencies, compile to convergence, locate the
first root cause, run profile-driven desk-reject checks, and hand exact PDF/page
facts to venue-matching.

Read `typesetting-resource-map.md` before running a real build. Read
`references/build_contract.md` before writing or consuming machine artifacts.
Use `references/latex_errors.md` only after the first source-located error is
known. Use a venue template under `templates/` only when it matches the current
author kit; the bundled copy is a starting point, not current venue truth.

## Non-negotiable boundaries

- Consume citation `delivery.json`, `references.bib` and
  `citekey-audit.json`. Require `delivery.status=DELIVERED`, declared
  `deliverable_hashes`, empty citation failures and empty claim-review
  leftovers. Declared citation deliverables must be relative paths inside the
  citation delivery directory, and the build snapshot must preserve the audit,
  failure and claim-review sidecars under provenance. Check staged keys and
  compilation. Do not re-decide DOI existence, metadata conflicts, retractions
  or claim relevance.
- Consume figure files, declared dimensions/DPI and source manifest. Require
  the manifest to be `light.figure_delivery.v1` or `light.figure_build.v1` and
  require the embedded file hash to match a declared output hash. For empirical
  figure deliveries, require confirmed result-analysis evidence binding. Check
  presence, embedding, float/layout and compilation. Do not redo visual
  honesty, scientific content or publication-size generation.
- Consume the approved paper-writing manuscript. Do not invent claims,
  references, experiments or numbers to close a page budget.
- Take page, anonymity, template, font and page-box rules only from user input
  or current authoritative instructions with URL/date provenance. Never embed a
  universal venue limit.
- Keep tool/resource failure as `UNAVAILABLE`. Never call it manuscript
  `ERROR`, never call it `PASS`, and never mark the delivery `DELIVERED`.
- Keep stage-11 critical scope to typesetting. Security/network/tool
  unavailability does not enlarge it. `ROUTES` has no key 11; repair failures
  inside stage 11 and never invent a back-edge.

## Local LaTeX environment contract

For a real PDF build, detect the local toolchain before claiming success:

- core: Python stdlib plus a LaTeX distribution such as TeX Live, MiKTeX,
  MacTeX or TinyTeX;
- compile driver: prefer `latexmk`; use `tectonic` only when its supported
  backend matches the manuscript;
- engines: `pdflatex`, `xelatex` and `lualatex` as selected from source/profile
  triggers;
- bibliography: `bibtex` for traditional `\bibliography{}` and `biber` for
  `biblatex` unless explicitly declared otherwise;
- PDF checks: `pdfinfo` and `pdffonts` when page box, page count or embedded
  font facts are required.

If the compiler, engine, backend, package or PDF inspector is missing, mark the
state `UNAVAILABLE`, explain the missing component, and ask the user whether to
install/configure it or switch toolchains. Never silently install system tools,
never call a missing toolchain a manuscript error, and never report a PDF as
delivered unless the build actually produced and checked that PDF.

## Workflow

### 1. Freeze the input contract

Copy `templates/typesetting_input.json`. Record:

- the paper-writing entrypoint plus every required source file;
- each figure source, target relative path, dimensions/DPI and delivery/build
  manifest;
- citation `delivery.json` and desired staged BibTeX filename; the delivery
  must be regenerated after citation edits so hashes match the referenced
  files;
- `light.typesetting_venue_profile.v1`, including source kind, URL if any,
  check date and rules.

If a venue rule is unknown, keep it `null`, `0` or absent. Do not infer it from
another venue or last year's template.

### 2. Preflight before compilation

```powershell
python scripts/build_submission.py --spec typesetting-input.json --preflight-only
```

Require a provenance-preserving `source/` snapshot. Check missing inputs,
`\input`/`\include`, graphics, labels/refs, citation-delivery schema/status,
deliverable hashes, delivered citekey audit, empty citation failure/review
handoffs, live staged citekeys, figure manifest output hashes, empirical
figure evidence binding, document class, required packages and local package
availability. Use a new/empty output directory per iteration; the builder
refuses stale run directories.

Classify:

| Evidence | State |
|---|---|
| missing manuscript/figure/BibTeX/key/label, stale upstream hash, open citation review, unconfirmed empirical-figure evidence or backend conflict | `ERROR` |
| required engine/backend/package/tool absent or cannot execute | `UNAVAILABLE` |
| no blocker | `PASS` |

### 3. Select engine and bibliography backend

Detect XeLaTeX for `fontspec`, `xeCJK`, `ctex`, `unicode-math` or
`polyglossia`; LuaLaTeX for Lua triggers; otherwise pdfLaTeX. Detect
traditional `\bibliography` as BibTeX and `biblatex` as Biber unless its
`backend=` option says otherwise.

If the profile engine conflicts with a hard XeLaTeX/LuaLaTeX source trigger,
or its backend differs from the source, stop with a root-cause `ERROR`; do not
mix BibTeX and Biber. A profile may deliberately select XeLaTeX for otherwise
pdfLaTeX-compatible source. Record the absolute executable path, version probe,
working directory, command array and shell rendering.

### 4. Compile and classify convergence

```powershell
python scripts/build_submission.py --spec typesetting-input.json
```

Prefer local `latexmk`; use Tectonic only when its supported backend matches.
Compile from the snapshot's manuscript directory so relative inputs resolve.
Save `latexmk` rule/run records, log/PDF SHA-256 and page count.

Use exactly four compile states:

- `PASS`: return code zero, PDF exists, no remaining undefined cite/ref or
  rerun signal.
- `ERROR`: manuscript/backend/input caused a nonzero build or no PDF.
- `UNAVAILABLE`: required local tool/resource could not launch/finish.
- `UNRESOLVED`: PDF exists but citation/reference convergence remains.

`ERROR` and `UNRESOLVED` exit 1. `UNAVAILABLE` exits 0 for the command-gate
boundary but remains undelivered.

### 5. Diagnose from the first root cause

Read `compile-report.json`, then the full log. Report the first
`file.tex:line`, compiler message and plain-language cause before secondary
warnings. Fix the earliest error first; recompile after one minimal repair.
Never silently rewrite prose, remove data or add fabricated bibliography.

When a fix loop repeats the same signature, stop and report `UNRESOLVED`
instead of making speculative edits.

### 6. Run the profile-driven desk-reject gate

```powershell
python scripts/desk_reject_gate.py `
  --tex typesetting-build/source/paper.tex `
  --pdf typesetting-build/compile/paper.pdf `
  --bib typesetting-build/source/references.bib `
  --log typesetting-build/compile/paper.log `
  --profile venue-profile.json `
  --report desk-reject-findings.json
```

Objective profile breaches may be critical: over page limit, unanonymous
author/PDF Author metadata, wrong document class, missing required package,
wrong page size, or unembedded font. TODOs, acknowledgements, self-reference,
links and box warnings stay warnings unless the current authoritative profile
defines an objective hard rule.

Static checks cannot prove semantic anonymity, interpret ambiguous venue
language or judge final visual quality. Inspect the rendered PDF and current
official analyzer/instructions before submission.

### 7. Emit canonical artifacts

Require:

- `build-manifest.json`;
- `compile-report.json` and compile log;
- `compliance-report.json` and desk-reject findings;
- PDF when produced;
- `failure.json` for failed/unavailable runs;
- `venue-handoff.json`;
- `delivery.json`.

Only compile=`PASS`, compliance=`PASS` and zero compliance critical may become
`DELIVERED`.
Preserve failed reports; they prove the fail→fix transition.

### 8. Derive readiness without collapsing evidence

Build a local readiness packet and run:

```powershell
python scripts/submission_readiness.py `
  --input templates/submission-readiness.example.json --as-of YYYY-MM-DD `
  --out submission-readiness-report.json
```

The public template is intentionally `UNKNOWN` and must exit 1. The state chain
is `INVENTORIED → SOURCE_BUILDABLE → TECHNICALLY_CHECKED →
VISUALLY_CHECKED → METADATA_MATCHED → VENUE_READY → USER_APPROVED`.
Compile exit 0 cannot skip unresolved references, compile `page_count`,
same-PDF binding, per-page render/review, metadata anonymity, current official
profile or exact article-type binding. `visual.source_pdf_sha256`,
`metadata.source_pdf_sha256`, `compliance.source_pdf_sha256` and any
`user_approval.pdf_sha256` must equal `compile.pdf_sha256`; `visual.page_count`
must equal `compile.page_count`; each visual page row needs `render_sha256`,
`render_tool`, `review_status=PASS`, `reviewer`/`reviewer_id` and non-future
`reviewed_at`. The compliance row must also name the same `venue` and
`article_type` as the profile. Artifact
Available/Functional/Reusable/Reproduced/Replicated remain separate; the script
records evidence and never awards an ACM or venue badge.

### 9. Run stage 11 and hand off

Run the `compile` command gate and `desk_reject` findings checkpoint:

```powershell
python ../light-orchestrator/scripts/run_checkpoint.py `
  --file .light/passport.yaml --stage 11 `
  --gate "compile=python scripts/compile_driver.py --compile paper.tex --outdir build --json-out compile-report.json --quiet" `
  --findings desk-reject-findings.json --ts <ISO8601> --write
```

On critical fail, repair stage 11 and rerun to `delivered`. Hand
venue-matching the `venue-handoff.json` PDF path/hash, page count, page size,
profile source and compliance report. Do not claim `ROUTES[11]` or create a
back-edge. `--quiet` keeps the Windows command gate locale-neutral; the full
diagnostic record remains in `compile-report.json`.

## ACT / ASK / NEVER

ACT:

- Snapshot declared inputs before modification.
- Run preflight, compile, rendered-PDF review, desk-reject gate and checkpoint.
- Preserve exact commands, hashes, statuses and failure artifacts.

ASK:

- Ask when a venue rule/source is missing or ambiguous.
- Ask before scientific-content cuts, changing bibliography systems, or
  replacing the user's official template.
- Ask for human confirmation of semantic anonymity and borderline layout.

NEVER:

- Never claim a compile, convergence, page count or metadata check that did not
  run.
- Never treat missing tools as a manuscript error or a successful delivery.
- Never redo citation authenticity, figure scientific QA or paper-writing.
- Never depend on paid Overleaf, private keys, browser plugins or npm-heavy
  tooling for the core path.

## Delivery self-check

- Input provenance and SHA-256 rows cover manuscript, figures, figure
  manifests, citation delivery/BibTeX/audit/failure/review artifacts and
  profile.
- Citation delivery status is `DELIVERED`; deliverable hashes match staged
  files; citation failures and claim-review leftovers are empty.
- Figure source manifests declare the embedded output hash; empirical figures
  carry confirmed result-analysis evidence binding.
- Engine/backend selection agrees with source and profile.
- Compile status is one of the four canonical states; PASS has a hashed PDF.
- Root cause has file/line when the compiler exposes it; warnings are separate.
- Citekeys, figures, labels and cross-references converge.
- Desk-reject criticals are zero or delivery is not marked delivered.
- Every visual/metadata/compliance/user-approval row is bound to the compiled
  PDF hash; every PDF page has a render hash, render tool, reviewer/date and
  review PASS row; profile is current and bound to the exact article type.
- Author-team repeatability was not relabelled independent reproduction/replication.
- Venue-matching receives real PDF/page/compliance facts.
- Stage 11 uses only `compile` and `desk_reject`; no route/back-edge was added.
