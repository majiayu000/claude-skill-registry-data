---
name: llmwiki-api
description: Interaktive Fernbedienung zur Steuerung der LLMWikiNG-API. Enthält alle API-Endpunkte, OKF-Richtlinien und anpassbare Konfigurationsvariablen.
---

# LLMWikiNG API-Fernbedienung

Dieses Dokument dient als direkte Fernbedienung zur Steuerung der LLMWikiNG-Plattform. **Passe die Werte im folgenden Konfigurationsblock an**, um die cURL-Befehle direkt kopieren und ausführen zu können.

---

## ⚙️ 1. Konfiguration (Vom Nutzer anpassbar)

Verwende diese Variablen in deinen Skripten oder passe sie hier direkt an:

```bash
# Basis-URL des Servers (z.B. Port 8080 oder 8081, oder externe Domain)
SERVER_URL="http://localhost:8081/LLMWikiNG"

# API-Key (erzeugt unter /settings -> API-Schlüssel)
API_KEY="llmw_dein_api_key_hier"

# Optionales Passwort (NUR nötig, wenn 'require_password' für diesen Key in der WebUI erzwungen wird. Ansonsten leer lassen!)
API_PASSWORD=""

# Ziel-Wiki (Da es mehrere Wikis gibt, z. B. 'main', 'wiki1', 'wiki2'. Jedes Wiki hat seine eigene Ordnerstruktur unter wikis/)
WIKI_NAME="main"
```

---

## 📦 2. Open Knowledge Format (OKF v0.1) Richtlinien

Wenn du Seiten via API erstellst oder aktualisierst, muss der Inhalt folgende Struktur aufweisen:

### YAML-Frontmatter (Pflicht):
```yaml
---
type: Concept         # Typ: Concept, Playbook, Reference, Table, Dataset
title: "Titel der Seite"
description: "Kurze Beschreibung des Inhalts"
resource: "file://raw/original_quelle.md" # Referenz auf Originaldatei
tags: [tag1, tag2]
timestamp: 2026-07-14T21:44:00Z
---
# Titel der Seite
Inhalt im Standard-Markdown...
```

*   **Verlinkungen:** Verwende nur native Markdown-Links: `[Link-Text](/concepts/ziel-seite.md)`. Obsidian-Wikilinks (`[[Ziel]]`) sind unzulässig.

---

## 🎛️ 3. API-Endpunkte (Die Fernbedienung)

Ersetze in den Beispielen die Variablen `$SERVER_URL`, `$API_KEY`, `$API_PASSWORD` und `$WIKI_NAME` durch deine oben konfigurierten Werte.

> [!NOTE]
> **API-Passwort Header:** Falls für deinen API-Key **kein** Passwort erzwungen wird, kannst du die Zeile `-H "X-API-Password: $API_PASSWORD"` in allen cURL-Befehlen einfach weglassen.

### A. Direktes Wiki-Management (Multi-Wiki Support)

#### 1. Direkter Ingest (Datei, URL oder Text in spezifisches Wiki hochladen & sofort verarbeiten)
Lädt Daten hoch und führt direkt das LLM-Ingest-Skript für dieses spezifische Wiki aus.

**a) Datei-Upload:**
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "X-API-Password: $API_PASSWORD" \
  -F "file=@/pfad/zu/deiner/datei.md" \
  -F "title=Optionale Dateibezeichnung" \
  "$SERVER_URL/wiki/$WIKI_NAME/api/ingest"
```

**b) URL-Ingest (Lädt URL herunter, konvertiert in Markdown und ingestiert):**
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "X-API-Password: $API_PASSWORD" \
  -F "url=https://example.com/artikellink" \
  -F "title=Mein URL Ingest" \
  "$SERVER_URL/wiki/$WIKI_NAME/api/ingest"
```

**c) Reiner Text-Ingest (Text-Paste):**
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "X-API-Password: $API_PASSWORD" \
  -F "text=# Überschrift\nInhalt des kopierten Texts..." \
  -F "title=Text-Paste-Titel" \
  "$SERVER_URL/wiki/$WIKI_NAME/api/ingest"
```

#### 2. Direktes Syncen
Synchronisiert Vektor-Embeddings und den Suchindex des Wikis.
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "X-API-Password: $API_PASSWORD" \
  "$SERVER_URL/wiki/$WIKI_NAME/api/sync"
```

---

### B. Standard API v1 (Daten-Routen)

#### 3. Wikis auflisten
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/wikis"
```

#### 4. Alle Seiten eines Wikis auflisten
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/wikis/$WIKI_NAME/pages"
```

#### 5. Inhalt einer Wiki-Seite abrufen
```bash
# Beispiel für Seite 'llm-wiki'
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/wikis/$WIKI_NAME/pages/llm-wiki"
```

#### 6. Neue Seite anlegen (Erfordert Scope: write)
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "test-seite", "content": "---\ntype: Concept\ntitle: Test-Seite\ntimestamp: 2026-07-14T21:44:00Z\n---\n# Test-Seite\nInhalt hier."}' \
  "$SERVER_URL/api/v1/wikis/$WIKI_NAME/pages"
```

#### 7. Seite exportieren
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  "$SERVER_URL/api/v1/wikis/$WIKI_NAME/pages/llm-wiki/export"
```

#### 8. Rohdatei ins Archiv hochladen (ohne sofortige Ingest-Verarbeitung)
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -F "file=@/pfad/zu/raw_datei.txt" \
  "$SERVER_URL/api/v1/wikis/$WIKI_NAME/ingest"
```

#### 9. Ausstehende Ingests anzeigen
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/wikis/$WIKI_NAME/pending"
```

#### 10. Ausstehende Ingests verarbeiten (Startet Hintergrundprozess)
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  "$SERVER_URL/api/v1/wikis/$WIKI_NAME/ingest/process"
```

#### 11. Volltextsuche (Unterstützt Cross-Wiki-Suche via wiki=all)
```bash
# Suche in einem bestimmten Wiki:
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/search?q=Suchbegriff&wiki=$WIKI_NAME"

# Cross-Wiki-Suche (alle Wikis durchsuchen):
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/search?q=Suchbegriff&wiki=all"
```

#### 12. Wissensgraph-Daten abrufen (Gesamter Graph)
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/wikis/$WIKI_NAME/graph"
```

#### 13. Wissensgraph-Daten paginiert abrufen (Für große Wikis)
```bash
# Holt Seite 0 mit max. 200 Knoten, optional gefiltert nach einem Tag
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/wikis/$WIKI_NAME/graph/paginated?page=0&page_size=200&tag=Concept"
```

#### 14. Wiki-Statistiken abrufen
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/wikis/$WIKI_NAME/stats"
```

#### 15. Linter ausführen
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/wikis/$WIKI_NAME/lint"
```

---

### C. System-, Admin- & Cache-Routen (Nur für Admin-Keys)

#### 16. Server-Status abrufen
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/status"
```

#### 17. Systemstatus & Traffic abrufen
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/system/status"
```

#### 18. Alle Wikis synchronisieren
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  "$SERVER_URL/api/v1/system/sync"
```

#### 19. Audit-Logs abrufen (Admin-API-Key erforderlich)
```bash
# Neueste 50 Einträge abrufen:
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/system/audit"

# Mit Filtern (action, username, start_date, end_date):
curl -H "X-API-Key: $API_KEY" \
  "$SERVER_URL/api/v1/system/audit?action=login_failed&limit=100"

# Zeitraum-Filter:
curl -H "X-API-Key: $API_KEY" \
  "$SERVER_URL/api/v1/system/audit?start_date=2026-07-01&end_date=2026-07-31"
```

Query-Parameter:
- `limit` (default: 50) – Maximale Anzahl Einträge
- `offset` (default: 0) – Pagination-Offset
- `action` – Filter auf Aktionstyp (z.B. `login`, `login_failed`, `page_delete`, `search`, `ingest`)
- `category` – Filter auf Kategorie (z.B. `auth`, `pages`, `search`, `ingest`, `system`)
- `username` – Filter auf bestimmten Benutzernamen
- `start_date` – Startzeit (ISO-Format: `YYYY-MM-DD`)
- `end_date` – Endzeit (ISO-Format: `YYYY-MM-DD`)
- `search` – Volltextsuche in Details, Username, IP und Aktion

#### 20. Update-Verfügbarkeit prüfen (Admin-API-Key erforderlich)
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/system/update/check"
```
Antwort:
```json
{
  "ok": true,
  "local_version": "3.0.0",
  "remote_version": "3.0.0",
  "update_available": false,
  "up_to_date": true
}
```

#### 21. Update ausführen (Admin-API-Key erforderlich)
```bash
curl -X POST -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/system/update/run"
```
Antwort:
```json
{
  "ok": true,
  "old_version": "2.15.3",
  "new_version": "3.0.0",
  "updated": true,
  "output": "... Update-Log ..."
}
```
**Hinweis:** Das Update-Skript sichert Benutzerdaten, führt `git reset --hard origin/main` aus und installiert Python-Abhängigkeiten. Timeout: 300 Sekunden.

#### 22. Cache-Statistiken abrufen
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/cache/stats"
```

#### 23. In-Memory Cache leeren
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  "$SERVER_URL/api/v1/cache/clear"
```

#### 23.1 Tailscale-Status abrufen (Admin-API-Key erforderlich)
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/system/tailscale/status"
```

#### 23.2 Tailscale-Konfiguration speichern (Admin-API-Key erforderlich)
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"hostname": "llmwiking", "auth_key": "tskey-...", "proxy_target": "http://127.0.0.1:8080", "funnel_enabled": false, "serve_enabled": true}' \
  "$SERVER_URL/api/v1/system/tailscale"
```

#### 23.3 Tailscale One-Click-Setup (Admin-API-Key erforderlich)
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"hostname": "llmwiking", "auth_key": "tskey-...", "funnel_enabled": true}' \
  "$SERVER_URL/api/v1/system/tailscale/setup"
```

#### 23.4 Weitere Tailscale-Aktionen (Admin-API-Key erforderlich)
```bash
# serve/funnel anwenden:
curl -X POST -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/system/tailscale/apply"

# HTTPS-Zertifikat via tailscale cert anfordern:
curl -X POST -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/system/tailscale/cert"

# Funnel & serve zurücksetzen:
curl -X POST -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/system/tailscale/reset"

# tailscale up / down:
curl -X POST -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/system/tailscale/up"
curl -X POST -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/system/tailscale/down"
```

#### 24. Benutzer auflisten
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/users"
```

#### 25. Neuen Benutzer anlegen
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"username": "neuer_nutzer", "password": "sicheres_passwort", "role": "editor"}' \
  "$SERVER_URL/api/v1/users"
```

#### 26. Benutzer löschen
```bash
# Ersetze USER_ID durch die ID aus der Benutzerliste
curl -X DELETE \
  -H "X-API-Key: $API_KEY" \
  "$SERVER_URL/api/v1/users/USER_ID"
```

#### 26.1 Benutzer bearbeiten (WebUI-Route, Session-basiert)
```bash
# Ersetze USER_ID durch die ID aus der Benutzerliste
# Felder: username, password (optional), role (admin/editor/viewer), active
curl -X POST \
  -b "session=DEIN_SESSION_COOKIE" \
  -d "username=neuer_name&role=editor&active=1" \
  "$SERVER_URL/users/USER_ID/edit"
```
Der eigene Account kann weder deaktiviert noch degradiert werden; der letzte aktive Administrator ist geschützt. Über MCP steht dasselbe als `okf_update_user` zur Verfügung.

#### 27. API-Keys auflisten
```bash
curl -H "X-API-Key: $API_KEY" "$SERVER_URL/api/v1/api-keys"
```

#### 28. Neuen API-Key generieren
```bash
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mein Skript Key", "require_password": true, "scopes": ["read", "write"]}' \
  "$SERVER_URL/api/v1/api-keys"
```

#### 29. API-Key löschen/widerrufen
```bash
# Ersetze KEY_ID durch die ID aus der API-Key-Liste
curl -X DELETE \
  -H "X-API-Key: $API_KEY" \
  "$SERVER_URL/api/v1/api-keys/KEY_ID"
```

---

## 🤖 3.5. MCP-Server (Model Context Protocol) – OKF v0.1

LLMWikiNG stellt einen nativen MCP-Server bereit, der KI-Agenten (Cursor, Windsurf, Claude Code) direkten Zugriff auf das Wiki im Open Knowledge Format (OKF v0.1) ermöglicht.

### Konfiguration

```bash
# MCP-API-Key (separate Umgebungsvariable oder in config.json)
MCP_KEY="dein_sicherer_mcp_key_2026"
MCP_SSE_URL="http://localhost:8080/LLMWikiNG/mcp/sse"
```

### MCP-Tools (49 Stück)

Das MCP-Interface kann alles, was auch die REST-API kann. Vollständige Parität zwischen API-Key und MCP-Agenten-Zugang.

| Tool | Beschreibung |
|------|-------------|
| **Wiki-Verwaltung** | |
| `okf_list_wikis` | Listet alle Wikis mit Metadaten |
| `okf_create_wiki` | Erstellt ein neues Wiki |
| `okf_update_wiki` | Bearbeitet Name/Beschreibung/Slug |
| `okf_delete_wiki` | Loescht ein Wiki |
| **Seiten-Verwaltung** | |
| `okf_list_pages` | Listet alle Seiten eines Wikis |
| `okf_read_concept` | Liest ein OKF-Konzept |
| `okf_write_concept` | Erstellt/Aktualisiert ein OKF-Konzept |
| `okf_delete_page` | Loescht eine Wiki-Seite |
| `okf_export_page` | Exportiert eine Seite nach output_docs/ |
| `okf_list_pending` | Listet Rohquellen auf Ingest |
| `okf_process_pending` | Verarbeitet ausstehende Rohquellen |
| `okf_ingest_text` | Ingest von reinem Text |
| **Suche & Analyse** | |
| `okf_search` | Volltextsuche |
| `okf_matrix_search` | Persistente Volltextsuche über den Matrix-Index (FTS5, `enable_matrix` erforderlich) |
| `okf_matrix_ingest` | Dokument direkt in den Matrix-Index einspielen (persistenter Index) |
| `okf_wiki_stats` | Wiki-Statistiken |
| `okf_graph` | Wissensgraph |
| `okf_lint` | Gesundheitspruefung |
| **Rohquellen** | |
| `okf_read_raw` | Liest Rohquelle aus raw/ |
| `okf_list_raw` | Listet alle Rohquellen |
| **System** | |
| `okf_system_status` | Systemstatus |
| `okf_system_sync` | Wiki-Synchronisation |
| `okf_audit_logs` | Audit-Protokolle |
| `okf_cache_stats` | Cache-Statistiken |
| `okf_cache_clear` | Cache leeren |
| **Benutzer** | |
| `okf_list_users` | Benutzer auflisten |
| `okf_create_user` | Benutzer erstellen |
| `okf_update_user` | Benutzer bearbeiten (Name, Passwort, Rolle, Aktivstatus) |
| `okf_delete_user` | Benutzer loeschen |
| **API-Keys** | |
| `okf_list_api_keys` | API-Keys auflisten |
| `okf_create_api_key` | API-Key erstellen |
| `okf_delete_api_key` | API-Key loeschen |
| **MCP-Keys** | |
| `okf_list_mcp_keys` | Per-User MCP-Keys auflisten |
| `okf_create_mcp_key` | Per-User MCP-Key mit Tool-Berechtigungen erstellen |
| `okf_delete_mcp_key` | Per-User MCP-Key loeschen |
| **Backups** | |
| `okf_list_backups` | Server-Backups auflisten |
| `okf_create_backup` | Server-Backup erstellen (.tar.xz) |
| `okf_restore_backup` | Server-Backup wiederherstellen |
| **Update** | |
| `okf_check_update` | Update-Verfuegbarkeit pruefen |
| `okf_run_update` | System-Update ausfuehren |
| **Tailscale & Funnel** | |
| `okf_tailscale_status` | Tailscale-Status & Konfiguration anzeigen |
| `okf_tailscale_save` | Tailscale-Konfiguration speichern |
| `okf_tailscale_setup` | Tailscale One-Click-Setup (up + serve/funnel) |
| `okf_tailscale_apply` | serve/funnel-Konfiguration anwenden |
| `okf_tailscale_cert` | HTTPS-Zertifikat via `tailscale cert` anfordern |
| `okf_tailscale_reset` | Funnel & serve zuruecksetzen |

### Matrix-Index (persistente Volltextsuche, ab v3.0.0)

Seit v3.0.0 ist der **Projekt-Matrix-Index** die einzige Such- und Sync-Engine von LLMWikiNG (keine externe Such-Binary erforderlich). Er ist eine persistente FTS5-Suche über SQLite-Shards unter `data/matrix/` (NAS-sicher: WAL, `synchronous=FULL`, `busy_timeout`), gesteuert über das Feature-Flag `enable_matrix` in `config.json`.

**REST-Endpunkte** (unter `${BASE}/api/v1/matrix`):

| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| GET / POST | `/search?q=...&wikis=main&limit=30` | FTS5-Suche mit `bm25`-Ranking und `snippet()`-Hervorhebung |
| POST | `/ingest` | Dokument zur Indexierung einreihen (202) |
| POST | `/ingest/bulk` | Mehrere Dokumente auf einmal einreihen |
| DELETE | `/document/{wiki_id}/{doc_id}` | Dokument aus dem Index entfernen (Admin) |
| GET | `/stats` | Shard-Anzahl, Index-Größe, Queue, Rebuild-Fortschritt |
| GET | `/health` | Registry- und Shard-Lesbarkeitsprüfung |
| POST | `/rebuild?wiki_id=all` | Vollständigen Neuaufbau im Hintergrund starten (Admin) |
| POST | `/prune` | Verwaiste Registry-Einträge entfernen (Admin) |

**Bootstrap / Neuaufbau:**

```bash
./wiki.sh matrix-rebuild
python3 scripts/bootstrap_matrix.py [--wiki <slug>]
```

**MCP-Tools:** `okf_matrix_search` (Gruppe `wiki_read`) und `okf_matrix_ingest` (Gruppe `wiki_write`). Die Web-UI-Suche, der API-Endpunkt `/api/v1/search` und der Settings-Tab „⚡ Matrix" bedienen sich desselben Index; ohne aktiviertes Flag fallen alle Pfade auf die Legacy-Suche zurück.

### Client-Einbindung

#### Antigravity CLI (`agy`) & Antigravity IDE

Füge die MCP-Konfiguration in `~/.gemini/antigravity-cli/settings.json` (global) oder `.agents/mcp_config.json` (Workspace) ein:

```json
{
  "mcpServers": {
    "llmwiki-okf": {
      "type": "http",
      "url": "http://localhost:8080/LLMWikiNG/mcp",
      "headers": {
        "X-MCP-Key": "dein_per_user_mcp_key",
        "X-API-Key": "dein_api_key"
      }
    }
  }
}
```

Oder nutze die Agent-Prompt-Konfiguration:

```
Bitte konfiguriere dich so, dass du dich mit dem LLMWikiNG-MCP-Server verbindest.
Der Server nutzt SSE (Server-Sent Events) unter der URL: http://localhost:8080/LLMWikiNG/mcp/sse.
Du musst die Header 'X-MCP-Key' mit dem Wert '<DEIN_MCP_SERVER_KEY>' und
'X-API-Key' mit dem Wert '<DEIN_AGENT_API_KEY>' mitsenden.
```

#### Cursor

Füge in Cursor unter Settings → Features → MCP hinzu:
- **Name:** LLMWikiNG-OKF
- **Type:** SSE
- **URL:** `http://localhost:8080/LLMWikiNG/mcp/sse`
- **Headers:** `{"X-API-Key": "dein_sicherer_mcp_key_2026"}`

#### OpenCode

Füge in `opencode.json` unter `mcp` hinzu:
```json
{
  "mcp": {
    "llmwiki-okf": {
      "type": "remote",
      "url": "http://localhost:8080/LLMWikiNG/mcp/sse",
      "enabled": true,
      "headers": {
        "X-MCP-Key": "dein_per_user_mcp_key",
        "X-API-Key": "dein_api_key"
      }
    }
  }
}
```

Beispiel mit öffentlicher Tailscale-Funnel-URL:
```json
{
  "mcp": {
    "llmwiki-okf": {
      "type": "remote",
      "url": "https://DEIN_TAILNET.ts.net/LLMWikiNG/mcp/sse",
      "enabled": true,
      "headers": {
        "X-MCP-Key": "dein_per_user_mcp_key",
        "X-API-Key": "dein_api_key"
      }
    }
  }
}
```

---

## 💻 4. Interaktiver CLI Ingest-Client (`tools/api_ingest_client.py`)

Für die komfortable Interaktion aus der Konsole steht das Skript `tools/api_ingest_client.py` bereit. Es fungiert als Fernbedienung mit automatischer Wiki-Auswahl:

### Ablauf:
1.  **Starten:** `./tools/api_ingest_client.py`
2.  **Wiki-Auswahl:** Das Skript ruft via API die Liste aller verfügbaren Wikis ab. Gib die Nummer deines gewünschten Wikis ein.
3.  **Aktion wählen:**
    - `[1]` Inhalt Ingestieren (Datei, URL oder Text)
    - `[2]` Volltextsuche im Wiki ausführen
4.  **Bei Ingest:** Wähle den Typ (Datei, URL, Text) und gib den Inhalt an. Du erhältst direkt einen **klickbaren Link** zur neuen Seite.
5.  **Bei Suche:** Gib deinen Suchbegriff ein. Die Treffer werden direkt im Terminal mit Score, Pfad, Link und farblich hervorgehobenem Textausschnitt (Snippet) ausgegeben.

### Konfiguration (Umgebungsvariablen):
Du kannst die Zugangsdaten direkt in deine Shell exportieren, damit das Skript ohne Nachfragen läuft:
```bash
export LLMWIKI_API_KEY="llmw_dein_schluessel"
export LLMWIKI_SERVER_URL="http://localhost:8081/LLMWikiNG"
export LLMWIKI_API_PASSWORD="optionales_passwort"
```
