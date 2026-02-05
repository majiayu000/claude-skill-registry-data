---
name: wordpress-themes
description: WordPress custom theme development specialist focused on clean, maintainable code following VIP standards. Includes modular theme structure, dart-sass via Homebrew, proper script/style enqueueing, template parts organization, text domain management, and comprehensive security practices (escaping, sanitization, file paths).
---

# WordPress Custom Theme Development

Build clean, VIP-compliant WordPress custom themes with modular structure and modern tooling.

## Core Philosophy

- **Minimal Plugin Dependency**: Use public plugins for specialized functions (SEO, security), keep custom code in theme
- **VIP Standards**: Follow WordPress VIP coding standards for enterprise-grade quality
- **Clean Organization**: Modular structure with clear separation of concerns
- **Maintainability**: Easy to understand, easy to update

## Theme Directory Structure

```
theme-root/
├── src/
│   └── scss/
│       ├── vendor/        # Third-party CSS (reset, normalize)
│       ├── core/          # Variables, mixins, utilities
│       ├── pages/         # Page-specific CSS
│       └── styles.scss    # Main entry point
├── assets/
│   ├── css/
│   │   ├── styles.css     # Compiled main stylesheet
│   │   └── pages/         # Compiled page-specific stylesheets
│   ├── img/site/
│   └── svg/
├── inc/
│   └── functions/
│       ├── css_pagetype.php
│       ├── js_scripts.php
│       ├── theme_media.php
│       └── custom_post_types.php
├── template-parts/
│   ├── content-post.php
│   ├── content-page.php
│   ├── content-[cpt].php
│   ├── footer-markup.php
│   └── header-markup.php
├── 404.php
├── footer.php
├── functions.php          # Clean, mostly includes
├── header.php
├── index.php
├── sidebar.php
├── style.css              # Theme metadata
└── template-front.php
```

## functions.php Pattern

Keep functions.php as a clean table of contents with descriptive comments.

```php
<?php

/**
 * Theme text domain constant
 */
if ( ! defined( 'CUSTOM_THEME_TEXT_DOMAIN' ) ) {
    define( 'CUSTOM_THEME_TEXT_DOMAIN', 'custom-theme' );
}

add_theme_support( "title-tag" );
add_theme_support( "responsive-embeds" );
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );

// includes js file based on page type
require get_template_directory() . '/inc/functions/js_scripts.php';

// includes css file based on page type
require get_template_directory() . '/inc/functions/css_pagetype.php';

// media and image support
require get_template_directory() . '/inc/functions/theme_media.php';

// custom post types and taxonomies
require get_template_directory() . '/inc/functions/custom_post_types.php';
```

**CRITICAL:** Never include `flush_rewrite_rules()` in production code, even commented out.

## CSS/Sass Workflow

### Setup (dart-sass via Homebrew)

```bash
# Installation
brew install sass/sass/sass
brew upgrade sass

# Watch mode (development)
cd src/scss
sass styles.scss:../../assets/css/styles.css --watch

# Build mode (production)
sass styles.scss:../../assets/css/styles.css --style=compressed
```

### Helpful Shell Aliases (zsh)

```bash
alias sassw='sass styles.scss:../../assets/css/styles.css --watch'
alias sassb='sass styles.scss:../../assets/css/styles.css --style=compressed'

# Page-specific Sass compilation
sassp() {
  if [[ -z "$1" ]]; then
    echo "Usage: sassp <filename> [build]"
    return 1
  fi
  if [[ "$2" == "build" ]]; then
    sass pages/${1}.scss:../../assets/css/pages/${1}.css --style=compressed
  else
    sass pages/${1}.scss:../../assets/css/pages/${1}.css --watch
  fi
}
```

### CSS Enqueueing

**File:** `/inc/functions/css_pagetype.php`

```php
<?php
// Global styles
if ( !function_exists ( "custom_theme_css_global" ) ) :
function custom_theme_css_global() {
    $theme_version = wp_get_theme()->get( "Version" );
    wp_enqueue_style( 
        "custom-theme-global", 
        get_template_directory_uri() . "/assets/css/styles.css", 
        array(), 
        $theme_version 
    );
}
add_action( "wp_enqueue_scripts", "custom_theme_css_global", 10 );
endif;

// Page-specific styles
if ( !function_exists ( "custom_theme_css_by_page_type" ) ) :
function custom_theme_css_by_page_type() {
    $theme_version = wp_get_theme()->get( "Version" );
    
    if ( is_front_page() || is_page('front-page') ) {
        wp_enqueue_style( 
            "custom-theme-front", 
            get_template_directory_uri() . "/assets/css/pages/front.css", 
            array(), 
            $theme_version 
        );
    }
}
add_action( "wp_enqueue_scripts", "custom_theme_css_by_page_type", 20 );
endif;
```

**Key Points:**
- Use theme version for cache busting
- Consistent handle naming (`custom-theme-*`)
- Page-specific CSS loaded conditionally
- Priority ordering (global at 10, specific at 20)

### JavaScript Enqueueing

**File:** `/inc/functions/js_scripts.php`

```php
<?php
if ( !function_exists ( "custom_theme_js_global" ) ) :
function custom_theme_js_global() {
    $theme_version = wp_get_theme()->get( 'Version' );
    
    // Main scripts: load in footer
    // wp_enqueue_script( 
    //     'theme-main', 
    //     get_template_directory_uri() . '/assets/js/app.js', 
    //     array(), 
    //     $theme_version, 
    //     true 
    // );
}
add_action('wp_enqueue_scripts', 'custom_theme_js_global');
endif;
```

**Key Points:**
- Always pass array for dependencies (even if empty)
- Always pass version for cache busting
- Use `true` for footer loading (better performance)

## Template Structure

### index.php Pattern

```php
<?php get_header(); ?>

<?php 
$page_class = is_front_page() ? 'front' : 'notfront';
?>

<main id="site-content" role="main" class="<?php echo esc_attr($page_class); ?>">
    <?php 
    if ( is_singular() ) {
        if ( have_posts() ) {
            while ( have_posts() ) {
                the_post();
                get_template_part( 'template-parts/content', get_post_type() );
            }
        }
    }
    ?>
</main>

<?php get_footer(); ?>
```

### header.php Pattern

```php
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<?php get_template_part( 'template-parts/header-markup' ); ?>
```

### footer.php Pattern

```php
<?php get_template_part( 'template-parts/footer-markup' ); ?>

<?php wp_footer(); ?>
</body>
</html>
```

## WordPress VIP Compliance

### Always Escape Output

```php
// Text content
echo esc_html( $text );

// HTML attributes
echo esc_attr( $class );

// URLs
echo esc_url( $url );

// Translation functions with escaping
esc_html__( 'Text', CUSTOM_THEME_TEXT_DOMAIN )
esc_attr__( 'Text', CUSTOM_THEME_TEXT_DOMAIN )
esc_html_e( 'Text', CUSTOM_THEME_TEXT_DOMAIN )
```

### Always Sanitize Input

```php
// Text fields
$value = sanitize_text_field( $_POST['field'] );

// URLs
$url = esc_url_raw( $_POST['url'] );

// Integers
$id = absint( $_POST['id'] );
```

### Proper File Paths

```php
// CORRECT: Use WordPress functions
get_template_directory()        // /path/to/theme
get_template_directory_uri()    // https://site.com/wp-content/themes/theme

// WRONG: Never hardcode paths
```

### Text Domain Best Practices

```php
// Define constant in functions.php
define( 'CUSTOM_THEME_TEXT_DOMAIN', 'custom-theme' );

// Use throughout theme
__( 'Read More', CUSTOM_THEME_TEXT_DOMAIN )
the_content( __( 'Continue reading', CUSTOM_THEME_TEXT_DOMAIN ) );
```

## Media Support

**File:** `/inc/functions/theme_media.php`

```php
<?php

// Post thumbnail support
add_theme_support( 'post-thumbnails' );

// Custom image sizes
add_image_size( 'hero-image', 1920, 1080, true );

// Add custom sizes to media library dropdown
if ( !function_exists( "custom_image_sizes" ) ) :
function custom_image_sizes( $sizes ) {
    return array_merge( $sizes, array(
        'hero-image' => __( 'Hero Image', CUSTOM_THEME_TEXT_DOMAIN ),
    ));
}
endif;
add_filter( 'image_size_names_choose', 'custom_image_sizes' );
```

## Template Parts Pattern

### content-post.php

```php
<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
    <header class="entry-header">
        <?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
    </header>

    <div class="entry-content">
        <?php the_content( __( 'Continue reading', CUSTOM_THEME_TEXT_DOMAIN ) ); ?>
    </div>

    <footer class="entry-footer">
        <?php the_date(); ?>
        <?php the_author(); ?>
    </footer>
</article>
```

## VIP Compliance Checklist

**Before deploying:**

- [ ] All output is escaped (`esc_html()`, `esc_attr()`, `esc_url()`)
- [ ] All input is sanitized
- [ ] Scripts/styles properly enqueued with versions
- [ ] Text domain constant defined and used throughout
- [ ] No `flush_rewrite_rules()` in code
- [ ] File paths use WordPress functions
- [ ] No hardcoded URLs or paths
- [ ] Template parts used for modular structure
- [ ] Theme versioning for cache busting

## Quick Reference

### Theme Support Features

```php
add_theme_support( 'title-tag' );
add_theme_support( 'post-thumbnails' );
add_theme_support( 'responsive-embeds' );
add_theme_support( 'html5', array( 'search-form', 'comment-form' ) );
```

### Clean Up WordPress Head

```php
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
```