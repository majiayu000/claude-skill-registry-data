---
name: critic-gate
version: 1.0.0
description: >-
  Deterministischer Critic mit hartem Gate — prüft Output-Gate, JSON-Schema, Assertion-Kriterien und vergibt Score. Rückgabe ist strukturiertes JSON für Retry-Entscheidung.
author: Yuno
category: software-development
license: MIT
lane:
  - worker-heavy
  - gate
reasoning_effort: xhigh
agent: Verifier
routing_hint: |
  **Agent-Scope:** Adversarial QA, audits, security scans, gates. Off-scope: building, designing, writing — return to Yuno for re-route.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# Critic-Gate

> **Deterministisches Quality-Gate — keine Bauchgefühle, nur Tatsachen.**
> Inspiriert von DeepEval LLM-as-a-Judge + Azure Agent Design Patterns.

## Prinzip

```

set -euo pipefail
Gate vor Score (DAG-Pattern):
  1. Ist der Output überhaupt bewertbar? (valides JSON? Pflicht-Sektionen da?)
  2. Nur WENN ja → subjektive Bewertung mit Assertions
  ```

So verschwendest du keinen Reasoning-Trace an kaputten Output.

## Strukturierter Input

Der Critic erwartet:

```json
{
  "output": "<Output vom Worker (Code, Text, JSON)>",
  "task_description": "<Was sollte der Output enthalten?>",
  "schema": {
    "type": "code|json|markdown|text",
    "required_sections": ["Error-Handling", "Tests", "README"],
    "language": "python"  // optional, für Syntax-Check
  },
  "assertions": [
    {"id": "err-handling", "text": "Error-Handling für HTTP 404 vorhanden", "critical": true},
    {"id": "tests", "text": "Mindestens ein Smoke-Test", "critical": false}
  ]
}
```

set -euo pipefail
## Strukturiertes Output

```json
{
  "gate_passed": true,
  "schema_valid": true,
  "criteria": [
    {"assertion": "Error-Handling für HTTP 404", "met": true, "evidence": "Zeile 42: try/except block"},
    {"assertion": "Mindestens ein Smoke-Test", "met": false, "fix": "Füge tests/test_basic.py mit assert True hinzu"}
  ],
  "score": 0.83,
  "verdict": "RETRY",   // PASS | RETRY | FAIL
  "feedback_for_worker": "Ergänze handle_retry() gemäß Plan-Schritt 4."
}
```

set -euo pipefail
## Verdikte

| Verdikt | Bedeutung | Aktion |
|---------|-----------|--------|
| **PASS** | Alle criteria met, keine Fixes nötig | Weiter zur Finalizing-Phase |
| **RETRY** | Einige criteria nicht met, aber fixbar | Feedback an Worker, Delta-Retry |
| **FAIL** | Kritische Assertion nicht met oder Schema kaputt | Eskalation an Supervisor |

## Regeln (hart, nicht verhandelbar)

1. **Critical Assertions**: Ein `critical: true` der nicht met ist → sofort FAIL, egal wie gut der Rest ist
2. **Schema-Check**: Wenn `type: code` gesetzt ist, muss es kompilierbaren Code enthalten. `type: json` muss valides JSON sein
3. **Evidence**: Jedes met=true muss Beweis liefern (Zeilennummer, Ausschnitt). Kein "sieht gut aus"
4. **No Hallucination**: Der Critic darf nicht raten. Wenn er den Output nicht analysieren kann → FAIL, nicht "vielleicht OK"
5. **Score**: Nur berechnen wenn gate_passed=true ist. Sonst score=0.0 automatisch

## Toolset

Der Critic läuft lokal über **Ollama** (`deepseek-r1:8b`) via Script (im Skill-Verzeichnis):

```bash
cat input.json | python3 ~/.hermes/skills/software-development/critic-gate/scripts/critic-gate-ollama.py
```

set -euo pipefail
Oder über den globalen Symlink (existiert nach erstmaligem Skill-Load):

```bash
cat input.json | python3 ~/.hermes/scripts/critic-gate-ollama.py
```

set -euo pipefail
Parameter im Script:
- `num_ctx: 16384` (deckelt, Koreaner-Kriterium: "maximaler Kontext besteht nur aus dem, was wirklich nötig ist")
- `temperature: 0.6` (DeepSeek R1 Standard)
- `timeout: 300s` (R1 braucht Zeit für Reasoning-Trace)
- Exit-Code: 0=PASS, 1=RETRY, 2=FAIL

## References

- `scripts/critic-gate-ollama.py` — Das ausführbare Critic-Script (Python, ~130 Zeilen)
- `references/deliverable-adversarial-audit.md` — **Systematische Adversarial-Audit-Methodik** für AI-generierte Deliverables.
  Fünf-Phasen-Checkliste (Surface Scan → Adversarial Probing → Claim Verification → Risk Callouts → Verdict)
  mit reproduzierbaren Edge-Case-Kategorien (Encoding, Numerics, CSV-Struktur, Exit-Codes, Output-Contract)
  **PLUS** Re-Audit-Methodik für Fix-Verifikation + Regression-Hunting nachdem Bugs behoben wurden
  (BOM-Detektion, Duplicate-Header-Silent-Data-Loss, Path-Leakage-in-stderr).
  **Laden, wenn ein Deliverable nicht nur gegen gegebene Assertions bewertet, sondern investigativ auf Lücken
  zwischen Behauptung und Realität geprüft werden soll.** Enthält reale Fehler aus dem csv_summary-Audit
  (5 Bugs, 9/9 Tests bestanden, trotzdem nicht productionsicher).

## Beispiel-Aufruf

```python
# Als Worker: generiere Code
code_output = generate_code(task)

# Als Critic: prüfe Code
critic_input = {
    "output": code_output,
    "task_description": "Baue einen HTTP-Client mit Retry-Logik",
    "schema": {"type": "code", "language": "python", "required_sections": ["Error-Handling"]},
    "assertions": [
        {"id": "retry", "text": "Retry-Logik für Connection-Error vorhanden", "critical": true},
        {"id": "timeout", "text": "Timeout-Parameter konfigurierbar", "critical": false}
    ]
}

# Critic liefert JSON → parse und entscheide
if result["verdict"] == "RETRY":
    worker.retry(task + result["feedback_for_worker"])
elif result["verdict"] == "FAIL":
    supervisor.escalate(task, result)
```

set -euo pipefail
## Integration in multi-agent-work

Im `multi-agent-work` Skill (Phase 5 → Evaluation):
- Nicht "bewerte mal" sagen
- Stattdessen: `critic-gate` mit konkreten Assertions aufrufen
- Resultat ist JSON → deterministisch weiterverarbeitbar
- Feedback_for_worker wird an Worker zurückgegeben (Delta-Retry)

## Optional/Opt-in Mode (Skip-Default)

Das Script unterstützt einen **Skip-Default** über die ENV-Var `HERMES_CRITIC_ENABLED`.
Wenn die Variable nicht gesetzt ist (oder `false`/`0`/`no`/`off`), wird der LLM-Call
**übersprungen** und sofort ein sauberes `SKIPPED`-JSON ausgegeben (Exit 0).
Setze `HERMES_CRITIC_ENABLED=true` (oder `1`/`yes`/`on`), um den echten Critic-Call
zu aktivieren.

**Use case:** Wenn das Hauptmodell ein schnelles lokales Modell ist (z.B. Qwen3.5-9B
auf 8GB VRAM), verdoppelt ein 60-300s R1-Critic-Call die Latenz jeder Aufgabe.
Skip-Modus = sofort, Exit 0, opt-in über ENV wenn man wirklich prüfen will.

**Skip-Output (ENV nicht gesetzt) — v2 ab 2026-06-08:**
```json
{
  "gate_passed": false,
  "schema_valid": true,
  "criteria": [],
  "score": 0.0,
  "verdict": "SKIPPED",
  "feedback_for_worker": "Critic deaktiviert (HERMES_CRITIC_ENABLED nicht gesetzt). Setze die ENV-Var auf 'true' um den Critic zu aktivieren.",
  "_critic_status": "skipped"
}
```

set -euo pipefail
**SEMANTIC FIX (2026-06-08):** `gate_passed` ist im SKIPPED-Modus `false`
(war vorher fälschlich `true`). Hintergrund: Vor dem Fix konnte ein
Worker aus `gate_passed: true` schließen "Code ist geprüft", obwohl KEIN
Check stattfand. Mit `false` ist klar: kein Quality-Gate aktiv gewesen.
Downstream-Consumer MÜSSEN jetzt `verdict` checken, nicht `gate_passed`.

**Erkennungs-Pattern für Downstream-Consumer:**

| `verdict` | `gate_passed` | `_critic_status` | Bedeutung | Aktion |
|-----------|---------------|------------------|-----------|--------|
| `"PASS"`  | `true`        | (fehlt)          | Echter LLM-Call, alle Assertions met | Weiter |
| `"RETRY"` | `false`       | (fehlt)          | Echter LLM-Call, fixbare Mängel | Delta-Retry |
| `"FAIL"`  | `false`       | (fehlt)          | Echter LLM-Call, kritische Mängel | Eskalation |
| `"SKIPPED"` | `false`     | `"skipped"`      | ENV-Var nicht gesetzt, kein Call | **PIPELINE MUSS ENTSCHEIDEN** — kein Default-Pass! |

**Aktivieren (Session-scoped):**
```bash
export HERMES_CRITIC_ENABLED=true
hermes ...     # Critic läuft für diese Session
```

set -euo pipefail
**Aktivieren (persistent, z.B. CI):**
```bash
echo 'export HERMES_CRITIC_ENABLED=true' >> ~/.bashrc
```

**Wichtige Pitfall:** `gate_passed: true` bei SKIPPED heißt **"nicht geprüft"**,
nicht "bestanden". Pipelines die `verdict == "SKIPPED"` nicht explizit
behandeln, schleusen den Output als gültig durch — was bei strict-gate
Workflows zu falschen Positiven führt. Immer `verdict` checken, nicht nur
`gate_passed`.

## Pitfalls

1. **Zu weiche Assertions** → "Code sieht gut aus" ist kein Kriterium. Konkret: "Line 15 enthält try-except"
2. **Zu viele Assertions** → 2-3 pro Task sind genug. Mehr = Noise
3. **Critic ohne Kontext** → Der Critic muss die Aufgabenbeschreibung kennen, sonst bewertet er falsche Kriterien
4. **Nur Score, kein Feedback** → Score allein hilft dem Worker nicht. Die `fix` und `feedback_for_worker` Felder sind der eigentliche Wert
5. **Timeout unterschätzt** → Lokaler R1:8b auf RTX 5060 braucht 30-120s für einfache Fälle, bis zu 300s für komplexe RETRY/FAIL-Analysen. Das Script hat 300s Timeout — nicht auf 60s verkürzen.
6. **Output zu lang** → Der Critic kürzt Output > 8000 Zeichen automatisch. Bei sehr langen Dateien (> 16K Tokens) leidet die Qualität. Vorher mit `output-validator` auf Schlüsselstellen reduzieren.
7. **SKIPPED mit PASS verwechselt** → `verdict == "SKIPPED"` + `_critic_status: "skipped"` ist **kein PASS**. Vor dem C1-Fix (2026-06-08) gab das Script fälschlich `gate_passed: true` zurück — das wurde korrigiert auf `gate_passed: false`. Downstream-Pipelines MÜSSEN `verdict` checken (nicht `gate_passed`) und `_critic_status: "skipped"` explizit behandeln, sonst schleusen sie ungeprüften Output als gültig durch. Die semantisch saubere Aussage ist: SKIPPED bedeutet "kein Gate aktiv", nicht "Gate bestanden".
