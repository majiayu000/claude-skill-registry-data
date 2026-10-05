---
name: vps-cleanup
description: Reclaim disk on a shared dev/staging VPS or server in approval-gated tiers without breaking concurrent agent sessions. Use when disk usage is high or full, on "No space left on device", when asked to clean up the disk, or before a large build on a nearly full box.
---

# VPS Cleanup

On a box where several agent sessions run at once, "stale-looking" is not "unused": a `/tmp`
worktree can back someone's open PR, a `<none>` image can back a running container, a cache dir
can be held open by a live process. Work in tiers: survey read-only, clear regenerable caches,
then ask the user **once, batched** before each approval tier. Anything uncertain goes on the
**keep list** with its reason.

## 0. Survey (read-only, delete nothing)

1. Baseline: `df -h /`, `docker system df`, `docker buildx du`. Trust `buildx du` for build
   cache: `docker system df` can report most of it as non-reclaimable (shared vs private
   records) while `buildx du` shows all of it reclaimable.
2. Size directories in the background: `du` across large file counts (`node_modules`, pnpm
   stores) runs for minutes and hits tool timeouts in the foreground.

   ```bash
   out=$(mktemp); echo "$out"
   nohup sh -c 'nice du -xh --max-depth=2 /tmp "$HOME" /opt /srv 2>/dev/null | sort -rh | head -80' > "$out" 2>&1 &
   ```

   Root-only dirs (`/var/lib/docker`) are unreadable; size them with `docker system df`.
3. List containers and images: `docker ps -a --size`, `docker images`.
4. Find live users of every candidate cache path before touching it:

   ```bash
   c=<candidate-path>
   pgrep -af 'npm|npx|pnpm|yarn|bun|pip|uv|playwright|puppeteer|go '
   for p in /proc/[0-9]*; do
     ls "$p/fd" >/dev/null 2>&1 || { echo "unreadable ${p#/proc/}"; continue; }
     { ls -l "$p/cwd" "$p/exe" "$p/fd"; cat "$p/maps"; } 2>/dev/null | grep -qF "$c" && echo "in use by ${p#/proc/}"
   done
   docker ps -q | xargs -r docker inspect --format '{{range .Mounts}}{{.Source}}{{"\n"}}{{end}}' | grep -F "$c"
   ```

   `exe` and `maps` catch running binaries and loaded libraries, which `fd` misses; the
   `docker inspect` line catches containers bind-mounting the path. A path in use is skipped
   and goes on the keep list. Example: `~/.npm/_npx` and `~/.cache/ms-playwright` used by
   running playwright-mcp servers. Unreadable processes (other users, root, containers) make
   the check incomplete: unless you run it as root, treat the path as possibly in use and move
   it to the next approval tier instead of Tier 1.

Done when: `df` baseline recorded, candidate list sized, every candidate cache checked for live
processes.

## Tier 1: regenerable caches (no approval needed)

The only cost is re-downloading or rebuilding. Skip anything the survey found in use. Run
these from `$HOME`, not inside a repo: Yarn Berry's `yarn cache clean` inside a project clears
its `.yarn/cache`, which zero-install repos track in git.

- `docker builder prune -af`: usually the single largest win.
- `pnpm store prune`: removes only packages no registered project references. Repeat with
  `pnpm store prune --store-dir <dir>` for each extra store.
- `pip cache purge`, `uv cache clean`, `yarn cache clean`, `npm cache clean --force` (leaves
  `_npx` alone).
- Only these `~/.cache` dirs: `go-build`, `puppeteer`, `ms-playwright`. Every other
  `~/.cache/*` entry (model or dataset caches, tool state, other agents' caches) goes into the
  Tier 2 question.

Done when: `df -h /` re-run and the tier's reclaim recorded.

## Tier 2: `/tmp` caches and worktrees (ask the user once, batched)

Build the full candidate list first, then ask one question listing every path with its size.
Delete only what the user approves. If a permission classifier or the user denies a deletion,
stop there: that path goes on the keep list.

Candidates:

- Per-issue cache dirs in `/tmp`: `*-npm-cache`, `*-uv-cache`, `*-bun-cache`, `*-m2`, XDG caches.
- Issue worktrees such as `/tmp/<repo>-issue-<n>`, only when **all** of these hold:

  ```bash
  d=/tmp/<repo>-issue-<n>
  git -C "$d" fetch --prune --quiet &&                                       # refresh remote refs
  [ "$(git -C "$d" rev-parse --show-toplevel)" = "$d" ] &&                    # git top-level
  [ -z "$(find "$d" -maxdepth 2 -path '*/.git' -prune -o -mtime -7 -print)" ] && # untouched 7+ days
  [ -z "$(git -C "$d" status --porcelain)" ] &&                               # clean
  [ -n "$(git -C "$d" branch -r --contains HEAD)" ] &&                        # HEAD is on a remote
  [ -z "$(git -C "$d" log --branches --not --remotes --oneline)" ] &&         # no unpushed branch
  [ -z "$(git -C "$d" stash list)" ] &&                                       # no stashes
  echo QUALIFIES || echo KEEP
  ```

  Only `QUALIFIES` is a candidate. `KEEP` goes on the keep list as *recent*, *dirty*, or *not
  pushed*; a failed fetch also means `KEEP`. In a linked worktree the branch and stash checks
  cover the whole parent clone, so they can over-keep, which is the safe direction. Large
  recent trees are usually active work in another concurrent session.

Deletion rules:

- Delete specific children only, never a shared parent dir (for example `/tmp/<shared-work-dir>`).
- Exclude live-process sockets (`/tmp/tmux-*`, `/tmp/ssh-*`, `/tmp/.X11-unix`, `/tmp/.ICE-unix`);
  see `tmux-orphaned-socket`.
- Go module caches are read-only: `chmod -R u+w <dir>` before `rm -rf <dir>`.
- Root-owned files from Docker runs without `--user`, for an already-approved path only.
  Mount only that path, never all of `/tmp`, and use an image already present locally
  (`docker images`); pulling one onto a full disk can fail:

  ```bash
  p=$(realpath -e -- "<approved-path>") && case "$p" in
    /tmp/?*) docker run --rm -v "$p:/target" <local-image> find /target -mindepth 1 -delete && rmdir "$p" ;;
    *) echo "refuse: $p" ;;
  esac
  ```

  This clears approved paths; it never routes around a denial.
- After deleting a linked worktree, run `git worktree prune` in its parent clone.

Done when: approved paths deleted, worktrees pruned, `df -h /` re-run and reclaim recorded.

## Tier 3: Docker images (ask the user once, batched)

1. Find unused images: those whose ID no container (running or stopped) references.

   ```bash
   used=$(mktemp)
   docker ps -aq | xargs -r docker inspect --format '{{.Image}}' | sort -u > "$used"
   docker images -q --no-trunc | sort -u | comm -23 - "$used"
   ```

2. Keep the current and one previous tag for every deployed app, whether or not a container
   exists (a stopped or `compose down` app has none). Read the image each app deploys from its
   compose or deploy config.
3. Present the list with repo, tag, and size in one question.
4. Remove approved images with plain `docker rmi`, never `-f`, so Docker refuses anything still
   in use. Use the ID for untagged images and `repo:tag` for each tag of a multi-tagged image
   (by ID Docker refuses it as "must be forced"). If `rmi` refuses, the image goes on the keep
   list; never retry with `-f`. A dangling `<none>` image can back a running container even
   when `docker system df -v` shows 0 containers for it.
5. `SIZE` double-counts shared layers: measure the reclaim with `df -h /` before and after,
   not by summing sizes.

Done when: approved images removed and reclaim measured by `df`.

## Report only (never delete)

- Docker volumes, including ones with 0 links: the user runs any volume deletion themselves
  (see `docker-volume-guardrails`).
- Running containers.
- Anything with uncommitted or unpushed git work.
- Root-owned system logs needing sudo (`/var/log/btmp`, the systemd journal): report sizes.

## Report

- `df -h /` before and after.
- Reclaim per tier.
- Keep list: every skipped path with its reason (in use, recent, dirty, not pushed, denied,
  rollback tag).
- Leftovers needing the user: volumes, sudo-only logs, denied paths, with sizes.
