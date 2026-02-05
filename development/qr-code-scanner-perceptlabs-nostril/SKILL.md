---
name: qr-code-scanner
description: Use when implementing QR code scanning - provides complete patterns for camera-based scanning, classifying scanned content (Bitcoin addresses, Lightning invoices, npubs, Cashu tokens), handling camera permissions, and paste from clipboard functionality
when_to_use: When adding QR code scanning functionality, implementing camera-based scanning, classifying scanned QR content, or handling QR code input from users
---

# QR Code Scanning

## Overview

Complete implementation guide for QR code scanning with camera-based detection and content classification. Supports Bitcoin addresses, Lightning invoices, Lightning addresses, Nostr npubs, and Cashu tokens.

**Core Capabilities:**
- Camera-based QR code scanning
- Automatic content classification
- Camera permission handling
- Paste from clipboard functionality
- Error recovery and fallbacks

## Prerequisites

**IMPORTANT:** Before adding dependencies, review your project's `package.json` to check if any of these packages already exist. If they do, verify the versions are compatible with the requirements below. Only add packages that are missing or need version updates.

**Required packages:**
```json
{
  "html5-qrcode": "^2.3.8"
}
```

## Implementation Checklist

- [ ] Install QR scanner package (`html5-qrcode`)
- [ ] Implement content classification logic
- [ ] Implement QR code scanning hook
- [ ] Handle camera permissions
- [ ] Add paste from clipboard functionality
- [ ] Add error handling and fallbacks
- [ ] Create QR scanner component

## Part 1: Content Classification

**CRITICAL:** Classify scanned content before processing to route to correct handlers.

```typescript
// hooks/useQRCodeScanner.ts
export type QRScanResult = 
  | { type: 'lightning_invoice'; value: string }
  | { type: 'lightning_address'; value: string }
  | { type: 'cashu_token'; value: string }
  | { type: 'bitcoin_address'; value: string }
  | { type: 'npub'; value: string }
  | { type: 'unknown'; value: string };

export function classifyQRCode(decodedText: string): QRScanResult {
  // Lightning invoice: lnbc... or lightning:lnbc...
  const lightningInvoiceMatch = decodedText.match(/^(?:lightning:)?(lnbc[a-z0-9]+)$/i);
  if (lightningInvoiceMatch) {
    return { type: 'lightning_invoice', value: lightningInvoiceMatch[1] };
  }

  // Lightning address: name@domain.tld or lightning:name@domain.tld
  const lightningAddressMatch = decodedText.match(/^(?:lightning:)?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$/);
  if (lightningAddressMatch) {
    return { type: 'lightning_address', value: lightningAddressMatch[1] };
  }

  // Cashu token: cashu...
  if (/^cashu[A-Za-z0-9+/=_-]+$/.test(decodedText)) {
    return { type: 'cashu_token', value: decodedText };
  }

  // Bitcoin address: bc1... or legacy (1..., 3...)
  if (/^(bc1|3|1)[a-zA-Z0-9]{25,62}$/.test(decodedText)) {
    return { type: 'bitcoin_address', value: decodedText };
  }

  // Nostr npub: npub1... or nostr:npub1...
  const npubMatch = decodedText.match(/^(?:nostr:)?(npub1[a-z0-9]{58})$/);
  if (npubMatch) {
    return { type: 'npub', value: npubMatch[1] };
  }

  return { type: 'unknown', value: decodedText };
}
```

**Why classify first?**
- Routes to correct handler automatically
- Validates format before processing
- Provides better error messages
- Prevents processing invalid data

## Part 2: Camera Scanning Hook

```typescript
// hooks/useQRCodeScanner.ts
import { useState, useCallback, useRef } from 'react';
import { Html5Qrcode } from 'html5-qrcode';
// optional import { useToast } from '@/hooks/useToast';
import type { QRScanResult } from './useQRCodeScanner';

export function useQRCodeScanner() {
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scannerRef = useRef<Html5Qrcode | null>(null);
  const isStartingRef = useRef(false);
  const shouldCancelRef = useRef(false);
  // Optional: User feedback notifications
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: Toast notifications (if useToast hook is available)
  // const { toast } = useToast();
  // Option 3: No notification handler

  const startScanning = useCallback(async (
    onResult: (result: QRScanResult) => void
  ): Promise<void> => {
    try {
      isStartingRef.current = true;
      shouldCancelRef.current = false;
      setError(null);
      
      // Find available cameras
      const devices = await Html5Qrcode.getCameras();
      if (devices.length === 0) {
        throw new Error('No cameras found');
      }

      // Check if cancelled during camera detection
      if (shouldCancelRef.current) {
        isStartingRef.current = false;
        return;
      }

      // Use rear camera by default, or first available
      const cameraId = devices.length > 1 
        ? devices.find(d => 
            d.label.toLowerCase().includes('back') || 
            d.label.toLowerCase().includes('rear')
          )?.id || devices[0].id
        : devices[0].id;

      // Initialize scanner (requires element with id="qr-reader")
      const scanner = new Html5Qrcode('qr-reader');
      scannerRef.current = scanner;

      // Start scanning
      await scanner.start(
        cameraId,
        {
          fps: 10,
          aspectRatio: 1,
          qrbox: 250
        },
        (decodedText) => {
          // Classify and handle result
          const result = classifyQRCode(decodedText);
          onResult(result);
        },
        (errorMessage) => {
          // Ignore "QR code not found" errors (normal during scanning)
          if (!errorMessage.includes('qr')) {
            console.debug('QR scan error:', errorMessage);
          }
        }
      );

      isStartingRef.current = false;
      setIsScanning(true);
      
    } catch (err) {
      isStartingRef.current = false;
      let errorMessage = 'Failed to start camera';
      
      if (err instanceof Error) {
        errorMessage = err.message;
      }
      
      // Provide helpful error messages
      if (errorMessage.includes('NotAllowedError') || errorMessage.includes('Permission denied')) {
        errorMessage = 'Camera permission denied. Please allow camera access.';
      } else if (errorMessage.includes('NotFoundError') || errorMessage.includes('No device')) {
        errorMessage = 'No camera found. Please connect a camera.';
      }
      
      setError(errorMessage);
      setIsScanning(false);
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.error('Camera Error:', errorMessage);
      // Option 2: Toast notification (if toast is available)
      // toast({ variant: "destructive", title: "Camera Error", description: errorMessage });
      // Option 3: No notification (silent failure)
    }
  }, []);

  const stopScanning = useCallback(async (): Promise<void> => {
    try {
      // Handle cancellation during startup
      if (isStartingRef.current) {
        shouldCancelRef.current = true;
        // Wait for startup to complete
        let attempts = 0;
        while (isStartingRef.current && attempts < 50) {
          await new Promise(resolve => setTimeout(resolve, 100));
          attempts++;
        }
      }
      
      if (scannerRef.current) {
        const scanner = scannerRef.current;
        
        // Check scanner state before stopping
        const state = scanner.getState();
        if (state === 2) { // SCANNING
          await scanner.stop();
        } else if (state === 1) { // STARTING
          await new Promise(resolve => setTimeout(resolve, 200));
          if (scanner.getState() === 2) {
            await scanner.stop();
          }
        }
        
        await scanner.clear();
        scannerRef.current = null;
      }
      
      shouldCancelRef.current = false;
      isStartingRef.current = false;
      setIsScanning(false);
      setError(null);
    } catch (err) {
      console.error('Error stopping scanner:', err);
      scannerRef.current = null;
      setIsScanning(false);
    }
  }, []);

  return {
    isScanning,
    error,
    startScanning,
    stopScanning,
    classifyQRCode,
  };
}
```

## Part 3: QR Scanner Component

```typescript
// components/QRScanner.tsx
import { useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import * as VisuallyHidden from '@radix-ui/react-visually-hidden';
// optional import { useToast } from '@/hooks/useToast';
import type { QRScanResult } from '@/hooks/useQRCodeScanner';

interface QRScannerProps {
  isOpen: boolean;
  onClose: () => Promise<void>;
  onResult: (result: QRScanResult) => void;
  classifyQRCode: (text: string) => QRScanResult;
  startScanning: (onResult: (result: QRScanResult) => void) => Promise<void>;
  stopScanning: () => Promise<void>;
  setModalOpen?: (isOpen: boolean) => void;
  qrError: string | null;
}

export function QRScanner({
  isOpen,
  onClose,
  onResult,
  classifyQRCode,
  startScanning,
  stopScanning,
  setModalOpen,
  qrError,
}: QRScannerProps) {
  // Optional: User feedback notifications
  // Option 1: Console logging
  // const logMessage = (message: string) => console.log(message);
  // Option 2: Toast notifications (if useToast hook is available)
  // const { toast } = useToast();
  // Option 3: No notification handler

  // Handle paste from clipboard
  const handlePasteQRCode = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (!text || !text.trim()) {
        // Optional: User feedback - choose one:
        // Option 1: Console logging
        // console.error('Clipboard Empty: No text found in clipboard');
        // Option 2: Toast notification (if toast is available)
        // toast({ variant: "destructive", title: "Clipboard Empty", description: "No text found in clipboard" });
        // Option 3: No notification (silent failure)
        return;
      }

      const result = classifyQRCode(text.trim());
      onResult(result);
      await stopScanning();
      await onClose();
    } catch (err) {
      console.error('Error pasting from clipboard:', err);
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.error('Paste Failed: Could not read from clipboard');
      // Option 2: Toast notification (if toast is available)
      // toast({ variant: "destructive", title: "Paste Failed", description: "Could not read from clipboard" });
      // Option 3: No notification (silent failure)
    }
  };

  // Start/stop scanning based on isOpen
  useEffect(() => {
    if (isOpen) {
      setModalOpen?.(true);
      startScanning(onResult);
    } else {
      setModalOpen?.(false);
      stopScanning();
    }
  }, [isOpen, startScanning, stopScanning, setModalOpen, onResult]);

  return (
    <Dialog open={isOpen} onOpenChange={async (open) => {
      if (!open) {
        await onClose();
      }
    }}>
      <DialogContent className="max-w-[min(90vw,500px)] w-full p-4 sm:p-6">
        <DialogHeader>
          <DialogTitle>Scan QR Code</DialogTitle>
          <VisuallyHidden.Root asChild>
            <DialogDescription>
              Position the QR code within the camera view to scan
            </DialogDescription>
          </VisuallyHidden.Root>
        </DialogHeader>

        <div className="relative w-full" style={{ aspectRatio: '1 / 1' }}>
          {/* Scanner requires element with id="qr-reader" */}
          <div
            id="qr-reader"
            className="w-full h-full rounded-xl overflow-hidden bg-muted"
          />

          {/* Error overlay */}
          {qrError && (
            <div className="absolute inset-x-4 top-4 p-3 bg-destructive text-destructive-foreground rounded-lg text-center z-50 shadow-lg">
              {qrError}
            </div>
          )}
        </div>

        {/* Paste from clipboard button */}
        <div className="mt-4 flex justify-center">
          <Button
            onClick={handlePasteQRCode}
            className="h-12 px-12 rounded-full"
            size="lg"
          >
            Paste
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

**Key Features:**
- **Paste from clipboard** - Alternative to camera scanning
- **Error overlay** - Displays camera errors above scanner
- **Proper cleanup** - Stops scanner when dialog closes
- **Accessibility** - Uses VisuallyHidden for screen readers
- **Responsive** - Works on mobile and desktop
- **Aspect ratio** - Maintains square scanner viewport

## Part 4: Paste from Clipboard

**CRITICAL:** Always provide paste functionality as an alternative to camera scanning. Users may have QR codes in text format or camera may be unavailable.

### Paste Implementation

```typescript
// In QRScanner component
const handlePasteQRCode = async () => {
  try {
    const text = await navigator.clipboard.readText();
    if (!text || !text.trim()) {
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.error('Clipboard Empty: No text found in clipboard');
      // Option 2: Toast notification (if toast is available)
      // toast({ variant: "destructive", title: "Clipboard Empty", description: "No text found in clipboard" });
      // Option 3: No notification (silent failure)
      return;
    }

    // Classify and process pasted content
    const result = classifyQRCode(text.trim());
    onResult(result);
    await stopScanning();
    await onClose();
  } catch (err) {
    // Optional: User feedback - choose one:
    // Option 1: Console logging
    // console.error('Paste Failed: Could not read from clipboard');
    // Option 2: Toast notification (if toast is available)
    // toast({ variant: "destructive", title: "Paste Failed", description: "Could not read from clipboard" });
    // Option 3: No notification (silent failure)
  }
};
```

**Why paste is essential:**
- Camera may be unavailable or denied
- Users may have QR code as text
- Faster for users who already have text copied
- Better accessibility for users who can't use camera

## Part 5: Content Type Handling

### Bitcoin Address Handling

```typescript
// Handle scanned Bitcoin address
function handleQRResult(result: QRScanResult) {
  if (result.type === 'bitcoin_address') {
    // Validate address format
    if (isValidBitcoinAddress(result.value)) {
      setBitcoinRecipient(result.value);
      setShowSendModal(true);
    } else {
      // Optional: User feedback - choose one:
      // Option 1: Console logging
      // console.error('Invalid Address: Scanned address is not valid');
      // Option 2: Toast notification (if toast is available)
      // toast({ variant: "destructive", title: "Invalid Address", description: "Scanned address is not valid" });
      // Option 3: No notification (silent failure)
    }
  }
}
```

### Lightning Invoice Handling

```typescript
if (result.type === 'lightning_invoice') {
  // Decode invoice to get amount
  const decoded = decodeLightningInvoice(result.value);
  setLightningInvoice(result.value);
  setDecodedInvoiceAmount(decoded.amount);
  setShowPayModal(true);
}
```

### Lightning Address Handling

```typescript
if (result.type === 'lightning_address') {
  // Validate and process Lightning address
  setLightningAddress(result.value);
  setShowPayModal(true);
}
```

### Cashu Token Handling

```typescript
if (result.type === 'cashu_token') {
  // Process Cashu token
  setCashuToken(result.value);
  setShowRedeemModal(true);
}
```

### npub Handling

```typescript
if (result.type === 'npub') {
  try {
    // Convert npub to Bitcoin address if needed
    const address = npubToBitcoinAddress(result.value);
    setBitcoinRecipient(address);
    setShowSendModal(true);
  } catch {
    // Optional: User feedback - choose one:
    // Option 1: Console logging
    // console.error('Invalid npub: Could not decode npub');
    // Option 2: Toast notification (if toast is available)
    // toast({ variant: "destructive", title: "Invalid npub", description: "Could not decode npub" });
    // Option 3: No notification (silent failure)
  }
}
```

### Unknown Content Handling

```typescript
if (result.type === 'unknown') {
  // Optional: User feedback - choose one:
  // Option 1: Console logging
  // console.error('Unknown Content: Could not classify scanned QR code');
  // Option 2: Toast notification (if toast is available)
  // toast({ variant: "destructive", title: "Unknown Content", description: "Could not classify scanned QR code" });
  // Option 3: No notification (silent failure)
  
  // Or show raw content for user to decide
  setRawContent(result.value);
  setShowUnknownContentModal(true);
}
```

## Common Pitfalls

### 1. ❌ Missing scanner element

**Problem:** Html5Qrcode requires a DOM element with `id="qr-reader"` to mount the scanner.

**Solution:** Always include the element before calling `startScanning`:
```tsx
<div id="qr-reader" className="w-full" />
```

### 2. ❌ Not handling camera permissions

**Problem:** Browser blocks camera access without user permission, causing errors.

**Solution:** Provide clear error messages and instructions:
```typescript
if (errorMessage.includes('NotAllowedError')) {
  errorMessage = 'Camera permission denied. Please allow camera access.';
}
```

### 3. ❌ Not cleaning up scanner

**Problem:** Scanner continues running after component unmounts, causing memory leaks.

**Solution:** Always stop scanner in cleanup:
```typescript
useEffect(() => {
  if (isOpen) {
    startScanning(onResult);
  }
  
  return () => {
    stopScanning(); // Cleanup on unmount
  };
}, [isOpen]);
```

### 4. ❌ Not providing paste alternative

**Problem:** Camera may be unavailable, denied, or users may have QR code as text. Without paste, users are blocked.

**Solution:** Always include paste from clipboard functionality:
```typescript
const handlePasteQRCode = async () => {
  const text = await navigator.clipboard.readText();
  const result = classifyQRCode(text.trim());
  onResult(result);
  await stopScanning();
  await onClose();
};
```

**Why:** Paste provides accessibility and fallback when camera fails.

### 5. ❌ Not classifying scanned content

**Problem:** Processing unknown content types causes errors.

**Solution:** Always classify first, then route:
```typescript
const result = classifyQRCode(decodedText);
if (result.type === 'bitcoin_address') {
  // Handle Bitcoin address
} else if (result.type === 'lightning_invoice') {
  // Handle Lightning invoice
}
```

### 6. ❌ Scanner state management issues

**Problem:** Trying to stop scanner while it's starting causes errors.

**Solution:** Use refs to track state and handle cancellation:
```typescript
const isStartingRef = useRef(false);
const shouldCancelRef = useRef(false);

// Check state before operations
if (isStartingRef.current) {
  shouldCancelRef.current = true;
  // Wait for startup to complete
}
```

### 7. ❌ Not handling multiple scans

**Problem:** Scanner may trigger multiple times for the same QR code.

**Solution:** Debounce or prevent duplicate scans:
```typescript
const lastScannedRef = useRef<string>('');

const handleScan = (result: QRScanResult) => {
  if (lastScannedRef.current === result.value) {
    return; // Ignore duplicate scan
  }
  lastScannedRef.current = result.value;
  onResult(result);
};
```

## Testing Strategy

### Unit Tests

```typescript
import { describe, it, expect } from 'vitest';
import { classifyQRCode } from '@/hooks/useQRCodeScanner';

describe('classifyQRCode', () => {
  it('classifies Bitcoin addresses', () => {
    const result = classifyQRCode('bc1p...');
    expect(result.type).toBe('bitcoin_address');
  });
  
  it('classifies Lightning invoices', () => {
    const result = classifyQRCode('lnbc123...');
    expect(result.type).toBe('lightning_invoice');
  });
  
  it('handles lightning: prefix', () => {
    const result = classifyQRCode('lightning:lnbc123...');
    expect(result.type).toBe('lightning_invoice');
    expect(result.value).toBe('lnbc123...');
  });
  
  it('classifies Lightning addresses', () => {
    const result = classifyQRCode('user@example.com');
    expect(result.type).toBe('lightning_address');
  });
  
  it('classifies Cashu tokens', () => {
    const result = classifyQRCode('cashuA...');
    expect(result.type).toBe('cashu_token');
  });
  
  it('classifies npubs', () => {
    const result = classifyQRCode('npub1abc...');
    expect(result.type).toBe('npub');
  });
  
  it('handles nostr: prefix', () => {
    const result = classifyQRCode('nostr:npub1abc...');
    expect(result.type).toBe('npub');
    expect(result.value).toBe('npub1abc...');
  });
  
  it('returns unknown for unrecognized content', () => {
    const result = classifyQRCode('random text');
    expect(result.type).toBe('unknown');
  });
});
```

### Integration Tests

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useQRCodeScanner } from '@/hooks/useQRCodeScanner';
import { Html5Qrcode } from 'html5-qrcode';

vi.mock('html5-qrcode');

describe('useQRCodeScanner', () => {
  beforeEach(() => {
    vi.mocked(Html5Qrcode.getCameras).mockResolvedValue([
      { id: 'camera1', label: 'Back Camera' }
    ]);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('starts scanning successfully', async () => {
    const mockScanner = {
      start: vi.fn().mockResolvedValue(undefined),
      stop: vi.fn().mockResolvedValue(undefined),
      clear: vi.fn().mockResolvedValue(undefined),
      getState: vi.fn().mockReturnValue(2), // SCANNING
    };
    
    vi.mocked(Html5Qrcode).mockImplementation(() => mockScanner as any);

    const { result } = renderHook(() => useQRCodeScanner());

    await result.current.startScanning(vi.fn());

    expect(mockScanner.start).toHaveBeenCalled();
    expect(result.current.isScanning).toBe(true);
  });

  it('handles camera permission errors', async () => {
    vi.mocked(Html5Qrcode.getCameras).mockRejectedValue(
      new Error('NotAllowedError: Permission denied')
    );

    const { result } = renderHook(() => useQRCodeScanner());

    await result.current.startScanning(vi.fn());

    expect(result.current.error).toContain('Camera permission denied');
    expect(result.current.isScanning).toBe(false);
  });

  it('stops scanning correctly', async () => {
    const mockScanner = {
      start: vi.fn().mockResolvedValue(undefined),
      stop: vi.fn().mockResolvedValue(undefined),
      clear: vi.fn().mockResolvedValue(undefined),
      getState: vi.fn().mockReturnValue(2), // SCANNING
    };
    
    vi.mocked(Html5Qrcode).mockImplementation(() => mockScanner as any);

    const { result } = renderHook(() => useQRCodeScanner());

    await result.current.startScanning(vi.fn());
    await result.current.stopScanning();

    expect(mockScanner.stop).toHaveBeenCalled();
    expect(mockScanner.clear).toHaveBeenCalled();
    expect(result.current.isScanning).toBe(false);
  });
});
```

## Security Considerations

1. **Validate scanned content** - Don't trust QR code content blindly, always validate format
2. **Sanitize before display** - Escape HTML in scanned text before showing to users
3. **Rate limit scanning** - Prevent rapid-fire scans that could be used for abuse
4. **Handle malicious QR codes** - Some QR codes can contain malicious URLs or data
5. **Verify content types** - Double-check classified content matches expected format before processing

## Verification Checklist

- [ ] Scanner starts and stops correctly
- [ ] Camera permissions handled gracefully
- [ ] Content classification accurate for all types
- [ ] Scanner cleanup on component unmount
- [ ] Error messages are user-friendly
- [ ] Works on mobile devices
- [ ] Handles camera switching (front/rear)
- [ ] Scanner state managed correctly
- [ ] No memory leaks from scanner instances
- [ ] Paste from clipboard works correctly
- [ ] All content types route to correct handlers
- [ ] Unknown content handled gracefully
- [ ] Duplicate scans prevented

## Summary

To implement QR code scanning:

1. **Install package** - `html5-qrcode`
2. **Classify content** - Route scanned content to correct handlers
3. **Scan QR codes** - Use `Html5Qrcode` with camera access
4. **Handle permissions** - Provide clear error messages for camera access
5. **Add paste functionality** - Provide clipboard paste as alternative
6. **Clean up** - Always stop scanner on unmount
7. **Test thoroughly** - Test all content types and error cases

**Key principle:** Classify scanned content before processing to ensure correct routing and validation.

