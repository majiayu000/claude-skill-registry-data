---
name: storm
description: Execute a deep research and writing pipeline using the STORM methodology, leveraging web tools and extensive human-in-the-loop feedback to produce grounded, comprehensive articles.
---

# STORM Deep Research Skill

This skill runs the STORM (Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Answering) workflow. It turns a topic into a deeply researched, cited long-form article.

## Tools to Use
Use the agent's native tools to run the pipeline:
- `tavily_search`: Find broad source coverage. Use `max_results` aggressively and prefer `search_depth: 'advanced'` when coverage matters.
- `obscura_web_scrape`: Read full pages when snippets are not enough.
- `context7_search` / `context7_docs`: Use for software libraries and framework docs.
- Local file tools (`write`, `edit`, `read`, `bash`): Keep all STORM artifacts in the local `.storm` directory.

## Artifact Layout
Always keep state in `.storm/<topic-slug>/` at the repository root.

Use this structure:

```text
.storm/<topic-slug>/
  topic.md
  outline/
    draft.md
    refined.md
  perspectives/
    index.md
    01-general/
      perspective.md
      conversation.md
      research/
        turn-01.md
        turn-02.md
    02-<perspective-slug>/
      perspective.md
      conversation.md
      research/
        turn-01.md
        turn-02.md
  references/
    index.json
    sources/
      source-0001.json
      source-0002.json
  sections/
    01-<section-slug>.md
    02-<section-slug>.md
  final_article.md
```

### File Rules
- Each perspective must live in its own directory under `.storm/<topic-slug>/perspectives/`.
- Each perspective directory must contain its own `perspective.md` and `conversation.md`.
- Research must not be kept in one shared file. Save each research turn in its own file under that perspective's `research/` directory.
- Store source material separately under `.storm/<topic-slug>/references/sources/`, with one file per source.
- Keep `.storm/<topic-slug>/references/index.json` as the lookup table for citation ids, URLs, titles, and file paths.

## Architecture & Workflow
The workflow has two phases: **Pre-writing** and **Writing**. Stop at every human checkpoint.

### Phase 1: Pre-writing
1. **Setup**
   - Create a URL-safe topic slug.
   - Create `.storm/<topic-slug>/` if missing.
   - Initialize `topic.md`, `outline/`, `perspectives/`, `references/`, `references/sources/`, and `sections/`.
   - Write the original topic and any user constraints to `.storm/<topic-slug>/topic.md`.

2. **Perspective Discovery**
   - Identify 5-7 distinct editorial perspectives.
   - Always include one general perspective.
   - Save the full list to `.storm/<topic-slug>/perspectives/index.md`.
   - Create one directory per perspective, using a numbered slug such as `01-general`, `02-market-view`, `03-technical-view`.
   - In each perspective directory, create `perspective.md` with:
     - perspective name
     - short description
     - key questions to explore
   - **Human-in-the-Loop Checkpoint 1:** Ask the user to review, add, remove, or rename perspectives before proceeding.

3. **Simulated Conversation & Deep Research**
   - Run a multi-turn Writer/Expert conversation for each perspective.
   - Keep each perspective isolated in its own directory.
   - Save the running Q&A transcript to that perspective's `conversation.md`.
   - For each research turn, create a separate file in `research/turn-XX.md`.
   - Each `turn-XX.md` file should include:
     - the writer question
     - the search queries used
     - the sources reviewed
     - the grounded findings
     - open questions for the next turn
   - When a source is used, save it as its own JSON file under `.storm/<topic-slug>/references/sources/`.
   - Update `.storm/<topic-slug>/references/index.json` with the source id, URL, title, perspective, research turn, and source file path.
   - Reuse existing source files when the same URL appears again. Do not create duplicates.
   - **Human-in-the-Loop Checkpoint 2:** After the conversations finish, ask the user whether the source depth is enough or whether any perspective needs more research.

4. **Outline Synthesis**
   - Generate a draft outline from the topic alone.
   - Save it to `.storm/<topic-slug>/outline/draft.md`.
   - Refine the outline using the perspective conversations and research files.
   - Save the refined version to `.storm/<topic-slug>/outline/refined.md`.
   - Merge overlapping sections.
   - **Human-in-the-Loop Checkpoint 3:** Present the refined outline and wait for approval.

### Phase 2: Writing
1. **Section-by-Section Generation**
   - Write each section from `.storm/<topic-slug>/outline/refined.md`.
   - During writing, use only the closed local reference set in `.storm/<topic-slug>/references/`.
   - Do not run new web searches during writing.
   - Insert inline citation markers such as `[1]`, `[2]` that resolve through `references/index.json`.
   - Save each section as its own file under `.storm/<topic-slug>/sections/`.
   - **Human-in-the-Loop Checkpoint 4:** Ask whether the user wants to review each section or the assembled draft.

2. **Polishing & Final Assembly**
   - Assemble the final article from the section files.
   - Add a lead summary.
   - Deduplicate repeated content.
   - Generate the final citation index from `references/index.json`.
   - Append a **References** section at the end of the article. Render it as a Markdown table with columns: `#`, `Title`, `URL`, and `Perspective`. Include every source that appears in `references/index.json`, ordered by citation number.
   - Save the article to `.storm/<topic-slug>/final_article.md`.
   - **Human-in-the-Loop Checkpoint 5:** Request final review.

## Execution Rules
- **Be exhaustive:** Search broadly during research.
- **Stay grounded:** During writing, use only the saved local references.
- **Always cite sources:** Every URL visited or used during research must appear in `references/index.json` and in the final article's References table. No source may be dropped silently.
- **Keep artifacts split:** Do not collapse perspectives into one shared conversation file. Do not collapse research turns into one shared research file.
- **Keep filenames stable:** Use numbered directories and numbered turn files so reruns stay predictable.
- **Stop at checkpoints:** Never skip a human approval step.
- **Minimum length:** The final article (`final_article.md`) must contain at least **50,000 words**. Before saving, run `wc -w final_article.md` and keep expanding sections until the count is met. Every section must be substantive — no padding, no repetition. Reach the target through depth: more analysis, more examples, more evidence, more context.
