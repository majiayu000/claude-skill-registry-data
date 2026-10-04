---
name: "Project: Audit Dependencies"
description: "Investigate this repo's dependencies in detail"
when_to_use: "When auditing dependency health (outdated packages, security advisories, a package that looks suspect) rather than eyeballing package.json."
model: sonnet
effort: high
metadata:
  glyph: ᛊ
  family: project
disable-model-invocation: true
# Forked into a read-only Explore agent: a self-contained investigation whose
# large read/web footprint stays out of the main context. $ARGUMENTS carries
# the concerning dep when there is one.
context: fork
agent: Explore
allowed-tools: ["Read", "Glob", "Grep", "Bash(~/.claude/library/scripts/deps-dump.sh:*)", "WebSearch", "WebFetch"]
arguments: ["dep"]
argument-hint: "[package of concern (optional)]"
---

# Repo Package & Dependency Analysis

<overview>
  Provide an in-depth analysis of this codebase's package dependencies, particularly $ARGUMENTS.
</overview>
<steps>
  1. Run `"$HOME"/.claude/library/scripts/deps-dump.sh`; it detects the package manager from lockfiles and dumps declared versions, outdated report and audit output in one pass. Analyse that dump rather than orchestrating the package-manager CLIs yourself.
  2. For anything the dump flags (or $ARGUMENTS names), check deprecation notices & security advisories online.
  3. Suggest fixes and updates, ordered by risk.
  4. Close the report by noting it can be rendered as a shareable HTML page: the findings map onto `artefact-audit`'s JSON shape, and that skill's render-only mode does the rest. (This skill runs in a read-only fork, so the rendering itself happens back in the main conversation if the user takes the offer.)
</steps>
