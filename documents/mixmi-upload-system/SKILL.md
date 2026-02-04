---
name: mixmi-upload-system
description: Complete documentation of the mixmi content upload system including Quick and Advanced modes, metadata requirements, attribution configuration, and file handling
metadata:
  status: Active
  implementation: Supabase + React - Alpha
  last_updated: 2025-10-26
---

# mixmi Upload System

> Documentation of the content upload process, metadata collection, and attribution configuration for the mixmi platform.

## Overview

The upload system provides two modes for content submission:
- **Quick Upload:** 4 steps, ~2 minutes, solo creators
- **Advanced Upload:** 7 steps, ~5-7 minutes, detailed attribution

Both modes support various content types: 8-bar loops, loop packs, songs, and EPs.

## Upload Modes

### Quick Upload Mode

**Target Users:** Solo creators, simple uploads  
**Time to Complete:** ~2 minutes  
**Attribution:** 100% to uploader

#### Step 1: Basic Information
```typescript
// Required Fields
content_type: '8-bar-loop' | 'loop-pack' | 'song' | 'ep'
title: string (conditional based on content_type)
artist: string (with autosuggest)
version?: string (optional remix identifier)

// Content-specific fields
pack_description?: string (Loop Packs only)
loop_category?: 'instrumental' | 'vocal' | 'beat' | 'stem' | 'other'
tell_us_more?: string (required if stem/other)

// Technical metadata
bpm?: number (required for loops/packs, optional for songs)
key?: string (optional, hidden for EPs)
```

#### Step 2: File Uploads
```typescript
// Cover Artwork
cover_image_url: string (upload or URL input)
imageInputType: 'upload' | 'url'

// Audio Files
audio_url?: string (single file for loop/song)
loop_files?: File[] (2-5 files for loop pack)
ep_files?: File[] (2-5 files for EP)

// Auto-detected
duration: number (from audio analysis)
bpm?: number (if not manually specified)
```

#### Step 3: Licensing & Pricing

**8-Bar Loop:**
- `allow_remixing`: true (required)
- `remix_price_stx`: 1 STX (fixed)
- `allow_downloads`: boolean (optional)
- `download_price_stx`: number (if downloads enabled)

**Loop Pack:**
- `allow_remixing`: true (required per loop)
- `remix_price_stx`: 1 STX per loop (fixed)
- `allow_downloads`: boolean (optional)
- `price_per_loop`: number
- `download_price_stx`: auto-calculated total

**Song:**
- `download_price`: number
- `price_stx`: same as download_price

**EP:**
- `price_per_song`: number
- `price_stx`: auto-calculated total

#### Step 4: Review & Submit
- Read-only summary of all entered data
- Edit buttons for each section
- Final submission

### Advanced Upload Mode

**Target Users:** Collaborations, detailed attribution  
**Time to Complete:** ~5-7 minutes  
**Attribution:** Customizable splits

#### Steps 1-4: Same as Quick Upload

#### Step 2 (Advanced): Composition Splits
```typescript
// Who wrote it? (up to 3 contributors)
composition_split_1_wallet: string (auto-filled from uploader)
composition_split_1_percentage: number

composition_split_2_wallet?: string
composition_split_2_percentage?: number

composition_split_3_wallet?: string
composition_split_3_percentage?: number

// Must sum to 100%
```

#### Step 3 (Advanced): Production Splits
```typescript
// Who recorded it? (up to 3 contributors)
production_split_1_wallet: string (auto-filled from uploader)
production_split_1_percentage: number

production_split_2_wallet?: string
production_split_2_percentage?: number

production_split_3_wallet?: string
production_split_3_percentage?: number

// Must sum to 100%
```

#### Step 4 (Advanced): Industry Identifiers
```typescript
isrc?: string // International Standard Recording Code
```

#### Steps 5-7: Continue with file upload, licensing, and review

## Location Tagging

Available in both modes, added during submission:

### User Input
```typescript
locationInput: string // User's search query
selectedLocations: string[] // Array of location names
selectedLocationCoords: Array<{
  lat: number,
  lng: number,
  name: string
}>
```

### Database Storage
```typescript
location_lat: number // Primary latitude
location_lng: number // Primary longitude
primary_location: string // Main location name
locations: Location[] // All location objects
tags: string[] // Auto-appended with "🌍 {location}"
```

## Database Schema

### ip_tracks Table Structure

#### Basic Fields
```sql
id UUID PRIMARY KEY
title VARCHAR
artist VARCHAR
wallet_address VARCHAR -- Uploader's wallet
version VARCHAR -- Version/remix identifier
created_at TIMESTAMP
updated_at TIMESTAMP
```

#### Content Type Fields
```sql
content_type VARCHAR -- 'loop' | 'loop_pack' | 'song' | 'ep'
loop_category VARCHAR -- For loops only
pack_description TEXT -- For loop packs
tell_us_more TEXT -- Additional description
```

#### File Storage
```sql
audio_url TEXT -- Single audio file URL
cover_image_url TEXT -- Cover art URL
loop_files JSONB -- Array of loop file URLs (packs)
ep_files JSONB -- Array of song file URLs (EPs)
duration INTEGER -- Duration in seconds
```

#### Technical Metadata
```sql
bpm INTEGER
key VARCHAR
tags TEXT[] -- Array of tags
notes TEXT -- Internal notes
```

#### Attribution Fields (7 slots each)
```sql
-- Composition splits
composition_split_1_wallet VARCHAR
composition_split_1_percentage INTEGER
-- ... up to composition_split_7_*

-- Production splits
production_split_1_wallet VARCHAR
production_split_1_percentage INTEGER
-- ... up to production_split_7_*
```

#### Licensing Fields
```sql
allow_remixing BOOLEAN
allow_downloads BOOLEAN
remix_price_stx DECIMAL(10,2)
download_price_stx DECIMAL(10,2)
license_type VARCHAR -- 'remix_only' | 'remix_external' | 'custom'
license_selection VARCHAR -- 'platform_remix' | 'platform_download'
```

#### Location Fields
```sql
location_lat DECIMAL
location_lng DECIMAL
primary_location VARCHAR
locations JSONB -- Array of location objects
```

#### Remix Tracking
```sql
remix_depth INTEGER DEFAULT 0
source_track_ids UUID[]
generation INTEGER
```

#### Future/Inactive Fields
```sql
-- Currently in database but not active
open_to_commercial BOOLEAN
open_to_collaboration BOOLEAN
commercial_contact VARCHAR
commercial_contact_fee DECIMAL
collab_contact VARCHAR
collab_contact_fee DECIMAL
uploader_wallet_override VARCHAR -- Temporary cleanup field
```

## File Handling

### Audio Files
- **Formats:** MP3, WAV, AIFF, FLAC
- **Max Size:** 50MB per file
- **Processing:** 
  - BPM detection
  - Waveform generation
  - Duration calculation
  - Format normalization

### Cover Images
- **Formats:** JPG, PNG, GIF, WebP
- **Max Size:** 5MB
- **Processing:**
  - Resize to standard dimensions
  - Generate thumbnails
  - Optimize for web

### Storage Strategy
```javascript
// Upload flow
1. Upload to Vercel Blob (temporary)
2. Process and validate
3. Move to Supabase Storage (permanent)
4. Update database with URLs
5. Clean up temporary files
```

## Validation Rules

### Title Validation
- Required for all content types
- Max 100 characters
- No special characters except: - _ ' " &

### Attribution Validation
- Percentages must sum to exactly 100%
- Wallet addresses must be valid
- Maximum 3 contributors in Quick mode
- Maximum 7 contributors in Advanced mode (future)

### Pricing Validation
- Minimum price: 0.1 STX
- Maximum price: 10,000 STX
- Remix price fixed at 1 STX per loop
- Download price must be > 0 if downloads enabled

### File Validation
- Audio file required
- Cover image required (or default assigned)
- Loop packs: 2-5 loops
- EPs: 2-5 songs

## API Endpoints

### Upload Initiation
```
POST /api/upload/start
Response: {
  uploadId: string,
  uploadUrls: {
    audio: string,
    cover: string
  }
}
```

### File Upload
```
POST /api/upload/audio
Body: FormData with audio file
Response: {
  url: string,
  duration: number,
  bpm?: number
}
```

### Metadata Submission
```
POST /api/upload/metadata
Body: {
  ...all form fields
}
Response: {
  trackId: string,
  success: boolean
}
```

### Upload Status
```
GET /api/upload/status/:uploadId
Response: {
  status: 'uploading' | 'processing' | 'complete' | 'failed',
  progress: number,
  trackId?: string
}
```

## UI/UX Considerations

### Progress Indicators
- Step counter (1 of 4 or 1 of 7)
- Progress bar
- Save draft capability
- Back navigation

### Form Behavior
- Auto-save to localStorage
- Field validation on blur
- Clear error messages
- Contextual help text

### Mobile Optimization
- Responsive forms
- Touch-friendly inputs
- Camera access for cover photos
- Simplified location picker

## Error Handling

### Common Errors
- **File too large:** Show size limit, suggest compression
- **Invalid format:** List accepted formats
- **Network timeout:** Auto-retry with exponential backoff
- **Validation failure:** Highlight specific fields
- **Server error:** Save draft, allow retry

### Recovery Mechanisms
1. Save form state to localStorage
2. Allow resume from draft
3. Retry failed uploads
4. Contact support option

## Future Enhancements

### Planned Features
- Bulk upload for multiple tracks
- Template system for frequent uploaders
- Auto-fill from previous uploads
- Collaborative upload sessions
- AI-assisted metadata extraction
- More granular licensing options

### Attribution Expansion
- Support for 7+ contributors
- AI attribution fields
- Community attribution
- Place/venue attribution (beyond TBD wallets)

### Integration Improvements
- Direct DAW upload plugins
- Mobile app with offline capability
- API for third-party tools
- Batch processing system

## Testing Checklist

### Critical Paths
1. **Quick Upload:** Solo loop upload
2. **Advanced Upload:** 3-way collaboration
3. **Loop Pack:** 5 loops with metadata
4. **EP Upload:** 5 songs with pricing
5. **Location Tagging:** Multiple locations
6. **Draft Recovery:** Interrupted upload

### Edge Cases
- Exactly 100% split calculation
- Maximum file sizes
- Special characters in titles
- Network interruption mid-upload
- Duplicate file detection

---

*Note: This documentation reflects current upload system. Features marked as "planned" or "future" are not yet implemented.*