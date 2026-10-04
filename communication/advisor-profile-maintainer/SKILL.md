---
name: advisor-profile-maintainer
description: Use when Codex should create, update, audit, or consult a private long-lived profile for an academic advisor, supervisor, mentor, committee member, PI, lab lead, collaborator, or evaluator from user-provided private notes, meeting records, emails, chat summaries, paper comments, draft feedback, lab interactions, or subjective observations. Maintain local evidence-backed advisor profiles focused on research taste, feedback style, writing preferences, experimental standards, communication habits, decision patterns, boundaries, risks, and user-specific relationship context. Use professor-fit-analyzer instead for public-source professor discovery or application fit dossiers. Use anysearch only when the user explicitly wants public facts or current external context added, and never send private notes to external search.
---

# Advisor Profile Maintainer

Maintain a private, evidence-backed model of how a specific advisor thinks, communicates, evaluates work, and interacts with the user. This skill is for durable local profile maintenance, not public professor scouting and not impersonation.

## Core Principles

- Treat user-provided private material as sensitive by default.
- Separate evidence, interpretation, and advice.
- Prefer small confirmed profile updates over large speculative rewrites.
- Store profiles as local files only when the user asks or approves.
- Never silently overwrite existing profile content.
- Never present the profile as the advisor's actual intent; describe it as a working model based on available evidence.

## Profile Modes

1. Create a new advisor profile.
   - Use when the user wants to start tracking a mentor, advisor, PI, committee member, or collaborator.
   - Ask for the profile name/slug only if not inferable.
   - If the user provides raw or summarized material, extract evidence first, then propose a starter profile.

2. Update an existing profile.
   - Use when the user provides new meeting notes, email/chat excerpts, comments, feedback, oral remarks, or observations.
   - Read the existing profile files if paths are known.
   - Produce a proposed update diff and ask for confirmation before writing.

3. Consult a profile.
   - Use when the user asks how this advisor might react, how to prepare for a meeting, how to revise a draft for them, or how to interpret feedback.
   - Cite profile evidence and confidence levels.
   - Do not invent new profile facts during consultation unless the user asks to update.

4. Audit or consolidate a profile.
   - Use when the profile is stale, contradictory, too speculative, too long, or mixed with raw private logs.
   - Preserve raw evidence references; demote unsupported claims; mark conflicts.

## Default Local Layout

When the user asks to persist a profile and does not specify a path, propose a repo-local or user-private location before writing:

```text
advisor-profiles/
  <advisor-slug>/
    profile.md
    preferences.md
    interaction-log.md
    evidence.jsonl
    update-log.md
```

Use `references/profile-schema.md` for file contents and section names.

## Workflow

1. Establish profile target and storage boundary.
   - Identify the advisor/person and relationship type.
   - Determine whether this is a create, update, consult, or audit request.
   - If writing files, confirm the target directory unless the user gave one.
   - Do not store raw private messages unless the user explicitly asks; prefer summarized evidence snippets.

2. Intake material.
   - Accept meeting notes, message excerpts, email summaries, paper comments, review comments, draft annotations, user observations, or public links.
   - Read `references/private-source-handling.md` before processing private or sensitive material.
   - If the user only gives broad impressions, mark them as user impressions rather than evidence.

3. Extract evidence units.
   - Convert material into small entries: date if known, source type, short excerpt or paraphrase, topic, observed behavior, possible interpretation, confidence, sensitivity.
   - Use evidence levels:
     - A: direct repeated evidence from original messages/comments or multiple meetings.
     - B: direct single evidence from one original note/comment.
     - C: user summary or recollection.
     - D: inference, hypothesis, or pattern needing confirmation.
   - Keep contradictory evidence instead of smoothing it away.

4. Map evidence to profile dimensions.
   - Research taste and intellectual standards.
   - Writing and presentation preferences.
   - Experimental or methodological standards.
   - Feedback and criticism style.
   - Communication habits and timing.
   - Decision patterns and risk tolerance.
   - Mentoring boundaries and support style.
   - User-specific relationship context.
   - Known red lines, sensitivities, or recurring misunderstandings.

5. Propose updates before writing.
   - Show a concise "candidate profile update" with additions, revisions, downgraded claims, conflicts, and open questions.
   - Label each update with evidence level and source reference.
   - Ask for confirmation before editing persisted files.

6. Write or update files only after approval.
   - Append evidence entries to `evidence.jsonl`.
   - Update synthesized claims in `profile.md` and `preferences.md`.
   - Add a dated note to `update-log.md`.
   - Append only relevant summarized events to `interaction-log.md`.
   - Avoid duplicating the same fact across files unless one entry is raw evidence and another is synthesis.

7. Use profile for advice.
   - When helping draft emails, meeting agendas, revision plans, or response strategies, cite the profile signals used.
   - Separate "likely advisor concern" from "recommended user action".
   - If confidence is low, say what new evidence would improve the model.

## External Search

- Default to no external search.
- Use `$anysearch` only when the user explicitly asks to enrich the profile with public facts or current context, such as a new paper, lab page update, public talk, or venue preference.
- Never paste private notes, emails, chat logs, personal identifiers, sensitive relationship details, or unpublished work into external search.
- If external context is needed, search anonymized or public-only terms.

## Output Shapes

For profile creation or update:

- Profile target
- Material processed
- Evidence units extracted
- Candidate profile updates
- Conflicts or uncertainty
- Proposed file changes
- Confirmation needed before write

For consultation:

- Question
- Relevant profile signals
- Likely advisor concerns
- Recommended strategy
- What to say / avoid
- Confidence and missing evidence

## Boundaries

- Do not impersonate the advisor as if they are present or consenting.
- Do not generate manipulative psychological tactics.
- Do not store secrets, medical details, family matters, protected traits, raw credentials, or full private chat logs unless the user explicitly requests and the storage path is private.
- Do not infer personality, ethics, or intentions from a single weak signal.
- Do not let user frustration become a one-sided negative profile; preserve counter-evidence and benign explanations.
- Do not use this skill for public professor discovery; route that to `$professor-fit-analyzer`.

## Source-Aware Notes

This skill is inspired by public mentor-distillation, person-profile, relationship-memory, and context-engine skills. Adapt those ideas conservatively: in academic advising, the goal is preparation and relationship memory, not simulating a real person's authority.
