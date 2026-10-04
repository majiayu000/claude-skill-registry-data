---
name: research-prompt-builder
description: Build structured research prompts through interactive multi-step hearings using AskUserQuestion with selection-based options (multi-select and free-text via "Other"). Use this skill when the user says things like "create a research prompt", "build a prompt for a research topic", "generate a survey prompt", "I want to create instructions for a paper survey", or "research prompt". Also triggers on Japanese equivalents like "調査プロンプトを作って", "研究テーマのプロンプトを作成", "サーベイ用のプロンプトを生成". Works across any research domain.
---

# Research Prompt Builder

Conduct step-by-step hearings using AskUserQuestion in selection format to generate a structured research prompt.

## Auto Mode (`--auto`)

When `$ARGUMENTS` contains `--auto`, run the entire workflow **non-interactively** — skip ALL AskUserQuestion calls and use the following defaults:

| Parameter | Default Value |
|-----------|--------------|
| Research Field | Input text から自動推定 |
| Objective | Method survey（手法サーベイ） |
| Exclusion Criteria | None（除外条件なし） |
| Goals | Paper list creation + Method comparison table + Taxonomy organization |
| Steps | Keyword search + Survey paper starting point |
| Rules | English papers only + Within last 3 years + Links required |
| Confirmation | Generate（確認なしで即生成） |
| Save Location | Under docs/research/ |

In `--auto` mode, the remaining text in `$ARGUMENTS` (after removing `--auto`) is used as the research theme. For example: `/research-prompt-builder --auto 因果推論 heterogeneous treatment effect` → theme is "因果推論 heterogeneous treatment effect".

The research field is inferred from the theme keywords. If the theme is ambiguous, default to "Machine Learning / AI".

If `$ARGUMENTS` does NOT contain `--auto`, proceed with the normal interactive workflow below.

## Overall Flow

1. Understand the research theme from the user's initial input
2. Gather missing information through step-by-step AskUserQuestion hearings
3. Generate the structured prompt, display it in the conversation, and save to file

All hearings use AskUserQuestion in selection format. Free-text input is accepted via the "Other" option (auto-appended). Always use the AskUserQuestion tool rather than asking questions as plain text.

## Step 1: Understand the Research Theme

> **`--auto` mode**: Skip the initial hearing. Use the theme from `$ARGUMENTS` directly and infer the research field automatically.

Analyze the user's initial input and assess how much of the following information is present:

- **Theme/title**: What to investigate
- **Objective**: Why to investigate
- **Exclusion criteria**: What to exclude
- **Goals**: Specific deliverables
- **Steps**: How to proceed
- **Rules**: Constraints to apply

Skip hearings for items with sufficient information in the initial input. Only ask about missing items. If the initial input is minimal, start by asking about the research field and topic.

### Initial hearing when input is minimal

```
AskUserQuestion:
  question: "Which research field should this prompt cover?"
  header: "Research Field"
  multiSelect: false
  options:
    - label: "Machine Learning / AI"
      description: "Deep learning, reinforcement learning, NLP, CV, and related ML topics"
    - label: "Statistics / Causal Inference"
      description: "Statistical methods, causal inference, experimental design, etc."
    - label: "Software Engineering"
      description: "Development methodologies, architecture, testing, etc."
    - label: "Natural Sciences / Engineering"
      description: "Physics, chemistry, biology, electrical engineering, etc."
```

Based on the answer, ask further about theme details. Dynamically compose options based on the selected field.

## Step 2: Objective Hearing

> **`--auto` mode**: Skip. Use "Method survey".

Once the theme is established, clarify the research objective. Skip if the objective is clear from the initial input.

```
AskUserQuestion:
  question: "What is the primary objective of this research?"
  header: "Objective"
  multiSelect: false
  options:
    - label: "Method survey"
      description: "Comprehensively survey and compare methods in a specific field"
    - label: "Track latest trends"
      description: "Understand recent research trends and new approaches"
    - label: "Implementation / application study"
      description: "Gather knowledge to apply a specific method to your own task"
    - label: "Theoretical understanding"
      description: "Deeply understand the theoretical background and mathematical foundations"
```

## Step 3: Exclusion Criteria Hearing

> **`--auto` mode**: Skip. Use "None" (除外条件なし).

Confirm exclusion criteria to narrow the research scope. Dynamically compose options based on the theme.

```
AskUserQuestion:
  question: "Are there any conditions you'd like to exclude from the research? (multiple selection)"
  header: "Exclusion Criteria"
  multiSelect: true
  options:
    - label: "{Theme-appropriate exclusion candidate 1}"
      description: "{Description}"
    - label: "{Theme-appropriate exclusion candidate 2}"
      description: "{Description}"
    - label: "{Theme-appropriate exclusion candidate 3}"
      description: "{Description}"
    - label: "None"
      description: "No exclusion criteria"
```

Dynamically generate options based on the theme. Examples:
- For ML: "Specific model architectures", "Specific tasks", "Theory-only papers"
- For causal inference: "Specific estimands", "Specific method categories", "Simulation-only studies"

## Step 4: Goals Hearing

> **`--auto` mode**: Skip. Use "Paper list creation" + "Method comparison table" + "Taxonomy organization".

Confirm specific deliverables and targets.

```
AskUserQuestion:
  question: "What goals do you prioritize for this research? (multiple selection)"
  header: "Goals"
  multiSelect: true
  options:
    - label: "Paper list creation"
      description: "Comprehensively list related papers"
    - label: "Method comparison table"
      description: "Create a table comparing method features, prerequisites, and performance"
    - label: "Taxonomy organization"
      description: "Classify methods by approach and direction"
    - label: "Implementation guide"
      description: "Compile implementation-relevant information and code examples"
```

## Step 5: Steps Hearing

> **`--auto` mode**: Skip. Use "Keyword search" + "Survey paper starting point".

Confirm the research approach.

```
AskUserQuestion:
  question: "How should the research proceed? (multiple selection)"
  header: "Steps"
  multiSelect: true
  options:
    - label: "Keyword search (Recommended)"
      description: "Collect search keywords and search Google Scholar/arXiv for papers"
    - label: "Citation network tracing"
      description: "Follow citations and references from key papers to discover related work"
    - label: "Survey paper starting point"
      description: "Start from existing survey papers and comprehensively cover related methods"
    - label: "Conference/journal specific"
      description: "Prioritize papers from specific conferences or journals"
```

## Step 6: Rules Hearing

> **`--auto` mode**: Skip. Use "English papers only" + "Within last 3 years" + "Links required".

Confirm research constraints and rules.

```
AskUserQuestion:
  question: "Select rules to apply to the research (multiple selection)"
  header: "Rules"
  multiSelect: true
  options:
    - label: "English papers only (Recommended)"
      description: "Limit to papers written in English"
    - label: "Within last N years"
      description: "Limit by publication recency"
    - label: "Keep summaries concise"
      description: "Summarize each paper in 3-5 sentences"
    - label: "Links required"
      description: "Always include links to papers"
```

If "Within last N years" is selected, ask for the specific number of years:

```
AskUserQuestion:
  question: "What time range should papers be limited to?"
  header: "Time Range"
  multiSelect: false
  options:
    - label: "Last 3 years (Recommended)"
      description: "Focus on relatively recent research"
    - label: "Last 5 years"
      description: "Broader recent coverage"
    - label: "Last 1 year"
      description: "Latest research only"
```

## Step 7: Confirmation and Generation

> **`--auto` mode**: Skip confirmation. Generate the prompt immediately and save to `docs/research/`.

Once all hearings are complete, summarize the collected information for confirmation.

```
AskUserQuestion:
  question: "Ready to generate the prompt with the following settings. Proceed?"
  header: "Confirmation"
  multiSelect: false
  options:
    - label: "Generate"
      description: "Generate the prompt and save to file"
    - label: "I want to revise something"
      description: "Modify specific items before generating"
```

Display a summary of collected information as text in the conversation before presenting the confirmation question.

If "I want to revise something" is selected, present the items as options and redo the hearing for the selected item.

## Output Format

Output in the following XML-based structure:

```markdown
## {Title}
<title>{Title}</title>
<objective>
{Objective description}
</objective>

<exclusion>
{Exclusion criteria list (bullet points)}
</exclusion>

<goals>
{Goals list (bullet points)}
</goals>

<steps>
{Numbered step list}
</steps>

<rules>
{Rules list (bullet points)}
</rules>
```

## Output Location

> **`--auto` mode**: Skip the save location hearing. Always save to `docs/research/` without asking.

1. **Display in conversation**: Show the full generated prompt in the conversation
2. **Save to file**: Confirm save location with the user

```
AskUserQuestion:
  question: "Where should the prompt be saved?"
  header: "Save Location"
  multiSelect: false
  options:
    - label: "Under docs/research/"
      description: "Save to the docs/research/ directory in the repository"
    - label: "Current directory"
      description: "Save to the current working directory"
    - label: "Don't save"
      description: "Display in conversation only, don't save to file"
```

Filename: `{theme-in-kebab-case}-prompt.md`

## Hearing Principles

- All hearings use AskUserQuestion in selection format. Do not use text-based questions
- Skip items that can be inferred from the user's initial input; only ask about gaps
- Dynamically compose options based on the theme (the examples above are templates — adjust content accordingly)
- A single AskUserQuestion can ask 1-4 questions simultaneously. Group related questions for efficient hearings
- When the user enters free text via "Other", reflect it directly in the prompt

## Language

- Keep method names and technical terms in their original language
- **All user-facing output, reports, and summaries must be written in Japanese(すべてのユーザーへの出力は日本語にしてください)**
