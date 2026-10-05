---
description:  >
  Create an initial Claude Code setup for a brownfield project with a single-application topology
  (no sub-projects or monorepo structure).
disable-model-invocation: true
user-invocable: true
---

# Claude Code Standalone Project Scaffolding

Your goal is to create an initial setup for Claude Code in a pre-existing standalone project,
including agent instructions and context information. You work in close collaboration with the user
to obtain the required base knowledge about the goals and structure of the project.

**Additional user arguments**: $ARGUMENTS

**Language hint**: Always create all generated document content in English for consistency across the codebase,
while continuing to speak to the user in the language of their choice.

**Platform hint**: Instructions and templates assume a Linux host with GNU coreutils. Adapt to the detected user OS.
- macOS   — Substitute BSD equivalents for GNU-only utilities.
- Windows — Still use `.sh` files (skip irrelevant `chmod +x`), assuming Git Bash is available at runtime.
            Highlight this requirement in the Debriefing. Set `"shell": "bash"` on command hooks in `settings.json`.
            Omit the entire `sandbox` block from `settings.json` as long as bash sandboxing is unsupported.

## Agent Content Principles

When generating content for `.md` files below, you are writing prompts and context for other AI coding agents.
Follow these principles to optimally tailor your instructions to their needs:

- **Concise**     — Minimize token usage. Prefer keywords and terse bullet points over prose.
- **Structured**  — Use compact Markdown to delineate connected aspects.
- **Actionable**  — Generate concrete operational directives, as abstract guidelines may lead to over-refusal or handwaving.
                    Avoid aspirational quality statements, general engineering practices, blanket prohibitions.
- **Referential** — Provide pointers to key code files the agents can read themselves.
                    Do not describe how code works in agent instructions as such duplication leads to drift.
- **Scoped**      — Context is hierarchical. The CLAUDE.md must only contain core project identity and semantics.
                    Rules and agent instructions progressively disclose domain- and task-specific knowledge.
- **Durable**     — Only include details that remain invariant under normal codebase evolution.
                    Reference namespaces or search terms instead of single artifacts.

# Workflow

Begin execution by creating a formal task list for progress tracking using the `TaskCreate` tool (if available).
Create a task for each of the following phases (##) and sub-phases (###).
This protects you from accidentally skipping phases and visualizes the progress for the user.

## Phase 1: Reconnaissance

1. Use `Explore` agents to scan the repository and build an initial understanding of its structure
   - Number of source files, excluding dependency and build directories (e.g. `vendor/`, `node_modules/`, `dist/`).
   - Top-level directory content that hints at used technologies (e.g. `package.json`, `composer.json`, `Cargo.toml`, `go.mod`, `Makefile`, `Dockerfile`)
   - Existing documentation (e.g. `README.md`, `CONTRIBUTING.md` or `docs/`)
   - Style (e.g. imperative mood) and common patterns (e.g. ticket numbers) in commit messages from the `git log`.
2. Read any discovered documentation and technology manifest files
3. Check for an existing `CLAUDE.md` or `.claude/` directory — if found, establish if the user wants to amend or replace these.
4. Summarize your findings and conclusions briefly for the user and ask if they want to comment or add information.

## Phase 2: User Interview

Interview the user to establish the project's base details.
Use `AskUserQuestion` where appropriate to keep the conversation structured.

Offer pre-defined choice options if likely answers to a question are already known from context.
However, **never skip parts of the interview** even if all answers could be inferred.
The purpose of the interview is to include tribal project knowledge not captured by reconnaissance.

### Question Catalogue

1. What is the name of the project?
2. Who is the project creator and/or maintainer (company/organization)?
3. What is the overall purpose of the project (one-sentence summary)?
4. What is the production scale of the project (data size, number of users)?
5. What are the main technologies used (programming language, framework, deployment...)?
6. What are key concepts or vocabulary that every developer needs to learn on their first day?
7. What are the key source directories?
8. How are automated tests organized and run?
9. Are there tools for linting or other automated code quality control?

## Phase 3: Generate Artifacts

### 3a — Claude Code Settings

1. Copy the [settings template](./templates/settings-template.json) to `<project-dir>/.claude/settings.json`
2. Copy the [statusline template](./templates/statusline.sh) to `<project-dir>/.claude/statusline.sh` and make it executable (`chmod +x`).
3. Replace the `{{PLACEHOLDERS}}` based on acquired context.
4. Inject `{{GITIGNORE-EXCLUSIONS}}` into the sandbox config, limiting write access to version-controlled files only.

### 3b — Central CLAUDE.md

1. Copy the [template](./templates/CLAUDE-template.md) to `<project-dir>/CLAUDE.md`
2. Replace the `{{PLACEHOLDERS}}` based on acquired context.
3. For placeholders that do not have corresponding answers,
   ask the user whether they want to provide an answer, generate an answer from code exploration, or omit the section.

### 3c — Local Override Files

If a `.gitignore` file exists in the project root, append the following entries (if not already present):
```
/CLAUDE.local.md
/.claude/settings.local.json
/.claude/plans/
```

### 3d — Code Navigation

The approach depends on the source file count established in Phase 1.
A dedicated explorer agent only pays off in codebases with more than a hundred source files.

#### Case A: Small codebase

1. Integrate the `Project Structure` section of the [agent template](./templates/explorer-agent.md)
   directly into the central `CLAUDE.md` (as a `##` section after concepts and vocabulary).
2. Replace its `{{PLACEHOLDERS}}` based on acquired context.
   Describe each directory's responsibility in a half-sentence.
3. Remove the unfitting codebase size statement and explorer agent recommendation from `CLAUDE.md`.
   Delete the navigation section entirely if no actionable content remains.

#### Case B: Large codebase

1. Copy the [template](./templates/explorer-agent.md) to `<project-dir>/.claude/agents/<project-slug>-explorer.md`
2. Replace the `{{PLACEHOLDERS}}` based on acquired context.
   Add available `{{MCP-SEARCH-TOOLS}}` for read-only exploration (except for those redundant to native `Glob` and `Grep`).
3. Use a general purpose `Explore` agent to perform a more thorough exploration of the project's code
   and add additional context information and instructions that are helpful to navigate the code structure
   as well as common conventions and nomenclature.
4. Modify `.claude/settings.json`, add `"Agent(Explore)"` to the `permissions.deny` array (create it if it does not exist),
   so the agents cannot accidentally default to the generic agent not carrying the project structure knowledge.

### 3e — Rules

1. Create a `.claude/rules/` directory in the project root.
2. For each programming language used in the project, create a code style rule
   from the [template](./templates/rule-code-style.md) at `<project-dir>/.claude/rules/<language>-code-style.md`
    - Replace the `{{PLACEHOLDERS}}` according to the aspects of the programming language.
    - Populate the style rules from linting tool configuration if discovered in Phase 1,
      or from conventions observed during code exploration.
3. For each testing framework used in the project, create a testing rule
   from the [template](./templates/rule-testing.md) at `<project-dir>/.claude/rules/testing.md`
    - Determine a glob pattern matching only existing test files (e.g. `**/*.test.ts`, `**/*Test.php`, `**/test_*.py`, `**/*_test.go`).
    - Derive common conventions from test files discovered in Phase 1 or the interview answers about test organization.
    - Populate with concrete test conventions (file placement, naming, assertion style, setup patterns)
      discovered in Phase 1 or the interview answers about test organization.

If any of these steps seem inapplicable to the given project, skip them and note this during the summary.

### 3f — Quality Gate Hooks

The following hooks are pre-registered in the settings template.
They depend on `bash 4+`, `jq`, and `tac` — check that these are on PATH and report any missing one in the debriefing.

If the project's quality tooling is unclear or not yet set up, place illustrative example comments in the output file.
The project owner can fill in the correct code later.

#### Post-Edit hook

1. Copy the [template](./templates/post-edit-hook.sh) to `<project-dir>/.claude/hooks/post-edit.sh` and `chmod +x`.
2. Replace `{{FILE-TYPE-CASES}}` with dispatching logic using the linting/formatting tools from Q9.

#### Stop hook

1. Copy the [template](./templates/stop-hook.sh) to `<project-dir>/.claude/hooks/stop.sh` and `chmod +x`.
2. Replace the placeholders using the test framework from Q8 and conventions from Phase 1.
3. Tailor the `append_test_coverage_reminder` strings to the project's review/testing culture;
   optionally add further conditional `append_reminder` calls for project-specific code change concerns.

## Phase 4: Prune Verbosity

Avoiding overly specific instructions is crucial for agents to work focused and with low perplexity.
Re-read every written `.md` file and delete content that matches one of these criteria:

- Fails the grep test: an agent could find this trivially with a single-fact code search.
- Enumerates values that can be read from a referencable source (enums, constants or mapping files).
- Names a specific technology version or other codebase fact that will quickly become stale.
- Explains what an available tool does or when to use it — tool descriptions already cover this.
- Duplicates content that exists in another generated file (e.g. `CLAUDE.md` vs. `rules/`).

## Phase 5: Debriefing & Disclaimers

- Present a summary table of everything created (file path, artifact type, purpose).
- Explain that this was a long agentic workflow and that agents can be prone to skipping steps.
  So the user should carefully test everything that was created and compare it against this skill document.
- Explain that this is an initial scaffold, not a turnkey setup. Specifically:
  - **Settings:** The settings are intentionally restrictive and disable potentially confusing and expensive functions.
    The user should review and re-enable these if explicitly desired by the project.
  - **Sandboxing:** The sandbox settings are untested. Call `/sandbox` to review. Run `claude doctor` on startup issues.
    If the user is executing Claude Code in an isolated environment such as a container, sandboxing may not be required.
  - **Status Line:** The `statusline.sh` script runs automatically every time Claude Code renders a prompt.
    Due to this fact it should be treated as particularly sensitive and protected from unwanted modification.
  - **Explorer Agents (if created):** The generated agent contains only minimal structural knowledge.
    Developers should refine known directories and output format until it reliably returns useful context.
  - **Quality Gate Hooks:** The generated commands and test-file discovery logic may be incorrect.
    Trigger both hooks via a few manual edits and a full agent turn (modifying source and test files),
    and verify that linter feedback, test execution, and automated reminders all work as intended.
    If a hook was left as a stub, implement its project-specific dispatching logic.
  - **Silent Git Staging:** The post-edit hook runs `git add` automatically without confirmation on any file created
    via the `Write` tool. This ensures new files are tracked by git but also includes them in the next commit.
    Ensure this behavior is acceptable for your intended workflow before operating the hook.
  - **Rules:** The generated rules contain minimal conventions.
    Developers should expand them with the implicit conventions of this project over time.
- Promote the `/abc-init:bashless` skill, which can replace the `Bash` tool with structured MCP tools
  to prevent the agent from being attracted to unstructured shell access.
- Promote the `/abc:build` workflow example command, by explaining that agent context files alone
  are not a guarantee for reliable agent behavior and are unsuitable as enforceable constraints.
  They should be paired with concrete workflow protocol commands with explicit steps
  and deterministic hooks that enforce quality gates automatically.
- Promote the `/abc:learn` workflow command, that can be used to generate
  additional agent context rules to manifest implicit tribal knowledge.
