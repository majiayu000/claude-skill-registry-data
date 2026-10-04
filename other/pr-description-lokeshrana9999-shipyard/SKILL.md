---
name: pr-description
description: Writes the PR description ("write the PR description", "draft the PR", "open a PR for this branch") as a pull request title and body from the branch's diff and history, shows the full draft for approval, then creates or updates the pull request on the project's code host and links any extended context. Use when a branch is ready to open or update a pull request or merge request, or when asked to write, draft, or publish a PR description.
disable-model-invocation: true
---

# PR description

Turn a branch into a pull request a reviewer can understand in under a minute: why it exists, what the diff can't show, what could break, and what feedback is wanted. Nothing reaches the code host until the user has seen everything that will be published.

## Inputs

- The branch's diff and commit history against its base branch.
- QA or test evidence, if a verification step produced any: scenario results, screenshots, commands and their output.
- **Project settings**: on every invocation, read `.claude/shipyard/pr-description.md` in the project root if it exists; its settings win over the defaults below. It can set the code host and how to publish to it, the base branch, the description length limit, title and tag conventions, and an extended-context destination (such as a wiki page) with its layout. Its shape is in [references/overlay-example.md](references/overlay-example.md).

## Output

A pull request created or updated on the code host, with its title and description, plus the extended-context page when the settings configure one. If publishing isn't possible, the title and description printed for the user to paste.

## Rules

- **One approval gate, before the first live write.** Everything that will be published is generated first and shown together, so one approval covers the whole batch. Nothing touches the code host before it.
- **Ground every claim in the diff.** Every change bullet and every risk names a real changed file. Generated descriptions of code changes often state things the diff doesn't contain, so check each claim against the diff, not just the wording.
- **The repo's template wins.** If the repo has a pull request template, fill its headings with this skill's content and keep its checklists and issue-linking lines. Creating a PR through a CLI or API usually skips the template, so apply it yourself. Write "N/A" in a template section that doesn't apply rather than padding it.
- **Testing comes only from real evidence.** Fill the testing section from actual results. Without any, leave a clear placeholder for the author, never a guess.
- **Degrade, don't abort.** If an extended-context publish fails, finish the pull request without it and say what's missing.
- **Match the repo's conventions** for the title prefix (for example conventional-commit types), tags, and emoji. The defaults are plain words and no emoji.

## Steps

```
- [ ] 1 Read the change
- [ ] 2 Draft title and description
- [ ] 3 Draw the reviewer diagram
- [ ] 4 Check the draft
- [ ] 5 Gate: show everything
- [ ] 6 Create or update the pull request
- [ ] 7 Publish extended context and link it
- [ ] 8 Report
```

**Plan (local, no side effects)**

1. **Read the change.** Find the base branch (settings, else the remote's default branch). Read the file list, the commit log, and the full diff against it. If nothing is ahead of the base, stop and say so. Find the code host from the git remote and look for a pull request template (for example under `.github/`, `.gitlab/`, or `docs/`). Check whether a pull request already exists for this branch, read-only; if one does, the publish step updates it.
2. **Draft the title and description** per [references/body-template.md](references/body-template.md): commits mapped to bullets (not one-to-one), impact areas and risks, unrelated changes, the review focus, and the testing section.
3. **Draw the reviewer diagram** when the change alters behavior across components or adds branching logic, using the flow-diagram skill for syntax and style. It answers the reviewer's question, what this change does to the system's behavior, not what the architecture is. See the diagram section of the body template.
4. **Check the draft.** Every change and risk bullet cites a file in the diff; drop any that don't. The description fits the host's length limit, measured the way the host counts. For a large change (default: more than 10 files, or more than 3 risk bullets), have a fresh subagent with only the diff and the draft flag anything the diff doesn't support, and fold its findings in.

**Gate**

5. `STOP — WAIT`. Show the user, together: the title; the full description; whether step 6 **creates** a pull request or **updates** an existing one; the extended-context plan, if any; each diagram. Add a size note when the change is large (default: more than about 400 changed lines or 10 files) or has unrelated changes: large pull requests get slower, less thorough review, so suggest splitting, without blocking. Wait for explicit approval, then run steps 6 to 8 as one batch.

**Publish (after approval)**

6. **Create or update the pull request** with the host's CLI, API, or a connected tool, as the settings say or as available. Offer a draft pull request if the user asked for one. If creating fails (branch not pushed, no access, no tool), stop publishing, print the title and description for manual use, and say why.
7. **Publish extended context**, only if the settings configure a destination. Hand it to a subagent with a self-contained brief, per [references/extended-context.md](references/extended-context.md), since it's tool-heavy and fails independently of the pull request. Then update the description with a one-sentence summary and link for each page, and the testing tally if QA evidence was published. Re-check the length limit before this update.
8. **Report**: the pull request link and title, each extended-context link or why it failed, and the final description length against the limit.

## Handoff

`next:` the pull request's human reviewers, with its link; the demo stage when the change is user-facing and the project has one.
