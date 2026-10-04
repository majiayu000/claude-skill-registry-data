---
name: design-doc-mermaid
description: Create Mermaid diagrams from text or source code, selecting the diagram type from the shape of the information (flowchart is the last resort). Use for "create a diagram", "generate mermaid", "code to diagram", 「図を描く」「図にする」「アーキテクチャ図」。
---

# Mermaid Architect - Hierarchical Diagram and Documentation Skill

Mermaid diagram and documentation system with specialized guides and code-to-diagram capabilities.

## Table of Contents

- [Decision Tree](#decision-tree)
- [Available Guides and Resources](#available-guides-and-resources)
- [Usage Patterns](#usage-patterns)
- [Resilient Workflow](#resilient-workflow)
- [Unicode Semantic Symbols](#unicode-semantic-symbols)
- [Python Utilities](#python-utilities)
- [Decision Tree Examples](#decision-tree-examples)
- [High-Contrast Styling](#high-contrast-styling)
- [File Organization](#file-organization)
- [Workflow Summary](#workflow-summary)
- [When to Use What](#when-to-use-what)
- [Best Practices](#best-practices)
- [Learning Path](#learning-path)

## Decision Tree

**How this skill works:**

1. **User makes a request** → Skill analyzes intent
2. **Skill determines diagram/document type** → Loads appropriate guide(s)
3. **Value Gate** → Before generating, pass the reverse-conversion test
4. **AI reads specialized guide** → Generates diagram/document using templates
5. **Result delivered** → With validation and export options

### Value Gate: reverse-conversion test (run before drawing)

A diagram must let the reader grasp the **structure** (relations, flow, hierarchy, branching) at a glance without reading prose. A diagram that merely re-packages sentences into boxes is noise, not visualization. See `docs/policy/documentation-policy.md` (「図にする前に『逆変換テスト』を通す」).

**Before generating any diagram, ask: "If I convert this diagram back into a bullet list, is any information lost?"**

- **Straight line (A→B→C) with no branch / merge / loop / parallelism**: No value → use a bullet list, not a diagram
- **Nodes convert back to bullets with zero information loss**: No value → use a table or bullet list
- **Just a 1-to-1 enumeration**: No value → use a table

Only draw when the content needs 2D placement — branching, merging, loops, parallelism, many-to-many, hierarchy, or state transitions. Diagram count is never a goal in itself.

### Type Gate: choose by shape, not by wording (run after the value gate)

Once you have decided to draw, **read `references/diagram-type-selection.md` and pick the type from the shape of the information** — not from the words the user used. "Show me the workflow" does not mean `flowchart`: if states change, it is `stateDiagram-v2`; if several actors exchange messages, it is `sequenceDiagram`; if work sits in status lanes, it is `kanban`.

`flowchart` / `graph` is the **last resort**, not the default. It can express almost anything, and that is exactly why it is chosen too often — being able to express something is not the same as being suited to it.

- **Pick from the shape**: Read `references/diagram-type-selection.md` and take the first matching row
- **flowchart needs justification**: Choose it only when every other row fails. Then state in one line why no other type fits
- **Cannot justify it?**: Choose again — the inability to explain means the shape was never checked
- **A matching row is not a licence**: Some types have narrow limits (`architecture-beta` cannot label edges at all). Check the row's conditions before committing

GitHub renders all 26 Mermaid diagram types (verified by rendering probe), so availability is never a reason to fall back to `flowchart`. Expressiveness is a separate question: when the chosen type cannot carry the information, `graph` with a stated reason is the correct answer, not a failure.

**User Intent Analysis:**

```mermaid
flowchart TD
    Start([User Request]) --> Analyze{Analyze Intent}

    Analyze -->|"a diagram is warranted"| TypeGate[Read Type Selection Table<br/>references/diagram-type-selection.md]
    TypeGate --> Shape{Match the shape<br/>of the information}
    Shape -->|"time-ordered exchange between actors"| Sequence[Load Sequence Diagram Guide<br/>references/guides/diagrams/sequence-diagrams.md]
    Shape -->|"infrastructure, deployment, cloud"| Deploy[Load Deployment Diagram Guide<br/>references/guides/diagrams/deployment-diagrams.md]
    Shape -->|"system components and boundaries"| Arch[Load Architecture Guide<br/>references/guides/diagrams/architecture-diagrams.md]
    Shape -->|"state / entity / hierarchy / quantity / set"| Catalog[Load Full Type Catalog<br/>references/mermaid-diagram-guide.md]
    Shape -->|"branching with no better fit"| Activity[Load Activity Diagram Guide<br/>references/guides/diagrams/activity-diagrams.md<br/>state why no other type fits]
    Analyze -->|"code to diagram"| CodeToDiag[Load Code-to-Diagram Guide<br/>references/guides/code-to-diagram/ + examples/]
    Analyze -->|"unicode symbols, icons"| Unicode[Load Unicode Symbols Guide<br/>references/guides/unicode-symbols/guide.md]
    Analyze -->|"extract, validate, convert"| Scripts[Use Python Scripts<br/>scripts/extract_mermaid.py<br/>scripts/mermaid_to_image.py]

    Activity --> Generate[Generate Diagram]
    Deploy --> Generate
    Arch --> Generate
    Sequence --> Generate
    CodeToDiag --> Generate
    Unicode --> Generate
    Scripts --> Execute[Execute Script]

    Generate --> Validate{Validate?}
    Validate -->|Yes| RunValidation[Run mmdc validation]
    Validate -->|No| Output
    RunValidation --> Output[Output Result]
    Execute --> Output

    classDef decision fill:#FFD700,stroke:#333,stroke-width:2px,color:black
    classDef guide fill:#90EE90,stroke:#333,stroke-width:2px,color:darkgreen
    classDef action fill:#87CEEB,stroke:#333,stroke-width:2px,color:darkblue

    class Analyze,Validate,Shape decision
    class TypeGate,Catalog,Activity,Deploy,Arch,Sequence,CodeToDiag,Unicode,Scripts guide
    class Generate,Execute,RunValidation,Output action
```

## Available Guides and Resources

### Type Selection (read this first)

| Resource                 | Full Path                              | What It Provides                                                                                              |
| ------------------------ | -------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Type Selection Table** | `references/diagram-type-selection.md` | Shape → diagram type, and how each shape degrades if drawn as a flowchart. **Entry point for every diagram.** |
| **Full Type Catalog**    | `references/mermaid-diagram-guide.md`  | Syntax and worked examples for all 26 diagram types                                                           |

### Deep-Dive Guides (`references/guides/diagrams/`)

These four cover the most common shapes in depth. They are **not** the full set of options — the catalog above is. Do not settle for one of these four just because it loaded first.

| Guide                 | Full Path                                             | Load When The Shape Is                                                | Examples                                                                    |
| --------------------- | ----------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Activity Diagrams     | `references/guides/diagrams/activity-diagrams.md`     | Workflows, processes, business logic, user flows, decision trees      | "Show checkout flow", "Document ETL pipeline", "Create approval workflow"   |
| Deployment Diagrams   | `references/guides/diagrams/deployment-diagrams.md`   | Infrastructure, cloud architecture, K8s, serverless, network topology | "Show AWS architecture", "Document GCP deployment", "Create K8s diagram"    |
| Architecture Diagrams | `references/guides/diagrams/architecture-diagrams.md` | System architecture, component design, high-level structure           | "Show system components", "Document microservices", "Architecture overview" |
| Sequence Diagrams     | `references/guides/diagrams/sequence-diagrams.md`     | API interactions, service communication, request/response flows       | "Show API call sequence", "Document auth flow", "Service interactions"      |

### Code-to-Diagram Guide & Examples

| Resource         | Full Path                                     | What It Provides                                                                                                   |
| ---------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Master Guide** | `references/guides/code-to-diagram/README.md` | Complete workflow for analyzing any codebase and extracting diagrams                                               |
| **Spring Boot**  | `examples/spring-boot/README.md`              | Controller→Service→Repository architecture, deployment config, sequence from methods, activity from business logic |
| **FastAPI**      | `examples/fastapi/README.md`                  | Python async patterns, Pydantic models, dependency injection, cloud deployment                                     |
| **React**        | `examples/react/README.md`                    | Component hierarchy, state management, data flow, build pipeline                                                   |
| **Python ETL**   | `examples/python-etl/README.md`               | Data pipeline, transformation steps, error handling, scheduling                                                    |
| **Node/Express** | `examples/node-webapp/README.md`              | Middleware chain, route handlers, async patterns, deployment                                                       |
| **Java Web App** | `examples/java-webapp/README.md`              | Traditional MVC, servlet containers, WAR deployment                                                                |

### Unicode Symbols Guide

**Full Path:** `references/guides/unicode-symbols/guide.md`

**Load when user mentions:** "unicode symbols", "emoji in diagrams", "semantic icons", "add symbols"

**Quick Reference:**

- 📦 Infrastructure: ☁️ 🌐 🔌 📡 🗄️
- ⚙️ Compute: ⚙️ ⚡ 🔄 ♻️ 🚀 💨
- 💾 Data: 💾 📦 📊 📈 🗃️ 🧊
- 📨 Messaging: 📨 📬 📤 📥 🐰 📢
- 🔐 Security: 🔐 🔑 🛡️ 🚪 👤 🎫
- 📝 Monitoring: 📝 📊 🚨 ⚠️ ✅ ❌

### Python Scripts (`scripts/`)

| Script                 | Use For                                                              | Load When                                                                 |
| ---------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `extract_mermaid.py`   | Extract diagrams from Markdown, validate syntax, replace with images | "extract diagrams", "validate mermaid", "find all diagrams"               |
| `mermaid_to_image.py`  | Convert .mmd to PNG/SVG, batch conversion, custom themes             | "convert to image", "render diagram", "create PNG"                        |
| `resilient_diagram.py` | Full workflow: save .mmd, generate image, validate, error recovery   | "generate diagram", "create diagram with validation", "resilient diagram" |

## Usage Patterns

Common request patterns and guide selection. See [When to Use What](#when-to-use-what) for complete mapping.

| Pattern          | Example Request                            | Guides to Load                       |
| ---------------- | ------------------------------------------ | ------------------------------------ |
| Single Diagram   | "Create activity diagram for login flow"   | Diagram type guide + Unicode symbols |
| Code-to-Diagram  | "Generate deployment from application.yml" | Framework example + Deployment guide |
| Extract/Validate | "Extract diagrams from design.md"          | Use `scripts/extract_mermaid.py`     |
| Batch Convert    | "Convert all .mmd to PNG"                  | Use `scripts/mermaid_to_image.py`    |

## Resilient Workflow

Use this workflow for every diagram: it ensures validation, error recovery, and consistent file organization.

**Full Guide:** `references/guides/resilient-workflow.md`

### Workflow Overview

```mermaid
flowchart LR
    A[1. Identify Type] --> B[2. Save .mmd + Image]
    B --> C{3. Valid?}
    C -->|Yes| D[4. Add to Markdown]
    C -->|No| E[5. Error Recovery]
    E --> F{Fix Found?}
    F -->|Yes| A
    F -->|No| G[Search External]
    G --> A

    classDef step fill:#90EE90,stroke:#333,color:darkgreen
    classDef decision fill:#FFD700,stroke:#333,color:black
    class A,B,D,E,G step
    class C,F decision
```

### Key Principle

Add a diagram to markdown only after it passes validation, so broken diagrams never reach the documentation.

**When you edit an existing Markdown file, validation covers every diagram in that file — not just the one you touched.** An edit can break a block you were not looking at, so the unit of validation must match the unit of change (the file). Examples that are broken on purpose belong in a `text` fence, never a `mermaid` one — otherwise they fail this check and render as errors on GitHub.

### Using the Script (Recommended)

```bash
# Generate with full error recovery
python scripts/resilient_diagram.py \
    --code "flowchart TD; A-->B" \
    --markdown-file design_doc \
    --diagram-num 1 \
    --title "process_flow" \
    --format png \
    --json
```

**Output:** Both `.mmd` and `.png` files in `./diagrams/` directory.

### File Naming Convention

```
./diagrams/<markdown_file>_<num>_<type>_<title>.mmd
./diagrams/<markdown_file>_<num>_<type>_<title>.png
```

**Example:** `./diagrams/api_design_01_sequence_auth_flow.png`

### Error Recovery Priority

When validation fails, the workflow automatically:

1. **Check troubleshooting guide** - `references/guides/troubleshooting.md` (28 documented errors)
2. **Search with perplexity** - `perplexity_ask` MCP for syntax questions
3. **Search with brave** - `brave_web_search` MCP for recent solutions
4. **Ask gemini** - `gemini` skill for alternative perspective
5. **General search** - `WebSearch` tool as fallback

### Manual Fallback Steps

If the script is unavailable:

1. **Identify diagram type** from first line (flowchart, sequence, etc.)
2. **Load reference guide** from `references/guides/diagrams/`
3. **Save to** `./diagrams/<markdown_file>_<num>_<type>_<title>.mmd`
4. **Validate:** `mmdc -i file.mmd -o file.png -b white`（mmdc が無ければ `npx -y @mermaid-js/mermaid-cli` に置き換える）。既存 Markdown を編集した場合は `python scripts/extract_mermaid.py <編集したファイル> --validate` でファイル内の全図をまとめて検証する（失敗があれば非ゼロ終了で報告される）
5. **On error:** Search `references/guides/troubleshooting.md` for matching error
6. **If not found:** Use search tools in priority order above
7. **Check the rendering:** 生成した PNG を Read ツールで開いて目視する（構文が通っても読めない崩れは目で見ないと分からない）
8. **Add reference:** `![Description](./diagrams/filename.png)`

### Pattern 6: Resilient Diagram Generation

**User:** "Create a sequence diagram and add it to the design doc"

**Skill Actions:**

1. Identify intent: **diagram generation** + **markdown integration**
2. Load workflow guide: `references/guides/resilient-workflow.md`
3. Identify diagram type: **sequence**
4. Load diagram guide: `references/guides/diagrams/sequence-diagrams.md`
5. Generate Mermaid code using templates
6. Execute resilient workflow:
   ```bash
   python scripts/resilient_diagram.py \
       --code "[generated code]" \
       --markdown-file design_doc \
       --diagram-num 1 \
       --title "api_sequence" \
       --json
   ```
7. If validation fails → Apply troubleshooting fix → Retry
8. On success → Add `![API Sequence](./diagrams/design_doc_01_sequence_api_sequence.png)` to markdown

## Unicode Semantic Symbols

Always use Unicode symbols to enhance diagram clarity. Common patterns:

### Infrastructure & Deployment

```mermaid
graph TB
    Client[👤 User] --> LB[🌐 Load Balancer]
    LB --> App1[⚙️ App Server 1]
    LB --> App2[⚙️ App Server 2]
    App1 --> DB[(💾 Database)]
    App1 --> Cache[(⚡ Redis)]
```

### Activity Flow with States

```mermaid
flowchart TD
    Start([🚀 Start]) --> Process[⚙️ Process Data]
    Process --> Check{✓ Valid?}
    Check -->|Yes| Save[💾 Save]
    Check -->|No| Error[❌ Error]
    Save --> Complete([✅ Complete])
```

### Microservices Architecture

```mermaid
graph TB
    API[🌐 API Gateway] --> Auth[🔐 Auth Service]
    API --> Orders[📋 Order Service]
    Orders --> Queue[📬 Message Queue]
    Queue --> Worker[⚙️ Background Worker]
    Worker --> Storage[📦 Object Storage]
```

**For complete symbol reference, load:** `references/guides/unicode-symbols/guide.md`

## Python Utilities

### Extract Mermaid Diagrams

```bash
# List all diagrams
python scripts/extract_mermaid.py document.md --list-only

# Extract to separate files
python scripts/extract_mermaid.py document.md --output-dir diagrams/

# Validate all diagrams
python scripts/extract_mermaid.py document.md --validate

# Replace with image references (for Confluence upload)
python scripts/extract_mermaid.py document.md --replace-with-images \
  --image-format png --output-markdown output.md
```

### Convert to Images

```bash
# Single conversion
python scripts/mermaid_to_image.py diagram.mmd output.png

# With custom settings
python scripts/mermaid_to_image.py diagram.mmd output.svg \
  --theme dark --background white --width 1200

# Batch convert directory
python scripts/mermaid_to_image.py diagrams/ output/ --format png --recursive

# From stdin
echo "graph TD; A-->B" | python scripts/mermaid_to_image.py - output.png
```

## Decision Tree Examples

### Example 1: User Asks for Workflow Diagram

**Input:** "Show the checkout process workflow"

**Skill Decision Path:**

```
1. Analyze: workflow, process → ACTIVITY DIAGRAM
2. Load guide: references/guides/diagrams/activity-diagrams.md
3. Find pattern: E-commerce checkout (template exists in guide)
4. Generate using template + Unicode symbols
5. Output activity diagram with decision points
```

**Output:** Complete activity diagram with Unicode symbols for cart, payment, order states.

### Example 2: User Provides Spring Boot Code

**Input:** "Here's my Spring Boot controller, create diagrams"

**Skill Decision Path:**

```
1. Analyze: Spring Boot, code provided → CODE-TO-DIAGRAM + SPRING BOOT
2. Load guides:
   - examples/spring-boot/README.md
   - references/guides/diagrams/architecture-diagrams.md (for structure)
   - references/guides/diagrams/sequence-diagrams.md (for method calls)
   - references/guides/diagrams/activity-diagrams.md (for business logic)
3. Generate multiple diagrams:
   a. Architecture diagram from @RestController/@Service/@Repository annotations
   b. Sequence diagram from method call chain
   c. Activity diagram from business logic flow
4. Output all diagrams with explanations
```

**Output:** 3-4 diagrams showing different views of the Spring Boot application.

### Example 3: User Wants Infrastructure Documentation

**Input:** "Document my GCP Cloud Run deployment with AlloyDB"

**Skill Decision Path:**

```
1. Analyze: infrastructure, GCP, Cloud Run → DEPLOYMENT DIAGRAM
2. Load guides:
   - references/guides/diagrams/deployment-diagrams.md
   - examples/spring-boot/ or examples/fastapi/ (if code provided)
3. Check for IaC files (Pulumi, Terraform, docker-compose)
4. Generate deployment diagram with:
   - Cloud Run services with specs
   - VPC connector
   - AlloyDB cluster
   - Security (IAM, Secret Manager)
   - Monitoring
5. Apply Unicode symbols for clarity
6. Output with resource specifications
```

**Output:** Complete GCP deployment diagram with all resources labeled.

## High-Contrast Styling

既定の `classDef` は次のとおり。**記法の例なので描画しない**（ノードが1つも無く、図にしても何も見えない）。

```text
classDef primary fill:#90EE90,stroke:#333,stroke-width:2px,color:darkgreen
classDef secondary fill:#87CEEB,stroke:#333,stroke-width:2px,color:darkblue
classDef database fill:#E6E6FA,stroke:#333,stroke-width:2px,color:darkblue
classDef error fill:#FFB6C1,stroke:#DC143C,stroke-width:2px,color:black
```

**Rules:**

- Light background → Dark text color
- Dark background → Light text color
- Always specify `color:` in every `classDef`

## File Organization

```
design-doc-mermaid/
├── SKILL.md                          # This file - Main orchestrator
├── README.md                         # User documentation
│
├── references/                       # Reference materials
│   ├── diagram-type-selection.md    # Shape → type. Entry point for every diagram
│   ├── mermaid-diagram-guide.md     # Full catalog: syntax for all 26 types
│   └── guides/                       # Specialized guides (load on-demand)
│       ├── diagrams/
│       │   ├── activity-diagrams.md      # Workflows, processes
│       │   ├── deployment-diagrams.md    # Infrastructure, cloud
│       │   ├── architecture-diagrams.md  # System architecture
│       │   └── sequence-diagrams.md      # API interactions
│       ├── code-to-diagram/
│       │   └── README.md                 # Master guide for code analysis
│       ├── unicode-symbols/
│       │   └── guide.md                  # Complete symbol reference
│       └── troubleshooting.md        # Common syntax errors & fixes
│
├── scripts/                          # Python utilities
│   ├── extract_mermaid.py           # Extract & validate diagrams
│   ├── mermaid_to_image.py          # Convert to PNG/SVG
│   └── resilient_diagram.py         # Full workflow with error recovery
│
└── examples/                         # Language-specific patterns
    ├── spring-boot/                 # Spring Boot patterns
    ├── fastapi/                     # FastAPI patterns
    ├── react/                       # React patterns
    ├── python-etl/                  # Data pipeline patterns
    ├── node-webapp/                 # Express.js patterns
    └── java-webapp/                 # Traditional Java patterns
```

## Workflow Summary

1. **Analyze user intent** → Determine diagram type or action needed
2. **Load appropriate guide(s)** → Read only what's needed (token efficient)
3. **Apply templates and patterns** → Use examples from guides
4. **Generate output** → Create diagram or document
5. **Validate** (optional) → Use scripts to verify
6. **Convert** (optional) → Export to images if needed

## When to Use What

Diagram requests route by **shape**, not by the words above them — always via `references/diagram-type-selection.md`. The rows below are for non-diagram actions and for loading deep-dive material once the type is already chosen.

- **Any diagram at all**: `references/diagram-type-selection.md` **first**, then the guide for the chosen type
- **Chosen type is sequence**: `references/guides/diagrams/sequence-diagrams.md`
- **Chosen type is deployment / infrastructure**: `references/guides/diagrams/deployment-diagrams.md`
- **Chosen type is architecture / components**: `references/guides/diagrams/architecture-diagrams.md`
- **Chosen type is flowchart (after justifying it)**: `references/guides/diagrams/activity-diagrams.md`
- **Chosen type is any other of the 26**: `references/mermaid-diagram-guide.md`
- **"Spring Boot code"**: `examples/spring-boot/` + relevant diagram guides
- **"FastAPI code", "Python API"**: `examples/fastapi/` + relevant diagram guides
- **"React app", "frontend"**: `examples/react/` + architecture guide
- **"ETL", "data pipeline", "Python batch"**: `examples/python-etl/` + activity guide
- **"symbols", "unicode", "emoji"**: `references/guides/unicode-symbols/guide.md`
- **"syntax error", "diagram won't render", "troubleshoot"**: `references/guides/troubleshooting.md`
- **"extract diagrams"**: `scripts/extract_mermaid.py`
- **"convert to image", "PNG", "SVG"**: `scripts/mermaid_to_image.py`
- **"create diagram", "generate diagram", "add diagram to markdown"**: `scripts/resilient_diagram.py` + `references/guides/resilient-workflow.md`

## Best Practices

1. **Single Responsibility**: One diagram = One concept
2. **Unicode Enhancement**: Always use semantic symbols for clarity
3. **High Contrast**: Never skip the `color:` property in styles
4. **Validate Early**: Use scripts to catch syntax errors
5. **Template Reuse**: Leverage existing templates and examples
6. **Load On-Demand**: Only read guides needed for the specific request
7. **Token Efficiency**: Use hierarchical loading instead of reading everything

## Learning Path

**New to Mermaid?** Start here:

1. Read `references/guides/unicode-symbols/guide.md` for symbol meanings
2. Read `references/guides/diagrams/activity-diagrams.md` for basic patterns
3. Try examples in `examples/spring-boot/` or `examples/fastapi/`
4. Use `scripts/extract_mermaid.py --validate` to check your work

**Need to document code?** Follow this:

1. Identify your framework → Load relevant `examples/{framework}/`
2. Match code pattern to diagram type
3. Use templates from guide
4. Validate with scripts

---

**Version:** 2.0 (Hierarchical Architecture)
**Last Updated:** 2025-01-13
**Maintained by:** Claude Code Skills
