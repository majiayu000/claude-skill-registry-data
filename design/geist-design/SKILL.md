---
name: geist-design
description: Review UI code for Geist Design System compliance (Vercel's design system). Use when asked to "check Geist", "review design", "apply Geist", or to audit whether a file conforms to the Geist Design System.
argument-hint: <file-or-pattern>
metadata:
  author: baan
  version: "1.0.0"
---

# Geist Design System Review

Review UI code against Vercel's Geist Design System.

## How It Works

1. Fetch the latest Geist guidelines from the sources below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all Geist rules
4. Output findings in `file:line` format with fix suggestions

## Guidelines Sources

Fetch before each review:

```
https://vercel.com/geist/introduction
https://vercel.com/geist/colors
https://vercel.com/geist/typography
```

## Core Geist Rules to Check

### Typography
- Minimum font size: `text-xs` (12px). `text-[10px]` or smaller is a violation
- Body text: `text-sm` (14px) = `text-copy-14`
- Labels/captions: `text-xs` (12px) = `text-label-12`
- Card/section titles: `text-base font-semibold` = `text-heading-16`
- Page titles: `text-2xl font-bold` = `text-heading-24`
- Numbers/data: always add `tabular-nums`
- Headings: consider `text-wrap: balance` (`text-balance`) to prevent widows

### Color (neutral-first)
- Primary text: `text-neutral-900` (Geist Color 10)
- Secondary text: `text-neutral-800` (Geist Color 9) — NOT `text-neutral-700`
- Tertiary/muted: `text-neutral-500`
- Labels/hints: `text-neutral-400`
- Borders: `border-neutral-200` (default), `border-neutral-300` (hover)
- Backgrounds: `bg-white` (card), `bg-neutral-50` (subtle)
- **Prohibited**: `bg-muted/50`, `text-muted-foreground` — use explicit neutral classes

### Spacing (generous)
- Card padding: `p-4` minimum (not `p-3`)
- List item gaps: `space-y-2.5` or `space-y-3` (not `space-y-2`)
- Grid gaps: `gap-3` or `gap-4` (not `gap-2`)
- Section spacing: `space-y-5` or `space-y-6`

### Components (shadcn/ui)
- Badge warning state: `Badge variant="outline"` with `text-amber-700 border-amber-300` — NOT `bg-amber-50` filled
- Badge shape: `rounded-md` for chips (not `rounded-full`)
- Lists with bullets: use `<ul><li>` structure — NOT `whitespace-pre-line` with string bullets
- Never use raw `bg-muted`, `bg-muted/50`, `text-muted-foreground` in components

### Accent Colors
- Only use accent colors with semantic meaning
- Green (`text-green-600`): success/completed states only
- Amber (`text-amber-700`): warning states only
- Red (`text-red-600`): error/destructive only
- No decorative accent colors

## Output Format

Group findings by file using `file:line` format:

```
file.tsx:42  text-[10px] → text-xs  (minimum font size)
file.tsx:87  text-neutral-700 → text-neutral-800  (Geist Color 9 for secondary text)
file.tsx:120 space-y-2 → space-y-2.5  (Geist spacing)
file.tsx:200 bg-muted/50 → bg-neutral-50 border-neutral-200  (explicit classes)
```

Prioritize: accessibility violations > color violations > spacing > typography refinements.

## Usage

When a user provides a file or pattern:
1. Fetch Geist docs from the sources above for latest rules
2. Read the specified files
3. Apply all rules
4. Output findings with terse fix suggestions

If no files specified, ask which files to review.
