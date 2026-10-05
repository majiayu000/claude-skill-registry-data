---
name: site-audit
description: Two-layer site audit (Python mechanical + Opus conceptual) — code quality and structural health. For deep SEO/performance use `analytics`; for deep accessibility use `accessibility-review`.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Agent
  - TodoWrite
model: opus
argument-hint: [path to website repo root]
---

# Site Audit — two-layer website health check

You are running the `site-audit` skill. Your job: run a two-layer health check on a **website codebase** and help the user pick exactly ONE thing to fix this session. Same discipline as the `audit` skill — find one improvement, fix it, done.

## Architecture (do not improvise — follow exactly)

**Layer 1 (deterministic Python):** `python3 tools/site_audit.py --root <path>` — walks the site repo, runs 12 mechanical checks on HTML/CSS/JS files, prints findings to stdout, generates `.tmp/site_audit_map.json` (metadata-only site map).

**Layer 2 (Opus subagent in isolated context):** Spawn an Explore-type subagent with `model: "opus"` so the analysis runs in a fresh context window — your main session never sees the site map or any file contents Layer 2 reads. Only the structured findings list crosses back into your conversation.

**Combined:** Both layers' findings get displayed as one numbered list, mechanical and conceptual interleaved by severity. The user picks ONE number; you then read ONLY the affected file(s) and propose a fix together.

## Step-by-step instructions

### Step 0 — Determine the site root

If `$ARGUMENTS` contains a path, use it. Otherwise:
1. Check if the current working directory contains `.html` files — if so, use CWD.
2. Else ask the user for the site root.
3. If neither works, ask the user for the path and STOP.

### Step 1 — Run Layer 1

```bash
python3 tools/site_audit.py --root "<site_root>"
```

This prints structured findings to stdout AND writes `.tmp/site_audit_map.json`. Capture both.

If the tool errors out, surface the error to the user and STOP.

### Step 2 — Spawn Layer 2 subagent

Use the Agent tool with these EXACT parameters:

```
subagent_type: "Explore"
model: "opus"
description: "Layer 2 conceptual site audit"
prompt: <see verbatim prompt below>
```

**Verbatim Layer 2 prompt** (substitute `{{SITE_ROOT}}` with the actual path):

> You are running Layer 2 of the site_audit workflow for the website at `{{SITE_ROOT}}`. A deterministic Python audit (Layer 1) has already run and produced a site map at `.tmp/site_audit_map.json` (in the agentic-workflow repo root). Your job: find CONCEPTUAL issues that the mechanical checker cannot catch.
>
> **INPUT:** read `.tmp/site_audit_map.json` first. It contains metadata for every HTML page, CSS file, and site structure. This is your PRIMARY source of truth.
>
> **PERMISSIONS:**
> - Use Read freely on `.tmp/site_audit_map.json`.
> - You MAY read up to 5 specific files in the website repo to drill into something the site map hints at. NO MORE.
> - DO NOT load entire directories. DO NOT grep across the whole repo.
> - DO NOT echo file contents in your response — only paths, line numbers, and one-line descriptions.
> - Do not write to any files.
>
> **CONCEPTUAL CATEGORIES TO LOOK FOR** (return findings in any combination of these):
>
> 1. `architecture_smell` — the site has patterns that imply it needs a template system but doesn't have one (e.g., many pages with near-identical structure). Look at page count, shared CSS refs, and inline script duplication from the site map.
> 2. `ux_inconsistency` — different pages have different navigation, CTA patterns, or form layouts. Compare page metadata across the site map entries.
> 3. `seo_strategy_gap` — pages target similar keywords without differentiation, or there is no clear internal linking strategy. Check titles, descriptions, and internal_links arrays.
> 4. `content_hierarchy` — heading structure doesn't match page purpose (e.g., course page h1 is generic, not course-specific). Check heading_sequence in the site map.
> 5. `conversion_path_break` — the user journey from landing to form submission has friction (e.g., pages with no forms, CTAs linking to external pages, inconsistent form targets). Check form_snippets and internal_links.
> 6. `design_system_gap` — CSS variables defined but underutilized, or multiple conflicting style patterns. Check css_files variables_defined against page count and structure.
> 7. `performance_architecture` — site-level performance patterns (all pages loading the same heavy assets, no code splitting, redundant external dependencies).
>
> **OUTPUT FORMAT (strict, no exceptions):**
>
> Return a markdown list of findings. NO preamble, NO summary, NO commentary. Just the findings. Each one in this exact shape:
>
> ```
> [CONCEPTUAL] <category_snake_case>
>     <relative/path/to/affected/file>
>     → <one-line description of the conceptual issue>
>     Fix: <one-line suggestion>
> ```
>
> Maximum 6 findings total. Order by severity (most concerning first). Quality over quantity.
>
> If you find ZERO real conceptual issues, return exactly:
>
> ```
> NO_CONCEPTUAL_FINDINGS
> ```
>
> Begin now. Read the site map first.

### Step 3 — Combine findings into one list

Take Layer 1 stdout (which already has its own numbered list `[1]`, `[2]`, ...) and append Layer 2's findings, continuing the numbering from where Layer 1 stopped.

Print to the user in this exact shape:

```
===============================================================
SITE AUDIT — <site root> — <timestamp>
Layer 1: <N> mechanical findings
Layer 2: <M> conceptual findings (subagent took <T>s)
===============================================================

<Layer 1 findings exactly as printed by tools/site_audit.py>

──────── CONCEPTUAL ────────
[N+1] [CONCEPTUAL] <category>
    <path>
    → <description>
    Fix: <fix>

[N+2] ...

===============================================================
Pick ONE finding to discuss in detail.
Reply with the number, "explain N" for more context,
or "skip" to bail out.
===============================================================
```

If Layer 2 returned `NO_CONCEPTUAL_FINDINGS`, say "Layer 2: 0 conceptual findings" and skip the CONCEPTUAL section.

### Step 4 — Wait for the user to pick

Stop and wait. Do NOT proceed to fix anything until the user replies with a number, "explain N", or "skip".

**On a number reply:** read the affected file(s) — and ONLY those file(s). Discuss the issue, propose a specific fix, wait for go-ahead.

**On "explain N":** read just enough to give a 2-3 sentence elaboration. Do not propose a fix yet.

**On "skip":** acknowledge and stop.

### Step 5 — Apply the fix (one finding only)

When the user approves a fix:
- Make the change with Edit or Write
- Re-run `python3 tools/site_audit.py --root "<site_root>" --mechanical-only --checks <relevant_check>` to confirm the finding is gone
- Show the before/after delta

**Hard rule: only fix ONE finding per invocation.**

## Important constraints

1. **Never echo file contents from the site map or from Layer 2 into the user-facing output.** Findings only contain paths and one-line descriptions.
2. **Never read more than necessary.** If the user picks finding [3], read that file only.
3. **The subagent's context is discarded.** Only the structured findings list crosses back.
4. **One fix per invocation.** Re-run for more.
5. **If Layer 2 fails or times out, fall back to Layer 1 only.** Still useful.

## See also

- [tools/site_audit.py](../../../tools/site_audit.py) — the Layer 1 implementation
- [workflows/site_audit.md](../../../workflows/site_audit.md) — the SOP and review-loop documentation
