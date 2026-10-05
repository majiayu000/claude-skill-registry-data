---
name: prose-clarity
description: "Rewrite and self-check drafted prose against a machine-checkable clarity standard derived from ASD-STE100 (Simplified Technical English) — no marketing adjectives, no phrasal verbs, no semicolons, active voice, short sentences, and a required carve-out for the epistemic hedge markers the evidence ledger depends on. Use when drafting any package document's prose, before returning a draft, or when an independent verification pass evaluates editorial quality. This skill MUST be consulted because a banned-word list alone barely moves AI slop — the habits that produce it (hedge-stacking, nominalization) generate new slop the list never anticipated — and only rules a script can verify hold up under revision."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
agent: general-purpose
---

# Prose Clarity

Owns the sentence- and paragraph-level form of drafted prose — never its truth, never its structure, never its claim state.

## Iron Law

**THE LINTER CATCHES FORM, NEVER TRUTH — AND A REQUIRED HEDGE ON AN `I`-STATE CLAIM IS NEVER A VIOLATION, IN ANY MODE.**

A sentence that must carry `[EV-####]`, keep `Inferred:`/`Unknown:`/`Recommendation:`, or preserve a limitation that keeps it true is correct at whatever length that takes. This skill fixes the form of slop. It cannot make a hollow paragraph true, and it never overrides an Iron Rule from another skill.

## Classification is by passage, not by document

Any line inside a numbered or bulleted step sequence, a runbook or procedure block, or a command caption resolves to **strict** mode: 20-word sentence cap, full rule set. Everything else — narrative rationale, executive summary, due-diligence prose — resolves to **STE-flavored**: 25-word cap, relaxed dictionary, same active-voice and no-phrasal-verb discipline. This is mechanically detectable from list markers and fenced/table syntax, and it handles a single document that mixes both, which most of them do.

## Hard categories — apply in every mode, always block

Banned marketing adjectives · banned phrasal verbs · semicolons · banned filler and hedge phrases (minus the carve-out below) · sentence-length cap for the resolved mode · paragraph cap (more than six sentences). Full lists: `references/prose-style-and-vocabulary.md`.

## Advisory categories — reported, never block

Passive voice, nominalization, em-dash count. Both grammar checks are heuristic and false-positive-prone — this plugin's own reference docs use em-dashes constitutively, so em-dash must never gate release. Advisory hits feed `dossier-pass-c-audience`'s Step 5 and the scorecard's Dimension 10 as context for whether a hard-category fix was genuine or superficial, not as findings on their own.

## The epistemic-hedging carve-out

`references/source-authority-and-claim-states.md` requires specific hedge phrases as structural markers for `Interpreted`-state claims: `"This suggests…"`, `"The most likely reading is…"`, `"Inferred from…"`, and the prose prefixes `Inferred:`, `Unknown:`, `Recommendation:`. These are the package's epistemic-honesty mechanism, not slop. A line opening with one of these markers is exempt from the hedge-phrase and sentence-length rules, in every mode, unconditionally. The full allow-list lives in `references/prose-style-and-vocabulary.md` — check it before ever touching a flagged hedge.

## The verbatim-collection exemption

`07-verification/documentation-verification-report.md` carries pass output that `/dossier:audit` Phase 3 requires to be collected unmodified. `bin/dossier-prose-lint.sh` recognizes an explicit `<!-- DOSSIER_VERBATIM_BEGIN -->` / `<!-- DOSSIER_VERBATIM_END -->` marker pair and exempts only the text between them from this skill's hard categories, and only when scanning that one file — the round heading and summary block outside the markers, and every other document in the package, are still linted normally. The markers are ordinary inert HTML comments everywhere else, so this is not a general "wrap it to exempt it" mechanism available to a document under revision. This exemption is specific to `dossier-prose-lint.sh` — it is not honored by `bin/dossier-claim-scan.sh` or any other dossier check. See `references/release-gate-conditions.md` G18 for the full mechanism and its malformed-marker handling.

## Precedence

Iron Rules from other skills always outrank this one. Where this skill and `disclosure-gating` appear to disagree on a public document, `disclosure-gating` wins — truth and legal exposure over style. Cross-document synonym rotation stays `project-modeling`'s and `dossier-pass-c-audience`'s job; this skill only concerns the document currently being drafted.

## Self-lint procedure

Run `bin/dossier-prose-lint.sh --file <path> --json`. Fix hard-category hits with `Edit`. Re-run, capped at two revision passes — the same per-document budget discipline `dossier-doc-drafter` already applies to context. Return the draft regardless of outcome after the cap, and if a violation remains, say so plainly and name the Iron Rule that made the fix impossible (a required citation, a required hedge, an owner name that cannot shrink).

## Output Format

```markdown
PROSE_LINT=clean
```
or
```markdown
PROSE_LINT={n} hard violation(s) after revision
| Category | Count | Location |
|---|---|---|
```

## Rationalization Prevention

| Excuse | Response |
|--------|----------|
| "This adjective is technically accurate" | Concreteness is the axis, not accuracy. Replace it with the fact it stands in for. |
| "Hedging shows appropriate humility" | Only for an `I`-state claim carrying the required marker. Elsewhere a hedge is a claim you will not make — write `Unknown:`, or make the claim. |
| "Passive voice reads more objective here" | It hides the actor a reader needs. Name them, or state that the actor is unknown. |
| "The sentence is long because the fact is complex" | Split it. Two 15-word sentences carry the same fact and cost a reader less. |
| "The linter flagged my required hedge" | Check the allow-list in `references/prose-style-and-vocabulary.md` first. This is very likely a linter defect, not a prose defect. |
| "It's just one em-dash" | Em-dash is advisory, not blocking. Do not spend a revision pass chasing it. |

## Integration

Loaded by `dossier-doc-drafter` for every document; it self-lints before returning a draft. Invoked independently by `dossier-pass-c-audience` in Step 5 — it re-runs the script itself rather than reading the drafter's self-report, preserving the Independence Protocol. Invoked by `bin/dossier-gate.sh` for release-gate condition `G18`, across the whole package. Referenced by Dimension 10 of `references/scorecard-rubric.md` for the advisory-category judgment context.

References: `references/prose-style-and-vocabulary.md`, `references/source-authority-and-claim-states.md`, `references/release-gate-conditions.md`.
