---
name: obsidian-ai-setup
description:
  Bootstrap an Obsidian vault with the AI Pro Obsidian Plugin. Creates the complete vault structure,
  system files, Obsidian configuration, memory system, hooks, and output styles, then runs
  personalized onboarding to tailor the workspace to the user. Uses a single universal structure
  with no mode selection. Trigger when the user says "set up", "bootstrap", "initialize",
  "onboarding", or runs `/obsidian-ai-setup`.
---

# AI Pro Obsidian Plugin — Setup + Onboarding

USE WHEN the user runs `/obsidian-ai-setup` or asks to set up their vault, bootstrap the assistant,
initialize the system, or configure the AI Pro Obsidian Plugin.

> [!important] User-facing language This skill is fully in English. Everything the user sees must be
> in English: orientation messages, form headings, bullet prompts in Phase B, the final Phase B+
> question, confirmations, and summaries.
>
> Internal instructions in this `SKILL.md` and technical values such as file names, frontmatter
> keys, `os-mode`, and slugs must remain as written.

> [!note] One universal mode This skill builds **one universal structure** — there is no "individual
> / company" mode selection. The base is a lightweight professional structure (`Context`,
> `Projects`, `Daily`, `Resources`, `Skills`, `Intelligence`) that works equally well for a solo
> operator or a small team. Do not create `Departments/`, `Team/{org}/Profiles/`, or separate
> business templates. `os-mode` is always `professional`.

This is a two-phase process:

- **Phase A**: Bootstrap — Create the universal directory structure and system files
- **Phase B**: Onboarding — Interview the user and personalize everything

## Pre-flight Check

Check if `claude.md` or `CLAUDE.md` exists **only** in the current working directory. Do NOT search
subdirectories or parent directories. Check only the exact current working directory path.

- **If it exists**: The vault is already set up. Ask the user:
  - Question: `This vault is already configured. What would you like to do?`
  - **`Restart onboarding`** — `Keep the structure and update files using new answers`
  - **`Full reset`** — `Delete everything and start from scratch (confirm twice before deleting)`
  - **`Cancel`** — `Do nothing`
- **If it does NOT exist**: Proceed with full setup (Phase A + Phase B)

> [!note] No mode selection There used to be a Phase 0 for choosing "individual / company" mode. It
> has been removed. The structure is always universal (`os-mode: professional`). Go directly to
> Phase A. Do not ask about a mode.

---

## Phase A: Bootstrap

Create the universal directory structure and write all system files. There is one structure — always
`os-mode: professional`.

### Resolving reference file paths

Every `references/<file>.md` mentioned below lives in the `references/` subdirectory next to **this
SKILL.md** — not in the user's working directory. Two conventions matter:

- **Read paths** (`references/foo.md`) → resolve relative to this SKILL.md's directory.
- **Write paths** (`./Foo/CLAUDE.md`) → resolve relative to the user's current working directory
  (the vault root).

If the Read tool cannot open a `references/...` path directly because some harnesses mount the skill
at a path that differs between Read and Bash, run a quick discovery step **once** before Step A.2:

```bash
# Find the references directory; cache the result for the rest of Phase A.
find / -type d -path '*obsidian-ai-setup/references' 2>/dev/null | head -1
```

Use that absolute path as the prefix for every reference read in Phase A and Phase B. Do not retry
path resolution per file. Resolve once and reuse.

### Step A.1: Create Directory Structure

One universal structure for everyone:

```bash
mkdir -p .claude
mkdir -p Context
mkdir -p Projects
mkdir -p Daily
mkdir -p Resources
mkdir -p Skills
mkdir -p Intelligence/meetings/team-standups
mkdir -p Intelligence/meetings/client-calls
mkdir -p Intelligence/meetings/one-on-ones
mkdir -p Intelligence/meetings/general
mkdir -p Intelligence/competitors
mkdir -p Intelligence/market
mkdir -p Intelligence/decisions
mkdir -p Intelligence/archive
```

No `Departments/`, no `Team/`, no `Onboarding/` — those were business-mode folders and are no longer
used.

### Step A.2: Write System Files from References

Read each reference file and write it to the corresponding local path. The reference files contain
the complete content for each system file.

**Shared system files:**

| Reference File                         | Creates at Local Path     |
| -------------------------------------- | ------------------------- |
| `references/settings-json-template.md` | `./.claude/settings.json` |
| `references/claudeignore-template.md`  | `./.claudeignore`         |
| `references/gitignore-template.md`     | `./.gitignore`            |

**Root CLAUDE.md template:**

| Reference File                     | Creates at Local Path |
| ---------------------------------- | --------------------- |
| `references/claude-md-template.md` | `./CLAUDE.md`         |

**Per-folder routing indexes** (every major folder gets its own `CLAUDE.md` — this matches the
production vault convention):

| Reference File                         | Creates at Local Path      |
| -------------------------------------- | -------------------------- |
| `references/claude-md-context.md`      | `./Context/CLAUDE.md`      |
| `references/claude-md-projects.md`     | `./Projects/CLAUDE.md`     |
| `references/claude-md-daily.md`        | `./Daily/CLAUDE.md`        |
| `references/claude-md-intelligence.md` | `./Intelligence/CLAUDE.md` |
| `references/claude-md-resources.md`    | `./Resources/CLAUDE.md`    |
| `references/claude-md-skills.md`       | `./Skills/CLAUDE.md`       |

For each row: read the reference file, then write its content to the local path.

### Step A.3: Initialize Starter Context Files

**Do NOT create placeholder skills.** The `Skills/` folder is created empty, with only its
`CLAUDE.md` routing index from Step A.2. The user adds their own skills later. No `linkedin-writer`,
no `newsletter-writer`, no example scaffolds.

Starter context file:

- Read `references/context-me.md` → write to `./Context/me.md`

That is the only starter context file. Everything else in `Context/` is created later during Phase B
Build, only when the onboarding answers actually contain data for it.

### Step A.4: Make Hooks Executable

```bash
chmod +x .claude/hooks/*.sh
```

### Step A.5: Confirm Bootstrap

Tell the user:

- "The vault structure has been created successfully."
- List the main folders created: `Context`, `Projects`, `Daily`, `Resources`, `Skills`,
  `Intelligence`
- Recommend opening this folder as a vault in Obsidian
- Recommend installing the **TaskNotes** community plugin if they want task management features
- Note that **Bases** (native database views) are built into Obsidian — no plugin is needed for
  queries
- Mention that `Resources/` is for prompts, frameworks, swipe files, templates, and reusable
  materials
- "Now let's personalize it for you."

Then proceed to Phase B.

---

## Phase B: Onboarding — Guided Brain Dump

This skill runs **inside Cowork**. Phase B uses Cowork's rich-HTML widget tool — **not**
AskUserQuestion — to render real forms with stacked categories, free-text textareas, and proper
styling. The form should match the look of `os-optimizer`'s "Audit run details" form.

This is a guided brain dump across **12 categories** of the user's life and work, batched into **3
rich-HTML forms** with 4 categories per form. Bullet points inside each category are **inspiration
prompts**. The user can riff on whatever feels relevant.

The pitch to the user: _sit down for an hour or two, pour a beer, order a pizza, and brain-dump.
This is not only about making the assistant personal on day one — it is a useful exercise in
itself._

### The tool: `mcp__visualize__show_widget` (Cowork-only)

Each of the 3 forms is **one** call to `mcp__visualize__show_widget`. The tool accepts:

| Field              | Purpose                                                                |
| ------------------ | ---------------------------------------------------------------------- |
| `title`            | Internal widget identifier, for example `ai_setup_form_1_you_business` |
| `loading_messages` | Array of short strings shown while the form renders                    |
| `widget_code`      | Raw HTML for the form, using Cowork's `elicit-*` class conventions     |

The user fills in the form and submits. The submitted values come back to the agent as the tool
result. The agent then proceeds to the next form. No AskUserQuestion. No radio buttons. No "Other"
box.

### How the user should respond — per category

Inside each category's textarea, the user can:

1. **Paste a Whisper / dictation transcript** — open phone or Mac dictation, ramble for 2–5 minutes,
   then paste the transcript.
2. **Paste documents** — links to PDFs, Notion pages, Google Docs, brand guides, About pages,
   LinkedIn profiles, OKR docs, decks, or file paths.
3. **Point at connectors** — paste a Notion workspace URL, wiki link, or Drive folder.
4. **Type long-form free text.**

There are two kinds of knowledge: **what lives in your head** (dictate it) and **what already lives
online or in a tool** (paste links, docs, files, or paths). The user can mix them freely per
category. Leave a textarea blank to skip that category.

### Before Form 1 — Send one orienting message

Send this verbatim or close to it. No tool call yet:

> Three short forms. Four categories each. Twelve categories total. This is not a questionnaire — it
> is a guided brain dump.
>
> In each category there are three ways to give me context: **a brain-dump field**, **a links and
> file paths field**, and **file uploads**. Use any of them or all of them. Dump whatever comes to
> mind around the bullet prompts. You do not need to answer every bullet. Leave a category empty to
> skip it.
>
> The best inputs are things like a dictation transcript, an About page, a brand book PDF, an OKR
> document, a LinkedIn profile, or a Notion page. The more context you give me, the less generic
> your vault will feel on day one.
>
> Sit down for an hour or two. Pour a beer. Order a pizza. It is worth it.
>
> Submit each form when you are ready. Write "skip all" at any point to move forward with defaults.

### Widget HTML template

Every category in every form uses this shape.

Each category gets **three inputs**: a brain-dump textarea, a links/paths textarea, and a file
upload input. Any or all can be filled. All blank = skip.

Inside `widget_code` for each form, build a `<form class="elicit">` containing one header and four
`elicit-group` blocks. Per category:

```html
<div class="elicit-group">
	<label class="elicit-question">{N}/12 — {Category name}</label>
	<div
		class="elicit-bullets"
		style="font-size:13px; color:var(--color-text-secondary); margin:8px 0">
		<ul style="margin:0; padding-left:18px">
			<li>{inspiration bullet 1}</li>
			<li>{inspiration bullet 2}</li>
			<li>{inspiration bullet 3}</li>
			<!-- etc -->
		</ul>
		<p style="margin-top:6px; font-style:italic"
			>Dump your thoughts below, OR paste links / file paths, OR upload documents. Any combination
			works. Leave everything empty to skip this category.</p
		>
	</div>

	<textarea
		class="elicit-textarea"
		name="cat{N}_braindump"
		rows="6"
		style="width:100%; border-radius:10px; padding:10px; border:1px solid var(--color-border-subtle); font-family:inherit; font-size:13px; margin-bottom:8px"
		placeholder="Brain dump — paste a dictation transcript or write freely…"></textarea>

	<textarea
		class="elicit-textarea"
		name="cat{N}_links"
		rows="2"
		style="width:100%; border-radius:10px; padding:10px; border:1px solid var(--color-border-subtle); font-family:inherit; font-size:13px; margin-bottom:8px"
		placeholder="Links and file paths — one per line (Notion URL, LinkedIn profile, /path/to/file.pdf, etc.)"></textarea>

	<input
		class="elicit-file"
		type="file"
		name="cat{N}_files"
		multiple
		accept=".md,.txt,.pdf,.docx,.pptx,.xlsx,.csv,.json,.yaml,.yml,.png,.jpg,.jpeg"
		style="font-size:12px; color:var(--color-text-secondary)" />
</div>
```

And one header at the top of `<form class="elicit">`:

```html
<div class="elicit-header">
	<svg
		viewBox="0 0 20 20"
		fill="currentColor"
		width="20"
		height="20">
		<!-- pencil/clipboard icon -->
	</svg>
	<span>{Form title}</span>
</div>
<div class="elicit-body">
	<!-- 4 elicit-group blocks -->
</div>
```

Reuse the SVG icon pattern from the optimizer's `Audit run details` widget, using the
clipboard-with-marks icon. Form titles: "You and the Business", "Customer and Brand", "How You
Work". The `{N}/12 — {Category name}` label and every bullet must be shown in English using the
category names and bullets defined below.

### Reading form submissions

When the widget returns, the result is a record mapping each input's `name` to its value:

- `cat{N}_braindump` → string (typed text / transcript)
- `cat{N}_links` → string (newline-separated URLs and file paths)
- `cat{N}_files` → array of file references (Cowork uploads these into the workspace folder; the
  result gives you the paths or signed URLs)

A category is "skipped" only when all three inputs are empty or blank.

### Ingestion between forms

After each form returns, for each category in that form:

1. **`cat{N}_braindump`** — if non-empty, tag and store raw in the working corpus under that
   category. Do not paraphrase.
2. **`cat{N}_links`** — split on newlines. For each line:
   - HTTP(S) URL → fetch with WebFetch / WebSearch.
   - Local file path → Read it.
   - Folder path → Glob, then Read each file.
3. **`cat{N}_files`** — for each uploaded file:
   - `.md`, `.txt`, `.json`, `.yaml`, `.csv` → Read directly
   - `.pdf` → Read with `pages` parameter if large
   - `.docx` / `.pptx` / `.xlsx` → use `pandoc` / `textutil` via Bash if available; otherwise note
     and continue
   - Images → Read with multimodal support

Merge everything into the corpus tagged by category. Then immediately fire the next form. No
commentary or summarization between forms.

The 12 categories use Oskar's category breakdown. Bullet inspiration prompts are Oskar's prompt
blocks, plus Ben's framing of "brain-dump anything around any of these bullets."

---

### The 12 Categories — 3 Forms × 4 Categories

This is the single universal onboarding flow. Slugs in `Title:` are internal identifiers; keep them
as written. Category headings, `Header:` values, and bullets are shown to the user in English.

**Form 1 — You and the Business** — one `mcp__visualize__show_widget` call. Title:
`ai_setup_form_1_you_business`. Contains Q1–Q4 as stacked `elicit-group` blocks.

**Q1. You.** Header: `You`

Bullets:

- Name, role/title, location, niche
- When and how you work best: mornings, deep-work blocks, after a walk, late at night, etc.
- If someone you respect introduced you in a room full of people you respect, how would you want
  them to describe you?
- Five qualities that describe you, one or two words each

**Q2. Your Origin and Point of View.** Header: `POV`

Bullets:

- Why you started, or how you came into the work you do now
- A belief or position you hold strongly, even when it is unpopular
- The "big idea" behind your work: wedge, thesis, core belief
- What you are fighting against: a category, behavior, competitor archetype, or status quo

**Q3. What You Sell.** Header: `Revenue Lines`

Bullets (write one paragraph for each revenue line; skip if none exist yet):

- Name, what it does, who it is for, current stage
- Current revenue baseline, if relevant
- How it started and what made you create it

**Q4. Promise.** Header: `Offer`

Bullets:

- One to three problems you solve for customers
- For each problem: do customers already know they have it, or do you need to educate them?
- Your value proposition in one sentence
- The promise or guarantee you make, explicit or implied
- Why customers actually choose you, using their words if you have heard them

**Form 2 — Customer and Brand** — one `mcp__visualize__show_widget` call. Title:
`ai_setup_form_2_customer_brand`. Contains Q5–Q8 as stacked `elicit-group` blocks.

**Q5. Customer.** Header: `Customer`

Bullets:

- Job title, role, niche, responsibility area
- What their day looks like and which tools they live in
- The language and words they use to describe their problem
- The dream outcome they want
- The situation they are in before they come to you — what triggered the search
- How long it usually takes them to decide to buy
- Media, podcasts, newsletters, or authors they follow
- Three to five real examples: names, LinkedIn profiles, or company names

**Q6. Your Voice and Visual Identity.** Header: `Voice`

Bullets:

- Tone descriptors that fit: direct, warm, dry, technical, playful, serious, supportive, etc.
- Five qualities that describe how you sound
- Signature phrases you actually use
- Words or phrases you would never use
- Topics you enjoy talking about
- Topics you refuse to discuss publicly
- Brand colors, fonts, slogans, if any
- The feeling people should leave with after reading your material
- Or paste a writing sample / link, and I will extract the voice from it

**Q7. Your Positioning.** Header: `Positioning`

Bullets:

- The enemy you are fighting: category, behavior, or competitor archetype
- How you solve the problem differently from the obvious alternatives
- Three to four clear messages you want associated with your name or brand

**Q8. Priorities This Year.** Header: `Priorities`

Bullets:

- One to three measurable outcomes: revenue, audience size, launch date, etc.
- The "why" behind each one
- What you are deliberately saying no to in order to stay focused

**Form 3 — How You Work** — one `mcp__visualize__show_widget` call. Title:
`ai_setup_form_3_how_you_operate`. Contains Q9–Q12 as stacked `elicit-group` blocks.

**Q9. Active Projects.** Header: `Projects`

Bullets (for each project):

- Name, one-line goal, status, deadline if any
- Which business it belongs to, if there are several
- Who else is involved

**Q10. People You Work With.** Header: `People`

Bullets:

- Team members, contractors, key external contacts
- For each person: name, role, how you work together
- Skip if you are completely solo

**Q11. Your Stack.** Header: `Stack`

Bullets:

- Your stack for communication, meetings, CRM, content, finance, development, and automation
- The source of truth for each major workflow: where deals live, where decisions live, where writing
  actually happens, where the calendar lives

**Q12. What Drains You and What Should Be Automated.** Header: `Drain`

Bullets:

- Top one or two painful recurring processes. Use this template: When **X** happens → I do **Y** →
  it takes **Z** time → the result is **W** → what I actually want is **V**
- What is currently consuming your attention: open loops, unresolved decisions, or things that
  should be done but are not done

---

The user submits each form with one click. Per-category response patterns:

- Type or paste a brain dump, transcript, links, docs, or file paths into the textarea
- Leave the textarea blank to skip that category
- Reply "skip all" between forms to stop asking and move to Phase B+

**Accept whatever they give.** Do not ask follow-up questions inside or between forms. Extract what
you can.

**If the user submits every form empty**, proceed to build with defaults only.

---

## Phase B+: Additional Context Drop

After Q12 or "skip all", and **before** Phase B Build, ask one final `AskUserQuestion` to invite any
leftover source material that did not surface during the 12 categories. Most users still have brand
decks, About pages, intake forms, LinkedIn URLs, Notion docs, PDFs, slide exports, voice/style
guides, OKR docs, org charts, project briefs, and similar materials. Always ask, even if Q1–Q12
looked rich.

**Call AskUserQuestion** with one question, header: `Context`

- Question: "Is there anything else I should extract context from before building the vault? Upload
  files (PDF, MD, DOCX), paste links (LinkedIn, websites, Notion pages, Google Docs), point me to a
  local folder, or paste raw text. The more context I have, the more personal your vault will be —
  instead of generic templates with placeholders."
- Options:
  - `Yes — I will paste links / upload files` — "Walk me through it"
  - `Yes — I will point to a local folder` — "I have local files"
  - `No — build from the answers above` — "Use what you already have"
  - `Skip` — "Skip this step"

**If the user picks a "Yes" option** or pastes content directly:

1. Collect everything they share. Be greedy — accept anything they offer.
2. **For each link**: call `WebFetch` or `WebSearch` if the URL is a search. Extract the relevant
   content.
3. **For each uploaded file or local file path**:
   - `.md`, `.txt`, `.json`, `.yaml`, `.csv` → read directly with `Read`
   - `.pdf` → read with `Read`, using the `pages` parameter if the file is longer than 10 pages
   - `.docx`, `.pptx`, `.xlsx` → use Bash with `pandoc` or `textutil` if available; otherwise tell
     the user to export as PDF or Markdown and share it again
   - Images / screenshots → read with multimodal support
4. **For a local folder path**: use `Glob` to enumerate, then read each file.
5. **Maintain a context corpus** in working memory: every fact, name, number, quote, and useful
   detail you find. Tag each item by likely target file, such as `me.md`, `brand.md`, `icp.md`,
   `strategy.md`, `projects/{name}`, etc.
6. After ingestion, briefly tell the user what you pulled, for example: "Pulled 4 files:
   brand-guidelines.pdf, about-page.md, okrs-2026.md, team-roster.csv. Fetched 18 links." One
   sentence. Then proceed to Build.

**If the user picks `No` or `Skip`**: proceed straight to Build with only the Q1–Q12 answers from
Phase B.

---

## Phase B Build: Personalize the Vault

After Q12 + the additional context drop, or after skips, build everything you can from what the user
gave you. Work silently. Do not narrate every step.

### CRITICAL: Real Personalization, Not Template Scaffolds

The reference files in `references/` are **scaffolds**. They show the section structure to use. They
are **not** the output. Do not copy a template verbatim with placeholders intact.

For every file you write:

1. **Read the reference template** to learn the section structure: headings, frontmatter shape, and
   section order.
2. **Replace every placeholder** — anything in `[brackets]` or marked as TBD — with real data
   extracted from the 12 Phase B answers and the Phase B+ corpus.
3. **If a section has zero supporting data** after exhausting both Q answers and the corpus, **omit
   the entire section** instead of writing `[name]` or `TBD`. The output should never contain
   bracketed placeholders.
4. **If only some bullets in a section have data**, keep the section and drop the empty bullets.
5. **Use the user's actual words, names, numbers, URLs, and quotes** wherever the corpus contains
   them. Do not paraphrase facts. Preserve specificity: exact company names, exact dollar figures,
   exact dates, and exact phrases the user uses.
6. **Cross-reference**: a single fact may belong in multiple files. For example, "we sell to RevOps
   leaders at Series B SaaS" belongs in both `icp.md` and `brand.md` positioning. Place it in every
   file where it is relevant.
7. **Frontmatter `updated:`** = today's date.

A finished context file should read like a real human-written document about the user. If it reads
like a fillable form, you did it wrong. Go back and fill it.

### Build Step 1: Create Context Files

For every file below, source data from BOTH the Q answers AND the Phase B+ corpus: uploaded files,
fetched links, and folder reads. The corpus usually contains the depth; Q answers are the anchors.
Q1–Q12 are the 12 onboarding categories.

- **`Context/me.md`** — Always created. Fill from Q1 (name, role, location, peer-intro line,
  attributes, working style), Q2 (origin / POV / wedge / enemy), Q12 (drains, open loops), and the
  corpus. Read `references/context-me.md` as scaffold.
- **`Context/business.md`** — Only if Q3 had content. Fill from Q3 (revenue lines: name, what it
  does, who it is for, stage, baseline, origin) and the corpus (About page, business overview docs).
  Read `references/context-business.md` as scaffold.
- **`Context/services.md`** — Only if Q3 lists multiple revenue lines or the corpus has
  product/service docs. Read `references/context-services.md` as scaffold.
- **`Context/pain-points.md`** — Only if Q4 named problems or Q2 surfaced one. Include an awareness
  column (aware vs needs education) using Q4's awareness signal. Read
  `references/context-pain-points.md` as scaffold.
- **`Context/icp.md`** — Only if Q5 had content or the corpus has ICP material. Fill role, day,
  language, dream outcome, trigger, decision time, media, and examples. Read
  `references/context-icp.md` as scaffold.
- **`Context/brand.md`** — Only if Q6 (voice), Q7 (positioning), or Q4 (why customers choose you)
  had content, or if the corpus has brand material. From Q4, take value proposition + why customers
  choose you. From Q6, take voice descriptors, signature phrases, words to avoid, feeling, colors,
  and fonts. From Q7, take enemy, differentiation, and key messages. Read
  `references/context-brand.md` as scaffold.
- **`Context/strategy.md`** — Only if Q8 had content. Fill priorities, why, and explicit nos. Read
  `references/context-strategy.md` as scaffold.
- **`Context/team.md`** — Only if Q10 had content (people / collaborators) or the corpus has a team
  / contractor list. Read `references/context-team.md` as scaffold.
- **`Context/infrastructure.md`** — Only if Q11 (stack) or Q12 (workflows) had content, or the
  corpus has a stack doc. Combine tool stack from Q11 with workflows to automate from Q12. Read
  `references/context-infrastructure.md` as scaffold.

### Build Step 2: Create Project Folders

Use Q9 (active projects), plus any project briefs, Notion exports, or project lists in the corpus.
Intelligently structure each project based on what the user gave you.

**Analyze the information and decide the right structure:**

- Simple mention ("working on a podcast") → just a `README.md`
- Moderate detail (scope, deadlines, people) → `README.md` + relevant subdirectories
- Rich info (briefs, specs, research, multiple workstreams) → full structure with subdirectories and
  files

**Create subdirectories only when the content justifies them:**

| Content type                              | Goes to                                 |
| ----------------------------------------- | --------------------------------------- |
| Overview, status, deadlines, contacts     | `README.md`                             |
| Research, competitor analysis, references | `research/{topic}.md`                   |
| Specs, requirements, briefs               | `specs/{name}.md` or `briefs/{name}.md` |
| Drafts, scripts, written content          | `drafts/{name}.md`                      |
| Ideas, brainstorms                        | `ideas/{name}.md`                       |
| Notes, working docs                       | `notes/{name}.md`                       |

**README.md is always the index:**

```markdown
---
type: project
status: active
owner: [name]
business: [business unit if applicable]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## Overview

[What this project is]

## Current Status

[Where things stand]

## Key Resources

[Links, tools, contacts]

## Next Steps

[What needs to happen]
```

Do not create empty subdirectories. Do not cram everything into the README. Distribute content into
the right files based on what it actually is.

### Build Step 3: Create First Daily Note

Create `Daily/YYYY-MM-DD.md` using today's date:

```markdown
---
type: daily-note
date: YYYY-MM-DD
---

# YYYY-MM-DD

## Session

- **Focus**: Initial vault setup and onboarding
- **Completed**: Full vault bootstrap + personalized onboarding
- **Next Steps**: [based on what was discussed]
```

### Build Step 4: Confirm Completion

Tell the user:

- A quick summary of what was created: which context files, how many projects, and any important
  structure
- "Open this folder in Obsidian to see your vault."
- "You can add more context anytime — just tell me and I will update the right files."
- Suggest a next action based on what they told you

## Guidelines

- No mode selection — one universal structure, always `os-mode: professional`
- Phase A is fully automated — no user input needed
- Phase B is **12 categories**, batched into **3 rich-HTML forms** rendered via
  `mcp__visualize__show_widget` (Cowork-only)
- Each form has 4 stacked categories with title, bullet inspiration, a brain-dump textarea, a
  links/paths textarea, and file upload
- It is a guided **brain dump**, not a Q&A box
- The bullets are inspiration, not strict questions
- Always recommend dictation / Whisper, plus pasting docs, links, and file paths into the textarea
- No follow-ups, no drilling deeper between forms
- Phase B+ is one final AskUserQuestion (or visualize widget) inviting any leftover files, links,
  folders, or raw text — always ask, even if Forms 1–3 looked rich
- Accept any format: typed brain dumps, Whisper transcripts, pasted docs, uploaded files, links
  (LinkedIn, websites, blog posts, Notion, Drive), local folder paths, or skips
- For every link the user pastes, fetch it with `WebFetch` / `WebSearch`; for every file or folder,
  read it with `Read` / `Glob`; merge everything into a single context corpus before building
- **Templates are scaffolds, not outputs.** Replace every `[bracketed placeholder]` with real user
  data. If a section has no data after exhausting Q answers + corpus, omit the section. Never leave
  placeholders in the written file.
- Preserve specificity: use the user's exact names, numbers, URLs, and phrasing
- Only create context files that have real content — do not create empty placeholder files
- Do not narrate every file you create — build the vault and summarize at the end
