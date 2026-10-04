---
name: output-validator
version: 1.0.0
description: >-
  Pre-Flight Scheck für jeden Output — validiert JSON, Markdown, Python-Syntax und Pflicht-Sektionen BEVOR der Output an den nächsten Schritt weitergegeben wird. Verhindert, dass malformierter Output in den Critic oder Handoff wandert.
author: Yuno
category: software-development
license: MIT
lane:
  - worker-flash
  - gate
reasoning_effort: high
agent: Verifier
routing_hint: |
  **Agent-Scope:** Adversarial QA, audits, security scans, gates. Off-scope: building, designing, writing — return to Yuno for re-route.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# Output-Validator

> **Schema-Check vor Handoff — keine Überraschungen im nächsten Schritt.**
> Inspiriert von Claude Agent SDK Structured Outputs.

## Prinzip

```
Output vom Worker → Validator → [PASS] → Critic/Handoff
                              → [FAIL] → Sofort-Fix oder Retry
```

Der Validator prüft **SURFACE**, nicht **SEMANTIK**:
- Syntax (ist das JSON valide?)
- Struktur (sind alle Pflicht-Felder da?)
- Typ (ist es Code, Markdown, JSON?)

Semantische Prüfung ("Macht der Code Sinn?") ist Aufgabe des Critic-Gates.

## Validierungs-Typen

### JSON-Validator
```python
validator.check_json(output, schema={
    "required_keys": ["name", "version", "data"],
    "types": {"version": "string", "data": "list"}
})
# → {"valid": false, "error": "Key 'version' fehlt"}
```

### Markdown-Validator
```python
validator.check_markdown(output, required_sections=[
    "# Überschrift",
    "## Setup",
    "## Usage"
])
# → {"valid": true, "missing_sections": []}
```

### Python-Code-Validator
```python
validator.check_python(output, requirements=[
    "def main",              # Funktion muss existieren
    "if __name__",           # Guard-Klausel
    "try:"                   # Error-Handling
])
# → {"valid": false, "missing": ["try:"], "syntax_error": None}
```

### Generic-Validator
```python
validator.check(output, format="text", min_length=100)
# → {"valid": true, "length": 450}
```

## Return-Wert (immer strukturiert)

```json
{
  "valid": false,
  "stage": "validator",           // validator | critic | handoff
  "format": "json",               // json | markdown | python | text
  "errors": [
    {"type": "missing_key", "field": "version", "severity": "critical"},
    {"type": "syntax_error", "line": 15, "severity": "fatal"}
  ],
  "fixes": [
    "Füge key 'version' hinzu",
    "Fixe Syntax-Fehler in Zeile 15"
  ],
  "retry_allowed": true,          // false bei fatalen Fehlern
  "summary": "2 Fehler gefunden, 2 fixbar"
}
```

## Severity-Levels

| Level | Bedeutung | Aktion |
|-------|-----------|--------|
| **fatal** | Kaputte Syntax, kompiliert nicht | Sofort-Retry, Worker bekommt konkrete Fehler |
| **critical** | Pflicht-Element fehlt | Retry, Worker bekommt Fehlerliste |
| **warning** | Stilistisch suboptimal | Weiter an Critic, aber mit Note |

## Integration in den Workflow

### Position im Pipeline

```
Research/Implementation →
  Worker-Output →
    [OUTPUT-VALIDATOR] →
      (PASS) → [CRITIC-GATE] → (PASS) → Handoff/Final
      (FAIL) → Delta-Feedback → Worker (Retry)
```

### Beispiel: multi-agent-work Phase 4

```python
# Worker liefert Code
code = worker.generate_code(task)

# Validator prüft Syntax + Struktur
v_result = validator.check_python(code, required=["def ", "try:"])
if not v_result["valid"]:
    worker.retry(task, feedback=v_result["fixes"])
    return  # Nicht weitermachen!

# Erst DANN an Critic
c_result = critic.evaluate(code, assertions=[...])
```

### Beispiel: RAG-Pipeline (nach JSON-Extraktion)

```python
# Worker extrahiert aus Dokument
json_output = worker.extract_structured_data(doc)

# Validator prüft JSON
check = validator.check_json(json_output, required_keys=["title", "content"])
if not check["valid"]:
    # Sofort re-extrahieren mit anderem Prompt
    json_output = worker.extract_with_schema(doc, schema=...)
```

## Kriterien pro Format

### Für Code (Python)
- Syntax valide (ast.parse)
- Alle import-Statements auflösbar
- Keine unbenutzten Variablen (optional)
- Guard-Klausel vorhanden (if __name__ == "__main__")
- Mindestens ein try/except oder Error-Handling

### Für JSON
- Valides JSON (json.loads ohne Fehler)
- Alle required_keys vorhanden
- Typen stimmen (string, list, dict, int, bool)
- Keine null-Werte für required Felder

### Für Markdown (Doku)
- H1-Überschrift vorhanden
- Alle required_sections als H2/H3
- Keine broken Links (optional, per regex)
- Mindestens 200 Zeichen

## Pitfalls

1. **Validator wird übersprungen** → "Der Critic findet es schon" → NEIN. Validator ist schnell, Critic ist langsam
2. **Zu strenge Regeln** → Warning als fatal behandeln → Worker wird frustriert
3. **Kein Schema-Update** → Wenn das Format ändert, muss der Validator mitgepatched werden
4. **Validator prüft Semantik** → NEIN. Der Validator prüft SYNTAX. Semantik ist Critic-Gate
5. **Validator läuft einmal und gut** → Für autonome Systeme (>5 min runtime, live state mutation) reicht ein einzelner Validator-Lauf NICHT. **Dry-Run-Validation-Loop VOR Live-Execute ist Pflicht** (siehe `references/dry-run-before-live-execute.md`). Beim GreyHack-Mission-Orchestrator-Bau (2026-07-06) fanden 30 Sek Dry-Run 5 echte Bugs (YAML-Parse-Error, Section-Header-Matching mit Emoji, OCR-Priorisierung, State-File-Pfad-Mismatch, Frontmatter-Überschreibung). Ohne Dry-Run hätten diese Bugs 60+ Min Live-Run korrumpiert.

## Further Reading

- **`references/dry-run-before-live-execute.md`** — Pflicht-8-Stufen-Dry-Run-Checkliste für autonome Systeme (Computer-Use, Cron-Deployments, Multi-Agent-Swarms). Inkl. der 5 realen Bugs aus dem GreyHack-Orchestrator-Bau als warnende Beispiele. **Laden, sobald du ein System baust, das autonom läuft oder Live-State mutiert.**
- **`references/preflight-check-mission-readiness.md`** — Pflicht-Environment-Readiness-Check (Binaries, Credentials, Paths, Window-Detection, Services). 10-Punkte-Standard-Checklist, 3-Tier-Severity-Modell (CRITICAL/OPTIONAL/INFO), 3 Output-Modi (Human/Verbose/JSON), CI/CD-freundliche Exit-Codes (0=GO, 1=CONDITIONAL, 2=NO-GO). **Laden, BEVOR du ein Dry-Run startest — Pre-Flight ist die Vorstufe zum Dry-Run und validiert das Environment, nicht die Script-Logik.**

## Shared Library

Der Output-Validator und das Critic-Gate sind zwei Anwendungen derselben Idee:

```
Validator   → Oberfläche (Syntax, Struktur, Schema)
Critic      → Tiefe (Semantik, Korrektheit, Qualität)
```

Beide nutzen dieselben Assertion-Patterns. Der Validator filtert schnell, der Critic prüft sorgfältig.

## Implementierung

```python
# Pseudocode für den Validator
import json, ast

class OutputValidator:
    def check(self, output, format, schema=None):
        if format == "json":
            return self._check_json(output, schema)
        elif format == "python":
            return self._check_python(output, schema)
        elif format == "markdown":
            return self._check_markdown(output, schema)
        else:
            return self._check_text(output, schema)

    def _check_python(self, code, schema):
        errors = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append({"type": "syntax", "line": e.lineno, "severity": "fatal"})

        for req in schema.get("required", []):
            if req not in code:
                errors.append({"type": "missing", "field": req, "severity": "critical"})

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "fixes": [e["field"] for e in errors if e["type"] == "missing"],
            "retry_allowed": all(e["severity"] != "fatal" for e in errors)
        }
```
