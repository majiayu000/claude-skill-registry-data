---
name: capabilities-registry
description: Use when asked what this install can do or what is pushed.
---

# Capabilities Registry — was dieses System hat, kann und veröffentlicht hat

## Wofür

Wenn jemand (der Nutzer, ein Cron-Job, ein Peer) fragt *„kannst du X?"*, *„was hast du?"*,
*„funktioniert Y wirklich?"* oder *„was ist schon gepusht?"* — dann ist die Antwort **nicht**
aus dem Gedächtnis zu erfinden, sondern aus zwei Artefakten zu lesen:

- `../CAPABILITY_STATUS.md` — Tabelle: Fähigkeit | Was es ist | **Beleg (gemessen)** | **Gepusht**
- `../capability_inventory.json` — dieselben Daten maschinenlesbar, mit Zeitstempel

## Die Regel, die hier zählt

**Keine Statusaussage ohne Messung.** Jede Zeile trägt in der Belegspalte die Beobachtung,
die sie stützt (Datum + was tatsächlich passiert ist). Wenn eine Fähigkeit nicht in der
Tabelle steht oder ihr Beleg älter ist als die letzte Änderung am Code, gilt sie als
**unbekannt** — nicht als „funktioniert".

## Auffrischen (statt raten)

```
python scripts/capability_inventory.py
```

Das Script misst alle mechanischen Werte neu (Ports, Dateien, Token, Git-Zustand,
Job-Registrierungen) und merged sie mit den handgeprüften Einträgen. Es ist der Job
**„Capability Inventory (self-audit)"** (täglich 05:00) — der Lauf ist still, wenn sich
nichts geändert hat.

## Statusvokabular

| Zeichen | Bedeutung |
|---|---|
| ✅ works | Läuft und wurde mit einem konkreten Ergebnis belegt. |
| 🟡 partial | Läuft, aber mit bekannten Lücken (z. B. Commits nur lokal, nicht gepusht). |
| ❌ broken | Defekt — mit dem Fehler in der Belegspalte. |
| ⚪ unused | Vorhanden, aber nie ausgeführt. Zählt **nicht** als funktionierend. |
| 🔒 blocked | Wartet auf eine Entscheidung von außen (z. B. Veröffentlichung). |

## Bekannte Fallen (aus echten Fehlschlägen)

- **Ein Feature-Label ist kein Beweis.** In diesem Install lieferte der Swarm Floskeltext
  in 0 ms (ImportError still geschluckt), `swarm create` stürzte bei jedem Aufruf ab und die
  Lern-Pipeline hatte keinen Fahrer. Alle drei sahen „implementiert" aus.
- **Push-Status prüfen, nicht annehmen.** Ein Commit im Installationsbaum ist **nicht**
  draußen. Erst `git branch -r --contains HEAD` oder die PR-Nummer in der Tabelle zählt.
- **Zeichen ≠ Bytes.** Das Skill-Limit von 100.000 gilt in Zeichen; eine Byte-Messung
  meldet fälschlich Überschreitungen bei Umlauten.
- **Grün aus dem Log ist kein Beweis für Wirkung.** Ein Job-Lauf kann „succeeded" melden,
  während die Ausgabe leer ist (still geschluckter Fehler). Erst das Artefakt prüfen.
