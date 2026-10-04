---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: Use when the user wants to send the same prompt to several LLMs and compare the answers - sequentially (stopwatch, clean per-lane timing) or in parallel (true race), with optional repetitions per model, judged by the starting model across quality, correctness, completeness, instruction fidelity and latency (time is only one dimension). Triggers on /compare-race, 'model race', 'vergleiche modelle', 'gleicher prompt an mehrere modelle'.
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: de
status: active
visibility: public
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Ausfuehrungsschicht fuer compare-race run (Spawn/Polling/Dateiprotokoll)', 'note': 'Optional. Ohne coma laeuft der modellmanuelle Weg: Spuren selbst ausfuehren und mit compare-race record einreichen.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.de.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — Pointer-Skill (Deutsch)

> **Dieser Skill ist ein reiner Pointer. Quelle der Wahrheit ist das Modul.**

## Modul-Pfad

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```

Repo: [github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## Anweisung an den Agenten

1. Lies den Rollen-Prompt **`prompts/RACE-STARTER.de.md`** im Modulordner und folge ihm.
   Du bist der RACE-STARTER — und per Default auch der **Judge** (Nutzerentscheidung
   2026-08-16).
2. Config prüfen (`compare-race config`; Host-Config unter `~/.compare-race/`).
   Modus wählen: `sequential` = Stoppuhr (saubere Einzelmessung je Spur) ·
   `parallel` = echtes Rennen. **Die Stoppuhr ist nur ein Bild** — Zeit ist eine
   Dimension unter Qualität, Korrektheit, Vollständigkeit, Anweisungstreue, Kosten.
3. Rennen starten (`compare-race run --prompt-file …`); ohne coma den modellmanuellen
   Weg über `compare-race record` gehen.
4. Als Judge die Rubrik in `RACE.md` des Race-Ordners ausfüllen — jede RUN-Datei
   selbst lesen; Befangenheit benennen, wenn das eigene Modell mitfährt.
5. Achsen-Disziplin: Zuschreiben nur, wenn genau eine Achse variiert
   (model = Rennen · run = Varianz · time = Modell-Drift).

## Kontingent-Warnung

Rennen kosten auf **jedem** beteiligten Kontingent (claude/codex/agy/kimi). Vor
großen Rennen (viele Spuren × Wiederholungen) den Nutzer fragen.
