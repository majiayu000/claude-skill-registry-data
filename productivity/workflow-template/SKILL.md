---
name: workflow-template
description: 'Use when the user wants a structured multi-agent plan for a domain task — server hardening, repo cleanup, security/CVE analysis, GreyScript tool dev, or Ollama/LLM setup. Domain-adapter for multi-agent-master-workflow with 🟥🟧🟨🟩 priority, Phase-1→Phase-2 gate, and Mnemosyne hooks. Trigger on: hardening plan, ollama optimization, CVE analyse, greyscript architecture, repo cleanup, systematischer plan für.'
version: 1.0.0
author: Yuno for the user
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - workflow
    - orchestration
    - planning
    - subagents
    - domain-templates
    - multi-agent
    - standard
    lane:
    - koenigin
    reasoning_effort: xhigh
    related_skills:
    - multi-agent-master-workflow
    - plan
    - subagent-driven-development
    - delegation-anti-patterns
---
# Workflow-Template (Standard)

the user's Standard-Workflow für strukturiertes Multi-Agent-Planen über fünf Domänen hinweg. Domain-Adapter für den bestehenden `multi-agent-master-workflow`-Skill, **kein** konkurrierender Orchestrator.

## Overview

Dieser Skill löst drei Probleme, die in the user's realer Arbeit immer wieder auftraten:

1. **Template-Drift**: Vor 2026-07-05 gab es fünf freie Markdown-Prompts mit unterschiedlicher Struktur, keinem Trigger-Mechanismus, und keinem Output-Vertrag.
2. **Standardisierungslücke**: `multi-agent-master-workflow` definiert das Muster (Queen/Worker/Gate), aber nicht die domänenspezifische Anwendung.
3. **Memory-Verlust**: Pläne wurden geschrieben, aber Lessons-Learned verschwanden aus dem Context nach Session-Ende.

Workflow-Template schließt diese Lücke, indem es fünf Domänen-Spezialisierungen (Hardening, Repo/CI, Security/CVE, GreyScript, Ollama) als wiederverwendbare Templates bereitstellt, mit gemeinsamer Phase-Struktur, einheitlichem Farbschema und Mnemosyne-Disziplin.

## When to Use

**Trigger-Phrasen** (Skill feuert automatisch):

- "ich brauche einen [hardening/plan/security/repo/ollama]-plan"
- "multi-agent master workflow für [domäne]"
- "führe eine systematische analyse durch für [X]"
- "systematischer plan für [X]"
- "standard workflow für [X]"
- "[Domain]-architektur planen"

**Don't use for**:

- Einfache Single-Step-Tasks (kein Multi-Agent nötig → direkt ausführen)
- Rein konversationelle Antworten (kein Artefakt nötig)
- Reine Recherche ohne Plan-Ausgabe (→ `web_search` oder `web_extract`)
- Tasks wo schon ein Skill existiert, der spezifischer passt (z.B. `plan` für Implementation-Pläne ohne Domain-Kontext)

## Integration with multi-agent-master-workflow

| Layer | Skill | Was er tut |
|-------|-------|------------|
| **Pattern** | `multi-agent-master-workflow` | Queen/Worker/Gate-Architektur, Phasen 1-5, Priorisierung |
| **Domain-Adapter** | `workflow-template` (dieser Skill) | Fünf Domänen-spezifische Ausprägungen, 🟥🟧🟨🟩-Standard, Mnemosyne-Disziplin |

**Regel**: Wann immer `multi-agent-master-workflow` triggert, prüfe **zuerst** ob `workflow-template` ein passendes Domain-Template hat. Wenn ja → nimm das Domain-Template und adaptiere die Schritte aus `multi-agent-master-workflow`. Wenn nein → nimm `multi-agent-master-workflow` direkt.

## Quick Decision Tree

→ Vollständiger Decision-Tree: `references/templates/00-decision-tree.md`
→ Consolidation Pattern (wie dieser Skill entstand): `references/consolidation-pattern.md`

Kurzfassung:

```
Was ist die Aufgabe?
├─ Server/Linux härten → 01-server-hardening
├─ Repo aufräumen + CI/CD → 02-repo-cicd
├─ Security/CVE-Analyse → 03-security-cve
├─ GreyScript-Tool bauen → 04-greyscript
├─ Ollama/LLM optimieren → 05-ollama-llm
└─ Kombiniert/multi-domain? → Siehe references/templates/combinations.md
```

## 🟥🟧🟨🟩 Farb-Legende

→ Vollständige Legende: `references/meta/color-legend.md`

| Stufe | Bedeutung | Wann? |
|-------|-----------|-------|
| 🟥 **Kritisch** | Blockiert / Lockout-Risiko / Datenverlust | Sofort, vor allem anderen |
| 🟧 **Hoch** | Spürbarer Nutzen / wichtiges Risiko | Nach 🟥-Block abgeschlossen |
| 🟨 **Mittel** | Komfort / Efficiency / Polish | Wenn 🟥🟧 durch sind |
| 🟩 **Optional** | Feinschliff / kosmetisch | Wenn überhaupt Zeit übrig |

## Standard-Workflow (für alle Templates)

```
┌─────────────────────────────────────────────┐
│ Phase 1: VORAB-PLAN (skill_view Domain-Tpl) │
│   - Lade passendes Template                  │
│   - Constraint-Check                         │
│   - ⚠ WARTE auf the user-Freigabe              │
└─────────────────────────────────────────────┘
                ↓ (Freigabe)
┌─────────────────────────────────────────────┐
│ Phase 2: AUTO-MODE / ORCHESTRIERUNG         │
│   - Konkrete Schritte / Befehle             │
│   - Git-Backup vor Destruktivem            │
│   - Verifikation nach jedem Schritt         │
│   - ⚠ QUEEN-VERIFICATION: Nach Sub-Agent-  │
│     Batch jede behauptete Datei selbst lesen│
│     (stat/read_file). Sub-Agent-Self-Reports│
│     sind NICHT vertrauenswürdig —           │
│     insbesondere write_file-Claims auf neue │
│     Dateien (vgl. Pitfall #7).              │
└─────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│ Phase 3: REFLECTION & PERSIST               │
│   - Mnemosyne-Memory schreiben (QUEEN,      │
│     NICHT an Sub-Agent delegieren —         │
│     leaf-agents haben keinen Zugriff auf    │
│     mnemosyne_remember)                     │
│   - System-Doku aktualisieren               │
│   - Skill-Patch bei Lessons-Learned         │
└─────────────────────────────────────────────┘
```

## Template-Index

→ Ausführliche Inhalte in `references/templates/`

| Template | Bewertung | Domain | Pitfall-Klasse |
|----------|-----------|--------|----------------|
| `01-server-hardening` | ⭐⭐⭐⭐⭐ | Linux/Cloud | Lockout-Risiko |
| `02-repo-cicd` | ⭐⭐⭐⭐ | DevOps | Force-Push-Damage |
| `03-security-cve` | ⭐⭐⭐⭐⭐ | Security | Legalität |
| `04-greyscript` | ⭐⭐⭐⭐ | GreyHack | GreyScript-Specifika |
| `05-ollama-llm` | ⭐⭐⭐ | AI-Infra | GPU-Konflikt |

## Mnemosyne-Disziplin

→ Vollständige Hook-Sammlung: `references/meta/mnemosyne-hooks.md`

Kurzfassung: Nach jeder Workflow-Template-Session **eine** `mnemosyne_remember`-Call mit Template-spezifischem Hook. `importance` zwischen 0.6 und 0.9 (höher für Security, niedriger für Polish). `veracity` = `tool` für Mess-Ergebnisse, `stated` für the user-Aussagen.

## Common Pitfalls

1. **Phase-1 übersprungen**: Direkt mit Code/Config anfangen ohne Freigabe → Lockout, Datenverlust, Halluzination. Immer **erst** Template laden, dann Constraint-Check, dann Freigabe.
2. **Falsche Domain-Klasse**: Ollama-Setup mit GreyScript-Pitfalls mischen → falsche Constraints. **Immer** Decision-Tree fragen.
3. **Templates kopieren ohne Anpassen**: Template-Struktur ist Skelett, nicht Copy-Paste. **Immer** Context-spezifische Pitfalls prüfen.
4. **🟥-Items als 🟨 behandelt**: Kritische Risiken werden im Output "weichgespült". Risiko-Skala ist **kein** Vorschlag, sondern Standard.
5. **Mnemosyne-Hook vergessen**: Nach Session ist Lessons-Learned weg. Hook ist **nicht** optional, sondern Teil des Workflows.
6. **Loader-Cache widerlegt**: `skill_view('workflow-template')` funktioniert **sofort** nach Skill-Erstellung — die YAML-Frontmatter + Content ist live. Bei Änderungen per `skill_manage(action='patch')` kann es sein, dass die Session die neue Version erst nach dem nächsten `skill_view`-Aufruf sieht. Im Zweifel: `skill_view(name)` nochmal aufrufen. **WICHTIG** — diese Eigenschaft betrifft nicht nur Auto-Discovery, sondern auch Tasks deren **Verifikation** an Loader-State hängt (z.B. "teste ob neu-erstellter Skill via Description-Keyword triggert"). Solche Tasks sind in der Current-Session **architecturally blocked** und brauchen eine Clean-Cut-Ceremony (siehe Pitfall #6.1).
6.1. **Clean-Cut-Ceremony bei architectural-blocked Tasks** *(fundiert 2026-07-06, Plan `workflow-templates-skill.md` Tasks 9+10)*: Wenn Verifikations-Tasks in der aktuellen Session nicht ausführbar sind (Loader-Cache, Reboot-abhängig, Cron-Tick-abhängig, External-Service-Setup-abhängig): nicht drumrum hacken, nicht still "open" lassen, nicht mit halbem Workaround tarnen. Stattdessen:
   (a) **Plan-Footer** mit explizitem `## Status` Block anhängen: `✅ Abgeschlossen: Tasks 1-N` + `🛑 Pending (blockiert): Tasks X-Y` mit **genauem Grund** (verlinkt auf den Pitfall der das blockiert)
   (b) **Eine** Mnemosyne-Memory mit `importance=0.6-0.7` (niedriger als Wissen — ist Hand-off), `veracity="stated"` (nicht "tool" — Arbeit wurde nicht verifiziert), `valid_until=<+7 Tage>` (Auto-Cleanup), und `source="<domain>-task-pending"` (eigener Namespace). Memory-Inhalt enthält **inline Eskalations-Clause**: "wenn diese Memory nach <Datum> noch existiert, in Telegram DM @OlympAgentBot eskalieren".
   (c) **Choice-Moment** vor User: 2-4 konkrete Cut-Optionen anbieten (Status-fixieren + Brücke, Quick-Workaround via expliziten `skill_view`, alles offen lassen), nicht offene "was willst du machen?"-Frage.
   (d) **"Skill loadable" ≠ "Skill auto-triggert"** unterscheiden: `skill_view('neuer-skill')` umgeht den Loader-Cache und lädt den Skill — funktioniert in current session. Tasks die **Auto-Discovery via Description-Keyword** verifizieren, brauchen aber zwingend eine fresh session. Diese Unterscheidung entscheidet ob Cut-Ceremony überhaupt nötig ist.
7. **Sub-Agent-Claims blind vertrauen**: Sub-Agents retournieren plausible Self-Reports ("0→123 Zeilen, 18 Links"), aber die Datei existiert **gar nicht**. Das `write_file`-Tool meldet dem Sub-Agent `success`, aber die Datei landet nicht auf Disk. **Immer selbst verifizieren**: nach jedem Sub-Agent-Batch `terminal("stat --format=%s <pfad>")` oder `read_file(path)` auf jede behauptete Datei laufen lassen. Das ist KEIN optionaler Step, sondern Teil der Königin-Pflicht. *Fundiert in Phase-6-Einsatz 2026-07-05: Cluster 1 behauptete MOC-Daily-Notes.md erstellt zu haben — existierte nicht.*
8. **Leaf-Agents können kein Mnemosyne**: `mnemosyne_remember` ist für leaf-role gesperrt. Wenn ein Sub-Agent einen Hook setzen soll → Hook als JSON-Struct im self-report ausgeben lassen (z.B. `~/.hermes/state/<cluster>-hooks.json`), und die Königin setzt ihn **inline** nach Batch-Completion. *Fundiert in Phase-6: Cluster-4-Subagent hat Hook-JSON abgelegt, Königin hat nachgesetzt.*
9. **Staffel-Pattern ignorieren bei 4+ Clustern**: Alle Cluster gleichzeitig feuern → Queue-Überlast, Patch-Konflikte, schweres Rollback. Bei ≥4 Clustern **immer gestaffelt**: (a) kritischen Cluster zuerst (Zero/Thin-Fix), (b) dann restliche parallel, (c) Königin inline nach allen. *Fundiert in Phase-6: User explizit "staffeln, mehr Sicherheit".*

## Verification Checklist

Nach jedem Template-Einsatz:

- [ ] Decision-Tree gewählt, nicht geraten
- [ ] Constraint-Check durchgeführt
- [ ] Phase-1-Freigabe von the user erhalten
- [ ] Backup vor destruktiven Schritten
- [ ] Verify-Kommandos nach jedem Schritt (Testplan)
- [ ] Rollback-Pfad für jeden Block dokumentiert
- [ ] Mnemosyne-Hook nach Session-Ende (QUEEN setzt Hooks, nicht Sub-Agent)
- [ ] Bei Lessons-Learned: Skill-Patch via `skill_manage(action='patch', name='workflow-template', ...)`
- [ ] **Sub-Agent-Claim-Verification**: Nach jedem Sub-Agent-Batch: JEDE behauptete Datei-Erstellung mit `stat --format=%s` oder `read_file` prüfen. Sub-Agent-behauptete "erledigt"-Claims sind NICHT verlässlich.
- [ ] **Staffel-Entscheidung dokumentiert** (parallel vs. gestaffelt, Begründung)

## Related Skills

- `multi-agent-master-workflow` — Pattern-Lieferant (Queen/Worker/Gate)
- `plan` — Implementation-Pläne ohne Domain-Kontext
- `subagent-driven-development` — Multi-Agent Phase-2 Pattern
- `delegation-anti-patterns` — Was man NICHT tun sollte bei Sub-Agents
- `hermes-agent-skill-authoring` — Skill-Conventions

## Maintenance

Versionierung: `MAJOR.MINOR.PATCH` in `SKILL.md` Frontmatter. Updates:
- Neues Domain-Template: MINOR bump
- Breaking Change in Phase-1-Output-Schema: MAJOR bump
- Pitfall/Fix ergänzt: PATCH bump

Bei jedem Update: CHANGELOG-Eintrag in `references/meta/changelog.md`.

## Strategy-Updates (Audit-Trail)

| Datum | Change | Begründung | the user-Hook |
|-------|--------|-----------|-----------|
| 2026-07-05 18:50 | Reasoning effort `high` → `xhigh` (subagent + king) | "wir haben es nicht eilig, sei genau und prüfe nach" | strategy-shift Mnem-`c608318c5004fa91` |

## Reasoning-Effort-Audit

**Current default**: `xhigh` (= max, slowest, highest quality).

**Trigger zum Wechsel zurück auf `high`**:
- the user sagt explizit "schneller bitte"
- Stage-3-Pipeline-Runs dauern > 10 Min regelmäßig
- Bei trivialen Tasks (Single-File-Edit, Drop-in-Replacement)

**Trigger zum Wechsel auf `xhigh`**: immer Default seit 2026-07-05 18:50.

Laufzeit-Erwartung pro Reasoning-Level (empirisch 2026-07-05):
- `high` (vorher): 5-7 Min pro Cluster
- `xhigh` (jetzt): 7-10 Min pro Cluster, dafür gründlichere Anti-Halluzination + Pattern-Anwendung
