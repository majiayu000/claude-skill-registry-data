---
name: formloop
description: Create Typeform-quality forms on-the-fly to ask a human structured questions, then resume execution when the form is submitted. Supports rich blocks (HTML mockup grids, drag-and-drop ranks, sliders with live previews) that chat and AskUserQuestion can't render. Use when you need 4+ structured inputs from a human in the loop, or when the choice is visual (designs, mockups, layouts).
triggers:
  - formloop
  - rich form
  - mockup picker
  - drag and drop ranking
  - slider with preview
  - multi-respondent form
  - team audit form
  - panel survey
---

# Skill formloop

**formloop** lets you generate a Typeform-quality form on-the-fly, ask a human structured questions, and resume execution when the form is submitted. The missing layer when `AskUserQuestion` saturates and chat is the wrong UI.

100% local. Server runs on `127.0.0.1:3847`. No accounts, no cloud, no telemetry.

## When to use formloop (vs alternatives)

| Situation | Use |
|---|---|
| 1-3 questions, 2-4 textual options, 1 respondent | Built-in `AskUserQuestion` |
| 4+ questions, 1 respondent | formloop ephemeral (`persistent: false`) |
| 4+ questions, multiple respondents (team, panel, audit) | formloop persistent + `list` |
| Visual choice — mockups, layouts, palettes | formloop `html-pick` |
| Rank by preference | formloop `rank` (drag-and-drop) |
| Numeric value with live visual preview | formloop `scale-preview` |
| Respondent fills from their phone | formloop (mobile-first) |

## Bootstrap (once per session)

Check that the server is up, otherwise start it. `npx formloop` boots a Next.js server on `127.0.0.1:3847` and auto-builds on first run.

```bash
# Verify
curl -s -m 2 http://127.0.0.1:3847/ -o /dev/null && echo "up" || echo "down"

# Start (one-line, no deps to install — the bin does it)
npx formloop
```

In Claude Code: run `npx formloop` via `Bash run_in_background: true`, then poll for readiness with `until curl -s -m 2 http://127.0.0.1:3847/ -o /dev/null; do sleep 1; done`.

## Ephemeral mode (1 respondent, urgent decision)

```bash
# 1. Create the form (auto-opens in browser unless --no-open)
npx formloop create --spec '{
  "title": "Hero design direction",
  "blocks": [
    {"kind": "html-pick", "id": "design", "title": "Which direction?",
     "options": [
       {"id": "a", "label": "Minimal", "html": "<div style=\"...\">Mockup A</div>"},
       {"id": "b", "label": "Bold",    "html": "<div style=\"...\">Mockup B</div>"}
     ]},
    {"kind": "textarea", "id": "notes", "title": "Any notes?", "required": false}
  ]
}'

# 2. Wait for submission (run in background so the conversation auto-resumes)
npx formloop wait --form-id <ID> --timeout 1800
```

Output of `wait`:
```json
{
  "form_id": "ABC123",
  "answers": {
    "Which direction?": "b",
    "Any notes?": "Looks great"
  },
  "submitted_at": "2026-05-26T15:00:00.000Z"
}
```

## Persistent mode (N respondents — audit, panel, survey)

```bash
npx formloop create --spec '{
  "title": "SAV rules audit — Batch 1",
  "persistent": true,
  "respondentField": {
    "type": "email-name",
    "required": true,
    "intro": "Your first name and email, so we can compare answers across reviewers"
  },
  "blocks": [
    {"kind": "html",
     "html": "<h2>Why this form?</h2><p>We audit ~80 SAV rules to identify critical / secondary / drop. Your input compared to others shows where we agree and where we don'\''t.</p>"},
    {"kind": "html",
     "html": "<div style=\"padding:16px;background:#f4f4f8;border-radius:8px\"><strong>Rule 1 — Dates</strong><br><br>NEVER give a past date as future date.<br>❌ \"shipping 21/04\" when we'\''re 25/04<br>✅ \"shipping within 2-3 business days\"</div>"},
    {"kind": "mc", "id": "rule1_decision", "title": "Rule 1 — Action?",
     "options": ["Keep as-is", "Amend", "Drop"]},
    {"kind": "textarea", "id": "rule1_comment", "title": "Rule 1 — Notes",
     "required": false},
    {"kind": "mc", "id": "rule1_importance", "title": "Rule 1 — Importance",
     "options": ["Critical", "Important", "Secondary", "Not sure"]}
  ]
}'
```

Then:

```bash
# Share the same URL with N respondents (email/Slack/etc).
# List all submissions at any time:
npx formloop list --form-id ABC123

# Or block until N submissions are in:
# (not yet in the bin — use the Python SDK: ask_form.py wait-n)
```

## Block types

| `kind` | Purpose | Required fields | Optional |
|---|---|---|---|
| `html` | Context / mockup / separator — not a question | `html` | — |
| `text` | Short text (1 line) | `id`, `title` | `placeholder`, `required` |
| `textarea` | Long text | `id`, `title` | `placeholder`, `required` |
| `mc` | Single choice (radio) | `id`, `title`, `options[]` | `description`, `required` |
| `multi` | Multi choice (checkboxes) | `id`, `title`, `options[]` | idem |
| `yn` | Yes/No | `id`, `title` | `labels: {yes, no}`, `required` |
| `number` | Integer or decimal | `id`, `title` | `min`, `max`, `required` |
| `scale` | 1-N numbered scale | `id`, `title`, `min`, `max` | `minLabel`, `maxLabel`, `required` |
| **`html-pick`** | **Clickable HTML mockup grid** | `id`, `title`, `options: {id, html, label?}[]` | `multi`, `required` |
| **`rank`** | **Drag-and-drop ordering** | `id`, `title`, `options[]` | `required` |
| **`scale-preview`** | **Slider with live HTML preview** (placeholders `{{value}}` and `{{percent}}`) | `id`, `title`, `min`, `max`, `previewHtml` | `minLabel`, `maxLabel`, `required` |

All embedded HTML is sanitized via DOMPurify server-side. `<script>`, event handlers, and iframes are stripped. SVG is allowed (charts, illustrations).

## `respondentField` — capture identity (persistent only)

```json
"respondentField": {
  "type": "email-name",
  "required": true,
  "intro": "Your first name and email"
}
```

Effect: Formloop renders 2 fields (first name + email) at the very start of the form. Each submission then includes `respondent: {name, email}` alongside `answers`.

## Best practices

**For multi-respondent (audit, panel):**
- `persistent: true` is mandatory — otherwise only the first respondent counts.
- `respondentField: email-name` unless you really want anonymous.
- Keep under 30 blocks. Beyond, drop-off explodes. Split big audits across thematic forms.
- Frame each item to audit with an `html` block that renders the item verbatim (title + ✅/❌ + real example) before the decision questions. Respondents shouldn't need to scroll a .md side-by-side.
- For diffusion: email/Slack with a clear intro — why this form, estimated time, how results are used.

**For ephemeral (1 decision):**
- Cap at 6-8 blocks.
- Prefer `html-pick` over `mc` when the choice is visual.
- Use `html` blocks as intros, not `description`, when you want rich HTML.

**For both:**
- Explicit titles: "Hero design direction" beats "A few questions".
- `required: false` on free-form `textarea` comments.
- Test the form URL yourself before sending it.

## Limitations

- No conditional logic (skip-if/else). All questions are seen by all respondents.
- No mid-form computation. Aggregate after submission.
- HTML sanitization is strict. Use `scale-preview` for interactivity.
- Spec TTL 24h, ephemeral response TTL 1h. Restart of the local server wipes everything (in-memory store).
- No push notifications to respondents — sending email/Slack is on the caller.
- 1 form = 1 spec. To iterate, create a new form (the old one stays accessible).

## Self-hosting

By default, `npx formloop` runs entirely on `127.0.0.1:3847` with an in-memory store. If you want persistence across restarts, set `KV_REST_API_URL` + `KV_REST_API_TOKEN` to point at an Upstash Redis (or any Upstash-compatible KV).

To require API auth (multi-user shared server), set `WEBHOOK_SECRET=<long-random-string>` and pass it as the `x-webhook-secret` header on every `/api/forms*` call.
