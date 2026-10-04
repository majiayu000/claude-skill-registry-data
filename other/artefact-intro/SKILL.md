---
name: "Artefacts: Introduce Repo"
description: "Render a visual HTML introduction to this codebase for a newly-joined developer"
when_to_use: "When onboarding someone new to a codebase, or when you want a visual architecture primer rather than a README skim."
model: sonnet
effort: high
metadata:
  glyph: ᛊ
  family: artefact
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Bash(git:*)", "Bash(open:*)", "Bash(mkdir:*)", "Write"]
argument-hint: "[focus of analysis (optional)]"
---

# Repo Introduction

<overview>
  Produce an interactive visual overview of this codebase aimed at a newly-joined developer.
  Uses the visual-explainer plugin to generate a standalone HTML page with architecture diagrams,
  module relationships, and project context.
</overview>
<steps>
  1. Load the visual-explainer skill AND the artefact-conventions skill: visual-explainer supplies the diagramming/rendering patterns, artefact-conventions supplies Jason's structural/aesthetic layer (masthead, palette-via-theme-tokens, theming contract with its masthead toggle control, honesty footer). They compose; neither replaces the other. This skill generates Mermaid architecture diagrams rendered once at load, so the theming contract's diagram rule applies directly: drive node/edge colours from the same CSS custom properties as the rest of the page, or re-render on both `matchMedia` change and `data-theme` mutation; a static render taken at load time strands its colours on the next toggle click.
  2. Per artefact-conventions Step 2: check {project_root}/docs/artefacts/ for existing artefacts. If this project already has one, read it and reuse its established palette/font-pairing/tone rather than defaulting to whatever visual-explainer would generate on its own; an intro page should look like it belongs with the project's other artefacts, not like a different tool made it.
  3. Analyse the codebase:
     - Read README.md, package.json/go.mod/Cargo.toml/pyproject.toml for identity and dependencies
     - Map top-level directory structure and entry points
     - Read key source files to understand module structure and public API surface
     - Skim git log for recent activity and key decisions
  4. If $ARGUMENTS contains content, treat it as a focus area and weight the analysis accordingly.
  5. Generate a visual HTML page following the visual-explainer workflow for the diagramming, and artefact-conventions for everything else (masthead, theming, collapsibility past ~4 sections, sourced footer):
     - Architecture snapshot (Mermaid diagram of modules and their relationships)
     - Project identity: what it does, who uses it, what stage it's at
     - Mental model essentials: invariants, non-obvious coupling, naming conventions, gotchas
     - Module map with responsibilities
  6. Write to {project_root}/docs/artefacts/intro-{slug}.html (the same home as every other project artefact) and open in browser.
</steps>
<inputs>
  $ARGUMENTS
</inputs>
