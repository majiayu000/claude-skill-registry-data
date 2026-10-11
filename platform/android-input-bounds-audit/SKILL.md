---
name: android-input-bounds-audit
description: "Use when adding a typed input or form field to an Android/Compose app, before shipping a form, when a derived metric (lean mass, BMR) can show a negative or absurd value without crashing, or when a numeric field is only checked for positivity or a text field has no length cap."
---

# Android input bounds audit

Finds the input defects that never crash: a typo reaches derived maths and the
app reports nonsense as fact. Ordered cheapest-first.

## 1. Enumerate every input, don't recall them

```bash
python - <<'PY'
import pathlib, re
for p in sorted(pathlib.Path("app/src/main/kotlin/<pkg>/ui").rglob("*.kt")):
    s = p.read_text(encoding="utf-8")
    for m in re.finditer(r"onValueChange\s*=\s*\{([^}]{0,90})\}", s):
        body = " ".join(m.group(1).split())
        capped = any(k in body for k in ("take(", "coerce", "filter"))
        print(f"{'ok ' if capped else 'RAW'} {p.name}:{s[:m.start()].count(chr(10))+1} {body[:78]}")
PY
```

Also sweep parsing sites: `grep -rn "toDoubleOrNull\|toIntOrNull"`. A field
validated only as `> 0.0` is the headline defect class.

## 2. Compute what the unbounded value does downstream

Do NOT argue from plausibility — run the formula:

```bash
python -c "w=80.0; bf=500.0; lean=w*(1-bf/100); print(lean, 370+21.6*lean)"
# lean mass -320 kg, BMR -6542 kcal  -> shown to the user as a fact
```

If the number is merely large, it may be acceptable. If it is *negative or
NaN*, the field is a defect regardless of how unlikely the typo is.

## 3. Bound it in ONE place

Create a single limits object with wide, defensible ranges and a comment giving
the real-world anchor (tallest human 272 cm, etc.). Wide enough to accept
records, narrow enough to catch a slipped decimal or a unit mix-up.

Wire it at three levels:
- the screen's `enabled =` gate,
- the repository (defence in depth for future callers),
- the **import path** — but *filter* implausible rows rather than `require`,
  because an old archive may carry a typo and losing one row beats losing the
  whole restore.

Never leave the same literal in two files; that duplication is the bug this
object exists to prevent.

## 4. Client caps must equal server CHECK constraints

Pin them with the migration-reading unit test in `wire-name-schema-drift-guard`
(its limits axis, mutation-proved from both sides). Patterns that match the two
constraint shapes:

```kotlin
Regex("""char_length\((?:trim\()?$column\)?\)\s*<=\s*(\d+)""")
Regex("""char_length\(trim\($column\)\)\s*between\s*(\d+)\s*and\s*(\d+)""")
```

## 5. Prove each gate on device

Read `enabled` off the clickable ancestor, never the button's text node, and
drive the case table in both directions — an absurd value must read
**disabled**, and a gate that is always disabled passes a one-sided check — per
`compose-control-tap-verification`.

## 6. Record what you deliberately left unbounded

Steppers (fixed increment per deliberate tap) usually should NOT be capped — a
cap low enough to matter refuses a legitimate heavy lift. Write the reason down
or the next audit re-opens it.
