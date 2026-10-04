---
name: write-readme
description: Use when creating or improving a README file for a software project or open-source repository
source: "GitHub Community Standards; Make a README (Danny Guo); Shields.io badge documentation"
tags: [readme, documentation, open-source, github, onboarding]
verified: true
---

# Write README

Write a README that turns a visitor into a contributor or user in under five minutes.

## Why This Is Best Practice

**Adopted by:** GitHub community standards checklist; required by npm, PyPI, and crates.io for package discoverability

**Impact:** Projects with complete READMEs receive 2-3x more stars and contributions on GitHub (GitHub Octoverse report); npm packages with detailed READMEs show higher install counts in equivalent categories

**Why best:** A README is the storefront for your project. Most visitors decide whether to use or contribute within 30 seconds. Clear purpose, instant setup, and visible build status eliminate the friction that causes capable people to close the tab.

## Steps

1. **Lead with the project name and a one-sentence purpose** — the very first line must answer "what does this do and who is it for"
2. **Add status badges** — CI status, coverage, version, and license badges from Shields.io signal project health at a glance
3. **Include a screenshot or demo** — a GIF, screenshot, or live demo link provides immediate visual context that prose cannot match
4. **Write a prerequisites section** — list runtime versions, required services, and environment variables before installation steps
5. **Write a quick-start block** — the fewest commands that produce a running result; test these commands in a clean environment before publishing
6. **Document configuration** — table of environment variables and config keys with type, default, and description
7. **Add contributing and license sections** — link to CONTRIBUTING.md if it exists; state the license with a link to the full text

## Rules

- The quick-start must work in a clean environment — test it before committing
- Every command block must specify the shell or interpreter expected
- Do not bury installation behind multiple headings — it must appear above the fold
- Include a license section on every README, even for internal projects
- Keep badges in a single row; more than six badges adds noise without signal

## Examples

**Weak opening:** "This is a tool I built."

**Strong opening:** `rtk` — a token-optimized CLI proxy for Claude Code that reduces API costs by 60-90% by filtering verbose command output before it reaches the model context.

## Common Mistakes

- Missing prerequisites: readers hit errors on step one and abandon the project
- Installation steps that only work on the author's machine due to undocumented env assumptions
- No license section: many companies cannot legally use unlicensed software, so omitting it forfeits enterprise users

## When NOT to Use

- Do not apply this skill to private internal microservices or tooling repositories where the audience is a single team with direct Slack access to the author, and a brief purpose comment at the top of the main file is sufficient orientation.
- Do not use this skill for libraries or packages that already have dedicated documentation sites (e.g., Docusaurus, Read the Docs), where the README should be a minimal pointer to that canonical source rather than a self-contained guide that will drift out of sync.
- Do not apply this skill to experimental or throwaway repositories created for a single spike or proof of concept, where investing in structured README content creates false signals of project maturity and misleads potential contributors about maintenance intentions.
