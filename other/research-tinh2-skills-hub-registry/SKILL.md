---
name: research
description: "Full-spectrum product research pipeline. Runs competitive analysis, technology trend scouting, user feedback analysis, and feature ideation. Triggers: on: research, competitive research, market research, feature discovery, what should we build next."
version: "2.0.1"
category: combo
platforms:
  - CLAUDE_CODE
---

You are an autonomous research-to-ideation agent. Do NOT ask the user questions.
Run the full pipeline below without pausing between phases.

TARGET:
$ARGUMENTS

============================================================
PHASE 1: COMPETITIVE GAP ANALYSIS  (/compete)
============================================================



PARALLEL EXECUTION: Use the Agent tool to run competitive analysis and feature discovery concurrently when both are independent.
- Agent A (Competitive Analysis): "Run /compete skill instructions — analyze the competitive landscape for this project. Return competitive gaps and opportunities."
- Agent B (Feature Discovery): "Run /new-features skill instructions — discover potential features from project docs and memory. Return feature candidates with priority."
- Wait for both agents to complete.
- Cross-reference findings: features that address competitive gaps get priority boost.


Follow the instructions defined in the `/compete` skill exactly.
Produce the full Competitive Gap Analysis output including all sections
(Product Identity, Competitive Landscape, Feature Matrix, Critical Gaps,
Strategic Gaps, Differentiators, Our Edges, Industry Trends, Recommended Roadmap, Summary).

Save the report to `docs/competitive-gap-analysis.md`
as specified by the `/compete` skill (create the `docs/` directory if it doesn't exist).

Do NOT stop here. Continue immediately to Phase 2.

============================================================
PHASE 2: TECHNOLOGY TREND RESEARCH
============================================================

Research current technology trends relevant to this project's domain.
Use web search to find:

1. **Emerging Technologies** — New frameworks, APIs, platforms, or paradigms
   that competitors or adjacent products are adopting (e.g., on-device ML,
   spatial computing, voice-first UX, AI-native workflows).
2. **Developer Ecosystem Shifts** — Changes in tooling, package ecosystems,
   or platform capabilities that could unlock new features or reduce cost
   (e.g., new OS APIs, free-tier expansions, open-source alternatives).
3. **UX/Design Trends** — Interaction patterns gaining traction in the
   category (e.g., progressive disclosure, ambient computing, micro-animations).
4. **Regulatory & Standards** — Upcoming regulations, accessibility mandates,
   or industry standards that may force or enable product changes.

For each trend, note:
- **Trend name**
- **Relevance** (HIGH / MEDIUM / LOW) — how directly it applies to this project
- **Adoption window** — how soon this matters (NOW / 6 months / 12+ months)
- **Opportunity** — what feature or improvement it could enable

Save to `docs/technology-trends.md`.

Do NOT stop here. Continue immediately to Phase 3.

============================================================
PHASE 3: USER FEEDBACK ANALYSIS
============================================================

Gather and analyze real user feedback from available sources:

1. **App Store Reviews** — If the product (or key competitors) are on app stores,
   search for reviews. Focus on 1-3 star reviews to surface pain points, and
   4-5 star reviews to find beloved features users would miss.
2. **GitHub Issues** — If the project or competitors have public repos, scan
   open and recently closed issues for feature requests, common bugs, and
   recurring complaints.
3. **Community Signals** — Search Reddit, forums, Twitter/X, or HackerNews
   for discussions about the product category. Note unmet needs users express.

Produce a summary with:
- **Top 10 Pain Points** — ranked by frequency/severity across all sources
- **Top 5 Beloved Features** — what users love and would be angry to lose
- **Top 5 Feature Requests** — most-requested features that don't exist yet
- **Sentiment Summary** — overall user sentiment toward the category

Save to `docs/user-feedback-analysis.md`.

Do NOT stop here. Continue immediately to Phase 4.

============================================================
PHASE 4: FEATURE IDEATION  (/new-features)
============================================================

Now follow the instructions defined in the `/new-features` skill exactly.

Read ALL `.md` files in the `docs/` directory — this includes:
- `docs/competitive-gap-analysis.md` from Phase 1
- `docs/technology-trends.md` from Phase 2
- `docs/user-feedback-analysis.md` from Phase 3
- Any other markdown files that already existed in the folder

Extract learnings from every file, synthesize feature ideas, and write
the report to `docs/NewFeatures-X.md` (where X is a 3-word kebab-case theme).

IMPORTANT: Features should heavily draw from ALL prior phases:
- Critical gaps and strategic gaps from Phase 1 → HIGH priority features
- Differentiator opportunities from Phase 1 → MEDIUM priority
- HIGH-relevance technology trends from Phase 2 → features that leverage new tech
- Top pain points and feature requests from Phase 3 → user-validated features
- Beloved features from Phase 3 → features to protect and enhance, not disrupt


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing all phases, validate the combined output:

1. Re-run the specific checks that originally found issues to confirm fixes.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

When all phases are complete, print a summary:

---
## Research Complete

**Files generated:**
1. `docs/competitive-gap-analysis.md` — Full competitive landscape + gap analysis
2. `docs/technology-trends.md` — Technology trends and opportunities
3. `docs/user-feedback-analysis.md` — User feedback from reviews, issues, and community
4. `docs/NewFeatures-[X].md` — Actionable feature ideas derived from all findings

**Key stats:**
- Competitors analyzed: [N]
- Technology trends identified: [N]
- User pain points surfaced: [N]
- Total gaps found: [N]
- Feature ideas generated: [N] (HIGH: [N], MEDIUM: [N], LOW: [N])

**Next steps:**
- Run `/spec [feature name]` to generate implementation stories
- Run `/iterate` to start building a feature
- Run `/arch-review` to assess architecture readiness for the proposed features
---


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /research — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

STRICT RULES:

- Do NOT skip any phase or reorder them.
- Do NOT ask the user for input between phases.
- Phase 4 MUST read the files written by Phases 1-3 — that's the whole point of the chain.
- All rules from `/compete` and `/new-features` apply to their respective phases.
- If a source is unavailable (e.g., no app store listing, no public repo), note it and move on — do not block the pipeline.
