---
name: mixmi-curation-model
description: Complete curation and streaming economics including playlists, radio, mixed content, revenue calculations, and the two-economy system (creation vs curation)
metadata:
  status: Active - Ready for Implementation
  implementation: Post-Database Cleanup
  last_updated: 2025-10-27
---

# mixmi Curation & Streaming Model
## Complete Implementation Guide

> Comprehensive documentation of curation economics, streaming revenue, and licensing for the mixmi platform

**Status:** Ready for Implementation (pending database cleanup)  
**Last Updated:** October 27, 2025  
**Blockchain:** Transitioning from Stacks to SUI

---

## Table of Contents

1. [Core Philosophy](#core-philosophy)
2. [The Two Economies](#the-two-economies)
3. [Streaming Model](#streaming-model)
4. [Licensing Tiers](#licensing-tiers)
5. [Curation: Song Playlists](#curation-song-playlists)
6. [Curation: Loop Pack Remixes](#curation-loop-pack-remixes)
7. [Revenue Calculations](#revenue-calculations)
8. [Database Requirements](#database-requirements)
9. [User Experience Flow](#user-experience-flow)
10. [Certificate Display](#certificate-display)

---

## Core Philosophy

### Curation is Valuable Work
Unlike Spotify where curators get exposure only, **mixmi pays curators for discovery and taste-making**. This creates economic incentives for quality curation and helps artists get discovered.

### Attribution ≠ Payment
- **Creation** (remixes) = IP inheritance + commission
- **Curation** (playlists, discovery) = No IP, but discovery commission
- Both are valuable, compensated differently

### Free Discovery
- Full loop previews (8 bars) = Always free
- Song previews (20 seconds) = Always free
- This removes friction from discovery while maintaining revenue on actual consumption

---

## Color System

### Complete Platform Palette

**Core Content Types:**
- 🟣 **Purple `#9772F4`** - Loops (remixable, creative)
- 🟡 **Gold `#FFE4B5`** - Songs (complete, finished)
- 🟦 **Indigo `#6366F1`** - Playlists (curated, collection)
- 🔷 **Sky Blue `#38BDF8`** - Video (visual, media)
- 🟠 **Orange `#FB923C`** - Radio (live, broadcast)

**UI Elements:**
- 🔵 **Cyan `#81E4F2`** - Interactive actions, buttons, accents

**Background:**
- **Dark Navy `#101726`** - All colors designed for high contrast on this background

**Border Conventions:**
- **2px** - Single item (loop, song, video)
- **4px** - Collection (loop pack, EP, playlist, radio station)

**Semantic Meanings:**
- Purple = Transformable (can be remixed, loaded to mixer)
- Gold = Finished work (ready for consumption)
- Indigo = Human curation (taste-making, discovery)
- Sky Blue = Visual medium (video content)
- Orange = Live transmission (real-time broadcast)

---

## Content Card Architecture

### Card Size Transformations

**Discovery (160px) → Storage (64px) → Widgets**

All content follows this flow:
1. **160px cards** appear on globe, stores, search results
2. Dragged to **crate** → transforms to 64px for storage
3. Dragged from crate to **target widgets** → plays/loads

### Drag Targets by Content Type

```
LOOPS (purple):
  → Crate (storage)
  → Mixer Decks (direct play/remix)
  → Playlist Widget (for listening)

SONGS (gold):
  → Crate (storage)
  → Playlist Widget (for listening)
  → Shopping Cart (via hover controls)

PLAYLISTS (indigo):
  → Crate (storage)
  → Playlist Widget (REPLACES current content)
  
RADIO STATIONS (orange, future):
  → Crate (storage)
  → Radio Widget (streams external)
  
VIDEOS (sky blue, future):
  → Crate (storage)
  → Video Widget (plays)
  → Playlist Widget (mixed media playlists)
```

**Important:** Shopping cart is NOT a drag target. Hover controls on cards send items to cart.

### Playlist Cube Behavior

**Display:**
- 160px card with 4px indigo border (collection indicator)
- Hover shows: "10 items • Curated by [Name]"
- Info emoji → Opens playlist details modal
- Chevron → Expands vertically (like loop packs/EPs)

**Expanded View:**
```
[Playlist: "Late Night Vibes"] 🔽
├─ 🟣 Chill Drums (loop)
├─ 🟣 Ambient Pad (loop)
├─ 🟡 Midnight Drive (song)
├─ 🟡 City Lights (song)
└─ ... (6 more items)
```

**Preview Options:**
- Click individual items in expanded view for 20-sec preview (songs) or full loop play
- Drag entire playlist cube to playlist widget to play full sequence

**Playlist Widget Behavior:**

**If widget is empty:**
- ✅ Unpacks all items into widget
- Title shows: "Playing: [Playlist Name] by [Curator]"
- Plays sequentially or user can skip around

**If widget has content:**
```
⚠️ Warning Modal:
"Replace current playlist?"
[Cancel] [Clear & Load]
```

**Adding Individual Items:**
```
⚠️ Options Modal:
"Add to current playlist?"
[Cancel] [Add to End] [Replace All]
```

**Note:** Playlists are NOT nested containers (no meta-curation for MVP). They contain only atomic content (individual loops, songs, videos, radio links).

---

## Radio Station Integration (Future)

### Architecture

**Your Database (Metadata):**
```sql
radio_stations
  - id, creator_id, title, genre
  - location_lat, location_lng
  - stream_url (points to external server)
  - is_live (boolean)
  - cover_image_url, description
```

**The Flow:**
1. Radio curator creates account, uploads "stations" as content type
2. Station appears on globe at real-world location
3. Shows on curator's store page as orange 160px card
4. User drags to **radio widget** (persistent, like playlist widget)
5. Widget requests from YOUR API: `/api/radio/play/:stationId`
6. Your backend returns: `{ streamUrl: "https://external-stream.com/..." }`
7. Your frontend audio element connects to their stream
8. User hears external radio station in your UI

**API Architecture:**
- **Discovery/metadata:** YOUR API (mixmi database)
- **Streaming:** THEIR API (external server hosts audio)
- You're embedding external streams with your metadata layer

**Revenue Model:**
- Free to listen (external streaming, no pass required)
- Curator earns 20% when:
  - Someone buys a track discovered from radio context
  - Attribution: "discovered via [Radio Station Name]"
  - Incentivizes radio hosts to play quality music that drives sales

**Radio Widget UI:**
```
┌────────────────────────────────┐
│  🔴 LIVE: Tresor Berlin        │
├────────────────────────────────┤
│  Techno • Berlin, Germany      │
│  Hosted by DJ Kommander        │
├────────────────────────────────┤
│  Now Playing:                  │
│  "Unknown Track" (via stream)  │
│  [streaming...]                │
│  🔇 ────●── 🔊                 │
│                                │
│  💬 Chat  🛒 Buy Pass         │
└────────────────────────────────┘
```

---

## The Two Economies

### Economy 1: Transformation (Remixes)
**When someone creates something NEW using existing content**

- Original creators contribute to new work's IP
- Remix creator gets 20% commission, NOT ownership
- IP inheritance flows through generations
- Pays licensing fee upfront (1 STX per loop)

**Example:** Producer remixes two loops
- Original Loop A creator: 40% of future sales
- Original Loop B creator: 40% of future sales
- Remix producer: 20% commission on future sales

**Applied to:** Loop remixes, derivative works

### Economy 2: Curation (Discovery)
**When someone showcases/presents existing content**

- NO IP inheritance whatsoever
- Curator gets 20% discovery commission
- Original creators keep 80%
- Can earn from ongoing discovery streams/sales

**Example:** DJ creates curated playlist
- When playlist sells: DJ 20%, artists 80%
- When songs stream from DJ's store: DJ 20%, artists 80%
- Original artists retain 100% IP rights

**Applied to:** Song playlists, curated collections, discovery referrals

---

## Streaming Model

### Economic Structure

**30-Minute Streaming Pass:**
- Price: **1 STX** (simple, like a parking meter)
- Platform cut: **20%** = 0.2 STX
- Available for creators/curators: **80%** = 0.8 STX

**Per-Stream Economics:**
- Average song: 3.5 minutes
- Songs per 30-min pass: ~8-9 songs
- **Revenue per full play: ~0.08 STX**

**At current STX price (~$0.45):**
- 0.08 STX = **~$0.036 per stream**
- Spotify = $0.003-0.004 per stream
- **mixmi pays 9-12x better than Spotify**

### What Counts as a Stream?

**Full Play Required:**
- Songs: Must play to completion (or substantial portion, e.g., 80%+)
- Loops: Do NOT count as streams (free discovery/advertising)
- Previews (20 sec): Do not count

**Platform Mechanics:**
- Loops play full 8 bars in widgets (free)
- Songs show 20-second preview unless user has pass
- Pass holders get unlimited streaming for 30 minutes

**Important:** Loops do NOT participate in streaming revenue model. Full loop plays in widgets/radio/playlists are free discovery. This is intentional - loop exposure = advertising that drives remix purchases.

---

## Licensing Tiers

### For LOOPS and LOOP PACKS

#### Tier 1: Platform Remix Only (Default)
- **Price:** 1 STX (fixed)
- **Allows:** Use in mixmi mixer to create remixes
- **Restricts:** Cannot download or use outside platform
- **Revenue:** Upfront 1 STX fee + 40% of any remixes created

#### Tier 2: Platform Remix + Download/Offline Use
- **Platform Price:** 1 STX (for remix use)
- **Download Price:** Custom (set by creator)
- **Allows:** All platform uses + download for external DAW/DJ use
- **Revenue:** 1 STX remix fee + download price + remix inheritance

### For SONGS and EPs

#### Tier 1: Platform Streaming Only (Default)
- **Price:** ~0.08 STX per stream (via 30-min passes)
- **Allows:** Streaming in playlists, radio, creator stores
- **Restricts:** Cannot download
- **Revenue:** Per-stream from passes + playlist sales

#### Tier 2: Platform Streaming + Download
- **Streaming:** ~0.08 STX per stream
- **Download Price:** Custom (set by creator)
- **Allows:** All streaming + download for offline/DJ use
- **Revenue:** Streaming revenue + download purchases

**Important:** Individual songs cannot be purchased for streaming - only accessed via passes. Download is separate tier.

---

## Curation: Song Playlists

### Mixed Content Playlists

**Playlists Can Contain:**
- Loops (8-bar, remixable)
- Songs (full tracks)
- EPs (which auto-unpack to individual songs)
- Loop Packs (which auto-unpack to individual loops)
- Future: Videos, Radio station links, Events

**No Content Type Restrictions:**
- A playlist can be 5 loops + 5 songs
- Or 10 songs
- Or 8 loops + 1 song + 1 video (future)
- The system auto-adapts revenue based on what's consumed

**Why Mixed Content Works:**

1. **Scene Capture** - "Austin Hip-Hop 2025" playlist could have:
   - Local producer loops (free discovery)
   - Released songs from Austin artists (streaming revenue)
   - Link to local radio station (free discovery + attribution)
   - Video of live performance (future)

2. **Smart Economics** - Revenue logic auto-adapts:
   - Songs → Generate streaming revenue
   - Loops → Free advertising, drive remix purchases
   - Radio/Video → Attribution tracking for discovery commissions

3. **Natural Curation** - DJs can showcase a song PLUS the loops used to make it
   - Song plays → Curator + artist earn streaming revenue
   - Loops play → Free exposure drives future remix sales
   - Curator earns 20% on ANY purchases from this context

### The Curator Flow

1. **Discovery**
   - Browse via globe, radio, genre tags, search
   - Preview 20 seconds of any song (free)
   - Click through to artist stores

2. **Collection (Crate)**
   - Drag tracks to persistent crate component
   - Crate follows across pages (except account/profile)
   - Can hold loops, songs, loop packs, EPs
   - Packs auto-unpack when dragged to playlist

3. **Curation (Playlist Widget)**
   - Drag from crate to playlist widget
   - Reorder tracks (drag to reorder)
   - Edit playlist metadata (title, description, cover)
   - Preview the flow

4. **Publishing**
   - Click "Publish to My Store" button
   - **FREE to publish** (no upfront cost)
   - Appears immediately on curator's creator store
   - Available for purchase or streaming

### Playlist Constraints

- **Maximum:** 10 items per playlist (for MVP)
- **Content:** Any mix of loops, songs, EPs, loop packs
- **Unpacking:** EPs and loop packs auto-unpack to individual tracks when added

### Revenue Model

**When playlist is purchased:**
```
Sale Price: X STX
├─ Curator: 20% (0.2X STX)
└─ Artists: 80% (0.8X STX) - split proportionally by track count
   - Only songs receive revenue
   - Loops get 0 (free advertising)
```

**When songs stream from curator's store:**
```
Pass Revenue: 1 STX
├─ Platform: 20% (0.2 STX)
└─ Available: 80% (0.8 STX)
    ├─ Curator: 20% of 0.8 = 0.16 STX
    └─ Artists: 80% of 0.8 = 0.64 STX (split per play)
```

**When songs stream from other sources:**
```
No curator involved = Artists get full 80% (after platform cut)
```

### Why This Works

- **Curator incentive:** Earn 20% on every play from your store
- **Artist benefit:** Get discovered, keep 80% AND all IP rights
- **Platform viral growth:** Curators become micro-labels, competing for audiences
- **No lock-in:** Artists can be in unlimited curator stores simultaneously

### The "Instant Record Label" Model

Anyone becomes a label through curation:
- Create account (can be pseudonymous/brand identity)
- Curate quality playlists
- Feature in your store
- Earn 20% on discoveries
- **No contracts, no exclusivity, no rights transfer**

**Artist strategy flip:**
- OLD: Seek ONE label deal → lose rights
- NEW: Appear in MANY curator stores → keep rights, multiple revenue streams

---

## Curation: Loop Pack Remixes

### The Remix Flow (Gen 1)

1. **Load loops** into mixer (2 loops max for Gen 1)
2. **Mix live** with professional DJ tools
3. **Record** your mix
4. **Select** 8-bar section to extract
5. **Pay licensing fee:** 2 STX (1 per loop)
6. **Receive** new track with inherited attribution

### Attribution Structure

**Each source loop contributes 50% to BOTH sides:**
- Composition: Loop A (50%), Loop B (50%)
- Sound Recording: Loop A (50%), Loop B (50%)

**The remixer gets 20% commission, NOT ownership:**
- When remix sells for 10 STX:
  - Remixer: 2 STX (20%)
  - Original creators: 8 STX (80%, split among them)

### This IS Curation + Creation

**It's curation because:**
- You selected which loops to combine (taste)
- You decided they work well together (discovery)
- You introduced people to those loops (amplification)

**It's creation because:**
- You made something new that didn't exist
- You added creative decision-making (mixing, timing, effects)
- You transformed the sources into new context

**Therefore:**
- You get the 20% curation commission
- BUT the originals keep 80% AND their IP flows through
- This is why you pay upfront (2 STX licensing fee)

### Multi-Generation Inheritance

Remixes can be remixed:
```
Original Loop A (100% comp, 100% prod)
    ↓ remixed with Loop B
Gen 1 Remix (Loop A 50%, Loop B 50% on both sides + 20% commission to remixer)
    ↓ remixed with Loop C
Gen 2 Remix (A 25%, B 25%, C 50% + 20% commission to new remixer)
```

Each generation, the original creators' IP dilutes BUT they continue earning from downstream uses.

---

## Revenue Calculations

### Example 1: Song Playlist Purchase

**Scenario:**
- 10-song playlist titled "Late Night Vibes"
- Curator: DJ Midnight
- Price: 5 STX

**Distribution:**
```
Total: 5 STX
├─ DJ Midnight (curator): 1 STX (20%)
└─ Artists: 4 STX (80%)
    ├─ Artist 1: 0.4 STX (10 tracks = 10% each)
    ├─ Artist 2: 0.4 STX
    ├─ Artist 3: 0.4 STX
    ├─ ... (7 more artists at 0.4 STX each)
    └─ Artist 10: 0.4 STX
```

### Example 2: Streaming from Curator Store

**Scenario:**
- User buys 30-min pass (1 STX)
- Plays 8 songs, all from DJ Midnight's store

**Distribution:**
```
Pass: 1 STX
├─ Platform: 0.2 STX (20%)
└─ Available: 0.8 STX (80%)
    ├─ DJ Midnight: 0.16 STX (20% of 0.8)
    └─ Artists: 0.64 STX (80% of 0.8)
        └─ Split: 0.08 STX per song × 8 songs
```

### Example 3: Mixed Streaming Sources

**Scenario:**
- User buys 30-min pass (1 STX)
- Plays 5 songs from DJ Midnight's store
- Plays 3 songs from random radio
- Plays 2 songs from artist pages directly

**Distribution:**
```
Pass: 1 STX → 0.8 STX available after platform cut

Songs from DJ Midnight's store (5 songs):
├─ DJ Midnight: 20% of (5/10 × 0.8) = 0.08 STX
└─ Those 5 artists: 80% of (5/10 × 0.8) = 0.32 STX

Songs from radio/direct (5 songs):
└─ Those 5 artists: 100% of (5/10 × 0.8) = 0.4 STX
    (No curator involved)
```

### Example 4: Mixed Content Playlist Streaming

**Scenario:**
- Playlist "Producer's Pack" by DJ Tools (5 loops + 5 songs)
- User buys 30-min pass (1 STX) and plays entire playlist

**Distribution:**
```
Pass: 1 STX → 0.8 STX available after platform cut

5 loops play: Generate 0 revenue (free discovery)
5 songs stream: Split the 0.8 STX

DJ Tools (curator): 20% of 0.8 = 0.16 STX
Song artists: 80% of 0.8 = 0.64 STX (0.128 per artist)
Loop creators: 0 STX (but gain exposure)
```

**If someone then buys a loop from that playlist:**
```
Loop price: 1 STX
├─ Loop creator: 0.8 STX (80%)
└─ DJ Tools: 0.2 STX (20% discovery commission)
```

### Example 5: Mixed Content Playlist Purchase

**Scenario:**
- Playlist "Scene Sounds" by DJ Austin (3 loops + 7 songs)
- Price: 8 STX

**Distribution:**
```
Total: 8 STX
├─ DJ Austin (curator): 1.6 STX (20%)
└─ Contents: 6.4 STX (80%)
    ├─ 7 Song artists: 6.4 STX split proportionally (0.914 each)
    └─ 3 Loop creators: 0 STX (free exposure, they earn from remixes)
```

**Rationale:** Loops get free advertising in the playlist. Revenue comes when someone:
- Buys the loop individually (1 STX → 0.8 to creator, 0.2 to curator)
- Uses it in a remix (1 STX licensing + 40% of future remix sales)

### Example 6: Loop Pack Remix

**Scenario:**
- Producer remixes "Beach Drums" (by Alice) + "Synth Waves" (by Bob)
- Pays 2 STX licensing fee (1 per loop)
- Later, remix sells for 10 STX

**Initial Payment (Licensing):**
```
2 STX upfront
├─ Alice (Beach Drums): 1 STX
└─ Bob (Synth Waves): 1 STX
```

**Future Sale (10 STX):**
```
10 STX remix sale
├─ Producer (remixer): 2 STX (20% commission)
└─ Original creators: 8 STX (80%)
    ├─ Alice: 4 STX (50% composition + 50% production)
    └─ Bob: 4 STX (50% composition + 50% production)
```

**Total earnings:**
- Alice: 1 STX (upfront) + 4 STX (sale) = **5 STX**
- Bob: 1 STX (upfront) + 4 STX (sale) = **5 STX**
- Producer: 2 STX (commission only)

---

## Database Requirements

### New Tables Needed

#### `playlists`
Core playlist information.

**Fields:**
- `id` - UUID, primary key
- `creator_id` - UUID, references users(id)
- `title` - VARCHAR(255)
- `description` - TEXT
- `cover_image_url` - VARCHAR(500)
- `purchase_price_stx` - DECIMAL (null = streaming only, access via pass)
- `is_published` - BOOLEAN (default false)
- `created_at` - TIMESTAMP
- `updated_at` - TIMESTAMP

#### `playlist_items` (NOT `playlist_tracks` - more flexible!)
Junction table for playlist contents with ordering.

**Critical Design:** This table uses `item_type` instead of foreign keys to specific tables. This allows playlists to contain ANY content type without schema changes.

**Fields:**
- `id` - UUID, primary key
- `playlist_id` - UUID, references playlists(id)
- `item_id` - UUID (references various tables based on item_type)
- `item_type` - VARCHAR: 'loop' | 'song' | 'ep' | 'loop_pack' | 'video' | 'radio_station' | 'event'
- `position` - INTEGER (for ordering, 0-9 for 10-item limit)
- `added_at` - TIMESTAMP

**Constraints:**
- Maximum 10 items per playlist (for MVP)
- Position must be unique within playlist
- Can mix any content types

**Why This Design:**
When you add video or radio stations, you don't change `playlist_items` structure. Just:
1. Create `video` or `radio_stations` table
2. Start inserting with `item_type = 'video'` or `'radio_station'`
3. UI automatically handles rendering based on item_type

**Query Pattern:**
```sql
-- Get playlist with all items
SELECT 
  pi.position,
  pi.item_type,
  CASE pi.item_type
    WHEN 'loop' THEN (SELECT row_to_json(t) FROM ip_tracks t WHERE t.id = pi.item_id)
    WHEN 'song' THEN (SELECT row_to_json(t) FROM ip_tracks t WHERE t.id = pi.item_id)
    WHEN 'video' THEN (SELECT row_to_json(v) FROM videos v WHERE v.id = pi.item_id)
    WHEN 'radio_station' THEN (SELECT row_to_json(r) FROM radio_stations r WHERE r.id = pi.item_id)
  END as item_data
FROM playlist_items pi
WHERE pi.playlist_id = $1
ORDER BY pi.position;
```

#### `stream_plays`
Track streaming attribution for revenue distribution.

**Fields:**
- `id` - UUID, primary key
- `track_id` - UUID, references ip_tracks(id)
- `user_id` - UUID, references users(id) - who streamed it
- `curator_id` - UUID, references users(id), nullable - if from curator store
- `playlist_id` - UUID, references playlists(id), nullable
- `pass_id` - UUID, references streaming_passes(id)
- `played_at` - TIMESTAMP
- `completion_percentage` - INTEGER (0-100, needs ≥80% to count)
- `revenue_stx` - DECIMAL (calculated share from pass)

#### `streaming_passes`
Track 30-minute streaming passes.

**Fields:**
- `id` - UUID, primary key
- `user_id` - UUID, references users(id)
- `purchased_at` - TIMESTAMP
- `expires_at` - TIMESTAMP (purchased_at + 30 minutes)
- `price_stx` - DECIMAL (currently 1 STX)
- `stacks_tx_id` - VARCHAR (blockchain transaction)
- `total_plays` - INTEGER (count of completed streams)
- `status` - VARCHAR ('active' | 'expired' | 'consumed')

### Modifications to Existing Tables

#### `ip_tracks`
Add/update licensing fields:

**New/Updated Fields:**
- `license_type` - VARCHAR: 'remix_only' | 'streaming_only' | 'remix_download' | 'streaming_download'
- `streaming_enabled` - BOOLEAN (for songs/EPs)
- `streaming_rate_stx` - DECIMAL (currently 0.08, calculated from passes)
- Keep existing: `remix_price_stx`, `download_price_stx`

#### `transactions`
Expand transaction types:

**Updated Fields:**
- `transaction_type` - Add: 'playlist_purchase' | 'streaming_pass' | 'curator_commission'
- `curator_id` - UUID, nullable (for curator attribution)
- `curator_amount` - DECIMAL (curator's 20% share)

---

## User Experience Flow

### For Curators

1. **Browse & Discover**
   - Use globe, radio, search, tags
   - Preview 20 sec of any song (free)
   - Click through to artist pages

2. **Build Collection**
   - Drag songs to crate
   - Crate persists across discovery surfaces
   - Can hold 100+ items (crate isn't limited)

3. **Create Playlist**
   - Drag from crate to playlist widget
   - Reorder (drag to reorder)
   - Maximum 10 items (songs, loops, mixed)
   - Add title, description, cover art

4. **Publish**
   - Click "Publish to My Store"
   - FREE (no upfront cost)
   - Set purchase price (optional)
   - Goes live immediately

5. **Earn**
   - 20% on playlist purchases
   - 20% on streams from your store
   - Track performance in analytics

### For Artists

1. **Upload Song**
   - Choose licensing tier
   - Tier 1: Streaming only (~0.08 STX/play)
   - Tier 2: Add download option (custom price)

2. **Get Discovered**
   - Appear in search, globe, radio
   - Curators find and playlist your song
   - No action needed from you

3. **Earn**
   - 80% from playlist sales
   - 80% from streaming (whether curated or not)
   - 100% of your IP rights
   - 100% of download sales (minus platform)

4. **Track Impact**
   - See which playlists feature your music
   - See which curators are driving plays
   - Optional: thank curators or collaborate

### For Listeners

1. **Free Discovery**
   - 20-second song previews
   - Full 8-bar loop plays
   - Browse globe, radio, stores

2. **Buy Pass**
   - 1 STX = 30 minutes
   - Unlimited streaming during pass
   - Works across all playlists/stores/radio

3. **Support Artists & Curators**
   - Your streams pay both
   - Buy playlists to support curation
   - Download songs for DJ/offline use

---

## Certificate Display

### For Original Uploads (Loops, Songs)

```
┌─────────────────────────────────────────────────────────┐
│  mixmi CERTIFICATE                                      │
│  VERIFIED UPLOAD                                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Album Art]  Title: "Beach Drums"                     │
│               Artist: DJ Pinkbunny                     │
│               Type: LOOP                                │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  UPLOAD DETAILS                                         │
│                                                         │
│  Upload Date:     October 9, 2025 at 23:24 UTC        │
│  Track ID:        a4dd0956-5931-4e50-9dbd-0126556f583c│
│  Uploader:        SP1DTN6E...ZXNCTN                    │
│  BPM:             110                                   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  INTELLECTUAL PROPERTY RIGHTS                           │
│                                                         │
│  Composition Rights:      100% - SP1DTN6E...ZXNCTN     │
│  Sound Recording Rights:  100% - SP1DTN6E...ZXNCTN     │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  USAGE PERMISSIONS                                      │
│                                                         │
│  License Type:       Platform Remix Only                │
│  Platform Price:     1 STX                              │
│  Download Price:     Not Available                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### For Curated Playlists

```
┌─────────────────────────────────────────────────────────┐
│  mixmi CERTIFICATE                                      │
│  VERIFIED UPLOAD                                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Cover Art]  Title: "Late Night Vibes"                │
│               Curator: DJ Midnight                      │
│               Type: CURATED PLAYLIST (10 tracks)        │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  UPLOAD DETAILS                                         │
│                                                         │
│  Created:         October 15, 2025 at 18:45 UTC       │
│  Playlist ID:     b2ff1234-8765-4a21-bcde-9876543210ab│
│  Curator:         SP2ABC...XYZDEF                      │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  CURATION ATTRIBUTION                                   │
│                                                         │
│  Curator Commission:  20% (discovery & curation)        │
│  Artist Revenue:      80% (split among 10 artists)      │
│                                                         │
│  Note: Curator earns commission but holds NO            │
│        intellectual property rights. All IP remains     │
│        with original artists.                           │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  USAGE PERMISSIONS                                      │
│                                                         │
│  License Type:       Curated Collection                 │
│  Collection Price:   5 STX                              │
│  Streaming:          Included in 30-min passes          │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  PLAYLIST CONTENTS                                      │
│                                                         │
│  1. "Midnight Drive" - Artist A                        │
│  2. "City Lights" - Artist B                           │
│  ... (expandable list)                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### For Remixes (Gen 1)

```
┌─────────────────────────────────────────────────────────┐
│  mixmi CERTIFICATE                                      │
│  VERIFIED UPLOAD                                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Album Art]  Title: "Beach Dreams Remix"              │
│               Remixer: Producer Charlie                 │
│               Type: GEN 1 REMIX                         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  UPLOAD DETAILS                                         │
│                                                         │
│  Created:         October 20, 2025 at 14:30 UTC       │
│  Track ID:        c3ee2345-9876-5b32-cdef-1234567890cd│
│  Remixer:         SP3DEF...ABCGHI                      │
│  Licensing Paid:  2 STX (1 per source loop)            │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  INTELLECTUAL PROPERTY RIGHTS                           │
│                                                         │
│  Composition Rights:                                    │
│    50% - SP1DTN6E...ZXNCTN (Beach Drums)               │
│    50% - SP2XYZ...PQRSTU (Synth Waves)                 │
│                                                         │
│  Sound Recording Rights:                                │
│    50% - SP1DTN6E...ZXNCTN (Beach Drums)               │
│    50% - SP2XYZ...PQRSTU (Synth Waves)                 │
│                                                         │
│  Remixer Commission: 20% of sales                       │
│  (Commission ≠ IP ownership)                            │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  USAGE PERMISSIONS                                      │
│                                                         │
│  License Type:       Platform Remix Only                │
│  Platform Price:     1 STX                              │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  SOURCE ATTRIBUTION                                     │
│                                                         │
│  Source 1: "Beach Drums" by DJ Pinkbunny               │
│            [link to original]                           │
│                                                         │
│  Source 2: "Synth Waves" by WaveRider                  │
│            [link to original]                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Future Content Types: Extensibility Pattern

### Adding New Content Types (Video, Events, etc.)

The playlist architecture supports infinite content types without database migrations. Here's the pattern:

**Step 1: Create New Content Table**
```sql
CREATE TABLE videos (
  id UUID PRIMARY KEY,
  creator_id UUID REFERENCES users(id),
  title VARCHAR(255),
  video_url VARCHAR(500),
  thumbnail_url VARCHAR(500),
  duration INTEGER, -- seconds
  location_lat DECIMAL,
  location_lng DECIMAL,
  created_at TIMESTAMP
);
```

**Step 2: Add UI Card Component**
```tsx
// components/VideoCard.tsx
// 160px card with 2px sky blue border
// Follows existing card patterns
```

**Step 3: Update item_type Enum**
```sql
-- Just start using it - no migration needed
INSERT INTO playlist_items (playlist_id, item_id, item_type, position)
VALUES ($1, $2, 'video', 0);
```

**Step 4: Update Revenue Logic**
```typescript
// lib/calculatePlaylistRevenue.ts
const revenueGeneratingTypes = ['song']; // Video = free for MVP
const items = playlist.items.filter(i => revenueGeneratingTypes.includes(i.item_type));
```

**That's it!** Playlists now support video without touching the playlist schema.

### Example: Video Content (Future)

**Content Type:** `video`  
**Color:** Sky Blue `#38BDF8`  
**Border:** 2px (single item)  
**Drag Targets:** Crate → Video Widget OR Playlist Widget  

**Revenue Model (for MVP):**
- Free to watch (no pass required)
- Creator earns when video drives purchases
- Curator gets 20% on purchases from video context
- Future: could add video-specific passes or ads

**Database:**
```sql
videos
  - id, creator_id, title, description
  - video_url, thumbnail_url, duration
  - location_lat, location_lng
  - view_count, like_count
  - created_at, updated_at
```

### Example: Events Content (Future)

**Content Type:** `event`  
**Color:** Amber `#F59E0B`  
**Border:** 4px dashed (upcoming) → 4px solid (live)  
**Drag Targets:** Calendar Widget (to save/RSVP)

**Revenue Model:**
- Ticket sales (if paid event)
- 20% to platform, 80% to organizer
- Curator gets 20% if discovered via their store

**Database:**
```sql
events
  - id, creator_id, title, description
  - event_type (concert, meetup, workshop)
  - start_time, end_time, timezone
  - location_lat, location_lng, venue_name
  - ticket_price_stx (null = free)
  - capacity, attendee_count
  - is_live (currently happening)
```

---

## Implementation Checklist

### Phase 1: Licensing Update (Do Now)
- [ ] Update IpTrackModal upload form
  - [ ] Loops: "Platform Remix Only" + optional Download
  - [ ] Songs: "Platform Streaming Only" + optional Download
  - [ ] Clear help text with streaming rate (~0.08 STX)
- [ ] Update Certificate component
  - [ ] Change "Production Rights" → "Sound Recording Rights"
  - [ ] Add "USAGE PERMISSIONS" section
  - [ ] Display license type and pricing

### Phase 2: Database Cleanup
- [ ] Clean up existing ip_tracks table
- [ ] Document current schema
- [ ] Plan curation tables (playlists, playlist_items, stream_plays, streaming_passes)

### Phase 3: Streaming Infrastructure
- [ ] Create streaming_passes table
- [ ] Build pass purchase flow
- [ ] Implement pass expiration logic
- [ ] Add "Buy 30-Min Pass" UI across platform

### Phase 4: Playlist Creation
- [ ] Create playlists + playlist_items tables
- [ ] Add "Publish to Store" button in playlist widget
- [ ] Build playlist creation API
- [ ] Implement 10-item limit

### Phase 5: Stream Attribution
- [ ] Create stream_plays table
- [ ] Track completion percentage (need ≥80% to count)
- [ ] Calculate per-stream revenue from passes
- [ ] Attribute to curator if from curator store

### Phase 6: Revenue Distribution
- [ ] Calculate 20/80 splits for curated streams
- [ ] Update payment splitter for curator commissions
- [ ] Build curator earnings dashboard
- [ ] Add artist discovery analytics

### Phase 7: Certificate Enhancement
- [ ] Add playlist certificate template
- [ ] Show curation attribution (20% curator, 80% artists)
- [ ] Display playlist contents
- [ ] Add "Note: No IP transfer" disclaimer

---

## Terms of Use Considerations

### Language to Include

**Streaming Economics:**
> "30-minute streaming passes cost 1 STX. The platform retains 20% for operations. The remaining 80% is distributed among artists and curators based on actual streams during the pass period. Each full song play is attributed approximately 0.08 STX in value. Songs must be played to substantial completion (80%+) to count as a stream."

**Curator Commission:**
> "Curators who create and publish playlists earn a 20% discovery commission on sales of those playlists and streams that originate from their creator stores. This commission compensates for curation labor and discovery work. Curators do NOT receive any intellectual property rights in the underlying works."

**Remix Attribution:**
> "When you create a remix using platform loops, you pay a licensing fee (currently 1 STX per source loop). You receive a 20% commission on future sales of your remix. The original loop creators retain intellectual property rights and receive 80% of remix sales, split proportionally among all original contributors. Your commission is compensation for creative curation and mixing work, not ownership."

**Loop Preview Policy:**
> "Full 8-bar loop previews are available free of charge to facilitate discovery and remixing. This is not considered streaming consumption and does not generate streaming revenue. Revenue for loop creators comes from remix licensing fees and direct purchases."

**Song Preview Policy:**
> "20-second song previews are available free of charge for discovery. To hear full songs, users must purchase a 30-minute streaming pass or download the song (if available). Previews do not generate streaming revenue."

---

## Future Enhancements (Post-MVP)

### Discovery Referral Tracking
Track when someone finds an artist through a curator and then purchases OTHER works by that artist. Curator gets referral fee (e.g., 5-10% of that sale).

**Potential logic:**
- Cookie/session tracking for 30 days
- "Discovered via [Curator Name]" attribution
- Ongoing passive income for good curation

### Dynamic Playlist Pricing
Let curators test different price points. Platform could suggest optimal pricing based on:
- Number of tracks
- Artist popularity
- Curator reputation
- Market data

### Playlist Analytics
Show curators:
- Total streams from their store
- Most popular tracks in their playlists
- Revenue per playlist
- Listener retention/engagement

### Collaborative Playlists
Multiple curators contribute to one playlist, split the 20% among them.

### Featured Playlist Marketplace
Platform highlights exceptional curation, giving curators exposure in exchange for reduced commission or featured placement fees.

### Playlist Genres & Moods
Standardized tagging for playlists so listeners can find "Late Night Jazz" or "Workout Beats" easily.

---

## Questions for Alpha Users

Before finalizing implementation, ask early users:

1. **Curator Economics:**
   - Is 20% fair compensation for curation work?
   - Would you curate for free initially to build reputation?
   - What analytics would help you curate better?

2. **Streaming Pricing:**
   - Is 1 STX / 30 minutes the right price point?
   - Should there be tiered passes (1hr, 3hr, 24hr)?
   - Would you buy passes regularly?

3. **Playlist Limits:**
   - Is 10 items enough for MVP?
   - Should there be mini-playlists (5 items) and mega-playlists (20 items)?
   - Different pricing by size?

4. **Discovery:**
   - How do you want to find new music?
   - Should curators be ranked/rated?
   - Should there be curator follows/subscriptions?

5. **Platform Cut:**
   - Is 20% fair for platform operations?
   - Would you accept higher % for better features?
   - Should there be discounts for high-volume creators?

---

## Migration to SUI

### What Changes

**Technical:**
- Smart contract language (Clarity → Move)
- Transaction format
- Wallet integration (easier onboarding)
- Gas token (STX → SUI)

**Economic:**
- Pricing will need recalculation based on SUI value
- Potentially micro-payments become easier (SUI is cheaper)
- Platform can subsidize initial costs more easily

**User Experience:**
- Easier wallet creation (no seed phrases needed)
- Faster transactions
- Lower friction onboarding

### What Stays Same

**Core Logic:**
- 20/80 curation split
- 50/50 remix inheritance  
- Attribution calculation
- TBD wallet concept
- UI/UX flow

**Philosophy:**
- Humans declare contribution
- Curation is valuable
- Attribution ≠ Payment
- Transparent economics

---

## Summary

### The Big Picture

mixmi creates two complementary economies:

1. **Creation Economy** - Remixers pay upfront, get commission, IP flows through
2. **Curation Economy** - Curators publish free, earn on discovery, no IP transfer

Both are valuable, both are compensated fairly, neither requires platform lock-in or exclusive deals.

### Why This Works

- **Artists:** Keep rights, get discovered, earn more than Spotify
- **Curators:** Get paid for taste, no contracts needed, unlimited playlists
- **Remixers:** Clear licensing, automatic attribution, ongoing revenue
- **Platform:** Sustainable 20% cut, viral growth through curation
- **Listeners:** Support both artists AND discoverers, transparent economics

### Next Steps

1. ✅ Update licensing UI (loops vs songs)
2. ✅ Add licensing to certificates
3. 🔄 Clean up database
4. ⏳ Build playlist tables
5. ⏳ Implement streaming passes
6. ⏳ Launch curation beta with alpha users
7. ⏳ Iterate based on feedback

---

**Document Version:** 1.0  
**Author:** mixmi Team  
**Purpose:** Implementation guide for curation & streaming features  
**Status:** Ready for development (pending database cleanup)
