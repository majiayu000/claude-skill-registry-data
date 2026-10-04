---
name: orbit-elementor-skins
description: Audit Elementor widget skins — Skin_Base subclasses that let one widget render in multiple visual styles (e.g. "Card", "List", "Carousel" variants of the same Posts widget). Use when the user says "Elementor skin", "Skin_Base", "widget variant", or has multiple similar widgets that should be skins of one.
---

# 🪐 orbit-elementor-skins — Widget skins

Skins are Elementor's variation system. One widget, multiple visual treatments, shared data + controls. Most plugins ship 5 separate widgets when 1 widget + 5 skins would be cleaner.

---

## Quick start

```bash
claude "/orbit-elementor-skins Audit ~/plugins/my-plugin for over-widgeting — places where multiple widgets should be skins of one."
```

---

## What it checks

### 1. Skin_Base subclass
```php
class Skin_Card extends \Elementor\Skin_Base {
  public function get_id() { return 'card'; }
  public function get_title() { return __( 'Card', 'my-plugin' ); }

  protected function _register_controls_actions() {
    add_action( "elementor/element/{$this->parent->get_name()}/section_card/before_section_end",
      [ $this, 'register_controls' ] );
  }

  public function render() {
    // Custom render for "card" treatment
  }
}
```

### 2. Skin registered on the widget
```php
class Widget_Posts extends \Elementor\Widget_Base {
  protected function _register_skins() {
    $this->add_skin( new Skin_Card( $this ) );
    $this->add_skin( new Skin_List( $this ) );
    $this->add_skin( new Skin_Grid( $this ) );
  }
}
```

### 3. Default skin
```php
$this->add_control( '_skin', [
  'type' => Controls_Manager::SELECT,
  'default' => 'card',
  // populated automatically from registered skins
] );
```

### 4. Use cases for skins vs separate widgets

| Use skin when | Use separate widget when |
|---|---|
| Same data shape (posts list, gallery items) | Different data sources |
| Same edit controls (with optional skin-specific extras) | Fundamentally different control set |
| Visual variant of the same concept | Conceptually different feature |

### 5. Skin-specific controls registered correctly
**Whitepaper intent:** Skin-specific controls must be added inside the right hook so they only appear when that skin is selected. Common bug: controls always show, regardless of selected skin.

---

## Output

```markdown
# Elementor Skins Audit — my-plugin

## Skins registered: 4
- my-plugin/posts widget — 4 skins (Card, List, Grid, Carousel) ✓

## Over-widgeting (consider migrating to skins)
- my-plugin/team-cards + my-plugin/team-list — same data, different treatment. Merge as skins.
- my-plugin/testimonial-grid + my-plugin/testimonial-carousel — same.

## Skin issues
- ⚠ Skin_Carousel registers controls outside _register_controls_actions — controls always show
```

---

## Pair with

- `/orbit-elementor-dev` — widget dev
- `/orbit-elementor-controls` — controls
- `/orbit-block-variations` — Gutenberg's equivalent concept

---

## Sources & Evergreen References

### Canonical docs
- [Widget Skins](https://developers.elementor.com/docs/widgets/widget-skin/) — Skin_Base reference
- [Hooks Reference](https://developers.elementor.com/docs/hooks/) — `before_section_end` etc.

### Rule lineage
- Skin_Base — stable since Elementor 2.0
- `_register_skins` (underscore prefix) — used in Elementor 2.x; `register_skins` (no underscore) became the convention in 3.0+ but both still work

### Last reviewed
- 2026-04-29 — re-review on Elementor major versions
