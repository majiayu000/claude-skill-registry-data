---
name: orbit-elementor-dev
description: Elementor widget development workflow audit — Widget_Base subclass structure, register_controls() patterns, render() escaping, content_template() for live preview, asset enqueue via get_script_depends() / get_style_depends(), responsive controls, and dynamic-tags integration. Use when the user says "Elementor widget", "create Elementor widget", "Widget_Base", or builds anything for Elementor.
---

# 🪐 orbit-elementor-dev — Elementor widget development

Elementor's widget API has its own rhythm — subclass `Widget_Base`, register controls, render with escaping. This skill audits that you're following the modern (3.18+) patterns.

---

## Quick start

```bash
claude "/orbit-elementor-dev Audit ~/plugins/my-plugin/widgets/ for Elementor widget best practices."
```

---

## What it checks

### 1. Widget structure
```php
class Widget_My_Hero extends \Elementor\Widget_Base {

  public function get_name() { return 'my-hero'; }
  public function get_title() { return __( 'My Hero', 'my-plugin' ); }
  public function get_icon() { return 'eicon-banner'; }
  public function get_categories() { return [ 'my-plugin' ]; }
  public function get_keywords() { return [ 'hero', 'banner' ]; }

  protected function register_controls() {
    $this->start_controls_section( 'content_section', [
      'label' => __( 'Content', 'my-plugin' ),
    ] );
    $this->add_control( 'title', [...] );
    $this->end_controls_section();
  }

  protected function render() { ... }
  protected function content_template() { ... }  // Live editor preview
}
```

### 2. Register the widget
```php
add_action( 'elementor/widgets/register', function( $widgets_manager ) {
  $widgets_manager->register( new \My_Plugin\Widget_My_Hero() );
} );
```

**Whitepaper intent:** `elementor/widgets/register` (with `r`) is the modern hook. Old `widgets_registered` is deprecated and triggers a console warning in Elementor 3.18+.

### 3. Output escaping in `render()`
```php
protected function render() {
  $settings = $this->get_settings_for_display();
  echo '<h2>' . esc_html( $settings['title'] ) . '</h2>';
  // For HTML content (set via WYSIWYG control):
  echo wp_kses_post( $settings['content'] );
}
```

### 4. Asset depends declared
```php
public function get_script_depends() { return [ 'my-hero' ]; }
public function get_style_depends() { return [ 'my-hero-style' ]; }
```

Register the handles via `wp_register_script()` / `wp_register_style()` at plugin load — Elementor enqueues them only when the widget is in the page.

### 5. Categories registered
```php
add_action( 'elementor/elements/categories_registered', function( $manager ) {
  $manager->add_category( 'my-plugin', [
    'title' => __( 'My Plugin', 'my-plugin' ),
    'icon'  => 'fa fa-plug',
  ] );
} );
```

### 6. Responsive controls
```php
$this->add_responsive_control( 'padding', [
  'label' => __( 'Padding', 'my-plugin' ),
  'type' => Controls_Manager::DIMENSIONS,
  'selectors' => [
    '{{WRAPPER}} .my-hero' => 'padding: {{TOP}}{{UNIT}} {{RIGHT}}{{UNIT}} {{BOTTOM}}{{UNIT}} {{LEFT}}{{UNIT}};',
  ],
] );
```

### 7. Editor preview via `content_template()`
```php
protected function content_template() {
  ?>
  <h2>{{{ settings.title }}}</h2>
  <?php
}
```

Without it, the editor only shows after-render → users can't see the widget update in real-time.

---

## Output

```markdown
# Elementor Widget Audit — my-plugin

## Widgets discovered: 12

### widget_my_hero (widgets/hero.php)
- ✓ Extends Widget_Base
- ✓ Registers via elementor/widgets/register
- ⚠ Missing content_template() — editor preview will be slow
- ❌ render() echoes $settings['title'] without esc_html (XSS)

[continue per widget]
```

---

## Pair with

- `/orbit-elementor-controls` — custom Control_Base subclasses
- `/orbit-elementor-compat` — vs Elementor versions
- `/orbit-elementor-pro` — Pro feature extension
- `/orbit-wp-security` — XSS in render output
- `/orbit-bundle-analysis` — verify asset depends actually conditional

---

## Sources & Evergreen References

### Canonical docs
- [Elementor Developers — Creating Widgets](https://developers.elementor.com/docs/widgets/) — root tutorial
- [Widget_Base API](https://developers.elementor.com/docs/widgets/widget-controls/) — class reference
- [Hooks Reference](https://developers.elementor.com/docs/hooks/) — every hook Elementor exposes
- [Elementor Coding Standards](https://developers.elementor.com/docs/general-info/coding-standards/) — naming, escaping, etc.

### Rule lineage
- `elementor/widgets/register` — modern hook (Elementor 3.5+, replaces `widgets_registered`)
- `register_controls` — modern method (replaces `_register_controls` underscore prefix in Elementor 3.1+)
- `get_script_depends` / `get_style_depends` — preferred enqueue path (Elementor 3.0+)
- `content_template` for live preview — long-standing best practice

### Last reviewed
- 2026-04-29 — re-review on Elementor minor releases (3.20, 3.22, 3.24…)
