---
name: shadcn-ui-theme
description: Apply pre-configured shadcn/ui themes with CSS variables. Use when user requests theme changes, color scheme updates, or design system modifications. Supports 17 themes including Default, Claude, Cyberpunk, Neo Brutalism, Supabase, Vercel, and more.
version: 1.0.0
dependencies: shadcn/ui, Tailwind CSS
allowed-tools: Read,Write,Edit
---

# Shadcn UI Theme System

Apply pre-configured shadcn/ui themes by replacing CSS variables in `app/globals.css` or `src/app/globals.css`.

**Available Themes:** 17 options with light/dark mode support

---

## Available Themes

### Default (by shadcn)
Neutral grayscale with balanced contrast. Professional, clean design.
**Use:** Corporate sites, SaaS dashboards, documentation

### Amber Minimal (by tweakcn)
Warm amber accent with minimal color palette. Earthy, inviting tone.
**Use:** Blogs, portfolios, creative agencies

### Blue (by shadcn)
Classic blue primary with cool tones. Trust-building, familiar.
**Use:** Finance, healthcare, enterprise apps

### Citrus (by styleglide)
Lime green with teal accents. Fresh, energetic vibe.
**Use:** Eco-friendly brands, fitness apps, food/beverage

### Claude (by tweakcn)
Terracotta and warm neutrals. Sophisticated, approachable.
**Use:** Design studios, consulting firms, premium brands

### Claymorphism (by tweakcn)
Soft purple with clay-inspired pastels. Modern, tactile feel.
**Use:** Creative tools, design apps, startups

### Cleanslate (by tweakcn)
Cool blue-grays with minimal saturation. Ultra-clean, spacious.
**Use:** Minimalist portfolios, tech products, meditation apps

### Cyberpunk (by tweakcn)
Hot pink and cyan neon. Bold, futuristic aesthetic.
**Use:** Gaming, tech events, nightlife, music platforms

### Kodama Grove (by tweakcn)
Olive greens with earthy browns. Nature-inspired palette.
**Use:** Outdoor brands, sustainability, organic products

### Modern Minimal (by tweakcn)
Pale blues with extreme simplicity. Scandinavian design.
**Use:** Architecture, furniture, high-end retail

### Neo Brutalism (by tweakcn)
Primary colors (red/blue/yellow) with black. Bold, geometric.
**Use:** Streetwear, art galleries, bold brands

### Red (by shadcn)
Vibrant red primary. High-energy, attention-grabbing.
**Use:** Sales, promotions, food delivery, alerts

### Spring Bouquet (by styleglide)
Forest green with purple accents. Botanical, elegant.
**Use:** Florists, weddings, lifestyle brands

### Sunset Horizon (by tweakcn)
Coral orange with peach tones. Warm, optimistic.
**Use:** Travel, hospitality, wellness, summer campaigns

### Supabase (by tweakcn)
Teal green signature color. Modern developer aesthetic.
**Use:** Developer tools, APIs, tech startups

### Typewriter (by styleglide)
High-contrast black/white. Newspaper-inspired.
**Use:** Publishing, journalism, vintage aesthetics

### Vercel (by tweakcn)
Pure black/white monochrome. Sleek, minimal.
**Use:** Tech portfolios, minimalist products, developer tools

---

## How to Apply Themes

### Step 1: Locate globals.css
Theme CSS variables typically live in:
- Next.js App Router: `app/globals.css`
- Next.js Pages Router: `src/app/globals.css` or `styles/globals.css`

Default theme for starting point:
```css
@import url("https://fonts.googleapis.com/css2?family=Roboto:ital%2Cwght@0%2C100..900;1%2C100..900&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Roboto+Mono:ital%2Cwght@0%2C100..700;1%2C100..700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Anton&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:ital%2Cwght@0%2C400..900;1%2C400..900&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Caveat:wght@400..700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Cal+Sans&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Merriweather:ital%2Copsz%2Cwght@0%2C18..144%2C300..900;1%2C18..144%2C300..900&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Figtree:ital%2Cwght@0%2C300..900;1%2C300..900&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Ubuntu:ital%2Cwght@0%2C300;0%2C400;0%2C500;0%2C700;1%2C300;1%2C400;1%2C500;1%2C700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Fahkwang:ital%2Cwght@0%2C200;0%2C300;0%2C400;0%2C500;0%2C600;0%2C700;1%2C200;1%2C300;1%2C400;1%2C500;1%2C600;1%2C700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Red+Hat+Text:ital%2Cwght@0%2C300..700;1%2C300..700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Inter:ital%2Copsz%2Cwght@0%2C14..32%2C100..900;1%2C14..32%2C100..900&display=swap");
@import url("https://fonts.googleapis.com/css2?family=DM+Sans:ital%2Copsz%2Cwght@0%2C9..40%2C100..1000;1%2C9..40%2C100..1000&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Instrument+Sans:ital%2Cwght@0%2C400..700;1%2C400..700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Assistant:wght@200..800&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Poppins:ital%2Cwght@0%2C100;0%2C200;0%2C300;0%2C400;0%2C500;0%2C600;0%2C700;0%2C800;0%2C900;1%2C100;1%2C200;1%2C300;1%2C400;1%2C500;1%2C600;1%2C700;1%2C800;1%2C900&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Geist:wght@100..900&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Nunito:ital%2Cwght@0%2C200..1000;1%2C200..1000&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Hedvig+Letters+Serif:opsz@12..24&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Antonio:wght@100..700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&display=swap");

@import "tailwindcss";

@plugin "@tailwindcss/typography";
@import "tw-animate-css";

@custom-variant dark (&:where(.dark, .dark *));

:root {
   --background: oklch(1 0 0);
   --foreground: oklch(0.141 0.005 285.823);
   --card: oklch(1 0 0);
   --card-foreground: oklch(0.141 0.005 285.823);
   --popover: oklch(1 0 0);
   --popover-foreground: oklch(0.141 0.005 285.823);
   --primary: oklch(0.21 0.006 285.885);
   --primary-foreground: oklch(0.985 0 0);
   --secondary: oklch(0.967 0.001 286.375);
   --secondary-foreground: oklch(0.21 0.006 285.885);
   --muted: oklch(0.967 0.001 286.375);
   --muted-foreground: oklch(0.552 0.016 285.938);
   --accent: oklch(0.967 0.001 286.375);
   --accent-foreground: oklch(0.21 0.006 285.885);
   --destructive: oklch(0.577 0.245 27.325);
   --border: oklch(0.92 0.004 286.32);
   --input: oklch(0.92 0.004 286.32);
   --ring: oklch(0.705 0.015 286.067);
   --chart-1: oklch(0.646 0.222 41.116);
   --chart-2: oklch(0.6 0.118 184.704);
   --chart-3: oklch(0.398 0.07 227.392);
   --chart-4: oklch(0.828 0.189 84.429);
   --chart-5: oklch(0.769 0.188 70.08);
   --sidebar: oklch(0.985 0 0);
   --sidebar-foreground: oklch(0.141 0.005 285.823);
   --sidebar-primary: oklch(0.21 0.006 285.885);
   --sidebar-primary-foreground: oklch(0.985 0 0);
   --sidebar-accent: oklch(0.967 0.001 286.375);
   --sidebar-accent-foreground: oklch(0.21 0.006 285.885);
   --sidebar-border: oklch(0.92 0.004 286.32);
   --sidebar-ring: oklch(0.705 0.015 286.067);

   --radius: 8px;

   --shadow-2xs: 0 1px 3px 0px hsl(0 0% 0% / 0.05);
   --shadow-xs: 0 1px 3px 0px hsl(0 0% 0% / 0.05);
   --shadow-sm:
           0 1px 3px 0px hsl(0 0% 0% / 0.1), 0 1px 2px -1px hsl(0 0% 0% / 0.1);
   --shadow: 0 1px 3px 0px hsl(0 0% 0% / 0.1), 0 1px 2px -1px hsl(0 0% 0% / 0.1);
   --shadow-md:
           0 1px 3px 0px hsl(0 0% 0% / 0.1), 0 2px 4px -1px hsl(0 0% 0% / 0.1);
   --shadow-lg:
           0 1px 3px 0px hsl(0 0% 0% / 0.1), 0 4px 6px -1px hsl(0 0% 0% / 0.1);
   --shadow-xl:
           0 1px 3px 0px hsl(0 0% 0% / 0.1), 0 8px 10px -1px hsl(0 0% 0% / 0.1);
   --shadow-2xl: 0 1px 3px 0px hsl(0 0% 0% / 0.25);

   /* Shadcnblocks.com */
   --muted-2: oklch(92.5%, 0%, 89.876%);
   --muted-2-foreground: oklch(55.2%, 3.5%, 285.938%);

   --gradient-1: oklch(64.3%, 40.75%, 269.926%);
   --gradient-2: oklch(72.7%, 46.75%, 144.688%);
   --gradient-3: oklch(70.1%, 37.75%, 339.956%);

   /* Fonts */
   --font-sans: "Inter", sans-serif;
   --font-serif: "Roboto Serif", serif;
   --font-mono: "Roboto Mono", monospace;
   --font-cursive: "Caveat", cursive;
   --font-playfair: "Playfair Display", serif;
   --font-caveat: "Caveat", cursive;
   --font-calSans: "Cal Sans", sans-serif;
   --font-bebasNeue: "Bebas Neue", sans-serif;
   --font-anton: "Anton", sans-serif;
   --font-instrumentSerif: "Instrument Serif", serif;
   --font-merriweather: "Merriweather", serif;
   --font-figtree: "Figtree", sans-serif;
   --font-ubuntu: "Ubuntu", sans-serif;
   --font-fahkwang: "Fahkwang", sans-serif;
   --font-red-hat-text: "Red Hat Text", sans-serif;
   --font-dm-sans: "DM Sans", sans-serif;
   --font-instrument-sans: "Instrument Sans", sans-serif;
   --font-assistant: "Assistant", sans-serif;
   --font-poppins: "Poppins", sans-serif;
   --font-geist: "Geist", sans-serif;
   --font-nunito: "Nunito", sans-serif;
   --font-hedvigLettersSerif: "Hedvig Letters Serif", serif;
   --font-antonio: "Antonio", sans-serif;
}
.dark {
   --background: oklch(0.141 0.005 285.823);
   --foreground: oklch(0.985 0 0);
   --card: oklch(0.21 0.006 285.885);
   --card-foreground: oklch(0.985 0 0);
   --popover: oklch(0.21 0.006 285.885);
   --popover-foreground: oklch(0.985 0 0);
   --primary: oklch(0.92 0.004 286.32);
   --primary-foreground: oklch(0.21 0.006 285.885);
   --secondary: oklch(0.274 0.006 286.033);
   --secondary-foreground: oklch(0.985 0 0);
   --muted: oklch(0.274 0.006 286.033);
   --muted-foreground: oklch(0.705 0.015 286.067);
   --accent: oklch(0.274 0.006 286.033);
   --accent-foreground: oklch(0.985 0 0);
   --destructive: oklch(0.704 0.191 22.216);
   --border: oklch(1 0 0 / 10%);
   --input: oklch(1 0 0 / 15%);
   --ring: oklch(0.552 0.016 285.938);
   --chart-1: oklch(0.488 0.243 264.376);
   --chart-2: oklch(0.696 0.17 162.48);
   --chart-3: oklch(0.769 0.188 70.08);
   --chart-4: oklch(0.627 0.265 303.9);
   --chart-5: oklch(0.645 0.246 16.439);
   --sidebar: oklch(0.21 0.006 285.885);
   --sidebar-foreground: oklch(0.985 0 0);
   --sidebar-primary: oklch(0.488 0.243 264.376);
   --sidebar-primary-foreground: oklch(0.985 0 0);
   --sidebar-accent: oklch(0.274 0.006 286.033);
   --sidebar-accent-foreground: oklch(0.985 0 0);
   --sidebar-border: oklch(1 0 0 / 10%);
   --sidebar-ring: oklch(0.552 0.016 285.938);

   /* Shadcnblocks.com */
   --muted-2: oklch(30.1%, 0%, 89.876%);
   --muted-2-foreground: oklch(80.2%, 1%, 286.305%);

   --gradient-1: oklch(27%, 39.25%, 269.284%);
   --gradient-2: oklch(72.7%, 46.75%, 144.688%);
   --gradient-3: oklch(70.1%, 37.75%, 339.956%);
}

@theme inline {
   --color-background: var(--background);
   --color-foreground: var(--foreground);
   --color-card: var(--card);
   --color-card-foreground: var(--card-foreground);
   --color-popover: var(--popover);
   --color-popover-foreground: var(--popover-foreground);
   --color-primary: var(--primary);
   --color-primary-foreground: var(--primary-foreground);
   --color-secondary: var(--secondary);
   --color-secondary-foreground: var(--secondary-foreground);
   --color-muted: var(--muted);
   --color-muted-foreground: var(--muted-foreground);
   --color-accent: var(--accent);
   --color-accent-foreground: var(--accent-foreground);
   --color-destructive: var(--destructive);
   --color-destructive-foreground: var(--destructive-foreground);
   --color-border: var(--border);
   --color-input: var(--input);
   --color-ring: var(--ring);

   --color-chart-1: var(--chart-1);
   --color-chart-2: var(--chart-2);
   --color-chart-3: var(--chart-3);
   --color-chart-4: var(--chart-4);
   --color-chart-5: var(--chart-5);

   /* Shadcnblocks.com */
   --color-muted-2: var(--muted-2);
   --color-muted-2-foreground: var(--muted-2-foreground);
   --color-transparent: transparent;

   --radius-xs: calc(var(--radius) - 4px);
   --radius-sm: calc(var(--radius) - 4px);
   --radius-md: calc(var(--radius) - 2px);
   --radius-lg: var(--radius);
   --radius-xl: calc(var(--radius) + 4px);

   --breakpoint-sm: 640px;
   --breakpoint-md: 768px;
   --breakpoint-lg: 1024px;
   --breakpoint-xl: 1280px;
   --breakpoint-2xl: 1536px; /* default is 1536px */

   --animate-accordion-down: accordion-down 0.2s ease-out;
   --animate-accordion-up: accordion-up 0.2s ease-out;
   --animate-fade-in-out: fade-in-out 4s ease-in-out;
   --animate-fade-in: fade-in 0.7s ease-out forwards;
   --animate-progress: progress 8s linear;
   --animate-infinite-slider: infiniteSlider 20s linear infinite;
   --animate-infinite-slider-reverse: infiniteSliderReverse 20s linear infinite;
   --animate-shadow-ping: shadow-ping 1.5s ease-in-out infinite;
   --animate-flip-btn: flip-btn 6s infinite steps(2, end);
   --animate-rotate-btn: rotate-btn 3s linear infinite both;
   --animate-light-to-right-top: light-to-right 4s linear infinite;
   --animate-light-to-right-bottom: light-to-right 4s linear infinite;
   --animate-marquee: marquee 25s linear infinite;
   --animate-marquee-vertical: marquee-vertical 25s linear infinite;
   --animate-slide-to-right: slide-to-right 3s linear infinite;
   --animate-slide-to-top: slide-to-top 3s linear infinite;
   --animate-shimmer-slide: shimmer-slide var(--speed) ease-in-out infinite
   alternate;
   --animate-spin-around: spin-around calc(var(--speed) * 2) infinite linear;
   --animate-shine: shine var(--duration) infinite linear;
   --animate-ripple: ripple var(--duration, 2s) ease calc(var(--i, 0) * 0.2s)
   infinite;
   --animate-orbit: orbit calc(var(--duration) * 1s) linear infinite;
   --animate-meteor: meteor 5s linear infinite;
   --animate-line-shadow: line-shadow 15s linear infinite;
   --animate-aurora: aurora 8s ease-in-out infinite alternate;
   --animate-aurora-background: aurora-background 60s linear infinite;
   --animate-slide-down: slideDown 100ms ease-out;
   --animate-slide-up: slideUp 100ms ease-out;
   --animate-slide-left: slideLeft 250ms ease-out;
   --animate-slide-right: slideRight 250ms ease-out;

   --color-sidebar-ring: var(--sidebar-ring);
   --color-sidebar-border: var(--sidebar-border);
   --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
   --color-sidebar-accent: var(--sidebar-accent);
   --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
   --color-sidebar-primary: var(--sidebar-primary);
   --color-sidebar-foreground: var(--sidebar-foreground);
   --color-sidebar: var(--sidebar);

   --font-sans: var(--font-sans);
   --font-serif: var(--font-serif);
   --font-mono: var(--font-mono);
   --font-cursive: var(--font-cursive);

   --font-playfair: var(--font-playfair);
   --font-caveat: var(--font-caveat);
   --font-calSans: var(--font-calSans);
   --font-bebasNeue: var(--font-bebasNeue);
   --font-instrumentSerif: var(--font-instrumentSerif);
   --font-anton: var(--font-anton);
   --font-merriweather: var(--font-merriweather);
   --font-figtree: var(--font-figtree);
   --font-ubuntu: var(--font-ubuntu);
   --font-fahkwang: var(--font-fahkwang);
   --font-red-hat-text: var(--font-red-hat-text);
   --font-dm-sans: var(--font-dm-sans);
   --font-instrument-sans: var(--font-instrument-sans);
   --font-assistant: var(--font-assistant);
   --font-poppins: var(--font-poppins);
   --font-geist: var(--font-geist);
   --font-nunito: var(--font-nunito);
   --font-hedvigLettersSerif: var(--font-hedvigLettersSerif);
   --font-antonio: var(--font-antonio);

   --shadow-2xs: var(--shadow-2xs);
   --shadow-xs: var(--shadow-xs);
   --shadow-sm: var(--shadow-sm);
   --shadow: var(--shadow);
   --shadow-md: var(--shadow-md);
   --shadow-lg: var(--shadow-lg);
   --shadow-xl: var(--shadow-xl);
   --shadow-2xl: var(--shadow-2xl);

   @keyframes accordion-down {
      from {
         height: 0;
      }
      to {
         height: var(--radix-accordion-content-height);
      }
   }

   @keyframes accordion-up {
      from {
         height: var(--radix-accordion-content-height);
      }
      to {
         height: 0;
      }
   }

   @keyframes fade-in-out {
      0% {
         opacity: 0;
      }
      20% {
         opacity: 1;
      }
      80% {
         opacity: 1;
      }
      100% {
         opacity: 0;
      }
   }

   @keyframes progress {
      from {
         width: "0%";
      }
      to {
         width: "100%";
      }
   }

   @keyframes infiniteSlider {
      0% {
         transform: "translateX(0)";
      }
      100% {
         transform: "translateX(calc(-250px * 5))";
      }
   }

   @keyframes infiniteSliderReverse {
      0% {
         transform: "translateX(calc(-250px * 5))";
      }
      100% {
         transform: "translateX(0)";
      }
   }

   @keyframes fade-in-scale {
      0% {
         opacity: 0;
         transform: scale(0.95);
      }
      100% {
         opacity: 1;
         transform: scale(1);
      }
   }

   @keyframes fade-in-scale-down {
      0% {
         opacity: 0;
         transform: scale(1.1);
      }
      100% {
         opacity: 1;
         transform: scale(1);
      }
   }

   @keyframes fade-in-slide-down {
      0% {
         transform: translateY(-24px);
         opacity: 0;
      }
      100% {
         transform: translateY(0);
         opacity: 1;
      }
   }

   @keyframes transform1 {
      0%,
      25%,
      100% {
         width: 100%;
         padding-bottom: 120%;
      }
      33.33%,
      58.33% {
         width: 0%;
         padding-bottom: 0%;
      }
      66.66%,
      91.66% {
         width: 90%;
         padding-bottom: 100%;
      }
   }

   @keyframes transform2 {
      0%,
      25%,
      100% {
         width: 65%;
         padding-bottom: 65%;
      }
      33.33%,
      58.33% {
         width: 95%;
         padding-bottom: 114%;
      }
      66.66%,
      91.66% {
         width: 52%;
         padding-bottom: 52%;
      }
   }

   @keyframes transform3 {
      0%,
      25%,
      100% {
         width: 78%;
         padding-bottom: 100%;
      }
      33.33%,
      58.33% {
         width: 78%;
         padding-bottom: 94%;
      }
      66.66%,
      91.66% {
         width: 95%;
         padding-bottom: 76%;
      }
   }

   @keyframes transform4 {
      0%,
      25%,
      66.66%,
      91.66%,
      100% {
         width: 0%;
         padding-bottom: 0%;
      }
      33.33%,
      58.33% {
         width: 65%;
         padding-bottom: 46%;
      }
   }

   @keyframes image1 {
      0%,
      25%,
      100% {
         opacity: 1;
      }
      33.33%,
      58.33%,
      66.66%,
      91.66% {
         opacity: 0;
      }
   }

   @keyframes image2 {
      0%,
      25%,
      33.33%,
      58.33%,
      100% {
         opacity: 0;
      }
      66.66%,
      91.66% {
         opacity: 1;
      }
   }

   @keyframes image3 {
      0%,
      25%,
      66.66%,
      91.66%,
      100% {
         opacity: 0;
      }
      33.33%,
      58.33% {
         opacity: 1;
      }
   }

   @keyframes gradient-spin {
      0% {
         transform: translateX(-50%) translateY(-50%) rotate(0deg);
      }
      100% {
         transform: translateX(-50%) translateY(-50%) rotate(360deg);
      }
   }

   @keyframes shadow-ping {
      0% {
         boxshadow: 0 0 0 0px var(--color-neutral-100);
      }
      50% {
         boxshadow: 0 0 0 12px var(--color-neutral-300);
      }
      100% {
         boxshadow: 0 0 0 12px transparent;
      }
   }

   @keyframes show-text {
      0%,
      14.28% {
         opacity: 0;
      }
      17%,
      26% {
         opacity: 1;
      }
      28.58%,
      100% {
         opacity: 0;
      }
   }

   @keyframes flip-btn {
      to {
         transform: rotate(360deg);
      }
   }

   @keyframes rotate-btn {
      to {
         transform: rotate(90deg);
      }
   }

   @keyframes slide-to-right {
      0% {
         opacity: 0;
         left: 0;
      }
      50% {
         opacity: 1;
      }
      100% {
         opacity: 0;
         left: 80%;
      }
   }

   @keyframes slide-to-top {
      0% {
         opacity: 0;
         bottom: 0;
      }
      50% {
         opacity: 1;
      }
      100% {
         opacity: 0;
         bottom: 80%;
      }
   }

   @keyframes light-to-right {
      0% {
         transform: translate(0%);
         opacity: 0;
      }
      50% {
         opacity: 1;
      }
      100% {
         transform: translate(100%);
         opacity: 0;
      }
   }

   @keyframes marquee {
      0% {
         transform: translateX(0%);
      }
      100% {
         transform: translateX(-100%);
      }
   }

   @keyframes marquee-vertical {
      from {
         transform: translateY(0);
      }
      to {
         transform: translateY(calc(-100% - var(--gap)));
      }
   }

   @keyframes fade-in {
      0% {
         opacity: 0;
         transform: translateY(20px);
      }
      100% {
         opacity: 1;
         transform: translateY(0);
      }
   }

   @keyframes shimmer-slide {
      to {
         transform: translate(calc(100cqw - 100%), 0);
      }
   }

   @keyframes spin-around {
      0% {
         transform: translateZ(0) rotate(0);
      }
      15%,
      35% {
         transform: translateZ(0) rotate(90deg);
      }
      65%,
      85% {
         transform: translateZ(0) rotate(270deg);
      }
      100% {
         transform: translateZ(0) rotate(360deg);
      }
   }

   @keyframes shine {
      0% {
         background-position: 0% 0%;
      }
      50% {
         background-position: 100% 100%;
      }
      to {
         background-position: 0% 0%;
      }
   }

   @keyframes aurora-background {
      from {
         background-position:
                 50% 50%,
                 50% 50%;
      }
      to {
         background-position:
                 350% 50%,
                 350% 50%;
      }
   }

   @keyframes aurora {
      0% {
         background-position: 0% 50%;
         transform: rotate(-5deg) scale(0.9);
      }
      25% {
         background-position: 50% 100%;
         transform: rotate(5deg) scale(1.1);
      }
      50% {
         background-position: 100% 50%;
         transform: rotate(-3deg) scale(0.95);
      }
      75% {
         background-position: 50% 0%;
         transform: rotate(3deg) scale(1.05);
      }
      100% {
         background-position: 0% 50%;
         transform: rotate(-5deg) scale(0.9);
      }
   }

   @keyframes ripple {
      0%,
      100% {
         transform: translate(-50%, -50%) scale(1);
      }
      50% {
         transform: translate(-50%, -50%) scale(0.9);
      }
   }

   @keyframes orbit {
      0% {
         transform: rotate(calc(var(--angle) * 1deg))
         translateY(calc(var(--radius) * 1px)) rotate(calc(var(--angle) * -1deg));
      }
      100% {
         transform: rotate(calc(var(--angle) * 1deg + 360deg))
         translateY(calc(var(--radius) * 1px))
         rotate(calc((var(--angle) * -1deg) - 360deg));
      }
   }

   @keyframes meteor {
      0% {
         transform: rotate(var(--angle)) translateX(0);
         opacity: 1;
      }
      70% {
         opacity: 1;
      }
      100% {
         transform: rotate(var(--angle)) translateX(-500px);
         opacity: 0;
      }
   }

   @keyframes line-shadow {
      0% {
         background-position: 0 0;
      }
      100% {
         background-position: 100% -100%;
      }
   }

   @keyframes slideDown {
      from {
         height: 0;
      }
      to {
         height: var(--radix-collapsible-content-height);
      }
   }

   @keyframes slideUp {
      from {
         height: var(--radix-collapsible-content-height);
      }
      to {
         height: 0;
      }
   }

   @keyframes slideLeft {
      from {
         width: 0;
      }
      to {
         width: var(--radix-collapsible-content-width);
      }
   }
   @keyframes slideRight {
      from {
         width: var(--radix-collapsible-content-width);
      }
      to {
         width: 0;
      }
   }
}

@utility container {
   margin-inline: auto;
   padding-inline: 2rem;
}

@layer components {
   button {
      cursor: pointer;
   }
   [class*="border"] {
      @apply border-border;
   }
}

@layer base {
   * {
      @apply border-border outline-ring/50;
   }
   body {
      @apply bg-background text-foreground font-sans antialiased;
      scrollbar-gutter: stable;
   }
}

#wrapper {
   margin-top: 60px;
}

.hide-scrollbar {
   scrollbar-width: none; /* Firefox */
   -ms-overflow-style: none; /* IE 10+ */
}

.hide-scrollbar::-webkit-scrollbar {
   display: none; /* Chrome, Safari, Opera */
}

html body[data-scroll-locked] {
   overflow-y: scroll !important;
   --removed-body-scroll-bar-size: 0 !important;
   margin-right: 0 !important;
   margin-top: 60px !important;
   &#explorer {
      margin-top: 0px !important;
   }
}
```

### Step 2: Replace :root and .dark sections
Find existing `:root` and `.dark` blocks in globals.css and replace with chosen theme variables.

### Step 3: Verify Tailwind Config
Ensure `tailwind.config.ts` references CSS variables:
```typescript
theme: {
  extend: {
    colors: {
      background: 'hsl(var(--background))',
      foreground: 'hsl(var(--foreground))',
      // ... other color mappings
    }
  }
}

```
## CSS Variable Structure

Each theme includes:

**Light Mode (`:root`):**
- `--background`: Page background
- `--foreground`: Main text color
- `--primary`: Primary action color (buttons, links)
- `--secondary`: Secondary elements
- `--accent`: Highlights, badges
- `--muted`: Disabled states, subtle backgrounds
- `--destructive`: Error/delete actions
- `--border`, `--input`, `--ring`: UI element styling
- `--card`, `--popover`: Elevated surfaces
- `--chart-1` through `--chart-5`: Data visualization colors
- `--sidebar-*`: Sidebar-specific colors
- `--radius`: Border radius (e.g., `1.25rem`)
- `--shadow-*`: Box shadow definitions
- Font variables: `--font-sans`, `--font-serif`, `--font-mono`

**Dark Mode (`.dark`):**
Same variable names with adjusted values for dark backgrounds.

---

## Example: Applying Claude Theme

**User request:** "Change to Claude theme"

**Action:**
1. Read current `app/globals.css`
2. Replace `:root` section with Claude light mode variables
3. Replace `.dark` section with Claude dark mode variables
4. Preserve other CSS (typography, base styles)

**Claude Theme CSS Variables:**

```css
:root {
  --background: oklch(0.92 0.00 48.72);
  --foreground: oklch(0.28 0.04 260.03);
  --card: oklch(0.97 0.00 106.42);
  --card-foreground: oklch(0.28 0.04 260.03);
  --popover: oklch(0.97 0.00 106.42);
  --popover-foreground: oklch(0.28 0.04 260.03);
  --primary: oklch(0.59 0.20 277.12);
  --primary-foreground: oklch(1.00 0 0);
  --secondary: oklch(0.87 0.00 56.37);
  --secondary-foreground: oklch(0.45 0.03 256.80);
  --muted: oklch(0.92 0.00 48.72);
  --muted-foreground: oklch(0.55 0.02 264.36);
  --accent: oklch(0.94 0.03 321.94);
  --accent-foreground: oklch(0.37 0.03 259.73);
  --destructive: oklch(0.64 0.21 25.33);
  --destructive-foreground: oklch(1.00 0 0);
  --border: oklch(0.87 0.00 56.37);
  --input: oklch(0.87 0.00 56.37);
  --ring: oklch(0.59 0.20 277.12);
  --chart-1: oklch(0.59 0.20 277.12);
  --chart-2: oklch(0.51 0.23 276.97);
  --chart-3: oklch(0.46 0.21 277.02);
  --chart-4: oklch(0.40 0.18 277.37);
  --chart-5: oklch(0.36 0.14 278.70);
  --sidebar: oklch(0.87 0.00 56.37);
  --sidebar-foreground: oklch(0.28 0.04 260.03);
  --sidebar-primary: oklch(0.59 0.20 277.12);
  --sidebar-primary-foreground: oklch(1.00 0 0);
  --sidebar-accent: oklch(0.94 0.03 321.94);
  --sidebar-accent-foreground: oklch(0.37 0.03 259.73);
  --sidebar-border: oklch(0.87 0.00 56.37);
  --sidebar-ring: oklch(0.59 0.20 277.12);
  --font-sans: Plus Jakarta Sans, sans-serif;
  --font-serif: Lora, serif;
  --font-mono: Roboto Mono, monospace;
  --radius: 1.25rem;
}

.dark {
  --background: oklch(0.22 0.01 67.44);
  --foreground: oklch(0.93 0.01 255.51);
  --card: oklch(0.28 0.01 59.34);
  --card-foreground: oklch(0.93 0.01 255.51);
  --popover: oklch(0.28 0.01 59.34);
  --popover-foreground: oklch(0.93 0.01 255.51);
  --primary: oklch(0.68 0.16 276.93);
  --primary-foreground: oklch(0.22 0.01 67.44);
  --secondary: oklch(0.34 0.01 59.42);
  --secondary-foreground: oklch(0.87 0.01 258.34);
  --muted: oklch(0.28 0.01 59.34);
  --muted-foreground: oklch(0.71 0.02 261.32);
  --accent: oklch(0.39 0.01 59.47);
  --accent-foreground: oklch(0.87 0.01 258.34);
  --destructive: oklch(0.64 0.21 25.33);
  --destructive-foreground: oklch(0.22 0.01 67.44);
  --border: oklch(0.34 0.01 59.42);
  --input: oklch(0.34 0.01 59.42);
  --ring: oklch(0.68 0.16 276.93);
  --chart-1: oklch(0.68 0.16 276.93);
  --chart-2: oklch(0.59 0.20 277.12);
  --chart-3: oklch(0.51 0.23 276.97);
  --chart-4: oklch(0.46 0.21 277.02);
  --chart-5: oklch(0.40 0.18 277.37);
  --sidebar: oklch(0.34 0.01 59.42);
  --sidebar-foreground: oklch(0.93 0.01 255.51);
  --sidebar-primary: oklch(0.68 0.16 276.93);
  --sidebar-primary-foreground: oklch(0.22 0.01 67.44);
  --sidebar-accent: oklch(0.39 0.01 59.47);
  --sidebar-accent-foreground: oklch(0.87 0.01 258.34);
  --sidebar-border: oklch(0.34 0.01 59.42);
  --sidebar-ring: oklch(0.68 0.16 276.93);
  --font-sans: Plus Jakarta Sans, sans-serif;
  --font-serif: Lora, serif;
  --font-mono: Roboto Mono, monospace;
  --radius: 1.25rem;
}
```

---

## Getting Full Theme CSS

To get complete CSS for any theme:

1. **Official Themes Source:** https://ui.shadcn.com/themes
2. **Community Themes:**
   - tweakcn themes: Search "tweakcn shadcn themes"
   - styleglide themes: Search "styleglide shadcn themes"
3. **Theme Generators:** Online tools for creating custom themes

**Workflow:**
- User requests theme → Look up theme CSS variables
- If theme not in this skill → Search official sources
- Copy `:root` and `.dark` blocks → Replace in globals.css

---

## Color Space: OKLCH

Themes use OKLCH color space:
- **Format:** `oklch(lightness chroma hue)`
- **Benefits:** Perceptually uniform, better gradients, wider gamut
- **Browser Support:** Modern browsers (2023+)
- **Fallback:** Consider HSL fallbacks for older browsers if needed

---

## Theme Selection Guide

**Corporate/Professional:** Default, Blue, Cleanslate, Modern Minimal
**Creative/Bold:** Cyberpunk, Neo Brutalism, Claude, Claymorphism
**Nature/Organic:** Citrus, Kodama Grove, Spring Bouquet
**Warm/Inviting:** Amber Minimal, Sunset Horizon, Red
**Developer/Tech:** Supabase, Vercel, Typewriter
**Minimal/Clean:** Modern Minimal, Vercel, Typewriter, Cleanslate

---

## Usage Tips

- **Test both modes:** Always verify light + dark mode appearance
- **Accessibility:** Check contrast ratios (WCAG AA minimum)
- **Brand alignment:** Match theme to brand colors/identity
- **User preference:** Support system theme detection
- **Gradual changes:** Preview theme before committing
- **Custom tweaks:** Adjust individual variables post-application

---

## Common Requests

**"Change to dark theme"** → Apply dark mode toggle, not full theme change
**"Make it more colorful"** → Suggest Cyberpunk, Neo Brutalism, Spring Bouquet
**"Corporate look"** → Default, Blue, Cleanslate
**"Match Supabase"** → Apply Supabase theme
**"Minimalist design"** → Modern Minimal, Vercel, Typewriter

---

**Reference:** https://ui.shadcn.com/themes
