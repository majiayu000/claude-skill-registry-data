---
name: Shopify Section Patterns
description: Best practices for creating Shopify 2.0 sections with inline CSS and JavaScript
---

# Shopify Section Patterns

## Section Anatomy

A complete Shopify section consists of:
1. **Liquid markup** - HTML structure with dynamic content
2. **Inline CSS** - `{% stylesheet %}` tag (optional)
3. **Inline JavaScript** - `{% javascript %}` tag (optional)
4. **Schema** - `{% schema %}` JSON configuration

## Complete Section Template

```liquid
{%- comment -%}
  Section: [Name]
  Description: [Brief description]
  Usage: Add via Theme Editor
{%- endcomment -%}

{%- liquid
  assign heading = section.settings.heading | default: 'Default Heading'
  assign bg_color = section.settings.bg_color
  assign text_color = section.settings.text_color
-%}

<section
  id="section-{{ section.id }}"
  class="my-section"
  data-section-id="{{ section.id }}"
>
  <div class="container">
    {%- if heading != blank -%}
      <h2>{{ heading | escape }}</h2>
    {%- endif -%}

    {%- comment -%} Section content {%- endcomment -%}
  </div>
</section>

{% stylesheet %}
  #section-{{ section.id }} {
    padding: {{ section.settings.padding_top }}px 0 {{ section.settings.padding_bottom }}px;
    background-color: {{ bg_color }};
    color: {{ text_color }};
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  @media (min-width: 768px) {
    /* Tablet styles */
  }

  @media (min-width: 1024px) {
    /* Desktop styles */
  }
{% endstylesheet %}

{% javascript %}
  (function() {
    'use strict';

    function initSection(sectionId) {
      const section = document.querySelector('[data-section-id="' + sectionId + '"]');
      if (!section) return;

      // Your JavaScript here
    }

    // Initialize on page load
    document.addEventListener('DOMContentLoaded', function() {
      initSection('{{ section.id }}');
    });

    // Re-initialize when section reloads in theme editor
    document.addEventListener('shopify:section:load', function(event) {
      if (event.detail.sectionId === '{{ section.id }}') {
        initSection('{{ section.id }}');
      }
    });
  })();
{% endjavascript %}

{% schema %}
{
  "name": "Section Name",
  "tag": "section",
  "class": "section-wrapper",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Default Heading"
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
  "presets": [
    {
      "name": "Section Name"
    }
  ]
}
{% endschema %}
```

## When to Use Inline CSS/JS

### Use Inline `{% stylesheet %}` When:
- CSS needs Liquid variables: `{{ section.settings.color }}`
- Dynamic styles based on merchant settings
- Section-specific styles that don't need external file

### Use Inline `{% javascript %}` When:
- JS needs Liquid settings: `{{ section.settings.enable_feature }}`
- Section-specific functionality
- Need access to `{{ section.id }}` or other Liquid values

### Skip Inline Tags When:
- Styles/scripts are static and reusable
- Better to use theme.css or theme.js
- No Liquid variables needed

## Common Section Patterns

### 1. Product Grid Section

```liquid
{%- liquid
  assign collection = section.settings.collection
  assign products_count = section.settings.products_count
  assign columns = section.settings.columns_desktop
-%}

<div class="product-grid">
  {%- for product in collection.products limit: products_count -%}
    <div class="product-item">
      <a href="{{ product.url }}">
        {%- if product.featured_image -%}
          <img
            src="{{ product.featured_image | image_url: width: 400 }}"
            alt="{{ product.featured_image.alt | escape }}"
            loading="lazy"
          >
        {%- endif -%}

        <h3>{{ product.title | escape }}</h3>
        <p>{{ product.price | money }}</p>
      </a>
    </div>
  {%- endfor -%}
</div>

{% stylesheet %}
  .product-grid {
    display: grid;
    gap: 1.5rem;
    grid-template-columns: 1fr;
  }

  @media (min-width: 768px) {
    .product-grid {
      grid-template-columns: repeat({{ columns }}, 1fr);
    }
  }
{% endstylesheet %}
```

### 2. Hero Banner Section

```liquid
{%- liquid
  assign image = section.settings.image
  assign heading = section.settings.heading
  assign text = section.settings.text
  assign button_label = section.settings.button_label
  assign button_link = section.settings.button_link
-%}

<div class="hero-banner">
  {%- if image -%}
    <div class="hero-banner__image">
      <img
        src="{{ image | image_url: width: 1600 }}"
        alt="{{ image.alt | escape }}"
      >
    </div>
  {%- endif -%}

  <div class="hero-banner__content">
    {%- if heading != blank -%}
      <h1>{{ heading | escape }}</h1>
    {%- endif -%}

    {%- if text != blank -%}
      <p>{{ text }}</p>
    {%- endif -%}

    {%- if button_label != blank and button_link != blank -%}
      <a href="{{ button_link }}" class="button">
        {{ button_label | escape }}
      </a>
    {%- endif -%}
  </div>
</div>

{% stylesheet %}
  .hero-banner {
    position: relative;
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
  }

  .hero-banner__image {
    position: absolute;
    inset: 0;
    z-index: -1;
  }

  .hero-banner__image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .hero-banner__content {
    padding: 2rem;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
  }

  .button {
    display: inline-block;
    padding: 1rem 2rem;
    background: #000;
    color: #fff;
    text-decoration: none;
    border-radius: 4px;
    margin-top: 1rem;
  }
{% endstylesheet %}
```

### 3. Testimonials Section with Blocks

```liquid
<div class="testimonials">
  {%- for block in section.blocks -%}
    <div class="testimonial" {{ block.shopify_attributes }}>
      {%- if block.settings.quote != blank -%}
        <blockquote>
          {{ block.settings.quote }}
        </blockquote>
      {%- endif -%}

      {%- if block.settings.author != blank -%}
        <cite>{{ block.settings.author | escape }}</cite>
      {%- endif -%}
    </div>
  {%- endfor -%}
</div>

{% schema %}
{
  "name": "Testimonials",
  "blocks": [
    {
      "type": "testimonial",
      "name": "Testimonial",
      "settings": [
        {
          "type": "textarea",
          "id": "quote",
          "label": "Quote"
        },
        {
          "type": "text",
          "id": "author",
          "label": "Author"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Testimonials",
      "blocks": [
        {
          "type": "testimonial"
        }
      ]
    }
  ]
}
{% endschema %}
```

## Shopify Section Events

Handle theme editor events:

```javascript
{% javascript %}
  (function() {
    'use strict';

    function initSection(sectionId) {
      const section = document.querySelector('[data-section-id="' + sectionId + '"]');
      if (!section) return;

      console.log('Section initialized:', sectionId);
    }

    function cleanupSection(sectionId) {
      // Clean up event listeners, timers, etc.
      console.log('Section cleaned up:', sectionId);
    }

    // Load event - section added or page loaded
    document.addEventListener('shopify:section:load', function(event) {
      initSection(event.detail.sectionId);
    });

    // Unload event - section removed
    document.addEventListener('shopify:section:unload', function(event) {
      cleanupSection(event.detail.sectionId);
    });

    // Select event - section selected in theme editor
    document.addEventListener('shopify:section:select', function(event) {
      console.log('Section selected:', event.detail.sectionId);
    });

    // Deselect event - section deselected in theme editor
    document.addEventListener('shopify:section:deselect', function(event) {
      console.log('Section deselected:', event.detail.sectionId);
    });

    // Block select event - block selected in theme editor
    document.addEventListener('shopify:block:select', function(event) {
      console.log('Block selected:', event.detail.blockId);
    });

    // Block deselect event - block deselected in theme editor
    document.addEventListener('shopify:block:deselect', function(event) {
      console.log('Block deselected:', event.detail.blockId);
    });

    // Initialize on page load
    document.addEventListener('DOMContentLoaded', function() {
      initSection('{{ section.id }}');
    });
  })();
{% endjavascript %}
```

## Best Practices

### 1. Use Section ID for Unique Styling
```liquid
<div id="section-{{ section.id }}" class="my-section">
  <!-- Content -->
</div>

{% stylesheet %}
  #section-{{ section.id }} {
    /* Section-specific styles using Liquid variables */
    background: {{ section.settings.bg_color }};
  }

  .my-section {
    /* General styles without Liquid variables */
    padding: 2rem 0;
  }
{% endstylesheet %}
```

### 2. Provide Sensible Defaults
```liquid
{%- liquid
  assign heading = section.settings.heading | default: 'Default Heading'
  assign columns = section.settings.columns | default: 3
  assign show_prices = section.settings.show_prices | default: true
-%}
```

### 3. Handle Empty States
```liquid
{%- if collection.products.size > 0 -%}
  <!-- Show products -->
{%- else -%}
  <p>No products available in this collection.</p>
{%- endif -%}
```

### 4. Mobile-First Responsive
```css
/* Mobile first - base styles */
.grid {
  grid-template-columns: 1fr;
}

/* Tablet and up */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### 5. Use data- Attributes for JavaScript
```liquid
<div
  class="slider"
  data-autoplay="{{ section.settings.autoplay }}"
  data-speed="{{ section.settings.speed }}"
>
  <!-- Slider content -->
</div>

{% javascript %}
  const slider = document.querySelector('.slider');
  const autoplay = slider.dataset.autoplay === 'true';
  const speed = parseInt(slider.dataset.speed, 10);
{% endjavascript %}
```

## Common Patterns

### Conditional Classes
```liquid
<div class="card{% if product.available %} in-stock{% else %} sold-out{% endif %}">
  <!-- Card content -->
</div>
```

### Dynamic Grid Columns
```liquid
{% stylesheet %}
  .product-grid {
    display: grid;
    gap: 1.5rem;
    grid-template-columns: repeat({{ section.settings.columns_mobile }}, 1fr);
  }

  @media (min-width: 1024px) {
    .product-grid {
      grid-template-columns: repeat({{ section.settings.columns_desktop }}, 1fr);
    }
  }
{% endstylesheet %}
```

### Loading States
```javascript
{% javascript %}
  function addToCart(button) {
    button.classList.add('loading');
    button.disabled = true;

    // Add to cart logic...

    button.classList.remove('loading');
    button.disabled = false;
  }
{% endjavascript %}
```

Create sections that are flexible, performant, and easy for merchants to customize through the theme editor.
