---
name: sync-to-azure
description: >-
  Syncs the current Power Apps Code App to the Fernand Gilbert Ltée Azure DevOps repo under
  code-apps/<app-name>/. Use for "push to company", "sync to azure", "push to FGL", "envoyer dans
  le repo de la compagnie", or when a finished feature should be shared with the team.
disable-model-invocation: true
---

# Sync Code App to Azure DevOps

Syncs the current working directory to `code-apps/<app-name>/` in the Fernand Gilbert Ltée
Azure DevOps repository. Does **not** build — syncs source as-is. Cross-platform: uses
`rsync` on macOS/Linux and `robocopy` on Windows/Git Bash.

**Excluded from sync** — dirs: `.claude/`, `.agents/`, `.codex/`, `.git/`, `node_modules/`,
`dist/`, `docs/`; files: `CLAUDE.md`, `AGENTS.md`, `*.local`, `.env*`.

> **Safety property:** the script commits **only inside the Azure mirror** at
> `~/.fgl-azure/repo`. It never creates a commit in the user's own project repo, on any
> branch. Syncing therefore cannot move one branch's work onto another.

---

## Which branch gets synced

The sync copies the **working tree as it is on disk**, i.e. whatever branch is currently
checked out. To sync a **different** branch (e.g. `master` instead of a feature/loop branch):

1. Confirm the working tree is **clean** (`git status --porcelain` empty). If not, stop and
   ask the user — never stash/commit on their behalf to force it.
2. `git checkout <branch>` (a plain checkout — **never** `merge`/`rebase`; switching branches
   does not move the previous branch's commits anywhere).
3. Run the sync (see below).
4. `git checkout <original-branch>` to return the user where they were.

Always switch back to the branch the user started on once the sync is done.

---

## PAT Setup (automatic)

On the **first run**, the script prompts for your Personal Access Token and saves it to
`~/.fgl-azure/.pat` (chmod 600 — readable only by you). You will never be prompted again.
The prompt is interactive (`read -s`) — if there's no TTY, the user must run that first run
themselves in their terminal, or pre-create `~/.fgl-azure/.pat`.

To create a PAT: Azure DevOps → profile picture (top right) → **Personal access tokens**
→ **New Token** → Scopes: **Code → Read & Write**.

> To reset the PAT (e.g. after expiry): `rm ~/.fgl-azure/.pat` then re-run the script.

---

## Commit message — must MEAN something to a colleague

The company Azure repo collapses **many** of the user's granular personal commits into **one**
sync commit. That single message is the only thing a teammate reading the company history will
see — so it MUST explain *what was actually done*, not file counts. It is **never** the source
branch's last commit subject.

How the message is built — a **changelog since the last sync**, not a diff stat:

- Each sync commit is stamped with a provenance trailer `Source-commit: <source HEAD sha>`
  (the script does this automatically).
- **`sync.sh --stage-only`** clones/pulls the mirror, copies the source in, stages it, and
  prints both the file delta (`--stat`/`--name-status`) **and the source commits since the last
  sync** — `git log <previous Source-commit>..HEAD` for THIS app (it reads the `Source-commit`
  trailer of the last mirror commit carrying this app's `Sync-app:` marker). That list is the raw
  material for the message.
- **`sync.sh -m "<message>"`** re-stages, commits with your message (auto-appending the new
  `Source-commit:` trailer), and pushes.

Running `sync.sh` with no arguments still works for manual use: it commits an auto-generated
stat-based summary (e.g. `temps-chantier-code-app: sync — 8 fichier(s) modifié(s) (src, public)`).
That fallback is the *bad* message we want to avoid — always drive it via `--stage-only` + `-m`.

---

## How Claude Should Use This Skill

1. Confirm the user is in a Code App project root (must have `package.json`).
2. **Branch check:** if the user wants a specific branch (e.g. `master`), follow
   *Which branch gets synced* above — clean tree → `git checkout <branch>` → (sync) →
   `git checkout` back afterwards.
3. **Inspect the delta + changelog:**
   ```bash
   bash ~/.claude/skills/sync-to-azure/scripts/sync.sh --stage-only
   ```
   Read the printed file delta AND the **source commits since the last sync** — that commit
   list is what you summarise.
4. **Write a MEANINGFUL message:** synthesise the changelog into a Conventional-Commits message
   a teammate could understand — a clear subject + (when the delta spans several themes) a short
   bulleted body grouping the work (feat / fix / ST / refactor …). Describe *what was done*, not
   how many files. If `--stage-only` reported "no provenance trailer" (first trailer-tracked
   sync), summarise the recent commits it printed instead.
5. **Show the message to the user and WAIT for approval** before pushing — it goes to the
   company repo. Do not push until they confirm (adjust the message if they ask).
6. **Commit & push** (auto-stamps the `Source-commit:` trailer):
   ```bash
   bash ~/.claude/skills/sync-to-azure/scripts/sync.sh -m "<approved message>"
   ```
7. If you switched branches in step 2, `git checkout` back to the user's original branch.
8. Report the app name synced and the exact commit message that was pushed.

---

## Reminder system (so a master push is never forgotten)

Pushing `master` to the **personal GitHub** does NOT auto-sync to Azure (the sync needs the
local PAT, and a good message needs Claude). Instead, two machine-local reminders fire — never
an auto-sync, by design:

- **git `pre-push` hook** → `temps-chantier-code-app/.husky/pre-push` (husky v9). On a push that
  includes `master`, it shows a macOS notification + stderr line "pense à /sync-to-azure". Fires
  for **every local push, including VS Code's Push button** (VS Code runs git hooks). It NEVER
  blocks the push (`set +e`, always `exit 0`). Kept machine-local: listed in `.git/info/exclude`
  (untracked) and excluded from the Azure sync — it must not reach the company repo.
<!-- runtime-slot:session-drift -->
- **SessionStart drift-check** → wired in the project's `.claude/settings.local.json`, runs
  `scripts/session-drift-notice.sh`. When Claude Code opens in this project and the mirror is
  **behind** master, it injects a note so Claude reminds the user. Silent when in sync/unknown.
  This is the catch-all for pushes the local hook can't see (e.g. claude.ai cloud routines).
<!-- /runtime-slot:session-drift -->

Both rely on `scripts/drift-status.sh`, which compares local `master` to the last synced source
SHA — the `Source-commit:` trailer of the most recent mirror commit carrying this app's
`Sync-app:` marker (found via `git log --grep`, so an empty provenance-marker commit counts too).
Until the first provenance-stamped commit exists, drift is reported `UNKNOWN` (the hook still
reminds on a master push; the session check stays silent).

---

## Troubleshooting Reference

| Symptom                    | Fix                                                                            |
| -------------------------- | ------------------------------------------------------------------------------ |
| `Authentication failed`    | PAT expired — `rm ~/.fgl-azure/.pat`, create a new PAT, then re-run the script |
| `Clone failed`             | Check VPN/network and confirm PAT has **Code Read & Write** scope              |
| `Push failed after rebase` | Manual conflict in `~/.fgl-azure/repo` — resolve then re-run                   |
| Wrong app name used        | Add `"name": "<your-app-name>"` field to `power.config.json`                   |
| `No package.json found`    | You're not in the Code App root — `cd` to the right folder first               |
| Synced the wrong branch    | Checkout the intended branch (clean tree) and re-run — see *Which branch gets synced* |
| No copy tool found         | Need `rsync` (macOS/Linux) or `robocopy` (Windows) on `PATH`                   |
| No reminder on master push | `.husky/pre-push` must exist + be executable; husky uses `core.hooksPath=.husky/_` |
| Drift always `UNKNOWN`     | Normal until the first trailer-stamped sync — re-sync once so the mirror carries `Source-commit:` |
