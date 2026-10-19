---
name: rotate-secrets
description: Rotate or replace a secret or key (BETTER_AUTH_SECRET, AI_SERVICE_SECRET, STALWART_WEBHOOK_SECRET, provider keys). Use when a secret leaked, a key is due for rotation, or the user asks how rotation works here.
argument-hint: <SECRET name>
disable-model-invocation: true
---

# Rotate secrets

Where secrets live: locally in `.env` (never read it; set values with
`bun run env:set KEY=value`). Deployed, in SOPS-encrypted Kubernetes Secrets committed
to git: `deploy/environments/<env>/secrets/<service>.sops.yaml`, each a Secret named
`director-editor-<service>` whose `stringData` holds that service's variables (platform
Secrets, such as the Cloudflare token, are in `deploy/platform/secrets/<env>/`). Argo CD
decrypts them into the cluster when the change reaches master (deploy/README.md,
"Secrets with SOPS"). Services read variables at start, so restart the affected
deployments once Argo CD has synced
(`kubectl -n director-editor rollout restart deployment/director-editor-<service>`).

Never decrypt a secrets file yourself (`sops -d`, `sops <file>`, `sops decrypt`): that
puts the values in the conversation. The user edits them with `sops <file>`, which opens
the decrypted Secret in their editor and encrypts it again on save; give them the exact
file and key to change. A brand-new value that nobody needs to see can be written
without showing it: `sops set <file> '["stringData"]["KEY"]' "\"$(openssl rand -base64 32)\""`.
Commit only encrypted files (`charts:check` and the pre-commit hook refuse plain ones).

## AI_SERVICE_SECRET (shared by api and ai)

Both sides must change together: AI_SERVICE_SECRET in api and ai
(`apps/ai/app/settings.py`). Set the new value in both services' Secrets, commit,
restart both once synced. AI calls fail until both sides run the new value (tokens live
60 s).

## BETTER_AUTH_SECRET

better-auth signs session cookies with it and encrypts Google's OAuth tokens and
two-factor secrets and backup codes with it. Never just
replace it: everything encrypted becomes unreadable. Rotate with versioned secrets
(`apps/api/src/auth/secrets.ts`):

1. Generate one: `openssl rand -base64 48`. Set `BETTER_AUTH_SECRETS` for the api,
   newest first: `1:<new>` the first time, then `2:<newer>,1:<new>` and so on. Keep
   `BETTER_AUTH_SECRET` as it is: it still decrypts values written before versions.
   Deployed, `BETTER_AUTH_SECRETS` goes in the api's Secret; locally
   `bun run env:set BETTER_AUTH_SECRETS=1:<new>`.
2. Commit, and restart the api once synced. Every session cookie is signed with the newest secret
   only, so everyone signs in again once; nothing else breaks.
3. Re-encrypt (safe while the api runs, safe to repeat): `bun run secrets:reencrypt`
   locally; deployed, a Job from the stack's suspended CronJob:
   `kubectl -n director-editor create job --from=cronjob/director-editor-reencrypt reencrypt-$(date +%s)`,
   then `kubectl -n director-editor logs -f job/<that job>`. Never `kubectl exec` it into a
   running api pod: the second process shares the pod's memory limit and gets the api
   OOM-killed. It moves every stored value to the newest version; a second run moves 0.
4. Then older versions can go from `BETTER_AUTH_SECRETS`. The legacy
   `BETTER_AUTH_SECRET` is still required by the api's environment; once re-encryption
   has run, its value no longer protects anything and can be replaced with a fresh one.

## STALWART_WEBHOOK_SECRET (the mail server's bounce webhook)

Stalwart signs with one key; the webhooks service accepts several, comma-separated.

1. New key: `openssl rand -base64 32`. In the webhooks Secret, set
   `STALWART_WEBHOOK_SECRET: "<new>,<old>"`; commit, restart webhooks once synced.
2. Give Stalwart the new one: the same key in the mail server's Secret (`stalwart` in
   namespace `mail`, under `deploy/platform/secrets/<env>/`), then restart it
   (`kubectl -n mail rollout restart statefulset/mail`); its settings plan re-applies on
   start.
3. Drop the old key from the webhooks Secret, commit, restart webhooks.

Locally: `bun run env:set STALWART_WEBHOOK_SECRET=<new>` and `bun run db:up:mail`.

## Provider keys (Google, YouTube, Gemini, Turnstile)

Create the new key at the provider, put it in the Secret of the service that uses it
(`GOOGLE_CLIENT_*`, `YOUTUBE_API_KEY` and the Turnstile keys belong to api,
`GOOGLE_API_KEY` to ai; see each app's `src/env.ts` and `apps/ai/app/settings.py`),
commit, restart that service once synced, then revoke the old key.

## A cluster's age key

It decrypts every Secret of its environment, and lives in three places that change
together: the `sops-age` Secret in `argocd`, the `infra-<env>` environment's
`SOPS_AGE_KEY` on GitHub, and the operator's safe copy. The steps are in
`deploy/README.md`, "Replacing a cluster's age key": the new public key next to the old
in `.sops.yaml` and `sops updatekeys`; the new private key in `SOPS_AGE_KEY` with
`sops_keys_version` raised by one in tfvars, then apply (OpenTofu can't see a write-only
key change) and restart the repo server; then remove the old public key and `updatekeys`
again. A leaked key means every secret it could decrypt is leaked too: rotate those
values as well.
