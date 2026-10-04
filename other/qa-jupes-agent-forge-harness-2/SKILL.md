---
name: qa
description: Run a conversational QA session where the user reports bugs or issues, and file durable Beads issues using project domain language. Use when the user wants to report bugs, do QA, file issues conversationally, or mentions a QA session.
---

# QA Session
Run an interactive QA session. The user describes one problem at a time; you clarify only what is needed, explore enough context to use the project's language, and file durable Beads issues from the user's perspective.

Do not diagnose or implement fixes during the QA session. The goal is high-quality issue capture.

## For each issue the user raises

### 1. Listen and lightly clarify
Let the user describe the problem in their own words. Ask at most 2-3 short clarifying questions focused on:
- What they expected versus what actually happened
- Steps to reproduce, if they are not clear enough to file
- Whether the problem is consistent or intermittent
- Impact, urgency, or workaround signals needed for priority

Do not over-interview. If the description is clear enough to file a durable issue, move on.

### 2. Explore context in the background
While keeping the conversation moving, gather lightweight context so the issue uses the right domain language:
- Read relevant `knowledge/` files first, especially `knowledge/_shared.yaml` and any applicable `knowledge/repos/<repo>.yaml`.
- If the affected area is unclear or the domain language is unfamiliar, run background exploration for the relevant repo or feature area.
- Look for user-facing behavior boundaries: what the feature is supposed to do, which actor sees the failure, and which workflow is interrupted.

This exploration is not a fix investigation. Use it to improve issue wording, not to cite internal implementation details.

### 3. Decide: single issue or breakdown
Before filing, decide whether the report is one issue or should become multiple Beads issues.

Break down when:
- The report spans multiple independent user-facing areas.
- Several symptoms can be fixed and verified independently.
- Different agents or people could work on separate slices in parallel.
- One slice blocks another and dependency order matters.

Keep as a single issue when:
- One behavior is wrong in one place.
- The symptoms describe the same user-facing failure.
- Splitting would create thin issues that cannot be independently verified.

### 4. Select priority
Before every `bd create`, use `.claude/skills/beads-priority-assignment/SKILL.md` to choose an explicit priority.
- Honor user-provided urgency such as "P0", "urgent", or "critical".
- Use impact, urgency, risk if deferred, and workaround availability to choose the tier.
- If there is no signal after applying the rubric, use the harness default: `P2` / `2` / `medium`.
- Do not leave priority unset when the Beads CLI supports `--priority`.

### 5. File the Beads issue(s)
Create issues with `bd create`. Do not default to GitHub issue commands or file anywhere else first. Once the report has enough detail to be durable, file it without a separate review gate and share the Beads ID(s).

Issues must be durable: they should still make sense after major refactors. Write from the user's perspective and focus on behavior over implementation.

#### Single issue template
Use this body:

```markdown
## What happened
[Describe the actual behavior the user experienced, in plain language.]

## What I expected
[Describe the expected behavior.]

## Steps to reproduce
1. [Concrete step a developer or agent can follow.]
2. [Use project domain terms, not internal module names.]
3. [Include relevant inputs, configuration, flags, or state.]

## Impact and frequency
[Who is affected, how often it happens, and any workaround.]

## Additional context
[Helpful observations from the user or context exploration. Use domain language, but do not cite files, line numbers, internal function names, or stack frames as the primary evidence.]
```

Command shape:

```bash
bd create --type bug --title "<user-facing issue title>" --description "<template markdown>" --priority <value> --repo <repo-or-.>
```

#### Breakdown template
Create issues in dependency order, blockers first, so real Beads IDs can be referenced. Use this body for each sub-issue:

```markdown
## Parent report
[Parent Bead ID if a tracking issue was created, or "Reported during QA session".]

## What's wrong
[Describe this specific behavior problem only.]

## What I expected
[Expected behavior for this specific slice.]

## Steps to reproduce
1. [Steps specific to this issue.]

## Blocked by
- None - can start immediately
or
- <bead-id>

## Impact and frequency
[Who is affected, how often it happens, and any workaround.]

## Additional context
[Relevant observations for this slice, stated in user-facing domain language.]
```

When creating a breakdown:
- Prefer many thin, independently verifiable issues over a few thick ones.
- Create blockers before blocked work.
- Add Beads dependencies after the relevant IDs exist:

```bash
bd dep add <blocker-id> --blocks <blocked-id>
```

- Mark independent slices as `None - can start immediately`.
- Maximize parallelism without splitting apart behavior that must be fixed together.

#### Rules for all issue bodies
- Reproduction steps are mandatory. If you cannot determine them, ask the user.
- Do not use file paths, line numbers, or internal function names as primary evidence.
- Describe behaviors, not code.
- Use the project's domain language from `knowledge/` and lightweight exploration.
- Keep each issue concise enough to read in about 30 seconds.
- Include priority on every issue.

After filing, share the Beads IDs, summarize any blocking relationships, and ask: "Next issue, or are we done?"

### 6. Continue the session
Keep going until the user says they are done. Treat each reported issue independently and avoid batching multiple user reports into one filing step unless the breakdown decision explicitly calls for it.
