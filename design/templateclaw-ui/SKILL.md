---
name: templateclaw-ui
description: "Generate modern UI components — cards, forms, navigation, modals, tables, hero sections, footers, and pricing tables. 2026 glassmorphism design with Tailwind CSS. Copy-paste ready."
allowed-tools: Read, Write, Edit
argument-hint: "[component: cards|forms|nav|modal|table|hero|footer|pricing]"
---

# TemplateClaw — UI Component Generator

Generate copy-paste ready UI components with 2026 design trends.

## When Invoked

1. If argument provided (e.g., `/templateclaw-ui cards`), generate that component
2. If no argument, ask: "Which component? (cards / forms / nav / modal / table / hero / footer / pricing)"
3. Multiple components: `/templateclaw-ui cards,forms,nav` generates all three

## Components

### Cards (6 variants)
- **Feature Card**: Icon + title + description + CTA link
- **Stats Card**: Big number + label + trend indicator (↑/↓)
- **Profile Card**: Avatar + name + role + social links
- **Product Card**: Image placeholder + title + price + add-to-cart
- **Testimonial Card**: Quote + author + star rating
- **Pricing Card**: Tier name + price + features list + CTA button

### Forms (4 variants)
- **Login Form**: Email + password + remember me + social login buttons
- **Signup Form**: Name + email + password + confirm + terms checkbox
- **Contact Form**: Name + email + subject + message textarea + submit
- **Search Form**: Search input with icon + filter dropdowns + results area

### Navigation (3 variants)
- **Top Navbar**: Logo + links + search + CTA button + mobile hamburger menu
- **Sidebar Nav**: Logo + grouped links with icons + collapse toggle
- **Breadcrumb**: Home > Category > Current with separator icons

### Modal (3 variants)
- **Confirm Modal**: Title + message + Cancel/Confirm buttons + backdrop blur
- **Form Modal**: Title + form fields + validation + submit
- **Image Modal**: Lightbox with zoom + prev/next + close

### Table (2 variants)
- **Data Table**: Sortable headers + search + pagination + row actions
- **Comparison Table**: Feature rows × product columns + check/cross icons

### Hero Section (3 variants)
- **Centered Hero**: Headline + subtitle + CTA + gradient mesh background
- **Split Hero**: Text left + visual right (gradient placeholder) + floating elements
- **Video Hero**: Background video placeholder + overlay text + play button

### Footer (2 variants)
- **Multi-column Footer**: Logo + 4 link columns + newsletter + social icons + copyright
- **Minimal Footer**: Logo + essential links + copyright (single row)

### Pricing Table (2 variants)
- **3-Tier Pricing**: Free/Pro/Enterprise cards + feature comparison + annual toggle
- **Usage-based Pricing**: Slider + calculated price + feature list

## Design Tokens

All components share:
```css
/* Glassmorphism Card */
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
}

/* Gradient Button */
.btn-gradient {
  background: linear-gradient(135deg, #7C3AED, #EC4899);
  transition: all 0.3s ease;
}
.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(124, 58, 237, 0.3);
}

/* Input Field */
.input-glass {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #F8FAFC;
}
.input-glass:focus {
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2);
}
```

## Output Format

- Each component as a self-contained HTML snippet
- Include a preview wrapper (`<div class="preview">`) showing the component
- Tailwind classes + minimal custom CSS
- Document props/slots with HTML comments:
  ```html
  <!-- PROP: title (string) -->
  <!-- PROP: icon (svg or emoji) -->
  <!-- SLOT: card-content -->
  ```
- Accessibility: ARIA roles, keyboard support, focus trap for modals
