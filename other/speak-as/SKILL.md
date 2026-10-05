---
name: speak-as
description: >-
  Write a public post in the owner's own voice with a role model's style and idea palette
  layered on top, reading a style-palette file so the same engine works for any thinker the
  owner has profiled. Draft-first. Triggers: "/speak-as <name>", "write in the style of <X>".
license: MIT
---

# /speak-as <role model> — a post in the owner's voice through the chosen thinker's optics

> 🧒 **When reporting to a non-technical owner:** end with a child-simple "In plain words" recap (only in the reply TO him, NEVER inside the post draft).

A thin writing engine, **parameterized by the role model**: it takes the **style palette of the chosen thinker** + **the owner's voice** + **his real material on the topic** and writes ONE post as a mix — "frame/optics from the role model, voice/confessional tone/concreteness from the owner". One engine for any role model (one person today, anyone tomorrow). A manual command "write a post in the style of X about Y" (≠ the daily [[content-factory]], ≠ the `/portret` dossier).

> [!warning] SAFETY FUSE (read this first)
> - ⭐ **The owner's authorial voice is written by the top-tier model or stronger** (a cheap model is forbidden for authorial text — a carve-out of `model-routing-sonnet-grunt`). Session weaker than that → delegate the WRITING itself to a top-model subagent (`Agent`, `model:'opus'`); the groundwork (resolving the role model, recall, choosing the platform) can run on the cheap model.
> - **INFLUENCE, NOT copying.** The role model's words = `origin: external`. Don't paste his phrases verbatim, don't pass his thoughts off as ours without rethinking them. The post stays the owner's post (`origin: anton`).
> - **Preserve the owner** — don't dissolve into the role model (his = the frame/optics, the owner's = the material and the voice).
> - **Privacy** from [[fb-diary-voice]] applies (names/amounts/sensitive material/live leads and deals must not be burned; abstract them up to an insight).
> - **Draft-first** — I hand over the draft, the owner posts it himself (publishing outbound = Tier-2).

## Step 0 — Resolve the role model → the palette (cheap, no LLM)
1. The role model's name → a latin slug (as in `07-People\person-<slug>.md`).
2. Look for the palette: `$OBSIDIAN_VAULT/08-Templates/style-<slug>-influence.md`.
   - **Exists** → load it (techniques + idea palette + "how to preserve the owner"). Carry on.
   - **Missing** → a STOP fork for the owner: "There is no style palette for <X> yet. Build one? → run `/portret <X>` (dossier + social media + DR), then I'll synthesise `style-<slug>-influence.md` and write in his style." Do not invent a style out of thin air.
3. Always load the owner's voice: [[fb-diary-voice]] — ⚠️ this is a MEMORY file on the system drive (`~\.claude\projects\...\memory\fb-diary-voice.md`), NOT a vault note; searching for it in the vault is pointless (the two-drives pitfall).

## Step 1 — RECALL on the topic (the material MUST be the owner's, not generalities)
`/ask "<topic>"` (RAG) · `/search "<words>"` (exact words) · a fresh day from the [[content-factory]] inbox if it is a diary post. The groundwork can run on a cheap subagent; the text itself — top model.

## Step 2 — Platform and length
Facebook diary ~3000–4500 chars (confessional, interwoven threads) · X — short (a hook formula + 1 thought) · Telegram content — medium. Not specified → default to the Facebook diary and say so.

## Step 3 — Write the mix (top model)
From the **role model** (out of his palette file): the frame, the optics, the signature techniques, the idea boundaries. From the **owner**: the concrete detail of the day, hard self-irony, vivid images, confessional tone, 1–2 genuine questions at the end, honesty. Contested topics — handled with epistemic neutrality ([[epistemic-neutrality]]).

## Step 4 — Self-check before handing it over (quality gate)
- [ ] Does it sound like **the owner**, not like a cosplay of the role model? (role model outweighs him → rewrite in the owner's voice)
- [ ] Is there a hook + a frame (formula/triad/theses) + 1–2 genuine questions?
- [ ] **Zero verbatim phrases** from the role model; ideas rethought, not copied?
- [ ] Privacy respected (no third-party names/amounts/live deals/sensitive material)?
- [ ] Length fits the platform? No long dashes ([[no-long-dashes]]).
Below the owner's bar → rewrite; don't hand over a weak draft.

## Delivery
A clean post block (ready to copy) + one line: role model · platform · length · which technique was used. The owner posts/edits it himself. Optionally — 2–3 hook headline variants.

## How to ADD a new role model (full cycle)
1. `/portret <Name>` → the dossier `person-<slug>` + (synthesis) an `insight-*` note on "how he thinks".
2. Synthesise the palette `08-Templates\style-<slug>-influence.md` following the reference palette (style techniques + idea palette + "how to preserve the owner" + the influence-not-copy fuse). Back up before writing ([[vault-backup-rule]]).
3. Done — `/speak-as <Name> about <topic>` works immediately (the same engine reads the new file).

## Gates and links
- Top model for the writing; groundwork on the cheap model. Draft-first; publication = Tier-2 (the owner himself).
- The reference palette · the core-ideas insight note · the voice [[fb-diary-voice]] · the pipeline [[content-factory]] · the person dossier.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
