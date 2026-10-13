---
name: codex-ratelimit-notify
description: "Send an IFTTT mobile push \"codex rate limit detected\" when an OpenAI Codex CLI run hits a rate/usage limit. The companion codex skills (/codex-review, /codex-2nd) fire this automatically via codex-rate-limit.js. Invoke manually whenever a codex run that BYPASSES that path — /codex-imagegen, /codex:codex-rescue, or an ad-hoc `codex exec` — shows \"you've hit your limit\", \"rate limit\", \"usage limit\", \"too many requests\", \"quota exceeded\", \"429\", or a reset time, even if the flow otherwise stays silent. Also use to test the notification."
allowed-tools:
  - Bash(node *)
---

# Codex Rate Limit → IFTTT Notify

Fire a mobile push **"codex rate limit detected"** the moment an OpenAI Codex CLI run
hits a rate/usage limit. This matters because the codex skills deliberately **silently
fall back to Opus** and never surface the limit in the terminal — so a phone push is the
only way the user learns Codex is throttled.

## How it's wired (usually automatic)

All rate-limit state, notification, and dedupe live in one script:
`$HOME/.claude/scripts/codex-rate-limit.js`.

The companion codex skills (`/codex-review`, `/codex-2nd`) already run `codex-rate-limit.js check-output` after
each Codex run. When it detects a limit it marks a lockout **and** fires the push — so for
those skills the notification happens on its own. You do **not** need this skill for them.

## When to invoke manually

Some Codex paths bypass `codex-rate-limit.js` entirely: `/codex-imagegen`,
`/codex:codex-rescue`, and any ad-hoc `codex exec` you run directly. If Codex output on one
of those paths shows a rate/usage limit, funnel it into the same script so both the push and
the shared lockout happen:

```bash
node "$HOME/.claude/scripts/codex-rate-limit.js" mark
```

`mark` records a 60-minute lockout (so the companion skills also back off) and fires the
deduped push. Prefer `mark` over a bare notification — a real limit should set the lockout.

Recognize a limit from these cues in Codex stdout/stderr:

- `you've hit your limit`
- `rate limit` / `too many requests` / `429`
- `usage limit` / `quota exceeded`
- a reset time like `resets 5pm`

The script's automatic detection (`check-output`/`check-stderr`) matches the phrase patterns
above but **not** a bare `429` or loose reset phrasings like `resets in 40 min` — so those
can slip past even the companion skills, which is another reason to funnel a limit you spot
into `mark` yourself.

## Notify without a lockout / test the push

To fire the push without touching the lockout (e.g. a quick end-to-end test of the IFTTT
wiring):

```bash
node "$HOME/.claude/scripts/codex-rate-limit.js" notify "test from codex-ratelimit-notify"
```

Check that the push arrives on the phone. Nothing else changes — Codex stays available. If
the key isn't configured, it prints `IFTTT_WEBHOOK_KEY not set — nothing sent.` instead.

## Mechanism

- **Channel**: IFTTT Webhooks event `Claude Code` (the same applet used by

  `hooks/notify-ifttt.sh`), key read from the `IFTTT_WEBHOOK_KEY` env var. If the key is
  unset on this machine, the notification is skipped silently.

- **Payload**: `value1` = `codex rate limit detected`, `value2` = reset detail (or, for the

  `notify` subcommand, the message you pass), `value3` = current working directory.

- **Dedupe**: fires at most once per lockout window — a second codex skill hitting the same

  wall won't buzz the phone again until the lockout expires.

- **Best-effort**: a failed webhook never breaks rate-limit tracking.
