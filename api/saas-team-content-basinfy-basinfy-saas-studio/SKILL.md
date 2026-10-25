---
name: saas-team-content
description: "Orchestrate the content & communication team — ux-content-strategist, copywriter, api-documentation-engineer, frontend-engineer — UX writing, API docs, transactional emails, and onboarding."
argument-hint: "[content initiative description] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/saas-team-content/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,review_mode,automation`

Resolved above — use as-is; `--review` overrides `review_mode` for this run.

# Team Content & Documentation

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

Orchestrate the content and technical documentation team to author clear product microcopy,
transactional email sequences, OpenAPI specifications, and interactive developer docs.

**Argument check:** If no description is provided, output:
> "Usage: `/saas-team-content [content description] [--review full|lean|solo]` — Describe the content or documentation deliverable (e.g. Transactional email notification suite, Developer API reference documentation, Onboarding empty states and tooltips, Product knowledge base)."

When this skill is invoked with a valid argument, orchestrate the team:

1. **UX Writing & Microcopy**:
   - `ux-content-strategist`: Craft clear, human, error messages, empty-state descriptions, tooltip helpers, and modal confirmations
   - Establish consistent tone of voice (helpful, concise, technically accurate)

2. **Transactional Emails**:
   - `copywriter`: Author responsive transactional emails (Welcome & verification, Workspace invite, Password reset, Invoice receipt, Usage threshold warning)
   - `frontend-engineer`: Implement email templates using React Email / HTML with responsive mobile styling

3. **API & Developer Documentation**:
   - `api-documentation-engineer`: Generate OpenAPI 3.1 schema from route handlers, write curl and SDK code examples, document error status codes and authentication schemes
   - Build developer docs navigation and search

4. **Review & Proofing**:
   - Proofread copy for clarity, internationalization compatibility, and tone consistency.

5. **Verdict**:
   - Output: **COMPLETE** — content, email templates, and documentation authored and integrated.
