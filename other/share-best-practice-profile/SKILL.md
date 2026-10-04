---
name: share-best-practice-profile
description: Use when the user wants to publish or share a practice profile — e.g., "share my team profile", "publish this profile", "open-source my backend-defaults profile".
source: Grimoire project conventions; GitHub Gist and repository conventions
tags: [profile, sharing, open-source, ecosystem, contributor]
related: [review-best-practice-profile, write-best-practice-profile, apply-best-practice-profile]
---

# Share Best Practice Profile

Publish a validated practice profile so others can install and use it.

## Why This Is Best Practice

**Adopted by:** The `eslint-config-*` ecosystem (3000+ published configs on npm) and VS Code extension packs demonstrate the value of community-shared configuration bundles. A single `eslint-config-airbnb` install replaced thousands of manual ESLint rule configurations. Grimoire profiles follow the same pattern — one shareable file replaces manual skill selection for everyone who shares the same context.
**Impact:** A shared profile eliminates onboarding friction for new team members and external contributors who need to activate the same practices. A profile shared publicly becomes a reusable community asset — the same leverage as an open-source library.
**Why best:** Sharing without review leads to broken profiles that fail silently for others. The gate (`review-best-practice-profile` first) ensures what is shared actually works.

Sources: npm `eslint-config-*` ecosystem; VS Code extension pack format; Grimoire `docs/profiles.md`

## Steps

### 1. Confirm the profile is reviewed

If `review-best-practice-profile` has not been run on this profile, run it now and resolve any `FAIL` results before continuing. Warnings are acceptable.

**Review gate:** Before sharing, `review-best-practice-profile` MUST have been run against this profile. If it hasn't been run this session, run it now. Do not skip this step — a profile shared without review may contain conflicts or missing fields that will confuse recipients. If the review produces FAIL findings, show them and require explicit user confirmation ('Share anyway? [y/n]') before proceeding.

---

### 2. Choose sharing format

```
Share as:
  [g] GitHub Gist    — single file, easy to update, direct install URL
  [r] GitHub repo    — full repo, recommended for maintained profiles
  [c] Clipboard      — copy TOML to clipboard for private sharing
```

**Gist** — best for personal or small team profiles.
**Repo** — best for maintained, versioned, community profiles. Use naming convention: `grimoire-profile-<name>`.

---

### 3. Prepare for sharing

Add a `description` field if absent — required for others to understand the profile:

```toml
name = "my-team"
description = "Backend team defaults — DDD, SOLID, clean architecture boundaries."
```

For repo shares, generate a minimal README:

```markdown
# grimoire-profile-my-team

Practice profile for grimoire — backend team defaults.

## Install

\`\`\`bash
curl -fsSL https://raw.githubusercontent.com/<user>/grimoire-profile-my-team/main/my-team.toml \
  -o .grimoire/profiles/my-team.toml
\`\`\`

## Activate

\`\`\`toml
# grimoire.toml
profiles = ["my-team"]
\`\`\`

## Skills included

- apply-solid-principles
- apply-domain-driven-design
- apply-low-coupling
```

---

### 4. Publish

**Auth check:** Before running any `gh` command:
1. Check `gh auth status` — if not authenticated, stop: 'Run `gh auth login` first, then re-run this skill.'
2. Check `gh` is installed — if not: 'Install GitHub CLI (`brew install gh` or https://cli.github.com), then re-run. Alternatively, share the profile file manually: attach `.grimoire/profiles/[profile-name].toml` to your PR or send directly.'
3. If the `gh` command fails after auth check passes: show the error and output: 'Manual fallback: commit the profile file and open a PR manually.'

**Gist:**
```bash
gh gist create .grimoire/profiles/my-team.toml --public --desc "grimoire profile: my-team"
```

**Repo:**
```bash
gh repo create grimoire-profile-my-team --public
git init && git add . && git commit -m "feat: initial profile"
git remote add origin https://github.com/<user>/grimoire-profile-my-team.git
git push -u origin main
```

---

### 5. Confirm with install instructions

```
✓ Published: https://gist.github.com/<user>/<id>

Others install with:
  curl -fsSL https://gist.githubusercontent.com/<user>/<id>/raw/my-team.toml \
    -o ~/.grimoire/profiles/my-team.toml

Then activate:
  profiles = ["my-team"]   # in grimoire.toml
```

**Install command:** Include the exact version or commit in the install command so recipients get the exact profile reviewed:
```
/plugin install [profile-name]@[version-or-commit]
```
If no version is tagged, include the Git commit SHA. A profile install without a version pin can drift as the source changes.

**Profile versioning strategy:**
1. **Git tag** (preferred): tag the commit that contains the profile with a semver tag: `git tag profiles/[profile-name]/v1.0.0`. Install command: `/plugin install [profile-name]@v1.0.0`
2. **Commit SHA** (fallback): if no tag exists, use the full commit SHA. Install command: `/plugin install [profile-name]@[sha]`
3. **No version** (not recommended): omit version only if the profile is in active development and recipients should always get latest. Note this in the install instructions.

**Which version strategy to use:**
- Profile has a stable release tag → use git tag (recipients get a known-stable version)
- No tag but content is finalized → use commit SHA (immutable reference, won't drift)
- Content is actively evolving → use no version, but add a warning: 'This profile is in development — recipients always get latest, which may change'

Never use 'no version' for a profile others will depend on in production workflows.

## Common Mistakes

**Sharing before reviewing.** Always run `review-best-practice-profile` first. A broken profile shared publicly is harder to fix than one caught before publish.

**Missing description.** Others can't evaluate a profile without knowing what it's for. Always include a `description` field before sharing.
