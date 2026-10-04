---
name: build-overview
description: Generates an experiment-overview snapshot of all research questions under research/reports/. Invoke when a new point-in-time report across all RQs should be produced.
disable-model-invocation: false
allowed-tools: Bash(./experiments/generate-snapshot-skeleton.py:*) Read Write Glob
---

# /build-overview — produce an experiment-overview snapshot

You produce a frozen, publishable research report from the current state of every `findings.md` under `research/questions-claude/`, `research/questions-opencode/`, `research/questions-cross/`, and `research/workflow-dev/`. The snapshot lands as a new file under `research/reports/experiment-overview-YYYY-MM-DD.md`.

## Core principle

`findings.md` = living document, growing list of status-tagged findings.
Snapshot = frozen, table-heavy report at a point in time.

Both exist in parallel. The snapshot is **not written from memory** — it is filled in from an auto-generated skeleton.

## Prerequisites

Required on `$PATH` for the Markdown snapshot (steps 1–5):

- `python3` — runs `experiments/generate-snapshot-skeleton.py`

Only needed when the user asks for a PDF (step 6):

- `pandoc` — Markdown → HTML (any version ≥ 2.9 works)
- `google-chrome` (or `chromium` — adjust the binary name in step 6) — headless `--print-to-pdf`
- `pdfinfo` (Poppler utils) — optional, used for the PDF verification check

If a PDF was requested and one of its tools is missing, finish the Markdown snapshot and report which tool is unavailable so the user can install it — do not treat it as a failure of the whole run.

## Lifecycle (6 steps)

### Step 1 — generate the skeleton

Bash:

```bash
./experiments/generate-snapshot-skeleton.py
```

**Before trusting the output, verify the script sees every RQ subtree.** `RQ_TREES` in `generate-snapshot-skeleton.py` is a hardcoded list. When a new subtree appears under `research/` (a new harness family, a new question class), the script silently omits it — no warning, no error, just a smaller snapshot. Cross-check the RQ count against the filesystem before proceeding:

```bash
# every dir with a README.md carrying an `id:` is an RQ
find research -mindepth 2 -maxdepth 2 -name README.md | xargs grep -l '^id:' | wc -l
./experiments/generate-snapshot-skeleton.py 2>&1 | grep 'RQs:'
```

If the two numbers disagree, add the missing subtree to `RQ_TREES` and regenerate — do not hand-patch the skeleton. (This bit in 2026-07: `questions-pi/` and `questions-cursor-cli/` were missing, which would have dropped 3 RQs and 140 runs from the report.)

The script writes to `/tmp/snapshot-skeleton-YYYY-MM-DD.md`. It auto-fills:

- Data-base count (from `experiments/runs/`)
- **Author line** — Marco Emrich, with EXACT-Coding co-credit "together with Ferdinand Ade". Two links, and they must not be swapped: the **name** links to the LinkedIn profile (<https://www.linkedin.com/in/marco-emrich>), **"EXACT Coding"** links to the book (<https://leanpub.com/exact-coding>). Link text and target have to match — a person's name pointing at a book, or a book title pointing at a profile, is wrong in a published document.
- **Repository link** (github.com/marcoemrich/agentic_coding_lab)
- **`## About the Study`** H2 — only the heading; the two flowing paragraphs underneath are TODO-markers (filled in step 3)
- **`### Scope`** H3 sub-heading — TODO-marker (filled in step 3)
- **`### AI Disclosure`** H3 sub-heading — full text is static
- **`## Key Findings`** H2 — TODO-marker (filled interactively in step 4)
- §1 Research-question overview table with per-RQ coverage (data-driven, regenerated from frontmatter)
- §2.1 Experiment-design tables: Workflow, Model × Thinking, Kata × Prompt style — all static
- §2.1 **workflow mechanics in detail** block — static, one bullet per workflow generation
- §2.2 Workflow → prompt mapping table — static
- §3 Methodology block — static, with a freshness-check TODO marker
- §3.2 **metric tables** (six grouped tables: Correctness, Efficiency, Code Mass & Size, Code Quality, Test Strength, TDD Discipline) — all static
- §3.3 Evaluation principles — static
- §4 Per RQ: heading + Data basis line + raw finding list + per-RQ synthesis TODO (current state, no status tags)
- §7 Reproducibility block — static
- §8 Files table — data-driven

Wherever Claude must fill in content, a `<!-- TODO Claude: ... -->` marker is left in place. **Everything else is static skeleton content — do not edit it during synthesis.** Concretely: Author / Repository / AI Disclosure blocks, all §1 / §2 / §3 / §7 / §8 tables and prose, and the workflow-mechanics block must stay byte-identical to what the skeleton produced.

### Step 2 — read the skeleton + every findings.md

Read the skeleton (`/tmp/snapshot-skeleton-YYYY-MM-DD.md`) and **every** `findings.md` under `research/questions-claude/*/`, `research/questions-opencode/*/`, `research/questions-cross/*/`, and `research/workflow-dev/*/` (skip dirs starting with `_`). Note for each RQ the current findings with their statement and data values.

`open-questions.md` (when present) does **not** go into the snapshot — those are internal backlog items for future batches, not publishable state.

### Step 3 — fill in the synthesis sections (except Key Findings)

Replace every `<!-- TODO Claude: ... -->` marker with real content — **except** the `## Key Findings` TODO, which is handled interactively in step 4. **Never leave any other TODO marker in place.**

Style requirements:

- **Glossary discipline:** Before step 3, read the glossary in the top-level `README.md`. Use terms like `code_mass`, `cc_loc`, `cc_longest_function`, `smell_total`, `verification_pct` only in the binding form defined there ("Code Mass (APP)", "Production LoC", "Smell Total", "Correctness (external)") or directly via the metric ID in backticks. Synonyms like "code volume", "total code size", "LoC size" — and the retired German forms ("Code-Mass", "Smell-Summe", "Produktiv-LoC", "Korrektheit (innen/außen)") — are forbidden: they are ambiguous or collide with established definitions (APP). The three complexity metrics carry **no** prose name at all — write `cc_longest_function`, `cognitive_max`, `cognitive_avg` or `mccabe_max` in backticks. "Complexity Peak", "Spitzen-Komplexität", "Cognitive Complexity peak" and "McCabe peak" are forbidden; the first of those had been used for three different metrics at once.
- **`## About the Study` (H2):** Two flowing paragraphs (no sub-headings between them):
  - **Paragraph 1 — EXACT Coding anchor.** Lab as the empirical validation platform for **EXACT Coding** (EXample-guided AI-Collaborative Test-driven Coding) — link the published book at <https://leanpub.com/exact-coding>. Never reference a local manuscript path; the snapshot is a public document and must not point at private filesystem locations. Position the workflow variants as a spectrum from Vibe-Coding baselines (v1/v2) over EXACT-conformant setups (v4/v6) to the Delayed-Refactor control (end-refactor-only).
  - **Paragraph 2 — Snapshot status.** Date, run count, RQ count, current research front. **Never use workflow version names (`v6.1-hybrid` etc.) here** — workflows are not yet introduced in §2.1; describe by mechanism instead (e.g. "hybrid workflow with skill-based red/green in shared context + isolated refactor subagent").

- **Reporting a subset of RQs.** The user may ask to leave a whole subtree out — most often `workflow-dev/`, which is tool-development on the measuring apparatus and hard to read without knowing the workflow version history. That is a legitimate editorial call, but it must be **visible, not silent**. When you drop a subtree:
  - Remove it in three places, not one: the §1 overview table block, the §4 sections, and the §8 files rows. Grep for leftovers afterwards (`grep -n '<subtree>' <snapshot>`) — some references are legitimate (methodology pointers in §2/§3/§7), so read each hit rather than deleting blindly.
  - Recompute the reported totals. The header, the intro paragraph and any "N research questions" phrasing must state the *reported* count, not the lab total. Derive both from the file itself:
    ```bash
    grep -c '^#### ' <snapshot>                                    # reported RQs
    python3 -c "import re,sys;print(sum(int(m) for m in re.findall(r'_Data basis: (\d+) runs',open(sys.argv[1]).read())))" <snapshot>
    ```
  - Say in the header and intro *what* was left out, *how large* it is, and *where it lives* — a reader who later finds 32 RQs in the repo but 19 in the report must be able to reconcile the two without asking.
- **`### Scope` (H3 sub-heading inside About the Study):** The three-axis scope named explicitly: (1) **Harness** — which agent CLIs, at which pinned versions, headless without HITL; (2) **Models** — which providers and families; (3) **Target language** — the per-run stack. State explicitly that findings hold **for** this stack and name what stays open (other target languages, interactive HITL setups, non-synthetic codebases).

  **Derive all three axes from the data, never from this skill's prose.** The scope is the fastest-drifting part of the whole document — each new harness or provider family silently invalidates it. Read the actual values before writing:

  ```bash
  grep -n 'npm install -g' experiments/docker/Dockerfile     # harness pins
  ls -d research/questions-*/                                 # harness families with RQs
  grep -h '^\s*model' research/questions-*/*/README.md | sort -u | head -40
  ```

  A stale scope is worse than a vague one: it tells readers the study is narrower than it is, and it reads as sloppiness precisely to the readers who check. (This bit in 2026-07: the skill still prescribed "only Claude Code CLI, only Anthropic models" while the data already spanned four harnesses and a dozen third-party models.)

  Do the same for the **HITL framing** — it is the one scope limit that never drifts, and it is worth more than one sentence. Several documented correctness losses are failure modes a single human question would catch (premature self-termination, incomplete test lists, mis-guessed CLI contracts). Say so: the numbers bound *unattended autonomy*, they are not a ceiling for supervised use.
- **Methodology (section 3):** Skeleton content is static. Verify against `experiments/docker/Dockerfile`, `experiments/analyze-run.sh`, `experiments/aggregate-by-query.py` whether the pipeline description is still accurate. On drift, correct in the snapshot. Replace the `<!-- TODO Claude: check whether still current ... -->` marker with either a brief confirmation ("pipeline unchanged since ...") or the corrected steps.
- **RQ sections (4.X):** Two artefacts per RQ, in this order:
  - **Overview table from `findings.md`** copied verbatim into the snapshot, placed directly after the `_Data basis: …_` line and before the `**Findings**:` list. Each findings.md carries an "Overview" or headline table near the top; copy it (with its caption + 🏆 markers) so readers see the numbers without leaving the snapshot. If a findings.md exposes two parallel overview tables (e.g. one per kata, as in RQ-tdd-quality), copy both.
  - **Synthesis paragraph** of 60–100 words after the `**Findings**:` list. Top finding in detail + at most one caveat from the finding itself (e.g. narrow data base, only one kata) + an explicit `[research/.../findings.md](relative/path)` link. Where coverage < 100 %, name it in the synthesis ("with currently N runs in M of K cells ...").
- **Model identifiers must carry their version.** A reader of the snapshot alone — with no access to the repo — must be able to tell *which* model produced a number. Most lab-variant IDs are self-describing (`glm-5-2`, `gpt-5-6-sol`, `opus-4-8-no-thinking`) and need nothing extra. Some are not: the cursor-cli arm uses `opus-cursor` / `composer-cursor` / `grok-cursor`, which name a family but no version. Wherever an RQ's table columns use version-less IDs, add a one-line mapping under the `_Data basis: …_` line — e.g. "Model IDs: `opus-cursor` → `claude-opus-4-8-medium`, …" — and make the §4 heading question name the versions too. The authoritative mapping is the `case "$model_name"` block in `experiments/docker/run-batch.sh` (and the RQ README's `factors.model` comments); never guess a version from the label.
- **Verbatim-copy applies to numbers, NOT to causal claims.** The "copy verbatim" rule protects against *fabricated numbers* — it does **not** make a finding's *causal/mechanistic sentence* trustworthy. A `findings.md` statement can carry a correct table and a wrong attribution. Before you promote any "factor X causes outcome Y" sentence (especially into Key Findings):
  - **Run the counter-cell check.** Workflows bundle several factors at once (spec style, test phase, refactor cadence, context isolation). Find the matrix cell that has X but *not* Y, or Y but *not* X — it is usually already in the table you just copied. Example from this lab: the periodic-refactor workflows score high on *both* correctness and quality, but `inline-tdd` (naive "use TDD", no enforced refactor cadence) reaches `verification_pct = 1.00` too — so correctness comes from spec + test-phase, and only quality comes from the refactor cadence. Two bundled levers, not one.
  - **Verify inherited mechanism sentences against the workflow definition.** When a finding describes *what a workflow does* ("Minimal-TDD without refactor phase"), check it against the actual workflow def (`experiments/workflows/<wf>/.claude/...`). `inline-tdd` is "a single agent told only *use TDD*, deciding its own structure" — calling it "TDD without a refactor phase" implies a controlled isolation that was never built. Describe what the workflow *is*, not a tidy abstraction of it.
  - Carry the inherited statement only after both checks pass; otherwise correct it in the synthesis (and flag the source `findings.md` to the user so the living doc gets fixed too).
- **Findings convention:** Snapshot shows **only the current state**. No status tags like `⚠️ bedingt` / `✅ stabil`, no comparisons with archive snapshots or older studies (e.g. the 235-run study). If findings.md still carries such status tags, drop them in the snapshot synthesis and only carry over the current statement. Reason: older runs had pipeline biases (see memory), comparisons are methodologically not robust.
- **Trophy convention (🏆) in cross-RQ summary tables:** If the snapshot includes pivot tables comparing workflows or models across outcomes, append 🏆 to the best value per row alongside the bold winner. Metric direction must be explicit (`smell_total` → "lower = better", `refactorings_applied` → "higher = better"). Award 🏆 only where the spread is meaningful — tied values get tied trophies, no winner gets fabricated from rounding noise. Same rule as in `findings.md` headline tables; see `run-rq` SKILL "Overview table" section for the full convention.
- **Cross-RQ synthesis (5):** 3–5 numbered points. Each point connects at least **two** RQs and would therefore not stand in any single findings.md.
- **Limitations (7):** 5–8 bullets. Mandatory: only Anthropic models, only synthetic katas, only TypeScript, headless without HITL, n ≤ 3 per cell. Optional: concrete coverage gaps from the per-RQ coverage values above (e.g. "RQ-model-quality only 1/5 cells fully populated").

Honesty rule: If an RQ has no robust findings in the current setup, **do not invent** something — say plainly "the current data base does not yield a robust finding" and use the synthesis to explain what is missing.

Attribution rule: Never credit a *bundled* workflow's outcome to a single one of its factors without the counter-cell check above. Correctness and code-quality are driven by different levers here (spec/test-phase vs. refactor cadence); a sentence that fuses them ("TDD makes it both correct and clean") is the default failure mode. Keep the two outcomes — and their causes — separate.

### Step 4 — propose Key Findings, let the human select

This is the only interactive step. Do **not** silently write the Key Findings — propose candidates and let the user pick.

**Always ask — and always offer both continuity and novelty.** The selection is the user's call every single time; never write the Key Findings from your own judgement, and never treat the previous snapshot as auto-approved. The question you put to the user must contain two clearly separated groups:

- **Carried-over candidates** — the previous snapshot's Key Findings with refreshed numbers. These are the study's public face: they get lifted into talks, slide decks and the manuscript, so their *wording* accumulates value across snapshots and should stay recognisable. Read the most recent `research/reports/experiment-overview-*.md` and any `slide-tables-*.md` (the talk-ready condensates) before drafting.
- **New candidates** — findings the old set could not carry, because the RQs behind them did not exist or had too little data last time. **Proposing these is mandatory, not optional.** Look specifically at: RQ subtrees added since the last snapshot, RQs whose coverage crossed `min_replicates` since then, and cross-RQ patterns that only became visible with the new cells. For each, say in one line why it is newly sayable ("only measurable since the fourth harness was added"). If you genuinely find no new candidate, say that explicitly and name what you checked — do not let the new group quietly stay empty.

Label each candidate as carried-over or new when presenting, so the user can weigh continuity against novelty deliberately.

For each carried-over finding, re-verify every number against the current `findings.md` rather than copying it forward. Values shift as cells grow — in 2026-07 the Example-Mapping effect widened from "+48–64 pp" to "+48–76 pp" because one cell had grown to n=9. Where a carried sentence mixes katas or workflows in a way the numbers do not support, fix it while carrying it and say so. A carried-over finding whose numbers no longer support it is a *finding in its own right* — report that to the user rather than silently dropping or softening it.

1. From the previous snapshot plus everything you read in step 2, assemble **5–7 candidates — at least two of them new** (see above). Each candidate carries: a bold-sentence title, 1–3 sentences with concrete numbers (`verification_pct`, `cognitive_max`, tokens), and a one-line practical consequence. **Apply the counter-cell + attribution checks (step 3) to every candidate** — Key Findings are where a wrong causal attribution does the most damage. A catchy title may name a factor ("strict TDD improves quality"), but the body must name the *isolated* lever (the enforced refactor cadence, not the TDD label) and must not let a correctness lever and a quality lever bleed into one claim.
2. Present the candidates as a numbered list in chat, plus a short "why these and not others" line. **Do not** name workflow versions like `v6.1-hybrid` in the Key Findings — workflows are not yet introduced at that early point in the document. Describe by mechanism instead ("hybrid workflow with skill-based red/green in shared context + isolated refactor subagent").
3. Use `AskUserQuestion` (multiSelect: true) to let the user pick **3–5** of the candidates. Accept "Other" answers as additions.
4. After the user has chosen, write the selected findings — verbatim with their bold titles and the practical-consequence line — into the `## Key Findings` block, replacing the TODO marker. Keep the previous snapshot's ordering for carried-over findings (readers and the deck know them in that order); place genuinely new ones by descending practical impact.
5. Open the block with a one-sentence TLDR framing that names the through-line, then "N key findings from the M research questions — Details in §4, Cross-RQ-Synthese in §5". Key Findings are read by people who will read nothing else; the framing sentence is what they take away if they stop after it. Make it state the actual structure of the result (e.g. that two levers drive two *different* outcomes), not a generic "TDD works".

### Step 5 — write the file

Take the date from the skeleton header (line 3: `Stand: YYYY-MM-DD.`) and write to:

```
research/reports/experiment-overview-YYYY-MM-DD.md
```

Then verify with Glob or Read that:

1. The file exists
2. No `<!-- TODO -->` markers remain
3. All current findings from the findings.md files are referenced somewhere in the RQ sections (number + statement)
4. Each RQ section carries the overview table from its `findings.md` before the `**Findings**:` list
5. No status tags (`⚠️ bedingt`, `✅ stabil`) and no references to old studies / archive snapshots in the published snapshot

### Step 6 — generate the PDF (on request only)

The Markdown file is the deliverable and the source of truth. **Do not build a PDF unless the user asks for one** — report PDFs are gitignored (`research/reports/*.pdf`) because they are large binary derivatives that bloat the repo and diff as noise. Anyone can rebuild one from the committed `.md` at any time with the snippet below.

When the user does ask, convert the Markdown snapshot to a PDF sibling via pandoc → Chromium headless:

```bash
SNAP=research/reports/experiment-overview-YYYY-MM-DD
pandoc "$SNAP.md" -o "$SNAP.html" --standalone --self-contained \
  --metadata title="Experiment-Overview YYYY-MM-DD" \
  --css=experiments/snapshot-style.css
google-chrome --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$SNAP.pdf" "file://$(pwd)/$SNAP.html" 2>/dev/null
rm "$SNAP.html"
```

The stylesheet (`experiments/snapshot-style.css`) is checked in so every regeneration uses the same A4 layout, page-break rules (tables may span pages, individual rows stay intact, header repeats), and typography. The intermediate HTML is throwaway.

**Why Chromium and not WeasyPrint:** earlier iterations used WeasyPrint, optionally with Ghostscript re-serialization. Both produced technically valid PDFs (`pdfinfo` confirms A4 portrait, rotation=0), but VS Code's built-in PDF preview (vscode-pdf, PDF.js-based) consistently rendered the content rotated 90° inside otherwise portrait pages. Chromium's `--print-to-pdf` writes PDFs through Skia/PDFium — the same lineage that PDF.js was forked from — so PDF.js-based viewers render them reliably. All other viewers (Browser, evince, okular, pdftoppm) handle Chromium output equally well. Chromium also packs the content denser (typically ~40% fewer pages than WeasyPrint for the same snapshot).

A harmless `Failed to load module: …libgiolibproxy.so` or `VAAPI version is too old` warning from Chromium can be ignored — they don't affect PDF output.

**PDF verification.** After generation, sanity-check the output:

```bash
pdfinfo "$SNAP.pdf" | grep -E "Pages|Page size|Page rot"
```

Expected: `Pages` ≥ 5, `Page size` ≈ `595 x 842 pts (A4)`, `Page rot` = `0`. If any of these are off (e.g. zero pages, landscape page size, non-zero rotation), the PDF is broken — report it instead of pretending it worked.

Report at the end in 1–2 sentences the output path (`.md`, plus the `.pdf` and its page count if one was requested) and any notable coverage gaps ("RQ-X is currently below min_replicates").

## Style template

`research/reports/experiment-overview-v2-2026-05-04.md` shows the target table density and section ordering. Read it for orientation **before** starting step 3. Adopt the table style and tone — not the specific numbers (those come from the current findings.md).

**Write each prose paragraph as a single unwrapped line.** Do not hard-wrap flowing text at 80/100 characters. Many Markdown renderers — including the one this repo's reports are read in — run with `breaks: true`, where a single newline becomes a visible line break instead of collapsing into flowing text. A source-wrapped paragraph then renders as ragged short lines with breaks mid-sentence. The published reports in `research/reports/` all follow the one-line-per-paragraph convention (paragraphs run 400–1200 characters); match it. This applies only to prose — tables, headings, list items, blockquotes and code blocks keep their own line structure.

Check before publishing, and compare against an existing report rather than a fixed threshold:

```bash
python3 - <<'PY'
import pathlib
for f in sorted(pathlib.Path('research/reports').glob('experiment-overview-*.md')):
    p=[l for l in f.read_text().splitlines()
       if l.strip() and not l.startswith(('|','#','-','>','_','*','`',' '))]
    if p: print(f'{f.name:42s} prose lines={len(p):4d}  max={max(map(len,p)):5d}')
PY
```

A new snapshot with several hundred short prose lines where its predecessors have a few dozen long ones is hard-wrapped and needs a reflow. To fix, join consecutive prose lines into one per paragraph while leaving every `|`, `#`, `>`, list-marker and fenced-code line untouched — then re-verify the structure counts (RQ sections, table rows, 🏆, list items) are unchanged, and grep for accidentally glued words.

## What is deliberately NOT part of your output

- Do not recompute or fabricate numbers — copy them verbatim from `findings.md` (overview tables and finding-internal values). Numbers in tables come from `findings.md`, never from re-running aggregation or estimating.
- No auto-commit. The snapshot is reviewed by the user before it goes into the repo.
- No diff against the previous snapshot — that would be a separate skill.
- No subagent delegation; everything in the main context.
- Do not silently choose the Key Findings for the user — step 4 is interactive by design.
