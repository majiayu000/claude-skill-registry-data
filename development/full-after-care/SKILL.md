---
name: full-after-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-24
aliases: [deep-after-care, repo-after-care-full, tiefe-repo-pflege, repo-tiefenpflege]
description: >
  Tiefe Pflegerunde für ein veröffentlichtes GitHub-Repository (Stufe 2): enthält den
  vollständigen surface-after-care-Durchlauf und ergänzt ihn um drei teure Schritte —
  rechtliche Ersteinschätzung über die Law-Checker mit Wiedervorlage nach einem Jahr
  (Gutachten bleibt gitignored im Repo), Querverweise zu verwandten Repos über ALLE
  Organisationen hinweg sowie das Nachziehen aller Sprachen auf App-Ebene, nicht nur in der
  Doku. Nutze diesen Skill bei "full after care", "deep after care", "tiefe Repo-Pflege",
  "große Runde", "Repo grundlegend durchgehen", wenn ein Repo länger nicht geprüft wurde,
  vor größeren Releases oder wenn rechtliche Relevanz, Querverweise oder Mehrsprachigkeit
  ausdrücklich Thema sind. Für die günstige, oft wiederholte Runde stattdessen
  surface-after-care; für die Erstveröffentlichung github-repo-care.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, legal, i18n, cross-linking, organization, documentation]
language: de
status: active
visibility: public

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: [surface-after-care]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="full-after-care banner">
# Full After Care — die tiefe Runde (Synonym: Deep After Care)

## Wann dieser Skill greift

Nutze ihn, wenn ein veröffentlichtes Repo **grundlegend** durchgegangen werden soll: länger nicht geprüft, vor einem größeren Release, bei rechtlich relevanten Gegenständen, oder wenn die Verzahnung mit den übrigen eigenen Projekten Thema ist.

Der Unterschied zur günstigen Runde ist der Aufwand, nicht die Sorgfalt: Stufe 2 verlässt die Grenzen des einzelnen Repos. Sie fragt Fremdquellen an (Rechtslage), inventarisiert **alle** Organisationen und greift in die Anwendung selbst ein (Sprachen). Deshalb läuft sie seltener — typischerweise einmal pro Repo und Jahr oder anlassbezogen.

## Ablauf

### Stufe 1 zuerst vollständig

Führe **`surface-after-care` komplett aus** — inklusive Schritt 0 (Distributionsflächen), Privacy-Gate, Veröffentlichungsabsicht, Banner, Ist-Soll-Abgleich, README-Sprachen, Sichtbarkeit, Organisationseintrag, Issues und PRs sowie Commit, Push und Flächen-Parität. Nichts davon wird hier wiederholt oder abgekürzt.

Die drei folgenden Schritte kommen obendrauf. Sie erzeugen ihrerseits Änderungen an Doku und Code — pushe sie im selben Rhythmus wie in Stufe 1 beschrieben, in thematisch getrennten Commits.

---

### 5. Rechtliche Ersteinschätzung mit Jahres-Wiedervorlage

#### Zuerst: Ist eine Einschätzung überhaupt fällig?

Sieh in `_after-care/RECHTSCHECK.md` nach (der Ordner ist gitignored, siehe unten). Steht dort ein Prüfdatum, das **weniger als ein Jahr** zurückliegt, wird dieser Schritt **übersprungen** — auch in der tiefen Runde. Eine frische Einschätzung noch einmal einzuholen kostet Zeit und Geld und bringt nichts Neues.

Ist das Datum **älter als ein Jahr** oder existiert die Datei nicht, wird geprüft. Der Grund für die Wiedervorlage ist nicht, dass das Gutachten schlechter wird, sondern dass sich die **Rechtslage** ändert: neue Verordnungen, geänderte Schwellenwerte, neue Rechtsprechung, veränderte Plattformregeln. Ein zwei Jahre altes Gutachten kann formal korrekt und praktisch überholt sein.

Außerhalb des Jahresrhythmus ist eine Neubewertung fällig, wenn sich der **Gegenstand** geändert hat: neue Datenkategorien, neuer Vertriebsweg, neues Geschäftsmodell, Lizenzwechsel, neue Abhängigkeit mit Copyleft, Ausweitung auf einen anderen Rechtsraum.

#### Ist das Repo rechtlich relevant?

Nicht jedes Projekt braucht das. Auslöser sind unter anderem:

- verarbeitet personenbezogene Daten, auch nur lokal
- greift auf fremde Dienste, Webseiten oder Schnittstellen zu (Nutzungsbedingungen, Scraping)
- gibt Auskunft in regulierten Feldern (Recht, Medizin, Steuern, Finanzen)
- trägt fremde Marken, Namen oder Logos im Namen, in der Doku oder im UI
- enthält Abhängigkeiten mit Copyleft oder unklarer Lizenz, oder liefert fremde Inhalte mit
- richtet sich an Minderjährige, verarbeitet Zahlungen, oder fällt unter Ausfuhr-/Kryptoregeln
- trifft automatisiert Entscheidungen über Menschen oder wird als KI-System eingeordnet

Trifft nichts davon zu, halte im Laufprotokoll **fest, dass geprüft und verneint wurde** — sonst stellt die nächste Runde dieselbe Frage von vorn.

#### Einschätzung einholen

Nutze die Law-Checker (Skill `law-checker`, Modul `law-checker`) und lege ihr den konkreten Sachverhalt vor: was die Anwendung tut, welche Daten sie berührt, über welche Kanäle sie vertrieben wird, welche Lizenzen mitlaufen, an wen sie sich richtet. Je konkreter der Sachverhalt, desto brauchbarer die Fundstellen. Ergebnis ist eine Ersteinschätzung mit Paragraphen-Belegen — **keine Rechtsberatung**; bei ernsthaftem Risiko ist das Ergebnis die Empfehlung, anwaltlich prüfen zu lassen, nicht das Urteil selbst.

#### Ablage

```
_after-care/
├── LOG.md                    # Laufprotokoll beider Stufen
└── RECHTSCHECK.md            # Datum, Gegenstand, Ergebnis, Auflagen, Wiedervorlage
```

`_after-care/` gehört in die `.gitignore`. Das ist kein Versteckspiel, sondern dieselbe Regel wie in Schritt 2b der Stufe 1: interne Arbeitsdokumente sind kein Repo-Inhalt. Bei einem Gutachten kommt hinzu, dass eine öffentlich mitgelieferte Risikoanalyse als Eingeständnis gelesen werden kann und Angreifern eine Landkarte liefert. Alternativ kann die Ablage außerhalb des Repos in einem eigenen Ordner erfolgen — wichtig ist nur, dass sie beim nächsten Lauf **auffindbar** ist, sonst greift die Jahresregel nicht.

Kopfzeile der Datei, maschinell lesbar halten:

```markdown
# Rechtscheck — <Projekt>
geprüft: 2026-07-24
gegenstand: lokale Dateiverwaltung, keine Cloud, keine personenbezogenen Daten Dritter
ergebnis: unbedenklich
auflagen: Hinweis auf MIT-Lizenz der eingebetteten Bibliothek X im README
wiedervorlage: 2027-07-24
```

Was aus der Einschätzung **öffentlich** wird, sind nur die **Konsequenzen**: eine Lizenzangabe, ein Haftungsausschluss, ein Datenschutzhinweis, eine präzisierte Beschreibung dessen, was die App tut. Diese Änderungen gehören ins Repo — die Begründung dahinter nicht.

---

### 9. Querverweise über alle Organisationen

Stufe 1 fragt nur, ob das Repo auf den Organisationsseiten steht. Stufe 2 geht eine Ebene tiefer: **Welche einzelnen Repos aus allen eigenen Organisationen hängen mit diesem hier zusammen — und wissen beide Seiten davon?**

```bash
gh api user/orgs --jq '.[].login'
for ORG in $(gh api user/orgs --jq '.[].login'); do
  gh repo list "$ORG" --limit 200 --json name,description,updatedAt,isArchived,primaryLanguage
done
```

Der Ertrag entsteht nicht durch das Auflisten, sondern durch das Erkennen von Beziehungen. Relevante Typen:

- **nutzt / wird genutzt von** — echte technische Abhängigkeit in beide Richtungen
- **gehört zur selben Familie** — gemeinsame Produktlinie, gemeinsames Präfix, gemeinsame Architektur
- **löst dasselbe Problem anders** — ein Nutzer, der auf dem einen landet, will oft das andere kennen
- **Vorgänger / Nachfolger** — abgelöste Projekte brauchen einen Wegweiser, sonst landen Nutzer dauerhaft auf dem toten Stand
- **Baustein / Komposition** — Bibliothek und die Anwendung, die sie einsetzt

Setze die Verweise **bidirektional**. Eine Einbahnstraße ist der häufigste Fehler dieses Schritts: Man ergänzt im gepflegten Repo eine Liste verwandter Projekte, und in den verwandten Projekten steht nichts. Wer dort landet, findet den Weg nie zurück.

Der Rückverweis wird im Gegen-Repo also tatsächlich gesetzt — nach der **Dirty-Tree-Regel** aus Schritt 11 der Stufe 1, kurz zusammengefasst: sauberer Baum → eigener Commit und Push; dirty in anderen Dateien → pfadgenau committen, nicht pushen; dirty in der Zieldatei oder aktive Sperre → nicht anfassen. Wird der Verweis nicht gesetzt, gehört er in die Aufgabenliste des Ziel-Repos (`AUFGABEN.txt`/`TODO.md`), bei Sperre nur ins eigene Laufprotokoll. So bleibt die Runde in sich abgeschlossen, ohne fremde Arbeitsstände zu gefährden und ohne dass der Verweis verloren geht.

Formuliere Verweise nutzenorientiert, nicht als Namensliste: „**projekt-b** — liest die von diesem Werkzeug erzeugten Exporte und macht daraus Berichte" ist brauchbar, „siehe auch: projekt-b" nicht.

Archivierte und offensichtlich tote Repos werden nicht verlinkt — außer als expliziter Nachfolger-Hinweis in die andere Richtung.

Diese Inventur ist der teuerste Teil der Runde. Wenn viele Organisationen und Repos zu prüfen sind, lohnt es sich, das Ergebnis der Repo-Inventur im Laufprotokoll abzulegen, damit die nächste tiefe Runde eines anderen Repos darauf aufsetzen kann.

---

### Alle Sprachen auf App-Ebene nachziehen

Stufe 1 sorgt für die README-Sprachfassungen. Hier geht es um das **Produkt selbst**: Oberflächentexte, Meldungen, Hilfen, CLI-Ausgaben, Fehlermeldungen, Store- und Registry-Beschreibungen.

Ermittle zuerst, welche Sprachen die Anwendung technisch bereits kennt und wie sie sie verwaltet:

```bash
rg -l "gettext|i18n|locale|translations|LC_MESSAGES|\.po$|messages\.json" --hidden
fd -e po -e pot -e ftl . 2>/dev/null; ls locales/ i18n/ lang/ translations/ 2>/dev/null
```

Dann die Lücken schließen, entlang von drei Fragen:

1. **Fehlen Sprachen**, die das Projekt haben sollte? Standardsprachen sind Deutsch, Englisch, Spanisch, vereinfachtes Chinesisch, Japanisch, Russisch — bei nutzernahen Anwendungen. Bei entwicklernahen Bibliotheken ist Englisch allein oft die richtige Antwort; eine unnötige Sprache ist dauerhafte Pflegelast, kein Gewinn.
2. **Sind die vorhandenen Sprachen vollständig?** Nach jedem Feature-Zyklus hängen die Nebensprachen hinterher. Neue Schlüssel ohne Übersetzung fallen im Betrieb oft auf die Leitsprache zurück und damit gar nicht auf — deshalb hier gezielt gegen die Leitsprache diffen, statt sich auf den Augenschein zu verlassen.
3. **Ist die Sprachwahl für Nutzer erreichbar?** Eine vollständige Übersetzung, die niemand einschalten kann, wirkt wie keine. Umschalter vorhanden, Auswahl persistent, Systemsprache als Vorgabe erkannt?

Halte dich an den im Projekt etablierten i18n-Mechanismus und führe keinen zweiten daneben ein. Prüfe die Ergebnisse in der **echten Oberfläche**, nicht nur in der Ressourcendatei: zu lange Zeichenketten brechen Layouts, und fehlende Zeichensatz-Unterstützung zeigt sich erst im Rendering (fehlende CJK-Glyphen erscheinen als leere Kästen).

Zum Schluss die Flächen aus Schritt 0 der Stufe 1 mitnehmen: Store- und Registry-Beschreibungen haben eigene Sprachfelder, die von der App-Übersetzung nicht automatisch mitwandern.

## Laufprotokoll

Ergänze `_after-care/LOG.md` um einen Eintrag mit der Stufe `full`:

```markdown
## 2026-07-24 — full
- Stufe 1 vollständig gelaufen (siehe Eintrag oben)
- Rechtscheck: fällig (letzter 2025-06-02) -> neu eingeholt, Ergebnis unbedenklich,
  Auflage Lizenzhinweis Bibliothek X umgesetzt, Wiedervorlage 2027-07-24
- Querverweise: 4 Orgas / 38 Repos geprüft, 3 Beziehungen gefunden,
  bidirektional gesetzt; Rückverweis in repo-y offen (dort aktiver Lock)
- Sprachen App-Ebene: ES ergänzt (312 Schlüssel), JA auf Stand gebracht,
  Umschalter war vorhanden aber nicht persistent -> gefixt
```

## Häufige Fehler

| Fehler | Korrektur |
|---|---|
| Rechtscheck erneut eingeholt, obwohl der letzte 3 Monate alt war | Datum in `RECHTSCHECK.md` zuerst lesen — unter einem Jahr wird übersprungen |
| Rechtscheck übersprungen, weil „hat sich nichts geändert" | Die Rechtslage ändert sich unabhängig vom Projekt; ab einem Jahr wird geprüft |
| Gutachten ins Repo committet | `_after-care/` gehört in die `.gitignore`; öffentlich werden nur die Konsequenzen |
| Verneinte Rechtsrelevanz nicht dokumentiert | Auch ein „nicht relevant" ist ein Befund und gehört ins Protokoll |
| Querverweise nur im gepflegten Repo gesetzt | Bidirektional setzen, sonst ist es eine Einbahnstraße |
| Nur die eigene Orga geprüft | Stufe 2 heißt alle Organisationen — genau das unterscheidet sie von Stufe 1 |
| Verweise als blosse Namensliste | Nutzen in einem Halbsatz erklären, sonst klickt niemand |
| Neue Sprache angelegt, aber nicht im UI erreichbar | Umschalter, Persistenz und Systemsprachen-Erkennung mitprüfen |
| Übersetzung nur in der Ressourcendatei geprüft | In der echten Oberfläche prüfen — Layoutbrüche und fehlende Glyphen zeigen sich erst dort |
| Store-/Registry-Sprachfelder vergessen | Sie wandern nicht mit der App-Übersetzung mit |

## Abschluss-Checkliste

- [ ] `surface-after-care` vollständig durchlaufen (inkl. Push und Flächen-Parität).
- [ ] Rechtsrelevanz geprüft; Ergebnis dokumentiert — auch wenn verneint.
- [ ] Rechtscheck fällig gewesen? Wenn ja: eingeholt, Auflagen umgesetzt, Wiedervorlage gesetzt.
- [ ] `_after-care/` in der `.gitignore`, Gutachten nicht getrackt.
- [ ] Alle Organisationen inventarisiert, Beziehungen bestimmt.
- [ ] Querverweise bidirektional gesetzt, in den Gegen-Repos committet und gepusht.
- [ ] Wegen dirty tree oder Sperre übersprungene Gegen-Repos als offene Punkte notiert.
- [ ] App-Sprachen vollständig, Umschalter erreichbar, in der Oberfläche geprüft.
- [ ] Store-/Registry-Sprachfelder mitgezogen.
- [ ] Laufprotokoll-Eintrag mit Stufe `full` geschrieben.

## Changelog

### 1.0.0 (2026-07-24)
- Initiale Version. Stufe 2 der Repo-Nachpflege, aufbauend auf `surface-after-care`.
