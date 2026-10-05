---
name: obsidian-ingest
description: >-
  Import any source into an Obsidian vault as well-linked atomic notes: social posts, Telegram
  HTML exports, ChatGPT JSON, voice-note transcripts, WhatsApp exports, Apple Notes, Notion
  dumps, pasted text, articles. Handles structure, frontmatter, provenance, dedup against
  existing notes and a closing RAG reindex. Triggers: "/obsidian-ingest", "import this into the
  vault", "file this".
license: MIT
---

# Obsidian Ingest

> 🧒 **Always, in every reply and progress log to the operator:** end with a child-simple "In plain words" recap in their language (plain words, no jargon) — their standing request. Scope: reports TO the operator only, never inside the vault notes you generate. See memory `eli5-always` / global `CLAUDE.md`.

This skill captures how the operator wants raw text turned into a clean, linked knowledge base. He is a perfectionist and values **thorough extraction over speed** — the goal is not to dump files but to transform raw material into atomic, well-linked notes that compound in value over time.

Read `references/vault-conventions.md` for the exact folder layout, naming, tag canon, and frontmatter templates. Read `references/pipeline.md` for the big-batch script pipeline. Read `references/source-adapters.md` for per-source parse specs (Facebook, Telegram, ChatGPT, WhatsApp, etc.). Read `references/second-brain-layer.md` for the distillation & retrieval layer (concept-synthesis "what I think about X" notes, prediction ledger, semantic search) — build/refresh after a big import so the vault stays a thinking partner, not just an archive. This SKILL.md is the decision layer; the references are the mechanics.

## Step zero: establish ownership

Before processing ANY material, establish provenance. For **known source types** (see table below) the provenance is already confirmed — skip the question and proceed. For **unknown material** (a file the operator just dropped, a pasted note, an unfamiliar export), always ask: *"Whose material is this — your own thinking, a conversation with others, or external content?"*

### Known-provenance sources (no need to ask)

| Source | origin | authored_by | Extra tags |
|---|---|---|---|
| Facebook posts export (`posts.md`) | `anton` | `human` | `facebook-diary, anton-original` |
| Telegram voice archive (content team) | `anton` | `human` (voice) / `hybrid` (summaries) | `anton-original` |
| the operator's own voice notes (m4a → transcribed) | `anton` | `human` | `anton-original` |
| ChatGPT conversations (the operator's chats) | `mixed` | `hybrid` | — |
| Nexus distilled (02-Decisions/03-Insights/05-Resources) | `anton` | `claude-cowork` | — |
| External podcasts / YouTube transcripts | `external` | `ai` | — |
| Dialogue subfolders (dialogues_work_acct_b_*) | `mixed` | `hybrid` | — |

### Unknown material — always ask

Record the answer as `origin` in frontmatter:
- `origin: anton` — the operator's own ideas → also tag `#anton-original`
- `origin: mixed` — conversations where the operator and others speak
- `origin: external` — others' content collected for reference

`origin` (whose *ideas*) is a different axis from `authored_by` (who *wrote* the text — human vs AI). Both are mandatory. **Transcription ≠ authorship** — if the operator spoke the words, it's `authored_by: human` + `origin: anton` even when a tool did voice→text.

> **Source NOT the operator's? Name the real author — never hang it on them (standing demand, 2026-06-08).** If evidence shows a source was authored by anyone other than the operator — a blogger, channel owner, journalist, podcast guest, a forwarded/saved article — **even when the operator collected or forwarded it** — set `origin: external` and record the real creator in an `author:` field; **never** `origin: anton` / `#anton-original`. Tells: self-identification, cross-post handles, third-person refs to the channel's own figures, and the **absence of the subject's own projects across the years they were active**. When unsure, ASK — the owner's words: "do not pin on me what I did NOT write". Canonical: memory [[provenance-attribute-real-author]].
>
> **Author ≠ processing tool (2026-06-09).** `authored_by` = WHO created the text (human / a specific AI). The import/enrich/transcribe/salvage TOOL goes in a SEPARATE field — `processed_by:` (or `transcribed_by:`/`summarized_by:`). NEVER let a pipeline name (`claude-cowork-*`) overwrite `authored_by` — mark the real author *and* keep the tool visible for traceability ("who is on the hook when something breaks").
>
> **Name the SPECIFIC AI (2026-06-09).** If the author is an AI, always name it concretely in `ai_author:` — **ChatGPT / Claude / Gemini + version** — never bare `ai`. ChatGPT-distilled research → `authored_by: ai` + `ai_author: ChatGPT` + `origin: mixed` (+ `processed_by:` the distiller), not `origin: anton`.

## First decision: small batch or big batch?

- **Small (≤ ~20 items / a few pasted notes):** handle inline, by hand, full manual control over each note. Go to "Inline processing".
- **Big (50+ items, a chat export, hundreds–thousands of messages):** use the checkpointed script pipeline. Hand-writing does not scale and drifts. Go to "Batch pipeline".

When unsure, count the input. A WhatsApp/Telegram export or a folder of transcripts is always "big".

## Storage decision — which layer? (set 2026-06-07 — decide BEFORE generating, EVERY import)

Don't reflexively turn everything into markdown files. At scale that lags Obsidian (it slows past ~50–100k files) and makes corpus-wide questions token-expensive. Route each kind of data to its STORE — the 3-layer model (full version: memory `vault-data-architecture` → **SQLite facts + RAG meaning + markdown thinking**):

- **High-volume structured records** (contacts, leads, transactions, rows, raw message text) → **SQLite**: entities in `leads.db`; raw **dialogue/message text → a separate `*_messages.db` + FTS5** (full-text search, 0 tokens, ms). One DB file beats 10⁴ note files.
- **Curated, human-read atomic notes** (the substantial relationships / concepts / insights worth *thinking* with) → **markdown** in the vault (the graph + reading layer) — generated FROM the data, for the top slice only.
- **Semantic recall** ("what do I think about X") → **RAG** (`brain_ask.py`) over the curated markdown, NOT the raw bulk; reindex after (`brain_embed_update.py`).

**Rule of thumb:** a source yielding >~2–3k items → the BULK lands in SQLite, only the curated top-slice becomes markdown. *Personal-DMs precedent (2026):* 80,791 contacts + 1.47M messages + 781k Airtable rows → `leads.db` (contacts/leads/airtable, joined by tg_id/handle) + `dm_messages.db` (message FTS); only **≥50-msg** relationships became `person-*` notes; **<5-msg** pings stayed index-only (a CSV registry), never tens of thousands of junk files. The **token-economy law** governs every LLM step (cheapest tool first — `CLAUDE.md` / `operating-agreement`).

## The non-negotiable rules (apply to both paths)

These are the operator's standing instructions. Don't re-ask them each time.

00. **RE-IMPORT GATE — sha256 the source BEFORE anything else (Rule 0′, set 2026-06-13 after a NO-OP catch saved a multi-hour pipeline run).** The very first action of *any* "import this corpus / add this dump / process these notes" task — **before Rule 0, before reading the file, before spawning a sub-agent** — is to ask *"did I already import this exact byte-stream?"* Run the gate: `python "$USERPROFILE/.claude/skills/obsidian-ingest/scripts/precheck_corpus.py" "<source-file>"` and read **line 1** (tab-separated `DECISION\thash\tbytes\tmatch-path`):
    - **`NO_OP`** → the source is byte-identical to an archived original under `_originals\`. **STOP. Do NOT re-run the pipeline.** Report to the operator where the existing import lives + that it's unchanged. Re-running would clear+regenerate identical files and burn tokens on already-done work (violates the token-economy law — cheap tool answered first).
    - **`CHANGED`** → same basename in `_originals\` but different bytes (the operator re-exported a grown source). Proceed as an **incremental** re-import: Rule 0 archives THIS version as a new snapshot, diff vs the prior snapshot, run the idempotent pipeline on the delta only. (This is the `telegram-reimport` path.)
    - **`NEW`** → no prior archive. Proceed with a normal first-time ingest (Rule 0 next).
    - **`MISSING` / `DIR_MODE_NOT_IMPLEMENTED`** → fix the path, or for a directory hash each top-level item separately.
    Why a script and not just "remember to check": a rule that lives only in memory gets skipped under load — the gate is a deterministic Step 0 that *can't* be forgotten because it sits at the top of this list. Provenance: memory [[crypto-essays-reimport-idempotent]]. Verified live across all 4 decision paths on 2026-06-13.

0. **Preserve the original — do this FIRST, every import (Rule 0).** Before parsing or transforming ANYTHING, archive the raw source **verbatim** to the permanent originals store and never delete it: `python $IMPORTS_ROOT/archive_original.py "<source path>" --source <key> --label "<note>"`. It copies the file/folder to `$OBSIDIAN_ROOT/_originals/<key>\<date>__<name>\` with a sha256 manifest, copy-only (the source is never moved or edited), idempotent (re-archiving identical content is skipped), and integrity-checked. This holds for **any** source — a Telegram/WhatsApp export, a CSV/Takeout dump, pasted text (write it to a `.txt` first, then archive that), a voice `.m4a`. The point: if we later delete or restructure derived notes, the untouched upstream source is still there to lean on. This is **distinct** from `vault_backup.py` (which git-commits the *vault*, i.e. the derived layer) and from rule 5 (one raw copy *inside a note*) — those protect the processed layer; Rule 0 protects the source artifact itself. Originals under `_originals\` are **never** auto-deleted.

1. **Decompose, don't just file.** One raw conversation usually becomes: a master/source note (raw text, one copy) **plus** extracted `concept-*` and `insight-*` notes for anything genuinely reusable. Filing without extraction wastes the material.
2. **One transcript = one primary concept.** Every transcript/long note should belong to at least one concept. Link it to an **existing** concept when one fits; create a new concept only when nothing fits. **Never proliferate near-duplicate concepts** — prefer linking over creating. **Weight the create-vs-link decision by `origin`:** for `#anton-original` material (the operator's own thinking — voice/diary/reflections, their side of dialogues, their AI prompts) actively look for an *emergent new concept* before defaulting to the nearest existing one — their authentic ideas are exactly where new concepts are born, so don't bury a genuinely new one inside a too-broad existing concept. For `origin: external` (podcasts, articles, others' lectures) and operational ledgers (purchases, CRM, tasks) stay strictly link-first — a new concept only for a genuinely new topic they care about.
3. **Provenance is mandatory — two independent axes.** Every note records both:
   - `authored_by: human | ai | hybrid` — who *wrote* the text. Voice transcripts & the operator's own writing = `human`; GPT/LLM summaries = `ai`; assistant-drafted/translated = `hybrid`; pre-2023 = `human`.
   - `origin: anton | mixed | external` — *whose ideas* they are (established in Step zero by **asking**, never guessing). `origin: anton` also gets the `#anton-original` tag.

   **Transcription is not authorship.** If the operator spoke or wrote the content, it stays `authored_by: human` + `origin: anton` **even when an assistant or a tool did the voice→text conversion**. The transcriber/translator goes in `transcribed_by`, never in `authored_by`/`origin`. Someone counts as author/origin only if the *ideas and words* are theirs — not if they merely typed up the operator's voice.

   These protect the operator's authentic voice from being blurred by AI text **and** from being confused with other people's thinking — keeping their own thoughts separable is their explicit, top priority.
4. **Auto-add new tags — never ask.** Reuse canonical tags from the vault first (see references). When the material needs a tag that doesn't exist, just add it. Don't pause to request approval.
5. **Raw text lives in exactly one copy.** Never store the same raw text twice. Dedup by **body content-hash** (exact dups only — near-dups with the same opening but different length are *different content*, never auto-delete them). If a curated note needs raw that lives elsewhere, link to it — don't re-embed. **Cross-source duplicates** are common: the same voice note may arrive both as a pasted note and inside a later chat export. When that happens, keep the systematic archive as the single raw copy and convert the earlier note into an **overlay** (frontmatter + summary + concept links that point to the raw via `[[links]]`), and record it in the MOC.
6. **Always cross-link, always maintain a Cross-MOC.** The vault must become a graph, not a pile. Wire links in every direction: note→concept (`concept:` field), concept→note (backlink section), **concept→concept** (a `## Related concepts` section built from a relatedness pass — see pipeline.md "Concept interlinking"), and note→source / source→derived. Each import gets/updates a `_<Source>-MOC.md` index that connects to the rest of the vault. Short `[[wikilinks]]` only (basename), never long `[[../../path.md]]` — short links survive reorganization (and Obsidian won't even resolve `..` relative wikilinks).
7. **Never edit the raw text itself.** Preserve wording, profanity, repetition, style. Strip only transcription-tool footers (e.g. "Transcribed by whisper AI") and move that metadata into frontmatter (`transcribed_by`, `summarized_by`).
8. **Finish with a report + link-integrity check.** End every run by validating that all `[[links]]` resolve (0 broken) and giving the operator a diff-style summary: files created, tags added, concepts mapped, duplicates resolved, anything flagged. **When the import contains `#anton-original` material, add a `candidate new concepts` line** — which emergent concepts you considered, which you created (nothing fit), and which you folded into an existing `[[concept-…]]` and why — so new-concept calls on the operator's own thinking are visible for them to confirm, never silent.
9. **Capture rules into the Bible — proactively.** Whenever the operator explicitly asks to record a rule ("add a rule", "this goes into the Bible"), OR a durable rule/policy is clearly needed, add it to the Bible as a `reglament-*` note — don't just acknowledge it. Append the rule to `$IMPORTS_ROOT/manual_rules.json` and rebuild with `build_rules2.py` (it merges manual rules, regenerates `_Operations-Bible-MOC.md`, and is guarded so it won't clobber the fleshed `concept-bible-*` sub-concepts). Ground the rule in a real message when possible; set provenance (the owner's directive → `origin: anton` + `#anton-original`; team SOP → `mixed`), assign a `theme` so it links the right `concept-bible-<theme>`, and update the MOC. Mechanics: the "Assistants-Ops" adapter in `references/source-adapters.md`.

10. **Prioritize by value × speed — quick wins first; never let slow-but-valuable block fast-and-valuable.** When a source — or a multi-source / multi-table job — offers more than can be done at once, order the work by the operator's triage (their explicit standing rule, 2026-06-06):
    1. **High value + fast → ALWAYS first.** Take the most important/valuable material that is *also* quick to extract. **If something is valuable but slow, do NOT do it in this pass** — it must never delay the quick high-value wins.
    2. **High value + slow → next (dig deeper).** Only after the quick wins are in, come back for the valuable material that takes longer to scrape / parse / collect / build.
    3. **Low value + very slow → last, or skip.** Not-very-valuable material that is expensive to gather comes dead last; do it only if it's genuinely worth the cost.

    (Fourth quadrant — *low value + fast* — do opportunistically only if nearly free, else skip.) This also fixes **ordering inside a big import**: front-load the small, high-signal tables/sources; leave giant low-signal dumps for the tail (e.g. pull a CRM's Investors/Contacts before a 250k-row scraped-members table). Always **state out loud what you are deferring or skipping** so nothing is silently dropped — deferred ≠ forgotten.

11. **Long-running task → periodic liveness check (~every 20 min).** On any task that runs for many minutes — a background export/import, a big batched GPU job, a long browser / computer-use session — do NOT fire-and-forget. At a regular cadence (the operator's rule: ~once every 20 minutes, or tied to natural checkpoints) verify everything is **still actually working**, not just nominally "running":
    - **Still making PROGRESS?** "Running" ≠ "advancing". Read the job's output / manifest / checkpoint and confirm counts are climbing, files are being written, the phase is moving — not stalled on a hang or an endless 429/retry loop.
    - **Tools & connections still ALIVE?** MCP servers (Telegram, Chrome, computer-use) and browser renderers can silently disconnect or freeze mid-run (both happened this session). Re-check whatever the task depends on.
    - **Any silent error?** backoff that isn't recovering, disk/auth failure, a crashed worker.

    If something broke: tell the operator, diagnose, and **recover from the last checkpoint** (restart the job, reconnect / re-auth the tool) — never assume it's fine just because it was an hour ago. Self-bounded jobs (hard per-request timeouts + the harness auto-notifying on completion/crash) need less babysitting; jobs that *can* hang silently need the active 20-min check. Mechanism when idle: a long (~1200 s) scheduled re-check, not tight polling. Complements the pre-flight MCP health-check rule.

12. **Finish the job + proactive status + a final report (the owner's standing demand, 2026-06-07 — set after I went silent during a multi-hour reindex and leaned on them to ping me).** Liveness (rule 11) is not enough; three more non-negotiables:
    - **Drive it to DONE — never park the work on the operator.** Never end a turn with "ping me when it's ready" except when genuinely blocked on (a) HIS decision or (b) a hard session/usage limit. A background job is NOT a stop: on completion the harness fires a `<task-notification>` and re-invokes you → continue the downstream steps (validate → move → report) THEN. On a hard limit: write the exact resume command and resume yourself the moment it clears.
    - **Never go silent.** On any job longer than a couple minutes: give an ETA up front and a one-line update at each phase boundary / each return from background. Silence between "launched" and "done" is the failure.
    - **A final report ALWAYS** (generalizes rule 8 from imports to *every* task): what changed (numbers) · self-checks run (0 broken links, parser counts, `pid in == pid out` — **measure, don't trust subagents' "done N" or your own assumption**) · what's deferred · next step · 🧒-recap. A task isn't done until the report is written.

13. **No-orphan rule (the operator's STANDING demand, 2026-06-13 — set after he found a high-value claude-ai artifact sitting with 0 backlinks).** Every note added to the vault MUST end up with ≥1 **incoming** wikilink from an existing layer (concept / MOC / decision / parent note) — forward-links alone are not enough, the note must be discoverable by `grep` from the OTHER side. Last mandatory step of EVERY ingest, inline or batch:
    - **Orphan-check** for each new basename: `grep -lE '\[\[<basename>(\||\])' $OBSIDIAN_VAULT` → must return ≥1 file *besides* the note itself. Batch: one pass over the basename list (deterministic, 0 LLM tokens — see [[vault-data-architecture]]).
    - **If 0 incoming** → wire it in:
      - forward-linked to concepts → add a one-line back-mention in the relevant `06-Concepts/concept-*.md` (under "See also" / "Related notes").
      - no covering concept → hang it under the nearest `_*-MOC.md`.
      - architectural / decision-shaped → entry in `02-Decisions/`.
    - **Report line is mandatory:** `orphan-check: N created · N back-linked · 0 orphaned`. `>0 orphaned` means ⚠️ unfinished, not "done".
    - **Exemptions (narrow):** `_originals/` (raw archive, [[preserve-originals-rule]]), `_drafts/`, `_imports/staging/`. Live vault notes never exempt.
    - Smell test before claiming done: "a year from now the owner greps by person / concept / topic — will this note surface?" No → finish the linking.

## Inline processing (small batch)

1. **Fingerprint first.** Skim the vault's current tag canon and existing `concept-*`/`person-*` names so new notes match (don't invent parallel vocabulary). See `references/vault-conventions.md`.
2. **Read each note fully** — not the first lines. Extract: type (concept/person/project/insight/conversation), entities mentioned, language, date, one-sentence thesis.
3. **Classify → folder** using the decision tree in references.
4. **Write the note**: canonical filename, full frontmatter (incl. `authored_by`), raw body untouched, `## See Also` with cross-links.
5. **Extract** concepts/insights worth their own note; link them both ways. For `#anton-original` notes, actively check for an *emergent new concept* (rule 2), not just the nearest existing fit.
6. **Map to a concept** (rule 2) and **update/!create the relevant MOC** (rule 6).
7. **Report** (rule 8).

## Batch pipeline (big batch)

Run the checkpointed pipeline so a mid-run failure never half-corrupts the vault. Each phase writes a checkpoint to `$IMPORTS_ROOT/` so any later phase can re-run without redoing earlier work. Full details and the bundled scripts are in `references/pipeline.md`.

Phases: **parse → JSONL** · **triage + sessionize** · **generate → STAGING** · **validate (0 broken links) in staging** · **move staging → vault** · **dedup (content-hash)** · **provenance backfill** · **build/refresh Cross-MOC** · **concept mapping (1 note = 1 concept)** · **report**.

Critical: generate into `$IMPORTS_ROOT/staging/` (mirroring the vault tree), validate there, and only then `cp -r` into the live vault. Never generate hundreds of files directly into the vault unverified.

## Compute: ALWAYS prefer GPU, ALWAYS detect first

The operator's standing rule: for any heavy/accelerable compute (embeddings, model inference, large tensor work), **use the GPU, not the CPU** — and because **he runs me on different machines**, never assume or hardcode a specific GPU. **Detect first, every time:** run `python $IMPORTS_ROOT/gpu_check.py` (or `nvidia-smi` + `torch.cuda.is_available()`). If a GPU exists but torch is the `+cpu` build, install the CUDA wheel `gpu_check.py` prints, then proceed on GPU. Falls back to CPU only when there's genuinely no accelerator (then prefer incremental/batched work). I/O-bound vault scripts (file walks, regex) gain nothing from GPU — this rule is for ML/tensor work.

**Never launch a long GPU job twice.** A GPU-OOM can leave the python process ALIVE as a zombie holding ~1.4 GB VRAM; relaunching "because it looks dead" stacks zombies until nothing loads (this actually happened — cost hours). Verify death via `nvidia-smi --query-compute-apps=pid`, not `wmic`/`tasklist` name-match (unreliable). The brain_* scripts now self-protect (single-instance lock, auto-kill stale, fp16, `--wait-gpu`, checkpoint-resume) — full **REINDEX PROTOCOL** + tooling in `references/second-brain-layer.md`. `gpu_check.py --kill` clears zombies.

## Windows / Cyrillic gotchas (learned the hard way)

- **Python `print()` of Cyrillic crashes** on Windows (cp1252 stdout). Write results to UTF-8 files and Read them; keep stdout ASCII-only (counts, slugs).
- **Don't `rm -rf` inside `%VAULT_ROOT%\`** — Obsidian and the Windows indexer hold file handles ("Device or resource busy"). Delete with `find ... -delete`, or generate into a fresh directory.
- **Filenames: transliterate Cyrillic → latin kebab**, date-prefix (`YYYY-MM-DD-slug.md`) so they sort chronologically; de-dup collisions with a numeric suffix.
- **Escaped pipes in tables:** inside a markdown table, write `[[target\|alias]]` (escaped pipe) so the table doesn't break; Obsidian still resolves it.

## What success looks like

A reader (or future the operator) lands on the Cross-MOC, navigates by month/theme/person, clicks into an atomic note, sees its provenance and its concept, and follows `[[links]]` to related ideas — with zero broken links and zero duplicated raw text. The vault gets *more* navigable with every import, not just bigger.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
