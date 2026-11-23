---
name: branches-and-pull-requests
description: Branch naming (feature/, fix/, chore/), how labels and release notes follow from the branch, the pull request template, and how changes get merged in the template repository. Use when creating a branch, writing a commit or opening a pull request.
metadata:
  scope: repository
---

# Branches and pull requests

## The rule

Every change goes through a pull request against `main`. A branch ruleset rejects any branch name except `main`, `feature/...`, `fix/...`, `chore/...` and `dependabot/...`. The prefix sets the release notes label automatically (`.github/labeler.yml`), and `.github/release.yml` groups the generated notes by label. The maintainer reviews and squash-merges; nobody merges their own pull request.

One pull request per completed feature, which tracks to one issue: the issue is cut at the size of the pull request worth reviewing. A decision made partway through a feature goes on that feature's branch, not a new pull request. A small, unrelated fix gets its own `fix/` branch.

| Prefix | For | Label | Release notes section |
| --- | --- | --- | --- |
| `feature/` | Something new for users of the template | `enhancement` | New features |
| `fix/` | Something that was wrong | `bug` | Bug fixes |
| `chore/` | Tidying, dependencies, docs, pipeline | none from the name | Other changes |

Changed files add labels too: `.github/**`, `Dockerfile` or `docker-compose.yml` add `build`; a change made only of Markdown or `docs/` adds `documentation`. Add `breaking-change` by hand when generated solutions or template options change in a way users will notice.

## Where we track work

`AGENTS.md` ships with "Where we track work" not set, because it's for the teams who use the template. In the template repository itself, plans and handoffs live in issues in [LeanMeanCleanApps/.github](https://github.com/LeanMeanCleanApps/.github/issues), on the Lean Mean Clean templates project. The `planning` skill in that repository has the details. Don't fill in the line in `AGENTS.md` here.

## Steps

1. Branch from an up-to-date `main`: `git switch -c fix/review-validation`. Short, lowercase, hyphenated.
2. Write commit messages as a sentence about the change, in the imperative: "Validate the star rating on update".
3. Open the pull request and fill in `.github/pull_request_template.md`: a two or three sentence summary, the linked issue (`Part of` or `Closes LeanMeanCleanApps/.github#<number>`), the type of change, and whether the shared layers are touched.
4. If shared layers, skills or repository setup changed, say so; the same change has to go to all five templates (`family-sync`).
5. Wait for every required check (`ci-pipeline`). Fix failures with new commits; don't force-push over review comments.

## Don't

- Push to `main`, or use any other branch prefix.
- Merge your own pull request.
- Bundle unrelated changes; they're easier to review apart.
- Add AI attribution lines or tool footers to pull request descriptions.

## Check

The labels appear on the pull request a few seconds after it opens, and every required check is green.
