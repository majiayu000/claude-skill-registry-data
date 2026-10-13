---
name: dev-linkify-cc-resources
description: "Link Claude Code skill names mentioned in a CodeGrid article (data/{series}/{n}.md) to the author's public claude-resources repo, pinned to the latest commit hash so links don't rot. Use when: (1) user says 'linkify cc resources', 'link the skills', 'link skill names', or invokes /dev-linkify-cc-resources; (2) editing a CodeGrid article that mentions `/commits`, `/pr-complete`, `/skill-creator` or other Claude Code skills and they should point to claude-resources. Only links skills that actually exist in the public repo; skips hypothetical examples and code blocks."
---

# Linkify CodeGrid skill mentions

CodeGrid articles in the AI-agents series mention Claude Code skills by name (`/commits`,
`/pr-complete`, …). This skill turns the first prose mention of each **published** skill
into a link to the author's public collection, [claude-resources](https://github.com/Takazudo/claude-resources),
pinned to the latest commit hash.

Pinning to a hash (not `main`) is deliberate: the repo changes often, and a hash-based ref
keeps the article's link pointing at the version that existed at writing time. The repo is
introduced once in an earlier article (a `[column]` titled 「筆者のスキルコレクション」 in
`9.md`), so later articles just inline-link — no need to re-introduce the repo.

## Workflow

### Step 1 — Identify the target article

Use the article the user is editing (from conversation context) or the path they pass. It's a
file like `data/{series-slug}/{n}.md` in the CodeGrid articles repo.

### Step 2 — Run the scan

```bash
python3 $HOME/.claude/skills/dev-linkify-cc-resources/scripts/scan.py <article.md>
```

The script resolves the claude-resources repo (`$HOME/repos/*/claude-resources`), fetches and
reads the latest `origin/main` hash, lists the published skills, and reports a `LINK THESE`
block: the first prose mention of each skill that exists in the repo, with the ready-to-paste
markdown. It already excludes mentions inside code blocks, mentions already linked, and names
that aren't real published skills.

Pass `--repo <path>` if the repo lives somewhere other than `$HOME/repos/*/claude-resources`.

### Step 3 — Apply the links

For each entry in `LINK THESE`, wrap the inline-code skill name in the suggested link, leaving
the surrounding prose untouched:

```text
…9回目の連載で紹介した`/commits`という…
→ …9回目の連載で紹介した[`/commits`](https://github.com/Takazudo/claude-resources/blob/<hash>/skills/commits/)という…
```

Edit the live article, not the scan output. After editing, the URL format is
`https://github.com/Takazudo/claude-resources/blob/<hash>/skills/<name>/` — keep `/blob/` and
the trailing slash (GitHub redirects directory `/blob/` to `/tree/`).

## What gets linked, and what doesn't

The scan's repo membership check enforces the editorial rule automatically:

- **Linked**: skills present in `claude-resources/skills/`, at their first prose mention.
- **Not linked**: names that are hypothetical examples in the prose (e.g. `/fix-typo`,

  `/brighten-photo`) or personal skills the author hasn't published (e.g. `/price-research`) —
  these simply aren't in the repo, so the scan won't surface them.

- **Skipped**: mentions inside fenced code blocks, and any skill already linked elsewhere in

  the article (only the first prose mention is linked, for readability).

If the user disagrees with a specific call (e.g. wants a second mention linked too, or wants to
skip re-linking a skill already linked in an earlier article), follow their preference — the
scan is a starting point, not a hard rule.
