---
name: readme-atlas
description: Write, improve, or review repository READMEs for accurate onboarding and polished visual presentation. Use for README creation, visual design, layout, badges, screenshots, project positioning, and translation, using repository evidence and patterns studied across open-source projects.
---

# README Atlas

Help the intended reader recognize the project, enjoy a coherent presentation, decide whether it fits, and reach a useful first result. Treat visual quality, factual accuracy, and onboarding as complementary parts of README quality. Choose the structure and visual language from the project's actual distribution, audience, and identity. A popular project's README is evidence of one editorial choice, not a universal template.

## Choose the task

- **Create:** inspect the project, choose a reader journey, and write the requested README.
- **Improve:** preserve correct information, useful anchors, and the project's voice; fix the reader's actual obstacles. Avoid a full rewrite for a narrow edit.
- **Review:** report concrete problems with evidence and proposed fixes. Do not edit unless requested.
- **Translate:** preserve commands, identifiers, URLs, requirements, and feature status. Keep language files mutually discoverable and flag factual drift separately from translation.

Use the requested language. Otherwise follow the existing README or the user's language for a new one. Create multiple language files only when requested or already part of the project.

## Establish the facts before the prose

Read the repository's applicable instructions and existing README. Inspect the smallest relevant set of manifests, public entry points, CLI help, examples, tests, CI, configuration samples, license, and documentation. For a monorepo, distinguish the root overview from package-level setup.

Identify whether this is the user distribution, a source tree, an extension, a format specification, or a content archive. Follow README symlinks or path pointers to the actual document before treating a monorepo root stub as missing onboarding. Check which packages are intended as public interfaces; importable internal modules are not automatically supported SDKs. Preserve the existing README format unless conversion is requested or needed for the task; RST substitutions, AsciiDoc directives, and text headings need their own syntax, not pasted Markdown or HTML conventions.

Build a compact working fact map; keep it out of the published README unless useful to readers:

| Reader needs to know | Best available evidence |
| --- | --- |
| What it does and who it serves | Public interfaces, examples, existing product documentation |
| How it is distributed | Package metadata, release artifacts, containers, deployment docs |
| Requirements and environments | Version constraints and CI matrix; distinguish declared from tested support |
| Install/run/import commands | Actual package name, scripts, entry points, examples, CLI help |
| First successful result | Example input plus assertion, response, screenshot, or documented behavior |
| Limitations and status | Implemented behavior, release notes, explicit maintainer statements |
| License and contribution path | Actual license file and contribution documentation |

Prefer implementation and maintained metadata when prose conflicts with them; report material discrepancies. Do not invent package publication, performance numbers, screenshots, hosted demos, CI badges, supported platforms, roadmap commitments, or a license. User-provided plans are plans until implemented. If a fact is missing, omit an optional claim or label the uncertainty outside the final README. Ask only when the missing fact changes the main onboarding path; continue independent work.

## Choose the reader journey

Identify the primary reader, their immediate job, and the smallest meaningful success. Select a route using [patterns.md](references/patterns.md) when the structure is uncertain:

| Repository | Primary route |
| --- | --- |
| Library / SDK | Install → import → input → output → API docs |
| CLI / developer tool | Install → command → visible result → common tasks / help |
| Desktop / web application | See the experience → download or launch → first interaction |
| Service / platform | Choose hosted, local, or self-hosted → prerequisites → start → verify |
| ML / research | Task → environment / weights / data → inference or reproduction → limits / citation |
| Systems / embedded | Reader role / target hardware → supported setup guide → build or first task → verification |
| Scientific / notebook environment | Core installation → small calculation or browser launch → optional examples / extensions |
| Curated list / learning resource | Scope → navigation → first reading or exercise → contribution rules |
| Periodical / content archive | Latest edition → dated archive → reading / submission route |
| Specification / interchange format | Scope → concepts / terminology → format details → implementations / contribution |
| Agent skill | Capability → install complete folder → invocation → expected artifact |

When mature documentation already owns onboarding, a short README with clearly labeled start links can be enough. When no such docs exist, keep the essential first-use path in the README. For knowledge repositories, navigation or a first exercise replaces software installation. Do not force every repository through a runnable quickstart.

## Design the presentation

For a new README, a substantial rewrite, or a visual review, read [visual-design.md](references/visual-design.md). Consider aesthetics even when the user only asks for a good README; scale the changes to the requested scope.

Choose a coherent direction: a clean technical document, a compact branded introduction, a product demonstration, or a navigable resource collection. Use the project's existing identity and real assets when available. Give the opening a clear focal point, a concise promise, useful entry links, and an appropriate preview. Keep headings, spacing, badges, image proportions, and accents consistent. A small project can look polished through typography and rhythm alone; a visual product often benefits from a real screenshot or demonstration.

When the README uses badges, keep **all badges together in one visible header group**, including download counts, compatibility, and community/listing badges. **Center the entire badge group and everything above it**: title, logo, tagline, and language links. Keep the following body left-aligned. Do not move badges into the footer or a collapsed section to reduce clutter. This is README Atlas's layout convention; see the markup example in [visual-design.md](references/visual-design.md).

Compose the rendered page deliberately. Keep body text and instructions easy to scan, use tables for short comparisons, and reserve collapsible sections for optional depth. Check how badges wrap, screenshots scale, and artwork contrasts with the background. For Markdown READMEs, use GitHub-compatible Markdown and simple supported HTML; preserve native syntax for other formats. Do not depend on custom CSS or scripts. Brand illustrations should be original or reusable with permission, and remain distinguishable from actual product screenshots.

## Write for the next decision

Open with the project name and a specific sentence: what it is, what it does, and for whom. Give the reader an immediate action or evidence of the result. Explain differentiators through supported behavior, not generic praise.

For a runnable quickstart, include necessary prerequisites, working directory, installation, minimal input, execution, and recognizable success. Make one supported path easy to follow; put substantial alternatives behind named sections or existing docs. Separate commands from expected output. Label the shell correctly; do not put Bash activation or quoting in a PowerShell block. Mark placeholders and show where required configuration comes from.

Keep first use separate from source development and production deployment. Surface an expensive model download, required credential, paid service, hardware requirement, or externally visible action before the command that depends on it. Include only costs and constraints established by the project.

Keep runtime requirements distinct from optional example, test, build, and extension-development dependencies. Where the project makes the distinction, label stable releases, experimental builds, and obsolete versions; link changing compatibility or board matrices to maintained guidance. If an example depends on application-defined helpers, either supply them for a runnable quickstart or clearly present an API illustration. Preserve actual shared-demo restrictions rather than treating every demo as an exercise environment.

Add sections only when they resolve a reader need:

- Small capability lists with links to deeper docs.
- Screenshots for interaction, command transcripts for CLI behavior, or architecture diagrams for deployment choices. Use actual assets and descriptive alt text; never fabricate a screenshot.
- Requirements, supported environments, and known limits near the affected steps.
- Benchmarks only with a traceable workload, environment, baseline, and method; preserve important caveats.
- A short navigation list when the page is long enough to need one.
- Existing help, contribution, security-reporting, and license destinations with accurate labels.

Move exhaustive flags, API catalogs, platform-specific build recipes, and long contributor instructions into existing documentation where possible. Do not create an entire docs site merely to shorten a README. Prefer relative links for repository files and check paths with exact case. Use a few useful badges only when their targets exist; stars, sponsor walls, and decorative headers are optional editorial choices.

## Validate the reader path

Read [review-checklist.md](references/review-checklist.md) for a full review or substantial rewrite; use only relevant checks for a small edit.

Trace every command against repository evidence. Execute a cheap, permitted first-use path when practical. Reading a command is not executing it; do not claim a smoke test passed when only metadata was checked. Do not execute deployment, paid API calls, destructive operations, or credential-consuming actions merely to validate prose without the needed authorization. If execution is unavailable, state the precise validation limit in the delivery note.

Check Markdown fences, links, images, anchors, and consistency across language versions. For substantial presentation changes, inspect the rendered README where possible, including a normal reading width and a narrow layout; check light/dark contrast when artwork or badge styling depends on the theme. Report source-only checks as such. Read the result as a new user: does it look coherent, can they identify the project, choose the correct route, and recognize success without guessing?

## Deliver

Write the requested file or return the requested review. Briefly report what changed, what was checked, and any unresolved factual blocker. Keep research notes, fact maps, and editorial commentary out of the README unless asked. Publish, commit, or change repository settings only when authorized by the user's task.

For underlying observations and their limits, consult the [200-project study index](references/source-study.md). It routes to fourteen domain groups plus the original detailed cases; read only the group relevant to the current task. The 1,000-Star minimum is a research-sample selection rule, not a requirement for repositories this skill can document.
