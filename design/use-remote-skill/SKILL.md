---
name: use-remote-skill
description: >
  Fetch and execute a remote skill on-the-fly without installing it permanently.
  Use when the user wants to try a skill once, run a skill from GitHub, use a remote skill without installing,
  or mentions "use-remote-skill", "run remote skill", "try this skill", "fetch skill", "one-time skill",
  or provides a GitHub URL/shorthand pointing to a skill they want to execute.
  This is the go-to skill whenever someone wants to use a skill they haven't installed locally.
  Also use when the user mentions skills.sh or wants to search for available skills.
user-invocable: true
argument-hint: "<source> [skill-name] [-- args for the skill]"
---

# use-remote-skill

Fetch a remote skill and execute it in the current session without installing it permanently. The skill is loaded, run, and discarded.

## Step 1: Parse arguments

The user's input after `/use-remote-skill` is flexible. Detect the format:

**Format 1 — Direct SKILL.md URL:**
Input ends with `SKILL.md`. Example: `https://raw.githubusercontent.com/owner/repo/main/skills/foo/SKILL.md`
→ You have the final URL. Go to Step 3.

**Format 2 — Full GitHub repo URL (± skill name):**
Starts with `https://github.com/`. Example: `https://github.com/owner/repo skill-name`
→ Extract `owner/repo` from URL. If a skill name follows, go to Step 2a. Otherwise go to Step 2b.

**Format 3 — GitHub shorthand (owner/repo + skill name):**
First arg contains exactly one `/` and does NOT start with `http`. Example: `anthropics/skills frontend-design`
→ Treat as `owner/repo`. Next argument is the skill name. Go to Step 2a.

**Format 4 — Skill name only (skills.sh search):**
First arg has no `/` and doesn't start with `http`. Example: `frontend-design`
→ Go to Step 2c.

**Special — skills.sh package URL:**
If input matches `https://skills.sh/package/github/{owner}/{repo}/{skill-name}`, extract owner, repo, and skill-name. Go to Step 2a.

In all formats, everything after `--` is the **task** to pass to the fetched skill.

## Step 2: Resolve the SKILL.md URL

### 2a. Resolve from owner/repo + skill-name

Try these URLs in order using WebFetch. Stop at the first successful (HTTP 200) response:

1. `https://raw.githubusercontent.com/{owner}/{repo}/main/skills/{skill-name}/SKILL.md`
2. `https://raw.githubusercontent.com/{owner}/{repo}/main/{skill-name}/SKILL.md`
3. `https://raw.githubusercontent.com/{owner}/{repo}/master/skills/{skill-name}/SKILL.md`
4. `https://raw.githubusercontent.com/{owner}/{repo}/master/{skill-name}/SKILL.md`

If all fail, tell the user: "Could not find skill '{skill-name}' in {owner}/{repo}. Check the skill name and repo."

### 2b. List skills in a repo (no skill name given)

Fetch the repo's skills directory listing:

```
https://api.github.com/repos/{owner}/{repo}/contents/skills
```

Use WebFetch with header `Accept: application/vnd.github.v3+json`. Parse the JSON response for entries with `"type": "dir"`. Present them as a numbered list:

```
Available skills in {owner}/{repo}:
  1. skill-a
  2. skill-b
  3. skill-c
Which one? (enter number or name)
```

Wait for the user to pick, then go to Step 2a with the chosen skill name.

If `skills/` doesn't exist (404), try the repo root (`/repos/{owner}/{repo}/contents`) and look for directories containing a `SKILL.md`.

### 2c. Search skills.sh by name

Fetch: `https://skills.sh/api/search?q={skill-name}` using WebFetch.

**Single result** → extract `source` (owner/repo) and `skillId` (skill name), go to Step 2a.

**Multiple results with a clear winner** (exact name match AND 3x+ more installs than runner-up) → use it automatically, go to Step 2a.

**Multiple results, no clear winner** → present options sorted by installs:
```
Found skills matching "{skill-name}":
  1. anthropics/skills/frontend-design (45,000 installs)
  2. pbakaus/impeccable/frontend-design (12,000 installs)
Which one? (enter number)
```
Wait for user to pick, extract source and skillId, go to Step 2a.

**No results** → tell the user: "No skills found matching '{skill-name}' on skills.sh. Try a different name or provide a GitHub URL directly."

## Step 3: Fetch the skill content

Use WebFetch to fetch the resolved SKILL.md URL. On failure:
- **404**: "Skill not found at {url}. Check the skill name and repo."
- **403**: "GitHub rate limit hit. Try again later or provide a direct raw URL."
- **Other error**: Show the HTTP status and URL.

## Step 4: Execute the fetched skill

1. **Show status:**
   ```
   Fetched "{skill-name}" from {source}. Running...
   ```

2. **Follow the fetched SKILL.md instructions exactly** as if it were a locally installed skill. Use the tools it specifies, produce the outputs it defines, follow its workflow step by step.

3. **Pass through arguments.** If the user provided text after `--`, treat it as the task/prompt for the fetched skill.

4. **Handle dependency files.** If the skill's instructions reference files at relative paths (e.g., `scripts/cli.mjs`, `references/foo.md`), construct the full raw GitHub URL using the same base path where SKILL.md was found and fetch them with WebFetch. If a referenced file can't be fetched, inform the user and continue — SKILL.md instructions are usually self-contained enough to be useful on their own.

5. **Do NOT persist the skill.** Don't write it to disk or add it to the user's installed skills. At the end, suggest:
   ```
   To install this skill permanently: npx skills add {owner}/{repo} --skill {skill-name}
   ```
