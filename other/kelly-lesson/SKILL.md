---
name: kelly-lesson
description: Lesson-plan generation and compliance-check desk (Busabase App-in-Skill) for a dean of studies or training-program lead. Use when the user invokes $kelly-lesson or /kelly-lesson, mentions lesson plan, 备课, 教案, teaching plan compliance, curriculum template, dean of studies, teacher training, wants lesson plans drafted from curriculum materials and the school template, teacher drafts imported and checked against quality standards, a review queue for approving plans, or a library of approved plans exported as documents.
metadata:
  category: education
  tags:
    - risk:gated-write
    - industry:education
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-lesson
    resources:
      - teachers
      - plans
      - checks
      - settings
    risk: gated-write

---

# Kelly Lesson

## Overview

Use this skill as the dean-of-studies (教导主任) lesson-plan operator. The school has a required lesson-plan template and quality standards, but teachers' plans vary wildly and checking them all by hand is expensive. Kelly Lesson lets the agent draft plans from curriculum materials plus the school template, run deterministic and agent-assisted compliance checks, and gives the dean a Busabase-backed App-in-Skill review queue (approve / request changes / block) plus a library of approved plans exportable as documents. Teachers' own drafts can also be imported and checked. Reading a curriculum document or a teacher's draft file is a genuine external operation a browser cannot perform: `scripts/ingest_plan.mjs` is the only place a plan enters the system, `scripts/run_checks.mjs` runs the compliance rules, and `scripts/execute_decisions.mjs` prints the plan for approved/changes-requested plans. The AirApp itself only reads Busabase and writes review decisions; export happens through `scripts/export_plans.mjs`, and sending feedback to a teacher is always delegated to another skill (e.g. kelly-email) after explicit approval.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, ingest/check what's due and give the user the clickable AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; then present numbered plans (`Plan #1`) and take verdicts in conversation.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Lesson overview"></td>
    <td width="50%"><img src="assets/screenshots/needs-review.webp" alt="Kelly Lesson review queue"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Teaching-quality desk with compliance pass rate, grade-by-subject coverage, per-teacher status, and the review queue.</td>
    <td><strong>Review queue</strong><br>Plan submissions with compliance summaries, agent revision suggestions, and drafted teacher feedback for approval.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/checks.webp" alt="Kelly Lesson compliance checks"></td>
    <td width="50%"><img src="assets/screenshots/plans.webp" alt="Kelly Lesson plan library"></td>
  </tr>
  <tr>
    <td><strong>Compliance checks</strong><br>Per-rule pass/warn/fail results with evidence snippets, filterable by rule and teacher.</td>
    <td><strong>Plan library</strong><br>Lesson plans by subject, grade, and teacher with source badges, compliance scores, and structured plan detail.</td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-lesson-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- Ingesting a plan is a local-file-only operation: `scripts/ingest_plan.mjs` reads a JSON payload file the agent prepares (from curriculum materials or a parsed teacher document) and writes it to Busabase. It never fetches documents from remote systems on its own.
- The AirApp reads and writes Busabase records only. It must not contact teachers, send messages, export documents, or mutate remote systems.
- Feedback to a teacher is approval-required: the app only stores a drafted note (`feedback-draft`) on the plan record; after the dean approves, the agent sends it via other channels/skills (for example kelly-email) and records the real handoff separately. `scripts/execute_decisions.mjs` never performs this send itself — it only writes an execution marker.
- Treat plans, teacher names, and school documents as private school data. Never commit local payload files, env files, or generated exports.

## Busabase Resources

Four Bases under one application Folder (`kelly-lesson`), declared in `content/kelly-lesson-app/app/js/config.js` and the generated template sidecars under `content/`:

- `teachers`: teachers referenced by lesson plans.
- `plans`: the plan library and review queue in one — structured sections, workflow status, compliance score, and the human decision + execution marker on the same row.
- `checks`: per-plan, per-rule compliance check results.
- `settings`: one row (`record-id: "config"`) with school profile, template sections, compliance rules, and export/feedback preferences.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/lesson-schema.md` for exact field shapes. Compliance scores, the review queue, the recent-activity feed, and metrics are recomputed client-side from the stored rows on every read (`content/kelly-lesson-app/app/js/lesson-model.js`'s `buildSnapshot`/`assembleSnapshot`), so the desk is always fresh regardless of when a browser session loads it relative to the last ingest/checks run.

## First Run And Onboarding

On invocation, check the `plans` Base. If it is empty, guide setup before ingesting real plans: ask, turn by turn, school profile (name, kind, term, class length in minutes), the school template sections (keys, labels, which are required), compliance rules with severities and params, subjects and grades in scope, and export preferences (format, output directory, whether DOCX conversion goes through the agent). Write the answers onto the Settings row, then ingest and check:

```bash
node skills/kelly-lesson/scripts/ingest_plan.mjs payload.json --apply
node skills/kelly-lesson/scripts/run_checks.mjs --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-lesson-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/overview`: teaching-quality command desk — KPI cards (plans total / approved / in revision, compliance pass rate), coverage by grade and subject, per-teacher status summary, review-queue preview, recent activity (derived from each plan's own timestamps).
- `#/plans` and `#/plans/<plan_id>`: the plan library — subject, grade, unit, teacher, source badge (`agent_draft`/`teacher_import`), compliance score, workflow status. Detail shows the full structured plan (objectives, key points and difficulties, materials, lesson-flow stages with timing, board plan, homework, reflection, safety notes, curriculum refs) with the compliance panel and an editable notes field alongside.
- `#/checks`: compliance results — every rule per plan with pass/warn/fail/agent-review badges and evidence snippets, filterable by rule, teacher, and result.
- `#/review`: the review queue — every plan with its workflow state (`needs_review` / `changes_requested` / `approved` / `done` / `blocked`), compliance summary, agent revision suggestions, editable feedback-to-teacher draft, `Review note`, decision buttons (approve / request changes / block), and a stable ref (`Plan #1`). Decisions write directly onto the plan record through `busabase-sdk`.
- `#/settings`: sanitized config summary — school profile, template sections, compliance rules with severities, subjects/grades, export prefs, feedback handoff, read live off the Settings Base.

Demo mode:

- `?demo=overview`, `?demo=plans`, `?demo=checks`, `?demo=review`, and `?demo=detail` open deterministic mock scenes for documentation and screenshots.
- `lang=en` or `lang=zh` forces UI chrome language; with `lang=zh` the demo content itself (school, teachers, plan titles, rules, feedback drafts) is meaningfully localized (北湖中学).
- Deep links such as `/?demo=review&lang=zh#/review` must work.
- Demo mode never reads or writes Busabase. Decision buttons still work in the UI but act on in-memory state only.

UI language: English and Chinese chrome with `Auto` default. Keep real plan content, teacher names, and imported documents in their original language.

## Drafting Workflow

1. Collect inputs: curriculum materials (textbook unit, standards excerpts, prior plans) and the configured template sections.
2. Draft the plan as a structured ingest payload — every required template section filled, at least 3 lesson-flow stages whose minutes sum to the class length, measurable objectives, homework, and a safety note when the lesson is a lab.
3. For a teacher's document, parse it into the same payload with `"source": "teacher_import"` — do not silently fix deficiencies; let the checks surface them.
4. Run the write path:

```bash
node skills/kelly-lesson/scripts/ingest_plan.mjs payload.json --apply
```

The script validates the payload against the school template sections stored on the Settings row, normalizes teachers/plans/checks, and upserts them into Busabase by natural key (`teacher_id`/name, `plan_id`) so re-ingests are idempotent. Without `--apply` it is a dry run.

## Check Workflow

1. Run `node skills/kelly-lesson/scripts/run_checks.mjs --apply`. Deterministic rules (section presence, stage count and timing, duration sums, homework, measurable-verb heuristics, lab safety) are computed from the compliance rules on the Settings row; per-plan compliance scores are recomputed idempotently.
2. Rules typed `agent_review` (for example curriculum alignment) are left as `agent_review`. Judge them yourself by comparing objectives with the cited curriculum refs, then deliver verdicts via an ingest payload's `check_results`; re-running the checker preserves agent-judged results.
3. Summarize failures for the dean by ingesting `compliance_summary`/`suggestions`/`feedback_draft` onto the plan record.
4. Give the user the AirApp URL and send them to `#/review`.

## Decisions And Execution Workflow

1. The dean reviews at `#/review`: approve, request changes (with a note), save an edited draft (revise), or block. Decisions write directly onto the plan record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. On explicit user request to execute, run `scripts/execute_decisions.mjs` (dry-run by default; `--apply` writes `execution-status: "ready_for_agent"` onto each decided plan with the concrete operation — `publish_plan` (from `approve`) or `request_revision` (from `request_changes`) — and target). No external side effects either way; the plan's workflow `status` never changes.
3. The agent then performs the approved follow-up outside the app: for `publish_plan`, run `scripts/export_plans.mjs` and send the feedback draft via other channels (e.g. kelly-email) after approval; for `request_revision`, redraft the plan per the review note, re-ingest, and re-run checks.

## Export Workflow

1. `node skills/kelly-lesson/scripts/export_plans.mjs --out <dir>` reads plans with status `approved` or `done` from Busabase and writes each as clean Markdown (default `exports/`, gitignored). Read-only against Busabase — no state is written back.
2. When the user wants Word/PDF documents, convert the exported Markdown with your document skills (docx/pdf); this skill never bundles converters.
3. Keep exports out of git and report the concrete file paths.

## Safety Defaults

- Approving, blocking, and sending teacher feedback are human decisions; never fabricate a verdict.
- Do not alter a teacher's imported content beyond structural parsing; flag problems via checks and suggestions instead.
- Use stable ids and natural-key upserts so repeated ingests, checks, and executions are idempotent.
- If the plan payload and the school template disagree (unknown rules or sections), stop and reconcile before executing.

## Useful Commands

```bash
node skills/kelly-lesson/scripts/ingest_plan.mjs payload.json --apply
node skills/kelly-lesson/scripts/run_checks.mjs --apply
node skills/kelly-lesson/scripts/execute_decisions.mjs
node skills/kelly-lesson/scripts/execute_decisions.mjs --apply
node skills/kelly-lesson/scripts/export_plans.mjs --out exports/
pnpm --dir skills/kelly-lesson/content/kelly-lesson-app dev
```

In normal use, invoke `/kelly-lesson`, let the skill ingest/check what's due, and open the AirApp.
