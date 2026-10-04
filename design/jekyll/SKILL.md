---
name: jekyll
description: Understand, review, design, implement, and troubleshoot Jekyll pages and sites using Liquid, front matter, layouts, includes, collections, themes, and assets. Use for conceptual Jekyll questions, tracing page rendering, creating or redesigning Jekyll pages, focused theme overrides, static HTML conversion to Jekyll, or relevant build failures. Not for Shopify Liquid, other site generators, prose-only editing, DESIGN.md authoring, or deployment operations alone.
---

# Jekyll

Use standard Jekyll to turn content and templates into maintainable static
pages. Keep the workflow independent of a particular theme, host, agent, CSS
framework, or frontend toolchain.

## Choose the activity

- **Explain or review:** explain concepts, trace supplied sources, or report
  evidence-backed findings; keep files unchanged.
- **Design:** propose the content structure, layout, reusable pieces, visual
  direction, and URLs in the response unless a durable artifact is requested.
  A proposal alone does not authorize implementation.
- **Implement:** create, change, redesign, or convert the requested pages and
  relevant source files, preserving unrelated work.
- **Troubleshoot:** isolate the failing source, configuration, or runtime seam.
  Diagnosis alone stays read-only; fix requests authorize relevant remediation.

Infer the activity from the request and existing authorization. Ask only about
unresolved choices that materially affect the result; reuse existing approval.

For a conceptual question without a site-specific dependency, answer directly
with the relevant Jekyll explanation and a small native example when useful.
Do not require a repository, inspect the environment, or ask for project files
merely to explain layouts, includes, collections, or URLs. Use applicable
official documentation for version-sensitive details; distinguish an example
from a claim about a site you have not inspected.

## Inspect a site when the task needs one

1. Read applicable instructions and working-tree changes. Locate the source
   and relevant configuration, dependencies, and content. Establish Jekyll from
   the explicit target or project evidence; Liquid or GitHub Pages alone is
   insufficient. Check installed versions where they affect the request.
2. Follow the touched page's layouts, includes, data, styles, and assets. Inspect
   the active theme before declaring a locally absent template missing. Expand
   investigation only to resolve a relevant uncertainty; inspect hosting and
   external tooling only when they affect the task.
3. Trace the required source-to-output path, or map it for a new page. Choose
   native content and presentation structures suited to the purpose, preserving
   established URLs and visual choices unless changing them is requested.
4. Return findings or a proposal, or make scoped source edits for implementation.
   Reuse meaningful shared layouts, includes, and data; preserve selectors and
   interactions when converting HTML. A new site can use ordinary Jekyll
   directories and HTML/CSS without an additional toolchain.
5. Verify at the task's scale. Before building or serving, read the build
   reference and inspect the configured destination. Check generated content,
   links, and assets; use available browser capabilities for visual changes.
   Build success alone does not establish visual correctness.

## Keep extensions conditional

Ruby, Bundler when used, and Jekyll's normal dependencies form the
expected runtime. Prefer core Jekyll and relevant existing capabilities. Add
an external dependency only for a requested capability they cannot reasonably
provide: explain the gap and choose the smallest compatible option. Avoid a
complicated substitute merely to evade a necessary dependency.

Preserve relevant integrations without automatically adding plugin bundles,
upgrading dependencies, replacing themes, or introducing search services, asset
pipelines, testing frameworks, or hosting integrations. Distinguish ordinary
Liquid listings from extension-dependent pagination; verify builder
compatibility only when relevant.

## Read selectively

| Need | Reference |
|---|---|
| Content modeling, front matter, rendering, Liquid, navigation, or URLs | [Content and Liquid](references/content-and-liquid.md) |
| Page structure, visual work, theme overrides, assets, or HTML conversion | [Page design and themes](references/page-design-and-themes.md) |
| Build/preview execution, missing content, runtime failures, or relevant compatibility | [Build and troubleshooting](references/build-and-troubleshooting.md) |
| Maintaining this skill, checking sources, or evaluating its boundaries | [Sources and validation](references/sources-and-validation.md) |

This skill is independently usable. When available and useful, add
`ui-guidance` for routine visual work or `ui-design-guidance` for deeper design
and UX review. Use `design-md-author` when the requested artifact is a visual
design document; prose-only editing belongs to the applicable writing workflow.
Custom Ruby plugin development, theme-gem distribution, broad migrations, and
deployment operations need a separately scoped workflow.

## Complete with evidence

Report the relevant explanation or changes, URLs, checks, and material gaps.
Distinguish source evidence, inferred output, observed builds/browser behavior,
and unavailable checks. A narrow question need not become a site audit.

Edit source rather than generated output or installed theme files. Builds and
previews execute project code and write output; installation may fetch and
execute dependencies. Keep those actions within the request's authorization.
Committing, publishing, or changing hosting is not implicit in a page edit.
