---
name: exchange-rates
description: Use when implementing exchange rate functionality - provides complete patterns for fetching BTC/fiat exchange rates from Coinbase API, caching strategies, conversion utilities, and React hooks for displaying rates in UI
when_to_use: When adding exchange rate display, converting between BTC and fiat currencies, showing USD equivalents for Bitcoin amounts, or implementing currency conversion features
---

# Exchange Rate Service

## Overview

Complete implementation guide for fetching and using Bitcoin exchange rates from Coinbase API. Includes caching strategies, conversion utilities, and React hooks for displaying rates in wallet UIs.

**Core Capabilities:**
- Fetch BTC exchange rates from Coinbase API
- Module-level caching to reduce API calls
- Convert between BTC, sats, and fiat currencies
- React hooks for real-time rate display
- Error handling with stale cache fallback
- Support for all major fiat currencies

**Key Architecture Pattern:** Module-level cache with configurable duration prevents excessive API calls while ensuring fresh data.

## Prerequisites

**No additional packages required** - Uses native `fetch` API.

**Coinbase API:**
- Base URL: `https://api.coinbase.com/v2/exchange-rates`
- No authentication required
- Rate limits: Fair use policy (implement caching to respect limits)

## Implementation Checklist

- [ ] Create exchange rate service with caching
- [ ] Implement BTC/fiat rate fetching
- [ ] Add conversion utilities (BTC↔USD, sats↔USD)
- [ ] Create React hook for exchange rates
- [ ] Add error handling and stale cache fallback
- [ ] Implement UI components for rate display
- [ ] Add loading states and error states

## Part 1: Exchange Rate Service

### Core Service Implementation

```typescript
// lib/exchangeRateService.ts
/**
 * Exchange rate service for fetching BTC/USD rates from Coinbase API
 * 
 * Module-level cache to avoid excessive API calls
 */
const COINBASE_API_URL = "https://api.coinbase.com/v2/exchange-rates";
const CACHE_DURATION_MS = 60000; // 1 minute cache

let cachedRate: number | null = null;
let cacheTimestamp: number = 0;

/**
 * Get the current BTC/USD exchange rate from Coinbase API
 * Uses caching to avoid excessive API calls
 * 
 * @returns Promise resolving to BTC/USD exchange rate
 */
export async function getBtcUsdRate(): Promise<number> {
  const now = Date.now();
  
  // Return cached rate if still valid
  if (cachedRate && (now - cacheTimestamp) < CACHE_DURATION_MS) {
    console.debug(`Using cached BTC/USD rate: ${cachedRate}`, {
      cache_age_ms: now - cacheTimestamp,
    });
    return cachedRate;
  }

  try {
    console.debug("Fetching BTC/USD rate from Coinbase API");

    const response = await fetch(`${COINBASE_API_URL}?currency=BTC`, {
      method: "GET",
      headers: {
        "Accept": "application/json",
        "User-Agent": "YourApp/1.0",
      },
      // Add timeout to prevent hanging
      signal: AbortSignal.timeout(10000), // 10 second timeout
    });

    if (!response.ok) {
      throw new Error(`Coinbase API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    
    // Validate response structure
    if (!data?.data?.rates?.USD) {
      throw new Error("Invalid response format from Coinbase API");
    }

    const rate = parseFloat(data.data.rates.USD);
    
    if (isNaN(rate) || rate <= 0) {
      throw new Error(`Invalid exchange rate received: ${data.data.rates.USD}`);
    }

    // Update cache
    cachedRate = rate;
    cacheTimestamp = now;

    console.info(`Fetched BTC/USD rate from Coinbase: ${rate}`, { rate });

    return rate;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    
    console.error(`Failed to fetch BTC/USD rate: ${errorMessage}`);

    // If we have a cached rate, use it as fallback
    if (cachedRate) {
      const cacheAge = now - cacheTimestamp;
      console.warn(`Using stale cached rate as fallback: ${cachedRate}`, {
        cache_age_ms: cacheAge,
      });
      return cachedRate;
    }

    // If no cached rate available, throw error
    throw new Error(`Unable to fetch BTC/USD exchange rate: ${errorMessage}`);
  }
}
```

**Key Features:**
- **Module-level cache** - Shared across all calls, prevents duplicate requests
- **Configurable cache duration** - Default 1 minute, adjustable
- **Stale cache fallback** - Uses old rate if API fails
- **Timeout protection** - 10 second timeout prevents hanging
- **Response validation** - Validates API response structure and values

### Conversion Utilities

```typescript
// lib/exchangeRateService.ts

/**
 * Convert BTC amount to USD using current exchange rate
 * 
 * @param btcAmount - Amount in BTC
 * @returns Promise resolving to USD amount
 */
export async function btcToUsd(btcAmount: number): Promise<number> {
  const rate = await getBtcUsdRate();
  return btcAmount * rate;
}

/**
 * Convert USD amount to BTC using current exchange rate
 * 
 * @param usdAmount - Amount in USD
 * @returns Promise resolving to BTC amount
 */
export async function usdToBtc(usdAmount: number): Promise<number> {
  const rate = await getBtcUsdRate();
  return usdAmount / rate;
}

/**
 * Convert sats to USD using current exchange rate
 * 
 * @param sats - Amount in satoshis
 * @returns Promise resolving to USD amount
 */
export async function satsToUsd(sats: number): Promise<number> {
  const btcAmount = sats / 100000000; // Convert sats to BTC
  return btcToUsd(btcAmount);
}

/**
 * Convert USD to sats using current exchange rate
 * 
 * @param usdAmount - Amount in USD
 * @returns Promise resolving to satoshis
 */
export async function usdToSats(usdAmount: number): Promise<number> {
  const btcAmount = await usdToBtc(usdAmount);
  return Math.floor(btcAmount * 100000000); // Convert BTC to sats
}
```

### Multi-Currency Support

**Available Fiat Currencies:**

Coinbase API supports all major fiat currencies. Common examples include:

**Major Currencies:**
- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- CNY (Chinese Yuan)
- CAD (Canadian Dollar)
- AUD (Australian Dollar)
- CHF (Swiss Franc)
- SEK (Swedish Krona)
- NOK (Norwegian Krone)
- DKK (Danish Krone)
- PLN (Polish Zloty)
- CZK (Czech Koruna)
- HUF (Hungarian Forint)
- RON (Romanian Leu)
- BGN (Bulgarian Lev)
- HRK (Croatian Kuna)

**Other Supported Currencies:**
- AED, AFN, ALL, AMD, ANG, AOA, ARS, AWG, AZN
- BBD, BDT, BHD, BIF, BMD, BND, BOB, BSD, BTN, BWP, BYN, BZD
- CDF, CLP, COP, CRC, CUP, CVE, CZK
- DJF, DOP, DZD
- EGP, ETB, EUR
- FJD, FKP
- GEL, GHS, GIP, GMD, GNF, GTQ, GYD
- HKD, HNL, HTG
- IDR, ILS, INR, IQD, IRR, ISK
- JMD, JOD, JPY
- KES, KGS, KHR, KMF, KPW, KRW, KWD, KYD, KZT
- LAK, LBP, LKR, LRD, LSL, LYD
- MAD, MDL, MGA, MKD, MMK, MNT, MOP, MRO, MRU, MUR, MVR, MWK, MXN, MYR, MZN
- NAD, NGN, NIO, NPR, NZD
- OMR
- PAB, PEN, PGK, PHP, PKR, PLN, PYG
- QAR
- RON, RSD, RUB, RWF
- SAR, SBD, SCR, SDG, SEK, SGD, SHP, SLL, SOS, SRD, STD, SVC, SYP, SZL
- THB, TJS, TMM, TMT, TND, TOP, TRY, TTD, TWD, TZS
- UAH, UGX, UYU, UZS
- VEF, VES, VND, VUV
- WST
- XAF, XCD, XOF, XPF
- YER
- ZAR, ZMK, ZMW, ZWD

**Note:** The API response includes rates for all currencies. To fetch a specific currency rate:

```typescript
/**
 * Get BTC exchange rate for any supported currency
 * 
 * @param currencyCode - ISO currency code (e.g., 'EUR', 'GBP', 'JPY')
 * @returns Promise resolving to BTC/[currency] exchange rate
 */
export async function getBtcRate(currencyCode: string): Promise<number> {
  const response = await fetch(`${COINBASE_API_URL}?currency=BTC`, {
    method: "GET",
    headers: {
      "Accept": "application/json",
    },
    signal: AbortSignal.timeout(10000),
  });

  if (!response.ok) {
    throw new Error(`Coinbase API error: ${response.status}`);
  }

  const data = await response.json();
  
  if (!data?.data?.rates?.[currencyCode]) {
    throw new Error(`Currency ${currencyCode} not supported`);
  }

  const rate = parseFloat(data.data.rates[currencyCode]);
  
  if (isNaN(rate) || rate <= 0) {
    throw new Error(`Invalid exchange rate for ${currencyCode}`);
  }

  return rate;
}
```

### Cache Management

```typescript
// lib/exchangeRateService.ts

/**
 * Clear the cached exchange rate (useful for testing or forcing refresh)
 */
export function clearCache(): void {
  cachedRate = null;
  cacheTimestamp = 0;
}

/**
 * Get cache status for debugging
 * 
 * @returns Cache status object
 */
export function getCacheStatus(): { 
  rate: number | null; 
  age_ms: number; 
  is_valid: boolean 
} {
  const now = Date.now();
  const age = now - cacheTimestamp;
  const isValid = cachedRate !== null && age < CACHE_DURATION_MS;
  
  return {
    rate: cachedRate,
    age_ms: age,
    is_valid: isValid,
  };
}
```

## Part 2: React Hooks

### Exchange Rate Hook

```typescript
// hooks/useExchangeRate.ts
import { useQuery } from '@tanstack/react-query';
import { getBtcUsdRate } from '@/lib/exchangeRateService';

/**
 * Hook to fetch and cache BTC/USD exchange rate
 * 
 * @example
 * ```tsx
 * const { data: rate, isLoading } = useExchangeRate();
 * 
 * if (rate) {
 *   const usdValue = balanceSats / 100000000 * rate;
 * }
 * ```
 */
export function useExchangeRate() {
  return useQuery({
    queryKey: ['btc-usd-rate'],
    queryFn: getBtcUsdRate,
    staleTime: 60000, // Consider stale after 1 minute
    refetchInterval: 120000, // Refetch every 2 minutes
    retry: 2,
    retryDelay: 1000,
  });
}
```

### Conversion Hook

```typescript
// hooks/useExchangeRate.ts
import { useMemo } from 'react';
import { useExchangeRate } from './useExchangeRate';

/**
 * Hook to convert sats to USD with current exchange rate
 * 
 * @param sats - Amount in satoshis
 * @returns USD amount or null if rate unavailable
 */
export function useSatsToUsd(sats: number | null | undefined) {
  const { data: rate } = useExchangeRate();
  
  return useMemo(() => {
    if (!sats || !rate) return null;
    return (sats / 100000000) * rate;
  }, [sats, rate]);
}

/**
 * Hook to convert USD to sats with current exchange rate
 * 
 * @param usd - Amount in USD
 * @returns Satoshis or null if rate unavailable
 */
export function useUsdToSats(usd: number | null | undefined) {
  const { data: rate } = useExchangeRate();
  
  return useMemo(() => {
    if (!usd || !rate) return null;
    return Math.floor((usd / rate) * 100000000);
  }, [usd, rate]);
}
```

## Part 3: UI Components

### Exchange Rate Display

```typescript
// components/ExchangeRateDisplay.tsx
import { useExchangeRate } from '@/hooks/useExchangeRate';
import { Skeleton } from '@/components/ui/skeleton';

export function ExchangeRateDisplay() {
  const { data: rate, isLoading, error } = useExchangeRate();

  if (isLoading) {
    return <Skeleton className="h-6 w-32" />;
  }

  if (error) {
    return (
      <span className="text-sm text-muted-foreground">
        Rate unavailable
      </span>
    );
  }

  if (!rate) {
    return null;
  }

  return (
    <div className="text-sm">
      <span className="text-muted-foreground">BTC/USD: </span>
      <span className="font-mono">${rate.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}</span>
    </div>
  );
}
```

### Balance with USD Equivalent

```typescript
// components/BalanceDisplay.tsx
import { useSatsToUsd } from '@/hooks/useExchangeRate';
import { Skeleton } from '@/components/ui/skeleton';

interface BalanceDisplayProps {
  sats: number;
}

export function BalanceDisplay({ sats }: BalanceDisplayProps) {
  const usdValue = useSatsToUsd(sats);

  return (
    <div className="space-y-1">
      <div className="text-2xl font-bold">
        {sats.toLocaleString()} sats
      </div>
      {usdValue !== null ? (
        <div className="text-sm text-muted-foreground">
          ≈ ${usdValue.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}
        </div>
      ) : (
        <Skeleton className="h-4 w-24" />
      )}
    </div>
  );
}
```

### Formatted Currency Display

```typescript
// components/CurrencyDisplay.tsx
import { useSatsToUsd } from '@/hooks/useExchangeRate';

interface CurrencyDisplayProps {
  sats: number;
  showSats?: boolean;
  showUsd?: boolean;
}

export function CurrencyDisplay({ 
  sats, 
  showSats = true, 
  showUsd = true 
}: CurrencyDisplayProps) {
  const usdValue = useSatsToUsd(sats);

  return (
    <div className="flex flex-col gap-1">
      {showSats && (
        <span className="font-mono">
          {sats.toLocaleString()} sats
        </span>
      )}
      {showUsd && usdValue !== null && (
        <span className="text-sm text-muted-foreground">
          ${usdValue.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          })}
        </span>
      )}
    </div>
  );
}
```

## Common Pitfalls

### 1. ❌ Not implementing caching

**Problem:** Fetching exchange rate on every render causes excessive API calls and rate limiting.

**Solution:** Use module-level cache with configurable duration:
```typescript
const CACHE_DURATION_MS = 60000; // 1 minute
let cachedRate: number | null = null;
let cacheTimestamp: number = 0;
```

### 2. ❌ Not handling API failures

**Problem:** API failures break the UI completely.

**Solution:** Always provide fallback to stale cache:
```typescript
if (cachedRate) {
  console.warn('Using stale cached rate as fallback');
  return cachedRate;
}
```

### 3. ❌ No timeout protection

**Problem:** Slow or hanging API calls freeze the UI.

**Solution:** Add timeout to fetch requests:
```typescript
signal: AbortSignal.timeout(10000), // 10 second timeout
```

### 4. ❌ Not validating API response

**Problem:** Invalid or unexpected API responses cause runtime errors.

**Solution:** Validate response structure:
```typescript
if (!data?.data?.rates?.USD) {
  throw new Error("Invalid response format");
}

const rate = parseFloat(data.data.rates.USD);
if (isNaN(rate) || rate <= 0) {
  throw new Error("Invalid exchange rate");
}
```

### 5. ❌ Incorrect satoshi conversion

**Problem:** Wrong conversion between sats and BTC causes incorrect amounts.

**Solution:** Always use correct conversion factors:
```typescript
// BTC to sats
const sats = btc * 100000000;

// Sats to BTC
const btc = sats / 100000000;
```

### 6. ❌ Not handling loading states

**Problem:** UI shows incorrect values while rate is loading.

**Solution:** Show loading skeleton or null until rate is available:
```typescript
const { data: rate, isLoading } = useExchangeRate();

if (isLoading) {
  return <Skeleton className="h-6 w-32" />;
}
```

## Testing Strategy

### Unit Tests

```typescript
// lib/exchangeRateService.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { getBtcUsdRate, clearCache, getCacheStatus } from './exchangeRateService';

describe('Exchange Rate Service', () => {
  beforeEach(() => {
    clearCache();
    vi.clearAllMocks();
  });

  describe('getBtcUsdRate', () => {
    it('fetches rate from Coinbase API', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          data: {
            rates: {
              USD: '50000.00',
            },
          },
        }),
      });

      const rate = await getBtcUsdRate();
      expect(rate).toBe(50000);
    });

    it('uses cached rate when available', async () => {
      // First call
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          data: { rates: { USD: '50000.00' } },
        }),
      });

      await getBtcUsdRate();
      const firstCallCount = vi.mocked(global.fetch).mock.calls.length;

      // Second call within cache window
      const rate = await getBtcUsdRate();
      const secondCallCount = vi.mocked(global.fetch).mock.calls.length;

      expect(rate).toBe(50000);
      expect(secondCallCount).toBe(firstCallCount); // No new API call
    });

    it('falls back to stale cache on API failure', async () => {
      // First call succeeds
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          data: { rates: { USD: '50000.00' } },
        }),
      });

      await getBtcUsdRate();

      // Second call fails
      global.fetch = vi.fn().mockRejectedValueOnce(new Error('Network error'));

      const rate = await getBtcUsdRate();
      expect(rate).toBe(50000); // Uses stale cache
    });

    it('throws error when no cache available and API fails', async () => {
      global.fetch = vi.fn().mockRejectedValue(new Error('Network error'));

      await expect(getBtcUsdRate()).rejects.toThrow('Unable to fetch');
    });

    it('validates API response structure', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ invalid: 'structure' }),
      });

      await expect(getBtcUsdRate()).rejects.toThrow('Invalid response format');
    });
  });

  describe('getCacheStatus', () => {
    it('returns cache status', () => {
      const status = getCacheStatus();
      expect(status).toHaveProperty('rate');
      expect(status).toHaveProperty('age_ms');
      expect(status).toHaveProperty('is_valid');
    });
  });
});
```

### Integration Tests

```typescript
// hooks/useExchangeRate.test.tsx
import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { useExchangeRate } from './useExchangeRate';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('useExchangeRate', () => {
  it('fetches exchange rate', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        data: { rates: { USD: '50000.00' } },
      }),
    });

    const { result } = renderHook(() => useExchangeRate(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toBe(50000);
  });
});
```

## API Reference

### Coinbase Exchange Rates API

**Endpoint:** `GET https://api.coinbase.com/v2/exchange-rates?currency=BTC`

**Response Format:**
```json
{
  "data": {
    "currency": "BTC",
    "rates": {
      "USD": "50000.00",
      "EUR": "45000.00",
      // ... all supported currencies
    }
  }
}
```

**Rate Limits:**
- No official rate limit documented
- Implement caching to respect fair use
- Recommended: Cache for 1-5 minutes

**Error Handling:**
- 4xx/5xx responses: Check `response.ok` and handle accordingly
- Network errors: Use stale cache fallback
- Invalid responses: Validate structure before using

## Summary

To implement exchange rate functionality:

1. **Create service** - Module-level cache with Coinbase API integration
2. **Add conversion utilities** - BTC↔USD, sats↔USD conversions
3. **Create React hooks** - Use TanStack Query for caching and refetching
4. **Build UI components** - Display rates with loading and error states
5. **Handle errors** - Fallback to stale cache, show user-friendly messages
6. **Test thoroughly** - Unit tests for service, integration tests for hooks

**Key principle:** Cache aggressively, validate responses, and always provide fallbacks for API failures.

