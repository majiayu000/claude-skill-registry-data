---
name: flui-architecture-expert
description: Expert on FLUI's three-tree architecture (View-Element-Render), widget composition, and Flutter-inspired patterns. Use when discussing views, elements, render objects, widget trees, or UI architecture.
---

# FLUI Architecture Expert

Deep expertise in FLUI's Flutter-inspired three-tree architecture.

## When to Use

Activate this skill when the user:
- Asks about View, Element, or RenderObject
- Discusses widget composition or tree structure
- Wants to understand build/layout/paint phases
- Needs to create custom render objects
- Has questions about the BuildContext

## Three-Tree Architecture

### View Tree (Immutable)
```
Purpose: Declarative UI description
Lifecycle: Created fresh each build
Key trait: View with build() -> impl IntoElement
```

**Rules:**
- Views must be `'static` but NOT necessarily Clone
- Use cheap-to-clone types (String, Arc<T>)
- Never mutate state directly - use signals

### Element Tree (Mutable)
```
Purpose: Manages widget lifecycle and state
Storage: Slab<Node<Element>> with ElementId keys
Key struct: Element with view_object: Box<dyn ViewObject>
```

**Critical Pattern - ElementId Offset:**
```rust
// Slab uses 0-based, ElementId uses 1-based (NonZeroUsize)
let id = slab.insert(node);
ElementId::new(id + 1)  // +1 for insertion

slab.get(element_id.get() - 1)  // -1 for access
```

### Render Tree (Layout/Paint)
```
Purpose: Layout calculation and painting
Arity system: Leaf, Single, Optional, Variable
Key trait: RenderBox<Arity>
```

**Arity Types:**
```rust
pub struct Leaf;        // 0 children (Text, Image)
pub struct Single;      // 1 child (Container, Padding)
pub struct Optional;    // 0-1 children (Conditional)
pub struct Variable;    // N children (Row, Column)
```

## Pipeline Phases

### Build Phase
- Traverses dirty elements
- Calls `view.build(ctx)` to generate new view tree
- Reconciles with existing element tree

### Layout Phase
- Top-down constraint passing
- Bottom-up size determination
- Uses `BoxConstraints` for flexible sizing

### Paint Phase
- Generates display list
- Layer composition
- GPU command generation via wgpu

## Widget Patterns

### Stateless Widget
```rust
pub struct MyWidget {
    pub text: String,
}

impl View for MyWidget {
    fn build(&self, ctx: &mut BuildContext) -> impl IntoElement {
        Text::new(&self.text)
    }
}
```

### Stateful Widget (with hooks)
```rust
impl View for Counter {
    fn build(&self, ctx: &mut BuildContext) -> impl IntoElement {
        let count = use_signal(ctx, 0);
        
        Button::new(format!("Count: {}", count.get()))
            .on_press(move || count.set(count.get() + 1))
    }
}
```

### Custom RenderObject
```rust
impl RenderBox<Single> for CustomRender {
    fn perform_layout(&mut self, constraints: BoxConstraints) -> Size {
        let child_size = self.child().layout(constraints);
        Size::new(child_size.width + 20.0, child_size.height + 20.0)
    }
    
    fn paint(&self, context: &mut PaintContext) {
        context.canvas.draw_rect(self.local_rect(), &self.paint);
        self.child().paint(context);
    }
}
```

## Common Issues

### Issue: Hook order changes
```rust
// BAD: Conditional hook
if condition {
    let signal = use_signal(ctx, 0);  // Will panic!
}

// GOOD: Always call hooks in same order
let signal = use_signal(ctx, 0);
if condition {
    // use signal
}
```

### Issue: Expensive rebuilds
```rust
// BAD: Large subtree rebuilt on every change
Column::new(vec![
    expensive_widget_tree(),  // Rebuilt every time
])

// GOOD: Use memoization or separate signals
let memoized = use_memo(ctx, || expensive_widget_tree());
```

## Architecture Verification Checklist

- [ ] Views are immutable
- [ ] State managed through signals
- [ ] ElementId uses +1/-1 offset correctly
- [ ] RenderObject arity matches child count
- [ ] No mutable references across tree boundaries
- [ ] BuildContext only accessed during build phase
