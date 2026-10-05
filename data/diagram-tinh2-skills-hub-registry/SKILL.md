---
name: diagram
description: "Generate Mermaid architecture diagrams from your codebase. Produces C4 context and container diagrams, sequence diagrams for key flows, ER diagrams from database schemas, and module dependency graphs. Use when you need architecture diagrams, system diagrams, database ERD, sequence diagrams, dependency visualization, or C4 model diagrams."
version: "2.0.0"
category: docs
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Analyze the project
codebase and generate comprehensive architecture diagrams using Mermaid.

INPUT:
$ARGUMENTS

Accepted arguments:
- No arguments: generate all applicable diagram types.
- `c4`: generate C4 Context and Container diagrams only.
- `sequence`: generate sequence diagrams for key flows only.
- `er`: generate ER diagram from database schema only.
- `deps` or `dependency`: generate module dependency graph only.
- A specific flow description (e.g., "user login flow"): generate a sequence
  diagram for that specific flow.

============================================================
PHASE 1: CODEBASE ANALYSIS
============================================================

Step 1.1 -- Tech Stack and Architecture Detection

Scan config files to determine: project type (web app, API, mobile, CLI, library,
monorepo), primary language/framework, database(s), external services (auth, payment,
email, storage), message queues, caching layers, and API gateway config.

Step 1.2 -- Service and Module Mapping

For monorepos/microservices: read docker-compose.yml or K8s manifests for service
definitions, map inter-service communication, identify external deps per service.

For monoliths: read directory structure to identify modules/domains, trace
import statements to map module dependencies, identify layer boundaries.

Step 1.3 -- Database Schema Extraction

Scan for schema definitions in: schema.prisma, *.entity.ts (TypeORM/MikroORM),
models/*.js (Sequelize), models.py (Django), db/schema.rb (Rails), models/*.py
(SQLAlchemy), schema.ts (Drizzle), migrations/*.sql, *.model.ts (Mongoose).

Extract: table/collection names, columns with types, primary/foreign keys,
relationships (1:1, 1:N, M:N), indexes, and enums.

Step 1.4 -- Key Flow Identification

Identify the most important flows to diagram:
- Authentication flow (login, signup, token refresh)
- Primary business flow (main use case)
- Data write flow (create/update through layers)
- API request lifecycle (middleware, validation, handler, response)
- Background job flow (if applicable)

For each flow, trace: entry point, middleware, service layer, data access,
external calls, and response construction.

============================================================
PHASE 2: DIAGRAM GENERATION
============================================================

Generate Mermaid diagrams. Use C4 syntax for architecture diagrams.

Step 2.1 -- C4 Context Diagram

Show the system in its environment: users/actors, the system boundary, and all
external systems it connects to. Use `C4Context` with `Person`, `System`,
`System_Ext`, and `Rel` elements. Keep it high-level -- no internal details.

Step 2.2 -- C4 Container Diagram

Show major containers within the system boundary: web apps, API servers, databases,
caches, workers, message queues. Use `C4Container` with `Container`, `ContainerDb`,
`ContainerQueue` elements. Show relationships with protocols (HTTPS, SQL, AMQP).

Step 2.3 -- Sequence Diagrams

For each key flow, generate a `sequenceDiagram` showing participants and
message flow. Always generate auth flow if auth exists. Generate the primary
business flow. Include request/response payloads as notes where helpful.

Step 2.4 -- ER Diagram

Generate from extracted schema using `erDiagram` syntax. Include all tables with
columns (name, type, PK/FK/UK markers) and relationships with cardinality
notation (||--o{, }o--o{, etc.).

Step 2.5 -- Module Dependency Graph

Generate a `graph TD` showing how internal modules depend on each other.
Place entry points (routes/controllers) at top, data stores at bottom,
external systems on sides. Flag circular dependencies as warnings.
Use `style` directives to color-code layers.

============================================================
PHASE 3: OUTPUT AND ORGANIZATION
============================================================

Create `docs/diagrams/` directory if it does not exist.

Write individual files:
- `docs/diagrams/c4-context.md` -- C4 Context diagram
- `docs/diagrams/c4-container.md` -- C4 Container diagram
- `docs/diagrams/sequence-auth.md` -- Auth sequence (if applicable)
- `docs/diagrams/sequence-[flow].md` -- Business flow sequence
- `docs/diagrams/er-diagram.md` -- ER diagram (if database exists)
- `docs/diagrams/dependency-graph.md` -- Module dependency graph

Each file: heading, brief explanation, Mermaid code block, notes on
simplifications. Skip diagram types with no data (no ER if no database).

Generate `docs/diagrams/README.md` index linking all diagrams with descriptions.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing documentation, validate completeness:

1. Verify all required sections are present and non-empty.
2. Verify internal cross-references and links resolve correctly.
3. Verify no placeholder text remains ("{TODO}", "[TBD]", "...", "etc.").
4. Verify code examples are syntactically valid.

IF VALIDATION FAILS:
- Identify which sections are incomplete or contain placeholders
- Re-generate only the deficient sections
- Repeat up to 2 iterations

============================================================
OUTPUT
============================================================

## Diagrams Generated

### System Profile
- **Type:** [monolith / microservices / monorepo]
- **Services:** [count]
- **Database Tables:** [count]
- **External Systems:** [count]

### Diagrams Created

| Diagram | File | Entities |
|---------|------|----------|
| C4 Context | docs/diagrams/c4-context.md | N systems |
| C4 Container | docs/diagrams/c4-container.md | N containers |
| Sequence: Auth | docs/diagrams/sequence-auth.md | N participants |
| ER Diagram | docs/diagrams/er-diagram.md | N tables |
| Dependencies | docs/diagrams/dependency-graph.md | N modules |

### Observations
- [Circular dependencies detected]
- [Isolated modules with no connections]
- [Missing relationships that could not be determined]


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /diagram — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT fabricate components, services, or tables. Only diagram what exists.
- Do NOT include internal implementation details in C4 Context diagrams.
- Do NOT generate diagrams for types with no data (no ER if no database).
- Do NOT use PlantUML -- use Mermaid exclusively for GitHub compatibility.
- Do NOT include sensitive info (credentials, internal URLs, IPs) in diagrams.
- Do NOT overwrite existing diagram files without reading them first.

NEXT STEPS:

After generating diagrams:
- "Run `/document` to check overall documentation health."
- "Run `/adr` to create ADRs explaining architectural decisions shown in diagrams."
- "Run `/onboarding` to include these diagrams in the developer onboarding guide."
