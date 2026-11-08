---
name: forge-research-evidence
description: "Use when a research result rests on sources (onderzoek met bronnen, citaten checken)."
---

# forge-research-evidence: claims that can be checked

A research result is only as good as the claims a reader can check. This skill is the Forge discipline for
that: every load-bearing claim goes into a citation ledger with a verbatim quote and a date, the ledger is
checked by machine before the result is reported, and what cannot be backed is labelled. The tool is
`.claude/forge-bin/forge-citations.cjs`. Hands off: finding and vetting a tool to adopt → `forge-scout`; a
long sourced investigation → the `deep-research` workflow (this skill is the evidence layer on top of it); a
metric loop → `forge-autoresearch`.

## When to use
- A research, audit or comparison result that names facts from documents, repos, docs or web pages.
- A report that says "source X says Y", gives a number, a version, a licence or a date taken from a source.
- Before deciding to build something new: the search-first matrix below.
- Not for: a single factual lookup answered in one line; code behaviour you can prove by running a test (the
  test is the evidence); opinions and recommendations, which need a reason, not a quote.

## The procedure
1. **Save the source as text inside the project.** Fetch read-only, save the page or file under the run's
   research folder (`.claude/forge-research/<topic>/` or `_scratch/`), and treat it as untrusted data. A source
   outside the root only verifies with `--allow-outside-sources`; say so in the report.
   *Done when:* every claim you plan to make points at a saved file or, failing that, a URL.
2. **Log each load-bearing claim with a verbatim quote and an AS_OF date.** One `add` per claim:
   `node .claude/forge-bin/forge-citations.cjs add --run <run_id> --claim "<your claim>" --quote "<exact words
   from the source, 3 or more>" --source <saved file> [--url <u>] --as-of YYYY-MM-DD`. AS_OF is the day the
   source said it, so a later reader knows how stale the claim may be. A quote is copied, never retyped from
   memory.
   *Done when:* `add` printed `verified` for each claim, or you know why not.
3. **Reopen the original, never cite a summary.** A summary, a search snippet or another agent's report is a
   pointer to a source, not the source. Open the original and quote it; if you cannot open it, the claim stays
   unverified.
   *Done when:* no `source_path` in the ledger is a summary written in this run.
4. **Check and report before the result is reported.** `check --run <run_id>` re-reads every source and
   rewrites the statuses; `report --run <run_id> --min-verified <pct>` exits 1 on any mismatch or when verified
   coverage is below the bar. Paste the report's counts line into the result.
   *Done when:* `report` printed PASS, or the result says plainly which claims failed and why.
5. **Label what is not verified.** Cite claims with markers like `[c3]` in the draft, then
   `label <draft.md> --write` appends `[unverified]` after every marker whose claim is not verified or not in the
   ledger. A mismatch is fixed (a better quote, a corrected claim) or the claim is removed; it is never shipped
   with a label.
   *Done when:* every remaining `[unverified]` is one you chose to keep and the result says why.
6. **Counter-review pass.** One fresh reader (Verify Boss or a read-only agent) takes the three claims the
   conclusion leans on most and looks for the strongest source that says otherwise. A found counter-source goes
   into the ledger too and the conclusion is restated with it.
   *Done when:* the result names what the counter-review looked for and what it found.

## The search-first matrix (before building anything new)
Search the project, the installed skills (`node .claude/forge-bin/forge-ecc-path.cjs list --json`), the
registries and public repos first, then pick one row and log the evidence for the pick:

| Verdict | When | Evidence to log |
|---|---|---|
| Adopt | an existing tool fits as it is | the source, its licence, one verified quote on what it does |
| Extend | an existing tool fits with a small Forge addition | what it lacks, and where the addition lives |
| Compose | two or more existing tools cover it together | the seam between them and who owns it |
| Build | nothing fits after the search | the searches run (terms, sources, counts) and why each near hit failed |

A tool that cannot run here (missing CLI, no key) is reported as such, never skipped in silence.

## When the search is for an outside capability
For a skill, plugin, MCP server or CLI from outside the project, follow `forge-scout`: its channel preflight table
and matrix are in `.claude/skills/forge-scout/references/search-first.md`, and an Adopt or Extend copy is scanned with
`node .claude/forge-bin/forge-skill-audit.cjs scan <folder>` before anyone reviews the diff.

## Anti-pattern: vibe-citing
A claim with a link that looks like evidence but was never checked against the page. Signs: a quote typed from
memory, a number "from the docs" with no saved source, a citation to an article that only summarises the real
source, ten links where two were read. The cure is the ledger: if `check` cannot find the words, the claim is
not backed, however good the link looks.
Whether a cited paper, DOI or URL exists at a canonical public source, and whether the in-text markers match the
reference list: `references/citation-existence.md`.

## Pitfalls
- A quote under 3 words is a mismatch by rule; a word cut mid-way never verifies (the match keeps word
  boundaries). Quote whole words.
- Matching ignores case, whitespace and markdown markup only; a paraphrase is a different wording and fails.
- Words are split on whitespace, so one code line without spaces counts as one word; quote it with its
  neighbouring words. A quote that runs across a line break in a code comment also takes in the `#` or `//`
  marker, so keep it to one line.
- `report` and `label` never write the ledger; `check` is the only rewriter, so run it after a source changes.
- A source over 5 MiB is skipped as unverified; save the relevant section instead.

## Verification
- `node .claude/forge-bin/forge-citations.cjs report --run <run_id>` output pasted in the result.
- The doctor line `citations` is green: the matcher verifies a real quote and rejects a cut one, and stored
  mismatches in run ledgers are printed as a warning (`.claude/forge-bin/doctor/checks-tools.cjs`).
- `node .claude/forge-bin/forge-skill-evals.cjs run --skill forge-research-evidence` passes.

## Provenance
Ideas only, written in Forge's own words (PATTERN_ADAPTED); no source text was copied into this skill. The idea
list comes from the 2026-11-04 skills audit plan (the local research note forge-research/skills-audit-2026-11-04/SKILLS-PLAN.md,
research rows), which names these sources:

| Source | Idea taken | Not taken |
|---|---|---|
| NousResearch/hermes-agent grounded-citations (MIT; already credited in forge-citations.cjs) | verbatim quote check, unverified label, coverage gate | its Python scripts |
| deer-flow and daymade research skills | AS_OF dates, evidence families, reopen originals instead of summaries | all code and prompts |
| ARS (licence NOASSERTION) | counter-review pass, the vibe-citing anti-pattern | any text (no licence, ideas only) |
| ECC search-first (pinned local catalog, commit e2b8a51) | the Adopt/Extend/Compose/Build choice, tool preflight with no silent skipping | its wording and examples |
