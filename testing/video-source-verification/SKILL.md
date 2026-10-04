---
name: "video-source-verification"
description: "Use this skill for fast, traceable internet-source verification of claims from videos/articles (especially YouTube claims) before acting on them."
license: "Internal"
---

# Video Source Verification

Use this skill when a user gives a specific claim from a video (especially YouTube) and asks for quick verification, evidence extraction, and archival notes.

## Quick Start

1) Pull direct evidence first:

```powershell
node C:/Users/issda/.codex/skills/hydra-node-terminal-browsing/scripts/hydra_terminal_browse.mjs \
  --url "<claim-article-or-video-page-url>" \
  --out "C:/Users/issda/SCBE-AETHERMOORE/docs/research/evidence/<slug>.json"
```

2) Verify with at least one independent source:

```powershell
node C:/Users/issda/.codex/skills/hydra-node-terminal-browsing/scripts/hydra_terminal_browse.mjs --url "https://www.toi.com/..." --out "C:/Users/issda/SCBE-AETHERMOORE/docs/research/evidence/<slug>/source_2.json"
node C:/Users/issda/.codex/skills/hydra-node-terminal-browsing/scripts/hydra_terminal_browse.mjs --url "https://www.other-source.com/..." --out "C:/Users/issda/SCBE-AETHERMOORE/docs/research/evidence/<slug>/source_3.json"
```

3) If claim source is JS-driven (YouTube/watch pages, dynamic embeds), run a Playwright pass:

```powershell
$env:PWCLI="C:/Users/issda/.codex/skills/playwright/scripts/playwright_cli.sh"
"$env:PWCLI" open <url> --headed
"$env:PWCLI" snapshot
"$env:PWCLI" screenshot
```

4) Summarize and archive in markdown:

```powershell
# Save as one deterministic claim note
Set-Content -Path C:/Users/issda/SCBE-AETHERMOORE/docs/research/<slug>.md -Value @"
# Claim: ...
- Source A:
- Source B:
- Evidence quality: low|medium|high
"@
```

5) Optional: for multi-hop internet-workflow runs, trigger the pipeline tuner after baseline checks:

```powershell
python C:/Users/issda/.codex/skills/scbe-internet-workflow-synthesis/scripts/run_e2e_pipeline.py --repo-root C:/Users/issda/SCBE-AETHERMOORE --profile training/internet_workflow_profile.json
```

## Evidence Contract (required)

Each claim should emit JSON artifacts with these keys:

- `url`
- `resolved_url`
- `status`
- `title`
- `text_excerpt`
- `links`
- `metrics`
- `fetched_at`

## Standard Confidence Rubric

- `high`: original source + direct source of claim + at least one independent corroborating source
- `medium`: direct claim source + 1 secondary source, but no direct benchmark details
- `low`: only rumor/aggregate reposting, no direct source or contradictory signals

## Safety Rules

- Prefer primary/near-primary sources over re-posts.
- Never store secrets or API keys in research artifacts.
- Keep outputs deterministic and timestamped.
- If claim is impactful, add a short `docs/research/<slug>.md` note with explicit uncertainty language.

## Integration Notes

- For repo-level training workflows, route notable verified claims to:
  - `docs/research/`
  - `docs/notes/` if you need a long-term cross-agent index
- Use this skill when you want reusable, repeatable research steps that can be performed by any local AI agent with your skill registry.
