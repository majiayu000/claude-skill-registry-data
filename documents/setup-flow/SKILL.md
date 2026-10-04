---
name: "setup-flow"
description: "Configure a repo for these skills: issue tracker, triage label vocabulary, domain doc layout, and optionally per-role model choices. Run once per repo before first use of to-tickets, to-spec, triage, or wayfinder. Use for /setup-flow or configure my skills for this repo."
disable-model-invocation: true
---

# Setup flow

Scaffold the per-repo configuration the other skills assume:

- **Issue tracker**: where issues live. `to-tickets`, `to-spec`, `triage`, and `wayfinder` all read and write through it.
- **Triage labels**: the strings behind the five canonical triage roles.
- **Domain docs**: where `CONTEXT.md` and ADRs live, and the rules for reading them.
- **Models** (optional): per-role overrides for the delegating skills.

Prompt-driven, not a script. Explore, present what you found, confirm, then
write. Run it again any time to change an answer.

## 1. Explore

Read what exists. Do not assume.

- `git remote -v` and `.git/config`. GitHub? GitLab? Which repo?
- `CLAUDE.md` and `AGENTS.md` at the root. Does either have an `## Agent skills` section?
- `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, `src/*/docs/adr/`
- `docs/agents/`: has this skill already run here?
- `.scratch/`: a local-markdown tracker convention already in use
- Is the `triage` skill installed? This decides whether Section B runs at all.
- Monorepo signals: `pnpm-workspace.yaml`, a `workspaces` field, a populated `packages/*` with its own `src/`. Absence means single-context, which is almost every repo.

**Check the tracker CLI is real before proposing it.** A `gh` on `PATH` is not
necessarily the GitHub CLI, and an unrelated script of the same name is a
common shadow:

```bash
gh --version 2>&1 | grep -q 'github\.com/cli/cli' && echo "real gh" || echo "NOT the GitHub CLI"
gh auth status 2>&1 | head -3   # want an authenticated account
```

Match on the `github.com/cli/cli` release URL, not on the words "gh version".
A shadowing script can print `gh version: v0.0.4` and pass a looser check.

Same for `glab`. If the CLI is missing, shadowed, or unauthenticated, say so
plainly and propose local markdown instead. Configuring a tracker the repo
cannot reach produces skills that fail on first use.

## 2. Present findings and ask

Summarise what is present and what is missing. Then take the sections in order,
one section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a
word. Give a one-line explainer only when the choice genuinely branches, and
skip a section entirely when exploration already settled it. Prefer
`AskUserQuestion` over free text.

**Section A: Issue tracker.**

> The issue tracker is where issues live for this repo. Skills need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow a workflow you describe.

Propose by remote, subject to the CLI check above:

- **GitHub**: GitHub Issues, via the `gh` CLI
- **GitLab**: GitLab Issues, via the `glab` CLI
- **Local markdown**: files under `.scratch/<feature>/`. Good for solo projects, repos without a remote, and any repo where the CLI check failed
- **Other** (Jira, Linear): ask for a one-paragraph description of the workflow, recorded as freeform prose

The GitHub and GitLab templates carry a "PRs as a request surface" flag,
defaulted off. Leave it off and do not raise it.

**Section B: Triage label vocabulary.** Skip entirely if `triage` is not
installed. Otherwise ask one question:

> Keep the default triage labels? (recommended: yes)

Defaults are the five canonical roles, each label equal to its name:
`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`.
Only if the user says no, usually because their tracker already uses other
names, collect the overrides so `triage` applies existing labels instead of
creating duplicates.

**Section C: Domain docs.** Default to **single-context** (one `CONTEXT.md`
plus `docs/adr/` at the root) and write it without asking. Offer
**multi-context** (a root `CONTEXT-MAP.md` pointing at per-context files) only
when exploration found monorepo signals.

**Section D: Models.** Optional, and worth skipping unless the user asks.

The delegating skills (`how`, `why`, `arena`, `swarm`, `architect`, `review`,
`reflect`) carry inline defaults of `opus`, `fable`, and `sonnet`. Those are
the only families available, so the pool is small and the defaults are usually
right.

Offer this section only when the user wants to change it. If they do, write
`docs/agents/models.md` with one line per role, and say plainly that the
skills fall back to their inline defaults for any role not listed.

Be honest about the ceiling while discussing it: every subagent is a Claude
model, so "a second opinion from a different model" is real but narrower than
a cross-vendor panel would be.

## 3. Confirm and edit

Show a draft of the `## Agent skills` block and the contents of
`docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and
`docs/agents/triage-labels.md` (the last only when `triage` is installed). Let
the user edit before writing.

## 4. Write

**Pick the file to edit.** If `CLAUDE.md` exists, edit it. Else if `AGENTS.md`
exists, edit it. If neither exists, ask which to create; do not pick for them.
Never create one when the other already exists.

If an `## Agent skills` block is already there, update it in place rather than
appending a duplicate. Do not touch surrounding sections.

```markdown
## Agent skills

### Issue tracker

[one-line summary]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary]. See `docs/agents/triage-labels.md`.

### Domain docs

[single-context or multi-context]. See `docs/agents/domain.md`.
```

Include the triage sub-block, and write `docs/agents/triage-labels.md`, only
when Section B ran.

Seed the docs files from the templates in this folder:

- [issue-tracker-github.md](./issue-tracker-github.md)
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md)
- [issue-tracker-local.md](./issue-tracker-local.md)
- [triage-labels.md](./triage-labels.md)
- [domain.md](./domain.md)

For "other" trackers, write `docs/agents/issue-tracker.md` from scratch from
the user's description.

## 5. Offer a verification skill

Check whether the project can already drive the real app for proof: a
`verify-*` skill, or an existing harness. If not, offer once:

> Want a project-local verification skill, so agents can drive the app the way a user does and prove changes work?

On yes, call the **verify** skill in generate mode. On no, move on without
pushing.

## 6. Done

Say what was written and which skills now read it. Mention they can edit
`docs/agents/*.md` directly; re-running this skill is only needed to switch
trackers or start over.
