---
name: section-backgrounds
description: Apply branding guidelines to page sections after style cleanup. Implements 60-30-10 color rule, alternates section backgrounds, and ensures visual hierarchy. Use for each page after running remove-inline-styles.
---

# Branding Implementation

Apply branding guidelines to create aesthetically clean websites.

## Workflow

1. **Review Page Sections** - Identify all sections on the page
2. **Apply 60-30-10 Rule** - Distribute colors appropriately
3. **Alternate Backgrounds** - Create visual rhythm
4. **Check Visual Hierarchy** - Ensure proper emphasis
5. **Verify Consistency** - Match overall brand style

## 60-30-10 Color Rule

See references/design-rules.md for details.

**60% - Dominant (Background)**
- Main page background: bg-background
- Most section backgrounds
- Creates visual foundation

**30% - Secondary (Supporting)**
- Alternating sections: bg-muted
- Cards and containers
- Creates depth and separation

**10% - Accent (Emphasis)**
- CTAs and buttons: bg-primary
- Highlights and important elements
- Draws attention to key actions

## Section Background Pattern

Alternate backgrounds for visual rhythm:

```
Section 1 (Hero):      bg-background
Section 2 (Logos):     bg-muted
Section 3 (Features):  bg-background
Section 4 (Process):   bg-muted
Section 5 (Pricing):   bg-background
Section 6 (Testimonial): bg-muted
Section 7 (FAQ):       bg-background
Section 8 (CTA):       bg-primary (accent - 10%)
Section 9 (Footer):    bg-muted or bg-background
```

## Visual Hierarchy Guidelines

**Primary Focus (10%):**
- Hero headline
- Primary CTA buttons
- Key statistics

**Secondary Focus (30%):**
- Section titles
- Feature highlights
- Pricing cards

**Supporting Content (60%):**
- Body text
- Descriptions
- Background elements

## Section Styling

### Hero Section
```jsx
<section className="bg-background">
  {/* Full-width, prominent */}
</section>
```

### Feature Sections
```jsx
<section className="bg-muted py-16 md:py-24">
  <div className="container">
    {/* Contained content */}
  </div>
</section>
```

### CTA Section
```jsx
<section className="bg-primary text-primary-foreground py-16">
  {/* Accent color, draws attention */}
</section>
```

## Spacing Consistency

Standard section padding:
- Mobile: py-12 or py-16
- Tablet: md:py-20
- Desktop: lg:py-24

Container usage:
```jsx
<div className="container">
  {/* All content centered, max-width applied */}
</div>
```

## Output

- Sections with appropriate backgrounds
- 60-30-10 color distribution
- Consistent spacing
- Clear visual hierarchy
- Professional, clean appearance
