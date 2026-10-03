---
name: send-to
description: Use when the user types /send-to <session-name> [content], asks to relay/forward something to another Claude Code session on this machine ("tell the other window/terminal about this"), needs to relay something to another HAPI session from inside a HAPI session (the user cited /sessions/<id>, or a session seen in list_peers/inspect_peer), or complains that another window doesn't show up in /list-agents or that messages aren't getting through.
argument-hint: "[target session name] [what to relay; omit to use what just happened in this conversation]"
---

# send-to — relay a message to another Claude Code session on this machine

Built on Claude Code's cross-session messaging: `ListAgents` lists the local peer sessions, `SendMessage` sends plain text by name (or by a `uds:` address). The receiver gets only that text — **none of this session's history, files, or context**.

Inside a HAPI session `SendMessage` remains the default delivery; HAPI's own `mcp__hapi__ping_peer` / `hapi ping-peer` is an acceptable alternative, but **never with force** — for a target it refuses, force means killing everything that side is running (see "HAPI sessions" below).

## Requirements

- Claude Code v2.1.224+, macOS/Linux (not available on native Windows). If `/list-agents` isn't recognized in a session, that session doesn't have the feature.
- Neighboring commands: `/list-agents` (alias `/peers`) shows reachable sessions; `/rename` names a session (only a named session can later be resumed with `claude --resume <name>`). Sending itself has no built-in slash command — which is exactly why this skill exists.
- **Cross-session discovery is isolated by profile; delivery is not isolated by account** (revised 2026-08-10, third revision, settled by a controlled experiment): each session writes its registration file only into its own profile's `sessions/` directory, and ListAgents reads only its own profile's registry — so windows in different profiles are mutually **invisible** to each other. At the delivery layer, though: **`SendMessage` with an explicit address `uds:/tmp/cc-socks/<pid>.sock` reaches straight across login accounts and needs no mutual visibility** — a controlled experiment (2026-08-10, run by the user) had a <account> window and a <account> window, both confirmed to be different login accounts and each absent from the other's ListAgents, and explicit-address delivery succeeded both ways with echoes received on both sides. (This supersedes the earlier "cannot send" conclusion from 2026-08-08 and the mixed sample from 2026-08-09; the method is preserved here — confirm both accounts differ, confirm two-way echo — as the bar for overturning this again in the future.) A session registers at startup (visibility usually within tens of seconds), regardless of whether it has ever sent a message.
- **There are three discovery channels but only one delivery channel**: discovery — `ListAgents` (peers visible within this profile), the identity registry `/tmp/cc-session-registry/` (a voluntarily self-reported name card shared across profiles, see "Identity registry" below), and a raw listing of `/tmp/cc-socks/` (last resort, only pid + mtime). Delivery — `SendMessage`, one channel, in two forms: by name or by `uds:` address. You may never use any other means to get content into the other session — bypassing SendMessage to write to its socket directly, touching another profile's registration/session files or identity-registry entries, switching CLAUDE_CONFIG_DIR to spin up a relay session, taking the session over yourself with `claude --resume`, injecting keystrokes into its terminal via tmux/screen, passing force to `mcp__hapi__ping_peer` / `hapi ping-peer`, a self-made JWT + curl to the hub's `/api/sessions/<id>/messages` — all forbidden, however technically feasible. SendMessage with a `uds:` address is a legitimate form of the official channel and is not covered by this prohibition.

## Steps

1. **Load the tool**: `SendMessage` is a deferred tool — load it first with `ToolSearch("select:SendMessage")`, or a direct call fails with InputValidationError. `ListAgents` needs no loading.
2. **Find the target**: work through a four-tier ladder. The ladder is not a "fall back if you must" sequence — L2 is a standard path on equal footing with L1, just queried differently.
   - **L1 — a hit in `ListAgents`** (visible within this profile): match the first word of the arguments case-insensitively: exact → prefix → substring. Listed names are mostly auto-generated as "dirname-2char" (e.g. `myapp-ec`); users often remember only "myapp" — that's normal input, not an error.
     - **Exactly 1 hit**: an exact or prefix hit → proceed, no extra confirmation needed; a hit found **only by substring** → show the user the full matched name for one confirmation before sending (so "app" can't silently land on "myapp-x7"). All three levels empty means 0 hits — never loosen the matching to fuzzy/edit-distance to manufacture a "hit".
     - **≥2 hits** → show the user the matching candidates (name, status, started) and let them pick via AskUserQuestion. Never pick "the most likely one" on the user's behalf, and never go digging through tmux / processes / the other session's screen to identify it — the listing is the only legitimate source of information.
     - **0 hits** → if the target window was opened moments ago, registration can lag by tens of seconds — re-run ListAgents once before judging. Still 0 → proceed to L2.
   - **L2 — read the identity registry (a standard path)**: 0 hits in `ListAgents` does not mean you're stuck — read `/tmp/cc-session-registry/` first (fields and usage in "Identity registry" below), match against what the user described by project name/account/start time, and filter out entries whose "socket has vanished or whose pid is dead" (two-condition check — see the validity note in "Identity registry" below):
     - Filtering leaves exactly one match → send directly to that entry's `uds:` address. This path is **just as normal as sending by name** — no need to hesitate or double-check with the user first.
     - Filtering still leaves **multiple live entries for the same project** (e.g. an interactive main session plus several independently self-registering Workflow-spawned agents) → always show the user the **human-readable identity** (project name, account, profile, start time, `cmd` summary) for every remaining candidate and let them pick — never decide on the user's behalf. `cmd` flags (such as `-p`/`--effort`) **must never be used as a filtering criterion** — a 2026-08-12 final-review test disproved that approach: every interactive main session on this machine carries `--effort ultracode` in its cmd too, so filtering on it would eliminate 100% of main sessions. An entry whose `cmd` carries `-p`/`--print` is usually a one-shot headless process, which can only serve as a **weak sort hint** in the candidate list (rank it lower) — never a unilateral filter.
     - No matching entry in the registry (the other profile has no registration hook installed — see the coverage-scope note in "Identity registry") → proceed to L3; this does not mean the target doesn't exist.
   - **L3 — the current address-source ladder** (once L2 comes up empty): try in this order:
     1. **What the other side already told you**: if the other window has self-reported an address in a message (the `from` value of a `<cross-session-message from="uds:...">`), reuse it as `to` directly — this is the most reliable source, and it's naturally available in reply scenarios.
     2. **Get the target window to speak first** (the preferred option when it hasn't messaged you yet): ask the user to type, **in the target window**, something like "send a message to <your project/window> saying you're here." Once it arrives, you get the address from `from=`, and the user never has to copy or paste anything, nor understand what a socket is. This is the lowest-cognitive-load option for the user.
     3. **What the user hands you**: the user runs `/list-agents` or checks the statusline **in the target window** to get that window's own address, then pastes it to you. One extra copy step compared to #2, but still doesn't require the user to understand sockets.
     4. **Candidate identification (last resort, usually a dead end)**: list every socket with `ls -lt /tmp/cc-socks/` and read candidates to the user by mtime and pid, **for the user to identify**.
        - **Be clear-eyed about its actual hit rate first**: an ordinary user cannot see, and cannot map, a socket/pid to one of their own windows. the user's own words on 2026-08-12: "I can't see the socket, I don't know either." So unless the user independently happens to know the target window's pid (rare), reading out the list just burns a conversational turn for nothing — **prefer L2 or #1/#2/#3 of L3 whenever they're available.**
        - The one scenario where reading the list is still worthwhile: among the candidates, **exactly one** socket's creation time lines up with something the user just did (e.g. the user says "I just opened a window" and exactly one socket in the list was created within the last few minutes). Even then, this is only **a checkable confirmation point for the user**, not you deciding on their behalf.
        - Hard prohibitions unchanged: never dig through processes/terminals on your own to identify the other party and decide for the user, and never send blind to an address the user hasn't identified.
   - **L4 — file-handoff fallback**: L2 and L3 both come up completely empty, or sending to an address the user identified/self-reported still fails → see "File-handoff fallback" below.
3. **Compose the message (self-containment is a hard rule)**: the receiver shares no context with this session; the message must stand alone:
   - Background: which project, what this is about;
   - Substance: branch names, commit ids, paths, conclusions spelled out in full — never "as we just discussed" or "the plan from earlier";
   - Expected action: what the receiver should do, and whether a reply is needed.
   - If the user gave no content (`/send-to myapp` and nothing else) → take the obvious thing to relay from the current conversation; if unsure what to relay, ask first.
4. **Send**: `SendMessage({to: "<name or uds: address>", summary: "<5-10 word summary>", message: "<body>"})`.
   - The first message to a given peer may fail with an error asking for a `[ref]` confirmation (e.g. `myapp-ec [226d36]`) — the error message shows the exact form to use; **resend copying it verbatim**. This is not a fault.
   - When sending to a `uds:` address (L2/L3), **identify yourself** at the top (which project/profile your window is), since the other side can't see you either. Whether you **block and wait for an echo** before considering the send complete follows the "two echo tiers" rule below.
5. **Report honestly**: a successful send only means the message went out — report "sent", never "they received/read it". When the two sessions' permission-mode classes differ, under default settings the message is **held** at the receiving side pending that user's approval; the hold notice arrives asynchronously and may land after you've already reported — so **the absence of a notice never lets you assert "it wasn't held."** When a hold notice does arrive, relay it honestly: "the message is held at the receiving session and needs approval there (or that session sets crossSessionInbound to accept)" — and don't spam resends over it.

## Two echo tiers (when sending to a uds: address, the L2/L3 distinction)

Sending to a `uds:` address (reachable via either L2 or L3) doesn't uniformly require waiting for an echo — it splits into two tiers based on whether the address is **registry-confirmed**:

- **Registry-confirmed** (all three hold at once: ① the identity-registry entry exists ② its socket still exists **and its pid process is still alive** (a `kill -0`-level check) ③ the entry's project/account matches what the user described): **send directly, no need to block on an echo** — still identify yourself on the first message (which project/profile your window is) and add a zero-cost error-correction invitation like "if you're not <target>, please reply and disregard," but you don't have to wait for that reply before considering it done. Delivery-status reporting still follows the same rule — say "sent" only (hold risk is independent of whether the address is confirmed, and applies regardless).
- **Unconfirmed** (an address narrowed down by L3's process of elimination, a candidate the user identified by ear, or an address self-reported by the other side / handed to you by the user without independent corroboration): still **mandatory to demand an echo** — not to verify the transport, but to **confirm you've got the right person** (an unlisted socket has no name to fall back on; only an echo confirms identity) and to guard against a silent hold swallowing the message on the other end. The first message must include "please reply to confirm receipt; if you're not <expected target>, please reply and disregard." **Without an echo, you may not treat it as delivered** (the other side may be busy, the message may be held pending their approval, or the address may simply be wrong) — and if it warrants it, move to L4 file handoff (real-world result from 2026-08-09: a misdirected send got corrected by a reply from the other side, with zero actual damage — proof this rule works, not just a formality).

## Identity registry

`/tmp/cc-session-registry/` is a name card each session voluntarily writes at startup, translating the "just pid + mtime, unidentifiable to anyone" socket listing from L3 into a human-readable identity — making L2 direct-send a standard path instead of a guessing game.

- **Directory**: `/tmp/cc-session-registry/`, mode `0700` (owner only), created by the registration hook if it doesn't exist. **Not placed inside `/tmp/cc-socks/`** — that directory is created and managed by Claude Code itself, and dropping foreign files into it risks cleanup conflicts.
- **File**: `<pid>.json`, pid aligned with `/tmp/cc-socks/<pid>.sock`, one file per session, which naturally avoids concurrent-write conflicts.
- **Fields**:

  | Field | Meaning | If unavailable |
  |---|---|---|
  | `pid` | Claude Code main-process pid (int) | Always present (no file written if this can't be determined) |
  | `socket` | full path to `/tmp/cc-socks/<pid>.sock` | same as above |
  | `account` | login account email | `"unknown"` |
  | `profile` | basename of `CLAUDE_CONFIG_DIR` | `"default"` |
  | `cwd` | full path of the session's working directory | `"unknown"` |
  | `project` | basename of cwd | `"unknown"` |
  | `session_id` | session_id from the hook's stdin JSON | `"unknown"` |
  | `source` | what triggered the hook (startup/resume/clear/compact) | `"unknown"` |
  | `cmd` | the launch command line of this Claude main process itself, used to distinguish an interactive main session from a derived/headless process | `"unknown"` |
  | `registered_at` | ISO8601 registration time | Always present |

- **Validity filtering**: an entry is valid only while "its socket still exists **and its pid process is still alive**" (a `kill -0`-level check) — **the reading side must filter on both conditions first**; a stale entry whose socket has vanished or whose pid is dead must never be treated as a sendable address. Checking the socket alone isn't enough: the socket file lingers after claude exits (an orphaned socket — confirmed on this machine: a socket file with no process behind it anymore), so a single-condition check produces phantom entries and a false "sendable."
- **Read-side display rule**: when the same project has multiple **live** entries (e.g. Workflow-spawned agents each getting their own socket and self-registering), `cmd` flags **must never be used as a filtering criterion** — every interactive main session on this machine carries flags like `--effort` too, so filtering on them would eliminate all main sessions; an entry whose `cmd` carries `-p`/`--print` is usually a one-shot headless process, which can only serve as a **weak sort hint** in the candidate list (rank it lower). Always present the candidates (project, account, start time, `cmd`) to the user to choose from — never decide on the user's behalf and send straight to one entry; the message may vanish along with a short-lived derived process while still being reported as "sent."
- **Cleanup**: the registration hook removes entries whose "socket has vanished or whose pid is dead" (two-condition check) every time it runs; the whole directory can be `rm -rf`'d at any time with no side effects (each session rebuilds its own entry on its next SessionStart).
- **Nature of this data**: the registry is a name card each session voluntarily self-reports, of the same nature as `ListAgents`' registration — **reading the registry is not surveillance**. The hard prohibition targets "unilaterally digging through processes/terminals by pid and deciding for the user" — that prohibition stands unchanged, and the registry doesn't alter it.
- **Coverage scope**: only sessions in a profile that has this plugin installed (or the equivalent registration hook wired in) will appear in the registry; **no entry in the registry ≠ the target window doesn't exist** — if you can't find it, fall back to L3, and never assert "it's not open" just because the registry came up empty. This is also why the hook needs to be installed and active in **every** profile: skip one profile, and windows in that profile can only ever be found via L3/L4. Real-world test note (two rounds, 2026-08-12): a Workflow-spawned agent is its own claude process with its own socket, but once the project-level settings hook was in place, a spawned agent's entry did not actually appear in the registry — the contamination scenario didn't reproduce. The "always show multiple live entries to the user" fallback rule above doesn't depend on this finding and stays in place regardless.
- **Opt-out**: `touch ~/.claude/.cc-session-registry-off` disables registration and cleanup globally (the hook exits silently when it sees the flag; delete the file to re-enable). What gets registered is identity metadata like the account and project directory — use this switch if you don't want to be listed; once disabled, new sessions are no longer registered (entries registered before the switch get filtered/swept as their sessions exit — the switch itself doesn't purge them instantly), and this machine's windows can only be found via L3/L4.

## HAPI sessions (the user cited /sessions/<id>, or the target is a session on the hub)

Since the HAPI build of the evening of 2026-08-26 (hapi repo main 6c91cfd2) there are two generations of behavior; first know which one the target is:

| Target session | When a hub message arrives (web / phone / `ping_peer`) | `ping_peer` without force |
|---|---|---|
| Terminal session opened after the upgrade (has a native message socket) | The message is written straight into its running Claude; the terminal shows "@ HAPI web/phone · the user themselves❯"; no switch to remote, no process killed; if the write fails it only notifies and keeps the message queued (tested) | Delivered directly |
| Terminal session opened before the upgrade, `HAPI_LOCAL_SOCKET_DELIVERY=0`, Windows | The whole Claude process tree gets SIGTERM (in-flight Workflows, subagents and background shells are lost), then it is relaunched in remote mode; double-space to get the terminal back (tested) | Refused with error `target_local_mode`; the target notices nothing (tested) |
| Offline | If the target's machine has a runner online, an unattended agent is spawned there with the target's stored permission mode to act on the message; an archived session gets restarted; "queued" means the target has not processed it yet (inferred from code) | Wakes it as before |
| Remote mode (controlled from web/phone, or runner-spawned) | Just queued | Delivered directly |

You do not have to tell the generations apart yourself: `ping_peer` carries its own guard and refuses when unsafe. Only four rules:

1. **Never pass `force: true` / `--force`.** The guard refuses precisely because the target is the old generation; the only thing force does is kill it. On a refusal (`target_local_mode`) → take this skill's ladder instead: match `claudeSessionId` from the `inspect_peer` output exactly against `session_id` in `/tmp/cc-session-registry/` entries (drop your own entry first, then apply the validity filter) → `SendMessage` to that `uds:` address; nothing found → L3 → L4.
2. **A message sent through `ping_peer` must open by identifying yourself** (which project and profile your Claude window is): the receiver's UI renders it as "the user themselves", so without that line the other side will act on it as the user's instruction.
3. **Never ping an offline target.** If the user really needs it woken, first relay the offline row of the table verbatim and get item-by-item confirmation; in the report say that "queued" only means queued. `ping_peer` refuses to target itself (`self_target`); don't try it on yourself either.
4. `inspect_peer` / `list_peers` are read-only, use them freely; `inspect_peer` now shows `mode: local|remote|offline` and `claudeSessionId`. Do not exchange a JWT and curl the hub's `/api/sessions/<id>/messages` yourself — that road has no guard, and for an old-generation terminal session it means killing the process.

`SendMessage` (by name or `uds:` address) works for every Claude Code session and remains the default delivery; `ping_peer` is the alternative channel for HAPI targets, with the upside that the message lands in hub history and is visible on the web.

**Excuses vs facts:**

| Excuse | Fact |
|---|---|
| "It was refused, force will get it through" | Refusal = the target is old-generation/fallback mode; force = killing everything it is running. Switch to SendMessage |
| "The target is new-generation, force is harmless" | A new-generation target is never refused, so force is never needed; the cases where force applies are exactly the ones that kill |
| "ping_peer can wake inactive sessions, let me wake it while I'm at it" | Waking = spawning an unattended agent on the other machine, with the other session's permission settings, to act on your message; ask the user first |
| "The hub's official REST API is the same as ping_peer, just curl it" | curl bypasses ping_peer's guard; for an old-generation terminal session it kills the process |
| "The content speaks for itself, no need to say who I am" | The other side sees "the user themselves❯" and will act on your words as the user's instruction |

**Stop the moment any of these crosses your mind:** about to pass force to `ping_peer`; about to run `hapi ping-peer … --force`; about to curl `/api/sessions/<id>/messages`; "let me try it on myself"; "it's offline, I'll just ping it awake".

## File-handoff fallback (L4: the target exists but the message can't reach it)

A cross-profile window can't receive the message, but **the user's hands can cross over** — handing off through the user is a legitimate path, entirely different from bypassing the platform boundary.

**Admission gate (either, otherwise no fallback)**: (a) both L2 (identity registry) and L3 (all four address-source options) have come up completely empty; or (b) you already obtained an address and sent per step 4 — including a verbatim [ref] resend — and it still failed, or you were owed an echo and never got one. A single send error does not constitute "unreachable" — and a [ref] confirmation request is not a fault at all. The fallback is not a convenience exit; L2 is the first choice whenever the target isn't in `ListAgents`.

1. Write what needs relaying into a handoff file following step 3's self-containment rules, saved at an absolute path (e.g. `/tmp/send-to-handoff-<target>-<HHMM>.md`); its content is bound by the same permission limits as in "Boundaries" below — never put an operation this session was denied into the handoff file for the other session to run;
2. Give the user one line they can paste straight into the target window: ``Read /tmp/send-to-handoff-….md and act on it``;
3. Report it straight: the message was **not sent** (it couldn't get through); the handoff file is in place, waiting for the user to paste — never dress "the file is written" up as "it has been relayed"; and until the user confirms they pasted it or the other session actually responds, never proceed as if the handoff content is already known to the other side.

## Boundaries

- Entries labeled Remote Control (other machines/web sessions) are **reply-only, cannot initiate** — if the match lands on one of these, explain that to the user instead of forcing a send.
- HAPI sessions in remote mode: their process is a non-interactive child hapi spawned; whether it registers a uds socket, and whether SendMessage reaches a human there, are both unverified. For such targets use `ping_peer` (without force — the message is only queued, no process is killed) or the L4 file handoff.
- To continue a whole conversation or share full context, use `claude --resume <name>`, not a message; for big files or long history, send the path and let the receiver read it itself.
- Permission boundary: never offload an operation this session was denied or would be blocked from doing onto another session **in any form** — messages, handoff files, and paste-lines for the user are all equally bound by this.

## Common mistakes

| Symptom | Fix |
|---|---|
| SendMessage fails with InputValidationError | Tool not loaded via ToolSearch first — back to step 1 |
| Error asks for a [ref] | Resend copying the exact form from the error — see step 4 |
| Multiple hits, picked one and sent anyway | Violation. Back to L1: show the list, ask the user |
| Message contains "as we just said" / "the earlier plan" | Not self-contained — rewrite per step 3 |
| Reporting "they received it" / "it wasn't held" after a successful send | Say "sent" only; hold notices arrive async — relay one honestly when it comes, see step 5 |
| Zero hits, declaring outright "the window isn't open / the name was misremembered" | It may be a window in another profile. Read the identity registry via L2 first (a standard path, not a last resort); only fall to L3's address ladder if L2 comes up empty too; only then downgrade to L4 file handoff if both L2 and L3 come up empty |
| Zero hits, and skipping straight to fiddling with the address ladder or the file-handoff fallback without reading the identity registry first | Violation. L2 is a standard path on equal footing with L1; the order must be L1 → L2 → L3 → L4, and L2 may never be skipped |
| Reading out the raw socket listing to the user the moment there are zero hits | Users cannot see or map a socket/pid to one of their windows — this question is usually a wasted turn. Reading the list is L3's last resort; L2 (identity registry) and L3's first three options (the other side self-reporting / getting the target to speak first / the user fetching the address in the target window) come before it and should be tried first |
| Insisting on waiting for an echo even for a registry-confirmed address | Not necessary. When all three conditions hold (entry exists + socket exists and pid alive + identity matches), send without blocking on an echo — see "Two echo tiers"; still identify yourself and offer the error-correction invitation, just don't block on it |
| Multiple live L2 entries for the same project (interactive main session + Workflow-spawned agents each self-registered), and picking one (e.g. "the only live entry" or the first one) without showing the user, then sending | Violation, and prone to hitting a short-lived derived process — the message vanishes along with it while still being reported as "sent." Multiple live entries for the same project must always be shown to the user to pick from — never decide on their behalf, see L2 |
| Using `cmd` flags like `-p`/`--effort` as a hard filtering criterion to eliminate candidates | Violation. A 2026-08-12 final-review test disproved this: every interactive main session on this machine carries `--effort ultracode` in its cmd too, so filtering on it would eliminate 100% of main sessions. Flags may only serve as a weak sort hint, never a filtering criterion — see the read-side display rule in "Identity registry" |
| Treating the identity registry as a surveillance tool and being afraid to use it, or the opposite — treating it as the sole source of truth and asserting "not in the registry = doesn't exist" | Both directions are wrong. Reading the registry means reading a name card the other side voluntarily self-reported, not surveillance; but a missing entry only means that profile has no hook installed, not that the target doesn't exist — see the coverage-scope note in "Identity registry" |
| Treating a single mixed sample as a mechanism-level conclusion | The 2026-08-10 lesson: an earlier apparent "success" turned out confounded because the target had been switched to the same account via ccswitch, which didn't actually prove anything; the settled conclusion (can send) only came from a controlled experiment (confirmed different accounts + two-way echo). Mechanism-level conclusions must rule out confounders first |
| Sending blind to a uds: address the user hasn't identified, that the other side hasn't self-reported, and that isn't registry-confirmed | Violation. An unconfirmed address may only be used if it came from one of the three sources (self-reported / user-provided / user-identified candidate), and an echo is always mandatory |
| Trying to use a channel other than SendMessage to get content into the other session (writing to its socket by hand, touching registration files or identity-registry entries, taking it over with --resume, injecting keystrokes via tmux…) | Always forbidden, regardless of technical feasibility. SendMessage with a uds: address is the legitimate channel; when truly unreachable, fall back to L4 file handoff (through the user's own hands) |
| Resending with force after `ping_peer` refused (target_local_mode), or curling the hub yourself | Violation — everything the other side is running gets killed; switch to SendMessage, see "HAPI sessions" |
| A message sent through `ping_peer` that does not open by identifying yourself | The receiver sees "the user themselves❯" and acts on your words as the user's instruction; see rule 2 in "HAPI sessions" |
