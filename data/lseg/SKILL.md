---
name: lseg
description: Use when fetching financial data from LSEG Workspace via the Eikon Data API. Covers cURL requests, field discovery, symbology conversion, and time series data retrieval.
---

# LSEG Workspace Data API

Access financial, vessel, and commodity data from LSEG Workspace via the Eikon Data API.

## Prerequisites

1. **LSEG Workspace** must be running on your machine (exposes local proxy on port 9000)
2. **App Key** - generate via Workspace: type `APPKEY` in search bar, select "Eikon Data API" checkbox

Store credentials in `.env`:
```bash
LSEG_APP_ID=your_app_key_here
LSEG_API_ENDPOINT=http://localhost:9000/api/udf/
```

## API basics

**Endpoint:** `http://localhost:9000/api/udf/`

**Required headers:**
```
Content-Type: application/json
x-tr-applicationid: <app_key>
X-Forwarded-Host: localhost
```

**Request format:**
```json
{
  "Entity": {
    "E": "<entity_type>",
    "W": { <parameters> }
  }
}
```

## Entity types

### DataGrid - fetch data for instruments

Basic query:
```bash
curl -s -X POST "$LSEG_API_ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "x-tr-applicationid: $LSEG_APP_ID" \
  -H "X-Forwarded-Host: localhost" \
  -d '{
    "Entity": {
      "E": "DataGrid",
      "W": {
        "instruments": ["AAPL.O", "MSFT.O"],
        "fields": [
          {"name": "TR.CommonName"},
          {"name": "TR.PriceClose"},
          {"name": "TR.PE"}
        ]
      }
    }
  }' | jq .
```

With date parameters (time series):
```bash
curl -s -X POST "$LSEG_API_ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "x-tr-applicationid: $LSEG_APP_ID" \
  -H "X-Forwarded-Host: localhost" \
  -d '{
    "Entity": {
      "E": "DataGrid",
      "W": {
        "instruments": ["AAPL.O"],
        "fields": [
          {"name": "TR.PriceClose"},
          {"name": "TR.Volume"}
        ],
        "parameters": {
          "SDate": "2025-01-01",
          "EDate": "2025-01-31",
          "TOP": 10000
        }
      }
    }
  }' | jq .
```

### SymbologySearch - convert identifiers

Convert between RIC, ISIN, IMO, CUSIP, SEDOL, etc:
```bash
curl -s -X POST "$LSEG_API_ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "x-tr-applicationid: $LSEG_APP_ID" \
  -H "X-Forwarded-Host: localhost" \
  -d '{
    "Entity": {
      "E": "SymbologySearch",
      "W": {
        "symbols": ["US0378331005"],
        "from": "ISIN",
        "to": ["RIC"],
        "bestMatch": true
      }
    }
  }' | jq .
```

**Common identifier types:** `RIC`, `ISIN`, `CUSIP`, `SEDOL`, `IMO`, `ticker`

## Response format

```json
{
  "columnHeadersCount": 1,
  "data": [
    ["AAPL.O", "Apple Inc", 278.28, 37.47],
    ["MSFT.O", "Microsoft Corp", 478.53, 34.05]
  ],
  "headers": [[
    {"displayName": "Instrument"},
    {"displayName": "Company Common Name", "field": "TR.COMMONNAME"},
    {"displayName": "Price Close", "field": "TR.PRICECLOSE"},
    {"displayName": "P/E (Daily Time Series Ratio)", "field": "TR.PE"}
  ]],
  "totalRowsCount": 3
}
```

## Common fields

### Equities
| Field | Description |
|-------|-------------|
| `TR.CommonName` | Company name |
| `TR.PriceClose` | Closing price |
| `TR.PriceOpen` | Opening price |
| `TR.PriceHigh` | Day high |
| `TR.PriceLow` | Day low |
| `TR.Volume` | Trading volume |
| `TR.PE` | P/E ratio |
| `TR.CompanyMarketCap` | Market capitalization |
| `TR.TotalEmployees` | Employee count |
| `TR.HeadquartersCountry` | HQ country |
| `TR.GICSSector` | GICS sector |

### Vessels (maritime)
| Field | Description |
|-------|-------------|
| `TR.AssetIMO` | IMO number |
| `TR.AssetName` | Vessel name |
| `TR.AssetDWT` | Deadweight tonnage |
| `TR.AssetCubicCapacity` | Cubic capacity |
| `TR.AssetDateTime` | Position timestamp |
| `TR.AssetLocationLongitude` | Longitude |
| `TR.AssetLocationLatitude` | Latitude |
| `TR.AssetLocationDraught` | Current draught |
| `TR.AssetSpeed` | Speed |
| `TR.AssetHeading` | Heading |
| `TR.AssetDestination` | Destination port |
| `TR.AssetLocationStatus` | Navigation status |

### Trade flows (vessels)
| Field | Description |
|-------|-------------|
| `TR.AssetFlowPermID` | Flow ID |
| `TR.AssetLoadingPort` | Loading port |
| `TR.AssetLoadingDateTo` | Loading date |
| `TR.AssetDischargingPort` | Discharge port |
| `TR.AssetDischargeDate` | Discharge date |
| `TR.AssetFlowCommodity` | Commodity |
| `TR.AssetVolume` | Volume |
| `TR.AssetCharterer` | Charterer |

## Helper scripts

This skill includes helper scripts in `.claude/skills/lseg/scripts/`:

| Script | Purpose |
|--------|---------|
| `lseg-query.sh` | General DataGrid queries |
| `lseg-symbology.sh` | Identifier conversion |
| `lseg-timeseries.sh` | Time series data |

**Usage:**
```bash
# Load environment
source .env

# Query company data
.claude/skills/lseg/scripts/lseg-query.sh "AAPL.O,MSFT.O" "TR.CommonName,TR.PriceClose"

# Convert ISIN to RIC
.claude/skills/lseg/scripts/lseg-symbology.sh "US0378331005" ISIN RIC

# Get time series
.claude/skills/lseg/scripts/lseg-timeseries.sh "AAPL.O" "TR.PriceClose" "2025-01-01" "2025-01-31"
```

## Rate limits

| Limit | Value |
|-------|-------|
| Requests per second | 5 |
| Requests per day | 10,000 |
| Data per minute | 50 MB |
| Data per day | 5 GB |
| get_data points | ~10,000 |
| get_timeseries (interday) | 3,000 rows |
| get_timeseries (intraday) | 50,000 rows |

## Troubleshooting

**Connection refused:** LSEG Workspace not running. Start the desktop app.

**401 Unauthorized:** Invalid or expired app key. Generate new key via `APPKEY` in Workspace.

**Empty response:** Check field names are correct (case-sensitive `TR.FieldName` format).

**Port 9000 in use:** Workspace may use next available port. Check Workspace settings or try 9001.

## References

- [Eikon Data API Documentation](https://developers.lseg.com/en/api-catalog/eikon/eikon-data-api/documentation)
- [Quick Start Guide](https://developers.lseg.com/en/api-catalog/eikon/eikon-data-api/quick-start)
- [LSEG Developer Community](https://community.developers.refinitiv.com/categories/eikon-data-apis)
