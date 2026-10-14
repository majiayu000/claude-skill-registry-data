---
name: craft-docs
description: Crafting a documentation site. Progressive depth, not progressive confusion.
---

# Skill: Craft Docs

> "Good documentation is a layered cake. A developer should be able to stop at any layer and walk away with enough to ship."

## The Standard

1. **`docs/` directory in the repo**: Markdown files that feed a docs renderer. The `docs/` directory appears when the package matures. Not every package needs one -- but every package with significant configuration surface area does.

2. **Frontmatter with weight ordering**: `weight: N` controls page order. Weight ordering keeps docs sorted without relying on filenames.

3. **Progressive depth**: Introduction, then basic usage, then advanced usage, then API reference. Each layer is self-contained. A developer can stop at "basic usage" and have a working integration.

   | Layer             | Location               | Content                                      |
   |-------------------|------------------------|----------------------------------------------|
   | **Pitch**         | README first screenful | What it does + 1-2 line code example         |
   | **Quick start**   | `introduction.md`      | Install + basic usage                        |
   | **Features**      | `basic-usage/`         | Individual feature pages                     |
   | **Customization** | `advanced-usage/`      | Custom implementations, extending interfaces |

   Never dump all features at once. Simple things simple, complex things possible.

4. **UPGRADING.md**: Reverse-chronological. Actionable bullet points, not essays. Before/after code examples. Full migration scripts when schema changes. Rate each breaking change as **High/Medium/Low** likelihood of impact. Developers need to triage -- not read every line.

5. **Config shown in installation docs**: The developer sees exactly what they are getting before publishing. Show the full config file with inline comments. No surprises after `php artisan vendor:publish`.

6. **Anticipate the wall**: Put warnings BEFORE the step that will trigger the error, not after. If a database user needs to adjust something, say so before the migration step -- not in a troubleshooting section they will find 20 minutes later.

7. **Versioned docs**: Maintain separate docs per major version. Old docs remain accessible. When a version reaches end-of-life, state it clearly.

8. **Automated migration guidance**: Where possible, include Rector rules or codemods for major version upgrades. Automation beats manual find-and-replace. Laravel Shift's approach with `driftingly/rector-laravel` is the gold standard -- version-specific rule sets and cumulative level sets.

## The Approaches

**Filament's versioned docs**: Every major version gets its own branch and docs. Automated upgrade scripts (`filament/upgrade`) rewrite application code for breaking changes. This dramatically lowers the cost of major versions.

**Docs-as-website**: The `docs/` directory feeds a docs renderer. Frontmatter carries version, slogan, and repo metadata. Each package version gets its own docs set.

## The Anti-Patterns

| Don't                                | Do                                              | Why                                                     |
|--------------------------------------|-------------------------------------------------|---------------------------------------------------------|
| Warnings after the failure step      | Warnings before the step                        | Developers read linearly -- catch them before they fall |
| Upgrade guides without code examples | Before/after code in every breaking change      | "Renamed X to Y" means nothing without code             |
| Flat docs with no progressive depth  | Layered structure: intro, basic, advanced       | Developers have different depth needs                   |
| Abandon docs for previous versions   | Maintain versioned docs with clear EOL          | Users on older versions still need documentation        |
| Hide config until after publish      | Show full config in installation docs           | No surprises -- informed decisions before commitment    |
| Upgrade guide as a wall of text      | Impact-rated changes: High/Medium/Low           | Developers triage -- help them prioritize               |
| Skip automated migration guidance    | Include Rector rules or codemods where possible | Automation beats manual find-and-replace                |

**See also:** decide-docs-site (when to build a docs site vs README-only), craft-deprecation (UPGRADING.md patterns).

## Real-World Examples

See [examples.md](examples.md).
