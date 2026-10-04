---
name: ssg
description: Static Site Generation for fast, pre-rendered web pages
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: web-development
---
## What I do
- Generate static HTML at build time
- Use getStaticProps
- Implement getStaticPaths
- Create dynamic static pages

## When to use me
When building fast, cacheable websites with dynamic content.

## Next.js SSG
```javascript
// pages/posts/[id].js
export async function getStaticPaths() {
  const posts = await fetchPosts();
  return {
    paths: posts.map(p => ({ params: { id: p.id } })),
    fallback: false
  };
}

export async function getStaticProps({ params }) {
  const post = await fetchPost(params.id);
  return { props: { post } };
}

export default function Post({ post }) {
  return <article><h1>{post.title}</h1></article>;
}
```
