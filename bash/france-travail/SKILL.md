---
name: france-travail
description: "Search France Travail (ex-Pole Emploi) job postings to detect hiring signals. Companies recruiting for DevSecOps, RGPD, or cybersecurity roles are hot consulting prospects. Use when the user asks about job market signals or wants to find companies hiring in specific tech domains."
metadata: { "openclaw": { "emoji": "\uD83D\uDCBC", "requires": { "bins": ["python3"] } } }
user-invocable: true
---

# france-travail

Search France Travail job postings to detect hiring signals.

## Triggers

- `/emploi DevSecOps Toulouse`
- `/emploi RGPD 31`
- "qui recrute en cybersecurite dans le 31?"
- "offres DevSecOps a Toulouse"
- "signaux de recrutement IT Occitanie"

## How it works

Queries the France Travail Partner API (Offres d'emploi v2). Requires OAuth2 authentication with client credentials.

1. Obtains an access token from `https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire`
2. Searches job postings via `https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search`

**Graceful degradation:** If credentials are not set, the script outputs a clear error message with setup instructions instead of crashing.

## Usage

```bash
python3 {baseDir}/scripts/ft.py --query "DevSecOps" --department 31 --format json
python3 {baseDir}/scripts/ft.py --query "RGPD DPO" --format text
python3 {baseDir}/scripts/ft.py --query "cybersecurite" --department 75 --per-page 25 --format json
```

## Arguments

| Argument       | Required | Default | Description                                  |
|----------------|----------|---------|----------------------------------------------|
| `--query`      | yes      |         | Job title, skill, or keyword to search        |
| `--department`  | no       |         | Department code (e.g. 31, 75)                 |
| `--commune`    | no       |         | INSEE commune code for precise location        |
| `--per-page`   | no       | 15      | Number of results (1-150)                      |
| `--format`     | no       | json    | Output format: `json` or `text`                |

## Output fields

- `company` — hiring company name
- `position` — job title
- `location` — city and department
- `contract_type` — CDI, CDD, freelance, etc.
- `salary` — salary range if available
- `date` — posting date
- `url` — link to the full job posting
- `prospect_signal` — "HOT" for DevSecOps/RGPD/cyber roles

## Environment variables

| Variable                       | Required | Description                          |
|--------------------------------|----------|--------------------------------------|
| `FRANCE_TRAVAIL_CLIENT_ID`     | yes      | OAuth2 client ID from France Travail |
| `FRANCE_TRAVAIL_CLIENT_SECRET` | yes      | OAuth2 client secret                 |

Get credentials at: https://francetravail.io/data/api/offres-emploi
