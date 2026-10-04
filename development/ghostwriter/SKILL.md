---
name: ghostwriter
description: Use when the user wants to create, generate, build, update, refresh, or improve their personal writing style guide from their own sent writing (Generate mode), OR when they ask the agent to write, draft, reply, rewrite, edit, polish, or humanize something in their voice (Use mode). Teach your agent how to write like you.
---

# Ghostwriter

**Teach your agent how to write like you.**

Ghostwriter turns your sent writing into a practical style guide your agent can use for drafts that sound like you, not like AI. It has two modes:

- **Generate mode** builds your personal style guide (usually `ghostwriter-guide.md`) by analyzing email, texts, Slack, or other writing you've actually sent.
- **Use mode** loads that guide and drafts or edits in your voice, with your personal style as the primary authority.

Once your personal guide is in place, agent-written drafts should feel spooky good.

This skill is agent-agnostic. It works with Claude Code, Codex, OpenCode/OpenClaw-style agents, Hermes, and similar local agents. It does not require any single vendor, tool, or data source — it adapts to whatever access the current environment already has.

---

## Step 0: Route to a mode

Read the user's request and pick a mode. Do this before anything else.

**Generate mode** — the user wants to *create or update the guide itself*. Triggers include:
> "create / generate / build / make my Ghostwriter guide", "update / refresh / improve my style guide", "analyze how I write", "teach you how I write", "learn my voice".

**Use mode** — the user wants the agent to *produce or edit writing* in their voice. Triggers include:
> "write / draft / reply / respond as me", "rewrite / edit / polish / humanize this in my voice", "make this sound like me", "draft an email/text/Slack message for me".

If the request is ambiguous (e.g. "help me with my writing"), ask one short clarifying question: are they building/updating the guide, or do they want something written now?

---

## Generate mode

Goal: produce a standalone markdown style guide the user can paste into *any* agent without the rest of this skill. Walk through five stages. Keep the user in control at each decision point.

Reference files (read the one that matches the chosen source — don't preload all of them):

- `references/source-detection.md` — how to inventory what access already exists
- `references/gmail-gogcli.md` — Gmail via `openclaw/gogcli`
- `references/gmail-googleworkspace-cli.md` — Gmail via `googleworkspace/cli`
- `references/local-email-exports.md` — `.mbox` / `.eml` / Takeout exports
- `references/imessage-macos.md` — local iMessage database on macOS
- `references/slack.md` — Slack via MCP or API
- `references/generic-corpora.md` — `.txt` / `.json` / `.csv` / mailbox / pasted text
- `references/analysis-framework.md` — what dimensions to extract and how
- `references/humanizer-cleanup.md` — the secondary AI-artifact cleanup pass

> **The user can point you at any source.** If they name a specific method they want used — a connector, MCP server, CLI, plugin, app integration, built-in tool, an export they've already made, or even "use the email access you already have" — **use that method** and skip ahead to privacy + collection. You don't need a reference file for it: apply the same guidelines to any source (sent messages only, filter noise, analyze the dimensions, write the guide). The reference files are examples, not an allow-list. When a tool behaves differently than a reference describes, adapt — the reference shows the *shape* of the workflow, not the only way to do it.

### Stage 1 — Detect existing access (do this first)

**Before suggesting any new setup, check what the current agent environment already has.** Least setup wins. Look for:

- Email access through a connector, MCP server, plugin, app integration, or built-in tool (e.g. a Gmail/Outlook connector, an email MCP).
- Slack access through an MCP server or app integration.
- A local messages database (iMessage on macOS).
- Any already-connected writing source.

Inventory what's available, then **recommend the existing path first** because it requires no new setup. See `references/source-detection.md` for how to probe each agent environment.

If nothing is connected, move to setup-based options in Stage 2.

### Stage 2 — Select source(s)

Present the available source methods and let the user choose one or more. Explain tradeoffs briefly (one line each), don't lecture:

- **Existing connector / MCP / plugin / built-in tool** — least setup; use if detected in Stage 1.
- **Gmail via `openclaw/gogcli`** — `gog` CLI, simple `gmail search`/`get`; good for quick local pulls. See `references/gmail-gogcli.md`.
- **Gmail via `googleworkspace/cli`** — `gws` CLI, dynamic Discovery-based access; good if you want the full Workspace surface. See `references/gmail-googleworkspace-cli.md`.
- **Local sent email export** — `.mbox` from Google Takeout or `.eml` files; no API access needed. See `references/local-email-exports.md`.
- **Local iMessage (macOS)** — adds short-form / texting voice. See `references/imessage-macos.md`.
- **Slack (MCP or API)** — workplace voice. See `references/slack.md`.
- **Other local corpora** — exported text, JSON, CSV, mailbox files, pasted samples. See `references/generic-corpora.md`.

For Gmail specifically, always offer **both** `openclaw/gogcli` and `googleworkspace/cli` and let the user pick.

If a chosen tool is missing or a source is unavailable, say so plainly and offer the next-best alternative. Never dead-end.

### Stage 3 — Confirm privacy, then collect

State privacy expectations and get explicit confirmation **before** reading anything:

- You will read only the sources the user names, and only their **sent** messages.
- The final guide stores **patterns, summaries, and synthetic examples written in their style** — not their raw private messages, unless they explicitly ask to include real quotes.
- Their writing will be processed by the **current agent/runtime** to analyze patterns. Local files and exports are not uploaded anywhere else by this skill, but connector/CLI sources may contact their normal service to fetch data, and hosted agents may process prompts/files according to that provider's privacy terms.

Then collect **sent messages only**. Filter out, where practical:

- Forwarded emails and quoted/replied thread history
- Transactional and automated messages (receipts, notifications, calendar invites)
- Link-only messages
- One-word/no-context messages in long-form sources; for texts/chat, preserve short reactions and fragments when they reveal the user's short-form voice
- Tapbacks and system-generated message rows (iMessage)
- Email signatures and boilerplate

Aim for enough volume to see patterns (a few hundred messages across contexts is plenty; even ~50–100 gives a usable first pass). Pull from more than one context if possible (e.g. email + texts) so the guide can distinguish long-form from short-form voice.

### Stage 4 — Analyze

Using `references/analysis-framework.md`, characterize the writing across these dimensions:

tone · rhythm · sentence length · openings · closings · formatting habits · humor · technical specificity · warmth · directness · uncertainty / hedging · how asks are made · feedback style · text-message behavior · context-specific differences (email vs. text vs. Slack vs. client-facing).

Capture concrete, reusable patterns — the actual greeting words they use, their median message length, their softeners, their sign-offs, words they favor and avoid. Prefer specifics over adjectives.

### Stage 5 — Write the guide

Produce a markdown file (default name `ghostwriter-guide.md`) modeled on `templates/ghostwriter-guide.template.md`. It must:

1. Be **directly usable by an agent** to draft email, texts, Slack messages, client updates, and similar writing.
2. Use synthetic examples written *in the user's style* rather than quoting their private messages (unless they asked to include real quotes).
3. Distinguish context-specific voices (long-form vs. short-form, work vs. personal).
4. End with a short **"Quick prompt for an agent"** paragraph — a single dense paragraph an agent can act on without reading the rest of the guide.
5. Include a **Humanizer compatibility** section that makes the personal style guide primary and applies Humanizer only as a secondary cleanup pass. Do **not** merge Humanizer rules into the voice rules in a way that dilutes the user's personal style.

Save the file, tell the user where it is, and remind them it's a standalone artifact they can paste into any agent.

---

## Use mode

Goal: draft or edit in the user's voice, with their personal guide as the primary authority.

### Step 1 — Find and read the guide

Search the working directory (and any path the user names) for a likely guide, in this order:

1. A path the user explicitly provides.
2. `ghostwriter-guide.md`
3. `write-like-me.md`, `style-guide.md`, `write-like-*.md`
4. Any markdown file the user points to.

**Read the whole guide before drafting.** It is the source of truth for voice.

If no guide is found: tell the user, then offer to (a) use a guide they paste/point to, or (b) run **Generate mode** to build one now. Do not silently fall back to generic writing.

### Step 2 — Gather only what's missing

Ask only for the audience/context details you genuinely need to write well: who it's going to, the relationship, the goal of the message, any must-include facts, and the channel (email / text / Slack / etc.) if it isn't obvious. Don't re-ask for anything the guide or the request already answers.

### Step 3 — Draft in the user's voice first

Write the draft using the guide as the primary authority. Match their:

- normal level of polish, warmth, brevity, punctuation, and formatting
- openings and closings for that channel and relationship
- directness, softeners, and the way they make asks
- channel-specific behavior (don't force email structure into a text)

### Step 4 — Run the Humanizer cleanup pass (secondary)

After the draft sounds like the user, do a final pass for common AI-writing artifacts using `references/humanizer-cleanup.md`. **The personal guide always wins.** Only apply a Humanizer rule where it does *not* conflict with the guide.

- If the guide says the user uses em dashes, exclamation points, emoji, or the rule of three, **keep them** — those are their voice, not AI tells.
- Remove artifacts the user genuinely doesn't produce (chatbot framing like "I hope this helps!", inflated significance, fake -ing depth, sycophantic openers, etc.).
- Do not flatten a specific personal voice into generic "human" prose. Humanizer is a guardrail against AI slop, not a second style guide.

### Step 5 — Deliver

Return the draft. If the channel allows fragments and low punctuation (texts), keep them. Briefly note any place you were unsure or made an assumption the user may want to change.

---

## Core principles (both modes)

- **Personal voice overrides generic writing advice, including Humanizer.** The guide is primary; Humanizer is a secondary cleanup pass only.
- **Privacy first.** Read only what the user confirms. Store patterns and synthetic examples in the output, not raw private messages, unless the user explicitly asks otherwise.
- **Progressive disclosure.** This file stays short; source- and task-specific detail lives in `references/`. Read only the references you need.
- **Vendor-neutral and graceful.** Prefer access that already exists. If a tool or source is missing, offer alternatives instead of failing.
- **The guide is a standalone artifact.** A user must be able to paste `ghostwriter-guide.md` into any other agent and get useful results without this skill.

## Attribution

The Humanizer cleanup pass adapts ideas from [`blader/humanizer`](https://github.com/blader/humanizer) (MIT, Copyright (c) 2025 Siqi Chen). See `THIRD_PARTY_NOTICES.md`.
