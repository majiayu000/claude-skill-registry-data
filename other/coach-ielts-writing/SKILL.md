---
name: coach-ielts-writing
description: Run a complete IELTS Writing Task 2 coaching cycle from timed first draft through evidence-based assessment, personalized active practice, delayed closed-book rewriting, comparison, and transfer checks. Use when the user asks in English or Chinese to practise, 批改, 重写, 复盘, continue, or track IELTS Task 2 writing. Do not use for Task 1, general translation, or isolated correction unless the user asks to add it to IELTS training.
---

# Coach IELTS Writing

Guide one IELTS Writing Task 2 essay through an active, spaced learning cycle. Keep management work automatic while preserving the user's essential learning actions: independent writing, retrieval, revision, generation, self-checking, delayed rewriting, and transfer.

## Start every invocation

1. Resolve `<skill-dir>` to the directory containing this `SKILL.md`, and resolve the learning workspace. Store user data in `<learning-workspace>/.coach-ielts-writing/`, never in this skill directory. If no workspace has been selected, suggest the current dedicated IELTS study directory and ask only if the location is genuinely ambiguous.
2. Run `python3.11 <skill-dir>/scripts/coach_state.py status --workspace <path>` before creating or resuming work.
3. Validate existing state with `python3.11 <skill-dir>/scripts/validate_state.py --workspace <path>`. If validation fails, preserve all files, report the exact issue, and offer safe recovery. Never overwrite an essay to repair metadata.
4. Present one primary next action. Do not dump the whole cycle into the conversation.
5. Follow an explicit user request to start a new cycle, but warn before creating a conflicting active cycle.
6. Enforce a state-specific read allowlist after `status` and validation. For `continue_lesson`, read only `cycle.json`, the lesson plan, the persisted cursor, and responses needed for the current item; do not enumerate or open Version 1, assessment, feedback, reference answers, or unrelated responses. For a rewrite, build and read only the rewrite packet plus minimal task status. A request for a model essay, answer, hint, or explanation never authorizes opening protected files. Open an immutable attempt only when the current workflow step is assessment or comparison and that text is strictly required.

## Route the request

| User intent                   | Action                                                                                      |
| ----------------------------- | ------------------------------------------------------------------------------------------- |
| Start practice / 给我一道题   | Start or resume a cycle; present one Task 2 prompt and the 40-minute conditions             |
| Submit or critique an essay   | Save the verbatim attempt first, then assess it                                             |
| Generate exercises / 专项训练 | Teach the selected ability first, then build one complete timed paper for independent use   |
| Continue / 今天做什么         | Use the deterministic `next_action` from local state                                        |
| Rewrite / 重写                | Use only the rewrite packet and record assistance honestly                                  |
| Compare versions              | Reassess with the same rubric version when possible, then run deterministic comparison      |
| Transfer check                | Use a different topic and surface form without naming the target expression                 |
| Progress / 能力档案           | Summarize evidence and due work; do not equate activity volume with mastery                 |
| Isolated sentence question    | Answer directly; optionally offer to attach it to the active cycle without forcing a lesson |

## Non-negotiable teaching rules

- Treat IELTS scores as evidence-based estimates, not official results. Always store the rubric version, model identifier, confidence, and quoted evidence.
- Distinguish hard grammar errors, collocation or naturalness problems, L1-influenced information structure, logic gaps, and optional style improvements.
- Select one required new core objective per lesson. Add a related secondary objective only when it shares the same decision rule and the same output can prove both. TR or CC core lessons do not add a new secondary objective.
- Keep recognition, judgment, and selection tasks to at most 3–4 items and no more than 25% of the lesson. Require at least 65% active-output time.
- Preserve the submitted answer sheet verbatim. Do not reveal answers, hints, or item-level judgments before the complete paper is submitted.
- Do not reveal a complete Band 7/7.5 essay or line-by-line answer set before Version 2 is submitted.
- Treat protected-file access as answer exposure even if the text is not copied into the final reply. Do not inspect Version 1, detailed feedback, lesson answers, or model language merely to decide that a request must be refused.
- A lesson can advance a skill only to `applied`. Only delayed, unprompted evidence can support `retained`; cross-topic evidence supports `transferred`.
- Do not let repeated recognition questions accumulate into mastery. Apply the evidence gates in `references/workflow-and-mastery.md`.
- Stop at 60 minutes. Save the current response, trim optional work, and schedule an 8–20 minute recovery task if evidence remains insufficient.
- Do not write essay text, provider secrets, or raw model traffic to Mind memory or ordinary logs.

## Run the cycle

### 1. Select and start Version 1

- Prefer a question not recently used, balancing question type, topic, and the user's history. Use a user-supplied prompt when requested.
- Save the exact prompt and start timestamp before showing it.
- State that the 40 minutes include planning, writing, and checking. Disable assistance conversationally: do not supply ideas, vocabulary, corrections, or an outline during the attempt.
- On submission, save the text verbatim and record elapsed time, interruptions, and assistance. Mark non-standard attempts instead of rejecting them.

### 2. Assess and narrow the target

Read `references/assessment-rubric.md`. Produce:

- TR, CC, LR, and GRA estimates with confidence and source evidence;
- paragraph-level reasoning analysis;
- sentence-level issues classified by type and severity;
- two or three candidate issues mapped to the supported `skill_id` values;
- one core objective chosen by score impact, recurrence, transfer value, and diagnostic confidence.

Show a one-minute summary first. Save detailed feedback locally and keep the full model essay locked.

### 3. Teach the focused ability

Read `references/lesson-design.md`. Before testing, give the learner a compact but substantial learning module tied to the exact weakness found in Version 1:

- state the ability target and the decision rule in plain Chinese;
- explain 3–5 transferable knowledge points with before/after examples from the learner's context;
- provide a small expression bank or thinking framework relevant to the topic or rhetorical function;
- walk through one worked example without revealing answers to the coming paper;
- use two quick self-checks and a readiness checklist.

The teaching module must explain how to make the writing decision, not merely list model sentences. Opening it does not start the paper timer. It must not display backend IDs, prompt fields, rubrics, confidence machinery, or hidden marking criteria.

### 4. Run the timed practice paper

Read `references/lesson-design.md` and `references/exercise-contracts.md`. Generate one coherent 60-minute paper with exactly eight self-contained questions, shown together before the timer starts:

1. two foundation questions for recognition and short explanation;
2. two repair questions using flawed but understandable excerpts;
3. two independent-generation questions in genuinely different contexts;
4. two integrated questions, including an IELTS-style paragraph.

The suggested minutes must total 60. Every question must state in one plain-Chinese instruction what to produce, its sentence or word range, all required ideas, and all restrictions. Do not show a separate marking-criteria block. Protected marking criteria may mirror the visible instruction for reliable evaluation, but must never add a hidden requirement.

Do not mark, hint, unlock answers, or adapt the next question while the user is working. Collect and save the complete answer sheet once. Then mark all eight answers together. Show a short whole-paper summary and expand detailed analysis, exact answer evidence, and an improved version only for questions below the published standard. A missed question does not trap the user on the page: record it as needing work and schedule it for later recovery.

### 5. Schedule delayed work

After the last teaching exposure, schedule:

- Version 2 after at least 24 hours, normally within D1–D2;
- a different-topic transfer opportunity in D5–D7;
- a mixed check around D14.

If a recovery lesson adds another teaching exposure, move the rewrite so at least 24 hours still separates teaching and testing. Local due tasks work without background notifications; create an external reminder only when the user explicitly asks and the relevant automation tool is available.

### 6. Protect Version 2

Generate the packet with:

```bash
python3.11 <skill-dir>/scripts/build_rewrite_packet.py --workspace <path> --cycle-id <id>
```

Recommend a fresh Codex task. During collection of Version 2, read only the packet and minimal cycle status; do not read Version 1, feedback, lesson responses, or reference answers. If the user asks for help, provide it only after confirming that the rewrite will be marked `assisted`; assisted work cannot prove retention.

### 7. Compare and test transfer

- Use the same assessment prompt and rubric versions for both attempts whenever possible. If versions differ, state that score movement is not directly comparable.
- Run `compare_attempts.py` for word count, issue frequency per 100 words, recurrence, time, and version-comparability metadata.
- A transfer task must change topic and surface wording, create a natural opportunity for the target ability, and avoid naming the rule or target phrase.
- One success is evidence, not final mastery. Preserve prior evidence when later performance is unstable; mark the skill for review rather than rewriting history.

## State and exchange operations

Read `references/state-schema.md` before state repair, import, export, or migration.

- Use `python3.11 <skill-dir>/scripts/coach_state.py` for initialization, cycle creation, legal transitions, lesson cursors, scheduling, response recording, and CycleBundle import/export.
- Export to canonical JSON (`--output cycle-bundle.json`) or a Web-compatible archive (`--output cycle.iwc-bundle.zip`); the output suffix selects the format. `import-bundle` accepts either format and safely detects ZIP content.
- Generate persistent entity IDs with `coach_state.py new-ids`; all entity, task, bundle, and conflict IDs are UUIDv7. Preserve imported Web IDs.
- Save `assessment`, `issue-evidence`, and `lesson-plan` JSON through `coach_state.py save-contract`; append exercise evidence through `record-response` and `record-evidence` instead of editing state JSON directly.
- Use expected revisions for mutations. On a conflict, re-read state and reconcile; never force an overwrite.
- Export excludes essay content by default. Include content only when the user explicitly asks to continue the full cycle elsewhere.
- Validate bundle version, JCS checksum, archive manifest, and secret exclusion before import. Never extract ZIP members; reject unsafe paths, duplicate members, oversized archives, and excessive expansion.
- For an existing cycle, accept only an idempotent snapshot or its direct append-only successor (`parentRevision` equals the current portable revision). Report immutable-content or branch conflicts and never force an overwrite.
- Do not delete a workspace or cycle without an explicit target and confirmation. This skill does not perform deletion automatically.

## Resource map

- `references/assessment-rubric.md`: four IELTS dimensions, evidence, issue labels, and comparison rules.
- `references/lesson-design.md`: complete-paper timing, question progression, clarity rules, and marking behavior.
- `references/workflow-and-mastery.md`: cycle states, scheduling, assistance, retention, and transfer evidence.
- `references/state-schema.md`: local files, JSON fields, atomicity, privacy, and CycleBundle.
- `references/exercise-contracts.md`: supported `skill_id` values, exercise types, plan and response contracts.

## Be honest about local-mode limits

- Record timing but do not claim to enforce a locked 40-minute editor.
- A fresh task reduces answer leakage but cannot technically prevent the user from opening old feedback.
- Without an automation tool, surface due work only when the skill is invoked again.
- Use sequential chat tasks and local reports instead of claiming Web-equivalent drag-and-drop or dashboards.
