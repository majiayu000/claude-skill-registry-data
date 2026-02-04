---
name: lsb-steganography
description: Use when implementing Least Significant Bit (LSB) steganography - allows hiding images or text within other images by encoding data in the least significant bits of pixel color channels
when_to_use: When adding steganographic image encoding, hiding images within images, encoding text into images, implementing invisible data storage in images, or building privacy-preserving image sharing features
---

# LSB Steganography Implementation

## Overview

Complete implementation guide for Least Significant Bit (LSB) steganography - a technique for hiding images or text within other images by encoding data in the least significant bits of pixel color channels. The hidden data is imperceptible to the human eye while remaining fully recoverable.

**Core Capabilities:**
- Hide images within other images using LSB encoding
- Encode text messages into images
- Decode hidden images or text from steganographic images
- Resize and pad images to match target dimensions
- Configurable number of bits per channel (1-8 bits)
- Zero-dependency core implementation (uses Canvas API)
- React hooks for easy integration
- Complete UI components for encoding/decoding

## How It Works

LSB steganography works by replacing the least significant bits of pixel color channels with data bits:

- **Image-to-Image**: Takes the most significant bits from a source image and embeds them into the least significant bits of a carrier image
- **Text-to-Image**: Converts text to binary and embeds it into the least significant bits of an image
- **Decoding**: Extracts the least significant bits and reconstructs the hidden data

**Key Concepts:**
- **n_bits**: Number of least significant bits to use (typically 1-4 for imperceptibility)
- **Color Channels**: RGB channels (Red, Green, Blue) each store 8 bits (0-255)
- **Capacity**: `width × height × 3 × n_bits` bits can be stored in an image

**Example:**
```
Carrier Image: 1000×1000 pixels
n_bits: 2
Capacity: 1000 × 1000 × 3 × 2 = 6,000,000 bits = 750 KB
```

## Prerequisites

**Browser-Native Implementation:**
This implementation uses **only native browser APIs** - no Node.js or external packages required for the core functionality.

**Required Browser APIs:**
- **Canvas API** - Native browser API for image manipulation (`HTMLCanvasElement`, `CanvasRenderingContext2D`)
- **File API** - Native browser API for file handling (`File`, `Blob`, `URL.createObjectURL`)
- **TextEncoder/TextDecoder** - Native browser APIs for UTF-8 encoding/decoding

**Optional dependencies:**
- `react` and `react-dom` for React hooks and components
- Optional user feedback (console.log, toast notifications, or silent)

**Browser Support:**
- Modern browsers with Canvas API support (Chrome, Firefox, Safari, Edge)
- FileReader API for image loading
- No build tools or transpilation required - works directly in the browser

**Note:** This implementation is designed for browser environments. For Node.js server-side use, you would need to adapt the code to use the `canvas` npm package, but the default implementation is 100% browser-native.

## Implementation Checklist

- [ ] Implement core bit manipulation functions
- [ ] Implement image-to-image encoding/decoding
- [ ] Implement text-to-image encoding/decoding
- [ ] Add image resizing and padding utilities
- [ ] Create React hooks for encoding/decoding
- [ ] Add UI components for image upload and display
- [ ] Implement error handling and validation
- [ ] Add capacity calculation utilities
- [ ] Create tests for encoding/decoding

## Part 1: Core Bit Manipulation Functions

### Constants

```typescript
// lib/lsbSteganography.ts
const MAX_COLOR_VALUE = 256;
const MAX_BIT_VALUE = 8;
```

### Remove N Least Significant Bits

```typescript
/**
 * Removes the n least significant bits from a color value.
 * Used to clear space for embedding data.
 * 
 * @param value - Color channel value (0-255)
 * @param n - Number of bits to remove (1-8)
 * @returns Value with n least significant bits set to 0
 */
export function removeNLeastSignificantBits(value: number, n: number): number {
  value = value >> n;
  return value << n;
}
```

**How it works:**
- Right shift by n bits (removes least significant bits)
- Left shift by n bits (restores position, zeros fill least significant bits)
- Example: `removeNLeastSignificantBits(107, 2)` → `104` (binary: `01101000`)

### Get N Least Significant Bits

```typescript
/**
 * Extracts the n least significant bits from a color value.
 * Used to retrieve embedded data.
 * 
 * @param value - Color channel value (0-255)
 * @param n - Number of bits to extract (1-8)
 * @returns The n least significant bits (0 to 2^n - 1)
 */
export function getNLeastSignificantBits(value: number, n: number): number {
  value = value << (MAX_BIT_VALUE - n);
  value = value % MAX_COLOR_VALUE;
  return value >> (MAX_BIT_VALUE - n);
}
```

**How it works:**
- Left shift to move bits to most significant position
- Modulo to keep within 8-bit range
- Right shift to move back to least significant position
- Example: `getNLeastSignificantBits(107, 2)` → `3` (binary: `11`)

### Get N Most Significant Bits

```typescript
/**
 * Extracts the n most significant bits from a color value.
 * Used to get the important bits from source images.
 * 
 * @param value - Color channel value (0-255)
 * @param n - Number of bits to extract (1-8)
 * @returns The n most significant bits (0 to 2^n - 1)
 */
export function getNMostSignificantBits(value: number, n: number): number {
  return value >> (MAX_BIT_VALUE - n);
}
```

**How it works:**
- Right shift to move most significant bits to least significant position
- Example: `getNMostSignificantBits(107, 2)` → `1` (binary: `01`)

### Shift N Bits to 8 Bits

```typescript
/**
 * Shifts n bits to fill an 8-bit value.
 * Used when reconstructing color values from extracted bits.
 * 
 * @param value - Bit value (0 to 2^n - 1)
 * @param n - Original number of bits
 * @returns Value shifted to 8-bit position
 */
export function shiftNBitsTo8(value: number, n: number): number {
  return value << (MAX_BIT_VALUE - n);
}
```

**How it works:**
- Left shift to move bits to most significant position
- Example: `shiftNBitsTo8(3, 2)` → `192` (binary: `11000000`)

## Part 2: Image-to-Image Encoding

### Load Image to Canvas

```typescript
/**
 * Loads an image file and returns a canvas element.
 * 
 * @param file - Image file (File or Blob)
 * @returns Promise resolving to HTMLCanvasElement
 */
export async function loadImageToCanvas(file: File | Blob): Promise<HTMLCanvasElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const url = URL.createObjectURL(file);
    
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      if (!ctx) {
        reject(new Error('Failed to get canvas context'));
        return;
      }
      ctx.drawImage(img, 0, 0);
      URL.revokeObjectURL(url);
      resolve(canvas);
    };
    
    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error('Failed to load image'));
    };
    
    img.src = url;
  });
}
```

### Get Image Data

```typescript
/**
 * Extracts pixel data from a canvas as RGB tuples.
 * 
 * @param canvas - Canvas element
 * @returns Array of [r, g, b] tuples
 */
export function getImageData(canvas: HTMLCanvasElement): [number, number, number][] {
  const ctx = canvas.getContext('2d');
  if (!ctx) {
    throw new Error('Failed to get canvas context');
  }
  
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const data = imageData.data;
  const pixels: [number, number, number][] = [];
  
  for (let i = 0; i < data.length; i += 4) {
    pixels.push([data[i], data[i + 1], data[i + 2]]);
  }
  
  return pixels;
}
```

### Create Image from Data

```typescript
/**
 * Creates a canvas from pixel data.
 * 
 * @param data - Array of [r, g, b] tuples
 * @param width - Image width
 * @param height - Image height
 * @returns Canvas element
 */
export function createImageFromData(
  data: [number, number, number][],
  width: number,
  height: number
): HTMLCanvasElement {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');
  if (!ctx) {
    throw new Error('Failed to get canvas context');
  }
  
  const imageData = ctx.createImageData(width, height);
  const pixels = imageData.data;
  
  for (let i = 0; i < data.length; i++) {
    const [r, g, b] = data[i];
    const idx = i * 4;
    pixels[idx] = r;
    pixels[idx + 1] = g;
    pixels[idx + 2] = b;
    pixels[idx + 3] = 255; // Alpha
  }
  
  ctx.putImageData(imageData, 0, 0);
  return canvas;
}
```

### LSB Encode (Image-to-Image)

```typescript
/**
 * Encodes a source image into a carrier image using LSB steganography.
 * 
 * @param imageToHide - Canvas of image to hide
 * @param imageToHideIn - Canvas of carrier image
 * @param nBits - Number of least significant bits to use (1-8)
 * @returns Canvas with encoded image
 */
export async function lsbEncode(
  imageToHide: HTMLCanvasElement,
  imageToHideIn: HTMLCanvasElement,
  nBits: number
): Promise<HTMLCanvasElement> {
  const width = imageToHide.width;
  const height = imageToHide.height;
  
  // Check if carrier image is large enough
  if (imageToHideIn.width < width || imageToHideIn.height < height) {
    throw new Error('Carrier image must be at least as large as image to hide');
  }
  
  const hidePixels = getImageData(imageToHide);
  const hideInPixels = getImageData(imageToHideIn);
  
  const encodedPixels: [number, number, number][] = [];
  
  for (let i = 0; i < hidePixels.length; i++) {
    const [rHide, gHide, bHide] = hidePixels[i];
    const [rHideIn, gHideIn, bHideIn] = hideInPixels[i];
    
    // Get most significant bits from image to hide
    const rHideMSB = getNMostSignificantBits(rHide, nBits);
    const gHideMSB = getNMostSignificantBits(gHide, nBits);
    const bHideMSB = getNMostSignificantBits(bHide, nBits);
    
    // Remove least significant bits from carrier image
    const rHideInLSB = removeNLeastSignificantBits(rHideIn, nBits);
    const gHideInLSB = removeNLeastSignificantBits(gHideIn, nBits);
    const bHideInLSB = removeNLeastSignificantBits(bHideIn, nBits);
    
    // Combine: carrier image (with cleared LSB) + hidden image (MSB)
    encodedPixels.push([
      rHideMSB + rHideInLSB,
      gHideMSB + gHideInLSB,
      bHideMSB + bHideInLSB
    ]);
  }
  
  return createImageFromData(encodedPixels, width, height);
}
```

**Key points:**
- Source image's most significant bits are embedded into carrier's least significant bits
- Carrier image must be at least as large as source image
- Resulting image looks nearly identical to carrier image

### LSB Decode (Image-to-Image)

```typescript
/**
 * Decodes a hidden image from an encoded image.
 * 
 * @param encodedCanvas - Canvas with encoded image
 * @param nBits - Number of least significant bits used (1-8)
 * @returns Canvas with decoded hidden image
 */
export function lsbDecode(
  encodedCanvas: HTMLCanvasElement,
  nBits: number
): HTMLCanvasElement {
  const width = encodedCanvas.width;
  const height = encodedCanvas.height;
  const encodedPixels = getImageData(encodedCanvas);
  
  const decodedPixels: [number, number, number][] = [];
  
  for (const [rEncoded, gEncoded, bEncoded] of encodedPixels) {
    // Extract least significant bits
    const rLSB = getNLeastSignificantBits(rEncoded, nBits);
    const gLSB = getNLeastSignificantBits(gEncoded, nBits);
    const bLSB = getNLeastSignificantBits(bEncoded, nBits);
    
    // Shift bits to 8-bit position to reconstruct color
    const r = shiftNBitsTo8(rLSB, nBits);
    const g = shiftNBitsTo8(gLSB, nBits);
    const b = shiftNBitsTo8(bLSB, nBits);
    
    decodedPixels.push([r, g, b]);
  }
  
  return createImageFromData(decodedPixels, width, height);
}
```

## Part 3: Text-to-Image Encoding

### Text to Binary

```typescript
/**
 * Converts text to binary representation.
 * 
 * @param text - Text to convert
 * @returns Binary string (padded to multiple of 8)
 */
export function textToBinary(text: string): string {
  const bytes = new TextEncoder().encode(text);
  let binary = '';
  for (const byte of bytes) {
    binary += byte.toString(2).padStart(8, '0');
  }
  return binary;
}
```

**How it works:**
- Uses `TextEncoder` to convert string to UTF-8 bytes
- Each byte converted to 8-bit binary string
- Handles all Unicode characters correctly

### Binary to Text

```typescript
/**
 * Converts binary representation back to text.
 * 
 * @param binary - Binary string (multiple of 8)
 * @returns Decoded text
 */
export function binaryToText(binary: string): string {
  const bytes: number[] = [];
  for (let i = 0; i < binary.length; i += 8) {
    const byte = parseInt(binary.substr(i, 8), 2);
    bytes.push(byte);
  }
  return new TextDecoder().decode(new Uint8Array(bytes));
}
```

### Encode Text in Image

```typescript
/**
 * Encodes text into an image using LSB steganography.
 * 
 * @param canvas - Canvas of carrier image
 * @param text - Text to hide
 * @param nBits - Number of least significant bits to use (1-8)
 * @returns Canvas with encoded text
 */
export function encodeTextInImage(
  canvas: HTMLCanvasElement,
  text: string,
  nBits: number = 2
): HTMLCanvasElement {
  const width = canvas.width;
  const height = canvas.height;
  const pixels = getImageData(canvas);
  
  // Convert text to binary
  const binaryText = textToBinary(text);
  
  // Add 32-bit length prefix (to know how much to decode)
  const lengthPrefix = binaryText.length.toString(2).padStart(32, '0');
  const fullBinary = lengthPrefix + binaryText;
  
  // Check capacity
  const maxBits = width * height * 3 * nBits;
  if (fullBinary.length > maxBits) {
    throw new Error(
      `Text is too long. Maximum ${maxBits} bits can be hidden (${Math.floor(maxBits / 8)} bytes).`
    );
  }
  
  // Encode binary into image
  let binaryIndex = 0;
  const encodedPixels: [number, number, number][] = [];
  
  for (let i = 0; i < pixels.length; i++) {
    const [r, g, b] = pixels[i];
    let rModified = r;
    let gModified = g;
    let bModified = b;
    
    // Red channel
    if (binaryIndex < fullBinary.length) {
      const bits = fullBinary.substr(binaryIndex, nBits);
      const bitValue = parseInt(bits.padEnd(nBits, '0'), 2);
      rModified = (r & ~((1 << nBits) - 1)) | bitValue;
      binaryIndex += nBits;
    }
    
    // Green channel
    if (binaryIndex < fullBinary.length) {
      const bits = fullBinary.substr(binaryIndex, nBits);
      const bitValue = parseInt(bits.padEnd(nBits, '0'), 2);
      gModified = (g & ~((1 << nBits) - 1)) | bitValue;
      binaryIndex += nBits;
    }
    
    // Blue channel
    if (binaryIndex < fullBinary.length) {
      const bits = fullBinary.substr(binaryIndex, nBits);
      const bitValue = parseInt(bits.padEnd(nBits, '0'), 2);
      bModified = (b & ~((1 << nBits) - 1)) | bitValue;
      binaryIndex += nBits;
    }
    
    encodedPixels.push([rModified, gModified, bModified]);
    
    if (binaryIndex >= fullBinary.length) {
      // Fill remaining pixels with original values
      for (let j = i + 1; j < pixels.length; j++) {
        encodedPixels.push(pixels[j]);
      }
      break;
    }
  }
  
  return createImageFromData(encodedPixels, width, height);
}
```

**Key points:**
- 32-bit length prefix stores text length for decoding
- Text encoded across RGB channels sequentially
- Capacity: `width × height × 3 × nBits` bits

### Decode Text from Image

```typescript
/**
 * Decodes hidden text from an image.
 * 
 * @param canvas - Canvas with encoded text
 * @param nBits - Number of least significant bits used (1-8)
 * @returns Decoded text
 */
export function decodeTextFromImage(
  canvas: HTMLCanvasElement,
  nBits: number = 2
): string {
  const pixels = getImageData(canvas);
  let binaryText = '';
  let bitCount = 0;
  let textLength: number | null = null;
  
  for (const [r, g, b] of pixels) {
    // Extract bits from each channel
    const rBits = r & ((1 << nBits) - 1);
    binaryText += rBits.toString(2).padStart(nBits, '0');
    bitCount += nBits;
    
    // Read length prefix (first 32 bits)
    if (textLength === null && bitCount >= 32) {
      textLength = parseInt(binaryText.substr(0, 32), 2);
      binaryText = binaryText.substr(32);
      bitCount -= 32;
    }
    
    if (textLength !== null && bitCount >= textLength) {
      break;
    }
    
    const gBits = g & ((1 << nBits) - 1);
    binaryText += gBits.toString(2).padStart(nBits, '0');
    bitCount += nBits;
    
    if (textLength !== null && bitCount >= textLength) {
      break;
    }
    
    const bBits = b & ((1 << nBits) - 1);
    binaryText += bBits.toString(2).padStart(nBits, '0');
    bitCount += nBits;
    
    if (textLength !== null && bitCount >= textLength) {
      break;
    }
  }
  
  // Trim to exact length and convert to text
  if (textLength === null) {
    throw new Error('Failed to decode text length');
  }
  
  const textBinary = binaryText.substr(0, textLength);
  return binaryToText(textBinary);
}
```

## Part 4: Image Utilities

### Resize and Pad Image

```typescript
/**
 * Resizes an image while maintaining aspect ratio and adds padding to match target size.
 * 
 * @param canvas - Source canvas
 * @param targetWidth - Target width
 * @param targetHeight - Target height
 * @param backgroundColor - Background color for padding (default: white)
 * @returns Resized and padded canvas
 */
export function resizeAndPadImage(
  canvas: HTMLCanvasElement,
  targetWidth: number,
  targetHeight: number,
  backgroundColor: string = '#FFFFFF'
): HTMLCanvasElement {
  // Calculate scaling to fit within target size while maintaining aspect ratio
  const scale = Math.min(targetWidth / canvas.width, targetHeight / canvas.height);
  const scaledWidth = Math.floor(canvas.width * scale);
  const scaledHeight = Math.floor(canvas.height * scale);
  
  // Create temporary canvas for resized image
  const tempCanvas = document.createElement('canvas');
  tempCanvas.width = scaledWidth;
  tempCanvas.height = scaledHeight;
  const tempCtx = tempCanvas.getContext('2d');
  if (!tempCtx) {
    throw new Error('Failed to get canvas context');
  }
  
  // Draw resized image
  tempCtx.drawImage(canvas, 0, 0, scaledWidth, scaledHeight);
  
  // Create final canvas with target size
  const finalCanvas = document.createElement('canvas');
  finalCanvas.width = targetWidth;
  finalCanvas.height = targetHeight;
  const finalCtx = finalCanvas.getContext('2d');
  if (!finalCtx) {
    throw new Error('Failed to get canvas context');
  }
  
  // Fill with background color
  finalCtx.fillStyle = backgroundColor;
  finalCtx.fillRect(0, 0, targetWidth, targetHeight);
  
  // Center the resized image
  const pasteX = (targetWidth - scaledWidth) / 2;
  const pasteY = (targetHeight - scaledHeight) / 2;
  finalCtx.drawImage(tempCanvas, pasteX, pasteY);
  
  return finalCanvas;
}
```

### Canvas to Blob

```typescript
/**
 * Converts a canvas to a Blob.
 * 
 * @param canvas - Canvas element
 * @param mimeType - MIME type (default: 'image/png')
 * @param quality - Quality for JPEG (0-1, default: 0.92)
 * @returns Promise resolving to Blob
 */
export function canvasToBlob(
  canvas: HTMLCanvasElement,
  mimeType: string = 'image/png',
  quality: number = 0.92
): Promise<Blob> {
  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => {
        if (blob) {
          resolve(blob);
        } else {
          reject(new Error('Failed to convert canvas to blob'));
        }
      },
      mimeType,
      quality
    );
  });
}
```

### Calculate Capacity

```typescript
/**
 * Calculates the maximum text capacity for an image.
 * 
 * @param width - Image width
 * @param height - Image height
 * @param nBits - Number of bits per channel (1-8)
 * @returns Maximum capacity in bytes
 */
export function calculateTextCapacity(
  width: number,
  height: number,
  nBits: number
): number {
  // Subtract 32 bits for length prefix
  const totalBits = width * height * 3 * nBits - 32;
  return Math.floor(totalBits / 8);
}
```

## Part 5: React Hooks

### Use LSB Encode (Image-to-Image)

```typescript
// hooks/useLSBEncode.ts
import { useState } from 'react';
import {
  loadImageToCanvas,
  lsbEncode,
  resizeAndPadImage,
  canvasToBlob
} from '@/lib/lsbSteganography';

export function useLSBEncode() {
  const [isEncoding, setIsEncoding] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const encode = async (
    imageToHide: File,
    carrierImage: File,
    nBits: number = 2
  ): Promise<Blob | null> => {
    setIsEncoding(true);
    setError(null);
    
    try {
      // Load images
      const hideCanvas = await loadImageToCanvas(imageToHide);
      const carrierCanvas = await loadImageToCanvas(carrierImage);
      
      // Resize and pad image to hide to match carrier
      const resizedHideCanvas = resizeAndPadImage(
        hideCanvas,
        carrierCanvas.width,
        carrierCanvas.height
      );
      
      // Encode
      const encodedCanvas = await lsbEncode(resizedHideCanvas, carrierCanvas, nBits);
      
      // Convert to blob
      const blob = await canvasToBlob(encodedCanvas);
      
      return blob;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Encoding failed';
      setError(message);
      return null;
    } finally {
      setIsEncoding(false);
    }
  };
  
  return { encode, isEncoding, error };
}
```

### Use LSB Decode (Image-to-Image)

```typescript
// hooks/useLSBDecode.ts
import { useState } from 'react';
import { loadImageToCanvas, lsbDecode, canvasToBlob } from '@/lib/lsbSteganography';

export function useLSBDecode() {
  const [isDecoding, setIsDecoding] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const decode = async (
    encodedImage: File,
    nBits: number = 2
  ): Promise<Blob | null> => {
    setIsDecoding(true);
    setError(null);
    
    try {
      const canvas = await loadImageToCanvas(encodedImage);
      const decodedCanvas = lsbDecode(canvas, nBits);
      const blob = await canvasToBlob(decodedCanvas);
      return blob;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Decoding failed';
      setError(message);
      return null;
    } finally {
      setIsDecoding(false);
    }
  };
  
  return { decode, isDecoding, error };
}
```

### Use Text Encode

```typescript
// hooks/useTextEncode.ts
import { useState } from 'react';
import {
  loadImageToCanvas,
  encodeTextInImage,
  calculateTextCapacity,
  canvasToBlob
} from '@/lib/lsbSteganography';

export function useTextEncode() {
  const [isEncoding, setIsEncoding] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const encode = async (
    carrierImage: File,
    text: string,
    nBits: number = 2
  ): Promise<Blob | null> => {
    setIsEncoding(true);
    setError(null);
    
    try {
      const canvas = await loadImageToCanvas(carrierImage);
      
      // Check capacity
      const capacity = calculateTextCapacity(canvas.width, canvas.height, nBits);
      if (text.length > capacity) {
        throw new Error(
          `Text is too long. Maximum ${capacity} characters can be encoded.`
        );
      }
      
      const encodedCanvas = encodeTextInImage(canvas, text, nBits);
      const blob = await canvasToBlob(encodedCanvas);
      return blob;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Encoding failed';
      setError(message);
      return null;
    } finally {
      setIsEncoding(false);
    }
  };
  
  return { encode, isEncoding, error };
}
```

### Use Text Decode

```typescript
// hooks/useTextDecode.ts
import { useState } from 'react';
import { loadImageToCanvas, decodeTextFromImage } from '@/lib/lsbSteganography';

export function useTextDecode() {
  const [isDecoding, setIsDecoding] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const decode = async (
    encodedImage: File,
    nBits: number = 2
  ): Promise<string | null> => {
    setIsDecoding(true);
    setError(null);
    
    try {
      const canvas = await loadImageToCanvas(encodedImage);
      const text = decodeTextFromImage(canvas, nBits);
      return text;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Decoding failed';
      setError(message);
      return null;
    } finally {
      setIsDecoding(false);
    }
  };
  
  return { decode, isDecoding, error };
}
```

## Part 6: UI Components

### Image-to-Image Encoding Component

```typescript
// components/LSBImageEncoder.tsx
import { useState } from 'react';
import { useLSBEncode } from '@/hooks/useLSBEncode';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export function LSBImageEncoder() {
  const [imageToHide, setImageToHide] = useState<File | null>(null);
  const [carrierImage, setCarrierImage] = useState<File | null>(null);
  const [nBits, setNBits] = useState(2);
  const [encodedImageUrl, setEncodedImageUrl] = useState<string | null>(null);
  const { encode, isEncoding, error } = useLSBEncode();
  
  const handleEncode = async () => {
    if (!imageToHide || !carrierImage) return;
    
    const blob = await encode(imageToHide, carrierImage, nBits);
    if (blob) {
      setEncodedImageUrl(URL.createObjectURL(blob));
    }
  };
  
  const handleDownload = () => {
    if (encodedImageUrl) {
      const a = document.createElement('a');
      a.href = encodedImageUrl;
      a.download = 'encoded-image.png';
      a.click();
    }
  };
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>LSB Image Encoder</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label>Image to Hide</Label>
          <Input
            type="file"
            accept="image/*"
            onChange={(e) => setImageToHide(e.target.files?.[0] || null)}
          />
        </div>
        
        <div className="space-y-2">
          <Label>Carrier Image</Label>
          <Input
            type="file"
            accept="image/*"
            onChange={(e) => setCarrierImage(e.target.files?.[0] || null)}
          />
        </div>
        
        <div className="space-y-2">
          <Label>Bits per Channel (1-8)</Label>
          <Input
            type="number"
            min="1"
            max="8"
            value={nBits}
            onChange={(e) => setNBits(parseInt(e.target.value) || 2)}
          />
        </div>
        
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        
        <Button onClick={handleEncode} disabled={isEncoding || !imageToHide || !carrierImage}>
          {isEncoding ? 'Encoding...' : 'Encode Image'}
        </Button>
        
        {encodedImageUrl && (
          <div className="space-y-2">
            <img src={encodedImageUrl} alt="Encoded" className="max-w-full" />
            <Button onClick={handleDownload}>Download Encoded Image</Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

### Text Encoding Component

```typescript
// components/LSBTextEncoder.tsx
import { useState } from 'react';
import { useTextEncode } from '@/hooks/useTextEncode';
import { calculateTextCapacity } from '@/lib/lsbSteganography';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

export function LSBTextEncoder() {
  const [carrierImage, setCarrierImage] = useState<File | null>(null);
  const [text, setText] = useState('');
  const [nBits, setNBits] = useState(2);
  const [encodedImageUrl, setEncodedImageUrl] = useState<string | null>(null);
  const [capacity, setCapacity] = useState<number | null>(null);
  const { encode, isEncoding, error } = useTextEncode();
  
  const handleImageLoad = async (file: File) => {
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => {
      const cap = calculateTextCapacity(img.width, img.height, nBits);
      setCapacity(cap);
      URL.revokeObjectURL(url);
    };
    img.src = url;
  };
  
  const handleEncode = async () => {
    if (!carrierImage) return;
    
    const blob = await encode(carrierImage, text, nBits);
    if (blob) {
      setEncodedImageUrl(URL.createObjectURL(blob));
    }
  };
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>LSB Text Encoder</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label>Carrier Image</Label>
          <Input
            type="file"
            accept="image/*"
            onChange={(e) => {
              const file = e.target.files?.[0];
              setCarrierImage(file);
              if (file) handleImageLoad(file);
            }}
          />
          {capacity !== null && (
            <p className="text-sm text-muted-foreground">
              Capacity: {capacity} characters
            </p>
          )}
        </div>
        
        <div className="space-y-2">
          <Label>Text to Hide</Label>
          <Textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={5}
          />
          <p className="text-sm text-muted-foreground">
            {text.length} / {capacity || '?'} characters
          </p>
        </div>
        
        <div className="space-y-2">
          <Label>Bits per Channel (1-8)</Label>
          <Input
            type="number"
            min="1"
            max="8"
            value={nBits}
            onChange={(e) => setNBits(parseInt(e.target.value) || 2)}
          />
        </div>
        
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        
        <Button onClick={handleEncode} disabled={isEncoding || !carrierImage || !text}>
          {isEncoding ? 'Encoding...' : 'Encode Text'}
        </Button>
        
        {encodedImageUrl && (
          <div className="space-y-2">
            <img src={encodedImageUrl} alt="Encoded" className="max-w-full" />
            <Button onClick={() => {
              const a = document.createElement('a');
              a.href = encodedImageUrl;
              a.download = 'encoded-text.png';
              a.click();
            }}>Download Encoded Image</Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

## Part 7: Usage Examples

### Basic Image-to-Image Encoding

```typescript
import { loadImageToCanvas, lsbEncode, lsbDecode, canvasToBlob } from '@/lib/lsbSteganography';

// Encode
const hideCanvas = await loadImageToCanvas(hideImageFile);
const carrierCanvas = await loadImageToCanvas(carrierImageFile);
const encodedCanvas = await lsbEncode(hideCanvas, carrierCanvas, 2);
const encodedBlob = await canvasToBlob(encodedCanvas);

// Decode
const encodedCanvas2 = await loadImageToCanvas(encodedBlob);
const decodedCanvas = lsbDecode(encodedCanvas2, 2);
const decodedBlob = await canvasToBlob(decodedCanvas);
```

### Basic Text Encoding

```typescript
import { loadImageToCanvas, encodeTextInImage, decodeTextFromImage } from '@/lib/lsbSteganography';

// Encode text
const carrierCanvas = await loadImageToCanvas(carrierImageFile);
const encodedCanvas = encodeTextInImage(carrierCanvas, 'Secret message!', 2);

// Decode text
const decodedText = decodeTextFromImage(encodedCanvas, 2);
console.log(decodedText); // "Secret message!"
```

### React Component Usage

```tsx
import { LSBImageEncoder } from '@/components/LSBImageEncoder';
import { LSBTextEncoder } from '@/components/LSBTextEncoder';

function SteganographyPage() {
  return (
    <div className="space-y-6">
      <LSBImageEncoder />
      <LSBTextEncoder />
    </div>
  );
}
```

## Part 8: Best Practices

### Choosing n_bits

- **1 bit**: Maximum imperceptibility, lowest capacity
- **2 bits**: Good balance (recommended default)
- **3-4 bits**: Higher capacity, slightly more visible
- **5-8 bits**: Maximum capacity, may be visible

### Image Selection

- **Carrier images**: Use images with natural variation (photos work better than solid colors)
- **High resolution**: More capacity for text encoding
- **Format**: PNG recommended (lossless), avoid JPEG (lossy compression destroys hidden data)

### Security Considerations

- **Not encryption**: LSB steganography is not encryption - it's obfuscation
- **Detectable**: Statistical analysis can detect LSB steganography
- **Use cases**: Best for hiding data in plain sight, not for security-critical applications
- **Combine with encryption**: For security, encrypt data before encoding

### Performance

- **Large images**: Processing can be slow for very large images (>10MP)
- **Web Workers**: Consider using Web Workers for encoding/decoding large images
- **Memory**: Be mindful of memory usage with large images

## Part 9: Error Handling

### Common Errors

```typescript
// Image too small
if (carrierCanvas.width < hideCanvas.width || carrierCanvas.height < hideCanvas.height) {
  throw new Error('Carrier image must be at least as large as image to hide');
}

// Text too long
const capacity = calculateTextCapacity(width, height, nBits);
if (text.length > capacity) {
  throw new Error(`Text exceeds capacity of ${capacity} characters`);
}

// Invalid n_bits
if (nBits < 1 || nBits > 8) {
  throw new Error('n_bits must be between 1 and 8');
}
```

### Validation Functions

```typescript
export function validateNBits(nBits: number): void {
  if (!Number.isInteger(nBits) || nBits < 1 || nBits > 8) {
    throw new Error('n_bits must be an integer between 1 and 8');
  }
}

export function validateImageSize(
  width: number,
  height: number,
  minWidth: number = 1,
  minHeight: number = 1
): void {
  if (width < minWidth || height < minHeight) {
    throw new Error(`Image must be at least ${minWidth}×${minHeight} pixels`);
  }
}
```

## Part 10: Testing

### Unit Tests

```typescript
import { describe, it, expect } from 'vitest';
import {
  removeNLeastSignificantBits,
  getNLeastSignificantBits,
  getNMostSignificantBits,
  textToBinary,
  binaryToText
} from '@/lib/lsbSteganography';

describe('LSB Steganography', () => {
  it('removes least significant bits correctly', () => {
    expect(removeNLeastSignificantBits(107, 2)).toBe(104);
  });
  
  it('extracts least significant bits correctly', () => {
    expect(getNLeastSignificantBits(107, 2)).toBe(3);
  });
  
  it('converts text to binary and back', () => {
    const text = 'Hello, World!';
    const binary = textToBinary(text);
    const decoded = binaryToText(binary);
    expect(decoded).toBe(text);
  });
});
```

### Integration Tests

```typescript
import { describe, it, expect } from 'vitest';
import {
  loadImageToCanvas,
  encodeTextInImage,
  decodeTextFromImage
} from '@/lib/lsbSteganography';

describe('Text Encoding/Decoding', () => {
  it('encodes and decodes text correctly', async () => {
    // Create test image
    const canvas = document.createElement('canvas');
    canvas.width = 100;
    canvas.height = 100;
    const ctx = canvas.getContext('2d')!;
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(0, 0, 100, 100);
    
    // Encode
    const text = 'Test message';
    const encoded = encodeTextInImage(canvas, text, 2);
    
    // Decode
    const decoded = decodeTextFromImage(encoded, 2);
    expect(decoded).toBe(text);
  });
});
```

## Summary

LSB steganography provides a powerful way to hide images or text within other images. Key points:

- **Image-to-Image**: Hide one image within another using most/least significant bits
- **Text-to-Image**: Encode text messages into images with capacity calculation
- **Bit Manipulation**: Core functions for bit-level operations
- **React Integration**: Hooks and components for easy UI integration
- **Error Handling**: Comprehensive validation and error messages
- **Best Practices**: Choose appropriate n_bits, use PNG format, consider security implications

The implementation is production-ready and can be integrated into any web application that needs steganographic capabilities.

