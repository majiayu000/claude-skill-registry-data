---
name: academic-study-coach
description: "Study coach: exam prep, flashcards, English papers/terms, NotebookLM, thesis talks, scholarly writing rules. Sınava hazırla, slaytı özetle, makaleyi çevir, tez sunumu."
---

# Academic Study Coach

Learning and academic work, physiotherapy/FTR first but usable for any course. Answer in the user's language; keep scientific terms exact.

## Choose the module

| Need | Module |
|---|---|
| Slides, PDFs, notes, screenshots or objectives → exam-ready study system (summary tables, high-yield points, flashcards, active recall, case/OSCE questions, study plan) | `physio-study-coach` |
| English article, abstract, guideline, table, acronym or term; sentence-by-sentence reading; academic/statistical language | `physio-clinical-english` |
| Prompts and outputs for Google NotebookLM (study guide, briefing, FAQ, quiz, mind map, Audio/Video Overview) | `notebooklm-prompt-architect` |
| Thesis defense, conference talk, seminar or journal-club slides | `academic-presentations` |
| Scholarly writing compliance: CRediT roles, preregistration, ORCID, preprints, open-access mandates, AI/LLM-use disclosure | `academic-writing` |
| Thesis/project topic ideas, research questions, novel angles | the separate `ai-research-skills` skill (`brainstorming-research-ideas`, `creative-thinking-for-research` modules) |

Related skills: literature search and critical appraisal → `medical-evidence-research`; a patient case → `physio-clinical-copilot`; generic slide/Word/PDF file handling → `office-docs-qa`.

## Rules

- Teach, do not only summarize: explain why, link concepts, and test recall.
- When course material is supplied, it is the source of truth for exam answers; label anything added from outside it.
- Never invent references, statistics, test values or guideline content; mark uncertainty.
- Keep study outputs compact and printable unless depth is requested.
- Research-ideation frameworks live in `ai-research-skills` (a CS/ML library); translate them to the user's field instead of copying ML examples.

## Module map

Open only the module(s) the request needs and read the module file completely before acting. Several modules may combine in one task.

| Module | Use when | File |
|---|---|---|
| `physio-study-coach` | Automatically turn physiotherapy and rehabilitation lecture slides, PDFs, textbook pages, class notes, screenshots, cases, or learning objectives into an exam-ready stud… | [MODULE.md](modules/physio-study-coach/MODULE.md) |
| `physio-clinical-english` | Read, translate, and deeply teach English physiotherapy and rehabilitation language without losing scientific detail. | [MODULE.md](modules/physio-clinical-english/MODULE.md) |
| `notebooklm-prompt-architect` | Automatically design high-quality, source-grounded prompts for Google NotebookLM when the user wants to study, research, summarize, compare, question, or create outputs … | [MODULE.md](modules/notebooklm-prompt-architect/MODULE.md) |
| `academic-presentations` | Plan, write, review, or improve academic presentations for thesis defenses, conferences, seminars, lab meetings, grant briefings, and research talks. | [MODULE.md](modules/academic-presentations/MODULE.md) |
| `academic-writing` | Scholarly writing and research compliance. | [MODULE.md](modules/academic-writing/MODULE.md) |

Supporting files (open only when the module points to them):

- `physio-study-coach`: [study-system.md](modules/physio-study-coach/references/study-system.md)
- `physio-clinical-english`: [contextual-teaching.md](modules/physio-clinical-english/references/contextual-teaching.md), [handoff-contract.md](modules/physio-clinical-english/references/handoff-contract.md), [safety-core.md](modules/physio-clinical-english/references/safety-core.md), [specialty-safeguards.md](modules/physio-clinical-english/references/specialty-safeguards.md)
- `notebooklm-prompt-architect`: [audio-overview-prompt.md](modules/notebooklm-prompt-architect/examples/audio-overview-prompt.md), [dense-study-note-prompt.md](modules/notebooklm-prompt-architect/examples/dense-study-note-prompt.md), [quiz-clinical-vignette-prompt.md](modules/notebooklm-prompt-architect/examples/quiz-clinical-vignette-prompt.md), [slide-deck-prompt.md](modules/notebooklm-prompt-architect/examples/slide-deck-prompt.md), [README.md](modules/notebooklm-prompt-architect/README.md), [notebooklm-artifact-templates.md](modules/notebooklm-prompt-architect/references/notebooklm-artifact-templates.md), [prompt-architecture.md](modules/notebooklm-prompt-architect/references/prompt-architecture.md), [prompt-patterns.md](modules/notebooklm-prompt-architect/references/prompt-patterns.md), [quality-checklist.md](modules/notebooklm-prompt-architect/references/quality-checklist.md), [source-strategy.md](modules/notebooklm-prompt-architect/references/source-strategy.md), [study-exam-playbooks.md](modules/notebooklm-prompt-architect/references/study-exam-playbooks.md), [SOURCES.md](modules/notebooklm-prompt-architect/SOURCES.md)
