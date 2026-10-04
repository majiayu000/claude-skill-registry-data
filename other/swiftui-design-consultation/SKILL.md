---
name: swiftui-design-consultation
description: |
  Apple-canon design system for SwiftUI projects: writes DESIGN.md plus a
  DesignSystem Swift Package, then runs a HIG-budgeted native review. Use
  when starting or refreshing a SwiftUI design system.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
  - ToolSearch
  - Artifact
  - mcp__swiftui-rag__corpus_info
  - mcp__swiftui-rag__search_swiftui_corpus
  - mcp__swiftui-rag__index_project
  - mcp__swiftui-rag__search_project
  - mcp__swiftui-rag__swift_typecheck
  - mcp__swiftui-rag__review_macos_hig
  - mcp__swiftui-rag__review_liquid_glass
  - mcp__swiftui-rag__review_accessibility
upstream_skills:
  - office-hours-track-aware (typical entry — writes .gstack/track first)
chains_to:
  - apple-native-review (platform read from .gstack/track)
---

# /superpowers-gstack:swiftui-design-consultation

Apple-canon design system consultation for SwiftUI projects. Output:
`DESIGN.md` + `DesignSystem/` Swift Package, reviewed against a HIG
conformance budget. The proposal is previewed as an Artifact page before
approval; `DESIGN.md` itself is the committed artefact — no `DESIGN.html`
is generated or committed. `templates/` and `bin/` live NEXT TO this
SKILL.md, not in the user's project: set `SKILL_DIR` to this skill's base
directory (shown when the skill loads) and address assets as `$SKILL_DIR/…`.

## Phase 0 — Setup

### Step 0.0: Initialize gstack helpers (set $SLUG)

Per-project state lives under `~/.gstack/projects/$SLUG/`, so `$SLUG`
(the gstack project identifier derived from the git remote) is set first.

```bash
SLUG_OUTPUT=$(~/.claude/skills/gstack/bin/gstack-slug 2>/dev/null)
[ -n "$SLUG_OUTPUT" ] && eval "$SLUG_OUTPUT"
if [ -z "${SLUG:-}" ]; then
  # Fallback: git toplevel basename, or pwd basename outside a repo.
  SLUG="$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")"
  export SLUG
fi
if [ -z "$SLUG" ] || [ "$SLUG" = "/" ]; then
  echo "FATAL: could not derive SLUG. Aborting." >&2
  exit 1
fi
mkdir -p ~/.gstack/projects/"$SLUG"
echo "SLUG: $SLUG"
```

### Step 0.1: Track self-bootstrap (inline platform question)

```bash
mkdir -p .gstack
if [ ! -f .gstack/track ] || [ -z "$(cat .gstack/track 2>/dev/null | tr -d '[:space:]')" ]; then
  echo "TRACK_MISSING"
else
  echo "TRACK: $(cat .gstack/track | tr -d '[:space:]')"
fi
```

If output is `TRACK_MISSING`, ask the platform question inline (the standard
flow asks it in `/superpowers-gstack:office-hours-track-aware`):

```
D0 — Which platform target does this project ship to?
ELI10: iPhone/iPad, Mac, or both — so the generated Package.swift and
  design defaults match. Set once per project; read by all swiftui-* skills.
Stakes if we pick wrong: wrong platforms in Package.swift; easy to re-run.
Recommendation: iOS only (most common for new projects)
A) iOS only (recommended) — iPadOS comes with the iOS target; smallest surface
B) macOS only — menu-bar tools, productivity apps, system utilities
C) Both iOS + macOS — max reach; more #if os() surfaces, longer compiles
```

Write the chosen value (`ios`, `macos` or `both`) and re-read it:

```bash
echo "$CHOICE" > .gstack/track
TRACK=$(cat .gstack/track | tr -d '[:space:]')
echo "TRACK: $TRACK"
```

`$TRACK` must be `ios`, `macos` or `both`; otherwise STOP: `BLOCKED — invalid .gstack/track value`.

### Step 0.2: Detect project mode

```bash
MODE="greenfield"
if find . -maxdepth 3 -type f \( -name "*.xcodeproj" -o -name "Package.swift" -o -name "*.swift" \) 2>/dev/null | head -1 | grep -q .; then
  MODE="existing"
fi
echo "MODE: $MODE"
```

### Step 0.3: Verify MCP surface

Call `mcp__swiftui-rag__corpus_info` (no arguments). The returned JSON
must have `runtime_version` (string), `sample_count` (> 0), `hig_rules`
(≥ 11 entries) and `accessibility_rules` (≥ 3 entries). Otherwise STOP:
`BLOCKED — swiftui-rag MCP unavailable. Run /sync-gbrain or check pipx install.`

Before calling any other `mcp__swiftui-rag__*` tool, load its schema via
ToolSearch and use the parameter names it reports.

### Step 0.4: Existing-project indexing

If `MODE` is `existing`, call `mcp__swiftui-rag__index_project` with the
repo root path and keep the returned project ID for Phase 1.

### Step 0.5: Read existing DESIGN.md if present

If `DESIGN.md` exists, read it: this is a refresh consultation, and
Phase 2 will offer keep / replace / refine per pillar.

## Phase 1 — Product Context

One combined AskUserQuestion brief with three fields. Platform is already
in `.gstack/track`; do not re-ask.

### Step 1.1: Pre-fill from project context

If `README.md` or `CLAUDE.md` exist, read them and extract product name,
audience and space/industry to pre-fill the brief.

If `MODE` is `existing`, call `mcp__swiftui-rag__search_project` with
`"Color extension"`, `"Font.system\|Font.custom"`,
`"\.material\|\.glassEffect"` and `"Color(red:"` (non-semantic colors, a
quality signal). Cache the counts: `N Color extensions, M Font
declarations, K material usages, X non-semantic colors flagged`.

### Step 1.2: Ask the combined Phase 1 question

```
D1 — Product context for the SwiftUI design system
ELI10: I need what the product IS, what feeling it should evoke (one
  anchor every later choice serves), and how strict the HIG bar is.
Stakes if we pick wrong: a vague memorable-thing gives a generic app; a
  loose budget lets POLISH findings pile up; an unclear audience mis-tunes
  defaults (productivity density vs reader whitespace).
Field 1 — Product context confirm/refine [pre-filled if found]
Field 2 — Memorable Apple thing: "What's the one Apple-native quality this
  app should be remembered for after first launch?" One sentence, e.g.
  "as fluid as Things", "as sharp as Linear-mac", "as quiet as Reeder".
Field 3 — HIG conformance budget
  A) Recommended: 0 CRITICAL · 0 SIGNIFICANT · ≤5 POLISH
  B) Strict: 0 / 0 / 0 (must feel Apple-native on first launch)
  C) Relaxed: 0 / 3 / 10 (early prototype)
```

If `MODE` is `existing`, prepend: `I indexed your project. Current
patterns: $N Color extensions, $M Font declarations, $K material usages,
$X non-semantic colors flagged. We can keep, replace, or refine each.`

### Step 1.3: Store the answer

Cache the answers in `~/.gstack/projects/$SLUG/swiftui-consultation-state.json`
with keys `track`, `product_context`, `memorable_thing`, `budget`
(`critical`/`significant`/`polish`), `mode`, `existing_patterns`. This
state survives /clear, so a long consultation can resume.

## Phase 2 — Proposal (Artifact preview + approval)

### Step 2.1: Ground each pillar in the corpus

Query `mcp__swiftui-rag__search_swiftui_corpus` per pillar, passing
`platform` from `$TRACK`: Typography `"typography roles SF Pro semantic
font"`, Color `"semantic color asset catalog dark mode adaptive"`,
Materials `"Liquid Glass material chrome content layer"`, Motion `"spring
animation snappy smooth named easing"`, Accessibility `"VoiceOver Dynamic
Type contrast accessibility"`. Each returns 3–5 corpus samples plus
HIG-page citations; they ground every proposed choice.

### Step 2.2: Write the proposal as Markdown

```bash
TS=$(date +%Y%m%d-%H%M%S)
PROPOSAL_PATH=~/.gstack/projects/"$SLUG"/design-proposal-"$TS".md
```

Write `$PROPOSAL_PATH` directly as Markdown. It is the single source of
truth: Phase 3 fills both `DESIGN.md` and the Swift templates from it, so
every section must carry concrete, named values — not only prose.

- H1 `Design Proposal: $PRODUCT_NAME`, then a metadata line with date,
  track, product context, memorable thing and aesthetic direction.
- H2 per pillar, each with rationale, HIG citation links and a table of
  choices: **Typography** (roles → `Font.TextStyle`), **Color** (brand
  hex values with light/dark backgrounds; semantic → system colors),
  **Materials** (where glass goes / doesn't), **Spacing & Radii** (named
  point constants), **Motion** (named presets with spring parameters),
  **Accessibility**, **Platforms** (per-track assertions).
- H2 **HIG Conformance Budget** (the Phase 1 numbers) and H2
  **Decisions Log** (one bullet per decision with its reason).

In refresh mode, mark each pillar `keep` / `replace` / `refine` against
the existing `DESIGN.md`.

### Step 2.3: Preview and ask approve / drill / change

Publish the proposal as a page with the Artifact tool (load the
`artifact-design` skill first) so the user reads it before approving:
typography specimens, color swatches in light and dark, material
placement, motion presets, budget panel and decisions log. Give the user
the link, then ask:

```
D2 — Does the proposed design system look right?
ELI10: The proposal page is published; pick approve, drill, change or restart.
A) Approve — write DESIGN.md + Swift Package now (recommended if it feels right)
B) Drill into [pillar] — tighten one pillar without committing the others
C) Change [pillar] — different direction for one pillar
D) Start over — rebuild the whole proposal with different constraints
```

If `A`: proceed to Phase 3. If `B` or `C`: ask which pillar, re-query
that pillar's corpus, rewrite that section, republish the same page, loop
back to D2. If `D`: go back to Phase 1.

### Step 2.4: Cache the approved proposal

```bash
cp "$PROPOSAL_PATH" ~/.gstack/projects/"$SLUG"/swiftui-consultation-state.proposal.md
```

Phase 3 reads this copy; the timestamped file stays as the audit trail.

## Phase 3 — Write Artefacts (with native-review chain)

Both `DESIGN.md` and `DesignSystem/*` are filled from the cached proposal,
so prose and Swift declarations name the same roles, colors and presets.
If the proposal's track differs from `$TRACK`, STOP and AskUserQuestion
which is authoritative.

### Step 3.1: Generate DESIGN.md from template (with overwrite safety)

```bash
PROPOSAL=~/.gstack/projects/"$SLUG"/swiftui-consultation-state.proposal.md
[ -f "$PROPOSAL" ] || { echo "ERROR: no cached proposal — Phase 2 must complete first."; exit 1; }
if [ -f DESIGN.md ]; then
  BACKUP="DESIGN.md.backup-$(date +%Y%m%d-%H%M%S)"
  cp DESIGN.md "$BACKUP"
  echo "Existing DESIGN.md backed up to $BACKUP"
fi
```

Read `$SKILL_DIR/templates/DESIGN.md.template` and substitute every
`{{TOKEN}}` from the matching proposal section: `{{DATE}}`,
`{{PRODUCT_CONTEXT}}`, `{{MEMORABLE_THING}}`, `{{AESTHETIC_DIRECTION}}`
from the metadata line; the seven `{{*_PROSE}}` tokens from the pillar
sections; `{{BUDGET_CRITICAL}}`, `{{BUDGET_SIGNIFICANT}}`,
`{{BUDGET_POLISH}}` from the budget section; `{{DECISIONS_LOG}}` as the
bulleted list. Write to `<repo>/DESIGN.md`. Never leave a token
unresolved or substitute an empty string — a missing value means the
proposal is incomplete; return to Phase 2 for that pillar.

### Step 3.2: Generate the Swift Package (with overwrite safety)

```bash
if [ -d DesignSystem ]; then
  BACKUP_DIR="DesignSystem.backup-$(date +%Y%m%d-%H%M%S)"
  mv DesignSystem "$BACKUP_DIR"
  echo "Existing DesignSystem/ moved to $BACKUP_DIR"
fi
mkdir -p DesignSystem/Sources/DesignSystem/Resources DesignSystem/Tests/DesignSystemTests
```

Read each template under `$SKILL_DIR/templates/`, substitute its tokens
from the proposal, and write it to the mapped path under `DesignSystem/`:

| Template | Output path | Tokens (proposal section) |
|---|---|---|
| `Package.swift.template` | `Package.swift` | `{{PLATFORMS}}` (from `$TRACK`) |
| `Colors.swift.template` | `Sources/DesignSystem/Colors.swift` | `{{BRAND_COLORS}}`, `{{SEMANTIC_COLORS}}` (Color) |
| `Typography.swift.template` | `Sources/DesignSystem/Typography.swift` | `{{TYPE_ROLES}}` (Typography) |
| `Spacing.swift.template` | `Sources/DesignSystem/Spacing.swift` | `{{SPACING_CONSTANTS}}`, `{{RADIUS_CONSTANTS}}` (Spacing & Radii) |
| `Motion.swift.template` | `Sources/DesignSystem/Motion.swift` | `{{MOTION_PRESETS}}` (Motion) |
| `Materials.swift.template` | `Sources/DesignSystem/Materials.swift` | none |
| `HIGBudgetTests.swift.template` | `Tests/DesignSystemTests/HIGBudgetTests.swift` | none |
| `PlatformsTests.swift.template` | `Tests/DesignSystemTests/PlatformsTests.swift` | `{{DECLARED_TRACK}}`, `{{PLATFORM_ASSERTIONS}}` (Platforms) |

`{{PLATFORMS}}` per `$TRACK`: `ios` → `.iOS(.v26)`, `macos` →
`.macOS(.v26)`, `both` → `.iOS(.v26), .macOS(.v26)`. Render brand colors
as `Color` extensions backed by color sets under
`Sources/DesignSystem/Resources/Assets.xcassets/` (light, dark and
high-contrast variants), semantic colors as extensions onto system
colors, motion presets as `static let X: Animation`, spacing and radii as
`static let X: CGFloat`, platform assertions as `#if os(...)` test guards.

**WCAG contrast check.** For each brand hex, run
`$SKILL_DIR/bin/contrast-check.sh` once against the proposed light
background and once against the dark background:

```bash
if RESULT=$("$SKILL_DIR/bin/contrast-check.sh" "$BRAND_HEX" "$BG_HEX" 2>&1); then
  PASS=$(echo "$RESULT" | grep -o '"pass_aa_normal": [a-z]*' | awk '{print $2}')
else
  PASS="error"; echo "WARN: contrast-check failed for $BRAND_HEX vs $BG_HEX" >&2
fi
```

If `PASS` is `error` (likely `bc` missing or invalid hex), ask the user
whether to accept the color without a verified contrast; never treat an
empty result as a pass. If `PASS` is `false`, report the `ratio` from the
JSON, flag which background fails WCAG AA, and AskUserQuestion: keep the
hex (override) or pick another. The skill does not auto-adjust colors.

### Step 3.3: Type-check the generated Swift

Call `mcp__swiftui-rag__swift_typecheck` on the generated code with
target versions per `$TRACK`: `ios` → `["iOS-26.0"]`, `macos` →
`["macOS-26.0"]`, `both` → both. On failure, fix the offending file
(usually a missing `#if os()` guard) and retry; hard cap 3 attempts, then
STOP and report the diagnostic.

### Step 3.4: Native review, one fix pass, one re-run

Run the review chain once, fix CRITICAL findings, re-run once, and report
what remains against the budget.

**Spec-level review (DESIGN.md).** Read `DESIGN.md` into context, then
invoke the merged native review with the platform from `.gstack/track`:

```
Read(file_path="<absolute path>/DESIGN.md")
Skill(skill="superpowers-gstack:apple-native-review",
      args="platform=$TRACK. Review the DESIGN.md just loaded into context: the design system spec for a SwiftUI project; budget is $BUDGET_CRITICAL/$BUDGET_SIGNIFICANT/$BUDGET_POLISH.")
```

Capture its verdict and findings by severity (CRITICAL, SIGNIFICANT,
POLISH).

**Code-level review** (each `.swift` under `DesignSystem/Sources/DesignSystem/`).
The tools are complementary; run them in parallel per file with the same
`swift_code` argument — but only the ones that match `$TRACK`:

| Tool | Rules | Runs when |
|---|---|---|
| `mcp__swiftui-rag__review_macos_hig` | full macOS HIG ruleset (C1, C2, S1–S9) | `macos` or `both` — never on an `ios` track: its menu-bar and window findings would be fed into the fix pass and steer the proposal toward the wrong platform |
| `mcp__swiftui-rag__review_accessibility` | A1–A3 | always |
| `mcp__swiftui-rag__review_liquid_glass` | Liquid Glass subset (C1, S7, S8) | always |

Aggregate all findings, spec-level and code-level, deduplicated by
`(rule_id, file:line)` — the Liquid Glass tool repeats a subset of the
HIG tool's findings; count each once.

**Fix pass.** For every CRITICAL finding: edit the cached proposal
Markdown (the single source of truth — never patch `DESIGN.md` or
`DesignSystem/*` directly), regenerate from Step 3.1 onwards, type-check
again, then re-run the spec-level and code-level reviews exactly once.

**Report.** Compare the re-run counts with the Phase 1 budget. Within
budget: continue to Step 3.5 and print `DESIGN.md + DesignSystem/
committed. 0 CRITICAL · 0 SIGNIFICANT · 3 POLISH (within budget of 0/0/5).`
Over budget: list the remaining findings ranked by severity with
`file:line` and a proposed fix, then AskUserQuestion `(A) ship anyway,
(B) override the budget to the actual numbers, (C) refine manually now`;
only `A` and `B` continue to Step 3.5.

### Step 3.5: Commit (including the .gstack/track marker)

`.gstack/track` is a project-level decision and ships in the repo. If the
project ignores `.gstack/`, force-add the marker and record an exception
so future runs don't silently drop it:

```bash
if git check-ignore -q .gstack/track 2>/dev/null; then
  grep -q '^!\.gstack/track$' .gitignore 2>/dev/null || echo '!.gstack/track' >> .gitignore
  git add .gitignore
  git add -f .gstack/track
else
  git add .gstack/track
fi

git add DESIGN.md DesignSystem/
git commit -m "feat: scaffold design system via swiftui-design-consultation

- DESIGN.md: design source of truth (HIG-cited)
- DesignSystem/: Swift Package (semantic colors, SF Pro typography, Liquid
  Glass discipline, motion presets, accessibility baseline); its tests
  enforce the conformance budget at CI time

Track: $TRACK
HIG findings: $CRITICAL CRITICAL · $SIGNIFICANT SIGNIFICANT · $POLISH POLISH"
```
