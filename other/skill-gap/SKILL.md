---
name: skill-gap
description: >-
  Audit recent agent work for recurring manual patterns that have no skill yet, cross-check
  against installed skills and public skill catalogs (installing beats building), and propose
  the top two or three as before/after. Read-only analysis. Triggers: "/skill-gap", "what skills
  should I build", "audit my skills".
license: MIT
---

# /skill-gap — what skill should we build next?

> 🧒 When reporting to a non-technical operator, end with a child-simple "In plain words" recap in their language. (memory `eli5-always`)

Finds the gap between what the operator DOES (recurring manual work across sessions) and what they HAVE (installed skills), and proposes the highest value × frequency new skills. Read-only; proposes, never auto-builds. Mirror of [[evaluate-recurring-into-routine]] (that catches one task → routine; this scans the whole fleet of sessions → skill gaps).

## Method (token-cheap — cheap tools first, [[vault-data-architecture]])
1. **The week's agenda (≈0 tokens):** `mcp__ccd_session_mgmt__list_sessions` (limit ~60) — session TITLES are the agenda; cluster them by theme. Don't read every transcript; use titles + memory. (Full-text `search_session_transcripts` needs the operator's approval — only if a cluster is ambiguous.) ⚠️ This only sees THIS machine's sessions; with the cross-machine relay live ([[machine-migration]], skill `inbox`) a pattern from another computer is invisible here — note the current-machine label and don't assume the gap is global.
2. **What's already built:** the installed skills (the Skill tool list) + on-disk `$USERPROFILE/.claude/skills/*\SKILL.md`. Also note scheduled routines that have NO manual skill twin.
3. **Cross-map:** for each session cluster, is there a skill that covers it? RECALL memory ([[machine-migration]], [[n8n-stack]], [[notebooklm-integration]], etc.) so you don't propose something a neighboring session already built — this is the #1 trap (a parallel session, INCLUDING one on another machine, may have shipped it; check `/inbox` / the relay).
4. **Rank gaps by value × repeat:** how many sessions touched it? does it hurt now? is the infra already there (→ thin wrapper, cheap to build)? Flag ⚠️ ADDED COMPLEXITY for anything heavy ([[ak47-simplicity]]).

## Output
- A ranked table: gap · where it showed up (which sessions) · score (HIGH/MED/LOW) · is the infra already there.
- Top 2-3 as **BEFORE→AFTER on real data** ([[show-before-after]]).
- Refresh the dashboard: `$OBSIDIAN_VAULT/_Dashboards/Skill-Gap-Audit.html` (the operator works by eye, [[prefer-visual-dashboards]]).
- Then 🧒 recap. End by asking which to build (their "+" = go).

## Daily routine
Scheduled twin `skill-gap-daily` runs this read-only and updates the dashboard + drops a one-line note if a NEW gap appeared since yesterday (don't nag if nothing changed). Grunt drafting → Sonnet; the judgment/ranking → keep on the session model ([[model-routing-sonnet-grunt]]).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
