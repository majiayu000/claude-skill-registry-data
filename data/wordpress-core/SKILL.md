---
name: wordpress-core
description: Core WordPress plugin development fundamentals including file structure, security patterns (sanitize, escape, nonces, capabilities), hooks system (actions/filters), database operations with wpdb, and coding standards. Use when creating plugins, implementing security, or working with core WordPress APIs.
---

# WordPress Core Development Skill

Core WordPress plugin development knowledge. Focus on fundamentals, security, and standard patterns.

**Target**: WordPress 6.8+

## WordPress Plugin File Structure

Standard organization for WordPress plugins:

```
plugin-name/
├── plugin-name.php              # Main plugin file (header, activation)
├── uninstall.php                # Uninstall cleanup (optional)
├── includes/
│   ├── class-plugin-name.php    # Main plugin class
│   ├── class-activator.php      # Activation logic
│   └── class-deactivator.php    # Deactivation logic
├── admin/
│   ├── class-admin.php          # Admin-specific functionality
│   ├── css/
│   ├── js/
│   └── partials/                # Admin view templates
├── public/
│   ├── class-public.php         # Public-facing functionality
│   ├── css/
│   ├── js/
│   └── partials/                # Public view templates
└── languages/                   # Translation files
```

**Key Principles**:
- Main plugin file contains header and initialization only
- Separate admin and public functionality
- Use classes for organization (recommended)
- Follow WordPress naming conventions (lowercase, hyphens)

## Plugin Header Format

Every plugin must have a header in the main file:

```php
<?php
/**
 * Plugin Name:       Your Plugin Name
 * Plugin URI:        https://example.com/plugin-name
 * Description:       Brief description of what the plugin does
 * Version:           1.0.0
 * Author:            Your Name
 * Author URI:        https://example.com
 * License:           GPL-2.0+
 * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
 * Text Domain:       plugin-name
 * Domain Path:       /languages
 */

// If this file is called directly, abort.
if ( ! defined( 'WPINC' ) ) {
	die;
}
```

**Required Fields**: Plugin Name
**Recommended**: Description, Version, Author, License, Text Domain

## Security Principles (CRITICAL)

WordPress security follows three golden rules:

### 1. Sanitize Input (Trust Nothing)

Always sanitize data coming from users:

```php
// Text input
$clean_text = sanitize_text_field( $_POST['user_input'] );

// Email
$clean_email = sanitize_email( $_POST['email'] );

// URL
$clean_url = esc_url_raw( $_POST['url'] );

// Integer
$clean_id = absint( $_POST['post_id'] );

// Array of text fields
$clean_array = array_map( 'sanitize_text_field', $_POST['items'] );
```

**Common Functions**:
- `sanitize_text_field()` - Strips tags, scripts
- `sanitize_email()` - Validates email format
- `sanitize_key()` - Lowercase alphanumeric, dashes, underscores
- `sanitize_title()` - Creates slug-safe string
- `esc_url_raw()` - Database-safe URL
- `absint()` - Absolute integer (positive only)
- `intval()` - Integer conversion

### 2. Escape Output (Never Trust Data)

Always escape data when outputting to HTML:

```php
// HTML content
echo esc_html( $user_data );

// HTML attributes
echo '<input value="' . esc_attr( $value ) . '">';

// URLs
echo '<a href="' . esc_url( $link ) . '">Link</a>';

// JavaScript
echo '<script>var data = ' . wp_json_encode( $data ) . ';</script>';

// Textarea
echo '<textarea>' . esc_textarea( $content ) . '</textarea>';
```

**Common Functions**:
- `esc_html()` - Escapes HTML (converts < > & " ')
- `esc_attr()` - Escapes HTML attributes
- `esc_url()` - Escapes URLs for output
- `esc_js()` - Escapes JavaScript strings
- `esc_textarea()` - Escapes textarea content
- `wp_kses_post()` - Allows safe HTML (like posts)

### 3. Nonces (Verify Intent)

Use nonces to prevent CSRF attacks:

```php
// Creating a nonce (in form)
wp_nonce_field( 'my_action_name', 'my_nonce_field' );

// Verifying a nonce (on submission)
if ( ! isset( $_POST['my_nonce_field'] ) ||
     ! wp_verify_nonce( $_POST['my_nonce_field'], 'my_action_name' ) ) {
	die( 'Security check failed' );
}

// URL nonces
$url = wp_nonce_url( 'admin.php?action=delete&id=123', 'delete_item_123' );

// Verify URL nonce
if ( ! isset( $_GET['_wpnonce'] ) ||
     ! wp_verify_nonce( $_GET['_wpnonce'], 'delete_item_123' ) ) {
	die( 'Security check failed' );
}
```

### 4. Capability Checks (Authorization)

Verify user has permission:

```php
// Check if user can perform action
if ( ! current_user_can( 'manage_options' ) ) {
	wp_die( 'You do not have sufficient permissions' );
}

// Common capabilities
current_user_can( 'edit_posts' );
current_user_can( 'publish_pages' );
current_user_can( 'edit_others_posts' );
```

**Security Checklist**:
- [ ] All user input sanitized
- [ ] All output escaped
- [ ] Nonces verify form submissions
- [ ] Capability checks on all admin actions
- [ ] Direct file access prevented (`defined( 'WPINC' )`)

## Hooks System (Actions and Filters)

WordPress uses hooks to allow plugins to modify behavior.

### Actions (Do Something)

Execute code at specific points:

```php
// Add an action
add_action( 'init', 'my_function' );
add_action( 'wp_enqueue_scripts', 'my_enqueue_function' );
add_action( 'admin_menu', 'my_menu_function' );

// Custom action (for your plugin)
do_action( 'my_plugin_custom_action', $param1, $param2 );
```

**Common Action Hooks**:
- `init` - WordPress initialized, user authenticated
- `admin_init` - Admin area initialized
- `admin_menu` - Time to add admin menu items
- `wp_enqueue_scripts` - Enqueue public scripts/styles
- `admin_enqueue_scripts` - Enqueue admin scripts/styles
- `wp_head` - Output to `<head>` section
- `wp_footer` - Output before `</body>`
- `save_post` - Post is being saved
- `admin_notices` - Display admin notices

### Filters (Modify Data)

Modify values before they're used:

```php
// Add a filter
add_filter( 'the_content', 'my_content_filter' );
add_filter( 'the_title', 'my_title_filter', 10, 2 );

function my_content_filter( $content ) {
	// Modify and return content
	return $content . '<p>Added text</p>';
}

// Custom filter (for your plugin)
$value = apply_filters( 'my_plugin_custom_filter', $value, $arg1, $arg2 );
```

**Common Filter Hooks**:
- `the_content` - Post content
- `the_title` - Post title
- `the_excerpt` - Post excerpt
- `wp_mail` - Email parameters
- `upload_mimes` - Allowed upload types
- `login_redirect` - Where to redirect after login

**Priority and Arguments**:
```php
// Priority: 10 is default, lower runs earlier
add_filter( 'the_title', 'my_filter', 5 ); // Runs early

// Accept multiple arguments
add_filter( 'the_title', 'my_filter', 10, 2 );
function my_filter( $title, $post_id ) {
	return $title;
}
```

## Database Interactions (wpdb)

Use `$wpdb` global for database queries.

### Basic Queries

```php
global $wpdb;

// Get single value
$count = $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->posts}" );

// Get single row
$post = $wpdb->get_row( "SELECT * FROM {$wpdb->posts} WHERE ID = 1" );

// Get multiple rows
$posts = $wpdb->get_results( "SELECT * FROM {$wpdb->posts} WHERE post_status = 'publish'" );

// Get column
$titles = $wpdb->get_col( "SELECT post_title FROM {$wpdb->posts}" );
```

### Prepared Statements (ALWAYS)

Never use string concatenation with user input:

```php
// WRONG - SQL Injection vulnerability
$wpdb->get_results( "SELECT * FROM {$wpdb->posts} WHERE ID = {$_GET['id']}" );

// CORRECT - Prepared statement
$id = absint( $_GET['id'] );
$wpdb->get_results( $wpdb->prepare(
	"SELECT * FROM {$wpdb->posts} WHERE ID = %d",
	$id
) );

// Multiple placeholders
$wpdb->get_results( $wpdb->prepare(
	"SELECT * FROM {$wpdb->posts} WHERE post_type = %s AND post_status = %s",
	$post_type,
	$status
) );
```

**Placeholders**:
- `%s` - String
- `%d` - Integer
- `%f` - Float

### Insert/Update/Delete

```php
// Insert
$wpdb->insert(
	$wpdb->prefix . 'my_table',
	array(
		'column1' => 'value1',
		'column2' => 123
	),
	array( '%s', '%d' ) // Format
);

// Update
$wpdb->update(
	$wpdb->prefix . 'my_table',
	array( 'column1' => 'new_value' ), // Data
	array( 'ID' => 123 ),               // Where
	array( '%s' ),                      // Data format
	array( '%d' )                       // Where format
);

// Delete
$wpdb->delete(
	$wpdb->prefix . 'my_table',
	array( 'ID' => 123 ),
	array( '%d' )
);
```

**Table Prefix**: Always use `$wpdb->prefix` for custom tables

## WordPress Coding Standards

Follow WordPress PHP coding standards:

**Naming Conventions**:
- Functions: `lowercase_with_underscores()`
- Classes: `Class_Name_With_Underscores`
- Constants: `UPPERCASE_WITH_UNDERSCORES`
- Files: `lowercase-with-hyphens.php`

**Indentation**: Tabs (not spaces)

**Bracing**:
```php
if ( condition ) {
	// Code
}
```

**Spacing**:
```php
// Always space after control structures
if ( condition ) {
	// Code
}

// Space around operators
$x = $y + $z;

// No space inside parentheses for function calls
my_function( $arg1, $arg2 );
```

**Yoda Conditions** (constants on left):
```php
if ( 'yes' === $value ) {
	// Prevents accidental assignment
}
```

## Helper Functions

**Plugin paths**:
```php
plugin_dir_path( __FILE__ ); // /path/to/wp-content/plugins/my-plugin/
plugin_dir_url( __FILE__ );  // https://example.com/wp-content/plugins/my-plugin/
plugin_basename( __FILE__ ); // my-plugin/my-plugin.php
```

**Get options**:
```php
get_option( 'option_name', 'default_value' );
update_option( 'option_name', $new_value );
delete_option( 'option_name' );
```

**Post meta**:
```php
get_post_meta( $post_id, 'meta_key', true ); // Single value
update_post_meta( $post_id, 'meta_key', $value );
delete_post_meta( $post_id, 'meta_key' );
```

**Transients (temporary cached data)**:
```php
set_transient( 'my_transient', $value, 3600 ); // 1 hour
$value = get_transient( 'my_transient' );
delete_transient( 'my_transient' );
```

## Progressive Disclosure

For advanced topics, see:
- See [{baseDir}/references/security-patterns.md](references/security-patterns.md) for advanced security patterns
- See [{baseDir}/references/hooks-api.md](references/hooks-api.md) for comprehensive hooks reference
- See [{baseDir}/references/database-patterns.md](references/database-patterns.md) for complex database operations

## Related Skills

- **wordpress-blocks** - Block development, Block Hooks API, Interactivity API
- **wordpress-modern** - Performance optimization, modern WP 6.8 features

## Best Practices Summary

1. **Security First**: Sanitize input, escape output, verify nonces, check capabilities
2. **Use WordPress APIs**: Don't reinvent the wheel, use built-in functions
3. **Follow Standards**: WordPress coding standards for consistency
4. **Prepare Statements**: Always use `$wpdb->prepare()` for queries
5. **Prefix Everything**: Avoid naming conflicts with unique prefixes
6. **Test**: Test activation, deactivation, different user roles
7. **Document**: Comment complex logic, use PHPDoc blocks
