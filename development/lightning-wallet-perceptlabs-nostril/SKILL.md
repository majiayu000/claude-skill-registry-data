---
name: lightning-wallet
description: Use when implementing a standalone Lightning wallet using Cashu mints - provides complete patterns for minting (receiving Lightning payments), melting (sending Lightning payments), mint management, transaction history, and integrating with Lightning addresses and invoices
when_to_use: When building a Lightning wallet with Cashu mints, implementing Lightning payment flows (send/receive), managing Cashu mints, processing Lightning invoices, or integrating Lightning address functionality with a custodial wallet
---

# Lightning Wallet Implementation

## Overview

Complete implementation guide for a standalone Lightning wallet using Cashu mints and the coco-cashu-core library. This wallet focuses on Lightning operations (minting and melting) rather than token management, providing a streamlined interface for sending and receiving Lightning payments through Cashu mints.

**Core Capabilities:**
- Receive Lightning payments via mint quotes (minting)
- Send Lightning payments via melt quotes (melting)
- Manage multiple Cashu mints with trust/remove operations
- Track transaction history (mint/melt operations)
- Integrate with Lightning addresses and BOLT11 invoices
- Automatic quote processing and state watching
- QR code generation for invoices
- Comprehensive error handling and user feedback

## Prerequisites

### Required Dependencies

**IMPORTANT:** Before adding dependencies, review your project's `package.json` to check if any of these packages already exist. If they do, verify the versions are compatible with the requirements below. Only add packages that are missing or need version updates.

Add these packages to `package.json`:

```json
{
  "dependencies": {
    "@cashu/cashu-ts": "2.8.1",
    "coco-cashu-core": "1.1.2-rc.30",
    "coco-cashu-indexeddb": "1.1.2-rc.30",
    "dexie": "^4.0.8",
    "@scure/bip39": "1.6.0",
    "@scure/bip32": "^2.0.1",
    "@noble/hashes": "^2.0.1",
    "@noble/curves": "^2.0.1"
  }
}
```

**Critical Notes:**
- `@cashu/cashu-ts@2.8.1` **MUST** be explicitly added (required by `coco-cashu-core@1.1.2-rc.30`; prevents build system from resolving to incompatible `3.0.2` which lacks required sub-paths)
- `dexie@^4.0.8` **MUST** be added (required by `coco-cashu-indexeddb@1.1.2-rc.30` for IndexedDB operations)
- `@scure/bip39@1.6.0` **MUST** be used (version 2.0.0+ requires `@noble/hashes@2.0.0` which is now compatible with the updated `coco-cashu-core@1.1.2-rc.30`, but `@scure/bip39@1.6.0` works with both `@noble/hashes@1.8.0` and `@noble/hashes@^2.0.1`)
- `@scure/bip32@^2.0.1` **MUST** be explicitly added if your project uses BIP32 (required by `coco-cashu-core@1.1.2-rc.30` which uses `@noble/hashes@^2.0.1`)
- `@noble/curves@^2.0.1` **MUST** be used (required by `coco-cashu-core@1.1.2-rc.30` which uses `@noble/hashes@^2.0.1`)
- `@noble/hashes@^2.0.1` **MUST** be used (required by `coco-cashu-core@1.1.2-rc.30` and compatible with `@scure/bip32@^2.0.1`)

### Build System Compatibility

**For browser-based builds (act2/Shakespeare):**
- The build system uses esm.sh CDN to fetch packages
- Ensure `package-lock.json` exists (generated via `npm install` if needed)
- All required nested dependencies are listed above - no additional packages needed

**For Node.js builds (Vite/Webpack):**
- Run `npm install` to install dependencies locally
- Verify `node_modules` contains all packages before building

**Required skills (must be referenced/implemented):**
- `qr-code-generator` - QR code generation for Lightning invoices (see `qr-code-generator` skill)
- `lightning-address` - Lightning address support for sending payments (see `lightning-address` skill)
- `lightning-invoice-decoder` - BOLT11 invoice decoding and validation (see `lightning-invoice-decoder` skill)
- `exchange-rates` - Exchange rate functionality for displaying BTC/fiat conversions (see `exchange-rates` skill)

**Optional skills:**
- `npub-cash-address` - Static Lightning address from npub.cash (`username@npubx.cash`) for receiving payments (see `npub-cash-address` skill)

## Implementation Checklist

- [ ] Add all required packages to `package.json`: `@cashu/cashu-ts@2.8.1`, `coco-cashu-core@1.1.2-rc.30`, `coco-cashu-indexeddb@1.1.2-rc.30`, `dexie@^4.0.8`, `@scure/bip39@1.6.0`, `@scure/bip32@^2.0.1` (if using BIP32), `@noble/hashes@^2.0.1`, `@noble/curves@^2.0.1`
- [ ] Initialize coco-cashu-core with IndexedDB backend
- [ ] Implement mnemonic generation and storage
- [ ] Add default mint (`https://mint.minibits.cash/Bitcoin`) automatically if no mints exist
- [ ] Create mint management (add, remove, trust) - **REQUIRED**: Users must be able to add/remove mints including the default
- [ ] Implement Lightning receive (mint quotes)
- [ ] Implement Lightning send (melt quotes)
- [ ] Add transaction history tracking
- [ ] **REQUIRED:** Implement `qr-code-generator` skill for invoice QR codes
- [ ] **REQUIRED:** Implement `lightning-address` skill for sending payments
- [ ] **REQUIRED:** Implement `lightning-invoice-decoder` skill for invoice validation
- [ ] **REQUIRED:** Implement `exchange-rates` skill for BTC/fiat conversions
- [ ] Implement automatic quote processing
- [ ] Add error handling and user feedback
- [ ] Create React hooks for wallet operations

## Part 1: Understanding the Lightning Wallet Architecture

### Wallet vs Token Wallet

This Lightning wallet is **standalone** and focuses exclusively on Lightning operations:

- **Minting**: Receive Lightning payments by creating mint quotes that generate Lightning invoices
- **Melting**: Send Lightning payments by creating melt quotes that pay Lightning invoices
- **No Token Operations**: This wallet does not handle Cashu token transfers, splitting, or token management

### Cashu Mint Architecture

Cashu mints act as Lightning payment processors:

1. **Mint Quote (Receive)**: Request a Lightning invoice from a mint
   - User requests invoice for X sats
   - Mint generates Lightning invoice
   - User pays invoice via Lightning
   - Mint issues Cashu tokens (automatically converted to balance)
   - Tokens are immediately available in wallet

2. **Melt Quote (Send)**: Pay a Lightning invoice using mint tokens
   - User provides Lightning invoice
   - Mint creates melt quote
   - Mint pays invoice via Lightning
   - Tokens are deducted from wallet balance

### Library Structure

The coco-cashu-core library provides:

- **Manager**: Main wallet interface (`initializeCoco`)
- **Repositories**: Direct data access (proofs, mints, history)
- **Events**: Real-time updates via event emitters
- **Services**: Built-in watchers and processors for automatic quote handling

## Part 2: Core Wallet Initialization

### Wallet Setup Hook

**Initialize the coco-cashu-core wallet with IndexedDB storage:**

```typescript
// hooks/wallet/useCashu.ts
import { useState, useEffect, useCallback, useRef } from 'react';
import { useLocalStorage } from '../useLocalStorage';
import * as bip39 from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english.js';
import { initializeCoco, ConsoleLogger, getEncodedToken, type Repositories } from 'coco-cashu-core';
import { IndexedDbRepositories } from 'coco-cashu-indexeddb';
import type { Mint } from 'coco-cashu-core';

// Types from coco-cashu-core
type CocoManager = Awaited<ReturnType<typeof initializeCoco>>;

// Singleton pattern to prevent multiple initializations
let globalCocoInstance: CocoManager | null = null;
let globalRepositories: Repositories | null = null;
let globalInitializationPromise: Promise<{ coco: CocoManager; repositories: Repositories }> | null = null;

export interface UseCashuReturn {
  // The typed coco manager (direct library access)
  coco: CocoManager | null;
  
  // Repositories for direct access to proof data
  repositories: Repositories | null;
  
  // React state (for reactivity)
  balances: { [mintUrl: string]: number };
  mints: Array<{ url: string; name?: string; info?: unknown }>;
  totalBalance: number;
  
  // Status
  isInitialized: boolean;
  isLoading: boolean;
  error: Error | null;
  
  // Mnemonic management
  mnemonic: string | null;
  setMnemonic: (mnemonic: string) => void;
  generateMnemonic: () => string;
  
  // Utility functions
  clearError: () => void;
  getEncodedToken: typeof getEncodedToken;
  refreshMints: () => Promise<void>;
}

export function useCashu(): UseCashuReturn {
  const [isInitialized, setIsInitialized] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  
  // Mnemonic management with localStorage
  const [mnemonic, setMnemonicState] = useLocalStorage<string | null>('cashu-mnemonic', null);
  
  // Manager instance ref
  const cocoRef = useRef<CocoManager | null>(null);
  const repositoriesRef = useRef<Repositories | null>(null);
  
  // React state for UI reactivity
  const [balances, setBalances] = useState<{ [mintUrl: string]: number }>({});
  const [mints, setMints] = useState<Array<{ url: string; name?: string; info?: unknown }>>([]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const generateMnemonic = useCallback(() => {
    return bip39.generateMnemonic(wordlist);
  }, []);

  const refreshMints = useCallback(async () => {
    const coco = cocoRef.current;
    if (!coco) return;
    
    try {
      // Only show trusted mints in the UI
      const mintList = await coco.mint.getAllTrustedMints();
      setMints(mintList.map((m: Mint) => ({ 
        url: m.mintUrl, 
        name: m.name,
        info: m.mintInfo
      })));
    } catch (err) {
      console.error('Failed to refresh mints:', err);
    }
  }, []);

  const setMnemonic = useCallback((newMnemonic: string) => {
    if (!bip39.validateMnemonic(newMnemonic, wordlist)) {
      throw new Error('Invalid mnemonic');
    }
    setMnemonicState(newMnemonic);
    // Reinitialize manager with new mnemonic
    setIsInitialized(false);
  }, [setMnemonicState]);

  // Initialize the coco manager
  const initializeCocoManager = useCallback(async () => {
    if (isInitialized || isLoading) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Use singleton pattern to prevent multiple initializations
      if (globalCocoInstance && globalRepositories) {
        cocoRef.current = globalCocoInstance;
        repositoriesRef.current = globalRepositories;
        setIsInitialized(true);
        setIsLoading(false);
        return;
      }
      
      // If there's already an initialization in progress, wait for it
      if (globalInitializationPromise) {
        console.log('Waiting for existing initialization...');
        const { coco, repositories } = await globalInitializationPromise;
        cocoRef.current = coco;
        repositoriesRef.current = repositories;
        setIsInitialized(true);
        setIsLoading(false);
        return;
      }
      
      // Generate or retrieve mnemonic
      let currentMnemonic = mnemonic;
      if (!currentMnemonic) {
        currentMnemonic = bip39.generateMnemonic(wordlist);
        setMnemonicState(currentMnemonic);
      }
      
      // Create seed from mnemonic
      const seed = bip39.mnemonicToSeedSync(currentMnemonic);
      
      // Initialize repositories with proper initialization
      const repo = new IndexedDbRepositories({ name: "cashu-wallet" });
      await repo.init(); // Ensure repository is properly initialized
      
      // Create initialization promise
      globalInitializationPromise = (async () => {
        const coco = await initializeCoco({
          repo,
          seedGetter: async () => seed,
          logger: new ConsoleLogger("coco", { level: "debug" }) // Use debug level for better logging
        });
        return { coco, repositories: repo };
      })();
      
      // Initialize coco manager using the new API
      const { coco, repositories } = await globalInitializationPromise;
      
      // Store as singleton
      console.log('Storing new coco instance as singleton');
      globalCocoInstance = coco;
      globalRepositories = repositories;
      globalInitializationPromise = null;
      cocoRef.current = coco;
      repositoriesRef.current = repositories;
      
      // Enable built-in services for automatic quote processing and state watching
      try {
        console.log('Enabling coco services...');
        await coco.enableMintQuoteWatcher({ watchExistingPendingOnStart: false });
        console.log('Mint quote watcher enabled');
        
        await coco.enableMintQuoteProcessor();
        console.log('Mint quote processor enabled');
        
        await coco.enableProofStateWatcher();
        console.log('Proof state watcher enabled');
        
        console.log('All coco services enabled successfully');
      } catch (err) {
        // Don't fail initialization if watchers can't be enabled
        console.warn('Failed to enable some coco services:', err);
      }
      
      // Add default mint if no mints exist (users can remove it later)
      try {
        const DEFAULT_MINT_URL = 'https://mint.minibits.cash/Bitcoin';
        const existingMints = await coco.mint.getAllTrustedMints();
        const hasDefaultMint = existingMints.some((m: Mint) => 
          m.mintUrl.toLowerCase() === DEFAULT_MINT_URL.toLowerCase()
        );
        
        if (!hasDefaultMint && existingMints.length === 0) {
          console.log('Adding default mint:', DEFAULT_MINT_URL);
          await coco.mint.addMint(DEFAULT_MINT_URL, { trusted: true });
          console.log('Default mint added successfully');
        }
      } catch (err) {
        // Don't fail initialization if default mint can't be added
        console.warn('Failed to add default mint:', err);
      }
      
      setIsInitialized(true);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to initialize Cashu wallet';
      setError(new Error(errorMessage));
      globalInitializationPromise = null; // Reset on error
    } finally {
      setIsLoading(false);
    }
  }, [isInitialized, isLoading, mnemonic, setMnemonicState]);

  // Initialize on mount and when mnemonic changes
  useEffect(() => {
    initializeCocoManager();
  }, [initializeCocoManager]);

  // Auto-refresh balances and mints on manager events
  useEffect(() => {
    const coco = cocoRef.current;
    if (!coco) return;
    
    const refreshBalances = async () => {
      try {
        const newBalances = await coco.wallet.getBalances();
        setBalances(newBalances);
      } catch (err) {
        console.log('Failed to refresh balances:', err);
      }
    };
    
    // Initial load
    refreshBalances();
    refreshMints();
    
    // Listen to events
    const unsubs = [
      coco.on('proofs:saved', refreshBalances),
      coco.on('proofs:state-changed', refreshBalances),
      coco.on('send:created', refreshBalances),
      coco.on('receive:created', refreshBalances),
      coco.on('mint:added', refreshMints),
      coco.on('mint:updated', refreshMints),
    ];
    
    return () => unsubs.forEach(unsub => unsub());
  }, [isInitialized, refreshMints]);

  // Calculate total balance
  const totalBalance = Object.values(balances).reduce((sum, balance) => sum + balance, 0);

  return {
    // The typed coco manager (direct library access)
    coco: cocoRef.current,
    
    // Repositories for direct access to proof data
    repositories: repositoriesRef.current,
    
    // React state (for reactivity)
    balances,
    mints,
    totalBalance,
    
    // Status
    isInitialized,
    isLoading,
    error,
    
    // Mnemonic management
    mnemonic,
    setMnemonic,
    generateMnemonic,
    
    // Utility functions
    clearError,
    getEncodedToken,
    refreshMints,
  };
}
```

**Key Points:**
- **Singleton Pattern**: Prevents multiple wallet initializations
- **Mnemonic Storage**: Uses localStorage for persistence
- **Automatic Services**: Enables quote watchers and processors for automatic handling
- **Default Mint**: Automatically adds `https://mint.minibits.cash/Bitcoin` as the default mint if no mints exist (users can remove it later)
- **Event Listeners**: Auto-refreshes balances and mints on wallet events
- **Repository Access**: Provides direct access to proof/mint data when needed

## Part 3: Mint Management

### Mint Manager Hook

**Manage Cashu mints (add, remove, trust):**

```typescript
// hooks/wallet/useMintManager.ts
import { useState, useCallback } from 'react';
import type { Manager, Repositories } from 'coco-cashu-core';
import { useToast } from '@/hooks/useToast';

export interface CashuMint {
  url: string;
  name?: string;
}

// Mint utility functions
export const getCleanMintLabel = (mint: { name?: string; url: string }): string => {
  if (mint.name && mint.name.trim().length > 0) {
    return mint.name.replace(/^https?:\/\//, '');
  }
  try {
    return new URL(mint.url).host;
  } catch {
    return mint.url.replace(/^https?:\/\//, '');
  }
};

export const isUnknownMintError = (err: unknown): boolean => {
  const errorMessage = err instanceof Error ? err.message : String(err);
  const errorName = err instanceof Error ? err.constructor.name : '';
  return errorName === 'UnknownMintError' || 
         errorMessage.includes('UnknownMintError') || 
         (errorMessage.includes('Mint') && errorMessage.includes('is not known'));
};

export const extractMintUrlFromError = (err: unknown): string | null => {
  const errorMessage = err instanceof Error ? err.message : String(err);
  const mintUrlMatch = errorMessage.match(/Mint (https?:\/\/[^\s]+)/);
  return mintUrlMatch?.[1] || null;
};

interface UseMintManagerProps {
  coco: Manager | null;
  mints: CashuMint[];
  repositories: Repositories | null;
  refreshMints: () => Promise<void>;
}

export function useMintManager({
  coco,
  mints,
  repositories,
  refreshMints,
}: UseMintManagerProps) {
  const { toast } = useToast();
  const [activeMintUrl, setActiveMintUrl] = useState<string | null>(null);
  const [mintUrl, setMintUrl] = useState('');
  const [mintToRemove, setMintToRemove] = useState<CashuMint | null>(null);
  const [showRemoveMintModal, setShowRemoveMintModal] = useState(false);

  // Set active mint
  const handleSetActiveMint = useCallback(
    async (url: string | null) => {
      setActiveMintUrl(url);
    },
    []
  );

  // Add a new mint
  const handleAddMint = useCallback(async () => {
    if (!mintUrl.trim() || !coco) return;
    try {
      // Normalize URL - add https:// if not present
      let normalizedUrl = mintUrl.trim();
      if (
        !normalizedUrl.startsWith('http://') &&
        !normalizedUrl.startsWith('https://')
      ) {
        normalizedUrl = `https://${normalizedUrl}`;
      }

      // Check if mint with same name already exists (case insensitive)
      const existingMint = mints.find(mint => 
        mint.url.toLowerCase() === normalizedUrl.toLowerCase()
      );
      
      if (existingMint) {
        // Default: Toast notification
        toast({ variant: 'destructive', title: 'Mint Already Exists', description: 'A mint with this URL already exists' });
        // Alternative options (commented):
        // Option 1: Console logging
        // console.error('Mint Already Exists: A mint with this URL already exists');
        // Option 2: No notification (silent failure)
        return;
      }

      // Add mint and automatically trust it
      await coco.mint.addMint(normalizedUrl, { trusted: true });
      setMintUrl('');

      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.log('Mint Added: Mint added and trusted successfully!');
      // Option 2: Toast notification (if toast is available)
      // toast({ title: 'Mint Added', description: 'Mint added and trusted successfully!' });
      // Option 3: No notification (silent success)
    } catch (err) {
      // Default: Toast notification
      toast({ variant: 'destructive', title: 'Add Mint Failed', description: err instanceof Error ? err.message : 'Unknown error' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Add Mint Failed:', err instanceof Error ? err.message : 'Unknown error');
      // Option 2: No notification (silent failure)
    }
  }, [mintUrl, coco, mints, toast]);

  // Show remove confirmation modal
  const handleRemoveMintClick = useCallback((mint: CashuMint) => {
    setMintToRemove(mint);
    setShowRemoveMintModal(true);
  }, []);

  // Confirm and remove mint
  const handleConfirmRemoveMint = useCallback(async () => {
    if (!mintToRemove || !repositories) return;

    try {
      // Delete the mint from the backend using the mint repository directly
      await repositories.mintRepository.deleteMint(mintToRemove.url);

      // If the removed mint was active, switch to the first available mint
      if (activeMintUrl === mintToRemove.url) {
        const remainingMints = mints.filter(
          (mint) => mint.url !== mintToRemove.url
        );
        if (remainingMints.length > 0) {
          handleSetActiveMint(remainingMints[0].url);
        } else {
          setActiveMintUrl(null);
        }
      }

      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.log('Mint Removed:', `${mintToRemove.name || mintToRemove.url} has been permanently removed`);
      // Option 2: Toast notification (if toast is available)
      // toast({ title: 'Mint Removed', description: `${mintToRemove.name || mintToRemove.url} has been permanently removed` });
      // Option 3: No notification (silent success)

      // Refresh the mints list to update the dropdown immediately
      await refreshMints();

      setShowRemoveMintModal(false);
      setMintToRemove(null);
    } catch (err) {
      // Default: Toast notification
      toast({ variant: 'destructive', title: 'Remove Mint Failed', description: err instanceof Error ? err.message : 'Unknown error' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Remove Mint Failed:', err instanceof Error ? err.message : 'Unknown error');
      // Option 2: No notification (silent failure)
    }
  }, [
    mintToRemove,
    mints,
    activeMintUrl,
    handleSetActiveMint,
    repositories,
    refreshMints,
    toast,
  ]);

  return {
    activeMintUrl,
    setActiveMintUrl: handleSetActiveMint,
    mintUrl,
    setMintUrl,
    handleAddMint,
    handleRemoveMintClick,
    handleConfirmRemoveMint,
    mintToRemove,
    setMintToRemove,
    showRemoveMintModal,
    setShowRemoveMintModal,
    getCleanMintLabel,
  };
}
```

**Key Operations:**
- **Add Mint**: Normalize URL, check for duplicates, add with trusted flag
- **Remove Mint**: Delete from repository, handle active mint switching (including the default mint - users are not locked to any mint)
- **Active Mint**: Track which mint is currently selected for operations
- **Error Handling**: Detect unknown mint errors and extract mint URLs from errors

**CRITICAL: Mint Management Requirements:**
- **Users must be able to add/remove mints**: The wallet must provide full mint management capabilities. Users are NOT locked to the default mint (`https://mint.minibits.cash/Bitcoin`) and can remove it if desired.
- **Default mint is optional**: The default mint is only added automatically if no mints exist. Once users add their own mints, they can remove the default mint just like any other mint.
- **Mint Selector UI**: Display a mint selector component that allows users to:
  - View all available mints with their balances
  - Select an active mint for operations
  - Add new mints inline
  - Remove mints (with confirmation modal) - **including the default mint**
  - See which mint is currently active
- **Active Mint Display**: Always show the currently selected mint in the wallet UI, as all Lightning operations (send/receive) require an active mint to be selected

## Part 4: Lightning Operations

### Receive Lightning Payments (Minting)

**Create mint quotes to receive Lightning payments:**

```typescript
// hooks/wallet/useLightningOperations.ts (excerpt)
import { useState, useCallback, useEffect, useRef } from 'react';
import type { Manager } from 'coco-cashu-core';
import { useToast } from '@/hooks/useToast';

interface UseLightningOperationsProps {
  coco: Manager | null;
  activeMintUrl: string | null;
  generateQRCode: (text: string) => Promise<string>;
}

export function useLightningOperations({
  coco,
  activeMintUrl,
  generateQRCode,
}: UseLightningOperationsProps) {
  // Default: Toast notifications
  const { toast } = useToast();
  // Alternative options (commented):
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: No notification handler
  
  // Receive state
  const [quoteAmount, setQuoteAmount] = useState('');
  
  // Invoice modal state
  const [showInvoiceModal, setShowInvoiceModal] = useState(false);
  const [currentInvoice, setCurrentInvoice] = useState<{
    quoteId: string;
    mintUrl: string;
    amount: number;
    invoice: string;
    qrCodeUrl: string;
    expiry: number;
  } | null>(null);

  // Ref to store the mint quote redeemed event unsubscribe function
  const mintQuoteUnsubscribeRef = useRef<(() => void) | null>(null);

  // Handle receive (Lightning quote/invoice creation)
  const handleLightningReceive = useCallback(async () => {
    if (!coco || !quoteAmount || !activeMintUrl) {
      return;
    }

    try {
      const amount = parseInt(quoteAmount);
      if (isNaN(amount) || amount <= 0) {
        // Default: Toast notification
        toast({ variant: 'destructive', title: 'Invalid Amount', description: 'Please enter a valid amount' });
        // Alternative options (commented):
        // Option 1: Console logging
        // console.error('Invalid Amount: Please enter a valid amount');
        // Option 2: No notification (silent failure)
        return;
      }
      
      const quote = await coco.quotes.createMintQuote(activeMintUrl, amount);

      // Generate QR code for the Lightning invoice
      const qrCodeUrl = await generateQRCode(quote.request);

      // Set the invoice data and show modal
      setCurrentInvoice({
        quoteId: quote.quote,
        mintUrl: activeMintUrl,
        amount,
        invoice: quote.request,
        qrCodeUrl,
        expiry: quote.expiry,
      });
      
      setShowInvoiceModal(true);
      setQuoteAmount('');

      // Clean up any previous listener
      if (mintQuoteUnsubscribeRef.current) {
        mintQuoteUnsubscribeRef.current();
        mintQuoteUnsubscribeRef.current = null;
      }

      // Listen for payment notification via mint-quote:redeemed event
      const quoteId = quote.quote;
      const invoiceAmount = amount;

      const unsubscribe = coco.on('mint-quote:redeemed', (payload: unknown) => {
        const redeemedQuote = payload as { quoteId?: string };

        // Check if this is the quote we're waiting for
        if (redeemedQuote.quoteId === quoteId) {
          // Default: Toast notification
          toast({ title: 'Payment Received', description: `Successfully received ${invoiceAmount} sats! Tokens have been added to your wallet.` });
          // Alternative options (commented):
          // Option 1: Console logging
          // console.log(`Payment Received: Successfully received ${invoiceAmount} sats! Tokens have been added to your wallet.`);
          // Option 2: No notification (silent success)
          setShowInvoiceModal(false);
          setCurrentInvoice(null);

          // Clean up the event listener
          mintQuoteUnsubscribeRef.current = null;
          unsubscribe();
        }
      });

      // Store unsubscribe function for cleanup
      mintQuoteUnsubscribeRef.current = unsubscribe;
    } catch (err) {
      // Default: Toast notification
      toast({ variant: 'destructive', title: 'Quote Creation Failed', description: err instanceof Error ? err.message : 'Unknown error' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Quote Creation Failed:', err instanceof Error ? err.message : 'Unknown error');
      // Option 2: No notification (silent failure)
    }
  }, [coco, quoteAmount, activeMintUrl, generateQRCode, toast]);

  return {
    quoteAmount,
    setQuoteAmount,
    showInvoiceModal,
    setShowInvoiceModal,
    currentInvoice,
    setCurrentInvoice,
    handleLightningReceive,
  };
}
```

**Key Points:**
- **Mint Quote Creation**: `coco.quotes.createMintQuote(mintUrl, amount)` returns invoice
- **QR Code Generation**: Generate QR for invoice display
- **Event Listening**: Listen for `mint-quote:redeemed` to detect payment
- **Automatic Processing**: Built-in quote processor handles invoice payment automatically

### Send Lightning Payments (Melting)

**Pay Lightning invoices using melt quotes:**

```typescript
// hooks/wallet/useLightningOperations.ts (excerpt)
import { decodeBolt11Amount, isValidBolt11Invoice } from '@/lib/bolt11Decoder';

export function useLightningOperations({
  coco,
  activeMintUrl,
  getLightningInvoice, // For Lightning addresses
}: UseLightningOperationsProps) {
  // Optional: User feedback notifications
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: Toast notifications (if useToast hook is available)
  // const { toast } = useToast();
  // Option 3: No notification handler
  
  // Send state
  const [lightningInvoice, setLightningInvoice] = useState('');
  const [lightningAddressInput, setLightningAddressInput] = useState('');
  const [lightningAddressAmount, setLightningAddressAmount] = useState('');
  const [pendingLightningAddress, setPendingLightningAddress] = useState<string | null>(null);
  const [decodedInvoiceAmount, setDecodedInvoiceAmount] = useState<number | null>(null);
  const [pendingInvoice, setPendingInvoice] = useState<string | null>(null);
  
  // Processing state to prevent concurrent executions
  const [isProcessingPayment, setIsProcessingPayment] = useState(false);

  // Detect input type and handle Lightning address/invoice parsing
  const detectAndHandleLightningInput = useCallback((input: string): 'lightning_address' | 'invoice' | null => {
    const trimmed = input.trim();
    if (!trimmed) return null;

    // Check if it's a Lightning address (contains @)
    if (trimmed.includes('@')) {
      setPendingLightningAddress(trimmed);
      setLightningAddressInput('');
      return 'lightning_address';
    }

    // Check if it's a Lightning invoice
    if (isValidBolt11Invoice(trimmed)) {
      const amount = decodeBolt11Amount(trimmed);
      if (amount) {
        // Show amount confirmation screen
        setPendingInvoice(trimmed);
        setDecodedInvoiceAmount(amount);
        setLightningInvoice('');
        return 'invoice';
      } else {
        // Failed to decode amount - show error
        // Default: Toast notification
        toast({ variant: 'destructive', title: 'Invalid Invoice', description: 'Unable to decode the lightning invoice amount. Please check the invoice format.' });
        // Alternative options (commented):
        // Option 1: Console logging
        // console.error('Invalid Invoice: Unable to decode the lightning invoice amount. Please check the invoice format.');
        // Option 2: No notification (silent failure)
        setLightningInvoice('');
        return null;
      }
    } else {
      // Not a valid BOLT11 invoice - show error
      // Default: Toast notification
      toast({ variant: 'destructive', title: 'Invalid Invoice', description: 'This does not appear to be a valid lightning invoice. Please check the format.' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Invalid Invoice: This does not appear to be a valid lightning invoice. Please check the format.');
      // Option 2: No notification (silent failure)
      setLightningInvoice('');
      return null;
    }
  }, [toast]);

  // Handle Lightning address payment
  const handleLightningAddressPayment = useCallback(async () => {
    // Prevent concurrent executions
    if (isProcessingPayment) {
      return;
    }

    if (!coco || !pendingLightningAddress || !lightningAddressAmount || !activeMintUrl) {
      return;
    }

    setIsProcessingPayment(true);

    try {
      const amount = parseInt(lightningAddressAmount);
      if (isNaN(amount) || amount <= 0) {
        // Default: Toast notification
        toast({ variant: 'destructive', title: 'Invalid Amount', description: 'Please enter a valid amount' });
        // Alternative options (commented):
        // Option 1: Console logging
        // console.error('Invalid Amount: Please enter a valid amount');
        // Option 2: No notification (silent failure)
        setIsProcessingPayment(false);
        return;
      }

      // Get invoice from Lightning address (REQUIRED: use lightning-address skill)
      const invoice = await getLightningInvoice({
        lightningAddress: pendingLightningAddress,
        amountSats: amount,
      });

      // Create melt quote and pay it
      const meltQuote = await coco.quotes.createMeltQuote(
        activeMintUrl,
        invoice
      );
      await coco.quotes.payMeltQuote(activeMintUrl, meltQuote.quote);

      // Default: Toast notification
      toast({ title: 'Payment Sent', description: `Successfully sent ${amount} sats to ${pendingLightningAddress}!` });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.log(`Payment Sent: Successfully sent ${amount} sats to ${pendingLightningAddress}!`);
      // Option 2: No notification (silent success)

      // Reset state
      setPendingLightningAddress(null);
      setLightningAddressInput('');
      setLightningAddressAmount('');
    } catch (err) {
      // Default: Toast notification
      toast({ variant: 'destructive', title: 'Payment Failed', description: err instanceof Error ? err.message : 'Unknown error' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Payment Failed:', err instanceof Error ? err.message : 'Unknown error');
      // Option 2: No notification (silent failure)
    } finally {
      setIsProcessingPayment(false);
    }
  }, [coco, pendingLightningAddress, lightningAddressAmount, activeMintUrl, getLightningInvoice, isProcessingPayment, toast]);

  // Handle confirmed invoice payment
  const handleConfirmInvoicePayment = useCallback(async () => {
    // Prevent concurrent executions
    if (isProcessingPayment) {
      return;
    }

    if (!coco || !pendingInvoice || !activeMintUrl) return;

    setIsProcessingPayment(true);

    try {
      const meltQuote = await coco.quotes.createMeltQuote(
        activeMintUrl,
        pendingInvoice
      );
      await coco.quotes.payMeltQuote(activeMintUrl, meltQuote.quote);

      // Default: Toast notification
      toast({ title: 'Invoice Paid', description: `Lightning invoice paid successfully for ${decodedInvoiceAmount} sats!` });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.log(`Invoice Paid: Lightning invoice paid successfully for ${decodedInvoiceAmount} sats!`);
      // Option 2: No notification (silent success)

      // Reset state
      setPendingInvoice(null);
      setDecodedInvoiceAmount(null);
    } catch (err) {
      // Default: Toast notification
      toast({ variant: 'destructive', title: 'Invoice Payment Failed', description: err instanceof Error ? err.message : 'Unknown error' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Invoice Payment Failed:', err instanceof Error ? err.message : 'Unknown error');
      // Option 2: No notification (silent failure)
    } finally {
      setIsProcessingPayment(false);
    }
  }, [coco, pendingInvoice, activeMintUrl, decodedInvoiceAmount, isProcessingPayment, toast]);

  return {
    // Send state
    lightningInvoice,
    setLightningInvoice,
    lightningAddressInput,
    setLightningAddressInput,
    lightningAddressAmount,
    setLightningAddressAmount,
    pendingLightningAddress,
    setPendingLightningAddress,
    decodedInvoiceAmount,
    setDecodedInvoiceAmount,
    pendingInvoice,
    setPendingInvoice,
    // Processing state
    isProcessingPayment,
    // Handlers
    detectAndHandleLightningInput,
    handleLightningAddressPayment,
    handleConfirmInvoicePayment,
  };
}
```

**Key Operations:**
- **Melt Quote Creation**: `coco.quotes.createMeltQuote(mintUrl, invoice)` creates quote
- **Quote Payment**: `coco.quotes.payMeltQuote(mintUrl, quoteId)` pays the invoice
- **Input Detection**: Automatically detects Lightning addresses vs BOLT11 invoices
- **Invoice Decoding**: **REQUIRED** - Uses `lightning-invoice-decoder` skill for amount extraction
- **Lightning Address Support**: **REQUIRED** - Uses `lightning-address` skill for invoice generation
- **QR Code Generation**: **REQUIRED** - Uses `qr-code-generator` skill for invoice QR codes

## Part 5: Transaction History

### History Manager Hook

**Track and display transaction history:**

```typescript
// hooks/wallet/useHistoryManager.ts
import { useState, useCallback, useEffect } from 'react';
import type { HistoryEntry, Manager } from 'coco-cashu-core';

interface UseHistoryManagerProps {
  coco: Manager | null;
  isInitialized: boolean;
}

export function useHistoryManager({
  coco,
  isInitialized,
}: UseHistoryManagerProps) {
  const [historyEntries, setHistoryEntries] = useState<HistoryEntry[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [isHistoryExpanded, setIsHistoryExpanded] = useState(false);

  // Load history from wallet
  const loadHistory = useCallback(async () => {
    if (!coco) return;

    try {
      setIsLoadingHistory(true);
      const entries = await coco.history.getPaginatedHistory(0, 50);
      
      // Filter out unpaid quotes: only show completed transactions
      // - Mint quotes: only show 'ISSUED' (completed)
      // - Melt quotes: only show 'PAID' (completed)
      // - Send/Receive: show all (no state field)
      const filteredEntries = entries.filter((entry) => {
        if (entry.type === 'mint') {
          return entry.state === 'ISSUED';
        }
        if (entry.type === 'melt') {
          return entry.state === 'PAID';
        }
        // Send and receive entries don't have a state field, show all
        return true;
      });
      
      setHistoryEntries(filteredEntries);
    } catch (err) {
      console.error('Failed to load history:', err);
    } finally {
      setIsLoadingHistory(false);
    }
  }, [coco]);

  // Load history on wallet initialization
  useEffect(() => {
    if (isInitialized && historyEntries.length === 0) {
      loadHistory();
    }
  }, [isInitialized, historyEntries.length, loadHistory]);

  // Auto-refresh on wallet events
  useEffect(() => {
    if (!isInitialized || !coco) return;

    // Listen for history updates (fires on send, receive transactions)
    const unsubscribeHistoryUpdated = coco.on('history:updated', () => {
      loadHistory();
    });

    // Listen for melt quote creation (coco-cashu bug: doesn't emit history:updated)
    const unsubscribeMeltCreated = coco.on('melt-quote:created', () => {
      loadHistory();
    });

    // Listen for melt quote paid (backup, in case creation event missed)
    const unsubscribeMeltPaid = coco.on('melt-quote:paid', () => {
      loadHistory();
    });

    // Listen for mint quote REDEEMED (only after invoice is paid, not created)
    const unsubscribeMintRedeemed = coco.on('mint-quote:redeemed', () => {
      loadHistory();
    });

    return () => {
      unsubscribeHistoryUpdated();
      unsubscribeMeltCreated();
      unsubscribeMeltPaid();
      unsubscribeMintRedeemed();
    };
  }, [isInitialized, coco, loadHistory]);

  return {
    historyEntries,
    setHistoryEntries,
    isLoadingHistory,
    isHistoryExpanded,
    setIsHistoryExpanded,
    loadHistory,
  };
}
```

**Key Points:**
- **Filtering**: Only show completed transactions (ISSUED mint quotes, PAID melt quotes)
- **Event Listeners**: Auto-refresh on quote creation, payment, and redemption
- **Pagination**: Use `getPaginatedHistory(offset, limit)` for large histories
- **State Management**: Track loading and expansion state for UI

## Part 6: Integration with Required Skills

### Lightning Address Integration (Required)

**CRITICAL:** The `lightning-address` skill is mandatory for this wallet. Use it for sending payments via Lightning addresses:

```typescript
// Import from lightning-address skill
import { useLightningAddress } from '@/hooks/useLightningAddress';

// In your component
const { getInvoice } = useLightningAddress();

// When user enters Lightning address
const invoice = await getInvoice({
  lightningAddress: 'alice@strike.me',
  amountSats: 1000,
  comment: 'Thanks for the coffee!'
});

// Then create melt quote with the invoice
const meltQuote = await coco.quotes.createMeltQuote(activeMintUrl, invoice);
await coco.quotes.payMeltQuote(activeMintUrl, meltQuote.quote);
```

### BOLT11 Invoice Decoder Integration (Required)

**CRITICAL:** The `lightning-invoice-decoder` skill is mandatory for this wallet. Use it for invoice validation and amount extraction:

```typescript
// Import from lightning-invoice-decoder skill
import { decodeBolt11Amount, isValidBolt11Invoice } from '@/lib/bolt11Decoder';

// Validate and decode invoice
if (isValidBolt11Invoice(invoiceString)) {
  const amount = decodeBolt11Amount(invoiceString);
  if (amount) {
    // Show amount confirmation to user
    // Then proceed with melt quote
  } else {
    // Amountless invoice - user must specify amount
  }
}
```

### QR Code Generation Integration (Required)

**CRITICAL:** The `qr-code-generator` skill is mandatory for this wallet. You must generate QR codes for Lightning invoices, but the specific display location and format are flexible.

**Example implementation for generating and displaying QR codes:**

This is an example implementation that can be customized or replaced based on your design needs. The requirement is to generate QR codes for invoices, but how and where you display them (modals, drawers, separate pages, etc.) is up to you.

```typescript
// Example: Using qr-code-generator skill (EXAMPLE - customize as needed)
// Import from qr-code-generator skill
import { useQRCodeGenerator } from '@/hooks/useQRCodeGenerator';

// In your component
const { generateQRCode } = useQRCodeGenerator();

// When creating a mint quote (receive)
const quote = await coco.quotes.createMintQuote(activeMintUrl, amount);
const qrCodeUrl = await generateQRCode(quote.request);

// Example display in modal (customize this to match your design)
// QR codes could also be displayed in drawers, separate pages, or other UI patterns
<QRModal
  qrCodeUrl={qrCodeUrl}
  content={quote.request}
  // ... other props
/>
```

**Example Usage Patterns (experiment with these or create your own):**
- **QR code generation**: Generate QR codes for all Lightning invoices (mint quotes)
- **Display location**: Display QR codes in modals, drawers, separate pages, or inline components
- **Invoice text**: Include invoice string alongside QR code for manual entry or copying
- **Expiry handling**: Show countdown timer or handle expiry gracefully
- **Custom styling**: Adapt the QR code display to match your application's design system
- **Multiple display options**: Allow users to view QR code in different formats or locations
- **Accessibility**: Ensure QR codes are accessible with proper alt text and sizing

### Exchange Rates Integration (Required)

**CRITICAL:** The `exchange-rates` skill is mandatory for this wallet. You must implement BTC/fiat currency conversions in your wallet UI, but the specific display format and location are flexible.

**Example implementation for displaying exchange rate conversions:**

This is an example implementation that can be customized or replaced based on your design needs. The requirement is to provide fiat currency conversions, but how and where you display them is up to you.

```typescript
// Example: Using exchange-rates skill (EXAMPLE - customize as needed)
// Import from exchange-rates skill
import { useExchangeRate } from '@/hooks/useExchangeRate';

// In your component
const { rate, isLoading, error } = useExchangeRate('USD');

// Calculate fiat equivalent
const balanceSats = 100000; // 100k sats
const usdValue = rate ? (balanceSats / 100_000_000) * rate : null;

// Example display (customize this to match your design)
return (
  <div>
    <div>{balanceSats.toLocaleString()} sats</div>
    {usdValue && (
      <div className="text-muted-foreground">
        ≈ ${usdValue.toFixed(2)} USD
      </div>
    )}
  </div>
);
```

**Example Usage Patterns (experiment with these or create your own):**
- **Balance display**: Show balance with fiat currency equivalents (toggle, inline, or separate display)
- **Transaction amounts**: Show transaction amounts in both sats and fiat
- **Invoice amounts**: Convert invoice amounts to fiat for user understanding
- **Display location**: Place exchange rate in wallet header, balance section, or transaction details
- **Multiple currencies**: Support multiple fiat currencies beyond USD
- **Custom formatting**: Adapt the display format to match your application's design system
- **Real-time updates**: Refresh exchange rates periodically or on user interaction

### npub.cash Static Address Integration (Optional)

**OPTIONAL:** The `npub-cash-address` skill provides static Lightning addresses for users. Use it to display a permanent Lightning address (`username@npubx.cash`) in the wallet UI:

```typescript
// Import from npub-cash-address skill
import { useNpubCash } from '@/hooks/wallet/useNpubCash';

// In your component
const { getUserInfo, isLoading } = useNpubCash();

// Get user's static Lightning address
const userInfo = await getUserInfo();
if (userInfo) {
  const username = userInfo.name || extractUsernameFromPubkey(userInfo.pubkey);
  const staticAddress = `${username}@npubx.cash`;
  
  // Display static address in wallet header
  <LightningAddressDisplay lightningAddress={staticAddress} />
}
```

**Benefits of static addresses:**
- Users can share a permanent address for receiving payments
- Others can send payments without user creating invoices first
- Better UX for recurring payments or donations
- Integrates with npub.cash quote syncing

**Note:** This is optional - users can still use the wallet without npub.cash. Static addresses are a convenience feature for better UX.

## Part 7: Error Handling

### Common Error Patterns

**Handle unknown mint errors:**

```typescript
import { isUnknownMintError, extractMintUrlFromError } from '@/hooks/wallet/useMintManager';
import { useToast } from '@/hooks/useToast';

// In a component or hook:
const { toast } = useToast();

try {
  await coco.quotes.createMintQuote(mintUrl, amount);
} catch (err) {
  if (isUnknownMintError(err)) {
    const extractedUrl = extractMintUrlFromError(err);
    // Default: Toast notification
    toast({ variant: 'destructive', title: 'Unknown Mint', description: `Mint ${extractedUrl || mintUrl} is not known. Please add it first.` });
    // Alternative options (commented):
    // Option 1: Console logging
    // console.error(`Unknown Mint: Mint ${extractedUrl || mintUrl} is not known. Please add it first.`);
    // Option 2: No notification (silent failure)
  } else {
    // Default: Toast notification
    toast({ variant: 'destructive', title: 'Error', description: err instanceof Error ? err.message : 'Unknown error' });
    // Alternative options (commented):
    // Option 1: Console logging
    // console.error('Error:', err instanceof Error ? err.message : 'Unknown error');
    // Option 2: No notification (silent failure)
  }
}
```

### Quote State Errors

**Handle quote expiry and failures:**

```typescript
import { useToast } from '@/hooks/useToast';

// In a component or hook:
const { toast } = useToast();

// Check quote expiry before displaying
const quote = await coco.quotes.createMintQuote(mintUrl, amount);
const now = Math.floor(Date.now() / 1000);
if (quote.expiry <= now) {
  // Default: Toast notification
  toast({ variant: 'destructive', title: 'Quote Expired', description: 'The quote has already expired. Please create a new one.' });
  // Alternative options (commented):
  // Option 1: Console logging
  // console.error('Quote Expired: The quote has already expired. Please create a new one.');
  // Option 2: No notification (silent failure)
  return;
}

// Listen for quote failures
coco.on('mint-quote:failed', (payload) => {
  // Default: Toast notification
  toast({ variant: 'destructive', title: 'Payment Failed', description: 'The Lightning payment failed. Please try again.' });
  // Alternative options (commented):
  // Option 1: Console logging
  // console.error('Payment Failed: The Lightning payment failed. Please try again.');
  // Option 2: No notification (silent failure)
});
```

## Part 8: UI Components

### Mint Selector Display

**CRITICAL:** The wallet UI must display a mint selector component that shows:
- **Active mint selection**: Current mint being used for operations
- **Mint list**: All available mints with balances held with that respective mint
- **Mint management**: Add/remove mints functionality (**REQUIRED** - users must be able to add and remove mints, including the default mint)
- **Balance per mint**: Display balance for each mint (supports sats/fiat toggle)

**Implementation Notes:**
- **Mint management is mandatory**: Users must have full control over their mints. The default mint (`https://mint.minibits.cash/Bitcoin`) is provided for convenience but can be removed just like any other mint.
- Use `useMintManager` hook for mint management state
- Display active mint prominently in wallet header or near payment controls unless otherwise specified
- Show mint selector as dropdown or similar selection component
- Require active mint selection before allowing send/receive operations
- Display mint balances with exchange rate conversion (see `exchange-rates` skill)
- **Never lock users to a specific mint**: All mints (including the default) should be removable via the UI

### Lightning Send/Receive UI Patterns (Example)

**CRITICAL: Use Drawers, Modals, or Separate Pages**

**Do not clutter the home screen with send/receive forms.** Instead, use one of these patterns:

- **Drawers**: Slide up from bottom (mobile-friendly, good for quick actions)
- **Modals**: Full-screen or centered overlays (good for focused workflows)
- **Separate Pages**: Dedicated routes for send/receive flows (good for complex multi-step flows)

**Example implementation for Lightning send and receive operations:**

This is an example implementation that can be customized or replaced based on your design needs. The send/receive UI should handle Lightning invoice input, Lightning address input, amount entry, and payment confirmation flows. **This component is designed to be used inside drawers, modals, or separate pages, not directly on the home screen.**

### Drawer Implementation Example

**How to wrap the payment card in a drawer:**

```typescript
// In your wallet component
import { Drawer, DrawerContent, DrawerDescription, DrawerHeader, DrawerTitle } from '@/components/ui/drawer';
import * as VisuallyHidden from '@radix-ui/react-visually-hidden';
import { LightningPaymentCard } from './LightningPaymentCard';

function WalletComponent() {
  const [showSendDrawer, setShowSendDrawer] = useState(false);
  const [showReceiveDrawer, setShowReceiveDrawer] = useState(false);
  
  // State for send/receive operations
  const [lightningInvoice, setLightningInvoice] = useState('');
  const [lightningAddressInput, setLightningAddressInput] = useState('');
  const [lightningAddressAmount, setLightningAddressAmount] = useState('');
  const [pendingLightningAddress, setPendingLightningAddress] = useState<string | null>(null);
  const [decodedInvoiceAmount, setDecodedInvoiceAmount] = useState<number | null>(null);
  const [pendingInvoice, setPendingInvoice] = useState<string | null>(null);
  const [quoteAmount, setQuoteAmount] = useState('');

  // CRITICAL: Reset all form state when drawer closes
  const handleSendDrawerClose = (open: boolean) => {
    setShowSendDrawer(open);
    if (!open) {
      // Reset all send-related state when drawer closes
      setLightningInvoice('');
      setLightningAddressInput('');
      setLightningAddressAmount('');
      setPendingLightningAddress(null);
      setDecodedInvoiceAmount(null);
      setPendingInvoice(null);
    }
  };

  const handleReceiveDrawerClose = (open: boolean) => {
    setShowReceiveDrawer(open);
    if (!open) {
      // Reset all receive-related state when drawer closes
      setQuoteAmount('');
    }
  };

  return (
    <>
      {/* Action buttons on home screen */}
      <div className="flex gap-4">
        <Button onClick={() => setShowReceiveDrawer(true)}>Receive</Button>
        <Button onClick={() => setShowSendDrawer(true)}>Send</Button>
      </div>

      {/* Send Drawer */}
      <Drawer open={showSendDrawer} onOpenChange={handleSendDrawerClose}>
        <DrawerContent className="min-h-[40vh] max-w-4xl mx-auto">
          <DrawerHeader>
            <DrawerTitle className="text-center text-3xl font-bold">Send</DrawerTitle>
            <VisuallyHidden.Root asChild>
              <DrawerDescription>
                Send Lightning payments
              </DrawerDescription>
            </VisuallyHidden.Root>
          </DrawerHeader>
          <div className="px-4 pb-6 pb-safe-bottom">
            <LightningPaymentCard
              mode="lightning"
              operation="send"
              lightningInvoice={lightningInvoice}
              setLightningInvoice={setLightningInvoice}
              lightningAddressInput={lightningAddressInput}
              setLightningAddressInput={setLightningAddressInput}
              lightningAddressAmount={lightningAddressAmount}
              setLightningAddressAmount={setLightningAddressAmount}
              pendingLightningAddress={pendingLightningAddress}
              setPendingLightningAddress={setPendingLightningAddress}
              decodedInvoiceAmount={decodedInvoiceAmount}
              setDecodedInvoiceAmount={setDecodedInvoiceAmount}
              pendingInvoice={pendingInvoice}
              setPendingInvoice={setPendingInvoice}
              quoteAmount=""
              setQuoteAmount={() => {}}
              activeMintUrl={activeMintUrl}
              onSend={handleSend}
              onReceive={() => {}}
              onConfirmInvoice={handleConfirmInvoicePayment}
              isResolvingAddress={isResolvingAddress}
              isLoading={isLoading}
            />
          </div>
        </DrawerContent>
      </Drawer>

      {/* Receive Drawer */}
      <Drawer open={showReceiveDrawer} onOpenChange={handleReceiveDrawerClose}>
        <DrawerContent className="min-h-[40vh] max-w-4xl mx-auto">
          <DrawerHeader>
            <DrawerTitle className="text-center text-3xl font-bold">Receive</DrawerTitle>
            <VisuallyHidden.Root asChild>
              <DrawerDescription>
                Receive Lightning payments
              </DrawerDescription>
            </VisuallyHidden.Root>
          </DrawerHeader>
          <div className="px-4 pb-6 pb-safe-bottom">
            <LightningPaymentCard
              mode="lightning"
              operation="receive"
              lightningInvoice=""
              setLightningInvoice={() => {}}
              lightningAddressInput=""
              setLightningAddressInput={() => {}}
              lightningAddressAmount=""
              setLightningAddressAmount={() => {}}
              pendingLightningAddress={null}
              setPendingLightningAddress={() => {}}
              decodedInvoiceAmount={null}
              setDecodedInvoiceAmount={() => {}}
              pendingInvoice={null}
              setPendingInvoice={() => {}}
              quoteAmount={quoteAmount}
              setQuoteAmount={setQuoteAmount}
              activeMintUrl={activeMintUrl}
              onSend={() => {}}
              onReceive={handleReceive}
              isResolvingAddress={false}
              isLoading={isLoading}
            />
          </div>
        </DrawerContent>
      </Drawer>
    </>
  );
}
```

**Key points:**
- **State cleanup**: Always reset form state when drawer closes (prevents stale data)
- **Drawer from shadcn/ui**: Use `Drawer`, `DrawerContent`, `DrawerHeader`, `DrawerTitle` components
- **Accessibility**: Include `VisuallyHidden` description for screen readers
- **Mobile-friendly**: Drawers slide up from bottom, perfect for mobile interfaces
- **Clean home screen**: Only show action buttons, not the full forms

```typescript
// components/LightningPaymentCard.tsx (EXAMPLE - customize as needed)
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Download, ArrowRight, Zap, X } from 'lucide-react';
import { useState } from 'react';

interface LightningPaymentCardProps {
  mode: 'lightning';
  operation: 'send' | 'receive';
  // Send props
  lightningInvoice: string;
  setLightningInvoice: (value: string) => void;
  lightningAddressInput: string;
  setLightningAddressInput: (value: string) => void;
  lightningAddressAmount: string;
  setLightningAddressAmount: (value: string) => void;
  pendingLightningAddress: string | null;
  setPendingLightningAddress: (value: string | null) => void;
  decodedInvoiceAmount: number | null;
  setDecodedInvoiceAmount: (value: number | null) => void;
  pendingInvoice: string | null;
  setPendingInvoice: (value: string | null) => void;
  // Receive props
  quoteAmount: string;
  setQuoteAmount: (value: string) => void;
  // Common props
  activeMintUrl: string | null;
  onSend: () => void;
  onReceive: () => void;
  onConfirmInvoice?: () => void;
  isResolvingAddress: boolean;
  isLoading: boolean;
}

// Helper to truncate addresses for display
const truncateAddress = (address: string): string => {
  if (address.length <= 26) return address;
  return address.slice(0, 12) + '...' + address.slice(-12);
};

export function LightningPaymentCard({
  operation,
  lightningInvoice,
  setLightningInvoice,
  lightningAddressInput,
  setLightningAddressInput,
  lightningAddressAmount,
  setLightningAddressAmount,
  pendingLightningAddress,
  setPendingLightningAddress,
  decodedInvoiceAmount,
  setDecodedInvoiceAmount,
  pendingInvoice,
  setPendingInvoice,
  quoteAmount,
  setQuoteAmount,
  activeMintUrl,
  onSend,
  onReceive,
  onConfirmInvoice,
  isResolvingAddress,
  isLoading,
}: LightningPaymentCardProps) {
  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="text-center">
        <div className="text-base text-muted-foreground mt-2">
          {operation === 'send' ? (
            pendingInvoice && decodedInvoiceAmount ? (
              // Invoice confirmation state
              <div className="flex items-center justify-center gap-2">
                <span className="inline-block px-3 py-1.5 bg-primary/10 border border-primary/20 rounded-md">
                  <span className="font-bold text-primary">Sending:</span>{' '}
                  <span className="font-semibold text-foreground">{decodedInvoiceAmount} sats</span>
                </span>
                <button
                  onClick={() => {
                    setPendingInvoice(null);
                    setDecodedInvoiceAmount(null);
                  }}
                  className="p-1.5 rounded-full hover:bg-muted transition-colors"
                  title="Cancel"
                >
                  <X className="h-4 w-4 text-muted-foreground" />
                </button>
              </div>
            ) : pendingLightningAddress ? (
              // Lightning address amount input state
              <div className="flex items-center justify-center gap-2">
                <span className="inline-block px-3 py-1.5 bg-primary/10 border border-primary/20 rounded-md">
                  <span className="font-bold text-primary">Sending:</span>{' '}
                  <span className="font-semibold text-foreground">{truncateAddress(pendingLightningAddress)}</span>
                </span>
                <button
                  onClick={() => {
                    setPendingLightningAddress(null);
                    setLightningAddressAmount('');
                  }}
                  className="p-1.5 rounded-full hover:bg-muted transition-colors"
                  title="Cancel"
                >
                  <X className="h-4 w-4 text-muted-foreground" />
                </button>
              </div>
            ) : (
              'Pay invoices or addresses'
            )
          ) : (
            'Deposit funds with Lightning'
          )}
        </div>
      </div>

      {/* Content */}
      <div className="space-y-8">
        {!activeMintUrl && (
          <div className="text-sm text-muted-foreground bg-muted p-3 rounded">
            {operation === 'send' 
              ? 'Select a mint to pay Lightning invoices'
              : 'Select a mint to create Lightning invoice'}
          </div>
        )}

        {operation === 'send' ? (
          // Send Mode
          pendingInvoice && decodedInvoiceAmount ? (
            // Step 3: Invoice confirmation
            <div className="space-y-8">
              <div className="flex justify-center mt-6 mb-safe-bottom pb-6">
                <Button
                  onClick={onConfirmInvoice}
                  disabled={!activeMintUrl || isLoading}
                  className="h-12 px-12 rounded-full"
                  size="lg"
                >
                  <Zap className="h-5 w-5" />
                </Button>
              </div>
            </div>
          ) : pendingLightningAddress ? (
            // Step 2: Lightning address amount input
            <div className="space-y-8">
              <Input
                placeholder="Amount (sats)"
                type="number"
                value={lightningAddressAmount}
                onChange={(e) => setLightningAddressAmount(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && lightningAddressAmount && activeMintUrl && !isResolvingAddress && !isLoading) {
                    onSend();
                  }
                }}
                disabled={!activeMintUrl}
                className="w-full h-16 !text-base text-center border bg-background focus:ring-2 focus:ring-ring focus:ring-offset-2 [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none [-moz-appearance:textfield]"
              />
              <div className="flex justify-center mt-6 mb-safe-bottom pb-6">
                <Button
                  onClick={onSend}
                  disabled={!lightningAddressAmount || !activeMintUrl || isResolvingAddress || isLoading}
                  className="h-12 px-12 rounded-full"
                  size="lg"
                >
                  <Zap className="h-5 w-5" />
                </Button>
              </div>
            </div>
          ) : (
            // Step 1: Invoice/address input
            <div className="space-y-8">
              <Input
                placeholder="lnbc... or user@domain.com"
                value={lightningInvoice || lightningAddressInput}
                onChange={(e) => {
                  const value = e.target.value;
                  if (value.includes('@')) {
                    setLightningAddressInput(value);
                    setLightningInvoice('');
                  } else {
                    setLightningInvoice(value);
                    setLightningAddressInput('');
                  }
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && (lightningInvoice.trim() || lightningAddressInput.trim()) && activeMintUrl && !isLoading) {
                    onSend();
                  }
                }}
                disabled={!activeMintUrl}
                className="w-full h-16 !text-base text-center border bg-background focus:ring-2 focus:ring-ring focus:ring-offset-2"
              />
              <div className="flex justify-center mt-6 mb-safe-bottom pb-6">
                <Button 
                  onClick={onSend} 
                  disabled={(!lightningInvoice.trim() && !lightningAddressInput.trim()) || !activeMintUrl || isLoading}
                  className="h-12 px-12 rounded-full"
                  size="lg"
                >
                  <ArrowRight className="h-5 w-5" />
                </Button>
              </div>
            </div>
          )
        ) : (
          // Receive Mode
          <div className="space-y-8">
            <Input
              placeholder="Amount (sats)"
              type="number"
              value={quoteAmount}
              onChange={(e) => setQuoteAmount(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && quoteAmount && activeMintUrl && !isLoading) {
                  onReceive();
                }
              }}
              disabled={!activeMintUrl}
              className="w-full h-16 !text-base text-center border bg-background focus:ring-2 focus:ring-ring focus:ring-offset-2 [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none [-moz-appearance:textfield]"
            />
            <div className="flex justify-center mt-6 mb-safe-bottom pb-6">
              <Button 
                onClick={onReceive} 
                disabled={!quoteAmount || !activeMintUrl || isLoading}
                className="h-12 px-12 rounded-full"
                size="lg"
              >
                <Zap className="h-5 w-5" />
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
```

**Example UI Patterns (experiment with these or create your own):**
- **Container patterns**: Use drawers (see drawer implementation example above), modals, or separate pages to contain send/receive flows
- **Multi-step send flow**: Invoice/address input → Amount input (for addresses) → Confirmation → Payment
- **State management**: Track pending invoice, pending address, and decoded amounts
- **State cleanup**: Reset all form state when drawer/modal closes (see drawer implementation example above)
- **Input validation**: Disable buttons when required fields are missing
- **Keyboard support**: Enter key triggers actions
- **Cancel buttons**: Allow users to cancel multi-step flows
- **Visual feedback**: Show pending states with badges and cancel buttons
- **Custom styling**: Adapt the design to match your application's design system
- **Alternative flows**: Experiment with single-step vs multi-step payment flows
- **Error handling**: Display validation errors and payment failures appropriately
- **Loading states**: Show loading indicators during payment processing
- **Success feedback**: Display confirmation messages after successful payments
- **Drawer implementation**: Use `Drawer` from shadcn/ui with proper state cleanup (see drawer implementation example above)

### Invoice Display Modal (Example)

**Example implementation for displaying Lightning invoice with QR code and expiry:**

This is an example implementation that can be customized or replaced based on your design needs. The invoice modal should display the Lightning invoice, QR code for easy scanning, and handle expiry appropriately.

```typescript
// components/InvoiceModal.tsx (EXAMPLE - customize as needed)
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { QRModal } from '@/components/ui/qr-modal';
import { useToast } from '@/hooks/useToast';

export function InvoiceModal({
  isOpen,
  onClose,
  invoice,
}: {
  isOpen: boolean;
  onClose: () => void;
  invoice: {
    quoteId: string;
    mintUrl: string;
    amount: number;
    invoice: string;
    qrCodeUrl: string;
    expiry: number;
  } | null;
}) {
  const { toast } = useToast();
  if (!invoice) return null;

  return (
    <QRModal
      isOpen={isOpen}
      onClose={onClose}
      title="Lightning Invoice"
      description={`Pay ${invoice.amount.toLocaleString()} sats`}
      qrCodeUrl={invoice.qrCodeUrl}
      content={invoice.invoice}
      icon="zap"
      expiryTimestamp={invoice.expiry}
      onExpiry={() => {
        // Default: Toast notification
        toast({ variant: 'destructive', title: 'Invoice Expired', description: 'The invoice has expired. Please create a new one.' });
        // Alternative options (commented):
        // Option 1: Console logging
        // console.error('Invoice Expired: The invoice has expired. Please create a new one.');
        // Option 2: No notification (silent failure)
        onClose();
      }}
    />
  );
}
```

**Example Invoice Display Patterns (experiment with these or create your own):**
- **QR code display**: Show QR code for easy scanning (using `qr-code-generator` skill)
- **Invoice text**: Display invoice string for manual entry or copying
- **Expiry handling**: Show countdown timer or handle expiry gracefully
- **Amount display**: Show invoice amount with optional fiat conversion (using `exchange-rates` skill)
- **Custom styling**: Adapt the modal design to match your application's design system
- **Copy functionality**: Add copy-to-clipboard for invoice string
- **Payment status**: Show payment status updates when invoice is paid

### Balance Display (Example)

**Example implementation for displaying Lightning wallet balance with exchange rate conversion:**

This is an example implementation that can be customized or replaced based on your design needs. The balance display should show the total balance across all mints, optionally with exchange rate conversion.

```typescript
// components/LightningBalanceDisplay.tsx (EXAMPLE - customize as needed)
import { useState, useEffect } from 'react';
import { getBtcUsdRate } from '@/lib/exchangeRateService';

interface LightningBalanceDisplayProps {
  totalBalance: number; // Total balance in sats
}

export function LightningBalanceDisplay({ totalBalance }: LightningBalanceDisplayProps) {
  const [showSats, setShowSats] = useState(true);
  const [btcUsdRate, setBtcUsdRate] = useState<number | null>(null);

  useEffect(() => {
    getBtcUsdRate()
      .then(rate => setBtcUsdRate(rate))
      .catch(() => setBtcUsdRate(null));
  }, []);

  const formatBalance = (): string => {
    if (showSats) {
      return totalBalance.toLocaleString();
    }
    
    if (btcUsdRate) {
      const usdAmount = (totalBalance / 100000000 * btcUsdRate).toFixed(2);
      return usdAmount;
    }
    
    return totalBalance.toLocaleString();
  };

  return (
    <div className="text-center py-2">
      <div className="flex items-center justify-center gap-3">
        <button
          onClick={() => setShowSats(!showSats)}
          className="text-6xl font-bold tabular-nums hover:opacity-80 transition-opacity cursor-pointer"
          title={`Click to show in ${showSats ? 'USD' : 'sats'}`}
        >
          <span className="italic">
            {showSats ? (
              <span className="text-orange-500/70">₿</span>
            ) : (
              <span className="text-green-500/70">$</span>
            )}
          </span>
          {formatBalance()}
        </button>
      </div>
    </div>
  );
}
```

**Example Balance Display Patterns (experiment with these or create your own):**
- **Toggle between sats and local currency**: Click balance to switch display mode
- **Exchange rate integration**: Fetch and display real-time rates using the `exchange-rates` skill
- **Responsive formatting**: Use toLocaleString() for number formatting
- **Custom styling**: Adapt the visual design to match your application's design system
- **Multiple currency support**: Extend to support multiple fiat currencies beyond USD
- **Balance breakdown**: Show balance per mint or other custom breakdowns

## Part 9: Best Practices

### Automatic Quote Processing

**Enable built-in services for automatic handling:**

```typescript
// In wallet initialization
await coco.enableMintQuoteWatcher({ watchExistingPendingOnStart: false });
await coco.enableMintQuoteProcessor();
await coco.enableProofStateWatcher();
```

**Benefits:**
- Automatically detects when invoices are paid
- Processes quotes without manual intervention
- Updates wallet state automatically
- Emits events for UI updates

### Event-Driven Architecture

**Use events for reactive UI updates:**

```typescript
// Listen to all relevant events
const unsubs = [
  coco.on('mint-quote:redeemed', handlePaymentReceived),
  coco.on('melt-quote:paid', handlePaymentSent),
  coco.on('proofs:saved', refreshBalances),
  coco.on('history:updated', refreshHistory),
];

// Clean up on unmount
return () => unsubs.forEach(unsub => unsub());
```

### Mint Selection

**Always require active mint for operations:**

```typescript
import { useToast } from '@/hooks/useToast';

// In a component or hook:
const { toast } = useToast();

if (!activeMintUrl) {
  // Default: Toast notification
  toast({ variant: 'destructive', title: 'No Mint Selected', description: 'Please select a mint before performing this operation.' });
  // Alternative options (commented):
  // Option 1: Console logging
  // console.error('No Mint Selected: Please select a mint before performing this operation.');
  // Option 2: No notification (silent failure)
  return;
}
```

## Part 10: Common Pitfalls

### 1. ❌ Not checking mint availability

**Problem:** Attempting operations without an active mint causes errors.

**Solution:** Always check for active mint before operations:
```typescript
if (!activeMintUrl || !coco) {
  return; // Or show error
}
```

### 2. ❌ Not handling quote expiry

**Problem:** Displaying expired invoices confuses users.

**Solution:** Check expiry before displaying and show countdown:
```typescript
const now = Math.floor(Date.now() / 1000);
if (quote.expiry <= now) {
  // Handle expired quote
}
```

### 3. ❌ Not cleaning up event listeners

**Problem:** Memory leaks from uncleaned event listeners.

**Solution:** Always return cleanup function:
```typescript
useEffect(() => {
  const unsubscribe = coco.on('event', handler);
  return () => unsubscribe();
}, [coco]);
```

### 4. ❌ Concurrent payment processing

**Problem:** Multiple simultaneous payments cause race conditions.

**Solution:** Use processing state flag:
```typescript
const [isProcessingPayment, setIsProcessingPayment] = useState(false);

if (isProcessingPayment) return; // Prevent concurrent execution
setIsProcessingPayment(true);
try {
  // Process payment
} finally {
  setIsProcessingPayment(false);
}
```

### 5. ❌ Not validating invoice format

**Problem:** Invalid invoices cause melt quote failures.

**Solution:** Always validate before processing:
```typescript
if (!isValidBolt11Invoice(invoice)) {
  // Optional: User feedback - choose one:
  // Option 1: Console logging
  // console.error('Invalid Invoice');
  // Option 2: Toast notification (if toast is available)
  // toast({ variant: 'destructive', title: 'Invalid Invoice' });
  // Option 3: No notification (silent failure)
  return;
}
```

### 6. ❌ Build errors: Failed to fetch from esm.sh

**Problem:** Build fails with dependency fetch errors.

**Solution:** Ensure all required packages are in `package.json` with the exact versions specified in Prerequisites:
- `@cashu/cashu-ts@2.8.1` (exact version - prevents 3.0.2 resolution)
- `@scure/bip39@1.6.0` (compatible with both `@noble/hashes@1.8.0` and `@noble/hashes@^2.0.1`)
- `@scure/bip32@^2.0.1` (required by `coco-cashu-core@1.1.2-rc.30` which uses `@noble/hashes@^2.0.1`)
- `@noble/curves@^2.0.1` (required by `coco-cashu-core@1.1.2-rc.30`)
- `@noble/hashes@^2.0.1` (required by `coco-cashu-core@1.1.2-rc.30`)

**Common Error Patterns:**
- `@cashu/cashu-ts@3.0.2` in errors → Explicitly add `@cashu/cashu-ts@2.8.1` to lock it
- `@noble/hashes@1.x` in errors → Update to `@noble/hashes@^2.0.1` (required by `coco-cashu-core@1.1.2-rc.30`)
- `@scure/bip32@1.7.0` in errors → Update to `@scure/bip32@^2.0.1` (required by `coco-cashu-core@1.1.2-rc.30`)

## Security Considerations

1. **Mnemonic Storage**: Store mnemonic securely (localStorage is acceptable for browser wallets, but consider encryption for production)
2. **Mint Trust**: Only trust mints from verified sources
3. **Invoice Validation**: Always validate BOLT11 invoices before processing
4. **Amount Verification**: Confirm amounts before processing payments
5. **Error Handling**: Don't expose internal errors to users
6. **Quote Expiry**: Always check quote expiry before displaying

## Verification Checklist

- [ ] Wallet initializes correctly with IndexedDB backend
- [ ] Default mint (`https://mint.minibits.cash/Bitcoin`) is automatically added if no mints exist
- [ ] Mnemonic generation and validation works
- [ ] Mint management (add, remove, trust) functions correctly
- [ ] **REQUIRED:** Users can remove the default mint (not locked to it)
- [ ] **REQUIRED:** Users can add their own mints
- [ ] Mint quotes create valid Lightning invoices
- [ ] Melt quotes pay invoices successfully
- [ ] Transaction history displays correctly
- [ ] Event listeners update UI reactively
- [ ] **REQUIRED:** `qr-code-generator` skill implemented and working
- [ ] **REQUIRED:** `lightning-address` skill implemented and working
- [ ] **REQUIRED:** `lightning-invoice-decoder` skill implemented and working
- [ ] **REQUIRED:** `exchange-rates` skill implemented and working
- [ ] Lightning address integration works (sending payments)
- [ ] BOLT11 invoice decoding works (validation and amount extraction)
- [ ] QR code generation for invoices works (display in modals, drawers, new screens, etc.)
- [ ] Exchange rate display works (BTC/fiat conversions)
- [ ] **OPTIONAL:** `npub-cash-address` skill implemented for static Lightning addresses
- [ ] Error handling covers all failure cases
- [ ] Quote expiry is handled gracefully
- [ ] Concurrent payment prevention works

## Summary

To implement a Lightning wallet with Cashu mints:

1. **Install dependencies** - Add all required packages to `package.json`: `@cashu/cashu-ts@2.8.1`, `coco-cashu-core@1.1.2-rc.30`, `coco-cashu-indexeddb@1.1.2-rc.30`, `dexie@^4.0.8`, `@scure/bip39@1.6.0`, `@scure/bip32@^2.0.1` (if using BIP32), `@noble/hashes@^2.0.1`, `@noble/curves@^2.0.1`
2. **Initialize wallet** - Use `initializeCoco` with IndexedDB repositories
3. **Add default mint** - Automatically add `https://mint.minibits.cash/Bitcoin` as the default mint if no mints exist (users can remove it later)
4. **Manage mints** - Add, remove, and trust Cashu mints (**REQUIRED**: Users must be able to add/remove mints, including the default mint)
5. **Receive payments** - Create mint quotes to generate Lightning invoices
6. **Send payments** - Create melt quotes to pay Lightning invoices
7. **Track history** - Use history manager to display transactions
8. **Integrate required skills** - Implement `qr-code-generator`, `lightning-address`, `lightning-invoice-decoder`, and `exchange-rates` skills
9. **Optional: Static addresses** - Implement `npub-cash-address` skill for permanent Lightning addresses (`username@npubx.cash`)
10. **Handle events** - Listen to coco events for reactive updates
11. **Enable services** - Use built-in watchers and processors for automatic handling

**Key principle:** This is a Lightning wallet, not a token wallet. Focus on minting (receiving) and melting (sending) operations, not token transfers or splitting.

**Default Mint:** The wallet automatically adds `https://mint.minibits.cash/Bitcoin` as a default mint for convenience, but users are NOT locked to it. Full mint management (add/remove) must be implemented so users can remove the default mint and add their own mints.

**Note:** All required dependencies are listed in Prerequisites. If build fails, verify all packages are present with correct versions (especially `@cashu/cashu-ts@2.8.1` to prevent 3.0.2 resolution, `coco-cashu-core@1.1.2-rc.30` and `coco-cashu-indexeddb@1.1.2-rc.30` for the latest features, and `dexie@^4.0.8` for IndexedDB support).

