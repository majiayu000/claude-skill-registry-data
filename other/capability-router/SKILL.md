---
name: capability-router
description: Use FIRST quando user faz request não-trivial. Retorna index resumido de plugins, MCP servers, skills e agents EOI-OS por capability category, com guidance "use X when Y". Trigger words/contexts:user pede algo complexo que requer ferramentas (deploy, security audit, design, knowledge graph, memory, swarm, data query, etc); user pergunta "que ferramenta usar pra X"; user faz request ambíguo que pode mapear a múltiplos tools; início de qualquer task que vai usar mais de 1 tool. NÃO usar para chat casual, perguntas simples, ou tasks já obvious (e.g., "lê esse arquivo" → Read direto).
---

# Capability Router — EOI-OS

Index resumido pra Claude rotear pro tool certo SEM varrer 791 skill descriptions.

## PLUGINS (59 ativos) por capability

### Comunicação / Productivity
- **productivity@knowledge-work-plugins**: Slack, Notion, Asana, Linear, Jira, ClickUp, Atlassian, Monday, Gmail, Google Calendar
- **enterprise-search**: Guru, Gmail, Calendar cross-tool search
- **commit-commands**: git commit, push, PR workflow

### Data / Analytics
- **data@knowledge-work-plugins**: Snowflake, Databricks, BigQuery, Hex, Amplitude, Definite
- **posthog@claude-plugins-official**: analytics, feature flags, experiments

### Code Intelligence
- **github**: PRs, issues, repos (HTTP MCP)
- **understand-anything**: knowledge graph + `/understand-*` commands
- **plugin-dev**: plugin development toolkit
- **firecrawl**: web scrape/crawl/search
- **context7**: up-to-date library docs lookup

### Security
- **security-guidance**: auto-review code for vulns (writes hooks)
- **semgrep**: static analysis security
- **sonatype-guide**: supply chain dep security
- **ruflo-security-audit**: security review, dependency scanning, CVE
- **ruflo-aidefence**: PII detection, prompt injection defense

### Testing / QA
- **playwright**: browser automation + E2E
- **pr-review-toolkit**: 6 specialized PR review agents
- **code-review**: PR review with confidence scoring
- **ruflo-testgen**: test gap detection + generation
- **coderabbit**: AI code review

### Observability / Monitoring
- **sentry**: error tracking, debug prod
- **claude-mem@thedotmack**: cross-session memory (3 MCP tools)
- **ruflo-observability**: structured logging + tracing + metrics
- **ruflo-cost-tracker**: token usage + cost per agent

### Multi-agent / Orchestration
- **ruflo-swarm**: agent teams, hierarchical/mesh/adaptive topologies
- **ruflo-autopilot**: autonomous /loop task completion
- **ruflo-intelligence**: self-learning SONA patterns
- **pro-workflow**: 18 hook events + 5 agents + reference guides
- **superpowers**: TDD, debugging, collaboration patterns

### Memory / RAG
- **pinecone**: vector DB (HTTP MCP)
- **ruflo-rag-memory**: HNSW search, AgentDB, semantic retrieval
- **ruflo-agentdb**: AgentDB memory controllers
- **ruflo-ruvector**: self-learning vector DB (HNSW, FlashAttention)
- **claude-mem**: cross-session memory bridge

### Documentation
- **ruflo-docs**: doc generation + drift detection
- **claude-md-management**: CLAUDE.md audit + improvement
- **ruflo-adr**: ADR lifecycle (Architecture Decision Records)
- **skill-creator**: create/improve/measure skills

### Deployment / Infra
- **vercel**: build/deploy web apps + agents (33 hooks)
- **ECC**: harness performance (64 agents + 261 skills + hooks)
- **ruflo-jujutsu**: advanced git workflows + risk scoring
- **ruflo-workflows**: visual workflow automation

### Domain-specific
- **ruflo-neural-trader**: trading models (LSTM/Transformer/N-BEATS) — D2 NOT-RECOMMENDED for DME
- **ruflo-market-data**: market feeds (financial)
- **ruflo-iot-cognitum**: IoT device management
- **ruflo-ruvllm**: local LLM inference

## MCP SERVERS standalone (user scope)

- **codegraph** (`codegraph serve --mcp`) → explore codebase. **47% menos tokens** vs grep+read. Use SEMPRE quando explore/scout codebase grande.
- **cve-mcp** → CVE/EPSS/CISA KEV/Shodan/VirusTotal lookup (27 tools). Use pra security audits + threat intel.
- **claude-skills-mcp** (uvx) → discovery de skills disponíveis
- **mem-hybrid** → memory backend
- **magic** (@21st-dev) → magic component generation
- **n8n-mcp** → n8n workflow integration

## SKILLS por categoria (~791 total)

### EOI-OS first-party (~25 — design DME doctrine)
- **criar-tirinhas** / **criar-tirinhas-care-sa** → planilhas médicas cirurgias
- **pre-deploy-validator** → 23-item checklist antes de prod
- **deploy-check** → quick pre-deploy checks
- **deslop** → remove código com cara de IA
- **graphify** → knowledge graph de codebase
- **mcp-builder** → criar MCP servers
- **notebooklm** → Google NotebookLM API
- **rebuild-skills**, **auto-update**, **verification-before-completion**
- **repo-fit-analyzer** → analisa repos do GitHub vs config EOI-OS

### Design (taste-skill 13 — anti-slop UI)
- **design-taste-frontend** → landing pages, portfolios premium
- **brandkit** → brand-kit boards, logo systems, identity
- **gpt-taste** → editorial typography + GSAP motion
- **minimalist-ui**, **industrial-brutalist-ui**, **high-end-visual-design**
- **imagegen-frontend-mobile/web** → premium screen mockups
- **redesign-existing-projects** → upgrade existing UI
- **stitch-design-taste** → Google Stitch DESIGN.md
- **image-to-code**, **full-output-enforcement**

### Cybersec (mukul975 754 — 26 domínios)
- Cloud Security (60), Threat Hunting (55), Threat Intel (50), Web App (42), Network (40), Malware (39), Forensics (37), SOC Ops (36), IAM (35), + 17 outros
- Trigger words: "audit security", "threat hunt", "CVE", "OWASP", "incident response", "forensics", "pentest", "red team", "compliance"

### Plugin-derived (~309 entries)
- firecrawl 10, sentry 26, posthog 55, pro-workflow 11, superpowers 14
- ECC ~416 (testing, security, backend patterns, languages-specific)
- ruflo 4×4 (core/swarm/rag/security)
- plugin-dev 7, sonatype-guide, semgrep, supabase, etc

## AGENTS customs (8 EOI-OS + 90+ plugin-derived)

### EOI-OS (escolha por intent — per CLAUDE.md routing table)
- **scout** (Sonnet 4.6) → buscar/explorar código
- **deployer** (Sonnet 4.6) → pre-deploy validation
- **implementer** (Opus 4.8) → implementar feature/fix bug
- **reviewer** (Opus 4.8) → review código
- **tester** (Opus 4.8) → testes
- **security-auditor** (Opus 4.8) → audit segurança
- **architect** (Fable 5) → arquitetura, PRD, decisão complexa
- **infra-architect** (Fable 5) → infraestrutura, cloud, networking

### Plugin-derived (top picks)
- **feature-dev:feature-dev** → guided feature development workflow
- **pr-review-toolkit:* (6 agents)** → code-reviewer, silent-failure-hunter, comment-analyzer, pr-test-analyzer, type-design-analyzer, code-simplifier
- **pro-workflow:orchestrator** → wire commands+agents+skills for complex features
- **claude-md-management:claude-md-improver** → audit/improve CLAUDE.md
- **ECC agents (64)** → planning, code-review, security analysis, backend, frontend, testing

## HOW TO USE (routing patterns)

| User intent | Tool/skill recomendado |
|---|---|
| "audita esse repo: <url>" | skill `repo-fit-analyzer` |
| "explora esse codebase" | MCP `codegraph_explore` (NÃO grep+read loops) |
| "checa CVEs do <lib>" | MCP `cve-mcp` tools |
| "deploy" / "manda pra prod" | skill `pre-deploy-validator` ANTES |
| "limpa código com cara de IA" | skill `deslop` |
| "faz UI/landing premium" | skill `design-taste-frontend` ou `gpt-taste` |
| "threat hunting" / "incident response" | cybersec skills (754) categoria threat |
| "swarm de agents" / "paralelizar" | `ruflo-swarm:swarm-init` ou `dispatching-parallel-agents` |
| "memory cross-session" | claude-mem MCP ou `ruflo-rag-memory:memory-bridge` |
| "commit" / "push" / "PR" | plugin `commit-commands:commit-push-pr` |
| "criar plugin/skill" | `plugin-dev:create-plugin` ou `skill-creator:skill-creator` |
| "criar tirinhas (médico)" | skill `criar-tirinhas` / `criar-tirinhas-care-sa` |
| "knowledge graph" | skill `graphify` OU `understand-anything@understand-anything` |

## REGRA OURO

Quando user pede algo:
1. Match contra **HOW TO USE** table primeiro
2. Se não match: scan categorias relevantes desta skill (não as 791 descriptions)
3. Se ainda não match: invoke skill específica que parece mais alinhada
4. NUNCA invoke múltiplos plugins/skills "no caso de" — escolha 1-2 e use bem

Anti-pattern: invocar 5 skills "to be safe" — inflaciona context, custa tokens, confunde response.
