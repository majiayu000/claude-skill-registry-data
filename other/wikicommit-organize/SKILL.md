---
name: wikicommit-organize
description: Propose groups for the pages of one wiki Type — "practices", "phenomena" and so on — and, once a person approves, record them in .wikicommit/groups/ and open a pull request that is not auto-merged. The pages themselves are never rewritten, so grouping sends no page back for review. Use this only when someone explicitly asks to organize, group or sort the pages of a Type, or to deal with the unclassified pages wikicommit-status reports. It writes a file and opens a PR, so do not use it to list or browse a Type's pages — wikicommit-search and wikicommit-status do that without writing.
disable-model-invocation: true
---

# wikicommit-organize

> **Paths in this file.** `references/…`, `scripts/…` and `../<other-skill>/…` are relative to this Skill's directory — the one holding this `SKILL.md`, which the runtime names when it loads the Skill — not to the repository root, because the Skills may be installed under `.claude/skills/` or `.agents/skills/`. Commands still run from the repository root, so spell the path out from there. Paths starting with `.wikicommit/` are repository-root paths as before.

A large Type is one long list: its `index.md` and the published site's left pane show every page of it in a single column. This Skill sorts one Type's pages into named groups. **The grouping lives in `.wikicommit/groups/<Type>.yml`, outside every page** — grouping is how pages are listed, not what they say, and writing it into a page would count as a content change and send every `reviewed` page it touched back to `pending`.

The AI proposes; a person decides; the decision reaches the default branch only through a pull request a person merges.

## Usage

```
/wikicommit-organize <Type>
```

`<Type>` is the Type as it appears in a WikiLink (`DefinedTerm`, `Place`, `custom/Decision`).

## The group file

```yaml
groups:
  practice:
    label: {ja: 実践・手法, en: Practices}
    criterion: "Describes something the reader does"
    pages: [vibe-coding, spec-driven-development]
  phenomenon:
    label: {en: Phenomena}
    criterion: "Names something that happens to a system or its users"
    pages: [context-rot]
unclassified_label: {it: Non classificati}   # optional; ja and en have a built-in heading
```

- **Keys** are lowercase letters, digits and hyphens. They are what the published site groups by; the `label` is what a reader sees, one per language. A language with no label shows the key.
- **`pages` are slugs** — the file name without `.md`, the same in every language — so one file groups every language's copy of a page.
- **A page is in one group at most.** A page no group names is shown under the unclassified heading.
- **`criterion`** is one sentence on what belongs in the group. It is what the next run of this Skill reads to place new pages the same way, so write it as a test a page passes or fails, not as a title.

## Processing Flow

### Step 0: Check the wiki

Stop with a message if `.wikicommit/config.yml` is missing (this is not a WikiCommit wiki) or if `.wikicommit/scripts/check_groups.py` is missing (the wiki's scripts predate this Skill; `/wikicommit-update` brings them in).

Stop, too, if anything under `.wikicommit/entity/` or `.wikicommit/groups/` is uncommitted:

```bash
git status --porcelain -- .wikicommit/entity .wikicommit/groups
```

This Skill rebuilds the Type's `index.md` from the pages on disk and commits it. Pages another Skill left uncommitted would be listed in that index without being in the pull request, so the index would link to pages the default branch does not have. Ask for `/wikicommit-merge` first.

**A non-interactive run decides nothing.** Every group and every placement rests on a person's answer, so when no one can answer, show the proposal (Step 3) and stop without writing.

Resolve the default branch:

```bash
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
```

Record it as `<default branch>`. If this fails, fall back to `main` and warn that Step 5's branch and pull request will fail if the real default branch differs.

### Step 1: See where the Type stands

```bash
python .wikicommit/scripts/check_groups.py --limit 30 --type "$(cat <<'EOF'
<Type>
EOF
)"
```

- `ERROR:` lines — the group file is invalid. Show them and stop; the file is a person's, and it is theirs to fix.
- `GROUP:` lines — the groups already decided, with their `criterion`.
- `STALE_MEMBER:` lines — slugs the file names that no longer have a page (deleted or renamed). Propose dropping each in Step 3.
- `UNCLASSIFIED:` lines — the pages to place, at most 30 per run. `TRUNCATED:` says how many more remain; tell the person, and that running this Skill again picks up the next batch. Thirty is what a person can still read as one list and check placement by placement.

If there are no unclassified pages and no stale members, say the Type is fully grouped and stop.

### Step 2: Read the pages — the reduced view, not the bodies

```bash
python .wikicommit/scripts/build_survey_view.py --pages <every path from the UNCLASSIFIED: lines>
```

Each page comes back as its title, `properties.description`, `##` headings and tags. **Do not read the page bodies.** What a page is about is all a placement needs, and thirty bodies do not fit in one context.

### Step 3: Propose

- **The group file exists**: place each unclassified page in the existing group whose `criterion` it passes. A page that passes none stays unclassified — say so rather than stretching a criterion. If several such pages share something no existing group covers, you may propose one new group (key, labels, criterion) for them, marked as new.
- **No group file**: propose the groups themselves — between two and seven, each with a key, a label in `translation.primary_lang` (and in each language of `translation.targets` if you can write it), a one-sentence criterion, and its pages. Groups should be about what the pages *are* (a phenomenon, a practice, a mechanism), so that a page generated later can be placed by reading the criterion. Do not group by source, by date or by how much a page says.

Show the proposal as a table — page title, slug, proposed group, and for each new group its criterion — plus the stale members to drop. Ask the person to approve, change placements, rename or merge groups, or leave pages unclassified. Change the proposal as they say and show it again until they approve.

### Step 4: Write

Write `.wikicommit/groups/<Type>.yml` (a custom type keeps its `custom/` segment: `.wikicommit/groups/custom/Decision.yml`) with the approved content: existing groups kept in their order with any new pages appended, new groups after them, approved stale members removed. Keep comments a person wrote in the file. Change nothing else in the file.

Validate it, and rebuild the Type's index in every language:

```bash
python .wikicommit/scripts/check_groups.py --type "$(cat <<'EOF'
<Type>
EOF
)"
python .wikicommit/scripts/rebuild_index.py .wikicommit/entity/<lang>/<Type> [...]
```

Fix the file if `check_groups.py` prints any `ERROR:`. Pass `rebuild_index.py` every `.wikicommit/entity/<lang>/<Type>` directory that exists. No page under `.wikicommit/entity/` changes — only each `index.md`.

### Step 5: Branch, commit, PR (no auto-merge)

```bash
git checkout "<default branch>"
git checkout -B wikicommit/organize-<TypeSlug>
git add .wikicommit/groups/<Type>.yml .wikicommit/entity/<lang>/<Type>/index.md [...]
git commit -m "$(cat <<'EOF'
groups: organize <Type> into <N> groups

<Co-Authored-By line>
Generated-By:   <current model ID>
EOF
)"
git push origin wikicommit/organize-<TypeSlug>
gh pr create \
  --title "$(cat <<'EOF'
groups: organize <Type>
EOF
)" \
  --body "<PR Description Template below>" \
  --base "<default branch>"
git checkout "<default branch>"
```

`<TypeSlug>` is `<Type>` with `/` replaced by `-`. The uncommitted group file and indexes come along to the new branch; Step 0 made sure nothing else under `.wikicommit/entity/` was uncommitted, so they are the only changes it carries. Never pass `--auto` and never run `gh pr merge`: whether a grouping fits is the reviewer's call.

<!-- commit-trailers:start (this block is identical in wikicommit-merge, -schema-propose, -update, -init and -organize; tests/test_commit_trailer_vendor_table.py holds them together) -->
**Commit trailers.** Always write `Generated-By:   <current model ID>`: the ID of the model actually running this Skill, exactly as the runtime reports it — the same self-reported value `wikicommit-generate` writes into a page's `generated_by` (keep any suffix; do not shorten or normalize it; never hardcode one). Then choose `<Co-Authored-By line>` from the start of that same ID, so the two lines can never name different vendors:

| `<current model ID>` starts with | `<Co-Authored-By line>` |
|---|---|
| `claude-`, or `claude-` after a provider prefix ending in `anthropic.` (Bedrock, e.g. `us.anthropic.claude-…`) | `Co-Authored-By: <Claude display name> <noreply@anthropic.com>` — the model's human-readable name, or just `Claude` when it is not known with confidence |
| `gpt-` or `codex` | `Co-Authored-By: Codex <noreply@openai.com>` |
| anything else | **no `Co-Authored-By` line at all** — `Generated-By` already records the model |

GitHub resolves a co-author by the email address and shows that vendor's avatar on the commit, so a line naming a vendor that did not run this Skill misattributes it; writing none is the correct answer for a model not in the table. Decide by the model, not by the harness running it — one harness can run models from more than one vendor. If the harness appends its own co-author line after this message, leave it; an identical duplicate does no harm.
<!-- commit-trailers:end -->

If `git push` or `gh pr create` fails, report it and leave the branch in place for the person; the file and the indexes are already committed on it.

#### PR Description Template

<!-- skill-vocabulary-exception: PR body; its reader is the reviewer deciding whether the grouping fits -->
```markdown
## Grouping for `<Type>`

<N> group(s), <M> page(s) placed this run, <K> page(s) still unclassified.

| Group | Label | Criterion | Pages |
|---|---|---|---|
| <key> | <labels> | <criterion> | <slugs> |

Dropped from the file (no such page any more): <slugs, or "none">

## What changes

- `.wikicommit/groups/<Type>.yml` — the grouping
- `index.md` of `<Type>` in each language — now split under one heading per group

No page under `.wikicommit/entity/` is modified, so no page's review status changes.

## Checklist for review

- [ ] Each criterion is a test a page passes or fails
- [ ] Each page sits in the group whose criterion it passes
- [ ] Pages left unclassified really fit no group

🤖 Proposed by wikicommit-organize — merge only after checking the grouping itself.
```

### Step 6: Report

Say, in plain words: how many pages were placed, which groups were created, how many remain unclassified, and the pull request's link. Then:

- Once the pull request is merged, the Type's index and the published site's left pane show the groups. Page URLs do not change.
- Pages generated later are not placed automatically; they appear as unclassified, and `/wikicommit-status` counts them. Run this Skill again when they have built up.

## Notes

- **Writes `.wikicommit/groups/<Type>.yml` and the Type's `index.md` files, nothing else.** Never edits a page, never auto-merges.
- **`wikicommit-generate` never writes the group file.** A new page waits as unclassified for a person's next decision rather than being placed by a criterion read differently on each run.
- **The file is a person's.** It can be edited by hand at any time; this Skill keeps what is there and adds to it.
