---
name: guidance
description: Add, edit, or audit guidance docs. Default writes guidance for Claude (.claude/guidance/, Markdown, moflo universal rules). -h writes for human readers (docs/, lighter ruleset). --html emits HTML with a minimal default stylesheet instead of Markdown. -a audits the .claude/guidance/ directory.
arguments: "[-a] [-h] [--html] <topic-or-path>"
---

# /guidance — Author and audit project guidance

Help the user write, edit, or audit guidance docs. By default the skill writes guidance **for Claude** into `.claude/guidance/` as Markdown and enforces the universal rules from `.claude/guidance/moflo-guidance-rules.md` (the single source of truth — do not paraphrase or duplicate). Flags switch the **audience** (`-h` → humans) and the **output format** (`--html` → HTML).

**Arguments:** $ARGUMENTS

## Modes and flags

| Flag | Effect |
|------|--------|
| (none) | Single-doc mode for **Claude** — Markdown, full universal rules, destination `.claude/guidance/<kebab-topic>.md` |
| `-h` | Switch audience to **humans** — Markdown, lighter human ruleset, destination `docs/<kebab-topic>.md` |
| `--html` | Emit **HTML** (with the minimal default stylesheet from Step 2.5) instead of Markdown. Composes with `-h`. |
| `-a` | **Audit** mode — two-pass triage of `.claude/guidance/` (Claude only). Cannot combine with `-h` or `--html`. |
| `<topic-or-path>` | Topic name (kebab-cased into the default destination) or an explicit file path that overrides the default destination. |

Combos:

- `-h --html` → HTML for humans, default destination `docs/<kebab-topic>.html`
- `--html` alone → HTML for Claude. Unusual: Claude reads Markdown, not HTML. Warn the user and offer to add `-h` (write to `docs/` instead).
- An explicit `<path>` always wins over the default destination. If the path's directory contradicts the audience flag (e.g. `-h .claude/guidance/foo.md`), warn but honor the path.
- `-a -h` / `-a --html` → reject; audit mode targets `.claude/guidance/` (Claude) and emits a triage report, not a doc.

## Step 0 — Memory First

Before reading any files, run a memory search:

```
mcp__moflo__memory_search { query: "guidance rules writing project conventions", namespace: "guidance" }
```

This pulls the user's project-specific guidance conventions (if any) plus the moflo universal rules into context. The memory-first gate will block file reads otherwise.

## Step 1 — Parse Flags, Audience, Format, and Target

Parse `$ARGUMENTS` into four values: **mode** (single-doc or audit), **audience** (claude or human), **format** (md or html), and **target path**.

**Mode** is `audit` if `-a` is present, otherwise `single-doc`.

**Audience and format:**

| Flag combo | Audience | Format | Default destination |
|------------|----------|--------|---------------------|
| (none) | claude | md | `.claude/guidance/<kebab-topic>.md` |
| `-h` | human | md | `docs/<kebab-topic>.md` |
| `--html` | claude | html | `.claude/guidance/<kebab-topic>.html` — **warn**: Claude reads MD; suggest adding `-h` |
| `-h --html` | human | html | `docs/<kebab-topic>.html` |

**Target path resolution:**

| Remaining positional arg | Single-doc behavior | Audit behavior |
|---|---|---|
| empty | Ask user for a topic; use default destination from the audience+format table above | Audit all `.md` files under `.claude/guidance/` recursively |
| `<topic>` (no slash) | Kebab-case and append to the default destination | Audit all `.md` files under `.claude/guidance/<topic>/` recursively |
| `<path>` (contains a slash) | Use that exact path; if the path's directory contradicts the audience flag, warn but honor the path | n/a — audit ignores explicit paths |

**Reject combos** that don't make sense and tell the user why: `-a -h`, `-a --html` (audit emits a triage report, not a doc; it's Claude-targeted by design).

If single-doc and the file already exists, briefly summarize what it contains (one sentence) before walking the user through edits — confirm you have the right file.

## Step 2 — Single-Doc Mode

The rules applied depend on the audience. Confirm audience + format with the user in one line before writing — e.g. *"Writing human-readable MD into `docs/auth-overview.md` — apply lighter human ruleset?"*

### Audience: Claude (default) — full universal rules

Apply the universal rules from `.claude/guidance/moflo-guidance-rules.md`. The rules cover (do not paraphrase — read the source):

1. Lead with `**Purpose:**` line after the H1
2. Be imperative, not descriptive
3. Use tables for decision logic
4. Code examples must be concrete
5. Keep files under 500 lines
6. Headings must be specific
7. Avoid the listed anti-patterns
8. Optimize for RAG chunking
9. End with a `## See Also` section
10. Never cite issue or PR numbers — write the rule, not where it came from

### Audience: Humans (`-h` flag) — lighter human ruleset

Drop the rules that serve Claude's RAG retrieval and imperative-mood enforcement; keep the rules that serve readability for any reader.

| # | Universal rule | For humans | Why the change |
|---|----------------|------------|----------------|
| 1 | `**Purpose:**` line after H1 | **Keep** | Helps any reader orient quickly |
| 2 | Imperative voice (must/always/never) | **Drop** | Humans tolerate narrative prose; rigid imperative reads cold |
| 3 | Tables for decision logic | Keep when applicable | Tables aid scanning regardless of audience |
| 4 | Concrete examples (no `[placeholder]`) | **Keep** | Always |
| 5 | Under 500 lines | **Keep** | Readability cap |
| 6 | Specific H2 headings (not "Overview") | **Keep** | Discoverability + TOC quality |
| 7 | Avoid anti-patterns | **Modified** | Short prose preambles ARE allowed for humans; code-comments-as-rules still bad |
| 8 | Optimize for RAG chunking | **Drop** | Humans don't query a vector index |
| 9 | `## See Also` section at end | **Keep** | Helps human readers traverse to related docs |
| 10 | No issue / PR citations | **Keep** | A bare issue number is unresolvable for any reader; provenance belongs in `git log` |

### Creating a new doc — scaffold this shape

```markdown
# <Specific Title — what this doc is and when to use>

**Purpose:** <one sentence on what this doc covers and when to reference it>

---

## <Specific H2 — first actionable rule or topic>

<Imperative rule, then rationale, then example.>

---

## <Specific H2 — second>

<Same shape.>

---

## See Also

- `.claude/guidance/<related-doc>.md` — One-line description of why related
- `.claude/guidance/<another>.md` — One-line description
```

After scaffolding, ask the user 2–4 targeted questions to populate the body — never auto-write opinionated content into the user's project. Their guidance must reflect their conventions, not Claude's.

### Editing an existing doc — checklist before proposing changes

For the loaded file, evaluate against the universal rules and report findings as a short table BEFORE editing:

| Check | Status |
|-------|--------|
| Has `**Purpose:**` line right after H1 | yes / no |
| Has `## See Also` section at end | yes / no |
| Under 500 lines | <count> lines |
| H2 headings are specific (not "Overview", "Configuration", "Examples") | list any generic ones |
| Uses imperative voice for rules ("must"/"always"/"never") not hedged ("should"/"might"/"consider") | list hedged phrases found |
| Has prose preamble before first rule | yes / no |
| Cites issue or PR numbers (`(#NNNN)`, `issue #NNNN`, `Epic #NNNN`) | list every citation found |

Then propose edits as concrete diffs — never rewrite the whole file unless the user asks.

## Step 2.5 — HTML Output (`--html` flag)

When `--html` is set, write the doc as a standalone HTML file with the minimal default stylesheet below. Author the content first as Markdown (so the audience-appropriate ruleset still drives structure and voice), then render it to HTML.

### Conversion rules

- `# H1` → `<h1>` (one per file — the title)
- `## H2` → `<h2>` (section headings; emit a blank `<hr/>` between sections for readability parity with the MD `---` separators)
- `### H3` → `<h3>`
- `**Purpose:** …` → `<p class="purpose"><strong>Purpose:</strong> …</p>` (styled to stand out — see CSS below)
- Paragraphs → `<p>`
- Inline `code` → `<code>`; fenced ``` blocks → `<pre><code>` with no syntax highlighting (zero dependencies)
- `**bold**` → `<strong>`, `*italic*` → `<em>`
- Bulleted lists → `<ul><li>`; numbered lists → `<ol><li>`
- Markdown tables → real `<table><thead><tr><th>` / `<tbody><tr><td>`
- Relative `.md` links in `See Also` → rewrite to `.html` (so a `docs/` tree of `--html` docs cross-links correctly)
- HTML-escape `<`, `>`, `&` in body text; do not escape inside `<pre><code>` beyond the standard three

### Minimal default stylesheet

Embed inline in `<style>` inside `<head>`. No external CSS, no JS, no web fonts. The goal is **readable standalone** on any browser without polish — restyle downstream if needed.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title><!-- doc H1 here --></title>
<style>
  :root { color-scheme: light dark; }
  body {
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    line-height: 1.6;
    max-width: 48rem;
    margin: 2rem auto;
    padding: 0 1.25rem;
    color: #222;
    background: #fff;
  }
  @media (prefers-color-scheme: dark) {
    body { color: #e6e6e6; background: #14171a; }
    a { color: #6fa8ff; }
    code, pre { background: #1f2429; }
    th { background: #1f2429; }
    hr { border-color: #2a3038; }
  }
  h1 { font-size: 1.9rem; margin-top: 0; }
  h2 { font-size: 1.4rem; margin-top: 2rem; border-bottom: 1px solid #ddd; padding-bottom: 0.25rem; }
  h3 { font-size: 1.15rem; margin-top: 1.5rem; }
  p.purpose {
    border-left: 3px solid #6fa8ff;
    padding: 0.5rem 0.75rem;
    background: rgba(111, 168, 255, 0.08);
    margin: 1rem 0;
  }
  code { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; background: #f4f4f4; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.9em; }
  pre { background: #f4f4f4; padding: 0.75rem 1rem; border-radius: 4px; overflow-x: auto; }
  pre code { background: transparent; padding: 0; }
  table { border-collapse: collapse; margin: 1rem 0; width: 100%; }
  th, td { border: 1px solid #ddd; padding: 0.4rem 0.6rem; text-align: left; vertical-align: top; }
  th { background: #f4f4f4; font-weight: 600; }
  hr { border: none; border-top: 1px solid #ddd; margin: 2rem 0; }
  a { color: #0a58ca; text-decoration: none; }
  a:hover { text-decoration: underline; }
</style>
</head>
<body>
<!-- rendered content here -->
</body>
</html>
```

### Workflow

1. Author the Markdown body in memory exactly as Step 2 would, applying the audience-appropriate ruleset.
2. **Show the rendered Markdown to the user first** and get sign-off on content (cheaper to iterate on MD than HTML).
3. Render to HTML using the conversion rules and embed the stylesheet.
4. Write the `.html` file to the resolved destination.
5. Offer to also save the Markdown source alongside (e.g. `docs/foo.html` + `docs/foo.md`) so the doc remains editable as MD — recommend yes when the audience is humans.

## Step 3 — Audit Mode (`-a`)

Audit mode runs **two passes**, then merges them into one triage report. Both passes are mandatory — never skip one to save tokens. The user typed `-a` because they want both signals.

### 3a. Structural audit (existing-doc rule conformance)

Scan the guidance directory and score each `.md` against the universal rules. Walk the directory yourself with `Glob` and `Read`; do not delegate to a subagent for the audit itself unless the user has 30+ files.

**Skip moflo-managed synced files first.** Read the first ~5 lines of every candidate file and check for an auto-generated marker matching `<!-- AUTO-GENERATED by (moflo|flo-setup)`. Files with that marker are mirrored from `node_modules/moflo/.claude/guidance/shipped/` on every session start — any audit-driven edit gets silently clobbered next session, so they MUST NOT enter the per-file scoring or appear in the fix triage.

Aggregate skipped files into a single rollup line in the report (count only, not actionable). Format:

```
moflo-managed synced files: <N> skipped (auto-generated; rule violations belong upstream — file an issue against the moflo package)
```

Then for each remaining (user-authored) `.md` file:

1. Count lines (`wc -l` via Bash, or read + split)
2. Check for `**Purpose:**` line right after H1
3. Check for `## See Also` (Title Case, capital A) at end
4. Look for generic headings: `^## (Overview|Configuration|Examples|Rules|Notes|Details|Information)$`
5. Look for hedged language: `\b(should|might|consider|may want to)\b` in rule contexts
6. Detect prose preambles (>3 paragraphs between H1 and first H2 rule)

Render a sortable table with one row per file, columns: file, lines, has-purpose, has-see-also, generic-headings count, hedged count. Highlight the worst offenders first.

**Note on `**Purpose:**` and `## See Also` regex:** ripgrep / Grep tool treats `**` as a glob escape and may return zero matches even when the markers are present. Use a plain string check (`Select-String` on Windows, `grep -F` elsewhere) or read the file and string-match in JS — never trust a zero count from a wildcard-ambiguous pattern without spot-checking one file.

### 3b. Gap analysis (what topics are missing)

Now look at *what isn't there*. Scan the codebase for high-leverage areas that lack a corresponding guidance doc, so Claude has nothing to follow when working in those areas.

**Detection sources** (read each that exists):

| Signal | What to learn |
|--------|---------------|
| `package.json` deps + devDeps | Frameworks/libraries the project relies on (React, Drizzle, Vitest, etc.) |
| `pyproject.toml` / `requirements.txt` / `Cargo.toml` / `go.mod` / `Gemfile` | Same idea, other ecosystems |
| Top-level source layout (`src/**`, `bin/**`, `scripts/**`, etc.) | Architectural concerns (e.g. a `daemon/` directory implies daemon architecture is a concern) |
| `.claude/helpers/`, `.claude/scripts/`, `.claude/hooks/` | Hook + helper authoring is in scope |
| MCP tool source (`mcp-tools/**`, `mcp-server/**`) | MCP tool authoring |
| Test directories | Testing conventions (load-bearing if specific patterns exist — e.g. golden-file tests, snapshot conventions) |
| `.github/workflows/` | CI/CD conventions |
| Recent `git log` for files repeatedly edited together | Cross-cutting concerns that need explicit guidance |

**Cross-reference:** for each detected concern, grep the existing `.claude/guidance/` corpus for keyword coverage. A topic is a **gap** if (a) the concern shows up in code (not just transitive deps) and (b) no existing guidance doc names it in the title or first H2.

**Severity table:**

| Concern type | Severity if unmatched |
|--------------|------------------------|
| Direct dep used pervasively (>10 files import it) | warn |
| Architectural directory with >5 files | warn |
| Direct dep used in 1–10 files | info |
| Helper/hook/MCP authoring surface with custom code | warn |
| CI/CD workflows beyond the standard ones | info |
| Cross-cutting concern from git-history co-change | info |

**Render gaps as a separate table** with columns: detected concern, evidence (file count or representative path), suggested doc filename, severity. Lead with the warns.

**Don't auto-write any new doc.** Surface the gap, name the concern, propose a filename — then ask the user which gaps (if any) they want to fill. The single-doc mode (Step 2) handles authoring once they pick.

### 3c. Combined triage and fixes

After both 3a and 3b, list the **top 3–5 priority items** across both passes in plain English. Mix them — a structural fix to an existing doc and a missing-doc gap can both make the top list. For each, explain WHY (rule citation for structural; concern + evidence for gaps) and propose either a per-file fix (3a) or a per-doc authoring flow (3b).

Ask the user which to apply, then walk through chosen items one at a time. **Never apply audit fixes without explicit per-file confirmation** — guidance is high-leverage; silent edits are dangerous. **Never auto-create gap docs** — every new doc starts as a single-doc mode session with the user.

## Step 4 — After Editing

Once the user confirms the doc looks right:

1. Save the file via `Write` (new) or `Edit` (existing).
2. If you added a new doc, ask the user which existing doc should link to it via See Also (rule #9 needs bidirectional links to work).
3. Suggest re-indexing if the user runs moflo: `node bin/index-guidance.mjs` (or just wait for next session-start auto-reindex). **Only Claude-audience MD docs in `.claude/guidance/` are indexed** — human docs in `docs/` and any `.html` output sit outside the RAG index by design.

## Cheatsheet — Universal Rules Recap

The full rules live in `.claude/guidance/moflo-guidance-rules.md`. Quick recap:

| # | Rule | One-line |
|---|------|----------|
| 1 | Structure for scanability | Purpose line + specific H2s + rule-first ordering |
| 2 | Imperative voice | "Must" / "always" / "never", not "should" / "might" |
| 3 | Tables for decisions | Conditional logic in tables, not nested bullets |
| 4 | Concrete examples | Realistic values, not `[placeholder]` |
| 5 | <500 lines | Split by concern when over |
| 6 | Specific headings | Not "Overview" / "Configuration" |
| 7 | Anti-patterns | Single source of truth, no preambles, prose for rules (not code comments) |
| 8 | RAG chunking | 5–30 lines per H2, self-contained openings, `---` between sections |
| 9 | See Also | Title Case, end of every file, relative paths |

## Important

- **Memory-first is mandatory.** Always run `mcp__moflo__memory_search` in step 0 — the gate blocks reads otherwise.
- **Never duplicate the rules in this skill.** Reference `.claude/guidance/moflo-guidance-rules.md` and ask the user to read it if they want depth.
- **Never auto-write opinionated content.** Guidance is the user's project policy; ask before injecting your own opinions.
- **Confirm per file in audit mode.** Bulk edits to the user's guidance directory are high-blast-radius — confirm each one.
- **The `moflo-` filename prefix is moflo-only.** Consumer projects writing their own guidance do not need it; it exists to avoid collisions when moflo's shipped guidance syncs into a consumer's directory.
- **`-h` does not change Step 0.** Memory search is still mandatory — only the ruleset and destination change. Audit mode (`-a`) remains Claude-only and ignores `-h` / `--html`.
- **`--html`: sign off on the Markdown first.** Render to HTML only after the user has approved the rendered Markdown — iterating on the HTML directly is slower and obscures content issues behind markup.

## See Also

- `.claude/guidance/moflo-guidance-rules.md` — Universal writing rules this skill enforces
- `.claude/guidance/moflo-memory-strategy.md` — How well-written guidance feeds the RAG index
- `.claude/guidance/moflo-task-icons.md` — UX rule the skill checks for any TaskCreate examples in the user's guidance
- `.claude/guidance/moflo-user-facing-language.md` — Companion rule for any user-visible text the user's guidance discusses
