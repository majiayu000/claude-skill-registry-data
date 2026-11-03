---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: >
  Komponiert video-synchronisierte Hintergrundmusik aus einem Storyline-JSON
  per lokaler Waveform-Synthese (numpy + ffmpeg). Stile: Chiptune, Ambient,
  Electronic. Deterministisch, offline, kein Cloud-Dienst.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: de
status: stable
visibility: public
dependencies:
  tools: [ffmpeg]
  services: []
  protocols: []
  python: [numpy]
provenance:
  origin: local-reconstruction
  origin_license: MIT
  notes: >
    Verfahren rekonstruiert aus einem video-synchronisierten Score, komponiert
    für ein 179,5-s-Erklärvideo (5 Musikabschnitte aus 7 Story-Akten
    gemappt). Kanonische Engine: ai-media-editor-Repo, tools/compose_music.py
    (github.com/ellmos-ai/ai-media-editor). Eine eigenständige Kopie liegt
    hier für Offline-Nutzung bei.
---

<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — Storyline → Score

Komponiert einen Hintergrund-Score, der dem dramaturgischen Bogen eines
Videos folgt, vollständig lokal: numpy-Waveform-Synthese (Oszillatoren,
ADSR, Layering, Delay-Reverb) + ffmpeg für die MP3-Kodierung. Keine Samples,
keine MIDI-Hardware, keine Cloud-API.

## Wann nutzen

- Ein Video/Podcast braucht Hintergrundmusik, die Story-Beats exakt auf
  Zeitstempeln trifft (Opening, Spannungstal, Drive-Abschnitt, Klimax,
  Outro).
- Ein deterministischer, neu-renderbarer Score wird gebraucht (gleicher
  Seed → gleiches Audio).
- Chiptune-, Ambient- oder Electronic-Stile sind akzeptabel.

## Wann NICHT nutzen (ehrliche Genre-Grenzen)

Waveform-Synthese kann **Chiptune-, Ambient- und Electronic**-Hintergrundbetten
liefern. Sie kann mit ihrem eingebauten Synth **kein Pop, Rock, Klassik oder
Orchester-Filmmusik** liefern — aber das Arrangement ist Backend-neutral:
siehe "Jenseits der Waveform-Synthese" unten, um dieselbe Komposition über
SoundFonts, Orchester-Bibliotheken oder externe Generierung zu rendern.

## Das Verfahren: Storyline → Score

So rekonstruiert wie im Referenz-Score (179,5 s, c-Moll):

1. **Story-Akte auf Musikabschnitte mappen.** Akte, die einen emotionalen
   Zustand teilen, verschmelzen zu einem Abschnitt (Referenz: 7 Akte →
   5 Abschnitte; Akte 1–3 bildeten ein einziges 62-s-ruhiges Opening). Jeder
   Abschnitt bekommt exaktes `start`/`end` in Sekunden.
2. **Emotion + Intensität je Abschnitt zuweisen.**
   - *Emotion* wählt die Akkordfolge (Skalenstufen, Moll-Beispiel):
     `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III ·
     `driving` i–VII–VI–V · `epic` iv–V–VI–i (V ist harmonisch-Moll-Dur).
   - *Intensität* (0–1) treibt Tempo-Gefühl (BPM), Layer-Anzahl und
     Lautstärke-Rampe. Layer treten bei Schwellen bei: Pads immer → spärliche
     Glocken (<0,3) → Arp (≥0,25) → Bass (≥0,4) → Lead (≥0,45) →
     Drums (≥0,5) → Drive-Extras (≥0,65) → Pad-Oktavverdopplung (≥0,85).
3. **Spezielle Events auf der Zeitachse platzieren.**
   - `damp`: Gauß'sche Lautstärke-Duck — `1 - depth · exp(-((t-T)²)/(2σ²))`.
     Referenz: depth 0,5, σ 1 s bei T=84 s, auf dem gesprochenen Beat
     "Two databases. Same cluster." (~1:24).
   - `climax`: Zeitfenster, das volle Layering, Spitzenlautstärke,
     oktavverdoppelte Pads erzwingt (Referenz: 154–170 s = 2:34–2:50, beim
     2D→3D-Morph).
   - `outro`: ab seinem Start fallen Drums/Bass/Lead weg und Glocken faden
     auf 20 % (Referenz: 170–179,5 s, Abspannkarte).
4. **Verkleben.** Raised-Cosine-Glättung an Abschnittsgrenzen (~2,5 s),
   globaler Fade-in/-out, Feedback-Delay-Reverb (100 ms, Decay 0,25),
   Tanh-Drive + Peak-Normalisierung auf ein Hintergrundniveau (gemessener
   Referenz-Master: Mittel ≈ −22 dB, Max ≈ −1,6 dB).
5. **Hinter dem Voiceover bleiben.** Als "background" markierte Abschnitte
   deckeln ihre Lautstärke-Rampe; der Score ist ein Bett, kein Lead.

## Nutzung

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```

Ausgabe: `score.wav` (Stereo 16-bit 44,1 kHz), `score.mp3` (192k, braucht
ffmpeg im PATH; sonst mit Warnung übersprungen), `score.notes.json` (das
Arrangement-/Noten-Log: jede platzierte Note mit Zeit, Layer, MIDI-Pitch,
Dauer, Velocity) und `score.mid` — eine echte **Standard-MIDI-Datei** (Typ 1:
Tempo-Spur mit einem Tempo-Event je Abschnitt, Noten-Spur mit
GM-Programm-Hinweisen je Stil, Drums auf GM-Kanal 10). Abhängigkeitsfrei
geschrieben; kein pretty_midi/mido nötig.

Determinismus: gleiche Storyline + gleicher `seed` → byte-identisches WAV.

## Storyline-JSON-Referenz

```json
{
  "title": "my-score",
  "duration": 179.5,
  "bpm": 100,
  "key": "C",
  "mode": "minor",
  "style": "chiptune",
  "seed": 42,
  "fade_in": 3.0,
  "fade_out": 5.0,
  "crossfade": 2.5,
  "peak": 0.85,
  "drive": 2.0,
  "reverb": {"delay_ms": 100, "decay": 0.25},
  "sections": [
    {"start": 0.0, "end": 62.0, "emotion": "calm", "intensity": 0.18, "bpm": 60,
     "comment": "optional note"},
    {"start": 62.0, "end": 88.0, "emotion": "tense", "intensity": 0.4, "bpm": 72}
  ],
  "events": [
    {"type": "damp", "time": 84.0, "depth": 0.5, "width": 1.0},
    {"type": "climax", "start": 154.0, "end": 170.0},
    {"type": "outro", "start": 170.0}
  ]
}
```

- `duration` (Pflicht, Sekunden), `sections` (Pflicht, ≥1, sortiert,
  überlappungsfrei, innerhalb der Dauer).
- Abschnitts-Felder: `start`, `end` (Pflicht); `emotion` ∈ calm | tense |
  alive | driving | epic | outro; `intensity` 0–1 (Standard je Emotion);
  `bpm` (Standard: globales `bpm`); `melody` (optionale MIDI-Liste, zyklisch;
  sonst wird ein geseedeter Random Walk über Skalentöne erzeugt).
- `key`: Notenname (C, C#, Db, …), `mode`: minor | major.
- `style`: chiptune | ambient | electronic (siehe unten).
- Event `damp`: `time` (s), `depth` 0–1, `width` = σ in Sekunden.
- Standardwerte für Fades/Crossfade/Peak/Drive/Reverb wie oben gezeigt;
  alle optional.

Vollständiges durchgerechnetes Beispiel (die Rekonstruktion des
Referenzvideos): [`example-storyline.json`](example-storyline.json) —
rendert einen 179,5-s-Score, der dem Master-Level des Originals entspricht
(Mittel ≈ −22 dB, Max ≈ −1,6 dB).

## Stil-Presets

| Stil | Lead | Bass/Arp | Drums | Charakter |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | triangle bass, schnelle square arps | Noise-basierter Kick/Hat/Snare | Retro-Konsole, arpeggio-getrieben (der Referenzstil) |
| `ambient` | weiches triangle/sine | langsame Arps, Long-Attack-Pads | erst ab Intensität ≥ 0,75 | spärlich, glocken-fokussiert, breites Reverb-Gefühl |
| `electronic` | sawtooth + detune + sub | druckvoller Bass, saw Arps | volles Kit | treibendes EDM-nahes Bett |

## Jenseits der Waveform-Synthese: bessere Sound-Backends

Die genannte Genre-Decke ist das **Sound-Backend, nicht die Komposition**.
Das Storyline→Score-Verfahren erzeugt ein Backend-neutrales Arrangement;
der mitgelieferte numpy-Synth ist nur der kostenlose Offline-Standard-Renderer.
Jeder Lauf schreibt zusätzlich eine Standard-MIDI-Datei (`<out>.mid`) —
über bessere Instrumente rendern:

- **Pfad A — SoundFont (empfohlen: lokal, kostenlos, keine Cloud).**
  FluidSynth installieren (fluidsynth.org, Windows: `winget install FluidSynth`)
  plus ein kostenloses GM-SoundFont (GeneralUser GS von S. Christian Collins,
  oder MuseScore_General.sf2). Dann:
  `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → MP3
  über ffmpeg. Das schaltet Pop-/Rock-Band-Sounds, Klavier, einfache
  Streicher frei.
- **Pfad B — Orchester/Film.** Kostenlose Orchester-Bibliotheken: VSCO 2
  Community Edition, Soni Musicae, Salamander Grand Piano. Bessere
  Streicher/Blechbläser, epischer. Ehrlicher Hinweis: Artikulation und
  Humanisierung (Velocity-Variation, Legato, Dynamik-Kurven) zählen mehr
  als der Sample-Satz — und echte Filmscore-Epik braucht zusätzlich
  Arrangement-Reife; ein Backend allein reicht nicht.
- **Pfad C — externe KI-Generierung (Suno u. a.).** Möglich, wirft aber
  Datenschutz-/Rechtefragen auf — nur nach ausdrücklicher Nutzerfreigabe,
  niemals als Standard.

Geplant, aber **noch nicht implementiert**: eine `humanize`-Option in der
Engine (Velocity-/Timing-Jitter je Note), damit sample-basiertes Rendern
nicht mechanisch klingt (als TODO im Engine-Docstring markiert).

## Grenzen

- Englische und deutsche Storyline-Kommentare sind unproblematisch;
  Keys/Values sind fest englisch.
- Sehr kurze Dauern (< ~10 s) funktionieren, stauchen aber die Dramaturgie
  (Fades und Crossfades werden automatisch auf 20 % der Dauer / 50 % des
  kürzesten Abschnitts gedeckelt).
- Das Noten-Log (`*.notes.json`) ist der analysefreundliche Datensatz; die
  `*.mid`-Datei ist das Austauschformat für DAWs/SoundFont-Renderer
  (GM-Programmnummern sind grobe Stil-Hinweise — nach Geschmack remappen).
