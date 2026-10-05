---
name: gatsby
description: Gatsby legacy framework skill covering GraphQL data layer, source plugins, image optimization, and migration paths. Use when maintaining or migrating Gatsby sites.
---

## gatsby

Static site generator with React. GraphQL data layer unifies all content sources at build time.

### Core Concepts
- GraphQL data layer: pull from any source, query at build time, shape per page
- Source plugins: gatsby-source-filesystem for local, gatsby-source-wordpress for CMS
- createPages API: gatsby-node.js programmatic page generation from queried nodes
- Schema customization: define types explicitly for content meshing across sources

### Queries & Pages
- Page queries in page components only, useStaticQuery in non-page components
- File system routes: src/pages/ for automatic route creation like Next.js pages/
- Template pages: createPages with template component and query context variables
- gatsby-plugin-image: StaticImage and GatsbyImage for optimized responsive images

### Best Practices
- useStaticQuery for shared data like site metadata, nav, and footer
- Prefer gatsby-plugin-image over raw img tags for automatic format/size optimization
- Keep gatsby-node.js lean, delegate logic to separate helper modules
- For new projects, choose Next.js or Astro instead of Gatsby

### Common Code Patterns
- createPages loops over GraphQL results, calls createPage per node with slug context
- StaticQuery hook in layout component for site title and SEO defaults
