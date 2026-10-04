---
name: ui-molecule
description: Atomic-design guidance for Molecules — functional groups of atoms (SearchBar = input + button + icon; FormField = label + input + error) with a single cohesive purpose. Use when authoring or reviewing components under ui/molecules, composing atoms, or deciding atom vs molecule vs organism.
when_to_use: Creating or reviewing molecule-level components; deciding whether a component is a molecule vs. an organism (no store connection = molecule); composing atoms without recreating their functionality; keeping molecules purely presentational.
paths:
  - "**/ui/molecules/**/*.{jsx,tsx,vue,js,ts}"
  - "**/components/molecules/**/*"
  - "**/molecules/**/*"
---

# Molecule

## What is a Molecule?

Molecules are functional UI groups composed of multiple atoms working together for a single purpose—like a search bar (input + button + icon) or form field (label + input + error). They're reusable interface patterns.

## Key Principles

1. **Composition Over Creation**: Build molecules by composing existing atoms, don't recreate atom functionality inside molecules.

2. **Single Cohesive Purpose**: A molecule does one thing (search, form field, card header)—if it does multiple distinct things, it's probably an organism.

3. **Props Passthrough**: Molecules receive data and pass relevant props to child atoms. They orchestrate, not originate.

## Best Practices

✅ **DO**:
- Import and compose atoms from your atom library
- Keep molecules under 100 lines of code
- Handle layout/spacing between atoms
- Communicate via callbacks (onSearch, onSubmit, onChange)
- Maintain consistent atom usage across similar molecules

❌ **DON'T**:
- Connect to global state or stores
- Fetch data—molecules are presentational
- Include complex business logic
- Hardcode atom variations—accept as props
- Nest molecules more than one level deep

## Code Patterns

### Recommended

```jsx
// SearchBar.jsx - Molecule composing atoms
import Input from '../atoms/Input';
import Button from '../atoms/Button';
import Icon from '../atoms/Icon';

const SearchBar = ({ value, onChange, onSearch, placeholder }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') onSearch(value);
  };

  return (
    <div className="search-bar">
      <Icon name="search" />
      <Input
        value={value}
        onChange={onChange}
        onKeyPress={handleKeyPress}
        placeholder={placeholder}
      />
      <Button label="Search" onClick={() => onSearch(value)} />
    </div>
  );
};
```

### Avoid

```jsx
// ❌ WRONG - Molecule connected to store
const SearchBar = () => {
  const dispatch = useDispatch();
  const query = useSelector(state => state.search.query);
  // Molecules shouldn't connect to store!
};

// ✅ CORRECT - Receives data via props
const SearchBar = ({ query, onQueryChange, onSearch }) => (
  // Pure presentational component
);
```

## Related Terminologies

- **Atom** (UI) - Building blocks molecules are composed of
- **Organism** (UI) - Larger components that compose molecules
- **Component** (UI) - Generic term; molecules are presentational components
- **Events** (UI) - How molecules communicate user interactions

## Quality Gates

- [ ] Composed of existing atoms (not recreating)
- [ ] Single cohesive purpose
- [ ] No state management connections
- [ ] No data fetching
- [ ] Handles layout between child atoms
- [ ] Uses callbacks for communication

**Source**: `/docs/ui/molecule.md`
