---
name: fb-finder
description: >
  Find the next batch of Facebook Business Page URLs for HVAC/local service leads using Serper.dev.
  Trigger this skill when the user says "podaj mi 30 linkow", "nastepna partia leadow", "znajdz kolejne linki FB",
  "podaj kolejne 30", "kolejna partia", "/fb-finder", or any variant asking for the next batch of Facebook leads.
allowed-tools: Bash
---

## What this skill does

Runs the Serper.dev scraper to find 30 clean Facebook Business Page URLs from the HVAC leads list,
then presents them in blocks of 10 ready to paste into "Open Multiple URLs" or any tab opener.

## Execution steps

### Step 1: Run the scraper

```bash
cd /workspaces/ZeroKlik && python3 run_fb_finder_serper.py
```

The script:
- Reads `hvac_leads_final.csv` (7,775 HVAC leads)
- Skips firms already in `fb-dm-done.txt`
- Searches Serper.dev Google for each firm's Facebook page
- Filters: 15-50 reviews, 4.5+ rating, no bad URLs
- Loops until 30 clean FB profile URLs found
- Saves all results to `fb-dm-results.csv` and progress to `fb-dm-done.txt`

Wait for it to finish -- takes 5-10 minutes.

### Step 2: Read results

After the script finishes, read the last 40 rows of `fb-dm-results.csv` and extract rows with `status=found` from the latest batch.

### Step 3: Flag suspicious URLs

Before presenting, flag these as suspicious (exclude from main list, note separately):
- Numeric-only paths: `facebook.com/100071691850608/` -- no business name in URL
- Personal profile pattern: `facebook.com/firstname.lastname/` -- e.g. `pete.murad`, `les.levy.1`
- Page name clearly mismatches lead name (e.g. "Kings Corner Entertainment" for "All Season Air")
- URL contains `/photo.php`, `/photos/`, `/posts/`, `/videos/`

`/p/Business-Name-123456/` style URLs are OK.

### Step 4: Present results

Present clean URLs exactly as plain text, one URL per line, with absolutely NO numbers, no bullet points, and no extra characters before the URLs. 
Insert a blank line after every 10th URL to create distinct blocks. Do NOT use code blocks (` ``` `).

Format exactly like this:
https://www.facebook.com/example1/
https://www.facebook.com/example2/
... (up to 10)
https://www.facebook.com/example10/

https://www.facebook.com/example11/
... (up to 20)
https://www.facebook.com/example20/

https://www.facebook.com/example21/
...

Then summary line at the very bottom:
> Znaleziono X czystych linkow. Pominieto Y podejrzanych (powod). Przetworzono Z firm lacznie.

Flagged ones listed separately at bottom: business name + reason.
