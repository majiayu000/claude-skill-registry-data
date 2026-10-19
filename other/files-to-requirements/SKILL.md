---
name: files-to-requirements
description: Turn scattered local files into structured knowledge and then into clarified requirements. Use when Codex needs to collect files from a local directory, filter by path, extension, or modified time, extract text and metadata, merge overlapping content, identify themes, generate requirement candidates, list ambiguity questions, and produce a final requirement summary from messy working materials instead of answering ad hoc questions.
---

# Files To Requirements

## Overview

Use this skill when the input is not one clean document but a local folder full of notes, docs, configs, drafts, logs, markdown files, or mixed working materials.
The goal is not RAG-style Q&A. The goal is to turn scattered files into a clear requirement statement with explicit gaps and follow-up questions.

## When To Use

- The user points to a local directory instead of a single source file.
- The source material is spread across multiple files or nested folders.
- The task is to clarify what is being asked, what is constrained, and what is still missing.
- The user wants a repeatable preprocessing workflow before summarization or requirement analysis.

Do not use this skill when:

- The user already provided one clean document and only wants a short `Requirements` and `Target` extraction.
- The task is general knowledge retrieval or open-ended Q&A over a knowledge base.

## Workflow

### 1. Collect files

- Start from the user-provided directory or file set.
- Filter by:
  - directory scope
  - file extension
  - modified time
  - optional filename keywords
- Prefer high-signal text sources first, such as `md`, `txt`, `rst`, `json`, `yaml`, `yml`, `csv`, source code comments, and lightweight docs.
- Exclude obvious low-value files such as binaries, lockfiles, build artifacts, vendor folders, caches, and generated bundles unless the user explicitly wants them.
- Record the collection rule you used so the result is auditable.

### 2. Extract text and metadata

- For each selected file, keep:
  - absolute or repo-relative path
  - title or inferred topic
  - modified time if available
  - short summary
  - key signals such as goals, constraints, decisions, TODOs, open questions, or interfaces
- Preserve evidence anchors by referencing the source file for important claims.
- If the file is too large, summarize only the sections that affect scope, constraints, or expected outcomes.

### 3. Identify themes and overlap

- Group files by topic, system, feature, project phase, or stakeholder concern.
- Merge duplicates and near-duplicates into one normalized statement.
- Separate:
  - repeated facts
  - conflicting statements
  - stale or superseded material
- Prefer the clearest and most recent source when two files say nearly the same thing.
- If two sources conflict and recency does not resolve it, keep both and mark the conflict explicitly.

### 4. Generate requirement candidates

- Convert the consolidated knowledge into candidate requirements under these lenses:
  - user goal
  - functional need
  - technical constraint
  - delivery or workflow expectation
  - missing dependency or missing decision
- Express each candidate as a short, reviewable statement.
- Mark whether each item is:
  - explicit
  - inferred
  - unresolved
- Do not present implementation ideas as requirements unless the source makes them mandatory.

### 5. Generate clarification questions

- Turn ambiguity into a short list of concrete follow-up questions.
- Focus questions on decisions that materially change scope, architecture, output, or sequencing.
- Prefer questions that can be answered with one sentence or a small option set.
- Group questions by topic if there are many, but keep them brief.

### 6. Produce the final requirement brief

- Produce a final structured summary that a teammate can use without re-reading the source files.
- Keep the brief stable and template-driven.
- Distinguish clearly between what is known, what is inferred, and what still needs confirmation.

## Default Output

Use this structure by default:

```markdown
## Collection Scope
- Path:
- Filters:
- Files reviewed:

## Source Inventory
- `path` | topic | modified | short summary

## Consolidated Knowledge
- Theme:
- Confirmed facts:
- Conflicts or duplicates:

## Requirement Candidates
- [Explicit] ...
- [Inferred] ...
- [Unresolved] ...

## Clarification Questions
- ...
- ...

## Final Requirement Brief
### Goal
...

### Requirements
- ...

### Constraints
- ...

### Missing Information
- ...
```

## Working Rules

- Stay anchored to files, not guesses.
- Prefer fewer, stronger requirement statements over long paraphrases.
- Keep provenance visible for anything important or controversial.
- If the source set is noisy, say which files drove the final conclusion.
- If the source set is incomplete, say so directly instead of filling gaps with assumptions.

## Relationship To Other Skills

- Use this skill before [`extract-requirements-target`](/Users/lex/git/knowledge/skills/extract-requirements-target/SKILL.md) when the real problem is scattered source collection and normalization.
- Use `extract-requirements-target` alone when the input is already a single document or a clean pasted block of text.

## Example Triggers

- "Scan this local folder and tell me the real requirements."
- "Collect these markdown and yaml files, merge overlapping notes, then clarify the ask."
- "I have a pile of local docs. Turn them into structured knowledge and then output requirement questions."
- "先整理本地目录里的文件，再帮我把需求澄清出来。"
