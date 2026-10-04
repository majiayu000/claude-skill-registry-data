---
name: get-started
description: Use when the user is new to Job Hunt Skills and wants to see what it does or set up their workspace — including "I'm new to Job Hunt Skills", "help me get started", "set me up", "first time using this", "here's my resume, tailor it for this job", "can you look at my resume", pasting a resume and a job posting together, or invoking /get-started. Also use when `my-documents/` has not been scaffolded yet. Once the user has existing source documents and is just iterating, prefer `resume-builder` or `resume-tailor` directly.
---

The onboarding wrapper for Job Hunt Skills. A first-time user should reach real value fast, then be invited into the deeper build — not marched through a 20-minute interview before seeing anything. This skill offers two doors: a **fast path** (paste a resume + a posting, get a tailored draft and honest audit in minutes) and the **deep build** (`resume-builder`'s full source-document interview). Lead with the fast path; the deep build is where the compounding value lives, offered once the user has felt the first win.

## Choosing the door

After orientation (step 1), route on what the user has:

- **Has an existing resume/CV or LinkedIn profile** → fast path (step 2). This is the default; most first-timers arrive with a resume.
- **Pasted a resume and a job posting already** → go straight into the fast path with that material.
- **No resume yet, or explicitly wants to build the source document properly** → deep build (step 4).

The fast path runs **in-chat first** and only touches disk once the user asks to save — so the workspace preflight (step 3) happens at save time, not before the user has seen anything. The deep build confirms the workspace up front because its whole output is files.

## Workflow

### 1. Orient the user — BEFORE any questions, forms, or input gathering

Give a short orientation in plain language **before** asking for any information. You're talking to a jobseeker, not a developer. Keep it to two or three sentences, then offer the fast path. Do not open with the long interview.

This step is load-bearing: hand over a long input form first and explain afterwards, and the form is already filled by the time the user knows what is happening or that fields can be skipped. Orientation MUST land first, and the user MUST choose a door before any structured prompt — single question, multi-field form, or batched interview — appears.

Convey, briefly:

- Job Hunt Skills helps run a practical, honest job search: tailoring your resume to real roles, honest feedback, company research, and interview prep — all from your own materials.
- The fastest way to see what it does: paste an existing resume (or LinkedIn profile) plus a job posting, and get a tailored draft and a straight-talking audit back in a few minutes.
- Nothing is invented on your behalf; gaps are surfaced, not filled with guesses.

Then ask the routing question in plain language:

> Do you have a resume — or a LinkedIn profile — and a job posting you're interested in? Paste both and I'll show you what this does. Or if you'd rather build your resume properly from scratch first, we can do that instead.

Vocabulary:
- Avoid internal terms in user-facing text: canonical, state layer, drift check, scaffolding, DOCX, PATH, Typst, tier, profile-strength score.
- When describing outputs, say "Word file", "PDF", and "a preview you can open in your browser". Frame extra output capability as an unlock ("installing Node gets you the Word file and PDF automatically"), never as something missing or degraded.

Route on the reply:

- **Has a resume/CV or LinkedIn (with or without a posting yet)** → fast path (step 2). If they have no specific posting, still run the fast path as a condensed audit of the resume alone and note that adding a posting sharpens it.
- **No resume, or wants to build the source document properly** → skip to the workspace confirmation (step 3) and then the deep build (step 4). For the deep build, ask the classic scope question: "Want a resume, a cover letter, or both? A short achievement-focused version or a longer CV-style version with a personal statement?" and whether they have existing material to work from.

Wait for the user's choice before running either path.

### 2. Fast path — show value in-chat, before touching disk

The goal: a first-timer with an existing resume reaches a tailored draft plus an honest audit **without completing the full interview**, in under ten minutes. This runs entirely in conversation; nothing is written to disk until the user asks to save.

**2a. Take the pasted material.** Accept the resume (or LinkedIn text) and the job posting as pasted text or a URL. If a posting URL fails, ask for pasted text. If they have no posting, proceed with the resume alone as an audit.

**2b. Invoke `resume-tailor` in quick mode.** Run `resume-tailor`'s in-chat quick-tailor path (its step 0.5): tailor from the pasted source with limited, paste-based evidence checking, plus a condensed `resume-auditor` pass. No scaffold, no preflight, no file writes yet. Produce, in this order:

1. **A 60-second read-back** — prove you understood the material before doing the slow work: "Here's what I see: eight years in B2B marketing, strongest evidence around lifecycle campaigns; this posting weights analytics experience you have but bury in bullet six." One short paragraph.
2. **Two or three before/after bullet rewrites** — show the transform as a diff, with the reasoning ("the posting leads on X; your original buried it; here's the reframe"), not a wall of finished text.
3. **One honest audit flag** — surface the single most callback-blocking issue, and if a claim isn't supported by the pasted material, flag it plainly. Don't skip it to be nice — an unflagged claim costs the user a wasted application later.

**2c. Close by naming what a saved workspace adds.** End the fast path by naming what a saved workspace and source document would add — this is the invitation into the deep build, per [state-layer §11](../_shared/state-layer.md#11-progress-and-reward):

> This is what it does with zero setup. It gets much stronger once your resume lives here as a source document and you've banked a few stories — the audit could *verify* those claims instead of just flagging them, and every future application starts from this baseline. Want me to save this and build that out now?

- **User wants to save / continue** → run the workspace preflight (step 3), then use the transition below. Do not save the in-chat tailored draft directly.
- **User is done for now** → that's a complete, successful first run. Don't force the save. Leave them with the one-line invitation to come back and `resume-builder` when ready.

**Resume Builder import/update transition.** After the user confirms which pasted resume/CV material should become their baseline, invoke `resume-builder` in a short import/update pass. It must preserve the user's chosen label, resolve any hard claim questions, save `my-documents/resume.md` or `my-documents/cv.md`, and assign or increment its integer `version`. Wait for the user to confirm that versioned source document before invoking `resume-tailor` again. The second tailor pass reads that saved source, reruns claim verification, and only then may save the tailored artifact with `source_document` and `source_version` frontmatter matching the source. The preview remains useful raw material, but it is never provenance.

If the user wants only the baseline saved, stop after `resume-builder`. If they also want the role-specific artifact, continue through `resume-tailor` steps 1–9 against the newly versioned source.

### 3. Confirm the workspace, then scaffold

Many users are not developers and will not know what a "working directory" is. Walk them through where their files will live in plain language, and **do not scaffold until they have confirmed a real folder on their own computer**. This step exists because early testers had Claude generate a resume that was never actually saved anywhere they could find — the file landed in the plugin install folder, invisible on the next session.

Follow the [Workspace Preflight (state-layer §10)](../_shared/state-layer.md#10-workspace-preflight). Concretely:

**3a. Show the current location and ask.**

Resolve the absolute path where files would land and ask plainly:

> Your job-hunt files will live in a folder on your computer. Right now I'd save them under:
>
> `{absolute path of cwd}`
>
> Does that look like the right place — a folder you picked for your job search? If you're not sure, just tell me and I'll help you set one up.

**3b. Handle the response.**

- **"Yes, that's right"** → proceed to 3d.

- **"I want a subfolder under that"** (e.g. they want files inside `{cwd}/job-hunt/` rather than mixed into `{cwd}/`):
  - Confirm the name they want.
  - Warn before creating: "I'll need to create a new folder there. You may see a permission prompt — accept it if you want me to continue."
  - Create the subfolder, then re-confirm the new path before scaffolding.

- **"I haven't picked a folder" / "I don't know what this is" / "That path looks wrong"** → see 3c. Do **not** scaffold a guess.

- **The resolved path looks like the plugin install location** → treat as "haven't picked a folder" and go to 3c.

**3c. Help a novice set up a folder.**

If the user doesn't have a folder yet, give them the platform-specific recovery and stop until they come back:

- **Codex CLI/IDE:** close the current run if necessary, open a terminal or IDE workspace at the folder the user wants, and start Codex from that folder. Example: create `~/Documents/job-hunt`, `cd` into it, then run `codex`; in an IDE, open that folder as the workspace before starting the skill again.
- **Desktop agents with folder controls (Codex in the ChatGPT desktop app, Work mode, or Cowork):** use the app's folder/workspace control to select a folder the user owns, then start a new conversation with that folder available. Use the current product label shown in the app; do not invent a settings-menu path that was not verified.
- **Claude Code:** exit Claude Code, `cd` into the chosen folder, then run `claude` again.

Do not try to "just save it somewhere reasonable" — that is the bug. Wait for the user to fix the folder, then restart cleanly.

**3d. Scaffold, with fallback, then verify.**

Once a real workspace folder is confirmed, build the structure under that folder. Two paths, same on-disk result:

- **Preferred:** run `node "{job_hunt_skills_root}/scripts/scaffold-state.mjs"`. The script is idempotent and creates only missing files. If it exits non-zero with the "working directory is the plugin install dir" message, surface that message verbatim and go back to 3c.
- **Fallback** (Node not installed, no shell access, command-not-found, or any other non-zero exit *except* the workspace-binding refusal): scaffold manually with native file tools per [state-layer §10 step 5](../_shared/state-layer.md#10-workspace-preflight). Cowork users are typically not developers; do not require them to install Node, and do not skip the scaffold because the script failed.

**Verify before continuing.** List the workspace folder and confirm all of these exist:

- Directories: `my-documents/`, `my-documents/applications/`, `my-documents/reports/`, `my-documents/proof-assets/`
- Files: `my-documents/applications.md`, `my-documents/story-bank.md`

If anything is missing, create it. Every downstream skill assumes this structure is in place; a half-scaffolded workspace is how a generated resume ends up stranded in chat. Verification is the gate, not the script's exit code.

On success, briefly recap: "Your files will live under `{absolute path}`, and I've set up the folders for resumes, applications, reports, and proof assets." One sentence, then move on to building.

**Vocabulary for this step:** "folder" not "directory", "your computer" not "filesystem", show the actual path (not a placeholder) so the user can read it.

### 4. Build the source documents

Invoke `resume-builder` and run its workflow end-to-end: gather existing materials, run the structured interview, generate outputs with claim checks, save, and export the Word file, PDF, and browser preview.

If the user signaled scope, pass it through so `resume-builder` can route to the right mode. If they arrived here from the fast path, feed the in-chat preview and original pasted material into the short import/update transition as raw material so the build starts warm without treating the preview as saved provenance.

### 5. Seed the story bank

After saving the source document(s), offer to capture the richest 2-3 accomplishments as STAR+R stubs in `my-documents/story-bank.md`. Do not assume. If they decline, move on.

If they accept, append each story using the canonical H2 + YAML + Situation / Task / Action / Result / Reflection schema from [state-layer section 7](../_shared/state-layer.md#7-story-bank-schema). Mark gaps with `[ASK: ...]` placeholders rather than inventing specifics.

### 6. Close the run

End with a short recap:

- Files created, with paths.
- Reminder that these source documents are what later skills read.

Then the two closing beats from [state-layer §11](../_shared/state-layer.md#11-progress-and-reward):

- **What this unlocked** — name the new capability in plain terms, e.g. "Your resume now lives here as a source document, so tailoring to a role, honest audits, and interview prep all draw from it — and the stories you banked will back up claims automatically."
- **Where things stand** — show the profile-strength line (`node "{job_hunt_skills_root}/scripts/profile-strength.mjs"`, or derive it natively) so the user sees their progress and the single best next step. Frame the next step as the natural continuation, not a chore.

Then point to the best next action:

- "Want honest feedback on what we just built? Use `resume-auditor`."
- "Found a specific role? Use `company-research` first, then `resume-tailor`."

## When not to use this skill

If the user already has `my-documents/resume.md` or `my-documents/cv.md` and is asking for an update, tweak, or rebuild, invoke `resume-builder` directly. If they already have a source document and just want to tailor to a posting, use `resume-tailor` directly.
