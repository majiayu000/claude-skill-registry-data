---
name: notebooklm-prompt-architect
description: Automatically design high-quality, source-grounded prompts for Google NotebookLM when the user wants to study, research, summarize, compare, question, or create outputs from uploaded sources. Use for NotebookLM study guides, briefing documents, FAQs, timelines, quizzes, flashcards, mind maps, Audio Overviews, Video Overviews, slide decks, infographics, reports, or prompts such as "NotebookLM'e ne yazayım?" and "bu kaynakların hepsini kullansın". Convert the user's goal, audience, source set, coverage requirement, language, depth, and output format into a copy-ready prompt that forbids unsupported additions and exposes conflicts or missing evidence. Do not claim to operate NotebookLM or know its current interface without verification.
---

# NotebookLM Prompt Architect

Produce the exact prompt the user can paste into NotebookLM. Ground every requested factual output in the notebook's selected sources and make coverage testable.

Start with [references/prompt-patterns.md](references/prompt-patterns.md). For a
complex notebook, consult [references/source-strategy.md](references/source-strategy.md),
[references/prompt-architecture.md](references/prompt-architecture.md), and
[references/quality-checklist.md](references/quality-checklist.md). Load only the
relevant artifact template, study playbook, or example instead of all supporting
files at once. When the subject is FTR coursework, use `$physio-study-coach` to
shape the learning design; when the user needs source research before
NotebookLM, use the appropriate research skill separately.

## Workflow

1. Resolve the outcome: understand, memorize, compare, revise, present, critique, or create a media overview.
2. Establish audience/level, language, scope, selected sources, excluded sources, required topics, desired length, and output type. Infer these when clear; ask only if a material choice is unresolved.
3. Translate “use everything” into a coverage contract: every selected source must contribute, major sections must be mapped, and omissions/unreadable gaps must be listed.
4. Add a grounding contract: use only selected sources for factual claims; cite source title and page/section/time marker when available; distinguish direct source statements, synthesis/inference, conflicts, and missing evidence.
5. Specify structure and quality criteria. For learning outputs include conceptual explanation, high-yield details, active recall, application, common confusions, and a coverage check.
6. For audio/video/presentation/infographic requests, specify narrative sequence, audience, tone, visual or scene logic, terminology, accessibility, and facts that must not be invented.
7. Return one copy-ready prompt first. Add optional alternate prompt only when a different format or level represents a real tradeoff.

## Grounding rules to embed

- Do not add outside facts unless a clearly separated section is explicitly requested.
- Do not fabricate a citation, quote, page, timestamp, source claim, or consensus.
- When sources conflict, show the conflicting statements and source identities rather than silently choosing one.
- When the answer cannot be established from selected sources, say exactly what is missing.
- Separate source summary from interpretation and generated educational examples.
- Do not present generated quiz questions or emphasis predictions as the instructor's real exam content.

## Output

Lead with `NotebookLM'e yapıştır:` followed by a fenced text block containing the prompt. Keep setup notes outside the block to at most a few lines. Do not surround the prompt with explanation that the user must delete before pasting.

If the user supplied no sources, still provide a prompt with clear placeholders such as `[SEÇİLİ KAYNAKLAR]`; do not invent filenames. If a current NotebookLM feature or button matters, verify it from current official documentation before giving interface steps.
