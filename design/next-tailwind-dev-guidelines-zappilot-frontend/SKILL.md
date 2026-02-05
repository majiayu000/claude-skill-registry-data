---
name: next-tailwind-dev-guidelines
description:
  Specialized development guidelines for the Zap Pilot frontend built with Next.js 15, React 19,
  Tailwind CSS v4, and TypeScript. Covers service-first architecture, component composition
  patterns, TanStack Query integration, Radix UI components, Web3 wallet integration via ThirdWeb
  SDK, routing with Next.js App Router, and progressive web app optimization. Use when working with
  React components, API integration, styling, data fetching, wallet connectivity, or building new
  features.
---

# Next.js + Tailwind Development Guidelines

**Tech Stack**: Next.js 15, React 19, Tailwind CSS v4, Radix UI, TanStack Query, ThirdWeb SDK v5,
TypeScript 5

This skill provides development guidelines specifically for the Zap Pilot frontend codebase. It
follows a **progressive disclosure pattern** - start here for the overview, then consult specific
resource files as needed.

## Core Principles

1. **Service-First Architecture**: All API operations use service functions (no classes)
2. **Component Composition**: Reusable, well-typed components with clear interfaces
3. **Type Safety**: Comprehensive TypeScript with strict configuration
4. **Performance**: Lazy loading, memoization, and React Query caching
5. **Accessibility**: ARIA labels and keyboard navigation support

## Quick Reference

### When Working With...

- **Components**: See `@components.md` for Radix UI patterns, composition, and prop interfaces
- **Routing**: See `@routing.md` for Next.js App Router patterns, navigation, and dynamic routes
- **Data Fetching**: See `@data-fetching.md` for TanStack Query patterns and caching strategies
- **Styling**: See `@styling.md` for Tailwind utilities, design tokens, and animations
- **Web3**: See `@web3-integration.md` for ThirdWeb SDK, wallet connectivity, and chain management

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── layout.tsx    # Root layout with providers
│   │   ├── page.tsx      # Home page
│   │   └── bundle/       # Bundle sharing feature
│   ├── components/       # Feature-based component organization
│   │   ├── ui/           # Design system components
│   │   ├── PortfolioAllocation/  # Portfolio management
│   │   ├── SwapPage/     # Trading interface
│   │   ├── Web3/         # Wallet connectivity
│   │   └── shared/       # Cross-feature components
│   ├── hooks/            # Custom hooks for business logic
│   │   ├── queries/      # React Query hooks
│   │   └── *.ts          # Domain-specific hooks
│   ├── services/         # API integration (service functions)
│   │   ├── accountService.ts    # User & wallet management
│   │   ├── intentService.ts     # Transaction execution
│   │   └── analyticsService.ts  # Portfolio analytics
│   ├── providers/        # React Context providers
│   ├── lib/              # Utilities and helpers
│   ├── types/            # TypeScript definitions
│   └── config/           # Configuration files
├── tests/                # Vitest unit tests and Playwright E2E
├── public/               # Static assets and PWA configuration
├── package.json
└── next.config.ts
```

## Common Development Tasks

### Creating a New Component

1. Define types in component file or `src/types/`
2. Create service functions in appropriate `src/services/` file
3. Create custom hooks for business logic in `src/hooks/`
4. Build UI component with proper TypeScript types
5. Add tests in `tests/unit/`
6. Document with JSDoc comments

### Creating a New API Integration

1. Add service function in `src/services/[feature]Service.ts`
2. Create React Query hook in `src/hooks/queries/`
3. Handle loading, error, and success states
4. Add error boundaries where needed

### Adding a New Page

1. Create route in `src/app/[route]/page.tsx`
2. Set up layout if needed (`layout.tsx`)
3. Implement page component with proper meta tags
4. Add navigation links
5. Test routing and data fetching

## Development Workflow

```bash
# Type check
npm run type-check

# Run tests
npm run test:unit

# Lint and format
npm run lint
npm run format

# Start dev server
npm run dev
```

## File Naming Conventions

- **Components**: PascalCase (e.g., `PortfolioCard.tsx`)
- **Hooks**: camelCase with `use` prefix (e.g., `usePortfolioData.ts`)
- **Services**: camelCase with `Service` suffix (e.g., `analyticsService.ts`)
- **Utils**: camelCase (e.g., `formatCurrency.ts`)
- **Types**: PascalCase (e.g., `PortfolioData.ts`)
- **Test files**: `*.test.ts` or `*.spec.ts`

## Progressive Disclosure Resources

For detailed guidance on specific topics, reference these files:

- `@components.md` - Radix UI patterns, component composition, prop interfaces, design system
- `@routing.md` - Next.js App Router, dynamic routes, navigation, layouts
- `@data-fetching.md` - TanStack Query patterns, caching, mutations, optimistic updates
- `@styling.md` - Tailwind CSS utilities, design tokens, animations, responsive design
- `@web3-integration.md` - ThirdWeb SDK integration, wallet connectivity, transaction handling
- `@main.md` - Additional patterns, error handling, testing standards, security practices

Use `@filename.md` syntax to include specific resource files when needed for deeper guidance.
