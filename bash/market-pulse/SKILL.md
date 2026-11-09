---
name: market-pulse
description: |
  Daily Indian market brief and regime check: pre-market (GIFT Nifty, global cues, crude, USD/INR,
  US yields), previous session's FII/DII cash flows and F&O participant positioning, India VIX,
  NIFTY/BANKNIFTY levels, sector rotation via NSE sectoral indices, breadth, F&O ban list, results
  and macro calendar (RBI MPC, CPI, Budget, US Fed), and post-market wrap.

  Use when the user asks: "how is the market today", "pre-market report", "what's GIFT Nifty saying",
  "FII DII data", "market breadth", "which sectors are strong", "is it a good time to buy", "end of
  day summary", or wants context before individual stock analysis.
---

# Market Pulse (India)

Market context decides most stock outcomes: on big index days, most large caps move with NIFTY. Build the brief from verifiable data with timestamps. Never fill gaps with plausible-sounding
numbers.

## When and what

| Time (IST) | Brief | Key inputs |
|---|---|---|
| 07:30–09:00 | **Pre-market** | GIFT Nifty vs NIFTY's previous close, US close (S&P 500, Nasdaq), Asia open (Nikkei, Hang Seng, Kospi), Brent, USD/INR, US 10Y, DXY, overnight news, results today, F&O ban list |
| 09:00–09:15 | Pre-open | NIFTY pre-open equilibrium price, gap size, gap-up/down breadth |
| Intraday | Pulse check | NIFTY/BANKNIFTY vs key levels, VIX change, sector heatmap, advance/decline, OI shifts at the nearest expiry |
| After 18:00 | **Post-market wrap** | Close, breadth, sector winners/losers, FII/DII provisional cash data, participant-wise F&O OI, bulk/block deals, tomorrow's events |

## Data sources (prefer the first that works)

1. **Broker MCP** for index quotes and candles (NIFTY 50, NIFTY BANK, INDIA VIX and sector indices).
2. **ta.py** with yfinance: `NIFTY`, `BANKNIFTY`, `SENSEX`, `INDIAVIX`, `NIFTYIT`, `NIFTYAUTO`,
   `NIFTYPHARMA`, `NIFTYFMCG`, `NIFTYMETAL`, `NIFTYREALTY`, `NIFTYENERGY`, `NIFTYPSUBANK`,
   `NIFTYINFRA`, `NIFTYMIDCAP150`, `NIFTYSMALLCAP250` (Yahoo has no history for NIFTY MEDIA or
   MIDCAP 100). For the full sector rotation table, run `sector-rotation`.
3. **Web (WebSearch/WebFetch)** for GIFT Nifty, FII/DII provisional figures (published by NSE each
   evening), the F&O ban list, the results calendar, bulk and block deals, and the RBI and economic
   calendars. nseindia.com blocks scripted requests, so use news or broker pages that republish the
   figures, and cite them.
4. **Deeper reads:** `fii-dii-flows` for flow streaks and the FII index-futures long/short ratio from
   NSE's participant-wise OI file, and `market-breadth` for a breadth health score.

```bash
for s in NIFTY BANKNIFTY INDIAVIX NIFTYIT NIFTYAUTO NIFTYPHARMA NIFTYFMCG NIFTYMETAL NIFTYREALTY; do
  python3 ../technical-analysis/scripts/ta.py summary --symbol $s --json > pulse_$s.json; done
```

## Reading the inputs

- **GIFT Nifty** trades nearly 21 hours on NSE IX. A gap against NIFTY's previous close previews the
  open. Its premium includes a small futures carry, so don't treat every 20 points as a signal.
- **FII/DII cash flows.** Persistent FII selling with DII (mutual fund SIP) buying is the recurring
  pattern. DIIs often absorb FII selling, so headline FII outflows alone rarely mean a crash. Look at
  multi-day streaks and size relative to the past month.
- **Participant-wise OI.** A FII index-futures long/short ratio below about 20–25% is extreme short
  positioning, which is prone to short-covering rallies. Above about 60–70% is crowded long.
- **India VIX.** Below 12 is complacent, 12–18 normal, 18–25 stressed, and above 25 panic. A rising
  VIX with a falling NIFTY is normal fear. A rising VIX with a rising NIFTY is an unusual warning.
- **Breadth.** An advance/decline ratio above 2 is broad strength; below 0.5 broad weakness. NIFTY up
  on weak breadth means a handful of heavyweights are carrying it.
- **Sector rotation.** Rank sector indices by 1-week and 1-month return and by distance from SMA50.
  Leaders above a rising SMA50 are where long setups concentrate.
- **Event calendar.** RBI MPC (six meetings a year), CPI (around the 12th of each month), GDP, the
  Union Budget (1 Feb), US Fed and CPI, quarterly results season (within 45 days of quarter end; 60
  for Q4), and index rebalancing (semi-annual; large passive flows on the effective date).

## Regime label (end every brief with one)

| Regime | Conditions | Implication for trades |
|---|---|---|
| Risk-on trend | NIFTY above rising SMA50/200, VIX < 15, breadth > 1.5 | Normal size, buy pullbacks in leaders |
| Choppy / range | NIFTY between flat MAs, VIX 13–18, mixed breadth | Half size, fade extremes, take quick profits |
| Correction | NIFTY below SMA50, VIX rising, breadth < 0.7 | Smaller size, tighter stops, cash is a position |
| Stress | VIX > 22, gap-downs, FII heavy selling | Capital preservation, hedges, no new leverage |

## Output

```markdown
# Market pulse — [date] [time IST] ([pre-market | intraday | post-market])
**Regime:** [label] — [one-line reason]

| Item | Value | As of / source |
|---|---|---|
| GIFT Nifty | [value] ([±pts] vs NIFTY close) | [hh:mm IST], [source] |
| NIFTY / BANKNIFTY | [close] / [close] | [close dd-mmm], [source] |
| India VIX | [value] ([±%]) | [close dd-mmm] |
| FII / DII cash | [−/+₹x cr] / [−/+₹y cr] | provisional, [dd-mmm], [source] |
| Breadth (A/D) | [adv/dec] | [time] |

**Levels:** NIFTY support .. / ..; resistance .. / .. (chart + OI walls)
**Sectors:** leaders .., laggards ..
**Today:** results (..), F&O ban (..), events (..), expiry (..)
**What would change the view:** ..
```
Every number needs its timestamp and source. Say "not available" rather than guessing.
