---
name: herald-events
description: Format eventów narracyjnych HERALD — JSON schema, typy efektów, zasady pisania. Aktywuj gdy tworzysz lub edytujesz pliki w data/events/.
---

# HERALD Events — Format i Zasady

## Pełna schema JSON

```json
{
  "id": "blood_work_piotr",
  "title": "Wyniki badań Piotra",
  "motyw": "cialo_w_kosmosie",
  "type": "weighted",
  "weight": 5,
  "act": ["II"],
  "requirements": {
    "flags": [],
    "min_act": "II",
    "crew_state": { "piotr_radiation_msv": "gt:217" }
  },
  "description": "Solomon przynosi wydruk do twojego terminala...",
  "inner_voices": [
    {
      "skill": "PRZETRWANIE",
      "min_value": 5,
      "text": "Przy obecnym tempie przekroczy limit w cyklu 41."
    },
    {
      "skill": "EMPATIA",
      "min_value": 4,
      "text": "Piotr wie. Nie powiedział ci bo nie chciał żebyś decydował za niego."
    }
  ],
  "choices": [
    {
      "id": "change_schedule",
      "text": "Zmień harmonogram — wcześniejszy torpor dla Piotra",
      "is_blue": false,
      "requires_skill": "EMPATIA",
      "min_skill_value": 6,
      "effects": [
        { "type": "flag", "value": "piotr_schedule_adjusted" }
      ]
    },
    {
      "id": "continue",
      "text": "Kontynuuj harmonogram — ryzyko w granicach",
      "effects": [
        { "type": "flag", "value": "piotr_radiation_risk_accepted" }
      ]
    },
    {
      "id": "solomon_protocol",
      "text": "[NIEBIESKI] Solomon projektuje protokół osłony",
      "is_blue": true,
      "requires_skill": "EMPATIA",
      "min_skill_value": 8,
      "min_morale": 60,
      "effects": [
        { "type": "resource", "target": "parts", "delta": -3 },
        { "type": "morale", "target": "piotr", "delta": 5 }
      ]
    }
  ]
}
```

## Typy efektów

| type | target | delta/value |
|---|---|---|
| morale | crew_id | int ± |
| health | crew_id | int ± |
| fatigue | crew_id | int ± |
| resource | oxygen/water/food/fuel/parts | int ± |
| flag | — | string (nazwa flagi) |
| relationship | crew_id | int ± (-2 do +1) |
| voice | skill name | int ± |
| lifedata | — | int ± |

## Zasady narracyjne

1. Tekst precyzyjny, bez patosu dla patosu
2. EMPATIA jest najcichszym głosem — mówi rzeczy Tomasz wie ale wypiera
3. CISZA pojawia się tylko gdy wartość >= 6
4. Blue check = is_blue: true + requires_skill + min_skill_value>=8 + min_morale>=60
5. Nie kończ description pointą — zostaw otwarte
6. Jeden event = jeden ładunek emocjonalny
