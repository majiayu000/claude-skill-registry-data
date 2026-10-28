---
name: deploy
description: >-
  Manage Deno Deploy cloud services using both `deno deploy` and `deployctl`.
  Use this skill for deploying projects, managing Build/Dev/Prod environments,
  monitoring logs, and troubleshooting issues like private npm dependencies.
---

# Deno Deploy

This skill covers managing Deno Deploy cloud services using the built-in `deno deploy` command and the advanced `deployctl` utility.

## Core Concepts (Deno 2.x / 2026)

- **Integrated Build System**: Deno Deploy now handles builds (install + build steps) on its own infrastructure with automatic caching and live logs.
- **Deployment Contexts**: Environment variables and configurations are separated into **Production**, **Development** (Preview/Branch), and **Build** contexts.
- **Runtime Permissions**: Applications run with `--allow-all` by default, supporting subprocesses, FFI, and full npm compatibility.
- **Static Assets**: First-class support for static files (Vite, SSG) which are automatically cached by the Deno Deploy CDN.

## Built-in `deno deploy`

The `deno deploy` command is integrated into the Deno CLI and is suitable for basic deployment tasks.

### Commands
- `deno deploy [OPTIONS] [entrypoint]`: Deploy the project. If `entrypoint` is omitted, it's guessed from `deno.json` or files.
- `deno deploy create`: Create a new application.
- `deno deploy env`: Manage environment variables in the cloud (supports contexts).
- `deno deploy logs`: Stream live logs from a deployed application.
- `deno deploy switch`: Switch between organizations and applications.
- `deno deploy sandbox`: Interact with sandboxes.
- `deno deploy setup-aws` / `setup-gcp`: Configure cloud connections (OIDC).
- `deno deploy logout`: Revoke the Deno Deploy authentication token.

---

## Advanced Management via `deployctl`

For more granular control, including listing deployments and managing projects, use `deployctl`.

### Installation
```bash
deno install -gArf jsr:@deno/deployctl
```

### Projects and Deployments
- `deployctl list`: List all deployments for the current project.
- `deployctl projects list`: List all projects in your account.
- `deployctl deployments show <id>`: Show detailed information for a specific deployment/build.
- `deployctl redeploy --deployment=<id>`: Roll back or redeploy a specific version.
- `deployctl projects create <name>`: Create a new project.
- `deployctl projects delete <name>`: Delete a project.

---

## Troubleshooting & Best Practices

### Local Debugging Protocol (CRITICAL)
**ALWAYS** test deployment commands locally before updating CI/CD workflows.
1. Use the same token as in CI/CD.
2. Verify file uploading and revision creation.
3. Check for `IsADirectory` errors (often caused by missing `.gitignore` entries like `.playwright-browsers/`).

### Unstable APIs (Deno KV, etc.)
If your app uses `Deno.openKv()` or other unstable APIs:
- **Local run**: Requires `--unstable-kv`.
- **Deno Deploy (CLI)**: The `deno deploy` command **DOES NOT** support `--unstable-kv` or `--unstable` flags.
- **Deno Deploy (Runtime)**: You **MUST** enable unstable features in `deno.json`:
  ```json
  {
    "unstable": ["kv"]
  }
  ```
  Without this, the app will fail with `TypeError: Deno.openKv is not a function` in the cloud.

### Exclusions and File Management
- **Native CLI**: `deno deploy` **DOES NOT** support the `--exclude` flag.
- **Solution**: Use `.gitignore` to exclude files and directories. All files not ignored by git will be uploaded.
- **Large Directories**: Always exclude large local-only directories (like `.playwright-browsers/`) to avoid `IsADirectory` errors and slow uploads.

### CI/CD with GitHub Actions
Recommended workflow for complex projects:
1. **Permissions**: If using OIDC (automatic auth), ensure correct permissions:
   ```yaml
   permissions:
     id-token: write
     contents: read
   ```
2. **Native CLI**: Prefer native `deno deploy` over `deployctl` Action if you encounter authorization issues (`The bearer token is invalid`).
3. **Explicit Entrypoint**: Always specify the entrypoint file to avoid guessing errors in CI.
   ```yaml
   - name: Upload to Deno Deploy
     run: deno deploy --app=my-app --token=${{ secrets.DENO_DEPLOY_TOKEN }} --prod main.ts
   ```

### Private Dependencies (npm/JSR)
Deployments from local console may fail with `Internal Server Error` if the project uses private npm packages.
- **Cause**: Deno Deploy build servers cannot access your local private registry credentials.
- **Solution**: Use **GitHub Actions**. It can authenticate against private registries before deploying.

## Common Workflows

### Deploying to Production (Explicit)
```bash
deno deploy --app=my-app --prod main.ts
```

### Managing Environment Variables
```bash
deno deploy env set MY_VAR=value --context=production
```
