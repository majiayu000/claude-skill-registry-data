---
name: obsi-knowledge-harvester
description: Standards for migrating topic notes from Projects/Inbox to the Knowledge Base.
---

# Knowledge Harvester Standards

## Purpose
To curate valuable knowledge from transient project work and move it to a permanent home.

## Migration Rules

### 1. Mapping Logic
- **Tech Stack**: Moves to `20_Learning/10_Topics/Tech_Stack/{Technology}/`
- **Domain Know-How**: Moves to `20_Learning/10_Topics/Domain/{Field}/`
- **General**: Moves to `20_Learning/10_Topics/General/`
- **Notebooks**: `.ipynb` files MUST be converted to `.md` with **Full FidelityAnalysis**.
  - **Structure**: Maintain original headers and markdown logic.
  - **Code**: Include all executable Python code in code blocks.
  - **Outputs**: Capture key text outputs (print, dataframes) in blocks.
  - **Images**: Describe the content/trend of charts if extraction is not possible.
  - **Analysis**: Add a brief "Analysis" comment for complex code blocks.
- **Overlap Protocol**: If a concept note already exists (e.g., `Transformer.md` vs `Transformer_Lab.ipynb`):
  - **Option A (Merge)**: Extract insights and append to the main note as a "## Practical Example" section.
  - **Option B (Supplement)**: Save as `Transformer_Supplementary.md` and link from the main note (`Related: [[...]]`).
  - **Prohibition**: Do NOT create duplicate concept notes. Notebooks are for *Verification/Practice*, not definition.
- **Plan Consolidation**: If a separate `Plan` or `Overview` file exists:
  - **Merge**: Extract 'Learning Goals' and 'Resources' -> Append to Main Note's Introduction or Metadata.
  - **Delete**: Remove the standalone Plan file to keep the folder clean.

### 2. Refactoring on Move
- **Tagging**: Swap `#project/note` -> `#knowledge/topic`.
- **Source Track**: Add `Source: Project Name (Archived)` to frontmatter as **Plain Text**. Do NOT use `[[WikiLink]]` to avoid back-linking to Archive.
- **Trace**: (Optional) Leave a placeholder link if the project still needs it explicitly.
