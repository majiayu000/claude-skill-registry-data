---
name: google-hotels-bladebro
description: Search Google Hotels for live hotel prices, ratings, availability, amenities and provider options using Bladebro. Use for hotel searches, accommodation comparisons, neighborhood comparisons, hotel prices, availability, specific hotels, or where to stay.
allowed-tools: Bash(bladebro:*), Bash(printf*), Bash(echo*)
---

# Google Hotels Search with Bladebro

Use Google Hotels through Bladebro. Prefer deterministic URL construction and Bladebro structured extraction over manually driving every widget.

## Boundaries

- Research and compare only. Do not complete a booking or payment.
- During primary search, stay on Google Hotels.
- After results are presented, you may inspect a hotel's own website or a provider page when the user asks for a direct-price/provider comparison.
- Treat prices and availability as live, time-sensitive observations.

## Session

Use a dedicated session/profile context. Bladebro daemon mode is preferred when available because Chrome state persists across commands.

Before first use in a workflow:

```bash
bladebro daemon >/dev/null 2>&1 || true
```

## Fast path: location + dates

Google Hotels supports a compact URL with a protobuf/base64 `ts` date parameter. Generate it rather than clicking the date picker.

```bash
hotel_ts() {
  local ci_y=$1 ci_m=$2 ci_d=$3 co_y=$4 co_m=$5 co_d=$6 nights=$7
  local cyl=$(printf '%02x' $(( ($ci_y & 0x7f) | 0x80 )))
  local cyh=$(printf '%02x' $(($ci_y >> 7)))
  local col=$(printf '%02x' $(( ($co_y & 0x7f) | 0x80 )))
  local coh=$(printf '%02x' $(($co_y >> 7)))
  echo -n "08011a200a021a00121a12140a0708${cyl}${cyh}10$(printf '%02x' $ci_m)18$(printf '%02x' $ci_d)120708${col}${coh}10$(printf '%02x' $co_m)18$(printf '%02x' $co_d)18$(printf '%02x' $nights)32020801" \
    | xxd -r -p | base64 | tr -d '\n='
}
```

Constraints: use this helper for years 2025–2030 and stays of 1–127 nights. If outside that range or if Google changes behavior, use the interactive fallback.

Build:

```text
https://www.google.com/travel/search?q={URL_ENCODED_QUERY}&qs=CAE4AA&ts={TS_PARAM}&ap=MAE
```

Examples of query intent:

- `Hotels in Hell's Kitchen New York`
- `Hotels near Eiffel Tower Paris`
- `Hotel Hendricks New York`

Navigate and inspect:

```bash
bladebro nav "$URL"
bladebro see extract auto --json
```

If extraction is incomplete:

```bash
bladebro see content --json
bladebro see model --json
```

Use `bladebro act collect max=40 timeout=30 --json` when the result list uses incremental/infinite loading.

## Filters

When the user specifies stars, price, amenities, free cancellation, guest/room counts, or another filter that is not encoded in the URL:

1. `bladebro see model --json`
2. Identify controls by accessible label/text, not brittle CSS selectors.
3. Use `bladebro act click text="..."`, `bladebro act fill ...`, or one batched call.
4. Prefer `bladebro act batch` / `bladebro run` for multi-step filters.
5. Read the returned delta; do not reflexively request a full page snapshot after every action.

Bladebro refs are designed to survive many re-renders; if a ref heals automatically, continue normally.

## Result extraction

For each useful hotel capture when available:

- Hotel name
- star class
- guest rating + review count
- price/night
- total stay price
- currency
- provider/source
- neighborhood/location cue
- key amenities
- cancellation/breakfast notes when visible

Do not infer missing fields.

## Specific-hotel drill-down

When the user wants one hotel:

1. Search exact hotel name + city + dates.
2. Open its result/detail panel.
3. Extract available room/provider prices.
4. Distinguish taxes/fees included vs excluded when Google shows that distinction.
5. If asked, compare with the hotel's direct website in a separate tab.

## Output

Default to 5–8 high-signal options, sorted according to the user's stated priorities. Use a compact table:

| Hotel | Rating | Price/night | Total | Why it fits |
|---|---:|---:|---:|---|

Then give one recommendation and the main tradeoff.

## Recovery

- Consent: follow the configured Bladebro consent policy; otherwise dismiss the banner.
- CAPTCHA/bot challenge: do not solve or bypass. Report the block.
- `View prices`: dates likely failed; verify the URL/date state.
- Wrong currency: note the displayed currency; do not silently convert unless requested.
- Map instead of list: switch to list view by visible text.
- Empty extraction: use `see content`, then `see model`, then interact explicitly.
