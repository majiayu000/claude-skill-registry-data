---
name: provision-tutorial-repo
description: Provision a new sap-tutorials tutorial repo pair (public source + private -Contribution), their four org teams, and the content-rebuild CI/notify workflows — matching the org convention used by every existing product repo. Use when asked to set up / create a new tutorial repository, repo pair, or product area in the sap-tutorials org.
---

# Provision a new tutorial repo pair

Sets up a new product area in the `sap-tutorials` org exactly like the existing
ones: a **public source repo** `<name>`, a **private QA repo**
`<name>-Contribution`, four org teams, base CI, and the content-rebuild notify
workflow that wires the repo into the `tutorials-ims` platform.

## When to use

Asked to "set up a new repo in sap-tutorials", "create the main and
-Contribution repos like the others", or stand up a new product/topic area.

## Prerequisites

- `gh` authenticated to **github.com** as a `sap-tutorials` **org owner**, or
  with an active **just-in-time (20-minute) admin elevation**. A plain org
  member cannot create repos or teams — `provision.sh` fails its preflight.
  Ask the requester to elevate right before you run the mutating steps.
- Node/`gh` `workflow` scope (needed to commit workflow files via the API).

## Key facts (why this works)

- **Templates carry the base CI.** `tutorial-repo-template` and
  `tutorial-repo-Contribution-template` are real GitHub template repos that
  already ship `community-requester-id.yaml`, `label-issues.yml`, and the two
  `tutorial-ci` caller workflows (`tutorial-pr-checks.yml` + `tutorial-pr-comment.yml`,
  pinned `@v1`). **No `tutorial-ci` rollout is required** — CI comes with the
  template.
- **Templates omit the notify workflow.** The per-repo rebuild-dispatch workflow
  is added separately: `notify-tutorials-ims.yml` on the source repo,
  `notify-qa.yml` on the Contribution repo. Both are repo-agnostic
  (`${{ github.repository }}`) — copy verbatim from any current repo
  (`btp-adai` / `btp-adai-Contribution` are the canonical source).
- **No tutorials-ims code change.** The platform auto-discovers any org repo
  that has a `tutorials/` folder (`scripts/parsers/github.ts` →
  `discoverAllTutorials`, skipping archived/fork/`EXCLUDED_REPOS`). A new source
  repo is picked up automatically once it has content; `-Contribution` repos are
  private and excluded by naming, like all the others.
- **Notify auth is org-level.** The notify workflow fires only when
  `vars.USE_GITHUB_APP == 'true'` and the `sap-tutorials-builder` App is
  installed on the repo (org secrets `TUTORIALS_APP_ID` / `TUTORIALS_APP_PRIVATE_KEY`
  are org-wide, visibility all). App installation is UI-only and org-owner-gated.

## Team convention

For product `<name>` (mirrors `ai-core`):

| Team | Repo | Grant |
|------|------|-------|
| `<name>-admin` | `<name>` | admin |
| `<name>-team` | `<name>` | maintain |
| `<name>-contribution-admin` | `<name>-Contribution` | admin |
| `<name>-contribution-team` | `<name>-Contribution` | maintain |

Admin grant tries the org JIT custom role `admin-ondemand` first, falling back
to plain `admin`. Admin-team membership usually mirrors between the source and
contribution admin teams; likewise for the maintain teams.

## Steps

1. **Confirm inputs** with the requester: product `<name>` (prefer a neutral
   name over a marketing product name), repo description, admin logins, team
   member logins. Confirm the 4-team layout (some ask for only 2).
2. **Dry-run first** to review every mutation:
   ```bash
   .claude/skills/provision-tutorial-repo/provision.sh \
     --name integration \
     --description "Developer Tutorials for SAP integration" \
     --admins "ajmaradiaga,jung-thomas" \
     --members "ajmaradiaga,PalakGarg7,manouxnam,shyam-corpworks" \
     --dry-run
   ```
3. **Ask the requester to elevate** (org-owner / 20-min JIT) — say so explicitly;
   creation fails without it.
4. **Run for real** (drop `--dry-run`). The script creates both repos, copies the
   notify workflows, sets `USE_GITHUB_APP=true`, creates the four teams, adds
   members, and applies the repo grants. It is re-runnable — existing teams are
   skipped.
5. **Complete the org-owner-only follow-ups** the script prints:
   - Install `sap-tutorials-builder` on both new repos (Contents:write on
     `tutorials-ims`).
   - Confirm the org `TUTORIALS_APP_*` secrets reach the new repos.
   - (Optional) mark `tutorial-pr-checks` Required in branch protection to make
     the structural checks blocking.
6. **Verify**: `gh repo view <org>/<name>`, list `.github/workflows` on both
   repos (5 workflows: 4 base + 1 notify), and `gh api orgs/<org>/teams/<team>/repos`
   shows the grants. A first tutorial push to `main` should trigger the notify
   workflow and a `tutorial-updated` rebuild in `tutorials-ims`.

## Gotchas

- Both templates default to `main`; keep it — the notify workflows trigger on
  `[master, main]` so `main` is correct and `master`-default repos still work.
- `-Contribution` MUST be **private**; source MUST be **public** (fork PRs get no
  secrets, and the public `tutorial-ci` must be checkout-able by every consumer).
- Team **slug == name** (all lowercase here), so membership/grant API calls use
  the name directly.
