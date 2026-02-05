---
name: react-component-developer
description: Expert in React 19 and Next.js 16 development with modern patterns including Server Components, hooks, and performance optimization. Use when creating new UI components, refactoring React code, or implementing interactive features.
---

# React Component Developer

Specialized agent for developing React 19 components in Next.js 16 with Shadcn/UI, TailwindCSS v4, and modern best practices.

## Project Stack

- **React**: 19.0 (latest with concurrent features)
- **Next.js**: 16.1 (App Router, static export)
- **UI Library**: Shadcn/UI + Radix UI primitives
- **Styling**: TailwindCSS v4
- **Icons**: Lucide React
- **Theme**: next-themes (dark/light mode)
- **Build**: Static export for Tauri

## Component Architecture

### 1. Component Organization

```
components/
├── eq-graph.tsx           # Canvas-based frequency response
├── band-editor.tsx        # Individual EQ band controls
├── preamp-control.tsx     # Master preamp slider
├── peak-meter.tsx         # Clipping indicator
├── profile-selector.tsx   # Profile dropdown
├── audio-status-panel.tsx # Real-time peak meter
├── setup-dialog.tsx       # Initial config
└── ui/                    # Shadcn/UI primitives
    ├── button.tsx
    ├── dialog.tsx
    ├── slider.tsx
    └── ...
```

### 2. State Management Patterns

**Use Custom Hooks for Logic:**

```typescript
// lib/use-equalizer.ts
export function useEqualizer() {
  const [bands, setBands] = useState<ParametricBand[]>([]);
  const [preamp, setPreamp] = useState(0);
  const [currentProfile, setCurrentProfile] = useState<string | null>(null);

  // Debounced save to backend
  const debouncedSave = useMemo(
    () =>
      debounce(async (settings: Settings) => {
        await updateSettings(settings);
      }, 500),
    []
  );

  useEffect(() => {
    debouncedSave({ bands, preamp });
  }, [bands, preamp]);

  const addBand = useCallback((band: ParametricBand) => {
    setBands((prev) => [...prev, band]);
  }, []);

  const removeBand = useCallback((index: number) => {
    setBands((prev) => prev.filter((_, i) => i !== index));
  }, []);

  return {
    bands,
    preamp,
    currentProfile,
    addBand,
    removeBand,
    setPreamp,
  };
}
```

**Component Uses Hook:**

```typescript
export function EqualizerPage() {
  const { bands, preamp, addBand, removeBand, setPreamp } = useEqualizer();

  return (
    <div className="space-y-4">
      <BandEditor bands={bands} onAdd={addBand} onRemove={removeBand} />
      <PreampControl value={preamp} onChange={setPreamp} />
      <EqGraph bands={bands} preamp={preamp} />
    </div>
  );
}
```

### 3. Component Patterns

**Controlled Components:**

```typescript
interface SliderProps {
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step: number;
  label: string;
}

export function GainSlider({ value, onChange, min, max, step, label }: SliderProps) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">{label}</label>
      <Slider
        value={[value]}
        onValueChange={(values) => onChange(values[0])}
        min={min}
        max={max}
        step={step}
      />
      <span className="text-xs text-muted-foreground">{value.toFixed(1)} dB</span>
    </div>
  );
}
```

**Uncontrolled with Ref (Canvas):**

```typescript
export function EqGraph({ bands, preamp }: { bands: ParametricBand[]; preamp: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    drawFrequencyResponse(ctx, bands, preamp, canvas.width, canvas.height);
  }, [bands, preamp]);

  return <canvas ref={canvasRef} width={800} height={400} className="w-full" />;
}
```

### 4. Performance Optimization

**useMemo for Expensive Calculations:**

```typescript
export function EqGraph({ bands, preamp }: EqGraphProps) {
  // Compute frequency response only when bands/preamp change
  const responseData = useMemo(() => {
    return calculateFrequencyResponse(bands, preamp);
  }, [bands, preamp]);

  return <Canvas data={responseData} />;
}
```

**useCallback for Event Handlers:**

```typescript
export function BandEditor({ bands, onChange }: BandEditorProps) {
  const handleFrequencyChange = useCallback(
    (index: number, freq: number) => {
      const newBands = [...bands];
      newBands[index].frequency = freq;
      onChange(newBands);
    },
    [bands, onChange]
  );

  return (
    <>
      {bands.map((band, i) => (
        <BandCard
          key={i}
          band={band}
          onFrequencyChange={(freq) => handleFrequencyChange(i, freq)}
        />
      ))}
    </>
  );
}
```

**React.memo for Pure Components:**

```typescript
interface BandCardProps {
  band: ParametricBand;
  onUpdate: (band: ParametricBand) => void;
}

export const BandCard = React.memo<BandCardProps>(({ band, onUpdate }) => {
  return (
    <div className="rounded-lg border p-4">
      {/* Band controls */}
    </div>
  );
});

BandCard.displayName = 'BandCard';
```

### 5. Shadcn/UI Integration

**Using Shadcn Components:**

```typescript
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader } from '@/components/ui/dialog';
import { Slider } from '@/components/ui/slider';

export function ProfileDialog({ open, onOpenChange }: DialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>Save Profile</DialogHeader>
        <Input placeholder="Profile name" />
        <Button onClick={handleSave}>Save</Button>
      </DialogContent>
    </Dialog>
  );
}
```

**Custom Variants with CVA:**

```typescript
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva('rounded-md font-medium transition-colors', {
  variants: {
    variant: {
      default: 'bg-primary text-primary-foreground hover:bg-primary/90',
      destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
      outline: 'border border-input hover:bg-accent',
    },
    size: {
      default: 'h-10 px-4',
      sm: 'h-8 px-3 text-sm',
      lg: 'h-12 px-6',
    },
  },
  defaultVariants: {
    variant: 'default',
    size: 'default',
  },
});

export function CustomButton({ variant, size, ...props }: ButtonProps) {
  return <button className={buttonVariants({ variant, size })} {...props} />;
}
```

### 6. TailwindCSS v4 Patterns

**Responsive Design:**

```tsx
<div className="
  grid grid-cols-1
  md:grid-cols-2
  lg:grid-cols-3
  gap-4
">
  {/* Responsive grid */}
</div>
```

**Dark Mode:**

```tsx
<div className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-gray-100
">
  {/* Auto-switches with theme */}
</div>
```

**Custom Colors:**

```tsx
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        'eq-peak': '#ef4444',
        'eq-safe': '#22c55e',
        'eq-warn': '#f59e0b',
      },
    },
  },
};

// Component
<div className="bg-eq-safe text-white">Safe Level</div>
```

### 7. Canvas Rendering (EQ Graph)

**Optimized Canvas Drawing:**

```typescript
export function drawFrequencyResponse(
  ctx: CanvasRenderingContext2D,
  bands: ParametricBand[],
  preamp: number,
  width: number,
  height: number
) {
  // Clear canvas
  ctx.clearRect(0, 0, width, height);

  // Pre-compute response
  const frequencies = generateLogFrequencies(20, 20000, 200);
  const response = calculateTotalResponse(bands, preamp, frequencies);

  // Set up styling
  ctx.strokeStyle = 'hsl(var(--primary))';
  ctx.lineWidth = 2;

  // Draw curve
  ctx.beginPath();
  frequencies.forEach((freq, i) => {
    const x = freqToX(freq, width);
    const y = dbToY(response[i], height);

    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();
}

function freqToX(freq: number, width: number): number {
  const logMin = Math.log10(20);
  const logMax = Math.log10(20000);
  const logFreq = Math.log10(freq);
  return ((logFreq - logMin) / (logMax - logMin)) * width;
}

function dbToY(db: number, height: number): number {
  const DB_RANGE = 40; // ±20 dB
  return height / 2 - (db / DB_RANGE) * height;
}
```

**High-DPI Canvas:**

```typescript
function setupCanvas(canvas: HTMLCanvasElement) {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();

  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;

  const ctx = canvas.getContext('2d')!;
  ctx.scale(dpr, dpr);

  canvas.style.width = `${rect.width}px`;
  canvas.style.height = `${rect.height}px`;

  return ctx;
}
```

### 8. Form Handling

**Controlled Forms:**

```typescript
export function ProfileSaveDialog({ onSave }: DialogProps) {
  const [name, setName] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name.trim()) {
      setError('Profile name required');
      return;
    }

    try {
      await onSave(name);
      setName('');
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Save failed');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Profile name"
      />
      {error && <p className="text-sm text-destructive">{error}</p>}
      <Button type="submit">Save</Button>
    </form>
  );
}
```

### 9. Event Listeners (Tauri Events)

**Listen to Backend Events:**

```typescript
import { listen } from '@tauri-apps/api/event';

export function usePeakMeter() {
  const [peak, setPeak] = useState<number>(0);

  useEffect(() => {
    let unlisten: (() => void) | null = null;

    listen<{ peakDb: number }>('peak_meter_update', (event) => {
      setPeak(event.payload.peakDb);
    }).then((fn) => {
      unlisten = fn;
    });

    return () => {
      unlisten?.();
    };
  }, []);

  return peak;
}
```

### 10. Keyboard Shortcuts

```typescript
export function useKeyboardShortcuts() {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl+S to save
      if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        saveProfile();
      }

      // Space to toggle
      if (e.key === ' ' && e.target === document.body) {
        e.preventDefault();
        toggleEQ();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);
}
```

## Best Practices

### Component Design

1. **Single Responsibility**: One component = one purpose
2. **Composition over Props**: Use children for flexibility
3. **Controlled vs Uncontrolled**: Prefer controlled for form inputs
4. **PropTypes with TypeScript**: Always type your props
5. **Default Props**: Use ES6 default parameters

### Performance

1. **Avoid Inline Functions**: Use useCallback for event handlers
2. **Memoize Expensive Calcs**: useMemo for complex computations
3. **React.memo for Pure Components**: Prevent unnecessary re-renders
4. **Key Props**: Use stable keys (not array indices)
5. **Virtual Scrolling**: For long lists (>100 items)

### Accessibility

1. **Semantic HTML**: Use proper elements (button, not div with onClick)
2. **ARIA Labels**: aria-label for icon-only buttons
3. **Keyboard Navigation**: All interactive elements focusable
4. **Focus Management**: Focus trap in modals
5. **Color Contrast**: WCAG AA compliance (4.5:1 for text)

### Styling

1. **TailwindCSS First**: Use utility classes
2. **Consistent Spacing**: Use Tailwind's spacing scale
3. **Theme Variables**: Use CSS custom properties for colors
4. **Responsive Design**: Mobile-first approach
5. **Dark Mode**: Support both light and dark themes

## Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { BandEditor } from './band-editor';

describe('BandEditor', () => {
  it('should add a new band', () => {
    const onAdd = vi.fn();
    render(<BandEditor bands={[]} onAdd={onAdd} />);

    const addButton = screen.getByRole('button', { name: /add band/i });
    fireEvent.click(addButton);

    expect(onAdd).toHaveBeenCalledTimes(1);
  });

  it('should remove a band', () => {
    const band = { frequency: 1000, gain: 3, qFactor: 1.41, filterType: 'Peaking' };
    const onRemove = vi.fn();

    render(<BandEditor bands={[band]} onRemove={onRemove} />);

    const removeButton = screen.getByRole('button', { name: /remove/i });
    fireEvent.click(removeButton);

    expect(onRemove).toHaveBeenCalledWith(0);
  });
});
```

## Common Pitfalls

1. **❌ Mutating State Directly**
   ```typescript
   // WRONG
   bands[0].gain = 5;
   setBands(bands);

   // RIGHT
   const newBands = [...bands];
   newBands[0] = { ...newBands[0], gain: 5 };
   setBands(newBands);
   ```

2. **❌ Missing Dependencies in useEffect**
   ```typescript
   // WRONG: Stale closure
   useEffect(() => {
     doSomething(value);
   }, []); // Missing 'value'

   // RIGHT
   useEffect(() => {
     doSomething(value);
   }, [value]);
   ```

3. **❌ Not Cleaning Up Effects**
   ```typescript
   // WRONG: Memory leak
   useEffect(() => {
     const interval = setInterval(update, 1000);
   }, []);

   // RIGHT
   useEffect(() => {
     const interval = setInterval(update, 1000);
     return () => clearInterval(interval);
   }, []);
   ```

## Reference Materials

- `references/react_19_features.md` - New React 19 features
- `references/shadcn_examples.md` - Common Shadcn/UI patterns
- `references/accessibility.md` - WCAG compliance guide
