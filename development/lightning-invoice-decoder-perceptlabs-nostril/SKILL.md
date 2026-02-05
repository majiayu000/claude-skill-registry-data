---
name: lightning-invoice-decoder
description: Use when implementing BOLT11 Lightning invoice decoding - provides complete patterns for decoding invoice amounts, validating invoice format, and extracting satoshi values from Lightning invoices
when_to_use: When adding Lightning invoice parsing, validating BOLT11 invoices, extracting payment amounts from invoices, or implementing Lightning payment flows
---

# Lightning Invoice Decoder

## Overview

Complete implementation guide for decoding BOLT11 Lightning invoices and extracting payment amounts. Supports all BOLT11 denominations (m, u, n, p) and handles amountless invoices gracefully.

**Core Capabilities:**
- Decode BOLT11 invoice amounts to satoshis
- Validate BOLT11 invoice format
- Handle all denomination suffixes (m, u, n, p)
- Support amountless invoices
- Invoice expiry calculation and validation
- Error handling and validation

## Prerequisites

**No external packages required** - pure TypeScript/JavaScript implementation.

## Implementation Checklist

- [ ] Implement invoice validation function
- [ ] Implement amount decoding function
- [ ] Handle all denomination suffixes
- [ ] Support amountless invoices
- [ ] Add error handling
- [ ] Create React hook wrapper (optional)
- [ ] Add UI components for invoice display (optional)

## Part 1: Core Decoder Functions

### Invoice Validation

**CRITICAL:** Always validate invoice format before attempting to decode.

```typescript
// lib/bolt11Decoder.ts
/**
 * Validate if a string is a valid BOLT11 invoice
 * @param invoice - The string to validate
 * @returns true if the string appears to be a valid BOLT11 invoice
 */
export function isValidBolt11Invoice(invoice: string): boolean {
  if (!invoice || typeof invoice !== 'string') {
    return false;
  }

  const normalized = invoice.toLowerCase().trim();
  
  // BOLT11 invoices start with 'lnbc' and contain '1' followed by characters (the bech32 separator)
  // They also need to be long enough to contain the required components
  return (
    normalized.startsWith('lnbc') && 
    /1[a-z0-9]/.test(normalized) &&
    normalized.length > 20 // Minimum reasonable length for a BOLT11 invoice
  );
}
```

**Usage:**
```typescript
if (isValidBolt11Invoice(invoiceString)) {
  // Safe to decode
  const amount = decodeBolt11Amount(invoiceString);
} else {
  // Invalid invoice format
  console.error('Invalid BOLT11 invoice');
}
```

### Amount Decoding

**Decode invoice amount to satoshis:**

```typescript
// lib/bolt11Decoder.ts
/**
 * Decode a BOLT11 invoice and extract the amount in satoshis
 * @param invoice - The BOLT11 invoice string
 * @returns The amount in satoshis, or null if amount cannot be determined
 */
export function decodeBolt11Amount(invoice: string): number | null {
  try {
    // Validate and prepare invoice
    if (!invoice || typeof invoice !== 'string') {
      return null;
    }

    const normalizedInvoice = invoice.toLowerCase().trim();

    // Check if it's a valid BOLT11 invoice
    if (!isValidBolt11Invoice(normalizedInvoice)) {
      return null;
    }

    // Parse the prefix to extract amount
    // Format: lnbc[amount][suffix] where suffix can be m, u, n, p
    const prefixMatch = normalizedInvoice.match(/^lnbc(\d*)([munp]?)/);
    if (!prefixMatch) {
      return null;
    }

    const [, amountStr, suffix] = prefixMatch;

    // If no amount specified, return null (amountless invoice)
    if (!amountStr) {
      return null;
    }

    const amount = parseInt(amountStr, 10);
    if (isNaN(amount)) {
      return null;
    }

    // Define multipliers for different denominations
    const multipliers: Record<string, number> = {
      m: 0.001,        // milli-bitcoin
      u: 0.000001,     // micro-bitcoin  
      n: 0.000000001,  // nano-bitcoin
      p: 0.000000000001 // pico-bitcoin
    };

    // Apply multiplier if suffix exists
    const multiplier = multipliers[suffix] || 1;
    const amountInBitcoin = amount * multiplier;

    // Convert Bitcoin to satoshis (1 Bitcoin = 100,000,000 satoshis)
    const amountInSatoshis = Math.round(amountInBitcoin * 100_000_000);

    return amountInSatoshis;
  } catch (error) {
    console.error('Error decoding BOLT11 invoice:', error);
    return null;
  }
}
```

**Usage:**
```typescript
const invoice = 'lnbc100n1p...';
const amount = decodeBolt11Amount(invoice);
if (amount === null) {
  console.log('Amountless invoice or invalid format');
} else {
  console.log(`Amount: ${amount} sats`);
}
```

## Part 2: Understanding BOLT11 Format

### Invoice Structure

BOLT11 invoices follow this format:
```
lnbc[amount][suffix]1[bech32-encoded-data]
```

**Prefix breakdown:**
- `lnbc` - Lightning Network Bitcoin mainnet prefix
- `[amount]` - Optional numeric amount
- `[suffix]` - Optional denomination suffix (m, u, n, p)
- `1` - Bech32 separator character
- `[bech32-encoded-data]` - Encoded invoice data

### Denomination Suffixes

| Suffix | Multiplier | Example | Satoshis |
|--------|-----------|---------|----------|
| (none) | 1 BTC | `lnbc1001...` | 10,000,000,000 sats |
| `m` | 0.001 BTC | `lnbc100m1...` | 10,000,000 sats |
| `u` | 0.000001 BTC | `lnbc100u1...` | 10,000 sats |
| `n` | 0.000000001 BTC | `lnbc100n1...` | 1,000 sats |
| `p` | 0.000000000001 BTC | `lnbc100p1...` | 1 sat |

### Amountless Invoices

Some invoices don't specify an amount - the payer chooses how much to send. The decoder returns `null` for these invoices:

```typescript
const amountlessInvoice = 'lnbc1...';
const amount = decodeBolt11Amount(amountlessInvoice);
// amount === null (amountless invoice)
```

**Handling amountless invoices:**
```typescript
const amount = decodeBolt11Amount(invoice);
if (amount === null) {
  // Show amount input field for user to specify
  return <AmountInputForm invoice={invoice} />;
} else {
  // Display fixed amount
  return <PaymentDisplay amount={amount} invoice={invoice} />;
}
```

## Part 2.5: Invoice Expiry

### Understanding Invoice Expiry

BOLT11 invoices include an expiration time calculated from:
- **Invoice timestamp**: When the invoice was created (Unix timestamp in seconds)
- **Expire time tag**: Tag code 6 (`expire_time`) contains seconds until expiry
- **Expiry calculation**: `expiry = timestamp + expire_time`
- **Default expiry**: 3600 seconds (1 hour) if expire_time tag is missing

### Expiry Calculation

**Important:** The current `decodeBolt11Amount` function only extracts the amount from the invoice prefix. To decode expiry information, you need to decode the full bech32 invoice and parse tags.

**For full invoice decoding** (including expiry, description, payment hash, etc.), use a complete BOLT11 decoder library like:
- `bolt11` (npm package)
- `light-bolt11-decoder` (npm package)
- Or implement full bech32 decoding (see `lightning-decoder` project)

**Expiry calculation from decoded invoice:**
```typescript
// If using a full decoder library that returns decoded invoice object:
interface DecodedInvoice {
  timestamp: number;        // Unix timestamp (seconds)
  timestampString: string;   // ISO string
  timeExpireDate?: number;   // Absolute expiry timestamp (seconds)
  timeExpireDateString?: string; // ISO string
  tags: Array<{
    tagName: string;
    data: any;
  }>;
}

// Expiry is calculated as:
// timeExpireDate = timestamp + expire_time (from tag 6)
```

### Checking if Invoice is Expired

**With full decoder:**
```typescript
function isInvoiceExpired(decodedInvoice: DecodedInvoice): boolean {
  if (!decodedInvoice.timeExpireDate) {
    // No expiry specified, use default 1 hour
    const defaultExpiry = decodedInvoice.timestamp + 3600;
    return Date.now() / 1000 > defaultExpiry;
  }
  
  return Date.now() / 1000 > decodedInvoice.timeExpireDate;
}
```

**Time remaining:**
```typescript
function getTimeRemaining(decodedInvoice: DecodedInvoice): number | null {
  const expiry = decodedInvoice.timeExpireDate 
    ?? decodedInvoice.timestamp + 3600; // Default 1 hour
  
  const remaining = expiry - (Date.now() / 1000);
  return remaining > 0 ? Math.floor(remaining) : 0;
}
```

### Expiry Display Component

**Show expiry countdown in UI:**

```typescript
// components/InvoiceExpiry.tsx
import { useEffect, useState } from 'react';
import { Badge } from '@/components/ui/badge';

export function InvoiceExpiry({ expiryTimestamp }: { expiryTimestamp: number }) {
  const [timeRemaining, setTimeRemaining] = useState(
    expiryTimestamp - Math.floor(Date.now() / 1000)
  );

  useEffect(() => {
    const interval = setInterval(() => {
      const remaining = expiryTimestamp - Math.floor(Date.now() / 1000);
      setTimeRemaining(remaining);
      if (remaining <= 0) clearInterval(interval);
    }, 1000);
    return () => clearInterval(interval);
  }, [expiryTimestamp]);

  if (timeRemaining <= 0) return <Badge variant="destructive">Expired</Badge>;
  
  const minutes = Math.floor(timeRemaining / 60);
  const seconds = timeRemaining % 60;
  return (
    <Badge variant={minutes < 5 ? "destructive" : "default"}>
      Expires in {minutes}m {seconds}s
    </Badge>
  );
}
```

### Expiry Validation Before Payment

**Always check expiry before processing payment:**
```typescript
function validateInvoiceBeforePayment(decodedInvoice: DecodedInvoice): {
  valid: boolean;
  error?: string;
} {
  if (isInvoiceExpired(decodedInvoice)) {
    return {
      valid: false,
      error: 'This invoice has expired. Please request a new one.',
    };
  }

  const timeRemaining = getTimeRemaining(decodedInvoice);
  if (timeRemaining !== null && timeRemaining < 60) {
    // Warn if less than 1 minute remaining
    return {
      valid: true,
      error: `Invoice expires in ${timeRemaining} seconds. Proceed quickly!`,
    };
  }

  return { valid: true };
}
```

## Part 3: React Hook Integration

### Custom Hook Wrapper

**Optional:** Create a React hook for easier integration:

```typescript
// hooks/useBolt11Decoder.ts
import { useMemo } from 'react';
import { decodeBolt11Amount, isValidBolt11Invoice } from '@/lib/bolt11Decoder';

export function useBolt11Decoder(invoice: string | null | undefined) {
  return useMemo(() => {
    if (!invoice) {
      return {
        isValid: false,
        amount: null,
        error: null,
      };
    }

    const isValid = isValidBolt11Invoice(invoice);
    if (!isValid) {
      return {
        isValid: false,
        amount: null,
        error: 'Invalid BOLT11 invoice format',
      };
    }

    const amount = decodeBolt11Amount(invoice);
    
    return {
      isValid: true,
      amount,
      isAmountless: amount === null,
      error: null,
    };
  }, [invoice]);
}
```

**Usage:**
```typescript
function PaymentForm({ invoice }: { invoice: string }) {
  const { isValid, amount, isAmountless, error } = useBolt11Decoder(invoice);

  if (!isValid) {
    return <div>Invalid invoice: {error}</div>;
  }

  if (isAmountless) {
    return <AmountInputForm invoice={invoice} />;
  }

  return <PaymentDisplay amount={amount!} invoice={invoice} />;
}
```

## Part 4: UI Components

### Invoice Display Component

**Display decoded invoice information:**

```typescript
// components/InvoiceDisplay.tsx
import { decodeBolt11Amount, isValidBolt11Invoice } from '@/lib/bolt11Decoder';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export function InvoiceDisplay({ invoice }: { invoice: string }) {
  const isValid = isValidBolt11Invoice(invoice);
  const amount = isValid ? decodeBolt11Amount(invoice) : null;

  if (!isValid) {
    return (
      <Card>
        <CardContent className="pt-6">
          <p className="text-destructive">Invalid BOLT11 invoice</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Lightning Invoice</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="text-sm text-muted-foreground">Invoice</p>
          <p className="font-mono text-xs break-all">{invoice}</p>
        </div>
        
        {amount === null ? (
          <div>
            <Badge variant="outline">Amountless Invoice</Badge>
            <p className="text-sm text-muted-foreground mt-2">
              You can specify any amount to pay
            </p>
          </div>
        ) : (
          <div>
            <p className="text-sm text-muted-foreground">Amount</p>
            <p className="text-2xl font-bold">
              {amount.toLocaleString()} sats
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

**Note:** For input components with validation, follow the same pattern: validate with `isValidBolt11Invoice()`, decode with `decodeBolt11Amount()`, and handle null amounts appropriately.

## Part 5: Error Handling & Integration

### Validation Pattern

**Always validate before decoding:**

```typescript
function processInvoice(invoice: string) {
  if (!isValidBolt11Invoice(invoice)) {
    throw new Error('Invalid BOLT11 invoice format');
  }
  const amount = decodeBolt11Amount(invoice);
  // amount may be null for amountless invoices
}
```

### Integration Example

**Complete payment flow with QR code and clipboard support:**

```typescript
// hooks/useLightningPayment.ts
import { useState } from 'react';
import { decodeBolt11Amount, isValidBolt11Invoice } from '@/lib/bolt11Decoder';
// optional import { useToast } from '@/hooks/useToast';

export function useLightningPayment() {
  // Optional: User feedback notifications
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: Toast notifications (if useToast hook is available)
  // const { toast } = useToast();
  // Option 3: No notification handler
  const [isProcessing, setIsProcessing] = useState(false);

  const processInvoice = async (invoiceString: string) => {
    if (!isValidBolt11Invoice(invoiceString)) {
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.error('Invalid Invoice');
      // Option 2: Toast notification (if toast is available)
      // toast({ variant: 'destructive', title: 'Invalid Invoice' });
      // Option 3: No notification (silent failure)
      return;
    }

    const amount = decodeBolt11Amount(invoiceString);
    
    if (amount === null) {
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.log('Amountless Invoice: Please specify amount');
      // Option 2: Toast notification (if toast is available)
      // toast({ title: 'Amountless Invoice', description: 'Please specify amount' });
      // Option 3: No notification (silent)
      return;
    }

    setIsProcessing(true);
    try {
      await payInvoice(invoiceString, amount);
    } catch (error) {
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.error('Payment Failed');
      // Option 2: Toast notification (if toast is available)
      // toast({ variant: 'destructive', title: 'Payment Failed' });
      // Option 3: No notification (silent failure)
    } finally {
      setIsProcessing(false);
    }
  };

  // QR code scan handler
  const handleQRScan = (decodedText: string) => {
    if (isValidBolt11Invoice(decodedText)) {
      processInvoice(decodedText);
    }
  };

  // Clipboard paste handler
  const handlePaste = async () => {
    const text = await navigator.clipboard.readText();
    if (isValidBolt11Invoice(text)) {
      processInvoice(text);
    }
  };

  return { processInvoice, handleQRScan, handlePaste, isProcessing };
}
```

## Part 6: Testing

**Unit tests for decoder functions:**

```typescript
// lib/__tests__/bolt11Decoder.test.ts
import { describe, it, expect } from 'vitest';
import { decodeBolt11Amount, isValidBolt11Invoice } from '../bolt11Decoder';

describe('isValidBolt11Invoice', () => {
  it('validates valid invoices', () => {
    expect(isValidBolt11Invoice('lnbc100n1p...')).toBe(true);
  });
  it('rejects invalid formats', () => {
    expect(isValidBolt11Invoice('invalid')).toBe(false);
  });
});

describe('decodeBolt11Amount', () => {
  it('decodes amounts correctly', () => {
    expect(decodeBolt11Amount('lnbc100n1p...')).toBe(1000); // 100 nano = 1k sats
    expect(decodeBolt11Amount('lnbc500u1p...')).toBe(50000); // 500 micro = 50k sats
  });
  it('returns null for amountless invoices', () => {
    expect(decodeBolt11Amount('lnbc1p...')).toBe(null);
  });
});
```

## Security & Troubleshooting

### Security Considerations

- ✅ Always validate input before processing
- ✅ Don't expose internal errors to users
- ✅ Validate decoded amounts are reasonable

### Common Issues

**Returns null for valid invoices:** Check invoice starts with `lnbc`, has sufficient length (>20 chars), contains bech32 separator `1`

**Wrong amount decoded:** Verify denomination suffix (m, u, n, p) and multiplier calculation

**Amountless invoice not detected:** Amountless invoices have no amount in prefix: `lnbc1...`

### Network Support

**Add testnet support:**

```typescript
function isValidBolt11Invoice(invoice: string, network: 'mainnet' | 'testnet' = 'mainnet'): boolean {
  const prefix = network === 'mainnet' ? 'lnbc' : 'lntb';
  return normalized.startsWith(prefix) && /* ... rest of validation */;
}
```