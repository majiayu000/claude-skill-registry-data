---
name: general-readme-skill
description: >
  Use when generating or improving README.md for any project.
  Trigger on /readme, "generate readme", "write readme",
  "create project documentation", "更新README", "帮我写 README".
version: 1.0
tags: documentation, readme, auto-generate, project-docs
---

# General README Skill
Generate professional, human-feeling README files for any project.
Strictly follow real project content, reject filler text and placeholder content.

## Overview
Full workflow: **Configure → Scan → Generate → Beautify → Output**
**Zero external dependencies.** All rules, templates and assets are embedded in the skill.
No third-party CLI, runtime or network service required for core functions.

## Trigger Rules
Trigger this skill when user inputs match any of the following:
- Exact command: `/readme`
- Text commands: generate readme, write readme, create project documentation, update readme
- Chinese commands: 帮我写 README, 生成项目文档, 更新README
- Scenario: User requests to create/rewrite/refresh project README

---

## Phase 1: Configuration
Collect configuration options from developer before generation.
All options have fixed default values for quick use.

Defaults (used when user supplies no configuration):
- Tone Profile = Professional
- Badge Style = Flat
- Primary language = English
- Secondary languages = none
If the user provides no configuration, use these defaults.

### 1. Tone Profile (Default: Professional)
Select README writing style:
- **Energetic** — Direct, confident, allow emojis in features. Reference: FastAPI style.
- **Minimal** — Terse, code-first, no redundant description. Reference: Tailwind CSS style.
- **Professional** — Neutral, structured, formal layout. Reference: Kubernetes style.

### 2. Badge Style (Default: Flat)
Select shields.io badge appearance:
- **Flat** — Clean, compact, standard style
- **Flat-square** — Sharp edges, modern compact style
- **for-the-badge** — Tall, bold, highly visual style

### 3. Multi-Language Setting
- Primary language (Default: English)
- Secondary languages (Optional: Chinese, Japanese, Korean, Spanish, French etc.)
File naming follows rules in `language-guide.md`.

---

## Phase 2: Project Scan
Use built-in `Read`, `Grep`, `Glob` tools to scan local project directory.
> Rules: Only read static files. **Never execute, modify or delete any project files.**
> Ignore directories: node_modules, .git, build, dist, __pycache__, .venv, .next, coverage, logs

Detector priority and tie-break rules (deterministic order):
1. Manifest parsing: inspect recognized manifests (package.json, pyproject.toml, go.mod, Cargo.toml, etc.). If a manifest clearly declares language/framework, mark that as primary.
2. Explicit dependency declarations: prefer declared dependencies/devDependencies when identifying frameworks.
3. File-extension majority: use only if manifests are absent or ambiguous.
4. Heuristic filename patterns: use as a last resort.
If multiple sources conflict, prefer the earlier item in this list. If manifests conflict (multiple package roots), prompt the user to choose which package root to document or follow the manifest precedence rules below.

### 2.1 Language Detection
1. Parse recognized manifests: package.json, pyproject.toml, Cargo.toml, go.mod, Gemfile, pom.xml, build.gradle. If a single manifest declares the project language unambiguously, that is the `Primary Language`.
2. If no manifest is present or manifests are ambiguous, use majority file-extension count across the selected package root.
3. If multiple manifests declare different languages for different package roots, prompt the user to select which package root to document, or default to manifest precedence: `package.json > pyproject.toml > go.mod > Cargo.toml`.

### 2.2 Framework Detection
Parse dependency fields to identify used frameworks:
- package.json → dependencies / devDependencies
- requirements.txt / pyproject.toml → Python frameworks
- Gemfile → Ruby frameworks
- go.mod → Go frameworks
- Cargo.toml → Rust frameworks

### 2.3 Build & CI/CD Detection
- Makefile → Make commands
- CMakeLists.txt → CMake build
- package.json → Scripts field
- Dockerfile / docker-compose.yml → Docker deployment
- .github/workflows / .gitlab-ci.yml / Jenkinsfile → CI/CD pipelines

### 2.4 Database & ORM Detection
- Database connection config: DATABASE_URL, DB_HOST and related fields
- ORM frameworks: Sequelize, TypeORM, Prisma, SQLAlchemy, ActiveRecord, GORM
- Database drivers in dependency list

### 2.5 Architecture Type Detection
Classify overall project architecture:
- **Microservice**: Multiple independent service folders + .proto / RPC files
- **Frontend-Backend Split**: client/server or frontend/backend directories
- **Monolithic**: Standard MVC / layered structure
- **Event-Driven**: Message queue dependencies (Kafka, RabbitMQ, etc.)

### 2.6 API Style Detection
Identify interface type:
- **REST**: Route / endpoint definition files
- **gRPC**: .proto definition files
- **GraphQL**: .graphql schema files
- **WebSocket**: WebSocket server implementation code

### 2.7 License Detection
- Read root `LICENSE` / `LICENSE.md`
- Recognize common licenses: MIT, Apache-2.0, GPL-3.0, BSD-2-Clause, BSD-3-Clause, ISC, MPL-2.0, Unlicense

If no LICENSE file is present, do not add a license section; instead add a one-line recommendation: `No LICENSE file detected. Add a LICENSE to clarify project licensing.`
If multiple conflicting license files are present, list them and prompt the user to confirm which to use (for example: `Detected license files: LICENSE, LICENSE.md. Please confirm which to use.`).

### 2.8 Project Type Detection
- **Library**: Publish config for distribution, no startup script
- **Application**: Has dev/start runtime scripts, not for public publishing
- **CLI Tool**: bin field, executable output, Go cmd/ directory
- **Static Site / Demo**: Frontend-only, no backend service

### 2.9 Git & Contributor Detection
- Do NOT execute commands or modify the repository. Never run `git` or other tools that alter state.
- If a readable `.git` directory or static contributor file (e.g., `CONTRIBUTORS`, `AUTHORS`) exists and can be inspected without executing commands, extract contributors' names only (no emails). Redact or omit sensitive metadata. Example: `Contributors: 3 (Alice, Bob, and 1 other)`.
- If git metadata is inaccessible (no `.git`, shallow clone, permission denied, or cannot be read without executing), skip contributor detection and include this note: `Contributor history unavailable (no git metadata access).` Offer an option to supply contributors manually.
- Extract commit convention rules only from static config files (e.g., `.github/commit-convention.md`, `CONTRIBUTING.md`)—do not execute or parse live git logs.

### 2.10 Configuration File Detection
Scan root & config folders for .env, .env.example, *.config, *.yml, *.yaml etc.

---

## Phase 3: Generate Content
Load all reference files first, then generate content strictly by rules.

### Load Reference Files
All references located in `references/` folder:
1. `tone-profiles.md` — Style rules & sample phrases
2. `badge-styles.md` — Badge layout & grouping rules
3. `badges.md` — Technology to shields.io badge mapping
4. `diagram-templates.md` — Mermaid templates + SVG fallback
5. `section-guidelines.md` — Section writing rules & banned phrases
6. `language-guide.md` — Multi-language naming & switcher rules

Reference-file missing / invalid behavior:
- Before generation, verify that all listed files in `references/` exist and are readable. If any are missing or malformed, abort generation and return: `Missing or invalid reference files: <list>. Generation paused.`
- Optionally allow a `proceed-with-defaults` flag to continue using built-in safe defaults; require explicit user confirmation to proceed.

### Fixed Section Order (Inverted Pyramid)
**Do NOT reorder sections. Skip any section if no matched project data.**
No N/A, Coming soon or placeholder content.

Fixed-order application and manual content preservation:
- Fixed section order applies only to auto-generated sections. Preserve any manually written content in-place when it is wrapped with HTML markers `<!-- MANUAL-START -->` and `<!-- MANUAL-END -->`, or when a top-level section is not tagged `<!-- AUTO-GENERATED -->`.
- If a preserved manual section breaks the fixed order, leave it in place and insert regenerated auto sections around it rather than moving or deleting manual content.

1. **Hero** — Project name(H1), one-line description, badges. **Use HTML centered layout for professional appearance (see Hero Template below).**
2. **Features / Why** — Max 6 core differentiating features
3. **Quick Start** — Max 4 copy-paste command steps
4. **Usage** — Real code examples, max 4 items
5. **Architecture Diagram** — Mermaid/SVG with color classes. **Required for all project types.** Select diagram type based on architecture (see diagram-templates.md)
6. **Configuration** — Table view, only if config files exist
7. **API** — Endpoint table, only if API routes exist
8. **Directory Structure** — Annotated tree, max depth = 3
9. **Tech Stack** — Grouped by technical layers
10. **Deployment** — Docker/CI guide, only if deployment files exist
11. **Contributing** — Standard fork → branch → commit → PR workflow
12. **License** — One-line license statement

### Hero Template (HTML Centered Layout)

The Hero section uses HTML `<p align="center">` tags for a professional, centered appearance. This layout is inspired by modern open-source projects like Understand Anything.

**Structure:**
```html
<h1 align="center">{PROJECT_NAME}</h1>
<p align="center">
  <strong>{ONE_LINE_DESCRIPTION}</strong>
  <br />
  <em>{SUBTITLE_WITH_KEYWORDS}</em>
</p>

<p align="center">
  <a href="#quick-start"><img src="https://img.shields.io/badge/{QUICK_START_TEXT}-{COLOR}?style=for-the-badge" alt="Quick Start" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/{LICENSE_TEXT}-{COLOR}?style=for-the-badge" alt="License" /></a>
</p>

<p align="center">
  {PLATFORM_BADGES}
</p>

<p align="center">
  {LANGUAGE_SWITCHER}
</p>
```

**Rules:**
- Title: Use `<h1 align="center">` instead of Markdown `#`
- Description: Use `<p align="center">` with `<strong>` for main description
- Subtitle: Use `<em>` for keywords/features line
- CTA Buttons: Use `for-the-badge` style for visibility (Quick Start, License)
- Platform Badges: Add AI IDE platform badges (Claude Code, Copilot, Cursor, etc.)
- Language Switcher: Use `<p align="center">` with anchor tags
- Badge Style: Platform badges use the user-selected style from Phase 1

**Platform Badge URLs:**
```markdown
![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=claude&logoColor=white)
![GitHub Copilot](https://img.shields.io/badge/GitHub_Copilot-000000?style=flat&logo=github&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-000000?style=flat&logo=cursor&logoColor=white)
![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-4285F4?style=flat&logo=google&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-000000?style=flat&logo=openai&logoColor=white)
```

### Critical Generation Rules (Must Follow)
1. **No fabrication**: All features, commands, code examples must come from real project files.
2. **Style consistency**: All text follows selected Tone Profile and banned phrase list.
3. **Badge rules**: Follow grouping & style in `badge-styles.md`.
4. **Structure rules**: Every section strictly obeys `section-guidelines.md`.
5. **Incremental Update**: If `README.md` already exists:
   - Preserve manual content only when explicitly marked: content between `<!-- MANUAL-START -->` and `<!-- MANUAL-END -->`, and any top-level sections not tagged `<!-- AUTO-GENERATED -->`.
   - Re-generate only sections marked `<!-- AUTO-GENERATED -->` or other clearly auto-scanned regions.

Precedence (constraint resolution order):
1. Privacy Protection (must) — mask secrets and private data.
2. Preserve manual content (markers above) — do not move or delete.
3. No fabrication — do not invent facts not present in project files.
4. Fixed section order — applies when composing only auto-generated sections; do not move preserved manual sections.
If constraints conflict, follow the numeric precedence above.
6. **Privacy Protection**: Mask sensitive keys, passwords and private info in config/code.

---

## Phase 4: Beautification (Auto-Triggered)

After Phase 3 generates the README, this phase automatically triggers to enhance visual presentation by replacing suitable Markdown syntax with HTML.

### 4.1 Trigger Conditions

- Automatically triggers after Phase 3 completes
- Skips if user explicitly disables beautification (`--no-beautify` flag)
- Skips if README already contains HTML markers (`<!-- BEAUTIFIED -->`)

### 4.2 Execution Flow

**Step 1: Analysis (Automatic)**
Scan the generated README.md and identify beautifiable elements:
- Hero region: title, description, badges, language switcher
- Content region: tables, lists, collapsible panels
- Code region: code blocks, Mermaid diagrams
- Structure region: dividers, anchor links

**Step 2: Confirmation (User Interaction)**
Display beautification suggestions to user:

```
AI: README generation complete! Analyzing beautification opportunities...

Found the following beautification suggestions:

1. ✅ [Hero] Title centered → <h1 align="center">
2. ✅ [Hero] Description centered and bold → <p align="center"><strong>
3. ✅ [Hero] Add CTA buttons
4. ✅ [Hero] Platform badges centered
5. ⚪ [Content] Tables keep Markdown (easier to maintain)
6. ⚪ [Code] Code blocks keep Markdown (has syntax highlighting)

Accept these suggestions?
[Accept All] [Confirm Each] [Reject All]
```

**Step 3: Execution (Automatic)**
Apply selected beautifications based on user confirmation.

### 4.3 Beautification Rules

**Hero Region (Mandatory):**
- Title: `# Title` → `<h1 align="center">Title</h1>`
- Description: `> Description` → `<p align="center"><strong>Description</strong></p>`
- Subtitle: keywords → `<p align="center"><em>keywords</em></p>`
- CTA Buttons: `[Quick Start](#)` → `<a href="#"><img src="badge?style=for-the-badge"></a>`
- Platform Badges: `![Badge](url)` → `<p align="center"><img src="url"></p>`
- Language Switcher: `[EN](README.md)` → `<p align="center"><a href="README.md">EN</a></p>`

**Content Region (Optional):**
- Tables: Keep Markdown (easier to maintain)
- Lists: Keep Markdown (easier to maintain)
- Collapsible panels: Keep HTML (already formatted)

**Code Region (Keep As-Is):**
- Code blocks: Keep Markdown (has syntax highlighting)
- Mermaid diagrams: Keep Markdown (GitHub native support)

**Structure Region (Optional):**
- Dividers: Keep `---`
- Anchor links: Keep Markdown

### 4.4 Reference Files

- `references/beautification-rules.md` — Detailed beautification rules and HTML templates
- `references/section-guidelines.md` — Section-specific beautification notes

### 4.5 Exception Handling

- If beautification fails for an element, keep original Markdown
- If user rejects all suggestions, skip beautification entirely
- Add `<!-- BEAUTIFIED -->` marker after successful beautification

---

## Phase 5: Output
1. Generate primary `README.md` in selected primary language.
2. Generate secondary files: `README-{lang}.md` for each extra language.
3. Add language switcher on top of every README file (follow `language-guide.md`).
4. Standard format: UTF-8 encoding, unified line break, clean empty lines.
5. Final prompt to user:
   > README generated successfully. Please review and adjust manually if needed.

### Exception Handling
- If project scan returns no valid data: Output short prompt: `No valid project content detected, cannot generate README.`
- If partial scan failed: Generate available sections only, no error placeholder.

---

## Reference Files Catalog
All supporting files are independent and can be updated separately without modifying main skill.

| File Name | Core Purpose |
|----------|-------------|
| tone-profiles.md | Definition & examples for 3 writing tones |
| badge-styles.md | Layout, size, grouping rules for 3 badge styles |
| badges.md | Mapping table: technology name → shields.io badge URL |
| diagram-templates.md | Reusable Mermaid diagrams + SVG fallback templates |
| section-guidelines.md | Global writing rules, banned phrases, per-section constraints |
| language-guide.md | Multi-language file name rules & language switcher format |
| beautification-rules.md | Phase 4 beautification rules, HTML templates, transformation examples |