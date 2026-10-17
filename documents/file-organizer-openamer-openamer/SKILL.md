---
name: file-organizer
description: 'Clean Desktop/DL: temp, MD5 dedupe, type-sort, undo.'
domain:
  - system
  - file-management
  - cleanup
trigger: |
  - User asks to clean Desktop/Downloads/Documents
  - User asks about duplicate files, large files, temp files
  - User asks to organize files by type
workflow: |
  1. Run `python scripts/file-organizer.py --scan` for overview
  2. Run `python scripts/file-organizer.py --dry-run --clean` to preview temp deletions
  3. Run `python scripts/file-organizer.py --clean` to delete temp files
  4. Run `python scripts/file-organizer.py --dry-run --dedupe` to preview dedup
  5. Run `python scripts/file-organizer.py --dedupe` to remove duplicates
  6. Run `python scripts/file-organizer.py --dry-run --organize` to preview organization
  7. Run `python scripts/file-organizer.py --organize` to organize by type
  8. Run `python scripts/file-organizer.py --undo` to revert last organize action
  9. Run `python scripts/file-organizer.py --report` to generate HTML report
---

# File Organizer

Automatisierte Verwaltung von **Desktop**, **Downloads** und **Documents**.

## Befehle

| Befehl | Beschreibung |
|--------|-------------|
| `--scan` | Scan + Zusammenfassung anzeigen |
| `--dry-run --clean` | Temp-Löschungen vorschauen |
| `--clean` | Temporäre Dateien (*.tmp, *.log, *.dmp, ...) löschen |
| `--dry-run --dedupe` | Duplikat-Löschungen vorschauen |
| `--dedupe` | Duplikate (MD5) entfernen, eine Kopie behalten |
| `--dry-run --organize` | Typ-Organisation vorschauen |
| `--organize` | Dateien in Kategorie-Ordner sortieren |
| `--undo` | Letzte `--organize`-Aktion rückgängig machen |
| `--report` | HTML-Report im Browser öffnen |

## Features

- **Temp-Cleanup**: *.tmp, *.log, *.dmp, *.bak, *.temp, *.cache, *.swp, *.swo
- **Large Files**: Alles >100 MB wird gelistet
- **Duplikaterkennung**: Gleiche Größe + MD5-Hash → Merge-Vorschlag
- **Ähnliche Dateien**: Gleicher Name + ähnliche Größe (±10%) → Ordner-Vorschlag
- **Typ-Organizer**: Bilder, Dokumente, Archive, Audio, Video, Code, Installers, Fonts, Sonstiges
- **Undo**: Organize-Aktionen können rückgängig gemacht werden
- **HTML-Report**: Farbiger Report mit Karten und Tabellen
- **State**: Historie in `~/.file-organizer/state.json`

## Kategorien

| Kategorie | Typische Extensions |
|-----------|-------------------|
| Bilder | .jpg .jpeg .png .gif .bmp .svg .webp .ico .tiff .raw .heic |
| Dokumente | .pdf .doc .docx .xls .xlsx .ppt .pptx .txt .rtf .md .csv |
| Archive | .zip .rar .7z .tar .gz .bz2 .xz .zst |
| Audio | .mp3 .wav .flac .aac .ogg .wma .m4a .opus |
| Video | .mp4 .avi .mkv .mov .wmv .flv .webm .m4v |
| Code | .py .js .ts .html .css .c .cpp .java .rs .go .sh .bat .json .yaml .xml |
| Installers | .exe .msi .dmg .iso .appimage .deb .rpm |
| Fonts | .ttf .otf .woff .woff2 .eot |

## Pfad

`scripts/file-organizer.py` — im OpenAmer Scripts-Verzeichnis.

## Cron

Der Cron-Job `fileorganizer_clean_24h` läuft alle 24 Stunden und entfernt automatisch temporäre Dateien.