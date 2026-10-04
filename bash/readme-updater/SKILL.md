---
name: readme-updater
description: >
  Update the root README.md with entries for new or changed agent companies.
  Use when a new company has been added to the repo, when company details have
  changed (agents added/removed, skills added/removed), or when the user asks
  to refresh/sync the README. Triggers on: "update the readme", "add this
  company to the readme", "sync readme", "refresh readme", or after creating
  a new company with company-creator.
---

# README Updater

Update the root `README.md` to reflect all companies in the repo, matching the established format.

## Workflow

### 1. Discover companies

List all top-level directories that contain a `COMPANY.md` file. Skip `default/`, `skills/`, and any dotfile directories.

### 2. Gather data for each company

For each company directory, collect:

- **Name and description** — from `COMPANY.md` YAML frontmatter (`name`) and the prose body (first paragraph after the frontmatter closing `---`)
- **Upstream source** — from the `Generated from [name](url)` line at the bottom of `COMPANY.md`. Extract both the display name and the URL
- **Agents** — list subdirectories under `agents/`. Count them. Format agent names by replacing hyphens with spaces and title-casing
- **Skills** — list `skills/*/SKILL.md` files. Count them. Use the directory name as the skill name

### 3. Generate org chart image

For each company that does NOT already have an `images/org-chart.png`, generate one:

```bash
~/geetorus scripts/generate-company-assets.ts <company-directory>
```

If the image already exists and the company hasn't changed, skip regeneration. If the user explicitly asks to regenerate, run it again.

### 4. Write the README

Replace the `## Companies` section in `README.md` with entries for every discovered company. Preserve all other sections (`## Structure`, `## Shared Skills`, `## Usage`, etc.) exactly as they are.

#### Entry format

Each company entry MUST follow this exact format:

````markdown
### [Company Name](./<directory-name>)

```bash
npx companies.sh add geetorusai/companies/<directory-name>
```

<One-sentence description from COMPANY.md body. Keep it concise — one to two sentences max.> Built from [upstream name](upstream-url).

![Company Name Org Chart](./<directory-name>/images/org-chart.png)

> **Agents (N):** Agent One, Agent Two, Agent Three (limit to 25 "and N more")
>
> **Skills (N):** skill-one, skill-two, skill-three (limit to 25 "and N more")
````

Rules:

- The heading links to the company directory
- The description is a brief summary, NOT the full COMPANY.md body
- The upstream source link comes from the "Generated from" line in COMPANY.md. Append it naturally to the description sentence (e.g., "Built from [gstack](url).")
- The org chart image path is always `./<dir>/images/org-chart.png`
- Agent names are title-cased with hyphens replaced by spaces
- Skill names stay hyphenated (as directory names)
- Agent and skill counts go in parentheses after the label
- If a company has no skills directory or no skills, omit the **Skills** line

#### Index table

Before the `## Companies` heading, include a summary index table:

```markdown
| Company                         | Agents | Skills | Source        |
| ------------------------------- | ------ | ------ | ------------- |
| [Company Name](#heading-anchor) | N      | N      | [source](url) |
```

- The Company column links to the heading anchor (lowercase, hyphens for spaces)
- Skills column shows `—` if the company has no skills
- Table order matches the company entry order below

#### Ordering

The first three companies are always **GStack**, **Superpowers Dev Shop**, and **Agency Agents**, in that order. Remaining companies follow alphabetically by directory name. Place `default` last if it is included.

#### Naming overrides

Some companies use a display name different from their COMPANY.md `name` field. Always apply these overrides:

- `agency-agents` directory → display as **Agency Agents** (not "The Agency")

### 5. Verify

After writing, read back the README and confirm:

- Every company directory with a COMPANY.md has an entry
- No company entries exist for directories that were removed
- All image paths point to files that exist
- Agent and skill counts match actual directory contents
