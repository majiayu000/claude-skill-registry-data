---
name: deploy-to-heroku
description: Deploy applications to Heroku with safe, read-only inspection first. Use when the agent needs to assess Heroku readiness, choose between Heroku Git and container deployment, create or target an app, wire a Heroku remote, or perform a controlled Heroku deployment.
---

# Deploy to Heroku

Deploy repositories to Heroku without assuming the deploy path up front.

## Start with inspection

Resolve this installed skill's directory first. Do not assume the current workspace contains the skill source repository.

Run the bundled preflight script from this skill's `scripts/` directory:

```bash
python3 /path/to/deploy-to-heroku/scripts/preflight.py
```

Use the output to identify:

- whether the Heroku CLI is installed
- whether the current shell is authenticated
- whether the repo already has a Heroku git remote
- whether the repo is better suited to buildpack deployment or container deployment

## Choose the deploy path

Prefer Heroku Git when the repository already looks like a standard buildpack app:

- `Procfile`
- a supported language manifest such as `package.json`, `requirements.txt`, `Gemfile`, or `pom.xml`
- no explicit requirement for Docker-only behavior

Prefer container deployment only when the repository clearly requires it:

- `Dockerfile` is the primary runtime contract
- `heroku.yml` already defines the build and release model
- the user explicitly asks for `container:*` commands

If the repository uses pipelines or review apps, coordinate with `heroku-pipelines-review-apps` instead of inventing a standalone deploy flow.

## Safe deployment sequence

1. Inspect local state before changing anything.
2. Confirm the target app name and environment before creating or reusing an app.
3. Verify authentication with `heroku auth:whoami`.
4. Confirm any app-creating action such as `heroku apps:create`.
5. Set or review the Heroku git remote with `heroku git:remote -a <app>` if the Git workflow is selected.
6. Check stack and buildpack assumptions before pushing.
7. Deploy with the smallest valid change surface:
   - `git push heroku <branch>:main` for Heroku Git
   - `heroku container:push` and `heroku container:release` only when container deployment is intentional
8. Verify the release with `heroku releases:info -a <app>` and a bounded log review instead of an endless log tail.

## Guardrails

Ask for confirmation before:

- creating an app
- changing the target app
- pushing to production
- switching deploy strategy
- changing buildpacks or stack

Treat `git push heroku` as production-changing unless the user has clearly established a non-production app.

## References

- Read `references/deployment-workflows.md` for command catalogs, decision rules, and source links.
