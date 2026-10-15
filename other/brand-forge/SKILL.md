---
name: brand-forge
description: >-
  Full brand package for a project or startup: verified name, slogans, logo concepts, palette, brand-tokens.css. Triggers: "branding", "brand forge", "name my app", "I need a name for", slogan/tagline, "trouve-moi un nom", "identité de marque". Image prompt only: chatgpt-image-prompt-architect.
---

# Brand Forge

Automate end-to-end branding: name, slogan, logo, colors, and AI image prompts —
delivered by a pipeline of expert **subagents run sequentially**, with built-in
deterministic trademark/domain verification and a machine-readable handoff to the
build stage.

## Process Overview

Six steps: gather requirements, run the sequential pipeline, lead transition checks, iterate, present, handoff build.

**Architecture (this is the mode, not a fallback):** the five roles run as
**sequential subagents via the standard Agent tool** — one isolated context per
role, handing off through files in `{output_dir}`, in the fixed order
research → names → verify → slogans → package. There is **no multi-agent team
runtime** — no shared task board, no polling, no broadcast messaging, no team
teardown. Each role is a single Agent call the lead spawns and awaits.

**Running the five roles inline in a single context is forbidden.** The whole gate
depends on the generator (naming expert) and the judge (verifier) living in separate
contexts; collapsing them defeats the verification. Likewise the identity-scoring
judge must be a different subagent than the creative director.

## Step 1: Gather Requirements

Ask the user with **exactly three multi-part `AskUserQuestion` calls** (the old
"max 3 questions" text actually smuggled in five — this is now honest). Skip a part
only if the user already answered it in context.

**AskUserQuestion #1 — Project context (open):**
"Tell me about your project/product/idea. What does it do, who is it for, and what
makes it different?" (If already explained, extract from context and skip.)

**AskUserQuestion #2 — Brand vibe + locale (two parts):**
- *Brand vibe* (single-select): Professional & sleek | Playful & modern | Techy & powerful | Minimal & elegant
- *Target market / locale* (single-select): FR / bilingue FR-EN (défaut clients AutoMintech) | English-first | Other (specify)

**AskUserQuestion #3 — Constraints + image tool (two parts):**
- *Constraints* (multi-select): No "AI" in name | Not too techy | Avoid competitor-similar names | No specific restrictions — plus a free-text "Any words, themes, or styles to avoid?"
- *AI image tool* (single-select): ChatGPT / OpenAI (gpt-image) | Gemini / Nano Banana Pro | Other/none

Extract these variables for the agent prompts (**every one must be filled before
any subagent is spawned — see the placeholder guard in Step 2**):

- `project_description`: What the product does in 2-3 sentences
- `industry`: The market/category (e.g., "voice-to-text", "project management")
- `product_type`: The concrete form factor — "desktop app" / "mobile app" / "web app" / "CLI" / "API" (used in research queries)
- `product_context`: Features, target audience, price point, platform
- `brand_vibe`: Selected archetype
- `target_audience`: Who uses it
- `value_prop`: Core value in one sentence
- `user_constraints`: All naming restrictions (the single canonical variable name — every agent template reads exactly `{user_constraints}`)
- `target_locale`: `FR-bilingual` (default) | `EN` | other — drives naming language, dual-language verification queries, and the French connotation check
- `naming_rule`: "When someone hears the name, they must immediately understand what the product does"
- `max_chars`: 10 (default; raised to 14 for round-3 two-word compounds — see Step 4)
- `min_names`: 30 (generate volume — expect 70-85% failure rate)
- `current_year`: the current calendar year (fill from today's date — used in research queries like "best {industry} products {current_year}")
- `image_gen_tool`: from AskUserQuestion #3 — routes to **chatgpt-image-prompt-architect** (OpenAI) or **nano-banana-prompt-engineer** (Gemini)
- `output_dir`: `docs/branding` in the project root (create if needed)
- `selection_criteria`: Derived from brand vibe + constraints
- `skill_dir`: the **absolute path** of this skill, resolved at runtime — `${CLAUDE_PLUGIN_ROOT}/skills/brand-forge` when installed as the `design-studio` plugin, or `~/.claude/skills/brand-forge` when the skill runs standalone — injected into every subagent prompt so references resolve from a blank context

## Step 2: Spawn the Sequential Pipeline

Read `references/agent-prompts.md` for the prompt templates and
`references/naming-strategies.md` + `references/visual-identity.md` for the encoded
craft. Fill each template with the Step-1 variables.

**Placeholder guard (mandatory, before each spawn):** scan the filled prompt for any
remaining `{placeholder}`. If ANY `{...}` token survives, do not spawn — fill it
first. The template variable set and the Step-1 variable set must match exactly
(diff = empty).

**Absolute references (mandatory):** subagents start from a blank context where a
relative path does not resolve. Every agent prompt must inject `skill_dir` and point
to the exact section, e.g. `Read first {skill_dir}/references/naming-strategies.md
§Common Failure Patterns` and (for the creative director) `{skill_dir}/references/visual-identity.md`.

**Run order (strictly sequential, one Agent call at a time):**

1. `researcher` → writes `research-findings.md`
2. `naming-expert` → reads research, writes `name-candidates.md`
3. `verifier` → reads candidates, writes `verification-report.md`
4. `copywriter` → reads verification, writes `slogans.md`
5. `creative-director` → reads all, writes `final-recommendation.md`

Spawn role N+1 **only after** the lead's transition check for role N passes (Step 3).

**Timeout / failure procedure:** if a role's subagent times out or returns no file,
**relaunch that same agent** (optionally with a narrower scope). **Never fabricate a
role's output** to keep the pipeline moving — a missing deliverable is a re-run, not
an invention.

## Step 3: Lead Transition Checks (accounting, not relaying)

The lead validates every transition with a written accounting check and sends the role back if it fails. Non-negotiable: after names, count >= `min_names`; after verification, 100% of candidates carry a verdict (PASS / CONDITIONAL / FAIL) plus >= 1 evidence URL, a per-name "Queries run" section exists, and the lead re-runs one query for 3 randomly picked names and compares; after slogans, run the ban-list check; before presentation, a real SVG was rendered at 16/32/512px and the contrast gate passed with computed ratios. Full checklist: `references/lead-checks-and-presentation.md` §Step 3.

## Step 4: Handle Iteration

If the verifier returns strictly fewer than 3 PASS names (CONDITIONAL do not count), tell the user and ask whether to run another naming round with a fresh naming-expert that avoids all failed names, or proceed. Round strategies (broad, compounds, two-word compounds at `max_chars` 14): `references/lead-checks-and-presentation.md` §Step 4.

## Step 5: Present Results

Read `final-recommendation.md`, present top 3 name+slogan combos, the #1 rendered SVG logo, the primary image prompt, palette with computed contrast ratios, the RDAP-dated domain and the "indicative, confirm with a registrar / legal validation required" caveat, then ask which name the user prefers. Detail: `references/lead-checks-and-presentation.md` §Step 5.

## Step 6: Handoff Build (mandatory final step)

Produce the machine-readable handoff so ship-polished-ui / design-forge BRIEF can
consume the brand without re-typing anything:

1. **`docs/branding/brand-package.md`** — follow the schema in
   `references/brand-package-template.md` **verbatim** (status, RDAP-dated domain,
   tokens mirroring brand-tokens.css exactly, typography with load URLs + licenses,
   voice, assets, validated slogans, brand-specific don'ts).
2. **`docs/branding/brand-tokens.css`** — CSS custom properties: light/dark colors,
   font families, type scale. The token values here are the **exact mirror** of the
   `tokens:` block in brand-package.md.
3. **Web assets checklist** — produce/place: `logo.svg`, `favicon.svg`, apple-touch
   icon, `og-image.png`, dark variants — conventional target paths under
   `public/brand/`.
4. **Lead verification:** `ls` + non-zero size on brand-package.md and
   brand-tokens.css, and confirm brand-tokens.css **parses** (simple read + a regex
   check that `--custom-property:` declarations are present).
5. **Propose the next stage explicitly:** "Run **design-forge BRIEF** with this
   package to produce the design-intent, or **ship-polished-ui** to build directly —
   both load `docs/branding/brand-package.md` as brand-fixed constraints."

## Output Files

The pipeline produces **7 deliverables** in `{output_dir}` (the lead verifies each exists):

| File | Contents |
|------|----------|
| `research-findings.md` | Market analysis, competitors, naming territories |
| `name-candidates.md` | All generated names with rationale |
| `verification-report.md` | RDAP + trademark/domain check + "Queries run" for every name |
| `slogans.md` | 3-5 slogans per verified name |
| `final-recommendation.md` | Name, slogans, rendered SVG logo, palette, image prompts |
| `brand-package.md` | Machine-readable handoff (schema A4) — consumed by the build pipeline |
| `brand-tokens.css` | CSS custom properties (light/dark, families, scale) — exact mirror of the package |

Tips for best results (product specificity, upfront constraints, trusting the verifier, expecting 2-3 rounds): `references/lead-checks-and-presentation.md` §Tips.
