---
name: mixmi-component-library
description: Component specifications, design patterns, and UI elements for the mixmi platform including TrackCard, grids, modals, and audio components
metadata:
  status: Active
  implementation: React + TypeScript - Alpha
  last_updated: 2025-10-26
---

# mixmi Component Library

> Comprehensive documentation of all UI components, design patterns, and interactive elements in the mixmi platform.

## Core Display Components

### TrackCard
**File:** `components/TrackCard.tsx`
**Size:** 160px × 160px square

#### Structure
- **Front (Default State):**
  - Cover image (full bleed)
  - Gradient overlay at bottom
  - Track title (truncated if long)
  - Artist name
  - Price badge (if applicable)
  - Track type icon (loop/song/pack/EP)

- **Hover State:**
  - Darkened overlay
  - Control buttons appear:
    - Play button (center)
    - Add to cart (top right)
    - Info button (bottom right)
  - Subtle scale animation (1.02x)

#### Props
```typescript
interface TrackCardProps {
  track: Track;
  size?: 'small' | 'medium' | 'large'; // 120px, 160px, 200px
  showPrice?: boolean;
  showControls?: boolean;
  onClick?: () => void;
  onPlay?: () => void;
  onAddToCart?: () => void;
  onInfo?: () => void;
}
```

#### Visual States
- Default (static display)
- Hover (shows controls)
- Playing (animated border)
- Loading (skeleton)
- Error (fallback image)
- Selected (highlighted border)

### ContentGrid
**File:** `components/ContentGrid.tsx`
**Layout:** Responsive grid of TrackCards

#### Grid Configuration
- **Desktop:** 6-7 columns
- **Tablet:** 4-5 columns  
- **Mobile:** 2-3 columns
- **Gap:** 16px (1rem)
- **Padding:** 24px container padding

#### Features
- Virtualization for large lists
- Lazy loading images
- Responsive breakpoints
- Filter/sort controls
- Empty state handling

### CreatorHeader
**File:** `components/CreatorHeader.tsx`
**Height:** 240px banner + 80px info bar

#### Elements
- Background image/gradient
- Avatar (120px circle)
- Creator name
- Wallet address (truncated)
- Stats (tracks, plays, earnings)
- Follow button
- Share button

### FilterTabs
**File:** `components/FilterTabs.tsx`

#### Tab Options
- All (total count)
- Loops (8-bar)
- Loop Packs (2-5 loops)
- Songs (full tracks)
- EPs (2-5 songs)

#### Visual Design
- Active tab: Purple background
- Inactive: Transparent with border
- Count badges on each tab
- Smooth transitions between states

## Modal Components

### TrackDetailsModal
**File:** `components/TrackDetailsModal.tsx`
**Size:** 800px max-width, 90vh max-height

#### Sections
1. **Header:**
   - Cover image (large)
   - Title and artist
   - Play controls
   - Close button

2. **Metadata Tabs:**
   - Details (BPM, key, duration, location)
   - Credits (attribution splits)
   - License (terms and pricing)
   - Source (for remixes)

3. **Actions:**
   - Download/Purchase button
   - Add to cart
   - Share
   - Report

### PaymentModal
**File:** `components/mixer/PaymentModal.tsx`
**Size:** 500px width

#### Flow Steps
1. **Remix Preview:**
   - Waveform visualization
   - 8-bar selection
   - Play preview button

2. **Attribution Setup:**
   - Title input
   - Artist name
   - Cover image upload

3. **Payment Breakdown:**
   - Source tracks (2 × 1 STX)
   - Total: 2 STX
   - Recipient list with percentages

4. **Wallet Connection:**
   - Connect button (if needed)
   - Balance display
   - Insufficient funds warning

5. **Confirmation:**
   - Processing spinner
   - Success animation
   - Transaction link

## Audio Components

### AudioPlayer
**File:** `components/AudioPlayer.tsx`
**Position:** Fixed bottom bar or inline

#### Controls
- Play/pause button
- Progress bar (draggable)
- Time display (current/total)
- Volume slider
- Track info display
- Next/previous (in playlists)

### WaveformDisplay
**File:** `components/WaveformDisplay.tsx`
**Powered by:** Wavesurfer.js

#### Features
- Real-time rendering
- Zoom controls
- Region selection
- Playhead position
- Loading state
- Error fallback

### DJMixer Interface
**File:** `components/mixer/DJMixer.tsx`

#### Channel Strip Components
- Volume fader (vertical)
- EQ knobs (high/mid/low)
- Gain control
- Cue button
- Load track button
- Track info display
- Waveform preview

#### Crossfader
- Horizontal slider
- A/B channel assignment
- Curve adjustment
- Cut buttons

## Form Components

### FileUpload
**File:** `components/FileUpload.tsx`

#### Features
- Drag and drop zone
- File type validation
- Progress indication
- Multiple file support
- Preview generation
- Size limits display

### SplitInput
**File:** `components/SplitInput.tsx`

#### Attribution Percentage Inputs
- Wallet address field
- Percentage slider/input
- Auto-calculation to 100%
- Add/remove contributors
- Validation messages
- TBD wallet option

### LocationPicker
**File:** `components/LocationPicker.tsx`

#### Interface
- Map view (Mapbox)
- Search bar
- Pin placement
- Coordinate display
- Named location input
- GPS auto-detect button

## Navigation Components

### TopNavigation
**File:** `components/Navigation.tsx`
**Height:** 64px

#### Elements
- Logo (left)
- Main nav links (center):
  - Globe
  - Mixer
  - Upload
  - Welcome
- User menu (right):
  - Avatar
  - Wallet connection
  - Settings dropdown

### MobileDrawer
**File:** `components/MobileDrawer.tsx`

#### Trigger: Hamburger menu
#### Content:
- User profile section
- Navigation links
- Settings
- Logout

## Utility Components

### LoadingStates
- **Skeleton:** Placeholder shapes
- **Spinner:** Circular loader
- **ProgressBar:** Linear progress
- **Shimmer:** Animated placeholder

### EmptyStates
- Icon illustration
- Descriptive text
- Action button (optional)
- Consistent styling across app

### ToastNotifications
**Position:** Top-right corner
**Types:**
- Success (green)
- Error (red)
- Warning (yellow)
- Info (blue)
**Auto-dismiss:** 5 seconds

## Design System

### Colors
```css
--primary: #8B5CF6; /* Purple */
--secondary: #EC4899; /* Pink */
--background: #0F0F0F; /* Near black */
--surface: #1A1A1A; /* Dark gray */
--text-primary: #FFFFFF;
--text-secondary: #A0A0A0;
--success: #10B981;
--error: #EF4444;
--warning: #F59E0B;
```

### Typography
- **Font:** System font stack
- **Headings:** Bold, 1.5-2.5rem
- **Body:** Regular, 0.875-1rem
- **Small:** 0.75-0.875rem

### Spacing Scale
- 4px (0.25rem)
- 8px (0.5rem)
- 16px (1rem)
- 24px (1.5rem)
- 32px (2rem)
- 48px (3rem)

### Border Radius
- Small: 4px
- Default: 8px
- Large: 16px
- Full: 9999px (circles)

### Shadows
- sm: 0 1px 2px rgba(0,0,0,0.05)
- md: 0 4px 6px rgba(0,0,0,0.1)
- lg: 0 10px 15px rgba(0,0,0,0.1)
- xl: 0 20px 25px rgba(0,0,0,0.1)

### Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

### Animation Timings
- Fast: 150ms
- Normal: 200ms
- Slow: 300ms
- Easing: cubic-bezier(0.4, 0, 0.2, 1)

## Interactive Patterns

### Hover Behaviors
- Buttons: Brightness increase
- Cards: Scale 1.02x + shadow
- Links: Underline appears
- All: 200ms transition

### Click Feedback
- Buttons: Scale 0.95x
- Cards: Brief highlight
- Ripple effect (Material-style)

### Loading Patterns
- Skeleton for layouts
- Spinner for actions
- Progress for uploads
- Shimmer for content

### Error Handling
- Inline validation messages
- Toast notifications
- Fallback UI components
- Retry mechanisms

## Accessibility Features

### Keyboard Navigation
- Tab order logical
- Focus indicators visible
- Skip links available
- Escape closes modals

### Screen Reader Support
- ARIA labels
- Role attributes
- Live regions for updates
- Semantic HTML

### Color Contrast
- WCAG AA compliant
- High contrast mode support
- Color-blind friendly palette

### Interactive Targets
- Minimum 44×44px touch targets
- Adequate spacing
- Clear hover states

---

*Component library version: 1.0.0*
*Last updated: October 2024*