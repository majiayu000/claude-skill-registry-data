---
description: Generate a cross-domain project summary report
---

# Report

Generate a comprehensive cross-domain report for "$ARGUMENTS" (or the entire `.metapowers/` directory if no argument given). Summarize progress, findings, and readiness across all active domains.

## Prerequisites

Requires `.metapowers/` directory with at least one domain's artifacts.

## Process

1. **Read the domain registry:**
   - Read `plugins/metapowers/shared/domain-registry.md` for domain structure
   - Read `.metapowers/config.md` if it exists for project context

2. **Scan all domain artifacts:**
   - For each domain with artifacts in `.metapowers/`:
     - Read the most recent/final artifact (e.g., the last completed phase)
     - Extract key findings, decisions, and outcomes
     - Note completion status

3. **Generate domain summaries:**

   For each active domain, extract the key insight:
   - **Research:** Problem statement and top recommendation
   - **Branding:** Positioning statement and brand personality
   - **Design:** Component contracts and design decisions
   - **Development:** Features built, test status, commits
   - **Accessibility:** Conformance level and outstanding issues
   - **Marketing:** Campaign strategy and channel plan
   - **Coaching:** Scores and top improvement areas
   - **Leadership:** Team structure and OKRs
   - **Project Management:** Sprint status and velocity
   - **Legal:** Compliance status and outstanding risks

4. **Identify cross-domain connections:**
   - Is branding being followed in marketing?
   - Are accessibility issues addressed in development?
   - Does the design align with the research findings?
   - Are coaching recommendations being acted on?

5. **Generate readiness assessment:**
   - What's complete and ready?
   - What's in progress?
   - What's blocked or needs attention?
   - What domains haven't been started but should be?

6. **Write the report** to `.metapowers/reports/$ARGUMENTS-report.md` (or `.metapowers/reports/<date>-project-report.md` if no argument) with sections:
   - **Executive Summary** — one-paragraph project status
   - **Domain Status** — per-domain progress and key findings
   - **Cross-Domain Insights** — connections and alignment
   - **Readiness Assessment** — what's ready, in progress, blocked
   - **Recommended Next Steps** — prioritized actions

## Output

The report written to `.metapowers/reports/`. Present the executive summary and recommended next steps to the user.
