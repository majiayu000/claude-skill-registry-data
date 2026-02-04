---
name: bitcoin-wallet
description: Use when implementing Bitcoin wallet features - provides complete architecture for on-chain Bitcoin transactions, UTXO management, address derivation from Nostr keys, and transaction handling with proper security patterns
when_to_use: When building Bitcoin wallet functionality, adding on-chain transaction support, implementing UTXO management, or integrating Bitcoin with Nostr-based applications
---

# Implementing Bitcoin Wallet

## Overview

This skill guides you through implementing a complete Bitcoin wallet system with on-chain transaction support, UTXO management, and integration with Nostr key infrastructure.

**Core Capabilities:**
- Send/receive on-chain Bitcoin transactions
- UTXO management and consolidation
- Bitcoin address derivation from Nostr public keys
- Transaction history tracking
- QR code support for addresses
- Fee estimation and transaction building

**Key Architecture Pattern:** The wallet derives Bitcoin addresses from Nostr public keys, enabling users to access Bitcoin using their Nostr identity without managing separate keys.

## Prerequisites

Before implementing a Bitcoin wallet, ensure:

1. **User authentication exists** - Requires user pubkey and private key access
2. **IMPORTANT:** Before adding dependencies, review your project's `package.json` to check if any of these packages already exist. If they do, verify the versions are compatible with the requirements below. Only add packages that are missing or need version updates.
3. **Required packages installed**:
   ```json
   {
     "bitcoinjs-lib": "^7.0.0",
     "@bitcoinerlab/secp256k1": "^1.2.0",
     "ecpair": "^3.0.0"
   }
   ```
3. **QR Code functionality** - **REQUIRED:** For displaying Bitcoin addresses as QR codes, use the `qr-code-generator` skill. **OPTIONAL:** For scanning recipient addresses, use the `qr-code-scanner` skill. These skills provide QR code generation, camera-based scanning, and content classification for Bitcoin addresses, Lightning invoices, and other formats.
4. **Exchange Rate functionality** - For displaying USD equivalents and converting between BTC/sats and fiat currencies, use the `exchange-rates` skill. This skill provides Coinbase API integration, caching strategies, and React hooks for displaying exchange rates in wallet UIs.

## Implementation Checklist

Create TodoWrite todos for each section:

- [ ] Initialize ECC library (`bitcoin.initEccLib(ecc)`) at module load
- [ ] Set up Bitcoin utility library
- [ ] Implement address derivation from Nostr keys
- [ ] Create UTXO fetching and management
- [ ] Build transaction creation and signing
- [ ] Implement balance tracking hooks
- [ ] Create transaction history hooks
- [ ] Build wallet UI components
- [ ] Add copy to clipboard functionality for addresses
- [ ] Add UTXO consolidation feature
- [ ] **REQUIRED:** Implement QR code generation for addresses (use `qr-code-generator` skill)
- [ ] **OPTIONAL:** Implement QR code scanning for recipient addresses (use `qr-code-scanner` skill)
- [ ] Add exchange rate display (use `exchange-rates` skill)
- [ ] Add comprehensive error handling

## Part 1: Core Bitcoin Utilities

**CRITICAL: ECC Library Initialization**

bitcoinjs-lib v7+ requires explicit ECC library initialization before any operations. Initialize once at the top of your bitcoin utilities file:

```typescript
// lib/bitcoin.ts
import * as bitcoin from 'bitcoinjs-lib';
import * as ecc from '@bitcoinerlab/secp256k1';

// Initialize ECC library - MUST be called before any bitcoinjs-lib operations
bitcoin.initEccLib(ecc);

// Now you can use bitcoinjs-lib functions
```

**Common Error:** Missing this causes "No ECC Library provided" errors. Initialize at module load time, not inside functions.

### Address Derivation from Nostr Keys

**Key Pattern:** Use Taproot (P2TR) addresses derived from Nostr public keys.

**CRITICAL: Key Format Differences**

- **Nostr pubkeys**: Always 32 bytes (64 hex chars), no prefix
- **Bitcoin compressed pubkeys**: 33 bytes with 02/03 prefix (66 hex chars)
- **For Taproot**: Always use 32-byte internal pubkey directly

```typescript
// lib/bitcoin.ts
import * as bitcoin from 'bitcoinjs-lib';
import * as ecc from '@bitcoinerlab/secp256k1';
import { nip19 } from 'nostr-tools';

// Initialize ECC library - MUST be called before any bitcoinjs-lib operations
bitcoin.initEccLib(ecc);

/**
 * Validate and normalize Nostr public key
 * Handles 0x prefix, validates length and format
 */
function validateAndConvertKey(pubkeyHex: string): Buffer {
  if (!pubkeyHex || typeof pubkeyHex !== 'string') {
    throw new Error('Invalid input: pubkey must be a non-empty string');
  }
  
  // Remove 0x prefix if present
  let cleanHex = pubkeyHex.trim();
  if (cleanHex.startsWith('0x')) {
    cleanHex = cleanHex.slice(2);
  }
  
  // Validate length (Nostr keys are always 64 hex chars = 32 bytes)
  if (cleanHex.length !== 64) {
    throw new Error(`Invalid pubkey length: expected 64 hex chars, got ${cleanHex.length}`);
  }
  
  // Validate hex format
  if (!/^[0-9a-fA-F]{64}$/.test(cleanHex)) {
    throw new Error('Invalid hex characters in pubkey');
  }
  
  // Convert to buffer
  const buffer = Buffer.from(cleanHex, 'hex');
  if (buffer.length !== 32) {
    throw new Error(`Buffer conversion failed: expected 32 bytes, got ${buffer.length}`);
  }
  
  return buffer;
}

/**
 * Convert Nostr public key (hex) to Bitcoin Taproot address
 * CRITICAL: Nostr keys are 32 bytes - use directly, don't remove bytes
 */
export function nostrPubkeyToBitcoinAddress(pubkeyHex: string): string {
  const pubkeyBuffer = validateAndConvertKey(pubkeyHex);
  
  const { address } = bitcoin.payments.p2tr({
    internalPubkey: pubkeyBuffer, // Use full 32-byte key directly
    network: bitcoin.networks.bitcoin,
  });
  
  if (!address) {
    throw new Error('Failed to generate Bitcoin address');
  }
  
  return address;
}

/**
 * Convert npub to Bitcoin address
 */
export function npubToBitcoinAddress(npub: string): string {
  const decoded = nip19.decode(npub);
  if (decoded.type !== 'npub') {
    throw new Error('Invalid npub format');
  }
  
  // npub.data is Uint8Array, convert to hex string
  const pubkeyHex = Buffer.from(decoded.data as Uint8Array).toString('hex');
  return nostrPubkeyToBitcoinAddress(pubkeyHex);
}

/**
 * Validate Bitcoin address format
 */
export function isValidBitcoinAddress(address: string): boolean {
  try {
    bitcoin.address.toOutputScript(address, bitcoin.networks.bitcoin);
    return true;
  } catch {
    return false;
  }
}
```

**Why Taproot?**
- Modern address format (bc1p...)
- Better privacy through key-path spending
- Lower transaction fees
- Future-proof for advanced features

### UTXO Management

**UTXO (Unspent Transaction Output)** represents spendable Bitcoin.

```typescript
// lib/bitcoin.ts
export interface UTXO {
  txid: string;
  vout: number;
  value: number; // in satoshis
  status: {
    confirmed: boolean;
    block_height?: number;
  };
}

/**
 * Fetch UTXOs from Blockstream API
 */
export async function fetchUTXOs(address: string): Promise<UTXO[]> {
  const response = await fetch(
    `https://blockstream.info/api/address/${address}/utxo`
  );
  
  if (!response.ok) {
    throw new Error('Failed to fetch UTXOs');
  }
  
  return await response.json();
}

/**
 * Calculate total spendable balance from UTXOs
 */
export function calculateBalance(utxos: UTXO[]): number {
  return utxos.reduce((sum, utxo) => sum + utxo.value, 0);
}

/**
 * Calculate maximum sendable amount (balance minus estimated fee)
 */
export function calculateMaxSendAmount(
  utxos: UTXO[],
  feeRate: number
): number {
  if (utxos.length === 0) {
    return 0;
  }
  
  const totalBalance = calculateBalance(utxos);
  
  // Estimate transaction size for Send Max (single output, no change)
  // P2TR input: ~57.5 vBytes, P2TR output: ~43 vBytes
  const estimatedSize = utxos.length * 57.5 + 43 + 10.5;
  const estimatedFee = Math.ceil(estimatedSize * feeRate);
  
  const maxAmount = totalBalance - estimatedFee;
  return Math.max(0, maxAmount);
}
```

### Fee Estimation

```typescript
// lib/bitcoin.ts
export interface FeeRates {
  fastestFee: number;
  halfHourFee: number;
  hourFee: number;
  economyFee: number;
  minimumFee: number;
}

/**
 * Fetch current fee rates from Blockstream API
 */
export async function getFeeRates(): Promise<FeeRates> {
  const response = await fetch(
    'https://blockstream.info/api/fee-estimates'
  );
  
  if (!response.ok) {
    throw new Error('Failed to fetch fee estimates');
  }
  
  const data = await response.json();
  
  return {
    fastestFee: Math.ceil(data['1'] || 1),
    halfHourFee: Math.ceil(data['3'] || 1),
    hourFee: Math.ceil(data['6'] || 1),
    economyFee: Math.ceil(data['144'] || 1),
    minimumFee: Math.ceil(data['504'] || 1),
  };
}
```

### Transaction Building and Signing

**Critical Security:** Never expose or log private keys.

```typescript
// lib/bitcoin.ts
import * as bitcoin from 'bitcoinjs-lib';
import * as ecc from '@bitcoinerlab/secp256k1';
import { ECPairFactory, type ECPairAPI } from 'ecpair';

// Initialize ECC library - MUST be called before any bitcoinjs-lib operations
bitcoin.initEccLib(ecc);

// Lazy initialization for ECPair (avoids issues in test environments)
let ECPair: ECPairAPI | null = null;
function getECPair(): ECPairAPI {
  if (!ECPair) {
    ECPair = ECPairFactory(ecc);
  }
  return ECPair;
}

/**
 * Create and sign a Bitcoin transaction
 * @param privateKeyHex - Private key in hex format (from nsec)
 * @param recipientAddress - Recipient Bitcoin address
 * @param amountSats - Amount to send in satoshis
 * @param utxos - Available UTXOs to spend
 * @param feeRate - Fee rate in sat/vB
 * @param sendMax - If true, send all available funds
 */
export async function createBitcoinTransaction(
  privateKeyHex: string,
  recipientAddress: string,
  amountSats: number,
  utxos: UTXO[],
  feeRate: number,
  sendMax: boolean = false
): Promise<{ txHex: string; fee: number }> {
  const privateKeyBuffer = Buffer.from(privateKeyHex, 'hex');
  const keyPair = getECPair().fromPrivateKey(privateKeyBuffer);
  
  // Get x-only public key (32 bytes) for Taproot
  // Remove the first byte (compression flag) from the 33-byte compressed pubkey
  const internalPubkey = keyPair.publicKey.slice(1, 33);
  
  // Get sender's address for change output
  const { address: changeAddress } = bitcoin.payments.p2tr({
    internalPubkey,
    network: bitcoin.networks.bitcoin,
  });
  
  if (!changeAddress) {
    throw new Error('Failed to generate change address');
  }
  
  // Create transaction builder
  const psbt = new bitcoin.Psbt({ network: bitcoin.networks.bitcoin });
  
  // Add inputs (UTXOs)
  let totalInput = 0;
  for (const utxo of utxos) {
    psbt.addInput({
      hash: utxo.txid,
      index: utxo.vout,
      witnessUtxo: {
        script: bitcoin.payments.p2tr({
          internalPubkey,
          network: bitcoin.networks.bitcoin,
        }).output!,
        value: BigInt(utxo.value),
      },
      tapInternalKey: internalPubkey,
    });
    
    totalInput += utxo.value;
  }
  
  // Estimate transaction size
  // P2TR input: ~57.5 vBytes, P2TR output: ~43 vBytes
  const outputCount = sendMax ? 1 : 2; // Send Max = 1 output, Regular = 2 outputs
  const estimatedSize = utxos.length * 57.5 + outputCount * 43 + 10.5;
  const estimatedFee = Math.ceil(estimatedSize * feeRate);
  
  if (sendMax) {
    // Send Max: send all UTXOs to recipient, no change
    const maxAmount = totalInput - estimatedFee;
    
    if (maxAmount <= 0) {
      throw new Error(
        `Insufficient funds for Send Max. Total: ${totalInput} sats, Fee: ${estimatedFee} sats`
      );
    }
    
    psbt.addOutput({
      address: recipientAddress,
      value: BigInt(maxAmount),
    });
  } else {
    // Regular transaction: calculate change
    const change = totalInput - amountSats - estimatedFee;
    
    if (change < 0) {
      throw new Error(
        `Insufficient funds. Need ${amountSats + estimatedFee} sats, have ${totalInput} sats`
      );
    }
    
    // Add output for recipient
    psbt.addOutput({
      address: recipientAddress,
      value: BigInt(amountSats),
    });
    
    // Add change output if significant (> dust limit)
    const dustLimit = 546; // Standard dust limit for Bitcoin
    if (change > dustLimit) {
      psbt.addOutput({
        address: changeAddress,
        value: BigInt(change),
      });
    }
  }
  
  // Create a Taproot signer (tweaked for key-path spending)
  const tweakedSigner = keyPair.tweak(
    bitcoin.crypto.taggedHash('TapTweak', internalPubkey)
  );
  
  // Sign all inputs
  for (let i = 0; i < utxos.length; i++) {
    psbt.signInput(i, tweakedSigner);
  }
  
  // Finalize and extract transaction
  psbt.finalizeAllInputs();
  const tx = psbt.extractTransaction();
  
  return {
    txHex: tx.toHex(),
    fee: estimatedFee,
  };
}

/**
 * Broadcast transaction to network
 */
export async function broadcastTransaction(txHex: string): Promise<string> {
  const response = await fetch('https://blockstream.info/api/tx', {
    method: 'POST',
    body: txHex,
  });
  
  if (!response.ok) {
    throw new Error('Failed to broadcast transaction');
  }
  
  return await response.text(); // Returns txid
}
```

## Part 2: React Hooks

### Private Key Access Hook

**Critical:** Only works with nsec login (not browser extensions or bunkers). 

```typescript
// hooks/useNsecAccess.ts
import { useNostrLogin } from '@nostrify/react/login';
import { nip19 } from 'nostr-tools';

/**
 * Hook to check if user logged in with nsec and get private key
 * SECURITY: Private key never leaves this hook except when explicitly requested
 */
export function useNsecAccess() {
  const { logins } = useNostrLogin();
  const currentLogin = logins[0];
  
  // Check if user logged in with nsec
  const hasNsecAccess = currentLogin?.type === 'nsec';
  
  // Get private key in hex format
  const getPrivateKey = (): string | null => {
    if (!hasNsecAccess || !currentLogin) return null;
    
    try {
      const loginData = currentLogin as { data?: { nsec: string } };
      const nsec = loginData.data?.nsec;
      
      if (!nsec) return null;
      
      const decoded = nip19.decode(nsec);
      if (decoded.type !== 'nsec') return null;
      
      return Buffer.from(decoded.data as Uint8Array).toString('hex');
    } catch (error) {
      console.error('Failed to decode nsec:', error);
      return null;
    }
  };
  
  return {
    hasNsecAccess,
    getPrivateKey,
    loginType: currentLogin?.type,
  };
}
```

### Balance Hook

```typescript
// hooks/wallet/useBitcoin.ts
import { useQuery } from '@tanstack/react-query';

export function useBitcoinBalance(address: string | null) {
  return useQuery({
    queryKey: ['bitcoin-balance', address],
    queryFn: async (): Promise<{ balance: number; utxos: UTXO[] }> => {
      if (!address) {
        return { balance: 0, utxos: [] };
      }
      
      const utxos = await fetchUTXOs(address);
      const balance = utxos.reduce((sum, utxo) => sum + utxo.value, 0);
      
      return { balance, utxos };
    },
    enabled: !!address,
    refetchInterval: 30000, // Refetch every 30 seconds
    staleTime: 10000, // Consider stale after 10 seconds
  });
}
```

### Transaction History Hook

```typescript
// hooks/wallet/useBitcoin.ts
export interface BitcoinTransaction {
  id: string;
  txid: string;
  type: 'sent' | 'received' | 'consolidate';
  amount: number; // satoshis
  fee?: number; // satoshis
  address: string;
  confirmations: number;
  blockHeight?: number;
  timestamp: number;
  status: 'confirmed' | 'unconfirmed' | 'pending';
}

export function useBitcoinTransactionHistory(address: string | null) {
  return useQuery({
    queryKey: ['bitcoin-transactions', address],
    queryFn: async (): Promise<BitcoinTransaction[]> => {
      if (!address) return [];
      
      // Fetch from Blockstream API
      const response = await fetch(
        `https://blockstream.info/api/address/${address}/txs`
      );
      
      if (!response.ok) {
        throw new Error('Failed to fetch transactions');
      }
      
      const txList = await response.json();
      
      // Transform to BitcoinTransaction format
      return txList.map((tx: any) => {
        // Determine if sent or received
        const isReceived = tx.vout.some(
          (output: any) => output.scriptpubkey_address === address
        );
        
        const isSent = tx.vin.some(
          (input: any) => input.prevout?.scriptpubkey_address === address
        );
        
        // Calculate amount for this address
        let amount = 0;
        let type: 'sent' | 'received' | 'consolidate';
        
        if (isReceived && !isSent) {
          type = 'received';
          amount = tx.vout
            .filter((output: any) => output.scriptpubkey_address === address)
            .reduce((sum: number, output: any) => sum + output.value, 0);
        } else if (isSent) {
          const inputsFromAddress = tx.vin
            .filter((input: any) => input.prevout?.scriptpubkey_address === address)
            .reduce((sum: number, input: any) => sum + (input.prevout?.value || 0), 0);
          
          const outputsToAddress = tx.vout
            .filter((output: any) => output.scriptpubkey_address === address)
            .reduce((sum: number, output: any) => sum + output.value, 0);
          
          const amountSentToOthers = inputsFromAddress - outputsToAddress - (tx.fee || 0);
          
          // Check if consolidation (self-send)
          if (amountSentToOthers <= 546 && outputsToAddress > 0) {
            type = 'consolidate';
            amount = outputsToAddress;
          } else {
            type = 'sent';
            amount = amountSentToOthers;
          }
        } else {
          type = 'received';
          amount = 0;
        }
        
        return {
          id: `${tx.txid}-${tx.vout}`,
          txid: tx.txid,
          type,
          amount: Math.abs(amount),
          fee: tx.fee,
          address,
          confirmations: tx.status.confirmed ? 1 : 0,
          blockHeight: tx.status.block_height,
          timestamp: (tx.status.block_time || 0) * 1000,
          status: tx.status.confirmed ? 'confirmed' : 'unconfirmed',
        } as BitcoinTransaction;
      });
    },
    enabled: !!address,
    refetchInterval: 30000,
    staleTime: 10000,
  });
}
```

### Operations Hook

```typescript
// hooks/wallet/useBitcoin.ts
import { useToast } from '@/hooks/useToast';

export function useBitcoinOperations(bitcoinAddress: string | null) {
  // Default: Toast notifications
  const { toast } = useToast();
  // Alternative options (commented):
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: No notification handler
  const { hasNsecAccess, getPrivateKey } = useNsecAccess();
  const { data: bitcoinBalanceData, refetch: refetchBalance } = useBitcoinBalance(bitcoinAddress);
  
  const utxos = bitcoinBalanceData?.utxos || [];
  const [feeRate, setFeeRate] = useState<number>(1);
  const [isConsolidating, setIsConsolidating] = useState(false);
  
  // Fetch fee rates on mount
  useEffect(() => {
    getFeeRates()
      .then(rates => setFeeRate(rates.fastestFee))
      .catch(() => {
        // Fallback to 1 sat/vB
      });
  }, []);
  
  const bitcoinMaxAmount = utxos.length > 0 
    ? calculateMaxSendAmount(utxos, feeRate) 
    : 0;
  
  // Send Bitcoin transaction
  const handleBitcoinSend = async (
    amount: string,
    recipientAddress: string,
    onSuccess: () => void
  ) => {
    if (!hasNsecAccess || !bitcoinAddress) {
      // Default: Toast notification
      toast({ variant: "destructive", title: "Error", description: "Nsec login required for Bitcoin transactions" });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Error: Nsec login required for Bitcoin transactions');
      // Option 2: No notification (silent failure)
      return;
    }
    
    try {
      const privateKey = getPrivateKey();
      if (!privateKey) {
        throw new Error('Unable to access private key');
      }
      
      const amountSats = parseInt(amount);
      if (isNaN(amountSats) || amountSats <= 0) {
        throw new Error('Invalid amount');
      }
      
      // Fetch fresh UTXOs and fee rates
      const [utxos, feeRates] = await Promise.all([
        fetchUTXOs(bitcoinAddress),
        getFeeRates(),
      ]);
      
      const isSendMax = amountSats === bitcoinMaxAmount;
      
      // Create and sign transaction
      const { txHex, fee } = await createBitcoinTransaction(
        privateKey,
        recipientAddress,
        amountSats,
        utxos,
        feeRates.fastestFee,
        isSendMax
      );
      
      // Broadcast
      const txId = await broadcastTransaction(txHex);
      
      // Default: Toast notification
      toast({ title: "Bitcoin Sent!", description: `Transaction ${txId.slice(0, 8)}... (Fee: ${fee} sats)` });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.log(`Bitcoin Sent! Transaction ${txId.slice(0, 8)}... (Fee: ${fee} sats)`);
      // Option 2: No notification (silent success)
      
      refetchBalance();
      onSuccess();
      
    } catch (error) {
      // Default: Toast notification
      toast({ variant: "destructive", title: "Send Failed", description: error instanceof Error ? error.message : 'Unknown error' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Send Failed:', error instanceof Error ? error.message : 'Unknown error');
      // Option 2: No notification (silent failure)
    }
  };
  
  // Consolidate UTXOs (combine multiple UTXOs into one)
  const handleConsolidateUtxos = async () => {
    if (!hasNsecAccess || !bitcoinAddress || utxos.length <= 1) {
      // Default: Toast notification
      toast({ variant: "destructive", title: "Error", description: "Cannot consolidate UTXOs" });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Error: Cannot consolidate UTXOs');
      // Option 2: No notification (silent failure)
      return;
    }
    
    setIsConsolidating(true);
    try {
      const privateKey = getPrivateKey();
      if (!privateKey) {
        throw new Error('Unable to access private key');
      }
      
      const consolidationAmount = calculateMaxSendAmount(utxos, feeRate);
      if (consolidationAmount <= 0) {
        throw new Error('Insufficient funds for consolidation');
      }
      
      // Self-send with all UTXOs
      const { txHex, fee } = await createBitcoinTransaction(
        privateKey,
        bitcoinAddress, // Send to self
        consolidationAmount,
        utxos,
        feeRate,
        true // sendMax = true
      );
      
      const txId = await broadcastTransaction(txHex);
      
      // Default: Toast notification
      toast({ title: "UTXOs Consolidated!", description: `Transaction ${txId.slice(0, 8)}... (Fee: ${fee} sats)` });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.log(`UTXOs Consolidated! Transaction ${txId.slice(0, 8)}... (Fee: ${fee} sats)`);
      // Option 2: No notification (silent success)
      
      refetchBalance();
      
    } catch (error) {
      // Default: Toast notification
      toast({ variant: "destructive", title: "Consolidation Failed", description: error instanceof Error ? error.message : 'Unknown error' });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Consolidation Failed:', error instanceof Error ? error.message : 'Unknown error');
      // Option 2: No notification (silent failure)
    } finally {
      setIsConsolidating(false);
    }
  };
  
  return {
    utxos,
    feeRate,
    isConsolidating,
    bitcoinMaxAmount,
    handleBitcoinSend,
    handleConsolidateUtxos,
  };
}
```

## Part 3: UI Components

### Copy to Clipboard Hook

**Essential for Bitcoin wallets:** Users need to copy Bitcoin addresses easily. This hook provides clipboard functionality with visual feedback.

```typescript
// hooks/useCopyToClipboard.ts
import { useState, useCallback } from 'react';
// optional import { useToast } from '@/hooks/useToast';

interface UseCopyToClipboardReturn {
  copy: (text: string) => Promise<void>;
  copied: boolean;
  copyError: string | null;
}

/**
 * Hook for copying text to clipboard with feedback
 * 
 * @example
 * ```tsx
 * const { copy, copied, copyError } = useCopyToClipboard();
 * 
 * await copy('bc1p...');
 * // copied will be true for 2 seconds
 * ```
 */
export function useCopyToClipboard(): UseCopyToClipboardReturn {
  const [copied, setCopied] = useState(false);
  const [copyError, setCopyError] = useState<string | null>(null);
  // Optional: User feedback notifications
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: Toast notifications (if useToast hook is available)
  // const { toast } = useToast();
  // Option 3: No notification handler

  const copy = useCallback(async (text: string): Promise<void> => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setCopyError(null);
      
      // Auto-reset copied state after 2 seconds
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      const errorMessage = 'Failed to copy to clipboard';
      console.error(errorMessage, err);
      setCopyError(errorMessage);
      
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.error('Failed to copy to clipboard:', err);
      // Option 2: Toast notification (if toast is available)
      // toast({ variant: "destructive", title: "Copy Failed", description: errorMessage });
      // Option 3: No notification (silent failure)
    }
  }, []);

  return {
    copy,
    copied,
    copyError,
  };
}
```

**Usage in wallet components:**
```typescript
// components/wallet/BitcoinWallet.tsx
import { useCopyToClipboard } from '@/hooks/useCopyToClipboard';
import { Button } from '@/components/ui/button';
import { Copy, Check } from 'lucide-react';

function BitcoinAddressDisplay({ address }: { address: string }) {
  const { copy, copied } = useCopyToClipboard();

  return (
    <div className="flex items-center gap-2">
      <code className="text-sm font-mono">{address}</code>
      <Button
        variant="ghost"
        size="icon"
        onClick={() => copy(address)}
        className="h-8 w-8"
      >
        {copied ? (
          <Check className="h-4 w-4 text-green-600" />
        ) : (
          <Copy className="h-4 w-4" />
        )}
      </Button>
    </div>
  );
}
```

**Key Features:**
- **Visual feedback** - Shows checkmark when copied
- **Auto-reset** - Returns to copy icon after 2 seconds
- **Error handling** - Optional user feedback (console.log, toast notifications, or silent)
- **Accessible** - Works with screen readers

### Main Wallet Component Structure

```typescript
// components/wallet/BitcoinWallet.tsx
import { BitcoinAddressDisplay } from './BitcoinAddressDisplay';
import { useSatsToUsd } from '@/hooks/useExchangeRate';

export function BitcoinWallet() {
  const { user } = useCurrentUser();
  const { hasNsecAccess } = useNsecAccess();
  // Optional: User feedback notifications
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: Toast notifications (if useToast hook is available)
  // const { toast } = useToast();
  // Option 3: No notification handler
  
  const bitcoinAddress = user?.pubkey 
    ? nostrPubkeyToBitcoinAddress(user.pubkey) 
    : null;
  
  const { data: balanceData } = useBitcoinBalance(bitcoinAddress);
  const { data: transactions } = useBitcoinTransactionHistory(bitcoinAddress);
  const {
    utxos,
    bitcoinMaxAmount,
    handleBitcoinSend,
    handleConsolidateUtxos,
  } = useBitcoinOperations(bitcoinAddress);
  
  // State
  const [amount, setAmount] = useState('');
  const [recipient, setRecipient] = useState('');
  const [showSendModal, setShowSendModal] = useState(false);
  
  // Exchange rate for USD display
  const balanceSats = balanceData?.balance || 0;
  const usdValue = useSatsToUsd(balanceSats);
  
  if (!hasNsecAccess) {
    return (
      <div className="p-4">
        <p>Bitcoin wallet requires nsec login</p>
      </div>
    );
  }
  
  return (
    <div className="space-y-4">
      {/* Balance Display with USD equivalent */}
      <div className="p-4 border rounded-lg">
        <h2 className="text-2xl font-bold">
          {balanceSats.toLocaleString()} sats
        </h2>
        {usdValue !== null && (
          <p className="text-sm text-muted-foreground">
            ≈ ${usdValue.toLocaleString('en-US', {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </p>
        )}
        {bitcoinAddress && (
          <BitcoinAddressDisplay address={bitcoinAddress} />
        )}
      </div>
      
      {/* Action Buttons */}
      <div className="flex gap-2">
        <Button onClick={() => setShowSendModal(true)}>
          Send
        </Button>
        <Button onClick={handleConsolidateUtxos}>
          Consolidate UTXOs
        </Button>
      </div>
      
      {/* Transaction History */}
      <div className="space-y-2">
        {transactions?.map((tx) => (
          <div key={tx.id} className="p-2 border rounded">
            <p>{tx.type}: {tx.amount} sats</p>
            <p className="text-sm text-muted-foreground">
              {tx.status}
            </p>
          </div>
        ))}
      </div>
      
      {/* Send Modal */}
      {showSendModal && (
        <SendModal
          amount={amount}
          setAmount={setAmount}
          recipient={recipient}
          setRecipient={setRecipient}
          maxAmount={bitcoinMaxAmount}
          onSend={() => {
            handleBitcoinSend(amount, recipient, () => {
              setShowSendModal(false);
              setAmount('');
              setRecipient('');
            });
          }}
          onClose={() => setShowSendModal(false)}
        />
      )}
    </div>
  );
}
```

### QR Code Integration

**REQUIRED:** Use the `qr-code-generator` skill for displaying Bitcoin addresses as QR codes. **OPTIONAL:** Use the `qr-code-scanner` skill for scanning recipient addresses.

**Displaying Bitcoin Address as QR Code:**

```typescript
// components/wallet/BitcoinWallet.tsx
import { useQRCodeGenerator } from '@/hooks/useQRCodeGenerator';
import { QRModal } from '@/components/QRModal';

function BitcoinWallet() {
  const { generateQRCode } = useQRCodeGenerator();
  const [showQRModal, setShowQRModal] = useState(false);
  
  // Generate QR code for Bitcoin address
  const handleShowQR = async () => {
    if (bitcoinAddress) {
      const qrDataUrl = await generateQRCode(bitcoinAddress);
      setShowQRModal(true);
    }
  };
  
  return (
    <>
      <Button onClick={handleShowQR}>Show QR Code</Button>
      {showQRModal && bitcoinAddress && (
        <QRModal
          isOpen={showQRModal}
          onClose={() => setShowQRModal(false)}
          qrDataUrl={await generateQRCode(bitcoinAddress)}
          address={bitcoinAddress}
        />
      )}
    </>
  );
}
```

**Scanning Recipient Address:**

```typescript
// components/wallet/SendModal.tsx
import { QRScanner } from '@/components/QRScanner';
import { useQRCodeScanner } from '@/hooks/useQRCodeScanner';
import { useToast } from '@/hooks/useToast';

function SendModal({ onSend, onClose }: SendModalProps) {
  const { toast } = useToast();
  const { classifyQRCode, startScanning, stopScanning, error: qrError } = useQRCodeScanner();
  const [showScanner, setShowScanner] = useState(false);
  const [recipient, setRecipient] = useState('');
  
  const handleQRResult = (result: QRScanResult) => {
    if (result.type === 'bitcoin_address') {
      setRecipient(result.value);
      setShowScanner(false);
    } else {
      // Default: Toast notification
      toast({ variant: "destructive", title: "Invalid QR Code", description: "Please scan a Bitcoin address" });
      // Alternative options (commented):
      // Option 1: Console logging
      // console.error('Invalid QR Code: Please scan a Bitcoin address');
      // Option 2: No notification (silent failure)
    }
  };
  
  return (
    <>
      <Button onClick={() => setShowScanner(true)}>Scan QR Code</Button>
      {showScanner && (
        <QRScanner
          isOpen={showScanner}
          onClose={async () => {
            await stopScanning();
            setShowScanner(false);
          }}
          onResult={handleQRResult}
          classifyQRCode={classifyQRCode}
          startScanning={startScanning}
          stopScanning={stopScanning}
          qrError={qrError}
        />
      )}
    </>
  );
}
```

**Key Integration Points:**
- **QR Generation (REQUIRED)** - Use `generateQRCode()` from `qr-code-generator` skill to create QR codes for Bitcoin addresses
- **QR Scanning (OPTIONAL)** - Use `QRScanner` component from `qr-code-scanner` skill to scan recipient addresses
- **Content Classification** - The `qr-code-scanner` skill automatically classifies Bitcoin addresses, Lightning invoices, and other formats
- **Error Handling** - Both generation and scanning include proper error handling

**See the `qr-code-generator` skill (required) and `qr-code-scanner` skill (optional) for complete implementation details.**

### Exchange Rate Integration

**Use the `exchange-rates` skill** for displaying USD equivalents and converting between BTC/sats and fiat currencies.

**Displaying Balance with USD Equivalent:**

```typescript
// components/wallet/BitcoinWallet.tsx
import { useSatsToUsd } from '@/hooks/useExchangeRate';
import { BalanceDisplay } from '@/components/wallet/BalanceDisplay';

function BitcoinWallet() {
  const { data: balanceData } = useBitcoinBalance(bitcoinAddress);
  const balanceSats = balanceData?.balance || 0;
  
  return (
    <div className="space-y-4">
      {/* Balance Display with USD equivalent */}
      <BalanceDisplay sats={balanceSats} />
      
      {/* Or inline display */}
      <div className="p-4 border rounded-lg">
        <h2 className="text-2xl font-bold">
          {balanceSats.toLocaleString()} sats
        </h2>
        <UsdEquivalent sats={balanceSats} />
      </div>
    </div>
  );
}

// Helper component for USD equivalent
function UsdEquivalent({ sats }: { sats: number }) {
  const usdValue = useSatsToUsd(sats);
  
  if (usdValue === null) {
    return (
      <p className="text-sm text-muted-foreground">
        Loading exchange rate...
      </p>
    );
  }
  
  return (
    <p className="text-sm text-muted-foreground">
      ≈ ${usdValue.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}
    </p>
  );
}
```

**Displaying Exchange Rate:**

```typescript
// components/wallet/BitcoinWallet.tsx
import { ExchangeRateDisplay } from '@/components/ExchangeRateDisplay';

function BitcoinWallet() {
  return (
    <div className="space-y-4">
      {/* Show current BTC/USD rate */}
      <ExchangeRateDisplay />
      
      {/* Rest of wallet UI */}
    </div>
  );
}
```

**Converting Transaction Amounts:**

```typescript
// components/wallet/TransactionHistory.tsx
import { useSatsToUsd } from '@/hooks/useExchangeRate';

function TransactionItem({ transaction }: { transaction: BitcoinTransaction }) {
  const usdValue = useSatsToUsd(transaction.amount);
  
  return (
    <div className="flex justify-between items-center">
      <div>
        <p>{transaction.type}: {transaction.amount.toLocaleString()} sats</p>
        {usdValue !== null && (
          <p className="text-sm text-muted-foreground">
            ≈ ${usdValue.toLocaleString('en-US', {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </p>
        )}
      </div>
      <span className="text-sm">{transaction.status}</span>
    </div>
  );
}
```

**Key Integration Points:**
- **USD Equivalents** - Use `useSatsToUsd()` hook to display USD values alongside satoshi amounts
- **Exchange Rate Display** - Use `ExchangeRateDisplay` component to show current BTC/USD rate
- **Automatic Caching** - The `exchange-rates` skill handles caching automatically
- **Error Handling** - Exchange rate hooks handle API failures gracefully with fallbacks

**See the `exchange-rates` skill for complete implementation details.**

## Part 4: Testing Strategy

**Follow TDD principles:** Write tests before implementation.

### Unit Tests

```typescript
// lib/bitcoin.test.ts
describe('Bitcoin Utilities', () => {
  describe('nostrPubkeyToBitcoinAddress', () => {
    test('converts valid 32-byte Nostr pubkey to Taproot address', () => {
      const pubkey = 'a'.repeat(64); // Valid 64-char hex = 32 bytes
      const address = nostrPubkeyToBitcoinAddress(pubkey);
      
      expect(address).toMatch(/^bc1p/);
      expect(address.length).toBeGreaterThan(50);
    });
    
    test('handles 0x prefix correctly', () => {
      const pubkey = '0x' + 'a'.repeat(64);
      expect(() => nostrPubkeyToBitcoinAddress(pubkey)).not.toThrow();
      const address = nostrPubkeyToBitcoinAddress(pubkey);
      expect(address).toMatch(/^bc1p/);
    });
    
    test('rejects invalid key lengths', () => {
      expect(() => {
        nostrPubkeyToBitcoinAddress('abc'); // Too short
      }).toThrow('Invalid pubkey length');
      
      expect(() => {
        nostrPubkeyToBitcoinAddress('a'.repeat(66)); // Too long
      }).toThrow('Invalid pubkey length');
    });
    
    test('rejects non-hex characters', () => {
      expect(() => {
        nostrPubkeyToBitcoinAddress('g'.repeat(64)); // Invalid hex
      }).toThrow('Invalid hex characters');
    });
    
    test('rejects empty or null input', () => {
      expect(() => nostrPubkeyToBitcoinAddress('')).toThrow();
      expect(() => nostrPubkeyToBitcoinAddress(null as any)).toThrow();
    });
    
    test('generates deterministic addresses', () => {
      const pubkey = 'b'.repeat(64);
      const addr1 = nostrPubkeyToBitcoinAddress(pubkey);
      const addr2 = nostrPubkeyToBitcoinAddress(pubkey);
      expect(addr1).toBe(addr2);
    });
  });
  
  describe('npubToBitcoinAddress', () => {
    test('converts valid npub to address', () => {
      // Use a real npub format (simplified test)
      const npub = 'npub1test...'; // Replace with valid npub in real test
      // This would require mocking nip19.decode
    });
    
    test('rejects invalid npub format', () => {
      expect(() => {
        npubToBitcoinAddress('invalid');
      }).toThrow();
    });
  });
  
  describe('calculateMaxSendAmount', () => {
    test('returns balance minus fee', () => {
      const utxos = [
        { txid: '123', vout: 0, value: 10000, status: { confirmed: true } }
      ];
      const feeRate = 1;
      
      const maxAmount = calculateMaxSendAmount(utxos, feeRate);
      
      expect(maxAmount).toBeLessThan(10000);
      expect(maxAmount).toBeGreaterThan(9000);
    });
    
    test('returns 0 if fee exceeds balance', () => {
      const utxos = [
        { txid: '123', vout: 0, value: 100, status: { confirmed: true } }
      ];
      const feeRate = 10;
      
      const maxAmount = calculateMaxSendAmount(utxos, feeRate);
      
      expect(maxAmount).toBe(0);
    });
  });
});
```

### Integration Tests

```typescript
// hooks/useBitcoin.test.tsx
describe('useBitcoinBalance', () => {
  test('fetches balance and UTXOs', async () => {
    const { result, waitFor } = renderHook(() => 
      useBitcoinBalance('bc1p...')
    );
    
    await waitFor(() => result.current.isSuccess);
    
    expect(result.current.data).toHaveProperty('balance');
    expect(result.current.data).toHaveProperty('utxos');
  });
});
```

## Security Considerations

### Critical Security Rules

1. **Never log private keys**
   - No console.log, no error messages, no debug output
   - Use secure memory handling

2. **Validate all inputs**
   - Bitcoin addresses
   - Transaction amounts
   - UTXO data from APIs

3. **Use HTTPS for all API calls**
   - Never send sensitive data over HTTP

4. **Implement rate limiting**
   - Prevent API abuse
   - Handle errors gracefully

5. **Verify transaction before broadcast**
   - Double-check recipient address
   - Confirm amounts
   - Show clear confirmation UI

6. **Handle errors without exposing details**
   ```typescript
   import { useToast } from '@/hooks/useToast';
   
   // In your component or hook:
   const { toast } = useToast();
   
   catch (error) {
     console.error('Transaction error:', error); // For developers
     // Default: Toast notification
     toast({ variant: "destructive", title: "Transaction Failed", description: "Please try again" });
     // Alternative options (commented):
     // Option 1: Console logging
     // console.error('Transaction Failed: Please try again');
     // Option 2: No notification (silent failure)
   }
   ```

## Common Pitfalls

### 1. ❌ Forgetting to initialize ECC library

**Problem:** bitcoinjs-lib v7+ requires `bitcoin.initEccLib(ecc)` before any operations. Missing this causes runtime errors when calling bitcoinjs-lib functions.

**Solution:** Initialize at module load time (top level of bitcoin utilities file):
```typescript
import * as bitcoin from 'bitcoinjs-lib';
import * as ecc from '@bitcoinerlab/secp256k1';

// Initialize ECC library immediately - MUST be at top level
bitcoin.initEccLib(ecc);
```

**Where:** Top level of your bitcoin utilities module, not inside functions. Call once when the module loads.

### 2. ❌ Treating Nostr keys like Bitcoin compressed keys

**Problem:** Nostr pubkeys are 32 bytes (64 hex chars) with no prefix. Bitcoin compressed keys are 33 bytes with 02/03 prefix. Using `.subarray(1, 33)` removes actual key data.

**Wrong:**
```typescript
internalPubkey: pubkeyBuffer.subarray(1, 33) // Removes first byte - WRONG for Nostr!
```

**Right:**
```typescript
internalPubkey: pubkeyBuffer // Use full 32-byte Nostr key directly
```

**Solution:** Always validate key length before conversion. Nostr keys = 64 hex chars exactly.

### 2. ❌ No validation before key conversion

**Problem:** `Buffer.from(pubkey, 'hex')` can fail silently or produce wrong-sized buffers.

**Wrong:**
```typescript
const buffer = Buffer.from(pubkeyHex, 'hex'); // No validation
```

**Right:**
```typescript
function validateAndConvertKey(pubkeyHex: string): Buffer {
  // Remove 0x prefix, validate length (64 chars), validate hex format
  // Then convert to buffer and verify 32 bytes
}
```

**Solution:** Always validate length, format, and buffer size before using keys.

### 3. ❌ Ignoring edge cases (0x prefix, whitespace, case)

**Problem:** Keys may come with `0x` prefix, whitespace, or mixed case.

**Solution:** Normalize input first:
```typescript
let cleanHex = pubkeyHex.trim();
if (cleanHex.startsWith('0x')) cleanHex = cleanHex.slice(2);
// Then validate and convert
```

### 4. ❌ Poor error messages

**Problem:** Generic errors like "Invalid key" don't help debugging.

**Wrong:**
```typescript
throw new Error('Invalid key');
```

**Right:**
```typescript
throw new Error(`Invalid pubkey length: expected 64 hex chars, got ${cleanHex.length}`);
```

**Solution:** Include specific details: expected vs actual values, what failed, why.

### 5. Forgetting to handle dust outputs

**Problem:** Creating outputs below 546 sats (dust threshold) makes transactions invalid.

**Solution:**
```typescript
if (changeAmount >= 546) {
  psbt.addOutput({ address: senderAddress, value: changeAmount });
}
```

### 6. Not refreshing UTXOs after transactions

**Problem:** Using stale UTXO data leads to double-spend attempts.

**Solution:** Always refetch UTXOs after broadcasting transactions.

### 7. Incorrect fee calculation

**Problem:** Underestimating fees causes transactions to be rejected or delayed.

**Solution:** Use current fee rates and add buffer for safety.

### 8. Not handling unconfirmed UTXOs

**Problem:** Spending unconfirmed UTXOs can cause transaction chains to fail.

**Solution:** Filter UTXOs by confirmation status:
```typescript
const confirmedUtxos = utxos.filter(utxo => utxo.status.confirmed);
```

## Extension Points

### Adding Advanced Features

**Replace-By-Fee (RBF):**
- Allow users to bump transaction fees
- Add RBF flag during transaction creation

**Coin Control:**
- Let users manually select which UTXOs to spend
- Add UTXO selection UI

**Multi-sig Support:**
- Implement P2WSH for multi-signature addresses
- Add co-signer coordination

## API Dependencies

### Blockstream API

Primary data source for Bitcoin operations:

- **Base URL:** `https://blockstream.info/api`
- **Rate Limits:** Respect fair use, implement retry logic
- **Endpoints:**
  - `/address/:address/utxo` - Fetch UTXOs
  - `/address/:address/txs` - Transaction history
  - `/tx/:txid` - Transaction details
  - `/fee-estimates` - Current fee rates
  - `/tx` (POST) - Broadcast transactions

**Alternative APIs:**
- Mempool.space API (compatible interface)
- Run your own Bitcoin node + Electrum server

## Verification Checklist

Before marking implementation complete:

### Address Generation Tests
- [ ] Test with multiple Nostr pubkeys (different keys produce different addresses)
- [ ] Verify addresses start with `bc1p` (Taproot format)
- [ ] Test with keys that have `0x` prefix (handled correctly)
- [ ] Test error handling for invalid inputs (wrong length, non-hex, empty)
- [ ] Verify addresses are deterministic (same key = same address)
- [ ] Test npub conversion to Bitcoin address

### Core Functionality
- [ ] All tests pass (unit + integration)
- [ ] UTXO fetching handles errors gracefully
- [ ] Transaction creation follows BIP standards
- [ ] Fee calculation is accurate
- [ ] Send Max works correctly
- [ ] UTXO consolidation creates valid transactions
- [ ] Transaction history displays correctly

### Security & Error Handling
- [ ] Private keys never logged or exposed
- [ ] All API calls have error handling
- [ ] Input validation catches invalid keys/addresses early
- [ ] Error messages are specific and helpful

### User Experience
- [ ] UI shows clear confirmation before sending
- [ ] Balance updates after transactions
- [ ] Loading states display during operations
- [ ] Error messages are user-friendly

### Testing
- [ ] Works with testnet for initial testing
- [ ] Integration tests cover full transaction flow
- [ ] Edge cases tested (dust outputs, unconfirmed UTXOs, etc.)

## Resources

**Bitcoin Improvement Proposals (BIPs):**
- BIP 340: Schnorr signatures
- BIP 341: Taproot
- BIP 86: Key derivation for P2TR addresses

**Documentation:**
- bitcoinjs-lib: https://github.com/bitcoinjs/bitcoinjs-lib
- Blockstream API: https://github.com/Blockstream/esplora/blob/master/API.md

## Summary

To implement a Bitcoin wallet:

1. **Start with TDD** - Write tests first for all functions
2. **Address derivation** - Convert Nostr keys to Bitcoin addresses
3. **UTXO management** - Fetch and track unspent outputs
4. **Transaction building** - Create, sign, and broadcast properly
5. **React hooks** - Implement balance, history, and operations
6. **UI components** - Build wallet interface
7. **Security** - Never expose private keys, validate everything
8. **Testing** - Comprehensive unit and integration tests

**Key principle:** The wallet enables Bitcoin functionality using Nostr identity, eliminating separate key management while maintaining Bitcoin's security model.

