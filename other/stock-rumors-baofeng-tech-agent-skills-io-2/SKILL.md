---
name: stock-rumors
description: Rumor Scanner — find early signals including M&A rumors, insider activity, analyst upgrades/downgrades, social whispers, and SEC/regulatory activity via AIsa API. Ranked by impact score. Use when the user asks about rumors, insider trading, M&A activity, analyst changes, or early market signals.
author: AIsa
version: 1.0.0
license: Apache-2.0
homepage: https://aisa.one
source: https://github.com/baofeng-tech/agent-skills-io/tree/main/targetSkills/stock-rumors
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 📊
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    optionalEnv:
    - AISA_BASE_URL
    - AISA_MODEL
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: 📊
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    optionalEnv:
    - AISA_BASE_URL
    - AISA_MODEL
    primaryEnv: AISA_API_KEY
---

# Rumor Scanner — AIsa Edition

Scan for early market signals and rumors using the AIsa API.

## Usage

```bash
python3 scripts/rumor_scanner.py
python3 scripts/rumor_scanner.py --focus ma
python3 scripts/rumor_scanner.py --focus insider
python3 scripts/rumor_scanner.py --focus analyst
python3 scripts/rumor_scanner.py --focus social
python3 scripts/rumor_scanner.py --output json
```

### Arguments

- `--focus`: Filter by `all` (default), `ma` (M&A), `insider`, `analyst`, or `social`
- `--output json`: Append structured JSON summary

## Signal Categories

- **M&A / Takeover Signals**: Acquisition, merger, buyout, strategic review keywords
- **Insider Trading Activity**: SEC EDGAR Form 4, cluster buying, 10b5-1 deviations
- **Analyst Actions**: Upgrades, downgrades, price target changes >15%, double-upgrades
- **Social & News Whispers**: "hearing that", "sources say", "rumored to", unusual social spikes
- **Regulatory / SEC Activity**: 13D/13G filings, investigations, Wells notices

## Output

Top 5 signals ranked by Impact Score with quality assessment, followed by an analyst note on the most actionable signals.

**NOT FINANCIAL ADVICE.** Rumors are unconfirmed. For informational purposes only.
