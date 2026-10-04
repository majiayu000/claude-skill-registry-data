---
name: publish-repo
description: Publish a local git repository to GitHub from Codex or AgInTi with safe commit discipline, metadata, citation, and push verification. For lachlanchen or LazyingArt repositories, default to the complete 11-language profile README, banner, support panel, and sponsor package.
---

# Publish Repo

Use this skill when the user asks to publish a local repository to GitHub, add repository metadata, set topics/homepage, write a polished public README, create profile-style multilingual README files, add LazyingArt banner/support panels, add `CITATION.cff` / a README citation block / GitHub's "Cite this repository" UI, add `.github/FUNDING.yml`, or prepare a repo for public release from Codex or AgInTi.

## Core Rules

- Read the repo's `AGENTS.md` first.
- Never revert unrelated user changes.
- Inspect `git status --short --branch` before staging.
- Stage only intended files unless the user explicitly asks for all changes.
- Commit before publishing when the repo has local changes.
- Do not publish a dirty worktree. The helper script refuses dirty trees by default.
- Use `gh` for GitHub repo creation, metadata, topics, and push validation.
- Prefer public visibility only when the user asks to publish publicly or gives no privacy constraint.

## Workflow

1. Audit the repository:
   - `git status --short --branch`
   - `git remote -v`
   - `gh auth status`
   - read `README.md`, `.gitignore`, and `AGENTS.md` if present.
2. Prepare public-facing resources:
   - polished `README.md`;
   - i18n README files when requested, and by default for a `lachlanchen` or LazyingArt publication;
   - `CITATION.cff` and README citation block when the repo should be citable;
   - banner/logo assets when useful;
   - resource map to papers, docs, references, demos, scripts, or skills.
3. Validate local content:
   - run relevant build/test commands;
   - verify links and file paths with `rg`/`find`;
   - compile papers if the repo contains LaTeX and the change affects it.
4. Commit intentionally:
   - use a concise imperative message;
   - include only files in scope.
5. Publish:
   - run `scripts/publish_repo.sh` from this skill, or manually run the same `gh` steps.
6. Verify:
   - `git status --short --branch`;
   - `gh repo view OWNER/REPO --json nameWithOwner,url,homepageUrl,description,repositoryTopics`;
   - open or report the final GitHub URL.

## Lachlanchen Publication Default

Use this mode automatically when the target owner is `lachlanchen`, the repository is a LazyingArt project, or the user asks for "beautiful README", "like lachlanchen profile", "11 languages", "LazyingArt banner", "donation panel", or `.github sponsor`. The user may explicitly opt out for a particular repository.

Read `references/lachlanchen-profile-readme-style.md` before editing. Required outputs:

- `README.md` in English.
- `i18n/README.ar.md`, `README.es.md`, `README.fr.md`, `README.ja.md`, `README.ko.md`, `README.vi.md`, `README.zh-Hans.md`, `README.zh-Hant.md`, `README.de.md`, and `README.ru.md`.
- The 11-language header on every README, with root-relative links in the root README and `../README.md` links in i18n files.
- LazyingArt banner from the profile README.
- Donation panel with Donate, PayPal, and Stripe links.
- `.github/FUNDING.yml` matching the lachlanchen profile sponsorship pattern.
- `CITATION.cff` at repository root, plus a citation block in `README.md` and all i18n README files.
- A concise repo-specific README body: project promise, visual/asset signal, current contents, quick start, validation/build commands, status, and links to key PDFs/docs/assets.
- GitHub About metadata: a concise description, the most relevant public product or project homepage, and repo-specific topics including `lazying-art`.

Treat the 11 README files as one public document set. When public-facing content changes materially, update every translation in the same publication commit. Do not machine-translate blindly if repo-specific terms matter. Preserve project names, command names, file paths, and badge labels. Translate section prose completely for each language, not only the headings.

Before publishing, run `scripts/check_profile_readmes.py` from this skill against the target repository. It verifies all 11 files, navigation, profile panels, section counts, substantive prose, and stable command/BibTeX blocks; it complements rather than replaces a human-quality translation review. After pushing, verify the live default branch plus description, homepage, and topics with `gh repo view`.

## Citation Mode

Use this mode when the user asks to make the repository citable, add a citation block, or show a citation below the GitHub About section.

- Add root `CITATION.cff`. GitHub reads this file from the default branch and renders **Cite this repository** in the repo UI.
- Include at least: `cff-version`, `message`, `type`, `title`, `authors`, `repository-code`, and `url` when available.
- Prefer `type: software` for code/research workspaces.
- Add a README `## Citation` section with a BibTeX block and a note that GitHub uses `CITATION.cff`.
- If i18n READMEs exist, add translated citation sections that link to `../CITATION.cff` and keep the same BibTeX block.
- Validate with `rg -n "CITATION\\.cff|Cite this repository|@software" README.md i18n CITATION.cff` and `git diff --check`.

## Helper Script

If this skill is vendored inside the target repository, run from that repository root:

```bash
skills/publish-repo/scripts/publish_repo.sh \
  --owner lachlanchen \
  --repo GaugeHand \
  --visibility public \
  --homepage https://lazying.art \
  --description "GaugeHand: a lockable contour-field robotic hand concept for dense-contact grasping" \
  --topics "robotics,robotic-hand,contour-gauge,pin-array,dense-contact,tactile-sensing,soft-robotics,gripper,manipulation,hardware-research,lazying-art"
```

If installed as a Codex user skill or loaded from LazySkills, run the script by absolute path while keeping the working directory at the repository root:

```bash
$LAZYSKILLS_ROOT/skills/publish-repo/scripts/publish_repo.sh \
  --owner lachlanchen \
  --repo GaugeHand \
  --visibility public \
  --homepage https://lazying.art \
  --description "GaugeHand: a lockable contour-field robotic hand concept for dense-contact grasping" \
  --topics "robotics,robotic-hand,contour-gauge,pin-array,dense-contact,tactile-sensing,soft-robotics,gripper,manipulation,hardware-research,lazying-art"
```

The script:

- requires `git` and `gh`;
- checks `gh auth status`;
- refuses to run if the worktree has uncommitted changes;
- creates the GitHub repo if it does not exist;
- adds `origin` if missing;
- pushes the current branch;
- sets homepage, description, and topics.

The script does not write README/i18n files. Codex or AgInTi must prepare and commit those files first.

## Codex Notes

Codex should do the editorial work and commit itself, then use the script for the GitHub-specific publishing step. If `gh` is not authenticated, stop and tell the user to run `gh auth login`.

## AgInTi Notes

AgInTi can call the same script as a deterministic publish step after its planning/editing phase. See `references/aginti-compatibility.md` for a compact task contract that AgInTi agents can reuse.

## Final Response Checklist

Report:

- GitHub URL;
- branch pushed;
- commit hash;
- metadata applied: homepage, description, topics;
- citation support added: `CITATION.cff`, README block, and i18n blocks if applicable;
- validation commands run;
- any blocker, such as missing auth or repo visibility failure.
