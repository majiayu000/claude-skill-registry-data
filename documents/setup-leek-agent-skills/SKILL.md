---
name: setup
description: "Configure this repo for the engineering skills: the markdown tracker layout, triage status vocabulary, and domain doc layout."
disable-model-invocation: true
---

# Setup

Scaffold the per-repo configuration that the engineering skills assume:

- **Markdown tracker**: where maps, specs, and tickets live as files under `.scratch/`
- **Triage status**: the `status:` frontmatter strings used for the five canonical triage roles
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Read whatever exists; don't assume:

- `AGENTS.md` / `CLAUDE.md` at the repo root: does an `## Agent skills` section already exist?
- `GLOSSARY.md` at the repo root (or the old `CONTEXT.md` / `CONTEXT-MAP.md`), `docs/adr/`
- `.agents/`: does this skill's prior output already exist (`domain.md`, `issue-tracker.md`, `triage-labels.md`)? These sit next to `.agents/skills/`; they are not skills.
- `docs/agents/`: leftover from an older setup. If those files exist and `.agents/` does not, move them.
- `.scratch/`: is the convention already in use, and at which levels?
- Is the `triage` skill installed? This decides whether Section B runs at all.

### 2. Present findings and ask

Summarise what's present and missing, then take the sections in order; one section, one answer. Lead each with the recommended answer so the user can accept it in a word. Use `AskUserQuestion` where available; otherwise ask in chat and wait.

**Section A: Issue tracker.** Markdown files under `.scratch/` are the only tracker these skills use: it needs no auth and keeps every map, spec, and ticket greppable next to the code. There is no choice to make here, so ask nothing: write `.agents/issue-tracker.md` from this skill's `issue-tracker.md` seed. Ask one question only if the repo already keeps this work somewhere other than `.scratch/`, and then only to confirm that path.

**Section B: Triage status vocabulary.** Skip entirely if the `triage` skill isn't installed. If it is, ask exactly one question: keep the default status strings? (recommended: **yes**). Defaults: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. Collect overrides only on "no".

**Section C (Domain docs.** Default to **single-context**) one `GLOSSARY.md` + `docs/adr/` at the repo root. Write it without asking. Offer multi-context (a root `GLOSSARY-MAP.md` pointing at per-module `GLOSSARY.md` files) only when exploration found real module boundaries (`app-modules/`, `modules/`, a monorepo layout). Found the old names? Include renaming them in the draft: `git mv` each `CONTEXT.md` to `GLOSSARY.md` and `CONTEXT-MAP.md` to `GLOSSARY-MAP.md`, then fix the map's links.

### 3. Confirm and write

Show a draft of the `## Agent skills` block and each `.agents/*.md` file; let the user edit before writing. If `docs/agents/` still holds a prior copy, move those files into `.agents/` instead of writing a second set.

Edit `CLAUDE.md` if it exists, else `AGENTS.md`; if neither exists, ask which to create. If an `## Agent skills` block already exists, update it in place, never append a duplicate.

```markdown
## Agent skills

### Issue tracker

[one-line summary]. See `.agents/issue-tracker.md`.

### Triage status

[one-line summary]. See `.agents/triage-labels.md`.

### Domain docs

[one-line summary: "single-context" or "multi-context"]. See `.agents/domain.md`.
```

Omit the `### Triage status` sub-block (and its file) when Section B didn't run.

Seed templates in this folder:

- [issue-tracker.md](./issue-tracker.md): the markdown layout for maps, specs, and tickets
- [triage-labels.md](./triage-labels.md): status role mapping (only if `triage` is installed)
- [domain.md](./domain.md), domain doc consumer rules + layout

### 4. Done

Tell the user setup is complete and which skills now read these files (`wayfinder`, `to-spec`, `to-tickets`, `implement`, `code-review`, `triage`). They can edit `.agents/*.md` directly later: re-running this skill is only needed to restart.
