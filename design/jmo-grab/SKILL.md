---
name: jmo-grab
description: "Save a design Johnathan likes into his personal design library, or search the library for relevant references. Use /jmo-grab (no args) to capture the component/design currently being discussed — code, design tokens, and a description — into ~/.claude/skills/jmo-grab/library/. Use /jmo-grab library to scan the library and surface designs relevant to whatever is currently being built. Triggers on phrases like 'grab this', 'save this design', 'I like this — keep it', 'jmo-grab', 'add to my library', 'find a similar design from my library', 'pull a reference from my saved designs'."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# jmo-grab — Personal Design Library

Johnathan's personal "screenshot but for code" — when he sees a UI component or design he likes, this skill captures the **code, design tokens, and a description** into a searchable library so future projects can reference it.

The library lives at `~/.claude/skills/jmo-grab/library/` as one markdown file per saved design. Each file is self-contained: the code, the tokens that make it work, and a description of what makes it good.

## Two modes

This skill has two modes selected by the first argument:

- **No args (default)** → **SAVE mode**: capture the design currently being discussed.
- **`library`** → **SEARCH mode**: scan saved designs and surface ones relevant to current work.

If `$ARGUMENTS` is empty or doesn't start with `library`/`search`/`find`/`browse`, run **SAVE mode**. Otherwise run **SEARCH mode**.

---

## SAVE mode

### Step 1 — Identify the target

Figure out what to save from conversation context. Don't ask if it's obvious; ask only if multiple things were discussed.

What counts as "the design":
- A specific component file (e.g. `components/StopDetail.tsx`)
- A visual pattern across files (e.g. "the day strip + map crossfade")
- A snippet from the conversation (paste the user pasted, or a block you wrote)
- A page/screen composed of several pieces

If unclear, use `AskUserQuestion` once with a short list of candidates pulled from the recent conversation.

### Step 2 — Pick a slug

The filename is `<component-name>.md` in kebab-case. Examples:
- `mobile-day-strip.md`
- `frosted-glass-sheet.md`
- `map-crossfade-transition.md`

Make the slug describe **what the design IS**, not where it came from. "spain-trip-stop-card.md" is bad; "expandable-stop-card.md" is good — the trip is incidental, the pattern is the asset.

If a file with that slug already exists, ask whether to:
1. Overwrite (Johnathan's iterating on the same idea)
2. Add a numeric suffix (these are different takes worth keeping both)
3. Rename to be more specific

### Step 3 — Extract code

Read the actual source file(s). Don't summarize or paraphrase — capture the literal code. If it's spread across files, include each file with its path.

For very large components (>300 lines), focus on:
- The structural JSX/markup
- The styling that makes it distinctive (Tailwind classes, CSS-in-JS, CSS modules)
- Any custom hooks/animations/state machines that drive the behavior

Skip boilerplate like generic prop-types, repeated event boilerplate, or imports that don't matter.

### Step 4 — Extract design tokens

This is the part most "save a snippet" tools miss. Walk through the code and pull out:

- **Colors** — exact hex/rgb/oklch values, or the token names (`bg-zinc-900`, `text-emerald-500`)
- **Typography** — font family, size, weight, tracking, line-height
- **Spacing** — gaps, padding, margin scales actually used
- **Radii** — `rounded-2xl`, `border-radius: 14px`
- **Shadows / blur** — `backdrop-blur-md`, custom box-shadows
- **Motion** — easing curves, durations, spring configs, stagger values
- **Breakpoints** — if the design responds, note the breakpoints

If the project uses Tailwind, list the actual utility classes that carry visual meaning. If it uses design tokens (CSS vars, theme files), resolve them to their literal values too — Johnathan will be referencing this from a different project where those tokens may not exist.

### Step 5 — Write the description

The description is what makes the library searchable. It must answer:

1. **What is this?** One sentence.
2. **What makes it distinctive?** What would make Johnathan want to reuse this — the specific move, not generic praise.
3. **When to reach for it.** Concrete situations where this design fits.
4. **Tags** — 5-10 short tags for grep-ability. Mix categories (`mobile`, `desktop`, `card`, `nav`, `modal`) with vibe (`minimal`, `dense`, `playful`, `editorial`) with mechanics (`crossfade`, `sticky`, `parallax`, `frosted`).

Avoid: "beautiful", "clean", "modern", "elegant" — these don't help future-you find anything.

### Step 6 — Write the file

Save to `~/.claude/skills/jmo-grab/library/<slug>.md` using this template:

```markdown
---
name: <slug>
saved: <YYYY-MM-DD>
source_project: <project name from cwd or git remote>
source_files:
  - <relative path 1>
  - <relative path 2>
tags: [tag1, tag2, tag3, ...]
---

# <Human-readable name>

## What it is
<One sentence.>

## What makes it good
<2-4 sentences on the specific moves that make this worth saving.>

## When to use it
<Concrete situations / shapes of problem this fits.>

## Design tokens

**Colors:** ...
**Typography:** ...
**Spacing:** ...
**Radii:** ...
**Shadows / blur:** ...
**Motion:** ...

## Code

### `<path/to/file.tsx>`
```tsx
<actual code>
```

### `<path/to/another.css>`
```css
<actual code>
```

## Notes
<Anything that won't be obvious from the code — gotchas, dependencies on parent context, why a non-obvious choice was made.>
```

### Step 7 — Confirm

After writing, output:
- The full path of the saved file
- The slug
- The tags
- A one-line summary

Don't read the file back to verify — `Write` would have errored if it failed.

---

## SEARCH mode (`/jmo-grab library`)

Triggered when `$ARGUMENTS` starts with `library`, `search`, `find`, or `browse`. Optional query terms after the keyword (e.g. `/jmo-grab library mobile sheet`) narrow the search.

### Step 1 — Understand the current context

Before reading the library, figure out what Johnathan is working on right now:
- What component/feature is the conversation about?
- What's the surface (mobile? desktop? marketing page? data-dense app?)
- What design problem is on the table (navigation? card layout? empty state? transition?)

If the conversation has no UI context yet, ask a short clarifying question: "What are you designing — and is it mobile, desktop, or both?"

If the user passed query terms after `library`, weight those heavily.

### Step 2 — Scan the library

```bash
ls ~/.claude/skills/jmo-grab/library/*.md 2>/dev/null
```

If empty, tell Johnathan the library has nothing saved yet and suggest he run `/jmo-grab` next time he sees something he likes.

For each file, read the **frontmatter + first two sections** (What it is, What makes it good). Don't read full code blocks during the scan — they're large and not needed for relevance scoring.

### Step 3 — Score and rank

For each saved design, judge relevance:
- **Tag overlap** with the current problem (highest signal)
- **"When to use it"** matches the current situation
- **Surface match** (mobile vs desktop)
- **Mechanic match** (if current task involves a crossfade and a saved design is about crossfades, that's a hit)

Pick the top 3-5. If nothing scores well, say so honestly rather than padding with weak matches.

### Step 4 — Present

For each pick, output a compact card:

```
### <name> — <slug>.md
<One-sentence what it is.>
**Why it's relevant:** <1-2 sentences tying it to current work.>
**Tags:** [...]
**Path:** ~/.claude/skills/jmo-grab/library/<slug>.md
```

Then ask: "Want me to pull the full code/tokens from any of these into the current work?"

If Johnathan picks one, read the full file and apply/adapt the patterns to the current context. Don't blindly paste — translate the tokens and structure into whatever stack the current project uses.

---

## Rules

- **Library files are reference material, not code to import.** When applying a saved design to a new project, adapt — don't just paste. Tailwind classes from one project might not match another's config.
- **Never delete library files** unless Johnathan explicitly asks. If he wants to update a saved design, prefer overwriting in place.
- **Don't pollute the library with mediocre saves.** If Johnathan says "grab this" about something that's just OK, ask once: "Sure — what specifically about it should I capture? I want the description to be useful later."
- **Tags are search weight.** Be generous but specific. `[mobile, sheet, frosted, drag-handle, ios-style]` beats `[mobile, ui, component]`.
- **Source paths are absolute references at save time.** They may not exist later if Johnathan moves projects — that's fine, the saved code in the markdown is the source of truth.
