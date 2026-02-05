# Warehouse Packing Application - Development Guide

## Project Overview

This is a **desktop application for warehouse packing operations** built with Electron + React + TypeScript. The app helps workers efficiently pack shipments by scanning QR codes, weighing items, capturing photos, and generating comprehensive reports.

### Key Requirements
- **Offline-first**: Works without internet connection
- **Portable**: No admin rights needed, runs as standalone executable
- **Hardware integration**: RS-232 scale (Radwag), QR scanners, camera
- **Premium UI/UX**: Spotify-level design quality with smooth animations
- **Multi-language support**: Polish (primary)

---

## Technical Stack

### Core Technologies
```json
{
  "electron": "33.0.0",
  "react": "18.2.0",
  "typescript": "5.3.0",
  "node": "20.11.0"
}
```

### Key Dependencies
```json
{
  "serialport": "12.0.0",           // RS-232 communication (Radwag scale)
  "better-sqlite3": "9.2.0",        // Local database
  "exceljs": "4.4.0",               // Excel export
  "jspdf": "2.5.1",                 // PDF generation
  "jspdf-autotable": "3.8.0",       // PDF tables
  "sharp": "0.33.0",                // Image compression
  "react-router-dom": "6.20.0",     // Routing
  "zustand": "4.4.7",               // State management
  "tailwindcss": "3.4.0",           // Styling
  "lucide-react": "0.294.0",        // Icons
  "date-fns": "3.0.0"               // Date formatting
}
```

### Development Tools
```json
{
  "electron-builder": "24.9.0",     // Packaging to portable .exe
  "webpack": "5.89.0",              // Bundling
  "electron-webpack": "2.8.2"       // Electron + Webpack integration
}
```

---

## Hardware Integration Details

### 1. Radwag Scale (WLC 30/60/C2/R)

**Connection:**
- Interface: RS-232 (DB9 male connector)
- Adapter: Moxa USB-to-Serial (null-modem cable)
- Protocol: RADWAG CBCP-02 (ASCII text)
- Settings: 9600 bps, 8N1 (8 data bits, no parity, 1 stop bit)
- Line ending: CR + LF (`\r\n`)

**Commands:**
```
SI   - Get current measurement (instant)
S    - Get stable measurement
Z    - Zero/tare
T    - Tare
C1   - Enable continuous mode
C0   - Disable continuous mode
```

**Response Format:**
```
S + 12.345 kg    (stable reading)
US + 12.345 kg   (unstable reading)
```

**Implementation Requirements:**
- Auto-detect COM port (list available ports, let user select)
- Wait for stable reading (parse 'S' vs 'US' prefix)
- Display real-time weight during measurement
- Handle disconnection gracefully (show error, allow reconnect)
- Store weight in grams (convert from kg automatically)

### 2. QR Scanner

**Type:** Zebra (or similar) - Keyboard wedge mode
**Behavior:** 
- Scans QR code → sends text as keyboard input
- Automatically appends Enter key at end
- No special driver needed (acts like keyboard)

**Implementation:**
- Listen to keyboard events in focused input field
- Detect rapid typing (QR scan) vs manual typing
- Parse SAP index from scanned string
- Auto-submit on Enter key

### 3. Camera

**Type:** Built-in laptop webcam or USB camera
**API:** Native Web API (`navigator.mediaDevices.getUserMedia()`)
**Requirements:**
- Live preview before capture
- Keyboard shortcuts: Space = capture, Enter = confirm, Esc = cancel
- Support multiple photos per item
- Mouse-friendly alternative controls

---

## Application Architecture

### File Structure
```
warehouse-packing-app/
├── src/
│   ├── main/                          # Electron main process
│   │   ├── index.ts                   # Main entry point
│   │   ├── database.ts                # SQLite setup & queries
│   │   ├── serialPort.ts              # Scale communication
│   │   ├── ipc-handlers.ts            # IPC communication handlers
│   │   └── fileSystem.ts              # File operations (export, save)
│   │
│   ├── renderer/                      # React application
│   │   ├── App.tsx                    # Main app component
│   │   ├── main.tsx                   # Renderer entry point
│   │   │
│   │   ├── components/                # React components
│   │   │   ├── Dashboard.tsx          # Main menu / shipment list
│   │   │   ├── ShipmentCreator.tsx    # Create new shipment
│   │   │   ├── PackingScreen.tsx      # Main packing interface
│   │   │   ├── PartCard.tsx           # Individual part in list
│   │   │   ├── ScanModal.tsx          # Modal shown after scan
│   │   │   ├── WeightCapture.tsx      # Weight measurement UI
│   │   │   ├── CountrySelector.tsx    # Country of origin picker
│   │   │   ├── PhotoCapture.tsx       # Camera interface
│   │   │   ├── ProgressBar.tsx        # Animated progress indicator
│   │   │   ├── Settings.tsx           # App settings
│   │   │   └── Statistics.tsx         # User stats & achievements
│   │   │
│   │   ├── services/                  # Business logic services
│   │   │   ├── ScaleService.ts        # Radwag scale communication
│   │   │   ├── QRService.ts           # QR scanning logic
│   │   │   ├── DatabaseService.ts     # SQLite queries wrapper
│   │   │   ├── ExcelService.ts        # Excel report generation
│   │   │   ├── PDFService.ts          # PDF report generation
│   │   │   ├── HTMLService.ts         # HTML report generation
│   │   │   ├── ImageService.ts        # Image compression
│   │   │   ├── VoiceService.ts        # Text-to-speech feedback
│   │   │   ├── AutosaveService.ts     # Auto-save every 2 minutes
│   │   │   ├── ExportService.ts       # Export to network drive
│   │   │   └── StatsService.ts        # Statistics & achievements
│   │   │
│   │   ├── store/                     # State management (Zustand)
│   │   │   ├── shipmentStore.ts       # Current shipment state
│   │   │   ├── settingsStore.ts       # App settings
│   │   │   └── uiStore.ts             # UI state (modals, etc)
│   │   │
│   │   ├── types/                     # TypeScript types
│   │   │   ├── shipment.ts
│   │   │   ├── part.ts
│   │   │   ├── scale.ts
│   │   │   └── report.ts
│   │   │
│   │   └── styles/                    # CSS/Tailwind
│   │       ├── globals.css
│   │       └── animations.css
│   │
│   └── shared/                        # Shared between main/renderer
│       ├── constants.ts
│       └── ipc-channels.ts            # IPC channel names
│
├── database/
│   └── schema.sql                     # SQLite schema
│
├── resources/                         # App resources
│   ├── icon.ico                       # App icon
│   └── sounds/                        # Sound effects (optional)
│
├── package.json
├── tsconfig.json
├── webpack.config.js
└── electron-builder.yml               # Build configuration
```

---

## Database Schema (SQLite)

```sql
-- Main shipments table
CREATE TABLE shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_number TEXT NOT NULL UNIQUE,
    destination TEXT NOT NULL,
    notes TEXT,
    created_at INTEGER NOT NULL,          -- Unix timestamp
    completed_at INTEGER,                 -- Unix timestamp (NULL if in progress)
    status TEXT NOT NULL DEFAULT 'in_progress',  -- 'in_progress', 'paused', 'completed'
    
    -- Configuration for this shipment
    require_weight BOOLEAN NOT NULL DEFAULT 0,
    require_country BOOLEAN NOT NULL DEFAULT 0,
    require_photos BOOLEAN NOT NULL DEFAULT 0,
    
    -- Metadata
    packed_by TEXT,                       -- User name (optional)
    packing_time_seconds INTEGER,         -- Total time spent packing
    
    -- Excel file reference
    excel_file_path TEXT,                 -- Path to original Excel file
    
    created_date TEXT NOT NULL            -- Date string for grouping (YYYY-MM-DD)
);

-- Parts in shipment
CREATE TABLE parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INTEGER NOT NULL,
    
    -- From Excel
    sap_index TEXT NOT NULL,
    description TEXT NOT NULL,
    quantity REAL NOT NULL,
    unit TEXT NOT NULL,
    
    -- Packing status
    status TEXT NOT NULL DEFAULT 'pending',  -- 'pending', 'packed'
    packed_at INTEGER,                       -- Unix timestamp
    packing_time_seconds INTEGER,            -- Time to pack this part
    
    -- Optional data
    weight_total REAL,                       -- Total weight in grams
    weight_per_unit REAL,                    -- Weight per unit in grams
    country_of_origin TEXT,
    
    -- Excel metadata (for advanced features)
    excel_row_number INTEGER,
    
    FOREIGN KEY (shipment_id) REFERENCES shipments(id) ON DELETE CASCADE
);

-- Photos attached to parts
CREATE TABLE photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    part_id INTEGER NOT NULL,
    
    photo_data BLOB NOT NULL,                -- Compressed JPEG (or path to file)
    thumbnail_data BLOB,                     -- Small thumbnail
    
    created_at INTEGER NOT NULL,
    file_size INTEGER,                       -- Bytes
    
    FOREIGN KEY (part_id) REFERENCES parts(id) ON DELETE CASCADE
);

-- Autosave snapshots
CREATE TABLE autosaves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id INTEGER NOT NULL,
    
    snapshot_data TEXT NOT NULL,             -- JSON snapshot of shipment state
    created_at INTEGER NOT NULL,
    
    FOREIGN KEY (shipment_id) REFERENCES shipments(id) ON DELETE CASCADE
);

-- User statistics
CREATE TABLE user_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    total_shipments INTEGER NOT NULL DEFAULT 0,
    total_parts INTEGER NOT NULL DEFAULT 0,
    total_packing_time_seconds INTEGER NOT NULL DEFAULT 0,
    
    fastest_part_time_seconds INTEGER,       -- Personal best
    fastest_shipment_time_seconds INTEGER,
    
    last_updated INTEGER NOT NULL
);

-- Achievements
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    achievement_id TEXT NOT NULL UNIQUE,     -- e.g., 'first_shipment', 'speed_demon'
    unlocked_at INTEGER NOT NULL,
    shipment_id INTEGER                      -- Which shipment unlocked it
);

-- App settings
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_parts_shipment ON parts(shipment_id);
CREATE INDEX idx_parts_status ON parts(status);
CREATE INDEX idx_photos_part ON photos(part_id);
CREATE INDEX idx_shipments_status ON shipments(status);
CREATE INDEX idx_shipments_date ON shipments(created_date);
```

---

## Core Features & Workflows

### 1. Create New Shipment

**User Flow:**
1. Click "New Shipment" button
2. Fill form:
   - Shipment number (required, unique)
   - Destination (required)
   - Notes (optional)
   - Upload Excel file with parts list
3. Configure data requirements:
   - ☐ Weight measurement required
   - ☐ Country of origin required
   - ☐ Photos required
4. Click "Start Packing" → Navigate to packing screen

**Excel File Format Expected:**
```
Column A: SAP Index (required)
Column B: Description (required)
Column C: Quantity (required)
Column D: Unit (required)
Column E: Country of Origin (optional - if 'COO' in header, enable country requirement)
```

**Implementation:**
- Use `exceljs` to parse Excel file
- Validate columns (at least 4 required)
- Auto-detect if country column exists
- Import all rows into `parts` table with status='pending'

### 2. Packing Screen (Main Interface)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  ← Back    WYS-001 │ Destination    [████████░░] 80% │ 8/10 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔍 [Scan QR or search...]                          [⚙️]    │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  TO PACK (2):                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ ☐ SAP-11111  Śruba M8 ocynkowana      50 szt        │  │
│  │ ☐ SAP-22222  Nakrętka M8               25 szt       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  PACKED (8): ▼                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ ✅ SAP-12345  Łożysko kulkowe         5 szt  2.3 kg │  │
│  │ ✅ SAP-67890  Uszczelka               12 szt         │  │
│  │ ... (collapsed, grayed out)                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  [💾 Save] [⏸️ Pause] [📊 Report] [📈 Stats] [⚙️ Settings] │
└─────────────────────────────────────────────────────────────┘
```

**Key Features:**
- **Search field**: Focus by default, auto-focus after each scan
- **QR Scanning**: 
  - Type in search field (scanner acts as keyboard)
  - Detect Enter key → search for SAP index
  - If found → show modal
  - If not found → show error toast
- **Manual selection**: Click on part card to pack
- **Progress**: 
  - Percentage bar (animated)
  - Count "X of Y parts packed"
- **List management**:
  - Unpacked parts at top (full opacity)
  - Packed parts at bottom (30% opacity, collapsed)
  - Smooth animations when moving between sections

**State Management:**
```typescript
interface PackingState {
  shipment: Shipment;
  parts: Part[];
  currentPart: Part | null;
  searchQuery: string;
  isScanning: boolean;
}
```

### 3. Part Scanning Modal

**Triggered when:**
- QR code scanned and part found
- User clicks on part in list

**Modal Content:**
```
┌─────────────────────────────────────────┐
│                                          │
│           SAP-11111                      │  ← 72px font
│                                          │
│      Śruba M8 ocynkowana                │  ← 24px
│                                          │
│           📦 50 szt                      │  ← 48px bold
│                                          │
├──────────────────────────────────────────┤
│  Scan again to confirm                   │
│  or press Enter                          │
├──────────────────────────────────────────┤
│           [PACK] (Enter)                 │
└──────────────────────────────────────────┘
```

**Behavior:**
- Show part details (large, readable)
- Wait for:
  - Second scan of same SAP index → proceed
  - Enter key → proceed
  - Escape key → cancel
  - Click outside → cancel
- If requires weight/country/photos → proceed to those screens
- If not → mark as packed immediately

**Voice Feedback:**
- On first scan: "Część zeskanowana" (Part scanned)
- On second scan/confirm: Proceed to next step

### 4. Weight Measurement

**Triggered when:** `require_weight = true` for shipment

**UI Flow:**
```
┌─────────────────────────────────────────┐
│  ⚖️ Weight Measurement                  │
├─────────────────────────────────────────┤
│                                          │
│  SAP-11111 | Śruba M8 | 50 szt         │
│                                          │
│  [🔄 Reading from scale...]             │
│  Current: 1.234 kg (unstable)           │
│                                          │
│  Waiting for stable reading...          │
│                                          │
├─────────────────────────────────────────┤
│  [0️⃣ Zero] [🧺 Tare]                   │
└─────────────────────────────────────────┘
```

**Once Stable:**
```
┌─────────────────────────────────────────┐
│  ⚖️ Weight: 1.250 kg                    │  ← Large
├─────────────────────────────────────────┤
│                                          │
│  Quantity packed:                        │
│                                          │
│  ┌──────────┬──────────┬─────────────┐ │
│  │ [1 szt]  │ [50 szt] │ [Other: __] │ │
│  └──────────┴──────────┴─────────────┘ │
│                                          │
│  📊 Details:                             │
│  Weight per unit: 0.025 kg               │
│  Total weight: 1.250 kg                  │
│                                          │
├─────────────────────────────────────────┤
│           [✅ CONFIRM] (Enter)           │
└─────────────────────────────────────────┘
```

**Implementation:**
```typescript
// services/ScaleService.ts
class ScaleService {
  async waitForStableReading(): Promise<WeightReading> {
    // Poll scale every 200ms
    // Return when reading is stable ('S' prefix)
    // Timeout after 30 seconds
  }
  
  async getWeight(): Promise<WeightReading> {
    // Send 'SI' command
    // Parse response
  }
  
  async zero(): Promise<void> {
    // Send 'Z' command
  }
  
  async tare(): Promise<void> {
    // Send 'T' command
  }
}
```

**Default Behavior:**
- Auto-select quantity from Excel (e.g., 50 szt)
- Calculate weight per unit automatically
- Allow override if user packed different quantity (1 szt, custom)

**Voice Feedback:**
- When stable: "Waga 1.25 kilograma" (Weight 1.25 kilograms)

### 5. Country of Origin Selection

**Triggered when:** `require_country = true` for shipment

**UI:**
```
┌─────────────────────────────────────────┐
│  🌍 Country of Origin                    │
├─────────────────────────────────────────┤
│                                          │
│  Quick select (press number):            │
│                                          │
│  ┌────┬────┬────┬────┬────┬────┬────┐  │
│  │ 1  │ 2  │ 3  │ 4  │ 5  │ 6  │ 7  │  │
│  │ CN │ US │ DE │ JP │ PL │ IT │ FR │  │
│  └────┴────┴────┴────┴────┴────┴────┘  │
│                                          │
│  [0] Other (type manually)               │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │ Search: [____________]           │   │
│  └──────────────────────────────────┘   │
│                                          │
│  Common countries:                       │
│  • China (CN)                            │
│  • United States (US)                    │
│  • Germany (DE)                          │
│  • ... (scrollable list)                 │
│                                          │
├─────────────────────────────────────────┤
│           [CONFIRM] (Enter)              │
└─────────────────────────────────────────┘
```

**Predefined Countries:**
```typescript
const QUICK_COUNTRIES = [
  { code: 'CN', name: 'China', key: '1' },
  { code: 'US', name: 'United States', key: '2' },
  { code: 'DE', name: 'Germany', key: '3' },
  { code: 'JP', name: 'Japan', key: '4' },
  { code: 'PL', name: 'Poland', key: '5' },
  { code: 'IT', name: 'Italy', key: '6' },
  { code: 'FR', name: 'France', key: '7' },
];
```

**Keyboard Navigation:**
- Press 1-7 → instant select
- Press 0 → manual input field
- Type to search → filter list
- Enter → confirm selection

### 6. Photo Capture

**Triggered when:** `require_photos = true` for shipment

**UI:**
```
┌─────────────────────────────────────────────────┐
│  📷 Photo Capture                               │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │                                         │    │
│  │      [Live Camera Preview]              │    │
│  │                                         │    │
│  │         640x480 or larger               │    │
│  │                                         │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  Controls:                                       │
│  [Space] Capture  [Enter] Confirm  [Esc] Cancel│
│                                                  │
│  Photos taken (2):                               │
│  ┌─────┐ ┌─────┐                                │
│  │ 📷1 │ │ 📷2 │ [+]                            │
│  └─────┘ └─────┘                                │
│                                                  │
├─────────────────────────────────────────────────┤
│  [📸 Capture] [✅ Confirm] [❌ Cancel]          │
└─────────────────────────────────────────────────┘
```

**Features:**
- Live preview from camera
- Keyboard shortcuts:
  - Space → take photo
  - Enter → confirm and proceed (if at least 1 photo)
  - Escape → cancel
- Allow multiple photos per part
- Show thumbnails of captured photos
- Click thumbnail to delete
- Mouse-friendly buttons as alternative

**Image Processing:**
```typescript
// services/ImageService.ts
class ImageService {
  async compressImage(imageBlob: Blob): Promise<Buffer> {
    // Resize to max 1920x1080
    // JPEG quality 75%
    // Return compressed buffer
    // Target: ~400 KB per photo
  }
  
  async createThumbnail(imageBlob: Blob): Promise<Buffer> {
    // Resize to 400x300
    // JPEG quality 60%
    // For display in lists/reports
  }
}
```

### 7. Completion & Animation

**After all data collected:**

**Animation Sequence:**
```
1. ✅ Green checkmark appears on modal (500ms)
2. Modal fades out (300ms)
3. Part card in list:
   - Background flashes green (200ms)
   - Slides down to "Packed" section (400ms)
   - Opacity reduces to 30% (300ms)
4. Progress bar animates forward (500ms)
5. Voice: "Spakowane" (Packed)
```

**If Last Part:**
```
1. All above animations
2. Confetti animation (2 seconds)
3. Success modal:
   ┌────────────────────────────┐
   │   🎉 All Packed!           │
   │                             │
   │   10 parts completed        │
   │   Time: 23 minutes          │
   │                             │
   │   [Generate Report]         │
   │   [Start New Shipment]      │
   └────────────────────────────┘
4. Voice: "Wszystkie części spakowane. Dobra robota!"
```

### 8. Auto-save

**Behavior:**
- Every 2 minutes: save current state to `autosaves` table
- On manual save button click: immediate save
- Store as JSON snapshot:
  ```json
  {
    "timestamp": 1699876543,
    "parts_packed": 7,
    "parts_total": 10,
    "current_part_id": 123,
    "parts_status": [
      { "id": 120, "status": "packed", "weight": 1250, ... },
      { "id": 121, "status": "packed", ... },
      ...
    ]
  }
  ```

**Recovery:**
- On app launch: check for incomplete shipments
- If found: show "Resume Packing" option
- Load last autosave snapshot
- Continue from where user left off

### 9. Report Generation

**Three Formats Generated:**

#### A. PDF Report
```
Format: Professional document
Content:
- Header: Shipment number, destination, date
- Summary: Total parts, total weight, packing time
- Table: All parts with details
- Footer: Generated timestamp

Libraries: jsPDF + jspdf-autotable
```

#### B. Excel Report
```
Format: Multi-sheet workbook
Sheet 1 "Summary":
  - Shipment metadata
  - Statistics
Sheet 2 "Parts":
  - Full parts list with all data
  - Sortable, filterable
Sheet 3 "Photos":
  - Thumbnails with references

Libraries: exceljs
```

#### C. HTML Report
```
Format: Interactive web page
Features:
- Sortable table (click headers)
- Photo gallery with lightbox
- Responsive design
- Print-friendly CSS
- Standalone (no external dependencies)

Can be opened in any browser
```

**Export Locations:**
```
1. Local temp folder:
   C:\Users\[USER]\AppData\Local\PakowanieApp\exports\[SHIPMENT_NUMBER]\
   
2. Network drive (configurable):
   Z:\Pakowanie\Wysyłki\[YEAR]\[MONTH]\[SHIPMENT_NUMBER]\
   
Structure:
├── raport.pdf
├── dane.xlsx
├── raport.html
├── photos/
│   ├── SAP-11111_1.jpg
│   ├── SAP-11111_2.jpg
│   └── SAP-22222_1.jpg
└── backup.db (optional - full database snapshot)
```

**Implementation:**
```typescript
// services/ExportService.ts
class ExportService {
  async exportShipment(shipmentId: number): Promise<void> {
    // 1. Generate all reports
    const pdf = await PDFService.generate(shipmentId);
    const excel = await ExcelService.generate(shipmentId);
    const html = await HTMLService.generate(shipmentId);
    
    // 2. Save locally
    await this.saveLocal(shipmentId, { pdf, excel, html });
    
    // 3. Export to network drive
    const networkPath = await this.getNetworkPath();
    if (networkPath) {
      await this.copyToNetwork(shipmentId, networkPath);
    }
    
    // 4. Optional: Send email notification
    // (if configured in settings)
  }
}
```

### 10. Statistics & Gamification

**User Stats Tracked:**
- Total shipments completed
- Total parts packed
- Total time spent packing
- Average time per part
- Fastest part packed
- Fastest shipment completed
- Parts per hour

**Achievements System:**
```typescript
const ACHIEVEMENTS = [
  {
    id: 'first_shipment',
    name: '🎉 Pierwsze Pakowanie',
    description: 'Skompletuj swoją pierwszą wysyłkę',
    condition: (stats) => stats.totalShipments >= 1
  },
  {
    id: 'speed_demon',
    name: '⚡ Demon Prędkości',
    description: 'Spakuj część w mniej niż 15 sekund',
    condition: (stats) => stats.fastestPartTime < 15
  },
  {
    id: 'century',
    name: '💯 Setka',
    description: 'Spakuj 100 części',
    condition: (stats) => stats.totalParts >= 100
  },
  {
    id: 'perfect_day',
    name: '🌟 Perfekcyjny Dzień',
    description: 'Skompletuj 5 wysyłek w jeden dzień',
    condition: (stats) => stats.shipmentsToday >= 5
  },
  {
    id: 'heavyweight',
    name: '🏋️ Ciężarowiec',
    description: 'Spakuj część ważącą ponad 50kg',
    condition: (part) => part.weight > 50000
  },
  {
    id: 'marathon',
    name: '🏃 Maraton',
    description: 'Spakuj wysyłkę z ponad 200 pozycjami',
    condition: (shipment) => shipment.partsCount > 200
  },
  {
    id: 'streak_7',
    name: '🔥 Seria 7 Dni',
    description: 'Pakuj przez 7 dni z rzędu',
    condition: (stats) => stats.currentStreak >= 7
  }
];
```

**UI Display:**
```
Dashboard → Statistics Tab
┌─────────────────────────────────────┐
│  👤 Twoje Statystyki                │
├─────────────────────────────────────┤
│  📦 Wysyłki: 47                     │
│  📋 Części: 2,341                   │
│  ⚡ Średni czas/część: 24s          │
│  🏆 Rekord dzienny: 8 wysyłek       │
├─────────────────────────────────────┤
│  🎯 Osiągnięcia (7/12)              │
│  ✅ 🎉 💯 ⚡ 🌟 🏋️ 🎖️            │
│  🔒 🔒 🔒 🔒 🔒                     │
├─────────────────────────────────────┤
│  📈 Ostatni tydzień:                │
│  ████████░░░░░░  (57% szybciej!)   │
└─────────────────────────────────────┘
```

**Achievement Unlock Animation:**
```
Popup (center screen, 3 seconds):
┌─────────────────────────────────┐
│   🎉 NOWE OSIĄGNIĘCIE!          │
│                                  │
│        ⚡ Demon Prędkości        │
│                                  │
│     Spakowałeś część             │
│     w 12 sekund!                 │
│                                  │
└─────────────────────────────────┘

+ Confetti animation
+ Sound effect (optional)
+ Voice: "Osiągnięcie odblokowane!"
```

---

## UI/UX Design Guidelines

### Design System (Spotify-inspired)

**Color Palette:**
```css
/* Dark theme (primary) */
--bg-primary: #0a0e27;          /* Deep dark blue */
--bg-secondary: #1a1f3a;        /* Lighter dark blue */
--bg-tertiary: #2a3150;         /* Card backgrounds */

--accent-primary: #3b82f6;      /* Blue (primary actions) */
--accent-secondary: #8b5cf6;    /* Purple (secondary) */
--accent-success: #10b981;      /* Green (success states) */
--accent-warning: #f59e0b;      /* Orange (warnings) */
--accent-error: #ef4444;        /* Red (errors) */

--text-primary: #ffffff;        /* White (main text) */
--text-secondary: #94a3b8;      /* Light gray (secondary text) */
--text-tertiary: #64748b;       /* Darker gray (disabled) */

/* Gradients */
--gradient-primary: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
--gradient-success: linear-gradient(135deg, #10b981 0%, #059669 100%);
```

**Typography:**
```css
/* Font family */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Font sizes */
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */
--text-4xl: 2.25rem;    /* 36px */
--text-6xl: 3.75rem;    /* 60px */

/* Font weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-black: 900;
```

**Spacing System:**
```css
/* Consistent spacing (Tailwind-like) */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

**Border Radius:**
```css
--radius-sm: 0.375rem;   /* 6px */
--radius-md: 0.5rem;     /* 8px */
--radius-lg: 0.75rem;    /* 12px */
--radius-xl: 1rem;       /* 16px */
--radius-2xl: 1.5rem;    /* 24px */
--radius-full: 9999px;   /* Fully rounded */
```

### Key Animations

**1. Card Hover:**
```css
.card {
  transition: all 0.2s ease;
}

.card:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
}
```

**2. Button Press:**
```css
.button {
  transition: all 0.15s ease;
}

.button:active {
  transform: scale(0.95);
}
```

**3. Slide In (for parts list):**
```css
@keyframes slideInFromLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.part-card {
  animation: slideInFromLeft 0.3s ease-out;
}
```

**4. Progress Bar Fill:**
```css
.progress-fill {
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
```

**5. Modal Fade In:**
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-backdrop {
  animation: fadeIn 0.2s ease;
}

.modal-content {
  animation: scaleIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

**6. Checkmark Animation:**
```css
@keyframes drawCheckmark {
  from {
    stroke-dashoffset: 100;
  }
  to {
    stroke-dashoffset: 0;
  }
}

.checkmark {
  stroke-dasharray: 100;
  animation: drawCheckmark 0.4s ease forwards;
}
```

**7. Confetti (on completion):**
```typescript
// Use react-confetti library
import Confetti from 'react-confetti';

<Confetti
  width={window.innerWidth}
  height={window.innerHeight}
  numberOfPieces={200}
  recycle={false}
  colors={['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b']}
/>
```

### Glassmorphism Effects

```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.glass-dark {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### Loading States

**Spinner:**
```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spinner {
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #3b82f6;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 0.8s linear infinite;
}
```

**Skeleton Loading:**
```css
@keyframes shimmer {
  0% {
    background-position: -468px 0;
  }
  100% {
    background-position: 468px 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.1) 0px,
    rgba(255, 255, 255, 0.2) 40px,
    rgba(255, 255, 255, 0.1) 80px
  );
  background-size: 800px 100px;
  animation: shimmer 2s infinite;
}
```

---

## Settings & Configuration

**User-Configurable Settings:**

```typescript
interface AppSettings {
  // Scale settings
  scaleComPort: string;           // e.g., 'COM3'
  scaleBaudRate: number;          // 9600 (fixed for Radwag)
  scaleAutoDetect: boolean;       // Try to find scale automatically
  
  // Export settings
  networkDrivePath: string;       // e.g., 'Z:\Pakowanie\Wysyłki'
  enableNetworkExport: boolean;
  autoExportOnComplete: boolean;
  
  // Voice feedback
  enableVoice: boolean;
  voiceVolume: number;            // 0-100
  voiceLanguage: 'pl-PL';
  
  // UI preferences
  theme: 'dark' | 'light';        // Dark by default
  animationsEnabled: boolean;
  soundEffectsEnabled: boolean;
  
  // Auto-save
  autosaveInterval: number;       // Minutes (default: 2)
  
  // Statistics
  showStatistics: boolean;
  enableAchievements: boolean;
  
  // Advanced
  debugMode: boolean;
  logLevel: 'error' | 'warn' | 'info' | 'debug';
}
```

**Settings UI:**
```
Settings Screen:
┌─────────────────────────────────────┐
│  ⚙️ Settings                        │
├─────────────────────────────────────┤
│                                      │
│  ⚖️ Scale Configuration              │
│  ┌────────────────────────────────┐ │
│  │ COM Port: [Dropdown ▼]        │ │
│  │ ☐ Auto-detect on startup      │ │
│  │ [Test Connection]              │ │
│  └────────────────────────────────┘ │
│                                      │
│  💾 Export Settings                  │
│  ┌────────────────────────────────┐ │
│  │ Network path: [________]       │ │
│  │ ☑ Export to network on finish │ │
│  │ ☐ Auto-export on complete     │ │
│  └────────────────────────────────┘ │
│                                      │
│  🎤 Voice Feedback                   │
│  ┌────────────────────────────────┐ │
│  │ ☑ Enable voice feedback        │ │
│  │ Volume: [████████░░] 80%       │ │
│  │ [Test Voice]                   │ │
│  └────────────────────────────────┘ │
│                                      │
│  🎨 Appearance                       │
│  ┌────────────────────────────────┐ │
│  │ Theme: (•) Dark  ( ) Light     │ │
│  │ ☑ Enable animations            │ │
│  │ ☑ Sound effects                │ │
│  └────────────────────────────────┘ │
│                                      │
├─────────────────────────────────────┤
│  [Save] [Cancel] [Reset to Default] │
└─────────────────────────────────────┘
```

---

## Error Handling & Edge Cases

### Critical Error Scenarios

**1. Scale Disconnected During Weighing:**
```typescript
try {
  const weight = await scaleService.getWeight();
} catch (error) {
  if (error.code === 'ENOENT' || error.message.includes('disconnected')) {
    showErrorModal({
      title: 'Waga Odłączona',
      message: 'Nie można odczytać wagi. Sprawdź połączenie i spróbuj ponownie.',
      actions: [
        { label: 'Połącz Ponownie', onClick: () => scaleService.reconnect() },
        { label: 'Pomiń Wagę', onClick: () => skipWeight() },
        { label: 'Wróć', onClick: () => goBack() }
      ]
    });
  }
}
```

**2. Scanned Part Not on List:**
```typescript
const part = findPartBySAP(scannedCode);
if (!part) {
  playErrorSound();
  voiceService.error('Części nie ma na liście');
  showToast({
    type: 'error',
    message: `SAP ${scannedCode} nie znajduje się na liście wysyłki`,
    duration: 5000
  });
  // Keep search field focused for retry
}
```

**3. Part Already Packed:**
```typescript
if (part.status === 'packed') {
  playWarningSound();
  voiceService.error('Część już spakowana');
  showWarningModal({
    title: '⚠️ Ostrzeżenie',
    message: `Część ${part.sapIndex} została już spakowana.`,
    subtext: `Spakowano: ${formatDate(part.packedAt)}`,
    actions: [
      { label: 'Pakuj Ponownie', onClick: () => packAgain(part) },
      { label: 'Anuluj', onClick: () => closeModal() }
    ]
  });
}
```

**4. Camera Permission Denied:**
```typescript
try {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
} catch (error) {
  if (error.name === 'NotAllowedError') {
    showErrorModal({
      title: 'Brak Dostępu do Kamery',
      message: 'Aplikacja nie ma uprawnień do kamery. Sprawdź ustawienia przeglądarki.',
      actions: [
        { label: 'Pomiń Zdjęcia', onClick: () => skipPhotos() },
        { label: 'Wróć', onClick: () => goBack() }
      ]
    });
  }
}
```

**5. Excel File Parsing Error:**
```typescript
try {
  const workbook = await exceljs.readFile(filePath);
} catch (error) {
  showErrorModal({
    title: 'Błąd Odczytu Pliku',
    message: 'Nie można odczytać pliku Excel. Upewnij się że format jest prawidłowy.',
    details: error.message,
    actions: [
      { label: 'Wybierz Inny Plik', onClick: () => selectFile() },
      { label: 'Anuluj', onClick: () => goBack() }
    ]
  });
}
```

**6. Network Drive Unavailable:**
```typescript
try {
  await exportToNetwork(shipmentId);
} catch (error) {
  showWarningModal({
    title: 'Eksport na Dysk Sieciowy',
    message: 'Nie można zapisać na dysku sieciowym. Pliki zapisano lokalnie.',
    subtext: `Lokalnie: ${localPath}`,
    actions: [
      { label: 'Spróbuj Ponownie', onClick: () => retryExport() },
      { label: 'OK', onClick: () => closeModal() }
    ]
  });
}
```

**7. Low Disk Space:**
```typescript
// Check before saving photos
const freeSpace = await checkDiskSpace();
if (freeSpace < 100 * 1024 * 1024) { // Less than 100 MB
  showWarningModal({
    title: 'Mało Miejsca na Dysku',
    message: `Pozostało tylko ${formatBytes(freeSpace)}. Rozważ usunięcie starych plików.`,
    actions: [
      { label: 'Kontynuuj', onClick: () => proceed() },
      { label: 'Otwórz Folder', onClick: () => openExportsFolder() }
    ]
  });
}
```

### Data Validation

**Excel Import Validation:**
```typescript
function validateExcelData(rows: any[]): ValidationResult {
  const errors: string[] = [];
  
  // Check required columns
  if (!rows[0].hasOwnProperty('SAP Index')) {
    errors.push('Brak kolumny "SAP Index"');
  }
  if (!rows[0].hasOwnProperty('Description')) {
    errors.push('Brak kolumny "Description"');
  }
  if (!rows[0].hasOwnProperty('Quantity')) {
    errors.push('Brak kolumny "Quantity"');
  }
  
  // Validate data
  rows.forEach((row, index) => {
    if (!row['SAP Index'] || row['SAP Index'].trim() === '') {
      errors.push(`Wiersz ${index + 2}: Brak SAP Index`);
    }
    if (!row['Quantity'] || isNaN(row['Quantity'])) {
      errors.push(`Wiersz ${index + 2}: Nieprawidłowa ilość`);
    }
  });
  
  return {
    valid: errors.length === 0,
    errors
  };
}
```

**Weight Validation:**
```typescript
function validateWeight(weight: number, quantity: number): ValidationResult {
  const errors: string[] = [];
  
  // Negative weight
  if (weight < 0) {
    errors.push('Waga nie może być ujemna');
  }
  
  // Unrealistic weight (> 100 kg per unit)
  const weightPerUnit = weight / quantity;
  if (weightPerUnit > 100000) { // 100 kg in grams
    errors.push('Waga na sztukę przekracza 100 kg. Sprawdź czy to prawidłowe.');
  }
  
  // Very light (< 1 gram per unit)
  if (weightPerUnit < 1 && weightPerUnit > 0) {
    errors.push('Waga na sztukę jest bardzo niska (<1g). Sprawdź czy to prawidłowe.');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings: errors // Show as warnings, allow proceed
  };
}
```

---

## Build & Deployment

### Development Setup

**Prerequisites:**
```bash
Node.js 20.11.0 (LTS)
npm 10.2.4
Windows 10/11
```

**Initial Setup:**
```bash
# Clone/create project
mkdir warehouse-packing-app
cd warehouse-packing-app

# Initialize
npm init -y

# Install dependencies
npm install electron react react-dom typescript
npm install serialport better-sqlite3 exceljs jspdf sharp
npm install zustand react-router-dom date-fns lucide-react
npm install tailwindcss autoprefixer postcss

# Install dev dependencies
npm install -D @types/react @types/node
npm install -D electron-builder webpack electron-webpack
npm install -D @serialport/parser-readline
```

**Scripts (package.json):**
```json
{
  "scripts": {
    "dev": "electron-webpack dev",
    "compile": "electron-webpack",
    "build": "electron-webpack && electron-builder",
    "build:portable": "electron-webpack && electron-builder --win portable",
    "start": "electron ."
  }
}
```

### Build Configuration

**electron-builder.yml:**
```yaml
appId: com.warehouse.packing
productName: PakowanieApp
copyright: Copyright © 2024

directories:
  output: dist
  buildResources: resources

win:
  target:
    - target: portable
      arch:
        - x64
  icon: resources/icon.ico
  
portable:
  artifactName: ${productName}-${version}-portable.exe

files:
  - "**/*"
  - "!**/*.ts"
  - "!*.map"

extraResources:
  - from: "database/schema.sql"
    to: "schema.sql"

# Don't include auto-updater
publish: null
```

**webpack.config.js:**
```javascript
module.exports = {
  target: 'electron-renderer',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader']
      }
    ]
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js']
  }
};
```

### Building for Production

**Build Portable .exe:**
```bash
npm run build:portable

# Output:
# dist/PakowanieApp-1.0.0-portable.exe (~150-200 MB)
```

**Verify Build:**
```bash
# Test on development machine
./dist/PakowanieApp-1.0.0-portable.exe

# Check:
- Does it launch?
- Can it connect to scale?
- Can it read Excel files?
- Does database initialize?
```

**Create Distribution Package:**
```bash
# Create folder structure
mkdir PakowanieApp-v1.0.0
cd PakowanieApp-v1.0.0

# Copy executable
cp dist/PakowanieApp-1.0.0-portable.exe ./PakowanieApp.exe

# Add README
echo "Warehouse Packing Application v1.0.0" > README.txt
echo "Double-click PakowanieApp.exe to run" >> README.txt

# Compress
# Windows: Right-click → Send to → Compressed folder
# Result: PakowanieApp-v1.0.0.zip
```

### Transfer to Production

**Via Google Drive:**
```
1. Upload PakowanieApp-v1.0.0.zip to Google Drive
2. On production machine:
   - Download ZIP
   - Extract to Desktop or C:\Users\[USER]\AppData\Local\
   - Run PakowanieApp.exe
3. First run:
   - Configure COM port in Settings
   - Test scale connection
   - Set network drive path (if applicable)
```

---

## Testing Strategy

### Manual Testing Checklist

**1. Hardware Integration:**
```
□ Scale connection
  □ Auto-detect COM port
  □ Manual COM port selection
  □ Get weight (SI command)
  □ Zero (Z command)
  □ Tare (T command)
  □ Stable vs unstable reading detection
  □ Disconnection handling
  □ Reconnection after disconnect

□ QR Scanner
  □ Scan SAP index → finds part
  □ Scan unknown SAP → shows error
  □ Scan already packed → shows warning
  □ Rapid scanning (multiple scans)

□ Camera
  □ Permission request
  □ Live preview
  □ Capture photo
  □ Multiple photos per part
  □ Delete photo
  □ Compression works (file size ~400 KB)
```

**2. Core Workflows:**
```
□ Create Shipment
  □ Import Excel file
  □ Validate Excel format
  □ Handle missing columns error
  □ Configure data requirements
  □ Navigate to packing screen

□ Packing Flow (full cycle)
  □ Scan part
  □ Modal shows correct data
  □ Second scan confirms
  □ Weight measurement (if required)
    □ Wait for stable reading
    □ Auto-calculate per-unit weight
    □ Override quantity
  □ Country selection (if required)
    □ Quick select (1-7 keys)
    □ Search/filter
  □ Photo capture (if required)
    □ Take 1 photo
    □ Take multiple photos
    □ Keyboard shortcuts work
  □ Completion animation
  □ Part moves to "Packed" section
  □ Progress updates

□ Special Cases
  □ Pack all parts → completion modal
  □ Pause packing → resume later
  □ Save manually → autosave timestamp updates
  □ Close app mid-packing → resume on relaunch
```

**3. Reports:**
```
□ Generate PDF
  □ Correct data
  □ Readable formatting
  □ Photos included (if any)

□ Generate Excel
  □ Multiple sheets present
  □ Formulas work (if any)
  □ Data complete

□ Generate HTML
  □ Opens in browser
  □ Table sortable
  □ Photo gallery works
  □ Print-friendly

□ Export to network
  □ Files appear in correct folder
  □ Structure matches specification
  □ Photos in /photos/ subfolder
```

**4. Statistics:**
```
□ Stats update after each shipment
□ Achievement unlocks trigger
□ Popup shows correctly
□ Stats persist across app restarts
```

**5. Settings:**
```
□ Save settings → persist after restart
□ COM port change → scale reconnects
□ Network path change → next export uses new path
□ Voice toggle → feedback stops/starts
□ Theme change → UI updates
```

### Automated Testing (Optional)

**Unit Tests (Jest):**
```typescript
// Example: services/ScaleService.test.ts
describe('ScaleService', () => {
  it('should parse stable reading correctly', () => {
    const reading = 'S + 12.345 kg\r\n';
    const result = ScaleService.parseReading(reading);
    expect(result.stable).toBe(true);
    expect(result.value).toBe(12.345);
    expect(result.unit).toBe('kg');
  });
  
  it('should detect unstable reading', () => {
    const reading = 'US + 12.345 kg\r\n';
    const result = ScaleService.parseReading(reading);
    expect(result.stable).toBe(false);
  });
});
```

---

## Troubleshooting Guide

### Common Issues & Solutions

**Issue: Scale not detected**
```
Symptoms: COM port list empty, or scale doesn't respond

Solutions:
1. Check physical connection (USB cable, Moxa adapter)
2. Verify in Device Manager (Windows):
   - Device Manager → Ports (COM & LPT)
   - Should see "USB Serial Port (COMX)"
3. Try different USB port
4. Restart app after connecting scale
5. Manually enter COM port number in Settings
6. Check if other software is using the port (close it)
```

**Issue: QR scanner not working**
```
Symptoms: Scanning doesn't trigger search

Solutions:
1. Verify scanner is in keyboard wedge mode (not USB HID)
2. Test scanner in Notepad (should type text)
3. Ensure search input field is focused (click it)
4. Check if scanner appends Enter key (required)
5. Try manual typing to verify input field works
```

**Issue: Camera permission denied**
```
Symptoms: Black screen instead of camera preview

Solutions:
1. Check Windows permissions:
   - Settings → Privacy → Camera
   - Enable for desktop apps
2. Check antivirus (may block camera access)
3. Try restarting app
4. Use external USB camera if built-in blocked
```

**Issue: Excel import fails**
```
Symptoms: Error when selecting Excel file

Solutions:
1. Verify file is .xlsx or .xls (not .csv)
2. Check required columns exist:
   - SAP Index, Description, Quantity, Unit
3. Ensure no merged cells in header row
4. Try opening file in Excel (verify it's not corrupted)
5. Save as new .xlsx file (File → Save As → Excel Workbook)
```

**Issue: Network export fails**
```
Symptoms: Files not appearing on network drive

Solutions:
1. Verify network path is accessible:
   - Open File Explorer → type path (e.g., Z:\Pakowanie)
   - Can you create a file there manually?
2. Check path format in Settings:
   - Windows: Z:\Pakowanie\Wysyłki
   - UNC: \\server\share\Pakowanie\Wysyłki
3. Ensure you have write permissions
4. Check if network drive is mapped (Map Network Drive)
5. Files saved locally even if network fails:
   - Check: C:\Users\[USER]\AppData\Local\PakowanieApp\exports\
```

**Issue: App won't start (Windows SmartScreen)**
```
Symptoms: "Windows protected your PC" message

Solutions:
1. Click "More info"
2. Click "Run anyway"
3. For future: right-click .exe → Properties → Unblock
```

**Issue: Database error on launch**
```
Symptoms: "Cannot open database" error

Solutions:
1. Check if database file is locked (close other instances)
2. Verify AppData folder is writable
3. Delete database file to reset (WARNING: loses all data):
   - C:\Users\[USER]\AppData\Local\PakowanieApp\data\database.db
4. App will recreate database on next launch
```

**Issue: Photos too large (disk space)**
```
Symptoms: Running out of space quickly

Solutions:
1. Check compression is working:
   - Photos should be ~400 KB each
   - If larger, compression may be failing
2. Clean up old exports:
   - Delete exports older than 3 months
   - Or run cleanup job in Settings
3. Reduce photo resolution in code (if needed)
4. Store photos on network drive instead of locally
```

---

## Performance Optimization

### Database Optimization

**Indexes:**
```sql
-- Already in schema, but verify they exist:
CREATE INDEX IF NOT EXISTS idx_parts_shipment ON parts(shipment_id);
CREATE INDEX IF NOT EXISTS idx_parts_status ON parts(status);
CREATE INDEX IF NOT EXISTS idx_photos_part ON photos(part_id);
CREATE INDEX IF NOT EXISTS idx_shipments_status ON shipments(status);
CREATE INDEX IF NOT EXISTS idx_shipments_date ON shipments(created_date);
```

**Query Optimization:**
```typescript
// Bad: Load all photos at once
const photos = await db.all('SELECT * FROM photos WHERE part_id = ?', [partId]);

// Good: Load thumbnails first, full photos on demand
const thumbnails = await db.all(
  'SELECT id, thumbnail_data FROM photos WHERE part_id = ?',
  [partId]
);
// Later, when user clicks:
const fullPhoto = await db.get(
  'SELECT photo_data FROM photos WHERE id = ?',
  [photoId]
);
```

**Connection Pooling:**
```typescript
// Use single database connection throughout app lifecycle
// Don't open/close for each query
class DatabaseService {
  private db: Database;
  
  constructor() {
    this.db = new Database(DB_PATH);
    this.db.pragma('journal_mode = WAL'); // Better concurrency
  }
  
  // Reuse this.db for all queries
}
```

### UI Performance

**Virtual Scrolling (for large shipments):**
```typescript
// For shipments with 200+ parts, use react-window
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={parts.length}
  itemSize={80}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>
      <PartCard part={parts[index]} />
    </div>
  )}
</FixedSizeList>
```

**Debounce Search:**
```typescript
const [searchQuery, setSearchQuery] = useState('');
const debouncedSearch = useMemo(
  () => debounce((query: string) => {
    // Perform search
    const results = searchParts(query);
    setFilteredParts(results);
  }, 300),
  []
);

useEffect(() => {
  debouncedSearch(searchQuery);
}, [searchQuery]);
```

**Lazy Load Images:**
```typescript
// Don't load all photos at once
<img
  src={thumbnailUrl}
  loading="lazy"
  onClick={() => loadFullImage(photoId)}
/>
```

### Memory Management

**Photo Storage Strategy:**
```typescript
// Store photos in separate files, not in database BLOB
// Database: Store file paths
// File system: Store actual JPEGs

// Good for large photos (>1 MB)
const photoPath = path.join(PHOTOS_DIR, `${partId}_${timestamp}.jpg`);
await fs.writeFile(photoPath, compressedPhoto);
await db.run(
  'INSERT INTO photos (part_id, photo_path) VALUES (?, ?)',
  [partId, photoPath]
);

// Load on demand
const photoData = await fs.readFile(photoPath);
```

**Cleanup Old Autosaves:**
```typescript
// Keep only last 10 autosaves per shipment
async cleanupAutosaves(shipmentId: number) {
  await db.run(`
    DELETE FROM autosaves
    WHERE shipment_id = ?
    AND id NOT IN (
      SELECT id FROM autosaves
      WHERE shipment_id = ?
      ORDER BY created_at DESC
      LIMIT 10
    )
  `, [shipmentId, shipmentId]);
}
```

---

## Security Considerations

### Data Protection

**Sensitive Data:**
```
✅ Safe to store locally:
- SAP indexes
- Part descriptions
- Quantities
- Weights
- Countries of origin
- Photos of parts

⚠️ Don't store:
- User passwords (use Windows authentication if needed)
- Personal employee data (names OK, IDs not)
- Financial data (prices, costs)
```

**Database Encryption (Optional):**
```typescript
// If needed, use SQLCipher instead of SQLite
// Adds encryption at rest
import Database from 'better-sqlite3';
const db = new Database('database.db');
db.pragma('key="your-encryption-key"');
```

### Network Security

**File Transfer:**
```typescript
// Use SMB (Windows native) for network drive
// Already encrypted if network is trusted

// For internet transfer (optional):
// Use HTTPS only, never HTTP
fetch('https://api.example.com/upload', {
  method: 'POST',
  body: formData,
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

### Input Validation

**Sanitize User Input:**
```typescript
function sanitizeInput(input: string): string {
  // Remove SQL injection attempts
  return input.replace(/['";\\]/g, '');
}

// Use parameterized queries (already doing this)
db.run('SELECT * FROM parts WHERE sap_index = ?', [sanitizedInput]);
```

**Validate File Paths:**
```typescript
function validatePath(userPath: string): boolean {
  // Prevent directory traversal
  const resolved = path.resolve(userPath);
  const allowed = path.resolve(EXPORTS_DIR);
  return resolved.startsWith(allowed);
}
```

---

## Maintenance & Updates

### Version Numbering

```
Format: MAJOR.MINOR.PATCH (Semantic Versioning)

Examples:
1.0.0 - Initial release
1.0.1 - Bug fix (scale reconnection)
1.1.0 - New feature (statistics dashboard)
2.0.0 - Breaking change (database schema change)
```

### Update Process

**For Bug Fixes:**
```
1. Fix code on development machine
2. Test thoroughly
3. Increment PATCH version (1.0.0 → 1.0.1)
4. Build new portable .exe
5. Upload to Google Drive as "PakowanieApp-v1.0.1.zip"
6. Notify users (email/Slack)
7. Users download and replace .exe
   (Data preserved - same database)
```

**For New Features:**
```
1. Develop feature
2. Update database schema if needed (with migration)
3. Increment MINOR version (1.0.1 → 1.1.0)
4. Build and distribute
5. On first launch: run database migrations
```

**Database Migrations:**
```typescript
// main/database.ts
const MIGRATIONS = [
  {
    version: 1,
    sql: `
      CREATE TABLE shipments (...);
      CREATE TABLE parts (...);
    `
  },
  {
    version: 2,
    sql: `
      ALTER TABLE parts ADD COLUMN excel_row_number INTEGER;
    `
  }
];

function runMigrations(db: Database) {
  const currentVersion = db.pragma('user_version', { simple: true });
  
  for (const migration of MIGRATIONS) {
    if (migration.version > currentVersion) {
      db.exec(migration.sql);
      db.pragma(`user_version = ${migration.version}`);
    }
  }
}
```

### Backup Strategy

**Automatic Backups:**
```typescript
// On shipment completion, create backup
async backupDatabase(shipmentId: number) {
  const timestamp = Date.now();
  const backupPath = path.join(
    BACKUPS_DIR,
    `backup_${shipmentId}_${timestamp}.db`
  );
  
  await fs.copyFile(DB_PATH, backupPath);
  
  // Clean old backups (keep last 30 days)
  this.cleanOldBackups();
}
```

**Manual Backup:**
```
Settings → Advanced → Backup Database
→ Creates copy of database.db in exports folder
```

### Log Files

**Logging Strategy:**
```typescript
// Use electron-log or winston
import log from 'electron-log';

// Levels: error, warn, info, debug
log.error('Scale connection failed', error);
log.info('Shipment completed', { id: shipmentId });
log.debug('QR scanned', { sap: sapIndex });

// Logs stored in:
// Windows: C:\Users\[USER]\AppData\Roaming\PakowanieApp\logs\
```

**Log Rotation:**
```typescript
log.transports.file.maxSize = 10 * 1024 * 1024; // 10 MB
log.transports.file.maxFiles = 5; // Keep last 5 files
```

---

## Future Enhancements (Ideas)

**Phase 2 Features:**
1. **Email Notifications**
   - Send email on shipment completion
   - Attach PDF report
   - Configurable recipients

2. **Barcode Printing**
   - Generate labels for parts without QR
   - Print on Zebra thermal printer
   - Include SAP index, description, quantity

3. **Multi-User Sync**
   - Central database (PostgreSQL/MySQL)
   - Real-time updates
   - Concurrent packing (different shipments)

4. **Mobile App**
   - React Native companion
   - Scan QR with phone camera
   - Lightweight packing interface

5. **Advanced Analytics**
   - Dashboard with charts
   - Packing trends over time
   - Efficiency metrics
   - Bottleneck identification

6. **Integration with SAP**
   - Auto-import parts from SAP
   - Update SAP after shipment completion
   - Real-time inventory sync

7. **Voice Commands**
   - "Spakuj" → confirm packing
   - "Waga" → read weight
   - "Następny" → next part

8. **Smart Packing Suggestions**
   - Optimal packing order
   - Group heavy items
   - Alert if weight distribution uneven

---

## Development Best Practices

### Code Style

**TypeScript:**
```typescript
// Use interfaces for data structures
interface Part {
  id: number;
  sapIndex: string;
  description: string;
  quantity: number;
  unit: string;
}

// Use enums for constants
enum PackingStatus {
  Pending = 'pending',
  Packed = 'packed'
}

// Use descriptive names
function calculateWeightPerUnit(totalWeight: number, quantity: number): number {
  return totalWeight / quantity;
}
```

**React Components:**
```typescript
// Use functional components with hooks
const PartCard: React.FC<{ part: Part; onPack: () => void }> = ({ part, onPack }) => {
  return (
    <div onClick={onPack}>
      {part.sapIndex} - {part.description}
    </div>
  );
};

// Extract complex logic to custom hooks
function useScaleConnection() {
  const [connected, setConnected] = useState(false);
  
  useEffect(() => {
    scaleService.connect()
      .then(() => setConnected(true))
      .catch(() => setConnected(false));
  }, []);
  
  return connected;
}
```

**Error Handling:**
```typescript
// Always handle errors gracefully
try {
  await riskyOperation();
} catch (error) {
  log.error('Operation failed', error);
  showUserFriendlyError(error);
  // Don't crash the app
}
```

### Git Workflow (Optional)

```bash
# Main branch: stable releases
git checkout main

# Development branch: ongoing work
git checkout -b develop

# Feature branches
git checkout -b feature/photo-capture

# Commit messages
git commit -m "feat: add photo capture functionality"
git commit -m "fix: scale reconnection after disconnect"
git commit -m "docs: update README with setup instructions"
```

### Documentation

**Code Comments:**
```typescript
/**
 * Waits for a stable weight reading from the Radwag scale.
 * Polls the scale every 200ms until a reading with 'S' prefix is received.
 * 
 * @param timeout - Maximum time to wait in milliseconds (default: 30000)
 * @returns Promise that resolves with stable weight reading
 * @throws Error if timeout is reached or scale disconnects
 */
async waitForStableReading(timeout: number = 30000): Promise<WeightReading> {
  // Implementation...
}
```

**README.md:**
```markdown
# Warehouse Packing Application

Desktop application for efficient warehouse packing operations.

## Features
- QR code scanning
- Weight measurement (Radwag scale)
- Photo capture
- Report generation (PDF, Excel, HTML)

## Setup
1. Install Node.js 20.11.0
2. Run `npm install`
3. Run `npm run dev` for development
4. Run `npm run build:portable` for production

## Hardware
- Radwag WLC scale (RS-232)
- QR scanner (keyboard wedge mode)
- Webcam or USB camera

## Usage
See USER_GUIDE.md for detailed instructions.
```

---

## Contact & Support

**For Claude Code:**
- Follow this guide step-by-step
- Start with core features (shipment creation, packing flow)
- Add hardware integration second (scale, camera)
- Add nice-to-have features last (statistics, voice)

**Development Priority:**
1. ✅ Database setup + basic UI
2. ✅ Shipment creation + Excel import
3. ✅ Packing screen + QR scanning
4. ✅ Weight measurement (scale integration)
5. ✅ Report generation (PDF, Excel)
6. ✅ Photo capture
7. ✅ Country selection
8. ✅ Statistics & achievements
9. ✅ Voice feedback
10. ✅ Network export

**Questions to ask if stuck:**
- "How do I structure the Electron IPC communication?"
- "Show me how to parse the Excel file with exceljs"
- "How do I implement the scale service with serialport?"
- "Create the packing screen component with all animations"
- "Generate the PDF report with jspdf"

**Remember:**
- Build incrementally
- Test each feature before moving on
- Use TypeScript for type safety
- Keep UI/UX smooth and responsive
- Handle errors gracefully
- Log everything for debugging

---

## Summary

This is a **comprehensive guide** for building a professional warehouse packing application. The app should:

✅ Work offline (local SQLite database)
✅ Integrate with Radwag scale (RS-232 protocol)
✅ Support QR scanning (keyboard wedge)
✅ Capture and compress photos
✅ Generate beautiful reports (PDF, Excel, HTML)
✅ Have Spotify-level UI/UX (smooth animations, modern design)
✅ Be portable (no installation, no admin rights)
✅ Export to network drive automatically
✅ Include statistics and achievements (gamification)
✅ Provide voice feedback (Polish text-to-speech)

**Tech Stack:**
- Electron 33 + React 18 + TypeScript 5
- SQLite (better-sqlite3)
- Tailwind CSS (styling)
- serialport (scale communication)
- exceljs, jspdf, sharp (reports & images)

**Target Environment:**
- Windows 11 laptops
- 2-3 packing stations
- 5-10 shipments per day
- 50-150 parts per shipment

**Key Success Factors:**
1. Reliable hardware integration (scale, scanner)
2. Smooth, intuitive UI/UX
3. Fast performance (even with 200+ parts)
4. Robust error handling
5. Easy updates and maintenance

Good luck! 🚀
