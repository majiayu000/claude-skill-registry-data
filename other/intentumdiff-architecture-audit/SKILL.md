---
name: intentumdiff-architecture-audit
description: >-
  Systematically reason over the IntentDiff codebase and find its real problems — invariant
  violations, architectural drift, latent bugs, and tech debt — then produce a ranked,
  root-caused findings report. Use this whenever the user asks to audit, review the
  architecture, "find all the problems/issues", health-check the repo, hunt tech debt, check
  for boundary/theme/privacy violations, or before a release-candidate gate. It gives a
  category-by-category probe checklist (engine boundary, index-space contract, theme-native,
  privacy/BYOK, Monaco-retirement, stick-plaster patterns, test health, dead code/stale docs),
  the commands/greps to run each, and a strict report format that demands root cause + a
  verification step, not just symptoms. This is the "sense" step of the intentdiff-dev-loop
  flywheel. Read intentdiff-architecture first; pull in the specific intentdiff-* skills as
  each category demands.
---

# IntentDiff — Architecture audit ("find all the problems")

Goal: turn "review the architecture" into a **repeatable, evidence-backed sweep** that ends
in a ranked findings report an agent can act on. Two principles govern the whole pass:

1. **Root cause, not symptoms.** A failing test or a wrong pixel is a lead, not a finding.
   Trace it to the construction that produced it. If a fix would compensate downstream for
   something built wrong upstream, the finding is the upstream construction. (See the
   "stick-plaster" category.)
2. **Verify before you report.** Each finding must include how you confirmed it (a repro, a
   grep hit with file:line, a failing assertion, a boundary-gate run) — and, where cheap,
   whether it is *pre-existing* vs newly introduced (stash the working changes and re-run).

Work category by category. For deep per-category probes, greps, and known traps, read
[references/audit-checklist.md](references/audit-checklist.md). The categories:

## 1. Engine boundary (Rust = engine, Python = shell)
The release contract. Look for processing/analysis logic added to Python instead of Rust, and
first-party product paths importing `intentdiff.analysis.*` / `intentdiff.core.engine`.
Authoritative: `docs/ENGINE_BOUNDARY_AUDIT.md`. Run the strict gate:
`INTENTDIFF_ENFORCE_RUST_ONLY_ENGINE=1 <pytest ...>`. New Python engine code is a finding.

## 2. Change-group index-space contract
The highest-recurrence bug class. Every `ChangeGroup` producer must carry node ids **or** be
honestly empty — never emit phantom `raw_change_indices` for a downstream pass to erase. Every
consumer must range-check dereferences and cover ungrouped changes. See
`intentdiff-engine` → `references/index-space-contract.md`. Audit new/edited producers and
consumers against that contract.

## 3. Theme-native styling (extension)
No hardcoded chrome hex literals, no bundled fonts, codicons-only, category colors via the
contributed `intentdiff.semanticChanges.*` tokens. Grep the panel/diagnostics HTML *output*
(not just `media/`) for hex literals, `iconSvg`/`<svg>` chrome icons, and font `<link>`s.
**Do not assume `test/themeColors.test.ts` enforces this** — it validates the contributed color
IDs + overview-ruler tokens but does **not** scan rendered HTML for chrome hex or custom icons.
There is standing drift here (100+ hardcoded hex + a custom `iconSvg` set in
`reviewWebviewModel.ts` `styles()` and `extension.ts` diagnostics HTML) that passes CI — a known
hotspot; confirm current state with a real grep rather than trusting the test.

## 4. Privacy / BYOK
No bundled API key, no paid proxy, keys only in SecretStorage, consent modal before any send,
verbatim source only to a **local** endpoint, unit tests do no network. Grep for hardcoded
keys, cloud URLs, `fetch(` outside the gated explainer, and network calls reachable from unit
tests. Cross-check `plugins/vscode/PRIVACY.md`.

## 5. Monaco-retirement / native-first
No reintroduced Monaco, `createDiffEditor` webview embeds, `media/monaco/` references, or
retired gap machinery (`gapStates`, `expandGap`, floating chevrons, `reconstructFullFile`).
Grep for these symbols.

## 6. Stick-plaster patterns
Downstream compensation for upstream defects; duplicated fixes; "fix the symptom" comments;
tags/flags whose only purpose is to make another pass clean up a mess. Each is a finding whose
recommended fix is *at the source*.

## 7. Test health
Run `pytest tests/unit`, `cargo test -p rust-core-host`, and `cd plugins/vscode && npm run lint
&& npm run test`. For every failure: get the traceback, root-cause it, and classify —
genuine regression (bisect-worthy) vs documented gap vs stale assertion/reference. Confirm
pre-existing vs introduced by stashing. `xfailed` markers are expected, not failures. Note
that the RC gate (`docs/BACKLOG.md` → "0.0.1 RC Release Gate") requires the suites green, so
undocumented failures are release blockers — surface them.

## 8. Dead code, stale docs, drift
Unused functions/branches, superseded paths, stale references (e.g. a fixture pointing at a
deleted test), and docs that contradict shipped behavior (reconcile `CLAUDE.md` /
`docs/architecture/diff-viewer.md` with the code).

## Report format (use this exactly)

Rank findings **most-severe first**. For each:

```
### [SEV: critical|high|medium|low] <one-line defect>
- **Category:** <one of the 8 above>
- **Location:** <path:line> (+ related sites)
- **Root cause:** <the construction that produces it, not the symptom>
- **Evidence:** <repro / grep hit / failing assertion / gate output; pre-existing? y/n>
- **Impact:** <what breaks, for whom>
- **Fix:** <the source-level fix, and which layer (Rust / Python shell / extension)>
- **Verify:** <the exact command/repro that will show it fixed>
```

End with a short **Summary**: counts by severity + category, the top 3 to fix first, and any
systemic theme (e.g. "three findings share the index-space root cause"). If a finding needs a
bigger effort than the current task, recommend a `docs/BACKLOG.md` entry rather than an inline
fix — the audit's job is to *find and rank*, the dev-loop's job is to *fix*.

## Scope control

A full sweep is large. If the user scoped it ("audit the extension", "check the engine after
my change"), run only the relevant categories but keep the same root-cause + verify rigor.
Prefer depth on real findings over breadth of shallow observations — a ranked list of five
confirmed, root-caused issues beats twenty unverified smells.
