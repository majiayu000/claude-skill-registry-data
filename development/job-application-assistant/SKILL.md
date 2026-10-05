---
name: job-application-assistant
description: "Tailors CVs and cover letters, evaluates job fit, and prepares interviews. Activates on: applying to a job, evaluating a posting, writing a CV/cover letter, interview prep."
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
  - WebSearch
---

## Purpose

This file is the Plane 1 knowledge anchor for the job application workflow (ARCH-0010). As a Plane 1 skill, it lives under `.claude/skills/job-application-assistant/` and provides the AI assistant with structured knowledge — it does not execute binaries. When activated, this skill loads candidate identity and preference data from the companion profile files and applies the framework rules that govern the drafter-reviewer pipeline (ARCH-0030). The skill supports all four pipeline steps: fit evaluation, CV generation, cover letter generation, and interview preparation. All steps operate under the no-fabrication rule (ARCH-0007), the read-before-write invariant, and the writing-style rules in `03-writing-style.md`.

## Trigger Phrases

- "Apply to <job/URL/company>"
- "Evaluate this job posting"
- "Tailor my CV for <role/company>"
- "Write a cover letter for <company>"
- "Prepare me for an interview with <company>"
- "Am I a good fit for <job>?"
- Any phrase about job applications, fit evaluation, or interview prep

## Companion Files

| File | When to Read |
|------|--------------|
| `01-candidate-profile.md` | Whenever candidate identity, education, experience, or skills data is needed |
| `02-behavioral-profile.md` | For behavioral/culture fit evaluation or when writing about personality fit |
| `03-writing-style.md` | Before generating any CV or cover letter content — rules always apply |
| `04-job-evaluation.md` | When evaluating fit for a job posting (Step 1 of pipeline) |
| `05-cv-templates.md` | When generating or tailoring a CV (Step 2 of pipeline) |
| `06-cover-letter-templates.md` | When generating a cover letter (Step 3 of pipeline) |
| `07-interview-prep.md` | When preparing for an interview or running practice sessions |
| `08-legitimacy.md` | Before drafting (Step 1) — assess posting legitimacy as a separate gate (REQ-8001) |

## Sub-Commands (REQ-6003)

| Entry Phrase | Pipeline Step | Files to Read |
|--------------|---------------|---------------|
| "Evaluate this job posting" | Step 1 — Fit Evaluation | `04-job-evaluation.md`, `08-legitimacy.md`, `01-candidate-profile.md`, `02-behavioral-profile.md` |
| "Write a CV for <company>" | Step 2 — CV Generation | `05-cv-templates.md`, `01-candidate-profile.md`, `03-writing-style.md` |
| "Write a cover letter for <company>" | Step 3 — Cover Letter | `06-cover-letter-templates.md`, `01-candidate-profile.md`, `02-behavioral-profile.md`, `03-writing-style.md` |
| "Prepare for interview with <company>" | Step 4 — Interview Prep | `07-interview-prep.md`, `01-candidate-profile.md` |

**Missing context rule:** Each sub-command can run without upstream steps having completed. If upstream context is missing, prompt: "I need [X] first — want me to run that step now?" Never silently fail or fabricate missing information (ARCH-0007). All sub-commands share `03-writing-style.md` rules, the no-fabrication rule, and the verification checklist.

## Contract

- Always read existing profile files before writing (read-before-write invariant)
- Respect `[UPPER_SNAKE_CASE]` placeholder tokens — do not overwrite them with invented data
- Default AI tool name in all generated documents: **Claude Code** (unless `[AI_TOOL_NAME]` is set in `01-candidate-profile.md` — DEC-017)
- Never fabricate skills, experience, or claims not present in the candidate profile (ARCH-0007)
- The full application pipeline (ARCH-0030) has 7 steps: 0=Parse, 1=Evaluate, 2=Draft, 3=Reviewer Dispatch, 4=Revise, 5=Compile+Verify, 6=Final Checklist. The Sub-Commands table above labels user-facing entry points (Fit Evaluation, CV Gen, Cover Letter, Interview Prep) using shorthand step names — these are not the same as the pipeline step numbers.
- The verification checklist (pipeline Step 6 — Final Checklist) runs exactly once at the end of the full `/apply` pipeline. It does NOT run during the reviewer pass (pipeline Step 3 — Reviewer Dispatch, a separate Claude Code invocation with fresh context per ARCH-0002). Never run the verification checklist inside the reviewer's context.
