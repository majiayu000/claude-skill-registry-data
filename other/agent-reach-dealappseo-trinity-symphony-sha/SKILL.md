---
name: agent-reach
description: >
  MUST USE when user wants to research/search/look up/find anything on the
  internet — e.g. "research this topic", "do a deep dive on X", "search the
  web for X", "see what people say about X", "look this up".

  Also MUST USE when user mentions any platform or shares any URL/link:
  Twitter/X, Reddit, Facebook, Instagram, YouTube, GitHub, Bilibili, XiaoHongShu,
  Xiaoyuzhou Podcast, LinkedIn/jobs/recruiting, V2EX, Xueqiu (stocks), RSS.

  15 platforms, multi-backend routing (OpenCLI / per-platform CLIs / APIs).
  Zero config for 6 channels. Run `agent-reach doctor --json` to see which
  backend serves each platform right now.

  NOT for: writing reports/analysis/translation (this skill only FETCHES
  internet content); posting/commenting/liking (write operations); platforms
  that already have a dedicated skill installed (prefer that skill).
metadata:
  homepage: https://github.com/Panniantong/Agent-Reach
---

<!-- TRINITY FLEET NOTE — added by us, not upstream. Everything below the next
     horizontal rule is Agent Reach's own documentation, vendored verbatim from
     Panniantong/Agent-Reach v1.5.0 @ 06c202b (MIT, see LICENSE-upstream). Update
     it by re-vendoring, not by editing in place. -->

# Read this before you trust `agent-reach doctor`

**`doctor` answers "is the tool installed and configured", NOT "can it reach the
internet".** Those come apart, and when they do, `doctor` reports the optimistic
one.

MEASURED 2026-08-29 from a sandboxed Claude Code Remote session:

| channel | `doctor` said | an actual call did |
|---|---|---|
| YouTube (yt-dlp) | ✅ available | **FAILED** — `Tunnel connection failed: 403 Forbidden` |
| Any web page (Jina Reader) | ✅ available | **FAILED** — `curl: (56) CONNECT tunnel failed, response 403` |
| RSS/Atom (feedparser) | ✅ available | **FAILED** — `URLError ... 403 Forbidden` |
| Exa web search | configured | **NOT_CHECKED** — needs interactive OAuth; times out unattended |
| V2EX | already reported unreachable | FAILED (agrees) |
| GitHub | needs `gh` | not installed here; this fleet uses the GitHub MCP tools |

`doctor`: **3/15 available.** Actually reachable from that session: **0/15.**

To its credit Agent Reach is honest about the one it cannot settle — it refuses
to call Exa available on configuration alone, saying it did not start the remote
service to verify. That is the right shape. The gap above is the environment
blocking egress, not the tool lying.

## What that means for you, concretely

1. **Before claiming a channel works, make one real call.** Doctor is a
   pre-flight, not evidence. Announce the backend you used, per rule 2 below.
2. **Read a failure by its shape.** `CONNECT tunnel failed, response 403` is the
   sandbox proxy refusing — the tool is fine and the same command works on a
   normal machine. An ordinary HTTP status in the response body means you
   connected and the server answered. Do not report the first as a broken tool.
3. **Three outcomes, never two.** A channel you could not reach is NOT_CHECKED,
   not FAILED — unless you actually got a refusal from the far end.
4. **Where this runs matters.** On a developer desktop or a T12 host with normal
   egress, the zero-config channels work as upstream documents. In a sandboxed
   CCR session, assume none of them do until a real call proves otherwise.

Install (machine-local, not carried by git):

```bash
git clone --depth 1 https://github.com/Panniantong/Agent-Reach.git /tmp/agent-reach
pip install /tmp/agent-reach && agent-reach doctor
```

The GitHub archive URL and PyPI are both wrong routes here: `archive/main.zip`
and `codeload.github.com` are proxy-403, and **the `agent-reach` package on PyPI
is a different project by a different author** (jgalea, v0.1.0) that happens to
share the name. Clone and install from source.

---

# Agent Reach — internet capability router

15 platforms, multiple backends each. **When this skill exists, use it for
these platforms — do not invent your own approach.**

## Standing rules (apply for the whole session)

1. **Health-check before acting**: for multi-backend/login-backed platforms (XiaoHongShu /
   Reddit / Bilibili / Twitter / Facebook / Instagram), run `agent-reach doctor --json` first.
   Use a populated `active_backend`; `active_backend: null` means Doctor deliberately skipped a
   live probe to avoid browser-cookie reads or remote writes, not that no backend exists. Only when
   the user's task requires that platform, run the reference's read-only command to verify it.
2. **Announce what you use**: say "using agent-reach, platform X via backend Y"
   before starting.
3. **On failure, follow the retry chains in references/** — never guess
   commands.
4. **For broad research tasks**: combine platforms (Exa for web search +
   Twitter/Reddit for discussions + XiaoHongShu/Bilibili for Chinese
   perspectives), collect in parallel, then synthesize.
5. **Watch versions for the user**: after finishing a substantial
   multi-platform task, run `agent-reach check-update` (fast, one API call).
   If a new version exists, append one line to your wrap-up: "Agent Reach
   vX.Y.Z is available — paste this to me to update: 帮我更新 Agent Reach：
   https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/update.md".
   Never interrupt the current task to update; never nag about the same version twice.

## Routing table

| User intent | Category | Details |
|---------|------|---------|
| Web / code search | search | [references/search.md](references/search.md) |
| XiaoHongShu / Twitter / Bilibili / V2EX / Reddit / Facebook / Instagram | social | [references/social.md](references/social.md) |
| Jobs / LinkedIn | career | [references/career.md](references/career.md) |
| GitHub / code | dev | [references/dev.md](references/dev.md) |
| Web pages / articles / RSS | web | [references/web.md](references/web.md) |
| YouTube / Bilibili / podcast transcripts | video | [references/video.md](references/video.md) |
| Xueqiu / stock quotes | finance | [references/finance.md](references/finance.md) |

## Zero-config quick commands

```bash
# Exa web search
mcporter call exa.web_search_exa query="query" numResults=5

# Read any web page
curl -s "https://r.jina.ai/URL"

# GitHub search
gh search repos "query" --sort stars --limit 10

# YouTube subtitles (never use yt-dlp for Bilibili; retry chain in video.md)
yt-dlp --write-sub --write-auto-sub --skip-download -o "/tmp/%(id)s" "URL"

# V2EX hot topics
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# Bilibili search (bili-cli, no login needed)
bili search "query" --type video -n 5
```

## Login-backed platforms (pick by doctor's active_backend)

Twitter boundary: cookies saved by `agent-reach configure twitter-cookies`
are used only by `doctor` to check whether explicit credentials are present.
`doctor` does not run `twitter status` or configure the current shell. Before
calling `twitter` directly, explicitly provide `TWITTER_AUTH_TOKEN` and
`TWITTER_CT0` in the child-process environment without logging their values.

XiaoHongShu boundary: Agent Reach must not log the user in or read browser
cookies. OpenCLI may use only an existing Chrome session explicitly controlled
by the user. If none exists, do not automate login; use a manual Cookie-Editor
export with xiaohongshu-mcp or a legacy tool instead.

```bash
# Twitter search (twitter-cli preferred; retry chain in social.md)
twitter search "query" -n 10

# Reddit (NO zero-config path — OpenCLI or rdt-cli, login required)
opencli reddit search "query" -f yaml   # desktop
rdt search "query" --limit 10            # legacy/server

# XiaoHongShu (desktop prefers OpenCLI)
opencli xiaohongshu search "query" -f yaml

# Facebook / Instagram (desktop OpenCLI, browser session)
opencli facebook search "query" -f yaml
opencli facebook groups -f yaml
opencli instagram search "query" -f yaml       # user search
opencli instagram user USERNAME -f yaml        # recent posts from one user
```

## Environment check

```bash
# Channel availability + which backend serves each platform
agent-reach doctor --json
```

## Discovering OpenCLI adapters

When the routing table lacks a needed platform or command, run `opencli list`,
then inspect `opencli <platform> --help`. Discovery proves only that an adapter
exists, not that authentication or target content works. Run read-only commands
only when the user's task requires that platform, and require non-empty content.

## Workspace rules

**Never create files in the agent workspace.** Use `/tmp/` for temporary
output and `~/.agent-reach/` for persistent data.

## Detailed references

Read the matching file when you need specifics (commands above cover the
common cases; references hold per-backend command groups, caveats, retry
chains — note: reference docs are written in Chinese, commands are universal):

- [Search](references/search.md) — Exa AI search
- [Social](references/social.md) — XiaoHongShu, Twitter, Bilibili, V2EX, Reddit, Facebook, Instagram (multi-backend/login-backed groups)
- [Career](references/career.md) — LinkedIn
- [Dev](references/dev.md) — GitHub CLI
- [Web](references/web.md) — Jina Reader, RSS
- [Video](references/video.md) — YouTube, Bilibili, Xiaoyuzhou
- [Finance](references/finance.md) — Xueqiu quotes, search and market content

## Configure a channel

If a channel needs setup, fetch the install guide:
https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md

The user only provides cookies / one extension click; the agent does the rest.
