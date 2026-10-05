---
name: cross-project-comparison
description: Compare the current project with an external knowledge source (Git repo, web article, or local path) to produce a structured gap analysis and adoption plan
---

# Cross-Project Comparison

Compare the current project with an external knowledge source to identify gaps, strengths, and adoption opportunities. The source can be a Git repository, a web article or blog post, or a local directory. Produces a prioritized plan for what to bring from the source into the current project.

## When to Use This Skill

Use this skill when:
- Comparing the current project with an external open-source project or internal sibling repository
- Analyzing a web article, blog post, or technical guide for ideas to adopt into the current project
- Benchmarking AI assistant configuration (skills, commands, hooks) between projects
- Evaluating whether patterns, tools, or configurations from another source should be adopted
- Auditing configuration drift between related projects (e.g., microservices that should share standards)
- Preparing an adoption or migration plan from one tooling setup to another

**Trigger phrases**: "compare projects", "benchmark against", "what does that project have", "adoption plan", "cross-project analysis", "compare repos", "what are we missing", "evaluate external repo", "analyze this article", "what can we learn from"

## What This Skill Does

1. **Source-adaptive analysis**: Detects whether the input is a Git repo, a web article, or a local path, and applies the appropriate analysis strategy.
2. **Multi-dimensional comparison** (for project sources): Evaluates both projects across 11 comparison dimensions covering stack, AI config, skills, commands, CI/CD, docs, testing, security, developer experience, structure, and patterns.
3. **Insight extraction** (for article sources): Extracts actionable techniques, patterns, and recommendations from an article, then evaluates each against the current project.
4. **Gap analysis**: Identifies what each source has that the current project lacks, and where the current project could be improved.
5. **Adoption planning**: Transforms gaps into a prioritized, sequenced, effort-estimated plan using a value/effort scoring matrix.
6. **Conflict detection**: Flags cases where adopting an external pattern would conflict with existing conventions or introduce unwanted dependencies.

## Instructions

### Step 1: Identify Source Type and Establish Scope

Classify the external source into one of three types:

| Source Type | When | Analysis Approach |
|-------------|------|-------------------|
| **Git repository** | URL contains `github.com`, `gitlab.com`, `bitbucket.org`, or ends in `.git` | Full 11-dimension comparison |
| **Web article** | Any other `http://` or `https://` URL | Insight extraction and relevance analysis |
| **Local path** | Filesystem path | Full 11-dimension comparison |

For project sources (repo or local), determine which of the 11 dimensions are relevant. For most comparisons, all dimensions apply. For focused comparisons (e.g., "compare only the testing setup"), limit to the relevant subset.

The 11 dimensions (for project sources):

| # | Dimension | What to Examine |
|---|-----------|----------------|
| 1 | **Project Identity** | Name, description, version, license, README quality |
| 2 | **Technology Stack** | Languages, frameworks, build tools, test runners, linters, package managers |
| 3 | **AI Assistant Configuration** | `.claude/`, `.github/copilot-instructions.md`, `.gemini/`, `.cursor/`, skills count, commands count, hooks, context files, instruction templates |
| 4 | **Project Structure** | Directory layout, organizational pattern (layered, feature-based, domain-driven), depth |
| 5 | **Skills and Capabilities** | Named skills, inferred capabilities from scripts/CI/config, coverage by category |
| 6 | **Commands and Automation** | Slash commands, scripts, Makefiles, task runners, npm/pip scripts |
| 7 | **CI/CD and Hooks** | GitHub Actions, GitLab CI, pre-commit hooks, automated checks, deployment pipelines |
| 8 | **Documentation** | README, API docs, architecture docs, ADRs, changelogs, guides, onboarding |
| 9 | **Testing Strategy** | Unit, integration, e2e, property-based, fuzz, mutation; coverage tooling |
| 10 | **Security Posture** | Dependency scanning, secret detection, SAST/DAST, security policies, CVE tracking |
| 11 | **Developer Experience** | Setup scripts, containerization, devcontainers, environment management, IDE config |

### Step 2: Inventory the Source

**For project sources (repo or local):**

Systematically collect findings for every in-scope dimension. Look at:
- Manifest files (package.json, pyproject.toml, Cargo.toml, go.mod)
- Configuration directories (.claude/, .github/, .vscode/, .devcontainer/)
- CI/CD files (.github/workflows/, .gitlab-ci.yml, Jenkinsfile)
- Documentation files (README.md, docs/, CHANGELOG.md, ARCHITECTURE.md)
- Script directories (scripts/, Makefile, justfile, taskfile)
- Test directories (tests/, __tests__/, spec/, test/)

**For article sources:**

Extract every actionable insight from the article:
- Techniques, methods, or patterns described
- Tools, libraries, or services recommended
- Best practices or anti-patterns identified
- Workflows or processes proposed
- Architectural or design recommendations

Number each insight and note which section of the article it comes from. Treat each insight as an equivalent to a "capability" in the project comparison.

### Step 3: Classify Differences

**For project sources**, place every difference into one of four buckets:

| Bucket | Symbol | Action |
|--------|--------|--------|
| **External-only** | + | Adoption candidate: evaluate for import |
| **Current-only** | = | Strength to preserve: do not lose this |
| **Both, different approach** | ~ | Compare quality: pick the better approach |
| **Both, equivalent** | . | No action needed |

**For article sources**, classify each extracted insight as:

| Status | Meaning |
|--------|---------|
| **Already implemented** | The current project does this. Cite the file(s) as evidence. |
| **Partially implemented** | The current project does something similar but with gaps. Cite file(s) and explain the gap. |
| **Missing** | The current project does not do this. Explain where it could be added. |
| **Not applicable** | The insight does not apply to this project's domain, stack, or goals. |

### Step 4: Score Adoption Candidates

Apply the value/effort matrix to each adoption candidate (whether from a project gap or an article insight):

```
           Low Effort    Medium Effort    High Effort
High Val   P0 (Now)      P1 (Soon)        P1 (Plan it)
Med Val    P1 (Soon)     P2 (This Q)      P3 (Backlog)
Low Val    P2 (If easy)  P3 (Backlog)     Skip
```

**Value criteria**:
- High: Addresses a known pain point, improves security, or unblocks a workflow
- Medium: Improves quality, coverage, or developer experience
- Low: Cosmetic, stylistic, or marginal improvement

**Effort criteria**:
- Low: Copy a file, add a config entry, or make a small edit
- Medium: Adapt a pattern to fit existing conventions, create new files, or update multiple locations
- High: Requires architectural changes, new dependencies, or significant refactoring

### Step 5: Security and Reverse-Engineering Assessment (MANDATORY)

Before sequencing any adoption items, run every candidate through the host repository's MCP registry and security policy. This gate prevents the common failure mode where a plausible-looking pattern would introduce a new third-party data processor, new outbound calls, or credential sprawl. The assessment has three parts:

**5.1 Threat model comparison** - for both projects, document: new runtime dependencies, outbound-call destinations, credentials/API keys required, whether source code / prompts / query text leaves the local machine, whether a new commercial relationship with a third party is required.

**5.2 Per-item risk scorecard** - assign each adoption candidate a risk tier: **None / Low / Medium / High**. High-risk items are gated on the viability analysis in 5.3 before they can appear in the adoption plan.

**5.3 Reverse-engineering viability** - classify every candidate per the decision tree:
- `re-full` - fully reverse-engineerable into a local internal artifact
- `re-partial` - partially reverse-engineerable; ship what's local, document the gap
- `skill-native` - achievable by instructing the agent's own LLM; replace with a skill, not an MCP / external integration
- `vendor-intrinsic` - third party IS the intended destination; defer rebuild to later unless audit posture is urgent
- `drop-outright` - no local equivalent possible and not worth the trust cost

**5.4 Recommendation ordering** - re-sequence all adoption candidates in this order before they enter the plan:
1. `skill-native` (zero-code wins first)
2. `re-full` / `re-partial` (build internal equivalents)
3. `vendor-intrinsic` (only when intrinsic AND non-RE'able AND extremely worth it; justify inline)
4. `drop-outright` (moves to the NOT-recommended list, not the plan)

This ordering IS the adoption plan. P-tier (value/effort from Step 4) operates WITHIN each RE bucket, not across buckets.

### Step 6: Sequence Adoption Items

Order the (RE-re-sequenced) adoption items accounting for dependencies. Items that enable other items come first. Group items that can be done in parallel. When chaining into `/generate-plan`, always pass `reverse-engineer-first=true` so the generated plan sequences phases per the RE ordering.

### Step 7: Document Risks and Conflicts

For each adoption item, explicitly document:
- Whether it conflicts with an existing pattern in the current project
- Whether it introduces a new dependency or maintenance burden
- Whether it requires changes to existing files (higher risk) vs. adding new files (lower risk)
- Any items explicitly NOT recommended for adoption, with reasoning

Items classified as `drop-outright` in Step 5 belong in the NOT-recommended list, with the policy grounds for rejection cited by name.

## Best Practices

- **Compare function, not form**: A Makefile and a justfile serve the same purpose. A `.cursorrules` file and a `$CODEX_HOME/skills/SKILL.md` file may encode the same knowledge differently. Look past the format to the capability.
- **Curate ruthlessly**: Do not recommend adopting everything. The cost of maintaining adopted code is ongoing. Only recommend items where the benefit clearly exceeds the maintenance cost.
- **Preserve identity**: The current project has its own conventions and style. Adapt patterns from the external source to fit, rather than copying verbatim.
- **Flag new dependencies**: Any adoption item that introduces a new tool, library, or runtime dependency deserves extra scrutiny.
- **Cite evidence**: Every claim must reference specific file paths (for projects) or article sections (for articles). "The article recommends better testing" is not actionable. "The article recommends property-based testing using Hypothesis (Section 3), and the current project has no property-based tests" is actionable.

## Quality Checklist

- [ ] The source type was correctly identified and the appropriate analysis strategy was applied
- [ ] For project sources: every comparison dimension has been evaluated for both projects
- [ ] For article sources: every actionable insight has been extracted and evaluated
- [ ] Every gap or relevance claim cites specific file paths or article sections
- [ ] Adoption items have concrete target locations in the current project
- [ ] Priority assignments are consistent with the value/effort matrix
- [ ] Conflicts with existing conventions are explicitly flagged
- [ ] Items NOT recommended for adoption include reasoning
- [ ] **Step 5 Security and Reverse-Engineering Assessment is complete** - threat model table, per-item risk scorecard, and per-item RE classification are all present
- [ ] **Step 5.4 ordering is used to sequence the adoption plan** - skill-native first, then RE builds, then vendor-intrinsic (justified), then drops moved to NOT-recommended
- [ ] **MCP Registry Policy is cited by name** in the Rationale column for every adoption item that involves an outbound call, new API key, new third-party data processor, or new runtime dependency
- [ ] Reports missing Step 5 fail this checklist

### Iterative Refinement Strategy

This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
