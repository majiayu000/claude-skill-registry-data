---
name: wordpress-blocks
description: WordPress block development including Gutenberg blocks, Block Hooks API for dynamic injection, Interactivity API for frontend features, custom post types, shortcodes, widgets, and meta boxes. Use when building blocks, adding interactivity, or creating content structures.
---

# WordPress Blocks Development Skill

Block-based development and content structures for WordPress 6.8+.

## Block Hooks API (WordPress 6.8+)

Dynamic injection of blocks into specific hook points in block-based themes.

### What It Does

Enables plugins to automatically insert blocks into templates without modifying template files directly. As of WordPress 6.8, this extends to post content itself, not just templates.

### Basic Usage

```php
// Register a block that hooks into a specific location
function my_plugin_register_hooked_block() {
	register_block_type( __DIR__ . '/build/my-block', array(
		'block_hooks' => array(
			'core/navigation' => 'last_child', // Insert as last child of navigation
		),
	) );
}
add_action( 'init', 'my_plugin_register_hooked_block' );
```

### Hook Positions

Available positions for block insertion:
- `before` - Before the target block
- `after` - After the target block
- `first_child` - First child of target block
- `last_child` - Last child of target block

### Filtering Block Hooks

```php
// Conditionally prevent block insertion
function my_filter_block_hooks( $hooked_blocks, $position, $anchor_block, $context ) {
	// Remove specific hooked block based on context
	if ( $context instanceof WP_Post && 'page' === $context->post_type ) {
		unset( $hooked_blocks['my-plugin/my-block'] );
	}
	return $hooked_blocks;
}
add_filter( 'hooked_block_types', 'my_filter_block_hooks', 10, 4 );
```

### Opting Out of Block Hooks (6.8)

```php
// Disable specific hooked blocks in post content
$post_content = '<!-- wp:core/navigation {"ignoredHookedBlocks":["my-plugin/my-block"]} /-->';
```

**Use Case**: Allow users to remove auto-injected blocks on specific posts.

### Use Cases

- Add plugin-specific blocks to all posts/pages automatically
- Insert promotional blocks at content end
- Add navigation items dynamically
- Inject analytics or tracking blocks

**Key Benefit**: Blocks remain visible and editable in Site Editor, unlike programmatic content injection.

## Interactivity API (WordPress 6.5+, Enhanced 6.8)

Standard way to add frontend interactivity to blocks without custom JavaScript frameworks.

### When to Use

- Need frontend interactivity (dropdowns, tabs, modals, filters)
- Want block-to-block communication
- Building dynamic features (search, shopping cart, instant navigation)
- Prefer declarative over imperative JavaScript

### Setup Requirements

1. **Install package**:
```bash
npm install @wordpress/interactivity --save
```

2. **Enable in block.json**:
```json
{
	"supports": {
		"interactivity": true
	},
	"viewScriptModule": "file:./view.js"
}
```

3. **Create view.js**:
```javascript
import { store } from '@wordpress/interactivity';

store( 'myPlugin', {
	state: {
		isOpen: false,
		count: 0
	},
	actions: {
		toggle: ( { state } ) => {
			state.isOpen = !state.isOpen;
		},
		increment: ( { state } ) => {
			state.count += 1;
		}
	},
	callbacks: {
		logOpen: ( { state } ) => {
			console.log( 'Is open:', state.isOpen );
		}
	}
} );
```

4. **Add directives in render.php**:
```php
<div
	data-wp-interactive="myPlugin"
	data-wp-context='{"isOpen": false}'
>
	<button
		data-wp-on--click="actions.toggle"
		data-wp-text="state.isOpen ? 'Close' : 'Open'"
	>
	</button>

	<div data-wp-bind--hidden="!state.isOpen">
		<p>This content toggles!</p>
	</div>
</div>
```

### Common Directives

- `data-wp-interactive` - Activates interactivity namespace
- `data-wp-context` - Local state for component
- `data-wp-on--{event}` - Event handlers (click, change, etc.)
- `data-wp-bind--{attribute}` - Bind attributes to state
- `data-wp-text` - Dynamic text content
- `data-wp-class--{classname}` - Conditional CSS classes
- `data-wp-each` - Loop over arrays (improved in 6.8)

### WordPress 6.8 Improvements

**wp-each directive enhancement**:
```php
<!-- Now handles non-iterable data gracefully -->
<ul data-wp-each="state.items">
	<li data-wp-text="context.item.name"></li>
</ul>
```

**Synchronous event handling**:
```javascript
import { store, withSyncEvent } from '@wordpress/interactivity';

store( 'myPlugin', {
	actions: {
		handleInput: withSyncEvent( ( { event, state } ) => {
			// Access event synchronously
			state.value = event.target.value;
		} )
	}
} );
```

### Accessing Context Programmatically (6.8+)

```javascript
import { store, getContext } from '@wordpress/interactivity';

store( 'myPlugin', {
	actions: {
		complexAction: () => {
			const context = getContext();
			// Access context.isOpen, context.count, etc.
			console.log( 'Current context:', context );
		}
	}
} );
```

### Shared State Across Blocks

Multiple blocks can share the same store namespace:

```javascript
// Block 1: Shopping Cart
store( 'myPlugin/shop', {
	state: {
		cartItems: [],
		total: 0
	},
	actions: {
		addToCart: ( { state }, product ) => {
			state.cartItems.push( product );
			state.total += product.price;
		}
	}
} );

// Block 2: Checkout Button (different block, same store)
store( 'myPlugin/shop', {
	actions: {
		checkout: ( { state } ) => {
			// Access shared state.cartItems
			console.log( 'Checking out', state.cartItems );
		}
	}
} );
```

**Key Pattern**: Use namespace like `myPlugin/feature` for shared state across blocks.

### Best Practices

- Use for client-side interactivity only (not server rendering)
- Keep state minimal and focused
- Leverage WordPress 6.8's improved error handling
- Use `withSyncEvent()` when you need immediate event access

## Custom Post Types

```php
function register_my_post_type() {
	$args = array(
		'public'      => true,
		'label'       => 'Books',
		'supports'    => array( 'title', 'editor', 'thumbnail' ),
		'has_archive' => true,
		'rewrite'     => array( 'slug' => 'books' ),
	);
	register_post_type( 'book', $args );
}
add_action( 'init', 'register_my_post_type' );
```

### Starter Content Patterns (WordPress 6.8)

WordPress 6.8 supports starter content for all post types:

```php
function my_register_cpt_with_starter_content() {
	register_post_type( 'portfolio', array(
		'public'   => true,
		'label'    => 'Portfolio',
		'supports' => array( 'title', 'editor', 'thumbnail' ),
		'template' => array(
			array( 'core/heading', array( 'content' => 'Project Title' ) ),
			array( 'core/paragraph', array( 'content' => 'Project description...' ) ),
			array( 'core/gallery' ),
		),
		'template_lock' => 'all', // Options: 'all', 'insert', false
	) );
}
add_action( 'init', 'my_register_cpt_with_starter_content' );
```

## Shortcodes

```php
function my_shortcode_function( $atts ) {
	$atts = shortcode_atts( array(
		'title' => 'Default Title',
		'count' => 5,
	), $atts );

	return '<div class="my-shortcode">' . esc_html( $atts['title'] ) . '</div>';
}
add_shortcode( 'my_shortcode', 'my_shortcode_function' );

// Usage: [my_shortcode title="Hello" count="10"]
```

## Meta Boxes

```php
function my_add_meta_box() {
	add_meta_box(
		'my_meta_box_id',
		'My Meta Box',
		'my_meta_box_callback',
		'post',
		'side'
	);
}
add_action( 'add_meta_boxes', 'my_add_meta_box' );

function my_meta_box_callback( $post ) {
	wp_nonce_field( 'my_meta_box_nonce', 'my_meta_box_nonce_field' );
	$value = get_post_meta( $post->ID, '_my_meta_key', true );
	echo '<input type="text" name="my_meta_field" value="' . esc_attr( $value ) . '">';
}

function my_save_meta_box( $post_id ) {
	if ( ! isset( $_POST['my_meta_box_nonce_field'] ) ||
	     ! wp_verify_nonce( $_POST['my_meta_box_nonce_field'], 'my_meta_box_nonce' ) ) {
		return;
	}

	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}

	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	if ( isset( $_POST['my_meta_field'] ) ) {
		$value = sanitize_text_field( $_POST['my_meta_field'] );
		update_post_meta( $post_id, '_my_meta_key', $value );
	}
}
add_action( 'save_post', 'my_save_meta_box' );
```

## Widgets

```php
class My_Widget extends WP_Widget {
	public function __construct() {
		parent::__construct(
			'my_widget',
			'My Widget',
			array( 'description' => 'Widget description' )
		);
	}

	public function widget( $args, $instance ) {
		echo $args['before_widget'];
		echo $args['before_title'] . esc_html( $instance['title'] ) . $args['after_title'];
		echo '<p>' . esc_html( $instance['text'] ) . '</p>';
		echo $args['after_widget'];
	}

	public function form( $instance ) {
		$title = isset( $instance['title'] ) ? $instance['title'] : '';
		$text  = isset( $instance['text'] ) ? $instance['text'] : '';
		?>
		<p>
			<label for="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>">Title:</label>
			<input class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>"
			       name="<?php echo esc_attr( $this->get_field_name( 'title' ) ); ?>"
			       type="text" value="<?php echo esc_attr( $title ); ?>">
		</p>
		<p>
			<label for="<?php echo esc_attr( $this->get_field_id( 'text' ) ); ?>">Text:</label>
			<input class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'text' ) ); ?>"
			       name="<?php echo esc_attr( $this->get_field_name( 'text' ) ); ?>"
			       type="text" value="<?php echo esc_attr( $text ); ?>">
		</p>
		<?php
	}

	public function update( $new_instance, $old_instance ) {
		$instance          = array();
		$instance['title'] = sanitize_text_field( $new_instance['title'] );
		$instance['text']  = sanitize_text_field( $new_instance['text'] );
		return $instance;
	}
}

function register_my_widget() {
	register_widget( 'My_Widget' );
}
add_action( 'widgets_init', 'register_my_widget' );
```

## Related Skills

- **wordpress-core** - Security, hooks, database, coding standards
- **wordpress-modern** - Performance optimization, asset loading, WP 6.8 features

## Best Practices Summary

1. **Block Hooks Over Manual Injection**: Use Block Hooks API instead of programmatic content insertion
2. **Interactivity API for Frontend**: Prefer Interactivity API over custom JavaScript for block interactivity
3. **Starter Content Templates**: Provide default content patterns for Custom Post Types
4. **Modern Block Development**: Use `viewScriptModule` for interactive blocks instead of legacy methods
5. **Graceful Degradation**: Ensure blocks work without JavaScript when possible
6. **Block-First Thinking**: Design plugin features as blocks when they need UI components
7. **Shared State**: Use namespaced stores (`myPlugin/feature`) for inter-block communication
