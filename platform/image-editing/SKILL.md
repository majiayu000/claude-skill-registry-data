---
name: image-editing
description: Use when editing and enhancing images for Xiaohongshu content, improving photo quality with filters and adjustments, creating visually appealing images, or preparing images for carousel posts
---

# Image Editing (图片编辑)

## Overview

Image editing is the process of enhancing, retouching, and transforming photos for Xiaohongshu content using mobile editing apps to create visually appealing, professional-looking images that attract attention and convey information effectively.

## When to Use

**Use when**:
- Preparing photos for Xiaohongshu posts
- Enhancing image quality (brightness, colors, sharpness)
- Creating before/after comparisons
- Adding text overlays and graphics
- Fixing photo issues (poor lighting, blemishes)
- Creating cohesive visual style across content

**Do NOT use when**:
- Image quality is already excellent (don't over-edit)
- Creating misleading edits (false before/after)
- Editing makes photo look unnatural (presets too heavy)

## Core Pattern

**Before** (unedited photos):
```
❌ "Posted raw photos, dull lighting, poor colors"
❌ "No consistent style, images look amateur"
❌ "Blemishes and imperfections visible"
❌ "Photos don't match aesthetic of account"
❌ "Low engagement on image posts"
```

**After** (professionally edited):
```
✅ "Consistent editing style, all photos cohesive"
✅ "Enhanced colors and lighting, photos pop"
✅ "Professional look, higher perceived quality"
✅ "Branded aesthetic, followers recognize my style"
✅ "Before/after edits show transformations clearly"
✅ "Engagement increased 40% after improving image quality"
```

**5 Image Editing Elements**:
1. **Basic Adjustments** - Exposure, brightness, contrast, saturation
2. **Color Correction** - Temperature, tint, vibrance, color grading
3. **Retouching** - Blemish removal, skin smoothing, body shaping
4. **Creative Effects** - Filters, presets, blurs, vignettes
5. **Text and Graphics** - Overlays, stickers, frames, watermarks

## Quick Reference

| Editing Tool | Best For | Learning Curve | Platform |
|--------------|----------|----------------|----------|
| **Xingtu (醒图)** | All-purpose editing | Low | iOS, Android |
| **Meitu (美图秀秀)** | Beauty retouching | Low | iOS, Android |
| **Snapseed** | Professional adjustments | Medium | iOS, Android |
| **Canva** | Text and graphics | Low | iOS, Android, Web |
| **Lightroom Mobile** | Color grading, presets | Medium-High | iOS, Android |

## Implementation

### Step 1: Master Basic Adjustments

**Fundamental Photo Enhancements**:
```
Basic Adjustments Framework:

1. Exposure and Brightness
   Purpose: Fix lighting issues

   Overexposed (too bright):
   - Decrease exposure: -0.3 to -0.7
   - Decrease highlights: -20 to -50
   - Result: Recover blown-out details

   Underexposed (too dark):
   - Increase exposure: +0.3 to +0.7
   - Increase shadows: +20 to +50
   - Result: Brighten dark areas

   Pro Tip:
   ✅ Use histogram (if available)
   ✅ Aim for balanced distribution (not clipped)
   ✅ Check for blown highlights (red areas in preview)

2. Contrast and Tone
   Purpose: Add depth and dimension

   Low Contrast (flat, dull):
   - Increase contrast: +10 to +30
   - Increase highlights: +10 to +20
   - Decrease shadows: -10 to -20
   - Result: More dynamic range

   High Contrast (harsh):
   - Decrease contrast: -10 to -20
   - Increase shadows: +10 to +20
   - Result: Softer, more balanced

   Rule of Thumb:
   Most photos benefit from: Contrast +15

3. Saturation and Vibrance
   Purpose: Enhance or mute colors

   Boost Colors:
   - Increase vibrance: +15 to +30 (skin-safe)
   - Increase saturation: +10 to +20 (cautiously)
   - Result: Richer, more appealing colors

   Mute Colors (muted aesthetic):
   - Decrease saturation: -10 to -30
   - Increase brightness: +5 to +10
   - Result: Soft, minimal look

   Pro Tip:
   ✅ Use vibrance first (skin-safe)
   ✅ Use saturation sparingly (can oversaturate skin)
   ✅ Match aesthetic to niche (bright for lifestyle, muted for fashion)

4. Sharpness and Clarity
   Purpose: Enhance details and edges

   Soft Photo (lacked focus):
   - Increase sharpness: +20 to +40
   - Increase clarity: +10 to +20
   - Result: Crisper details

   Over-Sharp (harsh edges):
   - Decrease sharpness: -10 to -20
   - Decrease clarity: -10 to -20
   - Result: Softer look

   Pro Tip:
   ✅ Apply sharpening last (after all other edits)
   ✅ Zoom to 100% to check for halos (oversharpening)
   ✅ Less is more (subtle sharpness looks more natural)

Basic Adjustments Recipe (Starting Point):
- Exposure: 0 (adjust based on lighting)
- Brightness: +5 (slight brighten)
- Contrast: +15 (add depth)
- Warmth: +5 (slight warmth, flattering)
- Saturation: +10 (color boost)
- Vibrance: +20 (skin-safe color boost)
- Sharpness: +25 (crisp details)
- Clarity: +10 (subtle definition)
```

### Step 2: Apply Color Grading

**Create Consistent Aesthetic**:
```
Color Grading Techniques:

1. Temperature and Tint
   Temperature (Warmth):
   - Cool (blue): -10 to -20 (clinical, modern)
   - Warm (yellow): +10 to +20 (cozy, friendly)

   Best for Skincare/Beauty:
   ✅ Warmth +5 to +15 (flattering skin tones)

   Best for Fashion:
   ⚪ Cool -5 to -15 (editorial look)

   Tint (Green-Magenta):
   - Most photos: 0 (neutral)
   - Correct color cast: -5 to +5
   - Creative: Adjust for mood

2. HSL (Hue, Saturation, Luminance)
   Hue (Color Color):
   - Shift specific colors (red → orange)
   - Creative: Change color palette
   - Example: Shift blue to teal for aesthetic

   Saturation (Color Intensity):
   - Boost specific colors: +10 to +30
   - Mute specific colors: -10 to -30
   - Example: Boost orange (skin flattering), mute green

   Luminance (Color Brightness):
   - Brighten specific colors: +10 to +30
   - Darken specific colors: -10 to -30
   - Example: Darken blue sky for drama

   Common HSL Adjustments:
   ✅ Orange (skin): Saturation +10, Luminance +5
   ✅ Blue (sky): Saturation +20, Luminance +10
   ✅ Green (nature): Saturation -10 (muted look)

3. Curves (Advanced)
   Purpose: Precise tonal control

   S-Curve (Contrast Boost):
   - Shadows: Lower left point slightly down
   - Highlights: Upper right point slightly up
   - Result: More contrast, pop

   Brighten Midtones:
   - Lift middle of curve upward
   - Result: Brighter image without blowing highlights

   Darken Highlights:
   - Lower upper part of curve
   - Result: Recover bright areas

   Pro Tip:
   ✅ Subtle curves adjustments (5-10 points)
   ✅ Avoid extreme curves (unnatural look)
   ✅ Use histogram as guide

4. Color Grading (Split Toning)
   Purpose: Creative color in highlights/shadows

   Warm Highlights, Cool Shadows:
   - Highlights: Yellow/orange, 10-20% saturation
   - Shadows: Blue, 10-20% saturation
   - Result: Cinematic, dimensional look

   Matching Popular Aesthetics:

   Instagram Aesthetic:
   - Highlights: Warm (yellow, 15% sat)
   - Shadows: Cool (blue, 10% sat)

   Minimal Aesthetic:
   - Highlights: Neutral (low saturation)
   - Shadows: Neutral (low saturation)

   Vintage Aesthetic:
   - Highlights: Warm (yellow, 20% sat)
   - Shadows: Warm (red, 15% sat)

5. Create and Save Presets
   Process:
   1. Edit photo to desired look
   2. Save adjustments as preset
   3. Name preset descriptively ("Warm Skincare", "Cool Fashion")
   4. Apply to future photos (one-tap consistency)

   Preset Benefits:
   ✅ Consistent aesthetic across account
   ✅ Faster editing workflow
   ✅ Recognizable brand style

   Preset Strategy:
   - Create 2-3 presets for different content types
   - Example: "Product Shot" (bright, clean), "Lifestyle" (warm, soft)
   - Apply preset, then fine-tune per photo
```

### Step 3: Retouch Photos

**Enhance Without Being Misleading**:
```
Retouching Ethics and Techniques:

1. Skin Retouching
   Blemish Removal:
   - Use: Healing brush or blemish tool
   - Remove: Acne, scars, spots
   - Keep: Skin texture (don't blur completely)

   Skin Smoothing:
   - Light: Reduce pores slightly (natural look)
   - Medium: Smooth skin texture (common in beauty)
   - Heavy: Airbrushed (highly edited)

   Ethical Guideline:
   ✅ Remove temporary blemishes (acne, redness)
   ✅ Keep permanent features (moles, scars)
   ✅ Don't oversmooth (uncanny valley)
   ✅ Disclose significant edits if misleading

2. Body and Face Reshaping
   Tools Available:
   - Slim face, enlarge eyes, smooth jawline
   - Lengthen legs, slim waist

   Ethical Concerns:
   ⚠️ Can create unrealistic expectations
   ⚠️ May promote body image issues
   ⚠️ Followers may feel inadequate

   Recommendation:
   ✅ Use minimally (subtle enhancements)
   ✅ Avoid extreme reshaping (obviously fake)
   ✅ Consider impact on audience (especially younger followers)
   ✅ Disclose edits if promoting body positivity

3. Background Cleanup
   Remove Distractions:
   - Use: Healing brush, clone tool
   - Remove: Trash, people in background, messy areas
   - Keep: Natural environment (don't fake backdrop)

   Background Replacement:
   - ⚠️ Can be misleading (not real location)
   - ✅ Acceptable if disclosed (studio backdrop)
   - ✅ Creative choice (artistic background)

   Ethics:
   ✅ Remove distractions (clutter, random objects)
   ❌ Fake location or setting (misleading)
   ❌ Create false context (not real situation)

4. Before/After Edits
   Purpose: Show transformation

   Ethical Before/After:
   ✅ Same lighting (no manipulation)
   ✅ Same angle (no perspective trick)
   ✅ Honest time gap (realistic timeline)
   ✅ Disclose products used (transparency)

   Misleading Before/After:
   ❌ Different lighting (after is brighter/better)
   ❌ Different angle (more flattering in after)
   ❌ Fake time gap (results not realistic)
   ❌ Heavily edited after photo

   Example (Ethical):
   Before: Acne breakout (real photo)
   After: After using skincare product for 30 days (real photo)
   Edits: Color correction only (no fake skin)

   Example (Misleading):
   Before: Poor lighting, bad angle
   After: Great lighting, better angle, heavy retouching
   Claim: "Product transformed my skin in 1 week" (unrealistic)

5. Transparency and Disclosure
   When to Disclose:
   ✅ Heavily edited photos (obviously retouched)
   ✅ Reshaped body/face significantly
   ✅ Fake background or setting
   ✅ Before/after with manipulated results

   How to Disclose:
   - Caption: "Edited for brightness/color"
   - Hashtag: #edited #notreal
   - Honest: "This took 20 minutes of editing"
   - Educate: Show before/after of edit process

   When Not Required:
   ✅ Basic adjustments (exposure, color)
   ✅ Blemish removal (temporary)
   ✅ Normal retouching (industry standard)

   Ethics Rule of Thumb:
   If edit creates unrealistic expectation → Disclose
   If edit is minor/basic → No disclosure needed
```

### Step 4: Add Creative Effects

**Enhance Visual Appeal**:
```
Creative Enhancement Options:

1. Filters and Presets
   Filter Types:
   - Bright/Airy: High exposure, low contrast, warm
   - Moody: Low exposure, high contrast, cool
   - Vintage: Fade, warm tone, slight vignette
   - Black & White: Classic, timeless

   Best Practices:
   ✅ Match filter to content mood
   ✅ Use consistently (build aesthetic)
   ✅ Don't over-filter (subtle is better)
   ✅ Create own presets (unique style)

   Filter Recommendations by Niche:

   Skincare/Beauty:
   - Bright, airy, warm
   - Low contrast, high exposure
   - Clean, fresh look

   Fashion:
   - Moody or minimal
   - Low saturation or black & white
   - Editorial style

   Food:
   - Warm, vibrant
   - High saturation (appetizing)
   - Slight contrast boost

2. Blur and Bokeh
   Purpose: Focus attention, create depth

   Radial Blur (Focus Subject):
   - Center sharp, edges blurred
   - Use for: Product shots, portraits
   - Settings: Blur amount 20-40%

   Tilt-Shift (Miniature Effect):
   - Horizontal blur band
   - Use for: Creative flat lay, scenes
   - Settings: Blur position top/bottom

   Background Blur (Portrait Mode):
   - Subject sharp, background blurred
   - Use for: portraits, product isolation
   - Settings: Blur amount 30-50%

3. Vignette
   Purpose: Draw attention to center

   Subtle Vignette:
   - Dark edges, bright center
   - Use for: Portraits, product shots
   - Settings: Vignette amount 10-20%

   Creative Vignette:
   - Strong dark edges
   - Use for: Dramatic effect
   - Settings: Vignette amount 30-40%

   Pro Tip:
   ✅ Subtle is better (10-15% is usually enough)
   ✅ Don't overuse (every photo doesn't need vignette)

4. Grain and Texture
   Purpose: Add film-like quality

   Film Grain:
   - Adds texture, reduces digital look
   - Use for: Vintage aesthetic, moody photos
   - Settings: Grain amount 15-30%

   Light Leaks:
   - Adds warm, dreamy spots
   - Use for: Creative, artistic photos
   - Settings: Leak opacity 20-40%

   Dust and Scratches:
   - Adds vintage, aged look
   - Use for: Retro aesthetic
   - Settings: Texture amount 10-20%

5. Duotone and Color Effects
   Duotone (Two-Color):
   - Shadows: One color
   - Highlights: Another color
   - Use for: Creative, artistic effect

   Gradient Map:
   - Maps grayscale to color gradient
   - Use for: Unified color scheme

   Color Splash:
   - Selective color (rest is B&W)
   - Use for: Focus attention on color element
```

### Step 5: Add Text and Graphics

**Create Informative Overlays**:
```
Text and Graphic Elements:

1. Text Overlays
   When to Add Text:
   ✅ Titles (product name, topic)
   ✅ Key points (summary slides)
   ✅ Call-to-action (follow, link in bio)
   ✅ Quotes (testimonials, tips)

   Text Design Principles:
   - Font: Readable, matches aesthetic (avoid overly decorative)
   - Size: Large enough to read on mobile screen
   - Color: High contrast (dark text on light, or vice versa)
   - Position: Don't cover focal point
   - Background: Semi-transparent box or blur behind text

   Tools:
   - Canva (text templates)
   - Xingtu (text overlays)
   - Phonto (custom fonts)

2. Stickers and Decorations
   Types:
   - Arrows (point to features)
   - Circles/Underlines (highlight text)
   - Icons (checkmarks, hearts, stars)
   - Frames (borders, corners)

   Usage:
   ✅ Highlight key information
   ✅ Add visual interest
   ✅ Guide viewer's eye
   ⚠️ Don't overuse (cluttered)

3. Watermarks
   Purpose: Protect content, brand image

   Placement:
   - Corner (least intrusive)
   - Center (harder to remove)
   - Tiled (repeating across image)

   Design:
   - Logo or username
   - Semi-transparent (30-50% opacity)
   - Small but visible

   Pro/Con:
   ✅ Protects from theft
   ❌ Distracts from image
   ❌ Reduces aesthetic quality

   Recommendation:
   - Use on high-value content (product photography)
   - Skip on personal photos (lifestyle, behind-the-scenes)

4. Frames and Borders
   Types:
   - Simple border (white, black line)
   - Polaroid frame (white bottom, text space)
   - Rounded corners (soft look)
   - Decorative frame (designer border)

   Usage:
   ✅ Separate image from background
   ✅ Add space for text
   ✅ Create cohesive look for carousel

5. Comparison Graphics
   Before/After Layout:
   - Side-by-side (before left, after right)
   - Split screen (vertical or horizontal divider)
   - Labels: "Before" and "After" text

   Design:
   ✅ Consistent lighting (no manipulation)
   ✅ Same size/scale (fair comparison)
   ✅ Clear labels (viewer knows which is which)
   ✅ Arrow or line highlighting difference

   Tools:
   - Before/After maker apps
   - Manual layout in Canva
   - Split screen in editing app
```

## Common Mistakes

| Mistake | Why Happens | Fix |
|---------|-------------|-----|
| Over-editing (too much filter) | Want perfect photo | Edit subtly, less is more |
| Inconsistent style across posts | Edit each photo individually | Create and use presets for consistency |
| Misleading before/after | Want dramatic results | Use same lighting/angle, disclose edits |
| Oversmoothing skin | Think flawless is best | Keep skin texture, natural look |
| Ignoring composition | Focus only on edits | Edit good photos (editing can't fix bad composition) |
| Heavy watermarks on all content | Fear of theft | Use selectively, or small unobtrusive watermark |
| Not saving presets | Recreate edits each time | Save successful edits as presets for efficiency |

## Real-World Impact

**Case Study: Image Quality Transformation**
- **Before**: Posted raw phone photos, inconsistent style, 5% engagement rate
- **After**: Learned image editing, created preset, consistent aesthetic
- **Result**: 40% increase in engagement, follower growth doubled, brand partnerships increased (professional look attracted brands)

**Data-Backed Insights**:
- Edited images receive 2-3x more engagement than unedited photos (same subject matter)
- Accounts with consistent editing aesthetic grow 2x faster than inconsistent accounts
- Bright, warm-toned photos get 20% more engagement than cool, dark photos (lifestyle niche)
- Before/after posts with honest edits get 3x more saves than other content types
- Over-edited photos (heavy filters, oversmoothed skin) reduce trust by 30%
- Professional-looking photos (clean edits) attract 2x more brand partnerships
- Light, airy presets most popular for skincare/beauty (70% of top accounts)

## Related Skills

**REQUIRED**: Use cover-design (image editing enhances cover design)
**REQUIRED**: Use image-text-content (polished images for图文 posts)

**Recommended for image editing**:
- **photo-editing-tools** (master specific editing apps)
- **content-layout** (combine edited images into carousels)
- **visual-branding** (create consistent editing style)
- **seeding-copywriting** (edited images support product content)

**Use image-editing WITH**:
- cover-design (edit cover images for maximum appeal)
- image-text-content (polish images for图文 content)
- carousel-creation (edit all carousel images cohesively)
