---
name: ui-visual-calibration
description: Translate fuzzy visual taste ("clean", "modern", "like Notion") into concrete structural decisions — Layout Archetype, Density, Shape Language, Surface Style, Palette Guidance — before any blueprint work begins. Use this skill whenever a user describes aesthetic preferences in vague terms, references a product they admire, or starts layout work without an agreed visual language. The output is a visual-calibration.md file that all downstream blueprint and component work references.
status: stable
---

# UI Visual Calibration

Translates vague aesthetic words and product references into a locked set of concrete visual decisions. Every decision in this file should be traceable to something the user said — not to the model's default taste. This document becomes the visual contract that `ui-blueprint`, `ui-component-spec`, and `ui-system` reference when making layout and styling choices.

## When to use this skill

Use this skill when:
- The user provides vague aesthetic words: "clean", "modern", "minimal", "professional", "sleek".
- The user references a product they like: "make it feel like Notion", "I want it to look like Linear", "something like Stripe's dashboard".
- The user is starting blueprint work and no visual-calibration.md exists yet.
- **Spec Recovery:** An implementation exists but no visual calibration sheet was created. Use this to document the as-built visual language and define the target visual language.
- A visual-calibration.md exists but is out of date after a brand change, a pivot, or a design direction reset.

Do **not** use this skill when:
- A current, approved visual-calibration.md already exists. Read it and reference it instead — do not re-run calibration and introduce conflicting decisions.
- The user is asking a narrow technical question that doesn't involve aesthetic choices (e.g. "what's the WCAG contrast ratio for large text?").

## Core principle

**Every vague word is a liability.** When the model encounters "clean" without translation, it makes a silent decision — likely the wrong one. This skill forces every vague aesthetic signal to become an explicit, user-confirmed choice before layout work begins. Unresolved vagueness at this stage multiplies into mismatched blueprints, mismatched components, and wasted revision cycles downstream.

## Observed vs. Target (Spec Recovery protocol)

When using this skill for **Spec Recovery**, distinguish between the current aesthetics and the intended style:

- **Observed Visual Language:** The density, shape language, and Surface Style as they exist in the current implementation.
- **Target Visual Language:** The desired aesthetic direction (e.g., if the user wants to keep the sidebar but make the palette "cleaner").
- **Gap:** Inconsistencies or accidental aesthetic choices in the current UI.

Use this to ensure the calibration sheet serves as a ground truth for intent, not just a description of implementation artifacts.

## Workflow

### Step 1 — Extract vague words

Read the user's message and pull out every word that describes appearance, feeling, or style without specifying a concrete visual property. Common examples: clean, modern, minimal, professional, sleek, premium, fun, playful, bold, corporate, edgy.

List each word. Do not translate yet — just collect them. If the user also named a reference product (Notion, Linear, Stripe, Vercel, GitHub), note it separately.

### Step 2 — Map each word using the vague-language-translator

For each extracted word, look it up in `shared/references/vague-language-translator.md` and list its translation options. The translator gives a set of concrete properties — do not pick one arbitrarily.

Example:
- "Modern" → Flat surface styles, large radius, muted palette, contemporary type, generous spacing
- "Clean" → More whitespace, fewer borders, lower color variety, simpler hierarchy

Where a word is not in the translator, break it down to its most plausible concrete properties and mark it as an assumption.

### Step 3 — Confirm with the user or flag as assumption

For each translation, do one of the following:
- **Confirm:** Ask the user to choose from the translation options. ("You said 'clean' — does that mean more whitespace, fewer borders, or both?")
- **Flag as assumption:** If the user is unavailable or has already moved on, record the translation as an assumption with a ⚠️ marker. Never silently adopt a translation without marking it.

If the user named a reference product, ask what specifically they like about it. "Notion-style" could mean sidebar navigation, dense content layout, muted palette, or all three — get a specific answer. If they can't say, flag the product reference as an assumption and extract the most commonly associated properties.

### Step 4 — Make each decision concrete

Using the confirmed (or assumed) translations, map everything to the five visual dimensions from `shared/references/visual-vocabulary.md`:

| Dimension | Source vocabulary |
|---|---|
| Layout Archetype | Sidebar App / Centered Card / Split Panel / Dashboard Grid / Wizard |
| Density | Sparse / Medium / Dense — with Tailwind token examples |
| Shape Language | Sharp (0–2px) / Mildly Rounded (4–8px) / Pill-like (rounded-full) |
| Surface Style | Flat / Outlined / Elevated / Glassy / Card-heavy |
| Palette Guidance | Describe in words (e.g. "muted neutrals with a single blue accent") |

Each dimension must resolve to exactly one value. If the user's input creates a conflict (e.g. "edgy but also friendly"), surface the contradiction as an open question — do not split the difference silently.

### Step 5 — Produce the visual-calibration.md output

Use the output template below. Save as `visual-calibration.md` in the spec package directory. Do not rename the file — downstream skills reference it by this name.

Before delivering, validate against the acceptance criteria at the bottom of this file.

## Output template

Always produce output in this exact structure.

```markdown
---
spec_type: visual-calibration
spec_id: <short-slug matching the brief slug, e.g. "billing-overview">
created: <YYYY-MM-DD>
based_on: brief-<slug>
status: draft
---

# Visual Calibration Sheet: <descriptive title>

## Translation Log

| User's word / phrase | Translator match | Concrete properties used | Confirmed or assumed |
|---|---|---|---|
| "clean" | Clean → More whitespace, fewer borders, lower color variety | Gap-8, p-8 spacing; no decorative borders | ✅ Confirmed by user |
| "modern" | Modern → Flat Surface Style, large radius, muted palette | Flat surface style; rounded-lg corners | ✅ Confirmed by user |
| "like Notion" | Not in translator — assumed sidebar nav, medium density, muted neutrals | Sidebar App archetype; Medium density | ⚠️ Assumed — user did not specify what they like about Notion |

## Concrete Visual Decisions

- **Layout Archetype:** <one value from visual-vocabulary.md — e.g. Sidebar App>
- **Density:** <one value — Sparse / Medium / Dense>
  - Tailwind tokens: `<e.g. gap-4, p-4, leading-normal>`
- **Shape Language:** <one value — Sharp / Mildly Rounded / Pill-like>
  - Tailwind tokens: `<e.g. rounded-md to rounded-lg>`
- **Surface Style:** <one value — Flat / Outlined / Elevated / Glassy / Card-heavy>
  - Tailwind tokens: `<e.g. shadow-none, solid background>`
- **Palette Guidance:** <describe in plain words — e.g. "Muted neutral base (gray-50 to gray-900) with a single indigo accent (indigo-600). No vibrant secondary colors.">

## Reference Products

<Only include this section if the user named products. If none were named, omit entirely.>

| Product | What the user wants to borrow | What to avoid from it |
|---|---|---|
| <e.g. Notion> | <e.g. Sidebar navigation, calm neutral palette, high text density> | <e.g. User did not mention it, so do not copy the block-editor content model> |

## Open Questions

<Numbered list of unresolved conflicts or decisions that need the user's answer before blueprint work begins. If none, write "None — all decisions confirmed.">

1. <e.g. "Density: user said 'clean' (implies sparse) but the feature requires a data table. Should the table use Dense density while the rest of the UI uses Sparse?">

## Assumptions

<List every assumption flagged ⚠️ in the Translation Log, restated here for easy review. If none, write "None.">

- ⚠️ ASSUMED: <the assumption>
```

## Example

**User says:** "I want the dashboard to feel clean and modern — kind of like how Notion feels."

### Step 1 output (extracted words):
- Vague words: "clean", "modern"
- Reference product: Notion

### Step 2 output (mapped):
- "Clean" → More whitespace, fewer borders, lower color variety, simpler hierarchy
- "Modern" → Flat surface styles, large radius, muted palette, contemporary type, generous spacing
- "Notion" → Not in translator. Common Notion associations: sidebar app layout, medium-to-dense text content, muted neutral palette (gray/beige), minimal chrome, card surfaces.

### Step 3 output (confirmed):
Model asks: "You mentioned 'clean and modern, like Notion' — a few quick questions: (1) Does clean mean more whitespace and fewer borders, or primarily fewer colors? (2) Notion is medium-density — is that right for your dashboard, or do you want it sparser? (3) What specifically do you like about Notion — the sidebar, the calm palette, or the block-based layout?"

User replies: "Whitespace and fewer borders, yes. Medium density is right. I like the sidebar and the calm palette — not the block layout."

### Step 4 + Step 5 output:

```markdown
---
spec_type: visual-calibration
spec_id: main-dashboard
created: 2026-05-06
based_on: brief-main-dashboard
status: draft
---

# Visual Calibration Sheet: Main Dashboard

## Translation Log

| User's word / phrase | Translator match | Concrete properties used | Confirmed or assumed |
|---|---|---|---|
| "clean" | Clean → More whitespace, fewer borders, lower color variety | Generous padding (p-8), no decorative borders, two-color palette | ✅ Confirmed |
| "modern" | Modern → Flat surface styles, large radius, muted palette, generous spacing | Flat surface style; rounded-lg corners; muted gray base | ✅ Confirmed |
| "like Notion — sidebar and calm palette" | Not in translator — extracted: sidebar nav, muted neutrals, minimal chrome | Sidebar App archetype; gray-50 to gray-900 palette | ✅ Confirmed (block-layout excluded) |

## Concrete Visual Decisions

- **Layout Archetype:** Sidebar App
- **Density:** Medium
  - Tailwind tokens: `gap-4`, `p-4`, `leading-normal`
- **Shape Language:** Mildly Rounded
  - Tailwind tokens: `rounded-md` to `rounded-lg`
- **Surface Style:** Flat
  - Tailwind tokens: `shadow-none`, solid background
- **Palette Guidance:** Muted neutral base (gray-50 to gray-900). Single accent color (slate-700 for primary actions). No vibrant secondaries.

## Reference Products

| Product | What the user wants to borrow | What to avoid from it |
|---|---|---|
| Notion | Sidebar navigation, calm neutral palette, minimal chrome | Block-editor content model (user explicitly excluded this) |

## Open Questions

None — all decisions confirmed.

## Assumptions

None.
```

## Anti-patterns

1. **Never invent concrete properties without tracing them to the user's input or a confirmed translation.** If a Density choice of "Sparse" does not appear in the Translation Log with a user-provided or translator-derived source, remove it or flag it as an assumption.
2. **Do not conflate Layout Archetype with Density.** They are independent dimensions. A Sidebar App can be Sparse or Dense. A Centered Card can be Dense. Treat them separately.
3. **Do not skip the Translation Log.** The log is the audit trail that prevents silent drift. Without it, later sessions cannot tell whether a decision was user-confirmed or model-invented, and calibration quietly unravels.
4. **Do not resolve conflicts between vague words silently.** If the user says "premium but also playful", do not average the two. Surface the contradiction in Open Questions.
5. **Do not re-run calibration when an approved sheet exists.** Running calibration twice without archiving the first version creates conflicting ground truth. If an update is needed, explicitly supersede the previous sheet and note what changed.

## Acceptance criteria for this skill's output

A visual-calibration.md produced by this skill is acceptable only if every one of these is true:

- [ ] Frontmatter is present with spec_type, spec_id, created date, and status.
- [ ] Translation Log is present and has one row for every vague word or reference product the user provided.
- [ ] Every row in the Translation Log has a "Confirmed or assumed" value — no row is blank.
- [ ] Every assumption is marked ⚠️ in the Translation Log and restated in the Assumptions section.
- [ ] All five Concrete Visual Decisions are present (Layout Archetype, Density, Shape Language, Surface Style, Palette Guidance) — none are omitted.
- [ ] Each Concrete Visual Decision resolves to exactly one value from visual-vocabulary.md (no ranges, no "either/or").
- [ ] Density entry includes at least one Tailwind token example.
- [ ] Shape Language entry includes at least one Tailwind token example.
- [ ] If the user named a reference product, the Reference Products section is present. If they named none, the section is absent.
- [ ] No vague words (clean, modern, minimal, professional, sleek, premium, etc.) appear in the Concrete Visual Decisions section without being translated into a structural property.

If any check fails, revise before delivering.

---

## Promotion checklist

Complete every item before changing `status: draft` to `status: stable`.

### Evidence on the settings-page fixture

- [ ] Running this skill against `examples/settings-page/brief.md` produces a `visual-calibration.md` that passes every item in the Acceptance criteria above.
- [ ] The output's Translation Log is non-empty — the settings-page brief contains at least one vague or implicit design preference that is translated.
- [ ] All five Concrete Visual Decisions are present in the output and none conflict with the settings-page brief constraints.

### Evidence on the spec-recovery-create fixture

- [ ] Running this skill against `examples/spec-recovery-create/brief.md` produces output consistent with `examples/spec-recovery-create/visual-calibration.md`.
- [ ] The Observed vs Target distinction from the recovery brief is reflected in the output (e.g., inconsistent border radii documented in Observed; single radius value specified in Target).

### Regression: does not invent decisions

- [ ] Given a brief with no visual preferences at all (only goal and user), the output marks every Concrete Visual Decision as ⚠️ assumed and lists all five in the Assumptions section.
- [ ] The skill does not silently default to any visual language — every default is explicit.

### Skill integration

- [ ] `validate-skill.py` passes for this skill with `status: stable` (no missing sections).
- [ ] `skills.json` entry for `ui-visual-calibration` has been updated to `"status": "stable"`.
- [ ] README Skill Map table has been updated to show `stable`.
