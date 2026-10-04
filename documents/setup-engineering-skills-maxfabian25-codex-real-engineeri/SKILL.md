---
name: setup-engineering-skills
description: Configure AGENTS.md and docs/agents. Use when this engineering skill pack lacks repo setup.
---

# Setup Engineering Skills

Scaffold the per-repo context that the engineering skills assume:

- **Issue tracker** - where issues live, such as GitHub, GitLab, local markdown, or another documented workflow.
- **Triage labels** - the concrete strings used for the five canonical triage states.
- **Domain docs** - where `CONTEXT.md`, `CONTEXT-MAP.md`, and ADRs live.

This is prompt-driven setup. Explore first, present what you found, confirm with the user, then write. Do not overwrite unrelated AGENTS.md content.

## Codex Interaction

Use `request_user_input` for each setup decision when the tool is available and the choices fit two or three options. Put the recommended option first. If the tool is unavailable, ask one concise plain-text question and wait.

## Process

### 1. Explore

Read the current repo state instead of assuming:

- `git remote -v` and `.git/config` - identify GitHub, GitLab, or another remote.
- Root `AGENTS.md` - check whether an `## Agent skills` section already exists.
- Root `CONTEXT.md` and `CONTEXT-MAP.md`.
- `docs/adr/` and any context-specific ADR directories.
- `docs/agents/` - detect prior setup output.
- `.scratch/` - detect an existing local-markdown issue convention.

### 2. Present findings and ask

Summarize what is present and missing. Then walk through these decisions one at a time:

1. **Issue tracker.** Recommend GitHub when the remote points to GitHub, GitLab when the remote points to GitLab, otherwise local markdown. If the user chooses another tracker, ask them for one paragraph describing the workflow.
2. **Triage label vocabulary.** Confirm the five role strings: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. Use defaults unless the project already has different labels or the user overrides them.
3. **Domain docs.** Confirm single-context (`CONTEXT.md` plus `docs/adr/`) or multi-context (`CONTEXT-MAP.md` pointing at multiple context docs).

### 3. Confirm and edit

Show the user a draft of:

- the `## Agent skills` block for `AGENTS.md`;
- `docs/agents/issue-tracker.md`;
- `docs/agents/triage-labels.md`;
- `docs/agents/domain.md`.

Wait for approval before writing unless the user has already explicitly approved those exact choices.

### 4. Write

Edit root `AGENTS.md`. If it does not exist, ask before creating it. If `## Agent skills` already exists, replace only that section.

Use this block shape:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout]. See `docs/agents/domain.md`.
```

Then write the `docs/agents/` files using these templates from this skill folder:

- [issue-tracker-github.md](./issue-tracker-github.md)
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)
- [issue-tracker-local.md](./issue-tracker-local.md)
- [triage-labels.md](./triage-labels.md)
- [domain.md](./domain.md)

For other trackers, write `docs/agents/issue-tracker.md` as concise prose from the user's description.

### 5. Finish

Tell the user which files changed and which skills now read from them. Mention that rerunning this setup is only needed when issue tracker, labels, or domain-doc layout changes.
