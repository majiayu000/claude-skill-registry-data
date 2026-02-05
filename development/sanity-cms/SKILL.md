---
name: sanity-cms
description: Integrate Sanity headless CMS for content management. Use when building content-driven sites with structured content, requiring an editor UI, or needing real-time previews.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Sanity CMS Skill

Integrate Sanity headless CMS for structured content management.

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Sanity Studio  │────▶│   Sanity API    │◀────│   Your Site     │
│  (Editor UI)    │     │   (Content DB)  │     │  (Astro/11ty)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
     Editors                 Hosted              Build-time fetch
```

## Project Setup

### Initialize Sanity

```bash
# Create new Sanity project
npm create sanity@latest -- --project-name my-project --dataset production

# Or add to existing project
npm install sanity @sanity/client
```

### Project Structure

```
project/
├── sanity/                 # Sanity Studio
│   ├── schemas/            # Content schemas
│   │   ├── index.js
│   │   ├── post.js
│   │   └── author.js
│   ├── sanity.config.js    # Studio config
│   └── sanity.cli.js       # CLI config
├── src/                    # Your site
│   └── lib/
│       └── sanity.js       # Client setup
└── package.json
```

## Schema Definition

### Basic Document Schema

```javascript
// sanity/schemas/post.js
export default {
  name: 'post',
  title: 'Blog Post',
  type: 'document',
  fields: [
    {
      name: 'title',
      title: 'Title',
      type: 'string',
      validation: (Rule) => Rule.required().max(100),
    },
    {
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      options: {
        source: 'title',
        maxLength: 96,
      },
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'publishedAt',
      title: 'Published At',
      type: 'datetime',
    },
    {
      name: 'author',
      title: 'Author',
      type: 'reference',
      to: [{ type: 'author' }],
    },
    {
      name: 'mainImage',
      title: 'Main Image',
      type: 'image',
      options: {
        hotspot: true,
      },
      fields: [
        {
          name: 'alt',
          title: 'Alt Text',
          type: 'string',
          validation: (Rule) => Rule.required(),
        },
      ],
    },
    {
      name: 'body',
      title: 'Body',
      type: 'array',
      of: [
        { type: 'block' },
        { type: 'image' },
        { type: 'code' },
      ],
    },
    {
      name: 'tags',
      title: 'Tags',
      type: 'array',
      of: [{ type: 'string' }],
      options: {
        layout: 'tags',
      },
    },
  ],
  preview: {
    select: {
      title: 'title',
      author: 'author.name',
      media: 'mainImage',
    },
    prepare({ title, author, media }) {
      return {
        title,
        subtitle: author ? `by ${author}` : '',
        media,
      };
    },
  },
};
```

### Author Schema

```javascript
// sanity/schemas/author.js
export default {
  name: 'author',
  title: 'Author',
  type: 'document',
  fields: [
    {
      name: 'name',
      title: 'Name',
      type: 'string',
      validation: (Rule) => Rule.required(),
    },
    {
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      options: { source: 'name' },
    },
    {
      name: 'image',
      title: 'Image',
      type: 'image',
    },
    {
      name: 'bio',
      title: 'Bio',
      type: 'text',
    },
  ],
};
```

### Register Schemas

```javascript
// sanity/schemas/index.js
import post from './post';
import author from './author';

export const schemaTypes = [post, author];
```

```javascript
// sanity/sanity.config.js
import { defineConfig } from 'sanity';
import { deskTool } from 'sanity/desk';
import { schemaTypes } from './schemas';

export default defineConfig({
  name: 'default',
  title: 'My Project',
  projectId: 'your-project-id',
  dataset: 'production',
  plugins: [deskTool()],
  schema: {
    types: schemaTypes,
  },
});
```

## Client Setup

### Sanity Client

```javascript
// src/lib/sanity.js
import { createClient } from '@sanity/client';

export const client = createClient({
  projectId: 'your-project-id',
  dataset: 'production',
  apiVersion: '2024-01-01',
  useCdn: true, // Use CDN for production
});

// For preview/draft content
export const previewClient = createClient({
  projectId: 'your-project-id',
  dataset: 'production',
  apiVersion: '2024-01-01',
  useCdn: false,
  token: process.env.SANITY_TOKEN, // Read token for drafts
});
```

### Environment Variables

```bash
# .env
SANITY_PROJECT_ID=your-project-id
SANITY_DATASET=production
SANITY_TOKEN=your-read-token  # For previews only
```

## GROQ Queries

### Basic Queries

```javascript
// Fetch all published posts
const posts = await client.fetch(`
  *[_type == "post" && !(_id in path("drafts.**"))] | order(publishedAt desc) {
    _id,
    title,
    "slug": slug.current,
    publishedAt,
    "author": author->name,
    "mainImage": mainImage.asset->url
  }
`);

// Fetch single post by slug
const post = await client.fetch(`
  *[_type == "post" && slug.current == $slug][0] {
    _id,
    title,
    body,
    publishedAt,
    "author": author->{name, image, bio},
    mainImage {
      asset->{url, metadata},
      alt
    }
  }
`, { slug: 'my-post-slug' });
```

### Common Query Patterns

```javascript
// Pagination
const page = 1;
const perPage = 10;
const posts = await client.fetch(`
  *[_type == "post"] | order(publishedAt desc) [$start...$end] {
    title,
    "slug": slug.current
  }
`, {
  start: (page - 1) * perPage,
  end: page * perPage,
});

// Filter by reference
const authorPosts = await client.fetch(`
  *[_type == "post" && author._ref == $authorId] {
    title,
    "slug": slug.current
  }
`, { authorId: 'author-id-here' });

// Search
const results = await client.fetch(`
  *[_type == "post" && title match $query] {
    title,
    "slug": slug.current
  }
`, { query: '*search*' });

// Count
const count = await client.fetch(`count(*[_type == "post"])`);
```

## Astro Integration

### Setup

```bash
npm install @sanity/astro @sanity/image-url
```

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import sanity from '@sanity/astro';

export default defineConfig({
  integrations: [
    sanity({
      projectId: 'your-project-id',
      dataset: 'production',
      useCdn: true,
    }),
  ],
});
```

### Fetching in Astro

```astro
---
// src/pages/blog/index.astro
import { sanityClient } from 'sanity:client';

const posts = await sanityClient.fetch(`
  *[_type == "post"] | order(publishedAt desc) {
    _id,
    title,
    "slug": slug.current,
    publishedAt
  }
`);
---

<ul>
  {posts.map((post) => (
    <li>
      <a href={`/blog/${post.slug}`}>{post.title}</a>
    </li>
  ))}
</ul>
```

### Dynamic Routes

```astro
---
// src/pages/blog/[slug].astro
import { sanityClient } from 'sanity:client';

export async function getStaticPaths() {
  const posts = await sanityClient.fetch(`
    *[_type == "post"] { "slug": slug.current }
  `);

  return posts.map((post) => ({
    params: { slug: post.slug },
  }));
}

const { slug } = Astro.params;

const post = await sanityClient.fetch(`
  *[_type == "post" && slug.current == $slug][0] {
    title,
    body,
    publishedAt
  }
`, { slug });
---

<article>
  <h1>{post.title}</h1>
  <!-- Render body -->
</article>
```

## 11ty Integration

### Data File

```javascript
// src/_data/posts.js
import { createClient } from '@sanity/client';

const client = createClient({
  projectId: process.env.SANITY_PROJECT_ID,
  dataset: 'production',
  apiVersion: '2024-01-01',
  useCdn: true,
});

export default async function() {
  return client.fetch(`
    *[_type == "post"] | order(publishedAt desc) {
      _id,
      title,
      "slug": slug.current,
      publishedAt,
      body
    }
  `);
}
```

### Template

```nunjucks
{# src/blog.njk #}
---
pagination:
  data: posts
  size: 1
  alias: post
permalink: /blog/{{ post.slug }}/
---

<article>
  <h1>{{ post.title }}</h1>
  <time>{{ post.publishedAt | dateFormat }}</time>
  <!-- Render body -->
</article>
```

## Image Handling

### Image URL Builder

```javascript
// src/lib/image.js
import imageUrlBuilder from '@sanity/image-url';
import { client } from './sanity.js';

const builder = imageUrlBuilder(client);

export function urlFor(source) {
  return builder.image(source);
}
```

### Usage

```javascript
import { urlFor } from '../lib/image.js';

// Get URL with transformations
const imageUrl = urlFor(post.mainImage)
  .width(800)
  .height(600)
  .format('webp')
  .url();

// Responsive images
const srcset = [400, 800, 1200]
  .map((w) => `${urlFor(post.mainImage).width(w).url()} ${w}w`)
  .join(', ');
```

## Portable Text (Rich Content)

### Rendering in Astro

```astro
---
import { PortableText } from '@portabletext/react';

const components = {
  types: {
    image: ({ value }) => (
      <img src={urlFor(value).width(800).url()} alt={value.alt} />
    ),
    code: ({ value }) => (
      <pre><code class={`language-${value.language}`}>{value.code}</code></pre>
    ),
  },
  marks: {
    link: ({ children, value }) => (
      <a href={value.href} target="_blank" rel="noopener">{children}</a>
    ),
  },
};
---

<PortableText value={post.body} components={components} />
```

## Preview Mode

### Astro Preview

```javascript
// src/pages/api/preview.js
export async function GET({ request, cookies }) {
  const url = new URL(request.url);
  const secret = url.searchParams.get('secret');
  const slug = url.searchParams.get('slug');

  if (secret !== process.env.PREVIEW_SECRET) {
    return new Response('Invalid secret', { status: 401 });
  }

  cookies.set('preview', 'true', { path: '/' });

  return Response.redirect(`/blog/${slug}`);
}
```

## Deployment

### Studio Hosting

```bash
# Deploy Sanity Studio
cd sanity
npx sanity deploy
```

### API Configuration

1. Go to sanity.io/manage
2. Add CORS origins for your site
3. Create API token for previews (read-only)

## Checklist

When integrating Sanity:

- [ ] Schemas define all content types
- [ ] Validation rules on required fields
- [ ] Client uses CDN in production
- [ ] Environment variables configured
- [ ] CORS origins set in Sanity dashboard
- [ ] Images use URL builder
- [ ] Portable Text has custom components
- [ ] Preview mode works (if needed)

## Related Skills

- **astro** - Astro integration patterns
- **eleventy** - 11ty data file patterns
- **env-config** - Environment variables
- **deployment** - Deploying with Sanity
