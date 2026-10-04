---
name: eli5-features
description: Generate user-friendly "Explain Like I'm 5" feature documentation for end users by reading the codebase. Use this skill whenever the user wants to document a feature for non-technical users, write help docs, create an explainer for a feature in their app, produce onboarding content, or asks "make a user doc for X". Trigger on phrasings like "ELI5 the closeout flow", "write user docs for the kanban view", "explain this feature to a customer", "make a help article for X", "document this for end users". Also known as "E-features-LI5". This skill produces plain-language docs written for someone with the app open trying to get something done — not internal developer docs (use the `teach` skill for those) and not feature announcements.
license: MIT
---

# E-features-LI5 (eli5-features)

Generate plain-language, end-user feature documentation by reading the code that implements the feature.

## What this skill does (and doesn't)

**Does:** Read the source of a feature, figure out what the feature actually *does for a user*, learn the product's UI terminology from the codebase, and produce a help-doc-shaped markdown file written in friendly plain language with mild personality.

**Does not:**
- Write developer/technical docs (use the `teach` skill).
- Write release notes or marketing announcements.
- Generate fake screenshots — instead, call out where screenshots would help so the user can drop real ones in later.
- Use jargon. No "endpoint," "schema," "API," "actor," "DTO."
- Pretend features do things they don't. If the doc would have to lie, refuse the lie and tell the user what the feature actually does.

## Core principle

**The doc is about the user's job, not the code's structure.** If you point this skill at `CloseoutForm.tsx`, the doc is "How to close out a ticket" — not "The CloseoutForm component." Translate code structure into user tasks.

## Workflow

### Phase 0 (Init): Style guide check

**This runs every time the skill is invoked.** It's cheap and keeps docs consistent across runs.

1. Look for a style guide at these paths (in order):
   - `docs/.eli5-style.md`
   - `.eli5-style.md`
   - `docs/_eli5-style.md`

2. **If found** — read it. Use its voice, structure, vocabulary, and output-location rules for everything downstream.

3. **If not found** — run `scripts/init_style_guide.sh <repo-path>`. This creates `docs/.eli5-style.md` from the template in `assets/style-guide-template.md`. Tell the user:

   > "I scaffolded an ELI5 style guide at `docs/.eli5-style.md` — defaults look reasonable for a generic SaaS product. I'll proceed with these defaults now; you can edit that file anytime to tune voice, sections, vocabulary, or output location for future runs."

   Then continue with the defaults. Don't make the user pause and customize before getting their first doc.

### Phase 1: Understand the target feature

Determine what feature the user wants documented. Inputs vary:

**Mode A — Feature name only.** "ELI5 the closeout flow." Need to find the code. Use a combination of:
- Filename search (`find . -iname '*closeout*'`)
- Grepping for the term in UI strings (`grep -rE 'closeout' app/ components/`)
- Asking the user if there are multiple plausible matches

**Mode B — File or directory.** "ELI5 `components/closeout-form.tsx`." Read it and its imports.

**Mode C — Code + description.** "ELI5 the kanban view — it's how dev_admins triage tickets." Use the description as a starting hypothesis, verify against the code.

If after a reasonable look you still can't tell what user-facing feature is being requested, **ask once**, specifically: "I found three things related to 'closeout': the form, the approval flow, and the rollback button. Which one (or all three)?"

### Phase 2: Learn the product's UI vocabulary

Before drafting, scan the codebase to learn what the UI calls things. Run `scripts/scan_ui_vocabulary.sh <repo-path>` — it pulls strings from JSX/JSX-like sources, button labels, page titles, navigation items.

For stack-specific extraction patterns and tricky cases (i18n string catalogs, conditional labels), see `references/vocabulary-extraction.md`.

Use those terms verbatim in the doc. **If the UI button says "Close Out", the doc says "Close Out" — not "submit closeout" or "complete resolution".** Mismatched vocabulary makes docs useless because users can't find what they're looking for.

If a developer-facing term is unavoidable (rare), translate it:
- `actor` → "you" or the role name as it appears in the UI
- `tenant` / `org` → use the product term ("workspace", "company", etc.)
- `closeout body` → "your closeout notes"

### Phase 3: Identify the user's journey

For each feature, figure out:

1. **Goal** — what is the user trying to accomplish? (Not "submit a form" — what's the *real* goal? "Tell the team my ticket is fixed.")
2. **Trigger** — when/why would a user start this flow? Usually a state ("my ticket is in 'In Progress' and I'm done") or a need ("I want to invite a teammate").
3. **Entry point** — where in the UI do they start? (Page, button, menu item — by its exact UI label.)
4. **The path** — the sequence of screens/clicks. Concretely.
5. **The result** — what changes? What do they see when it's done?
6. **Branches** — what can go wrong, what choices exist, what happens if they're missing something.
7. **Aftermath** — what happens next, especially anything that affects *other* users (emails sent, notifications, status changes visible to admins, etc.).

Read code to find these. Routes, route handlers, form submit handlers, redirect targets, success/error states.

### Phase 4: Spot media opportunities

As you draft, mark spots where a visual would help with inline callouts:

- `> 📸 **Screenshot opportunity:** show the kanban board with "In Progress" column highlighted`
- `> 🎥 **Video opportunity:** 15-second clip of dragging a ticket from "Triage" to "In Progress"`
- `> 📊 **Diagram opportunity:** flow of ticket states from intake → triage → closeout`
- `> 🖼️ **Image opportunity:** annotated screenshot of the closeout form with each field labeled`

Don't go wild — one to four media callouts per doc is usually right. Place them where:
- A screen has multiple things and "the button on the left" is ambiguous in prose
- A multi-step UI flow benefits from a quick visual
- A state diagram (lifecycle, kanban) would replace a long prose paragraph

Never write the doc *assuming* the screenshot will be there. The prose must stand on its own; media is bonus.

### Phase 5: Draft the doc

Use the section structure from the style guide (default in `assets/feature-doc-template.md`). Default sections:

1. **What is it / when would you use it** — one short paragraph, leads with the user's goal
2. **The quick version** — 3-6 numbered steps, just the actions
3. **Step by step** — the same steps expanded with what to expect at each
4. **What you'll see** — visual elements, button meanings, status indicators
5. **Common situations** — "What if I made a mistake?", "What if X isn't showing up?"
6. **What happens behind the scenes** *(optional)* — only if it helps the user understand a non-obvious effect ("when you close out a ticket, the client gets an email — they can approve or push back")
7. **Need help?** — fallback line

Not every feature needs all sections. A "log in" doc doesn't need "What happens behind the scenes." See `references/structure.md` for when to include or skip each section, and for variations covering tiny, multi-flow, and reference-heavy features.

Apply the voice rules from `references/voice.md`. The two most important:
- **ELI5 ≠ patronizing.** The reader is smart but busy and unfamiliar with the app.
- **Mildly funny ≠ trying-too-hard.** Humor is allowed only where it *reduces friction*. Never put a joke in a heading. Never use "buckle up" or "let's dive in." Dry, plain, occasionally human is the target.

Apply the anti-patterns rules from `references/anti-patterns.md`. Words and phrases to never use.

### Phase 6: Write the file

Output location comes from the style guide. Default: `docs/features/<feature-slug>.md`.

After writing:
- Show the user the file path
- Show a short preview (first 20 lines or so)
- Mention the media callouts: "I marked 3 places where a screenshot would help — see lines X, Y, Z."
- Offer next step: "Want me to revise the voice, add more detail to a section, or move on to another feature?"

## Important constraints

**Read enough code to write accurately.** A doc that says "click Submit to send your ticket" when the button actually says "Send to Triage" is worse than no doc. When in doubt, grep for the exact string.

**Never document features that don't exist.** If the user asks you to document a feature that you can't find in the code, say so: "I can't find code that matches 'team invite flow' in this repo. Want me to look in a specific directory, or is the feature called something else here?"

**Don't include unimplemented features.** If you see a button labeled "Export to PDF" but the handler is `// TODO`, don't write the export section as if it works.

**One feature per file, but be flexible.** If "the closeout flow" is genuinely three sub-features (submit / approve / reject), it's fine to make one doc covering all three under shared context, OR three separate docs that link to each other. The style guide tells you which the user prefers.

## Sampling for large features

If the feature spans 20+ files or 2000+ lines:

1. Read the top-level entry point first (the route, the page, the parent component)
2. Follow the user's path through the code — don't read every file, just the ones on the happy path
3. Note: "This is a large feature; I'm documenting the most common flows. There are advanced options for [X, Y] — happy to document those separately if you want."

## Graceful degradation

If `scripts/scan_ui_vocabulary.sh` can't run (restricted env), do it manually:
- Grep for `<Button>` / `<button>` / `aria-label=` / `title=` / page titles
- Pull strings out, build a small vocabulary list yourself

If `scripts/init_style_guide.sh` can't run, write the style guide directly using `assets/style-guide-template.md` as the source. The file ends up the same.

## Redirects

User asks for developer docs → "This skill writes for end users. For technical docs aimed at engineers reading the codebase, the `teach` skill is the right tool."

User asks for release notes / announcements → "This skill produces reference docs users land on later. For announcements ('we just shipped X, here's why you'd care'), that's a different shape — want me to draft one anyway, or just produce the help doc?"

User asks for API docs → "This skill is for end-user help. API docs for external developers want a different format with request/response examples — let me know if you want me to switch shape, or keep going with end-user."
