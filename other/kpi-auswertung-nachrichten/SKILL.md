---
name: kpi-auswertung-nachrichten
description: Verarbeitet die quartalsweise "Auswertung KPI X Monate"-PDF (BWA-Kennzahlen pro Filiale von der Buchhaltung/HQ) zu kurzen, verständlichen Filial-Nachrichten (Deutsch + Vietnamesisch) und trägt sie direkt in index.html ein, fertig zum Durchsehen und Versenden über die App. Benutze dieses Skill IMMER, wenn der Nutzer eine PDF mit "KPI", "Auswertung", "BWA" oder "X Monate" im Namen hochlädt oder erwähnt, auch wenn er nicht wörtlich "Skill" sagt — z.B. "hier ist die neue KPI-Auswertung", "quartalszahlen sind da", "kannst du die Filialen wieder informieren".
---

# KPI-/BWA-Auswertung → Filial-Nachrichten in der App

## Warum dieses Skill existiert

Jedes Quartal schickt die Buchhaltung eine PDF mit Umsatz/Wareneinsatz/
Personalkosten/Ergebnis pro Filiale (kommt nur per E-Mail, steht NICHT in
Axonity — kann also nicht automatisch abgeholt werden, das PDF muss der
Nutzer jedes Mal hochladen). Daraus entstehen kurze, verständliche
Nachrichten pro Filiale, die direkt in der App (nicht WhatsApp) an das
jeweilige Team geschickt werden — siehe die Karte "📊 KPI-Auswertung" im
Bereich Urlaub/Mitteilungen von `index.html` (`KPI_DRAFTS`-Array,
`kpiDraftsRender()`/`kpiDraftSend(i)`), die die Filial-Ziel-Mitteilung
(`news`-Collection, Feld `filiale`, siehe `maStartFbNews` in
`mitarbeiter.html`) wiederverwendet.

**Der eine große Stolperstein, den dieses Skill von Anfang an vermeidet:**
das PDF nennt Filialen oft anders/kürzer als die App (z.B.
"Bovenden-Industriestraße" im PDF vs. `"402207: E-Bovenden-
Industriestraße"` in echten `emps.filiale`-Werten) — und mindestens einmal
war der Name im PDF sogar ECHT falsch ("Friederichs" statt "Friedrich",
Kostenstelle 402302, live festgestellt 08.09.2026). Eine Nachricht mit
falschem `filiale`-Wert erreicht in der App NIEMANDEN (strenger
Gleichheits-Filter in `maStartFbNews`), ohne dass das auffällt. **Deshalb
immer über die Kostenstellen-Nummer matchen, nie über den Filialnamen aus
dem PDF** — siehe Schritt 3.

## Ablauf

### 1. PDF lesen und pro Filiale extrahieren

Die PDF hat eine Tabelle mit einer Zeile pro Filiale, erkennbar an der
**Kostenstellen-Nummer** (6-stellig, z.B. `402207`) — die ist der
zuverlässige Schlüssel, nicht der Filialname daneben. Für jede Filiale und
jeden Monat im Berichtszeitraum (meist ein Quartal, 3 Monate) die
tatsächlichen Euro-Werte lesen (nicht nur Prozente/Abweichungen):
- Umsatz
- Wareneinsatz (Materialkosten)
- Personalkosten
- Ergebnis (Gewinn/Verlust)

Daraus ein JSON bauen, ein Objekt pro Filiale:
```json
{
  "kostenstelle": "402207",
  "pdfName": "Bovenden-Industriestraße",
  "months": {
    "2026-06": {"umsatz": 41250, "wareneinsatz": 12100, "personal": 15800, "ergebnis": -820},
    "2026-07": {"umsatz": 43900, "wareneinsatz": 12500, "personal": 15800, "ergebnis": 640},
    "2026-08": {"umsatz": 42010, "wareneinsatz": 12300, "personal": 15800, "ergebnis": -110}
  }
}
```
In eine Datei im Scratchpad schreiben, z.B. `kpi_input.json` (alle Filialen
als Array).

### 2. Filialen den echten App-Daten zuordnen (Kostenstelle → echter Filialname)

```bash
cd C:\Users\Public\GLSC\automation
node src/match-kpi-branches.js <pfad>/kpi_input.json <pfad>/kpi_matched.json
```

Fragt live `emps` (nur `active:true`) ab, baut `Kostenstelle → echter
emps.filiale-String + region` und hängt das an jedes Objekt an
(`filiale`, `region`, `matched:true/false`). **Jede Zeile mit
`matched:false` genau ansehen und mit dem Nutzer klären**, bevor dafür eine
Nachricht gebaut wird (Tippfehler in der Kostenstelle? Filiale neu, noch
nicht in `emps`? Filiale inzwischen umbenannt/geschlossen?) — nie eine
unmatched Zeile einfach mit dem PDF-Namen weiterverwenden, das reproduziert
genau den Bug, den dieser Schritt verhindern soll.

### 3. Nachrichtentexte bauen (Deutsch + Vietnamesisch)

Pro Filiale einen kurzen Text in beiden Sprachen — Regeln, die der Nutzer
in der Vergangenheit explizit so festgelegt hat:

- **Kurz und ohne BWA-Fachjargon** — nicht jeder im Team versteht
  "Wareneinsatzquote" o.ä. Einfache Alltagssprache.
- **Konkrete Euro-Zahlen pro Monat** nennen (Umsatz, Personalkosten,
  Wareneinsatz, Ergebnis) statt nur Prozent/Trend — das Team soll sehen,
  worum es wirklich geht.
- **Kein "ruf mich an"/"lass uns zusammensetzen"/"sprechen wir darüber"** —
  die Nachricht geht an das GANZE Team der Filiale, nicht mehr 1:1 an den
  Shopleiter, ein Anruf-Angebot ergibt da keinen Sinn mehr.
- **Ton je nach Zahlen anpassen**: bei anhaltendem/wachsendem Verlust
  sachlich benennen, was auffällt (z.B. Personal- oder Wareneinsatzkosten
  im Verhältnis zum Umsatz hoch) — bei guter Entwicklung/steigendem Gewinn
  ausdrücklich loben.
- Beide Sprachfassungen inhaltlich gleich, nicht wörtlich übersetzt wo es
  im Vietnamesischen natürlicher klingt.

Vor dem Weitermachen die fertigen Texte **selbst gegen die verbotenen
Formulierungen prüfen** (grep-artig nach "telefonieren", "rufe an",
"zusammensetzen", "sprechen wir", "Anruf") — das war beim letzten Mal der
Abnahme-Check und sollte es wieder sein.

### 4. In index.html eintragen

Baut ein Array, ein Objekt pro Filiale, in `index.html` in der Variable
`KPI_DRAFTS`:
```js
{nr: 1, filiale: '402207: E-Bovenden-Industriestraße', de: '...', vi: '...'},
```
`filiale` **muss exakt** der `filiale`-Wert aus Schritt 2 sein (kein
Abtippen/Kürzen) — das ist der Wert, gegen den `mitarbeiter.html` beim
Anzeigen filtert.

**Technik zum Einfügen (bewährt aus dem letzten Durchlauf, JS-String-
Escaping ist bei ~28 Objekten von Hand fehleranfällig):**
1. Escaped-JS-Literal-Text generieren (eigenes kleines Node-Skript im
   Scratchpad, das die Werte aus `kpi_matched.json` + die gebauten Texte in
   `nr:...,\n filiale:'...',\n de:'...',\n vi:'...'` Zeilen umwandelt,
   dabei `\`, `'` und Zeilenumbrüche escapen).
2. In `index.html` die Stelle `content.indexOf('var KPI_DRAFTS = [')` bis
   `content.indexOf('\n];', searchFrom)` per Node-Skript ersetzen (nicht
   von Hand über den Edit-Tool-Diff, bei 28 langen Objekten zu
   fehleranfällig) — exakt dieselbe Technik wie letztes Mal.
3. Danach den Artikel/die Karte **"kpi-drafts-card"** kurz im Code
   gegenprüfen: sie ist aktuell über `regionRenderSwitcher()` auf
   `activeRegion==='ost'||activeRegion==='west'` beschränkt — falls
   inzwischen eine neue Region KPI-Nachrichten bekommen soll, diese Zeile
   mit erweitern.

### 5. Testen, bevor der Nutzer es sieht

- Browser öffnen (`.claude/launch.json` → `glsc-static`), als Manager
  einloggen (oder über `authGateHide()`/gemockte Session testen wie bei
  anderen Änderungen in diesem Projekt), Karte "📊 KPI-Auswertung" öffnen.
- Prüfen: alle Filialen aus Schritt 2 erscheinen als Karte, Text lesbar,
  keine der verbotenen Formulierungen aus Schritt 3 im gerenderten HTML.
- **Senden NIEMALS live gegen echte Mitarbeiter testen.** Stattdessen
  `window.fbDb` kurz durch ein Mock ersetzen (`collection().add()` fängt
  das Payload nur ab, schreibt nichts wirklich), `kpiDraftSend(i)` für 1-2
  Einträge aufrufen, Payload-Struktur (`filiale` exakt korrekt? `region`
  gesetzt?) verifizieren, danach `fbDb` wieder zurücksetzen — die im
  Projekt etablierte Vorgehensweise für "Senden" testen ohne echte Daten zu
  berühren.

### 6. Dem Nutzer zurückmelden

Kurz zusammenfassen: wie viele Filialen verarbeitet, wie viele
`matched:false` (und was damit passiert ist), auffällige Fälle (starker
Verlust/starke Verbesserung) kurz benennen — der Nutzer öffnet dann selbst
die App-Karte, liest jeden Entwurf durch und klickt pro Filiale auf Senden
(bewusst kein "alle auf einmal", siehe bestehendes UI).

## Optional: vollständiger Auswertungsbericht als Artifact

Zusätzlich zu den Kurznachrichten wurde beim letzten Mal auch ein
ausführlicher Bericht (Gebiet-Summen, Standorte mit anhaltendem Verlust vs.
starker Entwicklung, volle Vergleichstabelle) als Artifact veröffentlicht —
nur bauen, wenn der Nutzer das explizit will oder es aus dem Kontext klar
gewünscht ist, nicht automatisch bei jedem Durchlauf. Nutzt dieselben
Rohdaten aus Schritt 1, nur ausführlicher aufbereitet; `artifact-design`
Skill vorher laden.

## Kurzfassung für einen kompletten Durchlauf

```bash
# 1) PDF lesen, kpi_input.json im Scratchpad bauen (siehe Schritt 1)
cd C:\Users\Public\GLSC\automation
# 2) Filialen zuordnen
node src/match-kpi-branches.js <scratchpad>/kpi_input.json <scratchpad>/kpi_matched.json
# unmatched-Zeilen mit dem Nutzer klären
# 3) Texte bauen (DE+VI, Regeln aus Schritt 3), gegen verbotene Formulierungen prüfen
# 4) In index.html KPI_DRAFTS ersetzen (Node-Skript, siehe Schritt 4)
# 5) Im Browser testen (Karte rendert, kein verbotener Text, Send-Payload gemockt geprüft)
# 6) Nutzer Bescheid geben — er sendet pro Filiale selbst
```
