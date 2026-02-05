---
name: Shopify i18n Basics
description: Internationalization fundamentals for multi-language Shopify themes
---

# Shopify i18n Basics

## Locale File Structure

Shopify themes use JSON files in the `locales/` directory:

```
locales/
├── en.default.json          # English (default language)
├── en.default.schema.json   # English schema translations
├── fr.json                  # French translations
├── fr.schema.json           # French schema translations
├── de.json                  # German translations
└── de.schema.json           # German schema translations
```

## File Types

### 1. Content Translations (en.default.json)

Used for theme content displayed to customers:

```json
{
  "general": {
    "search": "Search",
    "cart": "Cart",
    "menu": "Menu",
    "close": "Close",
    "loading": "Loading...",
    "continue_shopping": "Continue Shopping"
  },
  "product": {
    "add_to_cart": "Add to Cart",
    "sold_out": "Sold Out",
    "unavailable": "Unavailable",
    "price": "Price",
    "vendor": "Vendor"
  },
  "cart": {
    "title": "Your Cart",
    "empty": "Your cart is empty",
    "subtotal": "Subtotal",
    "checkout": "Checkout"
  }
}
```

### 2. Schema Translations (en.default.schema.json)

Used for Theme Editor labels:

```json
{
  "sections": {
    "featured_products": {
      "name": "Featured Products",
      "settings": {
        "heading": {
          "label": "Heading",
          "info": "Section heading text"
        },
        "collection": {
          "label": "Collection"
        }
      }
    }
  }
}
```

## Using Translations in Liquid

### Basic Translation
```liquid
{{ 'general.search' | t }}
{{ 'product.add_to_cart' | t }}
{{ 'cart.title' | t }}
```

### Translation with Variables
```liquid
{%- # In locale file -%}
{
  "cart": {
    "item_count": "{{ count }} items"
  }
}

{%- # In Liquid -%}
{{ 'cart.item_count' | t: count: cart.item_count }}
```

### Translation with HTML
```liquid
{%- # In locale file -%}
{
  "general": {
    "continue_html": "Continue <span>shopping</span>"
  }
}

{%- # In Liquid -%}
{{ 'general.continue_html' | t }}
```

### Translation in Schema
```liquid
{% schema %}
{
  "name": "t:sections.featured_products.name",
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "t:sections.featured_products.settings.heading.label"
    }
  ]
}
{% endschema %}
```

## Common Translation Patterns

### General UI
```json
{
  "general": {
    "search": "Search",
    "cart": "Cart",
    "menu": "Menu",
    "close": "Close",
    "loading": "Loading...",
    "buttons": {
      "learn_more": "Learn More",
      "shop_now": "Shop Now",
      "view_all": "View All"
    },
    "forms": {
      "submit": "Submit",
      "email": "Email",
      "name": "Name",
      "message": "Message"
    }
  }
}
```

### Product-Specific
```json
{
  "product": {
    "add_to_cart": "Add to Cart",
    "sold_out": "Sold Out",
    "unavailable": "Unavailable",
    "in_stock": "In Stock",
    "out_of_stock": "Out of Stock",
    "price": {
      "from": "From {{ price }}",
      "regular_price": "Regular price",
      "sale_price": "Sale price"
    }
  }
}
```

### Cart & Checkout
```json
{
  "cart": {
    "title": "Cart",
    "empty": "Your cart is empty",
    "item_count": "{{ count }} items",
    "subtotal": "Subtotal",
    "shipping": "Shipping",
    "total": "Total",
    "checkout": "Checkout",
    "remove": "Remove"
  }
}
```

### Forms & Errors
```json
{
  "forms": {
    "contact": {
      "name": "Name",
      "email": "Email",
      "message": "Message",
      "send": "Send Message",
      "success": "Thank you for your message!",
      "error": "Please correct the errors below"
    }
  },
  "errors": {
    "general": "An error occurred",
    "required_field": "This field is required",
    "invalid_email": "Please enter a valid email"
  }
}
```

## Adding New Languages

### Step 1: Create Translation Files

**locales/fr.json** (French content):
```json
{
  "general": {
    "search": "Rechercher",
    "cart": "Panier",
    "menu": "Menu",
    "close": "Fermer"
  },
  "product": {
    "add_to_cart": "Ajouter au panier",
    "sold_out": "Épuisé"
  },
  "cart": {
    "title": "Votre panier",
    "empty": "Votre panier est vide",
    "checkout": "Commander"
  }
}
```

**locales/fr.schema.json** (French schema):
```json
{
  "sections": {
    "featured_products": {
      "name": "Produits vedettes",
      "settings": {
        "heading": {
          "label": "Titre"
        },
        "collection": {
          "label": "Collection"
        }
      }
    }
  }
}
```

### Step 2: Use in Liquid

The `| t` filter automatically uses the correct translation based on the store's language:

```liquid
{%- # Automatically shows "Search" in English, "Rechercher" in French -%}
<button>{{ 'general.search' | t }}</button>
```

## Best Practices

### 1. Use Clear, Descriptive Keys
```json
{%- # Good -%}
{
  "product": {
    "add_to_cart": "Add to Cart"
  }
}

{%- # Bad -%}
{
  "prod": {
    "btn1": "Add to Cart"
  }
}
```

### 2. Organize Logically
```json
{
  "general": { ... },      # General UI
  "navigation": { ... },   # Navigation items
  "product": { ... },      # Product-related
  "cart": { ... },         # Cart-related
  "forms": { ... }         # Forms
}
```

### 3. Keep Keys Consistent Across Languages

**en.default.json**:
```json
{
  "product": {
    "add_to_cart": "Add to Cart"
  }
}
```

**fr.json** (same structure):
```json
{
  "product": {
    "add_to_cart": "Ajouter au panier"
  }
}
```

### 4. Use Nested Objects for Clarity
```json
{%- # Good -%}
{
  "forms": {
    "contact": {
      "name": "Name",
      "email": "Email"
    }
  }
}

{%- # Less clear -%}
{
  "forms": {
    "contact_name": "Name",
    "contact_email": "Email"
  }
}
```

### 5. Handle Pluralization

```json
{
  "cart": {
    "item_count_one": "{{ count }} item",
    "item_count_other": "{{ count }} items"
  }
}
```

```liquid
{% if cart.item_count == 1 %}
  {{ 'cart.item_count_one' | t: count: cart.item_count }}
{% else %}
  {{ 'cart.item_count_other' | t: count: cart.item_count }}
{% endif %}
```

### 6. Document Variables

```json
{
  "_comment": "{{ price }} will be replaced with the actual price",
  "product": {
    "from_price": "From {{ price }}"
  }
}
```

### 7. Avoid Hardcoding Text

```liquid
{%- # Bad -%}
<h2>Featured Products</h2>

{%- # Good -%}
<h2>{{ 'sections.featured_products.heading' | t }}</h2>
```

## Common Translation Keys

### Navigation
```json
{
  "navigation": {
    "home": "Home",
    "shop": "Shop",
    "collections": "Collections",
    "about": "About",
    "contact": "Contact"
  }
}
```

### Accessibility
```json
{
  "accessibility": {
    "skip_to_content": "Skip to content",
    "close_menu": "Close menu",
    "open_menu": "Open menu",
    "next_slide": "Next slide",
    "previous_slide": "Previous slide"
  }
}
```

### Date & Time
```json
{
  "date": {
    "months": {
      "january": "January",
      "february": "February"
    },
    "days": {
      "monday": "Monday",
      "tuesday": "Tuesday"
    }
  }
}
```

## Complete Example

**locales/en.default.json**:
```json
{
  "general": {
    "search": "Search",
    "cart": "Cart",
    "menu": "Menu"
  },
  "product": {
    "add_to_cart": "Add to Cart",
    "from_price": "From {{ price }}"
  },
  "cart": {
    "title": "Your Cart",
    "empty": "Your cart is empty"
  }
}
```

**sections/featured-products.liquid**:
```liquid
<section>
  <h2>{{ 'sections.featured_products.heading' | t }}</h2>

  {%- for product in collection.products -%}
    <div>
      <h3>{{ product.title }}</h3>
      <p>{{ 'product.from_price' | t: price: product.price | money }}</p>
      <button>{{ 'product.add_to_cart' | t }}</button>
    </div>
  {%- endfor -%}
</section>
```

Use translation keys consistently to create themes that work seamlessly in multiple languages.
