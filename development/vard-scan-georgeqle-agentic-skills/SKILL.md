---
name: vard-scan
description: Scan for viral app opportunities from trends, gaps, and user pain points
type: research
version: v0.2
required_conventions: [alignment-page]
context_intake: artifact_only
---

# VARD Scan

Invoke as `/vard-scan`.

Rapid opportunity scanner for viral app ideas. Produces a lightweight brief after scope and artifact approval - enough to decide whether to build this week, not a full idea-scope-brief.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, timely signal categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the rapid VARD scan and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with the candidate briefs and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, task, or alignment files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language before final artifact approval. The approval request itself is the next action. Only emit `/vard-align` routing after the approved canonical scan artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1. For this skill, flat mode proposes `research/_working/preliminary-vard-scan-research.md`; product-path mode proposes `research/{slug}/_working/preliminary-vard-scan-research.md`.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. For VARD scan, write `research/_working/preliminary-vard-scan-research.md` or `research/{slug}/_working/preliminary-vard-scan-research.md`. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Keep the packet lightweight: 2-5 candidates, each only a few lines plus evidence/source notes. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate charts or diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a `Full Preliminary Packet` or `Full Working Packet` raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. For this skill, flat mode writes the approved scan to `research/vard-scan.md`; product-path mode writes `research/{slug}/vard-scan.md`. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Process

1. **Resolve scope:** Use `$ARGUMENTS` to narrow domain, audience, platform, timing window, or product path. If a non-archived `research/{slug}/` product path is in scope, use product-path output locations; otherwise use flat `research/` output locations.
2. **Gather signals:** After Stage 1 approval, scan for opportunities across:
   - Trending topics, memes, cultural moments with app potential
   - App Store / Play Store gaps and underserved niches
   - Twitter/Reddit/HN pain points that a simple tool could solve
   - Existing apps with poor UX that could be reimagined
   - Seasonal or time-sensitive opportunities
3. **Filter for VARD fit:** Each candidate must pass:
   - Buildable in 1-3 days by a solo developer
   - Viral or shareable mechanic (results people screenshot, share, or talk about)
   - No complex backend requirements (serverless-friendly)
   - Clear distribution channel (social, SEO, Product Hunt, etc.)
4. **Produce preliminary brief:** For each viable candidate (aim for 2-5), write the Stage 2 working packet with:
   - One-line concept
   - Why now (timeliness signal)
   - Viral mechanic (what makes people share it)
   - Build estimate (hours)
   - Distribution channel
   - Revenue potential (none / ads / freemium / one-time)
   - Evidence notes and confidence level
5. **Rank for artifact review:** Order candidates by virality, feasibility, and distribution clarity. Highlight the proposed top pick only in the Stage 2 working packet and artifact-review alignment page.
6. **Finalize after approval:** After final artifact approval, archive the working packet, write the approved canonical scan artifact, confirm the alignment page, and then recommend `/vard-align`.

## Output

Stage 1 output is only the scope-review alignment page and a concise request for final compiled YAML approving scope.

Stage 2 output is the working packet at `research/_working/preliminary-vard-scan-research.md` or `research/{slug}/_working/preliminary-vard-scan-research.md`, plus the updated artifact-review alignment page.

Stage 3 output is the approved canonical scan artifact at `research/vard-scan.md` or `research/{slug}/vard-scan.md`. End the final approved artifact with:

```md
**Top pick:** <concept name>
**Next work:** validate top pick feasibility
**Recommended next command:** /vard-align
```

## Constraints

- Do not produce full idea-scope-brief depth - keep each candidate to a few lines.
- Do not begin implementation or scaffolding.
- Do not run paid API calls or external account actions.
- If `$ARGUMENTS` specifies a domain or constraint, narrow the scan accordingly.
- Do not write canonical scan artifacts, specs, tasks, or next-command routing before final artifact approval.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/vard-scan-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention.
