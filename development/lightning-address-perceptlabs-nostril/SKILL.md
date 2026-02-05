---
name: lightning-address
description: Use when implementing Lightning address functionality - provides complete patterns for resolving Lightning addresses to invoices, generating invoices from addresses, displaying Lightning addresses in UI, and integrating with QR codes
when_to_use: When adding Lightning address support, implementing LNURL-pay protocol, generating invoices from Lightning addresses, displaying Lightning addresses in wallet UIs, or integrating Lightning addresses with QR code functionality
---

# Lightning Address Implementation

## Overview

Complete implementation guide for Lightning addresses (LNURL-pay protocol). Supports resolving Lightning addresses to invoices, generating invoices with amount and optional comments, displaying Lightning addresses in UI, and integrating with QR code functionality.

**Core Capabilities:**
- Resolve Lightning addresses to invoices via LNURL-pay protocol
- Generate invoices from Lightning addresses with amount validation
- Display Lightning addresses in wallet UI with copy/QR functionality
- Handle min/max amount constraints from providers
- Support optional comments in invoice requests
- Comprehensive error handling and validation
- QR code integration for Lightning addresses

## Prerequisites

**No external packages required** - uses native `fetch` API for HTTP requests.

**Optional dependencies:**
- QR code generation (see `qr-code-generator` skill)
- Optional user feedback (console.log, toast notifications, or silent)

## Implementation Checklist

- [ ] Implement Lightning address validation
- [ ] Implement LNURL-pay endpoint resolution
- [ ] Implement invoice generation from Lightning address
- [ ] Add amount validation (min/max bounds)
- [ ] Add optional comment support
- [ ] Create React hook wrapper
- [ ] Add UI components for Lightning address display
- [ ] Integrate with QR code generation
- [ ] Add error handling and user feedback

## Part 1: Understanding Lightning Addresses

### Lightning Address Format

Lightning addresses follow email-like format:
```
username@domain.com
```

**Examples:**
- `alice@strike.me`
- `satoshi@getalby.com`
- `user@npubx.cash`

### LNURL-pay Protocol Flow

Lightning addresses use the LNURL-pay protocol (LNURL specification):

1. **Resolve Address** → Fetch LNURL-pay endpoint
   - URL: `https://domain.com/.well-known/lnurlp/username`
   - Returns: LNURL-pay metadata (min/max amounts, callback URL)

2. **Request Invoice** → Call callback URL with amount
   - URL: `{callback}?amount={millisats}&comment={optional}`
   - Returns: BOLT11 invoice

### LNURL-pay Response Structure

```typescript
interface LNURLPayResponse {
  status: 'OK' | 'ERROR';
  tag: 'payRequest';
  commentAllowed?: number;        // Max comment length in characters
  minSendable: number;            // Minimum amount in millisats
  maxSendable: number;            // Maximum amount in millisats
  metadata: string;               // JSON string with payment metadata
  callback: string;               // URL to request invoice
}
```

### Invoice Response Structure

```typescript
interface LNURLInvoiceResponse {
  status: 'OK' | 'ERROR';
  reason?: string;                // Error reason if status is ERROR
  pr?: string;                    // BOLT11 invoice (payment request)
}
```

## Part 2: Core Implementation

### Lightning Address Validation

**CRITICAL:** Always validate Lightning address format before attempting resolution.

```typescript
// lib/lightningAddress.ts
/**
 * Validate if a string is a valid Lightning address
 * @param address - The string to validate
 * @returns true if the string appears to be a valid Lightning address
 */
export function isValidLightningAddress(address: string): boolean {
  if (!address || typeof address !== 'string') {
    return false;
  }

  const trimmed = address.trim();
  
  // Lightning addresses follow email format: username@domain.com
  // Must contain exactly one @ symbol
  const parts = trimmed.split('@');
  if (parts.length !== 2) {
    return false;
  }

  const [username, domain] = parts;
  
  // Username must be non-empty
  if (!username || username.length === 0) {
    return false;
  }

  // Domain must be valid (contains at least one dot, valid TLD)
  if (!domain || !domain.includes('.')) {
    return false;
  }

  // Basic domain validation (must have TLD)
  const domainParts = domain.split('.');
  if (domainParts.length < 2 || domainParts[domainParts.length - 1].length < 2) {
    return false;
  }

  return true;
}
```

**Usage:**
```typescript
if (isValidLightningAddress(address)) {
  // Safe to resolve
  const invoice = await getInvoiceFromLightningAddress(address, 1000);
} else {
  // Invalid address format
  console.error('Invalid Lightning address format');
}
```

### LNURL-pay Endpoint Resolution

**Resolve Lightning address to LNURL-pay endpoint:**

```typescript
// lib/lightningAddress.ts
/**
 * Resolve Lightning address to LNURL-pay endpoint
 * @param lightningAddress - Lightning address (username@domain.com)
 * @returns LNURL-pay response with metadata
 */
export async function resolveLightningAddress(
  lightningAddress: string
): Promise<LNURLPayResponse> {
  // Validate input
  if (!isValidLightningAddress(lightningAddress)) {
    throw new Error('Invalid Lightning address format. Expected: username@domain.com');
  }

  // Parse Lightning address
  const [username, domain] = lightningAddress.split('@');
  
  // Construct LNURL-pay endpoint
  const lnurlEndpoint = `https://${domain}/.well-known/lnurlp/${username}`;
  
  // Fetch LNURL-pay metadata
  const response = await fetch(lnurlEndpoint, {
    headers: { 'Accept': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(
      `Failed to resolve Lightning address: ${response.status} ${response.statusText}`
    );
  }

  const data: LNURLPayResponse = await response.json();

  // Validate response
  if (data.status && data.status !== 'OK') {
    throw new Error('LNURL endpoint returned error status');
  }

  if (data.tag !== 'payRequest') {
    throw new Error(`Unexpected LNURL tag: ${data.tag}`);
  }

  return data;
}
```

### Invoice Generation

**Generate invoice from Lightning address:**

```typescript
// lib/lightningAddress.ts
interface GetInvoiceParams {
  lightningAddress: string;
  amountSats: number;
  comment?: string;
}

/**
 * Get BOLT11 invoice from Lightning address
 * @param params - Lightning address, amount in sats, and optional comment
 * @returns BOLT11 invoice string
 * @throws Error if resolution fails
 */
export async function getInvoiceFromLightningAddress(
  params: GetInvoiceParams
): Promise<string> {
  const { lightningAddress, amountSats, comment } = params;

  // Validate inputs
  if (!isValidLightningAddress(lightningAddress)) {
    throw new Error('Invalid Lightning address format. Expected: username@domain.com');
  }

  if (amountSats <= 0) {
    throw new Error('Amount must be greater than 0');
  }

  // Step 1: Resolve LNURL-pay endpoint
  const lnurlData = await resolveLightningAddress(lightningAddress);

  // Step 2: Validate amount against min/max bounds
  const minSats = lnurlData.minSendable / 1000;
  const maxSats = lnurlData.maxSendable / 1000;

  if (amountSats < minSats) {
    throw new Error(`Amount ${amountSats} sats is below minimum ${minSats} sats`);
  }

  if (amountSats > maxSats) {
    throw new Error(`Amount ${amountSats} sats exceeds maximum ${maxSats} sats`);
  }

  // Step 3: Request invoice from callback URL
  const amountMsats = amountSats * 1000;
  const callbackUrl = new URL(lnurlData.callback);
  callbackUrl.searchParams.set('amount', amountMsats.toString());

  // Add comment if provided and allowed
  if (comment && lnurlData.commentAllowed) {
    if (comment.length > lnurlData.commentAllowed) {
      throw new Error(
        `Comment length ${comment.length} exceeds maximum ${lnurlData.commentAllowed} characters`
      );
    }
    callbackUrl.searchParams.set('comment', comment);
  }

  // Fetch invoice
  const invoiceResponse = await fetch(callbackUrl.toString(), {
    headers: { 'Accept': 'application/json' },
  });

  if (!invoiceResponse.ok) {
    throw new Error(
      `Failed to get invoice: ${invoiceResponse.status} ${invoiceResponse.statusText}`
    );
  }

  const invoiceData: LNURLInvoiceResponse = await invoiceResponse.json();

  // Check if we have a valid invoice
  if (invoiceData.pr) {
    return invoiceData.pr;
  }

  // If no invoice but has status field, check for errors
  if (invoiceData.status && invoiceData.status !== 'OK') {
    const errorReason = invoiceData.reason || 'Invoice generation failed';
    throw new Error(`Invoice generation failed: ${errorReason}`);
  }

  // If we get here, no invoice was provided
  throw new Error('No invoice returned from provider');
}
```

**Usage:**
```typescript
try {
  const invoice = await getInvoiceFromLightningAddress({
    lightningAddress: 'alice@strike.me',
    amountSats: 1000,
    comment: 'Thanks for the coffee!'
  });
  // Use invoice for payment
} catch (error) {
  console.error('Failed to get invoice:', error);
}
```

## Part 3: React Hook Implementation

### Custom Hook

**Create a React hook for Lightning address operations:**

```typescript
// hooks/useLightningAddress.ts
import { useState, useCallback } from 'react';
import { getInvoiceFromLightningAddress, isValidLightningAddress } from '@/lib/lightningAddress';
import type { GetInvoiceParams } from '@/lib/lightningAddress';

interface UseLightningAddressReturn {
  getInvoice: (params: GetInvoiceParams) => Promise<string>;
  isLoading: boolean;
  error: string | null;
}

/**
 * Hook for resolving Lightning addresses to invoices
 * 
 * @example
 * ```tsx
 * const { getInvoice, isLoading, error } = useLightningAddress();
 * 
 * const invoice = await getInvoice({
 *   lightningAddress: 'alice@strike.me',
 *   amountSats: 1000,
 *   comment: 'Thanks for the coffee!'
 * });
 * ```
 */
export function useLightningAddress(): UseLightningAddressReturn {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetches a Lightning invoice for the given address and amount
   * 
   * @param params - Lightning address, amount in sats, and optional comment
   * @returns BOLT11 invoice string
   * @throws Error if resolution fails
   */
  const getInvoice = useCallback(async (params: GetInvoiceParams): Promise<string> => {
    setIsLoading(true);
    setError(null);

    try {
      const invoice = await getInvoiceFromLightningAddress(params);
      setIsLoading(false);
      return invoice;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      setIsLoading(false);
      throw err;
    }
  }, []);

  return {
    getInvoice,
    isLoading,
    error,
  };
}
```

**Usage in components:**
```typescript
function PaymentForm() {
  const { getInvoice, isLoading, error } = useLightningAddress();
  const [lightningAddress, setLightningAddress] = useState('');
  const [amount, setAmount] = useState(0);

  const handlePay = async () => {
    try {
      const invoice = await getInvoice({
        lightningAddress,
        amountSats: amount,
      });
      // Process payment with invoice
    } catch (error) {
      // Error already set in hook
    }
  };

  return (
    <form onSubmit={handlePay}>
      <input
        value={lightningAddress}
        onChange={(e) => setLightningAddress(e.target.value)}
        placeholder="alice@strike.me"
      />
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(Number(e.target.value))}
        placeholder="Amount in sats"
      />
      {error && <div className="error">{error}</div>}
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Get Invoice'}
      </button>
    </form>
  );
}
```

## Part 4: UI Components

### Lightning Address Display Component

**Display Lightning address with copy and QR functionality:**

```typescript
// components/LightningAddressDisplay.tsx
import { useState } from 'react';
import { Copy, Check, QrCode } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useCopyToClipboard } from '@/hooks/useCopyToClipboard';
import { useQRCode } from '@/hooks/useQRCode';
import { QRModal } from '@/components/ui/qr-modal';

interface LightningAddressDisplayProps {
  lightningAddress: string;
  className?: string;
}

export function LightningAddressDisplay({
  lightningAddress,
  className,
}: LightningAddressDisplayProps) {
  const [copied, setCopied] = useState(false);
  const [showQR, setShowQR] = useState(false);
  const [qrCodeUrl, setQrCodeUrl] = useState<string>('');
  const { copy } = useCopyToClipboard();
  const { generateQRCode } = useQRCode();

  const handleCopy = async () => {
    await copy(lightningAddress);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleShowQR = async () => {
    const qr = await generateQRCode(lightningAddress);
    setQrCodeUrl(qr);
    setShowQR(true);
  };

  // Parse address for display
  const [username, domain] = lightningAddress.split('@');

  return (
    <>
      <div className={`flex gap-2 items-center ${className}`}>
        <button
          onClick={handleCopy}
          className="flex items-center gap-2 px-3 py-1.5 bg-muted hover:bg-muted/80 rounded-md border text-base font-mono transition-colors flex-1 h-[40px] min-w-0"
          title="Click to copy Lightning address"
        >
          <div className="min-w-0 flex-1 flex items-center">
            <span className="truncate min-w-0 flex-1">{username}</span>
            <span className="flex-shrink-0 text-muted-foreground">@{domain}</span>
          </div>
          {copied ? (
            <Check className="h-4 w-4 text-green-600 flex-shrink-0" />
          ) : (
            <Copy className="h-4 w-4 text-muted-foreground flex-shrink-0" />
          )}
        </button>
        <button
          onClick={handleShowQR}
          className="flex items-center justify-center px-2 py-1.5 hover:bg-muted rounded-md transition-colors h-[40px] w-[42px] flex-shrink-0"
          title="Show QR Code"
        >
          <QrCode className="h-4 w-4" />
        </button>
      </div>

      <QRModal
        isOpen={showQR}
        onClose={() => setShowQR(false)}
        title="Lightning Address"
        description="Scan this QR code to send a payment"
        qrCodeUrl={qrCodeUrl}
        content={lightningAddress}
        icon="zap"
      />
    </>
  );
}
```

### QR Modal Component

**Reusable QR code modal with expiry support:**

```typescript
// components/ui/qr-modal.tsx
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { X, Copy, Check, QrCode, Zap, Clock } from 'lucide-react';
import { useCopyToClipboard } from '@/hooks/useCopyToClipboard';
import { useEffect, useState } from 'react';

interface QRModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description: string;
  qrCodeUrl: string;
  content: string;
  icon?: 'qr' | 'zap';
  expiryTimestamp?: number;
  onExpiry?: () => void;
}

export function QRModal({
  isOpen,
  onClose,
  title,
  description,
  qrCodeUrl,
  content,
  icon = 'qr',
  expiryTimestamp,
  onExpiry,
}: QRModalProps) {
  const { copy, copied } = useCopyToClipboard();
  const [timeRemaining, setTimeRemaining] = useState<number | null>(null);
  
  const handleCopy = () => {
    copy(content);
  };
  
  // Countdown timer effect
  useEffect(() => {
    if (!isOpen || !expiryTimestamp) return;
    
    const updateTimer = () => {
      const now = Math.floor(Date.now() / 1000);
      const remaining = expiryTimestamp - now;
      
      if (remaining <= 0) {
        setTimeRemaining(0);
        if (onExpiry) {
          onExpiry();
        }
        onClose();
      } else {
        setTimeRemaining(remaining);
      }
    };
    
    updateTimer();
    const interval = setInterval(updateTimer, 1000);
    
    return () => clearInterval(interval);
  }, [isOpen, expiryTimestamp, onExpiry, onClose]);
  
  // Format time remaining as MM:SS
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };
  
  if (!isOpen) return null;

  const IconComponent = icon === 'zap' ? Zap : QrCode;

  return (
    <div 
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <Card 
        className="w-full max-w-md border-0 shadow-lg bg-background"
        onClick={(e) => e.stopPropagation()}
      >
        <CardHeader className="relative">
          <Button
            onClick={onClose}
            className="absolute top-2 right-2"
            size="sm"
            variant="ghost"
          >
            <X className="h-4 w-4" />
          </Button>
          <CardTitle className="flex items-center pr-8">
            <IconComponent className="h-5 w-5 mr-2" />
            {title}
          </CardTitle>
          <CardDescription>
            {description}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {expiryTimestamp && timeRemaining !== null && timeRemaining <= 3600 && (
            <div className="flex items-center justify-center gap-2 text-sm">
              <Clock className="h-4 w-4" />
              <span className={timeRemaining < 60 ? "text-destructive font-semibold" : "text-muted-foreground"}>
                Expires in {formatTime(timeRemaining)}
              </span>
            </div>
          )}
          <div className="flex justify-center">
            <div className="bg-white p-4 rounded-lg border shadow-sm">
              <img
                src={qrCodeUrl}
                alt={`${title} QR Code`}
                className="w-64 h-64 object-contain"
              />
            </div>
          </div>
          
          <div className="text-center">
            <div 
              className="bg-muted p-3 rounded-lg border font-mono text-sm cursor-pointer hover:bg-muted/80 transition-colors relative group"
              onClick={handleCopy}
              title="Click to copy full content"
            >
              {content.length > 33 
                ? `${content.substring(0, 15)}...${content.substring(content.length - 15)}` 
                : content}
              <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                {copied ? (
                  <Check className="h-4 w-4 text-green-600" />
                ) : (
                  <Copy className="h-4 w-4 text-muted-foreground" />
                )}
              </div>
            </div>
          </div>
          
        </CardContent>
      </Card>
    </div>
  );
}
```

### Integration in Wallet Header

**Example integration showing Lightning address in wallet header:**

```typescript
// components/wallet/WalletHeader.tsx (excerpt)
import { LightningAddressDisplay } from '@/components/LightningAddressDisplay';

export function WalletHeader({
  userPubkey,
  npubCashUsername,
  mode,
  // ... other props
}: WalletHeaderProps) {
  return (
    <div className="flex flex-col items-center pt-10 space-y-2">
      {/* ... balance display ... */}

      {/* Lightning Address Row */}
      {userPubkey && mode === 'lightning' && npubCashUsername && (
        <div className="mt-3 px-4 w-full max-w-[400px] mx-auto">
          <LightningAddressDisplay
            lightningAddress={`${npubCashUsername}@npubx.cash`}
          />
        </div>
      )}
    </div>
  );
}
```

## Part 5: Error Handling & Validation

### Comprehensive Error Handling

**Handle all error cases gracefully:**

```typescript
// lib/lightningAddress.ts
export class LightningAddressError extends Error {
  constructor(
    message: string,
    public code: 'INVALID_FORMAT' | 'RESOLUTION_FAILED' | 'AMOUNT_INVALID' | 'INVOICE_FAILED',
    public originalError?: Error
  ) {
    super(message);
    this.name = 'LightningAddressError';
  }
}

export async function getInvoiceFromLightningAddress(
  params: GetInvoiceParams
): Promise<string> {
  try {
    // Validate format
    if (!isValidLightningAddress(params.lightningAddress)) {
      throw new LightningAddressError(
        'Invalid Lightning address format. Expected: username@domain.com',
        'INVALID_FORMAT'
      );
    }

    // Validate amount
    if (params.amountSats <= 0) {
      throw new LightningAddressError(
        'Amount must be greater than 0',
        'AMOUNT_INVALID'
      );
    }

    // Resolve and get invoice
    const lnurlData = await resolveLightningAddress(params.lightningAddress);
    
    // ... rest of implementation with proper error handling
  } catch (error) {
    if (error instanceof LightningAddressError) {
      throw error;
    }
    
    // Wrap unknown errors
    throw new LightningAddressError(
      error instanceof Error ? error.message : 'Unknown error occurred',
      'INVOICE_FAILED',
      error instanceof Error ? error : undefined
    );
  }
}
```

### User-Friendly Error Messages

**Provide helpful error messages in UI:**

```typescript
// components/LightningAddressForm.tsx
function LightningAddressForm() {
  const { getInvoice, isLoading, error } = useLightningAddress();
  // Optional: User feedback notifications
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: Toast notifications (if useToast hook is available)
  // const { toast } = useToast();
  // Option 3: No notification handler

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const invoice = await getInvoice({
        lightningAddress: formData.address,
        amountSats: formData.amount,
      });
      // Process invoice
    } catch (error) {
      let message = 'Failed to get invoice';
      
      if (error instanceof LightningAddressError) {
        switch (error.code) {
          case 'INVALID_FORMAT':
            message = 'Invalid Lightning address. Use format: username@domain.com';
            break;
          case 'AMOUNT_INVALID':
            message = error.message;
            break;
          case 'RESOLUTION_FAILED':
            message = 'Could not resolve Lightning address. Check your connection.';
            break;
          case 'INVOICE_FAILED':
            message = 'Failed to generate invoice. Please try again.';
            break;
        }
      }
      
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.error('Failed to get invoice:', message);
      // Option 2: Toast notification (if toast is available)
      // toast({ variant: 'destructive', title: 'Error', description: message });
      // Option 3: No notification (silent failure)
    }
  };

  // ... rest of component
}
```

## Part 6: Advanced Features

### Amount Validation with Min/Max Display

**Show min/max amounts to users:**

```typescript
// hooks/useLightningAddressInfo.ts
import { useState, useCallback } from 'react';
import { resolveLightningAddress } from '@/lib/lightningAddress';

interface LightningAddressInfo {
  minSats: number;
  maxSats: number;
  commentAllowed?: number;
}

export function useLightningAddressInfo() {
  const [info, setInfo] = useState<LightningAddressInfo | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchInfo = useCallback(async (lightningAddress: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const lnurlData = await resolveLightningAddress(lightningAddress);
      setInfo({
        minSats: lnurlData.minSendable / 1000,
        maxSats: lnurlData.maxSendable / 1000,
        commentAllowed: lnurlData.commentAllowed,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch info');
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { info, fetchInfo, isLoading, error };
}
```

**Usage:**
```typescript
function PaymentForm({ lightningAddress }: { lightningAddress: string }) {
  const { info, fetchInfo, isLoading } = useLightningAddressInfo();
  const [amount, setAmount] = useState(0);

  useEffect(() => {
    fetchInfo(lightningAddress);
  }, [lightningAddress, fetchInfo]);

  return (
    <form>
      {info && (
        <div className="text-sm text-muted-foreground">
          Amount range: {info.minSats.toLocaleString()} - {info.maxSats.toLocaleString()} sats
        </div>
      )}
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(Number(e.target.value))}
        min={info?.minSats}
        max={info?.maxSats}
      />
    </form>
  );
}
```

### Comment Input with Length Validation

**Add comment input with character limit:**

```typescript
// components/LightningAddressPaymentForm.tsx
function LightningAddressPaymentForm({ lightningAddress }: { lightningAddress: string }) {
  const { info, fetchInfo } = useLightningAddressInfo();
  const { getInvoice } = useLightningAddress();
  const [comment, setComment] = useState('');

  useEffect(() => {
    fetchInfo(lightningAddress);
  }, [lightningAddress, fetchInfo]);

  const maxCommentLength = info?.commentAllowed || 0;
  const canAddComment = maxCommentLength > 0;

  return (
    <form>
      {/* Amount input */}
      
      {canAddComment && (
        <div>
          <label>
            Comment (optional)
            {maxCommentLength > 0 && (
              <span className="text-sm text-muted-foreground">
                {' '}(max {maxCommentLength} characters)
              </span>
            )}
          </label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            maxLength={maxCommentLength}
            rows={2}
          />
          <div className="text-xs text-muted-foreground text-right">
            {comment.length} / {maxCommentLength}
          </div>
        </div>
      )}
    </form>
  );
}
```

## Part 7: Testing

### Unit Tests

**Test Lightning address validation and resolution:**

```typescript
// lib/__tests__/lightningAddress.test.ts
import { describe, it, expect, vi } from 'vitest';
import { isValidLightningAddress, getInvoiceFromLightningAddress } from '../lightningAddress';

describe('isValidLightningAddress', () => {
  it('validates valid addresses', () => {
    expect(isValidLightningAddress('alice@strike.me')).toBe(true);
    expect(isValidLightningAddress('user@domain.com')).toBe(true);
  });

  it('rejects invalid formats', () => {
    expect(isValidLightningAddress('invalid')).toBe(false);
    expect(isValidLightningAddress('@domain.com')).toBe(false);
    expect(isValidLightningAddress('user@')).toBe(false);
    expect(isValidLightningAddress('user@domain')).toBe(false);
  });
});

describe('getInvoiceFromLightningAddress', () => {
  it('resolves address and gets invoice', async () => {
    // Mock fetch responses
    global.fetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          status: 'OK',
          tag: 'payRequest',
          minSendable: 1000,
          maxSendable: 1000000000,
          callback: 'https://strike.me/api/invoice',
          metadata: '[]',
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          status: 'OK',
          pr: 'lnbc100n1p...',
        }),
      });

    const invoice = await getInvoiceFromLightningAddress({
      lightningAddress: 'alice@strike.me',
      amountSats: 1000,
    });

    expect(invoice).toBe('lnbc100n1p...');
  });

  it('validates amount against min/max', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        status: 'OK',
        tag: 'payRequest',
        minSendable: 10000, // 10 sats
        maxSendable: 1000000, // 1000 sats
        callback: 'https://strike.me/api/invoice',
        metadata: '[]',
      }),
    });

    await expect(
      getInvoiceFromLightningAddress({
        lightningAddress: 'alice@strike.me',
        amountSats: 5, // Below minimum
      })
    ).rejects.toThrow('below minimum');
  });
});
```

## Part 8: Common Pitfalls

### 1. ❌ Not validating address format

**Problem:** Attempting to resolve invalid addresses causes unnecessary API calls.

**Solution:** Always validate format first:
```typescript
if (!isValidLightningAddress(address)) {
  throw new Error('Invalid Lightning address format');
}
```

### 2. ❌ Not checking amount bounds

**Problem:** Requesting invoices with amounts outside provider limits causes errors.

**Solution:** Always validate against min/max from LNURL-pay response:
```typescript
if (amountSats < minSats || amountSats > maxSats) {
  throw new Error('Amount out of range');
}
```

### 3. ❌ Not handling comment length limits

**Problem:** Sending comments longer than allowed causes invoice generation to fail.

**Solution:** Check `commentAllowed` and validate length:
```typescript
if (comment && lnurlData.commentAllowed && comment.length > lnurlData.commentAllowed) {
  throw new Error('Comment too long');
}
```

### 4. ❌ Not handling HTTP errors

**Problem:** Network failures or provider errors cause unhandled exceptions.

**Solution:** Always check response status and handle errors:
```typescript
if (!response.ok) {
  throw new Error(`Failed: ${response.status} ${response.statusText}`);
}
```

### 5. ❌ Not converting sats to millisats

**Problem:** LNURL-pay uses millisats, but amounts are often in sats.

**Solution:** Always convert when calling callback URL:
```typescript
const amountMsats = amountSats * 1000;
callbackUrl.searchParams.set('amount', amountMsats.toString());
```

### 6. ❌ Not handling optional invoice fields

**Problem:** Some providers return invoices without `status` field, causing validation to fail.

**Solution:** Check for invoice first, then status:
```typescript
if (invoiceData.pr) {
  return invoiceData.pr; // Invoice present, return it
}

if (invoiceData.status && invoiceData.status !== 'OK') {
  throw new Error(invoiceData.reason || 'Invoice generation failed');
}
```

## Security Considerations

1. **Validate all inputs** - Don't trust user-provided addresses or amounts
2. **Sanitize comments** - Some providers may have restrictions on comment content
3. **Handle errors gracefully** - Don't expose internal errors to users
4. **Rate limiting** - Consider rate limiting invoice requests to prevent abuse
5. **HTTPS only** - Always use HTTPS for LNURL-pay endpoints

## Verification Checklist

- [ ] Lightning address validation works correctly
- [ ] LNURL-pay endpoint resolution handles errors
- [ ] Amount validation against min/max bounds
- [ ] Comment support with length validation
- [ ] Invoice generation from callback URL
- [ ] Error handling for all failure cases
- [ ] UI components display addresses correctly
- [ ] QR code integration works
- [ ] Copy to clipboard functionality
- [ ] Loading states displayed during resolution
- [ ] User-friendly error messages

## Summary

To implement Lightning address functionality:

1. **Validate format** - Use `isValidLightningAddress()` before resolution
2. **Resolve endpoint** - Fetch LNURL-pay metadata from `.well-known/lnurlp/` endpoint
3. **Validate amount** - Check against min/max bounds from provider
4. **Request invoice** - Call callback URL with amount (and optional comment)
5. **Handle errors** - Provide user-friendly error messages for all failure cases
6. **Display in UI** - Show address with copy/QR functionality
7. **Test thoroughly** - Test validation, resolution, and error cases

**Key principle:** Lightning addresses use the LNURL-pay protocol - always resolve the endpoint first to get metadata (min/max amounts, callback URL) before requesting invoices.

