---
name: wordpress-blocks
description: WordPress custom Gutenberg block development with server-side PHP rendering. Includes block registration patterns, media upload integration, multiple item blocks, proper escaping/sanitization, and editor UI best practices. Maintains separation of concerns where editors control content while developers control design.
---

# WordPress Custom Gutenberg Blocks

Build custom Gutenberg blocks for WordPress themes that give content editors control over text and media while developers retain control over layout and design.

## Block Development Philosophy

**Editors Control:**
- Text content (headers, descriptions, body copy)
- Links and CTAs
- Images (via WordPress media uploader)

**Developers Control:**
- HTML structure and markup
- CSS styling and layout
- JavaScript functionality
- Design consistency

**Benefits:**
- Consistent design across the site
- Easy content updates without developer intervention
- Reduced risk of breaking layouts
- Cleaner, more maintainable codebase

## Block File Structure

Each block consists of three files:

```
inc/blocks/
├── block-name.php           # PHP registration and render
├── js/
│   └── block-name.js        # Editor JavaScript
└── css/                     # Optional
    └── block-name.css       # Block-specific styles
```

**Register block in functions.php:**
```php
// custom gutenberg blocks
require get_template_directory() . '/inc/blocks/hp-lede.php';
```

## Basic Block Template

### PHP Registration File

**File:** `/inc/blocks/block-name.php`

```php
<?php
/**
 * Block Name Block
 */

function register_block_name_block() {
    register_block_type('theme/block-name', array(
        'render_callback' => 'render_block_name_block',
        'attributes' => array(
            'blockTitle' => array(
                'type' => 'string',
                'default' => 'Default Title'
            ),
            'blockDescription' => array(
                'type' => 'string',
                'default' => 'Default description text.'
            ),
            'blockLink' => array(
                'type' => 'string',
                'default' => '/default-link/'
            ),
        ),
    ));
}
add_action('init', 'register_block_name_block');

function render_block_name_block($attributes) {
    // Sanitize and escape all attributes
    $block_title = isset($attributes['blockTitle']) ? esc_html($attributes['blockTitle']) : '';
    $block_description = isset($attributes['blockDescription']) ? esc_html($attributes['blockDescription']) : '';
    $block_link = isset($attributes['blockLink']) ? esc_url($attributes['blockLink']) : '';
    
    ob_start();
    ?>
    <section class="block-name">
        <h2><?php echo $block_title; ?></h2>
        <p><?php echo $block_description; ?></p>
        <a href="<?php echo $block_link; ?>" class="button">Learn More</a>
    </section>
    <?php
    return ob_get_clean();
}

function enqueue_block_name_block_editor_assets() {
    wp_enqueue_script(
        'block-name-block',
        get_template_directory_uri() . '/inc/blocks/js/block-name.js',
        array('wp-blocks', 'wp-element', 'wp-editor', 'wp-components'),
        filemtime(get_template_directory() . '/inc/blocks/js/block-name.js'),
        false
    );
}
add_action('enqueue_block_editor_assets', 'enqueue_block_name_block_editor_assets');
```

### JavaScript Editor File

**File:** `/inc/blocks/js/block-name.js`

```javascript
(function(wp) {
    const { registerBlockType } = wp.blocks;
    const { TextControl, TextareaControl } = wp.components;
    const { createElement: el } = wp.element;

    registerBlockType('theme/block-name', {
        title: 'Block Name',
        icon: 'admin-post',
        category: 'common',
        attributes: {
            blockTitle: {
                type: 'string',
                default: 'Default Title'
            },
            blockDescription: {
                type: 'string',
                default: 'Default description text.'
            },
            blockLink: {
                type: 'string',
                default: '/default-link/'
            }
        },

        edit: function(props) {
            const { attributes, setAttributes } = props;

            return el('div', { 
                className: 'block-name-editor',
                style: { padding: '20px', border: '1px solid #ddd' }
            },
                el('h3', {}, 'Block Name'),
                
                el(TextControl, {
                    label: 'Block Title',
                    value: attributes.blockTitle,
                    onChange: function(value) {
                        setAttributes({ blockTitle: value });
                    }
                }),
                
                el(TextareaControl, {
                    label: 'Description',
                    value: attributes.blockDescription,
                    onChange: function(value) {
                        setAttributes({ blockDescription: value });
                    },
                    rows: 4
                }),
                
                el(TextControl, {
                    label: 'Link',
                    value: attributes.blockLink,
                    onChange: function(value) {
                        setAttributes({ blockLink: value });
                    }
                })
            );
        },

        save: function() {
            return null; // Using PHP render callback
        }
    });
})(window.wp);
```

## Common Attribute Types

### Text Fields

**PHP:**
```php
'textField' => array(
    'type' => 'string',
    'default' => 'Default text'
),
```

**JavaScript:**
```javascript
el(TextControl, {
    label: 'Text Field',
    value: attributes.textField,
    onChange: function(value) {
        setAttributes({ textField: value });
    }
})
```

### Textarea Fields

**PHP:**
```php
'textareaField' => array(
    'type' => 'string',
    'default' => 'Default longer text'
),
```

**JavaScript:**
```javascript
el(TextareaControl, {
    label: 'Textarea Field',
    value: attributes.textareaField,
    onChange: function(value) {
        setAttributes({ textareaField: value });
    },
    rows: 6
})
```

### Number Fields

**PHP:**
```php
'numberField' => array(
    'type' => 'number',
    'default' => 0
),
```

**JavaScript:**
```javascript
el(TextControl, {
    label: 'Number Field',
    type: 'number',
    value: attributes.numberField,
    onChange: function(value) {
        setAttributes({ numberField: parseInt(value) });
    }
})
```

## Media Uploader Pattern

### Image Upload Attributes

**PHP:**
```php
'imageId' => array(
    'type' => 'number',
    'default' => 0
),
'imageUrl' => array(
    'type' => 'string',
    'default' => ''
),
```

### Image Upload in JavaScript

```javascript
const { MediaUpload, MediaUploadCheck } = wp.blockEditor;
const { Button } = wp.components;

// In edit function:
el(MediaUploadCheck, {},
    el(MediaUpload, {
        onSelect: function(media) {
            setAttributes({
                imageId: media.id,
                imageUrl: media.url
            });
        },
        allowedTypes: ['image'],
        value: attributes.imageId,
        render: function(obj) {
            return el('div', { className: 'media-upload-wrapper' },
                attributes.imageUrl ? 
                    el('div', {},
                        el('img', {
                            src: attributes.imageUrl,
                            style: { maxWidth: '200px', display: 'block', marginBottom: '10px' }
                        }),
                        el(Button, {
                            onClick: obj.open,
                            className: 'button'
                        }, 'Change Image'),
                        el(Button, {
                            onClick: function() {
                                setAttributes({
                                    imageId: 0,
                                    imageUrl: ''
                                });
                            },
                            className: 'button',
                            style: { marginLeft: '10px' }
                        }, 'Remove')
                    ) :
                    el(Button, {
                        onClick: obj.open,
                        className: 'button button-primary'
                    }, 'Upload Image')
            );
        }
    })
)
```

### Image Rendering in PHP

```php
// Get image URL from ID
$image_url = '';
if (isset($attributes['imageId']) && $attributes['imageId']) {
    $image_url = wp_get_attachment_image_url(absint($attributes['imageId']), 'full');
} elseif (isset($attributes['imageUrl'])) {
    $image_url = esc_url($attributes['imageUrl']);
}

// Render in template
<?php if ($image_url) : ?>
    <img src="<?php echo esc_url($image_url); ?>" alt="" class="block-image">
<?php endif; ?>
```

## Multiple Item Blocks Pattern

For blocks with repeating items:

### PHP Attributes for Multiple Items

```php
'attributes' => array(
    'blockTitle' => array(
        'type' => 'string',
        'default' => 'Additional Resources'
    ),
    // Item 1
    'item1ImageId' => array('type' => 'number', 'default' => 0),
    'item1ImageUrl' => array('type' => 'string', 'default' => ''),
    'item1Header' => array('type' => 'string', 'default' => 'Item 1 Title'),
    'item1Subhead' => array('type' => 'string', 'default' => 'Item 1 description'),
    'item1Link' => array('type' => 'string', 'default' => '/item-1/'),
    // Item 2
    'item2ImageId' => array('type' => 'number', 'default' => 0),
    'item2ImageUrl' => array('type' => 'string', 'default' => ''),
    'item2Header' => array('type' => 'string', 'default' => 'Item 2 Title'),
    'item2Subhead' => array('type' => 'string', 'default' => 'Item 2 description'),
    'item2Link' => array('type' => 'string', 'default' => '/item-2/'),
    // Item 3
    'item3ImageId' => array('type' => 'number', 'default' => 0),
    'item3ImageUrl' => array('type' => 'string', 'default' => ''),
    'item3Header' => array('type' => 'string', 'default' => 'Item 3 Title'),
    'item3Subhead' => array('type' => 'string', 'default' => 'Item 3 description'),
    'item3Link' => array('type' => 'string', 'default' => '/item-3/'),
),
```

### Helper Function for Media Uploaders

```javascript
function renderMediaUpload(itemNum) {
    const imageIdAttr = 'item' + itemNum + 'ImageId';
    const imageUrlAttr = 'item' + itemNum + 'ImageUrl';
    
    return el(MediaUploadCheck, {},
        el(MediaUpload, {
            onSelect: function(media) {
                const attrs = {};
                attrs[imageIdAttr] = media.id;
                attrs[imageUrlAttr] = media.url;
                setAttributes(attrs);
            },
            allowedTypes: ['image'],
            value: attributes[imageIdAttr],
            render: function(obj) {
                return el('div', { className: 'media-upload-wrapper' },
                    attributes[imageUrlAttr] ? 
                        el('div', {},
                            el('img', {
                                src: attributes[imageUrlAttr],
                                style: { maxWidth: '200px', display: 'block', marginBottom: '10px' }
                            }),
                            el(Button, {
                                onClick: obj.open,
                                className: 'button'
                            }, 'Change Image'),
                            el(Button, {
                                onClick: function() {
                                    const attrs = {};
                                    attrs[imageIdAttr] = 0;
                                    attrs[imageUrlAttr] = '';
                                    setAttributes(attrs);
                                },
                                className: 'button',
                                style: { marginLeft: '10px' }
                            }, 'Remove')
                        ) :
                        el(Button, {
                            onClick: obj.open,
                            className: 'button button-primary'
                        }, 'Upload Image')
                );
            }
        })
    );
}

// Use in edit function:
el('h4', {}, 'Item 1'),
renderMediaUpload(1),
el(TextControl, {
    label: 'Header',
    value: attributes.item1Header,
    onChange: function(value) {
        setAttributes({ item1Header: value });
    }
}),
// ... more fields
```

## WordPress VIP Compliance for Blocks

### Always Escape Output in PHP

```php
// Text
$title = isset($attributes['title']) ? esc_html($attributes['title']) : '';

// Attributes
$class = isset($attributes['className']) ? esc_attr($attributes['className']) : '';

// URLs
$link = isset($attributes['link']) ? esc_url($attributes['link']) : '';

// Multi-paragraph text (preserves formatting)
$description = isset($attributes['description']) ? wp_kses_post(wpautop($attributes['description'])) : '';
```

### Always Sanitize in PHP

```php
// Integers (for image IDs, etc.)
$image_id = isset($attributes['imageId']) ? absint($attributes['imageId']) : 0;

// Numbers
$count = isset($attributes['count']) ? intval($attributes['count']) : 0;
```

### Proper Asset Paths

```php
// CORRECT:
get_template_directory_uri() . '/inc/blocks/js/block-name.js'
get_template_directory_uri() . '/assets/img/site/hero.jpg'

// Use filemtime for cache busting
filemtime(get_template_directory() . '/inc/blocks/js/block-name.js')
```

### Required JavaScript Dependencies

```php
wp_enqueue_script(
    'block-name',
    get_template_directory_uri() . '/inc/blocks/js/block-name.js',
    array(
        'wp-blocks',      // Core block functionality
        'wp-element',     // React elements
        'wp-editor',      // Editor components
        'wp-components',  // UI components
        'wp-block-editor' // For MediaUpload
    ),
    filemtime(get_template_directory() . '/inc/blocks/js/block-name.js'),
    false // Load in header for editor
);
```

## Block Icons

Common Dashicons for blocks:

```javascript
icon: 'admin-post'      // Document
icon: 'megaphone'       // Announcement/Lede
icon: 'admin-links'     // Resources/Links
icon: 'info'            // Information
icon: 'warning'         // Urgent/Warning
icon: 'games'           // Sports/Games
icon: 'awards'          // Achievement
icon: 'media-document'  // Article
```

## Editor Styling Tips

### Add Visual Hierarchy in Editor

```javascript
el('div', { 
    className: 'block-editor',
    style: { padding: '20px', border: '1px solid #ddd' }
},
    el('h3', {}, 'Block Title'),
    el('hr'),
    el('h4', {}, 'Section 1'),
    // fields...
    el('hr'),
    el('h4', {}, 'Section 2'),
    // more fields...
)
```

### Add Preview in Editor

```javascript
el('div', { style: { marginTop: '15px', padding: '10px', backgroundColor: '#f0f0f0' } },
    el('strong', {}, 'Preview:'),
    el('p', { style: { marginTop: '10px' } }, attributes.description)
)
```

## Complete Block Example

**HP Lede Block with Image, Text, and CTA:**

### PHP File: `/inc/blocks/hp-lede.php`

```php
<?php
/**
 * HP Lede Block
 */

function register_hp_lede_block() {
    register_block_type('theme/hp-lede', array(
        'render_callback' => 'render_hp_lede_block',
        'attributes' => array(
            'ledeHeader' => array(
                'type' => 'string',
                'default' => ''
            ),
            'ledeSubhed' => array(
                'type' => 'string',
                'default' => ''
            ),
            'box1Title' => array(
                'type' => 'string',
                'default' => ''
            ),
            'box1Cta' => array(
                'type' => 'string',
                'default' => ''
            ),
            'box1Link' => array(
                'type' => 'string',
                'default' => ''
            ),
            'box2Title' => array(
                'type' => 'string',
                'default' => ''
            ),
            'box2Cta' => array(
                'type' => 'string',
                'default' => ''
            ),
            'box2Link' => array(
                'type' => 'string',
                'default' => ''
            ),
        ),
    ));
}
add_action('init', 'register_hp_lede_block');

function render_hp_lede_block($attributes) {
    $lede_header = isset($attributes['ledeHeader']) ? esc_html($attributes['ledeHeader']) : '';
    $lede_subhed = isset($attributes['ledeSubhed']) ? esc_html($attributes['ledeSubhed']) : '';
    $box1_title = isset($attributes['box1Title']) ? esc_html($attributes['box1Title']) : '';
    $box1_cta = isset($attributes['box1Cta']) ? esc_html($attributes['box1Cta']) : '';
    $box1_link = isset($attributes['box1Link']) ? esc_url($attributes['box1Link']) : '';
    $box2_title = isset($attributes['box2Title']) ? esc_html($attributes['box2Title']) : '';
    $box2_cta = isset($attributes['box2Cta']) ? esc_html($attributes['box2Cta']) : '';
    $box2_link = isset($attributes['box2Link']) ? esc_url($attributes['box2Link']) : '';
    
    $hero_image = get_template_directory_uri() . '/assets/img/site/hero-image-2.jpg';
    
    ob_start();
    ?>
    <section class="fullwidth-container page-home home-hero bg-yellow">
        <div class="lede-image">
            <img class="image" src="<?php echo esc_url($hero_image); ?>" alt="">
        </div>
        <div class="home-hero-text-container">
            <div class="home-hero-text">
                <h3 class="page-title"><?php echo $lede_header; ?></h3>
                <p class="page-subtitle"><?php echo $lede_subhed; ?></p>
            </div>
            <div class="home-hero-box-container">
                <a href="<?php echo $box1_link; ?>" class="home-lede-box box-1">
                    <h2><?php echo $box1_title; ?></h2>
                    <button class="button primary rounded red"><?php echo $box1_cta; ?></button>
                </a>
                <a href="<?php echo $box2_link; ?>" class="home-lede-box box-2">
                    <h2><?php echo $box2_title; ?></h2>
                    <button class="button primary rounded white"><?php echo $box2_cta; ?></button>
                </a>
            </div>
        </div>
    </section>
    <?php
    return ob_get_clean();
}

function enqueue_hp_lede_block_editor_assets() {
    wp_enqueue_script(
        'hp-lede-block',
        get_template_directory_uri() . '/inc/blocks/js/hp-lede.js',
        array('wp-blocks', 'wp-element', 'wp-editor', 'wp-components'),
        filemtime(get_template_directory() . '/inc/blocks/js/hp-lede.js'),
        false
    );
}
add_action('enqueue_block_editor_assets', 'enqueue_hp_lede_block_editor_assets');
```

### JavaScript File: `/inc/blocks/js/hp-lede.js`

```javascript
(function(wp) {
    const { registerBlockType } = wp.blocks;
    const { TextControl } = wp.components;
    const { createElement: el } = wp.element;

    registerBlockType('theme/hp-lede', {
        title: 'HP Lede',
        icon: 'megaphone',
        category: 'common',
        attributes: {
            ledeHeader: {
                type: 'string',
                default: ''
            },
            ledeSubhed: {
                type: 'string',
                default: ''
            },
            box1Title: {
                type: 'string',
                default: ''
            },
            box1Cta: {
                type: 'string',
                default: ''
            },
            box1Link: {
                type: 'string',
                default: ''
            },
            box2Title: {
                type: 'string',
                default: ''
            },
            box2Cta: {
                type: 'string',
                default: ''
            },
            box2Link: {
                type: 'string',
                default: ''
            }
        },

        edit: function(props) {
            const { attributes, setAttributes } = props;

            return el('div', { className: 'hp-lede-editor' },
                el('h3', {}, 'HP Lede Block'),
                
                el('h4', {}, 'Header Section'),
                el(TextControl, {
                    label: 'Lede Header',
                    value: attributes.ledeHeader,
                    onChange: function(value) {
                        setAttributes({ ledeHeader: value });
                    }
                }),
                el(TextControl, {
                    label: 'Lede Subhed',
                    value: attributes.ledeSubhed,
                    onChange: function(value) {
                        setAttributes({ ledeSubhed: value });
                    }
                }),
                
                el('h4', {}, 'Box 1'),
                el(TextControl, {
                    label: 'Box 1 Title',
                    value: attributes.box1Title,
                    onChange: function(value) {
                        setAttributes({ box1Title: value });
                    }
                }),
                el(TextControl, {
                    label: 'Box 1 CTA Text',
                    value: attributes.box1Cta,
                    onChange: function(value) {
                        setAttributes({ box1Cta: value });
                    }
                }),
                el(TextControl, {
                    label: 'Box 1 Link',
                    value: attributes.box1Link,
                    onChange: function(value) {
                        setAttributes({ box1Link: value });
                    }
                }),
                
                el('h4', {}, 'Box 2'),
                el(TextControl, {
                    label: 'Box 2 Title',
                    value: attributes.box2Title,
                    onChange: function(value) {
                        setAttributes({ box2Title: value });
                    }
                }),
                el(TextControl, {
                    label: 'Box 2 CTA Text',
                    value: attributes.box2Cta,
                    onChange: function(value) {
                        setAttributes({ box2Cta: value });
                    }
                }),
                el(TextControl, {
                    label: 'Box 2 Link',
                    value: attributes.box2Link,
                    onChange: function(value) {
                        setAttributes({ box2Link: value });
                    }
                })
            );
        },

        save: function() {
            return null;
        }
    });
})(window.wp);
```

## Quick Reference

### Block Registration Checklist

- [ ] PHP file in `/inc/blocks/`
- [ ] JavaScript file in `/inc/blocks/js/`
- [ ] Block registered with `register_block_type()`
- [ ] Render callback function created
- [ ] All attributes defined with types and defaults
- [ ] All output escaped (`esc_html()`, `esc_url()`, `esc_attr()`)
- [ ] Editor assets enqueued with dependencies
- [ ] Block added to functions.php includes
- [ ] Icon and category specified
- [ ] `save` function returns `null` (using PHP render)

### Common JavaScript Components

```javascript
const { registerBlockType } = wp.blocks;
const { TextControl, TextareaControl, Button } = wp.components;
const { MediaUpload, MediaUploadCheck } = wp.blockEditor;
const { createElement: el } = wp.element;
```

### Attribute Type Reference

```php
'string' => array('type' => 'string', 'default' => '')
'number' => array('type' => 'number', 'default' => 0)
'boolean' => array('type' => 'boolean', 'default' => false)
'array' => array('type' => 'array', 'default' => [])
'object' => array('type' => 'object', 'default' => {})
```