---
name: component-naming
description: Enforces consistent React component naming conventions across the portfolio codebase. Use when creating, reviewing, or refactoring components.
---

# Component Naming Conventions

Use this guide when creating or modifying React components to ensure consistent naming across the portfolio.

---

## Naming Rules

### 1. PascalCase for Components

All React components use PascalCase:

```typescript
// ✅ Good
export const FeaturedPost = () => {};
export const TagFilter = () => {};

// ❌ Bad
export const featuredPost = () => {};
export const featured_post = () => {};
```

### 2. Domain + Role Pattern

Combine domain context with component role for clarity:

```typescript
// ✅ Good - Clear domain and role
export const FeaturedPost = () => {};     // Featured (domain) + Post (role)
export const TagFilter = () => {};        // Tag (domain) + Filter (role)
export const ReadingProgress = () => {};  // Reading (domain) + Progress (role)
export const MetricCard = () => {};       // Metric (domain) + Card (role)
export const HeroSection = () => {};      // Hero (domain) + Section (role)

// ❌ Bad - Too generic or unclear
export const Card = () => {};             // No domain context
export const Filter = () => {};           // No specificity
export const Section = () => {};          // Meaningless
```

### 3. Compound Components for Subparts

Use dot notation for related subcomponents:

```typescript
// ✅ Good - Compound component pattern
export const PostCard = () => {};
PostCard.Image = () => {};
PostCard.Title = () => {};
PostCard.Meta = () => {};

// Usage
<PostCard>
  <PostCard.Image src={...} />
  <PostCard.Title>...</PostCard.Title>
  <PostCard.Meta date={...} />
</PostCard>

// ❌ Bad - Flat naming for related components
export const PostCardImage = () => {};
export const PostCardTitle = () => {};
export const PostCardMeta = () => {};
```

### 4. Avoid Problematic Suffixes

Never use these suffixes:

```typescript
// ❌ Avoid these suffixes
export const CardContainer = () => {};    // -Container
export const PostWrapper = () => {};      // -Wrapper
export const DataComponent = () => {};    // -Component
export const ListElement = () => {};      // -Element

// ✅ Use clear domain + role instead
export const MetricCard = () => {};
export const PostList = () => {};
export const TagBadge = () => {};
```

### 5. Avoid Layout/Styling Descriptions

Names should describe purpose, not appearance:

```typescript
// ❌ Bad - Describes layout/styling
export const LeftSidebar = () => {};
export const BigHeader = () => {};
export const RedButton = () => {};
export const TwoColumnGrid = () => {};

// ✅ Good - Describes purpose
export const NavigationSidebar = () => {};
export const PageHeader = () => {};
export const DangerButton = () => {};
export const BentoGrid = () => {};
```

---

## File Naming Convention

Files use **kebab-case** matching the component name:

| Component | File Name |
|-----------|-----------|
| `FeaturedPost` | `featured-post.tsx` |
| `TagFilter` | `tag-filter.tsx` |
| `ReadingProgress` | `reading-progress.tsx` |
| `MetricCard` | `metric-card.tsx` |
| `HeroSection` | `hero-section.tsx` |

---

## Component Location

| Location | Purpose |
|----------|---------|
| `components/` | Reusable components (not shadcn/ui) |
| `components/ui/` | shadcn/ui primitives (DO NOT MODIFY) |
| `components/shared/` | Shared layout components |
| `app/(blog)/_components/` | Route-specific, single-use components |

---

## Validation Checklist

When reviewing component names:

- [ ] Uses PascalCase
- [ ] Has clear domain context (not just "Card", "List", "Item")
- [ ] Has clear role (Chart, Card, List, Section, Filter, etc.)
- [ ] No -Container, -Wrapper, -Component suffixes
- [ ] No layout/styling descriptions (Left, Big, Red, TwoColumn)
- [ ] File name matches component in kebab-case
- [ ] Related subcomponents use compound pattern

---

## Examples for Blog Redesign

**Good patterns:**

| Component | Domain | Role |
|-----------|--------|------|
| `FeaturedPost` | Featured | Post |
| `TagFilter` | Tag | Filter |
| `ReadingProgress` | Reading | Progress |
| `PostGrid` | Post | Grid |
| `AuthorCard` | Author | Card |
| `BentoGrid` | Bento | Grid |
| `HeroSection` | Hero | Section |
| `LatestPosts` | Latest | Posts |
| `SkillsGrid` | Skills | Grid |
| `ContactCta` | Contact | Cta |

**Anti-patterns to avoid:**

- Generic names: `Card`, `Grid`, `List`, `Section`
- Layout names: `LeftPanel`, `MainContent`, `TopSection`
- Suffix pollution: `CardContainer`, `ListWrapper`, `PostComponent`

---

## Related Files

- `.claude/skills/design-language-system/SKILL.md` - Design system guidelines
- `apps/blog/src/components/` - Blog components
- `apps/blog/src/components/ui/` - shadcn/ui (do not modify)
