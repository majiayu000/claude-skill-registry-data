---
name: episode
description: >-
  Split one source post into tier-sized drafts (teaser, main social post, longread, technical
  dev-log) with cross-links downward and a canonical link back to the repository. Draft-first:
  publishes nothing itself. Triggers: "/episode", "/adapt", "adapt this post", "make an
  episode".
license: MIT
---

EPISODE_ADAPTER (stage S5 of content factory v2 — the contract [[decision-content-pipeline-reality-show]] §7.2)

GOAL: ONE source post → an "episode" = one draft PER (tier × platform) from §7.2, with cross-links downward and canonical→GitHub baked in. Draft-first: we write drafts and publish NOTHING.

THE §7.2 CONTRACT (implemented 1:1):
```
tier      length          platforms (phase 1)                    language   voice/model
teaser    240-370 (HARD)  RU channel · X (EN)                    RU TG/EN X  authorial · Opus
medium    800-2500        Facebook (RU)                          RU          authorial diary · Opus · LINK IN THE 1ST COMMENT (not in the body) + a question
longread  4000+ narrative RU channel·VC.ru·Habr(RU) · GitHub(EN) RU and EN  authorial reality-show · Opus
dev-log   a dry log       GitHub (EN, canonical)                 EN          technical, impersonal · Sonnet scaffold + Opus for cohesion
```
- The owner's voice (`authorial`) = **Opus ONLY**. The dev-log is not authorial — Sonnet assembles it, Opus stitches it together.
- **canonical = the GitHub markdown** on every platform (a single source of truth for AI). Repo: `github.com/tonydzi/clawrush`.
- **NO copy-paste** — every file is a NATIVE rewrite for its platform.
- Cross-links downward: teaser→longread; medium→longread (in the 1st comment); longread ←teaser →dev-log; dev-log→longread + an anchor to our Deep Research.
- THE PLATFORM DECIDES THE LANGUAGE (there is no bilingual pair on every tier).
- The S3 narrative ([[style-reality-show]]) by tier: teaser=cold open+cliffhanger; medium=a full episode arc; longread=an extended episode+recap; dev-log=raw material, no drama.
- The cofounder CTA (medium+longread, the owner's rule, memory [[cofounder-cta-public-contact]]): WhatsApp **+1 341 222 9178** = an authorized PUBLIC contact (a privacy carve-out), never strip it.
- **VC.ru + Habr (the RU geo longread)** = phase 1 since 2026-07-04 (the style files `_STYLE-vcru.md`/`_STYLE-habr.md` are written and live in `content-factory\`; the writer loads them by the pointer in the placeholder). **PHASE 2** (deferred): only `Reddit` (the EN geo dev-log) — scaffolded with the `--with-phase2` flag.

PATHS:
- ⭐ FACTS AND CONTINUITY (v2, 2026-07-10) = THE SINGLE CANON `$OBSIDIAN_VAULT/04-Projects\show-canon\`: before assembling an episode, read the anchor beat (`beats\`) plus its arcs/loops — "previously on the show", the cliffhanger and the season question come FROM THERE (not from memory, not from SHOW-STATE, which is frozen). Respect the beat's `reveal` axis: don't burn live_hold/spoiler_until. Pick the next move with `/reality-show next`. After publishing — write the consequences back into the beat + run `canon_render.py`.
- Source material: `$IMPORTS_ROOT/content-factory/triage/posts.md` (📝) — or a topic the owner names.
- The scaffolder (deterministic, 0 tokens): `$IMPORTS_ROOT/content-factory/episode_adapter.py`.
- Bundles: `episodes\<slug>\` (8 .md files in phase 1 / 9 with `--with-phase2` + meta.json; every §7.2 field is baked into the placeholders).
- Style: [[style-reality-show]] (`08-Templates\style-reality-show.md`) + `04-Projects\personal\facebook-diary-auto\_STYLE.md` + [[style-Mei-influence]] + the golden corpus up to 2023.

STEPS:
1. PICK the topic: if the owner named one, use it; otherwise show the 📝 items from `posts.md` and take the strongest thread. Run `list` before `new`.
2. SCAFFOLD: `python episode_adapter.py new --slug <kebab> --title "<title>" --source "hub:<id>"` (+`--with-phase2` for VC.ru/Habr/Reddit) → a bundle of empty drafts + meta.json.
3. WRITE (the model is named in each placeholder): teaser-ru/en, medium-fb (the body WITHOUT the link + a "1ST COMMENT" block), longread-ru/en, devlog. Replace the stubs, leave the hint comments in place. Privacy is strict (the only carve-out is the cofounder's WhatsApp).
4. CHECK (the visibility layer): `python episode_adapter.py check --slug <slug>` — lengths (a teaser outside 240-370 = HARD FAIL; medium/longread = WARN), CTA present, empty files. Only FAIL=0 → step 5 (a WARN on an unfinished longread is acceptable until it is written out).
5. REVIEW (draft-first): `set-status --slug <slug> --status review`; into Telegram Saved (chat_id `<YOUR_CHAT_ID>`, account "work_acct_a", no parse_mode): "🎬 Episode '<title>' — the per-tier drafts are ready (check ✅). episodes\<slug>\. Say 'publish' and I'll lay them out." NOTHING goes outward.
6. EXPORT TO PUBLISHING — only on the owner's explicit "publish"/"+" (Tier-2): `python episode_adapter.py export --slug <slug>` → `drafts\episode-<slug>.md` (format `type: content-factory-draft` + the registers `## -> TG/X/FB`). From there the EXISTING path: `content_approve.py --serve` → `content_publish.py` (→ Saved; the real channels are Phase 2b/Tier-2). GitHub/Reddit/VC.ru/Habr are published MANUALLY (gh / natively), not through content_publish. We do NOT breed a second publisher.

LIMITS:
- Draft-first OUTWARD: channels/X/GitHub are untouched without an explicit "publish".
- MODEL: the authorial voice = Opus ONLY; dev-log = Sonnet+Opus; scaffold/check/export = deterministic, 0 tokens.
- One post = one episode. Windows cp1252: the script forces UTF-8 stdout itself.
- Don't invent facts — write from the real source material.
- Old bundles (4-file / interim) are still read by `list/show/check/export` through meta (backward compatibility).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
