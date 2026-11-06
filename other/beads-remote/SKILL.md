---
name: beads-remote
description: Set up beads (bd) in a repo so its issues sync through a git remote on any host (GitLab, GitHub, Gitea, a bare repo on disk), or bring an existing remote's beads into a fresh clone. Use when the user wants beads shared across machines, a Box or a factory, asks to "sync beads", "add a beads remote", "bd init with a remote", or when bd sync/push fails on a repo that has no Dolt remote yet.
---

# beads-remote

Dolt stores beads in the repo's own git remote under `refs/dolt/data` (plus a `__dolt_remote_info__`
branch), so no extra server or account is needed: whoever can push the code can push the beads.

## Set up or join

Run the script from anywhere inside the repo:

```bash
scripts/beads-remote.sh                     # the repo's origin, prefix = directory name
scripts/beads-remote.sh --prefix web        # choose the prefix of a new database
scripts/beads-remote.sh --url git@github.com:org/repo.git
scripts/beads-remote.sh --cache-dir /var/tmp/cache/dolt-remote/web   # repo on EFS/NFS
```

It does only what is missing, so it is safe to run again:

1. Normalizes the URL for Dolt: `https://`, `http://`, `ssh://` and `file://` get `git+`; `git@host:path`
   becomes `git+ssh://git@host/path`; a path becomes `git+file://`.
2. No `.beads` yet: if the remote already has `refs/dolt/data`, clones those beads (their prefix wins);
   else `bd init --stealth` (beads files stay out of git via `.git/info/exclude`).
3. Adds the Dolt remote (`--allow-git-origin`, since sharing the code remote is the point) and sets
   `sync.remote`. A remote of the same name pointing elsewhere is an error, never overwritten.
4. With `--cache-dir`, moves Dolt's `git-remote-cache` there (embedded databases only).
5. Pulls when the remote has beads, pushes, then checks `refs/dolt/data` exists on the remote.

`scripts/test.sh` runs the whole round trip against a bare repo in a temp dir.

## Gotchas

- **Auth is plain git auth.** Whatever makes `git ls-remote <url>` work (SSH key, credential helper,
  a URL rewrite such as a broker's `insteadOf`) makes the push work. Check that first.
- **"ensure non-interactive auth is configured for GCM" can be a timeout, not auth.** Dolt reports a
  killed push that way. On a network filesystem the cache inside `.dolt` makes pushes slow: use
  `--cache-dir` on local disk, and recreate that directory at login if the disk is wiped on reboot
  (a dangling cache symlink breaks every push).
- **Shared Dolt server mode** (`BEADS_DOLT_SHARED_SERVER=1`) keeps the database outside `.beads`;
  `--cache-dir` is skipped there.
- **Protected branches:** the remote must accept a push of `refs/dolt/data` and the
  `__dolt_remote_info__` branch. Push rules that restrict branch names or refs block it.
- **Not stealth?** The script always uses `--stealth`. To commit `.beads/` config with the code, run
  `bd init` yourself first; the script then only adds the remote.
