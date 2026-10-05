---
name: add-jobs
description: Fetch, format, and add new visa-sponsored/relocation tech jobs to the job board. Use when the user asks to add jobs, fetch jobs, find new listings, update the job board, or mentions new roles to add.
---

# Add Jobs to VisaJobs.xyz

## Project Context

- **Site**: visajobs.xyz — static job board (Eleventy 3.x + Tailwind + Nunjucks)
- **Job data**: `src/_data/jobs.json` — single source of truth, array of job objects
- **Logos**: `media/` directory — company logo images
- **Build copies** `jobs.json` to `_site/db.json` automatically

## Job Object Schema

Every job entry must have ALL these fields:

```json
{
  "company": "Company Name",
  "position": "Job Title (include level + gender notation if applicable)",
  "location": "City, Country FLAG_EMOJI",
  "contract": "Full Time",
  "reloc": "Relocation Assistance",
  "visa": "Visa Sponsorship",
  "post_date": "Month DD, YYYY",
  "logo": "/media/company_logo.jpg",
  "description": "https://careers.company.com/specific-job-url"
}
```

### Field Rules

| Field | Format | Example |
|-------|--------|---------|
| `company` | Exact company name | `"Revolut"` |
| `position` | Full title from listing | `"Senior Backend Engineer (m/f/d)"` |
| `location` | `City, Country EMOJI` | `"Berlin, Germany 🇩🇪"` |
| `contract` | Always `"Full Time"` unless stated otherwise | `"Full Time"` |
| `reloc` | Always `"Relocation Assistance"` | |
| `visa` | Always `"Visa Sponsorship"` | |
| `post_date` | `"Month DD, YYYY"` format | `"March 10, 2026"` |
| `logo` | `/media/filename.jpg` | `"/media/revolut_logo.jpg"` |
| `description` | Direct apply URL or careers page | `"https://www.revolut.com/careers/"` |

## Workflow

### 1. Check existing jobs

```bash
python3 -c "import json; jobs=json.load(open('src/_data/jobs.json')); companies=sorted(set(j['company'] for j in jobs)); print(f'Total: {len(jobs)}'); print('\n'.join(companies))"
```

### 2. Find new jobs

Search these sources for visa-sponsored/relocation jobs NOT already in the board:

- **relocate.me** — curated relocation jobs
- **jaabz.com** — visa sponsorship aggregator
- **Company career pages** — direct listings
- **Greenhouse/Lever job boards** — ATS platforms

Focus on: Europe (Germany, Netherlands, UK, Spain, Denmark, Portugal, Poland, Czech Republic, etc.)

### 3. Download logos

For new companies, download logos to `media/`:

```bash
curl -sL -o media/COMPANY_logo.jpg "https://www.google.com/s2/favicons?domain=COMPANY_DOMAIN&sz=128"
```

Naming convention: `companyname_logo.jpg` (lowercase, underscores).

Check existing logos first: `ls media/`

### 4. Add jobs to jobs.json

- **Prepend** new jobs at the TOP of the array (newest first)
- Validate JSON after editing:

```bash
python3 -c "import json; json.load(open('src/_data/jobs.json')); print('Valid JSON')"
```

### 5. Verify

```bash
python3 -c "import json; jobs=json.load(open('src/_data/jobs.json')); print(f'Total jobs: {len(jobs)}'); print(f'First: {jobs[0][\"company\"]} - {jobs[0][\"position\"]}')"
```

## Common Flag Emojis

🇩🇪 Germany, 🇳🇱 Netherlands, 🇬🇧 United Kingdom, 🇪🇸 Spain, 🇩🇰 Denmark, 🇵🇹 Portugal, 🇵🇱 Poland, 🇨🇿 Czech Republic, 🇦🇹 Austria, 🇮🇪 Ireland, 🇫🇷 France, 🇸🇪 Sweden, 🇫🇮 Finland, 🇧🇪 Belgium, 🇨🇭 Switzerland, 🇮🇹 Italy

## Checklist

- [ ] No duplicate companies+positions already in jobs.json
- [ ] All fields present in every entry
- [ ] Logo file exists in `media/`
- [ ] `description` URL is a valid link (not placeholder)
- [ ] `post_date` uses today's date or the actual posting date
- [ ] JSON validates after editing
