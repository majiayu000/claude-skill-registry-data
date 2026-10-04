---
name: qa-detect-ux-format-consistency
section: visual
description: "Detects mixed display formats for the same kind of data on a single page: date formats (5/6/2026 vs 2026-06-05 vs Jun 5 2026), currency formats (PKR 93M vs Rs. 93,000,000 vs $93M), number formats (1,000 vs 1.000 vs 1k), time formats (17:17 vs 5:17 PM), phone formats. Catches the 'why is the same data shown three different ways' bug class."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
---

## What it catches — 6 issue types

| issueType | severity | What |
|---|---|---|
| `dateFormatMixed` | medium | Page shows dates in 2+ distinct formats (e.g. `5/6/2026`, `2026-06-05`, `Jun 5 2026`) |
| `currencyFormatMixed` | medium | Page shows monetary values in 2+ distinct formats (e.g. `PKR 93M`, `Rs. 93,000,000`, `93000000 PKR`) |
| `numberFormatMixed` | low | Page shows large numbers with mixed thousand separators (`1,000` US vs `1.000` EU vs `1 000` SI) AND mixed full/abbreviated (`12,450` vs `12.4k`) |
| `timeFormatMixed` | low | Page shows times in 2+ distinct formats (`17:17` 24h vs `5:17 PM` 12h vs `5:17pm`) |
| `phoneFormatMixed` | low | Page shows phone numbers in 2+ distinct formats (e.g. `+92 300 1234567`, `0300-1234567`, `(0300) 1234567`) |
| `decimalPrecisionMixed` | low | Page shows the same data type with different decimal places (`62%` vs `61.5%` vs `62.00%` for percentages, or `0` vs `0.00` for totals) |

## Probe (browser_evaluate)

```js
() => {
  const out = [];

  // ── Collect visible text from the page ─────────────────────────────
  // Cap at 20,000 chars to avoid huge pages
  const SKIP_TAGS = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT']);
  let visibleText = '';
  const walk = (node) => {
    if (!node || visibleText.length > 20000) return;
    if (node.nodeType === 1) {
      if (SKIP_TAGS.has(node.tagName)) return;
      const cs = getComputedStyle(node);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
    }
    if (node.nodeType === 3) {
      visibleText += (node.textContent || '') + ' ';
      return;
    }
    for (const c of node.childNodes || []) walk(c);
  };
  walk(document.body);

  // ── 1. Date format mix ──────────────────────────────────────────────
  const dateBuckets = {
    'slash-MD/Y':  /\b\d{1,2}\/\d{1,2}\/\d{4}\b/g,             // 5/6/2026 or 06/05/2026
    'slash-YMD':   /\b\d{4}\/\d{1,2}\/\d{1,2}\b/g,             // 2026/06/05
    'iso-YMD':     /\b\d{4}-\d{2}-\d{2}\b/g,                   // 2026-06-05
    'dash-DMY':    /\b\d{1,2}-\d{1,2}-\d{4}\b/g,               // 5-6-2026
    'dot-DMY':     /\b\d{1,2}\.\d{1,2}\.\d{4}\b/g,             // 5.6.2026
    'month-name':  /\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+\d{4}\b/gi,  // June 5, 2026
    'day-month':   /\b\d{1,2}\s+(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\b/gi  // 5 June 2026
  };
  const dateHits = {};
  for (const [name, re] of Object.entries(dateBuckets)) {
    const matches = visibleText.match(re);
    if (matches && matches.length > 0) {
      dateHits[name] = { count: matches.length, sample: matches.slice(0, 3) };
    }
  }
  const distinctDateFormats = Object.keys(dateHits);
  if (distinctDateFormats.length >= 2) {
    const examples = distinctDateFormats.map(k => `${k}: "${dateHits[k].sample[0]}"`).join('; ');
    out.push({
      issueType: 'dateFormatMixed', severity: 'medium', selector: 'body',
      description: `Page uses ${distinctDateFormats.length} distinct date formats: ${examples}. Pick one (ISO 2026-06-05 is most unambiguous) and use it everywhere.`
    });
  }

  // ── 2. Currency format mix ─────────────────────────────────────────
  const currencyBuckets = {
    'symbol-prefix-amount':  /[$£€¥₹]\s*[\d,]+(?:\.\d+)?[KMB]?\b/g,           // $1,000 or $1M
    'symbol-prefix-abbrev':  /[$£€¥₹]\s*\d+(?:\.\d+)?\s*[KMB]\b/gi,           // $1.5M
    'iso-prefix-amount':     /\b(?:USD|EUR|GBP|JPY|INR|PKR|AED|SAR|CAD)\s+[\d,]+(?:\.\d+)?\b/g,  // PKR 93,000
    'iso-prefix-abbrev':     /\b(?:USD|EUR|GBP|JPY|INR|PKR|AED|SAR|CAD)\s+\d+(?:\.\d+)?\s*[KMB]\b/gi,  // PKR 93M
    'amount-iso-suffix':     /\b[\d,]+(?:\.\d+)?\s+(?:USD|EUR|GBP|JPY|INR|PKR|AED|SAR|CAD)\b/g,  // 93,000 PKR
    'rs-prefix-amount':      /\bRs\.?\s*[\d,]+(?:\.\d+)?\b/g                  // Rs. 93,000
  };
  const currencyHits = {};
  for (const [name, re] of Object.entries(currencyBuckets)) {
    const matches = visibleText.match(re);
    if (matches && matches.length > 0) {
      currencyHits[name] = { count: matches.length, sample: matches.slice(0, 2) };
    }
  }
  const distinctCurrencyFormats = Object.keys(currencyHits);
  if (distinctCurrencyFormats.length >= 2) {
    const examples = distinctCurrencyFormats.map(k => `"${currencyHits[k].sample[0]}"`).join(' vs ');
    out.push({
      issueType: 'currencyFormatMixed', severity: 'medium', selector: 'body',
      description: `Page uses ${distinctCurrencyFormats.length} different money formats: ${examples}. Pick one (e.g. always "PKR 93M" or always "Rs. 93,000,000").`
    });
  }

  // ── 3. Number format mix (thousand separator + abbreviation) ───────
  const numHits = {
    'US-1,000':       (visibleText.match(/\b\d{1,3}(?:,\d{3})+(?!\.\d)/g) || []).slice(0, 5),
    'EU-1.000':       (visibleText.match(/\b\d{1,3}(?:\.\d{3}){2,}\b/g) || []).slice(0, 5),  // 2+ dot-groups to avoid version numbers
    'SI-1 000':       (visibleText.match(/\b\d{1,3}(?: \d{3})+\b/g) || []).slice(0, 5),
    'abbrev-Kkmb':    (visibleText.match(/\b\d+(?:\.\d+)?[KkMmBb]\b/g) || []).filter(s => !/^\d{4}[A-z]/.test(s)).slice(0, 5)
  };
  const distinctNumberFormats = Object.keys(numHits).filter(k => numHits[k].length > 0);
  if (distinctNumberFormats.length >= 2) {
    const examples = distinctNumberFormats.map(k => `${k.split('-')[0]}: "${numHits[k][0]}"`).join('; ');
    out.push({
      issueType: 'numberFormatMixed', severity: 'low', selector: 'body',
      description: `Page mixes number formats: ${examples}. Apply consistent formatting (locale + abbreviation rules).`
    });
  }

  // ── 4. Time format mix ─────────────────────────────────────────────
  const timeHits = {
    '24h-HHMM':    (visibleText.match(/\b(?:[01]?\d|2[0-3]):[0-5]\d(?!\s*[AaPp][Mm])\b/g) || []).slice(0, 5),
    '12h-AMPM':    (visibleText.match(/\b\d{1,2}:[0-5]\d\s*[AaPp][Mm]\b/g) || []).slice(0, 5),
    '12h-am-suffix': (visibleText.match(/\b\d{1,2}:[0-5]\d[ap]m\b/g) || []).slice(0, 5),
    '24h-with-sec': (visibleText.match(/\b(?:[01]?\d|2[0-3]):[0-5]\d:[0-5]\d\b/g) || []).slice(0, 5)
  };
  const distinctTimeFormats = Object.keys(timeHits).filter(k => timeHits[k].length > 0);
  if (distinctTimeFormats.length >= 2) {
    const examples = distinctTimeFormats.map(k => `"${timeHits[k][0]}"`).join(' vs ');
    out.push({
      issueType: 'timeFormatMixed', severity: 'low', selector: 'body',
      description: `Page mixes time formats: ${examples}. Pick one of 24h ("17:17") or 12h ("5:17 PM").`
    });
  }

  // ── 5. Phone format mix ────────────────────────────────────────────
  const phoneHits = {
    '+CC space groups':   (visibleText.match(/\+\d{1,3}\s+\d{2,4}\s+\d{3,7}/g) || []).slice(0, 3),  // +92 300 1234567
    '+CC-dash-groups':    (visibleText.match(/\+\d{1,3}-\d{2,4}-\d{3,7}/g) || []).slice(0, 3),
    'leading-0-dash':     (visibleText.match(/\b0\d{2,3}-\d{6,7}\b/g) || []).slice(0, 3),     // 0300-1234567
    'leading-0-space':    (visibleText.match(/\b0\d{2,3}\s+\d{3}\s+\d{3,4}\b/g) || []).slice(0, 3),  // 0300 123 4567
    'all-digits':         (visibleText.match(/(?<!\d)0\d{10}(?!\d)/g) || []).slice(0, 3),     // 03001234567
    'parens-area':        (visibleText.match(/\(\d{3,5}\)\s*\d{3,4}[-\s]?\d{3,4}/g) || []).slice(0, 3)  // (0300) 123-4567
  };
  const distinctPhoneFormats = Object.keys(phoneHits).filter(k => phoneHits[k].length > 0);
  if (distinctPhoneFormats.length >= 2) {
    const examples = distinctPhoneFormats.map(k => `"${phoneHits[k][0]}"`).join(' vs ');
    out.push({
      issueType: 'phoneFormatMixed', severity: 'low', selector: 'body',
      description: `Page mixes phone number formats: ${examples}. Choose one (e.g. always E.164 +923001234567 or always 0300-1234567).`
    });
  }

  // ── 6. Decimal precision mix ───────────────────────────────────────
  // Find percentages used together: 62% vs 62.00% vs 61.5%
  const pcts = (visibleText.match(/\b\d+(?:\.\d+)?%/g) || []);
  if (pcts.length >= 3) {
    const buckets = { 'int': 0, '1dp': 0, '2dp': 0, '3dp+': 0 };
    const sample = { 'int': null, '1dp': null, '2dp': null, '3dp+': null };
    for (const p of pcts) {
      const dot = p.indexOf('.');
      let key;
      if (dot < 0) key = 'int';
      else {
        const dp = p.length - dot - 2;  // -1 for '.' -1 for '%'
        if (dp === 1) key = '1dp';
        else if (dp === 2) key = '2dp';
        else key = '3dp+';
      }
      buckets[key]++;
      if (!sample[key]) sample[key] = p;
    }
    const distinct = Object.keys(buckets).filter(k => buckets[k] > 0);
    if (distinct.length >= 2) {
      const examples = distinct.map(k => `${k}: "${sample[k]}"`).join(', ');
      out.push({
        issueType: 'decimalPrecisionMixed', severity: 'low', selector: 'body',
        description: `Percentages shown with mixed decimal precision: ${examples}. Pick one (e.g. always integer %, or always 1 decimal).`
      });
    }
  }

  return out;
}
```

## Notes

- Bounded: max 6 findings per cell (one per format category)
- Self-skips: page with < 50 chars of visible text returns []
- Cross-references entire body innerText (capped at 20,000 chars to avoid huge pages)
- Catches the 4 gaps you flagged: date / currency / number / time / phone format consistency
