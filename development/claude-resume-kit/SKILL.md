---
name: claude-resume-kit
description: Adapt the external Claude Resume Kit workflow for Codex. Use when the user wants a researcher-oriented resume, academic CV, cover letter, or project/paper-to-resume workflow that extracts papers, reports, codebases, or research artifacts into a provenance-aware knowledge base, then generates tailored LaTeX resume/CV variants, cover letters, critiques, or revision plans without fabricating publication status, author contribution, metrics, roles, or ownership.
---

# Claude Resume Kit for Codex

This is a Codex-native wrapper around the upstream `ARPeeketi/claude-resume-kit` project. The upstream project is preserved under `assets/upstream-project/`; treat it as bundled reference material and reusable scaffold, not as already configured user data.

## Source And Provenance

- Upstream repo: `https://github.com/ARPeeketi/claude-resume-kit`
- Installed upstream commit: `69930e9de21d5595f9b8c9427adc9c51a9fcbc0e`
- License: MIT, preserved at `assets/upstream-project/LICENSE`
- Original Claude slash skills live in `assets/upstream-project/.claude/skills/`

## Codex Adaptation

The upstream workflow is slash-command based. In Codex, route natural-language requests to the equivalent upstream sub-workflow:

| User intent | Upstream file to read |
|---|---|
| Extract a paper, report, PDF, `.tex`, or codebase into resume evidence | `assets/upstream-project/.claude/skills/setup-extract/SKILL.md` |
| Build or refresh the resume knowledge base from extractions | `assets/upstream-project/.claude/skills/setup-build-kb/SKILL.md` |
| Generate a tailored resume or academic CV from a JD/opportunity | `assets/upstream-project/.claude/skills/make-resume/SKILL.md` |
| Generate a matching cover letter | `assets/upstream-project/.claude/skills/make-cl/SKILL.md` |
| Critique a generated resume/CV/cover letter package | `assets/upstream-project/.claude/skills/critique/SKILL.md` |
| Apply critique or user feedback to a package | `assets/upstream-project/.claude/skills/edit-resume/SKILL.md` |

Read only the relevant upstream sub-skill and the referenced upstream files it names. Do not load the entire upstream project unless the task really needs broad migration or debugging.

## Workflow

1. Identify whether the user is asking for extraction, knowledge-base setup, resume/CV generation, cover-letter generation, critique, or edit.
2. If starting a new project, create or use a working directory chosen by the user. Copy the scaffold from `assets/upstream-project/` into that working directory, excluding `.git` and any generated private output the user does not want copied.
3. Preserve the upstream directory contract inside the working project:
   - `config.md`
   - `CLAUDE.md`
   - `knowledge_base/papers/`
   - `knowledge_base/extractions/`
   - `resume_builder/experience/`
   - `resume_builder/bundles/`
   - `resume_builder/templates/`
   - `JDs/`
   - `output/`
4. Follow the selected upstream sub-skill, translating slash commands into ordinary Codex steps.
5. Preserve mandatory user-confirmation stops from upstream instructions. When the upstream workflow says to stop and wait, stop and ask the user rather than continuing silently.
6. Use the bundled LaTeX templates and helper scripts when generating final `.tex` outputs. If a local TeX toolchain is unavailable, still produce Markdown/session artifacts and clearly state that PDF compilation was not verified.

## Accuracy Rules

- Never claim unpublished, under-review, internal, draft, or coursework material is published.
- Never upgrade contribution verbs beyond evidence: use full-ownership verbs only for work the user actually led or solely performed.
- Never invent author position, publication venue, DOI, acceptance status, metrics, awards, affiliations, dates, roles, or tools.
- Track provenance for every achievement: source artifact, publication status, user's contribution, safe claims, hedged claims, and do-not-claim items.
- If evidence is missing, ask targeted questions or mark the item as uncertain.

## Practical Use In Codex

For a paper-to-CV task:

1. Read `setup-extract/SKILL.md`.
2. Extract metadata, methods, results, collaboration scope, user contribution, provenance notes, and bullet seeds.
3. Write the extraction into the working project's `knowledge_base/extractions/`.
4. Update `_INVENTORY.md` if present, or create it if missing.

For a tailored resume/CV task:

1. Read `make-resume/SKILL.md`.
2. Read the working project's `config.md`, selected JD/opportunity, relevant experience files, role bundle, and resume references.
3. Produce a session file, bullet plan, and then the resume/CV only after user confirmation where required.

For critique:

1. Read `critique/SKILL.md`.
2. Evaluate factual integrity, provenance, fit, formatting, AI-sounding language, and reviewer-perspective risk.
3. Return prioritized fixes and update the session file if the working project uses one.

## Boundaries

- Do not store secrets, tokens, private account data, cookies, or raw private transcripts in the skill or generated reusable scaffold.
- Do not edit the preserved upstream files inside `assets/upstream-project/` unless explicitly updating the installed skill itself.
- Do not treat the upstream example persona as user data.
- Do not submit applications, message recruiters, or automate platform actions.
