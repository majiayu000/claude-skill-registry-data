---
name: pptx-template-modifier-skill
description: >-
  Extend a PowerPoint template when a slide_type layout is missing —
  borrows/clones layouts into template_new.pptx. Normal filling:
  pptx-generate-slide-skill.
license: Apache-2.0
compatibility: opencode
category: Presentation
---

## Running the snippets

Snippets read this skill's scripts via `os.environ['SKILL_DIR']` and the sibling slide-engine skill via `SLIDE_SKILL_DIR` (defaults to `../pptx-generate-slide-skill` next to `SKILL_DIR` — `requiresSkills` co-installs them side-by-side at every target). **Export once per session**, e.g.:

```bash
export SKILL_DIR=~/.config/opencode/skills/pptx-template-modifier-skill   # ← your install location
# optional: export SLIDE_SKILL_DIR=... if the slide skill is not a sibling
```

A missing `SKILL_DIR` export fails loud (`KeyError`) by design.

## What I do

> **Prerequisite skill:** `pptx-generate-slide-skill` — my output is rendered
> by its fill engine (`ppt_builder.generate_ppt_from_data`). Install it too:
> `npx github:darellchua2/civiltekk-opencode-claude-skills add pptx-generate-slide-skill`.
> This handoff is an intentional, allowlisted cross-skill dependency (#437);
> it is the only one in this catalog.

I am the **pptx-template-modifier-skill** (Capability B). When the base `template.pptx` is **missing a layout** that a slide needs, I extend the template by **borrowing/cloning a layout** into a derived `template_new.pptx`, which the `pptx-generate-slide-skill` engine then renders against.

I do **not** fill templates myself. Normal filling is the `pptx-generate-slide-skill` skill's job. I am invoked only when the base template is missing a layout a slide needs.

**Clone policy (the default is missing-only).** `resolve_and_clone` / `plan_resolution` take a `clone_on` argument (issue #47, "option A"):

- `clone_on="missing"` **(default)** — clone only when a slide_type's layout is genuinely missing/unknown. **Over-limit content (body larger than its placeholder) is NOT cloned** under this policy; it is logged as a warning and handled by the density downshift in `pptx-subagent` (Stage 2).
- `clone_on="any"` — also clone for over-limit content (the original Capability B behaviour). Opt-in; the agent never passes this.

## The 4 stakeholder steps

My pipeline mirrors the four steps a human designer performs:

1. **Read the template** — resolve the render contract via `ppt_builder.get_render_contract` (US-4.1: prefers the embedded JSON, falls back to the P0 introspection engine `template_introspector`) to get the full contract: layouts, placeholder fingerprints, `content_area_in2`, theme, slide size.
2. **Read the Slide Master** — `template_reader.read_master()` reads master-level placeholders + theme (on top of the contract).
3. **Understand the requirement** — `constraint_checker.evaluate_slide()` estimates the content area a slide needs (from its word count) and compares it against the layout's `content_area_in2`, yielding a **fits / over-limit** verdict. It also flags a `slide_type` whose layout is missing.
4. **Missing → create** — when a slide_type's layout is missing (the default `clone_on="missing"` policy), `state_machine.plan_resolution()` plans a clone; P4's `layout_creator` performs the actual XML/part clone into `template_new.pptx`. Under the default policy over-limit slides are **not** cloned (option A) — only missing-layout slides are.

## The `template_new.pptx` lifecycle (DESIGN §5)

Two file roles:

| File | Role |
|------|------|
| `template.pptx` | **Immutable base** (user-supplied, single authoritative path). |
| `template_new.pptx` | **Derived / ephemeral** — produced only when the base cannot satisfy a layout requirement. |

On **every** generation request, the state machine runs:

1. **① Delete leftover** — if `template_new.pptx` exists, delete it (force freshness; the base is re-evaluated each request).
2. **② Introspect base** — `get_render_contract` (embedded-preferred, sidecar fallback).
3. **③ Scan** — for each slide, check its fingerprint + content size against the contract; under the default `clone_on="missing"` policy, collect slides whose **layout is missing** into a clone plan (over-limit slides are logged as warnings, not cloned).
4. **④ Clone** (P4) — produce `template_new.pptx` with the extended layout(s); swap the active template.
5. **⑤ Notify** — whenever `template_new.pptx` is used, emit a **mandatory** user notice naming the template + the reason (`template.pptx could not fit <reason>`).

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/template_reader.py` | `read_master(template_path)` — Slide Master placeholders + delegated contract. |
| `scripts/constraint_checker.py` | `evaluate_slide(...)` / `check_content_area(...)` — over-limit verdict. |
| `scripts/state_machine.py` | `plan_resolution(...)` — the ①→②→③→⑤ lifecycle; `resolve_and_clone(...)` — the **full loop** (plan + clone + hand-off); `build_notification(...)` — the user notice. |
| `scripts/layout_creator.py` | `clone_for_over_limit(...)` — the 7-step XML/part clone into `template_new.pptx` (DESIGN §7). |

## Usage — the full Capability B loop

`resolve_and_clone(base, slides)` runs the whole pipeline: it plans (①②③), and when a slide_type's layout is missing it **clones an extended layout** into `template_new.pptx` (P4), then returns the active template + the layout-name pins + the mandatory notification. Hand the result to the `pptx-generate-slide-skill` engine:

```bash
python -c "
import sys, os
sys.path.insert(0, os.path.join(os.environ['SKILL_DIR'], 'scripts'))
sys.path.insert(0, os.path.normpath(os.path.join(os.environ.get('SLIDE_SKILL_DIR', os.path.join(os.environ['SKILL_DIR'], os.pardir, 'pptx-generate-slide-skill')), 'scripts')))
from state_machine import resolve_and_clone
from ppt_builder import generate_ppt_from_data, DEFAULT_OUTPUT_DIR

active, overrides, note = resolve_and_clone(
    'template/default.pptx',
    <SLIDE_DATA_LIST>,
)
out = generate_ppt_from_data(
    <SLIDE_DATA_LIST>,
    template_path=active,                 # base, or template_new.pptx when a clone was made
    config_overrides=overrides,           # pins the missing-layout slide_types to the extended layouts
    output_path=str(DEFAULT_OUTPUT_DIR / 'deck.pptx'),
)
print(out)
if note:
    print(note)                           # MANDATORY: tell the user template_new.pptx was used + why
"
```

If cloning fails, `resolve_and_clone` **safely falls back** to the base template (no derived file produced) — the deck still renders, just without the extended layout.

### Safety guarantees

- The base `template.pptx` is **never written** — clones save only to the derived `template_new.pptx`.
- **Reload-verify** after every clone: the cloned layout must be findable by `get_by_name`.
- **Rollback**: any clone/verify failure deletes `template_new.pptx` so a broken derived file is never left behind.

## When to use me

- A required `slide_type` has no matching layout in the template (the default `clone_on="missing"` trigger). → **Capability B** (donor clone).
- You explicitly want to clone for over-limit content too — pass `clone_on="any"` (by default over-limit is handled by density downshift in `pptx-subagent`, not here). → **Capability B**.
- The user supplies a **designer deck with an empty master** (one blank layout, zero placeholders, all branding baked per-shape) and asks to "make a reusable template" or "promote slides to master". → **Capability C** (designer promotion).

Do **NOT** use me for normal filling, chart generation, or image embedding — those are `pptx-generate-slide-skill`.

## Capability C — Promote Designer Slides to Empty Master (BT-142 Phase 3.4)

**Trigger:** the source PPTX has an empty Slide Master (one blank `DEFAULT` layout, zero placeholders) and N hand-crafted designer slides whose branding (fonts, colors, accent shapes) is applied **per-shape** rather than through the theme. This is the shape of a designer-built deck exported from PowerPoint without a saved Slide Master. End-user intent: mimic PowerPoint's **Slide Master view → Add Layout** (or right-click slide → "Add to Master"), turning the N designed slides into named layouts attached to the master.

Capability C reverse-engineers each slide's structure into a **named layout with real placeholders** (TITLE/BODY/PICTURE/TABLE) on the Slide Master, while preserving decorative brand shapes (cards, accent bars, dividers) as non-placeholder layout shapes.

### When to use C vs B

| Trigger shape | Capability | Source of new layouts |
| ------------- | ---------- | --------------------- |
| Template has layouts but missing one for a slide_type | **B** (donor clone) | Donor template (external) |
| Template's master is empty; the user's own deck has the designed slides | **C** (designer promotion) | The source deck itself (reverse-engineered) |

### Algorithm (per slide)

0. **Inject Slide Master background** (once, before per-slide promotion) — `_compute_dominant_master_bg(slides, theme)` tallies each source slide's dominant bg (via XML or vision) and picks the most common. `_inject_master_background(prs, hex)` replaces the master's default `<p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef>` (which resolves to theme `lt1` — white in a dark-mode deck) with a solid `<p:bgPr><a:solidFill><a:srgbClr val="..."/></a:solidFill></p:bgPr>`. This makes the master thumbnail in PowerPoint's Slide Master view match the brand, and any layout that doesn't override `<p:bg>` inherits the correct dark color. Without this step, the "base" master slide stays white even though all promoted layouts are dark — visually inconsistent and confusing in Slide Master view.
1. **Cluster shapes by role** — `cluster_shapes_by_role(slide)` walks the slide's shapes and classifies each: largest-font text shape (≥28pt) → `title`, other text shapes → `body`, picture shapes → `picture`, table shapes → `table`, everything else → `decorative`.
2. **Allocate placeholder indices** — TITLE=0, BODY=1..n (reading order: top-to-bottom, left-to-right), PICTURE=10+, TABLE=20+.
3. **Promote to layout** — clone the slide as a new `SlideLayout` under the master; convert each clustered shape to its placeholder type via raw OOXML (`<p:ph type="..." idx="..."/>` under `<p:nvSpPr>/<p:nvPr>`). Decorative shapes are kept verbatim.
4. **Rewrite the theme XML** — `extract_theme_from_shapes(slides)` infers the major/minor font (most-used font across runs, weighted by run length) and 12 OPC color roles (sorted by brightness into dk1/lt1/dk2/lt2, remaining into accent1..4). `apply_theme_xml(prs, theme)` rewrites the master's `theme/theme1.xml` in place.
5. **Inject layout background** — `_inject_layout_background(new_element, bg_hex)` sets `<p:cSld><p:bg>` on each promoted layout. Background is resolved per-slide via `_resolve_slide_background(slide, vision_schema, theme)`: vision-derived `dominant_bg_hex` (confidence ≥ 0.5) takes precedence; otherwise `fallback_xml_background(slide, theme)` reads the largest covering shape's fill (handles both `<a:srgbClr>` direct RGB and `<a:schemeClr val="tx1|dk1|..."/>` theme references including ECMA-376 aliases); last resort is `theme["dk1"]`.
6. **Run container-fit check** — for each promoted layout, `container_check.container_violations(layout)` flags any text placeholder that geometrically extends beyond its visual container shape (the reference-template slide-4 defect: body text spilling past its container). Critical violations (>20px overflow) block the build by default; warnings (4–20px) are reported but non-blocking.
7. **Run WCAG 2.1 contrast check** — `contrast_check.contrast_violations(layout, theme, auto_fix=True)` flags any text placeholder whose effective foreground color (resolved from explicit rPr → theme `dk1` default) fails WCAG AA against its background (resolved from container fill → theme `lt1` → white). Required: 4.5:1 (normal text), 3:0:1 (large text ≥18pt). Severity: <3.0 critical, <4.5 warning. Auto-fix (default ON) overrides the placeholder's default run color to white/black based on background luminance; the violation is still reported with `auto_fixed=True`. On the reference template, this surfaced 53 critical defects (mostly `#FB923C` orange on `#FB923C` orange = 1.0:1 ratio, and light text on `#2DD4BF` teal); auto-fix resolved 43 (81%).
8. **Strip source slides** — template ≠ deck; the output has 0 slides + N layouts.

### Usage

```bash
python -c "
import sys, os
sys.path.insert(0, os.path.join(os.environ['SKILL_DIR'], 'scripts'))
from designer_promoter import promote_designer_slides
report = promote_designer_slides(
    source_pptx='/path/to/designer_deck.pptx',
    output_path='/path/to/designer_deck_template.pptx',
    layout_names={0: 'Cover', 1: 'Story', 2: 'Problem Impact', 3: 'Problem',
                  4: 'Solution', 5: 'Demo', 6: 'Market Validation',
                  7: 'Business Model', 8: 'Team', 9: 'Ask'},
    # theme_override={'major_font': 'Century Gothic', 'accent1': '#2DD4BF', ...}
)
print(report.to_dict())
"
```

**Output:** new `<source>_template.pptx` with: (a) rewritten Slide Master theme (major/minor fonts + 12 OPC color roles from the source's per-shape palette — not stock Office), (b) N named layouts with proper text/picture/table placeholders, (c) decorative brand shapes baked into each layout, (d) zero source slides.

**Container-fit safety:** the build runs `container_check` after each layout promotion. Critical violations raise `RuntimeError` (configurable via `container_critical_blocks=False`); warnings are reported in `PromotionReport.container_violations` for orchestrator follow-up (extend container, shorten text, or move placeholder).

### Scripts (Capability C)

| Script | Purpose |
|--------|---------|
| `scripts/designer_promoter.py` | `promote_designer_slides(source, output, ...)` — full pipeline. Also exposes `cluster_shapes_by_role`, `extract_theme_from_shapes`, `apply_theme_xml`, `_inject_master_background`, `_inject_layout_background`, `_compute_dominant_master_bg`. |
| `scripts/container_check.py` | `container_violations(layout)` / `check_template(prs)` — static geometry check. Raises `ContainerFitError` on critical violations when invoked as a gate. |
| `scripts/contrast_check.py` | `contrast_violations(layout, theme, auto_fix)` / `contrast_ratio(fg, bg)` — WCAG 2.1 contrast verification with optional auto-fix (flips low-contrast placeholder text to white/black based on background luminance). |
| `scripts/vision_extractor.py` | `render_slides_to_pngs(pptx)` / `build_image_analyzer_prompt(...)` / `aggregate_vision_results(...)` / `fallback_xml_background(slide, theme)` — vision-assisted schema extraction. Composes with the XML path: vision provides `dominant_bg_hex` for master + layout bg injection; XML provides precise shape geometry. |
| `scripts/pptx_validate.py` | Post-build validation gate: 8 static OOXML checks (zip, XML, content-types, broken/dangling rels, rel-type mismatch, empty r:id, duplicate layout ids) + `--fix` auto-repair + `--com` authoritative PowerPoint open test. **Run after every build.** |

### Cross-link to Capability B

Capability B (`state_machine.resolve_and_clone`) and Capability C (`designer_promoter.promote_designer_slides`) are siblings: B borrows from a donor, C reverse-engineers from the source. The orchestrator (`pptx-specialist-subagent` Stage -1) routes between them based on whether the master is empty.

## Post-build validation gate (MANDATORY)

python-pptx/lxml stay silent on defects that make PowerPoint show **"needs repair"**. After ANY Capability B/C build, run:

```bash
python scripts/pptx_validate.py <output>.pptx --fix --com
```

Exit 0 = clean. `--fix` safely repairs id collisions + empty `r:id` attrs in place. `--com` (Windows + PowerPoint + pywin32) is the **authoritative gate**: PowerPoint hard-fails COM open on repair-worthy files. Without LibreOffice, this replaces vision-render smoke testing. Kill lingering `POWERPNT.EXE` after a failed COM open before retesting (hidden modal blocks later opens); HRESULT `0x80070070` is PowerPoint's generic open-failure code, not disk-full.

Three defect classes this gate exists to catch (all seen in the wild on designer promotion):

1. **Duplicate `sldLayoutId` ids** — PowerPoint treats `sldMasterId` + `sldLayoutId` as ONE presentation-wide uniqueness space. Allocating from a single master's list collides on multi-master decks. (`designer_promoter._max_layout_id` now scans all masters + `sldMasterIdLst`.)
2. **Dangling relationship refs** — shapes `deepcopy`ed from slides carry `r:embed`/`r:link`/`r:id` values whose rIds don't exist in the new layout's `.rels`. (`_remap_shape_rels` recreates every referenced rel on the new part at copy time.)
3. **Rel-id type collision** — a copied `p14:media r:embed="rId1"` pointing at the layout's `rId1` = slideMaster rel (structural rel where image/media/video expected). Same fix: remap, never copy rIds verbatim. Empty `r:id=""` (from `ppaction://media` hlinks) is also invalid and is dropped.

## Reference

- Design: `docs/DESIGN-template-agnostic.md` inside the sibling `pptx-generate-slide-skill` directory — §5 (state machine), §7 (Capability B pipeline + 7-step clone).
