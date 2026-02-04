---
name: bel-crm-db
description: " Uses the mcp postgresql to read and write crm relevant data to the crm database:
  Its about:
  sales_opportunity (Verkaufschancen)
  person (Kontaktperson im Unternehmen)
  company_site (Ein Standort eines Unternehmens)
  event (Aktivität, TODO, ... insgesamt bilden die Aktivitäten die Historie und die Zukunft von company_site, person und sales_opportunity ab)
  data_files (Dateien: PDFs, Bilder, E-Mail-Anhänge, Office-Dokumente - verknüpft mit CRM-Entitäten)"
---

## CRITICAL: SQL Limitations - READ FIRST!

**Before writing ANY SQL, know these PostgreSQL MCP server limitations:**

| FORBIDDEN | WHY | USE INSTEAD |
|-----------|-----|-------------|
| `RETURNING` | Syntax error | Query ID separately with `read_query` |
| `ON CONFLICT` | Not supported | Check existence first, then INSERT or UPDATE |
| Multiple statements | Not allowed | One statement per tool call |

**Example - CORRECT pattern for INSERT:**
```sql
-- Step 1: write_query (NO RETURNING!)
INSERT INTO company_site (name, created_at, updated_at)
VALUES ('Acme GmbH', now(), now());

-- Step 2: read_query (get ID if needed)
SELECT id FROM company_site WHERE name = 'Acme GmbH' ORDER BY created_at DESC LIMIT 1;
```

**For complete SQL rules, see the `bel-crm-sql-rules` skill.**

---

You will probably only use those tools from postgresql mcp server:
- mcp__postgresql__read_query,
- mcp__postgresql__write_query

This is the SCHEMA you will work on:

 Hier ist das vollständige Datenbankschema:

  📊 Datenbank-Schema Übersicht

  Die Datenbank enthält 6 Tabellen für ein CRM-System:

  ---
  1. adressen (Legacy-Adresstabelle)

  Persönliche Kontaktdaten (deutschsprachig):

  | Spalte             | Typ       | Beschreibung         |
  |--------------------|-----------|----------------------|
  | id                 | INTEGER   | 🔑 Primary Key       |
  | vorname            | VARCHAR   | Vorname              |
  | nachname           | VARCHAR   | Nachname             |
  | strasse_hausnummer | VARCHAR   | Straße & Hausnummer  |
  | plz                | VARCHAR   | Postleitzahl         |
  | ort                | VARCHAR   | Ort                  |
  | email              | VARCHAR   | E-Mail               |
  | mobil              | VARCHAR   | Mobilnummer          |
  | tel                | VARCHAR   | Telefon              |
  | erstellt_am        | TIMESTAMP | Erstellungsdatum     |
  | aktualisiert_am    | TIMESTAMP | Aktualisierungsdatum |

  ---
  2. company_site (Unternehmensstandorte)

  Firmeninformationen und Standorte:

  | Spalte               | Typ       | Beschreibung             |
  |----------------------|-----------|--------------------------|
  | id                   | INTEGER   | 🔑 Primary Key           |
  | name                 | VARCHAR   | ⚠️ NOT NULL - Firmenname |
  | address_street       | VARCHAR   | Straße                   |
  | address_city         | VARCHAR   | Stadt                    |
  | address_state        | VARCHAR   | Bundesland               |
  | address_postal_code  | VARCHAR   | PLZ                      |
  | address_country      | VARCHAR   | Land                     |
  | industry             | VARCHAR   | Branche                  |
  | website              | VARCHAR   | Website                  |
  | linkedin_company_url | VARCHAR   | LinkedIn-Profil          |
  | company_size         | VARCHAR   | Unternehmensgröße        |
  | annual_revenue       | BIGINT    | Jahresumsatz             |
  | notes                | TEXT      | Notizen                  |
  | tags                 | JSONB     | Tags (JSON)              |
  | created_at           | TIMESTAMP | Erstellt am              |
  | updated_at           | TIMESTAMP | Aktualisiert am          |

  ---
  3. person (Kontaktpersonen)

  Ansprechpartner in Unternehmen:

  | Spalte          | Typ       | Beschreibung         |
  |-----------------|-----------|----------------------|
  | id              | INTEGER   | 🔑 Primary Key       |
  | name            | VARCHAR   | ⚠️ NOT NULL - Name   |
  | email           | VARCHAR   | E-Mail               |
  | phone           | VARCHAR   | Telefon              |
  | linkedin_url    | VARCHAR   | LinkedIn-Profil      |
  | company_site_id | INTEGER   | 🔗 FK → company_site |
  | job_title       | VARCHAR   | Jobtitel             |
  | department      | VARCHAR   | Abteilung            |
  | notes           | TEXT      | Notizen              |
  | tags            | JSONB     | Tags (JSON)          |
  | created_at      | TIMESTAMP | Erstellt am          |
  | updated_at      | TIMESTAMP | Aktualisiert am      |

  ---
  4. sales_opportunity (Verkaufschancen)

  Sales-Pipeline und Opportunities:

  | Spalte              | Typ       | Beschreibung             |
  |---------------------|-----------|--------------------------|
  | id                  | INTEGER   | 🔑 Primary Key           |
  | title               | VARCHAR   | ⚠️ NOT NULL - Titel      |
  | value_eur           | NUMERIC   | Wert in EUR              |
  | probability         | INTEGER   | Wahrscheinlichkeit (%)   |
  | status              | VARCHAR   | Status (default: 'open') |
  | description         | TEXT      | Beschreibung             |
  | expected_close_date | DATE      | Erwarteter Abschluss     |
  | actual_close_date   | DATE      | Tatsächlicher Abschluss  |
  | person_id           | INTEGER   | 🔗 FK → person           |
  | company_site_id     | INTEGER   | 🔗 FK → company_site     |
  | source              | VARCHAR   | Quelle                   |
  | competitors         | TEXT      | Wettbewerber             |
  | next_steps          | TEXT      | Nächste Schritte         |
  | notes               | TEXT      | Notizen                  |
  | tags                | JSONB     | Tags (JSON)              |
  | created_at          | TIMESTAMP | Erstellt am              |
  | updated_at          | TIMESTAMP | Aktualisiert am          |

  ---
  5. event (Aktivitäten/Events)

  Aktivitätsverlauf (Meetings, Calls, etc.):

  | Spalte          | Typ       | Beschreibung               |
  |-----------------|-----------|----------------------------|
  | id              | INTEGER   | 🔑 Primary Key             |
  | type            | VARCHAR   | ⚠️ NOT NULL - Event-Typ    |
  | description     | TEXT      | ⚠️ NOT NULL - Beschreibung |
  | event_date      | TIMESTAMP | ⚠️ NOT NULL - Event-Datum  |
  | person_id       | INTEGER   | 🔗 FK → person             |
  | company_site_id | INTEGER   | 🔗 FK → company_site       |
  | opportunity_id  | INTEGER   | 🔗 FK → sales_opportunity  |
  | metadata        | JSONB     | Zusatzdaten (JSON)         |
  | created_at      | TIMESTAMP | Erstellt am                |

  ---
  6. data_files (Dateien & E-Mail-Anhänge)

  Speichert Dateien (PDFs, Bilder, Office-Dokumente, E-Mail-Anhänge) mit Base64-Encoding:

  | Spalte               | Typ       | Beschreibung                                      |
  |----------------------|-----------|---------------------------------------------------|
  | id                   | INTEGER   | 🔑 Primary Key                                    |
  | person_id            | INTEGER   | 🔗 FK → person                                    |
  | company_site_id      | INTEGER   | 🔗 FK → company_site                              |
  | event_id             | INTEGER   | 🔗 FK → event                                     |
  | sales_opportunity_id | INTEGER   | 🔗 FK → sales_opportunity                         |
  | filename             | VARCHAR   | ⚠️ NOT NULL - Dateiname (oder E-Mail-Subject)    |
  | file_type            | VARCHAR   | ⚠️ NOT NULL - pdf, image, docx, pptx, xlsx, **email**, other |
  | mime_type            | VARCHAR   | MIME-Type (z.B. application/pdf, message/rfc822)  |
  | file_size_bytes      | BIGINT    | Dateigröße in Bytes (max 100MB)                   |
  | file_hash            | VARCHAR   | SHA-256 Hash (Duplikat-Erkennung)                 |
  | source               | VARCHAR   | ⚠️ NOT NULL - email_attachment, user_upload, agent_download, **email_message** |
  | source_email_id      | VARCHAR   | MS365 Message ID                                  |
  | source_path          | VARCHAR   | Originaler Dateipfad                              |
  | file_data            | TEXT      | Base64-kodierter Dateiinhalt (NULL bei E-Mails ohne Anhang) |
  | email_metadata       | JSONB     | E-Mail-Metadaten (from, to, cc, subject, date, importance) |
  | email_body_text      | TEXT      | E-Mail-Body als Plain Text                        |
  | email_body_html      | TEXT      | E-Mail-Body als HTML                              |
  | extracted_text       | TEXT      | Extrahierter Text (für Volltextsuche)             |
  | extraction_method    | VARCHAR   | pdf_text, ocr, docx_parse, email_body, etc.       |
  | extraction_status    | VARCHAR   | pending, completed, failed, skipped               |
  | extraction_error     | TEXT      | Fehlermeldung bei Extraktion                      |
  | description          | TEXT      | Benutzer-Beschreibung                             |
  | tags                 | JSONB     | Tags (JSON)                                       |
  | created_at           | TIMESTAMP | Erstellt am                                       |
  | updated_at           | TIMESTAMP | Aktualisiert am                                   |

  Beispiel - Komplette E-Mail speichern (mit Body):
  ```sql
  INSERT INTO data_files (
      person_id, filename, file_type, mime_type,
      source, source_email_id, email_metadata,
      email_body_text, email_body_html,
      extracted_text, extraction_method, extraction_status
  ) VALUES (
      1,
      'Re: Contract Draft',  -- Subject als filename
      'email',
      'message/rfc822',
      'email_message',
      'AAMkAGI2TG93AAA=',
      '{
        "subject": "Re: Contract Draft",
        "from": {"name": "John Doe", "email": "john@example.com"},
        "to": [{"email": "you@company.com"}],
        "cc": [{"email": "legal@company.com"}],
        "received_at": "2025-01-15T10:30:00Z",
        "importance": "high",
        "hasAttachments": true,
        "conversationId": "AAQkAGI2..."
      }'::jsonb,
      'Hallo, anbei der überarbeitete Vertragsentwurf...',  -- Plain text
      '<html><body><p>Hallo, anbei der überarbeitete Vertragsentwurf...</p></body></html>',
      'Hallo, anbei der überarbeitete Vertragsentwurf...',  -- Für Suche
      'email_body',
      'completed'
  ) RETURNING id, filename;
  ```

  Beispiel - E-Mail-Anhang speichern (verknüpft mit E-Mail):
  ```sql
  -- Erst E-Mail speichern, dann Anhänge mit gleicher source_email_id
  INSERT INTO data_files (
      person_id, filename, file_type, mime_type, file_size_bytes,
      source, source_email_id, file_data, email_metadata
  ) VALUES (
      1, 'contract.pdf', 'pdf', 'application/pdf', 245678,
      'email_attachment', 'AAMkAGI2TG93AAA=',  -- Gleiche ID wie E-Mail!
      '<base64-encoded-content>',
      '{"subject": "Re: Contract Draft", "from": {"email": "john@example.com"}}'::jsonb
  ) RETURNING id, filename;
  ```

  Alle Dateien einer E-Mail finden (E-Mail + Anhänge):
  ```sql
  SELECT id, filename, file_type, source, file_size_bytes
  FROM data_files
  WHERE source_email_id = 'AAMkAGI2TG93AAA='
  ORDER BY file_type = 'email' DESC, filename;
  ```

  Beispiel - Datei aus _DATA_FROM_USER hochladen:
  ```sql
  INSERT INTO data_files (
      company_site_id, filename, file_type, mime_type, file_size_bytes,
      source, source_path, file_data
  ) VALUES (
      5, 'proposal.pdf', 'pdf', 'application/pdf', 512000,
      'user_upload', '_DATA_FROM_USER/proposal.pdf',
      '<base64-encoded-content>'
  ) RETURNING id, filename;
  ```

  Volltextsuche in extrahiertem Text:
  ```sql
  SELECT id, filename, person_id, company_site_id
  FROM data_files
  WHERE to_tsvector('german', extracted_text) @@ to_tsquery('german', 'Vertrag & Angebot');
  ```

  ---
  7. schema_migrations (System-Tabelle)

  Datenbank-Migrationen:

  | Spalte      | Typ       | Beschreibung     |
  |-------------|-----------|------------------|
  | id          | BIGINT    | Migrations-ID    |
  | applied     | TIMESTAMP | Ausführungsdatum |
  | description | VARCHAR   | Beschreibung     |

  ---
  🔗 Beziehungen (Foreign Keys)

  company_site (1) ──┬── (N) person
                     ├── (N) sales_opportunity
                     ├── (N) event
                     └── (N) data_files

  person (1) ────────┬── (N) sales_opportunity
                     ├── (N) event
                     └── (N) data_files

  sales_opportunity (1) ─┬── (N) event
                         └── (N) data_files

  event (1) ──────────── (N) data_files

  ---
  ⚠️ WICHTIG: KEINE UNIQUE CONSTRAINTS AUF name!

  Die Tabellen haben KEINE UNIQUE-Constraints auf `name`:
  - company_site.name ist NICHT unique
  - person.name ist NICHT unique
  - sales_opportunity.title ist NICHT unique

  **NIEMALS `ON CONFLICT (name)` verwenden!** Das führt zu Fehlern!

  Stattdessen:
  1. ERST prüfen ob Eintrag existiert: `SELECT id FROM company_site WHERE name ILIKE '%..%'`
  2. DANN entweder UPDATE (wenn gefunden) oder INSERT (wenn nicht gefunden)

  Beispiel - Firma erstellen oder finden:
  ```sql
  -- SCHRITT 1: Prüfen ob existiert
  SELECT id, name FROM company_site WHERE name ILIKE '%Kölner Stadt%' LIMIT 1;

  -- SCHRITT 2a: Falls gefunden → UPDATE
  UPDATE company_site SET updated_at = CURRENT_TIMESTAMP, notes = 'Updated...' WHERE id = <gefundene_id>;

  -- SCHRITT 2b: Falls nicht gefunden → INSERT
  INSERT INTO company_site (name, address_city, created_at, updated_at)
  VALUES ('Neue Firma GmbH', 'Berlin', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
  RETURNING id;
  ```

  ---
  💡 Besonderheiten

  - JSONB-Felder: tags, metadata, email_metadata für flexible Erweiterungen
  - Timestamps: Auto-Update via CURRENT_TIMESTAMP
  - Dual-System: Alte adressen-Tabelle + neues CRM-Schema
  - Multi-Entity Events: Events können mit Person, Firma ODER Opportunity verknüpft sein
  - Dateispeicherung: Base64-kodiert in TEXT-Feld (max 100MB)
  - Volltextsuche: GIN-Index auf extracted_text für deutsche Suche
  - Duplikat-Erkennung: SHA-256 Hash auf file_hash

  ---
  📎 Datei-Workflows

  ### E-Mail-Anhänge extrahieren (MS365)

  1. E-Mails suchen:
     ```
     mcp__ms365__list-mail-messages mit filter oder search
     ```

  2. Anhänge auflisten:
     ```
     mcp__ms365__list-mail-attachments(messageId)
     ```

  3. Anhang-Inhalt holen (bereits Base64!):
     ```
     mcp__ms365__get-mail-attachment(messageId, attachmentId)
     → contentBytes ist bereits Base64-kodiert
     ```

  4. In CRM speichern:
     ```sql
     INSERT INTO data_files (person_id, filename, file_type, source, file_data, email_metadata)
     VALUES (...) RETURNING id;
     ```

  ### User-Upload aus _DATA_FROM_USER

  1. Datei lesen und Base64-kodieren (in Python/Node)
  2. SHA-256 Hash berechnen für Duplikat-Check
  3. In CRM mit source = 'user_upload' speichern

  ### Text-Extraktion

  | Dateityp | Methode | extraction_method |
  |----------|---------|-------------------|
  | PDF | Text-Extraktion (pypdf) | pdf_text |
  | PDF (gescannt) | OCR (pytesseract) | pdf_ocr |
  | Bild | OCR (pytesseract) | ocr |
  | DOCX | python-docx | docx_parse |
  | PPTX | python-pptx | pptx_parse |
  | XLSX | openpyxl | xlsx_parse |
