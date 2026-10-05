---
name: retro
description: >-
  Close a work session properly: reconcile it against the wider collaboration, inventory what
  was actually built from git log and recently-touched files, summarize the arc, classify each
  artifact as keep, one-off or promote-to-permanent, route the durable ones to memory, canon or
  a new skill, save the retro as a vault note, and hand back an enriched /compact block so
  working memory shrinks without losing the thread. Triggers: "/retro", "/rr", "wrap up the
  session".
license: MIT
---

# /retro — session retrospective (what we built · what we keep)

> 🧒 **When reporting to a non-technical owner:** end with a child-simple "In plain words" recap in his language. His standing request (memory `eli5-always`). Reports TO him only — not inside vault notes.

A retro = the Agile end-of-cycle ritual (**Keep / Drop / Try**) applied to a work session: look back, decide what survives. The goal is that **nothing reusable drowns in the transcript** — tools, rules, and lessons get caught and put in their right home.

## Step 0 — RECALL & RECONCILE FIRST (situate this session in the WHOLE collaboration)
**Before any inventory, RECALL WIDE — this is the heart of the retro, not a formality (the owner, 2026-07-02).** A session never happened in a vacuum: I run on multiple machines + a Cowork fleet concurrently, and this retro may be running **days/weeks/months after** the work. So recall here serves TWO jobs, not one:
- **(A) De-dupe** — a rule/skill/note I'm about to capture may already be done by a parallel session.
- **(B) Reconcile** — line up what THIS session did against everything the whole **hub / vault / peers** decided *since*; catch **drift, superseded decisions, contradictions**, and durable work not yet propagated. This is the RECALL-before-activity rule (`capture-rules-into-bible`) applied to retro.

**⏳ Measure the time-gap FIRST.** Check when this session's work actually happened (turnstate ledger / the digest's day-span) vs **now**. Old session → widen every lookup below to cover *"what changed SINCE"* — don't recall only the session's own window.

**Recall stack — cheap→expensive, mostly 0 tokens (use the existing tools, don't reinvent):**
1. **This session's spine (0 tok):** `python "$IMPORTS_ROOT/turnstate/turnstate_show.py"` — the black box of what THIS session actually asked / decided / touched (facts, not memory).
2. **Recent retros:** `ls "$OBSIDIAN_VAULT/01-Conversations/Claude/Retros/"` — widen the window to span the gap; read any same-topic retro since.
3. **Neighboring chats (lexical, 0 tok):** `/search <topic words>` (search_catalog.db, ~99k Telegram/FB/ChatGPT/Claude) — what did the owner or another session **dictate elsewhere** about this topic?
4. **Vault meaning (RAG):** `/ask <topic>` (`$IMPORTS_ROOT/brain_ask.py`) — what does the Second Brain already hold / already decide on this?
5. **Memory + vault grep** for every rule/concept/decision this session touched — already captured? **superseded / changed** since?
6. **Peers & cross-machine:** `/inbox` + `_machine-bus` + consensus commits — everything agreed on the OTHER machines; did a peer already decide, or undo, this?
7. **Declined journal:** skill `/declined` — did we already reject something this session quietly re-did?

**Attribution guard:** the Step-1 inventory is machine-wide and WILL include other sessions' artifacts (skills/scripts/commits from the fleet). Treat anything NOT created in THIS conversation as **someone else's** — flag it, never claim or re-route it.

**Output of Step 0 — one tight "🔎 reconciliation" block up front** (checked + verdict):
- **checked:** what I actually looked at (N retros / chats / vault / peers).
- **✅ aligned** — this session's calls match the collaboration; or
- **⚠️ drift** — session did X but [[note/decision]] elsewhere says Y (superseded / contradicts / already undone) → flag it for the owner; or
- **🔗 to propagate** — session's durable work not yet in vault / peers / the Bible → route it in Step 4.
If a parallel session already captured the durable item, **SKIP re-capturing** — just cross-link.

## Step 1 — Inventory (deterministic first; AK-47, ~free)
Ground the recap in facts, not memory alone — run the SHARED inventory script (same one the daily sweep uses, so the logic never drifts):
- `python "$IMPORTS_ROOT/retro_inventory.py" 1`  (arg = days; widen for a multi-day session)
- It prints `BUILT_ARTIFACTS <n>` and writes `$IMPORTS_ROOT/retro_candidates/digest-latest.md` — Read that digest: new/changed **skills**, **_imports scripts/sidecars**, **durable notes** (Protocols + Concepts), and recent **descriptive vault commits**.
- (⚠️ a concurrent Claude-Desktop fleet may interleave vault commits — its are descriptive; the terse `pre-intervention` ones are auto-backups.)
- **Cross-check** with what you (the agent) created/edited in THIS conversation: skills, scripts, vault notes, memory entries, `CLAUDE.md` edits, decisions made, rules captured, things flagged for the owner.

## Step 2 — Summarize the arc ("today we learned")
3–7 beats: starting idea → what got built → key realizations → what was decided. Honest, concise, his voice. This is the "Stan at the end of South Park" recap.

## Step 3 — Classify each artifact (Keep / Drop / Try) + tested? audit
For every thing made this session, also AUDIT a **tested? ✅/❌** column — did it pass `/tt` (=`/test`) when built? Retro does NOT do the testing itself (too late/cold at session end); it only audits the line. Any durable artifact that is **❌ or untested** → flag it + offer to run `/tt` on it NOW (per [[test-after-build-skill]]). Then classify:
- 🟢 **Keep & reuse** — permanent infra or a tool you'll run again (skills, durable notes, reusable scripts).
- 🟡 **One-off** — served its purpose; if the *pattern* is worth remembering, capture the pattern (not the artifact), then let it rest.
- ⬆️ **Promote** — currently ad-hoc but should become permanent → turn into a rule / skill / memory.

## Step 3📋 — Journal sync (the task registry; the owner's decree 2026-07-04)
Retro is the SAFETY NET of the task journal ([[task-journal-done-undone-linking]]): the in-session reflex ("formulated it → straight into the registry") catches tasks at birth; retro catches what slipped. Two moves, both against the ONE journal ([[task-backlog-registry]] — **v2 markdown-first, SHIPPED 2026-07-07**):
- **Source of truth = the markdown notes** `$OBSIDIAN_VAULT/10-Tasks/task-*.md` (template `_Task-Template.md`, MOC `_Tasks-MOC.md`). They are synced to the fleet, so they work from ANY machine without the bus and without an engine. Creating a task = a new file `task-YYYY-MM-DD-slug.md`; closing it = editing the frontmatter (`state`/`status` + evidence). The schema is strict: an unknown `state`/`prio` → `schema_errors` in the audit, not a silent default.
- **The dashboard and the audit are built by the indexer** `tasks_index.py` (markdown → `_Dashboards/Task-Backlog.html` + `10-Tasks/_audit/audit-latest.json`). It runs at night on the anchor node as the ONLY writer — do NOT run it by hand on the hub/laptop (two writers of one synced derivative = a sync conflict).
- ⛔ The old SQLite task-registry engine (which lived on the laptop) = an **emergency fallback, decommissioned**; it is not on the hub and must not be. Don't call it and don't "restore" it — v2 replaced it. (The name is deliberately not in code format: a backtick would read as "run this".)

The two retro operations:
- **Closed this session** → mark `done` **with evidence** (the /tt proof, commit, counter) + link what it unblocked. Claimed-done without proof → flag, don't close.
- **Still open** (every "📌 Open item", seed prompt, deferred tail, "later") → ensure it EXISTS in the registry with a link to where it was born + prio/type. Nothing from the open-items list may live only in the chat transcript.
Announce the delta in one line: "📋 journal: +N new · ✅M closed · unchanged K". Don't duplicate neighbouring registries (the DR registry, the improvements backlog, declined) — link, don't copy.

## Step 3🗺 — Roadmap checkpoint (the owner's decree 2026-07-16: "every retro says how far we moved on the roadmap")
Canon = `$OBSIDIAN_VAULT/04-Projects/ROADMAP.md` (the living public roadmap for followers). Three moves, all against THAT file:
- **We moved forward** → tick the checkboxes/statuses; a milestone at the "a follower would care" level → a line in the Ship log with a date.
- **A new direction appeared in this session** → add it to NOW/NEXT/LATER (without duplicating the detailed plans — link to them).
- **Nothing moved** → say so honestly in the report (that is a signal too).
Announce in one line: "🗺 roadmap: ✅N advanced · ➕M added · ⏸ no movement". Projecting the file publicly happens only through the content gate — the retro publishes nothing outbound.

## Step 3🔗 — Connect check (built → handed over → IS IT USED?) — the owner, 2026-07-04
The Connect rule ([[connect-rule-pipeline-ownership]]) applied at wrap-up: for EVERY artifact of this session, take the chain to its end — **"we assembled it" is NOT the finish line**. The finish = built → handed to a consumer → **actually used**. Three outcomes per artifact:
- ✅ **used** — there is a consumer and it consumes (the skill gets called, a routine reads the output, a CRM field is read, a dashboard is opened, the data arrived and was applied). **Name the consumer** — otherwise it is not a ✅.
- 🔗 **handed over, no consumption yet** — it arrived, but nobody reads/applies it yet → onto the pending board, assign a consumer/deadline.
- ⚠️ **built into thin air** — assembled and abandoned, no consumer at all (a dead letter with no consumer — like the relink queue: 29k orphans, 0 applied) → **FLAG IT to the owner explicitly**: "we built X and nobody uses it" → decide: wire up a consumer OR declare it discarded.

Silence ≠ used. "We built it" without a named consumer = an unfinished Connect, NOT "done". In one line: "🔗 Connect: ✅N used · 🔗M handed-over-waiting · ⚠️K into thin air".
**Exception — an R&D probe (edge 5 of the rulebook entry, DR26-07-04-HUB-13):** an explicitly marked experiment with a live time-box + a learning metric does NOT count as ⚠️ "thin air" — it is 🧪; but a probe with an EXPIRED time-box and no consumption/conclusion = ⚠️ → auto-kill (archive), with no sunk-cost negotiation. "Used" = a state change (applied/closed/recorded), not "opened" (Goodhart). This does not duplicate the journal (Step 3📋) — the journal catches "open/closed", Connect catches "does the built thing have a consumer, and does that consumer consume".

## Step 3🎙 — ON AIR check (v1.1, 2026-07-11)
One cheap deterministic move: `python ~/.claude/scripts/onair.py list` (memory `onair-board`).
- This session's own declaration still active → `onair close <id>` — never leave a stale sign hanging.
- The session DID large structural work (canon / sync / consensus / factory redo) **without** a declaration → flag it in the report: "⚠️ large work ran with no ON AIR sign" (anti-pencil-whipping; the 2026-07-08 consensus.py case).
- No claim + no large structural work → skip silently.

## Step 3⛳ — Drift audit → child sessions (the owner's decree 2026-07-11: retro spawns them ITSELF, no nudges)
The retro-time CLOSURE of the drift rule ([[goal-drift-offload-to-seed-sessions]] / CLAUDE.md § "drift from the main goal"): mid-flight that rule offloads weeds AS they appear; retro is the **safety net** for what slipped — the topics the session got blown into that are NOT the main goal and NOT finished.

Procedure (cheap — reuse material already in hand: Step 0 spine, Step 1 inventory, Step 3📋 journal):
1. **Name the session's MAIN goal** (turnstate spine / the first ask). One line: "⛳ session goal: <X>".
2. **List the drift**: topics we discussed / dug into / half-built that are neither the main goal nor done. Cross-check chips already issued mid-flight — those are NOT re-spawned, only their Connect status is reported.
3. **For each REAL drifted topic the retro CREATES the `spawn_task` chip ITSELF — no asking, no waiting** (the owner, 2026-07-11: "the retro command activates the neighbouring child sessions without my nudges"). Chip prompt = a self-contained seed (Outcome · Context from recall · Scope · Deliverable · DoD — the seed format from [[decompose-into-parallel-sessions]]); title = an imperative verb phrase. Creating a chip is SAFE and non-executing — the child session starts only when the owner clicks it, so no permission is needed. Register each chip in the task journal (Step 3📋) too — chip AND registry entry, never either-or.
4. **Threshold & cap:** only a real weed (discussed seriously / carries value / would otherwise be lost) — not every stray thought; **≤5 chips per retro**, the rest goes journal-only. Fallback on a bare CLI (no chip tool): text seeds + `/bg <seed>`.
5. **Report line:** "⛳ drift audit: goal <X> · drifted into N topics → 🧷M chips created · ♻️K issued mid-flight · 📋J journal-only". No drift → one word ("⛳ no drift"), skip the ceremony.

Distinct from Step 4★ (repeats → skill) and Step 3📋 (open/closed bookkeeping): this step catches **abandoned directions** and hands each one a clean child session. Fires (data loss / security / sync down) are never "drift to defer" — they were handled in-session or escalate now.

## Step 4 — Route durable items to their home (per `operating-agreement` → "Where durable rules go")
- Reusable **tool/script** → record in **memory** (path + when to re-run) so it's findable next time.
- Behavioral **rule about how I work** → global `CLAUDE.md` (short pointer) / a skill / memory / hook.
- Team/agent **rule** (acting for the owner) → the **Bible** (`reglament-*`, via skill `bible`).
- A genuinely-recurring **ritual** → its own skill.
- **Don't duplicate** — each level points down, never copies (AK-47).
- **🏠 Home-matrix audit (gate; canon: the rulebook entry on writing lessons into every home):** for EVERY rule/lesson captured this session, list all 6 homes (Bible · CLAUDE.md · memory+MEMORY.md · skill · hook/task · MOC) with an explicit ✅ written / ⛔ not-needed+reason — no silent skips — then prove by counter: `python ~/.claude/scripts/rule_home_guard.py <slug/keywords>` (exit 1 = no always-loaded trace → fix before closing the retro).

## Step 4📓 — The cofounder growth log (persona versioning; the owner, 2026-07-02)
If the session was MEANINGFUL for the cofounder line (built/decided/learned something real about the business or about working with the owner — not a trivial lookup): **append ONE entry** to memory `cofounder-growth-log.md` — `date · shell · a lesson about working with him · one self-upgrade` — and **review the recent entries**: what to keep in the character, what to tune. Durable character changes fold DOWN into `cofounder-identity` (memory) and/or `~/.claude/skills/cofounder/references/system-prompt.md` — the log is the journal, those are the canon. Twin of [[persona-pulse-measurement]] (that one logs friction/wins about ME helping HIM; this one logs MY growth). Skip silently for trivial sessions.

## Step 4🎭 — THE DAY'S BEATS INTO THE CANON (the law "canon before content", 2026-07-10)
The retro is the main systemic "beat writer" (the context is hot, the facts are verified). For every narratively significant event of the session (a milestone/failure/turn/decision/money/a response from the outside world — the `beat_kind` dictionary in `_SHOW-CANON.md`): create a beat in `$OBSIDIAN_VAULT/04-Projects\show-canon\beats\` from `_TEMPLATE-beat.md` (3 axes + beat_kind are mandatory; set `reveal` honestly — anything unresolved = live_hold). Then update the affected arcs/loops/season → `python $IMPORTS_ROOT/content-factory\canon_render.py` (lint + fresh public registries; pushing follows its own rules, not this one). An ordinary session with no narrative events → skip silently. This runs BEFORE Step 4🎬: the fact goes into the canon first, the content judgement second (the verdict then anchors on the beats just created).

## Step 4🎬 — Content check (the owner: "all our sessions are content", 2026-07-02)
Judge at retro-time, while context is hot: **does THIS session deserve content?** Verdict = **human-post** (route → content-factory / `/episode` / `/intention`; draft-first; the owner's authorial voice = the best model) · **dev-log** (a machine-readable "problem → how we fixed it → next-day correction" for robots/future model generations → the `/episode` dev-log tier, GitHub EN) · **both** · **no** (skip silently). The nightly robots (facebook-diary-auto, content-factory, intention-lane) stay as the safety net — this step is the hot-context first pass, and the owner can override at any moment ("this deserves a post"). Attribution + CTA per [[cofounder-identity]] ("Invented by Mycroft and Tony, Palo Alto AI Research Lab") and [[cofounder-cta-public-contact]].

## Step 4★ — The "repeats → make a skill" reflex (milestone closeout)
This is the step the owner asked for (2026-06-18): at a finished milestone, don't just *note* a repeating action — **offer to turn it into a skill**. It's the retro-time expression of the standing rule `evaluate-recurring-into-routine` (a recurring task → judge "should this become a routine?"). Mirror of [[capture-rules-into-bible]] (that catches *rules*; this catches *tasks-to-automate*).

**Trigger (catch it, don't wait to be asked):** any action that **repeated ≥2–3×** this session/milestone, OR that we'll **clearly return to** later (a manual sequence I re-typed, a multi-step procedure, a recurring check).

**Procedure — 4 cheap moves:**
1. **RECALL first — don't duplicate.** Skim the available skills + memory `automation-inventory` for an existing skill/routine/hook that already covers it. If one exists, point the owner to it instead of building a twin.
2. **⚠️ AK-47 guard — a skill is just a `SKILL.md`.** One markdown file with a procedure, NOT a server / DB / webhook / external service. (This is the exact trap the Codex milestone-retro report fell into — over-engineered for a SWE team; rejected 2026-06-18.) If the thing genuinely needs more than a markdown procedure, flag it **⚠️ ADDED COMPLEXITY** and let the owner decide.
3. **OFFER as BEFORE→AFTER** (per `show-before-after`) — one compact block:
   > **WHAT:** build `/<skill-name>` · **BEFORE:** how I do it by hand today (on a real example from this session) · **AFTER:** one command `/<name>` · **what breaks:** nothing (it's a layer on top) · **do it? yes/no**
4. **On the owner's "+" → build it via `skill-creator`.** Pick the right home by SHAPE (per `operating-agreement` → "Where durable rules go"):
   - an on-demand ritual I run when asked → a **skill** (`skill-creator`).
   - "every time automatically when X" → a **hook** (skill `update-config`), not a skill.
   - time-based "every Monday / every morning" → a **scheduled task / routine** (skill `schedule`).
   - "a routine" ≠ necessarily a 24/7 robot — often the right answer is a simple semi-automatic step + a reminder.
   Then route/link it normally (Step 4) and mention it in the final report (post-hoc, not for permission).

## Step 5 — Output (tight + scannable; a review artifact, not a novel)
1. **🎬 "Today we learned"** — the arc (Step 2).
2. **♻️ Reuse table** — artifact · 🟢/🟡/⬆️ · **tested? ✅/❌** · why · routed-to.
3. **🔁→🛠 Repeats → skills** — any action that repeated this milestone, offered as BEFORE→AFTER (Step 4★); mark each built / proposed / declined.
4. **🔗 Connect** — "✅N used · 🔗M handed-over-waiting · ⚠️K into thin air" (Step 3🔗); every ⚠️ flagged explicitly + the decision (wire up a consumer / discard it).
5. **⛳ Drift map** — "goal <X> · drifted into N topics → 🧷M chips created · ♻️K mid-flight · 📋J journal-only" (Step 3⛳); the chips are already created by now, listed post-hoc.
6. **📌 Open items** — anything flagged for the owner's decision; each one REGISTERED in the task journal (Step 3📋), shown as "#id · task · link".
7. **🗺 Roadmap** — the one-line delta from Step 3🗺 ("✅N advanced · ➕M added · ⏸ no movement").
7. **🗜 Compact handoff** — the saved-note path + the ready `/compact` line (Step 6).
8. **🧒 In plain words** recap.

## Step 6 — Compact handoff (retro ⇄ compact glue; STAY in the chat, never /clear)
The retro's distilled output IS the bridge file — so close the loop without losing context. Two moves:

**6a. Auto-save the retro to the vault IN COMPACT FORMAT** (standing authorization from the owner, 2026-06-12 — no per-run ask):
Write a clean note to `$OBSIDIAN_VAULT/01-Conversations/Claude/Retros/retro-<YYYY-MM-DD>-<latin-topic-slug>.md` — the filename is **ALWAYS Latin** per [[vault-conventions]] (a Cyrillic topic → a transliterated slug; keep the original title in the frontmatter `aliases:`).
- Content = frontmatter (`title`, `date`, `type: retro`, `source: claude-session`, `tags`) + the arc (Step 2) + the reuse table (Step 3/4) + **the compact 7-header distillation** (DECISIONS / TODO / NOW / PATHS AND VALUES / COUNTERS / OPEN / TOOLS AND CONTRACTS — per `$USERPROFILE/.claude/compact-prompt.md`). **This note IS the archive** — it doubles as the compact summary, so retro and compact are never written twice.
- **NO 🧒 block in the note** — vault notes keep their own voice (the ELI5 recap is for the reply TO the owner only).
- **Wikilinks: vault ≠ memory (two namespaces).** In the retro NOTE, `[[...]]` may target ONLY existing vault notes (`reglament-*`, `protocol-*`, `concept-*`, `decision-*`, another retro — verify each exists before writing); memory slugs (`machine-migration`, `ak47-simplicity`…) go as plain inline code. Caught 2026-07-04 (a re-check by another model): a retro shipped 7/7 broken links — all of them memory slugs. Canon: `deterministic-script-gotchas` → "Vault wikilinks ≠ memory slugs".
- **New-file append only** — never overwrite an existing retro. It's a scoped folder (sits next to the chat-to-vault notes), not a live concept/person note, so this is a safe write.
- The nightly **Brain Reindex @04:00** makes it `/ask`-searchable — no manual reindex needed.

**6b. Hand the owner the ready paste block** — ⚠️ CORRECTED 2026-07-22: a bare `/compact` does NOT read `CLAUDE.md § Compact Instructions`. That earlier claim was FALSE — PreCompact hooks cannot inject instructions (only block; issue #14160 pending), and the evidence is that 354/354 past compacts came out in the DEFAULT English template. Our 7-header format is applied ONLY when the block is pasted INLINE after the command: `/compact <text>`. So PRINT the fenced "ready-made line" block from `$USERPROFILE/.claude/compact-prompt.md` and tell him to PASTE it right after `/compact`. Then the fork:
> **"Done, everything is in the vault. Want to stay in the task but travel light — PASTE the block below in full after `/compact` (without it the compression falls back to the default English template instead of our 7-header one). Or start a new chat — everything is already archived and does not depend on that click."**
- **retro = "not sure whether it's time yet"** (it archives, so both doors stay open, risk-free); **compact = "I'm definitely staying"** → paste the block.
- I (the agent) **cannot press `/compact` myself** — it's a harness command. The archive is automatic; the squeeze + paste belongs to the human.

## Scope / don't-duplicate
- Internal build-retro only. NOT the public Facebook diary (`facebook-diary-daily`) and NOT the preference scanner (`preference-sweep-daily`).
- If a session built nothing durable, say so plainly — skip the ceremony (but still offer the `/compact` block if the chat got long).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
