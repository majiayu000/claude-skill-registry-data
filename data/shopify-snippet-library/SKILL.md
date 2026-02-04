---
name: Shopify Snippet Library
description: Reusable Liquid snippet patterns with proper documentation and parameter handling
---

# Shopify Snippet Library

## Snippet Documentation Format

All snippets should include documentation using Liquid comments:

```liquid
{% comment %}
  Snippet: [Name]
  Description: [What this snippet does]

  Parameters:
  - param_name {type} - Description [required/optional]

  Usage:
  {% render 'snippet-name', param_name: value %}

  Example:
  {% render 'product-card', product: product, show_vendor: true %}
{% endcomment %}
```

## Common Snippet Patterns

### 1. Product Card

```liquid
{% comment %}
  Snippet: Product Card
  Description: Displays a product with image, title, vendor, and price

  Parameters:
  - product {product} - The product object [required]
  - show_vendor {boolean} - Show product vendor (default: false) [optional]
  - image_size {number} - Image width in pixels (default: 400) [optional]
  - class {string} - Additional CSS classes [optional]

  Usage:
  {% render 'product-card', product: product, show_vendor: true, image_size: 600 %}
{% endcomment %}

{%- liquid
  assign show_vendor = show_vendor | default: false
  assign image_size = image_size | default: 400
-%}

{%- if product == blank -%}
  <div class="product-card product-card--empty {{ class }}">
    <p>Product not available</p>
  </div>
{%- else -%}
  <article class="product-card {{ class }}">
    <a href="{{ product.url }}" class="product-card__link">
      {%- if product.featured_image -%}
        <div class="product-card__image">
          <img
            src="{{ product.featured_image | image_url: width: image_size }}"
            alt="{{ product.featured_image.alt | escape }}"
            loading="lazy"
            width="{{ image_size }}"
            height="{{ image_size | divided_by: product.featured_image.aspect_ratio | ceil }}"
          >
        </div>
      {%- endif -%}

      <div class="product-card__info">
        {%- if show_vendor and product.vendor != blank -%}
          <p class="product-card__vendor">{{ product.vendor | escape }}</p>
        {%- endif -%}

        <h3 class="product-card__title">{{ product.title | escape }}</h3>

        <div class="product-card__price">
          {%- if product.compare_at_price > product.price -%}
            <span class="product-card__price--sale">{{ product.price | money }}</span>
            <span class="product-card__price--compare">{{ product.compare_at_price | money }}</span>
          {%- else -%}
            <span>{{ product.price | money }}</span>
          {%- endif -%}
        </div>
      </div>
    </a>
  </article>
{%- endif -%}
```

### 2. Button / Link

```liquid
{% comment %}
  Snippet: Button
  Description: Renders a customizable button or link

  Parameters:
  - text {string} - Button text [required]
  - url {string} - Button URL (makes it a link) [optional]
  - style {string} - Button style: 'primary', 'secondary', 'outline' (default: 'primary') [optional]
  - size {string} - Button size: 'small', 'medium', 'large' (default: 'medium') [optional]
  - class {string} - Additional CSS classes [optional]

  Usage:
  {% render 'button', text: 'Add to Cart', style: 'primary', size: 'large' %}
  {% render 'button', text: 'Learn More', url: '/pages/about', style: 'outline' %}
{% endcomment %}

{%- liquid
  assign style = style | default: 'primary'
  assign size = size | default: 'medium'
  assign btn_class = 'btn btn--' | append: style | append: ' btn--' | append: size
  if class
    assign btn_class = btn_class | append: ' ' | append: class
  endif
-%}

{%- if url != blank -%}
  <a href="{{ url }}" class="{{ btn_class }}">
    {{ text | escape }}
  </a>
{%- else -%}
  <button type="button" class="{{ btn_class }}">
    {{ text | escape }}
  </button>
{%- endif -%}
```

### 3. Icon (SVG)

```liquid
{% comment %}
  Snippet: Icon
  Description: Renders an SVG icon

  Parameters:
  - name {string} - Icon name (e.g., 'cart', 'heart', 'search') [required]
  - size {number} - Icon size in pixels (default: 24) [optional]
  - class {string} - Additional CSS classes [optional]

  Usage:
  {% render 'icon', name: 'cart', size: 20, class: 'icon-primary' %}
{% endcomment %}

{%- liquid
  assign size = size | default: 24
  assign icon_class = 'icon icon-' | append: name
  if class
    assign icon_class = icon_class | append: ' ' | append: class
  endif
-%}

<svg class="{{ icon_class }}" width="{{ size }}" height="{{ size }}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  {%- case name -%}
    {%- when 'cart' -%}
      <path d="M9 2L8 4H4C2.9 4 2 4.9 2 6V18C2 19.1 2.9 20 4 20H20C21.1 20 22 19.1 22 18V6C22 4.9 21.1 4 20 4H16L15 2H9Z" stroke="currentColor" stroke-width="2"/>
    {%- when 'heart' -%}
      <path d="M20.84 4.61C19.91 3.68 18.69 3.17 17.42 3.17C16.15 3.17 14.93 3.68 14 4.61L12 6.61L10 4.61C9.07 3.68 7.85 3.17 6.58 3.17C5.31 3.17 4.09 3.68 3.16 4.61C1.22 6.55 1.22 9.69 3.16 11.63L12 20.47L20.84 11.63C22.78 9.69 22.78 6.55 20.84 4.61Z" stroke="currentColor" stroke-width="2"/>
    {%- when 'search' -%}
      <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
      <path d="M21 21L16.65 16.65" stroke="currentColor" stroke-width="2"/>
    {%- when 'close' -%}
      <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2"/>
    {%- else -%}
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
  {%- endcase -%}
</svg>
```

### 4. Form Input

```liquid
{% comment %}
  Snippet: Form Input
  Description: Renders a form input field with label

  Parameters:
  - type {string} - Input type (text, email, tel, number, etc.) [required]
  - name {string} - Input name attribute [required]
  - label {string} - Input label [required]
  - required {boolean} - Make field required (default: false) [optional]
  - placeholder {string} - Placeholder text [optional]
  - value {string} - Default value [optional]
  - class {string} - Additional CSS classes [optional]

  Usage:
  {% render 'form-input', type: 'email', name: 'email', label: 'Email Address', required: true %}
{% endcomment %}

{%- liquid
  assign required = required | default: false
  assign input_id = 'input-' | append: name
-%}

<div class="form-field {{ class }}">
  <label for="{{ input_id }}" class="form-field__label">
    {{ label | escape }}
    {%- if required -%}
      <span class="form-field__required" aria-label="required">*</span>
    {%- endif -%}
  </label>

  <input
    type="{{ type }}"
    id="{{ input_id }}"
    name="{{ name }}"
    class="form-field__input"
    {%- if placeholder -%}placeholder="{{ placeholder | escape }}"{%- endif -%}
    {%- if value -%}value="{{ value | escape }}"{%- endif -%}
    {%- if required -%}required{%- endif -%}
    {%- if type == 'email' -%}autocomplete="email"{%- endif -%}
  >
</div>
```

### 5. Image with Fallback

```liquid
{% comment %}
  Snippet: Responsive Image
  Description: Renders a responsive image with fallback

  Parameters:
  - image {image} - The image object [required]
  - width {number} - Image width (default: 800) [optional]
  - height {number} - Image height [optional]
  - alt {string} - Alt text (uses image.alt if not provided) [optional]
  - class {string} - Additional CSS classes [optional]
  - loading {string} - Loading attribute: 'lazy' or 'eager' (default: 'lazy') [optional]

  Usage:
  {% render 'image', image: product.featured_image, width: 600, alt: product.title %}
{% endcomment %}

{%- liquid
  assign width = width | default: 800
  assign loading = loading | default: 'lazy'
  assign alt_text = alt | default: image.alt
-%}

{%- if image != blank -%}
  {%- if height -%}
    <img
      src="{{ image | image_url: width: width, height: height }}"
      alt="{{ alt_text | escape }}"
      width="{{ width }}"
      height="{{ height }}"
      loading="{{ loading }}"
      class="{{ class }}"
    >
  {%- else -%}
    <img
      srcset="
        {{ image | image_url: width: 400 }} 400w,
        {{ image | image_url: width: 800 }} 800w,
        {{ image | image_url: width: 1200 }} 1200w
      "
      sizes="(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw"
      src="{{ image | image_url: width: width }}"
      alt="{{ alt_text | escape }}"
      width="{{ width }}"
      height="{{ width | divided_by: image.aspect_ratio | ceil }}"
      loading="{{ loading }}"
      class="{{ class }}"
    >
  {%- endif -%}
{%- else -%}
  <div class="image-placeholder {{ class }}" role="img" aria-label="No image available"></div>
{%- endif -%}
```

### 6. Price Display

```liquid
{% comment %}
  Snippet: Price
  Description: Displays product price with sale indication

  Parameters:
  - product {product} - The product object [required]
  - show_compare {boolean} - Show compare at price (default: true) [optional]
  - class {string} - Additional CSS classes [optional]

  Usage:
  {% render 'price', product: product %}
  {% render 'price', product: product, show_compare: false %}
{% endcomment %}

{%- liquid
  assign show_compare = show_compare | default: true
  assign on_sale = false
  if product.compare_at_price > product.price
    assign on_sale = true
  endif
-%}

<div class="price {{ class }}{% if on_sale %} price--on-sale{% endif %}">
  {%- if on_sale -%}
    <span class="price__sale">{{ product.price | money }}</span>
    {%- if show_compare -%}
      <span class="price__compare">{{ product.compare_at_price | money }}</span>
    {%- endif -%}
  {%- else -%}
    <span class="price__regular">{{ product.price | money }}</span>
  {%- endif -%}
</div>
```

### 7. Badge / Tag

```liquid
{% comment %}
  Snippet: Badge
  Description: Displays a badge or tag

  Parameters:
  - text {string} - Badge text [required]
  - style {string} - Badge style: 'sale', 'new', 'featured', 'default' (default: 'default') [optional]
  - class {string} - Additional CSS classes [optional]

  Usage:
  {% render 'badge', text: 'Sale', style: 'sale' %}
  {% render 'badge', text: 'New Arrival', style: 'new' %}
{% endcomment %}

{%- liquid
  assign style = style | default: 'default'
  assign badge_class = 'badge badge--' | append: style
  if class
    assign badge_class = badge_class | append: ' ' | append: class
  endif
-%}

{%- if text != blank -%}
  <span class="{{ badge_class }}">
    {{ text | escape }}
  </span>
{%- endif -%}
```

### 8. Loading Spinner

```liquid
{% comment %}
  Snippet: Loading Spinner
  Description: Displays a loading spinner

  Parameters:
  - size {string} - Spinner size: 'small', 'medium', 'large' (default: 'medium') [optional]
  - class {string} - Additional CSS classes [optional]

  Usage:
  {% render 'loading-spinner', size: 'large' %}
{% endcomment %}

{%- liquid
  assign size = size | default: 'medium'
  assign spinner_class = 'spinner spinner--' | append: size
  if class
    assign spinner_class = spinner_class | append: ' ' | append: class
  endif
-%}

<div class="{{ spinner_class }}" role="status" aria-label="Loading">
  <svg class="spinner__svg" viewBox="0 0 50 50">
    <circle class="spinner__circle" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
  </svg>
  <span class="sr-only">Loading...</span>
</div>
```

## Best Practices

### 1. Always Document Parameters
```liquid
{% comment %}
  Parameters:
  - param {type} - Description [required/optional]
{% endcomment %}
```

### 2. Provide Defaults
```liquid
{%- liquid
  assign show_vendor = show_vendor | default: false
  assign image_size = image_size | default: 400
-%}
```

### 3. Validate Required Parameters
```liquid
{%- if product == blank -%}
  <p class="error">Product parameter is required</p>
  {%- return -%}
{%- endif -%}
```

### 4. Handle Empty States
```liquid
{%- if image != blank -%}
  <!-- Image markup -->
{%- else -%}
  <div class="placeholder">No image available</div>
{%- endif -%}
```

### 5. Escape User-Provided Content
```liquid
<h3>{{ product.title | escape }}</h3>
<p>{{ customer.name | escape }}</p>
```

### 6. Use Semantic HTML
```liquid
<article>  {%- # For products -%}
<nav>      {%- # For navigation -%}
<aside>    {%- # For sidebars -%}
<section>  {%- # For content sections -%}
```

### 7. Include Accessibility Attributes
```liquid
<button aria-label="Add {{ product.title | escape }} to cart">
  Add to Cart
</button>

<img src="..." alt="{{ image.alt | escape }}">

<div role="status" aria-live="polite">
  Item added to cart
</div>
```

Create well-documented, reusable snippets that are easy to understand and maintain.
