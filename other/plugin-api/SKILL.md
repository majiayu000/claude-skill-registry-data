---
name: plugin-api
category: software-development
description: "Vollständige Dokumentation des OpenAmer Plugin-API-Systems. Hooks, Events, Lifecycle, manifest.json Format, Config-Integration und Plugin-Manager."
---

# OpenAmer Plugin API

> **Dokumentation für Plugin-Autoren** — Architektur, Hooks, Lifecycle und
> Best Practices für das OpenAmer-Plugin-System.

---

## Inhaltsverzeichnis

1. [Architekturübersicht](#1-architekturübersicht)
2. [Plugin-Lifecycle](#2-plugin-lifecycle)
3. [Verfügbare Hooks](#3-verfügbare-hooks)
   - [onReady](#31-onready)
   - [onMessage](#32-onmessage)
   - [onCommand](#33-oncommand)
   - [onCronRun](#34-oncronrun)
   - [onToolCall](#35-ontoolcall)
4. [plugin.yaml — Manifest-Format](#4-pluginyaml--manifest-format)
5. [register(ctx) — Einsprungspunkt](#5-registerctx--einsprungspunkt)
6. [Context API (ctx)](#6-context-api-ctx)
7. [Config-Integration](#7-config-integration)
8. [Plugin-Manager](#8-plugin-manager)
9. [Best Practices & Pitfalls](#9-best-practices--pitfalls)
10. [Beispiel-Plugins](#10-beispiel-plugins)

---

## 1. Architekturübersicht

Das Plugin-System von OpenAmer erlaubt es, das Agent-Verhalten ohne
Kernänderungen zu erweitern. Plugins sind **selbstständige Python-Pakete**,
die in einem eigenen Verzeichnis unter `plugins/` oder `desktop-plugins/`
leben. Jedes Plugin:

- Deklariert seine Metadaten in einer **`plugin.yaml`**
- Registriert seine Hooks über eine **`register(ctx)`**-Funktion in
  **`__init__.py`**
- Nutzt die **Context API**, um sich im System einzuklinken

```
openamer-repo/
├── plugins/                    # Built-in Plugins (bundled)
│   ├── browser/
│   │   ├── browser_use/
│   │   │   ├── __init__.py
│   │   │   ├── plugin.yaml
│   │   │   └── provider.py
│   │   └── ...
│   ├── image_gen/
│   ├── memory/
│   └── ...
├── desktop-plugins/            # Desktop/User-Plugins
│   └── examples/
│       ├── hello-world/
│       └── slash-command/
└── scripts/
    └── plugin-manager.py       # CLI-Verwaltung
```

### Design-Prinzipien

| Prinzip | Beschreibung |
|---------|-------------|
| **Narrow Waist** | Das Plugin-API ist schmal — wenige Hooks, klare Verträge |
| **Selbstständig** | Jedes Plugin ist ein eigenständiges Python-Paket |
| **Keine Kern-Importe** | Plugins importieren NIEMALS Core-Module direkt — nur die Context API |
| **Config-gesteuert** | Plugins werden per `config.yaml` ein-/ausgeschaltet |
| **Thread-sicher** | Alle Hooks können in Multi-Thread-Umgebungen laufen |

---

## 2. Plugin-Lifecycle

Jedes Plugin durchläuft einen definierten Lifecycle:

```
┌──────────────────────────────────────────────────┐
│                   DISCOVERY                       │
│  Plugin wird beim Start im Plugin-Pfad gefunden   │
│  → plugin.yaml wird gelesen                       │
│  → Manifest wird validiert                        │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│                   LOADING                         │
│  __init__.py wird importiert                      │
│  register(ctx) wird aufgerufen                    │
│  → Hooks werden registriert                      │
│  → Initialisierungslogik läuft                   │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│                   ENABLED                         │
│  Plugin ist aktiv (sofern enabled: true)          │
│  → onReady feuert                                  │
│  → Hooks reagieren auf Events                     │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│                   DISABLED                        │
│  Plugin wird per Config ausgeschaltet             │
│  → Hook-Aufrufe werden ignoriert                  │
│  → Ressourcen bleiben geladen (kein Teardown)    │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│                   TEARDOWN                        │
│  (Nicht implementiert — cleanup per Cron/Manuell) │
└──────────────────────────────────────────────────┘
```

### Lifecycle-Details

| Phase | Beschreibung |
|-------|-------------|
| **Discovery** | Der Plugin-Loader durchsucht `plugins/` und `desktop-plugins/` nach `plugin.yaml`. Wird das Plugin per Config deaktiviert (`plugin.<name>.enabled: false`), wird es übersprungen. |
| **Loading** | Das `__init__.py` des Plugins wird importiert und `register(ctx)` aufgerufen. Das Plugin registriert hier seine Hooks. |
| **Enabled** | Sobald der Agent bereit ist, feuert `onReady`. Danach reagiert das Plugin auf Events gemäß seiner registrierten Hooks. |
| **Disabled** | Das Plugin bleibt im Speicher, aber Hook-Callbacks werden nicht aufgerufen. Ein Re-Enable zur Laufzeit ist möglich. |
| **Teardown** | Geplant für zukünftige Versionen — ermöglicht Ressourcen-Freigabe bei Plugin-Deaktivierung oder Agent-Shutdown. |

---

## 3. Verfügbare Hooks

Hooks sind die primäre Möglichkeit, in das Agent-Verhalten einzugreifen.
Jeder Hook hat einen definierten **Payload** und **Rückgabetyp**.

### 3.1 `onReady`

Wird einmal aufgerufen, nachdem der Agent vollständig gestartet ist und bevor
die erste User-Nachricht verarbeitet wird.

```python
def on_hook_ready(ctx) -> None:
    """Wird nach dem Agent-Start aufgerufen."""
    logger.info("Plugin bereit — Agent ist gestartet")
    ctx.register_tool("my_tool", my_tool_handler)
```

**Use Cases:**
- Einmalige Initialisierung (Client-Verbindung, Daten laden)
- Tools registrieren
- Hintergrund-Watcher starten

### 3.2 `onMessage`

Wird bei jeder eingehenden User-Nachricht aufgerufen — **vor** der
Agent-Verarbeitung.

```python
def on_hook_message(ctx, message: str) -> str | None:
    """Wird bei jeder User-Nachricht aufgerufen.
    
    Args:
        message: Die rohe User-Nachricht.
    
    Returns:
        Optional modifizierte Nachricht (wird an Agent weitergegeben)
        oder None (keine Änderung).
    """
    if "!wetter" in message:
        return ctx.format_weather(get_weather())
    return None  # Keine Änderung — an Agent weiterleiten
```

**Use Cases:**
- Message-Preprocessing (Slash-Commands, Makros)
- Keyword-Trigger (z. B. "!wetter Berlin")
- Content-Filter

### 3.3 `onCommand`

Wird bei registrierten Slash-Commands aufgerufen (`/cmd`).

```python
def on_hook_command(ctx, command: str, args: str) -> str | None:
    """Wird bei einem registrierten Slash-Command aufgerufen.
    
    Args:
        command: Der Command-Name ohne Slash (z. B. "translate" für "/translate")
        args: Die restliche Argument-Zeile
    
    Returns:
        Antwort-String oder None (wenn Command nicht behandelt)
    """
    if command == "translate":
        target = args.split() if args else "en"
        text = " ".join(args.split()[1:]) if len(args.split()) > 1 else ""
        return f"Übersetzung ({target}): {do_translate(text, target)}"
    return None
```

**Use Cases:**
- Eigene Slash-Commands (`/translate`, `/remind`, `/calc`)
- Workflow-Trigger (`/deploy`, `/build`)
- Integration externer APIs

### 3.4 `onCronRun`

Wird bei Cron-Job-Ausführung aufgerufen.

```python
def on_hook_cron(ctx, cron_id: str) -> None:
    """Wird bei Cron-Job-Execution aufgerufen.
    
    Args:
        cron_id: Die ID des Cron-Jobs (aus der Cron-Konfiguration).
    """
    if cron_id == "daily_summary":
        summary = generate_daily_summary()
        ctx.send_notification("daily-summary", summary)
```

**Use Cases:**
- Tägliche Reports / Zusammenfassungen
- Periodische Daten-Syncs
- Health-Checks
- Scheduled Cleanup

### 3.5 `onToolCall`

Wird **vor** und **nach** jedem Tool-Call des Agenten aufgerufen.

```python
def on_hook_tool_call(ctx, tool_name: str, arguments: dict, 
                      phase: str, result: Any = None) -> dict | None:
    """Wird vor/nach Tool-Calls aufgerufen.
    
    Args:
        tool_name: Name des aufgerufenen Tools
        arguments: Tool-Argumente
        phase: "before" (vor Ausführung) oder "after" (nach Ausführung)
        result: Tool-Ergebnis (nur bei phase="after")
    
    Returns:
        Bei phase="before": Optional modifizierte Argumente
        Bei phase="after": Optional modifiziertes Ergebnis
    """
    if phase == "before" and tool_name == "web_search":
        # Query-Logging
        ctx.log_debug(f"Web-Suche: {arguments.get('query', '')}")
        return None  # Keine Änderung an Argumenten
    
    if phase == "after" and tool_name == "terminal":
        # Nur erste 500 Zeichen des Outputs weitergeben
        result["output"] = result.get("output", "")[:500]
        return result
    
    return None
```

**Use Cases:**
- Tool-Usage-Logging / Audit
- Response-Truncation (große Outputs kürzen)
- Argument-Validierung
- Ergebnis-Anreicherung

---

## 4. `plugin.yaml` — Manifest-Format

Jedes Plugin benötigt eine `plugin.yaml` im Plugin-Stammverzeichnis.

### Minimal-Beispiel

```yaml
name: my-plugin
version: 1.0.0
description: "Kurze Beschreibung des Plugins"
author: "Dein Name"
```

### Vollständiges Schema

```yaml
# -- Pflichtfelder -----------------------------------------------------------
name: my-plugin                    # Eindeutiger Plugin-Name (lowercase, hyphens)
version: 1.0.0                    # Semver
description: "Kurze Beschreibung"  # Einzeilige Beschreibung
author: "Dein Name"               # Autor/Organisation

# -- Optionale Felder --------------------------------------------------------
kind: backend                      # plugin-Typ: backend | frontend | service | tool
license: "MIT"                    # SPDX-Lizenz-ID

# -- Hooks (vom Plugin genutzt, deklarativ für den Loader) -------------------
hooks:
  - onReady
  - onMessage
  - onCommand
  - onCronRun
  - onToolCall

# -- Bereitgestellte Provider (optional) -------------------------------------
provides:
  browser_providers:
    - my-browser
  tools:
    - my-custom-tool
  commands:
    - translate

# -- Abhängigkeiten (optional) -----------------------------------------------
requires:
  openamer: ">=0.4.0"             # Mindest-OpenAmer-Version
  python: ">=3.11"                # Python-Version
  plugins:                        # Benötigte andere Plugins
    - memory

# -- Konfigurations-Schema (optional) ----------------------------------------
config:
  schema:
    api_key:
      type: string
      description: "API-Key für externen Dienst"
      secret: true                 # Wert wird in .env erwartet
    timeout:
      type: integer
      default: 30
      description: "Timeout in Sekunden"
    endpoint:
      type: string
      default: "https://api.example.com"
```

### Felder im Detail

| Feld | Typ | Pflicht | Beschreibung |
|------|-----|---------|-------------|
| `name` | string | **Ja** | Eindeutiger Identifier. Wird in Config-Pfaden verwendet: `plugin.<name>.enabled` |
| `version` | string | **Ja** | Semver-konforme Version |
| `description` | string | **Ja** | Kurzbeschreibung (max. 120 Zeichen) |
| `author` | string | **Ja** | Autor oder Organisation |
| `kind` | string | Nein | Typ: `backend`, `frontend`, `service`, `tool` |
| `license` | string | Nein | SPDX-Lizenz-ID (z. B. `MIT`, `Apache-2.0`) |
| `hooks` | list | Nein | Deklarative Hook-Liste (vom Loader geprüft) |
| `provides` | dict | Nein | Vom Plugin bereitgestellte Provider/Tools/Commands |
| `requires` | dict | Nein | Abhängigkeiten zu OpenAmer-Version, Python, anderen Plugins |
| `config.schema` | dict | Nein | JSON-Schema-artige Konfigurationsdeklaration |

---

## 5. `register(ctx)` — Einsprungspunkt

Jedes Plugin muss eine `register(ctx)`-Funktion in **`__init__.py`** exportieren.
Sie ist der **einzige** Einsprungspunkt und wird vom Plugin-Loader aufgerufen.

### Signatur

```python
from typing import Any, Optional

def register(ctx: "PluginContext") -> None:
    """Plugin-Einsprungspunkt.
    
    Wird vom Plugin-Loader nach dem Import aufgerufen.
    Registriere hier deine Hooks.
    
    Args:
        ctx: PluginContext — die Context-API für das Plugin
    """
    pass
```

### Hook-Registrierung in `register()`

```python
def register(ctx) -> None:
    """Registriere alle Hooks des Plugins."""
    
    # onReady: einmalige Initialisierung nach Agent-Start
    @ctx.on_ready
    def on_ready():
        logger.info("Plugin ist bereit")
    
    # onMessage: verarbeite eingehende Nachrichten
    @ctx.on_message
    def on_message(message: str) -> Optional[str]:
        if "!ping" in message:
            return "pong!"
        return None
    
    # onCommand: Slash-Commands
    @ctx.on_command
    def on_command(command: str, args: str) -> Optional[str]:
        if command == "hello":
            return f"Hallo! Args: {args}"
        return None
```

### Direkte Hook-Registrierung (alternative Schreibweise)

```python
def register(ctx) -> None:
    ctx.on_ready(my_ready_handler)
    ctx.on_message(my_message_handler, priority=10)
    ctx.on_command("greet", my_greet_handler)
    ctx.on_cron("daily_report", my_cron_handler)
    ctx.on_tool_call(my_tool_call_handler, tools=["web_search", "terminal"])
```

---

## 6. Context API (ctx)

Der `ctx`-Parameter in `register()` bietet die vollständige Plugin-Schnittstelle.

### Methodenübersicht

| Methode | Beschreibung |
|---------|-------------|
| `ctx.on_ready(handler)` | Registriert `onReady`-Handler |
| `ctx.on_message(handler, priority=0)` | Registriert `onMessage`-Handler (höhere Priority = früherer Aufruf) |
| `ctx.on_command(command, handler)` | Registriert `onCommand`-Handler für `/command` |
| `ctx.on_cron(cron_id, handler)` | Registriert `onCronRun`-Handler für Cron-Job `cron_id` |
| `ctx.on_tool_call(handler, tools=None)` | Registriert `onToolCall`-Handler. `tools=None` = alle Tools |
| `ctx.register_tool(name, handler)` | Stellt ein neues Tool für den Agenten bereit |
| `ctx.register_browser_provider(provider)` | Registriert einen Browser-Provider |
| `ctx.get_config(key, default=None)` | Liest Plugin-Konfiguration aus `config.yaml` |
| `ctx.get_secret(key)` | Liest Secret aus `.env` (Feld mit `secret: true` in `plugin.yaml`) |
| `ctx.send_notification(channel, message)` | Sendet eine Notification (z. B. in die Chat-Oberfläche) |
| `ctx.log_info(msg)` | Loggt auf INFO-Ebene |
| `ctx.log_debug(msg)` | Loggt auf DEBUG-Ebene |
| `ctx.log_error(msg)` | Loggt auf ERROR-Ebene |
| `ctx.store.set(key, value)` | Persistente Schlüssel-Wert-Speicher (Plugin-scoped) |
| `ctx.store.get(key, default=None)` | Liest aus dem Plugin-Speicher |
| `ctx.get_plugin_dir()` | Gibt den absoluten Pfad zum Plugin-Verzeichnis zurück |

### Priority-System für `onMessage`

```python
def register(ctx) -> None:
    # Security-Filter läuft zuerst (priority=100)
    @ctx.on_message(priority=100)
    def security_filter(message):
        if contains_bad_words(message):
            return "[Nachricht blockiert durch Security-Plugin]"
        return None
    
    # Übersetzungs-Plugin läuft später (priority=0)
    @ctx.on_message(priority=0)
    def translator(message):
        if message.startswith("!translate"):
            return translate(message)
        return None
```

---

## 7. Config-Integration

Plugins werden über die OpenAmer-`config.yaml` gesteuert.

### Enable/Disable

```yaml
# config.yaml
plugin:
  hello-world:
    enabled: true      # Plugin ist aktiv
  slash-command:
    enabled: false     # Plugin ist deaktiviert (wird geladen, aber Hooks feuern nicht)
```

### Plugin-spezifische Konfiguration

```yaml
plugin:
  translate:
    enabled: true
    api_key: ""            # Direkter Key (nicht empfohlen — lieber .env)
    timeout: 30
    endpoint: "https://libretranslate.com/translate"
  weather:
    enabled: true
    units: metric          # metric | imperial
    default_city: "Berlin"
```

### Secrets in `.env`

Für sensitive Werte (API-Keys, Tokens) sollte das Plugin das `secret: true`-
Feld in der `plugin.yaml` nutzen. Der User setzt den Wert dann in `.env`:

```bash
# .env
MY_PLUGIN_API_KEY=sk-...
ANOTHER_SECRET=abc123
```

Das Plugin liest Secrets per `ctx.get_secret("api_key")`.

### CLI-Befehl

Plugins können per CLI ein-/ausgeschaltet werden:

```bash
# Plugin aktivieren
openamer config set plugin.hello-world.enabled true

# Plugin deaktivieren
openamer config set plugin.hello-world.enabled false

# Plugin-Konfiguration setzen
openamer config set plugin.weather.units metric

# Config anzeigen
openamer config get plugin.hello-world.enabled
```

Die Config-Integration folgt OpenAmers einheitlichem Konfigurationssystem:

```
config.yaml
├── plugin
│   ├── <plugin-name>
│   │   ├── enabled: true/false
│   │   ├── ... (plugin-spezifische Felder aus config.schema)
│   │   └── ... (vom Plugin definierte Konfiguration)
│   └── ...
├── model
├── memory
└── ...
```

---

## 8. Plugin-Manager

Der Plugin-Manager (`scripts/plugin-manager.py`) ist ein CLI-Tool zur
Verwaltung aller Plugins.

```bash
# Alle Plugins auflisten
python scripts/plugin-manager.py list

# Plugin installieren (aus Pfad)
python scripts/plugin-manager.py install ./desktop-plugins/examples/hello-world

# Plugin deaktivieren
python scripts/plugin-manager.py disable my-plugin

# Plugin aktivieren
python scripts/plugin-manager.py enable my-plugin

# Plugin-Health-Check
python scripts/plugin-manager.py check my-plugin

# Alle Plugins prüfen
python scripts/plugin-manager.py check --all
```

### Ausgabe-Beispiel: `plugin-manager.py list`

```
OpenAmer Plugin-Manager
═══════════════════════════════════════════════════════

Built-in Plugins (plugins/):
  ✓ browser-firecrawl   v1.0.0  enabled   Firecrawl cloud browser
  ✓ browser-browser-use v1.0.0  enabled   Browser Use cloud browser
  ✓ memory              v0.1.0  enabled   Persistent memory system
  ✓ image-gen           v0.1.0  enabled   Image generation

User Plugins (desktop-plugins/):
  ✗ hello-world         v1.0.0  disabled  Mein erstes Plugin
  ✓ slash-command       v1.0.0  enabled   Custom Slash-Commands

═══════════════════════════════════════════════════════
6 Plugins insgesamt | 5 enabled | 1 disabled
```

---

## 9. Best Practices & Pitfalls

### ✅ Best Practices

1. **isoliert bleiben** — Importiere NIEMALS direkte Core-Module
   (z. B. `from openamer_state import ...`). Nutze nur die Context API.
2. **Fehlerbehandlung** — Jeder Hook sollte try/except haben. Ein
   fehlerhafter Hook darf keine anderen Plugins blockieren.
3. **Lazy Initialization** — Teure Resourcen (API-Clients, DB-
   Verbindungen) erst in `onReady` initialisieren, nicht beim Import.
   Nutze `plugin_utils.lazy_singleton` für Thread-Safety.
4. **Kleine Hook-Bodies** — Hooks sollten schnell zurückkehren. Lange
   Operationen gehören in Hintergrund-Threads.
5. **Config vor Magic Values** — Hartcodierte Werte vermeiden; alles
   über `ctx.get_config()` steuerbar machen.
6. **Semver für Manifest** — Version erhöhen bei Breaking Changes im
   Plugin-Verhalten.
7. **Dokumentierte Hooks** — Deklariere genutzte Hooks in der
   `plugin.yaml` unter `hooks`, damit der Loader vorab prüfen kann.

### ⚠️ Typische Pitfalls

| Problem | Lösung |
|---------|--------|
| Plugin blockiert Agent-Start | `onReady` niemals blockierend machen; Hintergrund-Thread für langsame Init nutzen |
| Hook feuert nicht | Prüfen ob `plugin.<name>.enabled: true` in config.yaml |
| Config-Wert wird nicht gefunden | Plugin-Name in `plugin.yaml` mit Config-Pfad vergleichen (beide lowercase, hyphens) |
| Thread-Race beim Singleton | `plugin_utils.lazy_singleton` oder `SingletonSlot` verwenden |
| Plugin-Import-Fehler | `__init__.py` muss `register(ctx)` exportieren; alle Importe in `register()` (lazy) |
| Config-Änderung wirkt nicht | Config wird nur beim Agent-Neustart neu geladen (Runtime-Reload geplant) |
| `onMessage` überschreibt andere Plugins | `return None` wenn keine Änderung; `return str` nur wenn du die Nachricht ersetzen willst |

---

## 10. Beispiel-Plugins

| Plugin | Beschreibung | Ordner |
|--------|-------------|--------|
| **hello-world** | Minimal-Plugin: `onReady` → loggt "Hello World!", `onMessage` → !ping/pong | `desktop-plugins/examples/hello-world/` |
| **slash-command** | Slash-Commands: `/hello`, `/weather` | `desktop-plugins/examples/slash-command/` |

Beide sind vollständig implementiert unter `desktop-plugins/examples/`.

---

## Anhang: Plugin-API-Checkliste für Autoren

- [ ] `plugin.yaml` erstellt mit allen Pflichtfeldern
- [ ] `__init__.py` mit `register(ctx)`-Funktion
- [ ] Hooks in `plugin.yaml` deklariert
- [ ] Config-Schema definiert (falls Konfiguration nötig)
- [ ] Secrets über `secret: true` + `.env` gelöst (falls API-Keys nötig)
- [ ] `plugin.<name>.enabled: true` in `config.yaml` gesetzt
- [ ] Thread-Safety geprüft (`lazy_singleton` für Shared Resources)
- [ ] Fehlerbehandlung in jedem Hook (try/except)
- [ ] Keine direkten Core-Importe
- [ ] Mit `plugin-manager.py check` validiert