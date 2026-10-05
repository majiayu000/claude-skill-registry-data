---
name: github-search
description: |
  Search GitHub for repositories and code via web search to find reference implementations. 
  Triggers when: (1) User explicitly asks to find GitHub resources like "find me a library for XXX on GitHub", 
  (2) AI determines during development that referencing open-source implementations would be helpful.
  This skill uses web search, NO GitHub API or authentication required.
---

# GitHub Search Skill

Search GitHub for relevant repositories and code via web search, serving as contextual references for AI-generated code.

> **Important**: This skill only performs search and reference lookups. It does NOT include the ability to automatically install or execute open-source tools.

## Trigger Scenarios

### User-Initiated Triggers

When the user explicitly asks to find resources on GitHub:

- "Find me a library for XXX on GitHub"
- "Is there an open-source implementation of XXX I can reference?"
- "What good XXX tools are available on GitHub?"
- "Find me a code example for XXX"

### AI-Initiated Triggers

During development, the AI should proactively search for references in these situations:

- Before implementing complex features, check if mature open-source solutions exist
- When unsure about best practices, reference high-quality open-source implementations
- When specific domain code examples are needed (e.g., algorithms, design patterns)
- When the user's requirement is common enough that the open-source community likely has solutions

---

## Search Strategy

### Core Principle: Multi-Round Progressive Search

A single search often fails to gather sufficient information. Use a **multi-round search strategy**:

1. **Round 1 - Discovery**: Find relevant project names and links
2. **Round 2 - Evaluation**: Search specific projects to get quality info like Stars, activity, etc.
3. **Round 3 - Deep Dive** (optional): Visit project README or docs for usage details

### 1. Repository Search (Finding Libraries, Tools, Projects)

Used to find open-source projects that can be directly used or studied.

**Search Query Patterns**:

```
# Round 1: Broad discovery
best [task keywords] [library/tool/framework] github

# Round 2: Focused evaluation (use comparison queries for richer info)
[projectA] vs [projectB] comparison [year]

# Round 3: Deep dive (visit project directly)
site:github.com [author/project-name]
```

**Example Search Queries**:

| User Need | Round 1 (Discovery) | Round 2 (Evaluation) |
|-----------|---------------------|----------------------|
| Find a React form library | `best react form library github 2025` | `react-hook-form vs formik comparison` |
| Find a Python PDF tool | `best python pdf library github` | `PyPDF2 vs pdfplumber vs reportlab` |
| Find a Node.js cron framework | `best nodejs cron job framework github` | `node-cron vs bull vs agenda comparison` |
| Find a Go HTTP client | `best golang http client library github` | `resty vs req golang http client` |
| Find a Markdown editor component | `best react markdown editor component github` | `react-md-editor vs milkdown comparison` |

**Filter Dimensions** (add based on context as needed):

| Filter | Append to Query | When to Use |
|--------|----------------|-------------|
| Programming language | `python`, `typescript` | When tech stack is clear |
| Quality filter | `best`, `popular`, `awesome` | When a mature, stable solution is needed |
| Recency | Append current year e.g. `2025` | When latest recommendations are needed |
| Specific license | `MIT license` | When there are license requirements |
| Comparison | `vs`, `comparison`, `alternative` | When evaluating multiple options |

### 2. Code Search (Finding Implementation References, Usage Examples)

Used to find specific code implementations or usage examples.

**Search Query Patterns**:

```
# Pattern A: Search GitHub code directly
site:github.com [language] [feature/API] example

# Pattern B: Search tutorials/example articles (often include GitHub links)
[language] [feature] example tutorial github

# Pattern C: Search awesome lists
awesome [domain/technology] github
```

**Example Search Queries**:

| User Need | Recommended Search Query |
|-----------|-------------------------|
| How to use useEffect | `react useEffect best practices example github` |
| Python async request pattern | `python async http request aiohttp example github` |
| WebSocket server implementation | `site:github.com nodejs websocket server example typescript` |
| JWT authentication middleware | `express jwt authentication middleware example github` |
| File upload handling | `typescript file upload multer example github` |

**Filter Dimensions** (add based on context as needed):

| Filter | Append to Query | When to Use |
|--------|----------------|-------------|
| Programming language | `typescript`, `python`, etc. | When code language is clear |
| Framework/library | `react`, `express`, `fastapi`, etc. | When targeting a specific tech stack |
| Complete example | `full example`, `boilerplate`, `starter` | When a full runnable example is needed |
| Best practices | `best practices`, `production-ready` | When production-grade code is needed |

### 3. Getting Project Details

After discovering promising projects through search, use the `WebFetch` tool to visit GitHub repository pages for detailed information:

```
# Get project README, Stars, recent commits, etc.
WebFetch: https://github.com/{owner}/{repo}
```

This step provides precise Star counts, last update dates, README content, etc. for quality evaluation.

---

## Result Quality Evaluation

After obtaining search results, prioritize higher-quality resources as references.

### Evaluation Metrics

| Metric | ✅ Quality Signals | ⚠️ Warning Signals |
|--------|-------------------|---------------------|
| **Stars** | 1k+ stable, 10k+ excellent | < 100 (for mature domains) |
| **Recent commits** | Updated within 6 months | No updates for 2+ years |
| **Documentation quality** | Clear README with usage examples | Sparse or outdated docs |
| **Issue activity** | Issues get responses, regularly closed | Many unresolved issues |
| **Code quality** | Has tests, clear structure | No tests, messy code |

### Evaluation Priority

1. **High priority reference**: Stars > 1000 + active within 6 months + comprehensive docs
2. **Medium priority reference**: Stars 100-1000 + active within 1 year + basic docs
3. **Low priority reference**: Stars < 100 or inactive for 1+ year (use with caution)

### Special Cases

- **Emerging technologies**: Star requirements can be lowered; focus on code quality and activity
- **Niche domains**: Low Stars acceptable, but verify code usability
- **Learning references**: Even inactive projects can be referenced for implementation ideas

---

## Search Result Usage Guidelines

### Reporting Reference Sources to Users

After finding results, you **must** inform the user which open-source projects were referenced.

> **Formatting rules**:
> - Always prefix Star counts with the ⭐ emoji (e.g., `⭐ 10.5k`), both in table cells and inline mentions.
> - **Tables MUST include a separate "GitHub" column** containing the full repository URL (e.g., `https://github.com/owner/repo`). Do NOT use Markdown link syntax like `[GitHub](url)` — always output the raw URL so it displays correctly in terminal environments.

```markdown
📚 **References**

When implementing this feature, I referenced the following open-source projects:

1. **[Project Name](GitHub Link)** ⭐ Star Count
   - Brief explanation of why this project was chosen as reference
   - What parts were referenced (e.g., form validation logic, state management approach)

2. **[Project Name](GitHub Link)** ⭐ Star Count
   - Reference details
```

### Example Report

```markdown
📚 **References**

When implementing the React form validation feature, I referenced the following open-source projects:

1. **[react-hook-form/react-hook-form](https://github.com/react-hook-form/react-hook-form)** ⭐ 38.5k
   - Referenced its hook-based form state management approach
   - Learned from its error handling and validation trigger timing design

2. **[jquense/yup](https://github.com/jquense/yup)** ⭐ 21.8k
   - Referenced its schema-based validation rule definition approach
   - Borrowed from its chained API design pattern
```

### Citation Principles

1. **Clear attribution**: All referenced code must have source attribution
2. **Respect licenses**: Pay attention to the project's open-source license (MIT, Apache, etc.)
3. **Moderate reference**: Learn from ideas and designs; don't copy large sections directly
4. **Independent implementation**: Understand the approach, then implement in your own way rather than simply transplanting code

---

## Usage Limitations

### Capability Scope of This Skill

✅ **Supported**:
- Finding GitHub repositories via web search
- Finding code examples via web search
- Evaluating search result quality
- Serving as reference context for code generation

❌ **Not Supported**:
- Automatically installing discovered libraries/tools
- Automatically executing discovered code
- Cloning or downloading repositories
- Calling the GitHub API (no authentication required)

### Search Frequency Recommendations

- Avoid overly frequent searches within the same development task
- Clarify requirements first, then construct precise search queries
- Prioritize previously searched high-quality resources

---

## Search Examples

### Scenario 1: User Searching for a Library

**User**: Find me a good React drag-and-drop library on GitHub

**AI Behavior**:
1. Construct search query: `github react drag and drop library`
2. Execute web search
3. Evaluate result quality (Stars, activity, documentation)
4. Report recommended libraries and selection rationale to the user

**Output Example**:

```markdown
I searched GitHub for React drag-and-drop libraries. Here are my recommendations:

| Project | GitHub | Stars | Last Updated | Features |
|---------|--------|---------|-------------|----------|
| dnd-kit | https://github.com/clauderic/dnd-kit | ⭐ 10.5k | 2 weeks ago | Lightweight, modular, supports multiple sensors |
| react-beautiful-dnd | https://github.com/atlassian/react-beautiful-dnd | ⭐ 31.8k | 1 year ago | Smooth animations, clean API, but no longer maintained |
| react-dnd | https://github.com/react-dnd/react-dnd | ⭐ 20.3k | 3 months ago | Powerful, highly flexible, steeper learning curve |

**Recommendation**: For new projects, I suggest using `dnd-kit` — it's currently the most active and modern drag-and-drop library.

Would you like me to implement drag-and-drop functionality using one of these?
```

### Scenario 2: AI Proactively Searching for Reference Implementations

**User**: Help me build a Markdown live preview editor

**AI Behavior**:
1. Determine this is a complex feature that warrants referencing open-source implementations
2. Construct search query: `github react markdown editor preview`
3. Search and evaluate results
4. Reference the implementation approach of high-quality projects
5. Inform the user of reference sources, then begin implementation

**Output Example**:

```markdown
Sure, I'll help you build a Markdown live preview editor.

📚 **References**

I searched open-source solutions on GitHub and will reference the following projects' design approaches:

1. **[uiwjs/react-md-editor](https://github.com/uiwjs/react-md-editor)** ⭐ 1.8k
   - Referencing its split-pane preview layout design
   - Learning from its Markdown parsing and syntax highlighting approach

2. **[remarkjs/react-markdown](https://github.com/remarkjs/react-markdown)** ⭐ 12.1k
   - Referencing its remark-based Markdown parsing solution

Now starting implementation...
```

### Scenario 3: Finding Code Examples

**User**: How do I implement async HTTP requests in Python?

**AI Behavior**:
1. Construct search query: `github python async http request example aiohttp`
2. Search for code examples
3. Filter high-quality examples
4. Explain and provide code based on the examples

---

## Search Query Construction Tips

### Keyword Selection

| Scenario | Recommended Keywords |
|----------|---------------------|
| Finding complete projects | `library`, `framework`, `tool`, `sdk`, `kit` |
| Finding code examples | `example`, `snippet`, `sample`, `demo`, `usage` |
| Finding implementation approaches | `implementation`, `how to`, `tutorial` |
| Finding templates/scaffolds | `template`, `boilerplate`, `starter`, `scaffold` |
| Finding specific features | `plugin`, `extension`, `middleware`, `component` |

### Language Mapping

| Language | Search Keywords |
|----------|----------------|
| JavaScript | `javascript`, `js`, `node`, `nodejs` |
| TypeScript | `typescript`, `ts` |
| Python | `python`, `py` |
| Go | `golang`, `go` |
| Rust | `rust`, `rs` |
| Java | `java` |
| C# | `csharp`, `dotnet` |

### Framework Keywords

| Framework/Domain | Search Keywords |
|-----------------|----------------|
| React | `react`, `reactjs`, `nextjs` |
| Vue | `vue`, `vuejs`, `nuxt` |
| Node.js | `node`, `nodejs`, `express`, `nestjs` |
| Python Web | `django`, `flask`, `fastapi` |
| Mobile | `react-native`, `flutter`, `swift`, `kotlin` |
| CLI tools | `cli`, `command-line`, `terminal` |

---

## Important Notes

### Security Considerations

1. **No auto-execution**: Discovered code is for reference only; never auto-run
2. **Review code**: Check code security before referencing
3. **Verify sources**: Prioritize projects from well-known organizations/developers

### Copyright Respect

1. **Attribute sources**: Always credit the source when using referenced code
2. **Respect licenses**: Check the project's open-source license
3. **Avoid infringement**: Do not directly copy large sections of protected code

### Quality Assurance

1. **Verify code**: Referenced code must be validated for applicability
2. **Adapt accordingly**: Adjust based on actual requirements; don't copy blindly
3. **Test coverage**: Referenced code also needs testing and verification
