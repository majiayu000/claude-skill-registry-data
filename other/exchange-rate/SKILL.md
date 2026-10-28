---
name: exchange-rate
description: Query real-time exchange rates for any base currency via ExchangeRate-API. Use this skill whenever the user needs currency conversion rates, forex data, or wants to know how much one currency is worth in another.
license: MIT
---

# ExchangeRate — Real-time Exchange Rate Query

## Overview

Query real-time exchange rates for all supported currencies against a specified base currency via ExchangeRate-API.

| Property | Value |
|----------|-------|
| Endpoint | `GET https://app-dohnbj5by5mp-api-w9Rbo8E7p2b9.gateway.appmedo.com/v6/latest/{base_currency}` |
| Auth | Platform-managed gateway (`X-Gateway-Authorization: Bearer <INTEGRATIONS_API_KEY>`) |
| Supported Currencies | 161 (ISO 4217 three-letter codes) |
| Data Freshness | Daily updates (not tick-level) |
| Billing | Billed per call |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `base_currency` | `string` | Yes | Base currency code in ISO 4217 three-letter format, e.g. `USD`, `EUR`, `CNY` |

### Response Example (Success)

```json
{
  "result": "success",
  "documentation": "https://www.exchangerate-api.com/docs",
  "terms_of_use": "https://www.exchangerate-api.com/terms",
  "time_last_update_unix": 1234567890,
  "time_last_update_utc": "Wed, 01 Jan 2020 00:00:00 +0000",
  "time_next_update_unix": 1234567890,
  "time_next_update_utc": "Thu, 02 Jan 2020 00:00:00 +0000",
  "base_code": "USD",
  "conversion_rates": {
    "EUR": 0.85,
    "GBP": 0.75,
    "JPY": 110.5
  }
}
```

### Response Example (Error)

```json
{
  "result": "error",
  "error-type": "invalid-key"
}
```

Error types: `unsupported-code` (unsupported currency code), `malformed-request` (malformed request format), `invalid-key` (invalid key), `inactive-account` (account not activated), `quota-reached` (quota exhausted), `unknown-code` (unknown currency code).

---

## Usage at Generation Time (Direct Agent Call)

The platform manages the API key via `process.env["INTEGRATIONS_API_KEY"]`. Pass it as the `X-Gateway-Authorization` header — do not embed it in the URL path.

```typescript
interface ExchangeRateResponse {
  result: "success" | "error";
  "error-type"?: string;
  documentation?: string;
  terms_of_use?: string;
  time_last_update_unix?: number;
  time_last_update_utc?: string;
  time_next_update_unix?: number;
  time_next_update_utc?: string;
  base_code?: string;
  conversion_rates?: Record<string, number>;
}

async function getExchangeRates(baseCurrency: string): Promise<ExchangeRateResponse> {
  const apiKey = process.env["INTEGRATIONS_API_KEY"]; // platform-managed key
  const url = `https://app-dohnbj5by5mp-api-w9Rbo8E7p2b9.gateway.appmedo.com/v6/latest/${baseCurrency.toUpperCase()}`;

  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Accept": "application/json",
      "X-Gateway-Authorization": `Bearer ${apiKey}`,
    },
  });

  if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

  const json: ExchangeRateResponse = await response.json();

  if (json.result === "error") {
    throw new Error(`API error: ${json["error-type"]}`);
  }

  return json;
}

// Example: query exchange rates with USD as the base currency
const rates = await getExchangeRates("USD");
console.log(`1 USD = ${rates.conversion_rates?.EUR} EUR`);
```

---

## Usage at Runtime (Application Call via Edge Function)

When calling from within an application, proxy the request through an Edge Function to keep the API key off the client.

### Edge Function Code

```typescript
// edge-functions/exchange-rate.ts
import { serve } from "https://deno.land/std/http/server.ts";

serve(async (req: Request): Promise<Response> => {
  if (req.method !== "POST") {
    return new Response("Method Not Allowed", { status: 405 });
  }

  // Parse client request
  let baseCurrency: string;
  try {
    const body = await req.json();
    baseCurrency = body.base_currency;
    if (!baseCurrency) throw new Error("Missing base_currency");
  } catch {
    return new Response(JSON.stringify({ error: "Invalid request body" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Read platform-managed key — never expose to the client
  const apiKey = Deno.env.get("INTEGRATIONS_API_KEY");
  if (!apiKey) {
    return new Response(JSON.stringify({ error: "Server configuration error" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Call upstream via platform gateway
  const upstream = await fetch(
    `https://app-dohnbj5by5mp-api-w9Rbo8E7p2b9.gateway.appmedo.com/v6/latest/${baseCurrency.toUpperCase()}`,
    {
      method: "GET",
      headers: {
        "Accept": "application/json",
        "X-Gateway-Authorization": `Bearer ${apiKey}`,
      },
    }
  );

  // Forward quota/balance errors verbatim
  if (upstream.status === 429 || upstream.status === 402) {
    const errText = await upstream.text();
    return new Response(errText, {
      status: upstream.status,
      headers: { "Content-Type": "application/json" },
    });
  }

  if (!upstream.ok) {
    return new Response(
      JSON.stringify({ error: `Upstream error: ${upstream.status}` }),
      { status: 502, headers: { "Content-Type": "application/json" } }
    );
  }

  const data = await upstream.json();
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
});
```

### Frontend Call to Edge Function

**Recommended (when supabase client is available):**

```typescript
async function fetchExchangeRates(baseCurrency: string) {
  const { data, error } = await supabase.functions.invoke("exchange-rate", {
    body: { base_currency: baseCurrency },
  });
  if (error) throw error;
  if (data.result === "error") throw new Error(`API error: ${data["error-type"]}`);
  return data;
}
```

**Fallback (when supabase client is unavailable):**

```typescript
async function fetchExchangeRates(baseCurrency: string) {
  const res = await fetch(`${import.meta.env.VITE_SUPABASE_URL}/functions/v1/exchange-rate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ base_currency: baseCurrency }),
  });

  if (res.status === 429) {
    const err = await res.json();
    throw new Error(`Quota exhausted: ${err.message ?? res.statusText}`);
  }
  if (res.status === 402) {
    const err = await res.json();
    throw new Error(`Insufficient balance: ${err.message ?? res.statusText}`);
  }
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);

  const json = await res.json();
  if (json.result === "error") throw new Error(`API error: ${json["error-type"]}`);

  return json;
}
```

---

## Parameter Reference

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `base_currency` | `string` | Yes | ISO 4217 three-letter currency code, e.g. `USD`, `EUR`, `CNY`, `JPY` |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `result` | `string` | Request result: `"success"` or `"error"` |
| `error-type`? | `string` | Error type; only present when `result === "error"` |
| `documentation` | `string` | URL to API documentation |
| `terms_of_use` | `string` | URL to terms of use |
| `time_last_update_unix` | `number` | Timestamp of last rate update (Unix epoch) |
| `time_last_update_utc` | `string` | Timestamp of last rate update (UTC string) |
| `time_next_update_unix` | `number` | Timestamp of next scheduled rate update (Unix epoch) |
| `time_next_update_utc` | `string` | Timestamp of next scheduled rate update (UTC string) |
| `base_code` | `string` | Base currency code, matches the request |
| `conversion_rates` | `Record<string, number>` | Map of target currency codes (ISO 4217) to exchange rates from the base currency |

---

## Notes

- **Key security**: The API key is injected into the Edge Function via `INTEGRATIONS_API_KEY`. Never expose it in frontend code or version control.
- **Error handling**: Always check the `result` field in the response body. When `"error"`, handle accordingly based on `error-type`, especially `quota-reached`.
- **Billing**: This endpoint is billed per call. Avoid redundant calls in loops or polling — cache exchange rate data at the application layer (rates update once per day; use `time_next_update_utc` to know when to refresh).
- **Currency codes**: Only ISO 4217 standard three-letter codes are supported. Unsupported codes return `unsupported-code` or `unknown-code` errors.
- **Data freshness**: Rates are updated daily, not tick-level. Not suitable for high-frequency trading use cases.
- **Single base currency per request**: Each request specifies one base currency and returns rates against all 161 supported currencies.
