---
name: hook-generator
description: "Crafts proven, scroll-stopping video hooks from a 404-hook bank of top-performing reels (ranked by views). The creator brings a video idea, a rough script, or just a topic; Claude diagnoses which of the 8 hook structures fit, pulls the highest-performing frameworks from the data, and writes a spread of spoken hooks in the creator's voice — each anchored to a real framework with its view-count proof. Triggers: write a hook, write me a hook, hook for this video, hook for my video, generate hooks, give me hooks, hook ideas, viral hook, scroll stopper, opening line, hook generator, need a hook, what's a good hook for."
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/hook-generator/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.


# Hook Generator — proven hooks from real viral data

The creator brings a video idea (a topic, a rough concept, or a full script they already
wrote). Claude turns it into a set of **spoken hooks** — the first 3–5 seconds the
host says on camera — each one built on a framework that already went viral, in
the creator's own voice (`voice-dna.md`), tied to the positioning in `backbone/messaging.md`.

The edge is the data: a bank of **404 hooks** scraped from top-performing reels,
each tagged with its structure, framework, source, and **view count**. We don't
invent hook shapes from vibes — we pull the proven ones and pour the creator's idea into
them.

## The Flow

```
1. GATHER   — take the creator's idea / script / topic. Distill the core payoff.
2. DIAGNOSE — pick the 3–4 hook structures that fit (see reference/structures.md).
3. PULL     — run find_hooks.py to get the top proven frameworks + view proof.
4. WRITE    — generate 6–8 spoken hooks across those structures, in the creator's voice.
5. DELIVER  — present the options with the framework + proof behind each; recommend one.
```

## Step 1 — Gather the idea

Take whatever the creator gives you:
- **A full script / beat sheet** → the hook is the opening line; read the whole
  thing so the hook matches the payoff the video actually delivers.
- **A rough concept** (e.g. "a video about the one habit that doubled my output") →
  that's enough; pull the core transformation.
- **Just a topic** (e.g. "systems that save time") → make a reasonable read of the
  angle through the niche on the CLAUDE.md Creator Profile "Niche" line, state it
  in one line, and generate. Don't interrogate the creator — they'll redirect if it's off.

Find the **core** before writing: what's the payoff, the surprise, the enemy, or
the number? A hook is a promise the rest of the video keeps — you can't write the
promise until you know the payoff.

## Step 2 — Diagnose the structures

Read [reference/structures.md](reference/structures.md) and pick the **3–4
structures** that best fit this idea. The 8: Educational/Tutorial, Secret Reveal,
Contrarian/Negative, Raw Shock, Question, Experimentation, Fortuneteller,
Comparison. Quick map:

- Showing a system / how-to → **Educational**, **Secret Reveal**
- Hot take / picking a fight → **Contrarian**, **Question**
- A result that sounds fake → **Raw Shock**, **Comparison**, **Experimentation**
- Belief shift / story → **Fortuneteller**, **Secret Reveal**

Aim for a *spread* of distinct angles, not four flavors of one line.

## Step 3 — Pull the proven frameworks

The bank is the source of truth. Query it — never eyeball the raw CSV. Run from
the repo root (`python` on Windows):

```bash
python3 .claude/skills/hook-generator/scripts/find_hooks.py --list                          # the 8 + counts
python3 .claude/skills/hook-generator/scripts/find_hooks.py --structure "secret" --top 15   # top in one structure
python3 .claude/skills/hook-generator/scripts/find_hooks.py --structure all --top 3         # a spread across all 8
python3 .claude/skills/hook-generator/scripts/find_hooks.py --keyword ai --top 20           # topic-anchored search
python3 .claude/skills/hook-generator/scripts/find_hooks.py --structure question --keyword money
```

Pull frameworks for the structures you picked in Step 2. If the idea has a strong
topical anchor (a word from your niche: money, build, content, ai...), add
`--keyword` to surface hooks from adjacent topics — their *shape* transfers even
when the subject doesn't. Results are pre-ranked by performance (rank 1 ≈ 9.5M avg
views), so the top of each list is the strongest proof.

## Step 4 — Write the hooks

For each hook: take a proven **framework** (the `[X]/[Y]` template) and pour
the creator's idea into it. **Keep the framework's shape and rhythm** — that's the part
that's proven — and swap in the creator's specifics.

Voice and positioning come from the repo, never from this file:

- **Voice = `voice-dna.md`** (fallback: the Voice/Tone one-liner in the CLAUDE.md
  Creator Profile). Positioning and any real number = `backbone/messaging.md`
  (its proof bank). Never invent a register, a slang set, or a stat.
- **Own winners.** If `knowledge/winning-hooks.md` exists, read it: it holds hook
  shapes that already worked for this creator and outranks a generic bank row of
  the same shape.
- **Spoken, not written.** This is a line the creator *says* in the first 3 seconds, not
  a caption. Sounds like a FaceTime with a friend. (Short-form = spoken hook. If
  the idea is YouTube long-form, frame it as a **title** paired with the thumbnail
  instead; never substitute one for the other.)
- **Make them feel behind or surprised in 3 seconds.** Name the enemy the offer
  removes (see `backbone/offer.md`), drop a real number from the proof bank, or
  open a curiosity loop.
- **Don't jam the CTA into the hook.** The hook earns the watch; the offer ask
  (`backbone/offer.md`) comes later in the script. Don't drop a CTA by accident.

## Step 5 — Deliver

Present **6–8 hooks** in chat, grouped/labeled by structure so the creator sees distinct
angles. For each, show the line + the framework it's built on + the source's view
count (that's the trust signal — they asked for *proven* hooks). Format (the lines
below are illustrative; write your own from your niche):

```
**Option 1 — Secret Reveal**
"Nobody fumbled a bag harder than people still doing [the manual thing] by hand in 2026."
↳ framework: "Nobody [X failed action] harder than [Y example]" · 17.7M views (@frankmichaelsmith)

**Option 2 — Question**
"Is there any way for a one-person team to [the outcome]? Watch."
↳ framework: "Is there any way for [X] to [Y achieve goal]?" · 1.59M views (@codiesanchez)
```

If a hook is built on one of your own past winners instead of a bank row, cite it
as `↳ from your own winners (knowledge/winning-hooks.md)`.

End with a one-line **recommendation** (which to lead with and why). Then it's
the creator's pick — the chosen hook hands off to scripting.

## Rules

- **Data first, vibes second.** Every hook traces to a framework in the bank (or a
  hook from your own winners in `knowledge/winning-hooks.md`, when that file
  exists). Don't invent hook shapes from memory.
- **Query, don't read.** Use `find_hooks.py` to slice the bank. Never dump the
  171KB CSV into context.
- **Spoken line, not caption.** The artifact is what the creator says out loud (or, for
  YT long-form, the title). Never substitute a text overlay or caption.
- **Spread the angles.** 3–4 structures, distinct hooks — variety to pick from.
- **Voice is non-negotiable.** If a hook reads like LinkedIn, rewrite it. Pull from
  `voice-dna.md`, not a generic "viral" register.
- **The hook is a promise.** It must match the payoff the video actually delivers —
  no bait the script can't cash.

## Files

| Path | What it is |
|------|------------|
| `404-kallaway-hooks.csv` | The proven-hook bank — 404 hooks, ranked by views. Source of truth. Query via the script; don't read raw. |
| `scripts/find_hooks.py` | Slices the bank by structure / keyword, returns top frameworks + proof. |
| `reference/structures.md` | The 8 structures explained — trigger, best-for, your angle, top proof. Read this to pick structures. |
