---
name: website-team-setup
description: >
  Turn a one-owner new-website repo into one several people and AI assistants
  (Codex, Claude Code) can work on at once without overwriting each other: invite
  collaborators, set the repo settings, prove the CI workflow starts on its own
  (the fix for a silent one is bundled), block direct pushes to `main`, connect
  Cloudflare Pages to GitHub without the known traps, write rights, merge rule and
  who publishes live into `AGENTS.md`, hand the team a one-page guide. Run once,
  when a second person joins. Use it whenever the user mentions a colleague, client
  or second assistant joining a site repo, inviting someone to GitHub, "Update
  branch", pull requests not running CI, or connecting Cloudflare to the repo, even
  without the word "team". Trigger phrases: "set up the team", "my colleague will
  work on the site", "invite a collaborator", "block pushes to main", "CI is not
  running on pull requests".
---

# Website team setup — from one owner to a team, once

`new-website` scaffolds every site with an `AGENTS.md` (the working rules: fetch the
latest state first, pull request instead of a direct push, when a merge is allowed,
never invent facts, the new-page checklist) and a `CLAUDE.md` that imports it. Those
rules already work for one person. This skill does the part that only a **team** needs,
in the order we had to do it on a real site, with the traps we hit written in.

> **Human-in-the-loop.** Inviting people, accepting invitations, the Cloudflare
> dashboard, and any plan-dependent GitHub setting are the owner's clicks. You draft
> every value and run every command that `gh` can run; you never handle the owner's
> credentials or 2FA, and never drive a dashboard through blind screen control.

> **Language.** Talk to the owner in their language. `AGENTS.md` stays English on every
> site, like the skills: agents read it, and its Language rule has them reply in the
> person's language. `TEAM-GUIDE.md` is for people: translate it in-session when the
> team's language is not English (rules and commands intact), as `new-website` does
> for `PUBLISHING.md`.

Prerequisites: the site is on GitHub with `.github/workflows/ci.yml` from the kit, and
`AGENTS.md` exists. If it does not (a site scaffolded before the template existed),
copy `new-website/templates/AGENTS.md` + `templates/CLAUDE.md` in first and fill the
`[BRACKET]` slots per the note at its top, then continue here. Claude Code sites also
need the sync hook that `AGENTS.md` §1 relies on: if `.claude/hooks/git-stand.mjs` is
missing, copy it from `new-website/templates/claude/hooks/` and merge the `hooks` block of
`new-website/templates/claude/settings.json` into the site's `.claude/settings.json`.

Work on a branch and finish with a pull request — the rule the setup installs applies
to the setup itself. Say in the pull request that it touches `scripts/` (the hook) and
`AGENTS.md`.

## 1. Decide with the owner first (five questions)

Ask, one at a time, offer the options, record the answers — they feed §§2, 7, 8:

1. **Who joins?** GitHub usernames of the collaborators (they need accounts first; a
   free account is enough).
2. **Rights level** for collaborators, written into `AGENTS.md` §5:
   **content** (texts, images, collection entries) · **content + design** (also
   navigation, components, layouts, styles, existing pages, `src/config.ts`,
   `BRAND.md`) ·
   **everything** the owner may change (also new pages, tests, scripts, CI, settings).
   The reference site started at "content" and widened to "everything" within a day;
   pick what fits now, it is one line to change later. If only the owner publishes
   (Q4), say that "everything" includes `ship.sh`, the hook and the CI file, which a
   collaborator could then change and merge.
3. **Merge rule.** Default and recommended: a collaborator merges their **own** pull
   request when the checks are green, no placeholders remain and it is not a draft;
   other people's pull requests only after asking. Alternative: the owner merges
   everything. Lands in `AGENTS.md` §5 (the "Merge rule" line) and in the guide's
   Merge row.
4. **Who publishes live** — two-stage sites only (`main` = preview, `production` =
   live, `npm run ship`). Offer **owner only** as the default, or **every
   collaborator**. Single-stage sites skip this: a merge is live there, and the merge
   rule is the whole gate.
5. **How will they work?** Codex in the browser (nothing to install; GitHub connection
   in Codex), Codex or Claude Code locally (needs `SETUP.md`'s tools), or both. Decides
   what `TEAM-GUIDE.md` (§8) says.

## 2. Invite the collaborators

```bash
OWNER=<github-owner>; REPO=<repo>
# On a personal-account repo a collaborator always gets write access (push branches,
# open/merge pull requests; not admin): GitHub has no other level there, and the API's
# `permission` field applies to organization repos only.
gh api -X PUT "repos/$OWNER/$REPO/collaborators/<username>"
gh api "repos/$OWNER/$REPO/invitations" --jq '.[] | "\(.invitee.login) \(.permissions) pending"'
```
Dashboard path: repo → **Settings → Collaborators → Add people**. The invitee gets an
email and must **accept** it; until then `collaborators` does not list them. Tell the
owner to ask for the acceptance and re-check before assuming anyone can push:
`gh api "repos/$OWNER/$REPO/collaborators" --jq '.[].login'`.

Re-run safe: an existing collaborator is a no-op; a pending invitation is listed, not
duplicated.

## 3. Repository settings (one command)

```bash
gh repo edit "$OWNER/$REPO" --allow-update-branch --delete-branch-on-merge
gh api "repos/$OWNER/$REPO" --jq '{allow_update_branch, delete_branch_on_merge}'
```
- **`allow_update_branch`** shows the **"Update branch"** button on every pull request
  that is behind `main`. This is what makes "a second person opens a pull request while
  the first one merges" a one-click situation instead of a git lesson: press it, CI
  runs again on the merged state, then merge. Required: with a ruleset that demands
  up-to-date branches (§5) GitHub refuses to merge a stale one otherwise.
- **`delete_branch_on_merge`** removes the head branch after a merge, so the branch
  list stays readable for people who never learned to prune. GitHub never deletes a
  *base* branch, so `production` is safe. Pair it with `git config --global
  fetch.prune true` on each machine (`SETUP.md` §3 says so).

Dashboard path: **Settings → General → Pull Requests** → tick both.

### 3b. The remaining settings — what a clean team setup looks like on a personal-account repo

None of these blocks a team; each removes a trap we either hit or saw coming. Read
the current value first, change only what differs, and say what you changed.

| Setting | Set it to | Why | How |
|---|---|---|---|
| **Merge method** | one method only; keep **merge commits**, turn off rebase (squash is fine if the owner prefers one commit per pull request) | Rebase-merging rewrites the collaborators' commits, so the SHAs in their clones no longer match GitHub's, and the "Update branch" button then produces conflicts. One method means the button labels never change under a non-technical user. | `gh repo edit --enable-rebase-merge=false` (add `--enable-squash-merge=false` to keep merge commits only) |
| **Auto-merge** | **off** | "Enable auto-merge" merges the moment CI turns green, skipping the preview look that `AGENTS.md` §2 requires. | `gh repo edit --enable-auto-merge=false` |
| **Collaborator permission** | **write**, never maintain or admin | Write can push branches, open and merge pull requests; admin could change the settings this skill sets, or delete the repo. | §2 |
| **Visibility** | **private** (client work) | A public repo exposes drafts, `"[MISSING: …]"` placeholders and client photos before they are meant to be seen. Note: this is also what decides whether §5-A's ruleset is available for free. | `gh repo view --json visibility` |
| **Actions permissions** | **Allow all**, or narrow to **GitHub-owned and verified** | The kit's `ci.yml` uses only `actions/checkout` and `actions/setup-node`, so the narrow setting costs nothing and stops a collaborator's future workflow pulling an unvetted action. | Settings → Actions → General |
| **Actions minutes** (private repos) | know the budget: 2 000 free minutes/month on GitHub Free; the repo's **Actions** tab shows what each run takes. With **no payment method** on the account, GitHub blocks Actions once they are used up and charges nothing. **A $0 Actions budget with Stop usage already on the account blocks private-repo jobs the same way, payment method or not**, with a message that reads like a failed payment ("recent account payments have failed or your spending limit needs to be increased") and jobs that start zero steps. Check **Budgets and alerts** for an existing **Actions** budget. If the owner wants CI to keep running past the free minutes, edit it to a small cap they choose (say $10) with **Stop usage when budget limit is reached** kept on; create one only if none is there. Do not pick the "Copilot AI Credits" budget, a different product that the list may show first. Whether CI starts again after the change is confirmed only by the next push ([GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [budgets](https://docs.github.com/en/billing/how-tos/set-up-budgets)) | Every push to a pull request or to `main` starts a run, and the minutes add up; at the limit CI either starts costing money or silently stops, and then "green before merge" stops meaning anything. The `concurrency` block in the kit's `ci.yml` cancels a superseded run on the same branch, so a quick second push stops the first run instead of letting it finish. | https://github.com/settings/billing → **Budgets and alerts**; usage on the same billing pages |
| **Fork workflows** | leave the default (require approval for first-time contributors) | Collaborators push branches, not forks, so this never triggers for them; it only guards against a stranger's fork running CI on your minutes. | Settings → Actions → General |
| **Workflow token** | leave **read-only** (default) | The kit's CI writes nothing to the repo. | Settings → Actions → General |
| **Dependabot** | **security updates on**; version updates off unless the owner wants weekly dependency pull requests | Security updates arrive as ordinary pull requests that CI checks; version updates are noise for a non-technical team. | Settings → Code security |
| **Secret scanning + push protection** | **on** where the plan offers it (free on public repos; paid on private) | Catches a token pasted into a commit before it lands; the kit's `.gitignore` is the backstop either way. | Settings → Code security |
| **`production` branch** (two-stage) | protect against **deletion and force-push only** — no pull-request rule | `npm run ship` pushes `main:production` directly (a fast-forward push); a pull-request rule on `production` would break it. Rulesets need a public repo or a paid plan: on a free private repo this one is refused like §5-A's, and `production` has no server-side protection at all. Where rulesets are available, GitHub documents a **Restrict updates** rule (only bypass actors may push) and lists the repository admin role as a bypass actor, which would make "who may ship" (§1 Q4) enforced; this is not yet tested on a real site, so until it is, "who may ship" stays a written rule in `AGENTS.md`. | second ruleset, §5-A shape with only the `deletion` and `non_fast_forward` rules, `include: ["refs/heads/production"]` |
| **Cloudflare GitHub App** | access to **this repo only** | The app gets read access to every repo it is granted; least privilege. | GitHub → Settings → Applications → Cloudflare Workers and Pages → Configure (see §6.2) |
| **2FA** | recommended, not required: each collaborator turns on two-factor sign-in and adds a passkey | The website is the owner's, and anyone who gets into a collaborator's account can change it, so recommend it to each collaborator in those words. Never make it a condition: a personal-account repo cannot require it (only organizations can), and GitHub itself requires it only for some accounts (it tells those by email and on the site). Do not count on GitHub prompting a collaborator who only edits content; `TEAM-GUIDE.md` gives them the link. There is nothing to check from your side: `gh api users/<login>` shows nothing about 2FA, and GitHub documents no 2FA marker on Settings → Collaborators for a personal-account repo, so if the owner wants to know, ask. | the collaborator, at https://github.com/settings/security |
| **Watching** | each collaborator watches the repo (at least "Participating and @mentions", the default) | Otherwise nobody sees a review comment or a failed check on their pull request. | the "Watch" button on the repo |

Skipped on purpose: CODEOWNERS with required code-owner review (needs the paid
ruleset option on private repos and adds a review step the team did not ask for);
merge queues (paid); organization-level policies (this skill targets a repo on a
personal account — an organization owner has the equivalent settings under the
organization).

## 4. Prove that CI starts on its own (do not skip)

On the reference site the kit's workflow file had been on `main` for three weeks and
**had never run**: pushes to `main` produced no run at all, so "green checks before
merging" was an empty rule. What got it going was one manual start followed by a
throwaway pull request; afterwards every push and pull request ran normally. The root
cause was not pinned down (Actions permissions looked normal), so this skill does not
claim to prevent it — it **checks**, and if the check fails it does what worked:

```bash
# a) Are Actions allowed at all?
gh api "repos/$OWNER/$REPO/actions/permissions" --jq '{enabled, allowed_actions}'
# b) Is the workflow listed, and active (not disabled_manually / disabled_inactivity)?
gh workflow list --all
gh workflow enable ci.yml           # only if it shows as disabled
# c) Has it EVER run on a pull_request event? (push runs prove the file works, not the
#    trigger the merge gate relies on — a workflow whose pull_request trigger is broken
#    still shows green push runs on main)
gh run list --workflow ci.yml --event pull_request --limit 5
gh run list --workflow ci.yml --limit 5          # any run at all?
```
- (a) `enabled: false` → the owner turns it on: **Settings → Actions → General → Allow
  all actions**. GitHub also disables scheduled workflows after 60 days without repo
  activity; that does not apply to push/pull_request triggers, but a manually disabled
  workflow stays disabled until enabled.
- (c) no `pull_request` run → the throwaway pull request (step 2 below) is the
  proof; do step 1 as well when there is no run of any kind:
  ```bash
  gh workflow run ci.yml --ref main                        # 1. one manual start
  sleep 15   # the run takes a few seconds to appear; `gh run watch` needs its id
  id=$(gh run list --workflow ci.yml --event workflow_dispatch --limit 1 \
       --json databaseId --jq '.[0].databaseId')
  gh run watch "$id" --exit-status
  git switch --no-track -c ci/trigger-test origin/main      # 2. throwaway pull request
  git commit --allow-empty -m "CI trigger test (will be closed)"
  git push -u origin ci/trigger-test
  gh pr create --title "CI trigger test (will be closed)" \
     --body "Empty commit; only checks whether pull_request triggers CI."
  sleep 20   # the first check run takes a moment to be reported; too early = "no checks reported"
  gh pr checks ci/trigger-test --watch
  ```
  A run with `event: pull_request` must appear:
  `gh run list --workflow ci.yml --branch ci/trigger-test --event pull_request`.
  Then close the pull request and delete the branch:
  `gh pr close ci/trigger-test --delete-branch`.
  The first manual run may be **red** for a real reason (a type error nobody had seen
  because the suite never ran in CI) — that is a finding, not a trigger problem; fix it
  in its own pull request.
- Still nothing after both steps → stop and report; do not declare CI working. A team
  merging on "green" that never runs is worse than no rule.

While the throwaway pull request is open, look at its check list: if Cloudflare is
already connected (§6), it also proves "no leftover Workers Builds check" — see §6.2.
If Cloudflare is connected later, §6.2 opens a second one.

## 5. Block direct pushes to `main`

Two mechanisms, chosen by what the plan allows. Try the server-side one first: it is
the only one nobody can bypass.

**A. Ruleset (public repo, or private repo on a paid plan).** Pull request required,
the CI job required to pass on an up-to-date branch, no force push, no deletion.
`test` is the job id in the kit's `ci.yml`; use the job's `name:` instead if one is set.

```bash
# Re-run safe: create only if no ruleset of that name exists yet.
gh api "repos/$OWNER/$REPO/rulesets" --jq 'map(select(.name=="protect main")) | length'
# 0 → create:
gh api -X POST "repos/$OWNER/$REPO/rulesets" --input - <<'JSON'
{
  "name": "protect main",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [],
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "pull_request",
      "parameters": { "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false, "require_code_owner_review": false,
        "require_last_push_approval": false, "required_review_thread_resolution": false } },
    { "type": "required_status_checks",
      "parameters": { "strict_required_status_checks_policy": true,
        "required_status_checks": [ { "context": "test" } ] } }
  ]
}
JSON
gh api "repos/$OWNER/$REPO/rulesets" --jq '.[] | "\(.name) \(.enforcement)"'
```
**A ruleset that already exists is not proof.** A "protect main" left behind by an
earlier attempt, or edited in the dashboard since, may be looser than the one above
(a different check name, no up-to-date requirement, a bypass actor). So when the count
is not 0, read every one of them back (leftovers come in twos) and compare each with
the JSON above, rule by rule:
```bash
for id in $(gh api "repos/$OWNER/$REPO/rulesets" --jq '.[] | select(.name=="protect main") | .id'); do
  echo "== ruleset $id"
  gh api "repos/$OWNER/$REPO/rulesets/$id" \
     --jq '{enforcement, bypass_actors, conditions, rules: [.rules[] | {type, parameters}]}'
done
```
Anything that differs — `enforcement` not `active`, a non-empty `bypass_actors`, a
missing rule, `strict_required_status_checks_policy` false, a `context` that is not the
CI job's name — is fixed with `gh api -X PUT "repos/$OWNER/$REPO/rulesets/$id" --input -`
and the same JSON body (it carries `"bypass_actors": []` explicitly, so a bypass list
is cleared rather than left as GitHub found it). Read it back once more after the PUT.
Two rulesets of that name: bring one in line, then delete the other with the owner's
go-ahead (`gh api -X DELETE "repos/$OWNER/$REPO/rulesets/<other id>"`) — two rulesets
on the same branch both apply, and the looser one still blocks nothing. Confirm the
`context` against the job in `ci.yml` (`test` unless the site renamed it); a wrong
name blocks every merge, because a check that never reports never passes.

No bypass list: the rule applies to the owner too, which is the point. Dashboard
path: **Settings → Rules → Rulesets → New branch ruleset**. An approving review count of
0 keeps the gate "green CI + a human decided to merge", matching §1's merge rule; raise it
only if the owner wants a second pair of eyes on every change.

**B. The refusal.** On a **private repo on a free plan** the request comes back
`403` with an "upgrade" message: GitHub offers no server-side branch protection
there. Say so plainly, then enable the local guard the kit already ships:
`scripts/hooks/pre-push` contains a commented-out **PR-only main** block (the six
lines from `while read` to `done`, marked OPTIONAL). First read the current state —
re-runs must not edit twice, and a site scaffolded before the block existed has no
block to uncomment at all:
```bash
grep -n '^while read -r _lref' scripts/hooks/pre-push && echo "already enabled"
grep -Eq '^(# )?while read -r _lref' scripts/hooks/pre-push || echo "no block in this hook — older kit; merge the kit's templates/astro/scripts/hooks/pre-push in first"
```
The second grep looks for the block's own first line, commented out or not — not for
the `ALLOW_MAIN_PUSH` word, which the prose comment above the block also contains.
No block (the second line fires): bring the site's hook up to the kit's
`templates/astro/scripts/hooks/pre-push` **by hand** in the setup pull request, the
way `whats-new.sh` treats every drift-tracked file (it reports the hook, never
rewrites it — same as `ci.yml` in §6.8). Diff the two first: on a stock hook they
differ by four additions — the stdin capture, the block, the deletion-only skip and
the publish-classifier step — and the order matters: the skip sits below the block,
or a push deleting `main` gets past it; the capture sits above both, or the skip
never fires. A site
that added a step of its own keeps it. Re-stamp afterwards, as for any hand-merged tracked
file. Then continue. Found this on the first real site the skill ran on: its hook
predated the block.
If it is not enabled: remove the leading `# ` from those six lines and replace only
the first sentence of the comment above them ("OPTIONAL: PR-only main flow …") with
the date and why it is on — keep the rest of that comment: it says why the block must
stay above the build steps. The hook's comments, its header and this one, are the
**source of truth for what bypasses the block**: `ALLOW_MAIN_PUSH=1`, the deliberate
override (above the block); `git push --no-verify` and unsetting `core.hooksPath`
(header); a clone that never ran `npm install`, since the `prepare` script is what
wires the hook; and a site that is not the root of its git repo, where `prepare` leaves
the hook unwired. Commit that in the setup pull request. Then
tell the owner, and write into `AGENTS.md` §2, what it is: a **local convention**,
with the bypasses quoted from the hook's comments, not from memory. `PUBLISHING.md`
tells the owner to push to `main` directly (to publish on a single-stage site, to
update the preview on a two-stage one), which the block now refuses: in the setup pull
request, point those steps at a pull request, with `ALLOW_MAIN_PUSH=1` named as the
owner's deliberate exception. It does not touch
`npm run ship` (which pushes `main:production`), nor GitHub's own merges, nor Codex
in the cloud (which only ever creates pull requests). It is the best a free private
repo gets, and it is enough when everyone follows `AGENTS.md`.

**Verify — and not with a no-op push.** `git push origin main` with nothing to push
hands the hook nothing and sends GitHub nothing ("Everything up-to-date"), so it
"passes" both mechanisms without testing either. Instead:
```bash
# Ruleset (§5-A): read the effective rules back — must list pull_request and
# required_status_checks. A dry-run push never reaches GitHub's rules, so this
# read-back is the whole verification on a ruleset site.
gh api "repos/$OWNER/$REPO/rules/branches/main" --jq '.[].type'

# Hook (§5-B ONLY — on a ruleset site the hook is off by design and this would
# print "NOT blocked"): a dry run of a real ref update — the hook runs, nothing is
# transferred. Branch from the SETUP branch, not origin/main: git runs the hook from
# the checked-out files, and until the setup pull request merges, origin/main still
# has the block commented out, so a check from there always says "NOT blocked".
git switch --no-track -c setup/push-check setup/team   # the setup branch, block enabled
git commit --allow-empty -m "push-block check (never pushed)"
# The push is EXPECTED to fail, so test it as a condition — in a script run under
# `set -e` a bare failing push would abort before the cleanup line runs. Only the
# hook's own message counts as "blocked": a push can fail for other reasons.
if out="$(git push --dry-run origin HEAD:main 2>&1)"; then
  echo "NOT blocked — the hook is not active in this clone (npm install run? hooksPath set? site at the root of its repo?)"
elif grep -qF "Direct push to 'main' blocked" <<<"$out"; then
  echo "blocked as expected"
else
  echo "push failed for another reason — read it: $out"
fi
git switch - && git branch -D setup/push-check
```

## 6. Cloudflare: connect the repo to GitHub — with the traps

`new-website/references/CLOUDFLARE_FIRST_DEPLOY.md` has the bootstrap paths; a team
wants a project connected to GitHub (push-to-deploy, one preview address per pull
request). The setup script there ("S") makes one through Cloudflare's API, with the
build command and output folder of item 4 (no framework preset, which the build does not
need) and the production branch of item 5; from the owner's browser it needs a short-lived
token and the GitHub app's access to the repository; it does not create the `production`
branch (item 5) or touch the checks of items 2 and 8. By hand it is **B, git
integration**: walk the owner through it with these warnings ahead of each click:

1. **Pages, not Workers.** In the Cloudflare dashboard, **Workers & Pages → Create**
   opens on the **Workers** tab, and its "Import a repository" creates a **Worker**
   with *Workers Builds* — the wrong project type for this kit. Switch to the **Pages**
   tab first, then **Connect to Git**. (Same failure class as the `wrangler deploy` vs
   `wrangler pages deploy` mix-up in the deploy reference: if the result has a
   `*.workers.dev` address, it is the wrong type.)
2. **A Worker made by mistake leaves a check behind.** If step 1 went wrong once,
   deleting the Worker is not enough: its build connection keeps posting a **"Workers
   Builds"** check on every pull request (pending or failing forever). Remove the
   connection on the Worker (**Settings → Builds → disconnect**, or delete the Worker
   after disconnecting), then prove it is gone: open a throwaway pull request **after**
   connecting (the §4 recipe: empty commit, close and delete afterwards) — it must
   show only the **CI** check and the **Cloudflare Pages** preview check. If the
   Workers check is still there, the GitHub App installation still carries the
   trigger: GitHub → **Settings → Applications → Cloudflare Workers and Pages →
   Configure** → check which repos it may access, and remove and re-add the repo if
   needed.
3. **The project name is global.** `<name>.pages.dev` is one namespace across all
   Cloudflare accounts, so the obvious name may be taken with no explanation beyond a
   validation error. Pick a short alternative; it only changes the preview address.
   That address is the one Cloudflare gives the project, which is not always the name
   followed by `.pages.dev`: read it on the project's page (or in the setup script's
   report). Whatever it ends up being, write it into `AGENTS.md` (header + §2), `PUBLISHING.md`
   and the README's deploy section, and search the repo for the old one
   (`git grep -n '<old-name>.pages.dev'`, a site may have it in `src/config.ts`), so
   nobody quotes a preview address that does not exist.
4. **Build settings.** Framework preset **Astro**, build command `npm run build`,
   output directory `dist`. Node version comes from the repo's `.nvmrc`.
5. **Production branch = the publish model.** Two-stage: **`production`** (create the
   branch first if it does not exist yet, see `new-website` §4), so `main` stays the
   noindexed preview. Single-stage: `main` — and then set `PROD_BRANCH = 'main'` in
   `src/config.ts` in the setup pull request (the kit ships `'production'`), because
   analytics, once switched on, fires only when the two agree, silently never
   otherwise. `AGENTS.md` §2 must keep the block that matches (the other one is
   deleted at scaffold time — check it was).
6. **Pull request previews.** Once connected, every pull request gets its own preview
   address in its checks ("Cloudflare Pages" → *View deployment*), plus the stable
   alias `<branch>.<project>.pages.dev`. `AGENTS.md` §2 tells collaborators to look
   there before merging. Previews are noindexed by the kit's `functions/_middleware.ts`
   but public-by-URL (see `PUBLISHING.md`).
7. **Single-stage sites: a merge publishes.** Anything that runs only in
   `npm run ship` on this site must now run in CI, or it never runs. The kit's own
   `ship.sh` runs no tests (the pre-push hook and CI do), so a stock site has nothing
   to move; a site that added a ship-only gate of its own moves that command into
   `ci.yml` in the setup pull request.
8. **Placeholder gate — check the site actually has it.** The kit's `ci.yml` greps
   `src/` and `public/` for `"[MISSING: …]"` before the build, but only sites
   scaffolded after that step existed carry it: `whats-new.sh` reports drift in
   `ci.yml`, it never rewrites it. So `AGENTS.md`'s merge rule ("no placeholder is
   left") is enforced only if the step is there. First find out which **token** this
   site uses: `AGENTS.md` §4 names it, and a site with non-English content may use its own word
   (a German site might write `"[FEHLT: …]"`); the kit's step greps for `[MISSING:`
   and matches nothing else. Then check for the step itself — its `grep -rnI` line,
   not any mention of the word in a comment — add it if missing with the site's
   token in the pattern, and prove it fires before calling the setup done:
   ```bash
   grep -nF "grep -rnI" .github/workflows/ci.yml \
     || echo "placeholder step missing — copy it from the kit's templates/astro/.github/workflows/ci.yml and put this site's token in the pattern"
   ```
   Then plant one: a scratch branch with the site's own token (`"[MISSING: probe]"`,
   or `"[FEHLT: probe]"` on that German site) in any page, push it and open a **draft**
   pull request from it (the kit's CI runs on pushes only for `main` and `production`,
   so a pushed branch alone starts no check), watch the check turn red **at the step
   `No unfilled "[MISSING:" placeholders`**, then close the pull request and delete the
   branch. Red only later, at `npm test`, is `tests/placeholders.spec.ts` speaking: the
   grep step is missing or greps for another word. A push the hook refuses means the
   site's token is not the one in that spec's `DRAFT_TOKEN`; set it there too. A gate that has never fired is a hypothesis, and a gate
   probed with the wrong token proves the wrong thing.
9. **Direct-upload project already exists (deploy path A).** A git-connected Pages
   project is a *different project type*; Cloudflare cannot convert one into the
   other. Create the git-connected project under a new name, let it build once,
   then move the custom domain: remove it from the old project first (a domain can
   be attached to one Pages project at a time), attach it to the new one (Custom
   domains → Set up a domain), wait for it to show Active, and only then delete the
   old project. Do it in a quiet moment and check the live domain right after, with
   a cache-bust (`PUBLISHING.md` § "For AI assistants"). This sequence follows
   Cloudflare's documented behaviour and was not exercised on the reference site,
   which was git-connected from the start.

Verify: after the first merge, `<live-or-preview-url>/build.txt` shows the merge
commit id (the kit's build marker). Say which address is the **preview** and which is
**live** every time you quote one (`PUBLISHING.md` § "For AI assistants").

## 7. Rights and publish rights in `AGENTS.md`

Rewrite the four lines at the top of §5 from the §1 answers: collaborators (GitHub
usernames only, no emails), rights level, merge rule, and who publishes live
(two-stage) — or delete the publish line on a single-stage site. If §5-B enabled the
hook, add one sentence to §2 saying the block is local, with the bypasses quoted
from the hook's own comment block (§5-B). If §2 still says "The assistant never
merges" (a site scaffolded before the assistant could merge on request), replace that
bullet with the template's "Merging" bullet, or the guide in §8 promises what
`AGENTS.md` forbids. Read the whole
file once more: no `[BRACKET]` slot and no scaffold note may remain, and the publish
model block must match Cloudflare's production branch (§6.5).

## 8. The collaborators' guide

Copy `templates/TEAM-GUIDE.md` from this skill into the repo root as `TEAM-GUIDE.md`,
keep the part(s) that match §1's answer 5 (browser / local / both), fill every
`[BRACKET]` slot — site name, owner/repo, the owner's name for "who to ask" (a name,
never an email), the merge step in the numbered instructions and the Merge row
(`[MERGE_STEP]`, `[MERGE_RULE]`, both from §1 answer 3), and the "what merge does"
line (`[MERGE_MEANS]` with `[PREVIEW_URL]`, `[LIVE_URL]`, `[SHIP_RIGHTS]` from
answer 4; single-stage sites keep the "goes live" half) — and translate if the team's
language is not English. It is deliberately one page: where to start, the four moves
per task, when to ask.

## 9. Hand over

- Open the setup pull request (branch `setup/team`), describe in plain words: who was
  invited, which settings are on, how CI was proven, which push block is active and
  what it covers, the Cloudflare project and its addresses, the rights level, the
  publish rule. Note the `scripts/` and `AGENTS.md` changes explicitly (`AGENTS.md` §5).
- The owner merges it per the new rule, on GitHub or by telling the assistant to (this
  skill does not merge it unasked), then tells the
  collaborators to accept the invitation and read
  `TEAM-GUIDE.md`. Their first task: something small, so the whole loop (fetch, branch,
  pull request, green checks, preview, merge) is exercised once with the owner around.

Re-running the skill is safe: every step reports the current state before changing
anything, and none of §§2–6 creates a second copy of what exists.
