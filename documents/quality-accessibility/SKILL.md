---
name: quality-accessibility
description: Audit AICP for accessibility concerns in operator-facing surfaces — terminal CLI output (color contrast / screen-reader compatibility / Unicode dependence), interactive UI (`--dashboard`, `--interactive`), generated documentation (markdown links / table semantics). LOW APPLICABILITY for AICP (a backend AI platform) — this skill exists for completeness but most accessibility work belongs in fleet-facing UIs (Mission Control). Loads when the operator says "accessibility audit" / "color-blind safe" / "screen-reader compat" / "WCAG check" / "is the CLI usable without color".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: low
---

# quality-accessibility

Audit AICP's operator-facing surfaces for accessibility. AICP is a backend
AI platform (per CLAUDE.md `## Identity Profile`); accessibility scope here
is narrow: CLI terminal output (rich-formatted), interactive UIs
(`--dashboard`, `--interactive`), generated docs (markdown). Most
accessibility concerns in the broader fleet ecosystem live in **Mission
Control** (the fleet-facing web UI), NOT AICP.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "accessibility audit", "WCAG check",
  "color-blind safe", "screen-reader compat", "is the CLI usable without
  color"
- **CLI legibility**: operator notices `aicp --check` output relies on
  red/green coloring that's hard to read for color-blind users
- **Documentation accessibility**: review markdown for missing alt text
  on images, complex tables without summaries, or color-only meaning

Do NOT load when:

- The concern is fleet UI accessibility — Mission Control is a separate
  project; load the fleet's accessibility skill there
- The concern is general code quality (load `quality-audit` for the
  umbrella view; this skill is specifically a11y)
- The concern is performance (load `quality-performance`)

## Operations

### Operation 1 — Audit CLI color usage

**When**: verify rich-formatted CLI output works without color (e.g., for
operators piping to a file, using a non-color terminal, or with color-blindness).

**Process**:

1. Identify color usage in `aicp/cli/main.py` and `aicp/cli/dashboard.py`:
   `Grep -nE "console\.print.*\[(red|green|yellow|cyan|magenta|blue)\]"`
2. For each color use, ask: does the meaning depend ONLY on color?
   - GOOD: `[green]OK[/]` — color reinforces text "OK" (text alone conveys meaning)
   - BAD: just `[red]●[/]` with no text label — meaning is color-only
3. Check for `--no-color` / `NO_COLOR` env var support — rich respects
   `NO_COLOR=1` automatically; verify by running `NO_COLOR=1 aicp --check`
4. Recommend text labels alongside color codes for any BAD cases found

**Quality bar**: every color in CLI output should be REDUNDANT with text
content. Color reinforces; text carries meaning.

### Operation 2 — Audit interactive UI (`--dashboard`)

**When**: the live dashboard relies on visual layout that may not work
for screen reader users or low-vision operators.

**Process**:

1. Read `aicp/cli/dashboard.py` to understand the rich.Layout structure
2. Note: rich's Live + Layout uses ANSI escape sequences that screen
   readers cannot parse. The dashboard is fundamentally a sighted-user
   tool.
3. For accessibility-required workflows, recommend the alternative
   non-interactive surfaces:
   - `aicp --check` (one-shot, text-only output)
   - `aicp --metrics` (one-shot, text + table)
   - `aicp --observe` (one-shot snapshot)
4. Document the alternative-surface mapping in operator-facing docs if
   not already present

**Quality bar**: never claim the live dashboard is accessible. Recognize
its fundamental ANSI dependency and route accessibility-required users
to the snapshot-style alternatives.

### Operation 3 — Audit generated documentation

**When**: AICP-generated markdown (wiki/, docs/, generated reports) needs
to be accessible to screen-reader users consuming via VS Code or similar.

**Process**:

1. Inspect generated markdown for: alt text on images (rare in AICP),
   header hierarchy continuity (no h1→h3 skips), table caption attributes
2. AICP's wiki content (per `wiki/config/templates/`) generally has
   good semantic structure; verify no recent template drift
3. Skip image alt text concerns — AICP doesn't generate images in docs

**Quality bar**: header hierarchy must be continuous. Tables in wiki
content benefit from clear column headers but rarely need aria-* in
markdown context.

## Gotchas

- **Detection**: agent treats the live `--dashboard` as accessible.
  **Rule**: ANSI live-update is fundamentally inaccessible to screen
  readers; route to snapshot alternatives.
  **Reasoning**: rich.Live emits cursor-positioning escape codes that
  screen readers cannot interpret. Operators with screen reader needs
  use `--check`/`--metrics`/`--observe` instead.

- **Detection**: agent makes broad accessibility claims about AICP.
  **Rule**: AICP is a backend AI platform with narrow operator-facing
  surface. Accessibility scope is terminal CLI + generated docs ONLY.
  Don't audit non-existent UIs.
  **Reasoning**: scoping correctly avoids producing useless audit reports
  about UIs AICP doesn't have.

- **Detection**: agent confuses AICP accessibility with Mission Control accessibility.
  **Rule**: Mission Control is a separate project; its accessibility belongs
  to its own a11y skill, not this one.
  **Reasoning**: AICP exposes inference; Mission Control is the fleet UI.
  Different projects, different a11y scopes.

## Reference exemplars

- `aicp/cli/main.py` `_run_check()` line 771+ — uses [green]/[red]/[yellow]
  with text labels (good pattern)
- `aicp/cli/dashboard.py` — fundamentally inaccessible (rich.Live);
  document alternative surfaces
- Rich library's `NO_COLOR` env var support — built-in, no extra config

## Domain context

AICP operator-facing surface is narrow: Python CLI with rich-formatted
output. Most operator interaction is through `aicp <subcommand>` calls
producing terminal output. The live dashboard (`--dashboard`) is the
only interactive UI. Per CLAUDE.md `## Identity Profile` Type=product,
AICP serves operators (single-user) and the fleet (programmatic) — neither
demands extensive a11y work, but CLI hygiene (color-redundant text labels)
is universally good practice.

## Related skills

| Skill | When to use |
|-------|-------------|
| `quality-audit` | Umbrella quality review including this skill's scope |
| `quality-lint` | When CLI output has style issues (different from a11y) |
| (Mission Control's a11y skill) | When the concern is fleet-facing web UI accessibility |
