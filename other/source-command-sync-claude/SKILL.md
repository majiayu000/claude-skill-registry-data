---
name: "source-command-sync-claude"
description: "Sincronizza skills e comandi .Codex tra la repo Gravity e ~/.Codex globale"
---

# source-command-sync-claude

Use this skill when the user asks to run the migrated source command `sync-claude`.

## Command Template

Usa la skill `sync-Codex` per sincronizzare le cartelle `.Codex`.

Chiedi prima all'utente quale direzione vuole:
1. **Repo → Globale** — hai appena fatto un pull con nuove skills/comandi
2. **Globale → Repo** — hai creato o modificato una skill/comando in `~/.Codex` e vuoi salvarlo nella repo

Poi esegui la direzione scelta seguendo le istruzioni della skill.
