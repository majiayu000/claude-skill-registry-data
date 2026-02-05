---
name: ecommerce-theming
description: Complete theming guide for the e-commerce storefront. Documents all styled components and provides instructions for applying new themes. Use when customizing store appearance, changing color schemes, or restyling the entire application.
---

# E-Commerce Theming Guide

This skill provides a comprehensive map of all themed components in the storefront and instructions for applying new visual themes.

## Overview

This Next.js 16 e-commerce template uses a cohesive design system with **fully customizable** colors, typography, and styling patterns.

**IMPORTANT**: This is a TEMPLATE project. Color names and values shown in this guide (like "rose-gold", "champagne", etc.) are just the CURRENT EXAMPLE theme. When applying a new theme, you will:
1. Choose your own color palette completely from scratch
2. Name colors based on YOUR theme (e.g., "ocean-blue", "forest-green", "neon-pink")
3. Update all CSS variables and component references accordingly

The template structure stays the same, but colors are 100% dynamic and changeable based on your requirements.

## Theme Configuration Files

### 1. Tailwind Config (`tailwind.config.ts`)

**Location**: `d:\Projektit\Verkkokaupat\testi-kauppa\tailwind.config.ts`

This file defines:

- Font families (primary/secondary via CSS variables)
- Color system extending base Tailwind colors
- Border radius values
- Custom animations (shine, shimmer-x, shimmer-y)

**Custom colors defined**:

```typescript
colors: {
  // Shadcn/ui semantic colors (use HSL CSS variables)
  background: "hsl(var(--background))",
  foreground: "hsl(var(--foreground))",
  card: { DEFAULT, foreground },
  popover: { DEFAULT, foreground },
  primary: { DEFAULT, foreground },
  secondary: { DEFAULT, foreground },
  tertiary: { DEFAULT, foreground },
  muted: { DEFAULT, foreground },
  accent: { DEFAULT, foreground },
  destructive: { DEFAULT, foreground },
  border, input, ring,

  // Custom theme-specific colors (EXAMPLE - customize these!)
  // Current example: Jewelry theme
  "rose-gold": "hsl(var(--rose-gold))",      // → Rename to YOUR accent color
  champagne: "hsl(var(--champagne))",        // → Rename to YOUR secondary accent
  cream: "hsl(var(--cream))",                // → Rename to YOUR light background
  "warm-white": "hsl(var(--warm-white))",    // → Rename to YOUR main background
  "soft-blush": "hsl(var(--soft-blush))",    // → Rename to YOUR subtle accent
  "deep-burgundy": "hsl(var(--deep-burgundy))", // → Rename to YOUR dark accent
  charcoal: "hsl(var(--charcoal))",          // → Rename to YOUR text color
}
```

**Example for a different theme (Ocean Store)**:
```typescript
// Replace the above with:
"ocean-blue": "hsl(var(--ocean-blue))",      // Main accent
"seafoam": "hsl(var(--seafoam))",            // Secondary accent
"sand": "hsl(var(--sand))",                  // Light background
"pearl-white": "hsl(var(--pearl-white))",    // Main background
"coral": "hsl(var(--coral))",                // Subtle accent
"deep-navy": "hsl(var(--deep-navy))",        // Dark accent
"slate": "hsl(var(--slate))",                // Text color
```

### 2. Global CSS (`src/app/globals.css`)

**Location**: `d:\Projektit\Verkkokaupat\testi-kauppa\src\app\globals.css`

This file contains:

- **CSS Variable Definitions** (lines 6-50): All color values in HSL format
- **Dark Mode Variables** (lines 52-85): Alternative color scheme
- **Custom Utility Classes** (lines 143-254): Decorative effects

**How to change theme colors**:

1. Modify CSS variables in `:root` selector (lines 6-50)
2. Update custom color variables (lines 36-43)
3. Colors use HSL format: `hue saturation% lightness%`

**Color Variable Structure** (customize names AND values for your theme):

```css
:root {
  /* EXAMPLE: Current Jewelry Theme - REPLACE EVERYTHING BELOW */
  --rose-gold: 15 45% 65%;      /* Main accent - YOUR primary brand color */
  --champagne: 38 45% 78%;      /* Secondary accent - YOUR complementary color */
  --cream: 35 40% 95%;          /* Light background - YOUR soft background */
  --warm-white: 30 33% 98%;     /* Main background - YOUR page background */
  --soft-blush: 350 35% 90%;    /* Subtle accent - YOUR tertiary color */
  --deep-burgundy: 350 45% 30%; /* Dark accent - YOUR contrast/sale color */
  --charcoal: 20 15% 18%;       /* Main text - YOUR text color */
}
```

**These 7 color roles must be filled, but you choose the names and values**:
1. **Main Accent** - Primary brand color (buttons, links, highlights)
2. **Secondary Accent** - Complementary color (badges, secondary elements)
3. **Light Background** - Soft background for cards, sections
4. **Main Background** - Page background color
5. **Subtle Accent** - Tertiary/decorative color
6. **Dark Accent** - Contrast color for sales, warnings, errors
7. **Text Color** - Main text/foreground color

**Custom utility classes available** (rename these to match your theme):

- `.text-gradient-gold` - Gradient text effect (rename to match your theme, e.g., `.text-gradient-ocean`)
- `.text-gradient-rose` - Alternative gradient (customize colors and name)
- `.line-ornament` - Decorative line with centered element (theme-agnostic)
- `.diamond-shape` - Diamond clip-path for decorative elements (theme-agnostic)
- `.shimmer-gold` - Animated shimmer effect (rename and recolor, e.g., `.shimmer-blue`)
- `.card-lift` - Elegant hover lift animation (theme-agnostic)
- `.artistic-border` - Border with corner accents (theme-agnostic)
- `.octagon-clip` - Octagonal clip-path (theme-agnostic)

**Note**: Classes marked "theme-agnostic" don't need renaming, only color updates in their CSS.

### 3. Font Configuration (`src/lib/fonts.ts`)

**Location**: `d:\Projektit\Verkkokaupat\testi-kauppa\src\lib\fonts.ts` (likely)

Fonts are loaded via Next.js `next/font` and exposed as CSS variables:

- `--font-primary`: Used for headings, titles, prices
- `--font-secondary`: Used for body text, labels, descriptions

Applied in `globals.css` (lines 95-100):

```css
html {
  font-family: var(--font-secondary);
}
h1 {
  font-family: var(--font-primary);
}
```

## Component Styling Map

All components below use the theme colors and patterns. When restyling, update these files to match your new theme.

### Navigation Components

**Location**: `src/components/Navigation/`

1. **Navbar.tsx** - Main navigation bar

   - Uses `bg-warm-white`, `text-charcoal`
   - Border colors: `border-rose-gold/10`
   - Hover states with rose-gold accent

2. **NavbarLinks.tsx** - Desktop navigation links

   - Link hover effects
   - Active state indicators
   - Dropdown menus (if present)

3. **MobileLinks.tsx** - Mobile menu
   - Mobile drawer/menu styling
   - Hamburger icon states
   - Mobile-specific interactions

**Styling patterns**:

- Corner accent borders (animated on hover)
- Rose gold highlights on active/hover states
- Warm white backgrounds with subtle borders

### Homepage Components

**Location**: `src/components/`

1. **Hero.tsx** - Landing page hero section

   - Full-screen parallax hero
   - Decorative corner elements (lines 38-41)
   - Floating diamond decorations with animations (lines 62-89)
   - Gradient text effects: `.text-gradient-gold`
   - CTA buttons with charcoal/rose-gold styling
   - Framer Motion animations

2. **Homepage/CategorySection.tsx** - Category showcase

   - Grid layout for category cards
   - Hover effects with border animations
   - Category images with overlays

3. **Homepage/AboutMeSection.tsx** - About section on homepage
   - Text content styling
   - Decorative elements
   - Background treatments

**Styling patterns**:

- Parallax scrolling effects
- Staggered animations with Framer Motion
- Diamond-shaped decorative elements
- Corner border accents (see lines 149-157 in myorders/page.tsx for pattern)

### Product Components

**Location**: `src/components/`

1. **ProductCard.tsx** - Product grid cards

   - Card frame with corner accents (lines 38-45)
   - Image aspect ratio: square
   - Sale badge with burgundy background (lines 63-72)
   - Share button (appears on hover, lines 74-90)
   - "View product" slide-up indicator (lines 93-100)
   - Price display with sale/regular pricing
   - Availability indicator with colored dots
   - Hover effects: scale, corner expansion, overlay

2. **Product/ProductDetail.tsx** - Individual product page

   - Large product images with gallery
   - Variation selectors
   - Add to cart button styling
   - Product information layout
   - Related products section

3. **Product/Pagination.tsx** - Product list pagination

   - Page number styling
   - Active page indicator
   - Next/Previous buttons

4. **Product/SortOptions.tsx** - Product sorting dropdown
   - Dropdown menu styling
   - Sort option list
   - Selected state

**Styling patterns**:

- Animated corner borders: start at 6x6px, expand to 10x10px on hover
- Slide-up reveal effects on hover
- Image zoom transitions (scale-105)
- Gradient overlays on images
- Sale badges with decorative bottom border

### Cart & Checkout Components

**Location**: `src/components/Cart/`, `src/components/Checkout/`

**Cart Components**:

1. **Cart.tsx** - Cart drawer/modal
2. **CartItem.tsx** - Individual cart item
3. **CartPage.tsx** - Full cart page view
4. **CampaignAddedCartItems.tsx** - Campaign/promo items display
5. **CheckoutButton.tsx** - Proceed to checkout CTA

**Checkout Components**:

1. **CheckoutSteps.tsx** - Multi-step checkout indicator
2. **CustomerDataForm.tsx** - Customer information form
3. **SelectShipmentMethod.tsx** - Shipping method selector
4. **PaytrailCheckoutPage.tsx** - Paytrail payment integration
5. **PaytrailPaymentSelection.tsx** - Payment method selection
6. **StripeCheckoutPage.tsx** - Stripe payment integration
7. **/payment/success/{id}** - This is succesfull checkout route

**Styling patterns**:

- Form inputs with rose-gold focus rings
- Step indicators with active states
- Card-style containers with corner accents
- Submit buttons with hover transitions
- Validation states (error/success)

### Authentication & Dashboard Components

**Location**: `src/components/Auth/`, `src/components/CustomerDashboard/`

**Auth Components**:

1. **Loginform.tsx** - Login form
2. **RegisterForm.tsx** - Registration form
3. **DeleteWishListButton.tsx** - Remove wishlist item

**Dashboard Components**:

1. **EditCustomerForm.tsx** - Profile edit form

**Dashboard Pages** (`src/app/(auth)/(dashboard)/`):

1. **layout.tsx** - Dashboard layout wrapper
2. **mypage/page.tsx** - Dashboard home
3. **myorders/page.tsx** - Order history page (see example below)
4. **mywishlist/page.tsx** - Wishlist page

**Example Styling - Order Card** (from `myorders/page.tsx` lines 143-280):

```tsx
<div className="group relative bg-warm-white p-6 mb-6">
  {/* Border frame */}
  <div
    className="absolute inset-0 border border-rose-gold/10
                  group-hover:border-rose-gold/25 transition-colors"
  />

  {/* Corner accents - animate on hover */}
  <div
    className="absolute top-0 left-0 w-4 h-4 border-l border-t
                  border-rose-gold/20 group-hover:w-6 group-hover:h-6
                  transition-all duration-300"
  />
  {/* ...repeat for 4 corners */}
</div>
```

**Styling patterns**:

- Card layouts with corner decorations
- Status badges with color coding (champagne, rose-gold, burgundy)
- Gradient separator lines
- Icon integration from lucide-react
- Empty states with centered content

### About & Contact Components

**Location**: `src/components/Aboutpage/`, `src/components/Contactpage/`

1. **AboutBlock.tsx** - About page content blocks
2. **AboutCTA.tsx** - Call-to-action section (NEW)
3. **AboutHero.tsx** - About page hero (NEW)
4. **ContactForm.tsx** - Contact form

**About Page** (`src/app/(storefront)/about/page.tsx`)

**Styling patterns**:

- Content blocks with imagery
- Text hierarchy with primary/secondary fonts
- Decorative dividers
- CTA buttons matching global style

### Layout Components

1. **Footer.tsx** - Site footer

   - Multi-column layout
   - Social links
   - Copyright info
   - Decorative top border

2. **subtitle.tsx** - Reusable subtitle component
   - Consistent subtitle styling across pages
   - Decorative accents

**Page Layouts**:

- `src/app/layout.tsx` - Root layout
- `src/app/(storefront)/page.tsx` - Homepage layout
- `src/app/(storefront)/products/[...slug]/page.tsx` - Product pages
- `src/app/(storefront)/verify-email/page.tsx` - Email verification

## Styling Patterns & Conventions

### 1. Card Frame with Corner Accents

**Used in**: ProductCard, OrderCard, Dashboard cards, Empty states

```tsx
<div className="group relative bg-warm-white p-6">
  {/* Main border */}
  <div
    className="absolute inset-0 border border-rose-gold/10
                  group-hover:border-rose-gold/25 transition-colors"
  />

  {/* Animated corners (4 corners total) */}
  <div
    className="absolute top-0 left-0 w-6 h-6 border-l border-t
                  border-rose-gold/30 group-hover:w-10 group-hover:h-10
                  transition-all duration-500"
  />
  {/* ...top-right, bottom-left, bottom-right */}
</div>
```

### 2. Gradient Dividers

**Used in**: OrderCard, ProductDetail, Forms

```tsx
{
  /* Horizontal divider */
}
<div className="h-[1px] bg-gradient-to-r from-rose-gold/30 to-transparent" />;

{
  /* Full width with fade from center */
}
<div className="h-[1px] bg-gradient-to-r from-transparent via-rose-gold/40 to-transparent" />;
```

### 3. Status Badges

**Used in**: Order status, Product availability, Campaign labels

```tsx
<div
  className="inline-flex items-center gap-2 px-3 py-1.5
                border bg-rose-gold/20 text-charcoal
                border-rose-gold/40 font-secondary text-xs
                tracking-wider uppercase"
>
  <Icon className="w-3 h-3" />
  <span>STATUS TEXT</span>
</div>
```

### 4. Button Styles

**Primary CTA** (dark with accent hover):

```tsx
<button className="inline-flex items-center justify-center gap-3
                   px-8 py-3 bg-charcoal text-warm-white
                   font-secondary text-sm tracking-wider uppercase
                   transition-all duration-300 hover:bg-rose-gold">
```

**Secondary CTA** (outlined):

```tsx
<button className="inline-flex items-center gap-3 px-8 py-4
                   border border-charcoal/30 text-charcoal
                   font-secondary text-sm tracking-wider uppercase
                   hover:border-rose-gold hover:text-rose-gold">
```

### 5. Typography Hierarchy

- **Large Headings**: `font-primary text-4xl sm:text-5xl lg:text-6xl text-charcoal`
- **Section Titles**: `font-primary text-2xl md:text-3xl text-charcoal`
- **Body Text**: `font-secondary text-base text-charcoal/80`
- **Small Labels**: `font-secondary text-xs tracking-wider uppercase text-charcoal/70`
- **Prices**: `font-primary text-lg font-bold text-charcoal`

### 6. Decorative Elements

**Diamond bullets** (used in myorders header, line 304):

```tsx
<div className="w-1.5 h-1.5 bg-rose-gold/60 diamond-shape" />
```

**Section header pattern**:

```tsx
<div className="flex items-center gap-3 mb-2">
  <div className="w-1.5 h-1.5 bg-rose-gold/60 diamond-shape" />
  <h2 className="text-2xl md:text-3xl font-primary text-charcoal">
    Section Title
  </h2>
</div>
<p className="font-secondary text-charcoal/60 ml-5">
  Description text
</p>
```

### 7. Image Overlays

**On hover** (ProductCard, CategorySection):

```tsx
<div
  className="absolute inset-0 bg-gradient-to-t
                from-charcoal/20 via-transparent to-transparent
                opacity-0 group-hover:opacity-100
                transition-opacity duration-500"
/>
```

### 8. Empty States

**Pattern** (from myorders empty state, lines 314-337):

```tsx
<div className="relative bg-warm-white p-12 text-center">
  {/* Border + 4 corner accents */}
  <div className="absolute inset-0 border border-rose-gold/10" />
  <div
    className="absolute top-0 left-0 w-8 h-8 border-l border-t
                  border-rose-gold/30"
  />
  {/* ...3 more corners */}

  <div className="relative">
    <Icon className="w-16 h-16 text-charcoal/20 mx-auto mb-6" />
    <h3 className="text-xl font-primary text-charcoal mb-3">
      Empty State Title
    </h3>
    <p className="text-sm font-secondary text-charcoal/60 mb-6">Description</p>
    <Button>Call to Action</Button>
  </div>
</div>
```

## How to Apply a New Theme

**IMPORTANT REMINDER**: This is a completely dynamic theming system. You are NOT limited to the example colors shown in this guide. The workflow is:

1. **User specifies desired theme** - "I want ocean blues" or "I want forest greens" or "I want neon cyberpunk"
2. **Choose appropriate color names** - Name variables based on the theme (ocean-blue, forest-green, neon-pink, etc.)
3. **Update CSS variables** - Replace ALL color values in `globals.css`
4. **Update Tailwind config** - Rename color keys in `tailwind.config.ts`
5. **Find & replace in components** - Replace old color names with new names across all files

The structure below guides you through this process for ANY color scheme.

### Step 1: Choose Your Color Palette

Decide on your theme based on your e-commerce vertical or user requirements:

**Examples**:

- **Tech Store**: Dark grays, electric blue accents, modern sans-serif
- **Fashion Boutique**: Soft pastels, black & white, elegant serif
- **Organic Food**: Earthy greens, natural browns, warm cream
- **Luxury Watches**: Deep navy, gold accents, sophisticated serif
- **Handmade Crafts**: Vibrant colors, playful accents, friendly fonts

**Pick 5-7 colors** (the roles stay the same, names/values are YOUR choice):

1. **Main background** (lightest) - The page background color
   - Example names: `--warm-white`, `--pearl-white`, `--midnight-black`, `--cream-canvas`
2. **Secondary background** - Cards, sections, subtle background
   - Example names: `--cream`, `--sand`, `--charcoal-light`, `--soft-gray`
3. **Text color** (darkest) - Main text/foreground
   - Example names: `--charcoal`, `--slate`, `--ink-black`, `--pure-white`
4. **Primary accent** - Main brand color (buttons, links, highlights)
   - Example names: `--rose-gold`, `--ocean-blue`, `--forest-green`, `--neon-pink`
5. **Secondary accent** - Complementary color
   - Example names: `--champagne`, `--seafoam`, `--sage`, `--electric-purple`
6. **Subtle accent** - Tertiary/decorative
   - Example names: `--soft-blush`, `--coral`, `--mint`, `--lavender`
7. **Dark accent** - Contrast/sale/warning color
   - Example names: `--deep-burgundy`, `--deep-navy`, `--dark-forest`, `--crimson`

### Step 2: Update `globals.css`

**File**: `d:\Projektit\Verkkokaupat\testi-kauppa\src\app\globals.css`

Replace CSS variables in `:root` (lines 6-50):

```css
:root {
  /* Example: Tech Store Theme */
  --background: 220 15% 98%; /* Light gray-blue */
  --foreground: 220 20% 10%; /* Almost black */
  --card: 220 10% 95%; /* Slightly darker than bg */

  --primary: 220 90% 56%; /* Electric blue */
  --primary-foreground: 220 15% 98%;
  --secondary: 220 15% 88%;
  --secondary-foreground: 220 20% 10%;

  /* Custom theme colors */
  --electric-blue: 220 90% 56%; /* Replace rose-gold */
  --steel-gray: 220 10% 45%; /* Replace champagne */
  --light-gray: 220 10% 95%; /* Replace cream */
  --off-white: 220 15% 98%; /* Replace warm-white */
  --cyan-accent: 190 80% 50%; /* Replace soft-blush */
  --navy-dark: 220 50% 20%; /* Replace deep-burgundy */
  --charcoal: 220 20% 10%; /* Keep or adjust */
}
```

**Important**: If renaming custom colors (e.g., `rose-gold` → `electric-blue`), also update `tailwind.config.ts`.

### Step 3: Update `tailwind.config.ts`

**File**: `d:\Projektit\Verkkokaupat\testi-kauppa\tailwind.config.ts`

If you renamed custom colors, update color definitions (lines 56-62):

```typescript
colors: {
  // ... existing semantic colors ...

  // Rename custom colors to match your theme
  "electric-blue": "hsl(var(--electric-blue))",
  "steel-gray": "hsl(var(--steel-gray))",
  "light-gray": "hsl(var(--light-gray))",
  "off-white": "hsl(var(--off-white))",
  "cyan-accent": "hsl(var(--cyan-accent))",
  "navy-dark": "hsl(var(--navy-dark))",
  charcoal: "hsl(var(--charcoal))",
}
```

### Step 4: Update Fonts

**File**: `src/lib/fonts.ts` (create if doesn't exist)

Choose distinctive fonts following the `artistic-styling` skill guidelines:

**Good pairings**:

- **Tech**: JetBrains Mono (headings) + Inter (body) - but avoid if too generic
- **Editorial**: Playfair Display (headings) + Source Sans 3 (body)
- **Modern**: Outfit (headings) + Plus Jakarta Sans (body)
- **Luxury**: Cormorant Garamond (headings) + Montserrat (body)

```typescript
import { Plus_Jakarta_Sans, Outfit } from "next/font/google";

const primary = Outfit({
  subsets: ["latin"],
  variable: "--font-primary",
});

const secondary = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-secondary",
});

export { primary, secondary };
```

### Step 5: Global Find & Replace

Use your IDE's find & replace to swap color class names across all components.

**Find**: `rose-gold`
**Replace**: `electric-blue` (or your primary accent)

**Find**: `champagne`
**Replace**: `steel-gray` (or your secondary accent)

**Find**: `warm-white`
**Replace**: `off-white` (or your main background)

**Find**: `deep-burgundy`
**Replace**: `navy-dark` (or your sale/warning color)

**Files to update** (all modified files from git status):

- All components in `src/components/`
- All pages in `src/app/`
- `globals.css` utility classes (lines 143-254)

### Step 6: Update Custom Utility Classes

**File**: `src/app/globals.css` (lines 143-254)

Update gradient utilities to match new colors:

```css
.text-gradient-gold {
  /* Change to your primary accent gradient */
  background: linear-gradient(
    135deg,
    hsl(220 90% 56%),
    hsl(190 80% 50%),
    hsl(220 90% 56%)
  );
  /* ... */
}

.shimmer-gold {
  /* Update shimmer colors */
  background: linear-gradient(
    110deg,
    transparent 20%,
    hsl(220 90% 70% / 0.4) 40%,
    hsl(220 90% 80% / 0.6) 50%,
    hsl(220 90% 70% / 0.4) 60%,
    transparent 80%
  );
  /* ... */
}
```

### Step 7: Test & Refine

1. **Run dev server**: `npm run dev`
2. **Check all pages**:
   - Homepage (`/`)
   - Product listing (`/products`)
   - Product detail (`/product/[slug]`)
   - Cart & Checkout
   - Dashboard pages (login first)
   - About & Contact
3. **Test interactions**:
   - Hover states
   - Focus states (forms)
   - Active states (navigation)
   - Animations
4. **Responsive design**:
   - Mobile (< 768px)
   - Tablet (768px - 1024px)
   - Desktop (> 1024px)

### Step 8: Adjust Opacity & Contrast

Fine-tune color opacities for subtle effects:

- Borders: `/10`, `/20`, `/30` opacity
- Hover states: `/20` → `/40` transition
- Backgrounds: `/30`, `/50` for overlays
- Text: `/60`, `/70`, `/80` for hierarchy

Check WCAG contrast ratios:

- Text on background: minimum 4.5:1
- Large text (18px+): minimum 3:1
- Use a contrast checker tool

## Integration with Artistic Styling Skill

This theme skill works alongside the `artistic-styling` skill (`.claude/skills/artistic-styling/SKILL.md`).

**When to use each**:

- **artistic-styling**: Creating NEW components or designing from scratch
- **ecommerce-theming**: Restyling EXISTING components with a new theme

**Shared principles**:

- Avoid generic fonts (Inter, Roboto) - use distinctive choices
- Use CSS variables for consistency
- Commit to a cohesive color palette
- High contrast typography (weight, size)
- Meaningful animations and micro-interactions
- Tailwind v4 compatibility (use `gap-*`, not `space-x-*`)

## Quick Reference: Component Checklist

When applying a new theme, update these component categories:

- [ ] **Theme Config**

  - [ ] `globals.css` - CSS variables
  - [ ] `tailwind.config.ts` - Color definitions
  - [ ] `src/lib/fonts.ts` - Font imports
  - [ ] `src/app/layout.tsx` - Font className application

- [ ] **Navigation** (3 files)

  - [ ] `Navbar.tsx`
  - [ ] `NavbarLinks.tsx`
  - [ ] `MobileLinks.tsx`

- [ ] **Homepage** (4 files)

  - [ ] `Hero.tsx`
  - [ ] `Homepage/CategorySection.tsx`
  - [ ] `Homepage/AboutMeSection.tsx`
  - [ ] `src/app/(storefront)/page.tsx`

- [ ] **Products** (5 files)

  - [ ] `ProductCard.tsx`
  - [ ] `Product/ProductDetail.tsx`
  - [ ] `Product/Pagination.tsx`
  - [ ] `Product/SortOptions.tsx`
  - [ ] `src/app/(storefront)/products/[...slug]/page.tsx`

- [ ] **Cart & Checkout** (10 files)

  - [ ] `Cart/Cart.tsx`
  - [ ] `Cart/CartItem.tsx`
  - [ ] `Cart/CartPage.tsx`
  - [ ] `Cart/CampaignAddedCartItems.tsx`
  - [ ] `Cart/CheckoutButton.tsx`
  - [ ] `Checkout/CheckoutSteps.tsx`
  - [ ] `Checkout/CustomerDataForm.tsx`
  - [ ] `Checkout/SelectShipmentMethod.tsx`
  - [ ] `Checkout/PaytrailCheckoutPage.tsx`
  - [ ] `Checkout/StripeCheckoutPage.tsx`

- [ ] **Auth & Dashboard** (8 files)

  - [ ] `Auth/Loginform.tsx`
  - [ ] `Auth/RegisterForm.tsx`
  - [ ] `Auth/DeleteWishListButton.tsx`
  - [ ] `CustomerDashboard/EditCustomerForm.tsx`
  - [ ] `src/app/(auth)/(dashboard)/layout.tsx`
  - [ ] `src/app/(auth)/(dashboard)/mypage/page.tsx`
  - [ ] `src/app/(auth)/(dashboard)/myorders/page.tsx`
  - [ ] `src/app/(auth)/(dashboard)/mywishlist/page.tsx`

- [ ] **About & Contact** (5 files)

  - [ ] `Aboutpage/AboutBlock.tsx`
  - [ ] `Aboutpage/AboutCTA.tsx`
  - [ ] `Aboutpage/AboutHero.tsx`
  - [ ] `Contactpage/ContactForm.tsx`
  - [ ] `src/app/(storefront)/about/page.tsx`

- [ ] **Layout & Common** (4 files)
  - [ ] `Footer.tsx`
  - [ ] `subtitle.tsx`
  - [ ] `src/app/layout.tsx`
  - [ ] `src/app/(storefront)/verify-email/page.tsx`

**Total**: ~45 files to update for complete theme change

## Example Theme Transformations

**These are just EXAMPLES - your theme can be ANYTHING you want!**

### Example 1: Artisan Jewelry → Modern Tech Store

**User Request**: "I want a tech store with electric blue and dark grays"

**Changes**:

1. CSS variables in `globals.css`:
   - `--rose-gold: 15 45% 65%` → `--electric-blue: 220 90% 56%`
   - `--champagne: 38 45% 78%` → `--steel-gray: 220 10% 45%`
   - `--warm-white: 30 33% 98%` → `--off-white: 220 15% 98%`
   - `--deep-burgundy: 350 45% 30%` → `--navy-dark: 220 50% 20%`

2. Global find/replace:
   - `rose-gold` → `electric-blue` (~113 occurrences)
   - `champagne` → `steel-gray` (~28 occurrences)
   - `warm-white` → `off-white` (~95 occurrences)
   - `deep-burgundy` → `navy-dark` (~12 occurrences)

3. Fonts: Outfit + IBM Plex Sans

### Example 2: Artisan Jewelry → Organic Food Store

**User Request**: "I want earthy greens and natural browns for an organic food shop"

**Changes**:

1. CSS variables in `globals.css`:
   - `--rose-gold: 15 45% 65%` → `--forest-green: 140 45% 40%`
   - `--champagne: 38 45% 78%` → `--sage: 110 25% 65%`
   - `--warm-white: 30 33% 98%` → `--natural-cream: 40 30% 97%`
   - `--deep-burgundy: 350 45% 30%` → `--earth-brown: 25 50% 25%`

2. Global find/replace:
   - `rose-gold` → `forest-green`
   - `champagne` → `sage`
   - `warm-white` → `natural-cream`
   - `deep-burgundy` → `earth-brown`

3. Fonts: Newsreader + Source Sans 3

### Example 3: Artisan Jewelry → Neon Cyberpunk Store

**User Request**: "I want neon pink and purple on dark background for streetwear"

**Changes**:

1. CSS variables in `globals.css`:
   - `--rose-gold: 15 45% 65%` → `--neon-pink: 330 100% 60%`
   - `--champagne: 38 45% 78%` → `--electric-purple: 270 80% 65%`
   - `--warm-white: 30 33% 98%` → `--midnight: 240 20% 8%`
   - `--charcoal: 20 15% 18%` → `--pure-white: 0 0% 100%` (text now white!)
   - `--deep-burgundy: 350 45% 30%` → `--hot-magenta: 320 100% 50%`

2. Global find/replace + invert light/dark usage
3. Fonts: Syne + JetBrains Mono

**Key Point**: Notice how each transformation is completely different - colors, names, even light/dark inversions. The system is FULLY FLEXIBLE.

## Notes

- This skill documents the current state as of the latest git commit
- All components listed have been styled with the current theme
- Patterns are consistent across components for easy theming
- Use this as a map when customizing for different e-commerce verticals
- Combine with `artistic-styling` skill for best results when creating new components

## CRITICAL REMINDER FOR CLAUDE

When a user asks to apply a new theme:

1. **DO NOT** assume they want rose-gold, champagne, or any current colors
2. **ASK** what colors/theme they want if not specified
3. **CREATE** new color variable names that match their theme
4. **REPLACE** all color values with their chosen palette
5. **UPDATE** both `globals.css` AND `tailwind.config.ts` with new names
6. **FIND & REPLACE** old color names with new names across ALL components

**Example user requests you might receive**:
- "I want ocean blues and sandy beiges"
- "Make it dark mode with neon accents"
- "I want a luxury gold and black theme"
- "Give me forest greens and earthy browns"
- "I want pastel pink and lavender"

For EACH request, create a unique color system from scratch. The template structure stays the same, but colors are 100% customizable.
