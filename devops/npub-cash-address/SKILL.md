---
name: npub-cash-address
description: Use when implementing npub.cash static Lightning address functionality - provides complete patterns for obtaining static Lightning addresses (username@npubx.cash), managing npub.cash account settings, syncing quotes from npub.cash, and integrating with Lightning wallets
when_to_use: When building Lightning wallet features that need static addresses, implementing npub.cash integration, managing user Lightning addresses, or syncing quotes from npub.cash to Cashu wallets
---

# npub.cash Static Lightning Address Implementation

## Overview

Complete implementation guide for integrating with npub.cash to obtain static Lightning addresses for users. npub.cash provides a service that generates static Lightning addresses in the format `username@npubx.cash` based on a user's Nostr public key, allowing users to receive Lightning payments at a permanent address.

**Core Capabilities:**
- Obtain static Lightning address from npub.cash (`username@npubx.cash`)
- Manage npub.cash account settings (mint URL, lock quotes)
- Sync quotes from npub.cash to Cashu wallet
- Real-time quote subscription and updates
- NIP-98 authentication with npub.cash API
- Automatic mint management when syncing quotes

**Note:** This skill is **optional** for `lightning-wallet` implementations. Users can optionally use npub.cash to get a static Lightning address, but it's not required for basic Lightning wallet functionality.

## Prerequisites

**IMPORTANT:** Before adding dependencies, review your project's `package.json` to check if any of these packages already exist. If they do, verify the versions are compatible with the requirements below. Only add packages that are missing or need version updates.

**Required packages:**
- `npubcash-sdk@^0.2.0` - Official npub.cash SDK (minimum version 0.2.0, later versions acceptable)
- `npubcash-types` - TypeScript types for npub.cash (if not included in SDK)
- `nostr-tools@^2.13.0` - Nostr protocol utilities (for NIP-98 authentication)

**Required skills (must be referenced/implemented):**
- `qr-code-generator` - QR code generation for displaying Lightning addresses (see `qr-code-generator` skill)
- `lightning-wallet` - Lightning wallet operations (optional integration target)

**Optional dependencies:**
- NIP-98 authentication hook (for Nostr-based authentication)

## Implementation Checklist

- [ ] Set up NIP-98 authentication with npub.cash
- [ ] Initialize npubcash-sdk client
- [ ] Implement user info retrieval (get static Lightning address)
- [ ] Implement QR code generation for Lightning address (see `qr-code-generator` skill)
- [ ] Implement copy to clipboard functionality (see `bitcoin-wallet` skill for copy hook)
- [ ] Implement mint URL management
- [ ] Implement quote syncing from npub.cash
- [ ] Add real-time quote subscription
- [ ] Integrate with Lightning wallet (optional)
- [ ] Add error handling and user feedback

## Part 1: Understanding npub.cash Static Addresses

### Static Address vs Dynamic Invoices

**Static Lightning Address:**
- Format: `username@npubx.cash`
- Permanent address tied to user's Nostr pubkey
- Others can send payments to this address at any time
- npub.cash generates invoices on-demand when payments are received
- User doesn't need to create invoices manually

**Dynamic Invoices:**
- Created on-demand by user
- Expire after a set time
- User must generate and share each invoice
- More control but less convenient for recurring payments

### npub.cash Service

npub.cash provides:
- **Static addresses**: `username@npubx.cash` format
- **Quote management**: Tracks pending Lightning payments
- **Mint integration**: Links user's preferred Cashu mint
- **Real-time updates**: WebSocket subscription for quote updates

### Difference from lightning-address Skill

**This skill (`npub-cash-address`):**
- **Obtains** a static Lightning address from npub.cash
- Creates/manages the user's address on npub.cash
- Syncs quotes from npub.cash to wallet

**`lightning-address` skill:**
- **Resolves** any Lightning address to an invoice
- Takes an address (like `alice@strike.me`) and gets an invoice
- Works with any Lightning address provider

## Part 2: Core Implementation

### NIP-98 Authentication Setup

**Set up NIP-98 authentication for npub.cash API:**

```typescript
// hooks/useNIP98.ts (prerequisite)
import { useCallback } from 'react';
import { useCurrentUser } from './useCurrentUser';
import type { NostrEvent } from '@nostrify/nostrify';

export interface NIP98Options {
  url: string;
  method: string;
  body?: unknown;
}

/**
 * Hook for creating NIP-98 HTTP Authentication headers
 * Based on https://github.com/nostr-protocol/nips/blob/master/98.md
 */
export function useNIP98() {
  const { user } = useCurrentUser();

  /**
   * Create a NIP-98 authorization header for HTTP requests
   * @param options - The request details (url, method, optional body)
   * @returns Promise<string> - The "Nostr base64..." authorization header value
   */
  const createAuthHeader = useCallback(async (options: NIP98Options): Promise<string> => {
    if (!user) {
      throw new Error('User must be logged in to create NIP-98 auth header');
    }

    const { url, method, body } = options;
    
    // Parse URL to remove query parameters (per NIP-98 spec)
    const urlObj = new URL(url);
    const urlWithoutQuery = `${urlObj.protocol}//${urlObj.host}${urlObj.pathname}`;

    const tags: string[][] = [
      ['u', urlWithoutQuery],
      ['method', method.toUpperCase()],
    ];

    // If there's a request body (POST, PUT, PATCH), add payload hash
    if (body && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
      const bodyString = JSON.stringify(body);
      const encoder = new TextEncoder();
      const data = encoder.encode(bodyString);
      const hashBuffer = await crypto.subtle.digest('SHA-256', data);
      const payloadHash = Array.from(new Uint8Array(hashBuffer))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
      
      tags.push(['payload', payloadHash]);
    }

    // Create and sign the NIP-98 event (kind 27235)
    const event = await user.signer.signEvent({
      kind: 27235,
      content: '',
      tags,
      created_at: Math.floor(Date.now() / 1000),
    }) as NostrEvent;

    // Encode the event as base64
    const eventJson = JSON.stringify(event);
    const base64Event = btoa(eventJson);

    return `Nostr ${base64Event}`;
  }, [user]);

  return {
    createAuthHeader,
    isLoggedIn: !!user,
    pubkey: user?.pubkey,
    signer: user?.signer,
  };
}
```

**Key Points:**
- **NIP-98 Event**: Creates a kind 27235 event with URL and method tags
- **URL Parsing**: Removes query parameters per NIP-98 specification
- **Payload Hashing**: For POST/PUT/PATCH requests, includes SHA-256 hash of request body
- **Base64 Encoding**: Encodes signed event as base64 for HTTP Authorization header
- **Format**: Returns `"Nostr {base64Event}"` format for Authorization header

### npub.cash Hook Implementation

**Complete hook for npub.cash integration:**

```typescript
// hooks/wallet/useNpubCash.ts
import { useCallback, useState, useMemo, useRef } from 'react';
import { useNIP98 } from '../useNIP98';
import { NPCClient, JWTAuthProvider } from 'npubcash-sdk';
import type { Quote } from 'npubcash-types';
import type { Manager } from 'coco-cashu-core';
import type { EventTemplate, Event } from 'nostr-tools';
// optional import { useToast } from '@/hooks/useToast';

const NPUBCASH_BASE_URL = 'https://npubx.cash';

export interface NpubCashUserInfo {
  pubkey: string;
  name?: string;
  mintUrl: string; // API returns camelCase
  lockQuote: boolean; // API returns camelCase
}

/**
 * Hook for interacting with npub.cash API using the official SDK
 */
export function useNpubCash() {
  const { createAuthHeader, signer, isLoggedIn, pubkey } = useNIP98();
  // Optional: User feedback notifications
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: Toast notifications (if useToast hook is available)
  // const { toast } = useToast();
  // Option 3: No notification handler
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Ref to track last sync timestamp for incremental updates
  const lastSyncRef = useRef<number>(0);

  // Create NPCClient instance using the SDK with JWTAuthProvider for proper WebSocket auth
  const npcClient = useMemo(() => {
    if (!isLoggedIn || !signer) return null;
    // Adapt NostrSigner to JWTAuthProvider's expected SigningFunc signature
    const signingFunc = async (eventTemplate: EventTemplate): Promise<Event> => {
      return await signer.signEvent(eventTemplate);
    };
    const auth = new JWTAuthProvider(NPUBCASH_BASE_URL, signingFunc);
    return new NPCClient(NPUBCASH_BASE_URL, auth);
  }, [isLoggedIn, signer]);

  // Generic wrapper for SDK calls with loading state
  const withLoading = useCallback(async <T>(operation: () => Promise<T>): Promise<T | null> => {
    try {
      setIsLoading(true);
      setError(null);
      return await operation();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const setMint = useCallback(async (mintUrl: string): Promise<boolean> => {
    if (!npcClient) return false;
    const result = await withLoading(() => npcClient.settings.setMintUrl(mintUrl));
    return result !== null;
  }, [npcClient, withLoading]);

  const getUserInfo = useCallback(async (): Promise<NpubCashUserInfo | null> => {
    if (!npcClient) return null;
    
    // Since SDK doesn't have getUserInfo, we'll use manual implementation
    return withLoading(async () => {
      const url = `${NPUBCASH_BASE_URL}/api/v2/user/info`;
      const authHeader = await createAuthHeader({ url, method: 'GET' });
      
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Authorization': authHeader, 'Content-Type': 'application/json' },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Failed to get user info (${response.status})`);
      }

      const data = await response.json();
      return data.data.user;
    });
  }, [npcClient, createAuthHeader, withLoading]);

  const getAllQuotes = useCallback(async (): Promise<Quote[]> => {
    if (!npcClient) return [];
    const result = await withLoading(() => npcClient.getAllQuotes());
    return result || [];
  }, [npcClient, withLoading]);

  const getQuotesSince = useCallback(async (since: number): Promise<Quote[]> => {
    if (!npcClient) return [];
    const result = await withLoading(() => npcClient.getQuotesSince(since));
    return result || [];
  }, [npcClient, withLoading]);

  const setLockQuotes = useCallback(async (lockQuotes: boolean): Promise<boolean> => {
    if (!npcClient) return false;
    const result = await withLoading(() => npcClient.settings.setLock(lockQuotes));
    return result !== null;
  }, [npcClient, withLoading]);

  const subscribeToQuotes = useCallback((
    onUpdate: (quoteId: string) => void,
    onError?: (msg: string) => void
  ) => {
    if (!npcClient) return () => {};
    return npcClient.subscribe(onUpdate, onError);
  }, [npcClient]);

  const clearError = useCallback(() => setError(null), []);

  return {
    // Core methods
    setMint,
    getUserInfo,
    
    // Quote management methods
    getAllQuotes,
    getQuotesSince,
    setLockQuotes,
    subscribeToQuotes,
    
    // Status
    isLoading,
    error,
    isLoggedIn,
    pubkey,
    clearError,
    
    // SDK instance for advanced usage
    npcClient,
  };
}
```

## Part 3: Getting Static Lightning Address

### Retrieving User Info

**Get user's static Lightning address from npub.cash:**

```typescript
// In your component
const { getUserInfo, isLoading, error } = useNpubCash();

// Get user info (includes static address)
const userInfo = await getUserInfo();

if (userInfo) {
  // Extract username from pubkey or use name if available
  const username = userInfo.name || extractUsernameFromPubkey(userInfo.pubkey);
  const staticAddress = `${username}@npubx.cash`;
  
  console.log('Static Lightning address:', staticAddress);
  // Example: "alice@npubx.cash"
}
```

### Displaying Static Address

**Show static address in wallet UI with QR code and copy functionality:**

```typescript
// components/StaticAddressDisplay.tsx
import { useEffect, useState } from 'react';
import { useNpubCash } from '@/hooks/wallet/useNpubCash';
import { useQRCodeGenerator } from '@/hooks/useQRCodeGenerator';
import { useCopyToClipboard } from '@/hooks/useCopyToClipboard';
import { Button } from '@/components/ui/button';
import { Copy, Check } from 'lucide-react';
import { QRModal } from '@/components/QRModal';

export function StaticAddressDisplay() {
  const { getUserInfo, isLoading } = useNpubCash();
  const { generateQRCode, isGenerating: isGeneratingQR } = useQRCodeGenerator();
  const { copy, copied } = useCopyToClipboard();
  const [staticAddress, setStaticAddress] = useState<string | null>(null);
  const [qrCodeUrl, setQrCodeUrl] = useState<string>('');
  const [showQRModal, setShowQRModal] = useState(false);

  useEffect(() => {
    const fetchAddress = async () => {
      const userInfo = await getUserInfo();
      if (userInfo) {
        const username = userInfo.name || extractUsernameFromPubkey(userInfo.pubkey);
        const address = `${username}@npubx.cash`;
        setStaticAddress(address);
        
        // Generate QR code for the address
        const qrUrl = await generateQRCode(address);
        setQrCodeUrl(qrUrl);
      }
    };
    
    fetchAddress();
  }, [getUserInfo, generateQRCode]);

  if (isLoading) {
    return <div>Loading address...</div>;
  }

  if (!staticAddress) {
    return <div>No address available</div>;
  }

  return (
    <div className="space-y-4">
      <h3>Your Lightning Address</h3>
      
      {/* Address display with copy button */}
      <div className="flex items-center gap-2 p-3 bg-muted rounded-lg">
        <code className="flex-1 text-sm break-all">{staticAddress}</code>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => copy(staticAddress)}
          className="h-8 w-8 shrink-0"
          aria-label="Copy address"
        >
          {copied ? (
            <Check className="h-4 w-4 text-green-600" />
          ) : (
            <Copy className="h-4 w-4" />
          )}
        </Button>
      </div>

      {/* QR code display */}
      {qrCodeUrl && (
        <div className="flex flex-col items-center gap-2">
          <img
            src={qrCodeUrl}
            alt="QR Code"
            className="w-48 h-48 cursor-pointer"
            onClick={() => setShowQRModal(true)}
          />
          <Button
            variant="outline"
            onClick={() => setShowQRModal(true)}
            disabled={isGeneratingQR}
          >
            {isGeneratingQR ? 'Generating...' : 'View QR Code'}
          </Button>
        </div>
      )}

      {/* QR Modal */}
      <QRModal
        isOpen={showQRModal}
        onClose={() => setShowQRModal(false)}
        qrCodeUrl={qrCodeUrl}
        content={staticAddress}
        title="Lightning Address QR Code"
        description="Scan this QR code to send Lightning payments"
      />
    </div>
  );
}
```

**Key Features:**
- **QR Code Generation** - Uses `qr-code-generator` skill to create QR codes for the Lightning address
- **Copy to Clipboard** - Uses copy hook from `bitcoin-wallet` skill for easy address copying
- **Visual Feedback** - Shows checkmark when address is copied
- **QR Modal** - Full-screen QR code view with copy functionality
- **Accessibility** - Proper ARIA labels and keyboard navigation

### Username Extraction

**Extract username from Nostr pubkey:**

```typescript
// lib/npubCashUtils.ts
export function extractUsernameFromPubkey(pubkey: string): string {
  // npub.cash uses a deterministic username based on pubkey
  // This is typically the first 8-12 characters of the npub
  // You may need to check npub.cash API documentation for exact format
  
  // Example: Use first part of pubkey as username
  // In practice, npub.cash may provide this in the user info
  return pubkey.substring(0, 8);
}

// Or use the name from userInfo if available
const username = userInfo.name || extractUsernameFromPubkey(userInfo.pubkey);
```

## Part 4: Managing npub.cash Settings

### Setting Mint URL

**Configure user's preferred mint on npub.cash:**

```typescript
// In your component
const { setMint, isLoading } = useNpubCash();

// Set mint URL (links npub.cash to user's preferred Cashu mint)
const success = await setMint('https://mint.example.com');

if (success) {
  // Optional: User feedback - choose one:
  // Option 1: Console logging
  // console.log('Mint Updated: Your npub.cash mint has been updated');
  // Option 2: Toast notification (if toast is available)
  // toast({ title: 'Mint Updated', description: 'Your npub.cash mint has been updated' });
  // Option 3: No notification (silent success)
}
```

### Locking Quotes

**Prevent quote modifications (optional security feature):**

```typescript
// In your component
const { setLockQuotes, isLoading } = useNpubCash();

// Lock quotes to prevent modifications
const success = await setLockQuotes(true);

if (success) {
  // Optional: User feedback - choose one:
  // Option 1: Console logging
  // console.log('Quotes Locked: Your quotes are now locked');
  // Option 2: Toast notification (if toast is available)
  // toast({ title: 'Quotes Locked', description: 'Your quotes are now locked' });
  // Option 3: No notification (silent success)
}
```

## Part 5: Quote Syncing with Lightning Wallet

### Syncing Quotes from npub.cash

**Sync quotes from npub.cash to Cashu wallet:**

```typescript
// hooks/wallet/useNpubCash.ts (excerpt)
const refreshQuotes = useCallback(async (coco: Manager): Promise<void> => {
  if (!npcClient || !coco) return;
  
  try {
    // Fetch all quotes from npub.cash
    const quotes = await getAllQuotes();
    
    if (quotes.length === 0) {
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.log('No Quotes Found: No pending quotes found on npub.cash');
      // Option 2: Toast notification (if toast is available)
      // toast({ title: "No Quotes Found", description: "No pending quotes found on npub.cash" });
      // Option 3: No notification (silent)
      return;
    }
    
    // Group quotes by mint URL
    const quotesByMint = quotes.reduce((acc, quote) => {
      if (!acc[quote.mintUrl]) {
        acc[quote.mintUrl] = [];
      }
      acc[quote.mintUrl].push(quote);
      return acc;
    }, {} as Record<string, typeof quotes>);
    
    let addedQuotes = 0;
    
    // Process each mint's quotes
    for (const [mintUrl, mintQuotes] of Object.entries(quotesByMint)) {
      try {
        // Check if mint exists (known) by checking all mints
        const allMints = await coco.mint.getAllMints();
        const isKnown = allMints.some(m => m.mintUrl.toLowerCase() === mintUrl.toLowerCase());
        
        if (!isKnown) {
          await coco.mint.addMint(mintUrl, { trusted: true });
        } else {
          // Mint exists, ensure it's trusted
          const isTrusted = await coco.mint.isTrustedMint(mintUrl);
          if (!isTrusted) {
            await coco.mint.trustMint(mintUrl);
          }
        }
        
        // Add quotes to the wallet
        coco.quotes.addMintQuote(
          mintUrl,
          mintQuotes.map((q) => ({
            ...q,
            expiry: q.expiresAt,
            quote: q.quoteId,
            state: "PAID",
            unit: "sat",
          })),
        );
        
        addedQuotes += mintQuotes.length;
      } catch (err) {
        console.warn(`Failed to process quotes for mint ${mintUrl}:`, err);
      }
    }
    
    if (addedQuotes > 0) {
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.log(`Quotes Refreshed: Successfully added ${addedQuotes} quotes from npub.cash`);
      // Option 2: Toast notification (if toast is available)
      // toast({ title: "Quotes Refreshed", description: `Successfully added ${addedQuotes} quotes from npub.cash` });
      // Option 3: No notification (silent success)
    }
  } catch (err) {
    // Optional: User feedback - choose one:
    // Option 1: Console logging
    // console.error('Quote Refresh Failed:', err instanceof Error ? err.message : 'Unknown error');
    // Option 2: Toast notification (if toast is available)
    // toast({ variant: "destructive", title: "Refresh Failed", description: err instanceof Error ? err.message : 'Failed to refresh quotes' });
    // Option 3: No notification (silent failure)
  }
}, [npcClient, getAllQuotes]);
```

### Real-Time Quote Subscription

**Subscribe to real-time quote updates:**

```typescript
// hooks/wallet/useNpubCash.ts (excerpt)
const syncQuotesWithWallet = useCallback(async (coco: Manager): Promise<() => void> => {
  if (!npcClient || !coco) return () => {};
  
  try {
    // Fetch and sync all quotes initially
    const quotes = await getAllQuotes();
    if (quotes.length > 0) {
      // ... sync initial quotes (see refreshQuotes implementation)
    }
    
    // Subscribe to real-time updates
    const unsubscribe = subscribeToQuotes(
      async (quoteId: string) => {
        try {
          // When a quote is updated, fetch newer quotes and sync
          const recentQuotes = await getQuotesSince(lastSyncRef.current);
          if (recentQuotes.length > 0) {
            // ... sync recent quotes (see refreshQuotes implementation)
            lastSyncRef.current = Math.floor(Date.now() / 1000);
          }
        } catch (err) {
          console.error('Failed to sync quote update:', err);
        }
      },
      (err: string) => {
        console.error('Quote subscription error:', err);
        // Optional: User feedback - choose one:
        // Option 1: Console logging
        // console.error('Sync Error: Failed to sync quotes from npub.cash');
        // Option 2: Toast notification (if toast is available)
        // toast({ variant: "destructive", title: "Sync Error", description: "Failed to sync quotes from npub.cash" });
        // Option 3: No notification (silent failure)
      }
    );
    
    return unsubscribe;
  } catch (err) {
    console.error('Failed to set up quote sync:', err);
    return () => {};
  }
}, [npcClient, getAllQuotes, getQuotesSince, subscribeToQuotes]);
```

**Usage in component:**

```typescript
// In your component
const { syncQuotesWithWallet } = useNpubCash();
const { coco } = useCashu(); // From lightning-wallet skill

useEffect(() => {
  if (!coco || !isLoggedIn) return;
  
  // Set up real-time quote syncing
  const unsubscribe = await syncQuotesWithWallet(coco);
  
  return () => {
    if (unsubscribe) unsubscribe();
  };
}, [coco, isLoggedIn, syncQuotesWithWallet]);
```

## Part 6: Integration with Lightning Wallet

### Optional Integration

**This skill is optional for `lightning-wallet` implementations:**

```typescript
// components/wallet/WalletHeader.tsx (excerpt)
import { useNpubCash } from '@/hooks/wallet/useNpubCash';

export function WalletHeader({ userPubkey, mode }: WalletHeaderProps) {
  const { getUserInfo, isLoading } = useNpubCash();
  const [npubCashUsername, setNpubCashUsername] = useState<string | null>(null);

  useEffect(() => {
    if (userPubkey && mode === 'lightning') {
      // Optionally fetch npub.cash address
      const fetchAddress = async () => {
        const userInfo = await getUserInfo();
        if (userInfo) {
          const username = userInfo.name || extractUsernameFromPubkey(userInfo.pubkey);
          setNpubCashUsername(username);
        }
      };
      fetchAddress();
    }
  }, [userPubkey, mode, getUserInfo]);

  return (
    <div>
      {/* ... other wallet header content ... */}
      
      {/* Optionally show static address if available */}
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

### Syncing Mint Settings

**Sync mint URL between wallet and npub.cash:**

```typescript
// When user changes active mint in wallet
const { setMint } = useNpubCash();
const { activeMintUrl, setActiveMintUrl } = useMintManager({ /* ... */ });

const handleMintChange = async (mintUrl: string) => {
  // Update wallet mint
  await setActiveMintUrl(mintUrl);
  
  // Optionally sync to npub.cash
  if (isNpubCashLoggedIn) {
    await setMint(mintUrl);
  }
};
```

## Part 7: Error Handling

### Authentication Errors

**Handle NIP-98 authentication failures:**

```typescript
const { getUserInfo, error, isLoggedIn } = useNpubCash();

if (!isLoggedIn) {
  return (
    <div>
      <p>Please log in with Nostr to use npub.cash</p>
      <LoginArea />
    </div>
  );
}

if (error) {
  if (error.includes('401') || error.includes('Unauthorized')) {
    // Optional: User feedback - choose one:
    // Option 1: Console logging
    // console.error('Authentication Failed: Please log in again');
    // Option 2: Toast notification (if toast is available)
    // toast({ variant: 'destructive', title: 'Authentication Failed', description: 'Please log in again' });
    // Option 3: No notification (silent failure)
  }
}
```

### API Errors

**Handle npub.cash API errors:**

```typescript
try {
  const userInfo = await getUserInfo();
  if (!userInfo) {
    // Optional: User feedback - choose one:
    // Option 1: Console logging
    // console.error('Failed to Get Address: Could not retrieve your npub.cash address');
    // Option 2: Toast notification (if toast is available)
    // toast({ variant: 'destructive', title: 'Failed to Get Address', description: 'Could not retrieve your npub.cash address' });
    // Option 3: No notification (silent failure)
  }
} catch (err) {
  const errorMessage = err instanceof Error ? err.message : 'Unknown error';
  
  if (errorMessage.includes('404')) {
    // User may not have npub.cash account yet
    // Optional: User feedback - choose one:
    // Option 1: Console logging
    // console.log('No Account: You may need to create an npub.cash account first');
    // Option 2: Toast notification (if toast is available)
    // toast({ title: 'No Account', description: 'You may need to create an npub.cash account first' });
    // Option 3: No notification (silent)
  } else {
    // Optional: User feedback - choose one:
    // Option 1: Console logging
    // console.error('API Error:', errorMessage);
    // Option 2: Toast notification (if toast is available)
    // toast({ variant: 'destructive', title: 'Error', description: errorMessage });
    // Option 3: No notification (silent failure)
  }
}
```

## Part 8: Best Practices

### Lazy Loading

**Only fetch npub.cash data when needed:**

```typescript
// Don't fetch on every render
const [userInfo, setUserInfo] = useState<NpubCashUserInfo | null>(null);
const [hasFetched, setHasFetched] = useState(false);

const fetchUserInfo = useCallback(async () => {
  if (hasFetched) return; // Already fetched
  const info = await getUserInfo();
  setUserInfo(info);
  setHasFetched(true);
}, [getUserInfo, hasFetched]);

// Only fetch when user explicitly requests it or when component mounts
useEffect(() => {
  if (shouldShowAddress) {
    fetchUserInfo();
  }
}, [shouldShowAddress, fetchUserInfo]);
```

### Caching User Info

**Cache user info to avoid repeated API calls:**

```typescript
// Use React Query or similar for caching
import { useQuery } from '@tanstack/react-query';

const { data: userInfo } = useQuery({
  queryKey: ['npubcash-user-info', pubkey],
  queryFn: () => getUserInfo(),
  enabled: !!pubkey && isLoggedIn,
  staleTime: 5 * 60 * 1000, // Cache for 5 minutes
});
```

### Cleanup Subscriptions

**Always cleanup WebSocket subscriptions:**

```typescript
useEffect(() => {
  if (!coco || !isLoggedIn) return;
  
  const unsubscribe = await syncQuotesWithWallet(coco);
  
  return () => {
    if (unsubscribe) unsubscribe();
  };
}, [coco, isLoggedIn, syncQuotesWithWallet]);
```

## Part 9: Common Pitfalls

### 1. ❌ Not checking authentication

**Problem:** Attempting to use npub.cash without Nostr login causes errors.

**Solution:** Always check authentication:
```typescript
if (!isLoggedIn) {
  return <LoginPrompt />;
}
```

### 2. ❌ Not handling missing user info

**Problem:** Assuming user always has npub.cash account.

**Solution:** Handle null user info gracefully:
```typescript
const userInfo = await getUserInfo();
if (!userInfo) {
  // User may not have npub.cash account
  return <CreateAccountPrompt />;
}
```

### 3. ❌ Not cleaning up subscriptions

**Problem:** Memory leaks from uncleaned WebSocket subscriptions.

**Solution:** Always return cleanup function:
```typescript
useEffect(() => {
  const unsubscribe = await syncQuotesWithWallet(coco);
  return () => unsubscribe();
}, [coco, syncQuotesWithWallet]);
```

### 4. ❌ Not syncing mint settings

**Problem:** npub.cash and wallet use different mints.

**Solution:** Sync mint URL when user changes it:
```typescript
const handleMintChange = async (mintUrl: string) => {
  await setActiveMintUrl(mintUrl);
  if (isNpubCashLoggedIn) {
    await setMint(mintUrl); // Sync to npub.cash
  }
};
```

## Security Considerations

1. **NIP-98 Authentication**: Always use proper NIP-98 authentication for API calls
2. **Token Storage**: Don't store authentication tokens in localStorage
3. **Error Messages**: Don't expose internal API errors to users
4. **Quote Validation**: Validate quotes from npub.cash before adding to wallet
5. **Mint Trust**: Only trust mints from verified sources

## Verification Checklist

- [ ] NIP-98 authentication works correctly
- [ ] User info retrieval returns static address
- [ ] Static address displays correctly in UI
- [ ] Mint URL can be set and updated
- [ ] Quote syncing works (manual refresh)
- [ ] Real-time quote subscription works
- [ ] Quotes are properly added to wallet
- [ ] Unknown mints are automatically added
- [ ] WebSocket subscriptions are cleaned up
- [ ] Error handling covers all failure cases
- [ ] Integration with Lightning wallet works (optional)

## Summary

To implement npub.cash static Lightning address functionality:

1. **Set up NIP-98 authentication** - Required for npub.cash API access
2. **Initialize npubcash-sdk** - Use official SDK with JWTAuthProvider
3. **Get user info** - Retrieve static Lightning address (`username@npubx.cash`)
4. **Display address** - Show address in wallet UI with copy/QR functionality
5. **Manage settings** - Sync mint URL and lock quotes (optional)
6. **Sync quotes** - Fetch and sync quotes from npub.cash to wallet
7. **Subscribe to updates** - Use WebSocket for real-time quote updates
8. **Integrate with Lightning wallet** - Optional integration for enhanced UX

**Key principle:** This skill is for **obtaining** static Lightning addresses from npub.cash. Use the `lightning-address` skill to **resolve** any Lightning address (including npub.cash addresses) to invoices for sending payments.

