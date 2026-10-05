---
name: intake
description: >-
  Route a new rule, preference or policy edit into every home it belongs in (always-loaded
  canon, memory, the behavioral codex, a skill, a hook) and leave a trace in the always-loaded
  layer so parallel sessions pick it up on their own. Flow: dedup recall, classify by form,
  write to all homes, back up, report. Triggers: "/intake", "record this rule", "route this to
  its homes".
license: MIT
---

# /intake — the rule intake (route it to its homes, don't just write it down)

> 🧒 **When reporting to a non-technical owner:** end with a child-simple "In plain words" recap (memory `eli5-always`). Reports TO him only — never inside vault notes.

**Why (canon: memory `rules-intake-channel`).** This chat is the dedicated channel where the owner drops ALL rules/policies/Bible entries/skills/`CLAUDE.md` edits/preferences, so that working chats stay clean. My job is **not just to write it down, but to DELIVER** the rule to all of its homes, cross-link it, and leave a trace in the always-loaded layer, so that automatic/parallel processes see it on their next start. This skill = the same manual flow I repeated ~10× in one session, folded into a single command.

**Architecture (skill-design-three-layer):** a thin `SKILL.md` orchestrator + deterministic steps (backup/commit/grep) + an external store (CLAUDE.md, memory, the vault). The routing decision **is still shown to the owner** in the report — the skill does not hide the logic, it executes it without asking at every step.

---

## Step 0 — RECALL (dedup; cheap, ~0 tokens). NEVER spawn a duplicate
Before writing — check whether such a rule already exists (update it, don't spawn a copy; resolve conflicts by "newer beats older"):
- `MEMORY.md` is already in context — scan its index by topic.
- `grep` over memory: `$USERPROFILE/.claude/projects/<project>/memory/`.
- `grep` over the Bible/vault: `reglament-*` / `protocol-*` under `03-Insights\Operations\` and `05-Resources\Protocols\`; if needed, RAG via `brain_ask.py "<topic>"`.
- Found an existing one → **update it** (don't create a second), mark `supersedes` / refresh `date_established`. A conflict between the owner's own rules (`origin: anton`) is resolved only by him or by an explicit `supersedes`.

## Step 1 — Classify the rule by its FORM → pick the homes
Route per `operating-agreement` → "Where durable rules go" (do NOT duplicate the rule across files — each level REFERENCES the one below):
- **How I work / a machine process** (imports, dashboards, token economy, routines, my reply style) → `CLAUDE.md` (an always-on block) + memory (+ a line in `MEMORY.md`).
- **A durable fact / preference** → memory (`memory\*.md` + a pointer line in `MEMORY.md`).
- **An action ON THE OWNER'S BEHALF towards the outside world** (outreach, his chats, calendar, purchases, hiring, household) → **the Bible** (`reglament-*` in the vault) + if needed a lift into always-on in `CLAUDE.md`.
- **"Every time automatically when X"** → a **hook** (skill `update-config`), not "keep it in mind".
- **Time-based "every Monday / every morning"** → a **scheduled task / routine** (skill `schedule`).

## Step 1★ — THE TEST "could a HUMAN do this?" → YES → the rule ALSO GOES INTO THE BIBLE
If the rule could hypothetically be executed by the owner's **live assistant** (not only by me/code) — it is **duplicated into the Bible** (the single rulebook for all actors: the owner + assistants + AI). To keep the copies from drifting: **the canon of the human-executable part lives in the Bible**, and the machine layer (`CLAUDE.md`/memory) REFERENCES it. Purely mechanical things (an import script, a reindex — no human does that) are NOT duplicated into the Bible.

## Step 2 — THE KEY invariant: a trace in the always-loaded layer is MANDATORY
The only things that "surface by themselves" for parallel processes are the ones in the **always-loaded** layer: `CLAUDE.md` and the `MEMORY.md` index load into EVERY session; individual memory files load by relevance; **the vault does NOT surface on its own** (it needs grep/RAG); a skill surfaces on its trigger. → For a rule to become "background/automatic", it MUST leave a trace in `CLAUDE.md` or `MEMORY.md` (at least a pointer line to the canon), not only in the vault/skill.

## Step 3 — Write into every chosen home
- **Memory:** create/update `memory\<slug>.md` with frontmatter (`name`, `description`, `metadata.type`: user/feedback/project/reference). Body: for feedback/project — `**Why:**` + `**How to apply:**`. Use `[[name]]` links liberally. + one pointer line in `MEMORY.md` (`- [Title](file.md) — hook`, ≤200 chars).
- **CLAUDE.md:** if it is always-on — add a block `## ALWAYS: <topic> (standing — set <date>)` or append a bullet to an existing one; finish with "Canon: memory `<slug>` + Bible `<reglament>`". ⚠️ Entry budget: the block = ONLY trigger + gist + pointer, target ≤4 lines / ~900 characters; the mechanics (commands, formats, IDs, examples) live in the Bible/memory/skill, they have no place in CLAUDE.md. ⭐ PAY THE ENTRY FEE (Bible entry on optimising always-loaded files): BEFORE writing, run `python ~/.claude/scripts/claude_md_guard.py --preflight <block.md>` — exit 0 = go ahead; exit 1 = the file is in the yellow/red zone, first free up at least the block's size (compress a section with the harness `claude_md_compress.py index→build→verify` / move the body into the Bible), then write. We do not re-compress at the word level (declined) — structure only. The write hook on CLAUDE.md will repeat the warning, but the preflight is your step, don't wait for the hook.
- **The Bible (if Step 1★ applies):** a `reglament-*.md` in `03-Insights\Operations\` (or the right domain) in the `protocol-bible-as-prompt` format (the owner verbatim, `WHEN → DO`, frontmatter with `audience`/`origin`/`authored_by`/`date_established`/`status`/`confidence`). **Wire it into the MOC** (`_Operations-Bible-MOC` or the domain index) — otherwise the assistant will never find it.

## Step 4 — Backup + selective commit (safety)
- Writing into the vault → FIRST `vault_backup.py` ([[vault-backup-rule]]).
- **⚠️ If the shared backup is blocked** (the fuse catches someone else's mass deletions from a parallel fleet run) — do NOT force it; commit ONLY your own files: `cd $OBSIDIAN_VAULT && git add "<my file>" && git commit -m "..."`. Never `--force`, never a blanket glob delete.
- `CLAUDE.md`/memory are auto-committed by git (`claude-skills-git-backup`, a 15-minute task) — no separate commit needed.

## Step 4★ — THE HOMES MATRIX + the watchdog (a gate, not an option; canon: the Bible entry on writing lessons into every home)
Before the report, fill in the matrix: **each** of the 6 homes (Bible · CLAUDE.md · memory + MEMORY.md · skill · hook/task · MOC) gets an explicit verdict **✅ written / ⛔ not needed + reason** — silently skipping a home is not allowed (pitfall 2026-07-14: the Bible was forgotten because the route was kept "in the head"). Then prove it with the counter:
`python ~/.claude/scripts/rule_home_guard.py <slug/keywords>` — exit 1 = no trace in the always-loaded layer (Step 2 violated) → fix it before reporting.

## Step 5 — Report after the fact (NOT for permission — for transparency)
Briefly to the owner: **WHAT** the rule is · **THE HOMES MATRIX from Step 4★** (a verdict per home) · **what was cross-linked** · conflicts/duplicates (if an existing one was updated). Like with concepts — after the fact, without asking permission for each home.

---

## Boundaries / don't duplicate
- Always RECALL before writing (Step 0) — update what exists instead of spawning a second copy.
- The canon of this procedure = memory `rules-intake-channel` (this skill is its executable form). The mirror is `capture-rules-into-bible` (which catches rules in ANY chat; intake = the dedicated channel + the always-loaded-layer mechanics).
- Secrets (passwords/access/financial figures/"grey" techniques) — NEVER in the loaded layer (`CLAUDE.md`/`MEMORY.md`/the Bible); their home is `secrets\` (memory `credential-store`).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
