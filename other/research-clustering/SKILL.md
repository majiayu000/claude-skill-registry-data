---
name: research-clustering
description: Identifies research domains from text or keywords, clusters them into structured sub-areas, and generates an overview, keywords, and research strategy for each cluster. Use this skill for the initial "mapping" phase of any research project — patent searches, literature surveys, technology trend analysis, business case studies. Trigger on requests like "organize research areas", "classify research fields", "identify surrounding domains for this technology", "plan a survey", "decide patent search strategy", "literature mapping", "research landscape". Also triggers on Japanese equivalents like "調査領域を整理して", "研究分野を分類して", "サーベイの計画を立てて", "特許調査の方針を決めて". Use proactively whenever the user wants to structure research targets from keywords or text, understand the big picture before diving into papers/patents/technology, or split a broad field into prioritized sub-areas.
---

# Research Clustering — Domain Identification, Partitioning & Structuring

Takes text or keyword groups as input, identifies the academic/technical domains worth investigating, clusters (partitions) them, and outputs an overview, keywords, and research strategy for each cluster. This skill handles the "map-making" phase of a research project.

## Auto Mode (`--auto`)

When `$ARGUMENTS` contains `--auto`, run the entire workflow **non-interactively** — skip ALL AskUserQuestion calls and use the following defaults:

| Parameter | Default Value |
|-----------|--------------|
| Research Type | Academic Paper Survey |
| Time Range | Last 4 years |
| Search Languages | English + Japanese |
| Output Granularity | Standard |
| Next Action (Step 7) | Done (自動終了) |

In `--auto` mode, the remaining text in `$ARGUMENTS` (after removing `--auto`) is used as the research theme input. For example: `/research-clustering --auto LLM agent orchestration` → theme is "LLM agent orchestration".

If `$ARGUMENTS` does NOT contain `--auto`, proceed with the normal interactive workflow below.

## Workflow

### Step 1: Parse Input

Analyze the user's input and extract research seeds.

**Accepted input formats (support all):**
- Markdown file (keyword list, research theme description, etc.)
- Conversational text (natural-language description of the research topic)
- Any combination of the above

**Elements to extract:**
- Core keywords (technical terms, proper nouns, abbreviations)
- Research purpose and context (why do they want to investigate this?)
- Target domains (academic, patent, business, technology trends, etc.)
- Known constraints (excluded fields, language, region, etc.)

### Step 1.5: Preliminary Scan (Quick Scan)

Before the user hearing, run a lightweight web search on the input keywords to form a hypothesis about the research landscape. The goal is to improve the quality of the hearing — instead of asking vague questions like "what do you want to research?", present concrete options like "here's the field structure I see — which direction should we go deeper?"

**Preliminary search (2–3 queries, keep it lightweight):**
- `"{core keyword} survey"` or `"{core keyword} overview"` to grasp the overall landscape
- `"{core keyword} applications"` or `"{core keyword} use cases"` to check application areas
- If the input keywords are in Japanese, translate to English and search in both languages

**Information to extract from the preliminary scan:**
- Major sub-areas of the field (tentative cluster candidates)
- Recent trends and hot topics
- Potentially related adjacent fields
- Whether the field is paper-heavy, patent-heavy, or practice/case-study-heavy

**Present the hypothesis:**
Summarize the preliminary scan results concisely and present them during the hearing as: "Based on a quick scan, the field appears to be structured as follows..." This lets the user compare against their own research intent and give more precise direction.

### Step 2: User Hearing

> **`--auto` mode**: Skip this entire step. Use the default values from the Auto Mode table above.

Confirm research parameters via AskUserQuestion, informed by the preliminary scan results. Reflect scan-derived hypotheses in default values and option descriptions to reduce user burden.

#### Hearing 1: Research Type

```
AskUserQuestion:
  question: "What type of research would you like to conduct? (multiple selection)"
  header: "Research Type"
  multiSelect: true
  options:
    - label: "Academic Paper Survey"
      description: "Focus on academic papers (arXiv, IEEE, ACM, etc.)"
    - label: "Patent Search"
      description: "Focus on patent literature (USPTO, EPO, JPO, etc.)"
    - label: "Technology Trend Analysis"
      description: "Tech blogs, conference talks, OSS projects, etc."
    - label: "Business Case Study"
      description: "Enterprise adoption cases, market reports, industry trends"
```

#### Hearing 2: Time Range

```
AskUserQuestion:
  question: "What time range should the research cover?"
  header: "Time Range"
  multiSelect: false
  options:
    - label: "Last 4 years (default)"
      description: "Results from 2022 to present"
    - label: "Last 2 years"
      description: "Focus on the latest trends only"
    - label: "Last 7 years"
      description: "Broader coverage"
    - label: "Custom range"
      description: "Specify a custom time range"
```

If "Custom range" is selected, ask a follow-up AskUserQuestion for the specific years.

#### Hearing 3: Search Languages

```
AskUserQuestion:
  question: "Which languages should be used for web searches? (multiple selection)"
  header: "Search Languages"
  multiSelect: true
  options:
    - label: "English"
      description: "Search in English (covers most academic and international sources)"
    - label: "Japanese"
      description: "Search in Japanese (useful for JPO patents, domestic cases, Japanese papers)"
    - label: "Chinese"
      description: "Search in Chinese (useful for Chinese patents, CNKI papers)"
    - label: "Other"
      description: "Specify additional languages"
```

If "Other" is selected, ask a follow-up AskUserQuestion for the specific languages. Pre-select defaults based on the input: if the input contains Japanese text, default to English + Japanese; otherwise default to English only.

#### Hearing 4: Output Granularity

```
AskUserQuestion:
  question: "What level of detail do you want in the output?"
  header: "Output Granularity"
  multiSelect: false
  options:
    - label: "Standard (recommended)"
      description: "Domain partitioning + overview, keywords, and research strategy per cluster"
    - label: "Detailed"
      description: "Standard + representative papers/patents/cases per cluster"
    - label: "Overview only"
      description: "Domain partitioning and keywords only — quick big-picture view"
```

### Step 3: Domain Identification (Web Search)

Based on input keywords and confirmed parameters, use WebSearch to investigate related academic/technical domains.

**Search strategy:**

1. **Initial search**: Broad search using core keyword combinations
   - `"{keyword1} {keyword2} survey"` / `"{keyword1} {keyword2} review"`
   - `"{keyword} taxonomy"` / `"{keyword} classification"`
   - If keywords are in Japanese, translate to English and search in both languages

2. **For academic paper surveys, prioritize review/survey papers**
   - Review and survey papers provide an efficient overview of the entire field, so search for these first
   - Example queries: `"{topic} survey paper {year}"`, `"{topic} systematic review"`, `"{topic} literature review"`
   - Use the taxonomy/classification from discovered survey papers as the starting point for domain partitioning

3. **Expansion search**: Discover related fields from initial results
   - Identify adjacent domains from survey paper sections and classification schemes
   - Discover new axes from frequently co-occurring keywords

4. **For patent searches**: Also investigate IPC/CPC classification codes for technology classification reference

Compile a comprehensive list of candidate academic/technical domains related to the input theme.

### Step 4: Domain Clustering (Partitioning)

Partition the research targets into meaningful clusters based on information collected in Step 3.

**Partitioning principles:**
- Each cluster should be independently researchable
- Cluster boundaries should be clear (minimize overlap)
- Aim for 3–8 clusters (not too coarse, not too fine)
- Use up to 2 levels of hierarchy (major → minor) when the structure naturally calls for it

**Partitioning perspectives (select based on research type):**
- By method/approach (e.g., statistical methods / deep learning / rule-based)
- By application domain (e.g., healthcare / finance / manufacturing)
- By timeline (e.g., classical methods / recent developments / latest trends)
- By problem formulation (e.g., classification / regression / generation)

### Step 5: Cluster Elaboration

For each cluster, produce:

- **Cluster name**: A concise, descriptive title
- **Overview**: 2–5 sentences explaining the scope of the cluster
- **Keywords**: Technical terms and concepts belonging to the cluster (5–15 items)
- **Research strategy**: Recommended approach for deeper investigation of this cluster
- **Representative resources** (only for "Detailed" granularity): A few survey papers, key papers/patents/cases

For academic paper surveys, list the survey/review papers found in Step 3 as "seed resources" for the relevant cluster. Also show how the survey paper's taxonomy maps to the cluster structure.

### Step 6: Output File Generation

Select the output format based on the research scale:

#### Small to medium scale (5 or fewer clusters): Single file

Consolidate everything into one Markdown file.

#### Large scale (6 or more clusters): Directory structure

```
{output-dir}/
  index.md          # Overall overview + cluster list
  cluster-01-xxx.md # Detailed info for each cluster
  cluster-02-xxx.md
  ...
```

#### Output Template (single file / index.md)

```markdown
# {Research Theme}

## Research Parameters

- **Research type**: {Academic Paper Survey / Patent Search / ...}
- **Time range**: {YYYY – YYYY}
- **Generated on**: {YYYY-MM-DD}
- **Input keywords**: {original keyword list}

## Big Picture

{3–5 sentences on the overall positioning of the research theme, current state of the field, and major trends}

## Reference Survey/Review Papers

{For academic paper surveys. List discovered survey papers. Note that their taxonomies informed the domain partitioning}

| Title | Year | Summary | Link |
|-------|------|---------|------|
| {title} | {year} | {one-line summary} | {url} |

## Domain Map

{Conceptual diagram showing inter-cluster relationships. Use ASCII art or Mermaid notation}

## Cluster Summary

| # | Cluster Name | Keyword Count | Summary |
|---|-------------|---------------|---------|
| 1 | {name} | {n} | {one-line summary} |

## Cluster Details

### Cluster 1: {Cluster Name}

**Overview**: {2–5 sentence description}

**Keywords**:
`keyword1`, `keyword2`, `keyword3`, ...

**Research Strategy**:
- {Recommended search queries and information sources}
- {Notable research groups or companies}
- {Recommended reading order from survey papers}

**Representative Resources** (detailed granularity only):
| Title | Type | Year | Summary |
|-------|------|------|---------|
| {title} | Paper/Patent/Case | {year} | {summary} |

---

{Repeat for each cluster}
```

### Step 7: Output Confirmation and Next Actions

> **`--auto` mode**: Skip this step entirely. Treat the result as "Done" and finish.

After output is complete, confirm the next action via AskUserQuestion.

```
AskUserQuestion:
  question: "The domain map is complete. What would you like to do next?"
  header: "Next Action"
  multiSelect: false
  options:
    - label: "Done"
      description: "Finalize the current output"
    - label: "Adjust clusters"
      description: "Change partitioning granularity or classification axes and regenerate"
    - label: "Deep-dive into a specific cluster"
      description: "Investigate papers/patents for a selected cluster in detail"
    - label: "Generate research prompts"
      description: "Generate research prompt files for each cluster (integrates with research-prompt-builder)"
```

If "Deep-dive into a specific cluster" is selected, show a follow-up AskUserQuestion with cluster names as options. For deep-dive research, also suggest integrating with the research-retrieval skill to generate detailed paper lists per cluster.

## Output Location

**MUST READ FIRST**: Before deciding the output path, read `docs/research/README.md` (the single source of truth for the research directory layout) and `.claude/rules/research.md`.

### Path resolution

1. Identify the **domain** (`<domain>`, `snake_case`):
   - Infer from input file path if it lives under `docs/research/(runs|domains)/<domain>/...`
   - Otherwise infer from the research theme or ask the user
2. If `docs/research/domains/<domain>/domain.yaml` exists and defines `output_paths.clustering`, use it.
3. Otherwise use the default path:

   ```
   docs/research/runs/<domain>/clustering/<YYYYMMDD>/
   ```

   - Output `index.md` and `cluster-NN-*.md` files inside this directory.
   - `<YYYYMMDD>` is today's date (UTC or JST is acceptable, use whichever the pipeline uses).
4. **Never write directly under `docs/research/domains/<domain>/`** — that layer is composed of symlinks pointing into `runs/`.
5. **Never overwrite or modify existing files under `runs/<domain>/clustering/<old_date>/`** — clustering is append-only. Re-clustering creates a NEW dated directory.

### After writing

After the new clustering run is written, update (or instruct the pipeline/user to update) the latest pointer:

```bash
ln -snf <YYYYMMDD> docs/research/runs/<domain>/clustering/latest
ln -snf ../../runs/<domain>/clustering/latest docs/research/domains/<domain>/clustering
```

If the `domains/<domain>/` directory does not yet exist, create it (it is just a view layer).

## Parallel Processing

Run multiple web search queries in parallel for efficiency. Use the Agent tool to spawn subagents for concurrent searches.

## Integration with Other Skills

- **research-prompt-builder**: Can generate research prompts for each cluster
- **research-retrieval**: Can produce detailed paper lists per cluster

## Language

- User interactions (AskUserQuestion, etc.) follow the project's response language setting
- Technical terms, paper titles, and proper nouns are kept in their original language
- Web searches are conducted in the languages selected during Hearing 3 (Search Languages)
- **All user-facing output, reports, and summaries must be written in Japanese(すべてのユーザーへの出力は日本語にしてください)**
