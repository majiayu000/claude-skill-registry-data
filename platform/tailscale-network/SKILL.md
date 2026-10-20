---
name: tailscale-network
description: "Connect a Windows or Linux computer in Manus or Cue, including a Cloud Computer or sandbox, to the user's Tailscale network with authorization links for the user’s own browser, device approval, and access to tailnet services."
compatibility: opencode
---

# Connect a computer to Tailscale

“Connect to my Tailscale network” is sufficient. Handle setup and recovery yourself; ask only for a target computer when ambiguous, account/provider choices, necessary credentials or approvals, and a service address when needed. Give a brief starting update and verified result, without repeated waiting messages or worker acknowledgements.

## Configure

Identify the product and environment before presenting computer choices: Cue's default Sandbox is a persistent **Long Sandbox**, even when tools label it simply `sandbox`; Manus's temporary task Sandbox is temporary. Use this distinction in choices, authorization messages and the final result. A generic tool label, `/tmp` path or container hostname does not determine lifetime. If product context is unavailable, describe the environment as “Sandbox” without guessing its lifetime.

Discover the current session's available computers before checking Tailscale. Use a computer explicitly named or chosen by the user for this request. If none was specified and multiple computers are available (including the default sandbox), first ask which to connect, preferably with a native choice card showing actual names and OS when known. A default/current execution environment or an existing Tailscale login is not a user choice; do not silently select it or report the request complete based on it. With only one available computer, identify it and proceed. After selection, use that computer's terminal, not the default sandbox terminal. Record its identity and hostname; keep installation, daemon state and verification there. If unavailable, report that instead of silently switching machines. Never copy Tailscale state between machines.

Use only computers accessible through the current session's tools. In Cue, a Cloud Computer may need to be bound to the Agent; in Manus, it may need to be connected or selected for the task. Account ownership or an Online label alone is insufficient. If the target is unavailable, use the product's actual computer-selection or binding flow, then refresh and verify it before installing; do not invent a settings path or switch targets.

Detect OS/architecture, privileges, addresses/default route and existing Tailscale installation/login first. Reuse a working setup; confirm before replacing an account. Never reset state unless requested. Follow only the matching platform branch.

Cloud Computers and persistent sandboxes (including Cue Long Sandbox) default to persistent connectivity independent of the terminal or interactive login session, unless the user requests otherwise. Include this behavior in the existing device confirmation. On Windows enable Run Unattended; on Linux use an enabled system service or persistent process manager. This lasts only while the environment is running and its Tailscale state is retained; it does not keep a suspended or deleted sandbox online. For a temporary task sandbox, explain that connectivity lasts only while that environment runs and retains its state. On a replacement sandbox, inspect its actual state and obtain fresh authorization if needed; do not copy another sandbox's identity or promise cross-task connectivity.

### Windows

Use native PowerShell on the target, not WSL or a Linux terminal. Read [references/windows.md](references/windows.md) for installation and service handling, then continue with the shared sign-in and verification below. Linux TUN, systemd and link-local workarounds do not apply.

### Linux

Check sudo, `/dev/net/tun`, the existing Tailscale service, and port 1055.

Install the official distribution package if missing. On Ubuntu/Debian, download `https://tailscale.com/install.sh` with bounded, fail-on-error curl, inspect it, then run with sudo. Record the version and remove the installer.

On a Linux cloud computer with usable TUN and network privileges, prefer the vendor service's normal kernel networking. If TUN/privileges are unavailable, or the user requests proxy mode to avoid VPN conflicts, use userspace networking. Preserve an existing healthy mode. For userspace, preserve the vendor systemd unit and add this drop-in, adapting binary paths and choosing another loopback port if occupied:

```ini
# /etc/systemd/system/tailscaled.service.d/20-tailscale-userspace.conf
[Service]
ExecStart=
ExecStart=/usr/sbin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/run/tailscale/tailscaled.sock --port=0 --tun=userspace-networking --socks5-server=127.0.0.1:1055 --outbound-http-proxy-listen=127.0.0.1:1055
```

Reload systemd if changed, enable/start tailscaled, and verify its mode (kernel interface or userspace listener). The proxy serves applications; never point tailscaled's own HTTPS_PROXY at it. Without systemd, use a persistent process manager and explicit state/socket paths; `nohup ... &` may be killed when a terminal tool exits.

Check `tailscale status --json` health and recent daemon logs after startup **and after enrollment**. In a restricted Linux sandbox, kernel rule errors such as unsupported `connmark`/`CONNMARK`, `--nfmask`, or permission-denied netfilter operations mean kernel mode is incompatible even if a peer pong succeeds. For this outbound-access setup, switch once to the userspace drop-in above, preserving the same state, socket, account, hostname and other service environment overrides; restart the single daemon without logout or re-enrollment. Do not disable netfilter/firewalls or change host kernel modules to hide the error. If an existing setup also serves inbound traffic or routes, assess those dependencies before changing mode. Recheck health, identity/IP, peer connectivity and the requested service through the proxy; report unresolved warnings rather than claiming a clean result.

### Link-local-only network detection

Check immediately after startup: with only `169.254.x.x` IPv4/link-local IPv6, Tailscale 1.102.4 can report `v4=false v6=false`, pause its control client, and leave NeedsLogin with empty AuthURL despite working internet.

Confirm those interface/log symptoms and test:

```sh
curl --fail --connect-timeout 5 --max-time 15 'https://controlplane.tailscale.com/key?v=131'
```

If HTTP 200 returns valid JSON containing `publicKey` or `legacyPublicKey`, apply:

```ini
# /etc/systemd/system/tailscaled.service.d/30-tailscale-link-local-network.conf
[Service]
Environment=TS_ASSUME_NETWORK_UP_FOR_TEST=1
```

Reload/restart and verify the daemon received it; setting only the CLI environment is insufficient. Use `sudo env TS_ASSUME_NETWORK_UP_FOR_TEST=1 tailscale ...` for CLI calls if needed. This is a version-sensitive workaround: omit it with normal network detection and revalidate after upgrades. Do not fake cloud-provider variables or weaken TLS/firewalls. If it fails, diagnose the actual new error rather than repeat login attempts.

## Sign in and approve

Start a new node with its real hostname suffix:

```sh
sudo tailscale up --accept-dns=false --accept-routes=false \
  --hostname=tailscale-<hostname-suffix> --timeout=20s
```

On Windows, invoke the installed `tailscale.exe` with these arguments in PowerShell, without `sudo` or a Unix socket. On Linux use the configured socket/environment. Obtain the actual AuthURL from command output/status; a timeout while awaiting login is expected. Retain this attempt until it is demonstrably expired or invalid.

1. By default, return the target node's exact AuthURL as a clickable link. Identify the computer, explain that joining permits access under the tailnet's existing policies and state the connectivity lifetime above. Ask the user to open it in their own browser, choose their account/tailnet, and click **Connect**, then reply when done. Do not open a controlled browser or ask for a provider choice in this path; the user chooses on the website. Never request secrets in chat.
2. After every reply, read the target daemon's current status; “logged in” or “done” is not proof of device authorization. If `NeedsLogin` remains, return the same AuthURL again and explain that signing in alone is insufficient: finish **Connect**. Generate a replacement only if the original attempt has expired or is invalid.
3. If `NeedsMachineAuth`, return a device-admin approval link, preferably the exact device page when known; otherwise use `https://login.tailscale.com/admin/machines` with the observed device name, IP and account/tailnet. Ask the user or their administrator to approve that device and reply. Do not restart login or claim connectivity while approval is pending. Recheck state after their reply and continue verification when Running.

Treat the AuthURL as sensitive: anyone with it may enroll the computer into their tailnet. In a shared or group conversation, warn before posting it and offer a private authorization path. After enrollment, read the actual login account and tailnet from `tailscale status --json` and compare them with the user's intended account/tailnet when known, before accessing peers. If this enrollment is wrong or the user reports a mismatch, log out this new enrollment and obtain a fresh AuthURL. If the intended account is unknown, show the actual account/tailnet in the result for the user to check; do not add a routine confirmation round.

If the user requests browser-assisted authorization instead, open the same AuthURL through the session's browser tools. Reuse a signed-in profile through normal UI, including the chosen provider's OAuth buttons; do not export cookies. Ask for takeover only for an observed password/MFA/CAPTCHA or a tool limitation. Show the actual account, tailnet and device and obtain chat confirmation before clicking Connect; obtain explicit administrator approval before clicking Approve. Verify any action the user already completed instead of asking again.

Keep existing access policies unchanged; do not enable SSH, routes, exit nodes, or Funnel as part of ordinary setup. Resume verification automatically after each completed authorization step.

On managed Cloud Computers or kernel-mode sandboxes, do not select an exit node (`--exit-node`) or accept routes that could redirect the default route or Manus/Cue control traffic, even when requested: this can cut off the management connection and leave the computer unreachable. Explain that this network change is unsupported because it could disconnect the computer. If the user needs further help, direct them to the product's public support or feedback channel specified in the session instructions; do not invent a channel, expose internal references, or claim to have contacted a team or filed a request. Do not experiment with static-route exceptions or rely on an in-session rollback. Userspace proxy mode does not change host routes, but do not switch an existing setup to it without assessing its dependencies.

## Verify and use

- Confirm `BackendState=Running`, `Self.Online=true`, account and node IP; inspect `Health` and apply the Linux compatibility fallback above when indicated; list visible online peers. Probe a relevant peer with `tailscale ping --c=1 --timeout=5s --until-direct=false <peer>`. DERP is a valid connection.
- For a newly configured idle computer, restart Tailscale once through its service or configured persistent process manager (Windows: `Restart-Service Tailscale`; Linux service: tailscaled) and verify the same identity/IP and a peer pong. Preserve state; this does not guarantee survival of computer or sandbox deletion. Do not reboot or sign out just to test.
- Report the actual login account, tailnet, node/IP and verified reachability. If no peer responds, distinguish enrollment from connectivity. Ask which service to access if none was specified.

With native Windows or Linux kernel networking, access tailnet IPs directly. On Windows use `curl.exe` rather than PowerShell's `curl` alias. With `--accept-dns=false`, do not assume system MagicDNS resolution; resolve peer names from Tailscale status or use their IPs. Linux userspace mode supplies a proxy, not system routes; use it yourself for requested services:

```sh
curl --proxy socks5h://127.0.0.1:1055 --connect-timeout 5 --max-time 15 \
  'http://<peer-or-MagicDNS-name>:<port>/<path>'
```

Adapt the proxy address if changed. Verify the actual response; a pong alone does not prove application access. On failure, check proxy use, target listener, access policy, then application authentication. Do not scan unrelated services. For requested SSH access, read [references/ssh.md](references/ssh.md).

References for unfamiliar versions/errors: [userspace networking](https://tailscale.com/docs/concepts/userspace-networking), [CLI](https://tailscale.com/docs/reference/tailscale-cli), [tested network detection](https://github.com/tailscale/tailscale/blob/v1.102.4/net/netmon/state.go), [compatibility switch](https://github.com/tailscale/tailscale/blob/v1.102.4/envknob/envknob.go).
