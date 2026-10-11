---
name: examples
description: |
  End-to-end scenario walkthroughs for updating self-hosted Dify. Use when the user asks for "dify update example", "how to update dify", "show me an update walkthrough", "dify upgrade guide", "step-by-step dify update", or needs a complete example of the update process.
---

## Available Scenarios

| Scenario | Description | Reference |
|----------|-------------|-----------|
| Routine update | Latest stable tag, external vector store (Weaviate gate passes), backup with the stack down, no conflicts, env sync, pull and start | `references/scenarios/routine-update.md` |
| Tagged release update | Specific tag, bundled Weaviate: the pre-flight STOPs, the runbook is followed, the update is re-run; custom project name, one conflict on the generated compose file | `references/scenarios/tagged-release-update.md` |

## Quick Reference: Happy Path

Bundled Weaviate with data and a target of 1.17.1 or newer: stop at the pre-flight and follow the Weaviate runbook first (see the `update-workflow` skill). Everything else:

```bash
# From dify/ root directory
git fetch origin --tags
TARGET=$(git tag --list | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -1)   # latest stable tag

# Remember where dev is, so a rollback can put it back (and return to the branch you started on)
git rev-parse --abbrev-ref HEAD; git rev-parse dev

# Backup: stack down, then archive volumes (outside the repo, no secrets in output)
cd docker/
export COMPOSE_PROJECT_NAME=<project>   # project of the running stack (docker compose ls); keep it in this block
cp -p docker-compose.yaml <backup-dir>/ && cp -p .env <backup-dir>/
docker compose stop -t -1 weaviate   # only with VECTOR_STORE=weaviate: no timeout, never a hard kill
docker compose down -t 120
docker ps -q --filter "label=com.docker.compose.project.working_dir=$PWD"   # must print nothing before the archive
sudo tar -czpf <backup-dir>/volumes.tgz -C volumes .

# Merge
cd ..
git checkout dev
git merge "$TARGET"

# Sync environment: official script, secrets masked (see the env-sync skill)
cd docker/
bash dify-env-sync.sh   # run it through the masking filter; it DROPS keys that are not in the new .env.example
# then list dropped key names against <backup-dir>/.env and restore the ones you need (env-sync skill)

# Pull and start
docker compose pull
docker compose up -d

# Verify (init_permissions shows Exited (0): that is normal)
docker compose ps
```

## Quick Reference: Specific Version

```bash
git fetch origin --tags
# Weaviate gate first when the target is 1.17.1 or newer (update-workflow skill)
# ... backup as above ...
git checkout dev
git merge 1.17.1
# Resolve any conflicts: take upstream for docker-compose.yaml, keep customizations in .env or docker-compose.override.yaml
cd docker/
# Sync .env, restore dropped keys
export COMPOSE_PROJECT_NAME=myproject
docker compose pull
docker compose up -d
docker compose ps
```