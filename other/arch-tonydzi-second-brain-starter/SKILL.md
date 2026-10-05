---
name: arch
description: >-
  Read the system-architect map: a deterministic catalog of everything the setup is made of
  (vault, import scripts, scheduled tasks, MCP servers, SQLite databases, hooks, skills,
  dashboards), what is healthy and what fell off. Consult it before changing shared
  infrastructure and re-scan after. Triggers: "/arch", "/arch broken", "/arch scan", "what broke
  in the system".
license: MIT
---

<!-- RECONSTRUCTED 2026-06-24 on hub HUB-1 from the live engine ($IMPORTS_ROOT/arch) + memory system-architect, because the authoritative SKILL.md lives only on laptop LAPTOP-1 (~/.claude/skills/arch, not synced). When the laptop's copy arrives via _machine-bus, RECONCILE and replace if it differs. -->

# /arch — System Architect (the map and health of the whole system)

One place that knows what the system is made of, what is healthy, what fell over — and tests it. Deterministic, 0 tokens, READ-ONLY. This is **RECALL for the infrastructure layer**: look BEFORE changing shared infrastructure, rescan AFTER.

**Engine:** `$IMPORTS_ROOT/arch/` (git-backed in `_imports`). The source of truth is `system.db` (built by the nightly scan at 05:45). Dashboard `_Dashboards\System-Health.html`, MOC `00-System\_System-MOC.md`, auto-inventory `00-System\System-Automations.md` (replaces the manual [[automation-inventory]]).

## Commands

```bash
# status (default) — health summary + score
python "$IMPORTS_ROOT/arch/arch_status.py"

# only what is broken / red
python "$IMPORTS_ROOT/arch/arch_status.py" broken

# dead code — scripts wired to nothing
python "$IMPORTS_ROOT/arch/arch_status.py" dead
```

- **`/arch`** → `arch_status.py` (status).
- **`/arch broken`** → `arch_status.py broken`.
- **`/arch dead`** → `arch_status.py dead`.
- **`/arch scan`** (force a fresh scan, AFTER an infrastructure change) → rebuild the catalog:
  ```bash
  cd /d $IMPORTS_ROOT/arch
  python sys_scan.py && python sys_coverage.py && python build_system_docs.py && python build_arch_map.py && python sys_check.py
  ```
  (That is the `run_architect.cmd` pipeline minus the final `vault_backup.py`. The full nightly run = `run_architect.cmd`, scheduled task "System Architect Nightly" at 05:45.)

## When to use it (STANDING — an always-loaded rule)
- **BEFORE** adding/removing/changing shared infrastructure (a scheduled task, an `_imports` script, an MCP, a DB, a hook, a skill, a pipeline) → `/arch` / `/arch broken`: what exists and what depends on it — will I break a neighbour?
- **AFTER** the change → `/arch scan`, so the map does not fall behind reality.
- **RED** → deal with the red first; `result!=0` on a task does not always mean "broken" (a benign lock collision happens — check the source). Never delete an `active`/`critical` asset before understanding its dependencies.

## Pitfalls (from memory)
- A coverage metric must MEASURE the artifact, not hardcode a verdict (the false backup-line alarm, 2026-06-22).
- `RED.flag` is written only on critical/daily failures (SRE style: alert on the symptom). The phase-5 routine `system-architect-red-alert` (06:21) pings Telegram Saved Messages when red and stays silent when green.

## Canon
Memory [[system-architect]] · decision `decision-architect-system-platform` · the Bible rule "check the map before changing the system" (for human assistants and LLMs alike). Related: [[verify-existing-before-proposing]], [[automation-inventory]], [[vault-data-architecture]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
