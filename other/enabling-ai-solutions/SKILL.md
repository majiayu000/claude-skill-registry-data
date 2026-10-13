---
name: enabling-ai-solutions
description: >
  Designs and scopes AI solution architectures for personal projects, platform builds,
  and internal tooling. Use when mapping technical requirements to AI stack decisions,
  selecting LLM providers, sizing infrastructure, planning integrations, modeling costs,
  or producing a spec for any AI-enabled build. Triggers on: scope this AI build, what
  stack for this, design an AI solution, AI implementation plan, architecture for this
  project, how should I build this, what would this cost, help me think through the tech,
  AI enablement plan, integration architecture, infrastructure sizing, technology
  selection, reference architecture, solution design, or any request to turn a use case
  into a buildable technical plan.
version: "2.0.0"
allowed-tools: Read, Write, Web_Fetch
license: MIT
---

# Enabling AI Solutions

**TL;DR:** Turns a use case + constraints into a scoped, costed, buildable AI architecture. Personal projects, platform builds, internal tooling. Output scales from a quick stack decision to a full spec doc with cost model.

---

## File Map

```
enabling-ai-solutions/
├── SKILL.md                              ← You are here (80% of use cases)
├── references/
│   ├── component-selection.md            ← LLM tiers, frameworks, data layer, infra options
│   ├── sizing-calculator.md              ← Volume modeling, cost math, tier methodology
│   └── compliance-patterns.md           ← GDPR, HIPAA, [COMPLIANCE FRAMEWORK], PCI-DSS implementation
├── templates/
│   ├── quick-stack-decision.md           ← 2–5 min output for fast answers
│   ├── architecture-diagram.md           ← Mermaid diagram with routing pattern
│   └── spec-doc.md                       ← Full project spec for any scoped build
├── examples/
│   ├── solo-knowledge-base.md            ← Completed spec: personal knowledge base build
│   ├── research-agent-personal.md        ← Completed decision: personal research agent build
│   └── quick-stack-selection.md          ← Completed quick output: pgvector vs Pinecone
├── scripts/
│   └── sizing_calc.py                    ← Runnable sizing calculator (Python 3.10+)
└── workflows/
    └── discovery-to-delivery.md          ← Full process: intake → architecture → delivery
```

---

## Decision Tree: What Output Do You Need?

```
What's the context?
  ├─ Quick answer ("what stack for X?", "should I use A or B?")
  │   └─ → Read templates/quick-stack-decision.md
  │      → See examples/quick-stack-selection.md for a worked output
  │
  ├─ Personal project / platform build (FlashFusion, flashnframe, etc.)
  │   └─ → Read templates/architecture-diagram.md
  │      → See examples/research-agent-personal.md for a worked output
  │
  ├─ Scoped build (needs a full spec, phased plan, or cost model)
  │   └─ → Follow Golden Path below
  │      → Read templates/spec-doc.md for the output format
  │      → See examples/solo-knowledge-base.md for a worked output
  │
  └─ Scoped build with compliance or regulated data
      └─ → Golden Path + run scripts/sizing_calc.py
         → Read references/compliance-patterns.md
```

---

## Examples (Inline Summaries)

**Example 1 — Solo scoped build**
> "I want to build a personal knowledge base — ingest my notes, Notion exports, and research docs, then query them conversationally. Just me using it."

→ Scope → RAG pattern → Small tier (solo user) → spec doc. Full worked output: `examples/solo-knowledge-base.md`

**Example 2 — Personal platform build**
> "I want to add a research agent to FlashFusion — web search, summarize, store results."

→ Skip discovery. Stack decision: Sonnet 4.6 + Tavily + Supabase. Full worked output: `examples/research-agent-personal.md`

**Example 3 — Quick technology selection**
> "Should I use Pinecone or pgvector for this?"

→ Quick stack decision output. Full worked output: `examples/quick-stack-selection.md`

---

## Golden Path

### Step 1: Gather Context (2–5 questions max)

Ask only what blocks correctness. If already clear from conversation, skip.

```
- What problem is AI solving? (automation / retrieval / generation / analysis / multi-agent)
- Scale: users, requests/day, data volume?
- Existing stack and cloud provider?
- Compliance requirements? (HIPAA, GDPR, [COMPLIANCE FRAMEWORK], PCI-DSS, or none)
- Budget range, or "give me tiers"?
```

For structured discovery: see `workflows/discovery-to-delivery.md` → Discovery Phase.

### Step 2: Map Architecture Pattern

| Use Case | Pattern |
|----------|---------|
| Knowledge retrieval / Q&A | RAG: LLM + vector DB + document pipeline |
| Conversational agent | LLM + memory + tool use layer |
| Data analysis / reporting | LLM + structured data connector |
| Workflow automation | LLM + n8n / Make + trigger layer |
| Multi-agent orchestration | See `orchestrating-ai-agents` skill |

### Step 3: Select Components

Read `references/component-selection.md`. Choose LLM tier, framework, data layer, infra, observability. Document rationale — don't just list components.

### Step 4: Size Infrastructure

Option A — Quick: Use tier table in `references/sizing-calculator.md`.
Option B — Precise: Run `scripts/sizing_calc.py` with actual inputs.

### Step 5: Map Security and Compliance

For regulated data or any client engagement: read `references/compliance-patterns.md`. Apply the relevant framework checklist. Flag data residency before finalizing LLM selection.

### Step 6: Produce Output

- **Quick decision** → `templates/quick-stack-decision.md`
- **Architecture diagram** → `templates/architecture-diagram.md`
- **Full spec doc** → `templates/spec-doc.md`

Check `examples/` before writing if unfamiliar with the output format.

---

## 2026 Model Routing Pattern (Standard for Production)

Single-model setups waste 60–80% of LLM budget at scale. Route by complexity:

```
Request → Classifier (Haiku 4.5 / GPT-5.4 nano)
  ├─ Simple (extract, classify, format) → Haiku 4.5 / GPT-5.4 nano   <$0.10/M
  ├─ Medium (RAG, generation, analysis) → Sonnet 4.6 / GPT-5.4       $3–10/M
  └─ Complex (agents, long-doc, code)   → Opus 4.6 / GPT-5.4         $5–25/M
```

Add routing at >1K req/day. Below that, pick one mid-tier model and move on.

---

## Validation Gates

Before shipping any architecture:
- [ ] All integration points documented (auth, data flow, error handling)
- [ ] LLM selection justified against latency SLA and data privacy
- [ ] Infrastructure sized for peak (provisioned) or confirmed auto-scaling (serverless)
- [ ] Compliance requirements addressed or explicitly out of scope
- [ ] No single points of failure documented
- [ ] Cost broken down by component with realistic usage assumptions
- [ ] Secrets: no API keys in frontend/client-side code — env vars + server-side only
- [ ] Rollback strategy defined

---

## Cross-References

- `roi-calculator-building` — cost/benefit modeling for build decisions
- `use-case-discovery` — structured requirements gathering before architecture work
- `orchestrating-ai-agents` — multi-agent and MCP-based system patterns
- `ai-agents-workflow` — automation pipelines and tool integrations

---

## Self-Verification

- [ ] Gerund name matches directory name
- [ ] Description trigger-dense, under 1024 chars
- [ ] SKILL.md under 500 lines
- [ ] 3+ examples with concrete use cases
- [ ] All file map entries exist on disk
- [ ] No hardcoded branding, placeholder emails, dead cross-references
- [ ] CLAIMS footer present

---

## CLAIMS

- [SOURCED] Model routing reduces LLM cost 60–80% at scale vs. routing all traffic to a frontier model. Source: iternal.ai LLM selection guide, April 2026.
- [SOURCED] In mid-2026, the primary bottleneck for AI production systems is latency, reliability, and integration complexity — not token cost. Source: credentials.substack.com, Feb 2026.
- [GENERATED] S/M/L sizing tiers are reasonable starting estimates; actual costs vary by caching, usage distribution, and provider pricing changes.
- [GENERATED] Compliance framework content is current as of Jan 2026. Verify with legal for client-facing compliance commitments.

## COUNTEREXAMPLE

- Model routing adds classifier latency (~50–100ms) and engineering complexity. For low-volume or uniform-complexity workloads a single mid-tier model is simpler and cheaper.
- pgvector degrades above ~5M vectors; the recommendation inverts at that threshold.

## CONTRADICTIONS

- ! "Size for peak + 30% buffer" applies to provisioned deployments only. Serverless auto-scales — manual headroom is both unnecessary and misleading on serverless cost projections.
- ! "Strict p95 <500ms SLA" may prevent using frontier models entirely, making routing architecture moot — all traffic must stay on budget tier regardless of complexity.
