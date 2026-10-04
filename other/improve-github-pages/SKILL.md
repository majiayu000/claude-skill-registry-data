---
name: improve-github-pages
description: Analyze an existing GitHub Pages site and any available repository wiki, propose prioritized evidence-backed improvements, pause for explicit user approval, and then implement only the approved full or partial change set. Use for staged review-to-remediation of Pages content, navigation, accessibility, responsive layout, visual hierarchy, color scheme, typography, branding, and interactions. Do not use for a report-only audit, a net-new site, or changes the user already specified without requesting an approval gate.
---

# Improve GitHub Pages

Turn an existing Pages site into a reviewable improvement program, then apply only the changes the user selects.

## Enforce the two-phase gate

Phase 1 is read-only. Inspect, render, audit, and propose, but do not edit site files, dependencies, workflows, repository settings, or generated output. Always stop after presenting the proposal, even when the opening request broadly says to improve or redesign the site.

Phase 2 begins only after the user explicitly approves all changes or identifies approved proposal IDs. Approval to implement site changes does not authorize commit, push, publication, workflow changes, repository settings, domains, credentials, analytics, or external services unless those actions are separately named.

Do not treat “looks good,” “interesting,” or a request for explanation as implementation approval. Resolve ambiguous or conflicting selections before editing.

## Coordinate the Pages family

Treat the first three applicable specialists as required Phase 1 passes, not optional hand-offs. Read and apply their instructions so each concern contributes to the shared proposal set or coverage matrix.

- Apply `audit-github-pages-ux` to collect rendered evidence and prioritize defects.
- Apply `github-pages-content-architecture` to content, hierarchy, labels, navigation, and local search proposals.
- Apply `github-pages-visual-system` to color, typography, spacing, themes, branding, and responsive proposals or implementation.
- Apply `create-github-pages` when approved work changes the framework, routes, base path, build, dependencies, or deployment.

Keep one proposal ID and one approval state across these specialist concerns.

## Read the improvement contract

Read [references/approval-and-remediation.md](references/approval-and-remediation.md) before analyzing the site or interpreting approval.

## Phase 1: analyze and propose

Establish the repository, production-equivalent build, expected Pages base path, intended readers, current routes, branding evidence, and uncommitted changes. When a GitHub Wiki exists and is available through a supplied URL, connector, or local checkout, inventory it for useful setup guidance, examples, FAQ, troubleshooting, architectural rationale, and other material missing from the Pages site. Verify wiki claims against the current repository, flag stale or conflicting pages, and prefer linking, consolidating, or importing from a maintained canonical source over blind copying. Wiki analysis remains read-only and does not authorize editing the wiki.

When rendering is possible, inspect representative desktop and narrow-mobile journeys in every supported theme. Clearly separate rendered evidence from source-only inference.

After the defect audit, run a separate design-opportunity pass even when the current site is usable and technically sound. Treat a generic framework theme, weak project identity, undifferentiated hierarchy, underused repository assets, or a presentation that explains the project without expressing its character as possible enhancement evidence rather than defects. Explore restrained refinement, a distinctive repository-grounded direction, and a bold direction that materially changes the site's visual character. Discard arbitrary or weakly supported ideas; do not require an existing usability failure before recommending a strong enhancement.

When external browsing is available and useful, inspect a small set of current, relevant reference sites for transferable patterns. Cite the exact sources, explain why each pattern fits this repository and its readers, and propose an adaptation rather than imitation. Keep this research read-only and report when it was unavailable or unnecessary.

Present the result in three parts:

1. **Confirmed issues:** demonstrated usability, accessibility, content, navigation, responsive, or visual defects.
2. **Design opportunities:** viable improvements to identity, hierarchy, typography, color, spacing, layout, imagery, interaction, or responsive expression that need not repair a defect.
3. **Coverage matrix:** mark every applicable audit area as `defect`, `opportunity`, `healthy`, `not applicable`, or `not verified`, with a short reason. Never let a checked area disappear merely because no change is recommended.

Within **Design opportunities**, include a **Bold proposals** subsection containing the strongest one to three repository-grounded visual directions when viable. If none survives the evidence and risk filters, say so explicitly and explain why. Do not manufacture a fixed count of cosmetic variants.

Give every actionable confirmed issue and design opportunity one stable `GP-` ID and one shared approval state. Each proposal must include observed evidence or current ceiling, the concrete change or concept, expected reader benefit, affected scope, risk, and verification. Bold proposals must also state boldness, repository evidence, the visual-system impact, and a preview plan. Show color or theme changes as semantic token mappings and rendered-use examples rather than an unexplained palette.

End with an explicit approval prompt such as:

> Approve all proposals, approve selected IDs such as `GP-01, GP-04`, request revisions, or decline. No files have been changed.

Then stop.

## Phase 2: implement the approved scope

Before editing, re-check repository status and the proposal assumptions. If the site or overlapping files changed after the proposal, explain the drift and refresh affected proposals rather than applying stale edits.

Implement only approved IDs and their necessary disclosed prerequisites. Preserve unapproved behavior, public routes, branding, canonical content, user changes, and deployment configuration. If an approved item becomes materially broader during implementation, stop and request approval for the expansion.

Run applicable production builds, link and route checks, and rendered verification. Report implemented IDs, deviations, verification evidence, unapproved proposals left untouched, and any separately authorized delivery status.
