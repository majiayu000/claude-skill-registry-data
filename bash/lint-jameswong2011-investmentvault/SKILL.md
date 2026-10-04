---
name: lint
description: Run health checks on the vault for inconsistencies, stale data, orphaned notes, and missing connections. Use periodically or when user says "lint", "health check", or "audit".
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$lint`, or infer them from the user's request when this skill is invoked implicitly.

Comprehensive vault health audit. Read-only — never deletes, never edits. Report only.

Design rationale in `.agents/skills/lint/references/rationale.md` (§N.M anchors).

**Architecture (2026-07-08, script-first)**: the deterministic majority of the check registry (~45 of the registry's #1–#61, with #31 and #40 retired/unused — set-diffs, date arithmetic, regex, schema probes) is implemented in `.agents/skills/lint/scripts/lint.py`, following the `generate_graph.py` precedent. The script is the authoritative spec for those checks; this file specifies only the LLM-judgment checks and the merge procedure. Main-context cost drops from a full-vault read to one script call + targeted reads of flagged files.

## Step 0: Pre-flight (MANDATORY — runs before Scope Resolution)

### 0.1: Acquire vault lock (mode-dependent)

Per `.agents/skills/_shared/preflight.md` Procedure 1. Even though `$lint` never writes to vault content files, a lock is still acquired so that concurrent writers (e.g., a mid-flip `$sync` manifest, an in-flight `$prune` sector edit) do not cause `$lint` to see transient inconsistent state and raise false-positive flags.

- **Full mode** (`$lint` with no arguments): acquire a `vault-wide` scope lock. Timeout budget: 5 minutes.
- **Scoped mode** (`$lint TICKER`): acquire a `.vault-lock.readonly` lock. Timeout budget: 2 minutes.

Capture the token emitted at Step 0.1. Verify ownership (Procedure 1.5) before subsequent shell blocks. Release the lock explicitly in the final reporting shell block via `rm -f "$LOCK_FILE"`.

### 0.2: No rename-marker check

`$lint` is a read-only diagnostic skill and is an explicit exception in `.agents/skills/_shared/preflight.md` §2.1. `lint.py` #37 surfaces active `.rename_incomplete.*` markers as check output — hard-blocking would defeat lint's purpose.

## Step 1: Deterministic pass — run lint.py

```bash
python3 .agents/skills/lint/scripts/lint.py              # full mode
python3 .agents/skills/lint/scripts/lint.py --ticker $T  # scoped mode
```

- **Covers** (authoritative in-script): #1–#6 (empty-only for #5), #8, #10, #11, #12/#13 (mechanical flags), #14 (heading presence), #15, #16, #17–#27, #28 (candidates), #29 (presence checks a/b/c), #30, #32–#39, #41–#67 (#31, #40 retired/unused). New 2026-07-09: **#57** watermark-collapse alarm (pending-sync > 20% of vault notes → CRITICAL with sync-all-vs-advance guidance — the bulk-mtime failure class that silently breaks $sync default/all, $prune Phase 0.B, and $clean's safety-net); **#58** snapshot-integrity (snapshot .md lacking `snapshot_of:`/`snapshot_date:` frontmatter + any non-.md artifact in Snapshots/ — the class invisible to $clean and unrestorable-by-spec for $rollback); **#59** template-drift-at-birth (thesis <7d old already missing template sections → IMPORTANT immediately, split out of the #14 backlog — signals $thesis drifted from the template on that run). New 2026-07-14: **#60** conviction-trigger falsifiability (active/monitoring thesis whose `## Conviction Triggers` is a present-but-unfilled scaffold → IMPORTANT, or filled-but-carries-no-numeric/dated/named-observable-threshold → NICE; section-absent stays #14's job — the precondition `.agents/skills/_shared/trigger-touch.md` depends on); **#61** Key Metrics staleness (`key_metrics_last_refreshed` missing or >90d — IMPORTANT on high-conviction active, NICE elsewhere; consumes the field `$numbers` Step 11 writes). New 2026-07-15 (CHG-15, analytical tier): **#62** non-consensus-names-consensus (candidate — active/monitoring thesis whose `## Key Non-consensus Insights` states no consensus it opposes; LLM Step 2 confirms); **#63** Mental-Models stable-ID aggregate (ONE NICE listing populated `## Mental Models` sections lacking `[G-#]`/`§` citations — a convention-adoption backlog, not per-thesis defects; hypothesis-vs-verdict framing judged in Step 2); **#64** hedge-word ban (NICE — AGENTS.md Writing Standards filler words in thesis/sector/macro spines, "significantly" excluded as often-quantitative, capped 3/file); **#65** Summary-vs-frontmatter conviction consistency (candidate — Summary conviction word ≠ frontmatter; LLM confirms genuine stale statement vs conditional/negative prose); **#66** weakly-sourced spine figures (NICE — `[1×: …]`/`[est.]` provenance tags that reached a thesis body, pairs with CHG-10). New 2026-07-29: **#67** publish-flag coverage (thesis/sector/macro note missing the `publish:` frontmatter key → IMPORTANT — the GitHub→website sync silently skips it; `publish: false` passes as intentional unpublish; Research/ and Website/ out of scope by design).
- **Exit codes**: 0 = pass/nice-to-have · 1 = Important found · 2 = Critical found · 3 = self-validation failed (do NOT report partial results — fix the script invocation or escalate; the script's stderr states the cause).
- The script's report contains three severity sections plus a **Judgment candidates** section — those candidates are *inputs to Step 2*, not confirmed findings. Never copy candidates into the final report unreviewed.

## Step 2: LLM-judgment pass

Read ONLY the files the script flagged or that these checks name. Do not re-run any check the script covers; do not full-read the vault.

5. **Thin critical sections** — for each `#5` judgment candidate (section exists but under ~25 words), read the section and judge whether it is substantively empty (placeholder prose, restated heading) vs. legitimately terse. Substantively empty → Important.

7. **Old financial data** — for theses flagged by #6 or with `conviction: high`, read `## Key Metrics` and judge whether the data vintage (as-of dates, quarter references) is older than 6 months. Stale → Nice to Have; stale AND driving a conviction claim → Important.

9. **Unlinked mentions** — using Grep (word-bounded ticker tokens across `Theses/ Sectors/ Macro*/`), identify notes that discuss a ticker with a thesis but never wikilink it. Judgment: distinguish substantive discussion (flag, Nice to Have) from passing mention (skip).

12/13. **Conviction-evidence and Bull/Bear interpretation** — for each `#12` candidate and `#13` flag from the script, read the thesis and judge whether the mechanical count/ratio reflects a real evidence gap or bias. Upgrade to Important only with a specific stated reason.

28. **Partial-write confirmation** — for each `#28` candidate, read the flagged section and confirm whether it is genuinely truncated (mid-sentence, broken table) or a false positive (stylistic fragment, list item ending in a preposition-like token). Confirmed → Important, and name the likely matching snapshot in `_Archive/Snapshots/` if one exists.

29. **Registry reverse-check + semantic drift** — the script verified registry→skill presence. Do the reverse: scan each producer SKILL.md's quoted Log-prefix strings (Drift-coupling blocks, Log-format fences) for prefixes NOT in `.agents/skills/_shared/log-prefixes.md` → Important (`orphan coupling`). Also judge any `#29` script finding for semantic (not just literal) drift before reporting.

55. **Graph-primer anti-pattern review** — for each `#55` candidate, read the surrounding SKILL.md context and judge whether the matched phrase actually instructs primer-as-filter behavior (violation → Important) or is a negation/anti-pattern warning quoting the phrase (skip).

62. **Non-consensus names its consensus** — for each `#62` candidate, read `## Key Non-consensus Insights` and judge whether each insight actually states the consensus view it contradicts (prose or the CHG-11 `Consensus:` field). An insight that only asserts a positive view without naming what the market believes → Important (unfalsifiable positioning, not analysis); if the consensus is named in nearby prose the grep missed → skip.

63. **Mental-Models hypothesis-vs-verdict framing** — read the `## Mental Models` sections listed in the `#63` stable-ID aggregate (they are the populated ones). Judge whether "Triggers that fired" are held as hypotheses-to-test (READING PROTOCOL) or stated as verdicts/conclusions (e.g. "the moat is real, buy" rather than "layer-monopoly hypothesis — the falsifier is X"). Verdict framing → Important; note that the VLM lens's own `Alpha verdict` output-format field is legitimate and not itself a violation. The stable-ID absence is already reported mechanically (aggregate NICE) — do not re-flag it per-thesis.

65. **Conviction Summary-vs-frontmatter** — for each `#65` candidate, read the `## Summary` sentence containing the conviction word. Confirm it is a genuine stale statement (Summary asserts a conviction level that contradicts frontmatter, e.g. after a `$status` change) → Important; dismiss if the word appears in conditional/negative prose ("preclude high conviction until…", "would warrant medium") → skip. This is the INTC-class drift catcher.

## Step 3: Merged report

Merge Step 1 findings (verbatim) with Step 2 confirmations into the standard format. Attribute each finding to its check ID. Drop unconfirmed candidates silently.

### Critical (breaks research quality)
- [ ] [#ID] [Issue] — [File path] — [Specific problem]

### Important (gaps in coverage)
### Nice to Have (optimization)
### Stats
(reproduce the script's Stats block, plus: judgment candidates reviewed / confirmed / dismissed)

Release the lock in the same final shell block.

## Maintenance contract

- `lint.py` is the spec of record for the deterministic checks. When a check's rules change, edit the script (and its docstring COVERED list), not this file.
- New deterministic checks go in the script; new judgment checks go in Step 2 here.
- The script never writes vault state and reads a point-in-time snapshot in <1s, which also shrinks the lock-contention window that motivated Step 0.1's 5-minute budget.
- Cross-skill contracts enforced: `.agents/skills/_shared/log-prefixes.md` (#29), `.agents/skills/_shared/sector-resolution.md` (#30/#34), `.agents/skills/_shared/hot-md-contract.md` (#35/#42), `.agents/skills/_shared/graph-primer.md` (#54/#55), `.agents/skills/_shared/preflight.md` (#43).
