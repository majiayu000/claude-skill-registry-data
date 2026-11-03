---
name: llm-text-hygiene
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-07-04
updated: 2026-09-27
description: Entfernt KI-Spuren, Chat-Reste, Platzhalter und LLM-Stilmuster aus fertigen Texten und prüft die AI-Disclosure auf Vollständigkeit und korrekten Sitz.
standalone: true
anthropic_compatible: true
category: utilities
tags: [ai-disclosure, text-hygiene, qa, llm-cleanup, style-review]
status: active
language: de
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
---

<img src="banner.png" width="100%" alt="llm-text-hygiene banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


> **English Translation** — Official English version of `llm-text-hygiene`.



# LLM-Text-Hygiene — KI-Spuren aus fertigen Texten entfernen (Deutsch)

## Übersicht & Zweck

KI-gestützt entstandene Texte sammeln Rückstände, die im Entwurf unsichtbar bleiben und
erst im publizierten Dokument peinlich werden: Gesprächsfetzen aus der Chat-Session,
Regieanweisungen, die aus der Argumentationsstruktur herausfallen, Danksagungen an das
Sprachmodell, stehengebliebene Platzhalter, aufdringliche LLM-Stilmuster — und eine
AI-Disclosure, die fehlt, falsch platziert oder nicht mehr wahr ist. Dieser Skill ist der
systematische Reinigungs-Pass davor: prüfen, konservativ bereinigen, Disclosure richtig
stellen. **Er verändert nie die Substanz** — er entfernt, was nicht Teil des Werks ist.

## Prüfkatalog

Fünf Befundklassen, von eindeutig (direkt fixen) nach heikel (nur markieren):

### 1. Chat-Residue und Regieanweisungen (eindeutig → streichen/ausbessern)

Sätze, die zur ENTSTEHUNG des Texts gehören, nicht zum Text: „Wie besprochen lassen wir
diesen Teil im Paper, da …", „Hier ist der überarbeitete Abschnitt:", „Gerne ergänze
ich …", übrig gebliebene Prompt-Fragmente, Meta-Kommentare an den Auftraggeber.
**Erkennungsprinzip:** Der Satz fällt aus der Text- und Argumentationsstruktur heraus —
er adressiert eine Gesprächssituation statt den Leser. Beim Streichen prüfen, ob ein
inhaltlicher Rest gerettet werden muss (Begründung in Fußnote/Text überführen).

### 2. Platzhalter und Baustellen-Marker (eindeutig → auflösen)

`[TODO: …]`, `[Referenz einfügen]`, `XXX`, `<hier Beispiel>`, leere Abschnitte mit
Überschrift, „(Quelle?)". Auflösen oder — wenn nicht auflösbar — als echte offene
Aufgabe in die Projekt-TODO überführen und aus dem Deliverable entfernen.

### 3. LLM-Danksagungen und Anthropomorphes (eindeutig → entfernen)

Danksagungen an ChatGPT/Claude/Gemini & Co. gehören nicht in die Danksagung — Werkzeuge
werden nicht bedankt, ihr Einsatz wird in der AI-Disclosure deklariert. Ebenso entfernen:
anthropomorphe Formulierungen über das Werkzeug („die KI schlug freundlicherweise vor").

### 4. AI-Disclosure (prüfen → korrigieren)

- **Vorhanden?** Wenn das Dokument KI-gestützt entstand und Venue/Projekt eine Disclosure
  verlangt oder vorsieht: existiert der Abschnitt?
- **Korrekt?** Beschreibt sie den tatsächlichen Einsatz (nicht unter-, nicht übertrieben)?
  Nutzt sie das Disclosure-Schema des Projekts/der Venue, falls eines definiert ist
  (z. B. abgestufte Level)?
- **Richtig platziert?** An der venue-üblichen Stelle (Methoden/Acknowledgements-Umfeld/
  eigener Abschnitt), identisch in allen Sprachfassungen.

### 5. LLM-Stilmuster (heikel → nur klare Fälle fixen, Rest markieren)

Formelhafte Übergänge („Zusammenfassend lässt sich sagen", „Es ist wichtig zu betonen"),
Aufzählungs-Inflation wo Fließtext hingehört, „nicht nur … sondern auch"-Ketten,
Gedankenstrich-Dichte, Hedging-Floskeln, im Englischen die bekannten Marker (u. a.
„delve", „tapestry", „it's worth noting"). **Vorsicht:** Stil ist Urheber-Territorium —
nur eindeutige Formelhaftigkeit glätten, alles andere als Befundliste an den Autor geben
statt den Text umzuschreiben. Ein menschlich klingender Text ist nicht das Ziel des
Skills; das Ziel ist ein Text ohne Fremdkörper.

## Ablauf

1. **Scope klären:** Welche Deliverables (Dateien), welche Sprachfassungen? Änderungen
   IMMER synchron über alle Fassungen (Abgleich: `bilingual-doc-sync`).
2. **Mechanischer Scan:** Volltextsuche nach den Signal-Mustern (Tabelle unten) —
   billig, findet Klasse 2/3 und Teile von 1 zuverlässig.
3. **Lese-Pass:** Das Dokument entlang der Argumentationsstruktur lesen — Klasse-1-Funde
   erkennt man nur strukturell (Satz adressiert Gespräch statt Leser). Besonders prüfen:
   Abschnittsanfänge/-enden, Danksagungen, Einleitung/Fazit (dort landet Residue zuerst).
4. **Bereinigen:** Klassen 1–3 direkt fixen (konservativ, Substanz erhalten), Klasse 4
   korrigieren, Klasse 5 als Befundliste ausgeben; nur eindeutige Fälle direkt glätten.
5. **Dokumentieren:** Was gefunden/geändert/nur markiert wurde — bei Papern mit
   Versionierungspflicht vermerken, ob eine neue Version/ein Re-Upload nötig wird.
6. **Periodisch über einen Bestand:** mit `rotation-check` kombinieren (ein Dokument/
   Projekt pro Lauf, Registry als Gedächtnis).

**Optionales Werkzeug für Klasse 5 und AI-Disclosure:** Auf ausdrücklichen Nutzerwunsch —
nie automatisch — kann [`pasta-press`](https://github.com/ellmos-ai/pasta-press)
(öffentliches Repo, 100 % lokal über Ollama) zur Stilveredelung eingesetzt werden:
`pastapress process <datei>` bzw. `pastapress text "…"`. Grenze aus den Red Flags oben:
Dieser Skill poliert nicht selbst — pasta-press ersetzt nicht den Lese-Pass, und die
Markerbereinigung (Klassen 1–4) bleibt eine Prüfentscheidung dieses Skills, unabhängig
davon, ob pasta-press eingesetzt wird.

## Signal-Muster für den mechanischen Scan

| Klasse | Suchmuster (DE) | Suchmuster (EN) |
| --- | --- | --- |
| Chat-Residue | „wie besprochen", „wie gewünscht", „hier ist", „gerne", „im Chat", „wie du sagtest", „lassen wir" | "as discussed", "as requested", "here is the", "I have added", "per your" |
| Platzhalter | `TODO`, `XXX`, `[…einfügen]`, `<…>`, „Quelle?" | `TBD`, `[insert`, `placeholder`, `citation needed` |
| LLM-Dank | „Dank an ChatGPT/Claude/Gemini", „mithilfe von KI erstellt" (außerhalb Disclosure) | "thanks to ChatGPT/Claude", "grateful to the AI" |
| Stilmarker | „zusammenfassend lässt sich", „es ist wichtig zu betonen", „nicht nur … sondern auch" | "delve", "tapestry", "it's worth noting", "in conclusion" |

Die Tabelle ist Startpunkt, kein Filter-Ersatz: Muster liefern Kandidaten, die Entscheidung
fällt im Kontext (Schritt 3–4). Für rein mechanische Zeichen-Hygiene (Emoji-Scan,
Steuerzeichen, kaputte Umlaute) vorhandene Werkzeuge nutzen — Encoding-Schäden sind
`encoding-fix`-Territorium, nicht dieses Skills.

## Beispiel & Anwendung

```text
Auftrag: „Prüf das Paper vor dem Upload auf KI-Rückstände."

1. Scope: paper_de.tex + paper_en.tex.
2. Scan: 1× "as discussed" (EN, Abschnitt 4), 1× "[TODO: Referenz Smith]" (beide),
   Danksagung erwähnt "wertvolle Hilfe von Claude".
3. Lese-Pass: In der Einleitung ein Satz, der den Reviewer direkt adressiert
   („Diesen Einwand behandeln wir wie gewünscht in 3.2") → Regieanweisung.
4. Fixes: Regieanweisung gestrichen (Inhalt steckte schon in 3.2), TODO als Aufgabe
   in TODO.md überführt + Platzhalter entfernt, LLM-Dank gestrichen, stattdessen
   AI-Disclosure-Abschnitt auf tatsächlichen Einsatz präzisiert — alles in DE und EN.
5. Vermerk: inhaltliche Änderung → neue Paperversion nötig, in TODO.md eingetragen.
```

## Red Flags

| Gedanke | Realität |
| --- | --- |
| „Ich schreibe den Text gleich flüssiger" | Substanz und Stimme gehören dem Autor — der Skill entfernt Fremdkörper, er poliert nicht. |
| „Stilmarker gefunden → löschen" | Klasse 5 wird markiert, nicht automatisch umgeschrieben; nur eindeutige Formelhaftigkeit glätten. |
| „Die deutsche Fassung reicht" | Residue sitzt oft nur in EINER Fassung — immer alle Sprachfassungen prüfen und synchron halten. |
| „Disclosure raus, dann ist es sauber" | Falsch herum: LLM-Dank raus, korrekte Disclosure REIN — Verschleiern ist keine Hygiene. |

## Verwandte Skills & Werkzeuge

- `encoding-fix` — Byte-/Encoding-Reparatur (Mojibake); dieser Skill hier arbeitet auf Inhaltsebene.
- `bilingual-doc-sync` — Synchronhaltung der Sprachfassungen, in die Fixes eingepflegt werden.
- `rotation-check` — Gerüst für den periodischen Lauf über einen Dokumentbestand.
- `textproduction` — Text-Erzeugung (dieser Skill ist die QA danach).
- [`pasta-press`](https://github.com/ellmos-ai/pasta-press) — externes, öffentliches Werkzeug
  (kein Skill dieser Bibliothek): lokale KI-Textpresse via Ollama für Stilveredelung,
  Übersetzung und Marker-Entfernung. Optional für Klasse 5, nur auf Nutzerwunsch — dieser
  Skill poliert nicht selbst (siehe Red Flags und Ablauf).

## Änderungsprotokoll

### 1.1.0 (2026-09-27)
- `pasta-press` (öffentliches Repo `ellmos-ai/pasta-press`) als optionales Werkzeug für
  Klasse 5 (Stilmuster) und AI-Disclosure-Veredelung aufgenommen — nur auf Nutzerwunsch,
  Markerbereinigung bleibt Prüfentscheidung dieses Skills. Abschnitt „Verwandte Skills"
  zu „Verwandte Skills & Werkzeuge" erweitert. Alle sieben Sprachfassungen synchron
  aktualisiert; `SKILL.fr.md` war dabei tatsächlich unübersetzter deutscher Text unter
  französischem Deckblatt — als echte französische Übersetzung nachgezogen.

### 1.0.0 (2026-07-04)
- Initiale Version. Abstrahiert aus der Codex-Automation „research-llm-muster-check"
  (Chat-Anteile in Papern, LLM-Danksagungen, AI-Disclosure) und auf beliebige
  Deliverable-Texte verallgemeinert; Prüfkatalog um Platzhalter, Stilmuster und
  Scan-Signaltabelle erweitert.