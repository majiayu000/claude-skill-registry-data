---
name: exposure-guidance
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Graduierte Exposition bei Angststörungen: Angsthierarchie, SUDs-Skala, Expositionsplanung und -begleitung. Nur Psychoedukation, keine Durchführung.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [exposition, angst, phobie, suds, graduiert, verhaltenstherapie]
language: de
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/exposition_begleitung.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="exposure-guidance banner">

# Expositionsbegleitung

> Angst-Hierarchie, SUDs-Skala, graduierte Exposition und Habituation verstehen: Planung und Begleitung — echte Exposition nur mit Therapeut

Siehe: [ETHICS.md](../ETHICS.md)

---

## Kontext

Exposition (Konfrontationstherapie) ist eine der wirksamsten Methoden der
Verhaltenstherapie bei Angststörungen, Phobien, Zwangsstörungen und PTBS.
Sie basiert auf den Prinzipien der Habituation und Extinktion: Wenn man sich
einer angstauslösenden Situation wiederholt aussetzt, nimmt die Angstreaktion
über die Zeit ab.

Evidenz: Expositionstherapie ist die Gold-Standard-Behandlung für spezifische
Phobien, soziale Angst, Panikstörung und Agoraphobie (NICE Guidelines, Bandelow
et al. 2014, S3-Leitlinie Angststörungen). Effektstärken gehören zu den
höchsten in der Psychotherapieforschung.

**WICHTIG:** Dieser Skill unterstützt bei der PLANUNG von Expositionsübungen und
vermittelt das Verständnis der Wirkprinzipien. Die DURCHFÜHRUNG von Exposition
muss unter Anleitung eines qualifizierten Therapeuten erfolgen.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Wirkprinzipien verstehen

### Habituation

```
HABITUATION: Gewöhnung durch wiederholte Konfrontation

Angstlevel
100 |  *
    | * *
 80 |*   *
    |     *
 60 |      *
    |       *
 40 |        *
    |         *  *
 20 |          **  * *
    |                  * * * * * *
  0 |________________________________
    Zeit (während der Exposition)

Die Angst steigt zunächst an, erreicht einen Höhepunkt
und sinkt dann OHNE Flucht oder Vermeidung von selbst ab.

Entscheidende Erfahrung: "Die Angst geht vorbei, auch wenn
ich in der Situation bleibe."
```

### Extinktion (Neues Lernen)

```
EXTINKTION: Neue Erfahrungen überschreiben alte Angst-Assoziationen

Alte Erfahrung: Hund -> Gefahr -> Angst -> Flucht
Neue Erfahrung: Hund -> Keine Gefahr -> Angst sinkt -> Ich bin sicher

Die alte Assoziation wird nicht gelöscht, sondern durch neue
Erfahrungen überlagert. Deshalb kann die Angst in bestimmten
Kontexten zurückkehren (Renewal, Reinstatement) — was NORMAL ist.
```

### Warum Vermeidung das Problem aufrechterhält

```
DER VERMEIDUNGSTEUFELSKREIS:

Angstauslösende Situation
        |
        v
Angst steigt (unangenehm)
        |
        v
Vermeidung/Flucht
        |
        v
Kurzfristige Erleichterung (Angst sinkt sofort)
        |
        v
Langfristige Verstärkung der Angst
("Die Situation IST gefährlich, gut dass ich geflohen bin")
        |
        v
Nächstes Mal: Noch mehr Angst, noch mehr Vermeidung
```

---

## 2. Die SUDs-Skala

### Subjective Units of Distress (0-100)

```
SUDS-SKALA (Subjektive Belastungsskala)

  0  Völlig entspannt, keine Angst
 10  Minimale Anspannung, kaum spürbar
 20  Leichte Unruhe, gut auszuhalten
 30  Deutlich unangenehm, aber kontrollierbar
 40  Merkliche Angst, noch handlungsfähig
 50  Mittlere Angst, anstrengend aber machbar
 60  Starke Angst, Vermeidungsimpuls deutlich
 70  Sehr starke Angst, schwer auszuhalten
 80  Intensive Angst, am Rand der Belastbarkeit
 90  Extreme Angst, Panikgefühl
100  Maximale Angst, schlimmste vorstellbare Belastung
```

### Anwendung der SUDs-Skala

**Vor der Exposition:**
- Geschätzte Angst in der geplanten Situation (Erwartungswert)

**Während der Exposition:**
- Alle 5 Minuten den aktuellen SUDs-Wert einschätzen
- Dokumentieren, wie der Verlauf ist (steigt, sinkt, schwankt)

**Nach der Exposition:**
- Höchster SUDs-Wert? Endwert? Wie schnell ging die Angst zurück?
- War es so schlimm wie erwartet?

---

## 3. Angst-Hierarchie erstellen

### Prinzip

Eine Angst-Hierarchie ordnet angstauslösende Situationen vom niedrigsten
zum höchsten Angstlevel. Die Exposition beginnt mit leichten Situationen
und steigert sich schrittweise.

### Vorgehen

```
ANGST-HIERARCHIE ERSTELLEN

Schritt 1: Alle angstauslösenden Situationen sammeln
Schritt 2: Jede Situation mit SUDs-Wert (0-100) bewerten
Schritt 3: Von niedrig nach hoch ordnen
Schritt 4: Lücken füllen (möglichst 10er-Schritte)
```

### Beispiel: Angst vor Hunden

```
ANGST-HIERARCHIE: Hundephobie

SUDs | Situation
-----|--------------------------------------------------
 10  | Bild von einem Hund anschauen
 15  | Video von spielenden Hunden anschauen
 25  | Über eigene Erfahrungen mit Hunden sprechen
 30  | Einen kleinen Hund aus 10 Metern Entfernung beobachten
 40  | Einen kleinen Hund aus 5 Metern Entfernung beobachten
 50  | Neben einem angeleinten kleinen Hund stehen (2 Meter)
 55  | Einen kleinen angeleigten Hund berühren (Besitzer hält)
 60  | Einen mittelgroßen Hund aus 5 Metern beobachten
 65  | Neben einem angeleinten mittelgroßen Hund sitzen
 70  | Einen mittelgroßen Hund streicheln
 75  | An einem freilaufenden Hund vorbeigehen (Park)
 80  | Allein in einem Raum mit einem ruhigen Hund sein
 85  | Einen großen Hund streicheln
 90  | In einem Park mit mehreren freilaufenden Hunden sein
 95  | Einen Hund füttern
100  | Einen fremden Hund auf sich zulaufen lassen
```

### Beispiel: Soziale Angst

```
ANGST-HIERARCHIE: Soziale Angst

SUDs | Situation
-----|--------------------------------------------------
 15  | Einen Fremden nach der Uhrzeit fragen
 20  | Im Supermarkt an der Kasse ein kurzes Gespräch führen
 30  | In einer kleinen Gruppe eine Frage stellen
 40  | Einen Bekannten anrufen
 45  | Blickkontakt halten während eines Gesprächs
 55  | Allein in ein Cafe gehen und dort essen
 60  | Einer Gruppe von 5 Personen etwas erzählen
 70  | Bei einer Feier auf einen Fremden zugehen
 75  | Im Restaurant Essen zurückschicken
 80  | Vor 10 Personen eine kurze Präsentation halten
 85  | In einer Diskussion eine abweichende Meinung vertreten
 90  | Vor 30 Personen einen Vortrag halten
 95  | Spontan eine Rede halten (Toast, Tischrede)
```

### Vorlage zum Ausfüllen

```
MEINE ANGST-HIERARCHIE

Angstthema: [...]

SUDs | Situation
-----|--------------------------------------------------
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
```

---

## 4. Arten der Exposition

### Graduierte Exposition (In Vivo)

**Prinzip:** Schrittweise Konfrontation mit realen Situationen,
beginnend bei niedrigen SUDs-Werten.

```
ABLAUF GRADUIERTER EXPOSITION:

1. Angst-Hierarchie erstellen (siehe oben)
2. Mit der leichtesten Situation beginnen (SUDs 20-30)
3. In der Situation BLEIBEN, bis die Angst nachlässt
   (mindestens 50% Reduktion oder SUDs < 25)
4. Übung mehrfach wiederholen, bis die Situation
   routinemäßig bewältigbar ist
5. Nächste Stufe der Hierarchie angehen
6. Weiter bis zur Spitze
```

### Flooding (Reizüberflutung)

**Prinzip:** Direkte Konfrontation mit stark angstauslösenden Situationen
(hohe SUDs-Werte) für längere Zeit.

```
FLOODING:

- Sehr wirksam, aber belastender als graduierte Exposition
- Nur unter therapeutischer Anleitung
- Voraussetzung: Gute therapeutische Beziehung und Vorbereitung
- Nicht bei unkontrollierbaren Panikattacken oder Dissoziation
- NICHT durch einen KI-Assistenten anleiten — nur erklären
```

### Exposition in sensu (in der Vorstellung)

**Prinzip:** Angstauslösende Situationen in der Vorstellung durchleben.

```
EXPOSITION IN SENSU:

- Hilfreich als Vorbereitung auf reale Exposition
- Bei Situationen, die nicht leicht reproduzierbar sind
- Bei starker Vermeidung als Einstieg
- Ein KI-Assistent kann bei der Planung helfen, aber die Durchführung
  sollte therapeutisch begleitet sein
```

### Interozeptive Exposition

**Prinzip:** Gezieltes Hervorrufen von körperlichen Angstsymptomen
(z.B. Herzrasen durch Bewegung, Schwindel durch Drehen).

```
INTEROZEPTIVE EXPOSITION (bei Panikattacken):

- Durch Körperübungen: Hyperventilation, Strohhalm-Atmen,
  Kopfdrehen, Treppensteigen
- Ziel: Lernen, dass körperliche Symptome ungefährlich sind
- NUR unter therapeutischer Anleitung
```

---

## 5. Begleitete Expositionsplanung

### Vorbereitungsprotokoll

```
EXPOSITIONS-PLANUNGSPROTOKOLL

Datum: [...]
Therapeut informiert: [ ] Ja  [ ] Nein (PFLICHT!)

Angstthema: [...]
Gewährte Situation: [...]
Erwarteter SUDs-Wert: [...]
Stufe in der Hierarchie: [...]

Was genau werde ich tun: [...]
Wo: [...]
Wann: [...]
Wie lange: [...]
Allein oder begleitet: [...]

Meine größte Befürchtung: [...]
Was realistisch passieren wird: [...]

Notfallplan (falls SUDs > 90 oder Dissoziation):
1. Grounding (5-4-3-2-1)
2. Atemübung (Box-Breathing)
3. [Vertrauensperson anrufen]: Tel. [...]
4. Situation ordentlich verlassen (kein panisches Flüchten)
```

### Nachbereitungsprotokoll

```
EXPOSITIONS-NACHBEREITUNG

Datum: [...]
Situation: [...]

SUDs vorher (Erwartung): [...]
SUDs höchster Wert während: [...]
SUDs am Ende: [...]

Wie lange in der Situation geblieben: [...]
Habituation eingetreten: [ ] Ja  [ ] Teilweise  [ ] Nein

Was habe ich gelernt: [...]
War es so schlimm wie befürchtet: [ ] Schlimmer  [ ] Wie erwartet  [ ] Weniger schlimm

Was möchte ich beim nächsten Mal anders machen: [...]
Nächste Stufe: [...]
```

---

## 6. Sicherheitshinweise und Abbruchkriterien

### Voraussetzungen für Exposition

```
CHECKLISTE VOR EXPOSITIONSBEGINN:

[ ] Qualifizierter Therapeut ist einbezogen
[ ] Ausreichende Stabilisierung vorhanden
[ ] Angst-Hierarchie ist erstellt und besprochen
[ ] Notfallplan ist vorbereitet
[ ] Person versteht das Wirkprinzip (Habituation)
[ ] Keine akute Suizidalität
[ ] Keine unkontrollierte psychotische Symptomatik
[ ] Keine schwere dissoziative Störung (ohne therapeutische Begleitung)
[ ] Keine akute Substanzintoxikation
[ ] Person hat freiwillig zugestimmt (keine Zwangsexposition!)
```

### Abbruchkriterien

```
EXPOSITION ABBRECHEN, WENN:

- Dissoziation auftritt (Person "ist weg", reagiert nicht)
- Panikattacke mit Kontrollverlust
- Person will ausdrücklich abbrechen (Autonomie respektieren!)
- Körperliche Symptome: Brustschmerz, Atemnot, Ohnmacht
- Suizidgedanken während der Exposition
- Die Situation objektiv unsicher wird

BEI ABBRUCH:
1. Grounding und Stabilisierung (5-4-3-2-1, Atemübung)
2. Sicherstellen, dass die Person orientiert und stabil ist
3. Erfahrung besprechen (was ist passiert, was wurde gelernt)
4. Keinen Vorwurf machen ("Du hättest bleiben sollen")
5. Nächsten Schritt mit Therapeut planen
```

### Sicherheitsverhaltensweisen erkennen

```
SICHERHEITSVERHALTEN (Safety Behaviors):

Sicherheitsverhalten sind Strategien, die die Angst kurzfristig senken,
aber das Lernen verhindern:

| Sicherheitsverhalten | Problem |
|---------------------|---------|
| Ablenkung während Exposition | Verhindert volle Konfrontation |
| Handy griffbereit halten | "Ich habe es nur geschafft, weil..." |
| Begleitperson dabei | Lernt nicht, es allein zu schaffen |
| Beruhigungstablette vorher | Erfolg wird Tablette zugeschrieben |
| Nur kurz in Situation bleiben | Habituation hat keine Zeit |
| Fluchtweg im Kopf planen | Aufmerksamkeit nicht bei Erfahrung |

Ziel: Sicherheitsverhalten schrittweise reduzieren,
damit die volle Lernerfahrung möglich wird.
Aber: Nicht zu früh wegnehmen — in Absprache mit Therapeut.
```

---

## Ethik und Grenzen

**Ein KI-Assistent darf:**
- Expositionsprinzipien erklären (Psychoedukation)
- Angst-Hierarchie gemeinsam erstellen
- SUDs-Skala erklären und nutzen
- Expositionsplanung unterstützen (Protokolle ausfüllen)
- Nachbereitung dokumentieren
- Sicherheitshinweise geben
- Motivieren und normalisieren ("Angst bei Exposition ist erwünscht und normal")

**Ein KI-Assistent darf NICHT:**
- Exposition eigenständig durchführen oder anleiten
- Flooding anleiten (NUR Therapeut)
- Interozeptive Exposition anleiten (NUR Therapeut)
- Prolonged Exposure bei PTBS durchführen
- Exposition bei schwerer Dissoziation begleiten
- Zur Exposition drängen ("Du musst dich dem stellen")
- Ergebnisse garantieren
- Diagnosen stellen oder Therapieplan erstellen
- Medikamentenbezogene Empfehlungen geben

**BESONDERS STRENGE GRENZE:** Ein KI-Assistent plant und erklärt. Die echte Exposition
findet unter Anleitung eines qualifizierten Therapeuten statt. Bei jeder
Anfrage zur Durchführung: Verweis an Fachperson. Exposition ohne
professionelle Begleitung kann re-traumatisieren oder die Angst verstärken.

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
*Quellen: Foa & Kozak (1986), Craske et al. (2014), Bandelow et al. (2014), S3-Leitlinie Angststörungen (2014) — Keine professionelle Therapie*
