---
name: Frontend Architecture
description: This skill activates when users discuss component architecture, design systems, CSS methodologies, or frontend patterns. Provides guidance on React patterns, state management architecture, component hierarchies, and scalable frontend design systems.
---

# Frontend Architecture

Design scalable, maintainable frontend architectures for WordPress themes and modern web applications.

## When This Activates

- "design system", "component architecture", "CSS methodology"
- "state management", "component hierarchy", "atomic design"
- "frontend structure", "architecture patterns", "scalable frontend"
- User planning large-scale React/Vue/Svelte applications
- Discussing how to organize components and styles

---

## Component Architecture Patterns

### Atomic Design Methodology

```
Atoms → Molecules → Organisms → Templates → Pages
```

**For SkyyRose:**
```
atoms/
├── Button/              # Primary CTA buttons (#B76E79)
├── Input/               # Form inputs with luxury styling
├── Icon/                # SVG icon system
└── Typography/          # Archivo, sans-serif

molecules/
├── FormField/           # Label + Input + Error
├── ProductCard/         # Image + Title + Price + CTA
├── SearchBar/           # Input + Icon + Button
└── NavItem/             # Icon + Text + Badge

organisms/
├── ProductGrid/         # Multiple ProductCards
├── CheckoutForm/        # Multiple FormFields
├── SiteHeader/          # Logo + Nav + Search + Cart
└── ProductCarousel/     # Swiper + ProductCards

templates/
├── CollectionLayout/    # Header + Grid + Filters
├── ProductLayout/       # Header + 3D Viewer + Details
└── CheckoutLayout/      # Header + Form + Summary

pages/
├── HomePage/            # Hero + Collections + Features
├── CollectionPage/      # CollectionLayout with data
└── ProductPage/         # ProductLayout with product
```

### Feature-Based Organization

```typescript
// For complex features, group by domain
features/
├── product-configurator/
│   ├── components/
│   │   ├── ColorPicker.tsx
│   │   ├── SizeSelector.tsx
│   │   └── Scene3D.tsx
│   ├── hooks/
│   │   ├── useConfiguration.ts
│   │   └── use3DModel.ts
│   ├── store/
│   │   └── configurationSlice.ts
│   ├── types/
│   │   └── configuration.ts
│   └── index.tsx        # Public API

├── checkout/
│   ├── components/
│   ├── hooks/
│   ├── store/
│   └── index.tsx
```

---

## State Management Architecture

### When to Use What

| State Type | Solution | Example |
|------------|----------|---------|
| **Local UI** | useState | Modal open/closed, form inputs |
| **Form** | React Hook Form | Checkout, contact forms |
| **Shared UI** | Context + Reducer | Theme (dark/light), cart |
| **Server Cache** | TanStack Query | Products, orders, user |
| **Global App** | Zustand/Redux | Auth, preferences, config |

### SkyyRose Cart State Example

```typescript
// Using Zustand for simplicity
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartItem {
  productId: string;
  variantId?: string;
  quantity: number;
  price: number;
  name: string;
  image: string;
}

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (productId: string) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  clearCart: () => void;
  total: () => number;
}

export const useCart = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (item) =>
        set((state) => {
          const existing = state.items.find((i) => i.productId === item.productId);
          if (existing) {
            return {
              items: state.items.map((i) =>
                i.productId === item.productId
                  ? { ...i, quantity: i.quantity + item.quantity }
                  : i
              ),
            };
          }
          return { items: [...state.items, item] };
        }),

      removeItem: (productId) =>
        set((state) => ({
          items: state.items.filter((i) => i.productId !== productId),
        })),

      updateQuantity: (productId, quantity) =>
        set((state) => ({
          items: state.items.map((i) =>
            i.productId === productId ? { ...i, quantity } : i
          ),
        })),

      clearCart: () => set({ items: [] }),

      total: () => {
        return get().items.reduce((sum, item) => sum + item.price * item.quantity, 0);
      },
    }),
    {
      name: 'skyyrose-cart',
    }
  )
);
```

---

## CSS Architecture

### BEM + CSS Modules Pattern

```css
/* ProductCard.module.css */
.card {
  background: #FFFFFF;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
}

.card__image {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.card__title {
  font-family: 'Archivo', system-ui, sans-serif;
  color: #B76E79; /* SkyyRose primary */
  font-size: 1.5rem;
}

.card__price {
  font-weight: 600;
  color: #2C2C2C;
}

.card__button {
  background: linear-gradient(135deg, #B76E79, #D4A5AE);
  color: #FFFFFF;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.card__button:hover {
  opacity: 0.9;
}
```

```tsx
// ProductCard.tsx
import styles from './ProductCard.module.css';

export function ProductCard({ product }) {
  return (
    <div className={styles.card}>
      <img src={product.image} className={styles.card__image} />
      <h3 className={styles.card__title}>{product.name}</h3>
      <p className={styles.card__price}>${product.price}</p>
      <button className={styles.card__button}>Add to Cart</button>
    </div>
  );
}
```

### Tailwind + CVA Pattern

```tsx
// For utility-first approach
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-[#B76E79] text-white hover:bg-[#A55D68]',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
        ghost: 'hover:bg-gray-100',
      },
      size: {
        sm: 'h-9 px-3 text-sm',
        md: 'h-11 px-6',
        lg: 'h-13 px-8 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}
```

---

## Design System Implementation

### Token System

```typescript
// design-tokens.ts
export const tokens = {
  colors: {
    brand: {
      primary: '#B76E79',
      secondary: '#D4A5AE',
      dark: '#8B5663',
      light: '#F5E6E8',
    },
    neutral: {
      black: '#1A1A1A',
      gray: {
        900: '#2C2C2C',
        700: '#4A4A4A',
        500: '#767676',
        300: '#D1D1D1',
        100: '#F5F5F5',
      },
      white: '#FFFFFF',
    },
    semantic: {
      success: '#22C55E',
      warning: '#F59E0B',
      error: '#EF4444',
      info: '#3B82F6',
    },
  },

  typography: {
    fontFamily: {
      heading: "'Archivo', system-ui, sans-serif",
      body: "'Inter', sans-serif",
      mono: "'JetBrains Mono', monospace",
    },
    fontSize: {
      xs: '0.75rem',    // 12px
      sm: '0.875rem',   // 14px
      base: '1rem',     // 16px
      lg: '1.125rem',   // 18px
      xl: '1.25rem',    // 20px
      '2xl': '1.5rem',  // 24px
      '3xl': '1.875rem', // 30px
      '4xl': '2.25rem',  // 36px
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },

  spacing: {
    xs: '0.25rem',  // 4px
    sm: '0.5rem',   // 8px
    md: '1rem',     // 16px
    lg: '1.5rem',   // 24px
    xl: '2rem',     // 32px
    '2xl': '3rem',  // 48px
    '3xl': '4rem',  // 64px
  },

  animation: {
    duration: {
      fast: '150ms',
      base: '300ms',
      slow: '500ms',
    },
    easing: {
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      luxury: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)', // Smooth luxury feel
    },
  },
} as const;
```

---

## Component Communication Patterns

### Props Down, Events Up

```tsx
// Parent → Child: Props
// Child → Parent: Callbacks

// Parent
function ProductPage() {
  const [quantity, setQuantity] = useState(1);

  const handleAddToCart = (qty: number) => {
    addToCart({ ...product, quantity: qty });
  };

  return (
    <ProductDetails
      product={product}
      quantity={quantity}
      onQuantityChange={setQuantity}
      onAddToCart={handleAddToCart}
    />
  );
}

// Child
function ProductDetails({ product, quantity, onQuantityChange, onAddToCart }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <QuantitySelector value={quantity} onChange={onQuantityChange} />
      <button onClick={() => onAddToCart(quantity)}>
        Add to Cart
      </button>
    </div>
  );
}
```

### Context for Deep Props

```tsx
// Avoid prop drilling with context
import { createContext, useContext } from 'react';

const ThemeContext = createContext<{ mode: 'light' | 'dark' }>({ mode: 'light' });

export function ThemeProvider({ children }) {
  const [mode, setMode] = useState<'light' | 'dark'>('light');

  return (
    <ThemeContext.Provider value={{ mode, setMode }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);

// Deep nested component can access theme
function DeepNestedButton() {
  const { mode } = useTheme();
  return <button data-theme={mode}>Click</button>;
}
```

---

## Performance Architecture

### Code Splitting Strategy

```tsx
// Route-based splitting
import { lazy, Suspense } from 'react';

const HomePage = lazy(() => import('./pages/HomePage'));
const ProductPage = lazy(() => import('./pages/ProductPage'));
const CheckoutPage = lazy(() => import('./pages/CheckoutPage'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/products/:id" element={<ProductPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
      </Routes>
    </Suspense>
  );
}
```

### Component-level splitting

```tsx
// Heavy 3D component loaded on-demand
const Product3DViewer = lazy(() => import('./Product3DViewer'));

function ProductPage() {
  const [show3D, setShow3D] = useState(false);

  return (
    <div>
      <button onClick={() => setShow3D(true)}>View in 3D</button>

      {show3D && (
        <Suspense fallback={<div>Loading 3D viewer...</div>}>
          <Product3DViewer model={product.model} />
        </Suspense>
      )}
    </div>
  );
}
```

---

## WordPress Theme Integration

### Enqueue React App in Theme

```php
// functions.php
function skyyrose_enqueue_react_app() {
    $asset_file = get_template_directory() . '/build/index.asset.php';

    if (file_exists($asset_file)) {
        $asset = require $asset_file;

        wp_enqueue_script(
            'skyyrose-app',
            get_template_directory_uri() . '/build/index.js',
            $asset['dependencies'],
            $asset['version'],
            true
        );

        wp_enqueue_style(
            'skyyrose-app',
            get_template_directory_uri() . '/build/index.css',
            [],
            $asset['version']
        );

        // Pass data to React
        wp_localize_script('skyyrose-app', 'skyyRoseData', [
            'apiUrl' => rest_url('skyyrose/v1'),
            'nonce' => wp_create_nonce('wp_rest'),
            'brandColor' => '#B76E79',
            'collections' => get_skyyrose_collections(),
        ]);
    }
}
add_action('wp_enqueue_scripts', 'skyyrose_enqueue_react_app');
```

```tsx
// React app entry point
declare global {
  interface Window {
    skyyRoseData: {
      apiUrl: string;
      nonce: string;
      brandColor: string;
      collections: Array<{ id: string; name: string; slug: string }>;
    };
  }
}

const root = ReactDOM.createRoot(document.getElementById('skyyrose-app')!);
root.render(
  <StrictMode>
    <App config={window.skyyRoseData} />
  </StrictMode>
);
```

---

## Decision Framework

### When to Choose Architecture Pattern

| Scenario | Pattern |
|----------|---------|
| **Small theme** | Vanilla JS + WordPress | Keep it simple, no React needed |
| **Interactive features** | React islands | Hydrate specific components only |
| **SPA-like experience** | Full React SPA | Single page with routing |
| **Static + interactive** | Next.js SSG + ISR | Best of both worlds |
| **Complex state** | Redux/Zustand | Centralized state management |

---

## SkyyRose Best Practices

1. **Component naming**: `Skyy` prefix for custom components (`SkyyProductCard`, `SkyyCheckout`)
2. **Brand tokens**: Always use `tokens.colors.brand.primary` not hardcoded `#B76E79`
3. **Animations**: Use `tokens.animation.easing.luxury` for smooth, premium feel
4. **Typography**: Archivo for headings, Inter for body
5. **Spacing**: Use design tokens, not arbitrary values

---

## When User Asks For Architecture

1. **Understand scope**: How many pages? How complex?
2. **Assess interactivity**: Static content vs. dynamic features?
3. **Recommend pattern**: Feature-based, atomic, or hybrid
4. **Design state**: What needs to be shared? What's local?
5. **Plan performance**: Code splitting, lazy loading, SSR
6. **WordPress integration**: Theme structure, enqueue strategy

Provide complete, production-ready architecture plans with clear file structure and implementation order.
