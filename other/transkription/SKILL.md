---
name: transkription
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "Transcribes audio/video files to text. Uses Whisper (openai-whisper) or Vosk (offline) as optional backend — both are detected via presence check. Without backend: placeholder mode with dummy output (dry-run)."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [transkription, audio, speech-to-text, whisper, vosk, offline]
language: de
status: stable
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': [{'name': 'openai-whisper', 'optional': True, 'install': 'pip install openai-whisper', 'purpose': 'STT backend option 1 (cloud/local model)'}, {'name': 'vosk', 'optional': True, 'install': 'pip install vosk', 'purpose': 'STT backend option 2 (fully offline)'}]}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein direkter BACH-Origin vorhanden (transkriptions-service existiert nicht als Datei in BACH/system). Skill neu konzipiert. voice_stt.py aus BACH/hub/_services/voice/ hat das Backend-Muster inspiriert (optionale Imports mit Verfügbarkeits-Flags), wurde aber nicht direkt portiert.\n'}
---
<img src="banner.png" width="100%" alt="transkription banner">

## Zweck

Audio-/Video-Dateien in Text umwandeln — lokal, ohne Cloud-Pflicht. Der Skill
erkennt selbst, ob Whisper oder Vosk installiert ist, und wählt das beste
verfügbare Backend. Ohne Backend läuft er im Dry-Run-Modus und gibt einen
Platzhaltertext zurück, sodass der Workflow immer funktioniert.

Transkripte werden lokal in `transkription/store.db` gespeichert und können
abgefragt werden.

---

## Trigger

| Phrase | Aktion |
|---|---|
| „Transkribiere diese Audio" | Audio-Datei transkribieren |
| „Transkribiere [Datei]" | Benannte Datei transkribieren |
| „Zeig meine Transkripte" | Letzte Transkripte auflisten |
| „Suche Transkript [Begriff]" | Volltextsuche in Transkripten |
| „Exportiere Transkript [ID]" | Transkript als TXT exportieren |

---

## Workflow

1. **Backend-Check**: Prüfen ob `whisper` oder `vosk` importierbar ist.
2. **Datei-Prüfung**: Eingabedatei muss existieren (Audio: wav, mp3, m4a, ogg, flac; Video: mp4, mkv, webm — Extraktion via ffmpeg).
3. **Transkription**: Backend aufrufen und Rohtext erhalten.
4. **Speichern**: Ergebnis mit Metadaten (Datei, Dauer, Sprache, Backend, Zeitstempel) in `store.db`.
5. **Ausgabe**: Text zurückgeben; optional als `.txt` exportieren.

---

## CLI-Einstieg

```bash
# Datei transkribieren
python transkription_core.py transcribe audio.wav

# Mit expliziter Sprache
python transkription_core.py transcribe audio.mp3 --lang de

# Dry-Run (kein Backend nötig)
python transkription_core.py transcribe audio.wav --dry-run

# Transkripte auflisten
python transkription_core.py list [--limit 20]

# Volltextsuche
python transkription_core.py search "Begriff"

# Exportieren
python transkription_core.py export <id> [--out datei.txt]

# Backend-Check
python transkription_core.py check

# Alternativer Store-Pfad (z.B. für Tests)
python transkription_core.py --store /tmp/test.db transcribe audio.wav --dry-run
```

---

## Store

| Eigenschaft | Wert |
|---|---|
| Typ | SQLite |
| Pfad (Standard) | `skills/assist/transkription/store.db` |
| Override | `--store <pfad>` oder Env `TRANSKRIPTION_STORE` |
| Tabellen | `transcripts` |

### Schema `transcripts`

```sql
CREATE TABLE IF NOT EXISTS transcripts (
    id          TEXT PRIMARY KEY,  -- UUID (kurz: 8 Hex)
    file_path   TEXT NOT NULL,     -- Originalpfad der Audiodatei
    file_name   TEXT NOT NULL,     -- Dateiname (ohne Pfad, für Anzeige)
    text        TEXT NOT NULL,     -- Transkribierter Text
    language    TEXT,              -- Sprache (z.B. "de", "en")
    backend     TEXT,              -- "whisper" | "vosk" | "dry-run"
    duration_s  REAL,              -- Dauer in Sekunden (wenn bekannt)
    created_at  TEXT NOT NULL,     -- ISO-8601 Timestamp
    tags        TEXT               -- Komma-getrennte Tags (optional)
);
```

---

## Haltung

- Ohne installiertes Backend funktioniert der Skill im Dry-Run-Modus (Demo-Text).
- Whisper wird gegenüber Vosk bevorzugt (bessere Deutsch-Qualität).
- Die Wahl zwischen Whisper und Vosk kann per `assist/prefs.json` (`transkription_backend: "whisper"|"vosk"|"auto"`) festgelegt werden.
- ffmpeg für Video-Extraktion wird separat benötigt und ist nicht im Skill enthalten.

---

## Datenschutz

- **Alle Transkripte bleiben lokal** — keine Cloud-Übertragung ohne Whisper-Online-Modus.
- Whisper kann lokal (tiny/base/medium-Modell) oder über OpenAI-API genutzt werden.
  Standardmäßig wird das lokale Modell verwendet.
- `store.db` enthält potenziell sensible Gesprächsinhalte — **nicht in Git committen**.
- Empfehlung: `.gitignore` um `store.db` ergänzen.

---

## Verwandte Ressourcen

- BACH `hub/_services/voice/voice_stt.py` — Backend-Muster (Inspiration, read-only)
- Skill `utilities/yt-transcriber` — YouTube-Transkription (separater Skill, kein Duplikat: YT-spezifisch)
- `tools/module-installer/module_installer.py` — Registry enthält whisper + vosk

---

## Changelog

| Version | Datum | Änderung |
|---|---|---|
| 0.1.0 | 2026-06-22 | Erstanlage — eigener SQLite-Store, Whisper/Vosk-Presence-Check |
