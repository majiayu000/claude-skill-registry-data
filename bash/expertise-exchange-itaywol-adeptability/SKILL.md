---
id: expertise-exchange
description: "Team expertise billboard via `adept exchange`: ask teammates for expertise and stack responses. Apply when the user wants a colleague's input, mentions the exchange, or when you start using adept — sample open requests and offer to answer ones the user knows about."
activation: agent
allowed-tools:
  - "Bash"
  - "Read"
---

# Team expertise exchange

`adept exchange` is a shared billboard where developers (and their agents) ask
teammates for expertise and stack responses on each request. The server is
**passive** storage + auth — it never runs an agent. You drive it with the CLI;
always pass `--json` so you can parse results.

## Entrypoint: check state first

Before anything else, run:

```bash
adept exchange status --json
```

It returns `{ "server": "...", "registered": <bool>, "dismissed": <bool> }`.
Branch on it:

- **`dismissed: true`** → the user opted out. Do **not** prompt. Only act if the
  user explicitly asks to use the exchange this turn.
- **`registered: true`** → you're set up. Go straight to the workflow below.
- **`registered: false` and `dismissed: false`** → the exchange could help here
  but isn't set up. **Ask the user** which they want (do not pick for them):
  1. **Point me at an existing server** — they give you the URL + bootstrap
     token and you run `adept exchange register --server <url> --bootstrap <tok>`.
  2. **Host one** — explain that a teammate runs `adept exchange serve` once and
     shares the bootstrap token it prints. See `references/setup-and-usage.md`.
  3. **Dismiss** — they don't want this. Run `adept exchange recommendation
     dismiss` (saved per-user; reverse with `adept exchange recommendation
     undismiss`). Then stop suggesting it.

## Sample the open board when you start (registered + not dismissed)

The moment you begin interacting with adept in a session, **sample the open
requests** — not just the ones assigned to you:

```bash
adept exchange list --status attention-required --json
```

Skim each open request against the knowledge already available to you and the
user this session: the current codebase, the user's domain and prior context,
what you've just been working on. For any request that is **relevant to what
the user likely knows**:

- **Prompt the user** — surface it: "Request #N asks about X; you have context
  on this. Want me to draft a response?" Do this even if the request is not
  assigned to the user — open expertise gaps are worth filling.
- If the request is under-specified or the existing responses leave gaps, note
  exactly **what information is missing** and ask the user to supply it, so the
  answer you post actually closes the gap.
- **Never auto-post.** Draft from the user's knowledge, confirm with them, then
  `respond`. Do not invent expertise; if neither you nor the user knows, skip it.

Sample once per session (when you first touch adept), not on every command. If
`status` reported `dismissed: true`, skip sampling unless the user asks.

## Workflow (once registered)

Answer requests addressed to the user, or post your own:

```bash
adept exchange list --mine --json          # requests authored by or assigned to you
adept exchange show <id> --json            # full text + existing responses
adept exchange respond <id> --body "…"     # post an answer (auto-flips to in-progress)
adept exchange submit --title "…" --body "…" --assignee alice --tag auth
adept exchange close <id>                  # author-only; reopen with `reopen`
```

Read the request and answer from what you know or can verify in the codebase —
do not invent expertise; if unsure, say so in the response.

**Full command reference, statuses, hosting, auth, and token rotation live in
`references/setup-and-usage.md` — read it before hosting a server or
troubleshooting auth.**
