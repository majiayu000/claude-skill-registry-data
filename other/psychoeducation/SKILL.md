---
name: psychoeducation
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Psychoedukation zu Depression, Angststörungen, PTBS, bipolarer Störung, Schizophrenie, ADHS und Borderline. Wissensvermittlung ohne Diagnose.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [psychoedukation, depression, angst, ptbs, adhs, borderline, wissensvermittlung]
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
  origin_path: "system/skills/therapie/psychoedukation.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---
<img src="banner.png" width="100%" alt="psychoeducation banner">

# Psychoedukation

> Wissensvermittlung ueber psychische Erkrankungen, Symptome und Behandlungsansaetze

Siehe: [ETHICS.md](../ETHICS.md)

---

## Kontext

Psychoedukation bezeichnet die systematische Wissensvermittlung ueber psychische
Erkrankungen an Betroffene und Angehoerige. Ziel ist es, Verstaendnis fuer die
Erkrankung zu foerdern, Selbstmanagement zu staerken und Stigmatisierung abzubauen.

Evidenz: Psychoedukation ist als Baustein in allen Therapierichtlinien empfohlen
(DGPPN, NICE, APA) und reduziert nachweislich Rueckfallraten (Xia et al. 2011,
Cochrane Review).

**Hinweis:** Dies ist Unterstuetzung, kein Ersatz fuer professionelle Therapie.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Was ist Psychoedukation?

### Definition
Strukturierte Vermittlung von Wissen ueber psychische Erkrankungen mit dem Ziel,
Betroffene zu "Experten ihrer eigenen Erkrankung" zu machen.

### Ziele
- Krankheitsverstaendnis: Was habe ich? Warum?
- Fruehwarnsignale erkennen
- Behandlungsmoeglichkeiten kennen
- Selbstwirksamkeit foerdern
- Stigma reduzieren
- Adherence (Therapietreue) verbessern

### Evidenz
- Rueckfallpraevention bei Schizophrenie: NNT = 9 (Xia et al. 2011)
- Depression: Verbesserung der Therapietreue um 30-50% (Donker et al. 2009)
- Angststoerungen: Psychoedukation allein bereits mild wirksam (Donker et al. 2009)

---

## 2. Krankheitsbilder im Ueberblick

### 2.1 Depression (Major Depression)

**Was ist das?** Anhaltende Niedergeschlagenheit, Interessenverlust und Antriebslosigkeit
ueber mindestens 2 Wochen, die ueber normale Traurigkeit hinausgehen.

**Kernsymptome (ICD-11):**
- Depressive Stimmung (fast den ganzen Tag, fast jeden Tag)
- Interessenverlust / Freudlosigkeit (Anhedonie)
- Verminderter Antrieb / erhoehte Ermuedbarkeit

**Zusatzsymptome:** Konzentrationsprobleme, Schuldgefuehle, Schlafprobleme,
Appetitveraenderung, Suizidgedanken, psychomotorische Hemmung/Agitation

**Behandlung:** KVT, medikamentoes (SSRI, SNRI), Bewegung, Lichttherapie (saisonal)
**Selbsthilfe:** Tagesstruktur, Aktivitaetsaufbau, soziale Kontakte, Bewegung, Schlafhygiene

### 2.2 Angststoerungen

**Was ist das?** Uebermaessige, unkontrollierbare Angst oder Furcht, die das
alltaegliche Leben beeintraechtigt.

**Formen:**
- Generalisierte Angststoerung (GAS): Chronisches Sich-Sorgen
- Panikstoorung: Ploetzliche Angstanfaelle mit koerperlichen Symptomen
- Soziale Phobie: Angst vor Bewertung in sozialen Situationen
- Spezifische Phobien: Angst vor konkreten Objekten/Situationen
- Agoraphobie: Angst vor Orten/Situationen ohne Fluchtmoeglichkeit

**Behandlung:** KVT (Exposition, kognitive Umstrukturierung), SSRI, Entspannung
**Selbsthilfe:** Angst-Tagebuch, Atemuebungen, schrittweise Konfrontation

### 2.3 Posttraumatische Belastungsstoerung (PTBS)

**Was ist das?** Anhaltende Reaktion auf ein traumatisches Erlebnis (Bedrohung,
Gewalt, Unfall, Katastrophe) mit Wiedererleben, Vermeidung und Uebererregung.

**Kernsymptome:**
- Intrusionen (Flashbacks, Alptraeume)
- Vermeidungsverhalten
- Emotionale Taubheit oder Uebererregung
- Negative Veraenderungen von Gedanken und Stimmung

**Behandlung:** Traumafokussierte KVT, EMDR, Narrative Expositionstherapie
**Selbsthilfe:** Stabilisierungstechniken, Grounding, sichere Orte — KEINE Selbstexposition

### 2.4 Bipolare Stoerung

**Was ist das?** Wechsel zwischen depressiven und (hypo-)manischen Episoden.
Chronische Erkrankung mit hohem Rueckfallrisiko.

**Manische Episode:** Gehobene Stimmung, vermindertes Schlafbeduerfnis,
Groessenideen, gesteigerte Aktivitaet, Risikobereitschaft, Rededrang

**Behandlung:** Stimmungsstabilisierer (Lithium, Valproat), atypische Antipsychotika
**Selbsthilfe:** Stimmungstagebuch, regelmaessiger Schlafrhythmus, Fruehwarnsignale kennen

### 2.5 Schizophrenie

**Was ist das?** Schwere psychische Erkrankung mit Stoerungen des Denkens,
der Wahrnehmung und des Erlebens. Betrifft ca. 1% der Bevoelkerung.

**Positivsymptome:** Halluzinationen, Wahn, desorganisiertes Denken
**Negativsymptome:** Antriebslosigkeit, sozialer Rueckzug, Affektverflachung
**Kognitive Symptome:** Aufmerksamkeit, Gedaechtnis, exekutive Funktionen

**Behandlung:** Antipsychotika, KVT fuer Psychosen, Soziotherapie, Familieninterventionen
**Selbsthilfe:** Medikamenten-Adherence, Stressvermeidung, Fruehwarnsignale, Tagesstruktur

### 2.6 ADHS (Aufmerksamkeitsdefizit-Hyperaktivitaetsstoerung)

**Was ist das?** Neurobiologische Entwicklungsstoerung mit Unaufmerksamkeit,
Impulsivitaet und/oder Hyperaktivitaet. Beginnt in der Kindheit, persistiert
bei ca. 50% ins Erwachsenenalter.

**Behandlung:** Multimodal (Medikation, Psychoedukation, Coaching, KVT)
**Selbsthilfe:** Externe Strukturhilfen, Timer, Listen, Routinen, Bewegung

### 2.7 Borderline-Persoenlichkeitsstoerung (BPS)

**Was ist das?** Muster von Instabilitaet in Beziehungen, Selbstbild und
Affekten mit ausgepraegte Impulsivitaet. Hohe emotionale Verletzlichkeit.

**Kernsymptome:** Instabile Beziehungen, Identitaetsstoerung, Impulsivitaet,
affektive Instabilitaet, Selbstverletzung, chronische Leere, Dissoziationen

**Behandlung:** DBT (Linehan), Schematherapie, MBT, TFP
**Selbsthilfe:** Skills-Koffer, Notfallplan, Stresstoleranz-Skills

---

## 3. Stigma-Reduktion

### Haeufige Mythen und Fakten

| Mythos | Fakt |
|--------|------|
| "Psychisch Kranke sind gefaehrlich" | Betroffene sind haeufiger Opfer als Taeter |
| "Depression ist Willensschwaeche" | Depression ist eine neurobiologische Erkrankung |
| "Therapie ist nur Reden" | Evidenzbasierte Therapie veraendert nachweislich Hirnstrukturen |
| "Das waechst sich aus" | Viele Erkrankungen chronifizieren ohne Behandlung |
| "Medikamente machen abhaengig" | Antidepressiva erzeugen keine Abhaengigkeit |

### Sprache und Stigma
- "An Schizophrenie erkrankt" statt "schizophren"
- "Mensch mit Depression" statt "Depressiver"
- Person-first Language reduziert Stigma nachweislich (Granello & Gibbs, 2016)

---

## 4. Angehoerigen-Perspektive

- Psychische Erkrankungen betreffen das gesamte soziale Umfeld
- Angehoerige brauchen eigene Psychoedukation und Entlastung
- Expressed Emotion (EE): Hohe Kritik/Ueberinvolvement erhoehen Rueckfallrisiko
- Empfehlung: Angehoerigengruppen, Familien-Psychoedukation

---

## Ethik und Grenzen

**Ein KI-Assistent kann:**
- Sachliche Informationen zu Krankheitsbildern geben
- Haeufige Fragen beantworten
- Auf weiterfuehrende Ressourcen verweisen

**Ein KI-Assistent kann NICHT:**
- Diagnosen stellen oder bestaetigen
- Individuelle Behandlungsempfehlungen geben
- Professionelle Psychoedukation in Gruppenformat ersetzen

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
*Quellen: ICD-11, DGPPN-Leitlinien, Xia et al. (2011), Donker et al. (2009), Cochrane Reviews — Keine professionelle Therapie*
