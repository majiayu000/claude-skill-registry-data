---
name: dev-setup-webenv
description: "(Re)apply the Claude Code on the web profile setup. Use when: (1) User says '/dev-setup-webenv', 'set up web env', 'enable my skills on web', (2) A web session boots without the profile, (3) A new web environment or account needs the Setup script re-applied. Runs LOCALLY (Mac/terminal) — prints the canonical env setup script (PRIMARY: per-account, pre-launch, covers multi-repo sessions) and/or commits a single-repo SessionStart top-up hook from the bundled template."
argument-hint: "[--committed] [--env-script] [--self-only]"
---

# Dev: Set up / re-apply the Web Environment

Web sessions boot with the shared profile via two loaders:

| Loader | When it runs | Coverage |
|---|---|---|
| **Env Setup script** (`--env-script`, default) | pre-launch, per-account environment | every session, including multi-repo — the primary loader |
| **Committed hook** (`--committed`) | SessionStart, per-repo | single-repo sessions only — a redundancy fallback (fetches the mirror's default branch; skips when the env script already installed), never the only loader |

This skill runs on the **local terminal**; the download and install happen
later, inside the web container. When neither flag is passed, apply
`--env-script` — it is safe everywhere.

**Never put positional parameters (dollar sign + digit) anywhere in this
file** — skill argument substitution replaces them with invocation args and
corrupts embedded snippets. That is why the hook template lives in `assets/`
and the env script is read from disk instead of being embedded here.

## Step 1: Env setup script (`--env-script`, default)

1. Read `$HOME/.claude/web/env-setup-script.sh` (the canonical copy; the
   mirror ships it to the web container too) and print its contents verbatim
   for the user to paste into **claude.ai/code → Environment → Setup script**.

2. Tell the user to also fill the environment's **Environment variables**

   field:

   ```
   CLAUDE_WEB_PROFILE_OPT_IN=1
   DROPBOX_CCLOGS_DIR=/tmp/cclogs
   DROPBOX_SCREENSHOTS_DIR=/tmp/screenshots
   ```

   The `DROPBOX_*` stubs are needed because `$CLAUDE_ENV_FILE` (which
   `setup-web.sh` would otherwise write them to) may not exist pre-launch;
   the opt-in var feeds committed self-only hooks.

3. First-run check: the environment's setup output shows which tier worked —
   `claude-profile: cloned claude-settings` (tier 1, private clone) or
   `claude-profile: fetched claude-resources tarball` (fallback) — followed by
   `web profile installed into ...`.

## Step 2: Committed hook (`--committed`, optional top-up)

> **!! Team-repo safety !!** A committed `.claude/settings.json` affects
> **everyone** in the repo: on a teammate's web session it would overwrite
> their `~/.claude` and disable their permission prompts (web settings run in
> auto mode). Solo repos only, or get the owner's agreement — and prefer
> `--self-only`.

> **Single-repo sessions only.** Multi-repo web sessions never register
> repo-level settings hooks — this hook silently does nothing there. It is a
> top-up alongside Step 1, never the only loader.

1. Copy `assets/web-bootstrap.template.sh` (bundled in this skill's directory)
   to `<project>/.claude/web-bootstrap.sh` and `chmod +x` it.

2. If `--self-only` was passed: uncomment the `CLAUDE_WEB_PROFILE_OPT_IN` gate
   inside the copy, and **tell the user to set `CLAUDE_WEB_PROFILE_OPT_IN=1`
   in their per-account web environment variables** (already included in the
   Step 1 block) — without it the gate skips every session. The gate keys on a
   per-account env var — never on a committed email/identity (breaks on
   account switch; the harness email var is unreliable on web).

3. Register the hook in `<project>/.claude/settings.json` — **merge** into an

   existing file rather than overwriting:

   ```json
   {
     "$schema": "https://json.schemastore.org/claude-code-settings.json",
     "hooks": {
       "SessionStart": [
         {
           "hooks": [
             {
               "type": "command",
               "command": "/bin/bash \"$CLAUDE_PROJECT_DIR/.claude/web-bootstrap.sh\""
             }
           ]
         }
       ]
     }
   }
   ```

4. Commit both files (use `/co`) and push. In the report, always mention
   the single-repo-sessions-only limitation so a silent multi-repo skip is not
   mistaken for breakage.

## Prerequisites

- The public mirror must carry the web profile (`web/` +
  `scripts/setup-web.sh`) — publish with `/claude-resources-share`.
- Network policy must allow plain HTTPS egress to `github.com` (and its
  redirect target `codeload.github.com`) for the tarball tier.
- Tier 1 clone: `Takazudo/claude-settings` should be within the GitHub app's
  allowed repo scope. Optional — the tarball fallback covers a rejected clone.

## Gotchas (hard-won; do not re-litigate)

- **Multi-repo sessions never register repo-level settings hooks** (verified
  in-container): project dir is `/home/user`, repos are subdirectories;
  CLAUDE.md and skills load, hooks don't. Launcher-level hooks still fire, so
  "hooks work" is not evidence the repo hook ran. Only the env setup script
  covers these sessions.
- **`CLAUDE_CODE_REMOTE` is not guaranteed pre-launch**: `setup-web.sh` exits 0
  without it. The env script exports it explicitly — without that, the download
  succeeds and the install silently no-ops ("fetched fine, nothing installed").
- **Sentinel interplay**: the env script writes `~/.claude/.web-profile-source`
  after a successful install; the hook template skips when it is present, so a
  tier-1 private-clone profile is never clobbered by the hook's public-mirror
  tarball.
- **Scoped git proxy history** (mechanism: `gitConfigInjection` — the rewrite
  arrives via injected git config; `git config -l` in the container reveals
  it): out-of-scope `git clone` used to 403
  unconditionally; containers observed 2026-07 clone the user's own repos —
  but only post-boot (SessionStart context) was observed, and behavior has
  shifted once already. Every path keeps the tarball fallback. Verify from a
  web session with
  `git ls-remote --exit-code https://github.com/Takazudo/claude-settings HEAD`
  (expect a hash, not 403).
- **The Setup script result is cached as an environment snapshot** (docs:
  cached when it finishes in ~5 min). Sessions then boot the frozen
  `~/.claude` — a skill deleted/renamed upstream (e.g. old `/pr-complete`)
  lingers. Two guards: `setup-web.sh` prunes non-symlink skills/agents/commands
  missing from the source, and the user-level SessionStart hook in
  `web/settings.web.json` runs `scripts/web-refresh-profile.sh` each session
  (pull `~/.claude-src` or re-fetch the mirror, re-run `setup-web.sh` with
  `CLAUDE_WEB_SKIP_WISDOM=1`). To rebuild the snapshot itself, bump the
  `loader-rev` line and re-paste the script.
- **Cloud sessions never read the Mac's `~/.claude`** — only claude.ai
  account-enabled skills, the repo's `.claude/skills/`, and whatever the Setup
  script installs into the container's `~/.claude`. A skill appearing on web
  that no source has is either a stale snapshot or an account-level skill
  (claude.ai → Settings → Capabilities).
- `settings.local.json` is **not** an option — git-ignored, never reaches the
  web container.
- `setup-web.sh` sources from its own location, so it installs the downloaded
  profile's config, not the consumer project's.
