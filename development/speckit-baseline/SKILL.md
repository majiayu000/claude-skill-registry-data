---
name: speckit-baseline
description: Create baseline documentation for the project, establishing context for
  all future specs.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: workflows:commands/baseline.md
---

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

## What This Does

The baseline workflow creates foundational documentation by:
1. Establishing a comprehensive baseline specification of the project
2. Creating a change tracking document for all subsequent modifications

This provides essential context for you (the AI agent) when working on future tasks.

## Your Task

1. Run the script `.specify/extensions/workflows/scripts/bash/create-baseline.sh --json` from repo root and parse its JSON output for BASELINE_SPEC, CURRENT_STATE, BASELINE_COMMIT, and HAS_EXISTING_SPECS. All file paths must be absolute.
   **Note:** The script only accepts the `--json` flag and ignores `$ARGUMENTS`.
   **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

2. **Analyze the Project**:

   a. If HAS_EXISTING_SPECS is "true":
      - The baseline commit represents the project state BEFORE spec-kit was used
      - Use `git show BASELINE_COMMIT:path/to/file` to examine files at that point
      - Analyze that historical state to document what existed before specs

   b. If HAS_EXISTING_SPECS is "false":
      - Analyze the current project state
      - This is a fresh baseline for future work

3. **Generate baseline-spec.md**:

   Load `.specify/extensions/workflows/templates/baseline/baseline-spec-template.md` to understand the structure.

   Then comprehensively analyze the codebase (at the baseline commit if applicable) and fill in BASELINE_SPEC with:

   - **Executive Summary**: High-level overview of project purpose
   - **Project Structure**: Directory layout and key components
   - **Architecture**: System design, technology stack, patterns
   - **Core Functionality**: Primary features and user workflows
   - **Data Model**: Core entities and their relationships
   - **External Dependencies**: Third-party libraries and external services
   - **Build and Deployment**: Build process, testing strategy, deployment
   - **Configuration**: Environment variables, feature flags
   - **Known Issues**: Current limitations and technical debt
   - **Future Considerations**: Planned improvements and scalability concerns

   Be thorough - examine:
   - Package files (package.json, requirements.txt, pom.xml, etc.)
   - Build configurations (webpack, vite, Makefile, etc.)
   - Source code structure and key modules
   - README, documentation files
   - Configuration files
   - Database schemas or migrations
   - API routes/endpoints
   - Test files to understand tested functionality

4. **Generate current-state.md**:

   Load `.specify/extensions/workflows/templates/baseline/current-state-template.md` for structure.

   Scan the specs directory and enumerate all changes by type:

   - **Features**: List all `specs/###-*` directories with descriptions
   - **Modifications**: Find `specs/###-*/modifications/` subdirectories
   - **Bugfixes**: List `specs/bugfix/` entries
   - **Refactors**: List `specs/refactor/` entries
   - **Hotfixes**: List `specs/hotfix/` entries
   - **Deprecations**: List `specs/deprecate/` entries

   For unspecified changes (if HAS_EXISTING_SPECS is true):
   - Compare commits from BASELINE_COMMIT to HEAD
   - Identify commits not associated with spec directories

   Calculate statistics:
   - Counts for each workflow type
   - Total commits, files changed, lines added/removed
   - Specification coverage percentage

5. **Report completion**:

```
Baseline documentation created

**Location**: specs/history/
**Baseline Spec**: [BASELINE_SPEC path]
**Current State**: [CURRENT_STATE path]

{{If HAS_EXISTING_SPECS is true:}}
**Baseline Commit**: [BASELINE_COMMIT]
Note: Baseline represents project state before first spec-kit usage
{{end if}}

**What Was Documented:**

**Baseline Specification**:
- Project structure: [X] components identified
- Technology stack: [Languages/Frameworks]
- Core features: [X] primary features documented
- Architecture: [Brief architecture summary]

**Current State**:
- Features: [X] implemented
- Modifications: [X] tracked
- Bugfixes: [X] fixed
- Other workflows: [X] total
{{If unspecified changes found}}
- Unspecified: [X] commits without specs
{{end if}}

**Using This Context:**

The baseline documentation will help me (your AI assistant) understand:
- What the project does and how it's structured
- What has been built and modified
- Where technical debt exists
- What patterns and conventions to follow

This context will improve my suggestions for all future work.

**Next Steps:**
1. Review the generated documentation for accuracy
2. Make any corrections or additions to baseline-spec.md
3. Use this context when creating new specs with other workflows
4. Periodically update current-state.md as new specs are completed
```

## Important Notes

- **Do not create a git branch** - This is a documentation task
- **Be comprehensive** - The baseline is foundational context for all future work
- **Analyze deeply** - Don't just list files, understand what they do
- **Track everything** - In current-state.md, account for all changes
- **Update timestamps** - Replace {{DATE}} placeholders with actual dates
- **Link to sources** - Reference specific files and line numbers where relevant

## Quality Checks

Before finishing:
- [ ] baseline-spec.md covers all major aspects of the project
- [ ] Technology stack is accurately documented
- [ ] Core features are clearly described
- [ ] current-state.md accounts for all spec directories
- [ ] Statistics are calculated and included
- [ ] Both files use the provided template structure
- [ ] All placeholders are replaced with actual content