---
name: craft-readme
description: Crafting a README. The landing page for your package.
---

# Skill: Craft README

> "A README is a landing page, not documentation. It has one job: get the developer to install."

## The Standard

1. **H1 is a benefit statement**: Not the package name. "Associate users with permissions and roles" -- not "laravel-permission." The H1 sells what the package does. The name lives in `composer.json`.

2. **Show code in the first screenful**: A working example within the first scroll. No boilerplate, no `use` statements unless critical. Simple to complex progression. Casual confidence. No ceremony.

3. **Badge trio**: Version + Tests + Downloads. Always `?style=flat-square`. Three to four badges max -- more is noise.

4. **Section order**: Header image (dark/light responsive) -> H1 slogan -> Badges -> Brief description + code example -> Documentation link (if docs site exists) -> Installation (abbreviated) -> Testing -> Changelog -> Contributing -> Security Vulnerabilities -> Credits -> Alternatives (optional) -> License.

5. **README is a landing page, not documentation**: Keep it tight. One to five examples, then link to the docs site for depth. If your README needs a table of contents, you have too much README.

6. **No hype language**: No "amazing," "incredible," "revolutionary." Concrete, specific, casual confidence. The code speaks. If you need adjectives to sell your package, the package is not selling itself.

7. **List alternatives**: Listing competitors signals trust and maturity. A developer who sees alternatives listed knows you are confident in your offering.

## The Approaches

**Taylor's minimal style**: First-party package READMEs are thin. They link to the official docs at `laravel.com/docs/{feature}` and keep the README to installation + a single example. The framework's documentation site carries the weight.

**Filament's docs-as-product**: Documentation is a first-class deliverable. Dedicated testing docs per subsystem, code-heavy examples, plugin development guides, upgrade guides with automated migration scripts. The docs sell the platform.

**Spatie's landing page**: README is a sales page with dark/light responsive banner, benefit-driven H1, 1-5 code examples, then a link to the docs site. Every mature package follows this pattern.

## The Anti-Patterns

| Don't                          | Do                                         | Why                                                                              |
|--------------------------------|--------------------------------------------|----------------------------------------------------------------------------------|
| H1 = package name              | H1 = benefit statement                     | The name is on Packagist -- the README sells the value                           |
| Wall of text before code       | Code in the first screenful                | Developers scan, they don't read -- show, then tell                              |
| Full documentation in README   | Link to docs site, keep README tight       | README is a landing page, docs are the manual                                    |
| Hype language and superlatives | Concrete capability statements             | "Amazing" tells nothing -- "caches all GET requests for a week" tells everything |
| 6+ badges                      | Badge trio: version, tests, downloads      | More badges = more noise = less signal                                           |
| Skip the alternatives section  | List competitors openly                    | Confidence move -- it signals maturity                                           |
| Omit PR template guidance      | Include `.github/PULL_REQUEST_TEMPLATE.md` | Contributor experience starts before the first PR                                |

**See also:** craft-branding (banner assets and visual identity), decide-docs-site (when to move depth out of README).

## Real-World Examples

See [examples.md](examples.md).
