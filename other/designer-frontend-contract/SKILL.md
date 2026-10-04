---
name: designer-frontend-contract
description: "The universal, tech-agnostic DESIGNER ↔ FRONTEND contract — how the web designer and the frontend dev help each other, where they store their shared data, how they communicate, and how the contract between them is written and ENFORCED. Three sides: the DESIGNER freezes an approved mockup into a canonical oracle (oracle-manifest.json + baseline renders + a region/element inventory + token parity + a four-part visual acceptance contract); the FRONTEND dev consumes that contract and PORTS the oracle 1:1 (transcribe, never redesign), self-gating census → DOM → pixel before handoff; the VERIFIER (design-diff) independently screenshots every built page × access state × breakpoint against the frozen baseline and reports per-page PASS/FAIL — report-only, a mismatch is a gate reject. Works on ANY stack (Phoenix/LiveView, Rails/Hotwire, React, …): stack facts (dev server, template language, settle signal, token source, seed accounts) are read at runtime from docs/project_config/info.md, never baked in. Use when: freezing an approved design for handoff; building a page from a frozen mockup; verifying a built page matches the approved design; establishing/refreshing a design baseline; deciding where design/frontend data lives or how the two roles hand off. Owned by the design role; on the architecture role's verify path; consumed by the frontend dev."
---

TASKLANG
TYPE SKILL

IDENTITY "Designer ↔ Frontend Contract (universal — any stack)"
  > ONE skill = the WHOLE collaboration between the web designer and the frontend dev:
  > what each side PRODUCES for the other, where the shared data is STORED, how they
  > COMMUNICATE (paths + committed artifacts, never chat blobs), and how the CONTRACT
  > between them is written and mechanically ENFORCED. The designer freezes the approved
  > mockup into an ORACLE; the frontend PORTS it 1:1 and self-gates; the independent
  > design-diff VERIFIES the running UI against the oracle and feeds the pipeline's
  > verify gate. TECH-AGNOSTIC by construction: no framework, port, template language,
  > or product fact lives here — those are read from `docs/project_config/info.md`
  > (`{config.frontend_runtime}` + `{config.spec_path}`) at runtime.
  > It exists because builds without this contract silently re-style, drop whole page
  > regions, and ship broken UI that a green HTTP-200 smoke never catches.

This SKILL.md is a MAP. Detail lives in `workflows/` (the three role playbooks) +
`references/` (atomized notes) + `maps/` (machine-readable nav). Read this file +
`maps/index.json` to orient, then open ONLY the workflow/note a task needs.

---

## The three sides (who runs what)

| Side | Role | Playbook | Runs when |
|------|------|----------|-----------|
| **PRODUCER** | the design owner (skill owner) | [[designer-handoff]] | An approved mockup must become a build target: freeze → manifest → inventory → token parity → acceptance contract. |
| **CONSUMER** | the frontend owner | [[frontend-port]] | Building a page from a frozen oracle: consume the contract → port 1:1 → self-gate census→DOM→pixel → report + KB write-back. |
| **VERIFIER** | the design owner + whoever runs the verify gate | [[design-diff]] | Independently verifying built pages against the oracle (pipeline verify gate, fan-out audit finder, or ad-hoc). |

---

## Top Rules / Invariants (headlines — detail in references)

!!! **The contract is COMMITTED ARTIFACTS, not conversation.** Every handoff between the
    designer and the frontend travels as committed files under `docs/design/` (the
    designer's library) and `docs/frontend/` (the frontend's KB), referenced by PATH via
    pipeline-state. If an obligation isn't written into an artifact, it doesn't exist.
    → [[contract-and-communication]].

!!! **The oracle is `docs/design/`.** ONE canonical frozen renderable mockup per page
    (resolved via `docs/design/oracle-manifest.json` — never guessed), baseline renders
    per pinned breakpoint, and the rule oracle (`design-tokens` + `design-system.md`).
    Never diff or build against a guess or a re-derived design. → [[baseline-and-oracle]].

!!! **PORT, don't redesign.** The frontend OPENS the canonical oracle and transcribes its
    markup verbatim into the project's template language (typically a near-superset of
    HTML — apply only the mechanical escaping/attribute mapping the language requires,
    e.g. JSX's `class`→`className`), injecting ONLY the stack's dynamic bindings.
    Authoring a page fresh from memory is what drops whole regions. A change to the
    rendered DOM/CSS is a contract violation even if it "looks the same".
    → [[frontend-port]].

!!! **CENSUS FIRST — completeness before pixels.** Before any pixel diff, both the
    frontend self-gate and the verifier run the region/element COMPLETENESS CENSUS
    against the designer's inventory: every region + interactive element PRESENT, in
    order, none extra. A whole missing region is a **Blocker**; census needs NO pixel
    baseline, so it runs even when no baseline exists. A page can never PASS on a green
    pixel diff while its census is short. → [[region-census]].

!!! **ONE token source — declared, never assumed.** The mockup and the app render from the
    SAME declared token source, whatever the project declares in
    `{config.frontend_runtime}` (e.g. CSS custom properties in `:root`, a utility-framework
    config, a CSS-in-JS theme), mirrored by `docs/design/design-tokens`. Never introduce a
    SECOND styling source beside the declared one; never assume which kind it is — read the
    declaration. Verify a token resolves identically before porting.
    → [[fidelity-checks]], [[contract-and-communication]].

!!! **Every built page × every access state × every pinned breakpoint.** The verification
    matrix is pages × the project's access states (from `{config.frontend_runtime}` /
    the design spec) × the pinned breakpoints (default 375/768/1024/1440; the per-feature
    design spec's visual acceptance contract is authoritative). A page proven at one
    width/state is not proven. Screenshot the RUNNING app, never a static file.
    → [[design-diff]].

!!! **The verifier is REPORT-ONLY — findings are ROUTED.** Design-diff never edits
    application source (templates/views/components/stylesheets). Build drift + missing
    regions route to the FRONTEND dev (fix by porting the oracle); a legitimate design
    change routes to the DESIGNER (refresh the oracle + re-run the approval gate). A
    mismatch or broken/obscured interaction is a gate reject, same weight as a functional
    violation. → [[design-diff]], [[fidelity-checks]].

!!! **No oracle? ESTABLISH one — never silently pass.** When no frozen baseline exists
    (design phase skipped / migration), capture or promote an ACKNOWLEDGED baseline
    first, mark it `ESTABLISHED-THIS-RUN`, and diff against that. `[NO-ORACLE]` is a
    blocking finding, not a free pass. → [[baseline-and-oracle]].

!!! **Stack facts live in project config, product facts in the spec — NEVER here.** Dev
    server command/URL, per-PR preview scheme, template language + its dynamic-binding
    whitelist, settle signal, token-source path, seed accounts, access states: read them
    from `docs/project_config/info.md` (`{config.frontend_runtime}`). To reuse this skill
    on another project/stack, swap that config — not this skill.

---

## Workflows

| Playbook | What it does | Run when |
|----------|--------------|----------|
| [[designer-handoff]] | PRODUCER: freeze the approved mockup (pin widths · self-host fonts · snapshot baseline renders) → register it as THE canonical oracle in `oracle-manifest.json` → emit the region/element inventory → declare token parity → write the four-part visual acceptance contract into the design spec → hand off PATHS. | After the design approval gate passes and the build needs a measurable target. |
| [[frontend-port]] | CONSUMER: read the six binding inputs from the spec + manifest → verify token parity → PASS A static 1:1 transcription → PASS B interactivity without DOM change → self-gate census→DOM→pixel per component AND per assembled page/state → report evidence + write back the `docs/frontend/` KB. | Building/fixing a page that has a frozen oracle + acceptance contract. |
| [[design-diff]] | VERIFIER: resolve the oracle via the manifest → enumerate the page × state × breakpoint matrix → capture the RUNNING app post-settle → census FIRST → pixel-diff vs baseline → rule-check tokens/8pt/60-30-10 → hit-test interactions → per-page PASS/FAIL verdict, findings routed. | The pipeline verify gate, the fan-out audit's visual finder, or an ad-hoc fidelity pass. |

## References map

| Note | Summary | Load when |
|------|---------|-----------|
| [[contract-and-communication]] | THE CONTRACT ITSELF: the artifact/link graph both roles share, the storage layout (`docs/design/` library · `docs/frontend/` KB · `.ai_log/` evidence · pipeline-state paths), the communication protocol (handoff timing, ask-don't-guess, findings routing, deviations ledger, refresh loop), and the three-way `data-test` hook contract with QE. | Deciding where an artifact lives, how to hand off, who to ask/route to, or what each side owes the other. |
| [[baseline-and-oracle]] | What the oracle is (ONE canonical frozen renderable file per page via the manifest + baseline renders + the token/system rule oracle), how to resolve it per page/state, canvas-export de-framing, and how to ESTABLISH/REFRESH a baseline — including when the design phase was skipped. | Resolving/refreshing the baseline; no oracle exists yet; the design legitimately changed. |
| [[region-census]] | The region/element COMPLETENESS CENSUS — the FIRST check on both the frontend self-gate and the verifier: build the oracle's ordered inventory, walk the built DOM, tick each region/element off by `data-test`, FAIL on any missing/reordered/extra region. Needs no pixel baseline. | Gating a page; a whole section may be missing; the pixel diff "looks fine" but the page feels incomplete; no baseline exists. |
| [[fidelity-checks]] | The measurable checks + thresholds: completeness census (first), layout, spacing (8pt grid), color (palette + 60/30/10), type (scale/weight/line-height), token conformance (against the project's declared token source), DOM-structure preservation, and broken/obscured-interaction hit-testing; severity model + the PASS/FAIL rule. | Deciding what to measure; classifying a diff as PASS/FAIL; setting/holding the drift threshold. |

---

## Companion Files

- `FORMAT.md` — the handoff manifest (producer), the port-evidence report (consumer),
  the per-page PASS/FAIL design-diff report + gate verdict line (verifier).
- `VOICE.md` — communication style / tags (`[DESIGN-DIFF-*]`, `[NO-ORACLE]`,
  `[CONTRACT-GAP]`, report-only framing).
- `workflows/` — the three role playbooks mapped above.
- `references/` — the atomized knowledge notes mapped above.
- `maps/` — `index.json` (master nav), `tags.json`, `links.json`, `manifest.json`.

---

## Knowledge Strategy

- **Patterns to capture:** reliable screenshot/diff recipes (agent-browser + Playwright
  `toHaveScreenshot` / pixelmatch / odiff), per-breakpoint threshold tuning, recurring
  drift shapes (font-loading FOUT, second-styling-source drift, off-grid spacing),
  census misses and the inventory entries that would have caught them.
- **Examples to collect:** baseline establishment on a design-phase-skipped page,
  token-parity verification across stacks, obscured-interaction (overlay/z-index)
  catches, contract-gap escalations.
- **Update permission:** agents may freely add/update files in `references/`. Changes to
  `SKILL.md` require user approval.

---

VERSION 2.0

---

Made by **HasBrains** — https://hasbrains.com/
