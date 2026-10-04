---
name: review-content
description: Prüft Topic-JSON-Inhalte auf argumentative Qualität, Ausgewogenheit und intellektuelle Redlichkeit. Verwenden beim Erstellen neuer Themeninhalte, beim Hinzufügen von Abschnitten oder Argumenten, beim Bearbeiten bestehender Inhalte oder wenn der Nutzer eine Prüfung oder Verbesserung der argumentativen Stärke eines Factsheets wünscht.
argument-hint: "[topicId]"
allowed-tools: Read, Glob, Grep, Edit, WebSearch, Agent, AskUserQuestion, Bash(npm run lint), Bash(npm run build), Bash(node *)
---

# Inhaltliche Qualitätsprüfung für `public/data/$ARGUMENTS.json`

Ergänzt `verify-sources` (das die Datenlage prüft). Dieser Skill prüft, ob **Framing, Argumentation und Darstellung** intellektuell ehrlich sind und schwer angreifbar bleiben.

## Wann ausführen

- **Review-Modus**: Auf ausdrückliche Anfrage oder nach umfangreichen inhaltlichen Änderungen — liefert einen strukturierten Bericht
- **Autor-Modus**: Beim Erstellen oder Erweitern von Themeninhalten — Qualitätsdimensionen vor dem Schreiben als Leitplanken anwenden

## Qualitätsdimensionen

Jeder Inhaltsblock und jedes Argument MUSS diese 9 Prüfungen bestehen:

### 1. Nuance & Teilwahrheiten

Stammtisch-Aussagen sind oft nur teilweise wahr. Ein `response` darf nicht als reine „Widerlegung“ gerahmt sein, wenn der Claim einen legitimen Kern hat.

- Ist ein Claim teilweise zutreffend, dies ausdrücklich anerkennen, bevor Gegenbeweise folgen
- Formulierungen wie „Der Kern stimmt, aber…“, „Das war bis X richtig, seitdem…“ nutzen
- Kennzeichnen, wenn das `response` ein komplexes Thema schwarz-weiß behandelt

### 2. Claim-Source-Fit & Quellen-Unabhängigkeit

Die Quelle muss den konkreten Claim tatsächlich stützen. Überinterpretation ist der häufigste Fehler.

- Jeder `sourceRef` muss genau den Claim tragen, an den er gebunden ist — nicht mehr
- Stützt eine Quelle einen breiteren Trend, aber nicht die konkrete Zahl, das klar sagen
- `sourceRefs` entfernen, die den zugehörigen Inhaltsblock nicht direkt stützen

**Unabhängigkeit der Quellen:**
- Zentrale Datenpunkte (highlight-Fakten, `keyStats`, Kernzahlen in Argument-Antworten), die **allein** auf einer interessengebundenen Quelle beruhen (Verbände wie GDV/ADAC/BDA/DGB, Stiftungen mit Agenda, Auftragsstudien) → ⚠-Befund: amtliche/wissenschaftliche Quelle oder unabhängige Zweitquelle vorschlagen
- Ersatzweise muss die Herkunft im Text ausgewiesen sein („laut Branchenverband GDV …") statt die Zahl als neutralen Fakt zu präsentieren
- Auf Topic-Ebene prüfen: Hängt die Datenbasis einer ganzen Sektion an einem einzigen Herausgeber?

### 3. Annahmen-Transparenz

Kostenrechnungen und Projektionen müssen ihre Annahmen ehrlich offenlegen.

- Alle Rechnungen brauchen explizite Prämissen (Energiepreis, Nutzung, Region, Gebäudetyp)
- Sensitivität zeigen: Was ändert sich unter weniger günstigen Bedingungen?
- Bereichsangaben (`range_bar`) oder Einschränkungen in `text`-Blöcken bei unsicheren Projektionen nutzen
- Rechnungen kennzeichnen, die nur das Best-Case-Szenario zeigen

### 4. Fakt vs. Bewertung

Daten und Interpretation strikt trennen.

- `fact`- und `stat_grid`-Blöcke: nur überprüfbare Daten, keine Adjektive oder Framing
- `text`-Blöcke: dürfen Interpretation enthalten, müssen aber klar als solche erkennbar sein
- Argumente (`response`-Feld): Interpretation ist erwünscht, muss aber in den referenzierten Abschnitten verankert sein

### 5. Gegenargumente einbeziehen

Legitime Gegenpositionen stärken die Glaubwürdigkeit, wenn sie angesprochen statt ignoriert werden.

- Jedes Argument sollte die stärkste gegnerische Position anerkennen
- Muster wie „Kritiker wenden ein, dass… — allerdings zeigen die Daten…“
- Kann ein Gegenargument nicht mit Daten widerlegt werden, das ehrlich sagen
- `relatedSections` sollte auf Abschnitte verweisen, die die Belege liefern

### 6. Sprachliche Präzision

Absolutistische Sprache vermeiden, die unnötige Angriffsflächen schafft.

- **Nicht verwenden**: „beweist“, „widerlegt endgültig“, „die Medien verschweigen“, „eindeutig“
- **Besser**: „deutet darauf hin“, „die Daten zeigen“, „nach aktueller Studienlage“
- Notwendige Bedingungen nennen (z. B. „bei Nutzung erneuerbarer Energien“ bei EV-CO₂-Claims)
- Beim ersten Vorkommen volle Namen, Abkürzungen erst danach (z. B. „Statistisches Bundesamt (Destatis)“)

### 7. Argument-Claim-Passung

Das `response` muss den Claim direkt adressieren — nicht ein verwandtes, aber anderes Thema.

- `claim` und `response` als Paar lesen: Beantwortet das `response` tatsächlich die Frage?
- Kausallogik prüfen: Stützen die Belege die gezogene Schlussfolgerung?
- `relatedSections` muss Abschnitte enthalten, die das `response` wirklich untermauern
- `keywords` muss zu dem passen, was jemand bei diesem Claim sagen würde

### 8. Gesprächstauglichkeit

Ein Argument soll nicht nur als Faktencheck-Eintrag, sondern auch in der konkreten Gesprächssituation taugen. Die optionalen Felder `rhetoricalPattern` und `counterQuestions` adressieren das. Grundlage: politische Bildung (Hufer, bpb, KonterBUNT) und Misinformation-Forschung (Bruns et al., Scientific Reports 2024) — zusammengefasst im [Gesprächsleitfaden](https://fakten-stammtisch.de/leitfaden/).

**Wann beide Felder pflegen:**
- Bei jedem Argument mit korrigierendem Verdict (`false`, `mostly-false`, `misleading`, `lacks-context`, `outdated`, `partially-true`; bei `mostly-true` optional für den falschen Restanteil) — also überall, wo eine Fehlannahme korrigiert wird.
- **Ausnahme 1:** Argumente mit `verdict: "true"` brauchen keine Konter-Werkzeuge — eine zutreffende Behauptung wird bestätigt, nicht gekontert.
- **Ausnahme 2:** Argumente ohne Verdict (normative Wertedebatten, politische Forderungen) brauchen keine Konter-Werkzeuge — dort gibt es keine Falschaussage zum Korrigieren.

**Anforderungen an `response`:**
- **Truth-Sandwich-Einstieg**: Mit der korrekten Aussage beginnen, nicht mit der Wiederholung der Parole. Statt „Es stimmt nicht, dass …" lieber „Tatsächlich ist es so, dass …" oder „Die Zahlen zeigen das Gegenteil: …".
- Frame der Parole nicht unnötig wiederholen (Lakoff).

**Anforderungen an `rhetoricalPattern` (optional, 2–4 Sätze):**
- Benennt das **Denkmuster** hinter der Parole (z. B. Pauschalisierung, Lump-of-Labor-Trugschluss, Anekdotenargument, falsche Dichotomie, Korrelation-statt-Kausalität).
- Erklärt, **warum** das Muster im konkreten Fall in die Irre führt — nicht nur „die Parole ist falsch, weil X".
- Wiederholt die Parole sprachlich **nicht** — bezeichnet sie höchstens distanziert („die Parole unterstellt …", „die Aussage tut so, als ob …").
- Weglassen, wenn kein erkennbares Muster vorliegt (z. B. bei reinen Zahlen-Streits) — leeres Feld ist besser als künstliches Muster.

**Anforderungen an `counterQuestions` (optional, 2–3 Fragen):**
- **Sokratisch**: Zwingen das Gegenüber zur Präzisierung statt zu belehren.
- **Konkret**: Lösen Pauschalbegriffe auf („Welchen Job konkret?", „Wen meinst du konkret?").
- **Nicht polemisch, nicht rhetorisch fangend**: Müssen auch ehrlich beantwortbar sein, keine versteckten Anklagen.
- **Du-Form**, direkt ansprechbar in einem Gespräch.
- Maximal 3 Fragen — mehr wirkt wie ein Verhör.
- Jede Frage adressiert einen anderen Aspekt der Parole (z. B. Konkretisierung, Perspektivwechsel, Folgefrage).

**Antipattern für Gegenfragen:**
- Suggestivfragen mit eingebauter Wertung („Findest du das nicht selber lächerlich?")
- Belehrungen als Frage verkleidet („Weißt du eigentlich, dass …?")
- Mehr als 3 Fragen (Verhör-Effekt)
- Fragen, die das Gegenüber demütigen oder ins Lächerliche ziehen

### 9. Politische Neutralität

Die Seite bezieht Position für den wissenschaftlichen Kenntnisstand — nicht für ein politisches Lager. Färbung entsteht selten durch falsche Zahlen, sondern durch Verdicts auf Werturteilen, Plädoyer-Sprache und einseitige Claim-Auswahl.

**9a. Verdict-Disziplin (Empirie-Test):**
- Ein `verdict` ist nur zulässig, wenn der Claim **empirisch prüfbar** ist. Test: „Könnte eine Statistik oder Studie diese Aussage grundsätzlich widerlegen?" Wenn nein → kein Verdict.
- Die Skala reicht von `false` bis `true`: Ein empirisch schlicht **zutreffender** Stammtisch-Claim bekommt `verdict: "true"` — er wird bestätigt und eingeordnet, nicht weggelassen oder künstlich relativiert. Das stärkt die Balance (9c/9e): Berechtigte Sorgen jeder Richtung werden als solche ausgewiesen.
- Normative Claims (erkennbar an „sollte", „muss", „ist Privatsache", „ist gerecht/ungerecht", „bestraft", „hat da nichts zu suchen") bekommen **kein Verdict**. Das `response` ordnet dann die empirische Faktenbasis ein, stellt die stärksten Argumente beider Seiten dar und benennt explizit, wo der Wertkonflikt beginnt.
- Mischformen (empirische Prämisse + normative Forderung): Das Verdict **bleibt erhalten** und bezieht sich auf den empirischen Teil; im `response` die Ebenen klar trennen („Die zugrunde liegende Zahl stimmt nicht — ob man X dennoch will, ist eine Wertfrage"). `rhetoricalPattern` und `counterQuestions` bleiben gemäß Dim 8 ebenfalls bestehen.
- Verdict-Entfernung ist die **Ausnahme** für rein normative Claims ohne prüfbaren empirischen Kern — nur dann entfallen gemäß Dim 8 auch `rhetoricalPattern` und `counterQuestions`. Im Zweifel: Verdict behalten und die Ebenen im `response` trennen.

**9b. Kein Plädoyer:**
- Das `response` empfiehlt keine politische Maßnahme und erklärt keine politische Position für legitim, nötig oder überfällig („ist Teil legitimer Verteilungspolitik", „kann helfen, Arbeit zu entlasten" sind Plädoyers, keine Faktenchecks).
- Erlaubt: darstellen, was empirisch belegt ist, was Modellrechnungen zeigen und welche Annahmen sie machen. Nicht erlaubt: daraus eine Handlungsempfehlung ableiten.

**9c. Gleicher Maßstab unabhängig von der Richtung:**
- Verdicts werden nach denselben Kriterien vergeben, egal aus welcher politischen Richtung der Claim kommt. Prüffrage: „Würde ein inhaltlich gleich starker Claim der Gegenrichtung dasselbe Verdict bekommen?"
- Wahre Kerne in Claims jeder Richtung gleich großzügig anerkennen (Dim 1 symmetrisch anwenden).

**9d. Keine Lager-Sprache:**
- Kampfbegriffe und lagertypische Framings weder übernehmen noch selbst produzieren — weder „Sozialtourismus", „Klimahysterie", „Verbotspolitik" als eigene Wertung, noch „Villen der Superreichen", „Konzernlobby", „neoliberal" als eigene Wertung.
- Politische Kampfbegriffe dürfen distanziert analysiert werden (Herkunft, Bedeutung, Belegbarkeit), aber nicht als eigene Beschreibung der Wirklichkeit dienen.

**9e. Claim-Auswahl-Balance (Topic-Ebene):**
- Pro Thema prüfen: Existieren im realen Diskurs verbreitete Fehlannahmen aus **mehreren** politischen Richtungen? Dann sollten sie auch vertreten sein (z. B. neben „Bürgergeld lohnt sich mehr als Arbeit" auch „Sanktionen treffen nur Unschuldige", neben „Vermögenssteuer zerstört den Mittelstand" auch „Eine Vermögenssteuer allein saniert den Haushalt").
- Die Auswahl muss nicht 50/50 sein — sie folgt der Verbreitung der Parolen, nicht einer Quote. Aber: Fehlt eine Richtung komplett, obwohl es dort verbreitete falsche Claims gibt, ist das ein ⚠-Befund.

## Ablauf Review (Review-Modus)

1. **Laden** — `public/data/$ARGUMENTS.json` lesen, alle `arguments` und `sections` extrahieren
2. **Analysieren** — Pro Argument alle 9 Dimensionen bewerten. Pro Abschnitt Dimensionen 1–4 und 6 prüfen. Zusätzlich auf Topic-Ebene die Claim-Auswahl-Balance bewerten (Dim 9e).
3. **Einordnen** — Jedes Befund bewerten:
   - ✓ **OK**: Prüfung bestanden
   - ⚠ **VERBESSERBAR**: Nicht falsch, aber erzeugt Angriffsfläche — Verbesserung vorschlagen
   - ✗ **PROBLEM**: intellektuell unehrlich oder logisch mangelhaft — muss behoben werden
4. **Berichten** — Befunde nach Dimension gruppiert darstellen, mit konkreten Korrekturvorschlägen
5. **Umsetzen (autonom)** — Korrekturen direkt anwenden: alle ✗ PROBLEM-Befunde beheben, ⚠ VERBESSERBAR-Befunde soweit sinnvoll adressieren; danach `npm run lint && npm run build` ausführen. Jede Änderung im Bericht dokumentieren (Element, Dimension, alt → neu). Nicht auf Bestätigung warten — Ausnahme nur, wenn der Nutzer ausdrücklich um Rücksprache gebeten hat oder eine Korrektur die Kernaussage eines Arguments umkehren würde (dann per AskUserQuestion klären, falls ein Nutzer erreichbar ist, sonst konservativ korrigieren und prominent im Bericht ausweisen).

## Autor-Leitplanken (Autor-Modus)

Beim Schreiben neuer Inhalte vor dem Festhalten im JSON anwenden:

### Checkliste neues Argument

```
- [ ] Response erkennt den Wahrheitskern im Claim an (Dim 1)
- [ ] Jeder sourceRef stützt direkt den zugehörigen Claim (Dim 2)
- [ ] Zentrale Zahlen nicht allein auf interessengebundener Quelle; sonst Herkunft ausweisen (Dim 2)
- [ ] Rechnungen zeigen Annahmen und Sensitivität (Dim 3)
- [ ] Fakten und Interpretation klar getrennt (Dim 4)
- [ ] Stärkstes Gegenargument angesprochen (Dim 5)
- [ ] Keine absolutistische Sprache (Dim 6)
- [ ] Response beantwortet den Claim direkt (Dim 7)
- [ ] Response startet mit der korrekten Aussage (Truth Sandwich, Dim 8)
- [ ] rhetoricalPattern benennt das Denkmuster, ohne den Frame zu wiederholen (Dim 8, sofern Muster vorhanden)
- [ ] counterQuestions: 2–3 sokratische, konkrete, nicht polemische Fragen (Dim 8, bei Argumenten mit Verdict)
- [ ] Empirie-Test bestanden: Verdict nur bei empirisch prüfbaren Claims; zutreffende Claims bekommen `true` (Dim 9a)
- [ ] Response enthält kein politisches Plädoyer und keine Lager-Sprache (Dim 9b, 9d)
- [ ] Verdict-Maßstab unabhängig von der politischen Richtung des Claims (Dim 9c)
```

### Checkliste neuer Abschnitt

```
- [ ] Daten-Blöcke enthalten nur überprüfbare Fakten (Dim 4)
- [ ] Quellen stützen die konkreten Zahlen tatsächlich (Dim 2)
- [ ] Einschränkungen und Bedingungen genannt (Dim 3, 6)
- [ ] Keine aufgeladene Sprache in Beschriftungen oder Labels (Dim 6)
```

## Regeln

- **Autonome Abarbeitung**: Der Review-Modus läuft standardmäßig komplett durch — analysieren, berichten, Korrekturen anwenden, validieren. Der Bericht dokumentiert alle Änderungen; er ist kein Freigabe-Gate.
- **Kein Wegreden**: Berechtigte Kritik nicht entfernen — sie aufnehmen
- **Zurückhaltende Formulierungen**: Bei Unsicherheit abschwächen; nie überzeichnen
- **Position nur für die Evidenz**: Die Seite bezieht klar Stellung — aber für den wissenschaftlichen Kenntnisstand und gegen Falschaussagen, nicht für ein politisches Lager. Wo die Evidenz endet und das Werturteil beginnt, wird das ausgewiesen (Dim 9).
- **Ergänzt verify-sources**: Dieser Skill prüft Framing; `verify-sources` prüft Datenlage. Beides bei neuen Inhalten ausführen.

## Referenz

Siehe `${CLAUDE_SKILL_DIR}/reference.md` für konkrete Beispiele problematischer Muster und ihrer Korrekturen, abgeleitet aus realem Feedback.
