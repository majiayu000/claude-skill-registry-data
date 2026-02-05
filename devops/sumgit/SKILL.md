---
name: sumgit
description: |
  Summarize today's git commits as a narrative story with parallel agent analysis.
  Invoked with /sumgit. Deploys Explore agents to analyze workstreams and tell
  the story of your day's work.
allowed-tools: Bash(git:*), Task, Read, Grep, Glob
---

# sumgit - Daily Git Story

Tell the story of today's git commits by deploying parallel Explore agents to
analyze different workstreams and synthesize a narrative summary.

## Execution Steps

### Step 1: Gather Today's Commits

Run these git commands to understand today's work:

```bash
# Get commit count
git log --since="midnight" --oneline | wc -l

# Get detailed commit info with files
git log --since="midnight" --format="%H|%s|%an|%ai" --name-only

# Get statistics
git log --since="midnight" --stat --oneline
```

Count total commits. If zero commits today, show a friendly message:
"No commits today yet! Last commit was on [date]. Time to ship some code!"

If only 1-2 commits, provide a simple summary without deploying agents.

### Step 2: Identify Workstreams

Analyze commits to identify 2-4 distinct workstreams by:

1. **File path patterns**: Group files by directory structure
   - `src/components/` -> UI Components
   - `src/api/` or `api/` -> API/Backend
   - `tests/` or `*.test.*` -> Testing
   - `docs/` or `*.md` -> Documentation
   - `src/auth/` or `*auth*` -> Authentication
   - `styles/` or `*.css` -> Styling

2. **Commit message themes**: Look for prefixes and keywords
   - `fix:`, `bug`, `patch` -> Bug Fixes
   - `feat:`, `add`, `new` -> New Features
   - `refactor:`, `clean` -> Refactoring
   - `docs:`, `readme` -> Documentation
   - `test:`, `spec` -> Testing
   - `style:`, `ui`, `css` -> UI/Styling

3. **Related functionality**: Group commits that touch similar areas

Name each workstream with a descriptive title and assign an emoji:
- New Features
- Bug Fixes
- UI/Styling
- Authentication/Security
- API/Backend
- Testing
- Documentation
- Refactoring
- Infrastructure/DevOps

### Step 3: Deploy Parallel Explore Agents

Launch up to 3 Explore agents simultaneously using the Task tool with
subagent_type="Explore". Each agent analyzes one workstream.

**Agent prompt template**:
```
Analyze the [WORKSTREAM] changes in this repository from today's commits.

Files changed in this workstream:
[LIST OF FILES]

Commits in this workstream:
[COMMIT MESSAGES]

Please:
1. Read the key files that were modified
2. Understand what changed and why
3. Identify patterns, decisions, and impact
4. Note any new components, bug fixes, or improvements
5. Summarize in 2-3 bullet points with technical specifics

Focus on the "what" and "why" of changes, not line-by-line diffs.
```

Deploy agents in a SINGLE message with multiple Task tool calls to run them
in parallel. Wait for all agents to complete.

### Step 4: Synthesize Narrative

Combine agent findings into a cohesive story using this structure:

```markdown
# The Complete Day: [Month Day, Year]

[N] Commits Across [M] Major Workstreams

---

## [Workstream Emoji] Workstream 1: [Title]

[N commits description of this area]

### [Subheading if needed]
- Specific change with technical detail
- Another change with context
- Impact or improvement noted

---

## [Workstream Emoji] Workstream 2: [Title]

[Continue pattern...]

---

## Day Summary

| Metric           | Value                    |
|------------------|--------------------------|
| Total commits    | N                        |
| Files modified   | N+                       |
| New components   | N (list if applicable)   |
| Bugs squashed    | N                        |

## Themes of the Day

1. **[Theme Name]**: [One-sentence description]
2. **[Theme Name]**: [One-sentence description]
3. **[Theme Name]**: [One-sentence description]

[Celebratory closing line acknowledging the work done]
```

## Output Guidelines

- **Tone**: Conversational and celebratory, like a team standup recap
- **Technical accuracy**: Include specific file names, component names, function names
- **Structure**: Use consistent formatting with clear workstream separation
- **Metrics**: Always include the summary table for quick scanning
- **Themes**: Identify 2-4 high-level patterns (e.g., "Simplification", "Robustness")
- **Closing**: End with an encouraging note (e.g., "A productive day!")

## Edge Cases

### No commits today
```
No commits yet today!

Last commit was [X hours/days] ago: "[commit message]"

Time to write some code!
```

### Single commit
Provide a simple summary without deploying agents:
```
# Today: [Date]

1 commit today:

## [Commit message]
[Brief description of what changed]

Files: [list]
```

### Many commits (20+)
Group at a higher level, focusing on major themes rather than individual changes.
Limit to 4 workstreams maximum to keep the narrative digestible.

## Example Output

See [examples/sample-output.md](examples/sample-output.md) for a complete example.
