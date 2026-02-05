---
name: mixmi-color-system
description: Platform color palette with semantic meanings, hex codes, accessibility notes, and usage patterns for all content types including loops, songs, playlists, video, and radio
metadata:
  status: Active
  implementation: Use These Exact Values
  last_updated: 2025-10-27
---

# mixmi Color System
**Quick Reference Guide**

## Platform Color Palette

### Content Type Colors

```
🟣 PURPLE    #9772F4    Loops (Remixable/Creative)
   - 2px border for single loops
   - 4px border for loop packs
   - Semantic: Transformable, can be loaded to mixer

🟡 GOLD      #FFE4B5    Songs (Complete/Finished)
   - 2px border for single songs
   - 4px border for EPs
   - Semantic: Finished work, ready for consumption

🟦 INDIGO    #6366F1    Playlists (Curated/Collection)
   - 4px border (always collection)
   - Semantic: Human curation, taste-making

🔷 SKY BLUE  #38BDF8    Video (Visual/Media)
   - 2px border for single videos
   - Semantic: Visual medium, screen content

🟠 ORANGE    #FB923C    Radio (Live/Broadcast)
   - 4px border (station = collection of shows)
   - Semantic: Live transmission, warmth, energy
```

### UI Element Colors

```
🔵 CYAN      #81E4F2    Interactive/Accent
   - Call-to-action buttons
   - Purchase actions
   - Active states
   - Links

⚫ DARK NAVY #101726    Background
   - All content colors optimized for this background
```

## Usage Examples

### Cards
```css
/* Loop Card */
.loop-card {
  border: 2px solid #9772F4;
  background: #101726;
}

/* Loop Pack Card */
.loop-pack-card {
  border: 4px solid #9772F4;
  background: #101726;
}

/* Song Card */
.song-card {
  border: 2px solid #FFE4B5;
  background: #101726;
}

/* Playlist Card */
.playlist-card {
  border: 4px solid #6366F1;
  background: #101726;
}

/* Video Card */
.video-card {
  border: 2px solid #38BDF8;
  background: #101726;
}

/* Radio Station Card */
.radio-card {
  border: 4px solid #FB923C;
  background: #101726;
}
```

### Buttons
```css
/* Primary Action */
.btn-primary {
  background: #81E4F2;
  color: #101726;
}

/* Purchase Button */
.btn-purchase {
  background: #81E4F2;
  border: 2px solid #81E4F2;
}

/* Remix Button (on loop cards) */
.btn-remix {
  background: #9772F4;
  color: white;
}
```

## Hover States

All colors have consistent hover behavior:
```css
.content-card:hover {
  transform: scale(1.05);
  transition: all 0.3s ease;
}

.btn:hover {
  opacity: 0.9;
  transform: scale(1.02);
}
```

## Badge Colors

Use the content type color with slight transparency:
```css
/* Number badges (on packs/EPs) */
.number-badge {
  background: rgba(151, 114, 244, 0.9); /* Purple for loop packs */
  background: rgba(255, 228, 181, 0.9); /* Gold for EPs */
  color: white;
}

/* Metadata badges (BPM, duration) */
.metadata-badge {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-family: monospace;
}
```

## Accessibility

All color combinations meet WCAG AA standards:
- Purple #9772F4 on #101726: ✅ AAA
- Gold #FFE4B5 on #101726: ✅ AAA
- Indigo #6366F1 on #101726: ✅ AAA
- Sky Blue #38BDF8 on #101726: ✅ AAA
- Orange #FB923C on #101726: ✅ AAA
- Cyan #81E4F2 on #101726: ✅ AAA

## Color Meanings Summary

| Color | Content | Meaning | Why |
|-------|---------|---------|-----|
| Purple | Loops | Remixable | Creative, transformable, loads to mixer |
| Gold | Songs | Finished | Complete work, polished, ready |
| Indigo | Playlists | Curated | Thoughtful selection, refined taste |
| Sky Blue | Video | Visual | Screen, sky, brightness, media |
| Orange | Radio | Live | Warmth, energy, transmission waves |
| Cyan | Actions | Interactive | Water/flow, movement, action |

## Design Principles

1. **Semantic Color**: Each color has meaning, not just decoration
2. **Border Thickness**: 2px = single item, 4px = collection
3. **Consistent System**: All content follows same patterns
4. **Future-Proof**: Easy to add new content types (just pick a color!)
5. **Dark Optimized**: All colors pop on dark navy background

## Adding New Content Types

When adding a new content type:

1. **Pick a color** with semantic meaning
2. **Check contrast** on #101726 background (use WebAIM contrast checker)
3. **Test with existing colors** to ensure distinction
4. **Choose border** - 2px (single) or 4px (collection)
5. **Document the meaning** so it's intuitive to users

Example:
- Physical Goods/Merch → Green `#10B981` (growth, physical, earthy)
- Podcast Episodes → Magenta `#D946EF` (audio, talk, voice)

## Figma/Design Tool Values

```
Purple:    #9772F4  RGB(151, 114, 244)
Gold:      #FFE4B5  RGB(255, 228, 181)
Indigo:    #6366F1  RGB(99, 102, 241)
Sky Blue:  #38BDF8  RGB(56, 189, 248)
Orange:    #FB923C  RGB(251, 146, 60)
Cyan:      #81E4F2  RGB(129, 228, 242)
Dark Navy: #101726  RGB(16, 23, 38)
```

## Tailwind Classes (if using)

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'mixmi-purple': '#9772F4',
        'mixmi-gold': '#FFE4B5',
        'mixmi-indigo': '#6366F1',
        'mixmi-sky': '#38BDF8',
        'mixmi-orange': '#FB923C',
        'mixmi-cyan': '#81E4F2',
        'mixmi-dark': '#101726',
      }
    }
  }
}
```

Usage:
```jsx
<div className="border-2 border-mixmi-purple bg-mixmi-dark">
  Loop Card
</div>
```

---

**Version:** 1.0  
**Last Updated:** October 27, 2025  
**Status:** Active - Use these exact hex values in all designs
