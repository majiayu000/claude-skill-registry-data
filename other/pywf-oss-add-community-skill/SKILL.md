---
name: pywf-oss-add-community-skill
description: "Install an optional community Agent Skill from the pinned catalog after a security review, or add or update a catalog entry from a GitHub link. Use when the user asks which community skills are available, wants one installed, or gives a GitHub link to a skill to catalog or pin."
---

Install a community skill from the catalog, or add or update a catalog entry. A script does the installing; this skill picks the entry, reviews the staged content, and keeps the catalog correct.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/26-community-skills.md

Catalog: ../pywf-oss-base/assets/community-skills.toml

## Install a skill

The script commands are in `26-community-skills.md` section 3.

1. **Pick.** Run the script with `--list`, match the user's need against each entry's `when_to_use`, and confirm the choice with the user.
2. **Stage** with `--name <skill_name>`, without `--install`.
3. **Review** the staged folder as in `26-community-skills.md` section 4. Report what the skill does, what each script touches, and anything risky.
4. **Install.** After the user's yes, rerun with `--install`. Report the installed path and its `.source.json`.
5. **Git.** The skill is git-ignored by default. Ask whether it should be committed with the repo; if yes, delete its line from `.gitignore`.

## Add or update a catalog entry

1. From the user's GitHub link, find the skill folder and pin it, as in `26-community-skills.md` section 2.
2. Show the new or changed entry, with a proposed `when_to_use`, and save it after the user's yes. For a new entry, also add its `.gitignore` line.
3. Optionally stage it once, to prove the URL works.

## Boundaries

- Never install a skill that has not been staged and reviewed.
- Never run any of a downloaded skill's scripts during the review.
- Never overwrite an installed skill without the user's yes (`--force`).
