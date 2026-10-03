---
name: research-amend
description: Amend approved research artifacts through a bounded alignment-gated workflow
type: analysis
version: v0.2
required_conventions: [alignment-page]
argument-hint: "[research path or artifact] [amendment request]"
visual_tier: document
---

# Research Amend

Invoke as `$research-amend`.

Use this skill when the user wants to correct, add, or reweight already-approved research without rerunning an entire Pattern A research workflow by default. Typical inputs include a missed competitor, corrected pricing/source fact, new customer quote, stale source, or downstream-impacting correction.

`research-amend` is a bounded amendment workflow. It does not replace `customer-discovery`, `competitive-analysis`, `positioning`, `journey-map`, `research-roadmap`, or `reconcile-research`; it decides whether a narrow amendment is valid, prepares a reviewed change packet, and writes canonical updates only after alignment approval.

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell instead of the target skill. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

## Amendment Boundaries

Only use the bounded amendment path for research that is already canonical, approved, and specific enough to patch safely.

- **Low impact:** factual correction, source URL/date update, typo, or one profile/detail that does not change recommendations. Patch the affected canonical artifact and evidence/search log.
- **Medium impact:** one missed competitor, one new customer evidence item, or one limited correction that changes a matrix row, gap, caveat, or local recommendation. Patch affected intermediate(s), canonical synthesis sections, and evidence/search log.
- **High impact:** change affects category definition, strategic map, top recommendations, positioning assumptions, ICP, journey sequence, or downstream routing. Do not small-patch. Route to the affected Pattern A framework(s) and synthesis rerun.
- **Systemic impact:** new ICP/category, many missed competitors, stale source base, invalid original scope, or broad evidence collapse. Do not small-patch. Recommend a full Pattern A rerun or `$research-roadmap` to plan the rerun.

A single missed competitor defaults to **medium impact** when it changes one competitive row or local comparison, and escalates to **high** only when it changes category framing, strategic grouping, top recommendations, or synthesis conclusions.

## Inputs And Scope Resolution

1. Parse `$ARGUMENTS` for a research path, artifact path, product slug, and requested change.
2. If no clear path is supplied, read `research/.progress.yaml` when present and resolve active non-archived product paths. Auto-select only when exactly one active path or one non-archived `research/{slug}/` directory exists; otherwise ask which scope to amend.
3. Locate the target canonical artifact(s), related framework intermediates, working/archive records, search logs, evidence logs, alignment pages, and `.progress.yaml` entries for the resolved scope.
4. If the target artifact is still in `review`, has an active run manifest, or is not yet canonical, stop and route to the producing skill's active approval flow instead of amending.
5. If source freshness matters, verify the specific facts needed for the amendment using available local evidence and, when necessary, current primary sources. Cite sources in the amendment packet.

## Workflow

### 1. Triage

Classify the request as add, remove, replace, reweight, or verify. Then classify impact as low, medium, high, or systemic using the ladder above.

If impact is high or systemic, write no canonical changes. Explain the escalation, list the affected artifacts/frameworks, and recommend the specific rerun route:

- `customer-discovery` for ICP, segment, buyer, or customer-evidence changes.
- `competitive-analysis` for competitor set, pricing, feature, market-map, or whitespace changes.
- `positioning` for category, narrative, differentiation, or strategic assumptions.
- `journey-map` for lifecycle, workflow, channel, or touchpoint changes.
- `research-roadmap` when the affected route is unclear or multiple tracks must be sequenced.

### 2. Build The Amendment Packet

For low/medium impact, write a non-canonical working packet before any canonical edits:

- Flat mode: `research/_working/research-amend-{topic}.md`
- Product-path mode: `research/{slug}/_working/research-amend-{topic}.md`

The packet must include:

- amendment request and classification;
- target artifacts and exact sections expected to change;
- evidence delta with source citations, timestamps, and confidence;
- before/after summary for every affected claim, row, recommendation, or caveat;
- proposed canonical edits;
- archive plan for superseded artifacts;
- rollback note;
- downstream impact check.

### 3. Alignment Gate

Create or update `alignment/research-amend-{topic}.html` in `review` state before canonical writes. The page must render the full amendment packet, not just a summary, and include approval gates for:

- impact classification;
- target artifact list;
- evidence sufficiency;
- proposed canonical edits;
- downstream impact and rerun decision.

Stop for review. While the page is in `review`, do not write canonical research, do not route downstream, and do not claim the amendment is complete.

End the terminal response with:

```text
## Next Work
Review the amendment page, compile response YAML, clear context, and paste the compiled YAML into a fresh session.
```

The compiled YAML in the page must begin with the invocation comment and include top-level `command` plus `agent_routing.command` set to the same `$research-amend <same scope argument>` invocation.

### 4. Apply Approved Amendment

Only after final compiled YAML has `approval_status: ready-for-agent-review` and no unresolved negative feedback:

1. Apply approved edits to the working packet and page first.
2. Archive every superseded canonical artifact, intermediate, search/evidence log, and alignment page that will be replaced to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-path>`.
3. Patch only the approved affected canonical/intermediate/search-log files.
4. Add an `## Amendment Note` or equivalent dated note to each amended canonical artifact, naming the changed claims, evidence delta, and alignment page.
5. Convert the alignment page to `confirmed` with the approval record preserved.
6. Remove or archive the active working packet according to the archive plan.

Do not expand the patch opportunistically. If approval reveals a broader impact than the packet covered, return to triage and build a new review page or route to a rerun.

## Output

- Impact classification and rationale.
- Amendment packet path or escalation route.
- Alignment page path and review status.
- Canonical files changed, only after approval.
- Verification/source checks performed.
- Residual risks.
- Next work and command.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/research-amend-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
