---
name: slice
description: Run a MomentLens work slice (S-XX or P0-X) from docs/WorkSlices.md in stages, reading only the doc sections that slice cites and shipping it as a stack of PRs.
argument-hint: S-XX [schema|build <package>|done|cleanup]
disable-model-invocation: true
---

Run slice work for: $ARGUMENTS

The first word is the slice id. A second word picks the stage; with none, the stage is the read-back. The build stage takes a third word, the package: `api`, `mobile` or `worker`. If it is missing, ask which package; never pick one.

| Stage | Command | Runs sections | Ends at |
|---|---|---|---|
| Read-back | `/slice S-12` | 1, 2 | the slice card written to the issue, and the doc-fix PR if the read-back fixed docs |
| Schema | `/slice S-12 schema` | 3 | the schema PR open on the stack |
| Build | `/slice S-12 build api`, then `build mobile` | 4 | that package's PR open on the stack |
| Done | `/slice S-12 done` | 5 | every Definition of done item reported, the discussion log in the top PR, the review requested |
| Cleanup | `/slice S-12 cleanup` | 6 | the stack merged, the issue closed, the machine back on an up-to-date `main` |

**Each stage starts in a fresh session** (`/clear`). Two things cross from one stage to the next: the slice card in the slice's GitHub issue, which a person approved, and the stack's branches on GitHub. Never carry a stage's conversation into the next one (Handbook §18.8).

**No stage asks anyone to merge anything.** The slice ships as a stack of PRs that nobody merges until the done stage has finished and the stack has been reviewed.

These steps are the same for every developer and every agent. An agent tool that cannot run skills or subagents follows this file through the handoff template in `docs/WorkSlices.md`, doing the subagents' work itself.

Find the slice's issue once and reuse its number: `gh issue list --state all --search "<id> in:title" --json number,title,state`, the one whose title starts with `<id>:`.

## The stack

One branch and one PR for each stage that writes code or docs. Each branch is cut from the branch below it, and each PR targets that branch:

| Order | Branch | PR title | PR base |
|---|---|---|---|
| 1, only if the read-back fixed docs | `docs/<id>-rulings` | `<id>: doc fixes from the read-back` | `main` |
| 2 | `feat/<id>-schema` | `<id>: schema` | the branch below, or `main` |
| 3 on, one per package in the card's build order | `feat/<id>-<package>` | `<id>: <package>` | the branch below |

The id is lower case in branch names: `feat/s-12-schema`, `feat/s-12-api`.

- **Every stage starts with `git fetch origin`** and then cuts its branch from the one below: `git switch -c feat/s-12-api origin/feat/s-12-schema`. Only the bottom branch is cut from `origin/main`. If the branch below is not on GitHub, stop and say which stage has not run.
- **A rerun stage reuses its branch.** If the branch already exists, switch to it and carry on; never recreate it.
- **Push and open the PR at the end of the stage**: `git push -u origin <branch>`, then `gh pr create --base <branch below> --head <branch> --title "<title>" --body-file .slices/<id>/pr-<stage>.md`, with that file written to the sections of `.github/pull_request_template.md`. The bottom PR's body holds `Closes #<issue>`, because the bottom PR is the last one to reach `main`.
- **A fix that belongs lower in the stack goes lower.** If the api build finds the schema missing a field, stop and ask. The fix is a commit on the lowest branch it belongs to, and every branch above it is then rebased onto it (`git rebase origin/<branch below>`, then `git push --force-with-lease`). That is a force push, so it needs the developer's yes each time.
- **Work in the checkout the session starts in**, whether that is the developer's clone or a worktree the app made for the session. Never switch the branch of a checkout whose Metro is serving another branch (a listener on port 8081 or 8082); add a worktree instead, `git worktree add ../MomentLens-<id> <branch>`, and copy the two `.env` files into it.

Review and merging happen once, after the done stage, as Handbook §12 describes. GitHub requests the code owners' review on every PR from `.github/CODEOWNERS`, and `main` takes a PR only with a code-owner approval and a green CI run. A code owner's own stack needs green CI and `/code-review` instead. The stack merges from the top down with Rebase and merge, which keeps every commit.

**Check once per session whether the developer is a code owner** (D-117): they are when `gh api orgs/MomentLens/teams/maintainers/members -q '.[].login'` lists their login, `gh api user -q .login`. Several steps below differ for one. A code owner's merge to `main` uses `--admin`, which works only for a repository admin; if GitHub refuses it, treat the stack like anyone else's and ask a code owner to approve.

## Discussion log

The code owners read each slice's story in its final PR. A session's conversation is gone after `/clear`, so every stage writes down what mattered while it happens, not from memory at the end. Every slice keeps one, a code owner's own included (D-120).

Each stage keeps `.slices/<id>/discussion-<stage>.md` (the folder is gitignored) and adds to it as the conversation goes:

- The developer's instructions that steered the work, quoted word for word. Remove only secrets.
- Every question you asked and its answer, word for word.
- Every decision and who made it: the developer, Ukasha, or you as a routine call.
- What you tried and dropped, and why.
- Where the work departed from the card, and who agreed.
- What the developer reported from the phone or the dev server.
- Anything you pushed back on, and how it ended.

Never tool output, logs or code. The file opens with `## Discussion log: <stage>, <date>, <developer's GitHub login>` (`gh api user -q .login`). Before the stage ends, post it to the slice's issue with `gh issue comment <n> --body-file .slices/<id>/discussion-<stage>.md`. The done stage copies every one of them into the top PR.

## 1. Load the slice, not the docs

```
node scripts/doc.mjs slice <id>
```

It prints the phase's instructions where that phase has any, then the slice row with any warning paragraph written about it, then every section and decision the row cites, then the rows of the slices it depends on. A superseded or void decision is never expanded, only flagged.

**Read the phase paragraph first** when there is one. It carries what applies to every slice in the phase and to none of them in particular, which is where "build this with the verification check disabled, Phase 4 adds the gate" lives. It overrides the spec sections below it on purpose.

A section over 800 tokens with two or more subsections comes back as a menu of them with their sizes and the command to read one. `doc toc slices` marks a slice whose brief holds a menu with `+`. When a brief holds one, run the second command; the menu is not the content.

The brief ends with a line of ids one hop further out. Fetch one only when the brief says it matters: `doc D-55`.

Then, and only then:

1. **Check every dependency is finished.** A slice ships as a stack of PRs, so a merged PR with the id in its title proves nothing. The slice's issue closes when its stack reaches `main`. For each id in the "Depends on" column run `gh issue list --state all --search "<id> in:title" --json number,title,state` and read the issue whose title starts with `<id>:`. If it is open, stop and say which. If `gh` is missing or not logged in, ask. Never build against an interface you imagined.
2. Read the `AGENTS.md` of every package the slice touches.
3. Read `packages/shared-types`. Reuse a schema that exists. Never redeclare one.

**If `doc.mjs` is unavailable**, read the sections the slice row cites directly: every one is numbered, so `grep -n '^#### 4.11.4' docs/Idea.md` then `sed -n 'a,bp'`. Do not read a whole doc, and do not trust `grep -n '^#'` to find headings; it also matches a `#` comment inside a fenced code block. On Windows this needs Git Bash or WSL2.

## 2. Read the slice back before anything else

**Write nothing until this is done and the user has answered it.** Not a schema, not a file, not a test. This step exists to find what the docs get wrong about *this* slice while it is still cheap.

**Delegate the hunt when the brief is large.** The brief's header gives its size. Over about 1,500 tokens, start two subagents at once: `slice-auditor` with the slice id, which does items 4 and 5 below in its own context and returns findings, gaps, what it checked and the decisions needed; and the built-in `Explore` agent, asked what already exists in the code for each interface in the "Depends on" column, answering with paths and exported names only. Write items 1 to 3 while they run, use their reports for items 3 to 7, and check any finding you pass on against the ids it cites. Under about 1,500 tokens, do items 4 and 5 yourself: a small brief names few enough ids that the lookups cost less than a subagent does (Handbook §18.8).

This is an audit, not a summary. Do not open by praising the docs or restating the brief. Short sentences, complete lists: every item below is required, and "none" is only an answer if you say what you checked to reach it.

Produce these seven, in this order:

1. **What this slice is.** One paragraph in your own words: what someone can do when it is finished that they could not before. If you cannot write it without hedging, the brief is missing something; say what.
2. **How you would build it.** The shape, not the code. Tables and columns touched, endpoints, jobs, screens, and the order you would do them in. Name every file you would create or change, every dependency you would add (adding one is a decision, root `AGENTS.md`), and every negative test you will write: for each endpoint, another user, another event and the wrong role, plus a Do Not Publish subject and another viewer for anything that returns faces or images.
3. **What it inherits, and what it owes.** Read the row of every slice in the "Depends on" column and name the exact interface you build against: the schema in `packages/shared-types`, the endpoint, the column. If it does not exist yet, say so. Then run `node scripts/doc.mjs why <this slice>` and say which later slices read what you are about to write, and what that obliges you to get right now.
4. **Every edge case, by category.** Go through each of these and give at least one case, or say why the category cannot apply to this slice:
   - each role: Admin, Guest, Photographer, a pending member, a blocked member, a non-member
   - a Do Not Publish subject against every other viewer
   - offline, a retry, and the app killed between any two steps
   - two devices acting at once, one account or two people (an event has one Admin, D-102)
   - zero, one, the cap, and one past the cap (spec §4.17)
   - time: a sub-event starting, ending, running late, overlapping (spec §4.3)
   - a Realtime update arriving mid-action

   For each case, say what the docs say to do, citing the id, or say **"the docs do not say"**. Never fill a gap with a guess here; naming the gap is the work. Read the spec §5 subsections for this slice's area, whether or not the brief carries them; `doc spec §5` lists all six.
5. **What the docs get wrong.** Hunt, do not wait to notice. Do each of these and report what you found:
   - Look up every table, column, endpoint, job and R2 key the slice touches in `docs/ARCHITECTURE.md`, and compare it with how the spec and handbook sections in the brief describe it. Anything the API must do in one transaction has to go through a SQL function called with `rpc`, because supabase-js holds no transaction (D-95); flag any that the docs describe as two calls.
   - Compare every number in the brief (limits, sizes, radii, windows, thresholds) across every place it appears.
   - Check every cited `D-nn` for an "Amended" line or a later entry that changes it.
   - Check every rule in the brief against the numbered invariants in root `AGENTS.md`.

   Report each finding with the two ids that disagree, or one id and why it cannot work, plus the wording you propose. Then list what you checked and found consistent, so an empty findings list can be told apart from an unread brief.
6. **What this touches that fails silently.** The numbered invariants in root `AGENTS.md` and the human-read surfaces, by number, and the negative test that covers each one.
7. **What I need you to decide.** Every question above that only the team can answer, each with the option you recommend and what it costs.

Then **stop**. The user either says go or fixes the docs for this slice and the ones it depends on first. Log their answers word for word as they come.

**When the user has answered**, write the slice card into the issue's "Slice card" section, following the template there. `--body-file` replaces the whole body, so fetch it first: `gh issue view <n> --json body -q .body > .slices/<id>/issue.md`, replace only the Slice card section in that file, then `gh issue edit <n> --body-file .slices/<id>/issue.md`. It holds ids and paths, never copied doc text, and stays under about 900 tokens. Doc fixes the read-back turned up go on the bottom of the stack: branch `docs/<id>-rulings` from `origin/main`, pushed and opened as the stack's first PR. A doc fix that changes a decision needs a `D-nn` entry, and Ukasha rules on it in review. Then post the discussion log, and tell the user this stage is finished and the next is `/slice <id> schema` in a fresh session.

**The docs are a draft, not a contract.** They are written by the same agents that read them, and every review of them so far has found something wrong. If two sections disagree, or one describes something that cannot work, say so in step 5 and propose the wording. Do not bend the build to match a document, and do not invent a reading that makes a contradiction go away. Two things are different in kind: the numbered invariants in root `AGENTS.md` and the entries in `docs/DecisionLog.md` are decisions, not descriptions. Those you raise and the team rules on; you do not quietly build the other thing. `docs/ARCHITECTURE.md` wins over the spec and the handbook when they disagree (D-75), and it has been wrong too, so say when it is the one that looks wrong.

## 3. Schema

Load the card: `gh issue view <n> --json body`. `git fetch origin` and cut `feat/<id>-schema` from `origin/docs/<id>-rulings` if the read-back opened one, otherwise from `origin/main`. Read `packages/shared-types`. Write the zod schemas the card's "Produces" line names, and nothing else: every request, response and error shape the slice's endpoints use, following the paths, error body and status codes in Handbook §5.3. Run `pnpm typecheck`.

Commit, push, and open the PR `<id>: schema` on the stack. Do not wait for a review or a merge. Show the developer each exported schema name with its fields in a short list, since every later stage builds on that contract, then post the discussion log and tell them the next stage is `/slice <id> build <first package in the card>` in a fresh session.

## 4. Build

One package per session, in the card's build order: `/slice S-12 build api`, `/clear`, then `/slice S-12 build mobile`. Load the card, `git fetch origin`, and cut `feat/<id>-<package>` from the branch below it: the schema branch for the first package, the previous package's branch after that. If that branch is not on GitHub, stop and say which stage has not run. Read that package's `AGENTS.md`, the schema files the card names, by path, and the files you will change. Fetch a doc section only if the card lists its id.

**In the mobile build, ask for the screens once.** Before writing any screen, list the screens the card names and ask one question: do they have designs for these, as screenshots or Figma exports, or should you improvise? Never insist, and never ask twice. With no images, build every screen in the style of the screens already in `apps/mobile/src/features/`. With images for some screens, follow those and improvise the rest to match them. An image sets layout and direction; D-112 sets sizes and the spec sets behavior. The discussion log records which screens had an image and which were improvised, so the reviewer knows what to look at.

**The api build owns the card's migration**, if it has one. Create it with `pnpm exec supabase migration new <name>` and push it to the dev project when the tests or the phone need it, following Handbook §13.4 and asking first. Once pushed it is frozen: a change is a new migration.

1. Write each negative test the card lists for this package before the code it tests, run it, and watch it fail. Then write the code and watch it pass.
2. Run `slice-verifier` with the slice id, the package, the base (`origin/<the branch below>`), and the card's invariant numbers and negative tests. It runs the checks, keeps the full logs out of this session, and returns only failures.
3. Fix what it reports and run it again. After two failed rounds on the same failure, stop and ask the user; a third attempt means context is missing (Handbook §18.2).
4. When the verifier is clean, commit this package's work in small conventional commits.

Stay inside the package. Never edit `packages/shared-types`, `docs/` (the done stage writes any `ARCHITECTURE.md` change) or another package, and never add a dependency; if the card needs one of those, stop and ask. When the card is silent, wrong, or conflicts with a numbered invariant, ask the user rather than choosing a reading, and fix the card in the issue before building on the answer.

If the card says the slice touches the camera, GPS or the upload queue, ask the user to run it on a physical phone and report back, and log what they report. To try an API change on the phone before the stack merges, the developer deploys this branch to the dev server (Handbook §13.4); offer the commands, ask before running each, and remind them to put `main` back.

Push the branch and open `<id>: <package>` on the stack, naming the human-read surfaces the verifier listed. Post the discussion log. Tell the user the next stage: the next package in the card, or `/slice <id> done`.

## 5. Done

`git fetch origin` and check out the top branch of the stack. Run `slice-verifier` once more against the whole stack, with base `origin/main`. Then go through the Definition of done in `docs/WorkSlices.md` item by item. For each one say met or not met, with the evidence: the test name and file, the command and its result, or the reason it does not apply. Do not describe a slice as done while an item is unmet.

If `docs/ARCHITECTURE.md` needs an update, write it now as its own commit on the top branch, citing the D-entry or the merged code, and name it in that PR so the code owners approve it there (D-75, D-107). A code owner's own change needs no other approval. The build stages never edit `docs/`; only this stage and the read-back's doc-fix branch do.

Every PR in the stack names which of the four human-read surfaces it touches, or says it touches none. Fix any description that does not, with `gh pr edit <n> --body-file`.

**Put the discussion log in the top PR.** Collect every stage's log from the issue, `gh issue view <n> --json comments --jq '.comments[].body | select(startswith("## Discussion log"))'`, add this stage's own, and append them oldest first to the top PR's description inside a collapsed block:

```
<details>
<summary>Discussion log</summary>

(every stage's log, oldest first)

</details>
```

GitHub caps a description at 65,536 characters. If the logs would pass it, link each issue comment instead of copying it.

Post this stage's log to the issue, then tell the developer, and stop there:

1. The stack from bottom to top, each PR with its number and link.
2. **Review.** GitHub has already requested the code owners' review on every PR. Another developer's review is welcome and never required; if the developer wants one, give `gh pr edit <n> --add-reviewer <their GitHub login>` for each PR and offer to run it. **For a code owner's own stack** there is nobody to wait for: run `/code-review` on each PR, fix what it finds on the branch it belongs to, then record it on the PR with `gh pr comment <n> --body "/code-review ran: <n> findings, <what was fixed or why not>"`, and say the stack can merge once CI is green. An agent tool without `/code-review` reviews each diff against the numbered invariants itself, and says so in that comment.
3. How it lands: once every PR is approved, or for a code owner reviewed by `/code-review`, and green, it merges from the top down with Rebase and merge (Handbook §12). Folding the stack down drops the bottom PR's approval, so that PR needs approving once more before it reaches `main`. Then `/slice <id> cleanup` in a fresh session, which can do the merging too.

## 6. Cleanup

In a fresh session, once the stack is reviewed.

1. `git fetch --prune origin`, then list the slice's PRs: `gh pr list --state all --search "<id> in:title" --json number,title,state,headRefName,baseRefName,headRefOid,reviewDecision`.
2. **If any PR is still open**, and every open one is approved with green checks (`gh pr checks <n>`), list them top to bottom and offer to merge the stack. For a code owner's own stack, the `/code-review ran` comment on each PR stands in for the approval; a PR without one goes back to the done stage's review step. Merge only after the developer says yes, one PR at a time from the top: `gh pr merge <n> --rebase`, then `gh pr checks <next one down> --watch` until its checks pass, then the next. Folding the stack drops the bottom PR's approval: for anyone else's stack, stop there and ask the developer to get it approved again; for a code owner's, merge it with `gh pr merge <n> --rebase --admin`, which bypasses the review rule on `main` and never the CI rule. If GitHub cannot rebase one, stop and follow Handbook §12's conflict steps. If any open PR is not approved or not green, stop and say which, and what it waits on.
3. When the bottom PR has merged, check that the issue closed. If it is still open, close it with a comment listing the merged PRs.
4. **Check before deleting.** For each slice branch that exists locally, keep it and say why if its worktree has uncommitted changes (`git -C <path> status --porcelain`) or its tip is not the PR's `headRefOid`, which means commits that never reached GitHub.
5. Remove every worktree on a slice branch with `git worktree remove <path>`, never `--force`, then `git worktree prune`. If this session runs inside one of them, leave that one and tell the developer to remove it from their main clone afterwards. List any other worktree whose branch shows `gone` in `git branch -vv`, and offer to remove it the same way.
6. Delete the local slice branches with `git branch -D <branch>`. It has to be `-D`: Rebase and merge gives every commit a new id, so git cannot see that the branch merged. Step 4 is the check that replaces it.
7. **Bring `main` up to date** in the developer's main clone. If it is on a slice branch, `git switch main` first, unless Metro is serving it, in which case ask. Then `git pull --ff-only`. If `pnpm-lock.yaml` changed, run `pnpm install`. If `apps/mobile/package.json` or `apps/mobile/app.json` changed, tell the developer the development build may need a rebuild (Handbook §10).
8. **Put the dev server on `main`** if the stack touched `apps/api/`, `worker/` or `supabase/migrations/`, or its logs say a slice branch was deployed. Offer `ssh momentlens 'sudo bash /srv/momentlens/scripts/deploy.sh --branch main'` (Handbook §13.4) and run it only on a yes.
9. Delete `.slices/<id>/`.
10. Report what was removed, what was kept and why, and what the developer still has to do.
