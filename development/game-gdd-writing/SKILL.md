---
name: game-gdd-writing
description: Write an executable game design document where every section is a contract for a downstream build step. Use when turning a game idea into a buildable plan.
---

# Game GDD Writing

## When to use

- Converting a game idea or user requirement into a design document before implementation.
- Designing within a template/template-family architecture.

## When NOT to use

- One-off throwaway prototypes with no template architecture.
- Tweaking an existing game — edit values directly instead of re-designing.

## Design philosophy

1. **Config-driven**: every numeric value lives in the game configuration — never hardcoded in logic.
2. **Capability-based**: compose existing behaviors/systems; do not design custom engines.
3. **Hook-oriented**: customize by overriding documented hooks, not by rewriting base machinery.
4. **Template-first**: copy established templates and modify configuration — never write from scratch.

## The 6-section contract

The GDD is a technical specification. Each section feeds exactly one downstream step:

| Section | Content | Feeds |
|---|---|---|
| 0. Technical architecture | Archetype, base classes, scene flow diagram, ordered level list, every scene key used in transitions | Scene registration and level ordering |
| 1. Visual style & asset registry | One-sentence style anchor + strict asset table (category, key, vivid description, parameters) | Asset generation |
| 2. Game configuration | Complete config content with exact numbers | Configuration merge |
| 3. Entity/scene architecture | Which base classes to extend, which behaviors to attach with exact parameters, which hooks to override | Code implementation |
| 4. Level/content design | Predefined map templates (verbatim) or content data (dialogue, decks, questions) | Map/content generation |
| 5. Implementation roadmap | Numbered file-level operations in order | The task list |

## Hard rules

- **Exact values only.** Never write "appropriate amount" or "some damage". Every number is specified.
- **No from-scratch work.** Instead of "implement jump physics", write "use the movement behavior with jump power X". Instead of "design map", write "use predefined template B with these modifications".
- **No code snippets.** Describe behavior and configuration; code belongs to implementation.
- **Roadmap is mandatory and file-level.** If the roadmap lists fewer operations than the design implies, the design is incomplete.
- **Infrastructure config stays untouched.** Screen size, debug, and render settings belong to the template; the GDD only specifies game-specific values.

## Balance baselines (starting points, adjust to the game)

Entity heights: player 64–128 px, small enemy 48–80 px, boss 128–192 px, collectible 32–48 px.

Action-game health/damage: player ~100 HP dealing 20–40; enemies 20–80 HP dealing 10–30; bosses 150–400 HP dealing 25–60.

## Style anchor

Section 1 opens with one vivid sentence of art direction ("16-bit pixel art, vibrant colors, retro arcade style"). Everything visual inherits from it.
