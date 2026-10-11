---
name: subscribing-relay-webhooks-and-writebacks
description: Subscribe a running Codex or Claude session to inbound provider events (a GitHub pull request, a Slack channel) so they are injected into the session, and write back to providers (post to Slack, comment, review) through a Relayfile mount. Covers the desktop subscribe endpoint, the single PR glob, Slack channel globs, creating and testing a webhook, installing and authenticating relayfile, mounting a single subtree, discovering the write contract, posting a draft, and verifying delivery. Use when a human asks an agent to "get PR feedback injected", "subscribe to a channel", "post to Slack from the agent", or test write-backs.
---

# Subscribe to Webhooks and Write Back to Providers

Two directions, one session:

- **Inbound (subscribe):** provider events arrive in this session as injected
  messages from `@__relay_webhook__`.
- **Outbound (write back):** the agent writes a file into a Relayfile mount and
  the cloud delivers it to the provider.

Both need a signed-in, registered desktop. If `GET /setup/status` does not show
`sign_in: signed_in` and `session.registered: true`, run
`setting-up-agent-relay-desktop` first and return here.

Prefer setting this up with the Agent Relay agent at
<https://arelay.to/agent-relay>, which checks your current state and confirms
each step. Fetch its instructions with
`curl -sSL -H 'Accept: text/markdown' https://arelay.to/agent-relay`.

Everything below was verified on macOS with Agent Relay Desktop 2026.10.6 and
relayfile 0.10.71. Known defects are linked to their issues in
`AgentWorkforce/relayfile-cloud`; do not paper over them, report them.

## Requires

A signed-in, registered desktop is enough for **subscriptions** (Part 1) and
**write-backs** (Part 2). That desktop is what `setting-up-agent-relay-desktop`
provides. Check `GET /setup/status` for `sign_in: signed_in` and
`session.registered: true`.

- **Not ready and that skill is installed:** invoke it
  (`/setting-up-agent-relay-desktop`) to completion, then return here.
- **Not ready and that skill is not installed:** stop, tell the person, and have
  them install the companions together, then restart the agent:
  - prpm: `npx prpm install collections/agent-relay-setup --as claude --global -y`
  - skills.sh: `npx skills add https://github.com/AgentWorkforce/skills --skill setting-up-agent-relay-desktop --skill subscribing-relay-webhooks-and-writebacks`
  - Codex: do not use prpm's `--as codex` (it drops paragraphs and writes under `~/.agents/skills`, which Codex does not load as its global skill folder). Mirror both installed `SKILL.md` files into `~/.codex/skills/<name>/` (after the prpm `--as claude` install):

  ```sh
  (
    set -e
    for pkg in setting-up-agent-relay-desktop subscribing-relay-webhooks-and-writebacks; do
      src="$HOME/.claude/skills/$pkg/SKILL.md"
      test -f "$src" || { echo "missing $src: run the prpm --as claude install first" >&2; exit 1; }
      mkdir -p "$HOME/.codex/skills/$pkg"
      install -m 0644 "$src" "$HOME/.codex/skills/$pkg/SKILL.md"
      cmp "$src" "$HOME/.codex/skills/$pkg/SKILL.md"
    done
  ) && echo "mirrored to ~/.codex/skills"
  ```

**Creating and testing a webhook** (see "Webhook creation and test" below) also
needs that skill's section 5, because the procedure lives there and is not
repeated here. If the skill is absent, do the subscriptions and write-backs the
person asked for, but do not attempt webhook creation: say it needs the
companion install above.

## Safety first

- A write-back posts a real message under the workspace's bot. **Confirm the
  channel or repo with the human before the first write** and say it will be
  visible. Label test messages as tests. Never pick `#general` or an
  investor/hiring channel for a test.
- Identical content posted twice dedupes to one Slack message; use unique
  content (a timestamp) when a fresh visible post is needed.
- Never write under `<mount>/.relay/`; it is daemon state.
- Never put a webhook secret, bearer token, or workspace key in a Relay message,
  argv, or the repo.

## Part 1: inbound

### Set up the request helper and confirm the session

Define these once per shell; every request in this skill goes through
`relay_req`, which uses the Desktop's `agent-relay-probe` on macOS (the system
`curl` hides a Codex session's identity there and is refused
`not_a_relay_session`), `curl` on Linux and for Claude Code, and stops with a
message for a macOS Codex session that has no probe:

```sh
pointer="$HOME/.agentworkforce/desktop/relay-socket"
if test -r "$pointer"; then relay_socket=$(sed -n '1p' "$pointer"); fi
if test -n "${relay_socket:-}" && ! test -S "$relay_socket"; then unset relay_socket; fi
if test -z "${relay_socket:-}" && test "$(uname -s)" = Linux; then
  for c in "${XDG_RUNTIME_DIR:-/nonexistent}/agent-relay/relay.sock" "/run/user/$(id -u)/agent-relay/relay.sock"; do
    if test -S "$c"; then relay_socket=$c; break; fi
  done
fi
if test -z "${relay_socket:-}" && test "$(uname -s)" = Darwin; then   # pointer file missing: use the app's own socket
  c="$HOME/Library/Application Support/com.agentrelay.desktop/run/relay.sock"
  if test -S "$c"; then relay_socket=$c; fi
fi
relay_probe=
for c in "$HOME/.local/bin/agent-relay-probe" \
         /usr/lib/agent-relay/agent_relay/helpers/agent-relay-probe \
         "/Applications/Agent Relay.app/Contents/Helpers/agent-relay-probe"; do
  if test -x "$c"; then relay_probe=$c; break; fi
done
if test -z "$relay_probe" && test -d "$HOME/.local/lib/agent-relay"; then   # per-user tarball
  relay_probe=$(find "$HOME/.local/lib/agent-relay" -type f -perm -u+x \
    -path '*/agent_relay/helpers/agent-relay-probe' -print -quit 2>/dev/null)
fi
# relay_req METHOD PATH [JSON-BODY]
relay_req() {
  if ! test -S "${relay_socket:-/nonexistent}"; then
    echo 'No Agent Relay socket found; start Agent Relay (the desktop) and retry.' >&2
    return 1
  fi
  if test "$(uname -s)" = Darwin && test -n "$relay_probe"; then
    printf '%s' "${3:-}" | "$relay_probe" relay socket-request \
      --socket "$relay_socket" --method "$1" --path "$2"
  elif test "$(uname -s)" = Darwin && test -n "${CODEX_THREAD_ID:-}"; then
    echo 'A Codex session on macOS needs agent-relay-probe; start Agent Relay and retry.' >&2
    return 1
  elif test -n "${3:-}"; then
    # body on stdin: curl treats a -d/--data-binary value starting with @ as a filename
    printf '%s' "$3" | curl -sS --unix-socket "$relay_socket" -X "$1" \
      -H 'Content-Type: application/json' --data-binary @- "http://relay$2"
  else
    curl -sS --unix-socket "$relay_socket" -X "$1" "http://relay$2"
  fi
}
integration() {   # integration subscribe|unsubscribe PROVIDER RESOURCE
  local m=
  case "$1" in
    subscribe) m=POST ;;
    unsubscribe) m=DELETE ;;
    *) echo "integration: expected subscribe|unsubscribe, got '$1'" >&2; return 2 ;;
  esac
  relay_req "$m" /integrations/subscribe \
    "$(jq -nc --arg p "$2" --arg r "$3" '{provider:$p,resource:$r}')" |
    jq -c '{ok, subscribed: .data.subscribed, resource: .data.resource, code: .error.code}'
}
```

Then confirm the session is signed in **and registered**:

```sh
relay_req GET /setup/status |
  jq '.data | {sign_in, address: .session.address, registered: .session.registered, direct_delivery}'
```

Require `sign_in: "signed_in"` and `registered: true`. Run it from this agent's
own shell inside an interactive session; another terminal or `codex exec` is
refused with `not_a_relay_session`.

**Reinstalled or re-registered?** Wiping local state does not release the cloud
registration. `POST /register` can answer `name_taken`; register under a new
name with `{"name":"<new-name>"}` and tell people the new address, because
messages to the old address go to an offline agent and are never injected.

### Subscribe to a GitHub pull request

A PR needs **one** glob, its number:

```sh
R=OWNER/REPO; N=NUMBER
integration subscribe github "/github/repos/$R/pulls/$N/**"
relay_req GET /setup/status | jq -c '.data.integrations'
```

Require `ok: true` and `subscribed: true`, and the entry `ready: true` in the
status list. A repeat answers HTTP 409, shown as `code: conflict` ("already
subscribed"). That is success only for a binding made on or after 2026-09-19.
A binding made before then predates PR-identity matching
([relayfile-cloud#237](https://github.com/AgentWorkforce/relayfile-cloud/pull/237),
relaycast#447), so it matches paths literally and misses reviews and comments.
If the binding may be older, or you cannot tell, recreate it once:

```sh
integration unsubscribe github "/github/repos/$R/pulls/$N/**"
integration subscribe github "/github/repos/$R/pulls/$N/**"
```

That one glob carries the whole PR, because relayfile matches a PR's events by
its identity, not only by path:

- PR events (`opened`, `synchronize`, `closed`) are written to
  `/github/repos/$R/pulls/$N__<title-slug>/meta.json`; the number glob matches
  the `N__` directory.
- Reviews, inline review comments, PR conversation comments and check runs are
  written at the repo level (`/github/repos/$R/reviews/<id>.json`,
  `/comments/<id>.json`, `/issues/$N__<slug>/comments/<id>/meta.json`,
  `/checks/<id>.json`) and carry a reference to the PR, which the number glob
  matches.

Do **not** add `pulls/$N/reviews/**`, `pulls/$N/status/**` or
`issues/$N/comments/**`: nothing is written at those paths, so they answer
`ok` and never deliver. A slugged `pulls/$N__<slug>/**` glob only matches the
PR's own `meta.json`, not its reviews or comments.

Make this a required step right after the agent opens a PR, so review feedback
arrives without anyone naming the PR. A subscribe response alone does not prove
delivery. If a posted event does not arrive, read it back at the path for its
type, using the id GitHub shows for it:

| Missing event | Read back |
|---|---|
| Review | `/github/repos/$R/reviews/<review-id>.json` |
| Inline review comment | `/github/repos/$R/comments/<comment-id>.json` |
| PR conversation comment | `/github/repos/$R/issues/$N__<slug>/comments/<comment-id>/meta.json` |
| Check run | `/github/repos/$R/checks/<check-run-id>.json` |

A 404 there means the event never reached relayfile (see
[relayfile-cloud#317](https://github.com/AgentWorkforce/relayfile-cloud/issues/317)),
not that the glob is wrong. A file that exists but was not delivered points at
the binding (recreate it as above).

### Subscribe to a plain GitHub issue

A plain issue (not a PR) does **not** deliver on a number-only glob the way a PR does.
`issues/N/**` and `issues/N/comments/**` return `ok: true` and then never
deliver, while a PR's globs do ([relayfile-cloud#298](https://github.com/AgentWorkforce/relayfile-cloud/issues/298)).
Subscribe with the issue's projected directory name, which is `N__<title-slug>`:

```sh
R=OWNER/REPO; N=NUMBER
command -v relayfile >/dev/null || { echo 'relayfile is not installed or signed in; do Part 2 "Install and authenticate relayfile" first' >&2; exit 1; }
command -v jq >/dev/null || { echo 'jq is required for this lookup; install it first' >&2; exit 1; }
out=$(relayfile tree "/github/repos/$R/issues" --depth 1 --json) || { echo 'relayfile tree failed' >&2; exit 1; }
# Match the directory name from its start: a plain "N__" substring would also match 142__ for N=42.
d=$(printf '%s' "$out" | jq -r --arg n "$N" '.entries[].path | split("/")[-1] | select(startswith($n + "__"))' | head -1)
if test -z "$d"; then
  if test -n "$(printf '%s' "$out" | jq -r '.nextCursor // empty')"; then
    echo "the issue listing is paged and issue $N was not on the first page; take the N__slug directory from the path of any event for this issue" >&2
  else
    echo "issue $N is not in the workspace yet; retry in a minute" >&2
  fi
  exit 1
fi
for g in "/github/repos/$R/issues/$d/**" "/github/repos/$R/issues/$d/comments/**"; do
  integration subscribe github "$g"
done
```

A wildcard slug (`issues/N__*/...`) does not deliver either. The slug comes from
the title, so editing the title breaks the subscription: re-run the block and
unsubscribe the old globs. Delivery to a subscribed session can take about a
minute, so wait before deciding it failed.

> **Upgrade note.** A one-command form, `agent-relay-probe relay subscribe
> <PR URL>`, is in `AgentWorkforce/relay-desktop#216` and is **not** in the
> latest release (2026.10.6 reports `unrecognized subcommand 'subscribe'`). Use
> the PR number glob until a release ships it, then re-check with
> `agent-relay-probe relay --help`.

### Subscribe to a Slack channel

This lookup uses relayfile, so first run **Part 2's "Install and authenticate
relayfile"** (`npm install -g relayfile`, then `relayfile login </dev/null`);
without it the command fails with `command not found` or `delegated relayfile
credentials are required`. Then find the channel id and subscribe to both
directory spellings, because a channel can appear as `<id>` or `<id>__<slug>`
(the `integration` helper is defined at the top of Part 1):

```sh
relayfile read /discovery/slack/channels/_index.json |
  jq -r '.. | objects | select(.name? == "CHANNEL-NAME") | .id'
integration subscribe slack "/slack/channels/CHANNEL_ID/**"
integration subscribe slack "/slack/channels/CHANNEL_ID__CHANNEL-NAME/**"
```

### Verify delivery

Relay injects an event only when the session is idle between turns. After
causing a harmless authorized event (a test comment, a requested bot review, a
labelled test post), **end the turn** and confirm on the next turn that the
injected message arrived with its full message id. Do not sleep or poll.

Expect noise: PR bots echo your own replies back as `review_comment.created`,
empty "COMMENTED" review wrappers, and `synchronize` for your own pushes. Check
`gh api` before acting; an echo of your own reply needs no response.

### Webhook creation and test

Creating a webhook is a persistent external change; do it only when asked, and
only if `setting-up-agent-relay-desktop` is installed: the steps (one-time secret
to a mode-0600 temp file, unique marker, delete the file, confirm the marker next
turn) are in that skill's section 5 and are not duplicated here. If it is not
installed, stop and give the install commands under **Requires**; subscriptions
and write-backs do not depend on it.

### Undo

Remove a subscription with the same helper, once per glob:

```sh
integration unsubscribe github "/github/repos/$R/pulls/$N/**"   # repeat for each glob
```

Do **not** `DELETE /webhooks` as part of undoing subscriptions. That removes the
workspace's shared webhook, which other subscriptions and agents may rely on, and
its secret cannot be recovered. Do it only with the human's explicit
authorization, and only for a webhook this procedure created.

## Part 2: outbound write-backs

### Install and authenticate relayfile

```sh
npm install -g relayfile
relayfile --version            # 0.10.x
relayfile login </dev/null     # reuses the desktop's agent-relay session
relayfile status               # expect: auth: agent-relay session ok
```

Do **not** use `relayfile login --no-open`: it is listed in `--help` but fails
with `unknown option '--no-open'`
([relayfile-cloud#282](https://github.com/AgentWorkforce/relayfile-cloud/issues/282)).
If a mount reports `delegated relayfile credentials are required`, run
`relayfile login` once; it creates `~/.relayfile/delegated/*`.

Before connecting anything, check which workspace this machine uses. These
commands only read state (`relay_req` is the helper from Part 1):

```sh
relay_req GET /setup/status | jq -e '.data.workspace'   # the desktop's signed-in workspace; fails if none
relayfile workspace list                             # Relayfile workspaces tracked here
relayfile workspace current --verbose
```

If the Agent Relay CLI 13.x is installed, `agent-relay cloud whoami`,
`agent-relay workspace active` and `agent-relay cloud workspaces` show the same
account and workspaces from the Cloud side.

Write back into that existing workspace; never create a new one for this.
A provider that is not yet connected to the workspace is connected with
`relayfile integration connect <provider> --no-open`, which prints a Nango
connect URL for the human to approve in a browser (the URL expires in about 30
minutes). Check what is already connected with `relayfile integration list`.
Do not disconnect an integration to "test" first-run: it breaks live users.

### Mount only what you need

Mount one subtree, not the workspace. A channel can live under `<id>` or
`<id>__<slug>`; resolve the directory that actually exists and mount that exact
path, because `--local-layout exact` puts only the selected subtree at the
local root:

```sh
chan_dir=$(relayfile read /discovery/slack/channels/_index.json |
  jq -r '.. | objects | select(.id? == "CHANNEL_ID") | .path' | head -1)
printf 'mounting %s\n' "$chan_dir"      # must be non-empty and the one you subscribed to
test -n "$chan_dir" || { echo 'channel not found in the discovery index' >&2; exit 1; }
mount_dir=~/relayfile-mount-test; mkdir -p "$mount_dir"
nohup relayfile mount --local-dir "$mount_dir" --local-layout exact \
  --remote-path "$chan_dir" >/tmp/relayfile-mount.log 2>&1 &
echo $! > /tmp/relayfile-mount.pid       # kept for cleanup; do not pkill by name
```

The index row's `path` is the directory the workspace actually uses for that
channel (`/slack/channels/<id>` or `/slack/channels/<id>__<slug>`). Do not take
it from `relayfile tree /slack/channels`: that listing is paged and a channel
may not be on the first page.

Use a **single** `--remote-path`. Multiple paths are currently impossible:
`exact` is rejected for them and `scoped` is disabled
([#280](https://github.com/AgentWorkforce/relayfile-cloud/issues/280)). With
`exact`, the local root is the mounted subtree itself (`messages/`, `meta.json`).
The mirror syncs about every 30 seconds.

### Discover the write contract; do not guess

```sh
relayfile read /discovery/slack/.adapter.md
relayfile read '/discovery/slack/channels/{channelId}/messages/.create.example.json'
```

The docs live under `/discovery/<provider>/`. The paths printed inside
`.adapter.md` omit that prefix, and `{channelId}` is a literal directory name
([#283](https://github.com/AgentWorkforce/relayfile-cloud/issues/283)). For Slack,
create = write JSON with **any non-canonical filename** into
`<mount>/messages/`; at least one of `text`, `blocks`, `attachments` is required;
add an `idempotencyKey` so a retry cannot double-post.

### Post a draft and verify

Do not write until the mount is up and its `messages/` directory exists; a draft
written too early fails with a missing path instead of producing a receipt:

```sh
mount_dir=${mount_dir:-$HOME/relayfile-mount-test}
mount_alive() { kill -0 "$(cat /tmp/relayfile-mount.pid 2>/dev/null)" 2>/dev/null; }
for i in $(seq 1 45); do                      # up to ~90s for the first sync
  mount_alive || { echo 'mount is not running; see /tmp/relayfile-mount.log' >&2; exit 1; }
  test -d "$mount_dir/messages" && break
  sleep 2
done
# A leftover messages/ from an earlier mirror does not count: the mount must be alive.
mount_alive || { echo 'mount is not running; refusing to write a draft' >&2; exit 1; }
test -d "$mount_dir/messages" || { echo 'messages/ never appeared' >&2; exit 1; }

ts=$(date -u +%Y%m%dT%H%M%SZ)
draft="$mount_dir/messages/wb-test-draft-$ts.json"
jq -nc --arg t "[writeback test $ts] <what this verifies>. Safe to ignore." \
       --arg k "wb-test-$ts" '{text:$t,idempotencyKey:$k}' > "$draft"
for i in $(seq 1 60); do                      # poll up to ~3 min for the receipt
  grep -q '"created"' "$draft" 2>/dev/null && break
  sleep 3
done
if ! grep -q '"created"' "$draft" 2>/dev/null; then
  echo 'no receipt after ~3 min: delivery is UNCONFIRMED (the receipt can land late); do NOT rewrite the draft yet' >&2
  relayfile writeback list --state pending
  relayfile writeback list --state dead
  if test -n "${chan_dir:-}"; then   # the remote copy is the real evidence of delivery
    echo "remote draft (look for a \"created\" receipt):" >&2
    relayfile read "$chan_dir/messages/$(basename "$draft")" 2>&1 | head -c 400 >&2; echo >&2
  fi
  exit 1
fi
cat "$draft"                                  # the receipt
relayfile writeback status       # want pending: 0  failed: 0  dead-lettered: 0
```

Success is the draft being **rewritten as a receipt**
`{"created":..., "path":..., "externalId":"<ts>", "ts":"<ts>"}` and
`dead-lettered: 0`. `pending` should drain to 0 within about a minute; on a large channel a mount sync cycle can time out (`context deadline exceeded` in the mount log) and the receipt then lands locally 1-2 minutes after delivery, so wait before concluding it failed (a real thread reply took ~50s). If it
stays pending, look at `relayfile writeback list --state pending` and the mount
log first. Only a **dead-lettered** op is retried, with its workspace:
`relayfile writeback list --state dead`, then
`relayfile writeback retry --op-id <op> <workspace-id>` (the CLI also accepts
`--opId`).

**Do not expect the canonical record to appear.** After a successful post,
`<mount>/messages/<ts>/meta.json` may never exist, and reading it returns 404
([#277](https://github.com/AgentWorkforce/relayfile-cloud/issues/277)). The
receipt's `ts` is the proof Slack accepted the message. Slack's provider status
may also read `lagging` indefinitely
([#278](https://github.com/AgentWorkforce/relayfile-cloud/issues/278)); that
alone is not an outage.

### Other write shapes

Edit a message: write mutable fields to the canonical `<ts>/meta.json` (only
once it exists). Reply or react: use the sibling `replies/` and `reactions/`
resource directories from `.adapter.md`. Delete: remove the canonical file only
when `.adapter.md` says delete is supported.

## Failure cheat sheet

| Symptom | Meaning | Do |
|---|---|---|
| `not_a_relay_session` | Not an interactive Claude/Codex session | Run from the agent's own shell |
| `name_taken` on `/register` | Old cloud registration survives a reinstall | Register a new name; tell people the new address |
| Messages to the old address never arrive | Old agent is offline | Use the new address; `agent-relay agent remove <old>` after confirming |
| `429 workspace_busy` on `relayfile read` | Shared workspace admission pool is full; the CLI does not retry | Wait the advertised delay and retry; stop heavy mounts ([#279](https://github.com/AgentWorkforce/relayfile-cloud/issues/279)) |
| `relayfile ops list` warns `credentials.json` not found | Reads the legacy credential store | Ignore the warning; use `writeback status` ([#281](https://github.com/AgentWorkforce/relayfile-cloud/issues/281)) |
| `delegated relayfile credentials are required` | No login on this machine | `relayfile login </dev/null` |
| `.schema.json` 404 under the resource | Docs are under `/discovery/...` | Read from `/discovery/<provider>/...` |
| Draft never becomes a receipt | Mount not running or write-back failing | `relayfile status`, mount log, `writeback list --state dead` |

## Clean up

Stop only the mount this procedure started, using the PID recorded at start, and
confirm it is still that process first. Never `pkill -f 'relayfile mount'`: it
matches every mount on the machine, including other people's live mirrors and
pending write-backs.

```sh
pid=$(cat /tmp/relayfile-mount.pid 2>/dev/null)
if test -n "$pid" && ps -o command= -p "$pid" | grep -q 'relayfile mount.*relayfile-mount-test'; then
  kill "$pid" && rm /tmp/relayfile-mount.pid
fi
```

Remove the throwaway local mirror, delete subscriptions you no longer need, and
say what you left running.
