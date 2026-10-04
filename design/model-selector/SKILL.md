---
name: model-selector
description: Vergleicht verfügbare LLM-Modelle (Nous Portal) und hilft beim Auswählen des richtigen Modells für die jeweilige
  Aufgabe.
version: 1.0.0
author: yuno
license: MIT
platforms:
- linux
metadata:
  hermes:
    tags:
    - LLM
    - model-selection
    - nous-portal
    - pricing
lane: koenigin
reasoning_effort: xhigh
---
# Model Selector Guide

Welches Modell für welche Aufgabe im Nous Portal / Hermes Agent.

## Schnellauswahl

### Alltag & Schnelligkeit (gratis/niedrig)
- **openrouter/owl-alpha** — Gratis! 0$/token, 1M Context, #1 Free-Modell auf OpenRouter. Perfekt für Subagenten-Scouts im Bienenschwarm
- **qwen/qwen3.6-35b-a3b** — Allrounder, Code, Daily-Workflows, GreyScript, Hermes-Konfiguration (1M ctx, kostenlos)
- **stepfun/step-3.7-flash:free** — Schnellste Antwort, gute Qualität, kostenlos
- **google/gemini-2.0-flash** — Stark, schnell, kostenlos über Nous
- **meta/llama-3.1-8b-instruct** — Klein, schnell, für Simple-Aufgaben

### Code & Architektur (mittel)
- **deepseek/deepseek-v4-flash** — Reasoning + Code-Review, 13B aktiv (284B total), 3 Reasoning-Modi
- **qwen/qwen3.7-max** — Agent-Frontier-Modell (Mai 2026), schlägt Claude Opus 4.6 auf Agent-Benchmarks
  - $1.25/M Input, $3.75/M Output (50% Rabatt aktiv, Stand Jun 2026)
  - 1M Context, 65.5K Output, 54 tok/s, Tool-Error-Rate nur 2.31%
  - Nr. 1 App auf OpenRouter: Hermes Agent (65.1B Tokens)
  - Prompt Caching eingebaut (~47% Cache-Hit-Rate in der Praxis)
  - HINWEIS: qwen3.7-plus auf OpenRouter aktuell NICHT verfügbar — nur Max
- **moonshotai/kimi-k2.6** — Open-Weight Multimodal-Agent (Apr 2026), 1B MoE / 32B aktiv
  - $0.684/M Input, $3.42/M Output — günstiger als Qwen für Input-heavy Workloads
  - 262K Context (kleiner als Qwen), Open-Weight (auf HuggingFace)
  - GPQA Diamond: 91.1%, Agentic Index: 66.0 (besser als 94% der Modelle)
  - Stärken: Long-Horizon Coding, Multi-Agent Orchestration, UI/UX Generation
  - Cache-Pricing: $0.15–$0.37/M (je nach Provider), hohe Cache-Hit-Raten möglich

### Tiefe Analyse & Reasoning (höher)
- **anthropic/claude-sonnet-4.6** — Nuance, tiefes Verständnis, präzise Formatierung (aktueller Sonnet)
- **anthropic/claude-opus-4.8** — Premium-Frontier (Jun 2026), GPQA Diamond 93.5%, Code-Agent-Sweep. Bester Single-Call für tiefe Architektur, komplexe System-Designs, und LLM-Persona-Work. Teuer — nur einsetzen wenn's drauf ankommt. Modell-ID: `anthropic/claude-opus-4.8`
- **gpt-4o** — Allgemein stark, teurer
- **claude-3-opus** — Goldstandard für komplexe Logik (älter, teurer)

### Reasoning-Modelle (speziell)
- **deepseek/deepseek-v4-flash** — 3 Modi: Non-Think (direkt), Think High (mittel), Think Max (voll, bis 384K Token)
  - Reasoning-Nähe zu V4-Pro, 13B aktive Parameter (284B total)
  - V4 vereint Standard- und Reasoning-Fähigkeiten in einem Modell
  - **Hermes Config Mapping:** Reasoning-Modus über `agent.reasoning_effort` steuern.
    `none/minimal` = Non-Think, `low/medium` = Think High, `high/xhigh` = Think Max.
    ⚠️ **NICHT xhigh global setzen!** Kostet 20-30% extra Output-Tokens bei JEDER Nachricht.
    Global auf `medium` lassen, nur bei Bedarf per `/reasoning xhigh` aktivieren:
    `hermes config set agent.reasoning_effort medium`  # global
    `/reasoning xhigh`  # nur für komplexe Multi-Step-Analysen
- **qwen/qwen3.7-max** — Unterstützt `enable_thinking` + `preserve_thinking` (für Agentic Tasks empfohlen)
  - GPQA Diamond: 92.4% (besser als Opus 4.6 mit 91.3% und DS-V4-Pro mit 90.1%)

## Wichtige Fakten

### ⚠️ Provider-spezifische Modell-Namen
Die Modell-Namen unterscheiden sich je nach Provider — nicht davon ausgehen dass das OpenRouter-Format überall gilt!

| Provider | V4 Flash Name | V4 Pro Name |
|---|---|---|
| **Nous Portal** | `deepseek-v4-flash` | `deepseek-v4-pro` |
| **OpenRouter** | `deepseek/deepseek-v4-flash` | `deepseek/deepseek-v4-pro` |
| **DeepSeek direkt** | `deepseek-v4-flash` (via API) | `deepseek-v4-pro` |

⚠️ **V4 Flash ≠ Reasoning-Modus!** DeepSeek V4 Flash und V4 Pro sind separate Modelle, JEDES mit eigenen Reasoning-Modi (Think High / Think Max). Nicht verwechseln! Die Benennung "deepseek-v4-flash" ist der Modell-Name, nicht eine Einstellung.

- Größeres Tier (Plus/Max) = bessere Qualität, NICHT mehr Kontextfenster
- Kontextfenster ist eine harte Grenze: Qwen unterstützt bis 1M Token (~Roman)
- Reasoning-Modus wird via `agent.reasoning_effort` in Hermes config gesteuert:
  `hermes config set agent.reasoning_effort medium` (global sparsam)
  `high/xhigh` nur per `/reasoning xhigh` für komplexe Analysen.
  CLI-Persistenz: Braucht keinen `/reset` — wirkt sofort auf nächsten LLM-Call.
- ⚠️ **delegation.model/provider MÜSSEN gesetzt sein!** Wenn leer, nutzen Sub-Agenten das Default-Modell (→ kann teuer werden).
  `hermes config set delegation.model "deepseek/deepseek-v4-flash"` (free via Nous)
  `hermes config set delegation.provider "nous"`
  Ohne diese Settings hat the user ~$174/Woche nur für Sub-Agenten mit Opus 4.8 verloren.
- Yuno-Default: Qwen3.6 oder Step-Flash für 90% der Aufgaben
- Agent-Schwerarbeit (Discord-Bot, Cron-Architektur): qwen3.7-max empfohlen
- Premium-Analyse (Persona, Architektur, System-Design): claude-opus-4.8
- qwen3.7-plus auf OpenRouter aktuell nicht verfügbar (Stand Jun 2026)
- Nur bei echten Analyse-Aufgaben Claude Sonnet/DeepSeek-Reasoning einplanen

## Modell-Handoff nach Wechsel

Jeder Modell-Wechsel braucht ein Briefing, damit das neue Modell ohne Reibungsverlust weiterarbeiten kann.

- **Automatisch:** Der Morning-Cron generiert ein Kurzbriefing (`~/MODEL_HANDOFF_SHORT.md`)
  mit Projekt-Status + Blocker.
- **Ausführlich:** Volles Handoff (`~/MODEL_HANDOFF.md`) mit "Tips for the new model"-Sektion,
  in der selbst erlernte Pitfalls weitgegeben werden. Halte sie aktuell — das nächste Modell startet damit.

Referenzen
- `references/model-details.md` — Detaillierte Vergleiche, Reasoning-Modi, Benchmarks
- `references/deepseek-pricing.md` — DeepSeek V4 Flash & V4 Pro Preis-Details (Provider, Cache, Effektivkosten)
- `references/model-handoff-guide.md` — Leitfaden: Modell-Handoff generieren und pflegen

## Preis-Check Workflow

Bei Preis-Check-Anfragen (z.B. "preis-check Deepseek"):
1. Aktuelles Modell checken: `hermes config | grep -i <modell>`
2. **NICHT web_extract auf OpenRouter-Seiten** — Preise sind oft als Bilder eingebettet und nicht extrahierbar. Stattdessen `web_search` mit Query wie "deepseek v4 flash pricing costs per million tokens" — die Suchergebnis-Beschreibungen enthalten bereits die Kern-Preise
3. Für tiefere Daten: OpenRouter-API direkt nutzen oder `hermes insights --days 7` für reale Nutzungsdaten
4. Effektivpreise (cache-bereinigt) notieren — die Listenpreise sind oft irrelevant
5. Vergleichstabelle bauen: Provider × Kosten für Session/Tag/Monat
6. Nous Portal Free-Tier als Bonus hervorheben (falls zutreffend)