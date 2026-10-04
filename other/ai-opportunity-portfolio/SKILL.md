---
name: ai-opportunity-portfolio
description: "Identifies, scores (5-dimensional model: Business Impact, Technical Feasibility, Data Readiness, Strategic Alignment, Speed to Value/Risk), and prioritizes AI use cases with a 2x2 matrix (Quick Wins / Strategic Bets / Deprioritize / Hard-Low Value) — and classifies incremental and transformative opportunities separately."
---

# AI Opportunity Portfolio

## Purpose

Turns a raw list of AI use-case candidates (typically 20–100 items) into
an objectively scored, prioritized portfolio, from which the 3–5 highest-
value, lowest-risk items are selected to move forward. The skill
deliberately separates two different opportunity types —
**incremental efficiency gains** (making an existing process faster/
cheaper) and **transformative innovation** (new business that wasn't
possible before current AI capabilities) — because they're assessed
partly against different criteria.

## Anchored in research

- LinkedIn Skills on the Rise 2026 — AI Business Strategy
- Market research: open "Senior AI Business Designer"-type job postings
- A research report supplied by the user, "AI Business Designer in the
  Age of AI" (2026) — identifying AI opportunities at the strategic
  level (the original problem-type/data/flywheel/agentic-ness triage,
  now folded into point 4 below)
- Research digest "Methods, Frameworks, and Competencies for Identifying
  AI Opportunities and Capacity in Business" (2026) — the 5-dimensional
  scoring model (a synthesis of several industry AI capability
  reports), the 2x2 prioritization matrix, the Value Play taxonomy for
  transformative opportunities, the Deploy-Reshape-Invent taxonomy

## Method

1. **Assemble the raw list of candidates.** Start from existing friction
   points and value-chain bottlenecks — not from technology. Two
   complementary ways to assemble the raw list:
   - **Bottom-up** (if the process is already precisely described):
     use `../task-level-decomposition-and-automation-fit/SKILL.md` —
     its Automate/Augment-classified tasks are grouped here into
     larger opportunities.
   - **Top-down** (a fast first pass before a detailed process
     description): use `../ai-capability-pattern-matching/SKILL.md` —
     it poses the client the diagnostic questions of a ready-made
     capability pattern library and produces a validated raw list.
   If neither has been used, collect the list directly from
   stakeholders.
2. **Sort every candidate into one of two lanes before scoring:**
   - **Incremental efficiency gain** — the current process is done
     faster/cheaper. Cost-saving- and speed-driven (bottom-line
     impact).
   - **Transformative innovation** — a new business, product, or
     revenue stream that wasn't possible before current AI
     capabilities. Growth-driven (top-line impact). Check every
     candidate claimed as transformative against the Value Play
     taxonomy (point 3) — if it doesn't fit any of the three
     architectures, it's probably actually an incremental efficiency
     gain disguised as a big idea.
3. **For transformative candidates: check against the Value Play
   taxonomy.** Three known architectures for creating new AI value:
   - **Zero-Marginal-Cost Expertise** — packaging complex specialist
     expertise (legal, technical, medical) into a real-time,
     scalable service.
   - **Hyper-Personalization at Scale** — the product/service becomes
     dynamic for every user individually (e.g. tailored learning
     paths, financial products).
   - **Outcome-Based / Agentic Business** — moving from seat-based
     licensing/access pricing to outcome-based pricing (e.g. billing
     only for a resolved ticket or a closed deal).
   If a candidate doesn't fit any of these and isn't clearly a
   combination of them, reconsider whether it belongs in the
   transformative lane.
4. **Score every candidate on five dimensions (1–5 per dimension, max
   25 total):**
   - **Business Impact** — measurable euro or time value (ROI, hours
     saved, new revenue, churn impact).
   - **Technical Feasibility & AI Fit** — is the problem probabilistic
     or deterministic in nature? Does current LLM/AI technology fit
     the task without unreasonable hallucination risk? (Use the SML
     assessment from `../task-level-decomposition-and-automation-fit/SKILL.md`
     here if available — the problem type prediction/classification/
     generation also belongs in this dimension.)
   - **Data Readiness** — is the needed data available, in structured
     form, high quality, and interfaceable? Also assess **data
     flywheel potential**: does the solution generate unique data in
     use that improves the model over time and reinforces competitive
     advantage, or is it one-off data with no self-reinforcing loop?
     For a deeper diagnosis (the role of data, quality/bias,
     validating a flywheel claim), see
     `../../../data-strategy-and-literacy/skills/data-role-diagnosis/SKILL.md`
     and `../../../data-strategy-and-literacy/skills/data-ai-strategy-design-and-prioritization/SKILL.md`.
   - **Strategic Alignment** — does the target support the
     organization's 1–3-year core strategy, or is it a stand-alone
     experiment?
   - **Speed to Value & Governance/Risk** — implementation time as
     well as regulatory risk profile (e.g. EU AI Act classification:
     prohibited, high risk, low risk — see
     `../responsible-ai-and-governance-check/SKILL.md`). Also include
     **the degree of agentic-ness** here: is traditional rule-based
     automation enough, or does the opportunity require agentic,
     independent decision-making in unpredictable situations — an
     agentic solution is more expensive to build and govern, which
     slows down the Speed to Value score and should show up in it.
5. **Place every candidate on a 2x2 prioritization matrix** (vertical
   axis: Business Impact, horizontal axis: Technical Feasibility — use
   the point-4 scores):
   - **Quick Wins** (high impact, high feasibility) — low cost, fast
     implementation. Active piloting candidates.
   - **Strategic Bets** (high impact, low feasibility) — often
     transformative, require significant data/architecture investment
     before they're worth starting.
   - **Hard / Low Value** (low impact, low feasibility) — high
     technical bar, small ROI. Avoid.
   - **Deprioritize** (low impact, high feasibility) — easy to do but
     not worth it; low value doesn't justify the resources even when
     implementation would be easy.
6. **Also classify the selected Quick Wins and Strategic Bets items
   using BCG's Deploy-Reshape-Invent taxonomy** — this is a DIFFERENT
   question from the point-5 matrix: the matrix answers "is this worth
   doing and is it easy," Deploy-Reshape-Invent answers "what kind of
   change does this require of the organization":
   - **Deploy** — rolling out ready-made AI tools (e.g. copilots) for
     point tasks. Doesn't require process redesign.
   - **Reshape** — redesigning core functions and end-to-end
     processes around AI. Requires process change.
   - **Invent** — creating entirely new business models, products,
     and revenue streams. Requires building new business.
   **Don't confuse this with `../ai-capability-roadmap/SKILL.md`'s
   Horizon 1/2/3 breakdown** — Deploy-Reshape-Invent describes THE
   NATURE OF THE CHANGE (how deeply it touches the organization),
   Horizon 1/2/3 describes THE TIMELINE (when it's done). The same
   Reshape-level opportunity can land in any horizon depending on
   resources and dependencies.
7. **Produce the final output: a prioritized AI Opportunity Portfolio /
   Backlog** — for every selected item: name, lane (incremental/
   transformative; if transformative, which Value Play), 5D scores and
   total score, 2x2 position, Deploy/Reshape/Invent class. Move the
   3–5 highest-priority items into
   `../../../business-case-and-analysis/skills/business-case-builder/SKILL.md`
   for a deeper business case.
8. Validate the result with stakeholders or your own experience-based
   checklist. Make sure in particular that opportunities aren't
   assessed as an isolated silo but in relation to the organization's
   existing strategic goals.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured
  draft to support a human decision.
- Doesn't confirm figures, market data, or competitor data from
  memory — it uses the inputs you provide, or marks an assumption
  clearly (`[assumption — verify]`).
- Doesn't assess technical feasibility in depth — the Technical
  Feasibility dimension here is a rough 1–5 rating, not technical due
  diligence. For a deeper assessment, see
  `../ai-use-case-feasibility-and-poc-scoping/SKILL.md`.
- Doesn't do the task-level decomposition itself — if the raw list
  hasn't been assembled at the task level yet, use
  `../task-level-decomposition-and-automation-fit/SKILL.md` first.
- Doesn't replace `../ai-capability-roadmap/SKILL.md` for scheduling —
  it produces a prioritized list, not a scheduled roadmap.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb and heuristics for this technique — e.g.
  which dimensions carry the most practical weight in different
  industries
- concrete templates (into `../../references/`, e.g. a 5D scoring
  table template)
- reference cases / your own examples
- what this skill deliberately does *not* do (guardrails, common
  mistakes) — add to the list above

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new
fields to the frontmatter** — `name` and `description` are the only
ones allowed (see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Preceding skill in this pack (if a raw list doesn't exist yet):
  `../task-level-decomposition-and-automation-fit/SKILL.md` (bottom-up)
  or `../ai-capability-pattern-matching/SKILL.md` (top-down)
- Next in this pack (business model design): `../ai-native-business-model-canvas/SKILL.md`
  — designs the transition from an AI-enhanced business to an
  AI-native business model using an extended Business Model Canvas.
- Next in this pack (technical validation): `../ai-use-case-feasibility-and-poc-scoping/SKILL.md`
  — determines the technical boundary conditions of an AI use case and
  scopes the PoC phase.
- Next in this pack (scheduling): `../ai-capability-roadmap/SKILL.md`
  — places the selected items on a Horizon 1/2/3 timeline (a different
  question from this skill's Deploy/Reshape/Invent classification, see
  point 6).
- Related skill in another pack: `../../../opportunity-recognition/skills/opportunity-value-assessment/SKILL.md`
  — a more general, non-AI-specific opportunity assessment model.
- If the whole process is run as a paid consulting engagement:
  `../ai-discovery-engagement-design/SKILL.md`
- If the client is a public-sector or non-profit body: pre-screen with
  `../../../specialisation-packs/public-sector-ai-service-design/skills/ps-ai-opportunity-screening-for-public-value/SKILL.md`
  before or alongside this skill — public-value fit and mandate
  alignment change how the Business Impact dimension should be weighted.
- A ready-made skill chain for this situation: see `../../../playbooks/`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
