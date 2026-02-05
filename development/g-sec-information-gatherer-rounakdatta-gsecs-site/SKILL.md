---
name: G-Sec Information Gatherer
description: Scrapes relevant bulletins from the RBI website intelligently and figures out information about government securities issued. Applicable only for India.
---

# G-Sec Information Gatherer

## Instructions
Your source of truth is always the official RBI website Press Releases webpage, but you should access it cleverly as `python3 rbi_scraper.py <year> <month>`. Your monumental task is to figure out what's to be picked and what not to. Remember that every government security has three stages - announcement, intermediate notice of auction and issuance. This is how the bulletin titles look like:
- Announcement: "Auction of Government of India Dated Securities" or "Auction of Government of India Dated Security" (if it is a single one)
- Intermediate notice of auction : "Underwriting Auction for sale of Government Securities for ₹xxx crore on October xx, xxx" (or singular, you get the idea)
- Issuance: "Government Stock - Full Auction Results"

Don't be very rigid with these examples I shared, occasionally there could be certain titles of the bulletins which try to mean the same thing, but might be worded slightly differently. Use your best judgement to figure out what is what. Also, it is SUPER SUPER important to connect dots from around. For example, if you're told to check securities from April, you should proactively check if there were any annoucements in March, which got issued in April. So, you gotta be smart about connecting the dots. Also, always prefer looking at the HTML content instead of PDF, because it's just easier.

And to determine the security code correctly, you should use this formula. For example, "690GS65S25":
  Format breakdown:
  - 690 = Coupon rate (6.90 without decimal)
  - GS = Government Stock
  - 65 = Maturity year last 2 digits (2065 → 65)
  - S = Month indicator (S = September)
  - 25 = Issue year last 2 digits (2025 → 25)

Not just this pattern, for example, this shows up elsewhere as `690GOI65`. Similarly, we have codes like `710GS2029-GS` and so on. So `security_codes` should be an array consisting of all these known patterns (don't invent patterns, these are the three patterns we know so far).

To start with, we are only interested in Central Government issued securities, so please ignore state government securities for now. One more thing to note is that, if it is a fresh issue, then (obviously) the annoucement wouldn't have a yield number, so we gotta look for the subsequent intermediate notice of auction to get the yield. 

So, there'll be an initial backfilling task where we'd go through the long, long history and fetch info of all the government bonds out there. But otherwise, we'll be keeping our data upto date in the data/ directory with auto-incremented files, so you shouldn't have trouble figuring out how fresh our data is, and exactly which checkpoint to start from.

Our goal is to prepare a comprehensive dataset of these securities in clean, structured JSON, say something like this:

```json
{
  "security_name": "Government of India Dated Security XYZ",
  "security_type": "Gilt" or "SDL",
  "announcement_date": "YYYY-MM-DD",
  "auction_date": "YYYY-MM-DD",
  "issuance_date": "YYYY-MM-DD",
  "maturity_date": "YYYY-MM-DD",
  "coupon_rate": float,
  "yield_at_auction": float,
  "amount_issued_crore": float,
  "security_codes": ["unique code if available"] # probably something like 690GS65S25
  "interest_payment_frequency_regex": "semi-annual" # or if you find any other information about interest payment frequency
  "source_urls": [
    "url1",
    "url2",
    ...
  ],
  "additional_info": {
    // any other relevant info you can scrape
  }
}
```

But remember that each security should be in a single JSON file. And it should be like 2025-10_1.json, 2025-10_2.json etc for multiple securities issued in the same month. The `1`, `2` etc is just a serial number to differentiate between multiple securities issued in the same month.

I'm giving you a free hand here, so should you find any updates to any security, you should go ahead and update it. Remember to treat re-issuances as new, because they indeed are.

## CRITICAL: File Writing Rules

**ALL rough work, temporary files, scripts, and intermediate artifacts MUST go to `.tmp/` directory ONLY.**

This includes but is not limited to:
- Python scripts for scraping/parsing (extract_gsec_data.py, pdf_parser.py, fetch_gsecs.py, etc.)
- Status/progress reports (STATUS.md, COMPLETION_REPORT.md, FINAL_SUMMARY.md, etc.)
- Any intermediate processing files
- Downloaded PDFs or HTML files
- Debug outputs

**Absolute paths only:**
- Temporary work files: `/Users/rounak/personal/gsecs.site/.tmp/`
- Final JSON data: `/Users/rounak/personal/gsecs.site/data/`

**ONLY final, production-ready JSON data files** should be written to the `data/` directory in the format: `YYYY-MM_N.json`

**NEVER write ANY files:**
- To the `.claude/` directory - this is reserved for skill definitions only
- To the project root directory - NO scripts, reports, or any files at all

The `.tmp/` directory is already in `.gitignore` and is the correct place for all your working files.

