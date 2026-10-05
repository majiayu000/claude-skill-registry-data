---
name: zweitfiliale-zuordnung
description: Weist Mitarbeitern ohne Zweitfiliale (Cơ sở phụ) automatisch die geografisch nächstgelegene Filiale zu, basierend auf ihrer echten Wohnadresse aus Welo und den echten Filial-Adressen. Benutze dieses Skill IMMER, wenn der Nutzer über eine neue Filiale/neues tiệm/chi nhánh mới spricht, wenn neue Mitarbeiter ohne cơ sở phụ/Zweitfiliale hinzugekommen sind, oder wenn explizit nach "gắn cơ sở phụ", "Zweitfiliale zuordnen", "nächste Filiale" oder einer aktualisierten Personal-/Filialenliste (Excel) gefragt wird — auch wenn der Nutzer nicht wörtlich "Skill" sagt.
---

# Zweitfiliale-Zuordnung (nächstgelegene Filiale)

## Warum dieses Skill existiert

Mitarbeiter, die keine Zweitfiliale (Cơ sở phụ) haben, tauchen in keinem
Filial-Pool auf und werden bei der Urlaubsplanung (siehe die
`plan-urlaub-*.js`-Skripte in `automation/src/`) isoliert behandelt — sie
können dann niemandem als Vertretung dienen und niemand kann für sie
einspringen. Eine sinnvolle Zweitfiliale ist eine, die der Mitarbeiter
tatsächlich real erreichen kann — am besten ermittelt über die echte
Entfernung zwischen Wohnort und Filiale, nicht über Vermutungen anhand von
Stadtnamen.

## Schnellweg: 1 neuer Mitarbeiter (häufigster Fall)

Wenn nur 1 (oder wenige) neue Mitarbeiter dazugekommen sind und deren
Filiale bereits existiert, reichen 2 Befehle — kein Grund, alle 71
Mitarbeiter erneut abzufragen:

```bash
cd C:\Users\Public\GLSC\automation
node src/sync-employee-address.js        # findet automatisch nur die neue Person (siehe Schritt 2)
node src/compute-nearest-filiale.js      # berechnet automatisch nur fuer die neue Person (noch ohne Zweitfiliale)
# Ergebnis kurz pruefen (Ausreisser? siehe Schritt 3), dann:
node src/compute-nearest-filiale.js --apply
```

Nur wenn eine komplett neue FILIALE dazukommt (nicht nur ein neuer
Mitarbeiter an einer bestehenden), erst Schritt 1 unten ausführen.

## Voraussetzungen (bereits vorhanden, nicht neu bauen)

- Repo: `C:\Users\Public\GLSC` (NICHT der OneDrive-Pfad — siehe Projekt-Memory).
- Firestore-Collections: `emps` (Mitarbeiter, Feld `zweit`), `emp_welo`
  (u.a. Wohnadresse), `filialen_meta` (Filial-Adressen, Feld `region`
  `'west'`/`'ost'`).
- Skripte (alle in `automation/src/`, mit `node.exe <script>` von
  `automation/` aus aufrufen — Node-Pfad: siehe `.env`/vorherige Läufe, i.d.R.
  `C:\Users\DoungDucThang\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\node.exe`):
  - `sync-employee-address.js` — holt Wohnadressen von Welo.
  - `compute-nearest-filiale.js` — berechnet nächstgelegene Filiale + trägt sie ein.
  - `export-personnel-data.js` + `build_personnel_excel.py` — bauen die
    Excel-Referenzdatei.

## Ablauf

### 1. Neue Filiale? Erst die Adresse eintragen

Wenn eine komplett neue Filiale (nicht nur ein Mitarbeiter ohne
Zweitfiliale) dazugekommen ist, muss sie zuerst in `filialen_meta` stehen,
sonst kann Schritt 3 sie nicht als Kandidat berücksichtigen. Ort/Straße
lassen sich fast immer über die offizielle Sushi-Circle-Restaurant-Seite
oder eine Web-Suche nach `"Sushi Circle" <Supermarkt> <Stadt> <Straße>`
finden (Beispiel-Recherche siehe Konversation vom 04.09.2026 für
Bergneustadt/Bergisch Gladbach/Köln/Neuss/Bergheim). Trage die Adresse ein:

```js
db.collection('filialen_meta').doc(marktNr).set({
  name, marktNr, ort, strasse, plz, region, active: true, updatedAt: new Date().toISOString()
});
```

Prüfe dabei die Straßenschreibweise gegen die Geocoding-Antwort in Schritt 3
(Tippfehler wie "Inudstriestr." statt "Industriestr." lassen die Geocodierung
sonst leise scheitern, ohne offensichtlichen Fehler).

### 2. Wohnadressen aktuell halten

```bash
node src/sync-employee-address.js                  # NUR wer noch keine Adresse hat (Standard, schnell)
node src/sync-employee-address.js 340301 350153     # gezielter Refresh (z.B. nach Umzug) — erzwingt Neuladen
```

**Wichtig für den Normalfall "1 neuer Mitarbeiter":** ohne Argumente fragt
das Skript NICHT alle 71 Mitarbeiter erneut ab, sondern nur die, für die
in `emp_welo` noch kein `strasse`-Feld steht (Auftrag t.duong 04.09.2026:
"nur die neue Person nachschlagen, nicht alle"). Sind alle bereits
bekannt, beendet sich das Skript sofort ohne Welo-Login. Für einen
einzelnen neuen Mitarbeiter reicht also einfach der Aufruf ohne Argumente
— es wird ganz von selbst nur diese eine Person nachschlagen.

Loggt sich bei Welo ein, geht über `Personal > Suche "*"` (zeigt alle
zugeordneten Mitarbeiter) und liest pro Person die Detailseite
`/pf/info/{PersonalNr}.html` — Felder `Strasse:` und `PLZ / Ort:`. Schreibt
nach `emp_welo/{id}.{strasse, plz, ort}`. Läuft unter `withWeloLock`, also
sicher parallel zu anderen Welo-Syncs.

### 3. Nächstgelegene Filiale berechnen (erst OHNE --apply ansehen!)

```bash
node src/compute-nearest-filiale.js                 # nur wer noch keine Zweitfiliale hat
node src/compute-nearest-filiale.js 340301           # gezielt fuer 1 Person (auch wenn schon eine Zweitfiliale gesetzt ist)
```

Geocodiert Filial- und Mitarbeiter-Adressen kostenlos über OpenStreetMap
Nominatim (kein API-Key nötig, aber max. 1 Anfrage/Sekunde — das Skript
wartet das selbst ab; Filial-Koordinaten werden dauerhaft in
`filialen_meta.lat/lon` zwischengespeichert, werden also nie zweimal
geocodiert) und berechnet die echte Luftlinien-Entfernung (Haversine) zu
jeder anderen Filiale in derselben Region. Ergebnis landet in
`output/naechste_filiale_vorschlag.json` — dort auch `top3` je Person, für
den Fall, dass der nächstgelegene Vorschlag aus anderen Gründen nicht
passt.

**Öffentliche Verkehrsmittel bevorzugen, nicht nur Luftlinie:** die meisten
Mitarbeiter haben kein Auto — eine Filiale, die per Zug/Bus schnell
erreichbar ist, ist oft die bessere Wahl als eine, die zwar näher liegt,
aber schlecht angebunden ist. Das Skript liefert `top3`, nicht nur den
einen nächsten Kandidaten, genau dafür. Ein voll automatisierter
Fahrplan-Abgleich (Deutsche Bahn HAFAS, Google Maps) war beim Testen nicht
zuverlässig genug für dieses Environment (Netzwerk-Restriktionen bzw.
Cookie-Consent-Hürden) — bei einer Person, wo der `km`-Wert für eine
begründete Entscheidung nicht ausreicht (z.B. zwei ähnlich weit
entfernte Kandidaten aus `top3`), lohnt sich ein kurzer manueller Blick:
per Browser bahn.de oder Google Maps (Reisemodus "Nahverkehr") öffnen und
die `top3`-Kandidaten miteinander vergleichen, dann den besser
angebundenen statt automatisch den kürzesten wählen.

**Gebietsleiter/Regional-Rollen werden automatisch übersprungen:** Personen,
deren `emp_welo.taetigkeit` "GL" oder "Gebietsleiter" enthält (z.B. "Region
Ost - GL + QMB"), sind nicht an 1 Filiale gebunden — eine einzelne
"nächste Filiale" ergibt für sie keinen Sinn und wird gar nicht erst
berechnet (unabhängig von der Entfernung). Das schließt automatisch auch
Herrn Nguyen, Trong (West) mit ein, dessen Zweitfiliale-Liste ohnehin
manuell auf alle 11 West-Filialen gesetzt ist (siehe
`plan-urlaub-west.js`) — er soll hier nicht versehentlich auf 1 einzelne
Filiale reduziert werden.

**Vor dem Eintragen die Ergebnisse durchsehen und Ausreißer nicht
automatisch übernehmen:** In der Praxis gab es z.B. jemanden mit ~257 km
zur nächsten Filiale (Wohnort weit außerhalb des Einsatzgebiets) — für so
jemanden ergibt eine "nächste" Filiale keinen echten Sinn und sollte dem
Nutzer als offener Sonderfall gemeldet werden statt automatisch
zugewiesen zu werden. Als Faustregel: alles über ~50 km kurz erwähnen und
nachfragen, ob es trotzdem eingetragen werden soll.

### 4. Eintragen

```bash
node src/compute-nearest-filiale.js --apply                          # alle ohne Zweitfiliale
node src/compute-nearest-filiale.js --apply 340301 350153            # nur diese
```

Trägt `naechsteFiliale` als `emps.zweit` ein — aber NUR, wenn die Person
noch keine Zweitfiliale hat (überschreibt nie eine bestehende manuelle
Zuordnung). Bei Ausreißern (siehe Schritt 3) die betroffene Personal-Nr.
einfach weglassen.

### 5. Referenzdatei aktualisieren und an den Nutzer schicken

```bash
node src/export-personnel-data.js
python src/build_personnel_excel.py
```

Erzeugt `output/personal_und_filialen.xlsx` mit zwei Tabs:
- **Filialen** — Master-Adressliste aller Filialen (West grün, Ost orange
  hinterlegt). Neue Filialen werden hier einfach angehängt.
- **Mitarbeiter** — Stammfiliale, Zweitfiliale(n), Wohnadresse; Zeilen ohne
  Zweitfiliale sind rot markiert, damit offene Fälle sofort auffallen.

Datei danach per `SendUserFile` an den Nutzer schicken.

## Kurzfassung für einen kompletten Durchlauf (alle Mitarbeiter, z.B. Ersteinrichtung)

```bash
cd C:\Users\Public\GLSC\automation
node src/sync-employee-address.js
node src/compute-nearest-filiale.js
# Ergebnisse in output/naechste_filiale_vorschlag.json durchsehen, Ausreißer (>~50km) mit Nutzer klären
node src/compute-nearest-filiale.js --apply
node src/export-personnel-data.js
python src/build_personnel_excel.py
# personal_und_filialen.xlsx an Nutzer schicken
```
