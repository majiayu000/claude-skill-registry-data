---
license: Apache-2.0
name: ai-engineer
description: Build production-ready LLM applications, advanced RAG systems, and intelligent agents. Implements vector search, multimodal AI, agent orchestration, and enterprise AI integrations. Use PROACTIVELY for LLM features, chatbots, AI agents, or AI-powered applications.
allowed-tools: Read,Write,Edit,Glob,Grep,Bash,WebFetch,mcp__sequentialthinking__sequentialthinking
metadata:
  category: AI & Machine Learning
  tags:
    - llm
    - rag
    - agents
    - ai
    - production
    - embeddings
  provenance:
    kind: first-party
    owners:
      - port-daddy
  pairs-with:
    - skill: agentic-app-architecture
      reason: Decides the app's overall shape (transparency, memory, execution substrate) before this skill builds the RAG/agent internals inside it.
    - skill: agentic-infrastructure-2026
      reason: Picks the framework/observability/cost-governance stack this skill's RAG pipeline and agents run on top of.
    - skill: llm-router
      reason: Supplies the model-selection mechanics behind this skill's Model Routing Strategy decision point.
    - skill: episodic-memory-algorithms
      reason: Supplies the vector-store/retrieval algorithm internals behind this skill's RAG Component Selection decision point.
    - skill: prompt-engineer
      reason: Designs and audits the individual prompts this skill's LLM app is built from.
  io-contract:
    kind: deliverable
    consumes:
      - kind: ai-feature-requirement
        format: markdown
      - kind: ai-system-plan
        format: json
    produces:
      - kind: ai-system-design
        format: markdown
      - kind: ai-system-readiness-audit
        format: json
---
# AI Engineer

Expert in building production-ready LLM applications, from simple chatbots to complex multi-agent systems. Specializes in RAG architectures, vector databases, prompt management, and enterprise AI deployments.

## Decision Points

### RAG Component Selection
```
Start with a corpus policy, not a vendor preset:
├── Define data class, egress authority, retention, and disclosure filters
├── Select retrieval roles and a versioned profile for each
├── Bind every vector to `spaceId` (model/config/preprocessing/dimensions/metric)
├── Evaluate lexical+dense hybrid retrieval and bounded reranking on held-out tasks
├── Calibrate threshold, top-k, and reranking against cost-quality curves
└── Promote only the profile that meets the stated corpus-specific operating envelope
```

### Model Routing Strategy

Route through a versioned policy rather than query keywords, document count, or
provider names. First apply corpus authority, data-class, retention, egress,
tool, latency, and cost constraints. Then compare eligible profiles on the
target corpus and harness: task outcome, grounding, latency, cost, and failure
rate, with uncertainty. Keep the selected model/profile revision and the
evaluation receipt with each promotion. A request that does not fit a declared
operating envelope should be routed to an approved fallback or explicitly
rejected; it must not silently become lexical-only retrieval.

Model-selection mechanics belong to `llm-router`; this skill specifies the
evaluation and authorization inputs that a routing policy must consume.

### Agent vs RAG Decision
```
Task Classification:
├── Static Knowledge Query → Pure RAG
├── Need External APIs → Agent with tools
├── Multi-step Reasoning → Agent with planning
├── Real-time Data Required → Agent with live tools
└── Simple Q&A → RAG with fallback to agent
```

## Failure Modes

### **Semantic Mismatch Cascade**
**Symptoms**: Good retrieval precision but poor answer relevance, users say "close but not quite right"
**Detection Rule**: A held-out retrieval and answer-quality regression exceeds its pre-registered operating envelope.
**Root Cause**: Query and document embeddings optimized for different semantic spaces
**Fix**: Inspect authority filtering, query/document space identity, corpus coverage, and the calibrated profile before changing a model.

### **Context Window Overflow**
**Symptoms**: Responses become generic, model ignores specific retrieved context, inconsistent answers
**Detection Rule**: A pre-defined held-out probe shows that additional retrieved
context lowers grounded-task quality or raises a measurable irrelevance/error
rate. Record the actual probe and operating envelope; “generality score” is not
a defined universal metric.
**Root Cause**: Too many irrelevant chunks diluting relevant information
**Fix**: Choose context under a measured token/quality budget; thresholds are corpus-specific estimates, never portable constants.

### **Tool Hallucination Loop**
**Symptoms**: Agent makes up API calls, references non-existent functions, infinite retry cycles
**Detection Rule**: A versioned tool-contract harness records unsupported calls,
schema failures, or non-progressing recovery loops above the task's pre-registered
operating envelope.
**Root Cause**: Model trained on different tool schemas than implementation
**Fix**: Add tool validation layer and explicit error handling in agent system prompt

### **Embedding Drift Degradation**
**Symptoms**: Gradual decline in retrieval quality over time, seasonal performance drops
**Detection Rule**: A versioned holdout shows a decision-relevant regression relative to its recorded baseline and uncertainty interval.
**Root Cause**: Domain language evolves but embedding model remains static
**Fix**: Verify profile identity and re-embed or recalibrate only with a receipted migration.

### **Response Latency Creep**
**Symptoms**: P95 latency increases gradually, user complaints about slow responses
**Detection Rule**: A monitored latency distribution crosses the corpus policy's
calibrated SLO with enough observations to distinguish sustained regression from
ordinary variation.
**Root Cause**: Vector index degradation, context size inflation, or model endpoint saturation
**Fix**: Implement index optimization schedule, context pruning, and multi-model load balancing

## Worked Examples

### Hypothetical example: customer-support retrieval system

The values and components below are placeholders for showing the evaluation
sequence. They are not measured results, vendor recommendations, or profile
defaults.

**Initial requirements**: “Answer authorized support questions from a versioned
product corpus within a stated latency/cost envelope.”

**Step 1: Architecture decision**
- Declare corpus authority, retention, and redaction policy before indexing.
- Assign lexical, dense, and reranking roles with immutable compatible profile IDs.
- Select a hybrid candidate set and reranker only after comparing alternatives
  on a development split; freeze a held-out split for promotion.

**Step 2: Implementation walkthrough**

```typescript
const authorized = await authorityFilter(query, corpusPolicy);
const lexical = await lexicalRetriever.search(authorized);
const dense = await denseRetriever.search(authorized, { spaceId });
const candidates = reciprocalRankFuse(lexical, dense);
const reranked = await reranker.rank(authorized, candidates);
const selected = selectByCalibratedPolicy(reranked, evaluationProfile);

if (selected.needsEscalation) {
  return escalateWithEvidenceGap(selected);
}
```

**Step 3: Performance decision**
- Measure each role separately on the frozen corpus/harness: retrieval outcome,
  grounded answer outcome, latency, and cost.
- Change one profile or candidate-bound parameter at a time; compare paired
  outcomes with uncertainty against the declared operating envelope.
- Promote only when the evidence supports the stated user outcome. Otherwise
  retain the current profile or narrow the approved task envelope.

**Step 4: Evidence-gap handling**
- Detect questions whose authorized corpus lacks the required evidence.
- Escalate with the missing evidence and query context; do not invent an answer.

**Result**: a receipted corpus-policy/profile/harness decision, with an explicit
escalation path for evidence gaps. No performance result is implied by this example.

## Anti-Patterns

### Shipping RAG on Vibes

**Novice**: Ships retrieval after a handful of manual "looks good to me" spot-checks; no held-out
evaluation set, no CI gate, no measured recall/precision.
**Expert**: Stands up a repeatable eval harness (unit + retrieval + end-to-end + adversarial) before
shipping, and re-runs it on every prompt/retrieval/model change.
**Detection**: `ai_system_audit.mjs` returns `no-eval-harness` (critical) when `evalHarness.exists` is
false, and `eval-harness-thin` (medium) when it exists but lacks end-to-end/adversarial coverage.

### Grounding as a Prompt Suggestion, Not a Checked Property

**Novice**: Asks the model nicely to "cite your sources" and trusts that it will, with no retrieval
measurement and no validation that citations actually match retrieved content.
**Expert**: Measures retrieval@k recall/precision against a held-out set (never eyeballs "does this
answer look right"), requires citations for every factual claim, and validates output against
retrieved sources programmatically instead of trusting the prompt.
**Detection**: `ai_system_audit.mjs` returns `retrieval-never-measured` (critical) when
`retrieval.used` is true but recall/precision were never measured (the Semantic Mismatch Cascade
failure mode above), `no-grounding-requirement` (critical) when the system makes factual claims but
`grounding.citationsRequired` is false, and `grounding-not-enforced` (medium) when citations are
required but `sourceAttributionEnforced` is false.

### No Fallback, No Defense, No Ceiling

**Novice**: Ships an agent that always answers confidently (no low-confidence fallback), accepts raw
user text and retrieved documents into the same context with no isolation (no injection defense), and
has no per-request cost cap — a single adversarial or pathological request can run away.
**Expert**: Adds a confidence threshold with an explicit fallback action, isolates untrusted content
(user input, retrieved docs, tool output) from the system prompt, and enforces a per-request cost
ceiling as part of the design — not as an afterthought infra control.
**Detection**: `ai_system_audit.mjs` returns `no-low-confidence-fallback` (critical) when
`lowConfidenceFallback.exists` is false, `no-injection-defense` (critical) when the system accepts
untrusted input and `promptInjectionDefense.exists` is false, `no-cost-ceiling` (high) when
`costCeiling.enforced` is false, and `tool-hallucination-risk` (critical) — the Tool Hallucination
Loop failure mode above — when tools are used with no `toolUse.validationLayer`.

## Quality Gates

- [ ] Corpus policy filters authority before ranking and records selected profile/spaceId.
- [ ] Held-out retrieval, grounding, latency, and cost outcomes have task-specific acceptance criteria and uncertainty.
- [ ] Hybrid and reranked candidates are compared under the same corpus, model, and budget.
- [ ] Thresholds are calibrated on a development split, then frozen for a held-out check.
- [ ] Illustrative examples are not reported as measured production outcomes.
- [ ] Untrusted retrieved content stays data, with an explicit fallback for insufficient evidence.

See `references/corpus-profile-evaluation.md` for the required evaluation receipt.

## Machine-Checkable Audit

The build-quality subset of the Quality Gates above — the parts a JSON plan can state before a line
of code ships — is machine-checkable. `scripts/ai_system_audit.mjs` exports `auditAiSystem(plan)`,
which scores a JSON AI-system plan and flags the failure modes most likely to ship a broken AI
feature: no eval harness, unmeasured retrieval, unrequired/unenforced grounding, missing hallucination
guardrails, no low-confidence fallback, missing streaming UX on an interactive system, no prompt
injection defense on untrusted input, no enforced per-request cost ceiling, and unvalidated tool calls.

This is deliberately scoped to the AI system's own build quality — it does NOT re-check
`agentic-infrastructure-2026`'s `infra_readiness.mjs` gates (framework selection, MCP context
overhead, observability wiring, organizational/adoption readiness). A plan can pass this audit and
still fail that one (e.g. a well-built RAG pipeline with no chosen framework or kill switch), and vice
versa.

- `schemas/ai-system-plan.schema.json` — draft-07 shape of the plan the auditor consumes.
- `examples/sample-input.json` — a complete plan that scores `pass: true`.
- `examples/expected-output.md` — a "ships on vibes" plan audited, then the same plan fixed and passing.

```bash
node scripts/ai_system_audit.mjs --input examples/sample-input.json
# => { "pass": true, "score": 100, "findings": [], "recommendations": [...] }
```

## Not-For Boundaries

**Do NOT use this skill for:**

**Agent Infrastructure/Framework Selection** → Use `agentic-infrastructure-2026` instead
- Choosing LangGraph/CrewAI/Semantic Kernel/MCP
- Observability, evaluation-pipeline tooling, cost governance (kill switches, budget alerts, quotas)
- Adoption strategy, ROI measurement, pilot scoping

**Model-Routing Mechanics** → Use `llm-router` instead
- Building the routing layer that selects an approved, evaluated profile per request at runtime
- Cost/latency-tiered dispatch across providers

**Agentic App Shape Decisions** → Use `agentic-app-architecture` instead
- Interaction transparency, execution-substrate/side-effect isolation, overall memory/state shape
  (this skill builds what runs *inside* that shape, not the shape itself)

**Memory Algorithm Internals** → Use `episodic-memory-algorithms` instead
- Vector-index internals (HNSW/IVF/PQ), forgetting curves, memory consolidation mechanics

**Prompt Engineering Tasks** → Use `prompt-engineer` instead
- Optimizing prompt templates and instructions
- A/B testing prompt variations
- Chain-of-thought prompt design

**ML Model Training/Fine-tuning** → Out of scope for this skill; use dedicated model-training/fine-tuning tooling
- Training custom embedding models
- Fine-tuning LLMs on domain data
- Model architecture research

**Data Pipeline Engineering** → Use `data-pipeline-engineer` instead
- ETL processes for training data
- Data validation and cleaning workflows
- Batch processing systems

**Infrastructure/DevOps** → Out of scope for this skill; use your stack's infra/DevOps skill (e.g. `cloudflare-worker-dev`, `devops-automator`)
- Kubernetes deployment strategies
- Database optimization and sharding
- Load balancer configuration

**Analytics and Monitoring Setup** → Use `chatbot-analytics` instead
- Conversation flow analysis
- User behavior tracking
- Performance dashboard creation

**Delegate When:**
- Task requires deep ML training/fine-tuning expertise → dedicated model-training tooling
- Focus is on conversation design → `prompt-engineer`  
- Need infrastructure scaling → your stack's infra/DevOps skill
- Want usage analytics → `chatbot-analytics`
- Need agent infrastructure/framework/observability decisions → `agentic-infrastructure-2026`
- Need model-routing dispatch mechanics → `llm-router`
- Need the app's overall shape decided first → `agentic-app-architecture`
- Building non-AI features → Relevant specialist skill

## References

| File | Load When |
| --- | --- |
| `templates/output-template.md` | Drafting an AI system design and its Roadmap-Item trailer. |
| `schemas/ai-system-plan.schema.json` | Validating an AI-system-plan JSON payload's shape before auditing it. |
| `scripts/ai_system_audit.mjs` | Need deterministic scoring of a plan's build-quality readiness. |
| `examples/sample-input.json` | Need a complete plan that scores `pass: true`. |
| `examples/expected-output.md` | Need to see a "ships on vibes" system audited, then the same system fixed and passing. |
| `agents/openai.yaml` | Need a subagent descriptor for delegated AI-system design/build. |

<!-- BEGIN BUNDLE INDEX (auto: index_references.py) -->

## Skill Bundle Index

*Every file in this skill, and when to open it. Auto-generated; run `scripts/index_references.py --fix`.*

**root**
- [`CHANGELOG.md`](CHANGELOG.md) — AI Engineer — Changelog — - Imported from the global jury_rig skill catalog (`ai-engineer`, SKILL.md-only) into the repo.
- [`README.md`](README.md) — AI Engineer — Build production-ready LLM applications, RAG systems, and intelligent agents: retrieval component selection, model routing strategy, agent-v

**`agents/`**
- [`agents/openai.yaml`](agents/openai.yaml) — openai (data/schema)

**`examples/`**
- [`examples/expected-output.md`](examples/expected-output.md) — Example Output: AI Engineer — Scenario: a team ships a customer-support RAG chatbot after two weeks of manual "looks good to me" spot-checking.
- [`examples/sample-input.json`](examples/sample-input.json) — sample input (data/schema)

**`schemas/`**
- [`schemas/ai-system-plan.schema.json`](schemas/ai-system-plan.schema.json) — ai system plan.schema (data/schema)

**`scripts/`**
- [`scripts/ai_system_audit.mjs`](scripts/ai_system_audit.mjs)

**`templates/`**
- [`templates/output-template.md`](templates/output-template.md) — AI System Design Template — Fill in every section before implementation begins.

<!-- END BUNDLE INDEX -->
