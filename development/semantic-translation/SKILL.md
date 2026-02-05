---
name: Semantic Translation
description: This skill should be used when the user uses ambiguous terminology like "make it talk", "we need an api", "make it portable", "check for gaps", asks meta-questions like "am I making sense?", "does this make sense?", mentions being a "non-technical user", uses vague action verbs ("make it work", "do the thing"), mixes domain languages, uses invented terms, or when detecting semantic drift between human natural language and technical precision. Provides semantic translation, disambiguation, and domain knowledge mapping across Autogen, Langroid, MCP (Model Context Protocol), UTCP (Universal Tool Calling Protocol), FastAPI, Git/Gitflow, SRE (Site Reliability Engineering), and Memory Graphs domains. Bridges the gap between user intent and technical specificity through ontological translation.
version: 1.0.0
---

# Semantic Translation & Ontological Mapping

## Purpose

Prevent miscommunication, assumptions, and hallucinations by translating ambiguous user terminology into precise technical concepts across multiple domains. Act as a semantic bridge between human natural language and technical specificity, mapping concepts across Autogen, Langroid, MCP, UTCP, FastAPI, Git/Gitflow, SRE, and Memory Graphs ecosystems.

## Supported Domains

This skill provides semantic translation and disambiguation across 8 technical domains:

1. **Autogen** - Multi-agent orchestration (ConversableAgent, AssistantAgent, UserProxyAgent, GroupChat)
2. **Langroid** - Agent framework (ChatAgent, ToolAgent, Task orchestration)
3. **MCP (Model Context Protocol)** - Server types (SSE, stdio, HTTP, WebSocket), tools, resources, prompts, sampling
4. **UTCP (Universal Tool Calling Protocol)** - Framework-agnostic tool schemas, adapters, universal tool definitions
5. **FastAPI** - Python web framework (path operations, dependency injection with Depends(), Pydantic models, APIRouter)
6. **Git/Gitflow** - Version control workflows (feature/release/hotfix branches, merge strategies, collaboration patterns)
7. **SRE (Site Reliability Engineering)** - Observability pillars (logs/metrics/traces), SLO/SLI/SLA, incident management
8. **Memory Graphs** - Knowledge graph structures (entities, relationships, embeddings, episodic/semantic/procedural memory)

## The Core Problem

Users frequently encounter the "abyss" between natural language intent and technical precision:

- **Vague terminology**: "make it talk", "we need an api", "make it work"
- **Unclear scope**: "check for gaps", "make it portable"
- **Meta-questions**: "am I making sense?", "does this make sense?"
- **Domain confusion**: Mixing business and technical terminology
- **Invented terms**: User-created words not in domain vocabulary

Without intervention, these ambiguities lead to:
- AI assumptions and hallucinations
- Misaligned implementations
- Wasted development time
- Project failures from misunderstood requirements

## When to Use This Skill

Trigger semantic validation when detecting:

1. **Ambiguous Action Verbs**
   - "make it [X]" → Multiple technical interpretations possible
   - "do the thing" → No clear referent
   - "fix it" → Unclear what or how

2. **Meta-Questions (User Seeking Validation)**
   - "am I making sense?" → User uncertain about their explanation
   - "does this make sense?" → User seeking confirmation
   - "is this right?" → User wants validation
   - "non-technical user" → User self-identifies as potentially ambiguous

3. **Domain-Crossing Language**
   - Mixing business and technical terms
   - Unclear which framework/library intended
   - Generic terms with multiple technical meanings

4. **Unclear References**
   - "that", "the previous thing", "like before"
   - References without clear antecedents

5. **Scope Ambiguity**
   - "portable" → Docker? Cross-platform? Vendoring? Executable?
   - "api" → HTTP server? API client? API design? Internal interface?
   - "gaps" → Code coverage? Documentation? Features? Security?

## Core Workflow

### Step 1: Detect Ambiguity

Analyze the user's message for ambiguity signals. Use pattern matching from `scripts/detect-ambiguity.py` or manual analysis.

**High-confidence triggers (always validate):**
- Explicit meta-questions: "am I making sense?"
- Vague action verbs with unclear objects: "make it talk"
- Domain confusion: mixing incompatible terminology
- User self-identification: "I'm a non-technical user"

**Moderate-confidence triggers (validate if >80% confidence):**
- Generic technical terms: "api", "agent", "portable"
- Unclear scope: "check for gaps", "add validation"
- Invented terminology: words not in domain vocabulary

### Step 2: Query Knowledge Sources (In Order)

Query knowledge sources in this specific order for efficiency:

**1. Static Domain Knowledge (First - Fastest)**
- Query `knowledge/ambiguous-terms.json` for known ambiguous phrases
- Check `knowledge/technical-mappings.json` for domain-specific translations
- Review `knowledge/ontology-graph.json` for conceptual relationships

**2. External Documentation (Second - Authoritative)**
- Query official documentation (Autogen, Langroid, etc.) via available tools
- Use WebFetch, context7, or deepwiki MCP for current API references
- Validate against authoritative sources when static knowledge insufficient

**3. Codebase Validation (Third - Context-Specific)**
- Use LSP to query symbol definitions in user's project
- Use Grep to search for actual usage patterns
- Identify project-specific terminology and conventions

### Step 3: Translate Ambiguous → Precise

Map ambiguous terminology to precise technical concepts using domain knowledge.

**Translation process:**
1. Identify all possible technical interpretations
2. Rank by confidence score (from knowledge files)
3. Consider user's context (recent conversation, project domain)
4. Present options if multiple interpretations viable

**Example translation:**
```
Ambiguous: "make it talk"
Domain: Autogen
Possible translations:
- ConversableAgent.send() (confidence: 0.8, context: single message)
- register ConversableAgent (confidence: 0.7, context: enable conversation)
- GroupChat setup (confidence: 0.5, context: multi-agent conversation)
```

### Step 4: Engage Conversational Clarification

**Never assume.** Always verify understanding with the user.

Present options conversationally:
```
I notice "[ambiguous term]" could mean different things:

1. [Precise interpretation 1] - [Brief context]
2. [Precise interpretation 2] - [Brief context]
3. [Precise interpretation 3] - [Brief context]

[Ask clarifying question based on context]
```

**Tone guidelines:**
- Conversational, not clinical
- Helpful, not pedantic
- Transparent about uncertainty
- Frame as collaboration, not correction

**Wait for confirmation** before proceeding with implementation.

## Decision Trees

### Primary Decision Tree

```
User message received
├── Contains meta-question? ("am I making sense?")
│   ├── Yes → HIGH confidence, validate immediately
│   └── No → Continue analysis
├── Contains ambiguous action verb? ("make it talk")
│   ├── Yes → Check domain context
│   │   ├── Clear domain → Query knowledge, translate
│   │   └── Unclear domain → Ask which framework/library
│   └── No → Continue analysis
├── Contains vague scope? ("check for gaps", "make it portable")
│   ├── Yes → Query knowledge for common interpretations
│   │   ├── Multiple viable → Present options
│   │   └── One clear match → Confirm with user
│   └── No → Continue analysis
├── Contains domain-crossing language?
│   ├── Yes → Identify conflicting domains, ask clarification
│   └── No → Proceed normally (low ambiguity)
```

### Clarification Decision Tree

```
Ambiguity detected
├── Confidence score > 80%?
│   ├── Yes → Trigger validation
│   └── No → Monitor, don't interrupt
├── Query knowledge sources (static → external → codebase)
├── Translation mappings found?
│   ├── Yes, single mapping → Confirm with user
│   ├── Yes, multiple mappings → Present options
│   └── No mappings found → Ask open-ended clarification
└── User confirms → Proceed with precise terminology
```

## Domain Quick Reference

Key ambiguous terms across all 8 supported domains with precise translations:

### Autogen Domain

**"make it talk"** → ConversableAgent.send() (single message) vs initiate_chat() (conversation) vs GroupChat setup (multi-agent)
**"agent"** → ConversableAgent (base) vs AssistantAgent (LLM-powered) vs UserProxyAgent (human proxy)

### Langroid Domain

**"agent"** → ChatAgent (conversation) vs ToolAgent (function-calling)
**"task"** → Langroid Task object (orchestration) vs general task concept

### MCP Domain

**"mcp server"** → SSE server (web-based) vs stdio server (process-based) vs HTTP server vs WebSocket server
**"resource"** → MCP resource (data/content exposed by server) vs system resource (CPU/memory)
**"prompt"** → MCP prompt template (structured prompts) vs LLM prompt (text input)

### UTCP Domain

**"tool calling"** → UTCP universal calling (framework-agnostic) vs framework-specific (OpenAI tools, Anthropic tools)
**"tool schema"** → UTCP universal schema vs framework-specific schema

### FastAPI Domain

**"dependency"** → FastAPI Depends() (dependency injection) vs pip dependency (package) vs architectural dependency (service)
**"endpoint"** → Path operation decorator (@app.get) vs external API endpoint
**"model"** → Pydantic model (validation) vs database model (ORM) vs ML model

### Git/Gitflow Domain

**"merge"** → Merge commit (preserves history) vs squash merge (single commit) vs rebase (linear history)
**"branch"** → Gitflow branch type (feature/release/hotfix/develop/main) vs general branch name

### SRE Domain

**"observability"** → Logs (events) vs metrics (measurements) vs traces (request paths) - three pillars
**"sli"** → Availability SLI (uptime %) vs latency SLI (response time) vs error rate SLI (failure %)
**"incident"** → SEV-1 incident (critical outage) vs alert (automated notification) vs degradation (partial failure)

### Memory Graphs Domain

**"memory"** → Knowledge graph (structured entities/relationships) vs vector memory (embeddings) vs episodic memory (temporal context) vs system RAM
**"retrieval"** → Semantic search (embedding similarity) vs graph traversal (relationship following) vs hybrid approach

### Meta-Questions (Cross-Domain)

**"am I making sense?"** → Trigger explicit semantic validation across all domains
- Summarize recent conversation
- Identify detected ambiguities
- Ask domain-specific clarifying questions
- Confirm shared understanding with precise terminology

## Domain-Specific Validation

### Autogen Domain

**Key concepts to validate:**
- Agent types: ConversableAgent, AssistantAgent, UserProxyAgent
- Multi-agent: GroupChat, GroupChatManager
- Communication: send(), register_reply(), initiate_chat()
- Tools: register_for_execution(), register_for_llm()

**Common ambiguities:**
- "agent" → Which type? (ConversableAgent vs AssistantAgent vs UserProxyAgent)
- "group chat" → GroupChat object vs general multi-agent conversation
- "tools" → Function calling vs external tool integration

### Langroid Domain

**Key concepts to validate:**
- Agent types: ChatAgent, ToolAgent
- Tasks: Task orchestration and delegation
- Tools: ToolMessage, tool decorators
- Multi-agent: Agent collaboration patterns

**Common ambiguities:**
- "agent" → ChatAgent vs ToolAgent
- "task" → Langroid Task object vs general task concept
- "tools" → Langroid tool system vs general utilities

### MCP Domain

**Key concepts to validate:**
- Server types: SSE (Server-Sent Events), stdio, HTTP, WebSocket
- Components: tools, resources, prompts, sampling
- Integration: local server, remote server, managed server

**Common ambiguities:**
- "mcp server" → Which type? (SSE vs stdio vs HTTP vs WebSocket)
- "resource" → MCP resource (data/content) vs system resource
- "prompt" → MCP prompt template vs LLM prompt
- "tool" → MCP tool definition vs general function

### UTCP Domain

**Key concepts to validate:**
- Universal tool schemas: Framework-agnostic tool definitions
- Adapters: UTCP framework adapters for different AI frameworks
- Tool calling patterns: Universal invocation vs framework-specific

**Common ambiguities:**
- "tool calling" → UTCP universal calling vs framework-specific calling (OpenAI tools, Anthropic tools)
- "tool schema" → UTCP universal schema vs framework-specific schema
- "adapter" → UTCP framework adapter vs general adapter pattern
- "invocation" → UTCP tool invocation vs direct function call

### FastAPI Domain

**Key concepts to validate:**
- Path operations: Endpoint decorators (@app.get, @app.post)
- Dependency injection: Depends() mechanism
- Pydantic models: Request/response validation
- APIRouter: Endpoint organization and grouping

**Common ambiguities:**
- "dependency" → FastAPI Depends() vs pip package dependency vs architectural dependency
- "endpoint" → Path operation decorator vs external API endpoint
- "model" → Pydantic model vs database model vs ML model
- "route" → Path operation vs APIRouter vs URL routing
- "validation" → Pydantic automatic validation vs business logic validation

### Git/Gitflow Domain

**Key concepts to validate:**
- Branch types: feature/, release/, hotfix/, develop, main
- Merge strategies: merge commit, squash merge, rebase
- Workflows: Gitflow vs GitHub flow vs GitLab flow
- Operations: commit, push, pull, merge, rebase

**Common ambiguities:**
- "merge" → Merge commit vs squash merge vs rebase
- "branch" → Gitflow branch type (feature/release/hotfix) vs general branch
- "rebase" → Interactive rebase vs standard rebase vs rebase merge
- "commit" → Commit operation vs commit message vs specific commit SHA
- "workflow" → Gitflow workflow vs GitHub flow vs custom workflow

### SRE Domain

**Key concepts to validate:**
- Observability pillars: logs, metrics, traces
- SLI/SLO/SLA: Service Level Indicator/Objective/Agreement
- Incident management: SEV levels, on-call, postmortems
- Reliability patterns: error budgets, canary deployments, circuit breakers

**Common ambiguities:**
- "observability" → Which pillar? (logs vs metrics vs traces)
- "sli" → Which metric? (availability vs latency vs throughput vs error rate)
- "incident" → SEV-1 incident vs alert vs outage vs degradation
- "monitoring" → Monitoring (passive data collection) vs observability (active understanding)
- "on-call" → On-call rotation vs on-call engineer vs escalation policy

### Memory Graphs Domain

**Key concepts to validate:**
- Graph types: knowledge graph, memory graph, dependency graph
- Memory types: episodic, semantic, procedural
- Components: entities (nodes), relationships (edges), embeddings
- Operations: retrieval (semantic search, graph traversal), storage

**Common ambiguities:**
- "memory" → Knowledge graph vs vector memory vs episodic memory vs system RAM
- "graph" → Knowledge graph vs visualization graph vs dependency graph
- "embedding" → Vector embedding for semantic search vs embedding layer in neural networks
- "retrieval" → Semantic search via embeddings vs graph traversal vs hybrid
- "node" → Memory node (entity) vs graph node vs system node

### Generic/Framework-Agnostic

**When domain unclear:**
1. Don't assume framework
2. Ask explicitly: "Which framework/library are you using?"
3. Once identified, load domain-specific knowledge
4. Translate with domain context

## Confidence Scoring

Use confidence scores to determine intervention:

**High confidence (>80%):** Always validate
- Explicit meta-questions
- Known highly ambiguous terms (from knowledge files)
- Domain confusion detected
- User self-identifies ambiguity

**Medium confidence (50-80%):** Validate if multiple interpretations
- Generic technical terms with context clues
- Unclear scope with partial context
- Vague references with some antecedents

**Low confidence (<50%):** Monitor but don't interrupt
- Technical terms with clear context
- Conventional usage patterns
- Recent clarification provided

## Integration with Knowledge Files

### ambiguous-terms.json

Contains user phrases mapped to ambiguity scores and contexts.

**Query pattern:**
```python
term = extract_key_phrase(user_message)
entry = load_json("knowledge/ambiguous-terms.json").get(term)
if entry and entry["ambiguity_score"] > 0.8:
    trigger_validation(term, entry["contexts"])
```

### technical-mappings.json

Contains precise technical translations organized by domain.

**Query pattern:**
```python
mappings = load_json("knowledge/technical-mappings.json")
domain_mappings = mappings.get(domain, {})
translations = domain_mappings.get(ambiguous_term, [])
present_options(translations)
```

### ontology-graph.json

Contains conceptual relationships between terms across domains.

**Query pattern:**
```python
graph = load_json("knowledge/ontology-graph.json")
related_concepts = graph.get(concept, {}).get("related", [])
cross_domain = graph.get(concept, {}).get("cross_domain_equivalents", {})
```

## Working with Scripts

### scripts/detect-ambiguity.py

Pattern matching utility for ambiguity detection.

**Usage:**
```bash
python scripts/detect-ambiguity.py --message "user message here"
# Returns: confidence score, detected patterns, suggested validation
```

**When to use:**
- Programmatic ambiguity detection in hooks
- Batch analysis of conversation history
- Testing new ambiguity patterns

### scripts/domain-mapper.py

Term translation utility using knowledge files.

**Usage:**
```bash
python scripts/domain-mapper.py --term "make it talk" --domain autogen
# Returns: ranked translations with confidence scores
```

**When to use:**
- Translate specific terms
- Generate clarification options
- Validate translations against knowledge

### scripts/knowledge-query.py

Unified interface to all knowledge sources.

**Usage:**
```bash
python scripts/knowledge-query.py --term "api" --sources static,external,codebase
# Returns: results from each source in order
```

**When to use:**
- Query all knowledge sources in one call
- Implement the three-tier query workflow
- Aggregate results from multiple sources

## Additional Resources

### Reference Files

For detailed domain knowledge and advanced patterns:
- **`references/cognitive-framework.md`** - Complete AGENTS.md framework adapted for Claude Code
- **`references/decision-trees.md`** - Detailed decision trees and flowcharts
- **`references/domain-ontologies.md`** - Comprehensive domain knowledge graphs (Autogen, Langroid)
- **`references/translation-patterns.md`** - Extensive ambiguous→precise mappings

### Example Files

Working examples of semantic validation:
- **`examples/autogen-mappings.md`** - Autogen-specific ambiguity resolutions
- **`examples/langroid-mappings.md`** - Langroid-specific examples
- **`examples/common-ambiguities.md`** - Cross-domain frequent patterns

### Knowledge Files

Domain knowledge JSON files:
- **`knowledge/ambiguous-terms.json`** - User phrases with ambiguity scores
- **`knowledge/technical-mappings.json`** - Domain-specific translations
- **`knowledge/ontology-graph.json`** - Conceptual relationships

## Best Practices

### Always Verify, Never Assume

"Never ASSUME - it makes an ass out of u and me."

- Present options when ambiguity detected
- Ask clarifying questions before proceeding
- Confirm understanding with user
- Never proceed with interpretation alone

### Maintain Conversational Tone

- Avoid clinical language: "Ambiguity detected at 87% confidence"
- Use helpful framing: "I notice [term] could mean a few different things..."
- Frame as collaboration: "Let me make sure I understand..."
- Be transparent about uncertainty

### Respect User Triggers

Users have different patterns for expressing uncertainty. Learn from settings:
- Default triggers: "am I making sense?", "does this make sense?"
- Custom triggers from `.claude/semantic-linguist.local.md`
- Adapt to user's communication style

### Progressive Validation

Not every message needs validation:
- Start with high-confidence triggers only
- Expand to moderate-confidence as needed
- Don't interrupt clear, unambiguous requests
- Balance helpfulness with intrusiveness

## Configuration

Users can customize via `.claude/semantic-linguist.local.md`:

- **Sensitivity**: low, medium (default), high
- **Interaction style**: explicit (default), guided, silent
- **User trigger phrases**: Custom patterns to trigger validation
- **Custom terminology mappings**: Project-specific translations
- **Enabled domains**: Which domains to validate against

Respect user configuration when determining whether to trigger validation.

---

**Core principle**: Bridge the gap between human natural language and AI technical precision through systematic semantic validation and conversational clarification.
