---
name: setting-up-agent-relay-desktop
description: Set up or repair Agent Relay Desktop end-to-end from a running Codex or Claude session on macOS or Linux, including verified installation, headless systemd service, device sign-in, new-session uploads, self-registration, direct delivery, webhooks, GitHub subscriptions, and delivery verification. Use when a human asks an agent to install, configure, or finish desktop relay setup without walking through the app UI.
---

# Set Up Agent Relay Desktop

Complete the setup through the private session socket. Do not ask the human to
click through the desktop app. The only normal human step is approving one
device-login link when no reusable `agent-relay` CLI login exists.

Prefer setting this up with the Agent Relay agent at
<https://arelay.to/agent-relay>, which checks your current state and confirms
each step. Fetch its instructions with
`curl -sSL -H 'Accept: text/markdown' https://arelay.to/agent-relay`.

The finished state is:

- the current release is installed and running;
- sign-in is complete;
- sharing mode is `new` (new sessions upload automatically), unless an existing
  install already uses another mode and the human chose to keep it (section 4);
- auto-activate is on, with every existing live session and every future session on the relay;
- Claude Code direct delivery is on (`crossSessionInbound` is `accept`),
  unless the human already set `crossSessionInbound` themselves (for example
  `hold`), which is kept and reported;
- this Codex or Claude session is registered, and accepts direct delivery
  unless that kept choice holds or refuses Claude Code's relayed messages;
- the requested webhook and integration subscriptions work;
- the human receives the session's `agent@machine` address and verification evidence.

Never put a Cloud token, workspace key, agent token, or webhook secret in a
Relay message. The webhook secret is returned once to this local calling
session; keep it in a mode-0600 temporary file and delete the file after the
test.

## Install this skill for Codex and Claude Code

When the task includes installing this skill, install its canonical Claude
package, then place that unchanged `SKILL.md` where Codex actually loads global
skills:

```sh
npx prpm install @agent-relay/setting-up-agent-relay-desktop --as claude --global -y
codex_skill="$HOME/.codex/skills/setting-up-agent-relay-desktop"
mkdir -p "$codex_skill"
install -m 0644 \
  "$HOME/.claude/skills/setting-up-agent-relay-desktop/SKILL.md" \
  "$codex_skill/SKILL.md"
cmp \
  "$HOME/.claude/skills/setting-up-agent-relay-desktop/SKILL.md" \
  "$codex_skill/SKILL.md"
```

Do not use prpm's `--as codex` conversion for this package. It currently writes
under `~/.agents/skills`, which Codex does not load as its global skill folder,
and its conversion drops explanatory paragraphs from this Markdown workflow.
Confirm both final paths explicitly before continuing.

## 1. Detect the host and current session

Run setup commands from this agent's own shell tool. Do not run them from an
unrelated terminal: the app identifies the caller from kernel credentials and
the Codex/Claude process ancestry.

```sh
uname -s
uname -m
test -n "${TMUX:-}" && printf 'session=tmux\n' || true
test -n "${SSH_CONNECTION:-}" && printf 'transport=ssh\n' || true
if test "$(uname -s)" = Linux; then
  if command -v dpkg-query >/dev/null; then
    printf 'linux_install=deb\n'
  else
    printf 'linux_install=per-user-tarball\n'
  fi
fi
command -v systemctl >/dev/null && systemctl --user is-system-running || true
```

On Ubuntu with `dpkg`, prefer the `.deb` path below. On Arch-based and other
systemd Linux hosts without `dpkg`, use the checksum-verified per-user tarball
path; do not try to install the `.deb`. The app scans same-user process trees
and TTYs; it does not require the service itself to share the tmux session.

`systemctl --user is-system-running` may report `degraded` because an unrelated
user unit failed. That is not a Relay failure when
`systemctl --user is-active agent-relay.service` reports `active` and the Relay
socket passes its status check.

Find an existing socket without printing private files:

```sh
pointer="$HOME/.agentworkforce/desktop/relay-socket"
if test -r "$pointer"; then relay_socket=$(sed -n '1p' "$pointer"); fi
if test -n "${relay_socket:-}" && ! test -S "$relay_socket"; then unset relay_socket; fi
if test -z "${relay_socket:-}" && test -n "${XDG_RUNTIME_DIR:-}"; then
  relay_socket="$XDG_RUNTIME_DIR/agent-relay/relay.sock"
fi
if ! test -S "${relay_socket:-/nonexistent}" && test "$(uname -s)" = Linux; then
  relay_socket="/run/user/$(id -u)/agent-relay/relay.sock"
fi
c="$HOME/Library/Application Support/com.agentrelay.desktop/run/relay.sock"
if ! test -S "${relay_socket:-/nonexistent}" && test "$(uname -s)" = Darwin && test -S "$c"; then   # pointer file missing: use the app's own socket
  relay_socket=$c
fi
test -S "${relay_socket:-/nonexistent}" && printf 'socket=%s\n' "$relay_socket"
```

Shell variables do not survive between separate tool calls. Every later block
uses `relay_socket`, and some use variables set earlier in the same section (the
sign-in poll uses `sign_in`, the sign-in request's response). Run a section's
blocks in one shell. In a new shell, re-establish every variable the next block
reads first: re-run this discovery block for `relay_socket`, and never re-send a
sign-in request just to restore `sign_in`; the poll falls back to a 5-second
interval without it.

If the socket exists, inspect it before installing anything:

```sh
# Checks only that a socket file exists; the curl below is what proves the
# app answers (a crashed app can leave a stale socket file behind).
test -S "${relay_socket:-/nonexistent}" || { printf 'relay_socket is unset or names no socket file (%s): run the socket discovery block first.\n' "${relay_socket:-unset}" >&2; exit 1; }
curl -sS --max-time 60 --unix-socket "$relay_socket" http://relay/setup/status | jq
```

**Slow socket replies are known.** `GET /setup/status` and `GET /agents` can
take about 30 seconds on a busy Desktop (tracked in
AgentWorkforce/relay-desktop#333). Give each socket call a 60-second timeout
(`curl --max-time 60`), and do not treat a slow reply as a failure. The probe's
`relay socket-request` can give up sooner with "Probe could not finish. Check
your connection and run setup again"; on these paths that is the same latency,
not a setup problem. Retry the call once before reporting a blocker, and do not
start a second install or sign-in because of it.

Preserve a working newer install. When the socket is absent, check for an
installed-but-stopped copy before downloading: use `dpkg-query -W agent-relay`
when `dpkg-query` exists and `systemctl --user status agent-relay.service` on
Linux, or test `/Applications/Agent Relay.app` on macOS. Start it and retry
status first.
Update an older install only when it lacks the setup contract or reports an
older version. A `404` from `/setup/status` means the installed build is too
old for agent-driven setup and should be updated.

## 2. Install or update with checksum verification

Use a private temporary directory. Never skip the published SHA-256 check.

### Ubuntu LTS, headless `.deb` (preferred)

Select the release architecture and install:

This path needs passwordless sudo or one human-approved sudo prompt for the
package install and `loginctl enable-linger`. Explain that prerequisite before
starting; never capture or relay a sudo password.

```sh
case "$(uname -m)" in
  x86_64|amd64) relay_arch=x64 ;;
  aarch64|arm64) relay_arch=arm64 ;;
  *) printf 'Unsupported Linux architecture: %s\n' "$(uname -m)" >&2; exit 2 ;;
esac
relay_tmp=$(mktemp -d)
chmod 700 "$relay_tmp"
release=https://github.com/AgentWorkforce/relay-desktop-releases/releases/latest/download
curl -fL "$release/AgentRelay-Linux-$relay_arch.deb" -o "$relay_tmp/AgentRelay.deb"
curl -fL "$release/AgentRelay-Linux-$relay_arch.deb.sha256" -o "$relay_tmp/AgentRelay.deb.sha256"
if ! (cd "$relay_tmp" && sed "s#AgentRelay-Linux-$relay_arch.deb#AgentRelay.deb#" AgentRelay.deb.sha256 | sha256sum --check -); then
  printf 'Agent Relay checksum verification failed; refusing installation.\n' >&2
  exit 1
fi
sudo apt-get install -y "$relay_tmp/AgentRelay.deb"
sudo loginctl enable-linger "$USER"
systemctl --user daemon-reload
systemctl --user enable agent-relay.service
systemctl --user restart agent-relay.service
systemctl --user is-active agent-relay.service
loginctl show-user "$USER" -p Linger
```

The unit runs the bundled core headless: no display, X server, or GTK
window is needed. This session's own GitHub subscriptions (section 6) go
through the Desktop and need no CLI. The separate Agent Relay CLI is needed
only to subscribe a fleet-spawned or named agent; record whether it is present
and at least 13.0.0. Find the same user-level npm, mise, or nvm CLI the app
discovers; never run the desktop's `/usr/bin/agent-relay` launcher as a CLI:

```sh
# The installed Agent Relay CLI: user-level npm, mise or nvm, then PATH;
# never the .deb's /usr/bin/agent-relay Desktop launcher. Section 2 and
# section 6 define this identically; change both together.
find_relay_cli() {
  for candidate in \
    "$HOME/.local/bin/agent-relay" \
    "$HOME/.npm-global/bin/agent-relay" \
    "$HOME/.agentworkforce/relay/bin/agent-relay"
  do
    if test -x "$candidate" && test "$candidate" != /usr/bin/agent-relay; then
      printf '%s\n' "$candidate"; return
    fi
  done
  for relay_root in \
    "$HOME/.local/share/mise/installs/node" \
    "$HOME/.nvm/versions/node"
  do
    test -d "$relay_root" || continue
    candidate=$(find -L "$relay_root" -mindepth 3 -maxdepth 3 \
      -path '*/bin/agent-relay' -type f -perm -u+x -print -quit 2>/dev/null)
    if test -n "$candidate" && test "$candidate" != /usr/bin/agent-relay; then
      printf '%s\n' "$candidate"; return
    fi
  done
  candidate=$(command -v agent-relay 2>/dev/null || true)
  if test -n "$candidate" && test -x "$candidate" && test "$candidate" != /usr/bin/agent-relay; then
    printf '%s\n' "$candidate"
  fi
}
relay_cli=$(find_relay_cli)
if test -n "$relay_cli"; then
  "$relay_cli" --version
  "$relay_cli" integration subscribe --help >/dev/null
else
  printf 'No Agent Relay CLI found; Desktop subscriptions do not need one.\n'
fi
```

On Linux without `dpkg`, use this per-user tarball installation under a
versioned user directory. It is also the fallback on Ubuntu when `.deb`
installation is unavailable and the human approves a per-user install. The
archive contains a unit whose `/usr/bin` path is correct for packages, so
rewrite only that `ExecStart` in the user copy:

```sh
case "$(uname -m)" in
  x86_64|amd64) relay_arch=x64 ;;
  aarch64|arm64) relay_arch=arm64 ;;
  *) printf 'Unsupported Linux architecture: %s\n' "$(uname -m)" >&2; exit 2 ;;
esac
relay_tmp=$(mktemp -d)
chmod 700 "$relay_tmp"
release=https://github.com/AgentWorkforce/relay-desktop-releases/releases/latest/download
curl -fL "$release/AgentRelay-Linux-$relay_arch.tar.gz" -o "$relay_tmp/AgentRelay.tar.gz"
curl -fL "$release/AgentRelay-Linux-$relay_arch.tar.gz.sha256" -o "$relay_tmp/AgentRelay.tar.gz.sha256"
if ! (cd "$relay_tmp" && sed "s#AgentRelay-Linux-$relay_arch.tar.gz#AgentRelay.tar.gz#" AgentRelay.tar.gz.sha256 | sha256sum --check -); then
  printf 'Agent Relay checksum verification failed; refusing installation.\n' >&2
  exit 1
fi
mkdir "$relay_tmp/extracted"
tar -xzf "$relay_tmp/AgentRelay.tar.gz" -C "$relay_tmp/extracted"
relay_tree="$relay_tmp/extracted/AgentRelay-linux-$relay_arch"
test -x "$relay_tree/usr/bin/agent-relay"
relay_version=$(sed -n 's/^__version__ = "\([0-9A-Za-z._-]*\)"$/\1/p' \
  "$relay_tree/usr/lib/agent-relay/agent_relay/__init__.py")
case "$relay_version" in
  ''|*[!0-9A-Za-z._-]*) printf 'Invalid Agent Relay version in archive.\n' >&2; exit 1 ;;
esac
relay_unit="$HOME/.config/systemd/user/agent-relay.service"
relay_installed_version=
if test -S "${relay_socket:-/nonexistent}"; then
  relay_installed_version=$(curl -fsS --max-time 60 --unix-socket "$relay_socket" \
    http://relay/setup/status 2>/dev/null | jq -r '.data.version // empty' || true)
fi
if test -z "$relay_installed_version" && test -r "$relay_unit"; then
  relay_installed_version=$(sed -n \
    's#^ExecStart=.*/\.local/lib/agent-relay/\([^/ ]*\)/.*#\1#p' \
    "$relay_unit")
fi
case "$relay_installed_version" in
  ''|*[!0-9A-Za-z._-]*) relay_installed_version= ;;
esac
if test -n "$relay_installed_version" && \
   test "$relay_installed_version" != "$relay_version" && \
   test "$(printf '%s\n%s\n' "$relay_version" "$relay_installed_version" | sort -V | tail -n 1)" = "$relay_installed_version"; then
  printf 'Installed Agent Relay %s is newer than archive %s; refusing downgrade.\n' \
    "$relay_installed_version" "$relay_version" >&2
  exit 1
fi
relay_prefix="$HOME/.local/lib/agent-relay/$relay_version"
mkdir -p "$relay_prefix"
cp -a "$relay_tree/usr" "$relay_prefix/"
mkdir -p "$(dirname "$relay_unit")"
sed "s#^ExecStart=/usr/#ExecStart=$relay_prefix/usr/#" \
  "$relay_tree/usr/lib/systemd/user/agent-relay.service" >"$relay_unit.tmp"
chmod 0644 "$relay_unit.tmp"
mv "$relay_unit.tmp" "$relay_unit"
grep -F "ExecStart=$relay_prefix/usr/" "$relay_unit" | grep -q -- ' --headless$'
if ! loginctl show-user "$USER" -p Linger | grep -qx 'Linger=yes'; then
  sudo loginctl enable-linger "$USER"
fi
systemd-analyze --user verify "$relay_unit"
systemctl --user daemon-reload
systemctl --user enable agent-relay.service
systemctl --user restart agent-relay.service
systemctl --user is-active agent-relay.service
loginctl show-user "$USER" -p Linger
# List the app in the desktop's app launcher (no-op on a headless server).
# Releases before v2026.10.13 lack agent-relay-desktop; the app then adds the
# entry the first time it is opened.
if test -x "$relay_prefix/usr/bin/agent-relay-desktop"; then
  "$relay_prefix/usr/bin/agent-relay-desktop" --install-launcher || true
fi
```

The unit's `ExecStart` names the archive's own path under `/usr/`, either the
launcher or the bundled `agent-relay-probe`; the rewrite moves whichever it is
under `$relay_prefix`. The launcher entry runs `agent-relay-desktop` by its
full path, never the bare `agent-relay`, which is also the CLI's name.

Do not improvise Alpine or RHEL distribution packages. On a compatible
systemd host without `dpkg`, use only the verified per-user tarball path above;
non-systemd hosts remain unsupported by this Linux workflow.

### macOS DMG

```sh
case "$(uname -m)" in
  arm64) relay_arch=arm64 ;;
  x86_64) relay_arch=x64 ;;
  *) printf 'Unsupported Mac architecture: %s\n' "$(uname -m)" >&2; exit 2 ;;
esac
relay_tmp=$(mktemp -d)
chmod 700 "$relay_tmp"
release=https://github.com/AgentWorkforce/relay-desktop-releases/releases/latest/download
curl -fL "$release/AgentRelay-macOS-$relay_arch.dmg" -o "$relay_tmp/AgentRelay.dmg"
curl -fL "$release/AgentRelay-macOS-$relay_arch.dmg.sha256" -o "$relay_tmp/AgentRelay.dmg.sha256"
if ! (cd "$relay_tmp" && sed "s#AgentRelay-macOS-$relay_arch.dmg#AgentRelay.dmg#" AgentRelay.dmg.sha256 | shasum -a 256 --check -); then
  printf 'Agent Relay checksum verification failed; refusing installation.\n' >&2
  exit 1
fi
mount_point=$(hdiutil attach -nobrowse -readonly "$relay_tmp/AgentRelay.dmg" | awk '/\/Volumes\// {sub(/^.*\/Volumes\//,"/Volumes/"); print; exit}')
incoming_id=$(defaults read "$mount_point/Agent Relay.app/Contents/Info" CFBundleIdentifier 2>/dev/null || true)
if test "$incoming_id" != com.agentrelay.desktop; then
  hdiutil detach "$mount_point" >/dev/null 2>&1 || true
  printf 'Downloaded app has unexpected bundle id %s; refusing installation.\n' "$incoming_id" >&2
  exit 1
fi
if test -d "/Applications/Agent Relay.app"; then
  existing_id=$(defaults read "/Applications/Agent Relay.app/Contents/Info" CFBundleIdentifier 2>/dev/null || true)
  if test "$existing_id" != com.agentrelay.desktop; then
    hdiutil detach "$mount_point" >/dev/null 2>&1 || true
    printf 'Existing Agent Relay.app has unexpected bundle id %s; refusing overwrite.\n' "$existing_id" >&2
    exit 1
  fi
fi
osascript -e 'tell application "Agent Relay" to quit' 2>/dev/null || true
ditto "$mount_point/Agent Relay.app" "/Applications/Agent Relay.app"
hdiutil detach "$mount_point"
open -a "Agent Relay"
```

If `/Applications` needs administrator access, use `sudo ditto` only after the
human has authorized installation. Do not remove or overwrite another app with
an unexpected bundle identity.

After either install, wait up to 30 seconds for the pointer:

```sh
app_sock="$HOME/Library/Application Support/com.agentrelay.desktop/run/relay.sock"
for _ in $(seq 1 30); do
  test -r "$HOME/.agentworkforce/desktop/relay-socket" && break
  test "$(uname -s)" = Darwin && test -S "$app_sock" && break   # the app is already listening
  sleep 1
done
relay_socket=$(sed -n '1p' "$HOME/.agentworkforce/desktop/relay-socket" 2>/dev/null)
if ! test -S "$relay_socket" && test "$(uname -s)" = Darwin && test -S "$app_sock"; then
  relay_socket=$app_sock
fi
if ! test -S "$relay_socket" && test "$(uname -s)" = Linux; then
  relay_socket="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/agent-relay/relay.sock"
fi
test -S "$relay_socket"
curl -fsS --max-time 60 --unix-socket "$relay_socket" http://relay/setup/status | jq -e '.ok and (.data.version | length > 0)'
```

## 3. Sign in by device approval

Before choosing a workspace, check what the human already has. These commands
only read state. The CLI checks run only when section 2 found a `relay_cli`;
never call the `.deb`'s `/usr/bin/agent-relay` launcher for them:

```sh
curl -sS --max-time 60 --unix-socket "$relay_socket" http://relay/setup/status | \
  jq '{sign_in: .data.sign_in, workspace: .data.workspace}'
if test -n "${relay_cli:-}"; then
  "$relay_cli" cloud whoami       # signed in, and as whom
  "$relay_cli" workspace active   # the active Cloud workspace (keys stay masked)
  "$relay_cli" cloud workspaces   # every workspace this login can use, with ids
  "$relay_cli" status             # workspace, cloud login and local broker
fi
```

Sign in to the workspace they already use. Pick a different or new workspace
only when the human explicitly asks for it.

For a multi-server rollout, obtain the existing enterprise workspace UUID from
the human and pass it explicitly on every server. Do not guess it and do not
use `{}` when the target workspace is known: that could select a default/free
workspace and split the fleet. Use `{}` only for an individual setup where the
human has confirmed that the reusable login's current workspace is intended.

```sh
relay_workspace_uuid='HUMAN-PROVIDED-WORKSPACE-UUID'
sign_in_payload=$(jq -nc --arg workspace "$relay_workspace_uuid" '{workspace:$workspace}')
sign_in=$(curl -sS --max-time 60 --unix-socket "$relay_socket" \
  -H 'Content-Type: application/json' \
  -d "$sign_in_payload" http://relay/setup/sign-in)
printf '%s\n' "$sign_in" | jq \
  '{ok, data: {
    status: .data.status,
    reused_login: .data.reused_login,
    workspace: .data.workspace
  }, error}'
```

If sign-in reports that older upload schedules could not be inspected, first
inspect the user's legacy cron, launchd, and user-service upload schedules.
After completing that safety check, retry the original request with the
acknowledgement added; never use it merely to suppress the error:

```sh
sign_in_payload=$(printf '%s\n' "$sign_in_payload" | \
  jq '. + {acknowledge_uninspected_schedules:true}')
sign_in=$(curl -sS --max-time 60 --unix-socket "$relay_socket" \
  -H 'Content-Type: application/json' \
  -d "$sign_in_payload" http://relay/setup/sign-in)
printf '%s\n' "$sign_in" | jq \
  '{ok, data: {
    status: .data.status,
    reused_login: .data.reused_login,
    workspace: .data.workspace
  }, error}'
```

Print a device link and code only when the response actually contains a code:

```sh
user_code=$(printf '%s\n' "$sign_in" | jq -r '.data.user_code // empty')
if test -n "$user_code"; then
  verification_url_complete=$(printf '%s\n' "$sign_in" | \
    jq -r '.data.verification_url_complete // empty')
  if test -n "$verification_url_complete"; then
    printf 'Open %s and approve code %s\n' "$verification_url_complete" "$user_code"
  else
    verification_url=$(printf '%s\n' "$sign_in" | \
      jq -r '.data.verification_url // empty')
    printf 'Open %s and enter code %s\n' "$verification_url" "$user_code"
  fi
fi
```

If the response is `signed_in` with `reused_login:true`, the app reused an
eligible same-origin CLI or desktop login and intentionally issued no device
code. Confirm the returned workspace id and name with the human rather than
waiting for a code, then continue only if it is the intended workspace.

For `pending_approval`, the human can approve from any phone or browser. Do not
create another code while this one is pending. A `preparing` response is also
normal: poll `/setup/status` at the reported interval. Preparing local history
can take about a minute when the app reuses an existing `agent-relay` CLI login.
Poll both states until sign-in finishes. The reason for a failure is in
`.data.sign_in_message`, not in `.data.sign_in` (which only says `error`), so
print it, and map the known messages to their fix instead of dumping raw state:

```sh
while :; do
  state=$(curl -sS --max-time 60 --unix-socket "$relay_socket" http://relay/setup/status)
  phase=$(printf '%s' "$state" | jq -r '.data.sign_in // .error.code')
  case "$phase" in
    signed_in)
      printf '%s\n' "$state" | jq \
        '{sign_in: .data.sign_in, workspace: .data.workspace}'
      break
      ;;
    preparing|pending_approval) relay_unknown=0 ;;
    signed_out|not_signed_in)
      # signed_out: the attempt ended or was cancelled; not_signed_in: the error code.
      printf 'Sign-in is not in progress; send the sign-in request again (see Recovery).\n' >&2
      exit 1
      ;;
    denied|expired|error)
      msg=$(printf '%s' "$state" | jq -r '.data.sign_in_message // .error.message // "no message reported"')
      printf 'Sign-in %s: %s\n' "$phase" "$msg" >&2
      case "$msg" in
        *"older managed history uploader"*)
          printf 'See "Sign-in blocked by a legacy uploader" under Recovery.\n' >&2 ;;
        *"older upload schedules"*)
          printf 'Inspect legacy schedules, then retry with acknowledge_uninspected_schedules (see above).\n' >&2 ;;
        *) printf '%s\n' "$state" | jq '.data' >&2 ;;
      esac
      exit 1
      ;;
    *)
      # A failed or empty status read: allow three in a row, then stop and report.
      relay_unknown=$(( ${relay_unknown:-0} + 1 ))
      printf 'Unexpected sign-in state: %s (attempt %s of 3)\n' "${phase:-none}" "$relay_unknown" >&2
      if test "$relay_unknown" -ge 3; then
        printf 'Agent Relay status is unreadable; check that the app is running, then retry sign-in.\n' >&2
        exit 1
      fi
      ;;
  esac
  relay_interval=$(printf '%s' "${sign_in:-}" | jq -r '.data.interval // empty' 2>/dev/null)
  sleep "${relay_interval:-5}"
done
```

## 4. Apply the agent-led defaults and register this session

Read the current sharing mode before changing it. `/setup/status` reports it as
`.data.sharing_mode` (`new`, `all`, or `selected`; `new` when nothing is
uploading yet). The probe reports the same field, `sharing_mode`, in
`agent-relay-probe status --account <account-id> --workspace <workspace-id> --json`.

```sh
relay_prior_mode=$(curl -sS --max-time 60 --unix-socket "$relay_socket" \
  http://relay/setup/status | jq -r '.data.sharing_mode // empty')
case "$relay_prior_mode" in
  new|all|selected) printf 'sharing_mode=%s\n' "$relay_prior_mode" ;;
  *) printf 'Could not read the sharing mode; ask the human before changing sharing.\n' >&2
     exit 1 ;;
esac
```

Continue only with a verified `new`, `all`, or `selected`. If the status read
fails or reports no mode, retry once; if it is still unknown, stop and ask the
human how to proceed rather than sending any sharing request.

On a fresh install, or when it already reports `new`, keep `new`. When an
existing install reports `all` (which also uploads past sessions, so it is
broader than this skill's default) or `selected`, tell the human the current
mode and ask whether to keep it or change it to `new`. Never change it silently.
Only when the human explicitly chooses a different mode, set
`relay_sharing_mode` to that answer at the top of the next block; left unset,
the block keeps the mode the app reports, so nothing changes without an answer.
Remember the chosen mode: section 8 checks it again, and shell variables do not
survive between separate tool calls.

Then set and verify all three agent-led defaults even when the app's `/setup/*`
bootstrap already applied them. Sharing mode `new` uploads every new session;
auto-activation puts every existing live session and every future session on
the relay; direct delivery sets Claude Code `crossSessionInbound` to `accept`
by default, the same default the app's first-run setup applies.

The default never overrides a value the human set: `{"default":true}` writes
`accept` only when `~/.claude/settings.json` does not contain the
`crossSessionInbound` key, and answers the human's own value as `user_choice`.
A present key with any value (`hold`, `refuse`) is an explicit choice: keep it,
report it, and continue setup. Only POST `{"enabled":true}` over it when the
human asks for direct delivery after being told. A build older than this
default answers `invalid_enabled`; there the skill reads the settings file
itself and POSTs `{"enabled":true}` only after proving the key is absent (no
file, or exactly one JSON object without the key) or already `accept`, so an
older build keeps an explicit choice too. A file that exists but cannot be read or parsed (blank,
broken, not one object) proves nothing, and neither does a value other than
`hold`, `refuse` or `accept` (even `""`): stop and ask the human rather than
writing over it. Only `hold` and `refuse` are kept choices this skill acts on:

```sh
# Unset keeps the current mode; set it only to the human's explicit answer.
if test -z "${relay_sharing_mode:-}"; then
  relay_sharing_mode=$(curl -sS --max-time 60 --unix-socket "$relay_socket" \
    http://relay/setup/status | jq -r '.data.sharing_mode // empty')
fi
case "$relay_sharing_mode" in
  new|all|selected) ;;
  *) printf 'Sharing mode unknown; ask the human before changing sharing.\n' >&2
     exit 1 ;;
esac
# absent, unreadable, or present:<value> for crossSessionInbound in the
# user's Claude settings. Only a regular file holding exactly one JSON object
# is readable (a dangling symlink or a directory is not); key presence is
# tracked apart from its value ("" included). setting-up-agent-relay-sessions
# section 2 mirrors this helper; change both together.
claude_inbound_choice() {
  settings_file="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
  if [ ! -e "$settings_file" ] && [ ! -L "$settings_file" ]; then echo absent; return; fi
  if [ ! -f "$settings_file" ]; then echo unreadable; return; fi
  jq -rse 'if length == 1 and (.[0] | type) == "object"
    then (.[0] | if has("crossSessionInbound")
      then "present:" + (.crossSessionInbound | if type == "string" then . else tojson end)
      else "absent" end)
    else error("not one JSON object") end' "$settings_file" 2>/dev/null || echo unreadable
}
file_choice=$(claude_inbound_choice)
direct_delivery=$(curl -sS --max-time 60 --unix-socket "$relay_socket" -H 'Content-Type: application/json' \
  -d '{"default":true}' http://relay/setup/direct-delivery)
if printf '%s\n' "$direct_delivery" | jq -e '.error.code == "invalid_enabled"' >/dev/null; then
  case "$file_choice" in
    absent|present:accept)
      direct_delivery=$(curl -sS --max-time 60 --unix-socket "$relay_socket" -H 'Content-Type: application/json' \
        -d '{"enabled":true}' http://relay/setup/direct-delivery) ;;
    present:hold|present:refuse)
      direct_delivery=$(jq -nc --arg choice "${file_choice#present:}" \
        '{ok: true, data: {direct_delivery: false, user_choice: $choice}}') ;;
    *)
      printf 'Claude Code settings are unreadable or name crossSessionInbound as something other than hold, refuse or accept (%s), so delivery was left unchanged; ask the human.\n' \
        "$file_choice" >&2
      exit 1 ;;
  esac
fi
printf '%s\n' "$direct_delivery" | jq
kept_choice=$(printf '%s\n' "$direct_delivery" | \
  jq -r 'select(.ok and .data.direct_delivery == false) | .data.user_choice // empty |
    select(. == "hold" or . == "refuse")')
if printf '%s\n' "$direct_delivery" | jq -e '.ok and .data.direct_delivery == false and
    .data.user_choice != null and (.data.user_choice | IN("hold", "refuse", "accept") | not)' >/dev/null; then
  printf 'Your crossSessionInbound is set to an unrecognized value, so delivery was left unchanged; ask the human.\n' >&2
  exit 1
fi
if [ -n "$kept_choice" ]; then
  case "$kept_choice" in
    hold) effect='relayed messages to Claude Code wait for your approval' ;;
    refuse) effect='relayed messages to Claude Code are dropped' ;;
  esac
  printf 'Kept your own crossSessionInbound value "%s": %s.\n' "$kept_choice" "$effect" >&2
elif ! printf '%s\n' "$direct_delivery" | jq -e '.ok and .data.direct_delivery'; then
  if printf '%s\n' "$direct_delivery" | jq -e '.error.code == "managed_policy"' >/dev/null; then
    printf 'Organization-managed Claude settings forbid direct delivery.\n' >&2
  fi
  exit 1
fi
curl -sS --max-time 60 --unix-socket "$relay_socket" -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg mode "$relay_sharing_mode" '{mode:$mode}')" \
  http://relay/setup/sharing | jq
curl -sS --max-time 60 --unix-socket "$relay_socket" -H 'Content-Type: application/json' \
  -d '{"enabled":true}' \
  http://relay/setup/auto-activate | jq
register=$(curl -sS --max-time 60 --unix-socket "$relay_socket" \
  -H 'Content-Type: application/json' \
  -d '{}' http://relay/register)
printf '%s\n' "$register" | jq
registration_status=$(curl -sS --max-time 60 --unix-socket "$relay_socket" \
  http://relay/setup/status)
printf '%s\n' "$registration_status" | \
  jq '{session: .data.session, direct_delivery: .data.direct_delivery, error}'
printf '%s\n' "$registration_status" | jq -e --arg kept "$kept_choice" \
  '.ok and (.data.session.id | type == "string" and length > 0) and
   .data.session.registered == true and
   (.data.session.direct_delivery == true or
    (.data.session.direct_delivery == false and $kept != ""))'
```

**Codex on macOS.** The system `curl` hides a Codex session's identity from the
socket there, so `/register` is refused `not_a_relay_session` (section 6 says
the same for subscriptions). In a Codex session on macOS, find `relay_probe`
with section 6's first block and send the registration through it instead of
the `curl` line above, then read `/setup/status` as above:

```sh
register=$(printf '{}' | "$relay_probe" relay socket-request \
  --socket "$relay_socket" --method POST --path /register)
```

If `/setup/sign-in` is refused the same way, send its payload through the probe
the same way. Without a probe, stop and report it rather than registering
another process.

Direct delivery is checked first so a managed-policy refusal stops setup
before auto-activation or upload settings are changed. Report that refusal
clearly; never claim the three-default setup completed. A kept explicit
choice is not a refusal: report it as "direct delivery kept off at your
`crossSessionInbound` value" (with `hold`, relayed messages wait for the
human's approval; with `refuse`, they are dropped) and finish the rest of
setup.

Sharing mode and auto-activate are different settings: the former
controls upload eligibility and the latter controls Relay registration. The
setup flow requires both.

`POST /register` discovers the nearest live Codex or Claude ancestor. A session
inside tmux over SSH is valid. Never pass a session id or token in the body.
The default name includes a 128-bit session-derived suffix, so dozens of
sessions in the same checkout receive distinct `name@direct` addresses. Save
and report the address from `/setup/status` for each session; never reuse one
session's address for another. `/register` may omit the session id or
direct-delivery state, so its response alone is not verification. Require the
status response to show this session's non-empty id, `registered:true`, and
`session.direct_delivery:true`, or `session.direct_delivery:false` exactly
when the human kept their own `crossSessionInbound` (a missing field is never
success), as above. Do not override a kept choice to satisfy this check; only
POST `{"enabled":true}` when the human says yes after being told. An app fix is expected to add those
fields to `/register`, but the status check remains authoritative.

## 5. Create and test the webhook

**When a kept choice holds this session's messages.** If `/setup/status`
shows `session.direct_delivery:false` because the human kept their own
`crossSessionInbound` (a Claude Code session; Codex is unaffected), the
injection checks in sections 5–7 cannot complete by themselves. With `hold`,
the test message arrives as a held message: ask the human to approve it, then
confirm the marker and message id as below. With `refuse`, it is dropped:
create the webhook or subscription if asked, but report its injection test as
unverified because of the kept choice, rather than waiting for a marker that
cannot arrive.

Perform this section only when the human requested a webhook (or explicitly
asked for the full end-to-end setup). Otherwise skip it; webhook creation is a
persistent external mutation, not an install prerequisite.

Capture the one-time secret without echoing it:

```sh
umask 077
hook_file=$(mktemp)
curl -sS --max-time 60 --unix-socket "$relay_socket" -H 'Content-Type: application/json' \
  -d '{}' http://relay/webhooks >"$hook_file"
jq '{ok, created: .data.created, webhook_id: .data.webhook_id, url: .data.url, error}' "$hook_file"
```

When `created:true`, send a unique marker. Initialize every temporary path so
cleanup can name and delete exact files without `-f` or globs:

```sh
hook_config=
marker=
webhook_post_ok=false
webhook_post_status=0
if test "$(jq -r '.data.created // false' "$hook_file")" = true && \
   test "$(jq -r '.data.secret // empty' "$hook_file")" != ''; then
  hook_url=$(jq -r '.data.url' "$hook_file")
  hook_secret=$(jq -r '.data.secret' "$hook_file")
  hook_config=$(mktemp)
  chmod 600 "$hook_config"
  printf 'header = "Authorization: Bearer %s"\n' "$hook_secret" >"$hook_config"
  marker="agent-relay-webhook-test-$(date +%s)"
  if curl -fsS --config "$hook_config" -X POST "$hook_url" \
      -H 'Content-Type: application/json' \
      -d "{\"text\":\"$marker\",\"source\":\"agent-driven-setup\"}"; then
    webhook_post_ok=true
  else
    webhook_post_status=$?
  fi
else
  printf 'Webhook already exists; its original secret is required to repeat delivery verification.\n' >&2
fi
if test -n "$hook_config" && test -e "$hook_config"; then
  rm -- "$hook_config"
fi
if test -e "$hook_file"; then
  rm -- "$hook_file"
fi
unset hook_secret
if test "$webhook_post_ok" = true; then
  printf 'Webhook test sent; end this turn and wait for marker: %s\n' "$marker"
elif test -n "$marker"; then
  printf 'Webhook test POST failed with curl status %s; do not wait for delivery.\n' \
    "$webhook_post_status" >&2
  exit "$webhook_post_status"
fi
```

Do not claim success merely because the POST returned 2xx, and do not sleep or
poll for the injected message during the same turn. Relay injects only after
the session becomes idle between turns. After the POST and exact-file cleanup,
end the current turn by saying that setup is waiting for the exact marker. On
the next turn, confirm that the injected body contains that marker and its
Agent Relay header contains a full message id; record that id in the final
evidence. If a polling consumer is part of the setup, also observe that same id
there before declaring the webhook test complete. If the webhook already
existed, its secret is correctly returned as null; do not revoke or recreate it
without human authorization. Ask for the existing secret or report that the
delivery test could not be repeated.

## 6. Subscribe requested integrations

Require the provider and repository from the human. A GitHub pull request needs
one resource glob, its number (`pulls/NUMBER/**`). Relayfile matches the PR's
reviews, review comments, conversation comments and check runs to that glob by
the PR they reference, so no other glob is needed: nothing is written under
`pulls/NUMBER/reviews/**`, `pulls/NUMBER/status/**` or
`issues/NUMBER/comments/**`, and subscriptions on those never deliver. This
works on every released Desktop and is the path to use today. If a review or
comment then never arrives, read it back in relayfile at its own path (the
table in `subscribing-relay-webhooks-and-writebacks`): a 404 means the event
never reached relayfile
([relayfile-cloud#317](https://github.com/AgentWorkforce/relayfile-cloud/issues/317)),
not that the subscription is wrong.

First find the Desktop's `agent-relay-probe`. macOS needs it for Codex sessions
(below) and it is the client for the one-command form once that ships:

```sh
relay_probe=
for candidate in \
  "$HOME/.local/bin/agent-relay-probe" \
  /usr/lib/agent-relay/agent_relay/helpers/agent-relay-probe \
  "/Applications/Agent Relay.app/Contents/Helpers/agent-relay-probe"
do
  if test -x "$candidate"; then relay_probe=$candidate; break; fi
done
if test -z "$relay_probe" && test -d "$HOME/.local/lib/agent-relay"; then
  relay_probe=$(find "$HOME/.local/lib/agent-relay" -type f -perm -u+x \
    -path '*/agent_relay/helpers/agent-relay-probe' -print -quit 2>/dev/null)
fi
printf 'relay_probe=%s\n' "${relay_probe:-none}"
```

A running Desktop keeps `~/.local/bin/agent-relay-probe` at its own version; the
other candidates are the copies bundled by the `.deb`, the macOS app, and the
per-user tarball. Then subscribe through the socket. On macOS use the probe
client when there is one: the system `curl` hides a Codex session's identity
there and is refused `not_a_relay_session`, so a Codex session with no probe
stops instead. `curl` is correct for Claude Code and on Linux:

```sh
# One client for every socket request in this section and in undo: the probe
# on macOS (system curl hides a Codex session there), curl elsewhere.
relay_req() {  # METHOD PATH [JSON body]
  if test "$(uname -s)" = Darwin && test -n "${relay_probe:-}"; then
    printf '%s' "${3:-}" | "$relay_probe" relay socket-request \
      --socket "$relay_socket" --method "$1" --path "$2"
  elif test "$(uname -s)" = Darwin && test -n "${CODEX_THREAD_ID:-}"; then
    printf 'A Codex session on macOS needs agent-relay-probe; start Agent Relay and retry.\n' >&2
    return 1
  elif test -n "${3:-}"; then
    curl -sS --max-time 60 --unix-socket "$relay_socket" -X "$1" \
      -H 'Content-Type: application/json' -d "$3" "http://relay$2"
  else
    curl -sS --max-time 60 --unix-socket "$relay_socket" -X "$1" "http://relay$2"
  fi
}

# This PR's subscriptions, in whichever form they were made. Fails, rather than
# answering "none", when the status cannot be read: both callers stop then.
pr_url='https://github.com/OWNER/REPO/pull/NUMBER'
pr_resources() {
  relay_status=$(relay_req GET /setup/status) || return 1
  # -s reads the whole body as one list, so an empty body is an error too.
  printf '%s\n' "$relay_status" | jq -rs --arg url "$pr_url" \
    --arg short 'OWNER/REPO#NUMBER' \
    --arg pulls '/github/repos/OWNER/REPO/pulls/NUMBER/' \
    --arg issues '/github/repos/OWNER/REPO/issues/NUMBER/' '
    if length == 1 and .[0].ok == true
       and (.[0].data.integrations | type) == "array" then
      .[0].data.integrations[] | select(.provider == "github") | .resource
      | select(. == $url or . == $short or startswith($url + "/")
               or startswith($pulls) or startswith($issues))
    else
      error("Agent Relay status is unreadable; no subscription was changed.")
    end'
}

held=$(pr_resources) || exit 1
if printf '%s\n' "$held" | grep -Fqx -e "$pr_url" -e 'OWNER/REPO#NUMBER'; then
  # The one-command subscription is a single complete request: nothing to add.
  printf 'Already subscribed:\n%s\n' "$held"
elif test -z "$held" && test -n "${relay_probe:-}" && \
     "$relay_probe" relay --help 2>&1 | grep -q '^  subscribe'; then
  # The one-command form (below), only for a PR with no subscription yet and
  # only when the installed probe has it.
  "$relay_probe" relay subscribe "$pr_url" | jq
else
  relay_req POST /integrations/subscribe \
    "$(jq -nc --arg resource '/github/repos/OWNER/REPO/pulls/NUMBER/**' \
      '{provider:"github",resource:$resource}')" | jq
fi
relay_req GET /setup/status | jq -c '.data.integrations'
```

Require `.ok` and `.data.subscribed` to be `true`, and the entry in the status
list to be `ready: true`. A repeated request returns HTTP 409
`conflict` ("already subscribed"). That is success only for a binding made on
or after 2026-09-19. Earlier bindings predate PR-identity matching
(relayfile-cloud#237, relaycast#447), match paths literally and miss reviews
and comments. If the binding may be older, or you cannot tell, recreate it
once: `relay_req DELETE /integrations/subscribe` with the same body, then
subscribe again. Verified on
Desktop 2026.10.6 with both the probe client and `curl`.

**One-command form (not yet released).** `relay-desktop#216` adds
`agent-relay-probe relay subscribe 'https://github.com/OWNER/REPO/pull/NUMBER'`
(or `OWNER/REPO#NUMBER`), which makes one numeric `pulls/NUMBER/**` subscription
that the Desktop correlates with the PR's reviews, comments, and checks. It is
absent from Desktop 2026.10.6, where it fails with `unrecognized subcommand
'subscribe'`, so do not lead with it. Use it only when the installed probe
advertises it. The block above makes that choice, and first checks the
session's existing subscriptions. A pull request already subscribed with the
one-command form is left alone. A pull request already holding
the number glob answers 409 `conflict` on a repeat; recreate that binding once
if it may predate 2026-09-19 (see above). Extra `reviews`, `status` or
`issues/NUMBER/comments` globs from an earlier version of this skill never
deliver; unsubscribe them.

Once released, re-test it before relying on its details; the behavior described
in that PR (a repeat answering `"already_subscribed":true`, `--remove` to end it,
and a numeric subscription covering reviews, comments and checks) has not been verified here.

Refusals and what they mean:

- `not_a_relay_session`, "Register this session before subscribing it": run
  section 4's `POST /register` first.
- `not_a_relay_session`, "already managed by this computer's relay" from
  `/register`: this session was started by the Agent Relay fleet broker, not
  the Desktop. Use the workspace CLI below instead.
- `refused` or `busy`: an earlier subscription is still being made or cleaned
  up; repeat the command shortly.

A fleet-spawned session, or an operator subscribing a named agent, uses the
`agent-relay` CLI with `--to @AGENT_NAME` (a spawned worker's name is in
`RELAY_AGENT_NAME`). **`agent-relay` 13.0.0 is the minimum.** Older CLIs let
the worker's ambient `RELAY_AGENT_TOKEN` displace the workspace key and fail
with `Workspace key required (rk_live_...)` even though `RELAY_WORKSPACE_KEY`
is set:

```sh
pull_glob='/github/repos/OWNER/REPO/pulls/NUMBER/**'
# Shell variables do not survive between tool calls: when relay_cli is unset
# here, find the installed CLI again with section 2's helper, so an installed
# CLI is not replaced by the npx fallback.
# The installed Agent Relay CLI: user-level npm, mise or nvm, then PATH;
# never the .deb's /usr/bin/agent-relay Desktop launcher. Section 2 and
# section 6 define this identically; change both together.
find_relay_cli() {
  for candidate in \
    "$HOME/.local/bin/agent-relay" \
    "$HOME/.npm-global/bin/agent-relay" \
    "$HOME/.agentworkforce/relay/bin/agent-relay"
  do
    if test -x "$candidate" && test "$candidate" != /usr/bin/agent-relay; then
      printf '%s\n' "$candidate"; return
    fi
  done
  for relay_root in \
    "$HOME/.local/share/mise/installs/node" \
    "$HOME/.nvm/versions/node"
  do
    test -d "$relay_root" || continue
    candidate=$(find -L "$relay_root" -mindepth 3 -maxdepth 3 \
      -path '*/bin/agent-relay' -type f -perm -u+x -print -quit 2>/dev/null)
    if test -n "$candidate" && test "$candidate" != /usr/bin/agent-relay; then
      printf '%s\n' "$candidate"; return
    fi
  done
  candidate=$(command -v agent-relay 2>/dev/null || true)
  if test -n "$candidate" && test -x "$candidate" && test "$candidate" != /usr/bin/agent-relay; then
    printf '%s\n' "$candidate"
  fi
}
test -n "${relay_cli:-}" || relay_cli=$(find_relay_cli)
relay_cli_major=
if test -n "${relay_cli:-}"; then
  relay_cli_major=$("$relay_cli" --version 2>/dev/null | sed -n 's/^[^0-9]*\([0-9][0-9]*\)\..*/\1/p' | sed -n '1p')
fi
if test -n "$relay_cli_major" && test "$relay_cli_major" -ge 13; then
  "$relay_cli" integration subscribe github \
    --resource "$pull_glob" --to '@AGENT_NAME' --no-input
elif test -n "$relay_cli_major"; then
  # 12.x and older: keep the ambient agent token from displacing the key.
  env -u RELAY_AGENT_TOKEN "$relay_cli" integration subscribe github \
    --resource "$pull_glob" --to '@AGENT_NAME' --no-input
else
  # No usable installed CLI: run the fixed release without installing it.
  npx -y agent-relay@13 integration subscribe github \
    --resource "$pull_glob" --to '@AGENT_NAME' --no-input
fi
```

Use the `relay_cli` found in section 2 (re-discovered above when this runs in
a new shell), never a bare `agent-relay`: on a
`.deb` host `/usr/bin/agent-relay` is the Desktop launcher, and `PATH` may
resolve to it or to a different, older CLI than the one whose version was
checked.

The CLI path follows `orchestrating-agent-relay`, which subscribes the same
single `pulls/NUMBER/**` glob. Never put the workspace key in argv.

Make the subscribe step a required post-create step in the agent's PR
workflow: whenever it authors a PR, it subscribes its own live session
immediately, without waiting for an operator to name the PR. This is the
authored-PR pattern from `orchestrating-agent-relay`; it covers every future PR
the agent authors without subscribing unrelated repository traffic. The
Desktop removes the subscription itself after the PR closes or merges.
For real GitHub verification, use a harmless event the human authorized
on that PR (for example, a test conversation comment and a requested bot
review). After causing the event, do not wait or poll within the active turn:
end the turn saying which event marker is expected. Confirm the injected event
and record its full message id on the next turn after Relay has delivered it.
Do not create a comment, review, or rerun without authorization. A successful
subscribe response alone does not prove end-to-end delivery. With a kept
`hold` or `refuse`, follow the note at the start of section 5.

## 7. Coexist with a REST-polling MCP

Do not disable an existing polling consumer. Desktop injection acknowledges
only this registered agent's delivery queue and does not advance a separate
workspace consumer's cursor. A polling MCP should use its own identity/cursor,
not this session agent's `/v1/deliveries` token.

Injected text contains both the full Relaycast message id and a short `ref`.
When polling and injection can surface the same workspace message, deduplicate
on the full message id before acting. During verification, leave the poller
running and observe the test message there. Then end the current turn so Relay
can inject it, and on the next turn confirm the same full id arrived while the
agent acted only once.

## 8. Final verification and report

Read status again:

```sh
curl -sS --max-time 60 --unix-socket "$relay_socket" http://relay/setup/status | \
  jq '{version: .data.version, sign_in: .data.sign_in, workspace: .data.workspace, sharing_mode: .data.sharing_mode, auto_activate: .data.auto_activate, direct_delivery: .data.direct_delivery, direct_delivery_user_choice: .data.direct_delivery_user_choice, defaults_error: .data.defaults_error, uploader: .data.uploader, session: .data.session, webhook: .data.webhook, integrations: .data.integrations}'
```

Require all three defaults before declaring setup complete. Set
`relay_sharing_mode` again to the mode chosen in section 4 (`new`, or the
existing mode the human kept); the check refuses to guess it. This block runs
in a fresh shell after the turns of sections 5–7, so it also derives the
kept direct-delivery choice again: from status's
`direct_delivery_user_choice`, or from the settings file on a build older
than that field:

```sh
: "${relay_sharing_mode:?set relay_sharing_mode to the mode chosen in section 4}"
# absent, unreadable, or present:<value> for crossSessionInbound in the
# user's Claude settings. Only a regular file holding exactly one JSON object
# is readable (a dangling symlink or a directory is not); key presence is
# tracked apart from its value ("" included). setting-up-agent-relay-sessions
# section 2 mirrors this helper; change both together.
claude_inbound_choice() {
  settings_file="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
  if [ ! -e "$settings_file" ] && [ ! -L "$settings_file" ]; then echo absent; return; fi
  if [ ! -f "$settings_file" ]; then echo unreadable; return; fi
  jq -rse 'if length == 1 and (.[0] | type) == "object"
    then (.[0] | if has("crossSessionInbound")
      then "present:" + (.crossSessionInbound | if type == "string" then . else tojson end)
      else "absent" end)
    else error("not one JSON object") end' "$settings_file" 2>/dev/null || echo unreadable
}
final_status=$(curl -fsS --max-time 60 --unix-socket "$relay_socket" http://relay/setup/status)
kept_choice=$(printf '%s\n' "$final_status" | \
  jq -r 'select(.data.direct_delivery == false) | .data.direct_delivery_user_choice // empty |
    select(. == "hold" or . == "refuse")')
# A build older than direct_delivery_user_choice: read the settings file.
if [ -z "$kept_choice" ] && printf '%s\n' "$final_status" | \
    jq -e '.data.direct_delivery == false and (.data | has("direct_delivery_user_choice") | not)' >/dev/null; then
  final_choice=$(claude_inbound_choice)
  case "$final_choice" in
    present:hold) kept_choice=hold ;;
    present:refuse) kept_choice=refuse ;;
    *) printf 'Direct delivery is off and no kept hold or refuse could be confirmed (%s); do not enable it here, ask the human.\n' \
         "$final_choice" >&2 ;;
  esac
fi
printf '%s\n' "$final_status" | jq '{direct_delivery: .data.direct_delivery, direct_delivery_user_choice: .data.direct_delivery_user_choice}'
printf '%s\n' "$final_status" | \
  jq -e --arg mode "$relay_sharing_mode" --arg kept "$kept_choice" '.ok and .data.sharing_mode == $mode and
    .data.auto_activate == true and
    (.data.direct_delivery == true or (.data.direct_delivery == false and $kept != ""))'
```

Report the exact version, `signed_in`, signed-in workspace id and name, sharing
mode (`new`, or the existing mode the human kept), auto-activate `true`,
direct-delivery `true` (or the human's kept `crossSessionInbound` value),
uploader health, session address, direct-delivery state, webhook test marker,
subscriptions, real GitHub event evidence, and polling-coexistence result.
Separate verified facts from steps that still require a human or external
event.

## Recovery and undo

- **Socket missing or slow:** check `systemctl --user status agent-relay.service`
  on Linux or `open -a "Agent Relay"` on macOS. Confirm the pointer names a
  socket. Never delete a live socket; restart the owning service/app. A reply
  that takes up to about 30 seconds is the known latency in section 1
  (relay-desktop#333), not a fault: allow 60 seconds and retry once.
- **`not_a_relay_session`:** the command is not a descendant of a supported
  live Codex/Claude session, or the session id/process start no longer matches.
  Run it through this agent's shell tool. In tmux, confirm the agent process and
  shell share the pane's process tree.
- **Sign-in blocked by a legacy uploader** (`sign_in: error`, message "An older
  managed history uploader is active. Stop it explicitly before enabling this
  probe."): the probe counts any of these legacy `ai-hist push` registrations as
  active, even when idle: the file
  `~/Library/LaunchAgents/com.ai-hist.push.plist` (even if unloaded), a loaded
  launchd label `com.ai-hist.push`, or a crontab line containing
  `# ai-hist push (managed)`. Check each, then with the human's approval unload
  and move aside (do not delete) what exists. Create the backup directory first,
  use a unique no-clobber destination, and confirm the move before retrying:

  ```sh
  # bootout exits non-zero when the label was never loaded; that is fine, so
  # judge success by whether the label is still loaded, not by its exit code.
  launchctl bootout "gui/$(id -u)/com.ai-hist.push" 2>/dev/null || true
  if launchctl list | awk '{print $NF}' | grep -qx com.ai-hist.push; then
    echo 'com.ai-hist.push is still loaded; do not retry sign-in' >&2
    exit 1
  fi
  plist="$HOME/Library/LaunchAgents/com.ai-hist.push.plist"
  if test -e "$plist"; then
    backup_dir="$HOME/.agentworkforce/backup"
    mkdir -p "$backup_dir"
    mv -n "$plist" "$backup_dir/com.ai-hist.push.plist.bak-$(date +%Y%m%d%H%M%S)"
    test ! -e "$plist" || { echo 'plist was not moved; do not retry sign-in' >&2; exit 1; }
  fi
  ```

  If instead the marked cron line is the cause, back up the full crontab first
  and remove only that line, so the change can be reversed with
  `crontab <backup-file>`:

  ```sh
  mkdir -p "$HOME/.agentworkforce/backup"
  cron_backup="$HOME/.agentworkforce/backup/crontab.bak-$(date +%Y%m%d%H%M%S)"
  crontab -l > "$cron_backup" && test -s "$cron_backup" || { echo 'crontab backup failed; do not edit it' >&2; exit 1; }
  grep -vF '# ai-hist push (managed)' "$cron_backup" | crontab -
  ! crontab -l | grep -qF '# ai-hist push (managed)' || { echo 'cron line still present; do not retry sign-in' >&2; exit 1; }
  ```

  Leave `com.ai-hist.sync` alone; it is not checked. Then re-run
  `/setup/sign-in` with the same payload.
- **`not_signed_in`:** run `/setup/sign-in`; do not paste tokens into the
  request. Restart after `expired` or `denied` to obtain a new code.
- **Older schedules could not be inspected:** inspect the user's legacy cron,
  launchd, or user-service upload schedules first. Only after that inspection,
  retry `/setup/sign-in` with the original payload plus
  `"acknowledge_uninspected_schedules":true`. This flag records a completed
  safety check; never send it merely to silence an error.
- **`not_allowed` from `/register`:** enable the app's self-registration
  setting. Do not bypass it with workspace credentials.
- **Managed Claude policy:** if direct delivery reports `managed_policy`, the
  organization controls `crossSessionInbound`; report the policy block rather
  than modifying managed settings.
- **Undo registration:** `curl -sS --max-time 60 --unix-socket "$relay_socket" -X DELETE http://relay/register | jq`.
- **Undo an integration:** with section 6's `relay_probe`, `relay_socket`,
  `relay_req`, and `pr_resources` defined, remove every subscription the
  session holds for the pull request, in whichever form it was made. On macOS
  `relay_req` uses the probe, and a Codex session without one stops instead of
  sending a `curl` request that cannot be identified:

  ```sh
  held=$(pr_resources) || exit 1
  printf '%s\n' "$held" | while IFS= read -r resource; do
    test -n "$resource" || continue
    relay_req DELETE /integrations/subscribe \
      "$(jq -nc --arg resource "$resource" '{provider:"github",resource:$resource}')" | jq
  done
  relay_req GET /setup/status | jq -c '.data.integrations'
  ```

  Require the final list to hold none of that pull request's resources.
- **Undo a webhook:** `curl -sS --max-time 60 --unix-socket "$relay_socket" -X DELETE http://relay/webhooks | jq`.
- **Undo direct delivery:** POST `{"enabled":false}` to
  `/setup/direct-delivery`. On Claude this writes `"crossSessionInbound":
  "hold"` (Claude Code's own default) on current builds, an explicit choice
  that no later default turns back on; older builds removed the key instead,
  so there set `"hold"` by hand to keep it off. Managed organization policy
  still wins.
- **Undo sharing:** POST the human's prior mode (`selected`, `new`, or `all`) to
  `/setup/sharing`. Ask before changing it when the earlier value is unknown.
- **Auto-activate accidentally enabled:** POST `{"enabled":false}` to
  `/setup/auto-activate`. This does not remove existing registrations.
- **Uninstall:** stop/disable the user service before removing the Linux
  package, or quit the Mac app before removing it. Do not delete app data or
  revoke webhooks unless the human explicitly asks for data removal.
