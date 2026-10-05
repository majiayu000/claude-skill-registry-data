---
name: skill-builder
version: 1.0.0
description: Scaffold a new ralvaskills skill per SPECS.md — SKILL.md skeleton, optional STACK/RECIPES, folder placement, SPECS updates. Interview-first; never guesses. Use when authoring a new skill or invoking /skill-builder.
---

# Skill Builder

Meta-skill that scaffolds new skills under `skills/<category>/<skill-name>/` following [SPECS.md](../../../docs/SPECS.md). Generates structure; hands off content authoring. Templates and the full validation checklist live in [RECIPES.md](RECIPES.md).

## 1. When to invoke

- User says "let's create a new skill", "scaffold a skill", "I want to add a `<topic>-architect`", or invokes `/skill-builder`.
- User wants to verify whether an existing folder structure matches the conventions.
- User wants to move / rename a skill and needs the SPECS updates handled correctly.

## 2. Source of truth

**SPECS.md is canonical.** This skill cites and applies the rules; it does not redefine them. Sections it enforces:

- **Skill Authoring Guide** — SKILL.md format, STACK.md format, naming convention, description quality, supporting files (`UPPER_SNAKE_CASE.md`).
- **Repository & Folder Structure** — discovery rule (folder with `SKILL.md` is terminal; nested SKILL.md forbidden), category placement, personal-skills path-segment rule.
- **Which Skills Need a `STACK.md`** — heuristic table by parent folder; per-skill exceptions allowed.
- **Bundle & Skill Catalog** — bundle membership decisions.

If a question isn't answered here, **read SPECS.md before guessing.**

## 3. Interview-first protocol

**Never scaffold without an interview.** Ask in order; wait for each answer:

1. **Topic + suffix** — what does the skill enforce? Confirm the resulting `<name>` matches the SPECS naming convention. Suffix table in [RECIPES §5](RECIPES.md#5-naming-suffix-table).
2. **Category** — which parent folder? Use existing folders as the source of valid categories. If the right category doesn't exist, ask whether to add it (SPECS update required).
3. **Version target** — if the category requires `STACK.md` (per SPECS heuristic), what versions? For meta-skills with no library stack, confirm exemption ([RECIPES §8](RECIPES.md#8-stackmd-exemption-rules)).
4. **Bundle membership** — which bundle(s) include this skill, or is it standalone?
5. **Cross-skill ties** — which other skills should this one reference? These become `../<path>/SKILL.md` links.
6. **Attribution** — is this adapted from an external source (e.g. `mattpocock/skills`)?
7. **Body shape preview** — propose 5–12 section headings based on the topic. Confirm before writing the skeleton.
8. **Decisions list** (if any) — when the skill encodes opinionated defaults, surface them *before* generating the body.

## 4. Naming + placement

Validate against the SPECS naming convention ([RECIPES §5](RECIPES.md#5-naming-suffix-table)). Path follows category placement and the discovery rule: `skills/<category>/<name>/SKILL.md`. Never nest a `SKILL.md` inside another skill folder.

If the topic doesn't fit any suffix, propose a new one and update SPECS — don't shoehorn.

## 5. Frontmatter generation

One-line description in YAML scalar form. The description sits in Claude's always-loaded skill index — every line costs tokens on every turn, forever.

- WHAT first (topics, comma-separated). WHEN last (trigger phrases / commands).
- Version-sensitive skills mention the primary version target inline.
- Drop "Enforces strict", "Comprehensive guide to", and similar filler.
- One line; no `>` or `|` block scalars.

Template + good/bad examples in [RECIPES §1](RECIPES.md#1-frontmatter-template).

## 6. Body skeleton

Generate placeholders, not content. **Body discipline (per [SPECS — SKILL.md Format](../../../docs/SPECS.md#skillmd-format)):**

- **Rules first, code second.** Each section explains the rule and the *why*; code is illustrative, not exhaustive.
- **Code block ceiling: ~15 lines.** If it grows larger or appears as a full reference implementation (Dockerfile, auth middleware, project tree, test scaffold), move it to `RECIPES.md` and link with one line: *"Skeleton in [RECIPES.md](RECIPES.md)."*
- **Don't restate** patterns canonically explained elsewhere — link.
- **Target body size:** under ~10 KB / ~250 lines unless the topic is genuinely dense.

Standard section shape in [RECIPES §2](RECIPES.md#2-body-skeleton).

### When to scaffold a RECIPES.md

Create at scaffold time when the skill will plausibly contain:

- Multiple full reference implementations (Dockerfile, middleware, repo layout, test scaffold).
- A canonical "here's how the full pattern looks in <language>" section.
- Multiple sibling examples (Go + Python, several frameworks).

Skip when the skill is conceptual (catalog skills like `design-patterns`, methodology skills like `tdd`). For those, code snippets stay inline because they illustrate, not implement.

If unsure, write the skill first; factor recipes out when body crosses ~10 KB or a single section's code exceeds half its prose.

## 7. STACK.md — when and how

Check the SPECS "Which Skills Need a `STACK.md`" table keyed on parent folder. If yes (or "Depends" with version-sensitive content), generate per [RECIPES §3](RECIPES.md#3-stackmd-template). Exemption rules in [RECIPES §8](RECIPES.md#8-stackmd-exemption-rules).

**Fetching versions:** for Go libs, `https://proxy.golang.org/<module>/@latest`. For Python, `https://pypi.org/pypi/<package>/json`. For tools, `gh api repos/<owner>/<name>/releases/latest`. Always pin actual versions, never `latest`.

## 8. Cross-skill linking

Use relative paths from the new skill to its peers (e.g. `../../languages/go-architect/SKILL.md`). Standard ties by category in [RECIPES §4](RECIPES.md#4-standard-cross-skill-ties-by-category).

## 9. SPECS.md updates (atomic)

Every new skill requires 4–6 edits to SPECS.md, applied in one pass. Full list in [RECIPES §6](RECIPES.md#6-specsmd-atomic-update-list).

**Verify after editing:** grep SPECS for the skill name; every mention should make sense in context. Check that no `📋 planned` row remains for a skill that now exists.

## 10. Attribution

If adapted from an external source (e.g. Matt Pocock, Anthropic example, community pattern), append the attribution footer ([RECIPES §9](RECIPES.md#9-attribution-footer)). Verbatim copies require strict attribution; significantly evolved skills should still credit the origin idea.

## 11. Validation

Before declaring scaffold done, walk the full checklist in [RECIPES §7](RECIPES.md#7-validation-checklist). If any item fails, fix before handing off.

## 12. Hand-off

The scaffold is ready. Content authoring is the next step:

- Each section heading needs its bullets / paragraphs / illustrative snippets.
- Each architectural opinion needs to be stated explicitly (default + alternative + when-to-switch).
- Each `STACK.md` row needs a real pinned version (fetch live — don't guess).
- Long code recipes go in `RECIPES.md`, not in `SKILL.md`. As content lands, audit any code block past ~15 lines and factor it out.

Surface the scaffold to the user, summarise what was generated and where, and ask: *"Want me to fill in the section content now, or would you prefer to author it yourself?"*
