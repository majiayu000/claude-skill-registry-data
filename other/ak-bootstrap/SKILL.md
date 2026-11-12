---
name: ak-bootstrap
description: "Bootstrap web, mobile, CLI, API, MCP, WebMCP or library projects via ak-cook, ak-code-review, ak-enhance-ux-ax --auto and optional verified release; no planning."
when_to_use: "Invoke to start from scratch in auto, full, fast or parallel mode; --ask locks scope via ak-advise."
category: workflow
keywords: [scaffold, project, setup, boilerplate]
license: Proprietary
argument-hint: "[requirements] [--auto|--full|--fast|--parallel] [--ask] [--ultra] [--yagni] [--skip-journal]"
metadata:
  author: agentkit
  version: "1.2.0"
---

# Bootstrap - New Project Scaffolding

End-to-end project bootstrapping from idea to running code.

**Principles:** KISS, DRY | Full requested scope, nothing extra (`--yagni` to opt into scope-cutting) | Token efficiency | Concise reports

## Usage

```
/ak-bootstrap <user-requirements>
```

**Flags** (optional, default `--auto`):

| Flag | Mode | User Gates | Cook Skill |
|------|------|------------|------------|
| `--auto` | Automatic (default) | Authorization boundaries only | `--auto` |
| `--full` | Full interactive workflow | Missing material decisions | default continuation |
| `--fast` | Quick | Missing material decisions | `--fast` |
| `--parallel` | Multi-agent | Missing material decisions | `--parallel` |

**Composable flags** (combine with any mode):

| Flag | Effect |
|------|--------|
| `--ask` | Run the opening brainstorm gate as an `ak-advise` interview until the implementation scope is locked and confirmed, then continue in the selected mode (see Opening brainstorm gate) |
| `--yagni` | Opt into YAGNI: challenge and cut scope not needed for the stated outcome (default: scaffold the full requested scope). Passed through to `ak-cook` and `ak-code-review` |
| `--ultra` | Code review uses the best-of-5 verifier mode: the review phase runs `/ak-code-review codebase --ultra` (see Ultra Verifier Mode) |

**Example:**
```
/ak-bootstrap "Build a SaaS dashboard with auth" --fast
/ak-bootstrap "E-commerce platform with Stripe" --parallel
/ak-bootstrap "Redesign our marketing site" --ask
/ak-bootstrap "MCP server and CLI for our billing API"
```

## Opening brainstorm gate (all modes)

Before Git initialization, research, design, or scaffolding, capture:

- the intended product outcome;
- technology, safety, compatibility, and delivery constraints;
- explicit non-goals for this bootstrap;
- observable acceptance criteria for the running project.

Reuse an accepted brief or plan when it already contains these fields. How the
remaining gaps close depends on the flags:

- **Default (`--auto`, no `--ask`):** decide each gap yourself from the user's
  prompt, project instructions, the existing workspace, and remembered user
  preferences and prior decisions. Choose the option that best serves the stated
  outcome, record each choice as an assumption in the contract, and continue
  without an interview. Stop only at an authorization boundary: a missing
  secret, a destructive or outward-facing action the brief does not authorize,
  or spending the brief does not cover.
- **`--ask`:** activate `ak-advise` with the prompt and the evidence gathered so
  far. Let it interview the user one question at a time until outcome, scope,
  constraints, non-goals, acceptance criteria and definition of done are locked
  and the user confirms them. Use the confirmed result as the contract; skip
  advise's report delivery flags. If the runtime blocks invoking `ak-advise`
  from another skill, read its SKILL.md and run its interview steps directly.
- **`--full`, `--fast`, `--parallel` without `--ask`:** ask only about a missing
  decision that would materially change the product or safety.

No mode skips this gate; modes change execution and approval behavior only
after the contract is concrete.

Load `references/project-brief-checklist.md` and check the contract against
its core sections and the sections for each surface the project has (website
or web app, mobile app, CLI, API or service, MCP server, WebMCP, library or
SDK). A project can have several surfaces.

Record the brief's definition of done. When it names a live target
(production, a store, a registry), the project is done only after it is
released there and verified the way a real user or client reaches it; see
"Release and Live Verification" in `references/shared-phases.md`.

## Workflow Overview

```
[Brainstorm Contract (ak-advise with --ask)] → [Git Init] → [Research?] → [Tech Stack?] → [Design?] → [ak-cook: implement + test] → [ak-code-review] → [ak-enhance-ux-ax --auto (web)] → [Release & Live Verify?] → [Docs] → [Onboard] → [Done]
```

There is no separate planning phase: the locked brainstorm contract goes
straight to cook, which sizes its own implementation plan. Each mode loads a
specific workflow reference + shared phases.

## Mode Detection

If no mode flag is provided, default to `--auto`. `--ask` is not a mode; it
changes only how the opening gate closes.

Load the appropriate workflow reference:
- `--auto` (default): Load `references/workflow-auto.md`
- `--full`: Load `references/workflow-full.md`
- `--fast`: Load `references/workflow-fast.md`
- `--parallel`: Load `references/workflow-parallel.md`

All mode references inherit the opening brainstorm contract. Load
`references/shared-phases.md` for implementation through final report.

## Step 0: Git Init (ALL modes)

Inspect the actual destination, existing files, manifests and Git state first. Reuse an existing project and its branch conventions; never re-scaffold or reset it. Initialize Git only for a new project when included in the requested setup, using the repository’s requested/default branch. Preserve unrelated files.

When the brief asks for a remote repository, create it through `ak-github` with the requested owner, name and visibility, and push the default and environment branches. Apply branch protection in the release phase, after CI exists, so it cannot block the first CI setup commit. For a redesign, read the old project as a source and build the new one in its requested location; do not overwrite the old project unless the brief says so.

## Downstream ownership

After early phases (research, tech stack, design), trigger downstream skills:

### Surface Skills
Route each surface to its owning skill during tech stack, design and
implementation: `ak-web-frameworks` or `ak-frontend-development` for web,
`ak-mobile-development` for mobile, `ak-backend-development` for APIs,
`ak-mcp-builder` for MCP servers, `ak-webmcp` for WebMCP, `ak-agentize` for
agent-facing CLIs. The checklist names the rest.

### Design Phase
A project without a visual interface (for example a CLI, API, MCP server or
library) skips the wireframe and visual design steps in the workflow
references and designs its interface contract (commands, routes, tool
schemas, public API) as part of the brainstorm contract instead.

When the project has a visual interface and visual quality or art direction is
a primary requirement, the design step activates **ak-frontend-design** with
the accepted brand, keep and rebuild lists, and requested design contract files (for example `DESIGN.md`,
`REVIEW.md`, `AGENTS.md`). It owns art direction and polish; bootstrap does not
restate its guidance. When it is active, the `ui-ux-designer` wireframes in the
workflow references are produced under that direction, not as a second design.

### Implementation Phase
Bootstrap does not run `ak-plan`. Activate **ak-cook** directly with the
brainstorm contract (outcome, constraints, non-goals, acceptance criteria,
definition of done, recorded assumptions) plus the research, stack and design
outputs, and the mode-appropriate flag:
- `--full` → `/ak-cook <brainstorm contract>` (continue within accepted scope)
- `--auto` → `/ak-cook --auto <brainstorm contract>` (autonomous implementation)
- `--fast` → `/ak-cook --fast <brainstorm contract>` (skip extra research)
- `--parallel` → `/ak-cook --parallel <brainstorm contract>` (multi-agent execution)

Cook sizes its own implementation plan from the contract and runs the tests.

### Code Review Phase
After cook, activate **ak-code-review** on the new project (`codebase`; for
work added to an existing project, `--pending` while uncommitted, otherwise the
PR or each commit hash); add `--ultra` when bootstrap received it. Send
blocking findings back through cook with the same mode flag, then review again
with the same flags. Details and stop limits are in `references/shared-phases.md`.

### UX and AX Enhancement Phase
When the project has a website or web app, activate **ak-enhance-ux-ax
--auto** after code review passes, then continue to release. Skip it for
projects without a web surface. Details are in `references/shared-phases.md`.

## Role

Elite software engineering expert specializing in system architecture and technical decisions. Brutally honest about feasibility and trade-offs.

## Critical Rules

- Activate relevant skills from catalog during the process
- Keep all research reports ≤150 lines
- Resolve documentation paths from repository instructions and navigation
- DO NOT implement code directly — delegate through cook; do not add a separate `ak-plan` phase
- Lead with the outcome. Keep reports short by being selective, not by compressing the writing into fragments or arrow chains; write complete sentences.
- List unresolved questions at end of reports
- Follow the installed journal owner and its opt-out preference to write a concise technical journal entry upon completion — unless the shared "Journal step — opt-out" below applies.

### Journal step — opt-out

Skip the automatic `/ak-journal` step when either applies:
- The invocation includes the `--skip-journal` flag, OR
- `ak config prefs resolve --json | jq -r 'if .prefs.journal.auto == false then "false" else "true" end'` returns `false`. If the command errors or prints anything other than the exact string `false`, treat as `true` (default) — corrupt or missing config never suppresses the automatic journal.

Precedence: flag > project config > user config > default (`true`).
When skipped, print one line:
- `journal skipped by --skip-journal` (flag), or
- `journal skipped by preference` (config).

Explicit `/ak-journal` and `ak journal create` are unaffected.

## References

- `references/workflow-full.md` - Full interactive workflow
- `references/workflow-auto.md` - Auto workflow (default)
- `references/workflow-fast.md` - Fast workflow
- `references/workflow-parallel.md` - Parallel workflow
- `references/shared-phases.md` - Common phases (implementation → code review → UX/AX enhancement → release and live verification → final report)
- `references/project-brief-checklist.md` - Brief coverage checklist: core sections plus web, mobile, CLI, API, MCP, WebMCP and library surfaces

## Ultra Verifier Mode (`--ultra`)

Bootstrap does not fan itself. When `--ultra` is present, the code review
phase runs `/ak-code-review codebase --ultra` (for work added to an existing
project, `--pending --ultra` or the PR or commit with `--ultra`), including the
re-review after UX/AX enhancement, and the code-review skill owns the best-of-5
candidate dispatch, verification, and its evidence-validated union finalizer.
Cook and enhance-ux-ax still run with their mode-appropriate flags, so
`--ultra` combines with every mode, including `--parallel`. Never pair it with
code-review's `codebase parallel`, which that skill treats as a hard-stop.

Full mechanics live in `../ak-brainstorm/references/ultra-verifier-mode.md`. It
is a best-of-5 verifier mode inspired by LLM-as-a-Verifier, not the full
framework.
