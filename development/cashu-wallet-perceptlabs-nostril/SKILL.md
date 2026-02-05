---
name: cashu-wallet
description: Use when implementing Cashu token wallet functionality - provides complete patterns for sending and receiving Cashu tokens, token QR codes, automatic mint management, and integrating with Lightning wallet operations
when_to_use: When building a Cashu token wallet, implementing token send/receive operations, handling Cashu token transfers, managing token QR codes, or building a full-featured wallet that combines both Lightning and token operations
---

# Cashu Token Wallet Implementation

## Overview

Complete implementation guide for a Cashu token wallet using the coco-cashu-core library. This wallet focuses on Cashu token operations (sending and receiving tokens) and integrates with Lightning wallet functionality for minting and melting operations.

**Core Capabilities:**
- Send Cashu tokens to other users
- Receive Cashu tokens from other users
- Generate QR codes for token sharing
- Automatic mint management (add unknown mints automatically)
- Token encoding/decoding for sharing
- Integration with Lightning wallet for mint/melt operations
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
- `lightning-wallet` - **MANDATORY** - Lightning wallet operations (minting, melting, mint management, history) (see `lightning-wallet` skill)
- `qr-code-generator` - QR code generation for Cashu tokens (see `qr-code-generator` skill)
- `exchange-rates` - Exchange rate functionality for displaying BTC/fiat conversions (see `exchange-rates` skill)

**Optional skills:**
- `emoji-encoder` - Steganographic encoding for sharing tokens via emoji (typically 🥜 peanut emoji) (see `emoji-encoder` skill)

**Note:** Cashu token wallets require Lightning functionality because:
- Users need to mint tokens (receive Lightning payments) to get tokens
- Users need to melt tokens (send Lightning payments) to convert tokens to Lightning
- Mint management is shared between Lightning and token operations

## Implementation Checklist

- [ ] Add all required packages to `package.json`: `@cashu/cashu-ts@2.8.1`, `coco-cashu-core@1.1.2-rc.30`, `coco-cashu-indexeddb@1.1.2-rc.30`, `dexie@^4.0.8`, `@scure/bip39@1.6.0`, `@scure/bip32@^2.0.1` (if using BIP32), `@noble/hashes@^2.0.1`, `@noble/curves@^2.0.1`
- [ ] **REQUIRED:** Implement `lightning-wallet` skill (wallet initialization, mint management, history)
- [ ] Implement token receive operations
- [ ] Implement token send operations
- [ ] Add automatic mint management for unknown mints
- [ ] **REQUIRED:** Implement `qr-code-generator` skill for token QR codes
- [ ] **REQUIRED:** Implement `exchange-rates` skill for BTC/fiat conversions
- [ ] Add token encoding/decoding for sharing
- [ ] **OPTIONAL:** Implement `emoji-encoder` skill for emoji-based token sharing
- [ ] Integrate with Lightning wallet for shared functionality
- [ ] Add error handling and user feedback
- [ ] Create React hooks for token operations

## Part 1: Understanding Cashu Token Wallets

### Token Wallet vs Lightning Wallet

**Cashu Token Wallet:**
- Focuses on **token operations**: sending and receiving Cashu tokens
- Tokens are bearer assets that can be transferred peer-to-peer
- Requires Lightning wallet for minting (getting tokens) and melting (converting tokens to Lightning)

**Lightning Wallet:**
- Focuses on **Lightning operations**: minting (receiving Lightning) and melting (sending Lightning)
- Does not require token operations
- Can be standalone

**Relationship:**
- **Cashu token wallets require Lightning wallets** - You need Lightning functionality to mint and melt tokens
- **Lightning wallets do not require token wallets** - Lightning operations work independently
- **Shared functionality**: Both use the same mint management, wallet initialization, and transaction history

### Cashu Token Flow

1. **Getting Tokens (Minting)**: Use Lightning wallet to receive Lightning payments → tokens are issued
2. **Sending Tokens**: Create a token with specified amount → share token (QR code or text)
3. **Receiving Tokens**: Redeem token → tokens are added to wallet balance
4. **Converting to Lightning (Melting)**: Use Lightning wallet to send Lightning payments → tokens are deducted

### Token Format

Cashu tokens are encoded as strings (base64 or JSON) containing:
- Proofs (blinded signatures from mints)
- Mint URLs
- Amounts and denominations

Tokens can be shared via:
- QR codes (most common)
- Text/copy-paste
- Emoji encoding (using `emoji-encoder` skill - typically encoded into 🥜 peanut emoji)
- NFC or other transfer methods

## Part 2: Token Operations Hook

### Token Operations Implementation

**Complete token send/receive hook:**

```typescript
// hooks/wallet/useTokenOperations.ts
import { useState, useCallback } from 'react';
import { isUnknownMintError, extractMintUrlFromError } from './useMintManager';
import type { Manager } from 'coco-cashu-core';
import type { Token } from '@cashu/cashu-ts';
import { useToast } from '@/hooks/useToast';
// Optional: emoji-encoder skill
import { isEncoded, decode } from '@/lib/emojiEncoder';

interface UseTokenOperationsProps {
  coco: Manager | null;
  activeMintUrl: string | null;
  generateQRCode: (text: string) => Promise<string>;
  getEncodedToken: (token: Token | string) => string;
}

export function useTokenOperations({
  coco,
  activeMintUrl,
  generateQRCode,
  getEncodedToken,
}: UseTokenOperationsProps) {
  // Default: Toast notifications
  const { toast } = useToast();
  // Alternative options (commented):
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: No notification handler
  
  // Receive state
  const [tokenInput, setTokenInput] = useState('');
  
  // Send state
  const [sendAmount, setSendAmount] = useState('');
  
  // Transaction output state
  const [sentToken, setSentToken] = useState<string | null>(null);
  const [sentTokenQRCode, setSentTokenQRCode] = useState<string>('');

  // Generate QR code for sent token
  const generateSentTokenQRCode = useCallback(async (token: string) => {
    try {
      const qrCodeUrl = await generateQRCode(token);
      setSentTokenQRCode(qrCodeUrl);
    } catch (err) {
      console.error('Failed to generate sent token QR code:', err);
    }
  }, [generateQRCode]);

  // Handle unknown mint error by adding the mint and retrying
  const handleUnknownMintError = useCallback(
    async (mintUrl: string) => {
      if (!coco) return;

      try {
        console.log('Adding unknown mint:', mintUrl);

        // Check if mint exists (known) by checking all mints
        const allMints = await coco.mint.getAllMints();
        const isKnown = allMints.some(m => m.mintUrl.toLowerCase() === mintUrl.toLowerCase());
        
        if (isKnown) {
          // Mint exists but may not be trusted, ensure it's trusted
          const isTrusted = await coco.mint.isTrustedMint(mintUrl);
          if (!isTrusted) {
            await coco.mint.trustMint(mintUrl);
          }
        } else {
          // Add the mint and automatically trust it (user is explicitly receiving from it)
          await coco.mint.addMint(mintUrl, { trusted: true });
        }

        // Retry receiving the token
        await coco.wallet.receive(tokenInput);
        setTokenInput('');

        // Default: Toast notification
        toast({ title: 'Token Received', description: `Cashu token redeemed successfully! Added new mint: ${mintUrl}` });
        // Alternative options (commented):
        // Option 1: Console logging
        // console.log('Token Received: Cashu token redeemed successfully! Added new mint:', mintUrl);
        // Option 2: No notification (silent success)
      } catch (retryErr) {
        // Default: Toast notification
        toast({ variant: 'destructive', title: 'Receive Failed', description: `Failed to add mint and receive token: ${retryErr instanceof Error ? retryErr.message : 'Unknown error'}` });
        // Alternative options (commented):
        // Option 1: Console logging
        // console.error('Receive Failed:', retryErr instanceof Error ? retryErr.message : 'Unknown error');
        // Option 2: No notification (silent failure)
      }
    },
    [coco, tokenInput, toast]
  );

  // Handle receive (token)
  const handleTokenReceive = useCallback(async () => {
    if (!coco || !tokenInput) {
      return;
    }

    try {
      let tokenToProcess = tokenInput.trim();
      
      // Check if input is emoji-encoded (optional: using emoji-encoder skill)
      if (isEncoded && isEncoded(tokenToProcess)) {
        try {
          tokenToProcess = decode(tokenToProcess);
        } catch (decodeErr) {
          // Default: Toast notification
          toast({ variant: 'destructive', title: 'Invalid Emoji Token', description: 'Failed to decode emoji-encoded token' });
          // Alternative options (commented):
          // Option 1: Console logging
          // console.error('Invalid Emoji Token: Failed to decode emoji-encoded token');
          // Option 2: No notification (silent failure)
          return;
        }
      }
      
      console.log(
        'Attempting to receive token:',
        tokenToProcess.substring(0, 20) + '...'
      );
      await coco.wallet.receive(tokenToProcess);
      setTokenInput('');
      // Default: Toast notification
      toast({ title: 'Token Received', description: 'Cashu token redeemed successfully!' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.log('Token Received: Cashu token redeemed successfully!');
      // Option 2: No notification (silent success)
    } catch (err) {
      console.error('Token receive error:', err);

      // Handle UnknownMintError by automatically adding the mint
      if (isUnknownMintError(err)) {
        const mintUrl = extractMintUrlFromError(err);
        if (mintUrl) {
          await handleUnknownMintError(mintUrl);
          return;
        }
      }

      // Default: Toast notification
      toast({ variant: 'destructive', title: 'Receive Failed', description: err instanceof Error ? err.message : 'Unknown error' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Receive Failed:', err instanceof Error ? err.message : 'Unknown error');
      // Option 2: No notification (silent failure)
    }
  }, [coco, tokenInput, handleUnknownMintError, toast]);

  // Handle send (token)
  const handleTokenSend = useCallback(async () => {
    if (!coco || !sendAmount || !activeMintUrl) {
      return;
    }

    try {
      const amount = parseInt(sendAmount);
      if (isNaN(amount) || amount <= 0) {
        // Default: Toast notification
        toast({ variant: 'destructive', title: 'Invalid Amount', description: 'Please enter a valid amount' });
        // Alternative options (commented):
        // Option 1: Console logging
        // console.error('Invalid Amount: Please enter a valid amount');
        // Option 2: No notification (silent failure)
        return;
      }
      
      const token = await coco.wallet.send(activeMintUrl, amount);
      const encodedToken = getEncodedToken(token);
      setSentToken(encodedToken);
      await generateSentTokenQRCode(encodedToken);
      setSendAmount('');
    } catch (err) {
      // Default: Toast notification
      toast({ variant: 'destructive', title: 'Send Failed', description: err instanceof Error ? err.message : 'Unknown error' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Send Failed:', err instanceof Error ? err.message : 'Unknown error');
      // Option 2: No notification (silent failure)
    }
  }, [coco, sendAmount, activeMintUrl, getEncodedToken, generateSentTokenQRCode, toast]);

  return {
    // Receive state
    tokenInput,
    setTokenInput,
    // Send state
    sendAmount,
    setSendAmount,
    // Transaction output state
    sentToken,
    setSentToken,
    sentTokenQRCode,
    // Handlers
    handleTokenReceive,
    handleTokenSend,
  };
}
```

**Key Operations:**
- **Token Receive**: `coco.wallet.receive(tokenString)` - Redeems a Cashu token
- **Token Send**: `coco.wallet.send(mintUrl, amount)` - Creates a new token with specified amount
- **Token Encoding**: `getEncodedToken(token)` - Encodes token for sharing
- **QR Code Generation**: **REQUIRED** - Uses `qr-code-generator` skill for token QR codes
- **Automatic Mint Management**: Automatically adds and trusts unknown mints when receiving tokens

## Part 3: Integration with Lightning Wallet

### Shared Functionality

**CRITICAL:** The `lightning-wallet` skill is **mandatory** for Cashu token wallets. Reference it for:

1. **Wallet Initialization** - Use `useCashu` hook from lightning-wallet skill
2. **Mint Management** - Use `useMintManager` hook from lightning-wallet skill
3. **Transaction History** - Use `useHistoryManager` hook from lightning-wallet skill
4. **Lightning Operations** - Use `useLightningOperations` hook for minting/melting

### Wallet Initialization

**Use the same wallet initialization as Lightning wallet:**

```typescript
// Import from lightning-wallet skill
import { useCashu } from '@/hooks/wallet/useCashu';

// In your component
const {
  coco,
  repositories,
  balances,
  mints,
  totalBalance,
  isInitialized,
  isLoading,
  error,
} = useCashu();

// Use the same coco manager for both Lightning and token operations
```

### Mint Management

**Use the same mint management as Lightning wallet:**

```typescript
// Import from lightning-wallet skill
import { useMintManager } from '@/hooks/wallet/useMintManager';

// In your component
const {
  activeMintUrl,
  setActiveMintUrl,
  handleAddMint,
  handleRemoveMintClick,
  handleConfirmRemoveMint,
  getCleanMintLabel,
} = useMintManager({
  coco,
  mints,
  repositories,
  refreshMints,
});
```

### Transaction History

**Use the same history manager as Lightning wallet:**

```typescript
// Import from lightning-wallet skill
import { useHistoryManager } from '@/hooks/wallet/useHistoryManager';

// In your component
const {
  historyEntries,
  isLoadingHistory,
  isHistoryExpanded,
  setIsHistoryExpanded,
  loadHistory,
} = useHistoryManager({
  coco,
  isInitialized,
});
```

**Note:** History includes both Lightning operations (mint/melt) and token operations (send/receive).

## Part 4: Token Receive Operations

### Receiving Tokens

**Basic token receive:**

```typescript
// User pastes or scans a token
const tokenString = 'cashuAeyJ0b2tlbiI6...'; // Encoded token

// Receive the token
await coco.wallet.receive(tokenString);

// Tokens are automatically added to wallet balance
// Balance updates via event listeners (see lightning-wallet skill)
```

### Automatic Mint Management

**When receiving tokens from unknown mints:**

```typescript
try {
  await coco.wallet.receive(tokenString);
} catch (err) {
  if (isUnknownMintError(err)) {
    const mintUrl = extractMintUrlFromError(err);
    if (mintUrl) {
      // Automatically add and trust the mint
      const allMints = await coco.mint.getAllMints();
      const isKnown = allMints.some(m => 
        m.mintUrl.toLowerCase() === mintUrl.toLowerCase()
      );
      
      if (isKnown) {
        // Ensure mint is trusted
        const isTrusted = await coco.mint.isTrustedMint(mintUrl);
        if (!isTrusted) {
          await coco.mint.trustMint(mintUrl);
        }
      } else {
        // Add new mint and trust it
        await coco.mint.addMint(mintUrl, { trusted: true });
      }
      
      // Retry receiving the token
      await coco.wallet.receive(tokenString);
    }
  }
}
```

**Key Points:**
- **Automatic Mint Addition**: Unknown mints are automatically added when receiving tokens
- **Trust Management**: Mints are automatically trusted when receiving tokens (user explicitly accepts)
- **Error Recovery**: Retry token receive after adding mint

### Token Input Validation

**Validate token format before processing (handles emoji-encoded tokens):**

```typescript
import { isEncoded, decode } from '@/lib/emojiEncoder'; // Optional: emoji-encoder skill

function isValidCashuToken(token: string): boolean {
  if (!token || typeof token !== 'string') {
    return false;
  }
  
  let tokenToValidate = token.trim();
  
  // Check if token is emoji-encoded (optional: using emoji-encoder skill)
  if (isEncoded && isEncoded(tokenToValidate)) {
    try {
      // Decode emoji-encoded token first
      tokenToValidate = decode(tokenToValidate);
    } catch {
      return false; // Failed to decode emoji
    }
  }
  
  // Cashu tokens are base64-encoded JSON or plain JSON
  // Check for common patterns
  // Base64 encoded tokens start with 'cashuA' or 'cashu'
  if (tokenToValidate.startsWith('cashuA') || tokenToValidate.startsWith('cashu')) {
    return true;
  }
  
  // JSON tokens start with '{'
  if (tokenToValidate.startsWith('{')) {
    try {
      JSON.parse(tokenToValidate);
      return true;
    } catch {
      return false;
    }
  }
  
  return false;
}

// Usage with emoji decoding
import { useToast } from '@/hooks/useToast';

function handleTokenReceive() {
  const { toast } = useToast();
  let tokenToProcess = tokenInput.trim();
  
  // Check if input is emoji-encoded (optional: using emoji-encoder skill)
  if (isEncoded && isEncoded(tokenToProcess)) {
    try {
      tokenToProcess = decode(tokenToProcess);
    } catch (err) {
      // Default: Toast notification
      toast({ variant: 'destructive', title: 'Invalid Emoji Token', description: 'Failed to decode emoji-encoded token' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Invalid Emoji Token: Failed to decode emoji-encoded token');
      // Option 2: No notification (silent failure)
      return;
    }
  }
  
  if (!isValidCashuToken(tokenToProcess)) {
    // Default: Toast notification
    toast({ variant: 'destructive', title: 'Invalid Token', description: 'This does not appear to be a valid Cashu token' });
    // Alternative options (commented):
    // Option 1: Console logging
    // console.error('Invalid Token: This does not appear to be a valid Cashu token');
    // Option 2: No notification (silent failure)
    return;
  }
  
  // Proceed with receive
  await coco.wallet.receive(tokenToProcess);
}
```

## Part 5: Token Send Operations

### Sending Tokens

**Create and share a token:**

```typescript
// User specifies amount to send
const amount = 1000; // sats

// Create token from active mint
const token = await coco.wallet.send(activeMintUrl, amount);

// Encode token for sharing
const encodedToken = getEncodedToken(token);

// Generate QR code (REQUIRED: use qr-code-generator skill)
const qrCodeUrl = await generateQRCode(encodedToken);

// Display QR code or allow copy-paste
```

### Token Encoding

**Encode tokens for sharing:**

```typescript
// Import from coco-cashu-core
import { getEncodedToken } from 'coco-cashu-core';

// Encode token
const encodedToken = getEncodedToken(token);

// Token can now be shared via:
// - QR code
// - Text/copy-paste
// - NFC
// - Other transfer methods
```

### QR Code Generation (Required)

**CRITICAL:** The `qr-code-generator` skill is mandatory for this wallet. You must generate QR codes for Cashu tokens, but the specific display location and format are flexible.

**Example implementation for generating and displaying QR codes:**

This is an example implementation that can be customized or replaced based on your design needs. The requirement is to generate QR codes for tokens, but how and where you display them (modals, drawers, separate pages, etc.) is up to you.

```typescript
// Example: Using qr-code-generator skill (EXAMPLE - customize as needed)
// Import from qr-code-generator skill
import { useQRCodeGenerator } from '@/hooks/useQRCodeGenerator';

// In your component
const { generateQRCode } = useQRCodeGenerator();

// After creating token
const token = await coco.wallet.send(activeMintUrl, amount);
const encodedToken = getEncodedToken(token);
const qrCodeUrl = await generateQRCode(encodedToken);

// Example display in modal (customize this to match your design)
// QR codes could also be displayed in drawers, separate pages, or other UI patterns
<QRModal
  isOpen={showTokenModal}
  onClose={() => setShowTokenModal(false)}
  title="Cashu Token"
  description={`Send ${amount.toLocaleString()} sats`}
  qrCodeUrl={qrCodeUrl}
  content={encodedToken}
  icon="qr"
/>
```

**Example Usage Patterns (experiment with these or create your own):**
- **QR code generation**: Generate QR codes for all Cashu tokens
- **Display location**: Display QR codes in modals, drawers, separate pages, or inline components
- **Token text**: Include token string alongside QR code for manual entry or copying
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
const balanceSats = totalBalance; // From useCashu hook
const usdValue = rate ? (balanceSats / 100_000_000) * rate : null;

// Example display (customize this to match your design)
return (
  <div>
    <div className="text-2xl font-bold">
      {balanceSats.toLocaleString()} sats
    </div>
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
- **Transaction amounts**: Show token send/receive amounts in both sats and fiat
- **Token amounts**: Convert token amounts to fiat for user understanding
- **Display location**: Place exchange rate in wallet header, balance section, or transaction details
- **Multiple currencies**: Support multiple fiat currencies beyond USD
- **Custom formatting**: Adapt the display format to match your application's design system
- **Real-time updates**: Refresh exchange rates periodically or on user interaction

### Emoji Encoding Integration (Optional)

**OPTIONAL:** The `emoji-encoder` skill provides steganographic encoding for sharing tokens via emoji. Use it to encode Cashu tokens into emojis (typically the 🥜 peanut emoji) for easy sharing:

```typescript
// Import from emoji-encoder skill
import { encode, decode, isEncoded } from '@/lib/emojiEncoder';

// After creating token
const token = await coco.wallet.send(activeMintUrl, amount);
const encodedToken = getEncodedToken(token);

// Encode token into peanut emoji
const emojiToken = encode('🥜', encodedToken);

// Share the emoji (appears as just "🥜" but contains full token)
// User can copy/paste the emoji or share it in messages

// When receiving, decode the emoji
if (isEncoded(tokenInput)) {
  const decodedToken = decode(tokenInput);
  // decodedToken contains the full Cashu token string
  await coco.wallet.receive(decodedToken);
}
```

**Benefits of emoji encoding:**
- Tokens appear as a single emoji (🥜) - easy to share
- Works in any text-based communication (messages, social media, etc.)
- Invisible encoding - looks like just an emoji
- Can be decoded by any wallet that supports emoji-encoder

**Usage in token sharing:**
- Encode tokens into peanut emoji for social sharing
- Share via text messages, social media, or any text platform
- Decode emoji tokens when receiving
- Display emoji option alongside QR code and copy options

## Part 6: Token Display Components

### Token Send/Receive UI Patterns (Example)

**CRITICAL: Use Drawers, Modals, or Separate Pages**

**Do not clutter the home screen with send/receive forms.** Instead, use one of these patterns:

- **Drawers**: Slide up from bottom (mobile-friendly, good for quick actions)
- **Modals**: Full-screen or centered overlays (good for focused workflows)
- **Separate Pages**: Dedicated routes for send/receive flows (good for complex multi-step flows)

**Example implementation for Cashu token send and receive operations:**

This is an example implementation that can be customized or replaced based on your design needs. The send/receive UI should handle token input, amount entry, and token sharing flows. **This component is designed to be used inside drawers, modals, or separate pages, not directly on the home screen.**

### Drawer Implementation Example

**How to wrap the payment card in a drawer:**

```typescript
// In your wallet component
import { Drawer, DrawerContent, DrawerDescription, DrawerHeader, DrawerTitle } from '@/components/ui/drawer';
import * as VisuallyHidden from '@radix-ui/react-visually-hidden';
import { TokenPaymentCard } from './TokenPaymentCard';

function WalletComponent() {
  const [showSendDrawer, setShowSendDrawer] = useState(false);
  const [showReceiveDrawer, setShowReceiveDrawer] = useState(false);
  
  // State for send/receive operations
  const [sendAmount, setSendAmount] = useState('');
  const [tokenInput, setTokenInput] = useState('');

  // CRITICAL: Reset all form state when drawer closes
  const handleSendDrawerClose = (open: boolean) => {
    setShowSendDrawer(open);
    if (!open) {
      // Reset all send-related state when drawer closes
      setSendAmount('');
    }
  };

  const handleReceiveDrawerClose = (open: boolean) => {
    setShowReceiveDrawer(open);
    if (!open) {
      // Reset all receive-related state when drawer closes
      setTokenInput('');
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
                Send Cashu tokens
              </DrawerDescription>
            </VisuallyHidden.Root>
          </DrawerHeader>
          <div className="px-4 pb-6 pb-safe-bottom">
            <TokenPaymentCard
              mode="tokens"
              operation="send"
              sendAmount={sendAmount}
              setSendAmount={setSendAmount}
              tokenInput=""
              setTokenInput={() => {}}
              activeMintUrl={activeMintUrl}
              onSend={handleTokenSend}
              onReceive={() => {}}
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
                Receive Cashu tokens
              </DrawerDescription>
            </VisuallyHidden.Root>
          </DrawerHeader>
          <div className="px-4 pb-6 pb-safe-bottom">
            <TokenPaymentCard
              mode="tokens"
              operation="receive"
              sendAmount=""
              setSendAmount={() => {}}
              tokenInput={tokenInput}
              setTokenInput={setTokenInput}
              activeMintUrl={activeMintUrl}
              onSend={() => {}}
              onReceive={handleTokenReceive}
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
// components/TokenPaymentCard.tsx (EXAMPLE - customize as needed)
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Download } from 'lucide-react';

interface TokenPaymentCardProps {
  mode: 'tokens';
  operation: 'send' | 'receive';
  // Send props
  sendAmount: string;
  setSendAmount: (value: string) => void;
  // Receive props
  tokenInput: string;
  setTokenInput: (value: string) => void;
  // Common props
  activeMintUrl: string | null;
  onSend: () => void;
  onReceive: () => void;
  isLoading: boolean;
}

export function TokenPaymentCard({
  operation,
  sendAmount,
  setSendAmount,
  tokenInput,
  setTokenInput,
  activeMintUrl,
  onSend,
  onReceive,
  isLoading,
}: TokenPaymentCardProps) {
  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="text-center">
        <div className="text-base text-muted-foreground mt-2">
          {operation === 'send' ? (
            'Generate Cashu token to send'
          ) : (
            'Enter Cashu token to redeem'
          )}
        </div>
      </div>

      {/* Content */}
      <div className="space-y-8">
        {!activeMintUrl && (
          <div className="text-sm text-muted-foreground bg-muted p-3 rounded">
            {operation === 'send' 
              ? 'Select a mint to send tokens'
              : 'Select a mint to receive tokens'}
          </div>
        )}

        {operation === 'send' ? (
          // Send Mode: Amount input
          <div className="space-y-8">
            <Input
              placeholder="Amount (sats)"
              type="number"
              value={sendAmount}
              onChange={(e) => setSendAmount(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && sendAmount && activeMintUrl && !isLoading) {
                  onSend();
                }
              }}
              disabled={!activeMintUrl}
              className="w-full h-16 !text-base text-center border bg-background focus:ring-2 focus:ring-ring focus:ring-offset-2 [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none [-moz-appearance:textfield]"
            />
            <div className="flex justify-center mt-6 mb-safe-bottom pb-6">
              <Button 
                onClick={onSend} 
                disabled={!sendAmount || !activeMintUrl || isLoading}
                className="h-12 px-12 rounded-full"
                size="lg"
              >
                <Send className="h-5 w-5" />
              </Button>
            </div>
          </div>
        ) : (
          // Receive Mode: Token input
          <div className="space-y-8">
            <Input
              placeholder="cashuBo2Ft..."
              value={tokenInput}
              onChange={(e) => setTokenInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && tokenInput.trim() && activeMintUrl && !isLoading) {
                  onReceive();
                }
              }}
              disabled={!activeMintUrl}
              className="w-full h-16 !text-base text-center border bg-background focus:ring-2 focus:ring-ring focus:ring-offset-2 font-mono"
            />
            <div className="flex justify-center mt-6 mb-safe-bottom pb-6">
              <Button 
                onClick={onReceive} 
                disabled={!tokenInput.trim() || !activeMintUrl || isLoading}
                className="h-12 px-12 rounded-full"
                size="lg"
              >
                <Download className="h-5 w-5" />
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
- **Simple send flow**: Amount input → Generate token → Display QR code
- **Simple receive flow**: Token input → Redeem token
- **State cleanup**: Reset all form state when drawer/modal closes (see drawer implementation example above)
- **Input validation**: Disable buttons when required fields are missing
- **Keyboard support**: Enter key triggers actions
- **Mint requirement**: Show message when no mint is selected
- **Custom styling**: Adapt the design to match your application's design system
- **Alternative flows**: Experiment with single-step vs multi-step token flows
- **Error handling**: Display validation errors and token receive failures appropriately
- **Loading states**: Show loading indicators during token processing
- **Success feedback**: Display confirmation messages after successful token operations
- **Drawer implementation**: Use `Drawer` from shadcn/ui with proper state cleanup (see drawer implementation example above)

### Token QR Code Modal (Example)

**Example implementation for displaying Cashu token with QR code:**

This is an example implementation that can be customized or replaced based on your design needs. The token modal should display the Cashu token, QR code for easy scanning, and handle token sharing appropriately.

```typescript
// components/TokenModal.tsx (EXAMPLE - customize as needed)
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { QRModal } from '@/components/ui/qr-modal';

export function TokenModal({
  isOpen,
  onClose,
  token,
  amount,
  qrCodeUrl,
}: {
  isOpen: boolean;
  onClose: () => void;
  token: string;
  amount: number;
  qrCodeUrl: string;
}) {
  return (
    <QRModal
      isOpen={isOpen}
      onClose={onClose}
      title="Cashu Token"
      description={`Share this token to send ${amount.toLocaleString()} sats`}
      qrCodeUrl={qrCodeUrl}
      content={token}
      icon="qr"
    />
  );
}
```

**Example Token Display Patterns (experiment with these or create your own):**
- **QR code display**: Show QR code for easy scanning (using `qr-code-generator` skill)
- **Token text**: Display token string for manual entry or copying
- **Amount display**: Show token amount with optional fiat conversion (using `exchange-rates` skill)
- **Custom styling**: Adapt the modal design to match your application's design system
- **Copy functionality**: Add copy-to-clipboard for token string
- **Multiple sharing methods**: Provide QR code, copy, emoji encoding, and other sharing options
- **Display location**: Display tokens in modals, drawers, separate pages, or inline components

### Token Input Component (Example)

**Example input field for receiving tokens:**

This is an example implementation that can be customized or replaced based on your design needs. The token input should handle token entry, validation, and redemption flows.

```typescript
// components/TokenInput.tsx (EXAMPLE - customize as needed)
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';

export function TokenInput({
  tokenInput,
  setTokenInput,
  onReceive,
  isLoading,
  activeMintUrl,
}: {
  tokenInput: string;
  setTokenInput: (value: string) => void;
  onReceive: () => void;
  isLoading: boolean;
  activeMintUrl: string | null;
}) {
  return (
    <div className="space-y-2">
      <Textarea
        value={tokenInput}
        onChange={(e) => setTokenInput(e.target.value)}
        placeholder="Paste Cashu token here or scan QR code"
        rows={4}
        className="font-mono text-sm"
        disabled={!activeMintUrl}
      />
      <Button
        onClick={onReceive}
        disabled={!tokenInput.trim() || !activeMintUrl || isLoading}
        className="w-full"
      >
        {isLoading ? 'Receiving...' : 'Receive Token'}
      </Button>
    </div>
  );
}
```

**Example Token Input Patterns (experiment with these or create your own):**
- **Text input**: Single-line or multi-line input for token entry
- **Textarea**: Multi-line textarea for longer tokens or multiple tokens
- **Paste support**: Handle paste events for token input
- **Validation**: Show validation feedback for invalid token formats
- **Custom styling**: Adapt the input design to match your application's design system
- **Alternative layouts**: Experiment with different input field layouts and sizes
- **Error handling**: Display validation errors appropriately
- **Loading states**: Show loading indicators during token processing

### Balance Display (Example)

**Example implementation for displaying Cashu token wallet balance with exchange rate conversion:**

This is an example implementation that can be customized or replaced based on your design needs. The balance display should show the total balance across all mints, optionally with exchange rate conversion.

```typescript
// components/TokenBalanceDisplay.tsx (EXAMPLE - customize as needed)
import { useState, useEffect } from 'react';
import { getBtcUsdRate } from '@/lib/exchangeRateService';

interface TokenBalanceDisplayProps {
  totalBalance: number; // Total balance in sats across all mints
}

export function TokenBalanceDisplay({ totalBalance }: TokenBalanceDisplayProps) {
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
- **Aggregated balance**: Show total balance across all mints

## Part 7: Error Handling

### Unknown Mint Errors

**Handle unknown mints automatically:**

```typescript
import { isUnknownMintError, extractMintUrlFromError } from '@/hooks/wallet/useMintManager';
import { useToast } from '@/hooks/useToast';

// In your component or hook:
const { toast } = useToast();

try {
  await coco.wallet.receive(tokenInput);
} catch (err) {
  if (isUnknownMintError(err)) {
    const mintUrl = extractMintUrlFromError(err);
    if (mintUrl) {
      // Automatically add and trust the mint
      await handleUnknownMintError(mintUrl);
      return; // Successfully handled
    }
  }
  
  // Other errors
  // Default: Toast notification
  toast({ variant: 'destructive', title: 'Receive Failed', description: err instanceof Error ? err.message : 'Unknown error' });
  // Alternative options (commented):
  // Option 1: Console logging
  // console.error('Receive Failed:', err instanceof Error ? err.message : 'Unknown error');
  // Option 2: No notification (silent failure)
}
```

### Insufficient Balance Errors

**Handle insufficient balance when sending:**

```typescript
import { useToast } from '@/hooks/useToast';

// In your component or hook:
const { toast } = useToast();

try {
  const token = await coco.wallet.send(activeMintUrl, amount);
} catch (err) {
  const errorMessage = err instanceof Error ? err.message : '';
  
  if (errorMessage.includes('insufficient') || errorMessage.includes('balance')) {
    // Default: Toast notification
    toast({ variant: 'destructive', title: 'Insufficient Balance', description: `You don't have enough tokens. Current balance: ${balances[activeMintUrl] || 0} sats` });
    // Alternative options (commented):
    // Option 1: Console logging
    // console.error(`Insufficient Balance: You don't have enough tokens. Current balance: ${balances[activeMintUrl] || 0} sats`);
    // Option 2: No notification (silent failure)
  } else {
    // Default: Toast notification
    toast({ variant: 'destructive', title: 'Send Failed', description: errorMessage || 'Unknown error' });
    // Alternative options (commented):
    // Option 1: Console logging
    // console.error('Send Failed:', errorMessage || 'Unknown error');
    // Option 2: No notification (silent failure)
  }
}
```

### Token Validation Errors

**Handle invalid token formats:**

```typescript
import { useToast } from '@/hooks/useToast';

function handleTokenReceive() {
  const { toast } = useToast();
  
  if (!tokenInput.trim()) {
    // Default: Toast notification
    toast({ variant: 'destructive', title: 'No Token', description: 'Please paste or scan a Cashu token' });
    // Alternative options (commented):
    // Option 1: Console logging
    // console.error('No Token: Please paste or scan a Cashu token');
    // Option 2: No notification (silent failure)
    return;
  }
  
  if (!isValidCashuToken(tokenInput)) {
    // Default: Toast notification
    toast({ variant: 'destructive', title: 'Invalid Token', description: 'This does not appear to be a valid Cashu token format' });
    // Alternative options (commented):
    // Option 1: Console logging
    // console.error('Invalid Token: This does not appear to be a valid Cashu token format');
    // Option 2: No notification (silent failure)
    return;
  }
  
  // Proceed with receive
  handleTokenReceive();
}
```

## Part 8: Best Practices

### Automatic Mint Management

**Always handle unknown mints gracefully:**

```typescript
// Best practice: Automatically add and trust mints when receiving tokens
// User is explicitly accepting tokens from the mint
if (isUnknownMintError(err)) {
  const mintUrl = extractMintUrlFromError(err);
  if (mintUrl) {
    // Add mint automatically (user trusts the sender)
    await coco.mint.addMint(mintUrl, { trusted: true });
    // Retry receive
    await coco.wallet.receive(tokenInput);
  }
}
```

### Token Sharing UX

**Provide multiple sharing methods:**

```typescript
// 1. QR Code (primary method)
<QRModal qrCodeUrl={qrCodeUrl} content={encodedToken} />

// 2. Copy to clipboard
<Button onClick={() => copyToClipboard(encodedToken)}>
  Copy Token
</Button>

// 3. Emoji encoding (optional - using emoji-encoder skill)
import { encode } from '@/lib/emojiEncoder';
const emojiToken = encode('🥜', encodedToken);
<Button onClick={() => copyToClipboard(emojiToken)}>
  Copy as Emoji 🥜
</Button>

// 4. Share via other methods (NFC, etc.)
```

### Balance Updates

**Use event listeners for reactive balance updates:**

```typescript
// From lightning-wallet skill - balances update automatically
useEffect(() => {
  const coco = cocoRef.current;
  if (!coco) return;
  
  const refreshBalances = async () => {
    const newBalances = await coco.wallet.getBalances();
    setBalances(newBalances);
  };
  
  // Listen to token events
  const unsubs = [
    coco.on('proofs:saved', refreshBalances),
    coco.on('send:created', refreshBalances),
    coco.on('receive:created', refreshBalances),
  ];
  
  return () => unsubs.forEach(unsub => unsub());
}, [isInitialized]);
```

## Part 9: Common Pitfalls

### 1. ❌ Not handling unknown mints

**Problem:** Receiving tokens from unknown mints causes errors.

**Solution:** Automatically add and trust unknown mints:
```typescript
if (isUnknownMintError(err)) {
  const mintUrl = extractMintUrlFromError(err);
  if (mintUrl) {
    await coco.mint.addMint(mintUrl, { trusted: true });
    await coco.wallet.receive(tokenInput); // Retry
  }
}
```

### 2. ❌ Not validating token format

**Problem:** Invalid tokens cause confusing errors.

**Solution:** Validate token format before processing:
```typescript
import { useToast } from '@/hooks/useToast';

// In your component or hook:
const { toast } = useToast();

if (!isValidCashuToken(tokenInput)) {
  // Default: Toast notification
  toast({ variant: 'destructive', title: 'Invalid Token' });
  // Alternative options (commented):
  // Option 1: Console logging
  // console.error('Invalid Token');
  // Option 2: No notification (silent failure)
  return;
}
```

### 3. ❌ Not checking active mint

**Problem:** Sending tokens without active mint causes errors.

**Solution:** Always check for active mint:
```typescript
import { useToast } from '@/hooks/useToast';

// In your component or hook:
const { toast } = useToast();

if (!activeMintUrl || !coco) {
  // Default: Toast notification
  toast({ variant: 'destructive', title: 'No Mint Selected' });
  // Alternative options (commented):
  // Option 1: Console logging
  // console.error('No Mint Selected');
  // Option 2: No notification (silent failure)
  return;
}
```

### 4. ❌ Not encoding tokens for sharing

**Problem:** Raw token objects can't be shared easily.

**Solution:** Always encode tokens:
```typescript
const token = await coco.wallet.send(activeMintUrl, amount);
const encodedToken = getEncodedToken(token); // Encode for sharing
```

### 5. ❌ Not generating QR codes

**Problem:** Users can't easily share tokens.

**Solution:** **REQUIRED** - Always generate QR codes:
```typescript
const qrCodeUrl = await generateQRCode(encodedToken);
// Display in modal
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

1. **Mint Trust**: Automatically trusting mints when receiving tokens is acceptable (user explicitly accepts)
2. **Token Validation**: Always validate token format before processing
3. **Balance Verification**: Check balance before sending tokens
4. **Error Handling**: Don't expose internal errors to users
5. **Token Sharing**: Tokens are bearer assets - treat them like cash

## Verification Checklist

- [ ] **REQUIRED:** `lightning-wallet` skill implemented (wallet initialization, mint management, history)
- [ ] Token receive operations work correctly
- [ ] Token send operations work correctly
- [ ] Automatic mint management handles unknown mints
- [ ] **REQUIRED:** `qr-code-generator` skill implemented for token QR codes
- [ ] **REQUIRED:** `exchange-rates` skill implemented and working
- [ ] Token encoding/decoding works correctly
- [ ] Exchange rate display works (BTC/fiat conversions)
- [ ] QR code generation for tokens works
- [ ] Token validation handles invalid formats
- [ ] **OPTIONAL:** `emoji-encoder` skill implemented for emoji-based token sharing
- [ ] Error handling covers all failure cases
- [ ] Balance updates reactively via event listeners
- [ ] Integration with Lightning wallet works (shared functionality)

## Summary

To implement a Cashu token wallet:

1. **Install dependencies** - Add all required packages to `package.json`: `@cashu/cashu-ts@2.8.1`, `coco-cashu-core@1.1.2-rc.30`, `coco-cashu-indexeddb@1.1.2-rc.30`, `dexie@^4.0.8`, `@scure/bip39@1.6.0`, `@scure/bip32@^2.0.1` (if using BIP32), `@noble/hashes@^2.0.1`, `@noble/curves@^2.0.1`
2. **REQUIRED:** Implement `lightning-wallet` skill (wallet initialization, mint management, history)
3. **Token operations** - Send and receive Cashu tokens
4. **Automatic mint management** - Handle unknown mints automatically
5. **REQUIRED:** Implement `qr-code-generator` skill for token QR codes
6. **REQUIRED:** Implement `exchange-rates` skill for BTC/fiat conversions
7. **Token encoding** - Encode/decode tokens for sharing
8. **OPTIONAL:** Implement `emoji-encoder` skill for emoji-based token sharing
9. **Error handling** - Handle all failure cases gracefully
10. **Event listeners** - Use reactive updates for balance changes

**Key principle:** Cashu token wallets require Lightning functionality because users need to mint (receive Lightning) to get tokens and melt (send Lightning) to convert tokens back to Lightning.

**Note:** All required dependencies are listed in Prerequisites. If build fails, verify all packages are present with correct versions (especially `@cashu/cashu-ts@2.8.1` to prevent 3.0.2 resolution, `coco-cashu-core@1.1.2-rc.30` and `coco-cashu-indexeddb@1.1.2-rc.30` for the latest features, and `dexie@^4.0.8` for IndexedDB support).

