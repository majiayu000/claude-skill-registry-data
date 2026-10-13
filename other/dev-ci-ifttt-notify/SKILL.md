---
name: dev-ci-ifttt-notify
description: "Add an IFTTT webhook notify job to a GitHub Actions workflow for mobile push notifications on deploy/CI success or failure. Use when the user says 'IFTTT notify', 'deploy notification', 'CI notification', or 'push notification for CI'."
argument-hint: "[IFTTT_WEBHOOK_URL]"
---

# CI IFTTT Notification

Append a `notify` job to a GitHub Actions workflow (usually the production deploy workflow) that POSTs the run result to an IFTTT Webhooks URL held in the `IFTTT_PROD_NOTIFY` repo secret.

## Payload contract (convention C2 — this skill owns it)

Everything that posts to `IFTTT_PROD_NOTIFY` uses this layout. Mobile push shows only `value1` prominently, so it must be self-explanatory alone:

| Field | Content | Example |
| --- | --- | --- |
| `value1` | `<project>: <emoji> <status>` | `my-app: ✅ Deploy succeeded` |
| `value2` | Run URL | `https://github.com/.../runs/123` |
| `value3` | unused | `""` |

Never split project name and status across value1/value2. Emoji: `✅` success, `❌` failure (name the failed stage), `⚠️` cancelled/other.

## Notify job

```yaml
  notify:
    name: Notify
    needs: [quality, build, deploy] # ALL prior jobs
    if: always()
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Notify via IFTTT
        if: env.IFTTT_PROD_NOTIFY != ''
        env:
          IFTTT_PROD_NOTIFY: ${{ secrets.IFTTT_PROD_NOTIFY }}
        run: |
          QUALITY="${{ needs.quality.result }}"
          BUILD="${{ needs.build.result }}"
          DEPLOY="${{ needs.deploy.result }}"

          # deploy success first, then failures in pipeline order
          if [ "$DEPLOY" = "success" ]; then
            STATUS="✅ Deploy succeeded"
          elif [ "$QUALITY" = "failure" ]; then
            STATUS="❌ Quality checks failed"
          elif [ "$BUILD" = "failure" ]; then
            STATUS="❌ Build failed"
          elif [ "$DEPLOY" = "failure" ]; then
            STATUS="❌ Deploy failed"
          else
            STATUS="⚠️ Cancelled (quality=$QUALITY build=$BUILD deploy=$DEPLOY)"
          fi

          RUN_URL="${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"

          jq -n --arg v1 "<project-name>: $STATUS" --arg v2 "$RUN_URL" \
            '{value1: $v1, value2: $v2, value3: ""}' | \
          curl -sf -X POST "$IFTTT_PROD_NOTIFY" -H 'Content-Type: application/json' -d @-
```

- `secrets.*` cannot be used in an `if:` directly — map it to `env` on the step and test `env.IFTTT_PROD_NOTIFY != ''`. The job then skips silently in forks / repos without the secret.
- Build the JSON with `jq -n`, not string interpolation — dynamic values stay safely escaped.
- `needs` must list every job whose result is reported; a job missing from `needs` has no `needs.<job>.result`.
- Add a line about the notify job to the workflow's header comment if it has one.

## Secret and applet

```bash
gh secret set IFTTT_PROD_NOTIFY --body "<webhook-url>"   # omit --body to paste interactively
gh secret list
```

URL shape: `https://maker.ifttt.com/trigger/{EVENT}/with/key/{KEY}`. If the user has no applet yet: https://ifttt.com/maker_webhooks → trigger "Receive a web request" → action "Send a notification from the IFTTT app" with template `{{Value1}}` (`{{Value2}}` into the link field if the action has one).

An applet created with the old `{{Value1}}: {{Value2}}` template must be updated on the IFTTT side — that is a manual user action; tell the user.

Optional `.env.example` entry for documentation:

```bash
# IFTTT webhook for production deploy notifications (GitHub Actions secret)
# IFTTT_PROD_NOTIFY=https://maker.ifttt.com/trigger/{event}/with/key/xxxxxx
```

Test the webhook:

```bash
curl -sf -X POST "$IFTTT_PROD_NOTIFY" -H 'Content-Type: application/json' \
  -d '{"value1":"my-app: ✅ Deploy succeeded","value2":"https://github.com/owner/repo/actions/runs/123","value3":""}'
```
