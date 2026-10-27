---
name: explain-ace
description: >
  Explain how to work with ACE and what keeps it safe, answered from the live system. Use when
  someone is new to ACE, or asks how to reach it, who reviews its replies, who sees what, or what
  data it can reach.
---

# Explain ACE — answered from the live system

People only use ACE comfortably once they understand how they interact with it and what keeps
it safe (Jon, 2026-10-07). Those answers change week to week — routing, interfaces, turn modes,
Slack behaviour are all live configuration and fast-moving code — so **never answer from a
stored write-up, this file, or memory.** Read the current sources below, then answer.

## 1. Always share Canopy's own explainer

Canopy is the system ACE runs on, and it maintains its own explainer pages. Put both in the
reply, first time and whenever the question is about how the system works:

- **What Canopy is** (public, no login): https://canopy.dimagi.com/about
- **Canopy guide** (what every page in Canopy is for; Dimagi login): https://canopy.dimagi.com/guide

Canopy's address is whatever canopy-web says it is today: `CANOPY_PUBLIC_BASE_URL` in
`config/settings/connectlabs.py` (and the *Deployment* line of canopy-web's `CLAUDE.md`). It
moved from `labs.connect.dimagi.com/canopy/` to `canopy.dimagi.com` on 2026-10-05; the old
address still 302s browser pages, so a `curl -L` check "passes" on a stale link. Check a link
with plain `curl -s -o /dev/null -w '%{http_code} %{redirect_url}'` — a 302 to another host means
the link is stale. Never take a base URL from a memo, a note or an older doc.

Do not write or link an ACE-specific explainer doc as the answer. A dated snapshot is fine as
*reference* for one analysis (filed under an ACE project on canopy-web), never as the source.

## 2. Read the current state before answering

Read only what the question needs, and say in the answer what you read and when.

| Question | Read |
|---|---|
| Who may make ACE do what; what outsiders can do | `get_interface` (slug `ace`) and canopy-web `docs/architecture/access.md` (the decision table, agent roles) |
| Does a person have to approve replies; who can | `get_agent` (`turn_mode`, `owner`, `workspace`) + access.md rows on turn mode |
| Whose runner / which mode a person's or channel's work goes to | `list_agent_actor_routes`, `list_agent_runner_rules` (slug `ace`) |
| How Slack works (threads, DMs, `--history`, Stop, status lines) | canopy-web `apps/slack/services.py`, `views.py`, `window.py`, `status.py` |
| What Labs data a viewer or ACE sees | connect-labs `CLAUDE.md § Permission Model`, `connect_labs/labs/models.py` (`UserConnectToken`) |
| ACE's own rails (send path, deny rails, tenancy guard and its current warn/enforce mode) | this repo's `CLAUDE.md § Agent operating model`, `config/gating.json`, `config/tenancy-targets.json` |

Read canopy-web and connect-labs at **current `origin/main`** — a local checkout may be days
stale (`git fetch` first), or use `gh api repos/dimagi-internal/<repo>/contents/<path>`.

## 3. What a good answer covers

**Interaction model:** the channels (email to `ace@dimagi-ai.com`, Slack `@canopy ace` in a
thread or a DM, canopy chat, the Connect Labs agent panel); that Slack and canopy chat show the
whole session live while email returns only the output (Jon, 2026-10-07 — some people prefer
one, some the other); one thread per task, and separate threads run in parallel; approvals and
who gives them; that routing a person or channel to another runner moves who oversees it.

**ACE runs in your own Claude Code.** Anyone with ACE access who uses Claude Code works with
ACE in their own session: questions, reviews, Labs reads, even an opp run. They set it up once
with `canopy agent use ace` (read its `--help` for the current steps; it ends with the line that
starts ACE locally). It brings ACE's skills and env to their computer, and follow-ups stay in
the same session. `canopy agent dispatch --slug ace` is not how to reach ACE. It hands work to a
runner to do UNATTENDED, for when you want to walk away from it. Each dispatch starts a fresh
cloud session that remembers nothing earlier, and the reply read back through `canopy agent
turns` is cut at 2,000 characters. Measured 2026-10-23: two editors with no local ACE sent 17
questions this way in a day. 12 replies were cut at exactly 2,000 characters, and about half
the sessions only re-asked for the cut text, each one redoing the work.

**Security model:** who counts as whom and that a From: line proves nothing; that outsiders get
a confined session; manual mode; the rails enforced in code; and data.

**On data, the rule is the owner's (2026-10-07): share with ACE only what you would share with
your own AI assistant.** ACE runs in an ordinary Claude session that Jon or another operator
controls. There is no extra data control or security layer on top of that, so ACE is not a
safer or more restricted place than a person's own Claude. Say this plainly when someone asks
what they may share, and do not suggest ACE adds protections. Zero-data-retention (ZDR) mode
exists, but only Jon may use it. Nobody else can ask for it, so for everyone else the normal AI
rules apply. Labs reports still read Connect as each viewer, and the Labs agent panel acts as
the person who sent, whoever they are (owner included): on a labs page ACE reads labs only
through their act-as-you permission, never its own account ([`skills/_labs-on-a-page.md`](../_labs-on-a-page.md)). Do not present Slack as riskier than ACE itself; the real risk worth naming is
Canopy itself making a mistake.

**Honest limits:** say what is early, unverified, or not live, as the sources show it today.

## 4. Who changes things

Turn mode, admins, routing and the interface are set by ACE's owner or an admin on canopy-web,
never by ACE. Say so, and route the request to the owner rather than promising it.
