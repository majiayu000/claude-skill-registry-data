---
name: xueba
description: Use when the user wants to study, digest, restructure, or save learning material into Obsidian TAG-flow Markdown; create human-learnable and AI-readable notes, concept maps, Feynman questions, exercises, or review plans; audit or upgrade an existing Obsidian vault; learn from authenticated Feishu/Notion/Yuque/DingTalk/private docs; generate a learning expert prompt, learning expert operating system, or xueba expert mode; or clarify/agentize xueba as a skill, expert mode, agent object, or runtime agent. Trigger on 学霸, Obsidian, TAG流, 双链, 概念关系, AI读取区, 费曼, 复习计划, 知识库体检/升级, 学习专家, 专家提示词, 技能还是智能体, Xueba Agent, 智能体化学霸.
---

# 学霸

Current target version: xueba v2.0 local runtime harness. This is a Codex Skill plus Learning Expert Mode plus Agent Object Layer plus a deterministic local runtime harness. It is not yet a deployed autonomous daemon or cloud service.

Use this skill in five modes:

1. Study Mode: turn dense or fragmented learning material into one coherent Obsidian study note by default, with optional asset-package expansion only when requested.
2. Upgrade Mode: inspect an existing Obsidian vault or selected notes and identify knowledge that can be improved, merged, split, linked, retagged, verified, or turned into learning assets.
3. Learning Expert Mode: generate, refine, or explain xueba as a productized learning expert operating system with role anchoring, stable personality, capability modules, workflow, delivery contract, and quality gate.
4. Agent Design Mode: explain or design xueba as an agent object, including the boundary between skill, expert mode, and independent runtime agent.
5. Runtime Harness Mode: manage local deterministic task records, event logs, and memory-index scaffolds for xueba runtime experiments without claiming autonomous LLM execution.

The goal is not to summarize a source. The goal is to create and maintain notes that support understanding, retrieval, review, transfer, and long-term knowledge growth. The first learning output should usually be one complete Markdown note that explains the topic end to end in the style of a "systematic topic note"; many files are useful only after the user wants long-term decomposition.

The user's preferred knowledge style is TAG flow: light folders, strong tags, strong search, selective bidirectional links.

## Core Principles

- Optimize for learning, not note volume. A large MOC or many files does not mean the user has learned the topic.
- Keep every important claim traceable to a source, or mark it as an inference.
- Mark missing, uncertain, inferred, and source-grounded knowledge explicitly with labels such as `待补充`, `待验证`, `推论`, and `原文依据`.
- Use tags as controlled metadata. Do not invent near-duplicate tags.
- Use double links only for durable concepts, models, methods, people, technologies, or questions worth reusing.
- Distinguish source claims, AI synthesis, and user-context inference.
- Make the note useful for both human study and future AI reuse: stable headings, concept IDs, aliases, keywords, and explicit concept relationships are useful when they do not bloat the note.
- Produce exercises that force recall, explanation, transfer, and real work.
- Default to report-first when upgrading existing notes. Do not rewrite the user's notes unless they explicitly ask you to apply changes.
- Default to one-file output in Study Mode. The single note should resemble a polished Obsidian system topic note: abstract, mental map, concept network, Why/What/How, boundaries, Feynman loop, exercises, sources, and QA. Do not split into MOC, concepts, questions, and exercises as separate files unless the user explicitly asks for a knowledge asset package, concept cards, or long-term vault decomposition.
- Treat authenticated sources as a normal input class. Try safe authorization paths before giving up, but never bypass access controls, scrape cookies/tokens, ask for passwords, or fabricate content from a login page.
- Treat installing Obsidian or changing host applications as a host-system change. Explain the official source and command, use a dry run when useful, and proceed only when explicit user or host approval is available. If approval is unavailable, still prepare the learning draft, but do not claim it was saved to Obsidian.
- Save durable learning notes into the resolved Obsidian vault under `88-学习/`, not into machine-specific folders, existing personal taxonomies, or a generated-output scratch area. Use generated-output folders only for drafts, tests, failure reports, or intermediate artifacts when the user explicitly wants them.
- Saving to Obsidian means writing into the user's actual Obsidian vault, not merely the current Codex workspace. Resolve the live vault before saving.
- Do not hard-code machine-specific vault paths or Obsidian deep links in this skill. Treat Obsidian as local software plus a set of vault directories that must be discovered or provided at runtime.

## Safety Checkpoints

Stop and get explicit user or host approval before any action that changes the user's environment, existing vault, or task state beyond creating a new learning note.

- 🔴 CHECKPOINT / STOP 🛑: Before installing Obsidian or changing host applications, show the official source, dry-run result when available, and the exact command to run.
- 🔴 CHECKPOINT / STOP 🛑: Before rewriting, moving, splitting, merging, or retagging existing vault notes, present a report and wait for explicit permission to apply edits.
- 🔴 CHECKPOINT / STOP 🛑: Before creating a multi-file asset package, confirm that the user wants files beyond the default single system note.
- 🔴 CHECKPOINT / STOP 🛑: Before using an authenticated browser/session path, state what visible content will be read and confirm that no passwords, cookies, tokens, headers, or session storage will be requested or extracted.
- 🔴 CHECKPOINT / STOP 🛑: Before claiming runtime autonomy, verify that a scheduler, model executor, permission service, observability, deployment, and lifecycle manager actually exist. If not, describe only the local deterministic runtime harness.

## Supported Inputs

Accept these source types:

- Web URL: read the page when network/browser access is available. If inaccessible, ask for pasted content or a local export.
- Authenticated URL: Feishu, Notion, Yuque, DingTalk, private wiki, LMS, Google Docs, and internal docs may require a login session. Use the Authenticated Source Workflow before declaring failure.
- PDF or paper: extract title, author, date, abstract, section structure, page references, and formulas when available.
- Markdown, text, DOCX, slides, or spreadsheet notes: read with the appropriate local tool.
- Video transcript or meeting transcript: preserve timestamps when available.
- Pasted content: treat the pasted text as source and preserve user-provided context.
- Multiple sources: synthesize when they address the same topic; otherwise create one source note plus one synthesis index.

If the source cannot be parsed, return a structured failure with:

```markdown
## 无法处理
- 输入类型：
- 失败原因：
- 需要用户补充：
- 可替代方案：
```

Do not fabricate content to cover missing source text.

## Anti-Patterns And Blacklist

Do not perform these actions. If a user request seems to require one of them, stop, explain the boundary, and offer the safe alternative.

| Anti-pattern | Why it is unsafe or low quality | Safe alternative |
|---|---|---|
| Summarize a login page as if it were the source | It fabricates learning content and hides access failure | Use the Authenticated Source Workflow or return the structured failure block |
| Ask for passwords, 2FA codes, cookies, bearer tokens, authorization headers, or session storage | It bypasses normal access boundaries and exposes secrets | Use public access, official export/API/connector, already-open visible browser content, or user-pasted/exported text |
| Save final notes to the current workspace, generated-output, `/tmp`, `/private/tmp`, or an `obsidian://` link | It falsely reports Obsidian persistence | Resolve the real vault and write under `88-学习/` |
| Hard-code a machine-specific vault path or personal taxonomy | It breaks portability and may write to the wrong place | Resolve the vault at runtime and classify under `88-学习/[大学科]/[章节]/` |
| Default to many files, MOCs, concept cards, question files, and exercise files | It increases note volume without guaranteeing learning | Produce one coherent system note unless the user explicitly asks for an asset package |
| Create double links for ordinary keywords | It pollutes the graph and weakens retrieval | Link only durable reusable concepts, models, methods, people, technologies, or questions |
| Rewrite existing vault notes during an audit by default | It can destroy user organization before review | Report first; edit only after explicit approval |
| Claim the local runtime harness is an autonomous deployed agent | It overstates capability | State that it records tasks, state transitions, events, and memory-index scaffolds, but does not call an LLM or run in the background |
| Generate exercises without answers, scoring criteria, or expected outputs | The learner cannot self-check | Provide reference answers, rubrics, or expected deliverables for every exercise |

## Authenticated Source Workflow

When a source returns a login page, no-permission page, SSO page, empty shell, or JavaScript app without document text, read and follow `references/authenticated-sources.md`.

Never ask for passwords, 2FA codes, cookies, bearer tokens, authorization headers, or session storage. Never summarize a login page as if it were the learning source.

## Controlled Tag System

Use YAML frontmatter tags without `#`. In body text, use `#tag/path` only when necessary.

When choosing tags, domain labels, folder categories, or double-link candidates, read and follow `references/tag-taxonomy.md`.

Every Study Mode note should include these tag dimensions: `status/*`, `type/system-note`, `domain/*`, `source/*`, `access/*`, and `confidence/*`.

## Study Mode Output

Default output for Study Mode is a single Markdown file saved under `88-学习/` in the resolved Obsidian vault. First locate the vault/root, then create or reuse the `88-学习/` learning root and choose content-based subfolders under it.

## Obsidian Vault Resolution

Before writing files, resolve Obsidian and the target vault at runtime.

Prefer this script path when local script execution is available:

1. Resolve vault with `scripts/resolve_obsidian_vault.py --json`. Use `--vault` if the user provided an explicit vault path.
2. If Obsidian is installed but no `selected_vault` is found, rerun with `scripts/resolve_obsidian_vault.py --json --search`. Ask the user to choose only when multiple valid vaults remain or no vault can be resolved.
3. If `obsidian_installed` is false, request explicit approval to install Obsidian from the official GitHub releases repository. Use `scripts/install_obsidian.py --json --dry-run` to show the matched release/asset when helpful, then run `scripts/install_obsidian.py --json` only after approval, and rerun `scripts/resolve_obsidian_vault.py --json`.
4. Classify the note with `scripts/classify_learning_path.py`.
5. Write the note with `scripts/write_obsidian_note.py`.

If scripts are unavailable, read and follow `references/obsidian-workflow.md`.

Saving to Obsidian means writing a Markdown file into the resolved vault directory under `88-学习/`. Do not use current workspaces, generated-output directories, `/tmp`, `obsidian://` links, or a download prompt as save destinations.

Use one coherent note that contains the full learning experience. When writing the default single-file note, read and follow `references/note-template.md`.

Use Obsidian double links selectively inside this single note. If a concept deserves a future card, link it and mark it as "可拆卡", but do not create the separate card unless requested. Avoid making the output look like many small disconnected notes pasted together; the note must read as one complete explanation.

## Optional Asset Package

Only create a multi-file asset package when:

- the user explicitly asks for concept cards, MOC, or a full Obsidian asset package
- the source set is too large for one readable note and the user accepts splitting
- the task is upgrading an existing vault and separate reports/cards are safer

When needed, create this package:

```text
88-学习/[大学科]/[章节或知识要点]/[topic]/
  index.md
  overview.md
  notes.md
  concepts/
    [concept].md
  questions/
    feynman.md
    recall.md
  exercises/
    transfer.md
  review-plan.md
  sources.md
  qa.md
```

Avoid creating empty files.

Use readable Chinese titles for user-facing note titles. Use stable concept filenames that do not include course names, source names, or dates unless needed for disambiguation.

## Mode Selection

Choose Study Mode when the user provides new material or asks to learn a topic from sources.

Choose Upgrade Mode when the user asks to:

- inspect an Obsidian vault or folder
- find notes that can be upgraded
- improve tags, links, MOCs, concept cards, or sources
- detect weak, stale, duplicate, isolated, or overgrown notes
- convert messy notes into reusable learning assets
- build a learning roadmap from existing notes

If the user asks for both, run Upgrade Mode first to understand the existing knowledge base, then run Study Mode for new material and connect it to existing notes.

Choose Learning Expert Mode when the user asks to:

- generate a learning expert, learning expert prompt, or xueba expert mode
- productize a learning workflow into an expert/agent/skill
- explain how xueba should behave as a learning expert
- design a xueba expert team or multi-agent learning team

When using Learning Expert Mode, read and follow `references/learning-expert.md`, plus `references/expert-personality.md` when the task involves identity/style/self-introduction, and `references/expert-capabilities.md` when the task involves capability design, expert upgrade, or expert-mode evaluation. Do not simulate a multi-agent team by default; keep ordinary learning tasks in single-expert mode unless the user explicitly asks for team design.

Choose Agent Design Mode when the user asks whether xueba is a skill or agent, wants to agentize xueba, asks for an agent object/model/runtime, or wants to turn xueba into an independent long-running learning agent.

When using Agent Design Mode, read and follow `references/xueba-agent.md`, `references/agent-object.md`, and `references/runtime-agent.md` when runtime behavior is requested. Make the current boundary explicit: xueba now includes a local deterministic runtime harness for task state, event logs, and memory-index scaffolding, but it is not a deployed autonomous runtime agent unless a separate scheduler, model executor, permission service, observability, deployment, and lifecycle manager are built and verified.

Choose Runtime Harness Mode when the user asks to create, list, update, or inspect xueba runtime tasks, queue state, event logs, or memory-index scaffolds. Use `scripts/xueba_runtime.py`; do not simulate background autonomy.

## Workflow

This workflow describes Study Mode. Use the Upgrade Mode workflow below when the user asks to improve existing Obsidian content.

### 1. Establish Learning Intent

Before generating notes, infer or ask for:

- Topic
- User goal: overview, work application, exam prep, research, or decision support
- Target difficulty: beginner, intermediate, advanced
- Prior knowledge
- Target reader or use case when it changes the depth or examples
- Desired output location if saving files; if not provided, save under `88-学习/` and infer content-based subfolders from the topic

If the user wants you to continue without clarification, make conservative assumptions and record them in the single output note.

### 2. Parse And Normalize Sources

Extract:

- Title, author, source URL/path, publication date if available
- Source type
- Core thesis
- Section map
- Important definitions, claims, numbers, formulas, code, and examples
- Source anchors: URL, page number, heading, paragraph, timestamp, or file path
- Source-grounded facts, author opinions, inferred conclusions, missing parts, and items that need verification

Remove ads, navigation, repeated boilerplate, and low-value filler. Preserve technical details.

### 3. Build The Learning Model

Reconstruct the material using this order:

1. Why: problem, motivation, constraints, historical or business context
2. What: definitions, mechanisms, components, models, assumptions
3. How: procedure, examples, SOP, implementation pattern
4. Limits: boundary conditions, failure modes, common misconceptions, explicit "熔断条件"
5. Transfer: what the learner can do with this knowledge

Do not copy the original table of contents unless it is already the best learning structure.

Adapt the emphasis to the knowledge type:

- Technical knowledge: include application scenarios, implementation pattern, prerequisites, and common pitfalls.
- Theoretical knowledge: include definitions, assumptions, reasoning chain, boundary conditions, and counterexamples.
- Practical knowledge: include procedure, inputs, outputs, checklist, example, and failure checks.

### 4. Handle Concepts

In default one-file mode, include concepts in a table inside the note. Do not create separate concept files.

Use stable concept IDs such as `C001` inside the concept table when the note has multiple reusable concepts. Keep the human-facing concept name as the primary label, and use the ID only as a retrieval/relationship handle.

Create separate concept cards only in optional asset-package mode or when the user explicitly asks for cards.

When creating separate cards, create them only for durable concepts.

Each concept card should include:

```markdown
---
title: "[概念名]"
aliases: []
tags:
  - status/seed
  - type/concept
  - domain/[domain]
  - confidence/[level]
---

# [概念名]

## 一句话定义

## 边界
- 它是什么：
- 它不是什么：

## 反例

## 常见误区

## 应用场景

## 关联
- 前置：[[...]]
- 后续：[[...]]
- 易混：[[...]]

## 来源
- [source-anchor]
```

Avoid concept cards that only restate a paragraph. A concept card should be reusable outside the original source.

### 5. Generate Learning Tests

Create questions at four levels, preferably inside the single note:

- Recall: closed-book facts, definitions, steps.
- Explanation: Feynman-style explanation and misconception checks.
- Transfer: apply the idea to a new case.
- Real task: a practical output the user can produce.

Every question needs a reference answer, scoring criteria, or expected output. Do not create exercises without answers.

### 6. Build A Review Plan

Use spaced review intervals by default:

- Day 1: recall core concepts and explain the topic map from memory.
- Day 3: answer Feynman questions and correct weak concepts.
- Day 7: complete transfer exercise.
- Day 14: solve a real task or write a one-page synthesis.
- Day 30: decide whether to mark notes as `status/reviewed` or `status/mastered`.

Adapt the plan if the user has an exam date, project deadline, or weekly cadence.

### 7. Run Quality Gate

In default one-file mode, apply `references/quality-gate.md` and include the quality checklist from `references/note-template.md` under `## 5. 来源`. In asset-package mode, create `qa.md` with the same checks adapted to the generated package.

If an item cannot pass, explain the gap and how to fix it.

## Upgrade Mode Workflow

Use Upgrade Mode to evaluate and improve existing Obsidian knowledge. This mode is a knowledge-base audit, not a destructive rewrite.

When auditing or upgrading a vault, read and follow `references/upgrade-mode.md`.

When saving an Upgrade Mode report into the vault, use `88-学习/工具/Obsidian/知识库升级报告/YYYY-MM-DD-知识库升级报告.md` unless the user names another vault-relative path.

Default to report-only. Do not rewrite existing notes unless the user explicitly asks you to apply changes.

## Markdown Templates

Default single-file notes use `references/note-template.md` and the completion criteria in `references/quality-gate.md`. Upgrade reports use `references/upgrade-mode.md`.

Learning Expert Mode uses `references/learning-expert.md`, with `references/expert-personality.md` and `references/expert-capabilities.md` loaded when the user asks about expert identity, expert behavior, capability design, or upgrading xueba into an expert.

Agent Design Mode uses `references/xueba-agent.md`, `references/agent-object.md`, and `references/runtime-agent.md` when runtime behavior is in scope.

## Final Response

When done, report:

- Saved paths
- Source access limitations
- Main generated assets
- Quality gate status
- Next recommended review action

Do not report temporary draft paths as final saved paths.

Keep the response concise. The files should carry the detail.
