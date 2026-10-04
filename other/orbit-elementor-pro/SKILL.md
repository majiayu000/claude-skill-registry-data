---
name: orbit-elementor-pro
description: Audit a plugin extending Elementor Pro features — Form Action subclasses (form integrations), custom Display Conditions, custom Theme Builder locations, custom Popup triggers, custom Loop Item templates. Use when the user says "Elementor Pro extension", "Form Action handler", "Display Conditions", "Theme Builder location", or builds anything that requires Elementor Pro to be active.
---

# 🪐 orbit-elementor-pro — Pro feature extensions

Elementor Pro exposes hooks and base classes for plugins extending Forms, Display Conditions, Theme Builder, Popups, and Loop. This skill audits that those extensions follow the modern patterns.

---

## Quick start

```bash
claude "/orbit-elementor-pro Audit ~/plugins/my-plugin's Elementor Pro extensions."
```

---

## What it checks

### 1. Form Action subclass (form integrations)
```php
class Form_Action_Mailchimp extends \ElementorPro\Modules\Forms\Classes\Action_Base {
  public function get_name() { return 'mailchimp'; }
  public function get_label() { return 'Mailchimp'; }
  public function register_settings_section( $widget ) { ... }
  public function on_export( $element ) { ... }
  public function run( $record, $ajax_handler ) {
    // Send the form data to Mailchimp
  }
}

add_action( 'elementor_pro/forms/actions/register', function( $form_actions_registrar ) {
  $form_actions_registrar->register( new Form_Action_Mailchimp() );
} );
```

### 2. Pro detection (must check before extending)
```php
if ( ! did_action( 'elementor/loaded' ) || ! defined( 'ELEMENTOR_PRO_VERSION' ) ) {
  // Show admin notice: "Elementor Pro required"
  return;
}
```

### 3. Theme Builder location
```php
add_action( 'elementor/theme/register_locations', function( $manager ) {
  $manager->register_location( 'my-plugin-banner', [
    'label' => __( 'My Banner', 'my-plugin' ),
    'multiple' => false,
    'edit_in_content' => false,
  ] );
} );
```

### 4. Display Conditions extension
```php
class Condition_User_Plan extends \ElementorPro\Modules\DisplayConditions\Classes\Condition_Base {
  public function get_name() { return 'user-plan'; }
  public function get_label() { return __( 'User Plan', 'my-plugin' ); }
  public function check( $args ) {
    return get_user_meta( get_current_user_id(), 'plan', true ) === $args['plan'];
  }
}
```

### 5. AJAX handler nonces in Form Action
**Whitepaper intent:** Form Actions run AJAX via Elementor Pro's framework. Sensitive operations (write to external API with user data) still need nonce verification — Pro's nonce isn't enough for cross-cutting auth.

### 6. Popup trigger registration
```php
add_action( 'elementor_pro/popup/triggers/register', function( $manager ) {
  $manager->register( new Trigger_User_Plan() );
} );
```

---

## Output

```markdown
# Elementor Pro Extensions — my-plugin

## Form Actions: 2
- Mailchimp ✓ valid Action_Base subclass
- ConvertKit ⚠ missing on_export() method (won't survive form export/import)

## Theme Builder Locations: 1
- "My Banner" ✓ registered

## Display Conditions: 0

## Popup Triggers: 0

## Pro detection
- ❌ includes/class-form-mailchimp.php does NOT check ELEMENTOR_PRO_VERSION before extending
   → Crashes on sites without Pro. Add the guard.
```

---

## Pair with

- `/orbit-elementor-dev` — base widget dev
- `/orbit-elementor-controls` — control system
- `/orbit-wp-security` — Form Action handling sensitive form data

---

## Sources & Evergreen References

### Canonical docs
- [Form Actions](https://developers.elementor.com/docs/form-actions/) — Action_Base reference
- [Display Conditions](https://developers.elementor.com/docs/display-conditions/) — Condition_Base
- [Theme Builder Locations](https://developers.elementor.com/docs/theme-builder/) — register_locations API
- [Popup Triggers](https://developers.elementor.com/docs/popups/) — Trigger_Base
- [Pro Plugin Source](https://github.com/elementor/elementor-pro) — actual Pro source (private but readable when licensed)

### Rule lineage
- Action_Base — stable since Pro 2.0
- Display Conditions — Pro 3.5 (introduced)
- `elementor_pro/forms/actions/register` — modern hook (replaces older `add_form_actions`)

### Last reviewed
- 2026-04-29 — re-review on Pro minor releases
