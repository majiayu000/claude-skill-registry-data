---
name: infopage
description: Create clean, single-file HTML pages for displaying information. Use for quick reference pages, comparisons, lists, or any data you want to view in a browser.
---

# Infopage

Create document-style HTML pages. Utilitarian, readable, no decoration.

## Style

Warm, readable, classic. Serif typography with subtle color accents.

## Color Palette

| Name | Hex |
|------|-----|
| cream | `#f5f3e8` |
| black | `#222` |
| red | `#db5439` |
| pink | `rgba(220, 84, 57, 0.5)` |
| gold | `#eebe6d` |

### Valid Combinations

| Background | Text |
|------------|------|
| cream | black |
| red | black |
| pink | black |
| gold | black |
| black | cream |
| black | gold |

Use any combination, but:
- **Cards must all use the same combination**
- **Page background must differ from card background**

## Base Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PAGE_TITLE</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
    :root {
      --cream: #f5f3e8;
      --black: #222;
      --red: #db5439;
      --pink: rgba(220, 84, 57, 0.5);
      --gold: #eebe6d;
    }
  </style>
  <script>
    tailwind.config = {
      theme: {
        fontFamily: {
          serif: ['"Libre Baskerville"', 'Georgia', 'serif'],
        },
        extend: {
          colors: {
            cream: 'var(--cream)',
            black: 'var(--black)',
            red: 'var(--red)',
            pink: 'var(--pink)',
            gold: 'var(--gold)',
          }
        }
      }
    }
  </script>
</head>
<body class="bg-cream text-black font-serif min-h-screen">
  <div class="max-w-6xl mx-auto px-8 py-16">
    <header class="mb-12">
      <h1 class="text-2xl font-bold uppercase tracking-wide">PAGE_TITLE</h1>
      <p class="text-sm mt-2 italic text-black/70">SUBTITLE</p>
    </header>

    <main>
      <!-- Content -->
    </main>

    <footer class="mt-16 pt-8 border-t border-black/20 text-sm text-black/60">
      Generated DATE
    </footer>
  </div>
</body>
</html>
```

## Patterns

### Section with Heading

```html
<section>
  <h2 class="text-lg font-bold uppercase tracking-wide mb-4">Section Title</h2>
  <p class="leading-relaxed">Body text goes here.</p>
</section>
```

### Numbered List

```html
<ol class="space-y-3 list-decimal list-inside">
  <li><span class="font-semibold">Step one.</span> Description.</li>
  <li><span class="font-semibold">Step two.</span> Description.</li>
</ol>
```

### Bullet List

```html
<ul class="space-y-2">
  <li class="flex gap-3">
    <span>*</span>
    <span>Item description</span>
  </li>
</ul>
```

### Divider

```html
<hr class="my-8 border-black">
```

### Key-Value

```html
<dl class="space-y-2">
  <div class="flex gap-4">
    <dt class="font-semibold min-w-32">Label</dt>
    <dd>Value</dd>
  </div>
</dl>
```

### Table

```html
<table class="w-full text-sm border-collapse">
  <thead>
    <tr class="border-b-2 border-red">
      <th class="text-left py-3 px-4 font-bold">Name</th>
      <th class="text-left py-3 px-4 font-bold">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b border-black/10">
      <td class="py-3 px-4">Item</td>
      <td class="py-3 px-4 text-black/70">Details</td>
    </tr>
  </tbody>
</table>
```

### Cards (Preferred for Comparisons)

Cards show key facts at a glance. No verbose descriptions.

```html
<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
  <div class="bg-pink border-4 border-red p-5">
    <div class="flex justify-between items-start mb-3">
      <a href="https://example.com" class="font-bold uppercase text-sm tracking-wide hover:underline" target="_blank">App Name</a>
      <span class="text-xs font-bold bg-gold text-black px-2 py-1">92/100</span>
    </div>
    <p class="text-xl font-bold mb-3">$12/mo</p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="text-xs border border-black/30 px-2 py-1">Offline</span>
      <span class="text-xs border border-black/30 px-2 py-1">Local AI</span>
    </div>
    <dl class="text-sm space-y-1">
      <div class="flex justify-between">
        <dt class="text-black/70">Free Tier</dt>
        <dd class="font-semibold">Yes</dd>
      </div>
      <div class="flex justify-between">
        <dt class="text-black/70">Trial Length</dt>
        <dd>2,000 words/week</dd>
      </div>
    </dl>
  </div>
</div>
```

**Card content:**
- Clickable title (links to website, no separate "Visit Website")
- Rank/score badge
- Price
- Tags for key features
- Key facts (free tier, trial length, etc.)
- **No description paragraphs** - that's where AI waffle creeps in

**Grid columns:**
- 2-3 columns: `md:grid-cols-2 lg:grid-cols-3`
- More columns for simpler cards: `md:grid-cols-3 lg:grid-cols-4`

### Note/Callout

```html
<div class="border-l-4 border-red pl-4 my-6 py-3 pr-4">
  <p class="text-sm italic">Note: Important information here.</p>
</div>
```

### Tags/Badges

```html
<span class="text-xs font-bold bg-gold text-black px-2 py-1">Featured</span>
<span class="text-xs font-bold bg-red text-cream px-2 py-1">New</span>
<span class="text-xs border border-black/30 px-2 py-1">Tag</span>
```

### Links

```html
<a href="#" class="text-red hover:underline">Link text →</a>
```

## File Naming

**Default:** `index.html` in current directory

**If index.html exists:**
1. Ask user before overwriting, OR
2. Create a subdirectory: `./topic-name/index.html`

**Never:** Long descriptive filenames like `compare-voice-apps-on-mac.html`

**Examples:**
```
# Good
./index.html
./voice-apps/index.html
~/Desktop/examples/index.html

# Bad
./compare-voice-apps-on-mac.html
./my-keyboard-shortcuts-reference.html
```

## Rules

- Use only palette colors (cream, black, red, pink, gold)
- Cards use same bg color, distinct from page bg
- Border-4 for cards, not border-1
- No rounded corners
- Serif typography (Libre Baskerville)
- Generous whitespace
- **Prefer card grids over lists for comparisons**
- **Cards are minimal** - name + one key fact, click to expand
- **No AI waffle** - no "gold standard", "exceptionally accurate", just facts
- Transitions only on user action (expand/collapse OK, no auto-animations)

## TODO: Future Looks

- [ ] Monospace/terminal variant
- [ ] Sans-serif modern variant
- [ ] Dark mode (white on black)
