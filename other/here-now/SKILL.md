---
name: here-now
description: >
  Publish an intentional static-site or file snapshot to here.now, or keep and
  hand off private agent artifacts through here.now Drives. Use when asked to
  host, deploy, publish, share a URL, update a here.now site, save work for a
  later session, or give another agent scoped Drive access. Do not use for a
  deployed application backend, secrets, or a repository-wide upload.
allowed-tools: Read, Glob, Grep, Bash
trial_until: 2026-08-17
---

# here.now: publish artifacts without leaking a workspace

here.now has two different persistence models. Choose the model before touching
credentials or files:

| User outcome | Use | Boundary that matters |
|---|---|---|
| A public URL for a static page, PDF, image, video, or downloadable artifact | **Site** | Every file below the supplied path is a candidate for publication. |
| Private cross-session storage or an agent handoff | **Drive** | Files are private until a scoped token is shared. |
| A public rendering of a known private Drive snapshot | **Site from Drive** | The snapshot becomes public; use an account key and name the version if reproducibility matters. |

A Site is a versioned static artifact, not an application deployment. Do not use
it for a server, secret-bearing runtime configuration, authenticated API proxy,
or anything whose safety depends on a gitignore rule.

The bundled helpers are the operational interface. Run them from this skill
directory or invoke them by their full path:

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.claude/skills/here-now}"
"$SKILL_DIR/scripts/publish.sh" --help
"$SKILL_DIR/scripts/drive.sh" --help
```

If that global path is not installed, use `skills/here-now/scripts/...` from
this repository. The package tracks these shell helpers but deliberately
excludes the upstream bundled `jq` binary, so the runtime must provide `jq`
alongside `curl` and `file`. Do not replace the helpers with hand-written API
calls for a normal publish: they handle manifest hashes, skipped unchanged
uploads, finalization, state, ETags, and destructive-operation confirmations.

## Non-negotiable safety boundary

**Never publish a repository root or a broad working directory.** `publish.sh`
recursively includes files under its target; it does not apply `.gitignore`,
exclude `.env`, or exclude `.git`/`node_modules`. On a later run it can also
include the working directory's `.herenow/state.json`. `drive.sh import` skips
`.git` and `node_modules`, but it also does not protect `.env` or other secrets.

Build a narrow, disposable staging directory and publish or import only that
path. Inspect it immediately before an upload:

```bash
stage="$(mktemp -d)"
cp ./dist/index.html "$stage/index.html"
cp -R ./dist/assets "$stage/assets"
find "$stage" -type f -print | sort
"$SKILL_DIR/scripts/publish.sh" "$stage" --client claude-code
```

For a document or single image, pass that one file instead of its parent. For
HTML, `index.html` must be at the published directory root; publishing its
parent makes the nested directory part of the URL.

Do not copy credentials, `.env*`, SSH keys, `.git`, local state, source maps
that reveal private paths, or an unreviewed build directory into the stage.
Do not use `--base-url` with credentials unless the user has explicitly
approved that exact non-default endpoint; both helpers deliberately require
`--allow-nonherenow-base-url` before sending a token there.

## Operating procedure

### 1. Preflight and choose the smallest irreversible action

1. Ask whether the artifact is meant to be public or private. Treat an
   unspecified audience as private: use a Drive or request confirmation before
   publishing.
2. Identify the exact file set with `find`, not by assuming build output is
   safe. Create a staging directory for anything more than one known file.
3. Check the local prerequisites before preparing a large artifact:

   ```bash
   command -v curl file jq
   "$SKILL_DIR/scripts/publish.sh" --help >/dev/null
   ```

   The helpers use their bundled `jq` when available, otherwise system `jq`.
4. Determine persistence from credentials without printing the credential:

   ```bash
   test -n "${HERENOW_API_KEY:-}" && echo "account key available" || \
     test -s "$HOME/.herenow/credentials" && echo "account key file available" || \
     echo "anonymous publish only"
   ```

   No account key means a Site is anonymous and expires in 24 hours. A Drive
   cannot be used without an account API key or an already-scoped Drive token.
5. If a current product capability, quota, domain behavior, or API endpoint is
   material to the answer, fetch the current documentation before claiming it:

   ```bash
   curl -fsSL https://here.now/docs
   ```

   Script output and a successful API response are authoritative for the
   operation being performed. Do not claim an undocumented feature is absent
   merely because this skill does not describe it.

### 2. Publish a reviewed static artifact

Create a new Site:

```bash
"$SKILL_DIR/scripts/publish.sh" "$stage" --client claude-code
```

Update a known Site only when the user intended to replace that URL:

```bash
"$SKILL_DIR/scripts/publish.sh" "$stage" \
  --slug "existing-slug" --client claude-code
```

The helper performs **create/update -> upload -> finalize**. A create response
or uploaded bytes are not a successful publication; only an exit-zero run after
`finalizing...` is publish success. For updates it hashes files and the service
may report unchanged files as skipped. Do not interpret skipped files as a
failed update.

Use `--spa` only for a client-side router that should serve `index.html` on
unknown paths. Use `--title` and `--description` for a non-HTML viewer, not as a
substitute for meaningful HTML metadata. `--ttl` is an authenticated-publish
request; the final `publish_result.persistence` and `expires_at` lines, rather
than the requested flag, describe what actually happened.

### 3. Read the result contract, then verify the public artifact

`publish.sh` prints the current URL to stdout and machine-readable
`publish_result.*` facts to stderr. Capture both streams for the current run;
do not reconstruct status from `.herenow/state.json`.

```bash
"$SKILL_DIR/scripts/publish.sh" "$stage" --client claude-code \
  >publish.stdout 2>publish.stderr
site_url="$(tail -n 1 publish.stdout)"
grep '^publish_result\.' publish.stderr
curl -fsSI "$site_url"
```

A successful anonymous result has `auth_mode=anonymous` and
`persistence=expires_24h`. Tell the user it expires in 24 hours. Share a claim
URL only when the current stderr line has a non-empty HTTPS
`publish_result.claim_url`; claim tokens are returned once and cannot be
recovered. Never expose a claim token in a repository, commit, issue, or
screenshot.

A successful authenticated result has `auth_mode=authenticated`. Tell the user
whether it is permanent or expires at the reported timestamp. The script's
local `.herenow/state.json` is an update cache, not a user-facing source of
truth for a URL, auth mode, expiry, or claim status; keep it out of version
control and out of any staged publish directory.

If the HTTP verification fails after the helper exits zero, report the URL and
failure exactly, retain the stderr result facts, and investigate the artifact
or service response before saying it is live. Do not blindly retry a slug
update: retrying can replace the same public URL.

## Private Drive procedure

Use Drives for private handoff, durable notes, research, assets, and build
artifacts that should not become public. Start with a precise destination path
rather than a whole workspace:

```bash
"$SKILL_DIR/scripts/drive.sh" default
"$SKILL_DIR/scripts/drive.sh" put "My Drive" handoffs/2026-07-28/context.md \
  --from ./context.md
"$SKILL_DIR/scripts/drive.sh" cat "My Drive" handoffs/2026-07-28/context.md
```

The `put` path is concurrency-aware: it reads current metadata and sends
`ifMatch` for an existing file or `ifNoneMatch: "*"` for a new one. If a write
reports a conflict, fetch and review the current Drive content before choosing
to overwrite; never bypass the conflict with an unguarded direct API request.
Each file is limited to 500 MiB by the helper.

For a directory, preview the exact import first and use an isolated export
location on retrieval:

```bash
"$SKILL_DIR/scripts/drive.sh" import "My Drive" handoffs/2026-07-28 \
  --from "$stage" --dry-run
"$SKILL_DIR/scripts/drive.sh" import "My Drive" handoffs/2026-07-28 \
  --from "$stage"
"$SKILL_DIR/scripts/drive.sh" export "My Drive" handoffs/2026-07-28 \
  --to "$(mktemp -d)" --dry-run
```

`import` reports `planned`, `uploaded`, `skipped`, and `failed`; a nonzero
`failed` exits nonzero. Treat any failed count as an incomplete handoff. Verify
a critical file with `cat` or an export after import, not merely by a successful
command exit.

### Share the narrowest capability

A Drive share is a bearer capability. Give the receiving agent the minimum
permissions, shortest TTL, and narrowest prefix that completes the handoff:

```bash
"$SKILL_DIR/scripts/drive.sh" share "My Drive" \
  --perms read --prefix "handoffs/2026-07-28/" --ttl 7d --label "review handoff"
```

The share output is the handoff block. Do not paste its token into a committed
file, public Site, or broad chat transcript. A receiver using a Drive token
must reference the `drv_...` id rather than a Drive name; token credentials
cannot resolve names or list Drives. Preserve the supplied path prefix and
ETag behavior. Revoke a token when the task ends or its scope was wrong:

```bash
"$SKILL_DIR/scripts/drive.sh" tokens "My Drive"
"$SKILL_DIR/scripts/drive.sh" revoke "My Drive" "token-id"
```

`rm --recursive` requires `--confirm` with the exact path and bases deletion on
the Drive head version; `delete` similarly requires the exact Drive name. Do
not run either to "clean up" an uncertain handoff.

## Publish a Drive snapshot deliberately

Use this only when the user wants a **public** representation of a private
Drive artifact and an account API key is available:

```bash
"$SKILL_DIR/scripts/publish.sh" --from-drive "drv_..." \
  --version "dv_..." --client claude-code
```

Omit `--version` only when publishing the current head is explicitly intended.
Record the returned `publish_result.drive_version_id` with the URL so the
published artifact is traceable. This path does not create the local
`.herenow/state.json` cache and is always reported as authenticated.

## Credentials and failure handling

The helpers resolve an account key in this order: explicit `--api-key`,
`HERENOW_API_KEY`, then `$HOME/.herenow/credentials`. Use the credentials file
for interactive agent use and protect it with mode 600:

```bash
mkdir -p "$HOME/.herenow"
printf '%s\n' "$HERENOW_API_KEY" >"$HOME/.herenow/credentials"
chmod 600 "$HOME/.herenow/credentials"
```

Do not pass keys on a command line in an interactive session, print them,
commit them, or put them in a published staging tree. If an account key is
needed but absent, request the user's email and use the current here.now docs
for the one-time code flow; save the returned key yourself rather than asking
the user to manipulate a secret.

| Symptom | Correct response |
|---|---|
| `missing credentials` from `drive.sh` | Obtain account credentials or a scoped Drive token; do not fall back to public Site publication. |
| `refusing to send ... non-default base URL` | Stop unless the user explicitly authorized that endpoint; only then add the explicit override. |
| Upload failure or `finalize failed` | Report failure and preserve stderr. The Site is not live; fix the concrete file/network/API error before retrying. |
| Claim URL absent for anonymous Site | Tell the user it remains temporary; do not invent a URL from local state. |
| Drive conflict or ambiguous Drive name | Read current content or use the `drv_...` id; do not guess the target. |

## Completion message

For a Site, state: current `siteUrl`, whether it is anonymous/permanent/expiring
(as reported), whether verification passed, and the current HTTPS claim URL only
when applicable. For a Drive handoff, state: private destination path,
verification performed, and the scoped permission/TTL without repeating the
bearer token. Never call a Drive path a public URL.
