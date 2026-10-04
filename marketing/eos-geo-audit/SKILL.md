---
name: eos-geo-audit
description: Run a GEO (Generative Engine Optimization) audit on a publish-app site so ChatGPT / Perplexity / Claude / Gemini cite it correctly. Reads `data/apps/publish/sites.json` for the target site's built output, invokes the upstream `geo-seo-claude` skill against the built HTML, writes the audit report into the vault at `30_Resources/EmptyOS/publish/audits/<date>-geo-<site>.md`. Use when the user says "GEO audit", "audit my site for AI search", "check ChatGPT visibility", "are the AI engines citing my blog", "geo check", or before publishing a post the user wants discoverable. NOT for geographic/spatial analysis of geo apps (use geo-spatial-analyst), classic keyword/technical SEO strategy (use growth-seo-specialist), or drafting the post itself (use eos-devlog-publish / the publish app).
---

# EmptyOS GEO Audit

Wrapper around the upstream `geo-seo-claude` skill that points it at the right place: the publish app's built static output for a specific site. Output lives in the vault so future audits can diff against past ones.

## When to use

| User intent | Example phrasing |
|---|---|
| One-shot audit of the default site | "GEO audit", "audit my site for AI search" |
| Audit a specific site | "audit the portfolio site", "geo check on binbian.net" |
| Pre-publish gate | "is this post going to be cited by ChatGPT?" |
| Periodic check | "weekly GEO check" (run from a scheduler job) |

**Don't use** when the user wants traditional SEO (keyword density, backlinks) — `geo-seo-claude` upstream handles both, but the trigger phrases above are about AI-engine citability specifically. The skill itself will still produce a hybrid report.

## Prerequisites

This skill **wraps** `geo-seo-claude` (https://github.com/zubair-trabzada/geo-seo-claude). Install it once via your normal Claude Code skill mechanism (clone into `.claude/skills/` or however you manage personal skills). If it's not installed when this skill runs, the wrapper falls back to reporting the install steps and writing a minimal placeholder audit so the audit folder still has a dated entry to diff against next time.

The publish app must have built the target site at least once. Output lives at `data/apps/publish/sites/<site-id>/site/`.

## What it does

1. **Resolve the target site.** Read `data/apps/publish/sites.json`. If the user named a site, match by `id` or by `name` substring. Otherwise pick the site whose `id == "default"`, or the first site if no `default`.

2. **Confirm the built output exists.** Check `data/apps/publish/sites/<id>/site/index.html`. If missing, prompt the user to run a build first via the publish app (`POST /publish/api/build`) and stop.

3. **Invoke the upstream `geo-seo-claude` skill** against `data/apps/publish/sites/<id>/site/`. Pass any site metadata that helps it score brand authority correctly (site `domain`, `author`, `social_links` — from sites.json).

4. **Write the audit report** to the vault:
   ```
   {vault}/30_Resources/EmptyOS/publish/audits/YYYY-MM-DD-geo-<site-id>.md
   ```
   Use the existing daily date format (no time component) so a same-day re-run overwrites — audits are point-in-time snapshots, not streams.

5. **Include a `## Diff vs previous` section** when an earlier audit exists for the same site. Highlight: score change, new issues, resolved issues. Keep this section short (≤8 bullets) — the user reads it first.

6. **Report back in chat** with: site audited, audit file path, score (if upstream returns one), top 3 highest-leverage fixes. Don't dump the whole report into chat — link to the vault file.

## Output convention

```
{vault}/30_Resources/EmptyOS/publish/audits/
├── 2026-05-23-geo-default.md
├── 2026-05-23-geo-portfolio.md
├── 2026-05-16-geo-default.md       # last week's
└── 2026-04-30-geo-default.md       # last month's
```

Frontmatter on each audit:
```yaml
---
tags: [audit, geo, publish]
site_id: default
site_domain: binbian.net
audited: 2026-05-23
upstream_skill: geo-seo-claude
score: 78           # optional, only if upstream returned one
---
```

This lets future audits be queried via `VaultIndex` and the vault graph picks them up under the publish project.

## What this skill is NOT

- **Not a runner for the publish build itself.** It audits the output of a build; it never triggers one. Build via the publish app's own UI / API.
- **Not an auto-fixer.** It reports findings; the user (or a follow-up skill / agent) decides which fixes to apply. This matches EmptyOS's "with you, not for you" north star — schema markup changes to your published site shouldn't happen without you seeing them.
- **Not a recurring auto-runner.** If the user wants periodic audits, schedule it via the scheduler app pointing at this skill's invocation. Don't bake cron into the skill itself.

## Cost note

`geo-seo-claude` makes LLM calls (it grades pages, generates schema markup, classifies content for AI-engine compatibility). Cost scales with the site's page count. Surface this when the user invokes the skill against a site with >50 pages — give them a rough cost estimate and let them confirm before running.

## Cross-references

- `apps/public/standard/publish/` — owns the build that this skill audits. The `[provides.publish]` site config in `data/apps/publish/sites.json` is the source of truth.
- `.claude/skills/eos-screenshot/SKILL.md` — sibling skill for visual capture of the same sites; share the privacy/branding posture (`.eos-personal` + `.eos-branding`).
- Upstream `geo-seo-claude` — does the actual GEO scoring + recommendation work. This skill is purely the EmptyOS-context binding around it.
