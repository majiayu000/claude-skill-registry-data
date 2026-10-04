---
name: cloud-checkup
description: >-
  Read-only SRE checkup of any GCP project: deterministic probes of the edge, Cloud Run
  services, 7-day error logs, Cloud Scheduler, alert policies and uptime checks, Secret
  Manager and IAM, the data stores and the machine's own scheduled jobs, audited into one
  fixed status table (LIVE / WARNING / RED / INCONCLUSIVE) with evidence, findings by
  severity, what could not be checked, and a single OVERALL line delivered as one
  notification. Parametrised by a per-project manifest, so the same routine runs on every
  project. Use when the operator says "cloud checkup", "SRE check", "is everything live",
  "what's healthy / warning / red", "any errors this week", "audit the infra", "weekly
  checkup", "set up the weekly checkup", before a deploy or demo, or after an incident.
  Cloud Run first; App Engine and GKE differ only in the
  serving probes.
argument-hint: "[--manifest <path>] [--probes-only] [--install-schedule]"
---

# cloud-checkup

One routine, two entry points: in-session (you are the inspection layer) and headless
(scheduled or on demand). Both fill the same template, so two runs are comparable.

Read-only throughout. It never deploys, never mutates cloud state, never restarts or
unpauses anything.

## Three layers

| Layer | What it does | Survives without the next layer |
|---|---|---|
| 1. Deterministic probes | `scripts/cloud_checkup.sh`: curl, `gcloud ... describe`, `gcloud logging read`, scheduler, monitoring, secrets, IAM, local jobs. Writes a probes file. | Yes. The probes file is the artefact of record. |
| 2. Read-only inspection | Headless `claude -p` (or you, in session) reads the probes, queries the data stores, fills `templates/CHECKUP-TEMPLATE.md` into the report. | Yes. Without it the report is the probes file plus `OVERALL: INCONCLUSIVE`. |
| 3. One notification line | `scripts/notify.sh` posts the `OVERALL` verdict and the report path. | Yes. Suppressed with `CC_NO_NOTIFY=1`. |

Layer 1 exists so the routine still has value when the model is unavailable, rate-limited
or wrong. Never let layer 2 be the only thing that ran.

## Status legend

| Status | Rule |
|---|---|
| 🟢 LIVE | The check passes and that feature had zero errors in the review window. |
| 🟡 WARNING | It serves, but had errors in the window, or is degraded, paused, stale beyond its threshold, or drifted from the source of truth. |
| 🔴 RED | It errors right now, is down, or is halted. |
| ⚪ INCONCLUSIVE | It could not be read from this seat. Say what would be needed. |

**`PERMISSION_DENIED` reads as INCONCLUSIVE, never as zero.** A denied `logging read`
returns no rows; scoring that as "no errors" turns a blind seat into a green light. Every
probe captures stderr and marks the row INCONCLUSIVE on any permission or API error.
INCONCLUSIVE is a capability gap of the seat, not a health signal.

## Identity discipline

The machine's default `gcloud` account drifts between identities, and a stored credential
can mint a token for a different principal than the one you asked for.

1. **Pin `--account` on every call.** The script wraps `gcloud` in a `gc()` helper that
   always passes it. Never `gcloud config set account`: it mutates state the operator's
   other work depends on, and it survives the run.
2. **Verify the token identity, not the config.** The script mints an access token for the
   pinned account and reads the `email` back from
   `https://oauth2.googleapis.com/tokeninfo`. If that email is not the pinned account, the
   whole cloud plane is INCONCLUSIVE regardless of what the probes returned, because the
   reads were made as somebody else. The token goes over stdin, never into argv, and never
   into the probes file.
3. **Record the observed default** alongside the pinned account, so drift is visible
   without being acted on.

## Manifest

Everything project-specific lives in one YAML file. Copy `manifest.example.yaml` to the
project (`.cloud-checkup.yaml` at the repo root is the convention) and fill it in: project,
region, account, services, public URL and edge routes, expected security headers, log
review window, data stores, local jobs, ticket map, extra rows, notification sink,
schedule. The probe script reads it with `yq` when present, PyYAML next, and a small
built-in parser last; the inspection layer reads the file itself, so richer structures
(data stores, ticket map, extra rows) need no parser support.

## Run it

```bash
CC=~/.claude/skills/cloud-checkup

# In session: probes only, then you fill the template as layer 2.
CC_SKIP_AI=1 CC_NO_NOTIFY=1 CC_MANIFEST=.cloud-checkup.yaml "$CC/scripts/cloud_checkup.sh"

# Headless, full run (probes + inspection + notification).
CC_MANIFEST=.cloud-checkup.yaml "$CC/scripts/cloud_checkup.sh"
```

In-session, after the probes land: read the probes file, query each data store in
`data_stores[]` (see `modules/` for the per-type routine), fill every row of
`templates/CHECKUP-TEMPLATE.md`, compare against the previous report in the report
directory for "Changed since", map findings to `ticket_map`, and end the file with exactly
one `OVERALL:` line. Point `CC_OUT` at a scratch path when running probes-only, so the
stub never lands on the canonical report name. Lead the chat reply with RED rows, then
WARNING, then the `OVERALL` line and the report path. Do not commit; the operator does.

## Schedule it

Weekly is the right cadence: often enough to catch a dead writer before its data expires,
rare enough that the report is read.

- **macOS:** fill `templates/launchd.plist.tmpl`, install to `~/Library/LaunchAgents/`,
  `launchctl load` it. `StartCalendarInterval` uses local time, so the hour tracks the
  operator's clock through DST with no UTC conversion.
- **Linux and elsewhere:** `templates/cron.example`, or a systemd timer of the same shape.

**Logs never go in `/tmp`.** macOS purges `/tmp` after three days of no access, and it does
it while a long-lived process still holds the descriptors, so the failure that matters is
exactly the one whose log is gone. Both templates put stdout, stderr and the probes files
under `${CC_STATE_DIR:-$HOME/.local/state/cloud-checkup}`.

## Read-only by construction

Layer 2's headless tool grant is a **positive allowlist of exact read-only subcommands**,
not a denylist of dangerous ones. A denylist is a guess about what a future gcloud release
will name its mutating verbs; an allowlist fails closed when that guess is wrong. The list
lives in `scripts/cloud_checkup.sh` (`AI_ALLOW`) and holds only read forms: `gcloud`
`describe` / `list` / `read` / `get-iam-policy`, header-only and status-only `curl`, `git log`
and `git status`, local file reads, and the MongoDB MCP read tools by name (`find`,
`aggregate`, `count`, `explain`, list / schema / index / stats) — never a wildcard, which would
admit the server's insert, update, delete and drop tools. Launch the MongoDB server with
`--readOnly` as well. A short denylist sits behind it as defence in depth, not as the mechanism.

`Write` is the one grant that can change the working tree, and it is bounded by the prompt
(one report path) rather than by the grant. That is the routine's one residual: run the
checkup on a clean tree, and read the report's diff before committing it.

## What NOT to do

Not at any layer, not "just to confirm", not because a fix looks obvious:

- No deploy, no `gcloud run deploy`, no `gcloud builds submit`, no image promotion.
- No mutation of cloud state: no `services update`, no IAM binding, no secret version, no
  alert policy or uptime check creation, no `terraform apply`.
- No restart, no `launchctl kickstart`, no `systemctl restart`, no scheduler `resume` or
  `run`, no unpausing anything.
- No `gcloud config set`, no `gcloud auth login`, no credential rotation.
- No `git commit`, `git push`, `git checkout` or branch change.
- No destructive data operation, and no data write of any kind outside the report.

Remediation is the operator's, or a separate agent's, under its own approval. The checkup's
output is the ticket, not the fix.

## Changing the checkup itself

The checkup is the thing that tells the operator whether to trust the estate, so a silent
regression in it is worse than a red row. Changes to the script, the template or the prompt
carry an independent review bound to the exact diff, in the repo's own review-trailer form,
for example `Reviewer: PASS 2026-09-04 sha=<digest>`. The writer never approves its own
change. Whoever changed a status rule states which rows can flip because of it.

## Beyond Cloud Run

Layers 2 and 3, the legend, the identity discipline and the template are platform-neutral.
Only the serving probes in layer 1 change:

| Platform | Serving probe | Log filter | Currency row |
|---|---|---|---|
| Cloud Run (default) | `run services describe`, latest ready revision and traffic percent | `resource.type="cloud_run_revision"` | deployed image digest against the branch |
| App Engine | `app services list`, `app versions list --hide-no-traffic` | `resource.type="gae_app"` | serving version id and its traffic split |
| GKE | `container clusters describe`, then a read-only `kubectl get deploy,pods` | `resource.type="k8s_container"` | image tag on the deployment against the branch |

App Engine has no per-revision traffic pin, so the "latest revision at 100%" row becomes
"the serving version is the one that was deployed". GKE adds rows the others do not need:
node pool health, pod restart counts, and pending or evicted pods.

## Files

| Path | What |
|---|---|
| `manifest.example.yaml` | Per-project inputs, commented. |
| `scripts/cloud_checkup.sh` | Layer 1 probes, layer 2 dispatch, fallback report, layer 3 call. |
| `scripts/notify.sh` | Pluggable notification sink. Slack incoming webhook by default. |
| `templates/CHECKUP-TEMPLATE.md` | The fixed report. Generic rows plus `{{EXTRA_ROWS}}`. |
| `templates/checkup_prompt.md` | The layer 2 inspection prompt, manifest-parametrised. |
| `templates/launchd.plist.tmpl`, `templates/cron.example` | Schedule scaffolds. |
| `modules/mongodb_atlas.md` | Data-store module: what to assess, and the assess/plan/apply/rollback retention pattern. |
