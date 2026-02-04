---
name: eleventy
description: Build content-focused websites with Eleventy (11ty). Use when creating templates (.njk, .liquid), working with data cascade, collections, or deploying static sites.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Eleventy (11ty) Skill

Build fast, flexible static sites with Eleventy's zero-JS-by-default approach and powerful data cascade.

## Philosophy Alignment

Eleventy perfectly matches progressive enhancement principles:

| Principle | Eleventy Implementation |
|-----------|------------------------|
| HTML-first | Outputs pure static HTML |
| Zero JS by default | No JavaScript unless you add it |
| Template flexibility | Use any template language |
| Data-driven | Powerful data cascade system |

## Project Structure

```
src/
├── _includes/           # Layouts and partials
│   ├── layouts/
│   │   └── base.njk
│   └── partials/
│       └── header.njk
├── _data/               # Global data files
│   ├── site.json        # Site metadata
│   └── navigation.js    # Dynamic data
├── content/             # Content pages
│   ├── index.njk        # → /
│   ├── about.njk        # → /about/
│   └── blog/
│       ├── blog.json    # Directory data
│       └── post-1.md    # → /blog/post-1/
├── assets/
│   ├── css/
│   └── js/
└── eleventy.config.js   # Configuration
```

## Configuration

```javascript
// eleventy.config.js
export default function(eleventyConfig) {
  // Copy static assets
  eleventyConfig.addPassthroughCopy('src/assets');

  // Watch for changes
  eleventyConfig.addWatchTarget('src/assets/css/');

  // Add filters
  eleventyConfig.addFilter('dateFormat', (date, format) => {
    return new Intl.DateTimeFormat('en-US', {
      dateStyle: format || 'medium'
    }).format(date);
  });

  // Add shortcodes
  eleventyConfig.addShortcode('year', () => `${new Date().getFullYear()}`);

  // Add collections
  eleventyConfig.addCollection('posts', (collectionApi) => {
    return collectionApi
      .getFilteredByGlob('src/content/blog/*.md')
      .filter(post => !post.data.draft)
      .sort((a, b) => b.date - a.date);
  });

  return {
    dir: {
      input: 'src',
      output: '_site',
      includes: '_includes',
      data: '_data',
    },
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
  };
}
```

## Data Cascade

Data flows from global to specific, with later values overriding earlier:

```
1. Global Data (_data/*.json, _data/*.js)
2. Directory Data (blog/blog.json)
3. Template Front Matter
4. Computed Data
```

### Global Data

```json
// src/_data/site.json
{
  "title": "My Website",
  "description": "A website built with Eleventy",
  "url": "https://example.com",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  }
}
```

```javascript
// src/_data/navigation.js
export default [
  { text: 'Home', url: '/' },
  { text: 'About', url: '/about/' },
  { text: 'Blog', url: '/blog/' },
];
```

### Directory Data

Apply data to all files in a directory:

```json
// src/content/blog/blog.json
{
  "layout": "layouts/post.njk",
  "tags": ["posts"],
  "permalink": "/blog/{{ page.fileSlug }}/"
}
```

### Front Matter

```yaml
---
title: My Blog Post
description: A description of this post
date: 2024-01-15
tags:
  - javascript
  - tutorial
draft: false
---
```

## Template Languages

### Nunjucks (.njk)

Primary recommended template language:

```nunjucks
{# src/_includes/layouts/base.njk #}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="description" content="{{ description or site.description }}"/>
  <title>{{ title }} | {{ site.title }}</title>
  <link rel="stylesheet" href="/assets/css/main.css"/>
</head>
<body>
  {% include "partials/header.njk" %}

  <main>
    {{ content | safe }}
  </main>

  {% include "partials/footer.njk" %}
</body>
</html>
```

### Conditionals and Loops

```nunjucks
{# Conditionals #}
{% if featured %}
  <span class="badge">Featured</span>
{% endif %}

{% if posts.length %}
  <ul>
    {% for post in posts %}
      <li>
        <a href="{{ post.url }}">{{ post.data.title }}</a>
        <time datetime="{{ post.date | dateFormat }}">
          {{ post.date | dateFormat }}
        </time>
      </li>
    {% endfor %}
  </ul>
{% else %}
  <p>No posts yet.</p>
{% endif %}
```

### Macros (Reusable Components)

```nunjucks
{# src/_includes/macros/card.njk #}
{% macro card(title, href, description) %}
<article class="card">
  <h2><a href="{{ href }}">{{ title }}</a></h2>
  {% if description %}
    <p>{{ description }}</p>
  {% endif %}
</article>
{% endmacro %}

{# Usage #}
{% from "macros/card.njk" import card %}

{{ card(
  title="My Post",
  href="/blog/my-post/",
  description="A brief description"
) }}
```

## Collections

Group content for listing pages:

```javascript
// eleventy.config.js
eleventyConfig.addCollection('posts', (collectionApi) => {
  return collectionApi.getFilteredByGlob('src/content/blog/**/*.md');
});

// Tag-based collection (automatic)
// Any content with `tags: posts` in front matter
eleventyConfig.addCollection('posts', (collectionApi) => {
  return collectionApi.getFilteredByTag('posts');
});
```

### Using Collections

```nunjucks
{# List all posts #}
<ul>
{% for post in collections.posts %}
  <li>
    <a href="{{ post.url }}">{{ post.data.title }}</a>
  </li>
{% endfor %}
</ul>

{# Paginate posts #}
---
pagination:
  data: collections.posts
  size: 10
  alias: posts
---

{% for post in posts %}
  ...
{% endfor %}

{# Pagination navigation #}
{% if pagination.href.previous %}
  <a href="{{ pagination.href.previous }}">Previous</a>
{% endif %}
{% if pagination.href.next %}
  <a href="{{ pagination.href.next }}">Next</a>
{% endif %}
```

## Filters

Built-in and custom filters:

```javascript
// eleventy.config.js

// Date formatting
eleventyConfig.addFilter('dateFormat', (date, format = 'medium') => {
  return new Intl.DateTimeFormat('en-US', { dateStyle: format }).format(date);
});

// Reading time
eleventyConfig.addFilter('readingTime', (content) => {
  const words = content.split(/\s+/).length;
  const minutes = Math.ceil(words / 200);
  return `${minutes} min read`;
});

// Limit array
eleventyConfig.addFilter('limit', (arr, limit) => arr.slice(0, limit));

// Excerpt
eleventyConfig.addFilter('excerpt', (content, length = 200) => {
  const text = content.replace(/<[^>]+>/g, '');
  return text.length > length ? text.slice(0, length) + '...' : text;
});
```

```nunjucks
{# Usage #}
<time>{{ post.date | dateFormat('long') }}</time>
<span>{{ post.content | readingTime }}</span>
<p>{{ post.content | excerpt(150) }}</p>

{% for post in collections.posts | limit(5) %}
  ...
{% endfor %}
```

## Shortcodes

Reusable content snippets:

```javascript
// eleventy.config.js

// Simple shortcode
eleventyConfig.addShortcode('year', () => `${new Date().getFullYear()}`);

// Paired shortcode (with content)
eleventyConfig.addPairedShortcode('callout', (content, type = 'info') => {
  return `<aside class="callout callout--${type}">${content}</aside>`;
});

// Async shortcode (for fetching data)
eleventyConfig.addAsyncShortcode('image', async (src, alt) => {
  // Image optimization logic here
  return `<img src="${src}" alt="${alt}" loading="lazy"/>`;
});
```

```nunjucks
{# Usage #}
<p>Copyright {% year %}</p>

{% callout "warning" %}
  This is a warning message.
{% endcallout %}

{% image "hero.jpg", "A descriptive alt text" %}
```

## Permalinks

Control output URLs:

```yaml
---
# Static permalink
permalink: /custom-url/

# Dynamic permalink
permalink: /blog/{{ page.date | date: '%Y/%m' }}/{{ page.fileSlug }}/

# Disable output (data-only file)
permalink: false

# Multiple outputs (feeds)
permalink:
  - /feed.xml
  - /feed.json
---
```

## RSS Feed

```nunjucks
{# src/feed.njk #}
---
permalink: /feed.xml
eleventyExcludeFromCollections: true
---
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{{ site.title }}</title>
  <link href="{{ site.url }}/feed.xml" rel="self"/>
  <link href="{{ site.url }}/"/>
  <updated>{{ collections.posts[0].date | dateFormat }}</updated>
  <id>{{ site.url }}/</id>
  <author>
    <name>{{ site.author.name }}</name>
  </author>
  {% for post in collections.posts | limit(10) %}
  <entry>
    <title>{{ post.data.title }}</title>
    <link href="{{ site.url }}{{ post.url }}"/>
    <updated>{{ post.date | dateFormat }}</updated>
    <id>{{ site.url }}{{ post.url }}</id>
    <content type="html">{{ post.content | escape }}</content>
  </entry>
  {% endfor %}
</feed>
```

## Deployment

### Cloudflare Pages

```bash
# Build command
npx @11ty/eleventy

# Output directory
_site
```

### DigitalOcean App Platform

```yaml
# .do/app.yaml
name: my-eleventy-site
static_sites:
  - name: web
    source_dir: /
    build_command: npm run build
    output_dir: _site
```

## Checklist

Before deploying:

- [ ] Global data in `_data/` is complete
- [ ] Collections are properly configured
- [ ] Permalinks generate correct URLs
- [ ] RSS feed validates
- [ ] Images have alt text
- [ ] Build succeeds: `npx @11ty/eleventy`
- [ ] Output is correct in `_site/`

## Related Skills

- **xhtml-author** - HTML patterns for templates
- **markdown-author** - Content authoring
- **css-author** - Styling patterns
- **deployment** - Cloudflare and DigitalOcean
- **performance** - Static site optimization
