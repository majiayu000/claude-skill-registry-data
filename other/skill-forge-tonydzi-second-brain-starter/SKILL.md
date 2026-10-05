---
name: skill-forge
description: >-
  Create a node-local skill on a follower machine and prepare its promotion into the shared set
  through a gate. Use when a new skill idea appears on a peer and should not wait for the hub.
  Triggers: "/skill-forge <idea>".
permissions: [filesystem]
risk_level: shell-local
processes_untrusted_data: false
disable-model-invocation: false
origin: MAC-1
related: decision-2026-07-14-fleet-skill-autonomy-local-namespace
license: MIT
---

# skill-forge — a peer's skill forge (axis A + the promotion gate)

The implementation of the approved design [[decision-2026-07-14-fleet-skill-autonomy-local-namespace]]:
a peer creates ITS OWN skills locally (poisoning nobody — the blast radius on others is 0),
and they reach the fleet-wide set only through a gate. While named `local-*` a skill lives here only
(`.stignore local-*`: not synced, not rolled back by receiveonly, but still loaded by the loader).

The gatekeeper: `skill_guard.py` in this same folder (0 LLM, stdlib only). Rails from DR26-07-14-MAC-1-01.

---

## Mode A — `/skill-new` (create a local skill)

1. **Name** — `local-<slug>`, only `[a-z0-9-]`. Check it:
   `python ~/.claude/skills/skill-forge/skill_guard.py --check-name local-<slug>`
2. **Scaffold**: create `~/.claude/skills/local-<slug>/SKILL.md` with frontmatter:
   - `name`, `description` (when to invoke it), `permissions: [...]` (filesystem/shell/network — only what is truly needed),
     `risk_level` (inert / shell-local / shell-networked / secret-touching / always-loaded-core / irreversible — the taxonomy from the external DR),
     `processes_untrusted_data: true|false`, and `disable-model-invocation: true` for side-effecting or manual-only skills.
   - ⚠️ **shell is OFF by default**: do not ask for `shell` without a real need; a skill with shell requires a mandatory review at promotion time.
3. **Run the gate scan immediately**: `python ~/.claude/skills/skill-forge/skill_guard.py`
   (rail 1 collision + rail 3 sync-conflict — you learn at once whether you are shadowing a shared skill).
4. **`/tt`** the new skill (run it live → break it → prove it) BEFORE any promotion.

## Mode B — `/skill-promote` (local → the fleet-wide set)

The gate (approved by the owner): **`/tt` + leak scan + collision check + risk classification + one peer opinion → route it to the writer.**
A follower does NOT write the shared set itself (it is receiveonly) — it prepares a bundle and hands it to the single writer.

1. **Deterministic gate** (everything a machine can check, right here):
   ```
   python ~/.claude/skills/skill-forge/skill_guard.py --leak local-<slug>
   ```
   → collision (rail 1) + sync-conflict (rail 3) + name (step 2) + leak (rail 6). Exit 1 = stop.
   A heavier leak scan when available — `gitleaks`/`trufflehog` on top (the `/release-slice` engine).
2. **Did `/tt` pass?** — no ✅, no promotion.
3. **Risk class** → if `secret-touching` / `always-loaded-core` / `irreversible` / it triggers Tier-2 →
   **the owner's gate** (an ask in the approval channel); otherwise one peer opinion is enough.
4. **One peer opinion** — `bus_send.py <peer> "SKILL-REVIEW: local-<slug> …"` ([[peer-opinion-before-fleet-rollout]]).
5. **Route to the writer**: copy the bundle into `_machine-bus/_transit/canon-proposals/` + ping the writer
   (today the hub; after migration step 3, the anchor node). The writer strips the `local-` prefix, commits and syncs it to everyone
   ([[skills-rollout-all-machines-default]]). ⛔ A follower never strips `local-` itself — that is the writer's job.

---

## Boundaries (what this skill does NOT do)
- **Step 3 (moving the writer from hub to the anchor node)** — a fleet consensus decision, not made here.
- **Step 5 (codifying it into the Bible / CLAUDE.md)** — the canonical writer (the hub) does it, AFTER the mechanism is built.
- **OS-level read-only on shared/** (option B from the DR) — node infrastructure, separate from this skill.

🧒 In plain words: this is a workbench for inventing your own tool at home, checking that it breaks
nobody else's and hides no secret, and then handing it to the "master smith" who distributes it to everyone.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
