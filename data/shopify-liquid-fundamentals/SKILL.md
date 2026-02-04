---
name: Shopify Liquid Fundamentals
description: Core Shopify Liquid templating best practices for performance, maintainability, and clean code
---

# Shopify Liquid Fundamentals

## Core Principles

### Whitespace Control
- Use `{%- -%}` to trim whitespace around Liquid tags
- Prefer `{% render %}` over deprecated `{% include %}`
- Use `{% liquid %}` for multi-line logic blocks

**Example:**
```liquid
{%- liquid
  assign product_available = product.available | default: false
  assign product_price = product.price | default: 0

  if product == blank
    assign error_message = 'Product not found'
  endif
-%}
```

### Performance Optimization
- Minimize Liquid logic in templates
- Use `assign` for complex calculations instead of inline logic
- Cache expensive operations
- Use snippets for reusable code

**Good:**
```liquid
{%- assign discounted_price = product.price | times: 0.9 | money -%}
<p>Sale: {{ discounted_price }}</p>
```

**Bad:**
```liquid
<p>Sale: {{ product.price | times: 0.9 | money }}</p>
<p>Save: {{ product.price | times: 0.1 | money }}</p>
```

### Error Handling
Always provide defaults and handle empty states:

```liquid
{%- liquid
  assign heading = section.settings.heading | default: 'Default Heading'
  assign show_vendor = section.settings.show_vendor | default: false

  if product == blank
    assign error_message = 'Product unavailable'
  endif
-%}

{%- if error_message -%}
  <p class="error">{{ error_message }}</p>
{%- else -%}
  <!-- Normal content -->
{%- endif -%}
```

## Liquid Syntax Essentials

### Output
```liquid
{{ variable }}              # Output variable
{{ variable | escape }}     # Escape HTML
{{ variable | default: 'fallback' }}  # Provide default
{{- variable -}}            # Trim whitespace
```

### Logic
```liquid
{% if condition %}
{% elsif other_condition %}
{% else %}
{% endif %}

{% unless condition %}
{% endunless %}

{% case variable %}
  {% when 'value1' %}
  {% when 'value2' %}
  {% else %}
{% endcase %}
```

### Loops
```liquid
{% for item in collection %}
  {{ item.title }}
{% endfor %}

{% for item in collection limit: 4 %}
  {{ item.title }}
{% endfor %}

{% for i in (1..5) %}
  Item {{ i }}
{% endfor %}
```

### Variables
```liquid
{% assign name = 'value' %}
{% capture variable %}
  Content here
{% endcapture %}
```

## Common Filters

### String Filters
```liquid
{{ 'hello' | capitalize }}           # Hello
{{ 'HELLO' | downcase }}            # hello
{{ 'hello' | upcase }}              # HELLO
{{ 'hello world' | truncate: 8 }}   # hello...
{{ '<p>test</p>' | escape }}        # &lt;p&gt;test&lt;/p&gt;
{{ 'hello world' | remove: 'world' }} # hello
{{ 'hello' | append: ' world' }}    # hello world
```

### Array Filters
```liquid
{{ collection | size }}              # Number of items
{{ collection | first }}             # First item
{{ collection | last }}              # Last item
{{ collection | join: ', ' }}        # Join with comma
{{ collection | reverse }}           # Reverse order
{{ collection | sort: 'title' }}     # Sort by property
```

### Math Filters
```liquid
{{ 10 | plus: 5 }}                  # 15
{{ 10 | minus: 5 }}                 # 5
{{ 10 | times: 5 }}                 # 50
{{ 10 | divided_by: 5 }}            # 2
{{ 10.5 | ceil }}                   # 11
{{ 10.5 | floor }}                  # 10
{{ 10.5 | round }}                  # 11
```

### Money Filters
```liquid
{{ 1000 | money }}                  # $10.00
{{ 1000 | money_with_currency }}    # $10.00 USD
{{ 1000 | money_without_currency }} # 10.00
```

### Image Filters
```liquid
{{ image | image_url: width: 400 }}
{{ image | image_url: width: 400, height: 400 }}
{{ image | image_tag }}
{{ image | image_tag: alt: 'Description' }}
```

## Shopify Objects

### Global Objects
```liquid
{{ shop.name }}                     # Store name
{{ shop.email }}                    # Store email
{{ cart.item_count }}               # Cart items
{{ customer.name }}                 # Customer name (if logged in)
{{ settings.color_primary }}        # Theme setting
```

### Product Objects
```liquid
{{ product.title }}
{{ product.price }}
{{ product.compare_at_price }}
{{ product.available }}
{{ product.vendor }}
{{ product.type }}
{{ product.featured_image }}
{{ product.url }}
```

### Collection Objects
```liquid
{{ collection.title }}
{{ collection.description }}
{{ collection.products }}
{{ collection.products_count }}
{{ collection.url }}
```

## Best Practices

### 1. Always Escape User Input
```liquid
<h1>{{ product.title | escape }}</h1>
<p>{{ customer.name | escape }}</p>
```

### 2. Provide Defaults
```liquid
{%- assign heading = section.settings.heading | default: 'Default Title' -%}
{%- assign image = product.featured_image | default: blank -%}
```

### 3. Check for Blank Values
```liquid
{%- if heading != blank -%}
  <h2>{{ heading | escape }}</h2>
{%- endif -%}
```

### 4. Use Liquid Tag for Multi-line Logic
```liquid
{%- liquid
  assign is_sale = false
  if product.compare_at_price > product.price
    assign is_sale = true
  endif

  assign discount_percent = product.compare_at_price | minus: product.price | times: 100 | divided_by: product.compare_at_price
-%}
```

### 5. Minimize Nested Conditions
```liquid
{%- # Bad -%}
{% if product.available %}
  {% if product.compare_at_price > product.price %}
    <span>On Sale</span>
  {% endif %}
{% endif %}

{%- # Good -%}
{%- liquid
  assign is_on_sale = false
  if product.available and product.compare_at_price > product.price
    assign is_on_sale = true
  endif
-%}

{%- if is_on_sale -%}
  <span>On Sale</span>
{%- endif -%}
```

## Common Patterns

### Conditional Class Names
```liquid
<div class="product{% if product.available %} in-stock{% else %} out-of-stock{% endif %}">
  <!-- Content -->
</div>
```

### Loop with Index
```liquid
{%- for product in collection.products -%}
  <div class="product-{{ forloop.index }}">
    {%- if forloop.first -%}
      <span>Featured</span>
    {%- endif -%}
    {{ product.title }}
  </div>
{%- endfor -%}
```

### Empty State Handling
```liquid
{%- if collection.products.size > 0 -%}
  {%- for product in collection.products -%}
    <!-- Product markup -->
  {%- endfor -%}
{%- else -%}
  <p>No products available.</p>
{%- endif -%}
```

### Responsive Images
```liquid
{%- if product.featured_image -%}
  <img
    srcset="
      {{ product.featured_image | image_url: width: 400 }} 400w,
      {{ product.featured_image | image_url: width: 800 }} 800w,
      {{ product.featured_image | image_url: width: 1200 }} 1200w
    "
    sizes="(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw"
    src="{{ product.featured_image | image_url: width: 800 }}"
    alt="{{ product.featured_image.alt | escape }}"
    loading="lazy"
    width="800"
    height="{{ 800 | divided_by: product.featured_image.aspect_ratio | ceil }}"
  >
{%- endif -%}
```

## Rendering Snippets

### Basic Rendering
```liquid
{% render 'product-card' %}
```

### With Parameters
```liquid
{% render 'product-card', product: product, show_vendor: true %}
```

### With Multiple Parameters
```liquid
{% render 'button',
  text: 'Add to Cart',
  url: product.url,
  style: 'primary',
  size: 'large'
%}
```

## Performance Tips

1. **Limit loops** - Use `limit` parameter when possible
2. **Cache expensive operations** - Assign to variables
3. **Minimize API calls** - Don't call same object property multiple times
4. **Use snippets wisely** - Balance between reusability and overhead
5. **Optimize images** - Use appropriate sizes with image filters

## Common Mistakes to Avoid

❌ **Don't repeat expensive operations:**
```liquid
<p>{{ product.price | times: 1.1 | money }}</p>
<p>{{ product.price | times: 1.1 | money }}</p>
```

✅ **Do assign to variable:**
```liquid
{%- assign price_with_tax = product.price | times: 1.1 | money -%}
<p>{{ price_with_tax }}</p>
<p>{{ price_with_tax }}</p>
```

❌ **Don't forget to escape:**
```liquid
<h1>{{ product.title }}</h1>
```

✅ **Do escape user input:**
```liquid
<h1>{{ product.title | escape }}</h1>
```

❌ **Don't use deprecated include:**
```liquid
{% include 'snippet-name' %}
```

✅ **Do use render:**
```liquid
{% render 'snippet-name' %}
```

Follow these fundamentals for clean, performant, maintainable Shopify Liquid code.
