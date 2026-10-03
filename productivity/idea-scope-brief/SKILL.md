---
name: idea-scope-brief
description: Shape a rough product or project idea into a scoped brief before customer discovery, market research, specifications, UX, UI, or implementation planning
type: planning
version: v0.24
required_conventions: [alignment-page, interrogation-page]
argument-hint: "[optional rough idea, product thought, or product-path scope]"
context_intake: deep
---

# Idea Scope Brief

Invoke as `$idea-scope-brief`.

Use this skill when the user has a half-formed idea and needs it cleaned up enough to enter the normal research and planning workflow. This skill is intentionally pre-customer-discovery: it clarifies the concept, problem hypothesis, beneficiary hypothesis, value wedge, constraints, non-goals, and unknowns, but does not select a validated target-customer segment, analyze competitors, define UX/UI, choose architecture, decide platform fit, or write implementation specs.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the customer, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

1. **Resolve context**
   - Read `.agents/project.json` if it exists.
   - Read canonical deck metadata from `docs/decks.md` when present and from skillpacks manifest `decks[]` metadata when available. Use deck fields such as `name`, `title`, `domain`, `tempo`, `default_packs`, and `full_packs` as routing evidence.
   - Read repo-saved deck candidates from `.agents/project.json` before canonical fallbacks. Recognize top-level `saved_decks` and `decks` fields when present; entries may be strings or objects with fields such as `name`, `slug`, `title`, `domain`, `tempo`, `packs`, `install`, `install_command`, `description`, or `notes`.
   - Read README, CLAUDE.md, AGENTS.md, existing `research/`, `specs/`, and task docs when present.
   - Determine whether the current directory is already a bootstrapped project. Treat it as bootstrapped when it has meaningful `README.md` plus `AGENTS.md` or `CLAUDE.md`; treat it as unbootstrapped when those are missing, placeholder-only, or the user is describing an idea outside any project repo.
   - If `$ARGUMENTS` contains a rough idea, use it as the starting draft.
   - If `$ARGUMENTS` names a non-archived `research/{slug}/` product path, use that path. If it names only `research/_archive/{slug}/`, stop and warn that the path is archived.
   - Determine the concept identity and a normalized concept slug as soon as either is known from `$ARGUMENTS`, repo context, or the interview. Normalize by lowercasing, removing URL suffix noise, replacing non-alphanumeric runs with `-`, trimming leading/trailing `-`, and dropping only project-wide brand prefixes when the remaining word is the actual scoped concept (for example, `poketo.work` -> `work`; `Poketo Core` -> `poketo-core`).
   - If existing research or the prompt suggests multiple related concepts may exist, prefer slugged output paths over generic filenames. Reserve generic `idea-brief.md` only for a single unambiguous project-level concept.
   - If no rough idea is available from arguments or repo context, ask the user for the idea in plain language.
   - Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Treat `active_paths` as the current product/app/customer focuses and `product_paths[]` as parked, archived, or promoted product-path state, not git branch state.
   - When the prompt, repo context, interview, or pivot history surfaces multiple related concepts, apps, product lines, or future pivots, update or propose updates to `research/.progress.yaml` with product-path entries instead of merging them into one generic concept. Use fields: `id`, `label`, `scope_path`, `status`, `source_skill`, `reason`, `archive_reason`, `archived_at`, `promoted_at`, `evidence_refs`, `revisit_trigger`, `next_skill`, `pipeline_stage`, and `last_touched`. Set `pipeline_stage: idea-scope-brief` on entries created by this skill.
   - Keep the central concept in `active_paths` when it is the current focus. Record related or future concepts as `status: deferred` or `status: revisit_candidate` with a concrete revisit trigger and a likely next skill such as `$customer-discovery <path/audience>`; if `business-research` is not enabled, recommend `npx skillpacks install business-research` from the project shell, before `$customer-discovery`.
   - When 3+ product paths exist in the manifest, recommend `$product-line review` to the user for portfolio management; if `business-ops` is not enabled, recommend `npx skillpacks install business-ops` from the project shell, before `$product-line`.

2. **Keep the boundary clear**
   - Do not run customer discovery, competitive analysis, journey mapping, UX variation, UI interview, roadmap, or implementation planning inside this skill.
   - Do not validate the market with broad web research. Use light repo/context inspection only; downstream research skills own evidence gathering.
   - Treat every user claim as a hypothesis unless supported by existing project files.

Steps 3–5 are the **stage-zero interrogation loop** (see `## Interrogation Page` / `INTERROGATION-PAGE.md`): elicit the concept in HTML interrogation rounds before the stage-two alignment preview in step 6. Round 1 is the Idea Assumptions Manifest, rounds 2..N are adaptive follow-ups, and the step-5 coverage checkpoint is the loop's confidence-gate exit. This skill **cannot advance to the alignment preview until** the confidence gate passes with at least one completed round and every area covered or waived. Terminal questioning is the degraded fallback only when an HTML page cannot be opened.

3. **Surface an Idea Assumptions Manifest (interrogation round 1)**
   - Before deep questioning, present what you think the concept is.
   - Tag assumptions as `[from prompt]`, `[from repo]`, `[from research]`, or `[inferred]`.
   - Cover:
     - concept summary
     - problem hypothesis
     - target beneficiary or user hypothesis
     - product/category guess
     - early platform hints as hypotheses only, when the prompt clearly suggests web, mobile, CLI, API, SDK, extension, marketplace, integration, desktop, game, or other platform shape
     - value wedge
     - constraints
     - non-goals
     - riskiest unknowns
   - Render the assumptions as confirm/correct/flag controls in `interrogation/idea-scope-brief-r1-{branch}.html`, alongside the first batch of genuinely open questions (each marked `data-open-input`) where no assumption is derivable. Set `data-interrogation-round="1"`, `data-interrogation-gate="continue"`, and the answer sidecar `research/_working/interrogation-idea-scope-brief-r1.yaml`, open the page, and stop for the compiled round YAML.
   - Terminal fallback only: deliver the manifest inline as the final message text of its own turn; ask the confirmation question in the next turn (consistent with the one-question-per-turn cadence). Never emit it only as mid-turn text in a turn that ends with a tool or command call — harness rendering does not guarantee mid-turn text is shown. A confirmation question must never reference content the user has not been shown.

### Market Structure Handoff

During the Idea Assumptions Manifest, if the concept appears marketplace/platform/B2B2C/multi-sided, add a compact `Market Structure Handoff` note:

- Name the apparent sides and the expected value exchange between them.
- Mark those sides and exchanges as hypotheses, not validated customer segments; do not decide which side is the customer, buyer, or primary target segment here.
- Keep the source tag for each side as `[from prompt]`, `[from repo]`, or `[inferred]` unless the user provides a correction.
- If the concept appears single-sided, omit the handoff or state that no marketplace/platform/B2B2C/multi-sided handoff is apparent.

### Platform Hint Handoff

During the Idea Assumptions Manifest, record early platform hints only as hypotheses. Name the apparent platform shape when the prompt or repo context clearly suggests it, but do not rank platforms, choose a primary platform, or reject alternatives here. The **Platform Fit Workshop** in `$user-flow-map` owns the broad candidate set, platform ranking, platform probes, and production-platform recommendation.

### Deck Fit Handoff

During the Idea Assumptions Manifest and final idea brief, add a compact `Deck Fit Handoff` that routes the concept to the closest workflow deck when confidence is high:

1. **Build candidates**
   - Prefer saved repo candidates from `.agents/project.json` `saved_decks` or `decks` when present. Rank them against the concept before canonical fallbacks.
   - Fall back to the canonical deck set from `docs/decks.md` or skillpacks manifest metadata: `vard`, `ord`, `business-afps`, `devtool-afps`, and `game-afps`.
   - Treat a saved deck as canonical only when its `name` or `slug` preserves one of the canonical slugs and the entry does not materially override its packs or install command.
2. **Rank by domain, tempo, and concept signals**
   - Domain: route video games, prototypes, playable entertainment, game engines, store-page tests, playtests, and game assets to `game-afps`; route SDKs, CLIs, APIs, libraries, npm packages, OSS utilities, infrastructure products, developer platforms, and documentation-first developer workflows to developer decks; route SaaS, marketplaces, productivity apps, internal/admin tools, business workflows, and consumer apps to business/consumer decks.
   - Tempo: route day/week experiments, quick viral app tests, lightweight npm/CLI/library ideas, and low-investment distribution probes to rapid decks; route products, platforms, SDK/API strategies, SaaS/business concepts, lifecycle/growth work, or anything needing weeks/months of validation to deliberate decks.
   - Evidence priority: user prompt and interview corrections outrank repo defaults; existing research/spec/task files outrank inferred code shape; `.agents/project.json project_type` is a tie-breaker, not the primary signal.
   - Confidence is high only when domain and tempo both match and no strong contrary signal remains. If confidence is not high, do not force a deck as the primary command; use the fallback routing rules in `## Next Steps`.
3. **Default canonical examples**
   - Game or playable entertainment concept -> `game-afps`.
   - Lightweight OSS/devtool/npm/CLI/library idea -> `ord`.
   - Deliberate devtool/platform/SDK/API product -> `devtool-afps`.
   - Rapid consumer/business experiment -> `vard`.
   - Deliberate business/SaaS/consumer product -> `business-afps`.
4. **Render the handoff**
   - Include deck slug/title, source (`saved_decks`, `decks`, `docs/decks.md`, or manifest), domain fit, tempo fit, confidence, key evidence signals, and the install command.
   - For canonical decks, the primary install command is `npx skillpacks install-deck <deck>`.
   - For customized saved decks, do not use `install-deck` unless they preserve a canonical slug as described above. Use the saved `install_command` / `install` when present, or explicit package-install guidance such as `npx skillpacks install <pack...>` when the saved entry lists packs.
   - After a deck recommendation exists, keep downstream skill routing as secondary context only. For example, after `business-afps` installs the `business-research` pack, name the likely first post-install skill (`$customer-discovery`, `$devtool-positioning`, `$ord-scan`, `$vard-scan`, or `$game-audience`) without making it the primary command.
   - When high-confidence deck installation is the primary command, include a copy-pasteable secondary post-install line: `After install, start with: $customer-discovery [research/{slug}]`. Replace `$customer-discovery` with the exact likely first post-install skill for non-business decks, and include the scoped product path argument when a non-archived `research/{slug}` product path is available.

4. **Interrogate until concept-ready (adaptive rounds 2..N)**
   - Build adaptive follow-up interrogation rounds (`interrogation/idea-scope-brief-r{N}-{branch}.html`) seeded by the prior round's compiled answers, each with at least one open input (`data-open-input`) and its own answer sidecar.
   - Terminal fallback cadence is one primary decision question per turn by default. Use short follow-up bullets only when they clarify the same decision, not to batch unrelated questions.
   - Resolve only concept-level ambiguity:
     - what problem exists
     - who might care
     - what outcome changes for them
     - what makes the idea different enough to investigate
     - what must stay out of scope
     - what constraints are real now
   - When unsure, recommend a practical default and clearly mark it as an assumption.

5. **Coverage checkpoint**
   - This checkpoint is the interrogation loop's **confidence-gate exit**: build the exit interrogation round with `data-interrogation-gate="coverage-checkpoint"` presenting the final concept summary, unknowns, and readiness for customer discovery. Do not advance to step 6 until the user confirms completeness or every area is waived; flagging a gap raises the round number and continues the loop. (Terminal fallback: present the checkpoint inline per the Manifest Visibility Rule.)
   - Restate the resolved concept identity, slug, and exact output paths before writing.
   - If the conversation pivoted from the initial concept to a different central concept, write the pivoted concept to its own slugged brief and preserve the initial concept as a related or future concept in the brief and interview log. Do not merge both concepts into one generic project-level brief.
   - Ask whether any core premise, constraint, or non-goal is wrong before writing.

6. **Build pre-approval alignment preview**
   - Before writing any canonical `research/**/idea-brief.md`, `research/**/idea-brief-interview.md`, legacy flat `research/idea-brief-{slug}.md` variant, or `research/.progress.yaml`, build `alignment/idea-scope-brief-{topic}.html` as the review artifact.
   - The HTML page must render the Idea/Concept Assumptions Manifest, artifact destinations, proposed file changes, coverage checkpoint, and approval gates, including any Market Structure Handoff and Deck Fit Handoff.
   - Attempt to open the page in the browser and point the user at the repo-relative path.
   - Treat coverage-checkpoint confirmation as non-final; it only confirms the draft scope is ready to preview. Only final compiled YAML from the alignment page authorizes canonical writes.
   - Before compiled YAML approval, the next action is review or revision of the HTML alignment page. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after final compiled YAML approval has been provided and the approved artifacts below have been written or updated.
   - When feedback-only YAML is provided, revise the alignment page and ask again; do not write canonical artifacts until final compiled YAML approval is provided.

### Review-Only Product Path Approval

When the user approves a product-path fork or split at the alignment page level but explicitly withholds canonical-write approval (e.g., "review only, do not write canonical files"):

1. **Do not write canonical files.** Keep `research/.progress.yaml`, `research/{slug}/idea-brief.md`, and `research/{slug}/idea-brief-interview.md` unchanged.
2. **Render fully in the alignment page.** The proposed manifest entry, idea brief sections, and interview log for the review-only path must be rendered in full in the alignment page HTML — not summarized, linked, or embedded.
3. **Mark the page as review-only-approved.** Set `approval_status: review-only-approved` in the alignment page status block. This is distinct from `confirmed` (canonical artifacts written) and `review` (awaiting any approval).
4. **Downstream treatment.** Downstream skills must treat a review-only-approved path as provisional: it may be referenced as concept context, but it is not a canonical product path until manifest approval is later granted via a subsequent alignment cycle. See the provisional-path evidence rule in customer-discovery and competitive-analysis contracts.

## Output

Before writing anything in this section, verify the alignment page has final compiled YAML approval. Do not write canonical idea briefs, interview logs, or `research/.progress.yaml` until `alignment/idea-scope-brief-{topic}.html` has been reviewed and the user has provided final compiled YAML approval. Coverage-checkpoint confirmation is not final approval and does not authorize these writes.

Write:

- For one unambiguous project-level concept only: `research/idea-brief.md` and `research/idea-brief-interview.md`.
- When a product identity is known, multiple concepts exist or may exist, or a pivot occurs: prefer `research/{slug}/idea-brief.md` and `research/{slug}/idea-brief-interview.md`; preserve flat `research/idea-brief-{slug}.md` only as legacy compatibility when no product path is being introduced.
- If `$ARGUMENTS` names a non-archived product path, use unsuffixed scoped files under `research/{slug}/`: `research/{slug}/idea-brief.md` and `research/{slug}/idea-brief-interview.md`.
- `research/.progress.yaml` — create or update only when multiple concepts, product paths, product lines, product-path scopes, or pivots are present. Use `product_paths` terminology instead of branch terminology.

The idea brief must include:

- `## Summary`
- `## Problem Hypothesis`
- `## Beneficiary Hypothesis`
- `## Product Category Guess`
- `## Value Wedge`
- `## Constraints`
- `## Non-Goals`
- `## Assumptions And Unknowns`
- `## Customer Discovery Readiness`
- `## Deck Fit Handoff`
- `## Next Steps`

The `## Customer Discovery Readiness` section must state whether the concept is ready for `$customer-discovery`, what inputs `$customer-discovery` should use, and which assumptions should be tested first. If a scoped product path is active, name it as the `$customer-discovery` argument, such as `$customer-discovery research/{slug}`. If a Market Structure Handoff exists, include the apparent sides and value exchange as explicit inputs for `$customer-discovery` to validate or refute. If a high-confidence Deck Fit Handoff exists, explain that deck installation is the primary next command and customer discovery or other first workflow skills are secondary post-install context; still name the exact first post-install skill and scoped path argument when available.

The `## Deck Fit Handoff` section must state the best candidate deck, whether it came from saved repo config or canonical fallback metadata, the confidence level, the domain/tempo signals, the install command, and the likely first post-install skill. When confidence is high, include the exact secondary line `After install, start with: $customer-discovery [research/{slug}]`, replacing the skill and scoped path as needed. If no deck has high confidence, state the strongest candidates and why fallback routing is safer.

The `## Next Steps` section must recommend exactly one primary command:

- If Deck Fit Handoff confidence is high for a canonical deck: `npx skillpacks install-deck <deck>`.
- If Deck Fit Handoff confidence is high for a customized saved deck with an explicit install command: use that exact saved install command.
- If Deck Fit Handoff confidence is high for a customized saved deck with a pack list but no install command: `npx skillpacks install <pack...>`.
- If no deck has high confidence and the concept appears to be a business app or user-facing product while the business research lane is not enabled: `npx skillpacks install business-research` from the project shell — this installs the research skills (customer discovery, competitive analysis, value prop, positioning, lean canvas) needed before any repo bootstrapping or development.
- If no deck has high confidence and `business-research` or the compatibility `business-app` alias is enabled: `$customer-discovery`.
- If no deck has high confidence and the concept already has customer-discovery/market evidence but needs journey, onboarding, conversion, or retention planning: `npx skillpacks install customer-lifecycle` from the project shell.
- If no deck has high confidence and project type is unclear: `scripts/pack.sh recommend`.

When a deck primary command is available, downstream research, discovery, or first-workflow skill routing must appear only as secondary context, not as the primary command. For high-confidence deck installs, include exactly one copy-pasteable secondary post-install command line after the primary command, formatted as `After install, start with: $customer-discovery [research/{slug}]` for Codex business/customer-discovery routes when the product path is known.

Include 1-3 other options only when they are materially useful.

### Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/idea-scope-brief-{topic}.html`.

## Constraints

- Keep the skill short and pre-research.
- Do not write specs, UX variants, UI specs, roadmap phases, or implementation tasks.
- Do not recommend `$scaffold` unless the user explicitly asks to create a package/app shell before research; normal product flow scaffolds after research, prototype consolidation, spec, roadmap, and phase planning identify the first implementation target. `$scaffold` requires the monorepo pack (`npx skillpacks install monorepo` from the project shell).
- Do not update `tasks/todo.md`.
- New files do not need archive snapshots. Before replacing an existing idea brief, including slugged briefs, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Migration: if a project already has `research/concept-brief.md`, `research/concept-brief-interview.md`, or any `research/{slug}/concept-brief*.md` / `research/concept-brief-{slug}*.md` from a prior run, rename it to the `idea-brief` equivalent before re-running. Write only the `idea-brief` names and no longer recognizes the legacy `concept-brief` filenames.

## Interrogation Page

Follow the shared interrogation-page convention via the packaged convention resolver; output path is `interrogation/idea-scope-brief-r{N}-{branch}.html`. Before producing research, run the stage-zero interrogation loop, starting with the assumptions manifest as round 1, and loop until the confidence gate passes. This skill **cannot advance to stage one until** the confidence gate passes with at least one completed interrogation round and every interview area covered or waived. Each round page must contain at least one genuinely open input (`data-open-input`).

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
