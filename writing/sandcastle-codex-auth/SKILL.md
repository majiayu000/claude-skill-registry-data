---
name: sandcastle-codex-auth
description: Configure Sandcastle Docker runs to use a user's existing Codex CLI ChatGPT subscription login instead of an OpenAI API key. Use when Sandcastle with Codex fails auth, cannot find codex in Docker, cannot capture Codex sessions, or the user wants Sandcastle to run Codex with ChatGPT Pro/Plus auth from ~/.codex.
---

# Sandcastle Codex Auth

## Goal

Make Sandcastle's Docker sandbox run `codex` using the host's existing `~/.codex/auth.json` login, while keeping Sandcastle session capture working.

Reference article for more detail:
https://www.eddyvinck.com/blog/how-to-set-up-sandcastle-with-codex/

## Process

1. Verify host Codex login:

```sh
which codex
codex --version
test -f ~/.codex/auth.json
codex login status
```

Expected paid ChatGPT auth signal:

```text
Logged in using ChatGPT
```

2. Ensure `.sandcastle/Dockerfile` installs Codex inside the image:

```dockerfile
RUN npm install -g @openai/codex
```

Place it before `USER agent` / `USER ${AGENT_UID}:${AGENT_GID}`.

3. In `.sandcastle/main.mts`, import Node path helpers:

```ts
import os from "node:os";
import path from "node:path";
```

4. Add shared Codex paths:

```ts
const hostCodexHome = path.join(os.homedir(), ".codex");
const sandboxCodexMount = "/mnt/host-codex";
const sandboxCodexHome = "/home/agent/.codex";
```

5. Use one shared Docker provider for all `run()` and `createSandbox()` calls:

```ts
const dockerSandbox = docker({
  env: {
    CODEX_HOME: sandboxCodexHome,
  },
  mounts: [
    {
      hostPath: hostCodexHome,
      sandboxPath: sandboxCodexMount,
      readonly: true,
    },
  ],
});
```

Do not set `GH_TOKEN: process.env.GH_TOKEN ?? ""` in provider env; it overrides `.sandcastle/.env` with blank. Let Sandcastle resolve `.sandcastle/.env` and process env.

6. Copy auth into Codex home during `onSandboxReady`:

```ts
const hooks = {
  sandbox: {
    onSandboxReady: [
      {
        command: [
          `mkdir -p "${sandboxCodexHome}"`,
          `test -f "${sandboxCodexMount}/auth.json"`,
          `cp "${sandboxCodexMount}/auth.json" "${sandboxCodexHome}/auth.json"`,
          `if [ -f "${sandboxCodexMount}/config.toml" ]; then cp "${sandboxCodexMount}/config.toml" "${sandboxCodexHome}/config.toml"; fi`,
        ].join(" && "),
      },
      { command: "npm install" },
    ],
  },
};
```

Use `/home/agent/.codex`, not `/tmp/codex-home`; Sandcastle looks there for Codex session capture.

7. Replace every `sandbox: docker()` with:

```ts
sandbox: dockerSandbox
```

For `createSandbox()`, use:

```ts
const issueSandbox = await sandcastle.createSandbox({
  branch: issue.branch,
  sandbox: dockerSandbox,
  hooks,
});
```

Avoid naming the local sandbox handle `sandbox`; it can shadow `dockerSandbox` and cause type/name bugs.

8. On macOS Docker, remove `copyToWorktree: ["node_modules"]`.

Linux containers cannot use macOS native modules reliably. Let `npm install` run inside Docker.

9. Rebuild image:

```sh
bunx sandcastle docker build-image
```

10. Verify auth inside image without spending a model call:

```sh
docker run --rm --entrypoint sh \
  -v "$HOME/.codex:/mnt/host-codex:ro" \
  -e CODEX_HOME=/home/agent/.codex \
  sandcastle:$(basename "$PWD") \
  -lc 'mkdir -p "$CODEX_HOME" && test -f /mnt/host-codex/auth.json && cp /mnt/host-codex/auth.json "$CODEX_HOME/auth.json" && if [ -f /mnt/host-codex/config.toml ]; then cp /mnt/host-codex/config.toml "$CODEX_HOME/config.toml"; fi && codex --version && codex login status'
```

Expected:

```text
Logged in using ChatGPT
```

11. Configure GitHub CLI auth for sandbox prompt expansion.

Sandcastle expands prompt shell blocks such as ``!`gh issue list ...` `` inside the sandbox. Host `gh auth status` can pass while sandbox `gh` fails because the container cannot read the host GitHub CLI keyring.

Verify the host account can access the repo:

```sh
gh repo view OWNER/REPO --json nameWithOwner,viewerPermission
gh issue list -R OWNER/REPO --state open --limit 1 --json number,title
```

Use a fine-grained personal access token (`github_pat_...`) with access to only this repo; this is the default, best option for Sandcastle GitHub auth. Do not use the broad GitHub CLI OAuth token (`gho_...`) unless GitHub blocks fine-grained PAT access for the repo.

Tell the user to create the fine-grained token with these GitHub UI settings:

- Resource owner: repo owner, e.g. `OWNER`
- Repository access: Only select repositories -> `OWNER/REPO`
- Repository permissions:
  - Metadata: Read-only (required/automatic)
  - Issues: Read and write
  - Contents: No access, unless this same token will also be used for git push/API commits; then use Read and write
- Leave Pull requests, Actions, Workflows, Administration, Secrets, and all other permissions as No access.
- Expiration: set one, preferably 30-90 days.

Tell the user this token name and create a new token in the GitHub UI:

```md
!`open https://github.com/settings/personal-access-tokens >/dev/null 2>&1; u="${GH_REPO:-$(git config --get remote.origin.url 2>/dev/null || basename "$PWD")}"; u="${u%.git}"; u="${u##*:}"; u="${u#*github.com/}"; p="${u##*/}"; p="${p:-$(basename "$PWD")}"; p="$(printf '%s' "$p" | tr '[:upper:]_' '[:lower:]-' | sed -E 's/[^a-z0-9-]+/-/g; s/-+/-/g; s/^-|-$//g' | cut -c1-40)"; printf 'sandcastle-%s-%s\n' "$p" "$(date +%Y-%m)"`
```

Create `.sandcastle/.env` with an empty `GH_TOKEN=` slot and explicit repo:

```sh
umask 077
{
  printf 'GH_TOKEN=\n'
  printf 'GH_REPO=OWNER/REPO\n'
} > .sandcastle/.env
chmod 600 .sandcastle/.env
```

Tell the user to paste the token locally in `.sandcastle/.env` after `GH_TOKEN=`. Never ask the user to paste GitHub tokens into chat.

Ensure `.sandcastle/.gitignore` contains:

```gitignore
.env
logs/
worktrees/
```

Use `GH_REPO` when the git remote is a fork, renamed repo, or SSH host alias such as `github-personal`; otherwise `gh` inside Docker may not infer the GitHub repo. If a collaborator-only repo does not appear in the fine-grained PAT repo picker, fallback to `gh auth token`, a classic PAT with repo access, or a repo-installed GitHub App, assuming org policy allows it.

Verify GitHub auth inside Docker without spending a model call:

```sh
docker run --rm --entrypoint sh \
  --env-file .sandcastle/.env \
  -v "$PWD:/home/agent/workspace" \
  -w /home/agent/workspace \
  sandcastle:$(basename "$PWD") \
  -lc 'gh issue list --state open --limit 1 --json number,title'
```

If `.sandcastle/main.mts` sets a custom Docker `imageName`, use that image instead of `sandcastle:$(basename "$PWD")`.

12. If `.sandcastle/main.mts` has red TypeScript squiggles for `node:*`, `process`, `@ai-hero/sandcastle`, or `zod`, make the root workspace a Node TypeScript project.

Install Node types at the repo root:

```sh
bun add -d @types/node@^20
```

Add root `tsconfig.json` if absent:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ESNext"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "types": ["node"]
  },
  "include": [".sandcastle/**/*.mts"]
}
```

Workspace/app tsconfigs usually do not cover root `.sandcastle` files, so VS Code can otherwise infer the wrong project.

Validate the editor-facing TypeScript project:

```sh
bunx --bun tsc --noEmit -p tsconfig.json --pretty false
```

If VS Code still shows old errors after this passes, restart the TypeScript server.

13. Validate script syntax:

```sh
bun build .sandcastle/main.mts --target=node --outfile=/tmp/sandcastle-main-check.js
```

If running TypeScript directly, missing `@types/node` may make `tsc` fail even when runtime is fine.

14. Add convenience script if absent:

```json
{
  "scripts": {
    "sandcastle": "npx tsx .sandcastle/main.mts"
  }
}
```

Run with:

```sh
bun run sandcastle
```

## Common Errors

- `sh: codex: command not found`: install Codex in `.sandcastle/Dockerfile`, then rebuild image.
- `Session capture failed`: set `CODEX_HOME=/home/agent/.codex`.
- `invalid ELF header`: stop copying host `node_modules`; run `npm install` in Docker.
- `GH_TOKEN` missing despite `.sandcastle/.env`: check provider env is not overriding it with `""`.
- `gh issue list` asks for `gh auth login` inside Docker: write `GH_TOKEN` to `.sandcastle/.env`.
- `none of the git remotes configured for this repository point to a known GitHub host`: add `GH_REPO=OWNER/REPO` to `.sandcastle/.env`.
- Collaborator repo missing from fine-grained PAT picker: use `gh auth token` or a classic PAT with repo access, if org policy allows it.
- Red squiggles on `node:*` imports / `process`: add root `@types/node` and a root `tsconfig.json` that includes `.sandcastle/**/*.mts`.
