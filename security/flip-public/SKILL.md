---
name: flip-public
description: Pre-flip checklist + procedure for making a private GitHub repo public. Verifies the project has a /setup skill, a LICENSE (default MIT), scrubbed content (regex + Haiku layers), README onboarding pattern, security pass for credentials and internal references. Use when a repo is about to be flipped public for the first time. The flip is one-way — treat as point of no return.
user-invocable: true
---

# Flip Public

The bar to clear before flipping a private GitHub repo public. Walk the user through the checklist; everything must be ✅ before the flip.

**Public is one-way.** After the flip, anyone can clone the full history including commits, PR descriptions, and closed-but-public discussions. Making it private again doesn't unindex Google, doesn't recall forks, doesn't undo anything. This skill is the bar to clear.

## When to invoke

- The user says "flip this public", "make this public", "we're ready to go public with X."
- A repo's first launch is on the runway and going public is part of the launch.

## When NOT to invoke

- Repo is already public (verify via `gh repo view <owner>/<name> --json visibility`).
- The user wants to share a single file or branch — flipping the whole repo is the wrong tool.

## Checklist (each must be ✅)

### 1. /setup skill exists

Every public repo onboards via clone → `claude` → `/setup`. Verify `.claude/skills/setup/SKILL.md` exists in the repo.

If missing: pause and create it first. Mirror the pattern from `ai-team-lead` or `claude-live-feedback-plugin` — walk through dependency installs, config files, optional pieces, pause for user consent on side-effects.

### 2. LICENSE file present

- Check `LICENSE` (or `LICENSE.md` / `LICENSE.txt`) at repo root.
- If missing: **default to MIT**. Use `gh repo view fryanpan/<some-other-repo> --json licenseInfo` to find a working template, OR fetch the canonical MIT text. Set the copyright year and name correctly.
- For non-MIT (Apache-2.0, GPL, etc.), get explicit confirmation from the user.

### 3. README onboards new readers

- `README.md` exists at root.
- README explains in 1-2 sentences: what the project is, why it exists, who it's for.
- README has a `## Getting started` (or similarly-named) section with the standard pattern:
  ```
  1. Clone: git clone https://github.com/<owner>/<name>.git
  2. Start Claude: claude
  3. Ask for setup: please help me do setup
  ```
- README references the license at the bottom.
- No `*.local` URLs (readers reach via the public internet — use Tailscale or public domains only).

### 4. Scrubbing pass — both layers + manual surfaces

**Automated:**
```sh
python3 scripts/scrub-check.py --scan-all-tracked
python3 scripts/scrub-haiku.py --scan-all-tracked   # if wired
```

For each finding:
- **True positive** — anonymize, generalize, or delete. Re-run scrub until clean.
- **False positive** (public sibling repo flagged because it's in registry.yaml) — confirm via `gh repo view fryanpan/<sibling> --json visibility` that the mentioned repo is public, then proceed with `SCRUB_SKIP=1 git push ...` and note the false-positive reasoning in the commit message.

**Manual (scrub-check only sees tracked files):**
- **Full commit history** — `git log --all --pretty=full` and skim for project names, real names, internal URLs.
- **PR descriptions + PR comments** — also become public on flip. `gh pr list --state all --json number,title,body | jq ...` for a quick scan.
- **Closed issues + their comments** — same surface.

If commit history has scrubbable content: **squash to a single "Initial release" commit** before flipping (`git reset --soft <root> && git commit --amend`). For multi-author repos, get author consent before squashing — squash erases authorship attribution.

**Ask what the history is FOR before you squash it.** Squashing destroys every commit date, and dates are the whole evidentiary value when a repo exists to show *when* work was done — prior art against a client or employer, an invention-assignment boundary, a priority claim. In those cases the dated history IS the deliverable, and squashing it to satisfy this checklist would delete the thing being published. Scrub by rewriting content across history (`git filter-repo`) or by publishing a curated copy, and keep the timestamps. Health Tool caught this step pointed the wrong way on 2026-08-24, on a repo being published specifically to date prior art.

### 5. Security pass

Beyond what scrub-check catches:

- **Hardcoded credentials** — grep tracked files for: `token`, `password`, `secret`, `api_key`, `BEGIN PRIVATE KEY`, `xoxb-`, `gh[ps]_`, `sk-ant-`, `sk-` (OpenAI), AWS access key patterns.
- **Internal URLs / IPs** — `*.internal`, your tailnet hostnames, IPs in `10.x` / `172.16-31.x` / `192.168.x`.
- **Real names** that haven't been consented to for *this specific public artifact*. Past consent for one venue doesn't transfer.
- **Test fixtures + seed data** — JSON/YAML/SQL fixtures with real emails, real names, internal codenames.
- **CI configs** — `.github/workflows/`, `Makefile`, package scripts referencing private deploy targets or internal dashboards.

### 6. Working tree + remote are clean

```sh
git status                       # empty
git log @{u}..HEAD               # empty
git ls-files | head              # sanity-check
```

### 7. Run the flip

**No remote yet** (brand-new public repo from a local-only project):
```sh
gh repo create fryanpan/<name> --public --source=<absolute-path> --push
```

**Already on GitHub as private** (existing repo flipping visibility):
```sh
gh repo edit fryanpan/<name> --visibility public
```

### 8. Configure branch protection on `main` — required before strangers can see the repo

**Bar to meet:**

- Nobody can merge to `main` without the user's approval — PR-review required (≥1 approving review) + `enforce_admins: true` so even the owner can't bypass.
- Nobody except registered collaborators can push branches or commits — push restrictions to an explicit allowlist (typically just the owner) OR use Rulesets to restrict push.

**The window between flipping public and applying protection should be near-zero** — set protection immediately. If the repo is being flipped from private→public, set protection BEFORE the visibility flip. If using `gh repo create --public`, set protection in the same minute as creation.

**Command template (personal-account repos):**

```bash
gh api -X PUT "repos/<owner>/<repo>/branches/main/protection" \
  --input - <<'EOF'
{
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true,
    "require_last_push_approval": true
  },
  "enforce_admins": true,
  "required_status_checks": null,
  "restrictions": {"users": ["<owner>"], "teams": [], "apps": []},
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_linear_history": true,
  "required_conversation_resolution": true
}
EOF
```

Substitute `<owner>` (e.g. `fryanpan`) and the default branch (often `main`, sometimes `master` or `stage`).

**Caveat:** the classic `restrictions` field for push-allowlist only works reliably on organization repos or paid personal-plan tiers. For personal-account repos on the free tier, `restrictions` may be silently ignored and the push-allowlist must be configured via GitHub's newer **Rulesets** UI: `Settings → Rules → Rulesets → New ruleset → "Restrict who can push to matching refs"`. The PR-review and `enforce_admins` flags work on personal repos via the classic API above.

**Verify after applying:**

```bash
gh api "repos/<owner>/<repo>/branches/main/protection" --jq '{
  reviews_required: .required_pull_request_reviews.required_approving_review_count,
  enforce_admins: .enforce_admins.enabled,
  push_restricted: (.restrictions != null),
  force_push_blocked: (.allow_force_pushes.enabled == false),
  deletion_blocked: (.allow_deletions.enabled == false)
}'
```

All five should be truthy / non-null.

### 9. Post-flip sanity check

- Open the repo in **incognito** (no auth). Confirm what a stranger sees matches expectation.
- If anything still surfaces that shouldn't:
  - Currently-tracked file → PR a sanitized version + force-push that.
  - Commit message / PR description → rewrite history with force-push (high cost; coordinate with collaborators).
  - Closed-but-public discussion → edit or delete the comment via GitHub UI.
  - In edge cases, accept the exposure rather than break the public history. Surface the trade-off to the user.

## After flipping

- Confirm: `https://github.com/<owner>/<name>` is the live URL.
- Suggest a brief announcement if the user wants visibility (Slack, Discord, X, blog post).
- If the repo's name is in `registry.yaml`, note it's now public — eventually the scrub-check tool can use a public-marker to skip false positives on this repo's mention by name in other repos.

## What to avoid

- **Don't flip without running scrub.** "It's just my notes" is exactly when leaks slip.
- **Don't flip without a license.** Without one, default copyright is "all rights reserved" — readers can't fork or modify.
- **Don't flip without `/setup` + onboarding README.** Public = strangers will try to use it; the bar for onboarding is higher than for a private repo.
- **Don't flip and "clean up history later."** Public commit history is permanent and indexed. If squashing is needed, do it before the flip.
- **Don't skip the post-flip incognito check.** Your IDE shows you a version with caches + auth; a stranger sees something else.
- **Don't flip a multi-author repo without informing the contributors.** Their commits become public attributions too.

## Reference

- `plugin/team-lead-fleet/rules/public-content-scrubbing.md` — principle-level rules about private vs public content.
- `plugin/team-lead-fleet/rules/security-posture.md` — credential hygiene + ops rules.
- `scripts/scrub-check.py` + `scripts/scrub-haiku.py` — automated scrub layers.
- Example skills: `ai-team-lead/.claude/skills/setup/SKILL.md` and `claude-live-feedback-plugin/.claude/skills/setup/SKILL.md` are the canonical `/setup` patterns.
