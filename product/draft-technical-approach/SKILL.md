---
name: draft-technical-approach
description: Create an architecture.yaml artifact with technology selections, NFRs, platforms, integrations, and agentic PCAM design from a features specification
user-invocable: false
model: sonnet
allowed-tools: Read, Write
---

# draft-technical-approach

Model-invocable skill for creating architecture specifications as structured YAML.

## Purpose

Transform a features specification (behaviors, invariants, feature scope) into a concrete `architecture.yaml` artifact that names specific technologies for every architectural component and makes all technology selection decisions. The artifact must be specific enough that an implementer can begin coding without making technology selection decisions.

You DO create the architecture.yaml artifact. You do NOT validate it or decide what happens next.

## Output Schema

The output MUST conform to `schemas/architecture.yaml` in this skill's directory. Read the schema before producing output. Every field defined in the schema must be present in the output YAML. The schema is the contract — if it's in the schema, it's in the output.

## Input

Receive from agent:
- `features_yaml_path` — (required) Path to features.yaml
- `intent` — (optional) Product intent string for additional context
- `vision_path` — (optional) Path to a locked vision document for enrichment
- `output_base` — (required) Base path for output, e.g., `.garura/product/architecture/`
- `profiles_ref` — (optional) Path to product.yaml containing profiles section. When provided, NFR profile levels drive the nfrs section, and profile values inform technology selection reasoning via LTM architecture knowledge "When to Choose" matching.
- `product_yaml_path` — (optional) Path to product.yaml for profile and context extraction
- `roadmap_yaml_path` — (optional) Path to roadmap.yaml for epic/feature context
- `ltm_architecture_path` — (optional) Path to LTM architecture knowledge directory (default: `~/.garura/core/memory/knowledge/arch/`)

## Process

1. **Read features specification:** Load the `features_yaml_path` document. Extract: product identity, architectural invariants, feature list, behaviors, blast_radius entries, and scope boundaries.

2. **Read vision and profiles (if provided):** If `vision_path` or `product_yaml_path` is provided, load and extract strategic goals, target users, value proposition, and profiles for architectural context. If `profiles_ref` is provided, extract all three profile axes (PP, NFR, QP) — these are primary inputs for technology selection and NFR derivation.

2b. **Read LTM architecture knowledge (if provided):** If `ltm_architecture_path` is provided, read the `_index.md` and relevant architecture files. Match "When to Choose" and "When to Avoid" prose against profile values. This informs pattern, stack, platform, and data store selection. Load files whose search patterns match the product's domain and profile characteristics.

3. **Check for existing artifact:** Read `{output_base}/architecture.yaml`. If LOCKED, return structured failure: "architecture.yaml is LOCKED -- drop to DRAFT first." If DRAFT exists, overwrite (agent re-triggered DRAFT).

4. **Compose architecture.yaml:** Build the artifact conforming to the architecture.yaml schema. Every architectural component MUST map to a named technology -- specific databases, frameworks, SDKs, hosting platforms, libraries. No vague references like "a relational database" or "a message queue." Every technology choice MUST include rationale.

   **Top-level fields:**
   - `slug` — from features.yaml slug
   - `status` — always `DRAFT`
   - `created_at`, `updated_at` — current ISO-8601 timestamp
   - `features_ref` — path to features.yaml

   **`principles` section:** Implementation principles guiding all technology and design decisions. Derived from the features.yaml architectural invariants. Each principle gets a stable ID (TP1, TP2, ...) with principle statement and rationale.

   **`architecture` section:**
   - `topology` — ASCII diagram or structured description of the system topology showing deployment units and communication patterns
   - `deployment_units` — list of named units with responsibility and communication protocol/pattern

   **`nfrs` section (NON-FUNCTIONAL REQUIREMENTS):** Explicit, prioritized NFR statements for:
   - `performance` — response time targets, throughput thresholds
   - `scalability` — concurrency, volume expectations
   - `security` — encryption, auth, data protection requirements
   - `availability` — uptime SLA, recovery objectives
   - `compliance` — regulatory or data residency requirements
   Each requirement gets a `requirement` string and `priority` (must | should | nice-to-have).

   **When `profiles_ref` is provided:** NFR requirements MUST be derived from the NFR Profile levels in product.yaml. Map each NFR dimension level to concrete, measurable requirements:
   - NFR-1 (Risk) level 3 → "Monitoring and alerting for all customer-facing endpoints"
   - NFR-2 (Security) level 3 → "MFA, RBAC, encryption in transit, API key management"
   - NFR-3 (Performance) level 4 → "Sub-100ms API responses for critical paths"
   - NFR-4 (Availability) level 3 → "99.9% uptime, automated failover, blue-green deployments"
   - NFR-5 (Compliance) level 3 → "GDPR compliance, privacy by design, consent management"
   - NFR-6 (Scalability) level 3 → "Horizontal scaling, load balancing, designed for 10x growth"
   - NFR-7 (Data Sensitivity) level 3 → "PII encryption at rest, access logging"
   The rationale for each requirement must reference the NFR dimension and level it was derived from.

   **`stack` section:** Concrete technology selections -- specific named products. For each entry: component, technology (e.g., "React 19", "Python 3.12", "Claude Sonnet"), purpose, rationale. Organize by deployment unit and infrastructure. Include deliberate exclusions with rationale where relevant.

   **`platforms` section (NEW):** Category-level platform decisions. For each platform: category (cms | commerce | payments | agentic | auth | messaging | analytics | search), platform (specific named product), purpose, rationale, features_served (list of feature IDs from features.yaml).

   **`integrations` section (NEW):** Third-party APIs, webhooks, external services. For each integration: name, type (api | webhook | sdk | file-exchange | event-stream), provider, purpose, direction (inbound | outbound | bidirectional), auth_method, features_served.

   **`technical_risks` section:** Risks that could affect implementation. Each risk: description, affected_features (list of feature IDs), severity (low | medium | high), mitigation approach.

   **`deployment` section:** For each service/unit: service name, platform (hosting), purpose.

   **`observability` section:** tracing (tool + what gets traced), metrics (list of named metric targets), logging (approach and tool).

   **`agentic` section (PCAM model -- include only if the product has agentic/AI components):**
   - `perception` — signals (inputs): signal name, source, format
   - `cognition` — agents (what thinks): agent name, role, autonomy (full | supervised | gated), model (specific LLM)
   - `action` — tools (what agents can do): tool name, purpose, available_to list
   - `memory` — data layer: approach (rag | graph | hybrid | vector | relational), stm, ltm, embeddings
   If the product has no agentic components, omit this section entirely.

5. **Validate completeness:** Before writing, verify that every feature in features.yaml has corresponding architecture coverage -- deployment unit, stack entry, or platform assignment. If any feature lacks architecture coverage, add the missing component with rationale.

6. **Write artifact:** Write `architecture.yaml` at `{output_base}/architecture.yaml` with `status: DRAFT`.

7. **Return output.**

## Output

```yaml
architecture_yaml:
  path: "{full path to architecture.yaml}"
  architecture_yaml_path: "{full path to architecture.yaml}"
  sections:
    - principles
    - architecture
    - nfrs
    - stack
    - platforms
    - integrations
    - technical_risks
    - deployment
    - observability
    - agentic
  has_agentic: true | false
  status: "DRAFT"
```

**IMPORTANT**: This skill produces an artifact and returns metadata. The calling agent receives this output and decides what to do next. Do NOT instruct the agent to return or stop.

## Constraints

- NEVER use vague technology references -- every component must name a specific product, library, framework, or platform
- NEVER overwrite a LOCKED architecture.yaml -- return structured failure
- NEVER invent product behaviors -- derive architecture from features.yaml behaviors and invariants
- NEVER confuse implementation machinery for the product architecture -- the architecture serves the product spec, not the other way around
- ALWAYS set `status: DRAFT` in the written artifact
- ALWAYS include rationale for every technology selection
- ALWAYS include the nfrs section with at least performance and security entries
- ALWAYS include platforms and integrations sections (may be empty lists for greenfield with no external dependencies)
- ALWAYS ensure the artifact is concrete enough for a code-builder agent to implement from without making technology selection decisions
- ALWAYS include features_served references in platforms and integrations entries so the reader knows which features depend on each external system
- WHEN profiles_ref is provided, ALWAYS derive NFR requirements from NFR Profile levels with traceable rationale
- WHEN ltm_architecture_path is provided, ALWAYS read and reference LTM architecture knowledge in technology selection reasoning
- ALWAYS include profiles_ref in the output artifact when profiles were used as input
- Audience is architects and implementers -- write with precision, not marketing language

## Version

| Field | Value |
|-------|-------|
| Version | 2.0.0 |
| Category | analysis |
