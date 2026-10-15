---
name: teacher-profile
description: "Establish, update, and maintain a single teacher's operating context — their role(s), duties/workload, the handoff & role-interaction map (who they pass work to and receive it from: case manager, AP, counselor, nurse, co-teacher, grade/department team), their school assignment, and personal preferences/defaults — then register it into the shared context as classroom/teacher-scope sop_refs + overrides so every other skill adapts to THIS teacher's reality. Use when a teacher says 'set up my profile', 'this is my role/situation', 'I'm a co-teacher / case manager / department head', 'who handles X at my school', 'remember my preferences', or when another skill needs to know a teacher's duties/handoffs. The profile is a GITIGNORED local store (their data, never committed). Do NOT use for student records (shared/records/), for the school/program directory (canonical-sources/schools/), or for bulk staff directories (shared/staff/, gated) — this is the one teacher's own self-described SOP."
---

# teacher-profile

## What this skill does
Captures one teacher's **operating profile** through a short setup wizard and keeps it current. A profile
records: the teacher's **identity-lite** (display name + school, no sensitive PII), their **role(s)**
(supports multi-role, e.g. "5th-grade teacher + MTSS lead"), **duties/workload**, a **handoff &
role-interaction map** (for each recurring handoff: what, to/from whom by *role*, trigger, cadence), and
**preferences/defaults** (tone, templates, pacing norms, communication rules). Public sites won't have
the teacher's true day-to-day situation — so **teacher-stated facts outrank any crawled inference**, and
every field carries provenance + confidence.

The profile is written to a **gitignored local store** (`teacher.local.json` under
`shared/context/profiles/`; shape shown by `shared/context/profiles/teacher.example.json`, validated by
`shared/context/profiles/teacher.schema.json`) and **registered into the shared context**
(`shared/context/`) as classroom/teacher-scope `sop_refs` + `overrides`, so `lesson-planner`,
`family-communication`, `meeting-classifier`, `intervention-mtss`, `special-education-support`, and the
records handoffs all adapt without anyone editing a skill.

## How it works — the unified pipeline
Follow the shared pipeline in `references/method.md`
(`Request → Routing → Protocol Enforcement → Generation → Validation → Quality Gates →
Approval/Certification → Release`). The domain work happens in Generation:
`Wizard intake → Role/handoff modeling → Context registration (sop_refs/overrides) → Validation`.
See `references/wizard.md` for the interview script and `references/profile-model.md` for the data model.

- **User-truth vs inference** — a teacher-stated fact is `provenance: teacher_stated` (high confidence);
  anything pulled from a public site is `provenance: crawled` (low/medium) and is **confirmed by the
  teacher** before it shapes behavior. Teacher-stated always wins (`shared/context/source-of-truth.md`).
- **Handoffs are role-based, not person-based** — map to roles (case manager, AP, counselor) so the
  profile survives staff turnover; an optional person link comes only from the gated `shared/staff/`.
- **School link** — the teacher's school resolves against `canonical-sources/schools/` (MSID), so the profile stays
  consistent with the district index.
- **Quality** — self-check against `references/quality-gates.md`, then hand to `quality-review`.

## Privacy & storage (non-negotiable)
- The profile is **gitignored** (the `*.local.json` files under `shared/context/profiles/`) — the
  teacher's own data, opt-in, never committed. A committed `teacher.example.json` shows the shape with
  placeholders only.
- **No student PII** ever; the teacher's own contact details are minimum-necessary and stay local.
- Updating the profile updates behavior on the next run — no skill edit, no redeploy.

## Artifacts
See `references/artifact-types.md` for the artifact types this skill produces and their specs.

## Output: always emit the metadata block
Every artifact ends with the metadata block from `references/metadata-schema.md`, including the
per-dimension quality scores, the decision, and `human_review_required: true` — outputs are
decision support, not final professional or legal determinations. Use placeholders only; never real
student data.
