---
name: handoff
description: "Create a handoff document for the current animath session. Invoke at the end of a conversation when the user or an agent asks to wrap up / hand off the session (e.g. /handoff) — do not auto-invoke spontaneously."
---

# Handoff Document Generator

Create a handoff document for the current session. ONLY write the document — do NOT
fix, investigate, or run any code (except `npm run build` for build status).

## Steps

1. Resolve the **branch slug**: `git branch --show-current`, strip a leading
   `claude/`, replace `/` with `-` (e.g. `claude/menu-bar` → `menu-bar`).
2. Find the current session's progress report in
   `docs/sessions/progress/<branch-slug>/` (most recent by filename).
3. Read the progress report to understand what happened this session.
4. Run `npm run build` to get current build status (`tsc && vite build` — the only
   CI check), unless it was already run recently in this session. Note the result
   (pass / fail + first error).
5. Write the handoff to `docs/sessions/handoff/<branch-slug>/` with the **same
   filename** as the progress report (create the folder if needed). Declare
   `signals:` and `next:` (required — see Document Structure).
6. Run `npm run sessions:lint -- docs/sessions/handoff/<branch-slug>/<file>.md` (or
   the whole corpus) and fix any **errors** it reports on your files — this is the
   contract the control center scrapes; CI runs `--strict`.
7. Regenerate the cross-branch control center: run `npm run sessions`
   (`docs/sessions/build-sessions.mjs` — converts every branch's reports to
   Markdown, renders the rich HTML, and rebuilds `control-center.html`).

## Path & Filename Convention

Session logs are committed and partitioned per branch:
`docs/sessions/handoff/<branch-slug>/YYYY-MM-DD-SNN-description.md` — the filename
must match the progress report exactly (including the `.md` extension), and the
`<branch-slug>` folder must match the one the progress report lives in.

## Document Structure

Copy `docs/sessions/_template-handoff.md` and fill in the `[bracketed]` parts. It is
**Markdown + YAML frontmatter** (full spec: `docs/sessions/REPORT_STYLE.md`). The
frontmatter carries **status / branch / pr / build** (keep it accurate — the control
center indexes it). Always includes: **Summary**; **What changed** (or "What we
found" / "The problem"); **Key files**; **Open / not done**; **Context**;
**Self-reflection**.

**Required at every handoff:** declare the **dashboard signals** in the frontmatter —
`signals:` (closed vocab: `needs-dan` / `phone-needed` / `visual-unverified` /
`not-live`; write `null` if genuinely none) and `next:` (one line, the single most
useful next action). These feed the control center's "Start here" digest, so they are
not optional — write `signals: null` rather than omitting it, and declare only what's
genuinely true. Then **consult `docs/sessions/TODO.md` and append any carry-over work
to it** — the durable backlog — each item with a `[category]`, a `!priority`, and a
note that will inform the next round (see that file's header for the format, and
`REPORT_STYLE.md` §1.2). For shelved/abandoned work, set `status: stopped` (a frozen
record exempt from the lint contract) rather than leaving it `in-progress`.

> [!NOTE]
> `npm run sessions:lint` validates this contract (signals/app tokens, status/kind/
> build enums, the Self-reflection Follow-up line). Run it before finishing; a clean
> `--strict` pass is the bar the control center relies on.

- **Key files** in a Markdown table. Make each `file:line` a real link pinned to the
  commit `<SHA>` so it doesn't rot:
  `[\`path:line\`](https://github.com/piyarsquare/animath/blob/<SHA>/<path>#L<line>)`.
- **Callouts** use GitHub alerts for the one thing the next agent must know:
  `> [!CAUTION]` (gotcha) / `> [!IMPORTANT]` (decision) / `> [!WARNING]` / `> [!NOTE]`.
- Sections are `##` headings; the rendered view builds the TOC, anchors, and
  scroll-spy automatically.

Append the **Self-Reflection Protocol** (`.claude/prompts/self-reflection.md`) verbatim
as the final `## Self-reflection` section (it's already Markdown). Keep the heading and
the closing `**Follow-up value:** <LEVEL> — …` line exact — the control center's
**Reflections** view scrapes them for its exit-interview digest.

## Rules

- Distill, don't copy — the handoff should be shorter and more focused than the
  progress report.
- Write for the next agent who has zero memory of this session.
- Include specific file paths with line numbers for key code locations
  (`src/...tsx:line`).
- Include concrete data (numbers, timings, build result) not vague descriptions.
- If the session was investigation/design only with no code changes, say so
  explicitly at the top.
