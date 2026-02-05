---
name: Shopify Schema Design
description: Best practices for creating comprehensive section schemas with all setting types
---

# Shopify Schema Design

## Schema Structure

The `{% schema %}` tag defines how a section appears in the theme editor:

```json
{
  "name": "Section Name",
  "tag": "section",
  "class": "section-class",
  "limit": 1,
  "settings": [...],
  "blocks": [...],
  "presets": [...]
}
```

## Setting Types

### Text Input
```json
{
  "type": "text",
  "id": "heading",
  "label": "Heading",
  "default": "Default text",
  "info": "Helpful description",
  "placeholder": "Enter text here"
}
```

### Textarea
```json
{
  "type": "textarea",
  "id": "description",
  "label": "Description",
  "default": "Default description"
}
```

### Rich Text
```json
{
  "type": "richtext",
  "id": "content",
  "label": "Content",
  "default": "<p>Default rich text content</p>"
}
```

### Number / Range
```json
{
  "type": "range",
  "id": "padding",
  "label": "Padding",
  "min": 0,
  "max": 100,
  "step": 4,
  "unit": "px",
  "default": 40,
  "info": "Section padding in pixels"
}
```

### Checkbox
```json
{
  "type": "checkbox",
  "id": "show_vendor",
  "label": "Show Product Vendor",
  "default": true,
  "info": "Display vendor name on product cards"
}
```

### Select / Dropdown
```json
{
  "type": "select",
  "id": "layout",
  "label": "Layout Style",
  "options": [
    {
      "value": "grid",
      "label": "Grid"
    },
    {
      "value": "carousel",
      "label": "Carousel"
    },
    {
      "value": "list",
      "label": "List"
    }
  ],
  "default": "grid",
  "info": "Choose how products are displayed"
}
```

### Radio Buttons
```json
{
  "type": "radio",
  "id": "alignment",
  "label": "Text Alignment",
  "options": [
    {
      "value": "left",
      "label": "Left"
    },
    {
      "value": "center",
      "label": "Center"
    },
    {
      "value": "right",
      "label": "Right"
    }
  ],
  "default": "center"
}
```

### Color Picker
```json
{
  "type": "color",
  "id": "bg_color",
  "label": "Background Color",
  "default": "#ffffff",
  "info": "Section background color"
}
```

### Color Background
```json
{
  "type": "color_background",
  "id": "background_gradient",
  "label": "Background Gradient",
  "info": "Supports solid colors and gradients"
}
```

### Image Picker
```json
{
  "type": "image_picker",
  "id": "image",
  "label": "Image",
  "info": "Recommended size: 1600 x 900 px"
}
```

### Font Picker
```json
{
  "type": "font_picker",
  "id": "heading_font",
  "label": "Heading Font",
  "default": "assistant_n4",
  "info": "Choose font for headings"
}
```

### Collection Picker
```json
{
  "type": "collection",
  "id": "collection",
  "label": "Collection"
}
```

### Product Picker
```json
{
  "type": "product",
  "id": "featured_product",
  "label": "Featured Product"
}
```

### Product List
```json
{
  "type": "product_list",
  "id": "products",
  "label": "Products",
  "limit": 12,
  "info": "Select up to 12 products"
}
```

### Collection List
```json
{
  "type": "collection_list",
  "id": "collections",
  "label": "Collections",
  "limit": 8
}
```

### Blog Picker
```json
{
  "type": "blog",
  "id": "blog",
  "label": "Blog"
}
```

### Article Picker
```json
{
  "type": "article",
  "id": "article",
  "label": "Article"
}
```

### Page Picker
```json
{
  "type": "page",
  "id": "page",
  "label": "Page"
}
```

### Link / URL
```json
{
  "type": "url",
  "id": "button_link",
  "label": "Button Link",
  "info": "Link to internal page or external URL"
}
```

### Video URL
```json
{
  "type": "video_url",
  "id": "video",
  "label": "Video URL",
  "accept": ["youtube", "vimeo"],
  "info": "Supports YouTube and Vimeo"
}
```

### HTML
```json
{
  "type": "html",
  "id": "custom_html",
  "label": "Custom HTML",
  "info": "Add custom HTML code"
}
```

### Liquid
```json
{
  "type": "liquid",
  "id": "custom_liquid",
  "label": "Custom Liquid",
  "info": "Add custom Liquid code"
}
```

## Organizational Elements

### Header
```json
{
  "type": "header",
  "content": "Section Heading"
}
```

### Paragraph
```json
{
  "type": "paragraph",
  "content": "Helpful information or instructions for merchants."
}
```

## Complete Schema Example

```json
{% schema %}
{
  "name": "Product Grid",
  "tag": "section",
  "class": "product-grid-section",
  "settings": [
    {
      "type": "header",
      "content": "Content"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Featured Products"
    },
    {
      "type": "richtext",
      "id": "description",
      "label": "Description"
    },
    {
      "type": "collection",
      "id": "collection",
      "label": "Collection"
    },
    {
      "type": "range",
      "id": "products_count",
      "label": "Number of Products",
      "min": 2,
      "max": 12,
      "step": 1,
      "default": 4
    },
    {
      "type": "header",
      "content": "Layout"
    },
    {
      "type": "select",
      "id": "layout",
      "label": "Layout Style",
      "options": [
        {
          "value": "grid",
          "label": "Grid"
        },
        {
          "value": "carousel",
          "label": "Carousel"
        }
      ],
      "default": "grid"
    },
    {
      "type": "select",
      "id": "columns_desktop",
      "label": "Desktop Columns",
      "options": [
        {
          "value": "2",
          "label": "2"
        },
        {
          "value": "3",
          "label": "3"
        },
        {
          "value": "4",
          "label": "4"
        }
      ],
      "default": "4"
    },
    {
      "type": "select",
      "id": "columns_mobile",
      "label": "Mobile Columns",
      "options": [
        {
          "value": "1",
          "label": "1"
        },
        {
          "value": "2",
          "label": "2"
        }
      ],
      "default": "1"
    },
    {
      "type": "header",
      "content": "Product Card"
    },
    {
      "type": "checkbox",
      "id": "show_vendor",
      "label": "Show Product Vendor",
      "default": false
    },
    {
      "type": "checkbox",
      "id": "show_quick_view",
      "label": "Enable Quick View",
      "default": true
    },
    {
      "type": "header",
      "content": "Colors"
    },
    {
      "type": "color",
      "id": "bg_color",
      "label": "Background Color",
      "default": "#ffffff"
    },
    {
      "type": "color",
      "id": "text_color",
      "label": "Text Color",
      "default": "#000000"
    },
    {
      "type": "header",
      "content": "Spacing"
    },
    {
      "type": "range",
      "id": "padding_top",
      "label": "Top Spacing",
      "min": 0,
      "max": 100,
      "step": 4,
      "unit": "px",
      "default": 40
    },
    {
      "type": "range",
      "id": "padding_bottom",
      "label": "Bottom Spacing",
      "min": 0,
      "max": 100,
      "step": 4,
      "unit": "px",
      "default": 40
    }
  ],
  "blocks": [
    {
      "type": "featured_product",
      "name": "Featured Product",
      "settings": [
        {
          "type": "product",
          "id": "product",
          "label": "Product"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Product Grid",
      "settings": {
        "heading": "Featured Products",
        "products_count": 4
      }
    }
  ]
}
{% endschema %}
```

## Blocks Configuration

### Basic Blocks
```json
{
  "blocks": [
    {
      "type": "heading",
      "name": "Heading",
      "settings": [
        {
          "type": "text",
          "id": "text",
          "label": "Text",
          "default": "Heading"
        }
      ]
    },
    {
      "type": "paragraph",
      "name": "Paragraph",
      "settings": [
        {
          "type": "richtext",
          "id": "content",
          "label": "Content"
        }
      ]
    }
  ],
  "max_blocks": 10
}
```

### Accept All Theme Blocks
```json
{
  "blocks": [
    {
      "type": "@theme"
    }
  ]
}
```

### Accept App Blocks
```json
{
  "blocks": [
    {
      "type": "@app"
    }
  ]
}
```

## Presets

### Basic Preset
```json
{
  "presets": [
    {
      "name": "Hero Banner"
    }
  ]
}
```

### Preset with Default Settings
```json
{
  "presets": [
    {
      "name": "Product Grid",
      "settings": {
        "heading": "Featured Products",
        "products_count": 4,
        "columns_desktop": "4"
      }
    }
  ]
}
```

### Preset with Blocks
```json
{
  "presets": [
    {
      "name": "Testimonials",
      "blocks": [
        {
          "type": "testimonial"
        },
        {
          "type": "testimonial"
        },
        {
          "type": "testimonial"
        }
      ]
    }
  ]
}
```

## Best Practices

### 1. Group Related Settings with Headers
```json
{
  "settings": [
    {
      "type": "header",
      "content": "Content Settings"
    },
    {
      "type": "text",
      "id": "heading",
      "label": "Heading"
    },
    {
      "type": "header",
      "content": "Layout Settings"
    },
    {
      "type": "select",
      "id": "columns",
      "label": "Columns"
    }
  ]
}
```

### 2. Always Provide Defaults
```json
{
  "type": "text",
  "id": "heading",
  "label": "Heading",
  "default": "Default Heading"  ← Always provide!
}
```

### 3. Add Info Text for Complex Settings
```json
{
  "type": "range",
  "id": "products_count",
  "label": "Number of Products",
  "min": 2,
  "max": 12,
  "default": 4,
  "info": "Maximum number of products to display from the selected collection"
}
```

### 4. Use Appropriate Input Types
- Text/numbers → `text`, `textarea`, `number`, `range`
- True/false → `checkbox`
- Multiple options → `select`, `radio`
- Resources → `collection`, `product`, `image_picker`
- Colors → `color`, `color_background`

### 5. Set Reasonable Limits
```json
{
  "type": "range",
  "id": "padding",
  "min": 0,        ← Minimum value
  "max": 100,      ← Maximum value
  "step": 4,       ← Increment
  "default": 40    ← Sensible default
}
```

### 6. Include Presets for Quick Setup
```json
{
  "presets": [
    {
      "name": "Section Name",
      "settings": {
        "heading": "Default Heading",
        "show_feature": true
      },
      "blocks": [
        {
          "type": "block_type"
        }
      ]
    }
  ]
}
```

Create schemas that make section customization intuitive and efficient for merchants.
