---
name: kelly-homework-coach
description: Friendly elementary-school homework tutoring App-in-Skill. Use when the user invokes $kelly-homework-coach or /kelly-homework-coach, mentions 小学生作业辅导, homework photo tutoring, 拍照讲题, 作业答疑, 错题本, error notebook, mistake-book review, practice paper generation, exam paper analysis, parent/teacher review of AI explanations, or wants a child-friendly UI for step-by-step homework help with parent/teacher review and safety boundaries.
metadata:
  category: education
  tags:
    - risk:local-write
    - industry:education
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-homework-coach
    resources:
      - questions
      - mistakes
      - papers
      - reviews
      - settings
    risk: local-write

---

# Kelly Homework Coach

## Overview

Use this skill as a child-friendly homework coaching desk for elementary students. The agent explains photographed or pasted questions, analyzes wrong answers, turns mistakes into a review notebook, and prepares practice papers; the AirApp gives students a warm study surface and gives parents/teachers a calm Busabase-backed review desk for mistake analysis and paper planning.

Default interaction mode: App UI. Unless the user explicitly asks for chat-only handling, ensure Busabase resources are provisioned (the AirApp does this lazily on first run), record any newly explained question/mistake/paper with `scripts/record_homework.mjs`, and give the actual AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says `纯聊天`, `chat only`, `不要打开 UI`, or similar; in that mode use stable references such as `Question #1`, `Mistake #2`, and `Paper #1`.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-homework-coach-app/` artifact. The app renders on the **editorial** visual preset (`references/editorial-visual-system.md`): `app/styles/editorial.css` is a byte-identical copy of the shared asset and the only file allowed to know a colour, a font size, a radius, or a duration, and `scripts/check.mjs` fails the build when a raw one comes back. Default family `sage-clay`, register `desk`.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- Original-image storage is opt-in: ask permission per photo before uploading an attachment to Busabase. Explain that an attachment may have an accessible URL. The browser never uploads photos. Never place private originals in Demo fixtures or public artifacts.
- The skill may inspect uploaded homework photos, run OCR/vision reasoning through the active model, explain questions, identify mistakes, generate practice items, and record the result to this skill's own Busabase Bases via `scripts/record_homework.mjs`. It never calls a school system, uploads a child's photo outside the current chat session without explicit per-photo attachment consent, contacts a teacher, or publishes/exports a paper itself.
- The AirApp reads and writes its own Busabase Bases only; it never mutates an external system. Parent/teacher review decisions (approve / request changes / block) write straight onto the review record through `busabase-sdk`.
- Child-facing output must be encouraging, step-by-step, and age-appropriate. Prefer hints and concepts over blunt answer dumping unless the user asks for the answer.
- Parent/teacher-facing analysis may be more diagnostic, but should avoid shame language. Treat the student as capable and learning.
- Student photos, names, school data, and answers are private education data. Never embed raw photo bytes in a text/JSON field. Default to a short `photo_label`; only link an uploaded `original-image` attachment after explicit per-photo consent. Never commit any local credential file.

## Busabase Resources

Five Bases under one application Folder (`kelly-homework-coach`), declared in `content/kelly-homework-coach-app/app/js/config.js` and the generated template sidecars under `content/`:

- `questions`: one row per homework question the agent has explained (from a photo, pasted text, or a paper) — prompt/answers, outcome, and the child-facing explanation (kid summary, steps, key concept, self check, next hint). Written by `scripts/record_homework.mjs`.
- `mistakes`: one row per mistake-book entry (stable id so repeated review updates the same card) — root cause, misconception, fix strategy, similar practice prompt, parent note.
- `papers`: one row per practice paper plan or completed-paper analysis — focus topics, linked mistakes, difficulty mix, items, and (once analyzed) wrong-question count/strengths/review plan.
- `reviews`: one row per parent/teacher review item (targets a question, mistake, or paper) — the raw review fields plus the reviewer's decision (`decision-action`/`decision-comment`/`decided-at`) and, once `scripts/execute_decisions.mjs` runs, an execution marker, all written directly onto the same row. A decision also mirrors the resulting status onto the target question/mistake/paper's own row.
- `settings`: sanitized config summary (student profile, subjects, learning policy, practice defaults, export policy — no secrets) plus the two authored aggregate metrics that cannot be recomputed from the current record lists (`mastery_score`, `questions_analyzed` — an all-time history).

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/homework-schema.md` for exact field shapes.

## How A New Question/Mistake/Paper Enters The System

There is no upload API and the AirApp's photo box never uploads a file anywhere — it only lets the student pick a local filename and copies a chat prompt asking the agent to analyze it (`content/kelly-homework-coach-app/app/app.js`'s `renderPhotoBox()`/`data-copy-prompt="photo"`). The agent does the actual work in the same chat session (OCR/vision reasoning, drafting the child-facing explanation, identifying the mistake) and then calls the trusted script below with its own Busabase credentials to record the result:

```bash
node skills/kelly-homework-coach/scripts/record_homework.mjs --file payload.json --apply
```

Without `--apply` this is a dry run that only prints the planned upserts. The payload is a JSON object with optional `questions`/`mistakes`/`papers`/`reviews` arrays (see the script's header comment for the exact shape); each item is upserted by its stable id. Include one useful `reviews` entry for a new question or paper. A factual mistake card accompanying the same question should be covered by the question confirmation, not a duplicate confirmation. For a mistake-only update, preserve existing review decisions; never create an unnecessary second review. Include a `reviews` entry alongside a standalone judgement requiring review so a parent/teacher can approve it in the app — the script itself never sets a review's decision fields (`decision-action`/`decision-comment`/`decided-at`/`execution-*`), even if a payload happens to include them; a freshly recorded review always starts `needs_review`, and re-syncing an existing review preserves whatever decision a human already made.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-homework-coach-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/student`: student study desk with a photo/intake box (local-only filename picker plus a copy-to-chat prompt), current question, gentle step-by-step explanation, hint ladder, and "I understand" / "I still need help" controls.
- `#/student/<question_id>`: question detail with the original prompt text, the student's answer, concept explanation, steps, self-check, and next hint.
- `#/mistakes`: mistake notebook with due-review chips, topic filters, root-cause analysis, similar practice prompt, and review history.
- `#/papers`: practice paper list, including mistake-focused settings, estimated minutes, and paper analysis (wrong-question count, strengths, review plan). A paper whose `items` carry an answer key can be **sat** here — see Practice Runner below.
- `#/review`: parent/teacher review queue with stable refs, workflow states (`needs_review` / `changes_requested` / `approved` / `done` / `blocked`), an editable review note, suggested actions, and approve/request-changes/block decisions — written directly onto the review record through `busabase-sdk`.
- `#/settings`: sanitized config summary, data provider, learning policy, answer-reveal rule, language, and a **Style** tab that switches the editorial colour family on `<html data-theme>`. Never exposes a secret value.

## Demo Mode

- `?demo=student`, `?demo=mistakes`, `?demo=papers`, and `?demo=review` open the deterministic offline dataset for screenshots, review, and demo recordings (the scenario only selects which route to demo — the underlying data is always the same `demoSnapshot()`). Demo mode never reads or writes Busabase.
- **Demo decisions really apply, in memory.** Approve / request changes / block mutate the rendered snapshot through the same `statusForAction()` the Busabase provider calls, mirror the new status onto the target question/mistake/paper, and play one confirmation highlight — then a refresh restores the fixture. Nothing is persisted and nothing leaves the tab.
- The demo dataset contains a record that must **not** be approved: `q-area-blurred` / `rv-area-blurred`, where the photo hides one side length, the agent assumed `8 cm`, and its own read confidence is `0.41`. It exists so the review surface can be demonstrated making a judgement rather than rubber-stamping.
- `lang=en`, `lang=zh`, or `lang=zh-CN` forces UI chrome language. Chinese is **Simplified, mainland wording** (四年级 / 错题本 / 练习卷); `resolveLanguage()` routes every `zh-*` tag to that one bundle.
- Deep links such as `/?demo=student&lang=zh-CN#/student` must work.

## Homework Photo Workflow

1. Ingest the student's photo or pasted problem text. If using vision/OCR, keep extracted text local unless the user explicitly approves a connector; use a short `photo_label` by default (e.g. "Homework photo, page 18 question 6"). An `original-image` attachment may be uploaded and linked only with explicit per-photo consent.
2. Identify subject, grade, topic, required answer type, and whether the student's current answer is correct, wrong, or uncertain.
3. Draft a child-facing explanation: one friendly summary, 2-5 short steps, one key concept, one self-check, and a next hint. Avoid long lectures.
4. If wrong, create or update a mistake item with root cause, misconception, fix strategy, similar practice prompt, and a next review date.
5. Call `node scripts/record_homework.mjs --file payload.json --apply` with the question (and mistake, if any) plus a matching `reviews` entry, then send the user to `#/student` or `#/review`.

## Mistake Notebook Workflow

1. Group mistakes by topic, error type, and review due date; keep stable ids so repeated analysis updates the same mistake instead of duplicating it.
2. Use supportive language: "还差一步" / "try this check" rather than "careless" unless the evidence specifically supports a careless-slip label.
3. For each mistake, store a "how to fix next time" rule and a similar practice prompt. Do not store excessive raw photo content.
4. When a review's decision is `request_changes`, the linked review row's status stays `changes_requested`, which is exactly the retired app's "queued agent task" (see `pendingAgentTasks()` in `content/kelly-homework-coach-app/app/js/homework-model.js`). Redraft the explanation, mistake card, or paper plan, then re-run `scripts/record_homework.mjs` with the updated content and the same review id.

## Practice Paper And Analysis Workflow

1. Build practice papers from target subject/topic, grade, difficulty mix, and recent mistakes.
2. Generate a paper plan first: title, question count, estimated minutes, topics, linked mistakes, and answer-key policy. Parent/teacher approval is required before export.
3. Write each item as `{ prompt, answer, hint, topic }` so the student can sit the paper in the app. `items` has always been a free JSON array, so this is not a schema change — a plain string still parses, it just cannot be marked. An item that genuinely has no single right answer (「说说这篇短文的中心意思」) carries `answer: ""` and is reported for a person to read rather than auto-marked.
4. After a completed paper is analyzed, list all wrong questions with topic, root cause, concept gap, and recommended review sequence.
5. Export approved papers locally only, outside this app, after review. This skill never sends anything to school systems or messaging apps.

## Practice Runner

A paper with an answer key can be sat in the app: `#/papers/<paper_id>` → **开始做这张卷**. One question at a time, answer, mark, next.

- **Marking is local and deterministic.** `gradeAnswer()` in `homework-model.js` normalizes full-width digits, whitespace, a trailing period and case, then compares exactly. No model call and no fuzzy match — a child is told they got it wrong, so the rule has to be one you can explain to them.
- **`hint_first` is enforced here, not just documented.** The first wrong answer gets the item's `hint`; only a second wrong attempt reveals `answer`. When `learning_policy.answer_policy` is not `hint_first`, the answer shows immediately. A hint must never contain its own answer — `test/homework-model.test.mjs` asserts this across the whole demo dataset.
- **The score is over marked items, based on the final answers; first answers and retry history are separately stored and must not be mistaken for independent mastery.** `attempt.graded`, not `attempt.total`: an open-response item nobody marked is not a question the child got wrong.
- **Handing in proposes one row update.** The attempt goes onto the paper's **own** record (`analysis.attempt`, plus `analysis.wrong_count`), and `analysis.attempts` preserves history. One pending request is returned; the old paper review is not reset or reused as an approval of new results. After a reviewed merge, the parent sees each answer and retry in the old paper review detail but makes a **separate, attempt-scoped result decision** on the paper analysis. Open responses need one manual mark each and a parent note; the decision creates another pending CR and does not reuse the old paper approval or unlock practice. `papers` is already defined as holding "a completed-paper analysis", so this is an update through the existing `records.changeRequest` path — no new Base, no create procedure, and no widening of what the AirApp may write.
- **The runner never writes a mistake card.** Turning a wrong answer into a root cause and a misconception is a judgement about a child's learning; the agent drafts those (`scripts/record_homework.mjs`) and a parent approves them. The runner reports only what it can prove: which items were wrong, what was given, what was expected, and how many hints were used.

So the loop is: agent builds the paper → student sits it → app marks and hands in (pending CR) → reviewer merges that factual attempt → parent judges open responses in `#/review` (separate pending CR) → reviewer merges that result decision → agent may separately draft missed-item mistake cards for approval.

## Review And Execution Loop

1. Send parent/teacher users to `#/review`. Decisions write straight onto the review record through `busabase-sdk` (`records.changeRequest`), with `autoMerge: false` in both local and deployed runtimes. Record ingestion also proposes pending requests and returns their IDs; a reviewed merge is separate from confirming the learning content. Approving or blocking also mirrors the resulting status onto the linked question/mistake/paper's own row.
2. Before executing anything, run `node scripts/execute_decisions.mjs` for a dry run. With `--apply`, it re-reads every decided review and writes an execution marker (`execution-status`, `execution-detail`, `executed-at`) onto it, reporting the local-only operation (`add_to_mistake_book`, `mark_understood`, `queue_practice_paper`, `export_paper_plan`, `request_revision`, `block_item`) the agent should perform next, and for approve/block also sets the review's final status (`done`/`blocked`). It performs no export, filing, or external transmission.

## Safety Defaults

- Never shame the child. Avoid labels like "lazy", "stupid", or "careless" unless reframed as a fixable pattern with evidence.
- Never present uncertain OCR/vision as certain. If the photo is blurry, ask for a clearer image or parent/teacher confirmation.
- Do not generate high-stakes claims such as diagnoses, school placement decisions, or formal grades.
- Do not reveal a full answer before offering a hint path when the configured answer policy is `hint_first`.
- `scripts/execute_decisions.mjs` never invents a new automated action beyond what a review's own `proposed_action` already reports, and `scripts/record_homework.mjs` never sets a review's decision fields itself — a parent/teacher must always decide through the app.

## Useful Commands

```bash
node skills/kelly-homework-coach/scripts/record_homework.mjs --file payload.json --apply
node skills/kelly-homework-coach/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-homework-coach/content/kelly-homework-coach-app dev
```

## Corrected learning workflow and current limits

- Child feedback ("I understand" / "need a hint") is local feedback, not a parent approval or proof of mastery. It can be copied to chat; it is not automatically persisted.
- A wrong choice proves an incorrect answer, not a cause. Without a student's working, use "cause not yet verified"; parent impressions remain observations. Do not block factual ingestion on an unknown cause. Update stable cards rather than creating duplicates.
- Mistake details allow cause supplementation on the existing record. Preserve other analysis fields, status and latest head. All saves are pending requests. UI status follows at most five request IDs in the current tab's session storage; older/cross-device requests are not automatically discovered. Do not ask children to manage CR IDs.
- "Copy a paper request" is only a chat handoff. It reads the linked latest question, includes its text and stable Space/Base/question/mistake/attachment references, and does not copy private image URLs, send a message or generate a paper. The agent must inspect actual attachments; if viewing fails, say so. A mathematically verified diagram based on human-confirmed conditions is a separate alternative, not evidence that the original was viewed.
- Each geometry exercise needs a corresponding usable diagram. Items may include `diagram: {points: {A:[x,y], B:[x,y], C:[x,y], D:[x,y], E:[x,y], G:[x,y], H:[x,y], Q:[x,y]}, note}` for the rectangle-fold scenario. This is a limited structured renderer, not arbitrary SVG support. Add `explanation` per item and `parent_answer` for open responses.
- Merge the paper ingestion and its single review record to make it appear in Papers. Parent confirmation must become canonical before practice starts. Draft/blocked papers cannot be started. Code changes required by a new item format must be merged and Run first.
- Papers is the child-facing view: no parent deep notes or answer keys are rendered there. The parent review shows each diagram, answer and reasoning with "Confirm this practice paper". This is UI separation, **not authorization isolation**: the browser receives the answer-key payload and all routes remain accessible.
- Practice is one item at a time. Open responses use a textarea and need manual judgement. First wrong objective response gets a hint when configured; success or a later failure reveals item reasoning. Keep first responses, retries and hint use. Unsubmitted runs do not survive refresh; grading is exact normalized text, not semantic equivalence.
- New attempts do not automatically update mistake mastery or create mistake cards. There is no automatic multi-mistake worksheet builder or AI call in the browser. Result review records manual marks and parent note on the same paper after an independent reviewed merge; it does not automatically change mastery, create mistakes, or authorize a new sitting.
- `record_homework.mjs --apply` submits pending CRs only. `execute_decisions.mjs --apply` remains a separate privileged execution operation that may merge its marker writes; run it only with explicit authority after verifying the business decision.
