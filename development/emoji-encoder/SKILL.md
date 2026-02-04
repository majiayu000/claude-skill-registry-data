---
name: emoji-encoder
description: Use when implementing steganographic text encoding using Unicode Variation Selectors - allows encoding any message invisibly into emojis, letters, or any characters using Unicode Variation Selectors (U+FE00-U+FE0F and U+E0100-U+E01EF)
when_to_use: When adding steganographic encoding, hiding data in plain text, encoding messages into emojis/characters, or implementing invisible data encoding using Unicode Variation Selectors
---

# Emoji Encoder - Steganographic Text Encoding

## Overview

Complete implementation guide for encoding any text message invisibly into emojis, letters, or any Unicode characters using Unicode Variation Selectors. The encoded data appears as just the marker character (emoji/letter) followed by invisible variation selector characters, making it perfect for steganographic applications.

**Core Capabilities:**
- Encode any UTF-8 text into invisible Unicode Variation Selectors
- Use any character as a marker (emojis, letters, symbols)
- Decode hidden messages from encoded text
- Detect if text contains encoded data
- React hooks for easy integration
- Zero external dependencies - pure TypeScript/JavaScript

## How It Works

The encoding uses Unicode Variation Selectors to invisibly encode UTF-8 bytes:

- **Bytes 0-15**: Encoded as Variation Selectors (U+FE00-U+FE0F)
- **Bytes 16-255**: Encoded as Variation Selectors Supplement (U+E0100-U+E01EF)
- **Marker**: **Any Unicode character** (emoji, letter, symbol, number, punctuation, etc.) appears before encoded data
- **Result**: Appears as just the marker character, with invisible encoded data following

**CRITICAL:** The marker can be **any Unicode character** - there are no restrictions. Use emojis, letters, numbers, symbols, or any other Unicode character that fits your use case.

**Example:**
```
Input: "Hello, World!"
Marker: "🥜"
Output: "🥜" + [invisible variation selectors]
```

The output looks like just "🥜" but contains the full encoded message.

## Prerequisites

**IMPORTANT:** Before adding dependencies, review your project's `package.json` to check if any of these packages already exist. If they do, verify the versions are compatible with the requirements below. Only add packages that are missing or need version updates.

**Required packages:**
```json
{
  "typescript": "^5.x"
}
```

**No external dependencies required** - uses only native JavaScript/TypeScript APIs.

## Implementation Checklist

- [ ] Implement core encoding/decoding functions
- [ ] Add React hooks for easy integration
- [ ] Create UI components for encoding/decoding
- [ ] Add emoji/character selector component
- [ ] Implement detection function (isEncoded)
- [ ] Add error handling and validation
- [ ] Create tests for encoding/decoding
- [ ] Add copy-to-clipboard functionality

## Part 1: Core Encoding Functions

### Unicode Variation Selector Constants

```typescript
// Variation selectors block https://unicode.org/charts/nameslist/n_FE00.html
// VS1..=VS16
const VARIATION_SELECTOR_START = 0xfe00;
const VARIATION_SELECTOR_END = 0xfe0f;

// Variation selectors supplement https://unicode.org/charts/nameslist/n_E0100.html
// VS17..=VS256
const VARIATION_SELECTOR_SUPPLEMENT_START = 0xe0100;
const VARIATION_SELECTOR_SUPPLEMENT_END = 0xe01ef;
```

### Byte to Variation Selector

```typescript
export function toVariationSelector(byte: number): string | null {
    if (byte >= 0 && byte < 16) {
        return String.fromCodePoint(VARIATION_SELECTOR_START + byte);
    } else if (byte >= 16 && byte < 256) {
        return String.fromCodePoint(VARIATION_SELECTOR_SUPPLEMENT_START + byte - 16);
    } else {
        return null;
    }
}
```

**How it works:**
- Bytes 0-15 map to U+FE00-U+FE0F (16 characters)
- Bytes 16-255 map to U+E0100-U+E01EF (240 characters)
- Total coverage: 256 possible byte values

### Variation Selector to Byte

```typescript
export function fromVariationSelector(codePoint: number): number | null {
    if (codePoint >= VARIATION_SELECTOR_START && codePoint <= VARIATION_SELECTOR_END) {
        return codePoint - VARIATION_SELECTOR_START;
    } else if (codePoint >= VARIATION_SELECTOR_SUPPLEMENT_START && codePoint <= VARIATION_SELECTOR_SUPPLEMENT_END) {
        return codePoint - VARIATION_SELECTOR_SUPPLEMENT_START + 16;
    } else {
        return null;
    }
}
```

**Reverse mapping:**
- U+FE00-U+FE0F → bytes 0-15
- U+E0100-U+E01EF → bytes 16-255

### Encode Function

```typescript
export function encode(marker: string, text: string): string {
    // Convert the string to utf-8 bytes
    const bytes = new TextEncoder().encode(text);
    let encoded = marker;

    for (const byte of bytes) {
        const selector = toVariationSelector(byte);
        if (selector === null) {
            throw new Error(`Invalid byte value: ${byte}`);
        }
        encoded += selector;
    }

    return encoded;
}
```

**Key points:**
- Uses `TextEncoder` to convert string to UTF-8 bytes
- Marker appears first (visible character)
- Each byte encoded as variation selector (invisible)
- Handles all UTF-8 characters (including Unicode)

**Usage:**
```typescript
const encoded = encode('🥜', 'Hello, World!');
// Result: "🥜" + [invisible characters]
```

### Decode Function

```typescript
export function decode(text: string): string {
    let decoded: number[] = [];
    const chars = Array.from(text);

    for (const char of chars) {
        const codePoint = char.codePointAt(0);
        if (codePoint === undefined) continue;
        
        const byte = fromVariationSelector(codePoint);

        if (byte === null && decoded.length > 0) {
            // Stop at first non-variation-selector after decoding started
            break;
        } else if (byte === null) {
            // Skip non-variation-selector characters before decoding starts
            continue;
        }

        decoded.push(byte);
    }

    if (decoded.length === 0) {
        throw new Error('No encoded data found');
    }

    const decodedArray = new Uint8Array(decoded);
    return new TextDecoder().decode(decodedArray);
}
```

**Key points:**
- Skips marker character (first non-variation-selector)
- Stops at first non-variation-selector after decoding starts
- Uses `TextDecoder` to convert UTF-8 bytes back to string
- Handles all UTF-8 characters correctly

**Usage:**
```typescript
const decoded = decode(encodedText);
// Result: "Hello, World!"
```

## Part 2: React Hook Implementation

### useEmojiEncoding Hook

```typescript
import { useCallback } from 'react';

export interface EmojiEncodingOptions {
  /** Marker/prefix before encoded data (default: '🥜'). Can be any string, emoji, or empty. */
  marker?: string;
}

/**
 * Hook for encoding and decoding any string data using Unicode Variation Selectors.
 * 
 * Encodes data invisibly using Unicode Variation Selectors (U+FE00-U+FE0F for bytes 0-15,
 * U+E0100-U+E01EF for bytes 16-255). The marker appears as just an emoji followed by invisible characters.
 * 
 * @param options - Configuration options
 * @param options.marker - Marker/prefix before encoded data (default: '🥜')
 * 
 * @example
 * ```tsx
 * const { encode, decode } = useEmojiEncoding({ marker: '🔐' });
 * const encoded = encode('secret data');
 * const decoded = decode(encoded);
 * ```
 */
export function useEmojiEncoding(options: EmojiEncodingOptions = {}) {
  const { marker = '🥜' } = options;

  const byteToVariationSelector = useCallback((byteValue: number): string => {
    if (byteValue >= 0 && byteValue <= 15) {
      return String.fromCodePoint(0xfe00 + byteValue);
    }
    if (byteValue >= 16 && byteValue <= 255) {
      return String.fromCodePoint(0xe0100 + (byteValue - 16));
    }
    return '';
  }, []);

  const variationSelectorToByte = useCallback((char: string): number | null => {
    const codePoint = char.codePointAt(0);
    if (codePoint === undefined) return null;

    if (codePoint >= 0xfe00 && codePoint <= 0xfe0f) {
      return codePoint - 0xfe00;
    }
    if (codePoint >= 0xe0100 && codePoint <= 0xe01ef) {
      return codePoint - 0xe0100 + 16;
    }
    return null;
  }, []);

  const encode = useCallback((data: string): string => {
    const bytes = new TextEncoder().encode(data);
    return (
      marker +
      Array.from(bytes)
        .map((byte) => byteToVariationSelector(byte))
        .join('')
    );
  }, [marker, byteToVariationSelector]);

  const decode = useCallback((encoded: string): string | undefined => {
    try {
      const decoded: number[] = [];
      for (const char of Array.from(encoded)) {
        const byteValue = variationSelectorToByte(char);
        if (byteValue === null && decoded.length > 0) break;
        if (byteValue === null) continue;
        decoded.push(byteValue);
      }
      
      if (decoded.length === 0) return undefined;
      
      const decodedArray = new Uint8Array(decoded);
      return new TextDecoder().decode(decodedArray);
    } catch (error) {
      console.error('Failed to decode emoji-encoded data:', error);
      return undefined;
    }
  }, [variationSelectorToByte]);

  const isEncoded = useCallback((text: string): boolean => {
    if (marker && !text.includes(marker)) return false;
    const decoded = decode(text);
    return decoded !== undefined && decoded.length > 0;
  }, [marker, decode]);

  return {
    encode,
    decode,
    isEncoded,
  };
}
```

**Usage:**
```typescript
function MyComponent() {
  const { encode, decode, isEncoded } = useEmojiEncoding({ marker: '🔐' });
  
  const handleEncode = () => {
    const encoded = encode('secret message');
    console.log(encoded); // "🔐" + invisible characters
  };
  
  const handleDecode = () => {
    const decoded = decode(encodedText);
    console.log(decoded); // "secret message"
  };
  
  const checkIfEncoded = () => {
    if (isEncoded(someText)) {
      console.log('Text contains encoded data!');
    }
  };
}
```

## Part 3: UI Components

### Emoji Selector Component

```typescript
// components/EmojiSelector.tsx
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface EmojiSelectorProps {
  emojiList: string[];
  selectedEmoji: string;
  onEmojiSelect: (emoji: string) => void;
  disabled?: boolean;
}

export function EmojiSelector({
  emojiList,
  selectedEmoji,
  onEmojiSelect,
  disabled = false,
}: EmojiSelectorProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {emojiList.map((emoji) => (
        <Button
          key={emoji}
          variant={selectedEmoji === emoji ? 'default' : 'outline'}
          size="icon"
          onClick={() => onEmojiSelect(emoji)}
          disabled={disabled}
          className={cn(
            'text-xl',
            selectedEmoji === emoji && 'ring-2 ring-primary'
          )}
        >
          {emoji}
        </Button>
      ))}
    </div>
  );
}
```

### Encoder/Decoder Component

```typescript
// components/EncoderDecoder.tsx
"use client"

import { useEffect, useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { CardContent } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Copy, Check } from "lucide-react";
import { encode, decode } from "@/lib/encoding";
import { EmojiSelector } from "@/components/EmojiSelector";
// Optional: Provide suggested markers, but users can use ANY Unicode character
import { SUGGESTED_MARKERS } from "@/lib/markers";

export function EncoderDecoder() {
  const [mode, setMode] = useState<'encode' | 'decode'>('encode');
  const [inputText, setInputText] = useState("");
  const [selectedMarker, setSelectedMarker] = useState("🥜");
  const [outputText, setOutputText] = useState("");
  const [errorText, setErrorText] = useState("");
  const [copied, setCopied] = useState(false);

  // Convert input whenever it changes
  useEffect(() => {
    try {
      if (mode === 'encode') {
        const output = encode(selectedMarker, inputText);
        setOutputText(output);
        setErrorText("");
      } else {
        const output = decode(inputText);
        setOutputText(output);
        setErrorText("");
      }
    } catch (e) {
      setOutputText("");
      setErrorText(`Error ${mode === "encode" ? "encoding" : "decoding"}: ${e instanceof Error ? e.message : 'Invalid input'}`);
    }
  }, [mode, selectedMarker, inputText]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(outputText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <CardContent className="space-y-4">
      <p className="text-sm text-muted-foreground">
        This tool allows you to encode a hidden message into any Unicode character (emoji, letter, symbol, etc.). 
        You can copy and paste text with a hidden message in it to decode the message.
      </p>

      <div className="flex items-center justify-center space-x-2">
        <Label htmlFor="mode-toggle">Decode</Label>
        <Switch 
          id="mode-toggle" 
          checked={mode === 'encode'} 
          onCheckedChange={(checked) => {
            setMode(checked ? 'encode' : 'decode');
            setInputText("");
          }} 
        />
        <Label htmlFor="mode-toggle">Encode</Label>
      </div>

      <div className="space-y-2">
        <Label htmlFor="input">
          {mode === 'encode' ? 'Enter text to encode' : 'Paste encoded text to decode'}
        </Label>
        <Textarea
          id="input"
          placeholder={mode === 'encode' ? "Enter text to encode" : "Paste an emoji/character to decode"}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          className="min-h-[100px] font-mono"
        />
      </div>

      {mode === 'encode' && (
        <>
          <div className="space-y-2">
            <Label htmlFor="marker-input">
              Marker character (any Unicode character works)
            </Label>
            <div className="flex gap-2">
              <input
                id="marker-input"
                type="text"
                value={selectedMarker}
                onChange={(e) => setSelectedMarker(e.target.value || '🥜')}
                placeholder="Enter any character"
                className="flex-1 px-3 py-2 border rounded-md"
                maxLength={1}
              />
            </div>
            <p className="text-xs text-muted-foreground">
              You can use any Unicode character: emojis, letters, numbers, symbols, etc.
            </p>
          </div>

          {/* Optional: Show suggested markers for convenience */}
          <div className="space-y-2">
            <Label>Or pick from suggested markers</Label>
            <EmojiSelector
              onEmojiSelect={setSelectedMarker}
              selectedEmoji={selectedMarker}
              emojiList={SUGGESTED_MARKERS}
            />
          </div>
        </>
      )}

      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label htmlFor="output">
            {mode === 'encode' ? 'Encoded output' : 'Decoded output'}
          </Label>
          {outputText && (
            <Button
              onClick={handleCopy}
              size="sm"
              variant="ghost"
              className="h-8"
            >
              {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
            </Button>
          )}
        </div>
        <Textarea
          id="output"
          placeholder={`${mode === "encode" ? "Encoded" : "Decoded"} output`}
          value={outputText}
          readOnly
          className="min-h-[100px] font-mono"
        />
      </div>

      {errorText && (
        <div className="text-sm text-destructive text-center p-2 bg-destructive/10 rounded">
          {errorText}
        </div>
      )}
    </CardContent>
  );
}
```

## Part 4: Marker Characters

**CRITICAL: Any Unicode Character Can Be Used as a Marker**

The marker character can be **any Unicode character** - emojis, letters, numbers, symbols, punctuation, or any other Unicode character. There are no restrictions on which character you use as a marker.

**Examples of valid markers:**
- Emojis: `🥜`, `🔐`, `😀`, `🚀`
- Letters: `a`, `Z`, `α`, `Ω`
- Numbers: `1`, `0`, `π`, `∞`
- Symbols: `!`, `@`, `#`, `$`, `%`, `&`, `*`
- Punctuation: `.`, `,`, `;`, `:`, `?`, `!`
- Any other Unicode character

**Implementation:**
```typescript
// You can use any character as a marker
const encoded1 = encode('🥜', 'secret message');  // Emoji marker
const encoded2 = encode('a', 'secret message');  // Letter marker
const encoded3 = encode('!', 'secret message');  // Symbol marker
const encoded4 = encode('π', 'secret message');  // Greek letter marker
const encoded5 = encode('∞', 'secret message');  // Mathematical symbol marker

// All of these work perfectly - choose whatever marker fits your use case
```

**Why this matters:**
- No need to restrict users to predefined lists
- Choose markers that fit your application's context
- Use different markers for different purposes or users
- Support any character your users might want to use

## Part 5: Detection and Validation

### isEncoded Function

```typescript
export function isEncoded(text: string, marker?: string): boolean {
  // If marker specified, check for its presence
  if (marker && !text.includes(marker)) {
    return false;
  }
  
  try {
    const decoded = decode(text);
    return decoded !== undefined && decoded.length > 0;
  } catch {
    return false;
  }
}
```

**Usage:**
```typescript
if (isEncoded(someText, '🥜')) {
  console.log('Text contains encoded data with peanut marker');
}
```

### Validation Helper

```typescript
export function validateEncoded(text: string, marker?: string): {
  isValid: boolean;
  error?: string;
} {
  if (!text || text.length === 0) {
    return { isValid: false, error: 'Text is empty' };
  }
  
  if (marker && !text.startsWith(marker)) {
    return { isValid: false, error: `Text does not start with marker: ${marker}` };
  }
  
  try {
    const decoded = decode(text);
    if (!decoded || decoded.length === 0) {
      return { isValid: false, error: 'No encoded data found' };
    }
    return { isValid: true };
  } catch (error) {
    return { 
      isValid: false, 
      error: error instanceof Error ? error.message : 'Decoding failed' 
    };
  }
}
```

## Part 6: Testing

### Unit Tests

```typescript
import { describe, test, expect } from 'vitest';
import { encode, decode, toVariationSelector, fromVariationSelector } from './encoding';
import { EMOJI_LIST, ALPHABET_LIST } from './emoji';

describe('emoji encoder/decoder', () => {
  test('should correctly encode and decode strings', () => {
    const testStrings = [
      'Hello, World!',
      'Testing 123',
      'Special chars: !@#$%^&*()',
      'Unicode: 你好，世界',
      '',  // empty string
      ' ', // space only
      'Multi\nline\ntext',
      'JSON: {"key": "value"}',
    ];

    for (const marker of [...EMOJI_LIST, ...ALPHABET_LIST]) {
      for (const str of testStrings) {
        const encoded = encode(marker, str);
        const decoded = decode(encoded);

        // Ensure decoding returns the original string
        expect(decoded).toBe(str);

        // Ensure encoded string starts with marker
        expect(encoded.startsWith(marker)).toBe(true);
      }
    }
  });

  test('toVariationSelector should map bytes correctly', () => {
    // Test bytes 0-15
    for (let i = 0; i < 16; i++) {
      const selector = toVariationSelector(i);
      expect(selector).not.toBeNull();
      expect(selector?.codePointAt(0)).toBe(0xfe00 + i);
    }

    // Test bytes 16-255
    for (let i = 16; i < 256; i++) {
      const selector = toVariationSelector(i);
      expect(selector).not.toBeNull();
      expect(selector?.codePointAt(0)).toBe(0xe0100 + (i - 16));
    }

    // Test invalid byte
    expect(toVariationSelector(256)).toBeNull();
    expect(toVariationSelector(-1)).toBeNull();
  });

  test('fromVariationSelector should reverse mapping correctly', () => {
    // Test variation selectors 0xFE00-0xFE0F
    for (let i = 0; i < 16; i++) {
      const byte = fromVariationSelector(0xfe00 + i);
      expect(byte).toBe(i);
    }

    // Test variation selectors supplement 0xE0100-0xE01EF
    for (let i = 16; i < 256; i++) {
      const byte = fromVariationSelector(0xe0100 + (i - 16));
      expect(byte).toBe(i);
    }

    // Test invalid code points
    expect(fromVariationSelector(0xfdfe)).toBeNull();
    expect(fromVariationSelector(0xe01f0)).toBeNull();
  });

  test('should handle empty string encoding', () => {
    const encoded = encode('🥜', '');
    expect(encoded).toBe('🥜');
    
    const decoded = decode(encoded);
    expect(decoded).toBe('');
  });

  test('should handle very long strings', () => {
    const longString = 'A'.repeat(10000);
    const encoded = encode('🥜', longString);
    const decoded = decode(encoded);
    expect(decoded).toBe(longString);
  });

  test('should handle binary data', () => {
    // Create binary-like string
    const binaryString = String.fromCharCode(...Array.from({ length: 256 }, (_, i) => i));
    const encoded = encode('🥜', binaryString);
    const decoded = decode(encoded);
    expect(decoded).toBe(binaryString);
  });
});
```

## Part 7: Common Pitfalls

### 1. ❌ Not handling UTF-8 correctly

**Problem:** Using `charCodeAt()` instead of `TextEncoder`/`TextDecoder` breaks Unicode characters.

**Solution:** Always use `TextEncoder`/`TextDecoder`:
```typescript
// ❌ Wrong
const bytes = Array.from(text).map(c => c.charCodeAt(0));

// ✅ Correct
const bytes = new TextEncoder().encode(text);
```

### 2. ❌ Not using `codePointAt()` for multi-byte characters

**Problem:** Using `charCodeAt()` doesn't handle Unicode characters outside the Basic Multilingual Plane.

**Solution:** Use `codePointAt()`:
```typescript
// ❌ Wrong
const codePoint = char.charCodeAt(0);

// ✅ Correct
const codePoint = char.codePointAt(0);
```

### 3. ❌ Not handling empty strings

**Problem:** Empty string encoding/decoding can cause errors.

**Solution:** Handle empty strings explicitly:
```typescript
export function encode(marker: string, text: string): string {
  if (text === '') {
    return marker;
  }
  // ... rest of encoding
}

export function decode(text: string): string {
  // Skip marker, check if any variation selectors exist
  const chars = Array.from(text);
  let hasVariationSelectors = false;
  // ... check for variation selectors
  if (!hasVariationSelectors) {
    return '';
  }
  // ... rest of decoding
}
```

### 4. ❌ Not stopping at first non-variation-selector

**Problem:** Decoding continues through regular text after encoded data.

**Solution:** Stop decoding at first non-variation-selector:
```typescript
for (const char of chars) {
  const byte = fromVariationSelector(char.codePointAt(0)!);
  if (byte === null && decoded.length > 0) {
    break; // Stop at first non-variation-selector
  }
  // ... continue decoding
}
```

### 5. ❌ Copying encoded text loses invisible characters

**Problem:** Some applications strip invisible Unicode characters when copying.

**Solution:** 
- Use `navigator.clipboard.writeText()` for reliable copying
- Warn users that some apps may strip invisible characters
- Provide alternative sharing methods (QR code, direct link)

### 6. ❌ Not validating before decoding

**Problem:** Decoding invalid text causes errors.

**Solution:** Validate before decoding:
```typescript
try {
  const decoded = decode(text);
  if (!decoded || decoded.length === 0) {
    throw new Error('No encoded data found');
  }
  return decoded;
} catch (error) {
  console.error('Decoding failed:', error);
  return undefined;
}
```

## Part 8: Advanced Usage

### Custom Marker Detection

```typescript
export function detectMarker(text: string): string | null {
  const chars = Array.from(text);
  if (chars.length === 0) return null;
  
  // First character is likely the marker
  const firstChar = chars[0];
  
  // Check if rest are variation selectors
  let hasVariationSelectors = false;
  for (let i = 1; i < chars.length; i++) {
    const codePoint = chars[i].codePointAt(0);
    if (codePoint === undefined) continue;
    
    if (
      (codePoint >= 0xfe00 && codePoint <= 0xfe0f) ||
      (codePoint >= 0xe0100 && codePoint <= 0xe01ef)
    ) {
      hasVariationSelectors = true;
      break;
    }
  }
  
  return hasVariationSelectors ? firstChar : null;
}
```

### Batch Encoding/Decoding

```typescript
export function encodeBatch(marker: string, texts: string[]): string[] {
  return texts.map(text => encode(marker, text));
}

export function decodeBatch(encodedTexts: string[]): string[] {
  return encodedTexts.map(text => {
    try {
      return decode(text);
    } catch {
      return '';
    }
  });
}
```

### URL-Safe Encoding

```typescript
export function encodeToUrl(marker: string, text: string): string {
  const encoded = encode(marker, text);
  return encodeURIComponent(encoded);
}

export function decodeFromUrl(encodedUrl: string): string {
  try {
    const decoded = decodeURIComponent(encodedUrl);
    return decode(decoded);
  } catch {
    throw new Error('Invalid URL-encoded data');
  }
}
```

## Security Considerations

1. **Steganography, not encryption** - This is steganography (hiding data), not encryption (securing data). The encoded data can be decoded by anyone who knows the technique.

2. **Invisible characters** - Some applications may strip invisible Unicode characters. Test in your target applications.

3. **Character limits** - Some platforms have character limits that may truncate encoded messages.

4. **Copy/paste reliability** - Not all applications preserve invisible characters when copying. Test thoroughly.

5. **Detection** - Encoded text can be detected by checking for variation selectors. This is not secure against determined adversaries.

## Use Cases

### 1. Steganographic Messaging
Hide messages in plain sight using emojis or letters as markers.

### 2. Watermarking
Embed metadata invisibly in text content.

### 3. Cashu Token Encoding
Encode Cashu tokens into emojis for easy sharing (peanut emoji marker).

### 4. Nostr Integration
Encode Nostr event IDs or other data invisibly in messages.

### 5. QR Code Alternative
Encode data into text that can be copied/pasted instead of QR codes.

## Verification Checklist

- [ ] Encoding/decoding works for all UTF-8 characters
- [ ] Empty strings handled correctly
- [ ] Very long strings handled correctly
- [ ] Binary data handled correctly
- [ ] Multiple markers work correctly
- [ ] Detection function works correctly
- [ ] Error handling is graceful
- [ ] React hooks work correctly
- [ ] UI components are accessible
- [ ] Copy-to-clipboard works reliably
- [ ] Tests cover edge cases

## Summary

To implement emoji encoding:

1. **Core functions** - Implement `encode()` and `decode()` using Unicode Variation Selectors
2. **React hooks** - Create `useEmojiEncoding()` hook for easy integration
3. **UI components** - Build encoder/decoder interface with emoji/character selector
4. **Detection** - Add `isEncoded()` function to detect encoded text
5. **Error handling** - Validate inputs and handle errors gracefully
6. **Testing** - Test with various text types, Unicode characters, and edge cases

**Key principle:** Use Unicode Variation Selectors (U+FE00-U+FE0F and U+E0100-U+E01EF) to invisibly encode UTF-8 bytes, making any character (emoji, letter, symbol) a potential marker for steganographic encoding.

