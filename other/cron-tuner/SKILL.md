---
name: cron-tuner
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-01
updated: 2026-08-23
language: de
visibility: public
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [cadence, scheduler, cooldown, backoff, self-tuning, cron]
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
description: Selbstjustierende Takt-Regelschleife für wiederkehrende Agenten-Scans. Nutzen, wenn ein geplanter Scan sein Intervall bei Aktivität schärfen und bei Stille abkühlen soll, ohne Operator-Eingriff.
---

<img src="banner.png" width="100%" alt="cron-tuner banner">

# cron-tuner — selbstjustierende Takt-Regelschleife

Eine **selbstjustierende** Regelschleife für wiederkehrende, zeitplangetriebene
Arbeit (Cron-Jobs, geplante Aufgaben, Timer). Statt eines festen Intervalls
passt der Job seinen eigenen Takt an: er schärft bei Arbeit und kühlt bei
Stille ab. Host- und plattformneutral; das Muster funktioniert mit jedem
Scheduler.

## Wann nutzen

- Ein wiederkehrender Scan (Mailbox-Watch, Sync-Yard-Scan, Queue-Poll) soll
  während eines aktiven "Match" schnell reagieren und in Leerlaufphasen
  günstig bleiben.
- Die Anpassung soll **auditierbar** sein (eine State-Datei) statt implizit
  in einer Konversation oder im Kopf einer Person.

## Konzepte

- **Regelschleife**: messen → entscheiden → handeln → persistieren. Jeder
  Lauf endet mit dem Schreiben seines States; jeder Lauf beginnt mit dessen
  Lesen.
- **Aktivierung**: neue Arbeit gefunden → direkt auf das schnellste
  Intervall springen.
- **Cooldown-Leiter**: leere Läufe rücken eine Leiter herab; jede Stufe
  gilt nur, wenn sich das Intervall tatsächlich ändert.
- **Deckel**: niemals über ein definiertes Maximalintervall hinaus
  entspannen.

## Referenzschema

| Bedingung | Neues Intervall |
|---|---|
| neue Arbeit gefunden | schnellstes (z. B. 15 min) |
| 4 aufeinanderfolgende leere Läufe | 30 min |
| 6 aufeinanderfolgende leere Läufe | 1 h |
| jeder weitere leere Lauf | verdoppeln (2 h, 4 h, 8 h) |
| Deckel | 24 h (niemals höher) |

Die Schwellen auf die Arbeitslast abstimmen; die Verdopplung einfach und den
Deckel explizit halten.

## State-Datei (Pflicht)

Eine kleine JSON-Datei je Worker, z. B. `cron-tuner-state.json`:

```json
{
  "empty_runs": 0,
  "interval_minutes": 15,
  "note": "cron-tuner state"
}
```

Regeln:

1. **Datei, nicht Gedächtnis.** Der Zähler muss Kontext-Kompaktierung,
   Session-Neustarts und Operator-Wechsel überleben und für Menschen und
   andere Agenten einsehbar sein. Den Takt nicht in der Konversationshistorie
   verfolgen.
2. **Nur bei Änderung neu schreiben.** Den State bei jedem Lauf persistieren,
   aber den geplanten Job nur ersetzen, wenn sich das Intervall tatsächlich
   ändert.
3. **Neuer Job = neuer Zeitplan, gleicher State.** Ein Taktwechsel bedeutet,
   den alten Job zu löschen und einen neuen mit dem neuen Intervall
   anzulegen; der Zähler läuft weiter.

## Betriebsregeln

- **Arbeit entscheidet, nicht Stimmung.** Nur beobachtete Ankünfte ändern
  den Takt — niemals Erwartungen oder Näherungen.
- **Anti-Herden-Offsets.** Volle-Stunde- und Halbe-Stunde-Marken für das
  schnellste Intervall meiden (z. B. Minuten 7/22/37/52), damit Flotten
  nicht im Gleichschritt feuern.
- **Fail-Safe:** Verstummt ein Partnersystem, gilt die normale
  Vakanz-/Abwesenheitsregel — der Tuner eskaliert nie in Poll-Fluten.
- **Belege:** Jeder Taktwechsel wird mit Grund, altem und neuem Intervall
  protokolliert.

## Erweiterbarkeit (Registry der Loop-Typen)

Der Skill ist die Heimat für weitere selbstjustierende Loop-Typen über die
Zeit:

- **cooldown** (dieses Schema: Stille → langsamer)
- **backoff** (Fehler → langsamer, Erfolg → schneller)
- **burst** (Ankunfts-Spitze → temporärer Schnellmodus mit explizitem Ende)
- **wake-assist** (externe Wake-Nachricht → sofortiger Lauf außerhalb des
  Zyklus)

Neue Loop-Typen bekommen hier ein Unterkapitel plus ihr eigenes
State-Datei-Schema.
