---
name: resume-tailoring
description: Adapt the external Claude Code resume-tailoring skill for Codex. Use when the user wants to tailor a resume or CV to a specific job description, research role, internship, RA/PhD opportunity, or batch of similar opportunities using an existing resume library, JD analysis, company/role research, branching experience discovery, confidence-scored evidence matching, truthful reframing, gap analysis, ATS-aware output, and change logs without fabricating skills, metrics, roles, dates, publications, or seniority.
---

# Resume Tailoring for Codex

This is a Codex-native adaptation of the external `varunr89/resume-tailoring-skill`. The upstream skill and supporting references are preserved under `references/upstream/`.

## Source And Provenance

- Upstream repo: `https://github.com/varunr89/resume-tailoring-skill`
- Installed upstream commit: `9a4a0f20f5983d1b533627b8c5191acd1ca0cd89`
- License: MIT, preserved at `references/upstream/LICENSE`
- Upstream skill: `references/upstream/SKILL.upstream.md`

## When To Use

Use this skill when the user provides, or wants to prepare for, a specific opportunity and has existing resume/CV material, project notes, papers, or experience records that can be truthfully reused.

Prefer `claude-resume-kit` when the central task is extracting research papers, reports, or codebases into a provenance-aware academic CV knowledge base. Use this skill when the central task is matching a resume/CV library to one or more target opportunities.

## Required Inputs

- Target JD, role description, professor/RA opportunity, or opportunity notes.
- Resume/CV library path, existing CV file, or enough raw experience material to build a small library.
- Desired output format: Markdown by default; DOCX/PDF/LaTeX only when the local toolchain or user requirement supports it.

## Reference Routing

Read these files only when needed:

- `references/upstream/SKILL.upstream.md`: full upstream workflow.
- `references/upstream/research-prompts.md`: company, role, and JD research templates.
- `references/upstream/matching-strategies.md`: confidence scoring and truthful reframing.
- `references/upstream/branching-questions.md`: conversational experience discovery.
- `references/upstream/multi-job-workflow.md`: batch mode for 3-5 similar opportunities.

## Workflow

1. Build or locate the experience library.
   - Use `resumes/` in the current project by default when it exists.
   - Accept Markdown, plain text, pasted CVs, project notes, or user-provided experience records.
   - Extract roles, dates, companies/institutions, bullets, skills, education, publications, projects, and metrics.

2. Analyze the target opportunity.
   - Parse must-have requirements, nice-to-have requirements, implied skills, keywords, audience, and risk factors.
   - For current or specific opportunities, research public official sources when useful and available.
   - Keep official facts, inferred role needs, and anecdotal context separate.

3. Propose a structure before generation.
   - Recommend section order, role consolidation, title framing, skills grouping, and bullet allocation.
   - Ask for confirmation when the structure materially changes the user's positioning.

4. Match evidence to requirements.
   - Use the upstream confidence model: direct, transferable, adjacent, and impact alignment.
   - Show low-confidence matches and gaps rather than hiding them.
   - For each important reframing, preserve a before/after note and why it remains truthful.

5. Run branching experience discovery when gaps matter.
   - Ask focused follow-up questions instead of a static questionnaire.
   - Capture only experiences the user confirms.
   - Tag new evidence with scope, date, source, and confidence.

6. Generate the tailored output.
   - Produce a tailored resume/CV in Markdown unless another format is requested and feasible.
   - Include a generation report with requirement coverage, evidence mapping, gaps, reframings, and interview-prep notes.
   - If generating files, keep source data and output in the user's chosen project directory.

7. Offer library update.
   - Ask before adding generated or newly discovered content back into the reusable library.
   - Do not overwrite the user's master resume/CV without explicit confirmation.

## Truthfulness Contract

- Never invent roles, companies, institutions, dates, publications, skills, tools, metrics, awards, degrees, or seniority.
- Never add a keyword unless it is directly evidenced, adjacent and clearly framed, or explicitly user-confirmed.
- Never inflate "assisted", "contributed", or "implemented a component" into "led", "owned", or "architected" without evidence.
- Keep gaps honest; recommend cover-letter framing, interview preparation, or future work rather than padding the resume.
- For academic CVs, distinguish publications, manuscripts under review, works in progress, course projects, reproductions, and internal reports.

## Output Shape

For substantive tasks, return or write:

- Tailored resume/CV draft.
- Evidence mapping table.
- Gap and risk notes.
- Change log or before/after reframing notes.
- Suggested next revision.

For quick critique tasks, lead with the highest-risk issues and then concise fixes.

## Boundaries

- Do not automate job applications, recruiter messages, platform submissions, or login-gated actions.
- Do not store secrets, cookies, tokens, private account data, or unrevised sensitive personal information.
- Do not depend on an external API unless the user explicitly requests and configures it.
