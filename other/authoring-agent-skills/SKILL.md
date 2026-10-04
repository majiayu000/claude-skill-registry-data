---
name: authoring-agent-skills
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P002
  - P003
  - P004
  - P006
  - P007
  - P011
  - P014
  - P015
  - P017
  - P019
  - P020
  - P021
  - P022
  - P024
  - P025
  - P032
  - P037
  - P045
  - P047
  - P048
  - P053
  - P055
  - P056
  - P058
  - P061
  - P079
  - P085
  - P086
  - P087
  - P100
  - P108
  - P109
  - P110
  - P112
  - P113
  - P116
  - P119
  - P120
  - P123
  - P137
  - P139
  - P147
  claims:
  - C00001
  - C00002
  - C00003
  - C00004
  - C00006
  - C00008
  - C00009
  - C00017
  - C00019
  - C00021
  - C00022
  - C00023
  - C00056
  - C00057
  evidence: []
  source_anchors: []
  authored_from_digest: 79884ee9a61c2909ebbe8e670d594967f48568d22e30eda084a5ef5b2550175b
---


# Skill: authoring-agent-skills

## Purpose

Author an Agent Skill as a self-contained SKILL.md — plus optional bundled scripts, references, and assets — that an agent can discover from its description, load lazily, and run reliably. It keeps the always-loaded frontmatter tiny, designs for three-tier progressive disclosure, writes the body as a scannable operational recipe within its context budget, pushes deterministic work into bundled scripts, and stays portable across the platforms that implement the open Agent Skills standard.

## When to use

- Creating a new skill, or restructuring one whose SKILL.md has grown large or unfocused.
- Writing or reviewing the frontmatter name and description that drive discovery and triggering.
- Deciding how to split instructions, references, scripts, and assets across the skill folder for progressive disclosure.
- Making one skill run unchanged across the agent platforms that implement the standard.

## Procedure

Work the practices the situation engages; each restates a promoted principle — apply it and cite the principle id.

- Design Skills for progressive disclosure and a small context footprint [P001].
- Treat the SKILL.md description as the sole triggering signal and invest effort accordingly [P002].
- Apply progressive disclosure [P003].
- Author each agent skill as a self-contained directory whose SKILL.md is the entry point and which also holds any scripts or resources the instructions reference; Copilot auto-discovers every file in that directory when the skill [P004].
- Author skills from the agent's perspective and iterate empirically [P006].
- Design Skills for three-tier progressive disclosure [P007].
- Write instructions that are structured, scannable [P011].
- Treat Skills as executable software [P014].
- Write concise skill descriptions with clear scope and boundaries, front-loading the primary use case and trigger words [P015].
- For deterministic, repeatable work, ship an executable script and have Claude run it via bash rather than generating code inline [P017].
- Match instruction strictness to task risk and fragility [P019].
- Package skills in the standard Agent Skills folder format [P020].
- Always supply the required SKILL.md frontmatter [P021].
- Use progressive disclosure [P022].
- Enforce Skill frontmatter constraints [P024].
- Bundle reusable deterministic scripts for repeatable, mechanically checkable skill operations [P025].
- Rely on Claude's automatic Skill matching and progressive disclosure rather than hardcoding invocation [P032].
- Write the SKILL.md body as actionable instructions, examples [P037].
- Use skills to turn multi-step tasks into consistent, auditable, repeatable procedures rather than one-off ad-hoc runs [P045].
- Author skills against the open Agent Skills specification to keep them portable across compatible AI platforms [P047].
- Use forward-slash file paths in skill instructions and references for cross-platform compatibility [P048].
- Aim for moderate detail [P053].
- When multiple tools or approaches could work, pick one default and mention alternatives only briefly instead of presenting equal options [P055].
- Use rendered images and visual inspection when a skill must reason about spatial layout, form structure, or other visual input properties [P056].
- Scaffold a new skill with the skill-creator skill instead of hand-editing files [P058].
- Make frontmatter descriptions precise enough for automatic loading [P061].
- Keep every Skill concise [P079].
- Author every Skill as a SKILL.md with valid YAML frontmatter carrying the required name and description; keep name ≤64 chars of lowercase letters, numbers and hyphens with no XML tags and no reserved words [P085].
- Write skill metadata so discovery works [P086].
- Author a skill as a SKILL.md plus optional scripts, references [P087].
- Author each skill to encode discovery, orchestration [P100].
- For reusable logic, bundle a self-contained script that declares its dependencies inline [P108].
- Structure every skill as a directory whose SKILL.md opens with YAML frontmatter defining name and description; the agent pre-loads that metadata at startup as the first level of progressive disclosure [P109].
- Package deterministic or expensive operations as executable code inside the skill instead of relying on token generation; code is cheaper for such work and gives consistent, repeatable results [P110].
- Keep the main skill file concise, structured [P112].
- Package multi-step workflows with bundled instructions, scripts [P113].
- Constrain the skill name to 1-64 characters using only lowercase alphanumerics and hyphens, never starting or ending with a hyphen and never using consecutive hyphens [P116].
- Offer multiple authoring paths [P119].
- Package every skill as a minimal, valid skill folder [P120].
- Match instruction specificity to task fragility [P123].
- Package a skill as a directory containing a SKILL.md [P137].
- Structure every Agent Skill as a folder containing a single SKILL.md file that opens with a YAML frontmatter block [P139].
- Prefer high-fidelity references [P147].

## Inputs

- The skill or capability being authored, its current SKILL.md and folder layout if any, and the workflow it must perform.
- The target surface(s) and any observed behaviour or failure, plus the current SKILL.md, instruction files, or layout under review.

## Output

A prioritized set of recommendations. Per finding: name the specific skill mechanism (frontmatter field, bundled file, header, flag, command, or building block), give the correction, cite the governing principle id, and state the residual trade-off or the referral. Highest-impact first. This advises how to build and operate the skill; it does not write the domain feature, edit the caller's canonical files, or assert effectiveness without an evaluation.

## Anti-patterns to flag

- Overlooking [P001]: Design Skills for progressive disclosure and a small context footprint.
- Overlooking [P002]: Treat the SKILL.md description as the sole triggering signal and invest effort accordingly.
- Overlooking [P003]: Apply progressive disclosure.
- Overlooking [P004]: Author each agent skill as a self-contained directory whose SKILL.md is the entry point and which also holds any scripts or resources.
- Overlooking [P006]: Author skills from the agent's perspective and iterate empirically.
- Overlooking [P007]: Design Skills for three-tier progressive disclosure.

## References

See `../../references/skill-format-and-frontmatter-reference.md`, `../../references/platform-customization-matrix.md`, `../../references/context-and-harness-engineering-reference.md` for lookup detail, and `../../principles/principles.yaml` for the full statement behind every cited id.

## Grounding

Derived from P001, P002, P003, P004, P006, P007, P011, P014, P015, P017, P019, P020, P021, P022, P024, P025, P032, P037, P045, P047, P048, P053, P055, P056, P058, P061, P079, P085, P086, P087, P100, P108, P109, P110, P112, P113, P116, P119, P120, P123, P137, P139, P147, grounded in the fifty-nine ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`. Distillation-only: no verbatim source quotation.
