---
name: kelly-writer
description: Repurpose source content into channel-ready drafts with a Busabase App-in-Skill review and export workflow. Use when the user asks to write content, make a content pack, turn a main blog/long article/transcript/notes into Xiaohongshu, WeChat, newsletter, LinkedIn, X/Twitter, short video scripts, SEO snippets, or a multi-platform publishing plan; also use when they ask for a content approval dashboard or App-in-Skill content workflow.
metadata:
  category: marketing
  tags:
    - risk:gated-write
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-writer
    resources:
      - drafts
      - settings
    risk: gated-write

---

# Kelly Writer

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Writer overview"></td>
    <td width="50%"><img src="assets/screenshots/distribution.webp" alt="Kelly Writer distribution review"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Channel breakdown and the drafts that need attention next.</td>
    <td><strong>Drafts</strong><br>Channel-ready draft review queue with editable title/body, review notes, and approval controls.</td>
  </tr>
</table>

## Overview

Kelly Writer is a Busabase Cloud App-in-Skill. Its canonical product surface
is the AirApp in Busabase, not a separate local-data product. The same Hono
source supports an explicitly requested local preview with OAuth connection
bootstrap. Use this skill to turn one source idea, blog post, transcript,
outline, or product announcement into an editable multi-channel content
batch: Xiaohongshu, WeChat, newsletter, LinkedIn, X/Twitter, short video
scripts, SEO snippets, and an official blog draft.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, generate drafts straight into Busabase and give the user the
clickable AirApp URL. Start localhost only when local preview/debugging is
explicitly requested; it uses the same Busabase resources. Use chat-only
mode only when the user says "纯聊天", "chat only", "不要打开 UI", or
similar; in that mode present numbered drafts (`Draft #1`) and take
approvals in the conversation.

This skill is an implementation of the **App-in-Skill** pattern — a
Codex/agent skill paired with a small companion UI for review and approval.
See the spec paper: <https://mr-kelly.github.io/research/app-in-skill-specification-for-pairing-agent-skills-with-a-local-companion-ui.pdf>.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-writer-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## Boundary

- The skill may extract the source's core idea, proof points, and examples,
  draft channel-specific variants, and write it all to Busabase.
- The AirApp reads and writes Busabase records only. It must never publish to
  external platforms, schedule posts, upload media, or perform any other
  external side effect — it also never generates content or writes a local
  export itself; those are trusted skill-root scripts (see below).
- Exporting is always approval-required. `scripts/export_decisions.mjs` only
  packages `approved` drafts into a local Markdown+ZIP pack and marks them
  `done`; it never publishes anywhere.
- Treat source material and drafts as the user's content. Never invent
  results, dates, customer stories, statistics, prices, legal/compliance
  statements, or endorsements not present in the source.

## Busabase Resources

Two Bases under one application Folder (`kelly-writer`), declared in
`content/kelly-writer-app/app/js/config.js` and the generated template sidecars under `content/`:

- `drafts`: the review queue — one record per channel draft (title, body,
  hook, cta, hashtags, title options, media brief, source notes, risk,
  canonical idea, source summary, `source-draft-path` for local image
  packaging at export time), workflow `status`, and the human verdict fields
  `decision-note` / `decided-at`.
- `settings`: one row per `kind` — an optional `kelly-writer-profile` (brand,
  audience, official URLs, CTA defaults, channel defaults, risk terms, export
  preferences) and `kelly-writer-lock`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space. Metrics and the channel breakdown are
computed client-side from the `drafts` Base on every read — they are never
stored.

The topic-discovery / todo-queue / canonical-main-draft ideation stages from
this skill's pre-Busabase local-file shape were already local-only and
ephemeral (client-derived, never persisted) even in that shape's own
Busabase provider notes; this Busabase-only shape keeps only the durable
unit of work — the per-channel draft record — as the review queue.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-writer-app dev` only when local preview/debugging is explicitly
requested.

Required app views (hash routes):

- `#/overview`: metrics (needs review / approved / done / blocked), the
  channel breakdown, and the top drafts still needing review.
- `#/drafts`: the review queue over channel drafts in workflow states
  `needs_review`, `to_approve`, `changes_requested`, `approved`, `done`,
  `blocked`. Each item shows a stable ref (`#3`), channel/format/status
  badges, an editable title and body, hashtags/CTA/media brief/title-options
  support panels, a `Review note` textarea, and Approve / Request changes /
  Block buttons that write the verdict directly onto the draft record.
- `#/settings`: sanitized config summary — brand/audience/tone, configured
  channels, onboarding state, and the exact `node scripts/generate_batch.mjs`
  / `node scripts/export_decisions.mjs` commands to run next. Never expose
  secret values.

Demo mode:

- `?demo=1` (or `?demo=overview`) opens a deterministic mock content batch
  ("A practical launch guide for a local-first AI workflow") for
  documentation and screenshots.
- `?demo=drafts` and `?demo=settings` select named mock scenes.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase.

UI language: support English and Chinese chrome with `Auto` default. Keep
titles, hooks, bodies, and hashtags in their original language.

## Review Workflow

A human verdict (`approve` / `request_changes` / `block` / `revise`) writes
the new `status` plus `decision-note` / `decided-at` (and, for `approve` or
`revise`, the edited `title` / `body`) directly onto the draft record
through `busabase-sdk`. From a standalone local preview the write merges
immediately (trusted operator); from the deployed AirApp it creates a
pending ChangeRequest for the trusted process to merge.

## Scripts

Both scripts are trusted, skill-root Node processes with their own
`package.json` (`busabase-sdk` dependency) — the AirApp browser never runs
them and never calls `bases.createChangeRequest`/writes a local file itself.

- `node scripts/generate_batch.mjs --source <path-or-text> [--channels official_blog,xiaohongshu,wechat,newsletter,linkedin,x] [--audience "..."] [--cta "..."] [--source-draft-path <path>] [--apply]`
  Reads a source (a file path or inline text), derives deterministic
  per-channel draft heuristics (first-pass only — Codex should improve each
  draft with judgment afterward, either by editing the record's `title`/
  `body` or via a decision on the same record), and writes one new `drafts`
  record per channel to Busabase. Without `--apply` this is a dry run that
  only prints the drafts it would create.
- `node scripts/export_decisions.mjs [--apply] [--out <dir>]`
  Re-reads Busabase for drafts with `status: "approved"`, packages each as a
  Markdown file (title/channel/format/review note/body/CTA/hashtags/media
  brief) plus a ZIP archive (Markdown + any locally-referenced images next
  to the original source, resolved via `source-draft-path` and
  `KELLY_WRITER_CONTENT_ROOT`) under `exports/<batch-id>/` at the skill
  root, then marks each exported draft `done`. Without `--apply` this is a
  dry run that only prints what would be exported.

## Normal Workflow

1. Detect mode. Default to App UI.
2. Clarify or infer the source, target audience, desired channels, language,
   and CTA.
3. Run `node scripts/generate_batch.mjs --source ... --apply` to write a
   fresh batch of channel drafts to Busabase, then improve each draft's
   `title`/`body` with judgment (the generator's heuristics are a first
   pass) before handing the batch to the user.
4. Give the user the AirApp URL (or local preview URL) to review, edit, and
   approve drafts.
5. For a draft moved to `changes_requested`, re-draft it per the review
   comment and write it back to `needs_review`.
6. On "export approved drafts": run `node scripts/export_decisions.mjs
   --apply` to package every approved draft into a channel-ready ZIP pack
   under `exports/` and mark it `done`. This skill never publishes anywhere
   itself — handing the exported pack to a publishing connector is a
   separate, explicitly authorized step.
7. Never export a draft without an explicit `approve` decision, and never
   re-export a draft already `done`.

## Content Generation Rules

- Preserve the source's claims. Do not invent results, dates, customer
  stories, statistics, prices, legal/compliance statements, or endorsements.
- Ask or leave `needs_review`/blocked when the source lacks needed proof,
  product details, screenshots, links, or policy facts.
- Separate platform adaptation from translation: changing channel format is
  allowed; changing the promise is not.
- Prefer concrete hooks, specifics, and reader benefit over generic
  motivational copy.
- Keep CTA and links consistent with the settings profile or the user's
  explicit request.
- For Chinese-language work, support natural Simplified Chinese by default
  unless the source/user asks for another language.
- For Xiaohongshu, produce a scroll-stopping title, short structured body,
  optional image/carousel brief, and hashtag set.
- For long-form derivatives such as newsletter or WeChat, preserve nuance
  and structure; avoid shrinking the idea into slogans.
- For short social posts, make each post independently understandable; do
  not rely on the reader seeing the original blog.

Read `references/channel-playbook.md` when choosing or adapting
channel-specific formats.

## Safety Defaults

- Treat exporting as approval-required; a draft without an explicit
  `approve` decision is never eligible for `scripts/export_decisions.mjs`.
- Store only the minimum content needed for review; keep secrets and
  Busabase credentials out of drafts and logs.
- Keep stable ids (`draft_id`, `ref`, `batch_id`) so repeated updates and
  exports are idempotent.

## Chat-Only Mode

When the user asks to avoid the UI:

1. Produce a compact channel plan.
2. Present numbered drafts with channel, title/hook, body, CTA, and notes.
3. Ask for approval or edits.
4. After approval, run `node scripts/export_decisions.mjs --apply` (or write
   the final approved pack to local Markdown directly) if the user wants
   files.

Never claim content is published unless the user explicitly used a
publishing connector and it succeeded.
