---
name: skill-template
description: >-
  Bootstrap a new standalone skill repo under gaia-research/ from the canonical
  template set at gaia-research/gaia-research/templates/skill-repo/. Handles
  the full flow: interactive prompts for all placeholders, fetches templates via
  the GitHub API, substitutes values, creates the new repo
  (gaia-research/skill-<name>), writes README.md / SKILL.md / install.sh /
  .gitignore / LICENSE / powered-by-gaia.svg, makes the initial commit and
  pushes. Also supports update mode: re-applies the template structure to a
  pre-existing skill repo and opens a draft PR with the drift. Use when the
  user says "new skill repo", "bootstrap a skill repo", "/skill-template",
  "create skill-foo", "spin up a gaia-research skill repo", "template a new
  skill", "align skill-fuse to the template", or
  "/skill-template update <repo>".
  Requires: gh CLI (authenticated with gaia-research org access), python3, git.
version: 1.0.0
---

# skill-template

Bootstrap a new `gaia-research/skill-*` repo — or realign an existing one — from
the canonical template at
[`gaia-research/gaia-research/templates/skill-repo/`](https://github.com/gaia-research/gaia-research/tree/main/templates/skill-repo/).

## Modes

| Mode | Invocation | What it does |
|---|---|---|
| **create** | `/skill-template <name>` or `/skill-template` | New repo `gaia-research/skill-<name>`, initial commit, pushed to `main` |
| **update** | `/skill-template update <repo>` | Clones existing repo, re-renders templates, opens draft PR with drift only |

## Requirements

- `gh` CLI authenticated with a token that can create public repos under `gaia-research/`
- `git`
- `python3` (used for placeholder substitution — handles multi-line values and backticks safely)

## Create flow

### Step 1 — collect inputs

Prompt the user for each value. Skip any that were passed on the command line.

| Prompt | Variable | Example |
|---|---|---|
| Skill name (kebab-case, no `skill-` prefix) | `SKILL_NAME` | `ci-churn` |
| Display name (Title Case) | `SKILL_DISPLAY_NAME` | `CI Churn` |
| Tagline (one sentence — the pain point) | `SKILL_TAGLINE` | `Measure CI waste on avoidable pushes.` |
| Description (2–3 sentences) | `SKILL_DESCRIPTION` | `Classifies every commit…` |
| Invoke trigger | `INVOKE_TRIGGER` | `/ci-churn` |
| Requirements | `REQUIREMENTS` | `gh CLI (authenticated), Python 3.8+` |
| Files the installer fetches (space-separated) | `FILES_TO_FETCH_RAW` | `ci_churn.py SKILL.md` |
| Main script filename (or blank if none) | `SCRIPT_NAME` | `ci_churn.py` |
| Example output (paste terminal capture) | `EXAMPLE_OUTPUT_RAW` | actual output |

Derive automatically (do not prompt):
- `REPO_SLUG` = `skill-${SKILL_NAME}`
- `INSTALL_PATH` = `.agents/skills/${SKILL_NAME}`
- `YEAR` = `$(date +%Y)`
- `ORG` = `gaia-research`
- `FILES_TO_FETCH` = each token from `FILES_TO_FETCH_RAW` wrapped in double-quotes, joined by a space (e.g. `"ci_churn.py" "SKILL.md"`)
- `EXAMPLE_OUTPUT` = `EXAMPLE_OUTPUT_RAW` wrapped in a triple-backtick block if not already fenced

### Step 2 — echo plan and confirm

Print a summary and ask for confirmation before making any network calls:

```
About to create: gaia-research/skill-<name>
  Invoke trigger : /<name>
  Install path   : .agents/skills/<name>
  Installer gets : <files>
  Repo will be   : https://github.com/gaia-research/skill-<name>
Proceed? [y/N]
```

Abort on anything other than `y`/`Y`.

### Step 3 — fetch templates

Use `curl`, not `gh api` (avoids path-rewriting issues on Windows). Do NOT
clone `gaia-research/gaia-research` — the repo is large.

```bash
BASE="https://raw.githubusercontent.com/gaia-research/gaia-research/main/templates/skill-repo"
TMPDIR_TEMPLATES="$(mktemp -d)"
for f in README.template.md SKILL.template.md install.template.sh \
         .gitignore LICENSE.template powered-by-gaia.svg; do
  curl -fsSL "${BASE}/${f}" -o "${TMPDIR_TEMPLATES}/${f}"
done
```

If any fetch returns non-200, bail with:
```
ERROR: Could not fetch template file '<f>' from gaia-research/gaia-research.
The templates may not be published yet. Check:
https://github.com/gaia-research/gaia-research/tree/main/templates/skill-repo
```

### Step 4 — substitute placeholders

Use Python (not sed) — multi-line values and backticks break sed.

```python
import os, pathlib, shutil

subs = {
    "{{skill_name}}": os.environ["SKILL_NAME"],
    "{{skill_display_name}}": os.environ["SKILL_DISPLAY_NAME"],
    "{{skill_tagline}}": os.environ["SKILL_TAGLINE"],
    "{{skill_description}}": os.environ["SKILL_DESCRIPTION"],
    "{{repo_slug}}": os.environ["REPO_SLUG"],
    "{{invoke_trigger}}": os.environ["INVOKE_TRIGGER"],
    "{{install_path}}": os.environ["INSTALL_PATH"],
    "{{example_output}}": os.environ["EXAMPLE_OUTPUT"],
    "{{requirements}}": os.environ["REQUIREMENTS"],
    "{{year}}": os.environ["YEAR"],
    "{{org}}": os.environ["ORG"],
    "{{script_name}}": os.environ.get("SCRIPT_NAME", ""),
    "{{files_to_fetch}}": os.environ["FILES_TO_FETCH"],
}

src_dir = pathlib.Path(os.environ["TMPDIR_TEMPLATES"])
out_dir = pathlib.Path(os.environ["OUT_DIR"])
out_dir.mkdir(parents=True, exist_ok=True)

for src_name, dst_name in [
    ("README.template.md", "README.md"),
    ("SKILL.template.md",  "SKILL.md"),
    ("install.template.sh", "install.sh"),
    ("LICENSE.template",   "LICENSE"),
]:
    text = (src_dir / src_name).read_text(encoding="utf-8")
    for k, v in subs.items():
        text = text.replace(k, v)
    (out_dir / dst_name).write_text(text, encoding="utf-8")

# Static files — copy unchanged
for static in [".gitignore", "powered-by-gaia.svg"]:
    shutil.copy(src_dir / static, out_dir / static)
```

### Step 5 — create the repo, commit, push

```bash
OUT_DIR="/tmp/${REPO_SLUG}"
cd "$OUT_DIR"
chmod +x install.sh
git init -b main
git add .
git commit -m "chore: bootstrap ${REPO_SLUG} from templates/skill-repo

Generated by /skill-template. Placeholders substituted by ci-churn-style Python substitution.
Template source: https://github.com/gaia-research/gaia-research/tree/main/templates/skill-repo"
gh repo create "gaia-research/${REPO_SLUG}" \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "${SKILL_TAGLINE}"
```

### Step 6 — print final report

```
✓  Created: https://github.com/gaia-research/<repo-slug>
✓  Files: README.md  SKILL.md  install.sh  LICENSE  .gitignore  powered-by-gaia.svg

   Install one-liner:
   bash <(curl -fsSL https://raw.githubusercontent.com/gaia-research/<repo-slug>/main/install.sh)

   Next steps:
   1. Add the skill payload (script/logic files) and push a second commit
   2. Test the one-liner in a scratch dir that has .agents/skills/ present
   3. Update the gaia-skill-tree skills source list in registry/skill-sources.md
```

## Update flow

Invocation: `/skill-template update <existing-repo>`

1. Shallow-clone: `gh repo clone gaia-research/<repo> /tmp/<repo> -- --depth=1`
2. Auto-derive placeholder values from the existing `README.md` and `SKILL.md`
   (skill name from `SKILL.md` frontmatter `name:`, tagline from first `>` blockquote
   in README, invoke trigger from `## Install` one-liner, etc.). Confirm each with the user.
3. Fetch templates (Step 3) and substitute (Step 4) into `/tmp/<repo>-rendered/`.
4. Create branch `template/align-v1` in the cloned repo.
5. Copy only the six template outputs over the working tree:
   `README.md`, `SKILL.md`, `install.sh`, `.gitignore`, `LICENSE`, `powered-by-gaia.svg`.
   **Never touch the skill's logic files** (Python scripts, reference docs, etc.).
6. Show the diff; ask which files to apply (default: all).
7. Commit accepted changes and open a draft PR:
   ```bash
   git add -A
   git commit -m "chore: align to templates/skill-repo v1"
   git push -u origin template/align-v1
   gh pr create --draft \
     --title "chore: align to templates/skill-repo v1" \
     --body "Automated realignment via /skill-template update."
   ```

## Guardrails

- **Never push directly to `main` on an existing repo.** Update mode always uses a branch + draft PR.
- **Never touch logic files during update mode.** Only the six template outputs: `README.md`, `SKILL.md`, `install.sh`, `.gitignore`, `LICENSE`, `powered-by-gaia.svg`.
- **Never hard-code placeholder values.** Non-TTY: bail with the list of missing variables.
- **If `gh repo create` fails because the repo exists**, offer to switch to update mode.
- **Template static files** (`.gitignore`, `powered-by-gaia.svg`) are copied as bytes; never run substitution on them.

## Notes

- Template source: `gaia-research/gaia-research` → `templates/skill-repo/`
- Human bootstrap guide: same dir → `TEMPLATE_README.md`
- Token-spend logging: log as a comment on the new repo's first issue or the PR that created it.
- The `version:` field in this SKILL.md tracks the **skill** version. The template bundle version lives inside `SKILL.template.md` frontmatter and is independent.
