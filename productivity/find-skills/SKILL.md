---
name: find-skills
description: Discover, vet, and optionally install agent skills when the user asks "find a skill for X", "is there a skill that can...", "how do I add support for X", or otherwise wants reusable/installable agent capabilities. Do not use for ordinary task execution unless the user is explicitly exploring skills, tools, or capability extensions.
---

# Find Skills

This skill helps discover, evaluate, and optionally install skills from the
open agent skills ecosystem.

## When to Use

Use this skill when the user:

- Says "find a skill for X", "is there a skill for X", or "what skill should I
  install for X".
- Asks how to add a reusable capability, connector-like workflow, tool template,
  or agent extension.
- Mentions they want better agent support for a recurring domain such as design,
  testing, deployment, writing, data analysis, or code review.
- Asks whether a specialized workflow might already exist as an installable
  skill.

## When Not to Use

Do not use this skill just because the user asks for help with a task. If the
task can be handled directly with the current tools and the user is not asking
about reusable/installable capabilities, do the task instead.

Do not use this skill for local skill authoring or editing. Use `skill-creator`
when the user wants to create or improve a skill. Preserve `skill-audit`'s
explicit-only invocation policy; an ordinary review request does not activate it.

## Sources and Commands

The Skills CLI (`npx skills`) is the package manager for the open agent skills
ecosystem. The public catalog is at https://skills.sh/.

Useful commands:

```bash
npx skills find [query]
npx skills add <package>
npx skills check
npx skills update
```

Catalog contents, install counts, and source repositories change over time. Use
current CLI/catalog results for recommendations; do not rely on stale examples
or memory for package names, popularity, or safety.

## Workflow

### 1. Clarify the Need

Identify:

1. The domain, such as React, testing, design, deployment, or writing.
2. The concrete workflow the user wants help with.
3. Whether they want a skill recommendation, installation, or just a capability
   answer.

Ask a clarifying question only when the target workflow is too ambiguous to
search productively.

### 2. Search Current Sources

Check the skills catalog and CLI before recommending a package:

```bash
npx skills find <specific keywords>
```

Use specific search terms first, then try close synonyms if results are weak.
Examples:

- "react performance" for React app optimization.
- "pr review" or "code review" for pull-request workflows.
- "changelog" or "release notes" for release documentation.

If the CLI is unavailable or network access fails, use the catalog website if
possible. If neither source can be checked, say that the search could not be
verified instead of inventing results.

### 3. Vet Candidates

Do not recommend a skill based only on a search-result title. Before presenting
a recommendation, check the candidate's catalog page and source repository when
available.

Prefer candidates with:

1. A clear `SKILL.md` matching the user's workflow.
2. A reputable maintainer or source repository.
3. Meaningful usage signals such as install count, stars, recent maintenance,
   or inclusion in a trusted collection.
4. Narrow, understandable permissions and no surprising external side effects.

Treat low-install, abandoned, or unknown-source skills as experimental. Never
present unverified install counts, stars, or package metadata as facts.

### 4. Present Options

Return a short ranked list. For each candidate include:

1. Skill/package name.
2. Why it fits the user's workflow.
3. Verification signals you actually checked.
4. Install command.
5. Catalog or repository link.
6. Caveats, especially if trust or maintenance is uncertain.

If there is one clearly best candidate, recommend that one and mention any
reasonable alternatives only briefly.

### 5. Install Only With Explicit Approval

Installing a skill changes the user's local/global agent configuration. Do not
install, update, or run `npx skills add` unless the user has explicitly asked to
install that exact package or confirms after seeing the recommendation.

After approval, resolve the requested scope, target agents, and canonical
installation directories. Preserve a project-local or single-agent request;
use `-g` only for a global installation. Check the CLI's current destination
mapping against the repository's conventions before running it.

For a destination compatible with the CLI, select only the approved skill
and agents, for example:

```bash
npx skills add <owner/repo> --skill <skill> --agent <agent> --copy -y
```

Use `-y` only after the exact package is approved. In dotfiles, preserve the
paired tracked roots unless the user selected one agent. Use copy installation
where a target resolves under Google Drive; symlinks there cannot sync. Keep
downloads, staging checkouts, and package-manager caches outside Drive. If the
CLI's destination differs from the canonical root, stage the approved source
outside Drive and install the inspected files into that root with the available
skill installer or file tools. Do not silently create a second skill root.

Inspect an existing same-name skill before replacing it. Then resolve and read
the installed `SKILL.md`, confirm its real location and contents, and run the
repository's pairing/documentation checks. CLI success alone does not establish
that the active agent can discover the intended copy.

### 6. When No Good Skill Exists

If no relevant skill is found:

1. State the search terms and sources checked.
2. Say that no good match was found.
3. Offer to help with the underlying task directly.
4. If the workflow is recurring, suggest creating a local skill with
   `skill-creator` or starting from `npx skills init`.

## Output Shape

For discovery-only requests, end with a concise recommendation and the evidence
behind it. For installation requests, include what was installed, where it was
installed if the CLI reports a path, and how you verified it.
