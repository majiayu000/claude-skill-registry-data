---
name: ads-parser
description: >-
  Collect and analyze a company's advertising from public ad-transparency libraries — LinkedIn Ad Library, Google Ads Transparency Center, Meta Ad Library — with exact ad texts, run dates, disclosed impressions and links to every ad. Use when someone asks what ads a company runs, how a competitor advertises, or wants a creative teardown from the libraries. Triggers: "what ads does X run", "competitor ads", "ad library", "collect X's creatives".
---

# Ads parser

Collects a company's ads from three transparency libraries through [SearchApi.io](https://www.searchapi.io), plus direct fetches of public LinkedIn Ad Library pages (no login needed).


**Key:** `SEARCHAPI_KEY`, from the environment or `~/.config/marketing-agent-kit/.env`. Setup: `connections/searchapi.md`, or run the `connect` skill.

Engine docs: `https://www.searchapi.io/docs/<engine-name-with-dashes>`. Check an engine's parameters before using it for the first time. Only successful (HTTP 200) requests are billed; new accounts get 100 free requests.

## Workflow

Create `raw/ads/` in the working folder. Save every response as JSON with a meaningful name. Write the analysis from the raw files only — never from memory of what a response said.

### 1. LinkedIn Ad Library — the richest source, with traps

Read `references/linkedin-ad-library.md` **before starting**. It covers the `companyIds` trick, why a name search returns impostors, and when impressions are disclosed. Short version:

```bash
# keyword search — also returns ads BY OTHERS that mention the brand:
python3 ${CLAUDE_SKILL_DIR}/scripts/searchapi.py --engine linkedin_ad_library --out raw/ads/li-q.json q=<company>

# detail page for each ad id you found — public, no login. Save the HTML right away:
curl -s -A "Mozilla/5.0" "https://www.linkedin.com/ad-library/detail/<AD_ID>" -o raw/ads/li-detail-<AD_ID>.html
# or the structured version through SearchApi:
python3 ${CLAUDE_SKILL_DIR}/scripts/searchapi.py --engine linkedin_ad_library_ad_details --out raw/ads/li-ad-<AD_ID>.json ad_id=<AD_ID>
```

### 2. Google Ads Transparency Center

```bash
# find the advertiser id first:
python3 ${CLAUDE_SKILL_DIR}/scripts/searchapi.py --engine google_ads_transparency_center_advertiser_search --out raw/ads/g-adv.json q=<company>
# then the creatives:
python3 ${CLAUDE_SKILL_DIR}/scripts/searchapi.py --engine google_ads_transparency_center --out raw/ads/g-1.json advertiser_id=AR...
```

Creative previews are images that carry the exact ad texts. Save them and transcribe the texts verbatim in the analysis. Link each creative to its page: `https://adstransparency.google.com/advertiser/<ADVERTISER_ID>/creative/<CREATIVE_ID>`.

### 3. Meta Ad Library

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/searchapi.py --engine meta_ad_library --out raw/ads/meta-q.json q=<company>
# find the page id by name, if you don't have it:
python3 ${CLAUDE_SKILL_DIR}/scripts/searchapi.py --engine meta_ad_library_page_search --out raw/ads/meta-pages.json q=<company>
# confirm the page is really theirs before attributing ads (same-name pages are common):
python3 ${CLAUDE_SKILL_DIR}/scripts/searchapi.py --engine meta_ad_library_page_info --out raw/ads/meta-page.json page_id=<ID>
```

Meta sorts by impressions by default, not by date — pass `sort_by` if you need the newest first. Zero ads is a finding, not a failure. State it explicitly — it tells you where the company does *not* look for its audience.

## Reporting rules

- Every ad in the report links to its library page. Every date is labelled ("Ran from … to …").
- Impressions only where the library actually discloses them; otherwise write "the library does not disclose this". LinkedIn discloses impressions, run dates and targeting **only for ads shown in the EU** — outside the EU those fields are simply missing.
- **No budget or spend estimates.** Libraries don't disclose spend for ordinary commercial ads (Meta's spend fields are filled for political and social-issue ads), and third-party dollar estimates (including Ahrefs paid-traffic cost) are unreliable. Quote a spend figure only if the library itself shows it; otherwise say it isn't disclosed.
- No comparisons of ad volume between competitors unless explicitly requested.
- Job ads are a hiring signal, not demand generation — analyse them separately.
- Separate the company's own ads from third-party ads that merely mention the brand. A keyword search returns both; the third-party ones are a separate signal (who compares themselves to the brand, who rides on it).

## Adapt it

- If you track the same competitors every month, keep their LinkedIn `companyIds`, Google advertiser ids and Meta page ids in a small `competitors.json` next to your reports. Lookups are the slow, error-prone part.
- Video ads: libraries give the cover image and text, not the file. If you need what is said in the video, download what the library exposes and transcribe it with Whisper.
