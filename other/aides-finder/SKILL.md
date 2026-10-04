---
name: aides-finder
description: "Find eligible subsidies, grants, and calls for projects matching a given topic and territory. Use when the user asks about available funding, subventions, or financial aid for a project, especially for associations and ESS structures."
metadata: { "openclaw": { "emoji": "\uD83D\uDCB0", "requires": { "bins": ["python3"] } } }
user-invocable: true
---

# aides-finder

Find subsidies, grants, and calls for projects from public funders.

## Triggers

- `/aides cybersecurite Occitanie`
- `/aides audit digital association`
- "quelles subventions pour un audit digital?"
- "appels a projets ESS 2026"
- "aides pour cybersecurite en Occitanie"

## How it works

Queries two complementary sources:

1. **Aides-Territoires API** (beta.gouv.fr, no auth) — the national database of public aids. Covers state, regional, departmental, and EU funding.
2. **Calendrier-Subvention API** (local instance, `SUBVENTION_API_BASE` env var) — internal calendar of tracked funding opportunities. Falls back gracefully if unavailable.

## Usage

```bash
python3 {baseDir}/scripts/aides.py --query "cybersecurite" --territory "Occitanie" --format json
python3 {baseDir}/scripts/aides.py --query "audit digital" --audience association --format text
python3 {baseDir}/scripts/aides.py --query "transition numerique" --department 31 --format json
```

## Arguments

| Argument       | Required | Default      | Description                                        |
|----------------|----------|--------------|----------------------------------------------------|
| `--query`      | yes      |              | Keywords describing the project or sector           |
| `--territory`  | no       |              | Region name (e.g. Occitanie, Ile-de-France)         |
| `--department`  | no       |              | Department code (e.g. 31, 75)                       |
| `--audience`   | no       | association  | Target audience: association, commune, epci, entreprise |
| `--call-only`  | no       | false        | Only show active calls for projects                  |
| `--per-page`   | no       | 20           | Number of results (1-100)                            |
| `--format`     | no       | json         | Output format: `json` or `text`                      |

## Output fields

- `name` — aid title
- `funder` — funding organization
- `amount` — funding range or amount
- `deadline` — application deadline (null if rolling)
- `eligibility` — who can apply
- `description` — short summary
- `url` — link to the full aid page
- `is_call_for_project` — whether this is an active call

## Environment variables

| Variable              | Required | Default                          | Description                        |
|-----------------------|----------|----------------------------------|------------------------------------|
| `SUBVENTION_API_BASE` | no       | `http://host.docker.internal:3000` | Base URL for calendrier-subvention |
