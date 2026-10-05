---
name: umsatz-wochenbericht
description: Baut den wöchentlichen "Umsatz-Maßnahmenbericht" (PDF + editierbares .docx) für die Filialen, die der Nutzer diese Woche im Fokus hat - mit echten Firestore-Zahlen (Ist-Umsatz vs. Tagesziel) als Chart. Benutze dieses Skill IMMER, wenn der Nutzer nach dem "wöchentlichen Bericht", "Umsatzbericht", "Bericht für die Fokus-Filialen" fragt oder erwähnt, was er diese Woche für 1-2 bestimmte Filialen zur Umsatzverbesserung getan hat - auch wenn er nicht wörtlich "Skill" sagt, z.B. "hier ist der Stand für Bad Hersfeld diese Woche", "kannst du den Dienstagsbericht bauen".
---

# Wöchentlicher Umsatz-Maßnahmenbericht

## Warum dieses Skill existiert

Der Nutzer (Gebietsleiter) schreibt jeden Dienstag einen Bericht: was wurde
diese Woche getan, um den Umsatz von 1-2 konkreten Filialen zu verbessern.
Der Bericht braucht echte Zahlen (nicht nur die eigene Einschätzung) - daher
zieht dieses Skill die tatsächlichen Firestore-Daten (tägliches Ist vs. das
Live-Tagesziel aus Axonity) und baut daraus einen Chart, kombiniert mit dem
Text, den nur der Nutzer liefern kann: was wurde diese Woche konkret gemacht,
und warum.

**Die Skripte liegen fest unter `automation/src/wochenbericht/`** (nicht in
`scratch/` - sie sind wiederverwendbares Werkzeug, keine Wegwerf-Skripte).
Jeder Bericht bekommt einen eigenen, frischen Arbeitsordner im Scratchpad
(z.B. `wochenbericht-kw41/`) - die Skripte selbst kennen keine bestimmte
Woche, alle Pfade kommen als Argumente.

## Feste Stil-Vorgaben des Nutzers (gelten für jeden Durchlauf)

- **Keine Gedankenstriche „—"** in jedem selbst geschriebenen Text (Rückmeldung
  28.09.2026) - stattdessen einen normalen Bindestrich „-" verwenden. Gilt für
  alle Textfelder in `week-config.json`, nicht nur für einen Abschnitt.
- **Keine alten Charts wiederverwenden.** Pro Filiale gibt es nur noch den
  täglichen Ist-vs-Tagesziel-Chart (ändert sich jede Woche wirklich) - KEIN
  Monatsumsatz-Balkendiagramm mehr, das über mehrere Wochenberichte hinweg
  identisch aussehen würde, solange sich der Kalendermonat nicht ändert
  (Rückmeldung 28.09.2026). Monats-Trends gehören als Zahl in den Analyse-Text
  (`analysis`), nicht als eigenes Chart.
- Wenn ein `systemChange`-Abschnitt Screenshots der App zeigen soll: siehe
  eigener Abschnitt unten.

## Was NUR der Nutzer liefern kann (jede Woche neu erfragen)

Kein Skript kann erfinden, was diese Woche tatsächlich unternommen wurde -
das MUSS im Gespräch mit dem Nutzer geklärt werden, bevor der Bericht gebaut
wird:
- **Welche Filiale(n)** stehen diese Woche im Fokus (Kostenstellen-Nummer,
  6-stellig, z.B. `402240` - dieselbe Nummer wie in `filiale_umsatz`/
  `filiale_produktion`, nicht raten).
- **Was wurde konkret gemacht** pro Filiale (die Maßnahme) - und **warum**
  (z.B. Personalmangel, Urlaubs-Häufung, geplanter Test).
- Ob es diese Woche ein **gebietsweites Thema** gibt, das alle Filialen
  betrifft (optional - siehe `systemChange` unten). Die meisten Wochen NICHT,
  einfach weglassen.
- Wenn eine Maßnahme von echten externen Fakten abhängt (z.B. wann an einem
  bestimmten Ort am meisten los ist), das aktiv recherchieren statt zu raten
  - siehe Beispiel Google-Maps-Stoßzeiten in der Historie dieses Skills
    (KW40: Verkostungs-Zeitfenster anhand echter "Stoßzeiten"-Daten des
    jeweiligen Marktes bei Google Maps festgelegt, inkl. Fund einer
    Feiertagsschließung, die die ursprüngliche Wochenplanung berührt hätte).

## Ablauf

### 1. Rohdaten holen

```bash
cd C:\Users\Public\GLSC\automation
node src/wochenbericht/fetch-data.js <marktNr1,marktNr2,...> <scratchpad>/data.json
```
Holt pro Kostenstelle: `filiale_umsatz` (Monatswerte, nur noch für die
Analyse-Prosa relevant), `tagesziel` (tägliches Ziel) und `filiale_produktion`
(tägliches Ist, Axonity - inkl. `produzierteWare`/`anzahlSorten`, falls für
eine Maßnahme Produktionsmengen statt Umsatz gebraucht werden, siehe KW40
Bad Hersfeld). Fehlt für eine Filiale die monatliche Historie, das im
Analyse-Text kurz erwähnen (kein eigener Chart/Hinweisblock mehr nötig, seit
der Monats-Chart komplett entfällt).

### 2. Woche-Konfiguration schreiben

Eine `week-config.json` im selben Scratchpad-Ordner, mit dem Text aus dem
Gespräch mit dem Nutzer (Schema siehe unten). Ton/Stil: sachlich, konkrete
Zahlen aus `data.json` einbauen (z.B. "-7,0 % Monatsumsatz, aber Personal-
kosten -24,3 %"), keine Floskeln, keine „—".

### 3. Bericht bauen (PDF)

```bash
node src/wochenbericht/build-report.js <scratchpad>/data.json <scratchpad>/week-config.json <scratchpad>/report.html
node src/wochenbericht/render.js <scratchpad>/report.html <scratchpad>/report.pdf
```

### 4. Editierbares .docx (immer mitliefern, siehe frühere Rückmeldung des Nutzers)

```bash
node src/wochenbericht/render-chart-pngs.js <scratchpad>/data.json <scratchpad>/week-config.json <scratchpad>/chart-png
node src/wochenbericht/build-docx.js <scratchpad>/data.json <scratchpad>/week-config.json <scratchpad>/report.docx
```
Wichtig: der Ordnername für die Chart-PNGs muss **exakt `chart-png`** heißen
(nicht umbenennen) - `build-docx.js` sucht dort fest nach `chart-png/
manifest.json`, relativ zum Ordner von `week-config.json`.

### 5. Prüfen, bevor der Nutzer es sieht

- **HTML/PDF**: es gibt kein PDF-Vorschau-Tool auf diesem Rechner (kein
  `poppler`) - stattdessen den Abschnitts-Aufbau im `report.html` direkt
  gegenprüfen (z.B. `grep "<h2>"` - Nummerierung muss lückenlos sein) und die
  Dateigröße von `report.pdf` auf Plausibilität prüfen (wächst spürbar mit
  jedem eingebetteten Screenshot, das ist normal).
- **.docx**: kein LibreOffice auf diesem Rechner - für eine schnelle
  Textprüfung reicht, die XML direkt aus der `.docx` (ZIP) zu entpacken und
  auf Stichworte zu grep(en); für eine echte visuelle Prüfung PowerShell +
  Word-COM-Automatisierung (`New-Object -ComObject Word.Application`,
  `SaveAs` zu PDF), wie beim ersten Durchlauf gemacht. Auch prüfen, wie viele
  `word/media/*`-Dateien in der `.docx` (ZIP) stecken - muss zur Anzahl
  Screenshots + Charts passen, sonst fehlt etwas beim Einbetten.
- Prüfen, dass keine „—" im gerenderten `report.html` vorkommen (z.B.
  `grep -c "—" report.html` sollte 0 sein, außer in Firmennamen o.Ä.).

### 6. Liefern

PDF **und** .docx per `SendUserFile` schicken (beide, nicht nur eins - der
Nutzer wollte in der Vergangenheit ausdrücklich beides). Kurze
Zusammenfassung: welche Filialen, auffällige Zahlen, ob eine Kostenstelle
ohne Monatshistorie dabei war.

## Schema `week-config.json`

```json
{
  "title": "Umsatz-Maßnahmenbericht",
  "subtitle": "Kalenderwoche 41 · Dienstag, 6. Oktober 2026",
  "author": "Thang Duc Duong",
  "created": "06.10.2026",
  "systemChange": {
    "heading": "Text OHNE führende Nummer - die wird automatisch vorangestellt",
    "intro": "...",
    "calloutLabel": "z.B. LÖSUNG oder HINWEIS",
    "calloutText": "Absatz 1.\n\nAbsatz 2 (durch \\n\\n getrennt = eigener Absatz in PDF UND docx).",
    "screenshots": [
      {"file": "shot1.png", "caption": "Kurzer Bildtext 1."},
      {"file": "shot2.png", "caption": "Kurzer Bildtext 2."}
    ],
    "outro": "..."
  },
  "storesIntro": "Kurzer Einleitungssatz vor den Filial-Abschnitten.",
  "stores": [
    {
      "marktNr": "402240",
      "name": "Heilbad Heiligenstadt",
      "measure": "Maßnahme diese Woche, in ganzen Sätzen.",
      "measureShort": "Kurzfassung für die Zusammenfassungs-Tabelle.",
      "analysis": "Kurzanalyse - konkrete Zahlen aus data.json, nicht nur Prozent."
    }
  ],
  "nextSteps": ["Nächster Schritt 1", "Nächster Schritt 2"]
}
```

**`systemChange` ist komplett optional** - Feld weglassen (nicht `null`
setzen, einfach den Key nicht schreiben), wenn es diese Woche kein
gebietsweites Thema gibt. Beide Renderer (`build-report.js`/`build-docx.js`)
lassen den Abschnitt dann automatisch weg **und nummerieren "Filialen im
Fokus" (1.) und "Zusammenfassung" (2.) automatisch neu** - nichts von Hand
anpassen. `screenshots[].file`-Pfade sind relativ zum Ordner von
`week-config.json` (dem Scratchpad-Ordner dieser Woche), nicht zum Skript.
`screenshots` ist ein Array - 0, 1 oder mehrere Bilder, werden paarweise
nebeneinander gesetzt (PDF: flex-wrap-Galerie, docx: 2-spaltige Tabelle).

**`region` ist ebenfalls optional** (Rückmeldung 28.09.2026: "Gebiet Ost"
sollte weg) - Feld weglassen, dann zeigt der Kopf nur noch "Gebietsleiter: ...
· Erstellt am ...". Nur wieder hinzufügen, wenn der Nutzer es für eine
bestimmte Woche ausdrücklich wieder haben will.

## Screenshots der App für `systemChange` erzeugen

Wenn der `systemChange`-Abschnitt zeigen soll, wie eine Funktion in der App
tatsächlich aussieht, gibt es keinen echten Test-Login im Browser - aber es
gibt Admin-SDK-Zugriff auf Node-Ebene (`automation/src/firestore-client.js`).
**Bevorzugte Technik (Rückmeldung 28.09.2026 - viel überzeugender als leere
Mock-Daten): echte, aktuelle Firestore-Daten per Admin-SDK abfragen und
direkt in die Render-Funktion der Seite injizieren**, statt die Seite leer/
mit erfundenen Werten zu mocken. Vorgehen (siehe `wochenbericht-kw40/
shot-inventur2.js` in der Session-Historie als Vorlage):

1. **Zuerst prüfen, ob es echte, aktuell relevante Daten gibt** - z.B. für
   Inventur: `db.collection('inventur_period').get()` nach einem Zeitraum
   durchsuchen, dessen `start`/`end` HEUTE einschließt; dann
   `db.collection('inventur_counts').where('month','==',...).get()` für die
   echten Fortschritte, und `db.collection('inventur_photos').get()` für
   echte Artikelfotos (Feld `variants[].img`, base64-Data-URL). Ergebnis mit
   `fs.writeFileSync(...)` als JSON im Wochenordner ablegen.
2. `.claude/launch.json` → `glsc-static` starten (lokaler Server für
   `mitarbeiter.html`/`index.html`).
3. Ein Playwright-Skript im Wochenordner schreiben: `page.goto()` auf die
   lokale Seite, dann per `page.evaluate()` die echten Daten aus Schritt 1
   als globale Variablen setzen (z.B. Inventur-Mitarbeiteransicht: `ivCounts`
   = echtes `counts`-Objekt, `ivPhotos` = echtes Foto-Objekt, `maSession` mit
   echtem Filialnamen/Namen; Admin-Ansicht in `index.html`: `activeRegion`,
   `invCounts` = alle echten Zählungen des Monats), dazu
   `#login-screen`/`#update-box`/`#auth-gate`/`#global-refresh-btn`
   ausblenden, `#app`/`#main-wrap` einblenden, passendes `.panel`/`.app-ico`
   aktiv setzen, danach die echte Render-Funktion selbst aufrufen (z.B.
   `ivRender()`, `invRenderSubmissions()`) - alles unveränderter
   Produktivcode, nur der Dateninput kommt vom Mock statt vom echten
   Firestore-Listener (der im gemockten Browser an den echten Security Rules
   scheitern würde).
4. **Nur wenn keine echten aktuellen Daten existieren**, auf leere Mock-Werte
   zurückfallen (Zählwerte 0, keine Fotos) - dann in der Bildunterschrift
   **nicht als "reale Live-Daten" bezeichnen**, sondern neutral als Ansicht
   der App beschriften.
5. Für Elemente, die weit unten auf einer langen Seite liegen (z.B. die
   Admin-Karte in `index.html`): **`elementHandle.screenshot({path:...})`
   verwenden, nicht manuell `boundingBox()` + `page.screenshot({clip:...})`**
   - Playwright scrollt beim Element-Screenshot selbst korrekt hin; ein
   manueller `clip()` bezieht sich auf die aktuelle Viewport-Position und
   trifft daneben, wenn das Element außerhalb der Startansicht liegt (genau
   dieser Fehler kostete in KW40 einen Fehlversuch).
6. Für eine sehr lange scrollbare Liste (z.B. alle Artikel einer Kategorie)
   trotzdem mit `boundingBox()` + `page.screenshot({clip:...H begrenzt})`
   auf eine realistische Bildschirmhöhe (~700-800px) zuschneiden - sonst wird
   das Bild absurd lang.

## Kurzfassung für einen kompletten Durchlauf

```bash
cd C:\Users\Public\GLSC\automation
node src/wochenbericht/fetch-data.js <marktNrs> <scratchpad>/data.json
# week-config.json im Gespräch mit dem Nutzer füllen (siehe Schema oben, keine „—")
# bei Bedarf: Screenshots der App erzeugen (siehe Abschnitt oben)
node src/wochenbericht/build-report.js <scratchpad>/data.json <scratchpad>/week-config.json <scratchpad>/report.html
node src/wochenbericht/render.js <scratchpad>/report.html <scratchpad>/report.pdf
node src/wochenbericht/render-chart-pngs.js <scratchpad>/data.json <scratchpad>/week-config.json <scratchpad>/chart-png
node src/wochenbericht/build-docx.js <scratchpad>/data.json <scratchpad>/week-config.json <scratchpad>/report.docx
# Abschnitts-Nummerierung/„—"-Freiheit gegenprüfen, dann PDF + docx per SendUserFile liefern
```
