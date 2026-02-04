---
name: agent-certifier
description: >
  Given a human certification or license (e.g. PL-300, SAP B1, Azure AI Engineer),
  create a production-ready agent skill profile and certification ladder, including
  skills.yaml entries, agent YAML, and skills documentation, using the anthropics/skills
  SKILL.md conventions.
---

# Agent Certifier

This skill turns **human certifications** (e.g. PL-300, CPA, SAP B1, Azure AI)
into **machine-certifiable agents** with clear skills, benchmarks, and a signed
competency contract.

Use this skill when the user gives:
- A human cert or license name (e.g. "PL-300: Power BI Data Analyst")
- Optionally one or more reference repos or products (e.g. `microsoft/powerbi-desktop-samples`)
- A target agent name/slug (e.g. `powerbi-bi-architect`)

Your job is to emit a **complete, market-ready bundle**:
- A skills spec (YAML) with levels, benchmarks, and tools
- An agent spec (YAML) wired to those skills
- A human-readable `skills.md` for documentation
- Optional certification JWT schema, compatible with an external CertificationAuthority

---

## When to Use This Skill

Invoke this skill whenever the user wants to:

- Translate a human certification (Azure, SAP, CPA, Azure AI, etc.) into an **agent certification ladder**
- Define **skills + tools + benchmarks** for an agent in a reusable, model-agnostic way
- Produce **ready-to-commit** files for a repo:
  - `skills/<domain>.yaml`
  - `agents/<agent_slug>.yaml`
  - `docs/<agent_slug>-skills.md`

The output should be designed so it can be:
- Used by Claude Skills (this SKILL.md format)
- Loaded by OpenSkills (`anthropics/skills` compatible)
- Reused by other agents (Gemini, OpenAI, etc.) via the same YAML contracts

---

## Input Format

Assume the user will give you (in natural language, not strict JSON):

- Human cert(s) and level(s)
  - e.g. "PL-300 + DP-500 + Power Platform Solution Architect Expert"
- Domain / role
  - e.g. "Power BI / Fabric BI Architect for retail dashboards"
- Reference repos or artifacts (optional but common)
  - e.g. GitHub URLs, product pages, sample `.pbix`, `.twb`, etc.
- Target agent id/slug
  - e.g. `powerbi_bi_architect`

You must **infer missing pieces** safely and document assumptions.

---

## What To Produce

Always produce **three main artifacts** (as copy-paste-ready blocks):

### 1. `skills/<domain>.yaml`

A YAML file that defines:

- `version`, `domain`
- `human_analogs`: list of human certs you are mirroring
- `sources`: reference repos or artifacts (GitHub, sample files)
- `tools`: logical tool contract names (e.g. `pbix_reader`, `dax_analyzer`)
- `skills`:
  - Each with `id`, `level` (fundamentals/role_based/specialty/business/expert etc.)
  - `human_analog`, `description`
  - `required_tools`, optional `prerequisites`
  - `benchmarks`: each with `id`, `description`, `repo_source`, and `success_criteria` list

Keep tool names **abstract** so they can be mapped to OpenAI/Gemini/Claude tool schemas later.

### 2. `agents/<agent_slug>.yaml`

An agent spec that:

- References the domain and skill IDs from the skills YAML
- Lists required tools by id
- Defines `human_cert_analogs` (strings)
- Defines `certification_policy`:
  - Levels (`fundamentals`, `associate`, `expert`, etc.)
  - `required_skills` for each level
  - `min_benchmarks_passed` per level
  - `issuance` block:
    - `title_template`
    - `validity_days`
    - `conditions` (bullets)

Include a `benchmarks_runtime` block describing:

- `repo_sources` (e.g. `microsoft/powerbi-desktop-samples`)
- `execution.runner` (e.g. `ci.pipeline.powerbi`)
- `schedule` (e.g. `nightly`)

### 3. `docs/<agent_slug>-skills.md`

A markdown doc for humans that:

- Explains which human certs this agent emulates
- Lists each skill level with:
  - Human analog
  - Capabilities (bullets)
  - Benchmark(s) and pass criteria
- Explains the **certification policy**:
  - What "Fundamentals / Associate / Expert Certified" means
  - How the external `CertificationAuthority` JWT is issued & used

Structure this as:

1. Overview
2. Human Certification Analogs
3. Tools Required
4. Skill Levels & Benchmarks
5. Certification Policy

---

## Instructions

When this skill is active:

1. **Parse the user brief.**
   - Identify the **domain** (e.g. Power BI, SAP B1, Azure AI, Odoo).
   - Extract all human certification names and their levels.
   - Note any reference repos / products / sample files.

2. **Define the skills ladder.**
   - Map human certs into 3–5 levels:
     - fundamentals → role_based → specialty → business → expert
   - For each level:
     - Write a concise description of capabilities.
     - Choose the tools needed (abstract names).
     - Design 1–3 concrete benchmarks that can be evaluated automatically.
   - Benchmarks must have **clear, measurable pass criteria** (e.g. KPI parity within 1%, build succeeds, tests green, etc.).

3. **Design tool contracts.**
   - Keep tools **model-agnostic**:
     - Do NOT hard-code OpenAI / Gemini / Claude APIs.
     - Use logical names (e.g. `ocr_gateway`, `sap_b1_api_client`, `pbix_reader`).
   - Focus on what the tool does, not how it's implemented.

4. **Generate the three artifacts.**
   - Emit them in this order, each in its own fenced code block:
     1. `skills/<domain>.yaml`
     2. `agents/<agent_slug>.yaml`
     3. `docs/<agent_slug>-skills.md`
   - Make them **ready to commit** (no placeholders like `TODO` or `...`).

5. **State assumptions & risks briefly.**
   - At the end, add a short "Assumptions & Risks" section (3–6 bullets) outside the code blocks:
     - List any big assumptions (e.g. data source, repos, tools).
     - Flag anything that absolutely needs human review (compliance, PII, prod access).

---

## Examples

### Example 1 – Power BI Architect

> "Create an agent that is equivalent to PL-300 + DP-500 + Power Platform Solution Architect, using `microsoft/powerbi-desktop-samples` as the benchmark repo. Agent slug: `powerbi_bi_architect`."

You should:
- Define `domain: "cloud_ai_platforms.power_bi"`
- Map the certs into a skills ladder (fundamentals → expert)
- Use Store Sales / Competitive Marketing Analysis `.pbix` as benchmarks
- Emit YAML + docs as specified above

### Example 2 – Azure AI Engineer

> "Build an agent certified at the same level as Azure AI Engineer Associate, focused on RAG systems for finance dashboards."

You should:
- Create a `cloud_ai_platforms.azure_ai_rag` skills domain
- Define tools like `embedding_indexer`, `rag_query_runner`, `azure_openai_client`
- Add benchmarks: end-to-end RAG flow, latency, accuracy, hallucination checks
- Emit all three artifacts.

### Example 3 – Retail Analytics (Scout)

> "Certify an agent at the same level as a Retail Analytics Data Engineer for sari-sari / FMCG dashboards, using the Scout dashboard as the benchmark."

You should:
- Create `retail_analytics.scout` domain
- Define tools: `supabase_query_runner`, `kpi_validator`, `chart_renderer`
- Add benchmarks: schema validation, KPI accuracy, dashboard render time
- Emit YAML + docs

---

## Guidelines

- Prefer **clear, testable benchmarks** over vague descriptions.
- Keep everything **implementation-agnostic**:
  - No hard-wiring to a single model provider.
  - Assume tools can be backed by Claude, OpenAI, Gemini, or local models.
- Favor **production-readiness**:
  - Think like a vendor shipping a marketplace agent, not a demo.
  - Include governance/security considerations where relevant (RLS, PII, secrets).
- Never include real secrets or API keys in outputs.

---

## Related Skills

- `engine-spec-writer` – Creates engine.yaml specs for IPAI Platform
- `supabase-schema-designer` – Designs Supabase schemas with RLS
- `dashboard-builder` – Builds Next.js dashboards from specs
